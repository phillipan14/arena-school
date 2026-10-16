"""Shared helper: serve the repo root on a free port and open the deck in export (final) state."""
import functools, http.server, threading, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','..'))
SLUG=os.path.basename(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
class _Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
def serve():
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(_Q,directory=ROOT))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    return f'http://127.0.0.1:{srv.server_address[1]}/talks/{SLUG}/deck.html?stage'
def open_export(pg,url):
    pg.goto(url,wait_until='networkidle');pg.evaluate('document.fonts.ready');pg.wait_for_timeout(500)
    pg.evaluate("document.documentElement.classList.add('export');window.__space&&window.__space()");pg.wait_for_timeout(400)
def goto(pg,n):
    pg.evaluate(f"document.getElementById('deck').scrollTop=document.querySelectorAll('section.s')[{n-1}].offsetTop");pg.wait_for_timeout(300)
