"""Project-wide handoffs and retry-safe import/result transactions."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
from bridge import bounded_text, normalize, page, resolve_task, task_summary


class ProjectFlow:
    def summary(self, since=None):
        """Small default context; explicit handoff retains all project information."""
        s = self.read(); key = s['projectId']+':'+str(s['revision'])
        result = dict(projectId=s['projectId'], revision=s['revision'], cursor=key)
        if since == key: return dict(result, unchanged=True)
        clipped = []
        def short(name, text, limit):
            if len(text)>limit: clipped.append(name)
            return text[:limit]
        result.update(name=s['name'], goal=short('goal',s.get('goal',''),240),
            nextStep=short('nextStep',s.get('nextStep',''),240),
            stage=short('stage',s.get('progress',{}).get('stage',''),80),
            counts={k:len(s[k]) for k in ('assets','notes','tasks')}, imagesIncluded=False)
        active=[t for t in s['tasks'] if t['status'] not in ('done','cancelled')]
        result['activeTasks']=dict(total=len(active),items=[dict(ref=t['ref'],status=t['status']) for t in active[-3:]])
        result['truncatedFields']=clipped
        from storyboard import board, issues
        shots=board(s)['shots']
        result['storyboard']=dict(shots=len(shots),entities=len(board(s)['entities']),needsReview=sum(bool(issues(s,shot)) for shot in shots))
        return result

    def paths(self, state=None):
        state = state or self.read()
        root = Path(state.get('workspaceRoot') or (self.root.parent if self.root.name=='.canvas' else self.root)).resolve()
        return dict(workspace=str(root),process=str(root/'过程'),delivery=str(root/'交付'),dataDir=str(self.root))

    def project_handoff(self, section='summary', offset=0, limit=12, checkpoint=None):
        current = self.read(); s = current; captured = None
        if checkpoint:
            with self.connect() as con:
                row = con.execute('SELECT payload,created FROM handoffs WHERE id=?',(checkpoint,)).fetchone()
            if not row: raise ValueError('交接快照不存在')
            s = normalize(json.loads(row[0]), self.root); captured = row[1]
        if section != 'summary':
            if section not in ('assets','nodes','edges','annotations','notes','tasks','versions','shots','entities'):
                raise ValueError('不支持的交接章节')
            items = s.get('versionChoices',[]) if section=='versions' else (s['storyboard'][section] if section in ('shots','entities') else s[section])
            return dict(projectId=s['projectId'],checkpoint=checkpoint,revision=s['revision'],section=section,**page(items,offset,limit))
        choices = []
        for choice in s.get('versionChoices',[]):
            asset = next((a for a in s['assets'] if a['id']==choice['assetId']),None)
            choices.append(dict(choice,title=asset['title'] if asset else '缺失素材',version=asset.get('version') if asset else None))
        counts = {key:len(s[key]) for key in ('assets','nodes','edges','annotations','notes','tasks')}
        task_counts = {key:sum(t['status']==key for t in s['tasks']) for key in ('queued','running','review','done','failed','cancelled')}
        return dict(project=self.project_info(s),revision=s['revision'],currentRevision=current['revision'],
            checkpoint=checkpoint,capturedAt=captured,imagesIncluded=False,paths=self.paths(s),
            progress=s.get('progress',{}),versionChoices=page(choices,offset,limit),counts=counts,taskCounts=task_counts,
            tasks=page([task_summary(t) for t in reversed(s['tasks'])],offset,limit),
            notes=page([dict(id=n['id'],title=n['title'],excerpt=n['text'][:240]) for n in s['notes']],offset,limit),
            sections=['assets','nodes','edges','annotations','notes','tasks','versions','shots','entities'],
            resumeRule='先核对项目、已选版本与进行中/待确认任务。交接不授权执行队列；不可重复生成已有结果。')

    def checkpoint(self, body):
        from store import now, uid
        request = bounded_text(body.get('requestId'),'请求编号',100,True)
        title = bounded_text(body.get('title','项目交接'),'交接标题',120,True)
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            old=con.execute('SELECT id,title,revision,created FROM handoffs WHERE request=?',(request,)).fetchone()
            if old:
                if old[1]!=title: raise ValueError('交接请求编号已用于不同标题')
                return dict(id=old[0],title=old[1],revision=old[2],createdAt=old[3])
            revision,payload=con.execute('SELECT revision,payload FROM project WHERE id=1').fetchone()
            if body.get('expectedRevision')!=revision: raise ValueError('项目已变化，请重新读取后交接')
            s=normalize(json.loads(payload),self.root);s['revision']=revision
            key,created=uid('handoff'),now()
            con.execute('INSERT INTO handoffs VALUES (?,?,?,?,?,?)',(key,request,title,revision,created,json.dumps(s,ensure_ascii=False)))
        return dict(id=key,title=title,revision=revision,createdAt=created)

    def checkpoints(self, offset=0, limit=12):
        with self.connect() as con:
            rows=con.execute('SELECT id,title,revision,created FROM handoffs ORDER BY created DESC').fetchall()
        return page([dict(id=r[0],title=r[1],revision=r[2],createdAt=r[3]) for r in rows],offset,limit)

    def choose_version(self, body):
        from store import now
        status=body.get('disposition')
        if status not in ('candidate','selected','rejected','delivered'): raise ValueError('版本取舍不正确')
        reason=bounded_text(body.get('reason',''),'版本依据',2000)
        def update(s):
            if body.get('expectedRevision')!=s['revision']: raise ValueError('项目已变化，请重新读取版本')
            a=next((a for a in s['assets'] if a['id']==body.get('assetId')),None)
            if not a: raise ValueError('素材不属于此项目')
            choice=dict(assetId=a['id'],disposition=status,reason=reason,updatedAt=now())
            s['versionChoices']=[v for v in s.get('versionChoices',[]) if v['assetId']!=a['id']]+[choice]
            a['disposition']=status
            return choice
        return self.change(update)

    def _prepare_imports(self, entries):
        from store import MEDIA_EXTS, valid_path
        if not isinstance(entries,list) or len(entries)>30: raise ValueError('单次最多30项素材')
        prepared=[]
        for entry in entries:
            if not isinstance(entry,dict): raise ValueError('素材条目须为对象')
            path=Path(entry['path']).resolve(strict=True)
            if not path.is_file() or path.suffix.lower() not in MEDIA_EXTS: raise ValueError('请选择支持的图片或视频')
            mode=entry.get('mode','reference')
            if mode=='copy':
                directory=Path(self.paths()['process'])/'导入素材';directory.mkdir(parents=True,exist_ok=True)
                # Content addressing makes retry copies stable and never overwrites an existing file.
                digest=hashlib.sha256()
                with path.open('rb') as f:
                    for block in iter(lambda:f.read(1024*1024),b''): digest.update(block)
                dest=directory/(digest.hexdigest()+path.suffix.lower())
                if not dest.exists():
                    from store import uid
                    temp=directory/(uid('import')+'.tmp')
                    shutil.copy2(path,temp)
                    check=hashlib.sha256()
                    with temp.open('rb') as f:
                        for block in iter(lambda:f.read(1024*1024),b''):check.update(block)
                    if check.hexdigest()!=digest.hexdigest():
                        temp.unlink();raise ValueError('复制时原件发生变化，请重试')
                    # Hard-link publishes without replacing an already published retry copy.
                    try: dest.hardlink_to(temp)
                    except FileExistsError: pass
                    finally: temp.unlink()
                path=dest
            elif mode!='reference': raise ValueError('导入方式须为 reference 或 copy')
            else: valid_path(path)
            a=self.prepare_asset(path,entry.get('title') or Path(entry['path']).stem)
            a['sourcePath']=str(Path(entry['path']).resolve())
            prepared.append((a,entry.get('parentNode')))
        return prepared

    def _operation(self, kind, body, action):
        request=bounded_text(body.get('requestId'),'请求编号',100,True)
        signature=json.dumps(body,sort_keys=True,ensure_ascii=False)
        def run(s):
            receipt=next((r for r in s.get('operationReceipts',[]) if r['requestId']==request),None)
            if receipt:
                if receipt['kind']!=kind or receipt['signature']!=signature: raise ValueError('请求编号已用于不同内容')
                return receipt['result']
            result=action(s)
            s.setdefault('operationReceipts',[]).append(dict(requestId=request,kind=kind,signature=signature,result=result))
            return result
        return self.change(run)

    def _receipt(self, kind, body):
        # Resolve successful retries before checking files: sources may have moved after commit.
        for r in self.read().get('operationReceipts',[]):
            if r['requestId']==body.get('requestId'):
                if r['kind']!=kind or r['signature']!=json.dumps(body,sort_keys=True,ensure_ascii=False): raise ValueError('请求编号已用于不同内容')
                return r['result']

    def ingest(self, body):
        old=self._receipt('ingest',body)
        if old is not None:return old
        prepared=self._prepare_imports(body.get('files'))
        if not prepared: raise ValueError('请提供素材')
        def add(s):
            result=[]
            for a,parent in prepared:
                attached=self.attach_asset(s,a,parent=parent)
                result.append(dict(assetId=attached['id'],title=attached['title'],version=attached.get('version'),
                    nodeId=next(n['id'] for n in s['nodes'] if n.get('assetId')==a['id'])))
            return dict(projectId=s['projectId'],assets=result)
        return self._operation('ingest',body,add)

    def publish_result(self, body):
        old=self._receipt('result',body)
        if old is not None:return old
        text=bounded_text(body.get('text'),'结果说明',50000,True)
        task=resolve_task(self.read(),body.get('task'))
        if task['status']!='running':raise ValueError('先认领指定任务，再回写结果')
        if task['intent']=='discuss' and body.get('files'):raise ValueError('讨论任务不能登记制作输出')
        prepared=self._prepare_imports(body.get('files',[]))
        def complete(s):
            t=resolve_task(s,body.get('task'))
            if t['status']!='running':raise ValueError('任务状态已变化，未回写')
            for a,parent in prepared:
                a.update(status='待用户确认',group='制作结果')
                self.attach_asset(s,a,parent=parent,task_ref=t['id'])
            self.transition_task(s,t['id'],'review',text)
            return dict(projectId=s['projectId'],task=task_summary(t),outputAssetIds=t['outputAssetIds'])
        return self._operation('result',body,complete)
