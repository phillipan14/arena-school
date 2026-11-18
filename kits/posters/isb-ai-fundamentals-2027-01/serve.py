#!/usr/bin/env python3
"""Local preview: serve /_v3/ from v3/, then out/, then the repo's riso/web fonts and logos, then fall back to the live arenaschool.org for every other asset (cached)."""
import http.server, urllib.request, pathlib, sys
ROOT = pathlib.Path(__file__).parent; OUT = ROOT / 'out'; CACHE = ROOT / '.cache'
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split('?')[0].split('#')[0]
        f = OUT / p.lstrip('/')
        if p.startswith('/_v3/'): f = ROOT / 'v3' / p[len('/_v3/'):]
        if not f.exists() and (ROOT.parents[1] / 'riso' / 'web' / p.lstrip('/')).is_file(): f = ROOT.parents[1] / 'riso' / 'web' / p.lstrip('/')
        if f.is_dir(): f = f / 'index.html'
        if not f.exists() and (OUT / (p.lstrip('/') + '.html')).exists(): f = OUT / (p.lstrip('/') + '.html')
        if not f.exists():
            f = CACHE / (p.lstrip('/') or 'index.html')
            if f.is_dir() or p.endswith('/'): f = f / 'index.html'
            if not f.exists():
                try:
                    data = urllib.request.urlopen('https://arenaschool.org' + p, timeout=30).read()
                except Exception as e:
                    self.send_error(404, str(e)); return
                f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(data)
        b = f.read_bytes(); ext = f.suffix
        ct = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'}.get(ext, 'text/html; charset=utf-8')
        self.send_response(200); self.send_header('Content-Type', ct); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length', len(b)); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 8795), H).serve_forever()
