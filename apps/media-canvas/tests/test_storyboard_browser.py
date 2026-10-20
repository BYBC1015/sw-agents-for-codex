"""Optional real-browser regression using only synthetic, temporary media."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from PIL import Image, ImageDraw

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from registry import Registry
from server import Handler, ThreadingHTTPServer


@unittest.skipUnless(importlib.util.find_spec('playwright'), 'Optional Playwright is not installed')
class StoryboardBrowserTests(unittest.TestCase):
    def test_edit_shared_change_restore_and_reviewed_download(self):
        from playwright.sync_api import sync_playwright, expect
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();registry=Registry(root/'catalog.sqlite3',root/'work')
            project=registry.create(dict(requestId='demo',name='连续性回归测试'))
            store=registry.store(project['projectId']);count=0
            def write(action,key,**kwargs):
                nonlocal count
                count+=1
                return store.storyboard_write(dict(action=action,id=key,requestId=f'seed-{count}',expectedRevision=store.read()['revision'],**kwargs))
            image=Image.new('RGB',(640,360),'#dde5ed');draw=ImageDraw.Draw(image)
            draw.rectangle((70,90,180,320),fill='#31567d');draw.rectangle((420,60,560,330),fill='#a4a49d')
            source=root/'synthetic.png';image.save(source)
            with patch('store.ALLOWED_ROOTS',[root]):
                asset=store.ingest(dict(requestId='image',files=[dict(path=str(source),mode='copy')]))['assets'][0]
            write('entity','coat',kind='wardrobe',fields=dict(description='蓝色外套',locks=['外套保持蓝色']))
            for n in range(1,7):
                write('shot',f'S{n:02}',fields=dict(title=f'测试镜头 {n}',script='合成测试画面',camera='中景',duration=5,entityRefs={'coat':1} if n<5 else {},outputAssetId=asset['assetId']))
                write('review',f'S{n:02}',shotVersion=1,status='pass',evidence='合成软件测试，不是真实作品验收')
            server=ThreadingHTTPServer(('127.0.0.1',0),Handler);server.registry=registry;server.store=store;server.daemon_threads=True
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                with sync_playwright() as p:
                    browser=p.chromium.launch(headless=True)
                    page=browser.new_page(viewport={'width':1440,'height':1080});errors=[]
                    page.on('pageerror',lambda error:errors.append(str(error)))
                    page.goto(f'http://127.0.0.1:{server.server_port}/?project={project["projectId"]}')
                    page.get_by_role('button',name='分镜与连续性',exact=True).click()
                    expect(page.get_by_role('heading',name='6 个镜头 · 30 秒')).to_be_visible()
                    def row(key):return page.locator('.story-row').filter(has=page.locator('strong').filter(has_text=key))
                    row('S03').get_by_role('button',name='编辑镜头').click()
                    page.get_by_label('机位 / 景别 / 运镜').fill('俯拍')
                    page.get_by_role('button',name='保存新版本').click()
                    expect(row('S03')).to_contain_text('v2');expect(row('S03')).to_contain_text('缺少本镜头版本的输出图')
                    expect(row('S02')).to_contain_text('v1')
                    row('coat').get_by_role('button',name='编辑 / 查看影响').click()
                    expect(page.locator('#story-editor')).to_contain_text('S01、S02、S03、S04')
                    page.get_by_label('设定说明').fill('红色外套')
                    page.get_by_label('必须保留的细节（每行一条）').fill('外套保持红色')
                    page.get_by_role('button',name='保存新版本').click()
                    expect(row('S01')).to_contain_text('使用 v1，当前 v2')
                    row('coat').get_by_label('选定版本').select_option('1')
                    row('coat').get_by_role('button',name='切换到此版本').click()
                    expect(row('S01')).to_contain_text('已通过视觉验收')
                    row('S03').get_by_label('选定版本').select_option('1')
                    row('S03').get_by_role('button',name='切换到此版本').click()
                    expect(row('S03')).to_contain_text('已通过视觉验收')
                    with page.expect_download() as download:
                        page.get_by_role('button',name='导出验收清单',exact=True).click()
                    data=json.loads(Path(download.value.path()).read_text(encoding='utf-8'))
                    self.assertTrue(data['ready']);self.assertEqual(data['shots'][2]['version'],1)
                    self.assertEqual(data['totalDuration'],30);self.assertNotIn('path',json.dumps(data))
                    self.assertEqual(errors,[])
                    browser.close()
            finally:
                server.shutdown();server.server_close();worker.join()


if __name__=='__main__':unittest.main()
