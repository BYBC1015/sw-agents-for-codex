"""Local canvas state. No model calls, uploads, or source-media writes."""
from __future__ import annotations
import copy
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import subprocess
import threading
import uuid
from datetime import datetime, timezone
from bridge import ContextBridge, normalize, resolve_task, bounded_text
from project_flow import ProjectFlow
from layout import place, apply_layout
from storyboard import StoryboardFlow
from settings import DEFAULT_DATA, ALLOWED_ROOTS, FFMPEG, FFPROBE

APP_ROOT = Path(__file__).resolve().parent
MEDIA_EXTS = {'.mp4', '.mov', '.mkv', '.webm', '.jpg', '.jpeg', '.png', '.webp'}
MEDIA_LOCK = threading.Lock()

def now():
    return datetime.now(timezone.utc).isoformat()

def uid(prefix):
    return prefix + '_' + uuid.uuid4().hex[:16]

def valid_path(value):
    p = Path(value).resolve(strict=True)
    if not any(p.is_relative_to(root) for root in ALLOWED_ROOTS):
        raise ValueError('素材须位于已配置的素材目录内；其他文件可使用 copy 导入')
    if not p.is_file() or p.suffix.lower() not in MEDIA_EXTS:
        raise ValueError('请选择支持的图片或视频文件')
    return p

