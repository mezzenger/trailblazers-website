#!/usr/bin/env python3
"""Serve a production build at its GitHub Pages project path for browser review."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
build = root / 'dist'
target = root / '.browser-preview' / 'trailblazers-website'
if not (build / 'index.html').exists():
    raise SystemExit('Run npm run build before browser review.')
if target.exists():
    shutil.rmtree(target)
target.parent.mkdir(exist_ok=True)
shutil.copytree(build, target)
print('Serving production build at http://127.0.0.1:8000/trailblazers-website/', flush=True)
handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(target.parent), **kwargs)
ThreadingHTTPServer(('127.0.0.1', 8000), handler).serve_forever()
