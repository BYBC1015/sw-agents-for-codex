import copy
import http.client
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from store import Store, valid_path
from server import Handler, ThreadingHTTPServer

class CanvasTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.store=Store(self.tmp.name)
        self.asset=dict(id='a_'+'a'*20,path='E:/Downloads/test.mov',title='测试素材',kind='video',fps=50,frames=150,
                        width=3840,height=2160,bytes=6,mtimeNs=1,status='待复核',group='测试',duration=3)
        def seed(s):
            s['assets']=[self.asset];s['nodes']=[dict(id='n1',kind='asset',assetId=self.asset['id'],x=0,y=0)];s['selected']=['n1']
        self.store.change(seed)

    def tearDown(self):self.tmp.cleanup()

    def create(self):return self.store.create_task(dict(requestId='request1',text='检查火根',nodeIds=['n1'],frameRange='F100–120'))

    def test_snapshot_dedup_and_restart(self):
        self.store.annotate(dict(assetId=self.asset['id'],frame=100,rect=[.1,.2,.3,.4],text='第一条意见'))
        task=self.create()
        self.store.annotate(dict(assetId=self.asset['id'],frame=110,text='后续意见'))
        self.assertEqual(task['id'],self.create()['id'])
        restarted=Store(self.tmp.name)
        self.assertEqual(len(restarted.read()['tasks']),1)
        self.assertEqual(len(restarted.context(task['id'])['input']['annotations']),1)
        self.assertEqual(len(restarted.read()['annotations']),2)

    def test_layout_patch_keeps_new_result(self):
        task=self.create();self.store.update_task(task['id'],'running');self.store.update_task(task['id'],'review','检查完成，仍需用户确认')
        self.store.patch_board({'positions':{'n1':{'x':320,'y':150}},'selected':['n1']})
        state=self.store.read()
        self.assertEqual(state['nodes'][0]['x'],320)
        self.assertEqual(len([n for n in state['nodes'] if n['kind']=='result']),1)
        self.assertEqual(state['tasks'][0]['status'],'review')
        self.store.update_task(task['id'],'done')
        with self.assertRaises(ValueError):self.store.update_task(task['id'],'running')

    def test_invalid_rect_and_coordinates_are_atomic(self):
        before=self.store.read()
        with self.assertRaises(ValueError):self.store.annotate(dict(assetId=self.asset['id'],frame=150,text='越界'))
        with self.assertRaises(ValueError):self.store.annotate(dict(assetId=self.asset['id'],frame=0,rect=[.9,.9,.5,.5],text='越界'))
        with self.assertRaises(ValueError):self.store.patch_board({'positions':{'n1':{'x':200,'y':float('nan')}}})
        self.assertEqual(self.store.read(),before)

    def test_cli_roundtrip(self):
        task=self.create();cli=Path(__file__).resolve().parents[1]/'canvas_cli.py'
        def run(*args):return json.loads(subprocess.check_output([sys.executable,'-B','-X','utf8',str(cli),'--data-dir',self.tmp.name,*args],encoding='utf-8'))
        self.assertEqual(run('context','--task',task['id'])['input']['assets'][0]['id'],self.asset['id'])
        self.assertEqual(run('claim',task['id'])['status'],'running')
        note=Path(self.tmp.name)/'result.txt';note.write_text('已检查本次选中内容。',encoding='utf-8')
        self.assertEqual(run('complete',task['id'],'--body-file',str(note))['status'],'review')
        self.assertEqual(Store(self.tmp.name).read()['tasks'][0]['result'],'已检查本次选中内容。')

    def test_path_boundary(self):
        p=Path(self.tmp.name)/'outside.png';p.write_bytes(b'test')
        with self.assertRaises(ValueError):valid_path(p)

class HttpTests(unittest.TestCase):
    setUp=CanvasTests.setUp
    tearDown=CanvasTests.tearDown
    def test_media_range_and_local_origin(self):
        directory=self.store.cache/self.asset['id'];directory.mkdir();(directory/'preview.mp4').write_bytes(b'abcdef')
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.store=self.store;server.daemon_threads=True
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def request(method,path,body=None,headers=None):
            con=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=5)
            con.request(method,path,body=body,headers=headers or {});res=con.getresponse();result=(res.status,dict(res.getheaders()),res.read());con.close();return result
        try:
            url='/media/'+self.asset['id']+'/preview'
            code,headers,data=request('GET',url,headers={'Range':'bytes=1-3'})
            self.assertEqual((code,data),(206,b'bcd'));self.assertEqual(headers['Content-Range'],'bytes 1-3/6')
            self.assertEqual(request('GET',url,headers={'Range':'bytes=-2'})[2],b'ef')
            self.assertEqual(request('GET',url,headers={'Range':'bytes=10-20'})[0],416)
            self.assertEqual(request('GET','/api/state',headers={'Host':'attacker.invalid'})[0],403)
            self.assertEqual(request('POST','/api/board','{}',{'Content-Type':'application/json','X-Canvas-Client':'web','Origin':'https://example.com'})[0],403)
            self.assertEqual(request('GET','/media/../../store.py')[0],404)
            self.assertEqual(request('POST','/api/board','{}',{'Content-Type':'application/json','X-Canvas-Client':'web'})[0],200)
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
