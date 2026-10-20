"""Local project catalogue and explicit conversation bindings; no global active project."""
from contextlib import contextmanager
import json
from pathlib import Path
import re
import sqlite3
import uuid
from urllib.parse import urlencode
from bridge import bounded_text, page
from store import Store, now

from settings import DEFAULT_REGISTRY, DEFAULT_WORKSPACE


class Registry:
    def __init__(self, path=DEFAULT_REGISTRY, workspace=DEFAULT_WORKSPACE):
        self.path = Path(path).resolve()
        self.workspace = Path(workspace).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as con:
            con.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, path TEXT UNIQUE NOT NULL, created TEXT NOT NULL, opened TEXT NOT NULL, request TEXT UNIQUE, spec TEXT)')
            con.execute('CREATE TABLE IF NOT EXISTS bindings (conversation TEXT PRIMARY KEY, project TEXT NOT NULL, label TEXT NOT NULL, version INTEGER NOT NULL, updated TEXT NOT NULL)')

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.path, timeout=20)
        con.row_factory = sqlite3.Row
        try:
            with con: yield con
        finally: con.close()

    def register(self, data_dir):
        path = Path(data_dir).resolve()
        if not (path/'project.sqlite3').is_file():
            raise ValueError('项目数据库不存在，不自动创建')
        store = Store(path); pid = store.read()['projectId']
        with self.connect() as con:
            old = con.execute('SELECT * FROM projects WHERE id=? OR path=?', (pid, str(path))).fetchone()
            if old and (old['id'] != pid or old['path'] != str(path)):
                raise ValueError('项目编号或目录冲突，请保留原登记位置')
            con.execute('INSERT OR IGNORE INTO projects VALUES (?,?,?,?,NULL,NULL)', (pid,str(path),now(),now()))
        return self.describe(pid)

    def store(self, project):
        with self.connect() as con:
            row = con.execute('SELECT * FROM projects WHERE id=?', (project,)).fetchone()
        if not row: raise ValueError('项目未登记，请从项目列表选择')
        path = Path(row['path'])
        if not (path/'project.sqlite3').is_file(): raise ValueError('项目文件已离线或移动，请恢复原目录')
        store = Store(path); store.check_project(project)
        return store

    def describe(self, project):
        s = self.store(project); state = s.read()
        return dict(projectId=project, name=state['name'], goal=state['goal'], dataDir=str(s.root),
                    revision=state['revision'], assetCount=len(state['assets']),
                    activeTasks=sum(t['status'] not in ('done','cancelled') for t in state['tasks']))

    def projects(self, query='', offset=0, limit=12):
        with self.connect() as con:
            rows = con.execute('SELECT * FROM projects ORDER BY opened DESC, created DESC').fetchall()
        items = []
        for row in rows:
            try: item = self.describe(row['id'])
            except (ValueError, OSError, sqlite3.Error): item = dict(projectId=row['id'], name=row['id'], dataDir=row['path'], unavailable=True)
            if query.casefold() in (item['name']+' '+item['projectId']).casefold(): items.append(item)
        return page(items, offset, limit)

    def create(self, body):
        name = bounded_text(body.get('name'), '项目名', 80, True)
        goal = bounded_text(body.get('goal',''), '目标', 1000)
        request = bounded_text(body.get('requestId'), '请求编号', 100, True)
        if re.search(r'[<>:"/\\|?*\x00-\x1f]', name) or name.endswith(('.', ' ')) or name in ('.','..') or re.match(r'^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(?:\.|$)', name, re.I):
            raise ValueError('项目名称不能含 Windows 路径保留字符或设备名称')
        spec = json.dumps(dict(name=name,goal=goal),sort_keys=True,ensure_ascii=False)
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            old = con.execute('SELECT * FROM projects WHERE request=?',(request,)).fetchone()
            if old:
                if old['spec'] != spec: raise ValueError('请求编号已用于其他新项目')
                pid = old['id']
            else:
                base = (self.workspace/name).resolve()
                if not base.is_relative_to(self.workspace): raise ValueError('项目目录超出工作区')
                if base.exists(): base = self.workspace/(name+'_'+uuid.uuid4().hex[:6])
                base.mkdir(parents=True,exist_ok=False)
                for folder in ('过程','交付'): (base/folder).mkdir()
                s = Store(base/'.canvas')
                s.change(lambda state: state.update(name=name,goal=goal,workspaceRoot=str(base)))
                pid = s.read()['projectId']
                con.execute('INSERT INTO projects VALUES (?,?,?,?,?,?)',(pid,str(s.root),now(),now(),request,spec))
        return self.describe(pid)

    def touch(self, project):
        self.store(project)
        with self.connect() as con: con.execute('UPDATE projects SET opened=? WHERE id=?',(now(),project))
        return self.describe(project)

    def binding(self, conversation):
        conversation = bounded_text(conversation,'对话编号',160,True)
        with self.connect() as con:
            row = con.execute('SELECT * FROM bindings WHERE conversation=?',(conversation,)).fetchone()
        if not row: return dict(conversationId=conversation,projectId=None,version=0)
        return dict(conversationId=conversation,projectId=row['project'],label=row['label'],version=row['version'],updatedAt=row['updated'])

    def bind(self, body):
        conversation = bounded_text(body.get('conversationId'),'对话编号',160,True)
        project = body.get('projectId'); self.store(project)
        label = bounded_text(body.get('label','当前对话'),'对话名称',120,True)
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            row = con.execute('SELECT * FROM bindings WHERE conversation=?',(conversation,)).fetchone()
            version = row['version'] if row else 0
            if body.get('expectedVersion') != version: raise ValueError('对话绑定已变化，请重新读取后切换')
            if not row or row['project'] != project or row['label'] != label:
                con.execute('INSERT OR REPLACE INTO bindings VALUES (?,?,?,?,?)',(conversation,project,label,version+1,now()))
        return self.binding(conversation)

    @contextmanager
    def guard(self, conversation, project, version=None):
        # Hold the catalogue transaction across the write: rebind cannot race an in-flight write.
        with self.connect() as con:
            con.execute('BEGIN IMMEDIATE')
            row = con.execute('SELECT * FROM bindings WHERE conversation=?',(conversation,)).fetchone()
            if not row or row['project'] != project or (version is not None and version != row['version']):
                raise ValueError('对话与目标项目不一致，未写入；请明确切换对话绑定')
            yield

    def url(self, project, base='http://127.0.0.1:8961/', conversation=None):
        params = dict(project=project)
        if conversation: params['conversation']=conversation
        return base.split('?')[0]+'?'+urlencode(params)

    def launch(self, conversation, base='http://127.0.0.1:8961/'):
        if not conversation or not conversation.strip():
            return dict(projectId=None, bindingVersion=0, mode='blank', url=base.split('?')[0])
        binding = self.binding(conversation)
        project = binding['projectId']
        if not project:
            token = uuid.uuid5(uuid.NAMESPACE_URL, 'sw-canvas:' + conversation).hex
            created = self.create(dict(requestId='auto-blank-' + token,
                                       name='空白画布-' + token[:12], goal=''))
            try:
                binding = self.bind(dict(conversationId=conversation, projectId=created['projectId'],
                                         expectedVersion=binding['version'], label='自动绑定空画布'))
            except ValueError:
                # Another launch or an explicit selection may have bound this chat first.
                binding = self.binding(conversation)
                if not binding['projectId']:
                    raise
            project = binding['projectId']
        params = dict(conversation=conversation)
        if project: params['project'] = project
        return dict(projectId=project, bindingVersion=binding['version'],
                    mode='bound' if project else 'blank', url=base.split('?')[0]+'?'+urlencode(params))
