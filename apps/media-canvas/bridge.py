"""Small, paged context packets shared by HTTP, CLI and page tools."""
import copy
import hashlib
import re
from pathlib import Path


def normalize(state, root):
    # Legacy projects gain stable identities in memory; reading does not migrate the DB.
    state.setdefault('projectId', 'P' + hashlib.sha256(str(root).encode()).hexdigest()[:8].upper())
    state.setdefault('schemaVersion', 2)
    state.setdefault('goal', '')
    state.setdefault('decisions', '')
    state.setdefault('nextStep', '')
    state.setdefault('notes', [])
    state.setdefault('progress', {'stage':'', 'blockers':'', 'openQuestions':'', 'deliveryNotes':''})
    state.setdefault('versionChoices', [])
    state.setdefault('storyboard', {'entities': [], 'shots': []})
    for index, task in enumerate(state['tasks'], 1):
        task.setdefault('ref', f'T{index:03}')
        task.setdefault('intent', 'execute')
        task.setdefault('outputAssetIds', [])
    return state


def resolve_task(state, reference):
    task = next((t for t in state['tasks'] if reference in (t['id'], t['ref'])), None)
    if task is None:
        raise ValueError('任务不存在，请核对项目和任务编号')
    return task


def page(items, offset=0, limit=12):
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError('分页要求 offset >= 0，limit 为 1–20')
    end = min(len(items), offset + limit)
    return dict(items=items[offset:end], total=len(items), nextOffset=end if end < len(items) else None)


def frame_window(value):
    match = re.fullmatch(r'\s*[Ff]?(\d+)\s*(?:[-–—~至]\s*[Ff]?(\d+))?\s*', value)
    if not match:
        return None
    start, end = int(match[1]), int(match[2] or match[1])
    if start > end:
        raise ValueError('帧范围起点不能大于终点')
    return [start, end]


def task_summary(task):
    return {k: task.get(k) for k in ('id', 'ref', 'intent', 'status', 'frameRange', 'createdAt', 'updatedAt')} | {
        'text': task['text'][:240], 'outputAssetIds': task.get('outputAssetIds', [])}


def bounded_text(value, name, maximum, required=False):
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(f'{name}须为{maximum}字以内的' + ('非空文字' if required else '文字'))
    return value.strip()