def run_media(args, timeout=120):
    result = subprocess.run([str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-nostdin', *args],
                            capture_output=True, timeout=timeout, creationflags=0x08000000 if os.name == 'nt' else 0)
    if result.returncode:
        raise ValueError('预览生成失败：' + result.stderr.decode('utf-8', errors='replace')[-600:])

class Store(ContextBridge, ProjectFlow, StoryboardFlow):
    def __init__(self, data_dir=DEFAULT_DATA):
        self.root = Path(data_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.cache = self.root / 'cache'
        self.cache.mkdir(exist_ok=True)
        self.db = self.root / 'project.sqlite3'
        with self.connect() as con:
            con.execute('PRAGMA journal_mode=WAL')
            con.execute('CREATE TABLE IF NOT EXISTS project (id INTEGER PRIMARY KEY, revision INTEGER NOT NULL, payload TEXT NOT NULL)')
            con.execute('CREATE TABLE IF NOT EXISTS handoffs (id TEXT PRIMARY KEY, request TEXT UNIQUE, title TEXT, revision INTEGER, created TEXT, payload TEXT)')
            initial = dict(projectId='P'+uuid.uuid4().hex[:8].upper(), schemaVersion=2,
                name='未命名画布项目', goal='', decisions='', nextStep='', notes=[],
                constraints=['保持原片与旧版本', '仅本地制作，不上传'],
                assets=[], nodes=[], edges=[], annotations=[], tasks=[], camera=dict(x=35,y=45,zoom=1), selected=[])
            con.execute('INSERT OR IGNORE INTO project VALUES (1,0,?)', (json.dumps(initial, ensure_ascii=False),))

    @contextmanager
    def connect(self):
        con=sqlite3.connect(self.db, timeout=15)
        try:
            with con:yield con
        finally:con.close()

    def read(self):
        with self.connect() as con:
            rev, payload = con.execute('SELECT revision,payload FROM project WHERE id=1').fetchone()
        data = json.loads(payload)
        data['revision'] = rev
        return normalize(data, self.root)

    def change(self, action):
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            rev, payload = con.execute('SELECT revision,payload FROM project WHERE id=1').fetchone()
            state = normalize(json.loads(payload), self.root)
            state['revision'] = rev
            result = action(state)
            state.pop('revision', None)
            con.execute('UPDATE project SET revision=?,payload=? WHERE id=1', (rev+1,json.dumps(state,ensure_ascii=False)))
        return result

    def prepare_asset(self, path, title=None, status='已导入', group='素材'):
        p = valid_path(path)
        stat = p.stat()
        asset_id = 'a_' + hashlib.sha256(f'{p}|{stat.st_size}|{stat.st_mtime_ns}'.encode()).hexdigest()[:20]
        directory = self.cache / asset_id
        directory.mkdir(exist_ok=True)
        manifest = directory / 'asset.json'
        with MEDIA_LOCK:
            if manifest.exists():
                asset = json.loads(manifest.read_text(encoding='utf-8'))
            else:
                is_image = p.suffix.lower() in {'.jpg','.jpeg','.png','.webp'}
                asset = dict(id=asset_id,path=str(p),fileName=p.name,bytes=stat.st_size,mtimeNs=stat.st_mtime_ns,
                             kind='image' if is_image else 'video',createdAt=now())
                if is_image:
                    from PIL import Image, ImageOps
                    with Image.open(p) as original:
                        im = ImageOps.exif_transpose(original).convert('RGB')
                        asset.update(width=im.width,height=im.height,fps=None,frames=1,duration=0)
                        im.thumbnail((1600,1600)); im.save(directory/'preview.jpg',quality=90)
                        im.thumbnail((480,320)); im.save(directory/'thumb.jpg',quality=82)
                else:
                    probe = json.loads(subprocess.check_output([str(FFPROBE),'-v','error','-show_streams','-show_format','-of','json',str(p)],timeout=30))
                    video = next(s for s in probe['streams'] if s['codec_type']=='video')
                    num,den = video.get('avg_frame_rate','0/1').split('/')
                    fps=float(num)/float(den) if float(den) else 25
                    duration=float(video.get('duration') or probe['format'].get('duration') or 0)
                    asset.update(width=video['width'],height=video['height'],fps=fps or 25,
                                 frames=int(video.get('nb_frames') or round(duration*(fps or 25))),duration=duration)
                    # ProRes and 4K masters stay untouched. Browser playback uses a small proxy.
                    preview = directory/'preview.mp4'
                    if not preview.exists():
                        partial = directory/'preview.part.mp4'
                        run_media(['-y','-i',str(p),'-map','0:v:0','-map','0:a:0?',
                            '-vf','scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2',
                            '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',
                            '-c:a','aac','-b:a','160k','-movflags','+faststart',str(partial)],timeout=600)
                        os.replace(partial,preview)
                    run_media(['-y','-ss',str(min(1.5,duration/2)),'-i',str(preview),'-frames:v','1',
                               '-vf','scale=480:-2','-q:v','3',str(directory/'thumb.jpg')])
                temp = manifest.with_suffix('.tmp')
                temp.write_text(json.dumps(asset,ensure_ascii=False),encoding='utf-8')
                os.replace(temp,manifest)
        asset = copy.deepcopy(asset)
        asset.update(title=title or p.stem,status=status,group=group)
        return asset

    def import_asset(self, path, title=None, status='已导入', group='素材', position=None, parent=None, task_ref=None):
        if task_ref and resolve_task(self.read(), task_ref)['status'] not in ('running', 'review'):
            raise ValueError('只有处理中或待确认任务可以登记输出')
        asset = self.prepare_asset(path,title,status,group)
        return self.change(lambda s:self.attach_asset(s,asset,position,parent,task_ref))

    def attach_asset(self,s,asset,position=None,parent=None,task_ref=None):
        if parent and not any(n['id']==parent and n['kind']=='asset' for n in s['nodes']):
            raise ValueError('来源素材节点不存在于此项目')
        def add(s):
            task = resolve_task(s, task_ref) if task_ref else None
            if task and task['intent']=='discuss':raise ValueError('讨论任务不能登记制作输出')
            if task and task['status'] not in ('running', 'review'):
                raise ValueError('任务状态已变化，未登记输出')
            existing = next((a for a in s['assets'] if a['id']==asset['id']),None)
            if existing:
                node=next(n for n in s['nodes'] if n.get('assetId')==asset['id'])
            else:
                source_node=next((n for n in s['nodes'] if n['id']==parent),None)
                source=next((a for a in s['assets'] if source_node and a['id']==source_node.get('assetId')),None)
                asset['lineage']=source.get('lineage',source['id']) if source else asset['id']
                asset['version']=1+max((a.get('version',1) for a in s['assets'] if a.get('lineage',a['id'])==asset['lineage']),default=0)
                s['assets'].append(asset)
                anchor=next((n for n in s['nodes'] if task and n.get('taskId')==task['id']),None) or source_node
                node=dict(id=uid('node'),kind='asset',assetId=asset['id'])
                preferred=position or dict(x=anchor['x']+330 if anchor else 40,y=anchor['y'] if anchor else 40)
                node.update(place(s['nodes'],node,**preferred))
                s['nodes'].append(node)
            if parent and any(x['id']==parent for x in s['nodes']):
                if parent != node['id'] and not any(e['source']==parent and e['target']==node['id'] for e in s['edges']):
                    s['edges'].append(dict(id=uid('edge'),source=parent,target=node['id'],label='新版本'))
            if task and asset['id'] not in task['outputAssetIds']:
                task['outputAssetIds'].append(asset['id'])
                task_node=next(n for n in s['nodes'] if n.get('taskId')==task['id'])
                s['edges'].append(dict(id=uid('edge'),source=task_node['id'],target=node['id'],label='任务输出'))
            return existing or asset
        return add(s)

    def patch_board(self, body):
        def action(s):
            ids={n['id'] for n in s['nodes']}
            for n in s['nodes']:
                p=body.get('positions',{}).get(n['id'])
                if p:
                    for key in ('x','y'):
                        v=p.get(key)
                        if not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>100000:
                            raise ValueError('无效节点坐标')
                        n[key]=v
            if 'camera' in body:
                c=body['camera']
                if not all(isinstance(c.get(k),(int,float)) and math.isfinite(c[k]) for k in ('x','y','zoom')):
                    raise ValueError('无效画布位置')
                s['camera']=dict(x=max(-100000,min(100000,c['x'])),y=max(-100000,min(100000,c['y'])),zoom=max(.25,min(2,c['zoom'])))
            if 'selected' in body:
                s['selected']=[x for x in body['selected'] if x in ids][:100]
            e=body.get('edge')
            if e:
                if e.get('source') not in ids or e.get('target') not in ids or e['source']==e['target']:
                    raise ValueError('请选择两个不同的有效节点')
                if not any(x['source']==e['source'] and x['target']==e['target'] for x in s['edges']):
                    s['edges'].append(dict(id=uid('edge'),source=e['source'],target=e['target'],label='参考'))
            if body.get('removeEdge'):
                s['edges']=[e for e in s['edges'] if e['id']!=body['removeEdge']]
            return {'saved':True}
        return self.change(action)

    def annotate(self, body):
        def action(s):
            asset=next((a for a in s['assets'] if a['id']==body.get('assetId')),None)
            if not asset: raise ValueError('素材不存在')
            text=str(body.get('text','')).strip()[:2000]
            if not text: raise ValueError('请填写标注意见')
            frame=body.get('frame',0)
            if not isinstance(frame,int) or not 0<=frame<max(1,asset['frames']): raise ValueError('帧号超出范围')
            rect=body.get('rect')
            if rect is not None:
                if not isinstance(rect,list) or len(rect)!=4 or not all(isinstance(v,(float,int)) and math.isfinite(v) and 0<=v<=1 for v in rect):
                    raise ValueError('无效标注区域')
                if rect[2]<=0 or rect[3]<=0 or rect[0]+rect[2]>1.001 or rect[1]+rect[3]>1.001: raise ValueError('无效标注区域')
            note=dict(id=uid('note'),assetId=asset['id'],frame=frame,rect=rect,text=text,createdAt=now())
            s['annotations'].append(note)
            return note
        return self.change(action)

    def create_task(self, body):
        def action(s):
            request_id=str(body.get('requestId',''))
            if not request_id or len(request_id)>100: raise ValueError('请求编号无效')
            old=next((t for t in s['tasks'] if t['requestId']==request_id),None)
            if old:
                if (old['text'],old['frameRange'],old['intent'],{n['id'] for n in old['input']['nodes']}) != (
                    str(body.get('text','')).strip(),str(body.get('frameRange','')),body.get('intent','execute'),set(body.get('nodeIds',[]))):
                    raise ValueError('请求编号已用于不同内容，请先检查已有任务')
                return old
            text=bounded_text(body.get('text',''), '任务说明', 8000, True)
            if not text: raise ValueError('请填写任务说明')
            intent=body.get('intent','execute')
            if intent not in ('discuss','execute'):raise ValueError('任务用途不正确')
            frames=bounded_text(body.get('frameRange',''), '帧范围', 100)
            snapshot=self.snapshot(s,body.get('nodeIds',[]),frames)
            nodes=[n for n in s['nodes'] if n['id'] in {v['id'] for v in snapshot['nodes']}]
            task=dict(id=uid('task'),ref=f'T{len(s["tasks"])+1:03}',intent=intent,outputAssetIds=[],
                requestId=request_id,text=text,frameRange=frames,
                status='queued',createdAt=now(),updatedAt=now(),input=snapshot)
            s['tasks'].append(task)
            task_node=dict(id=uid('node'),kind='task',taskId=task['id'])
            task_node.update(place(s['nodes'],task_node,max(n['x'] for n in nodes)+330,min(n['y'] for n in nodes)))
            s['nodes'].append(task_node)
            for n in nodes:s['edges'].append(dict(id=uid('edge'),source=n['id'],target=task_node['id'],label='任务输入'))
            return task
        return self.change(action)

    def update_task(self, task_id, status, result=None):
        return self.change(lambda s:self.transition_task(s,task_id,status,result))

    def layout(self,body):
        return self.change(lambda s:apply_layout(s,body))

    def transition_task(self, s, task_id, status, result=None):
        allowed={'queued':{'running','cancelled'},'running':{'review','failed','queued'},'review':{'done','running'},'failed':{'queued'},'done':set(),'cancelled':set()}
        def action(s):
            t=resolve_task(s,task_id)
            if status not in allowed[t['status']]: raise ValueError('不允许的任务状态转换')
            t['status']=status;t['updatedAt']=now()
            if status=='done':
                for a in s['assets']:
                    if a['id'] in t.get('outputAssetIds',[]):a['status']='已确认'
            if result is not None:
                t['result']=str(result)[:50000]
                old=next((n for n in s['nodes'] if n.get('resultTaskId')==t['id']),None)
                if not old:
                    parent=next(n for n in s['nodes'] if n.get('taskId')==t['id'])
                    outputs=[n for n in s['nodes'] if n.get('assetId') in t.get('outputAssetIds',[])]
                    old=dict(id=uid('node'),kind='result',resultTaskId=t['id'])
                    old.update(place(s['nodes'],old,max(n['x'] for n in outputs or [parent])+330,parent['y']))
                    s['nodes'].append(old)
                    s['edges'].append(dict(id=uid('edge'),source=parent['id'],target=old['id'],label='执行结果'))
            return t
        return action(s)

    def context(self, task_id=None):
        s=self.read()
        if task_id:
            return resolve_task(s,task_id)
        selected={n['assetId'] for n in s['nodes'] if n['id'] in s['selected'] and n['kind']=='asset'}
        return dict(project=s['name'],constraints=s['constraints'],revision=s['revision'],
                    nodes=[dict(id=n['id'],assetId=n['assetId']) for n in s['nodes'] if n['id'] in s['selected'] and n['kind']=='asset'],
                    assets=[a for a in s['assets'] if a['id'] in selected],
                    annotations=[a for a in s['annotations'] if a['assetId'] in selected],
                    queuedTasks=[dict(id=t['id'],text=t['text'],frameRange=t['frameRange'],status=t['status']) for t in s['tasks'] if t['status']=='queued'])

    def frame_file(self, asset, frame):
        if not isinstance(frame,int) or not 0<=frame<max(1,asset['frames']):raise ValueError('帧号超出范围')
        p=valid_path(asset['path'])
        stat=p.stat()
        if stat.st_size!=asset['bytes'] or stat.st_mtime_ns!=asset['mtimeNs']:
            raise ValueError('原文件已变化，请重新导入此版本')
        if asset['kind']=='image':return self.cache/asset['id']/'preview.jpg'
        output=self.cache/asset['id']/f'frame-{frame:07}.jpg'
        with MEDIA_LOCK:
            if not output.exists():
                # Frame-index selection from the original, not time-seeking a proxy.
                run_media(['-y','-i',str(p),'-vf',f'select=eq(n\\,{frame}),scale=1920:-2',
                           '-frames:v','1','-q:v','2',str(output)])
        return output
