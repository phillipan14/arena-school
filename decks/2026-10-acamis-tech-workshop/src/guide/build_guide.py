"""China-accessible AI tool guide (A4 PDF) for the ACAMIS session page.

Data: guide/tools.json (edit facts there). Output: talks/<slug>/china-ai-tool-guide.pdf
Run:  python3 decks/<slug>/src/guide/build_guide.py
"""
import functools, html, http.server, json, os, sys, threading
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(H))
from site_paths import ROOT, OUT
D = json.load(open(os.path.join(H, 'tools.json'), encoding='utf-8'))
e = html.escape

def section(sec):
    rows = ''.join(
        f'<tr><td class="t"><b>{e(t["name"])}</b><span class="zh">{e(t.get("zh",""))}</span><span class="mk">{e(t["maker"])}</span></td>'
        f'<td class="g">{e(t["good_for"])}</td><td class="u">{e(t["url"])}</td></tr>' for t in sec['tools'])
    return f'<section class="job"><h2>{e(sec["job"])}</h2><table>{rows}</table></section>'

def bullets(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="/fonts/fonts.css"><link rel="stylesheet" href="/fonts/zh/zh.css?v=2">
<style>
@page{{size:A4;margin:16mm 16mm 15mm}}
:root{{--ink:#0B1A4A;--ink2:#2F55A8;--text:#2b3346;--muted:#6b7385;--line:#d9cfc0;--paper:#FBF7F0}}
*{{box-sizing:border-box}}
body{{margin:0;font:400 9.6pt/1.36 Newsreader,Georgia,serif;color:var(--text);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
header{{display:flex;justify-content:space-between;align-items:center;padding-bottom:5mm;border-bottom:1.2pt solid var(--ink)}}
header{{gap:8mm}} header img{{height:10mm}}
header .ev{{white-space:nowrap;font:600 7.2pt/1.3 Newsreader,serif;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);text-align:right}}
h1{{margin:5mm 0 1.5mm;font:500 21pt/1.12 Newsreader,serif;letter-spacing:-.01em;color:var(--ink)}}
h1 em{{font-style:italic;color:var(--ink2)}}
.lede{{margin:0 0 4mm;font-size:10pt;color:var(--text)}}
.job{{break-inside:avoid;margin:0 0 3.5mm}}
h2{{margin:0 0 1.5mm;font:600 8pt/1.2 Newsreader,serif;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}}
table{{width:100%;border-collapse:collapse;border-top:.6pt solid var(--line)}}
td{{padding:1.35mm 2mm 1.35mm 0;border-bottom:.6pt solid var(--line);vertical-align:baseline}}
td.t{{width:36%}} td.t b{{font-weight:600;color:var(--ink)}}
td.t .zh{{margin-left:1.6mm;font-family:'Noto Serif SC','Songti SC',serif;color:var(--ink)}}
td.t .mk{{display:block;font-size:8pt;color:var(--muted)}}
td.g{{width:40%}} td.u{{font-size:8.8pt;color:var(--ink2)}}
.box{{break-inside:avoid;margin:0 0 4.5mm;padding:4mm 5mm;border-radius:2mm;background:var(--paper);border:.6pt solid var(--line)}}
.box h2{{margin-bottom:2mm}} .box p{{margin:0 0 1.5mm}} .box ul{{margin:0;padding-left:4.5mm}} .box li{{margin:0 0 1.2mm}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
footer{{margin-top:3mm;padding-top:3mm;border-top:.6pt solid var(--line);font-size:8.4pt;color:var(--muted);display:flex;justify-content:space-between;gap:6mm}}
footer b{{color:var(--ink)}} footer span:last-child{{white-space:nowrap}}
.pb{{break-before:page}}
</style></head><body>
<header><img src="/decks/img/acamis/a-wordmark-url-navy.png" alt="Arena School, arenaschool.org"><div class="ev">{e(D["event"])}</div></header>
<h1>{D["title_html"]}</h1>
<p class="lede">{D["lede"]}</p>
{''.join(section(s) for s in D["sections"])}
<div class="pb"></div>
<div class="box"><h2>{e(D["blocked"]["h"])}</h2><p>{D["blocked"]["p"]}</p></div>
<div class="box"><h2>{e(D["licensed"]["h"])}</h2><p>{D["licensed"]["p"]}</p></div>
<div class="two">
 <div class="box"><h2>{e(D["before"]["h"])}</h2>{bullets(D["before"]["items"])}</div>
 <div class="box"><h2>{e(D["minors"]["h"])}</h2>{bullets(D["minors"]["items"])}</div>
</div>
<footer><span>{D["footer_left"]}</span><span>{D["footer_right"]}</span></footer>
</body></html>'''

out_html = os.path.join(H, 'guide.html'); open(out_html, 'w', encoding='utf-8').write(page)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
rel = os.path.relpath(out_html, ROOT)
pdf = os.path.join(OUT, 'china-ai-tool-guide.pdf')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/{rel}', wait_until='networkidle'); pg.evaluate('document.fonts.ready')
    pg.pdf(path=pdf, format='A4', print_background=True, prefer_css_page_size=True)
    pg.set_viewport_size({'width': 794, 'height': 1123}); pg.screenshot(path=os.path.join(H, 'preview.png'), full_page=True)
    b.close()
srv.shutdown(); print(os.path.relpath(pdf, ROOT))