class ContextBridge:
    def check_project(self, expected):
        if expected and expected != self.read()['projectId']:
            raise ValueError('项目编号不匹配，未执行操作')

    def project_info(self, state=None):
        state = state or self.read()
        return {k: state[k] for k in ('projectId', 'name', 'goal', 'decisions', 'nextStep', 'constraints')}

    def update_project(self, body):
        def update(state):
            if body.get('expectedRevision') != state['revision']:
                raise ValueError('项目已变化，请重新读取后保存')
            for key, size in [('name', 120), ('goal', 1000), ('decisions', 3000), ('nextStep', 1000)]:
                if key in body:
                    state[key] = bounded_text(body[key], key, size, key == 'name')
            if 'constraints' in body:
                values = body['constraints']
                if not isinstance(values, list) or len(values) > 20:
                    raise ValueError('项目约束最多20条')
                state['constraints'] = [bounded_text(v, '约束', 300, True) for v in values]
            if 'progress' in body:
                if not isinstance(body['progress'],dict):raise ValueError('进度须为对象')
                for key in ('stage','blockers','openQuestions','deliveryNotes'):
                    if key in body['progress']:state['progress'][key]=bounded_text(body['progress'][key],key,2000)
            return self.project_info(state)
        return self.change(update)

    def snapshot(self, state, node_ids, frames=''):
        if not isinstance(node_ids, list) or not 1 <= len(node_ids) <= 100 or not all(isinstance(n, str) for n in node_ids):
            raise ValueError('请选择1–100个素材或文字节点')
        chosen = set(node_ids)
        nodes = [n for n in state['nodes'] if n['id'] in chosen and n['kind'] in ('asset', 'note')]
        if len(nodes) != len(chosen):
            raise ValueError('所选对象已不存在，或不是素材/文字节点')
        asset_ids = {n['assetId'] for n in nodes if n['kind'] == 'asset'}
        note_ids = {n['noteId'] for n in nodes if n['kind'] == 'note'}
        assets = [a for a in state['assets'] if a['id'] in asset_ids]
        window = frame_window(frames) if frames else None
        if window and any(window[1] >= a['frames'] for a in assets if a['kind'] == 'video'):
            raise ValueError('帧范围超出所选视频，请分开创建任务或调整范围')
        kinds = {a['id']: a['kind'] for a in assets}
        annotations = [a for a in state['annotations'] if a['assetId'] in asset_ids and (
            window is None or kinds[a['assetId']] == 'image' or window[0] <= a['frame'] <= window[1])]
        return copy.deepcopy(dict(project=state['name'], projectInfo=self.project_info(state),
            revision=state['revision'], constraints=state['constraints'],
            nodes=[{k: n[k] for k in ('id', 'assetId', 'noteId') if k in n} for n in nodes],
            projectId=state['projectId'], assets=assets, notes=[n for n in state['notes'] if n['id'] in note_ids],
            annotations=annotations, frameWindow=window))

    def add_note(self, body):
        from store import uid, now
        title = bounded_text(body.get('title', ''), '标题', 120, True)
        content = bounded_text(body.get('text', ''), '内容', 12000, True)
        request_id = bounded_text(body.get('requestId', ''), '请求编号', 100, True)
        def add(state):
            existing = next((n for n in state['notes'] if n.get('requestId') == request_id), None)
            if existing:
                if (existing['title'], existing['text']) != (title, content):
                    raise ValueError('请求编号已用于不同内容')
                return existing
            parents = body.get('nodeIds', [])
            if not isinstance(parents, list) or len(parents) > 100 or not all(isinstance(n, str) for n in parents):
                raise ValueError('关联节点不正确')
            ids = {n['id'] for n in state['nodes']}
            if not set(parents).issubset(ids):
                raise ValueError('关联节点不存在')
            note = dict(id=uid('note'), title=title, text=content, requestId=request_id, createdAt=now())
            from layout import place
            anchors=[n for n in state['nodes'] if n['id'] in parents]
            node = dict(id=uid('node'), kind='note', noteId=note['id'])
            node.update(place(state['nodes'],node,max(n['x'] for n in anchors)+330 if anchors else 40,min(n['y'] for n in anchors) if anchors else 40))
            note['nodeId'] = node['id']
            state['notes'].append(note)
            state['nodes'].append(node)
            for parent in set(parents):
                state['edges'].append(dict(id=uid('edge'), source=parent, target=node['id'], label='方案/结论'))
            return note
        return self.change(add)

    def _scope(self, state, reference=None, node_ids=None):
        if reference:
            task = resolve_task(state, reference)
            return task['input'], task
        ids = state['selected'] if node_ids is None else node_ids
        # Current selection may contain task/result cards. Read their summary separately.
        if not isinstance(ids, list) or not all(isinstance(n, str) for n in ids) or len(ids) > 100:
            raise ValueError('所选节点列表不正确')
        selected_nodes = [n for n in state['nodes'] if n['id'] in ids]
        if len(selected_nodes) == 1 and selected_nodes[0]['kind'] in ('task', 'result'):
            node = selected_nodes[0]
            task = resolve_task(state, node.get('taskId') or node['resultTaskId'])
            return task['input'], task
        valid = [n['id'] for n in state['nodes'] if n['id'] in ids and n['kind'] in ('asset', 'note')]
        if valid:
            return self.snapshot(state, valid), None
        return dict(nodes=[], assets=[], notes=[], annotations=[]), None

    def packet(self, reference=None, node_ids=None, offset=0, limit=12):
        state = self.read()
        scope, task = self._scope(state, reference, node_ids)
        assets = [{k: a.get(k) for k in ('id', 'title', 'kind', 'width', 'height', 'frames', 'status','version','lineage','disposition')} for a in scope['assets']]
        notes = [dict(id=n['id'], title=n['title'], excerpt=n['text'][:240]) for n in scope.get('notes', [])]
        annotations = [{k: a.get(k) for k in ('id', 'assetId', 'frame', 'rect')} | {'excerpt': a['text'][:240]} for a in scope['annotations']]
        packet = dict(project=self.project_info(state), revision=state['revision'],
            source='frozen-task' if task else 'live-selection', imagesIncluded=False,
            nodes=page(scope['nodes'], offset, limit), assets=page(assets, offset, limit),
            notes=page(notes, offset, limit), annotations=page(annotations, offset, limit),
            readMore='detail: assets / annotations / notes / result；分页 nextOffset；视觉检查按需读取帧')
        if task:
            packet['task'] = task_summary(task) | {'text': task['text']}
            packet['inputProject'] = scope.get('projectInfo', {'name': scope['project'], 'constraints': scope['constraints']})
            packet['frameWindow'] = scope.get('frameWindow')
            packet['result'] = dict(excerpt=task.get('result', '')[:400], available=bool(task.get('result')))
        else:
            active = [task_summary(t) for t in reversed(state['tasks']) if t['status'] not in ('done', 'cancelled')]
            packet['tasks'] = page(active, offset, limit)
        return packet

    def detail(self, kind, reference=None, node_ids=None, offset=0, limit=12):
        state = self.read()
        scope, task = self._scope(state, reference, node_ids)
        if kind == 'result':
            if task is None:
                raise ValueError('读取结果需要任务编号')
            return dict(task=task_summary(task), text=task.get('result', ''),
                assets=[a for a in state['assets'] if a['id'] in task.get('outputAssetIds', [])])
        if kind not in ('assets', 'annotations', 'notes'):
            raise ValueError('不支持的详情类型')
        return page(scope.get(kind, []), offset, limit)

    def list_tasks(self, offset=0, limit=12):
        return page([task_summary(t) for t in reversed(self.read()['tasks'])], offset, limit)

    def handoff(self, reference=None, url=None, checkpoint=None):
        state = self.read()
        if checkpoint:self.project_handoff(checkpoint=checkpoint)
        task = resolve_task(state, reference) if reference else None
        cli = Path(__file__).resolve().with_name('canvas_cli.py')
        command = f'canvas_cli.py --data-dir "{self.root}" --project {state["projectId"]} packet'
        if task:
            command += ' --task ' + task['ref']
        else:
            command=command.removesuffix('packet')+'project-handoff'
            if checkpoint:command+=' --checkpoint '+checkpoint
        intent = '只讨论，不执行制作任务' if not task or task['intent'] == 'discuss' else '读取后处理指定任务'
        if task and task['status'] in ('done', 'cancelled'):
            intent = '只读取记录与结果，不重新执行'
        elif task and task['status'] == 'review':
            intent = '读取任务与待确认结果；后续修改以我本次要求为准'
        text = f'接续本地画布 {state["projectId"]}' + (f' / {task["ref"]}' if task else '')
        text += f'：{intent}。\nCLI：{cli}\n读取命令：{command}\n先读简短任务包；图片、帧和历史按需读取，结果回写画布。'
        if not task:
            text += '\n这是完整项目交接。先读目标、已确认决定、版本取舍、任务状态和下一步，再按章节读取必要详情；使用实际对话编号建立项目绑定。不要自动执行队列。'
        if url:
            text += '\n画布：' + url
        return dict(text=text, projectId=state['projectId'], taskRef=task['ref'] if task else None,checkpoint=checkpoint)

    def asset_frame(self, asset_id, frame, reference=None):
        state = self.read()
        source = resolve_task(state, reference)['input']['assets'] if reference else state['assets']
        asset = next((a for a in source if a['id'] == asset_id), None)
        if asset is None:
            raise ValueError('素材不属于当前项目或指定任务')
        path = self.frame_file(asset, frame)
        return dict(assetId=asset_id, frame=frame, path=str(path), viewed=False,
            note='仅定位/准备文件；需要视觉检查时再读取图片。')
