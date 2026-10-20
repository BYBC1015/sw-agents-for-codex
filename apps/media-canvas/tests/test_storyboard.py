import copy
import http.client
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from store import Store
from server import Handler, ThreadingHTTPServer


class StoryboardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.s = Store(self.tmp.name)
        self.counter = 0
        self.s.change(lambda s: s['assets'].extend([dict(id='image-old',title='synthetic old'),dict(id='image-new',title='synthetic new')]))
        self.write('entity', 'coat', kind='wardrobe', fields=dict(description='蓝外套', locks=['外套为蓝色'], assetId='image-old'))
        for n in range(1, 7):
            self.write('shot', f'S{n:02}', fields=dict(title=f'镜头{n}', script='回家故事', duration=5,
                       camera='中景', entityRefs={'coat': 1} if n < 5 else {}, locks=['门在画面左侧'], outputAssetId='image-old'))
            self.write('review', f'S{n:02}', shotVersion=1, status='pass', evidence='合成测试记录，不代表真实媒体验收')

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, action, key, **kwargs):
        self.counter += 1
        return self.s.storyboard_write(dict(action=action,id=key,requestId=f'req-{self.counter}',
                                           expectedRevision=self.s.read()['revision'], **kwargs))

    def test_thirty_second_story_camera_edit_isolates_one_shot_and_restore_exports_selected_version(self):
        before = self.s.storyboard_export(final=True)
        self.assertEqual(before['totalDuration'], 30)
        self.write('shot','S03',fields=dict(camera='俯拍'))
        after = self.s.storyboard_export()
        self.assertEqual([s for s in before['shots'] if s['id']!='S03'],[s for s in after['shots'] if s['id']!='S03'])
        edited = after['shots'][2]
        self.assertEqual(edited['entityRefs'], {'coat':1})
        self.assertIsNone(edited['outputAssetId'])
        self.assertEqual(edited['reviews'], [])
        with self.assertRaises(ValueError): self.s.storyboard_export(final=True)
        self.write('select','S03',kind='shot',version=1)
        restored = self.s.storyboard_export(final=True)
        self.assertEqual(restored['shots'][2]['camera'], '中景')
        self.assertEqual(restored['shots'][2]['outputAssetId'], 'image-old')
        self.assertEqual(restored['shots'][2]['version'], 1)

    def test_shared_wardrobe_change_reports_exact_impact_without_changing_shots(self):
        before = copy.deepcopy(self.s.read()['storyboard']['shots'])
        impact = self.s.storyboard_impact('coat')
        self.assertEqual([s['shotId'] for s in impact['affectedShots']], ['S01','S02','S03','S04'])
        self.write('entity','coat',fields=dict(description='红外套',locks=['外套为红色']))
        self.assertEqual(before, self.s.read()['storyboard']['shots'])
        affected = [s['id'] for s in self.s.storyboard_export()['shots'] if s['issues']]
        self.assertEqual(affected, ['S01','S02','S03','S04'])
        with self.assertRaises(ValueError): self.write('review','S01',shotVersion=1,status='pass',evidence='旧图')
        self.assertFalse(self.s.read()['tasks'])
        self.assertEqual(self.s.summary()['storyboard']['needsReview'], 4)

    def test_reconcile_new_output_requires_explicit_new_review(self):
        self.write('entity','coat',fields=dict(description='红外套',locks=['外套为红色']))
        self.write('shot','S01',fields=dict(entityRefs={'coat':2},outputAssetId='image-new'))
        shot=self.s.storyboard_export()['shots'][0]
        self.assertEqual(shot['issues'], [dict(type='visual-review',status='unchecked')])
        self.write('review','S01',shotVersion=2,status='pass',evidence='已核对新版本合成记录')
        self.assertEqual(self.s.storyboard_export()['shots'][0]['issues'], [])
        self.assertIn('外套为红色', self.s.shot_packet('S01')['locks'])
        self.assertIn('门在画面左侧', self.s.shot_packet('S01')['locks'])

    def test_invalid_refs_assets_and_stale_revision_roll_back(self):
        for fields in (dict(entityRefs={'coat':99}), dict(entityRefs={'foreign':1}), dict(outputAssetId='foreign'),dict(duration=float('nan'))):
            before=self.s.read()
            with self.assertRaises(ValueError): self.write('shot','S01',fields=fields)
            self.assertEqual(self.s.read(),before)
        before=self.s.read()
        with self.assertRaises(ValueError): self.s.storyboard_write(dict(action='shot',id='S01',requestId='stale',expectedRevision=-1,fields=dict(camera='new')))
        self.assertEqual(self.s.read(),before)

    def test_retry_same_request_is_idempotent_different_body_rejected(self):
        body=dict(action='shot',id='S01',requestId='retry',expectedRevision=self.s.read()['revision'],fields=dict(camera='近景'))
        first=self.s.storyboard_write(body)
        self.assertEqual(first,self.s.storyboard_write(body))
        self.assertEqual(len(self.s.read()['storyboard']['shots'][0]['versions']),2)
        with self.assertRaises(ValueError): self.s.storyboard_write(dict(body,fields=dict(camera='远景')))

    def test_checkpoint_retains_old_selected_shot_and_locks(self):
        checkpoint=self.s.checkpoint(dict(requestId='snap',title='baseline',expectedRevision=self.s.read()['revision']))
        self.write('shot','S01',fields=dict(camera='特写'))
        saved=self.s.project_handoff('shots',checkpoint=checkpoint['id'])
        self.assertEqual(saved['items'][0]['currentVersion'],1)
        self.assertEqual(self.s.shot_packet('S01')['shotVersion'],2)
        self.assertEqual(Store(self.tmp.name).shot_packet('S01')['shotVersion'],2)

    def test_cli_and_http_expose_same_selected_records(self):
        cli=Path(__file__).resolve().parents[1]/'canvas_cli.py'
        raw=subprocess.check_output([sys.executable,'-B','-X','utf8',str(cli),'--data-dir',self.tmp.name,'shot-packet','--shot','S03'],encoding='utf-8')
        self.assertEqual(json.loads(raw)['shotId'],'S03')
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.store=self.s
        worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
        connection=http.client.HTTPConnection('127.0.0.1',server.server_port)
        try:
            connection.request('GET','/api/storyboard-export?final=1')
            response=connection.getresponse();data=json.loads(response.read())
            self.assertEqual(response.status,200);self.assertTrue(data['ready'])
            body=dict(projectId=self.s.read()['projectId'],expectedRevision=self.s.read()['revision'],requestId='http-edit',action='shot',id='S03',fields=dict(camera='俯拍'))
            connection.request('POST','/api/storyboard',json.dumps(body),{'Content-Type':'application/json','X-Canvas-Client':'web'})
            response=connection.getresponse();response.read();self.assertEqual(response.status,200)
            connection.request('GET','/api/storyboard-export?final=1')
            response=connection.getresponse();response.read();self.assertEqual(response.status,400)
        finally:
            connection.close();server.shutdown();server.server_close();worker.join()

    def test_legacy_read_does_not_rewrite_database(self):
        before=self.s.read()['revision']
        self.s.storyboard_read()
        self.assertEqual(self.s.read()['revision'],before)


if __name__=='__main__': unittest.main()
