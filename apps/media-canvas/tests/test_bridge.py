import copy
import http.client
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

import test_canvas
from store import Store, ALLOWED_ROOTS, valid_path
from server import Handler, ThreadingHTTPServer


class BridgeTests(unittest.TestCase):
    setUp = test_canvas.CanvasTests.setUp
    tearDown = test_canvas.CanvasTests.tearDown
    create = test_canvas.CanvasTests.create

    def test_read_legacy_does_not_rewrite_payload_or_revision(self):
        with self.store.connect() as con:
            row = con.execute('SELECT revision,payload FROM project').fetchone()
            payload = json.loads(row[1])
            for key in ['projectId', 'schemaVersion', 'notes', 'goal', 'decisions', 'nextStep']:
                payload.pop(key, None)
            raw = json.dumps(payload)
            con.execute('UPDATE project SET payload=?', (raw,))
        state = self.store.read()
        self.assertEqual(state['projectId'], Store(self.tmp.name).read()['projectId'])
        self.store.packet()
        with self.store.connect() as con:
            self.assertEqual(con.execute('SELECT revision,payload FROM project').fetchone(), (row[0], raw))

    def test_discussion_freezes_note_project_and_frame_annotations(self):
        n = self.store.add_note(dict(requestId='note1', title='方向', text='锁定暖色', nodeIds=['n1']))
        for frame in [99, 100, 120, 121]:
            self.store.annotate(dict(assetId=self.asset['id'], frame=frame, text=str(frame)))
        t = self.store.create_task(dict(requestId='d1', intent='discuss', text='讨论这段', frameRange='F100–120', nodeIds=['n1', n['nodeId']]))
        self.assertEqual([a['frame'] for a in t['input']['annotations']], [100, 120])
        self.store.change(lambda s: (s['selected'].clear(), s['notes'][0].update(text='已改'), s.update(goal='新目标')))
        packet = self.store.packet(t['ref'])
        self.assertEqual(packet['source'], 'frozen-task')
        self.assertEqual(packet['notes']['items'][0]['excerpt'], '锁定暖色')
        self.assertEqual(packet['inputProject']['goal'], '')
        self.assertEqual(packet['project']['goal'], '新目标')
        self.assertIn('只讨论，不执行', self.store.handoff(t['ref'])['text'])
        self.assertEqual(len(packet['nodes']['items']), 2)

    def test_default_packet_is_bounded_and_details_are_explicit(self):
        def add(state):
            state['annotations'] = [dict(id=f'a{i}', assetId=self.asset['id'], frame=i%150, text='文'*2000, rect=None) for i in range(200)]
        self.store.change(add)
        for i in range(25):
            self.store.create_task(dict(requestId=str(i), text='问'*8000, nodeIds=['n1']))
        packet = self.store.packet()
        self.assertLess(len(json.dumps(packet, ensure_ascii=False)), 18000)
        self.assertEqual(packet['annotations']['total'], 200)
        self.assertEqual(packet['annotations']['nextOffset'], 12)
        self.assertEqual(packet['tasks']['total'], 25)
        self.assertFalse(packet['imagesIncluded'])
        self.assertNotIn('path', packet['assets']['items'][0])
        details = self.store.detail('annotations', 'T001', offset=12, limit=2)
        self.assertEqual(len(details['items'][0]['text']), 2000)
        self.assertEqual(details['items'][0]['id'], 'a12')
        with self.assertRaises(ValueError): self.store.packet(limit=100)

    def test_retries_are_idempotent_and_conflicting_payload_is_rejected(self):
        task = self.create()
        self.assertEqual(Store(self.tmp.name).create_task(dict(requestId='request1', text='检查火根', nodeIds=['n1'], frameRange='F100–120'))['id'], task['id'])
        before = self.store.read()
        with self.assertRaises(ValueError):
            self.store.create_task(dict(requestId='request1', text='不同内容', nodeIds=['n1']))
        self.assertEqual(self.store.read(), before)

    def test_result_links_and_duplicate_registration(self):
        task = self.create()
        output = copy.deepcopy(self.asset); output['id'] = 'a_'+'b'*20
        with patch.object(self.store, 'prepare_asset', return_value=output):
            with self.assertRaises(ValueError): self.store.import_asset('ignored', task_ref=task['ref'])
            self.store.update_task(task['ref'], 'running')
            self.store.import_asset('ignored', task_ref=task['ref'])
            self.store.import_asset('ignored', task_ref=task['ref'])
        state = self.store.read()
        self.assertEqual(state['tasks'][0]['outputAssetIds'], [output['id']])
        self.assertEqual(len([e for e in state['edges'] if e['label']=='任务输出']), 1)
        self.store.update_task(task['ref'], 'review', '结果说明')
        self.assertEqual(self.store.detail('result', task['ref'])['assets'][0]['id'], output['id'])

    def test_project_guard_and_conflicting_edit(self):
        state = self.store.read()
        with self.assertRaises(ValueError): self.store.check_project('PWRONG')
        self.store.update_project(dict(expectedRevision=state['revision'], name='项目甲', decisions='已确认'))
        with self.assertRaises(ValueError): self.store.update_project(dict(expectedRevision=state['revision'], name='过期覆盖'))
        self.assertEqual(self.store.read()['name'], '项目甲')

    def test_select_task_card_resolves_frozen_input(self):
        task = self.create()
        node = next(n for n in self.store.read()['nodes'] if n.get('taskId') == task['id'])
        packet = self.store.packet(node_ids=[node['id']])
        self.assertEqual(packet['task']['ref'], task['ref'])
        self.assertEqual(packet['source'], 'frozen-task')
        self.store.update_task(task['ref'], 'cancelled')
        self.assertIn('不重新执行', self.store.handoff(task['ref'])['text'])

    def test_image_source_change_rejected_before_cached_frame(self):
        source = Path(self.tmp.name)/'picture.png'; source.write_bytes(b'changed')
        asset = dict(self.asset, path=str(source), kind='image', frames=1)
        with patch('store.valid_path', return_value=source):
            with self.assertRaisesRegex(ValueError, '原文件已变化'): self.store.frame_file(asset, 0)

    def test_t_drive_root_and_sibling_boundary(self):
        import os
        if os.name == 'nt':self.assertIn(Path('T:/Work素材').resolve(), ALLOWED_ROOTS)
        root = Path(self.tmp.name)/'allowed'; root.mkdir()
        inside = root/'图.png'; inside.write_bytes(b'x')
        sibling = root.with_name('allowed-other'); sibling.mkdir(); outside = sibling/'图.png'; outside.write_bytes(b'x')
        with patch('store.ALLOWED_ROOTS', [root.resolve()]):
            self.assertEqual(valid_path(inside), inside.resolve())
            with self.assertRaises(ValueError): valid_path(outside)

    def test_cli_fresh_session_packet_backup_and_no_accidental_init(self):
        task = self.create()
        cli = Path(__file__).resolve().parents[1]/'canvas_cli.py'
        def run(data, *args):
            return subprocess.run([sys.executable, '-B', '-X', 'utf8', str(cli), '--data-dir', str(data), *args], capture_output=True, text=True, encoding='utf-8')
        result = run(self.tmp.name, '--project', self.store.read()['projectId'], 'packet', '--task', task['ref'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['task']['text'], task['text'])
        backup = Path(self.tmp.name)/'backup.sqlite3'
        self.assertEqual(run(self.tmp.name, 'backup', '--path', str(backup)).returncode, 0)
        con = sqlite3.connect(backup)
        try:
            self.assertEqual(len(json.loads(con.execute('SELECT payload FROM project').fetchone()[0])['tasks']), 1)
        finally:
            con.close()
        missing = Path(self.tmp.name)/'missing'
        self.assertNotEqual(run(missing, 'packet').returncode, 0)
        self.assertFalse(missing.exists())
        self.assertNotEqual(run(self.tmp.name, 'init', '--name', '覆盖').returncode, 0)

    def test_http_context_read_is_nonmutating_and_project_scoped(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler);server.store = self.store;server.daemon_threads = True
        thread = threading.Thread(target=server.serve_forever, daemon=True);thread.start()
        def request(method, path, body=None):
            con = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=5)
            headers = {'Content-Type':'application/json', 'X-Canvas-Client':'web'}
            con.request(method, path, json.dumps(body) if body is not None else None, headers)
            res=con.getresponse();data=res.read();code=res.status;con.close();return code,json.loads(data)
        try:
            before = self.store.read()
            code, data = request('POST','/api/read-context',dict(projectId=before['projectId'],nodeIds=['n1']))
            self.assertEqual(code,200);self.assertEqual(data['assets']['total'],1)
            self.assertEqual(self.store.read(),before)
            self.assertEqual(request('GET','/api/packet?project=PWRONG')[0],400)
            code,t = request('POST','/api/tasks',dict(requestId='web1',text='讨论',nodeIds=['n1'],intent='discuss'))
            self.assertEqual(code,200);self.assertEqual(t['ref'],'T001');self.assertNotIn('input',t)
            self.assertEqual(request('GET','/api/packet?task=T001')[1]['task']['intent'],'discuss')
        finally:
            server.shutdown();server.server_close();thread.join()


if __name__ == '__main__': unittest.main()
