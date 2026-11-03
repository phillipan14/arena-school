#!/usr/bin/env python3
"""Serve the riso kits' web root (riso/web) so /fonts, /logos, /art, /card, and /_kit resolve.
Usage: python3 riso/serve.py [port]   (8780 for most kits; 8781 for the isb-coffee and lux-poster-1115 render scripts)"""
import http.server, functools, pathlib, sys
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8780
class Q(http.server.SimpleHTTPRequestHandler):
    def end_headers(self): self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def log_message(self, *a): pass
web = pathlib.Path(__file__).parent / 'web'
print(f'Serving {web} at http://127.0.0.1:{port}/_kit/ (Ctrl+C to stop)')
http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(Q, directory=str(web))).serve_forever()
