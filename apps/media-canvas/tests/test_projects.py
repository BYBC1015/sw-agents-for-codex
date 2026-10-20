import copy
import http.client
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from PIL import Image
from registry import Registry
from server import Handler,ThreadingHTTPServer


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.work=self.root/'work';self.catalog=self.root/'catalog.sqlite3'
        self.allowed=patch('store.ALLOWED_ROOTS',[self.work.resolve()]);self.allowed.start()
        self.r=Registry(self.catalog,self.work)
        self.a=self.r.create(dict(requestId='a',name='项目甲',goal='甲目标'))
        self.b=self.r.create(dict(requestId='b',name='项目乙',goal='乙目标'))
        self.s=self.r.store(self.a['projectId'])
        self.source=self.root/'source.png';Image.new('RGB',(60,40),'blue').save(self.source)
        self.other=self.root/'other.png';Image.new('RGB',(60,40),'orange').save(self.other)

    def tearDown(self):self.allowed.stop();self.tmp.cleanup()

    def ingest(self):
        return self.s.ingest(dict(requestId='in1',files=[dict(path=str(self.source),mode='copy',title='参考')]))['assets'][0]

    def task(self):
        a=self.ingest()
        t=self.s.create_task(dict(requestId='task1',intent='execute',text='仅测试状态',nodeIds=[a['nodeId']]))
        return a,t

    def test_project_create_retry_search_and_duplicate_name_isolation(self):
        retry=self.r.create(dict(requestId='a',name='项目甲',goal='甲目标'))
        self.assertEqual(retry['projectId'],self.a['projectId'])
        with self.assertRaises(ValueError):self.r.create(dict(requestId='a',name='其他'))
        second=self.r.create(dict(requestId='a2',name='项目甲'))
        self.assertNotEqual(second['dataDir'],self.a['dataDir'])
        self.assertEqual(self.r.projects('项目甲')['total'],2)
        self.assertTrue((Path(self.a['dataDir']).parent/'交付').is_dir())
        for name in ('../other','CON','a/b','LPT1.txt'):
            with self.assertRaises(ValueError):self.r.create(dict(requestId=name,name=name))

    def test_missing_project_never_reinitialized_and_clones_rejected(self):
        clone=self.root/'clone';shutil.copytree(self.s.root,clone)
        with self.assertRaises(ValueError):self.r.register(clone)
        missing=Path(self.b['dataDir'])/'project.sqlite3';missing.unlink()
        with self.assertRaises(ValueError):self.r.store(self.b['projectId'])
        self.assertFalse(missing.exists())
        self.assertTrue(next(p for p in self.r.projects()['items'] if p['projectId']==self.b['projectId'])['unavailable'])

    def test_binding_is_persistent_isolated_and_cas_guarded(self):
        a=self.a['projectId'];b=self.b['projectId']
        self.r.bind(dict(conversationId='chat-a',projectId=a,expectedVersion=0))
        self.r.bind(dict(conversationId='chat-b',projectId=b,expectedVersion=0))
        restored=Registry(self.catalog,self.work)
        self.assertEqual(restored.binding('chat-a')['projectId'],a)
        with self.assertRaises(ValueError):self.r.bind(dict(conversationId='chat-a',projectId=b,expectedVersion=0))
        with self.assertRaises(ValueError):
            with self.r.guard('chat-a',b):pass
        self.r.bind(dict(conversationId='chat-a',projectId=b,expectedVersion=1))
        with self.assertRaises(ValueError):
            with self.r.guard('chat-a',a,1):pass
        self.assertEqual(self.r.binding('chat-b')['version'],1)

    def test_fresh_launch_binds_empty_project_and_reuses_only_its_own_binding(self):
        before=self.r.projects()['total']
        self.r.bind(dict(conversationId='old-chat',projectId=self.a['projectId'],expectedVersion=0))
        fresh=self.r.launch('new-chat')
        self.assertNotIn(fresh['projectId'],[self.a['projectId'],self.b['projectId']])
        self.assertEqual(fresh['mode'],'bound')
        self.assertEqual(fresh['bindingVersion'],1)
        self.assertIn('project='+fresh['projectId'],fresh['url'])
        self.assertNotIn('projects=',fresh['url'])
        state=self.r.store(fresh['projectId']).read()
        for field in ('assets','nodes','tasks','notes'):
            self.assertEqual(state[field],[])
        self.assertEqual(self.r.launch('new-chat'),fresh)
        self.assertEqual(self.r.projects()['total'],before+1)
        self.assertEqual(self.r.launch('old-chat')['projectId'],self.a['projectId'])
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(__file__).resolve().parents[1]/'canvas_cli.py'),
            '--registry',str(self.catalog),'--conversation','new-chat','launch'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),fresh)

    def test_distinct_chats_get_distinct_blank_projects_and_missing_id_creates_nothing(self):
        before=self.r.projects()['total']
        for conversation in (None,'','  '):
            blank=self.r.launch(conversation)
            self.assertEqual(blank['mode'],'blank')
            self.assertIsNone(blank['projectId'])
        self.assertEqual(self.r.projects()['total'],before)
        first=self.r.launch('first-chat')
        second=self.r.launch('second-chat')
        self.assertNotEqual(first['projectId'],second['projectId'])

    def test_concurrent_launches_create_and_bind_one_project(self):
        from concurrent.futures import ThreadPoolExecutor
        before=self.r.projects()['total']
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(self.r.launch,['same-chat','same-chat']))
        self.assertEqual(results[0],results[1])
        self.assertEqual(self.r.projects()['total'],before+1)

    def test_compact_summary_has_bounded_text_and_project_scoped_cursor(self):
        self.s.change(lambda s:s.update(goal='长'*1000,nextStep='步'*2000,decisions='决定'*1000))
        summary=self.s.summary()
        self.assertEqual(len(summary['goal']),240)
        self.assertEqual(len(summary['nextStep']),240)
        self.assertEqual(summary['truncatedFields'],['goal','nextStep'])
        self.assertNotIn('decisions',summary)
        self.assertNotIn('paths',summary)
        self.assertLess(len(json.dumps(summary,ensure_ascii=False)),1100)
        unchanged=self.s.summary(summary['cursor'])
        self.assertTrue(unchanged['unchanged'])
        self.assertNotIn('goal',unchanged)
        other=self.r.store(self.b['projectId']).summary(summary['cursor'])
        self.assertNotIn('unchanged',other)
        self.s.add_note(dict(requestId='changed',title='新决定',text='已确认'))
        self.assertNotIn('unchanged',self.s.summary(summary['cursor']))
        self.assertEqual(self.s.project_handoff()['project']['decisions'],'决定'*1000)

    def test_identical_task_refs_stay_in_their_project(self):
        _,first=self.task()
        second_store=self.r.store(self.b['projectId'])
        note=second_store.add_note(dict(requestId='b-note',title='乙方案',text='只属于乙'))
        second=second_store.create_task(dict(requestId='b-task',intent='discuss',text='乙的讨论',nodeIds=[note['nodeId']]))
        self.assertEqual(first['ref'],second['ref'])
        self.assertNotEqual(first['id'],second['id'])
        self.assertEqual(second_store.packet('T001')['task']['text'],'乙的讨论')
        self.assertEqual(self.s.packet('T001')['task']['text'],'仅测试状态')
        self.assertEqual(second_store.packet('T001')['assets']['total'],0)

    def test_rebind_waits_for_inflight_guard(self):
        a=self.a['projectId'];b=self.b['projectId'];started=threading.Event();finished=threading.Event()
        self.r.bind(dict(conversationId='chat',projectId=a,expectedVersion=0))
        def rebind():
            started.set();self.r.bind(dict(conversationId='chat',projectId=b,expectedVersion=1));finished.set()
        with self.r.guard('chat',a,1):
            thread=threading.Thread(target=rebind);thread.start();started.wait(2)
            self.assertFalse(finished.wait(.1))
            self.s.add_note(dict(requestId='guard-note',title='在途写入',text='属于甲'))
        thread.join(3);self.assertTrue(finished.is_set())
        self.assertEqual(len(self.r.store(b).read()['notes']),0)

    def test_copy_import_is_non_destructive_and_retry_survives_missing_source(self):
        original=self.source.read_bytes();before=self.source.stat().st_mtime_ns
        a=self.ingest();state=self.s.read();stored=state['assets'][0]
        self.assertTrue(Path(stored['path']).is_relative_to(Path(self.s.paths()['process'])))
        self.assertEqual(self.source.read_bytes(),original);self.assertEqual(self.source.stat().st_mtime_ns,before)
        self.source.unlink()
        self.assertEqual(self.ingest()['assetId'],a['assetId'])
        self.assertEqual(len(self.s.read()['assets']),1)
        with self.assertRaises(ValueError):self.s.ingest(dict(requestId='in1',files=[]))

    def test_result_is_atomic_versioned_and_idempotent(self):
        a,t=self.task();self.s.update_task(t['ref'],'running')
        body=dict(requestId='result1',task=t['ref'],text='软件测试结果',files=[dict(path=str(self.other),mode='copy',parentNode=a['nodeId'])])
        before=self.s.read();bad=copy.deepcopy(body);bad['files'][0]['parentNode']='foreign-node'
        with self.assertRaises(ValueError):self.s.publish_result(bad)
        self.assertEqual(self.s.read(),before)
        result=self.s.publish_result(body);self.assertEqual(result['task']['status'],'review')
        self.assertEqual(self.s.read()['assets'][1]['version'],2)
        self.other.unlink();self.assertEqual(self.s.publish_result(body),result)
        s=self.s.read();self.assertEqual(len(s['assets']),2)
        self.assertEqual(len([n for n in s['nodes'] if n['kind']=='result']),1)
        self.s.update_task(t['ref'],'done');self.assertEqual(self.s.read()['assets'][1]['status'],'已确认')

    def test_discuss_cannot_publish_media(self):
        a=self.ingest();t=self.s.create_task(dict(requestId='d',intent='discuss',text='只讨论',nodeIds=[a['nodeId']]))
        self.s.update_task(t['ref'],'running')
        with self.assertRaises(ValueError):self.s.publish_result(dict(requestId='r',task=t['ref'],text='说明',files=[dict(path=str(self.other),mode='copy')]))
        self.s.publish_result(dict(requestId='r2',task=t['ref'],text='讨论说明'))
        self.assertEqual(self.s.read()['tasks'][0]['status'],'review')

    def test_complete_handoff_is_project_wide_immutable_and_paged(self):
        a,t=self.task();self.s.update_project(dict(expectedRevision=self.s.read()['revision'],decisions='已定蓝色',nextStep='等待确认',progress=dict(stage='比较',blockers='待反馈',openQuestions='是否采用',deliveryNotes='PNG')))
        self.s.choose_version(dict(expectedRevision=self.s.read()['revision'],assetId=a['assetId'],disposition='selected',reason='构图已确认'))
        self.s.add_note(dict(requestId='n',title='未选中方案',text='也必须交接'))
        body=dict(requestId='cp',title='完整项目',expectedRevision=self.s.read()['revision'])
        cp=self.s.checkpoint(body);self.assertEqual(self.s.checkpoint(body),cp)
        self.s.update_project(dict(expectedRevision=self.s.read()['revision'],decisions='后来改变'))
        snapshot=self.s.project_handoff(checkpoint=cp['id'])
        self.assertEqual(snapshot['project']['decisions'],'已定蓝色');self.assertEqual(snapshot['progress']['blockers'],'待反馈')
        self.assertEqual(snapshot['versionChoices']['items'][0]['reason'],'构图已确认')
        self.assertEqual(snapshot['counts']['notes'],1);self.assertFalse(snapshot['imagesIncluded'])
        self.assertEqual(self.s.project_handoff('tasks',checkpoint=cp['id'])['items'][0]['input']['assets'][0]['id'],a['assetId'])
        self.assertIsNotNone(self.s.project_handoff('nodes',limit=1,checkpoint=cp['id'])['nextOffset'])
        with self.assertRaises(ValueError):self.s.checkpoint(dict(body,requestId='stale'))

    def test_fresh_cli_resumes_binding_and_rejects_wrong_project(self):
        a=self.a['projectId'];self.r.bind(dict(conversationId='real-test-conversation',projectId=a,expectedVersion=0))
        cli=Path(__file__).resolve().parents[1]/'canvas_cli.py'
        def run(*args):return subprocess.run([sys.executable,'-B','-X','utf8',str(cli),'--registry',str(self.catalog),'--conversation','real-test-conversation',*args],capture_output=True,text=True,encoding='utf-8')
        result=run('project-handoff');self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['project']['projectId'],a)
        self.assertNotEqual(run('--project',self.b['projectId'],'packet').returncode,0)
        body=self.root/'note.json';body.write_text(json.dumps(dict(requestId='n',title='测试',text='测试')),encoding='utf-8')
        self.assertNotEqual(run('note','--body-file',str(body)).returncode,0)
        self.assertEqual(run('--project',a,'note','--body-file',str(body)).returncode,0)
        self.assertEqual(len(self.r.store(self.b['projectId']).read()['notes']),0)

    def test_http_projects_and_media_are_routed_per_request(self):
        a=self.ingest();pid=self.a['projectId'];other=self.b['projectId']
        self.r.bind(dict(conversationId='chat',projectId=pid,expectedVersion=0))
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.store=self.s;server.registry=self.r;server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def request(method,path,body=None):
            con=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
            con.request(method,path,json.dumps(body) if body is not None else None,{'Content-Type':'application/json','X-Canvas-Client':'web'})
            res=con.getresponse();data=res.read();status=res.status;con.close();return status,data
        try:
            self.assertEqual(request('GET','/api/state')[0],400)
            self.assertEqual(json.loads(request('GET','/api/state?project='+other)[1])['assets'],[])
            self.assertEqual(request('GET',f"/media/{a['assetId']}/thumb?project={other}")[0],404)
            self.assertEqual(request('GET',f"/media/{a['assetId']}/thumb?project={pid}")[0],200)
            body=dict(projectId=other,conversationId='chat',requestId='wrong',title='不能串项目',text='测试')
            self.assertEqual(request('POST','/api/notes',body)[0],400)
            self.assertEqual(request('POST','/api/notes',dict(body,projectId=pid))[0],200)
            self.assertEqual(json.loads(request('GET','/api/projects')[1])['total'],2)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
