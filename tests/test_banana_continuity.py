import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('banana_continuity',ROOT/'banana-pro/scripts/generate_openrouter_image.py')
banana=importlib.util.module_from_spec(spec);spec.loader.exec_module(banana)


class LockTests(unittest.TestCase):
    def test_long_description_and_retry_preserve_every_locked_item(self):
        locked=['外套为蓝色','左手拿灯，灯芯始终位于玻璃罩内','主标题必须保留“归家”']
        prompt='场景：'+('雨夜街道，电影构图。'*1000)
        normal, compressed=banana._protected_prompt(prompt,locked,1000)
        retry=banana._retry_prompt(prompt,locked,1000)
        self.assertTrue(compressed)
        self.assertLessEqual(len(normal),1000)
        for lock in locked:
            self.assertIn(lock,normal);self.assertIn(lock,retry)
        self.assertNotIn('no text',retry)

    def test_over_budget_constraints_fail_instead_of_truncating(self):
        with self.assertRaises(ValueError):banana._protected_prompt('描述'*500,['身份锁定'*300],900)
        full,_=banana._protected_prompt('描述',['身份锁定'*300],900,False)
        self.assertIn('身份锁定'*300,full)

    def test_inline_locks_survive_legacy_callers(self):
        prompt='场景：'+'雨夜'*1500+'\n禁止：改变主角的脸\n锁定：红色围巾'
        sent,_=banana._protected_prompt(prompt,[],900)
        self.assertIn('禁止：改变主角的脸',sent)
        self.assertIn('锁定：红色围巾',sent)

    def test_cli_dry_run_consumes_canvas_packet_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);packet=root/'packet.json';packet.write_text(json.dumps({'locks':['蓝外套'],'issues':[]}),encoding='utf-8')
            args=['banana','--prompt','回家的人','--lock-file',str(packet),'--output-dir',str(root/'out'),'--dry-run']
            with patch.object(sys,'argv',args),patch.object(banana,'_post_json') as post,contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(banana.main(),0)
                post.assert_not_called()
            sent=(root/'out/banana_prompt_used.txt').read_text(encoding='utf-8')
            self.assertIn('蓝外套',sent)
            packet.write_text(json.dumps({'locks':['蓝外套'],'issues':[{'type':'dependency'}]}),encoding='utf-8')
            with patch.object(sys,'argv',args),patch.object(banana,'_post_json') as post:
                with self.assertRaises(ValueError):banana.main()
                post.assert_not_called()

    def test_empty_result_paid_retry_receives_locks_and_requested_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);packet=root/'locks.json';packet.write_text('["主标题保留归家", "蓝外套"]',encoding='utf-8')
            args=['banana','--prompt','场景：'+'夜景'*1500,'--lock-file',str(packet),'--output-dir',str(root/'out')]
            payloads=[]
            def capture(payload,*args):payloads.append(payload);return {'choices':[{'message':{}}]}
            with patch.object(sys,'argv',args),patch.object(banana,'_post_json',side_effect=capture),patch.object(banana,'_read_api_key',return_value='fake-test-key'),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(banana.main(),3)
            self.assertEqual(len(payloads),2)
            for payload in payloads:
                content=payload['messages'][0]['content']
                self.assertIn('主标题保留归家',content);self.assertIn('蓝外套',content)


if __name__=='__main__':unittest.main()
