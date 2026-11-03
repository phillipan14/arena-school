"""List text blocks whose last line holds a single word (orphans) in an Arena print doc."""
import http.server, threading, functools, pathlib, sys
from playwright.sync_api import sync_playwright
KIT = pathlib.Path(__file__).parent; src = pathlib.Path(sys.argv[1]).resolve()
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(KIT / 'site')))
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = r"""(()=>{const out=[];const pages=[...document.querySelectorAll('.pg')];
document.querySelectorAll('p,li,td,h1,h2,h3,.nm,.cap,.sub,.out,.day span,.lede').forEach(el=>{
  if([...el.children].some(c=>['P','LI','TD','DIV','TABLE','UL','OL'].includes(c.tagName)))return;
  const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const words=[];let n;
  while(n=w.nextNode()){const re=/\S+/g;let m;while(m=re.exec(n.data)){const r=document.createRange();r.setStart(n,m.index);r.setEnd(n,m.index+m[0].length);const b=r.getClientRects()[0];if(b)words.push({t:m[0],y:Math.round(b.top)})}}
  if(words.length<3)return;const lines=[...new Set(words.map(x=>x.y))];if(lines.length<2)return;
  const last=lines[lines.length-1];const lw=words.filter(x=>Math.abs(x.y-last)<3);
  if(lw.length===1){const pg=pages.findIndex(p=>p.contains(el))+1;out.push('p'+pg+': "'+el.textContent.trim().slice(0,70)+'…" -> last line: '+lw[0].t)}});return out})()"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123})
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/fonts/gf.css'); pg.set_content(src.read_text(), wait_until='networkidle')
    pg.emulate_media(media='print'); pg.evaluate('document.fonts.ready')
    res = pg.evaluate(JS); print('\n'.join(res) if res else 'no orphans')
    b.close()
srv.shutdown()
