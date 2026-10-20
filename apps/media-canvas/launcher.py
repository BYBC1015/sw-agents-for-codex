"""Start or reuse this local Canvas without changing project data."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import urlopen
import webbrowser
from settings import VERSION, DEFAULT_DATA, DEFAULT_REGISTRY, DEFAULT_WORKSPACE


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('--port',type=int,default=8961)
    parser.add_argument('--data-dir',type=Path,default=DEFAULT_DATA)
    parser.add_argument('--registry',type=Path,default=DEFAULT_REGISTRY)
    parser.add_argument('--workspace-root',type=Path,default=DEFAULT_WORKSPACE)
    args=parser.parse_args()
    if not 1<=args.port<=65535:parser.error('port must be 1–65535')
    url=f'http://127.0.0.1:{args.port}/'
    data=args.data_dir.resolve();registry=args.registry.resolve()
    def check():
        with urlopen(url+'api/health',timeout=2) as response:health=json.load(response)
        if health.get('app')!='media-canvas' or health.get('version')!=VERSION or Path(health['dataDir']).resolve()!=data or Path(health['registry']).resolve()!=registry:
            raise ValueError('端口已有其他版本或项目服务；请关闭原服务，或指定另一个端口。')
    with socket.socket() as probe:
        in_use=probe.connect_ex(('127.0.0.1',args.port))==0
    if in_use:check()
    else:
        data.mkdir(parents=True,exist_ok=True)
        with (data/'server.log').open('ab') as out,(data/'server-error.log').open('ab') as err:
            process=subprocess.Popen([sys.executable,'-B','-X','utf8',str(Path(__file__).with_name('server.py')),
                '--port',str(args.port),'--data-dir',str(data),'--registry',str(registry),'--workspace-root',str(args.workspace_root.resolve())],
                stdin=subprocess.DEVNULL,stdout=out,stderr=err,
                creationflags=0x08000000 if os.name=='nt' else 0,start_new_session=os.name!='nt')
        (data/'server.pid').write_text(str(process.pid),encoding='ascii')
        for _ in range(50):
            try:check();break
            except (OSError,TimeoutError):
                if process.poll() is not None:raise RuntimeError('Canvas 启动失败，请查看 server-error.log')
                time.sleep(.2)
        else:raise RuntimeError('Canvas 尚未就绪，请查看服务日志')
    if not args.no_browser:webbrowser.open(url)
    print(url)

if __name__=='__main__':main()
