"""Explicit project and conversation routing for local canvas collaboration."""
import argparse
from contextlib import nullcontext
import json
import sqlite3
from pathlib import Path
from store import Store, DEFAULT_DATA
from registry import Registry, DEFAULT_REGISTRY, DEFAULT_WORKSPACE
from bridge import task_summary

READS={'context','packet','tasks','detail','handoff','frame','project-handoff','checkpoints','backup','summary','storyboard','shot-packet','storyboard-impact','storyboard-export'}

def read_body(args):
    body=json.loads(args.body_file.read_text(encoding='utf-8-sig'))
    if not isinstance(body,dict):raise ValueError('JSON 文件须为对象')
    return body

def project_command(s,args):
    name=args.command
    if name=='storyboard':return s.storyboard_read(args.kind,args.offset,args.limit)
    if name=='storyboard-edit':return s.storyboard_write(read_body(args))
    if name=='shot-packet':return s.shot_packet(args.shot)
    if name=='storyboard-impact':return s.storyboard_impact(args.entity)
    if name=='storyboard-export':return s.storyboard_export(args.final)
    if name=='summary':return s.summary(args.since)
    if name=='context':return s.context(args.task)
    if name=='packet':return s.packet(args.task,args.nodes,args.offset,args.limit)
    if name=='tasks':return s.list_tasks(args.offset,args.limit)
    if name=='detail':return s.detail(args.kind,args.task,args.nodes,args.offset,args.limit)
    if name=='handoff':return s.handoff(args.task,args.url,args.checkpoint)
    if name=='frame':return s.asset_frame(args.asset,args.n,args.task)
    if name=='project-handoff':return s.project_handoff(args.section,args.offset,args.limit,args.checkpoint)
    if name=='checkpoints':return s.checkpoints(args.offset,args.limit)
    if name in ('note','create-task','project','checkpoint','version','ingest','result','layout'):
        body=read_body(args)
        if name=='note':
            n=s.add_note(body);return {k:n[k] for k in ('id','title','nodeId')}
        if name=='create-task':return task_summary(s.create_task(body))
        return {'project':s.update_project,'checkpoint':s.checkpoint,'version':s.choose_version,
                'ingest':s.ingest,'result':s.publish_result,'layout':s.layout}[name](body)
    if name=='init':return s.update_project(dict(expectedRevision=s.read()['revision'],name=args.name,goal=args.goal))
    if name=='backup':
        if args.path.exists():raise ValueError('备份目标已存在，不覆盖')
        args.path.parent.mkdir(parents=True,exist_ok=True)
        with s.connect() as source:
            dest=sqlite3.connect(args.path)
            try:source.backup(dest)
            finally:dest.close()
        return {'backup':str(args.path.resolve())}
    if name in ('claim','requeue'):return task_summary(s.update_task(args.task_id,'running' if name=='claim' else 'queued'))
    if name in ('complete','fail'):
        text=args.body_file.read_text(encoding='utf-8-sig')
        return task_summary(s.update_task(args.task_id,'review' if name=='complete' else 'failed',text))
    return s.import_asset(args.path,args.title,'待用户确认' if name=='add-result' else '已导入',
                '制作结果' if name=='add-result' else '素材',parent=args.parent_node,task_ref=args.task)

