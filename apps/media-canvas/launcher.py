"""Start or reuse this local Canvas without changing project data."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from urllib.request import urlopen
import webbrowser
from settings import VERSION, DEFAULT_DATA, DEFAULT_REGISTRY, DEFAULT_WORKSPACE


def start_background(command, data):
    """WMI owns the Windows server so shell/process-tree cleanup cannot own it."""
    if os.name != 'nt':
        return subprocess.Popen(command, stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                start_new_session=True).pid
    # Values travel as JSON on stdin, never interpolated as PowerShell source.
    script = r"""
$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [Text.UTF8Encoding]::new()
$request = [Console]::In.ReadToEnd() | ConvertFrom-Json
$startup = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{
    ShowWindow = [uint16]0
    CreateFlags = [uint32]0x09000400
    EnvironmentVariables = [string[]]$request.environment
}
$result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{
    CommandLine = [string]$request.command
    CurrentDirectory = [string]$request.directory
    ProcessStartupInformation = $startup
}
if ($result.ReturnValue -ne 0) { throw "Canvas background start failed: $($result.ReturnValue)" }
[Console]::Write($result.ProcessId)
"""
    allowed = {
        'PATH', 'SYSTEMROOT', 'WINDIR', 'SYSTEMDRIVE', 'USERPROFILE', 'HOMEDRIVE',
        'HOMEPATH', 'TEMP', 'TMP', 'APPDATA', 'LOCALAPPDATA', 'PROGRAMDATA',
        'MEDIA_CANVAS_MEDIA_ROOTS', 'MEDIA_CANVAS_FFMPEG', 'MEDIA_CANVAS_FFPROBE',
        'MEDIA_CANVAS_HOME', 'MEDIA_CANVAS_DATA', 'MEDIA_CANVAS_REGISTRY', 'MEDIA_CANVAS_WORKSPACE',
    }
    request = dict(command=subprocess.list2cmdline(command), directory=str(data),
                   environment=[f'{k}={v}' for k,v in os.environ.items() if k.upper() in allowed])
    powershell = Path(os.environ['SYSTEMROOT'])/'System32/WindowsPowerShell/v1.0/powershell.exe'
    result = subprocess.run(
        [str(powershell), '-NoProfile', '-NonInteractive', '-Command', script],
        input=json.dumps(request), capture_output=True, text=True, encoding='utf-8',
        creationflags=subprocess.CREATE_NO_WINDOW, timeout=25)
    if result.returncode:
        raise RuntimeError('Canvas 后台启动失败（Windows WMI）；请检查本机 WMI 服务。\n'+result.stderr.strip())
    return int(result.stdout.strip())


def serve(args, data, registry):
    """Own log files in the detached process, including startup failures."""
    data.mkdir(parents=True, exist_ok=True)
    with (data/'server.log').open('a', encoding='utf-8', buffering=1) as out, \
         (data/'server-error.log').open('a', encoding='utf-8', buffering=1) as err:
        sys.stdout, sys.stderr = out, err
        print(f'{datetime.now(timezone.utc).isoformat()} start pid={os.getpid()} version={VERSION}')
        try:
            from server import main as server_main
            server_main(['--port', str(args.port), '--data-dir', str(data),
                         '--registry', str(registry), '--workspace-root', str(args.workspace_root.resolve())])
        except BaseException:
            traceback.print_exc()
            raise SystemExit(1)
        finally:
            print(f'{datetime.now(timezone.utc).isoformat()} stop pid={os.getpid()}')
            sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('--port',type=int,default=8961)
    parser.add_argument('--data-dir',type=Path,default=DEFAULT_DATA)
    parser.add_argument('--registry',type=Path,default=DEFAULT_REGISTRY)
    parser.add_argument('--workspace-root',type=Path,default=DEFAULT_WORKSPACE)
    parser.add_argument('--serve', action='store_true', help=argparse.SUPPRESS)
    args=parser.parse_args()
    if not 1<=args.port<=65535:parser.error('port must be 1–65535')
    url=f'http://127.0.0.1:{args.port}/'
    data=args.data_dir.resolve();registry=args.registry.resolve()
    if args.serve:
        serve(args, data, registry)
        return
    def check():
        with urlopen(url+'api/health',timeout=2) as response:health=json.load(response)
        if health.get('app')!='media-canvas' or health.get('version')!=VERSION or Path(health['dataDir']).resolve()!=data or Path(health['registry']).resolve()!=registry:
            raise ValueError('端口已有其他版本或项目服务；请关闭原服务，或指定另一个端口。')
    with socket.socket() as probe:
        in_use=probe.connect_ex(('127.0.0.1',args.port))==0
    if in_use:check()
    else:
        data.mkdir(parents=True,exist_ok=True)
        pid=start_background([sys.executable,'-B','-X','utf8',str(Path(__file__).resolve()),'--serve',
            '--port',str(args.port),'--data-dir',str(data),'--registry',str(registry),
            '--workspace-root',str(args.workspace_root.resolve())],data)
        (data/'server.pid').write_text(str(pid),encoding='ascii')
        for _ in range(50):
            try:check();break
            except (OSError,TimeoutError):
                time.sleep(.2)
        else:raise RuntimeError('Canvas 尚未就绪，请查看服务日志')
    if not args.no_browser:webbrowser.open(url)
    print(url)

if __name__=='__main__':main()
