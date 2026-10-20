from __future__ import annotations
import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from contextlib import nullcontext
from urllib.parse import urlsplit, parse_qs
from store import Store, DEFAULT_DATA, APP_ROOT, ALLOWED_ROOTS
from settings import VERSION
from bridge import task_summary, resolve_task
from registry import Registry, DEFAULT_REGISTRY, DEFAULT_WORKSPACE

class Handler(BaseHTTPRequestHandler):
    server_version='MediaCanvas/'+VERSION

    def project_store(self, project=None, required=True):
        registry=getattr(self.server,'registry',None)
        if registry:
            if not project and required:raise ValueError('请求必须指定项目编号，请刷新画布')
            return registry.store(project or self.server.store.read()['projectId'])
        self.server.store.check_project(project)
        return self.server.store
    protocol_version='HTTP/1.1'

    def log_message(self, fmt, *args):
        pass

    def trusted(self):
        allowed={f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
        if self.headers.get('Host') not in allowed: return False
        origin=self.headers.get('Origin')
        return not origin or origin in {'http://'+x for x in allowed}

    def json_response(self, data, code=200):
        payload=json.dumps(data,ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(payload)))
        self.end_headers()
        if self.command!='HEAD':self.wfile.write(payload)

    def send_file(self, path, cache=False, download=False):
        path=Path(path)
        if not path.is_file():self.json_response({'error':'文件不存在'},404);return
        size=path.stat().st_size;start=0;end=size-1;code=200
        value=self.headers.get('Range')
        if value:
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',value)
            try:
                if not match or not any(match.groups()):raise ValueError()
                a,b=match.groups()
                if a:start=int(a);end=min(int(b),size-1) if b else size-1
                else:
                    length=int(b)
                    if length<=0:raise ValueError()
                    start=max(0,size-length)
                if not 0<=start<=end<size:raise ValueError()
                code=206
            except ValueError:
                self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return
        self.send_response(code)
        self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length',str(max(0,end-start+1)))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Cache-Control','private, max-age=86400' if cache else 'no-cache')
        if code==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        if download:self.send_header('Content-Disposition','attachment')
        self.end_headers()
        if self.command=='HEAD':return
        try:
            with path.open('rb') as f:
                f.seek(start);remaining=end-start+1
                while remaining>0:
                    block=f.read(min(256*1024,remaining))
                    if not block:break
                    self.wfile.write(block);remaining-=len(block)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass

    def do_HEAD(self):self.do_GET()

    def do_GET(self):
        if not self.trusted():self.json_response({'error':'仅允许本机同源访问'},403);return
        parsed=urlsplit(self.path);path=parsed.path;store=self.server.store
        try:
            query=parse_qs(parsed.query,keep_blank_values=True);get=lambda key,default=None:query.get(key,[default])[0]
            registry=getattr(self.server,'registry',None)
            if path=='/api/projects' and registry:
                self.json_response(registry.projects(get('q',''),int(get('offset',0)),int(get('limit',12))));return
            if path=='/api/binding' and registry:
                result=registry.binding(get('conversation'))
                if result['projectId']:result['projectName']=registry.describe(result['projectId'])['name']
                self.json_response(result);return
            if path.startswith(('/api/','/media/')):store=self.project_store(get('project'),required=path!='/api/health')
            if path=='/api/health':
                self.json_response(dict(app='media-canvas',version=VERSION,bridge='conversation-bound',dataDir=str(store.root),projectId=store.read()['projectId'],registry=str(registry.path) if registry else None,mediaRoots=[str(p) for p in ALLOWED_ROOTS]));return
            if path=='/api/project-handoff':
                self.json_response(store.project_handoff(get('section','summary'),int(get('offset',0)),int(get('limit',12)),get('checkpoint')));return
            if path=='/api/summary':
                self.json_response(store.summary(get('since')));return
            if path=='/api/storyboard':
                self.json_response(store.storyboard_read(get('kind','shots'),int(get('offset',0)),int(get('limit',12))));return
            if path=='/api/storyboard-impact':
                self.json_response(store.storyboard_impact(get('entity')));return
            if path=='/api/shot-packet':
                self.json_response(store.shot_packet(get('shot')));return
            if path=='/api/storyboard-export':
                self.json_response(store.storyboard_export(get('final')=='1'));return
            if path=='/api/checkpoints':
                self.json_response(store.checkpoints(int(get('offset',0)),int(get('limit',12))));return
            if path=='/api/state':
                s=store.read();rev=parse_qs(parsed.query).get('revision',[''])[0]
                self.json_response({'unchanged':True,'revision':s['revision']} if rev==str(s['revision']) else s);return
            if path=='/api/context':
                self.json_response(store.context(parse_qs(parsed.query).get('task',[None])[0]));return
            if path in ('/api/packet','/api/detail','/api/tasks','/api/handoff'):
                query=parse_qs(parsed.query,keep_blank_values=True);get=lambda key,default=None:query.get(key,[default])[0]
                store.check_project(get('project'))
                offset=int(get('offset','0'));limit=int(get('limit','12'));reference=get('task')
                nodes=get('nodes');nodes=nodes.split(',') if nodes else ([] if nodes=='' else None)
                if path=='/api/packet':result=store.packet(reference,nodes,offset,limit)
                elif path=='/api/detail':result=store.detail(get('kind'),reference,nodes,offset,limit)
                elif path=='/api/tasks':result=store.list_tasks(offset,limit)
                else:
                    url=f'http://127.0.0.1:{self.server.server_port}/?project='+store.read()['projectId']
                    result=store.handoff(reference,url,get('checkpoint'))
                    if registry:
                        result['registry']=str(registry.path)
                        result['text']+='\n项目目录索引：'+str(registry.path)
                self.json_response(result);return
            match=re.fullmatch(r'/media/(a_[a-f0-9]{20})/(thumb|preview|original|frame)',path)
            if match:
                asset=next((a for a in store.read()['assets'] if a['id']==match[1]),None)
                if not asset:self.json_response({'error':'素材不存在'},404);return
                directory=store.cache/asset['id'];mode=match[2]
                if mode=='original':file=Path(asset['path'])
                elif mode=='thumb':file=directory/'thumb.jpg'
                elif mode=='preview':file=directory/('preview.jpg' if asset['kind']=='image' else 'preview.mp4')
                else:file=store.frame_file(asset,int(parse_qs(parsed.query).get('n',['0'])[0]))
                self.send_file(file,cache=mode!='original',download=mode=='original');return
            files={'/':'index.html','/geometry.js':'geometry.js','/app.js':'app.js','/style.css':'style.css','/site-tools.js':'site-tools.js','/projects.js':'projects.js','/storyboard.js':'storyboard.js'}
            if path in files:self.send_file(APP_ROOT/'web'/files[path]);return
            self.json_response({'error':'未找到'},404)
        except (ValueError,FileNotFoundError,KeyError) as exc:self.json_response({'error':str(exc)},400)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):pass

    def do_POST(self):
        if not self.trusted() or self.headers.get('X-Canvas-Client')!='web':
            self.json_response({'error':'仅允许本机画布提交'},403);return
        if self.headers.get_content_type()!='application/json':self.json_response({'error':'需要 JSON'},415);return
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=1024*1024:raise ValueError('请求大小不正确')
            body=json.loads(self.rfile.read(length));store=self.server.store
            if not isinstance(body,dict):raise ValueError('请求格式不正确')
            path=urlsplit(self.path).path
            registry=getattr(self.server,'registry',None)
            if registry and path in ('/api/projects/new','/api/projects/open','/api/bind'):
                if path=='/api/projects/new':result=registry.create(body)
                elif path=='/api/projects/open':result=registry.touch(body.get('projectId'))
                else:result=registry.bind(body)
                self.json_response(result);return
            store=self.project_store(body.get('projectId'))
            guard=registry.guard(body['conversationId'],body.get('projectId'),body.get('bindingVersion')) if registry and body.get('conversationId') else nullcontext()
            with guard:result=self.write_project(path,store,body)
            self.json_response(result)
        except (ValueError,KeyError,FileNotFoundError,TypeError) as exc:self.json_response({'error':str(exc)},400)
        except Exception as exc:self.json_response({'error':'操作失败：'+type(exc).__name__},500)

    def write_project(self,path,store,body):
        if path=='/api/board':result=store.patch_board(body)
        elif path=='/api/layout':result=store.layout(body)
        elif path=='/api/storyboard':result=store.storyboard_write(body)
        elif path=='/api/import':result=store.import_asset(body['path'],body.get('title'))
        elif path=='/api/annotations':result=store.annotate(body)
        elif path=='/api/tasks':result=task_summary(store.create_task(body))
        elif path=='/api/notes':
            note=store.add_note(body);result={k:note[k] for k in ('id','title','nodeId')}
        elif path=='/api/project':result=store.update_project(body)
        elif path=='/api/checkpoints':result=store.checkpoint(body)
        elif path=='/api/versions':result=store.choose_version(body)
        elif path=='/api/ingest':result=store.ingest(body)
        elif path=='/api/result':result=store.publish_result(body)
        elif path=='/api/claim':result=task_summary(store.update_task(body['task'],'running'))
        elif path=='/api/read-context':
            store.check_project(body.get('projectId'))
            result=store.packet(body.get('task'),body.get('nodeIds'),body.get('offset',0),body.get('limit',12))
        elif path=='/api/task-action':
            # Browser owns user cancellation and acceptance; Codex owns execution states.
            if body.get('status') not in {'cancelled','done','queued'}:raise ValueError('此操作需要 Codex 执行接口')
            current=resolve_task(store.read(),body['id'])
            if body['status']=='queued' and (not current or current['status']!='failed'):raise ValueError('只有失败任务可以在网页重新排队')
            result=store.update_task(body['id'],body['status'])
        else:raise ValueError('未找到接口')
        return result

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,default=DEFAULT_DATA)
    parser.add_argument('--port',type=int,default=8961)
    parser.add_argument('--registry',type=Path,default=DEFAULT_REGISTRY)
    parser.add_argument('--workspace-root',type=Path,default=DEFAULT_WORKSPACE)
    args=parser.parse_args(argv);store=Store(args.data_dir)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.daemon_threads=True;server.store=store
    server.registry=Registry(args.registry,args.workspace_root);server.registry.register(store.root)
    print(f'http://127.0.0.1:{server.server_port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