def main():
    parser=argparse.ArgumentParser(description='SW Canvas · 项目、对话绑定、完整交接')
    parser.add_argument('--data-dir',type=Path)
    parser.add_argument('--project',help='固定本次操作所属项目')
    parser.add_argument('--registry',type=Path,default=DEFAULT_REGISTRY)
    parser.add_argument('--workspace-root',type=Path,default=DEFAULT_WORKSPACE)
    parser.add_argument('--conversation',help='实际 Codex 对话编号')
    parser.add_argument('--binding-version',type=int)
    sub=parser.add_subparsers(dest='command',required=True)
    c=sub.add_parser('storyboard');c.add_argument('--kind',choices=['shots','entities'],default='shots');c.add_argument('--offset',type=int,default=0);c.add_argument('--limit',type=int,default=12)
    c=sub.add_parser('storyboard-edit');c.add_argument('--body-file',type=Path,required=True)
    c=sub.add_parser('shot-packet');c.add_argument('--shot',required=True)
    c=sub.add_parser('storyboard-impact');c.add_argument('--entity',required=True)
    c=sub.add_parser('storyboard-export');c.add_argument('--final',action='store_true')
    c=sub.add_parser('context');c.add_argument('--task')
    c=sub.add_parser('summary');c.add_argument('--since')
    c=sub.add_parser('launch');c.add_argument('--url',default='http://127.0.0.1:8961/')
    for name in ('packet','tasks','detail','project-handoff','checkpoints','projects'):
        c=sub.add_parser(name);c.add_argument('--offset',type=int,default=0);c.add_argument('--limit',type=int,default=12)
        if name in ('packet','detail'):
            c.add_argument('--task');c.add_argument('--nodes',nargs='*')
        if name=='detail':c.add_argument('kind',choices=['assets','annotations','notes','result'])
        if name=='project-handoff':c.add_argument('--section',default='summary');c.add_argument('--checkpoint')
        if name=='projects':c.add_argument('--query',default='')
    c=sub.add_parser('handoff');c.add_argument('--task');c.add_argument('--url');c.add_argument('--checkpoint')
    c=sub.add_parser('frame');c.add_argument('--asset',required=True);c.add_argument('--n',type=int,required=True);c.add_argument('--task')
    for name in ('note','create-task','project','checkpoint','version','ingest','result','create-project','bind','layout'):
        c=sub.add_parser(name);c.add_argument('--body-file',type=Path,required=True)
    sub.add_parser('register');sub.add_parser('binding')
    c=sub.add_parser('open');c.add_argument('--url',default='http://127.0.0.1:8961/')
    c=sub.add_parser('init');c.add_argument('--name',required=True);c.add_argument('--goal',default='')
    c=sub.add_parser('backup');c.add_argument('--path',type=Path,required=True)
    for name in ('claim','requeue'):
        p=sub.add_parser(name);p.add_argument('task_id')
    for name in ('complete','fail'):
        p=sub.add_parser(name);p.add_argument('task_id');p.add_argument('--body-file',type=Path,required=True)
    for name in ('import','add-result'):
        p=sub.add_parser(name);p.add_argument('--path',required=True);p.add_argument('--title');p.add_argument('--parent-node');p.add_argument('--task')
    args=parser.parse_args()
    try:
        catalogue={'projects','create-project','register','binding','bind','open','launch'}
        registry=Registry(args.registry,args.workspace_root) if args.command in catalogue or args.conversation or (args.project and not args.data_dir) else None
        if args.command in catalogue:
            if args.command=='projects':result=registry.projects(args.query,args.offset,args.limit)
            elif args.command=='create-project':result=registry.create(read_body(args))
            elif args.command=='register':result=registry.register(args.data_dir or DEFAULT_DATA)
            elif args.command=='binding':result=registry.binding(args.conversation)
            elif args.command=='launch':result=registry.launch(args.conversation,args.url)
            elif args.command=='bind':
                body=read_body(args)
                if args.conversation and body.get('conversationId')!=args.conversation:raise ValueError('对话编号不一致')
                if args.project and body.get('projectId')!=args.project:raise ValueError('项目编号不一致')
                result=registry.bind(body)
            else:
                pid=args.project or (registry.binding(args.conversation)['projectId'] if args.conversation else None)
                result=registry.touch(pid);result['url']=registry.url(pid,args.url,args.conversation)
        else:
            if args.conversation and args.command not in READS and not args.project:
                raise ValueError('对话写入必须显式指定 --project，防止切换后误写')
            pid=args.project
            if args.conversation and not pid:pid=registry.binding(args.conversation)['projectId']
            if args.conversation and not pid:raise ValueError('此对话尚未绑定项目')
            if args.data_dir or not pid:
                data=args.data_dir or DEFAULT_DATA;exists=(data/'project.sqlite3').is_file()
                if args.command=='init' and exists:raise ValueError('项目已存在；init 不覆盖已有项目')
                if args.command!='init' and not exists:raise ValueError('项目数据库不存在，请核对目录')
                s=Store(data);s.check_project(pid)
                if registry:registry.register(s.root)
            else:s=registry.store(pid)
            pid=s.read()['projectId']
            guard=registry.guard(args.conversation,pid,args.binding_version) if args.conversation else nullcontext()
            with guard:result=project_command(s,args)
        print(json.dumps(result,ensure_ascii=False,separators=(',',':')))
    except (ValueError,KeyError,TypeError,FileNotFoundError,OSError) as exc:
        parser.exit(2,json.dumps({'error':str(exc)},ensure_ascii=False)+'\n')

if __name__=='__main__':main()
