"""Portable defaults; preserve established Windows locations when they exist."""
import json
import os
from pathlib import Path
import shutil

VERSION = '0.4.0'
HOME = Path(os.environ.get('MEDIA_CANVAS_HOME', str(Path.home() / 'SWCanvas'))).expanduser().resolve()
LEGACY_WORKSPACE = Path('T:/Work素材')
LEGACY_DATA = Path('E:/Downloads/制作画布_项目数据')
DEFAULT_WORKSPACE = Path(os.environ.get('MEDIA_CANVAS_WORKSPACE', str(LEGACY_WORKSPACE if os.name == 'nt' and LEGACY_WORKSPACE.is_dir() else HOME / 'projects'))).expanduser().resolve()
DEFAULT_DATA = Path(os.environ.get('MEDIA_CANVAS_DATA', str(LEGACY_DATA if os.name == 'nt' and LEGACY_DATA.is_dir() else HOME / 'default'))).expanduser().resolve()
DEFAULT_REGISTRY = Path(os.environ.get('MEDIA_CANVAS_REGISTRY', str(DEFAULT_WORKSPACE / '.media-canvas' / 'catalog.sqlite3'))).expanduser().resolve()
ALLOWED_ROOTS = [DEFAULT_WORKSPACE, Path.home() / 'Downloads']
if os.name == 'nt':
    ALLOWED_ROOTS.extend([Path('T:/Work素材'), Path('E:/Downloads')])
if os.environ.get('MEDIA_CANVAS_MEDIA_ROOTS'):
    roots = json.loads(os.environ['MEDIA_CANVAS_MEDIA_ROOTS'])
    if not isinstance(roots, list) or not all(isinstance(p, str) and p for p in roots):
        raise ValueError('MEDIA_CANVAS_MEDIA_ROOTS must be a JSON array of paths')
    ALLOWED_ROOTS.extend(Path(p).expanduser() for p in roots)
ALLOWED_ROOTS = [p.resolve() for p in ALLOWED_ROOTS]
FFMPEG = Path(os.environ.get('MEDIA_CANVAS_FFMPEG') or shutil.which('ffmpeg') or ('C:/Program Files/FFmpeg/ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'))
FFPROBE = Path(os.environ.get('MEDIA_CANVAS_FFPROBE') or shutil.which('ffprobe') or str(FFMPEG.with_name('ffprobe.exe' if os.name == 'nt' else 'ffprobe')))

if __name__ == '__main__':
    print(json.dumps(dict(version=VERSION,data=str(DEFAULT_DATA),registry=str(DEFAULT_REGISTRY),workspace=str(DEFAULT_WORKSPACE)),ensure_ascii=False))
