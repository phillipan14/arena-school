"""Three parent one-pager concepts (RETHINK-BRIEF, Oct 18, 2026). Concepts only; not shipped.
  (a) poster: demo day          (b) a week at Arena          (c) editorial: what your child walks away with
Copy comes from the shipped one-pager's verified sources (tools/one-pager/build.py). Real repo photos only.
  python3 tools/one-pager/concepts/build_concepts.py OUT_DIR      (needs the local server on 127.0.0.1:8931)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))
import build as B  # noqa: E402

PX, PROG = B.PX['en'], B.PROG['en']
TEAM = ['caltech', 'harvard', 'brown', 'tsinghua-lockup', 'isb', 'apple', 'mckinsey', 'goldman', 'yc', 'microsoft-ai', 'deloitte', 'kimi-wordmark']
H = dict(B.STUDIED + B.WORKED)
ROOTCSS = re.search(r'(?s):root\s*\{.*?\n\}', open(os.path.join(ROOT, 'css', 'pro.css'), encoding='utf-8').read()).group(0)
MEM = ('<span class="mem"><span class="ml">A member of</span><img src="/logos/partners/anthropic.svg" alt="Anthropic Startup Program" style="height:2.3mm" />'
       '<img src="/logos/partners/openai.svg" alt="OpenAI Partner Network" style="height:4.2mm" /></span>')
WM = '<img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" />'
WMN = '<img class="wm" src="/logos/arena/wordmark-navy-1600.png" alt="Arena School" />'
TEAMROW = ('<div class="team"><span class="tl">Coached by a team from</span><div class="tg">%s</div></div>'
           % ''.join('<span><img src="/logos/cred/%s.png" alt="" style="height:%smm" /></span>' % (k, H[k]) for k in TEAM))
CTA = ('<footer class="cta"><div><b>Two ways to start.</b><span>Ask your child’s school to bring Arena, or enroll in the Year-Long Project '
       'Mentorship directly.</span></div><div class="ct"><b>phillip@arenaschool.org</b><span>arenaschool.org</span></div></footer>')
NOTE = 'Admissions decisions rest with each university; we do not promise an outcome.'
KEEP = PX['keep']   # (icon, title, line)

BASE = """
@page { size: A4; margin: 0; } * { box-sizing: border-box; }
html, body { margin: 0; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Geist', system-ui, sans-serif; color: #1E2740; font-size: 8.4pt; line-height: 1.4; }
.op { width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; position: relative; }
h1, h2, h3, .serif { font-family: 'Newsreader', Georgia, serif; font-weight: 500; margin: 0; }
em { font-style: italic; } .k { font: 600 7pt/1.2 'Geist', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4A5578; }
.ic { width: 5.4mm; height: 5.4mm; color: var(--pro-action); }
.mem { display: inline-flex; align-items: center; gap: 2.6mm; } .ml { font: 600 7pt/1 'Geist', sans-serif; letter-spacing: .12em; text-transform: uppercase; }
.team { display: grid; grid-template-columns: 46mm 1fr; align-items: center; gap: 4mm; padding: 4mm 12mm; border-top: 1px solid var(--pro-line); }
.team .tl { font: 600 7pt/1.3 'Geist', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4A5578; }
.tg { display: grid; grid-template-columns: repeat(6, 1fr); row-gap: 1.6mm; align-items: center; }
.tg span { display: flex; justify-content: center; } .tg span:nth-child(6n+1) { justify-content: flex-start; } .tg span:nth-child(6n) { justify-content: flex-end; }
.tg img { width: auto; filter: grayscale(1) brightness(0); opacity: .7; }
.cta { display: flex; justify-content: space-between; align-items: center; background: #0B1A4A; color: #fff; padding: 5mm 12mm; }
.cta b { display: block; font: 500 13pt/1.2 'Newsreader', serif; } .cta span { font-size: 8pt; color: rgba(255,255,255,.82); }
.cta .ct { text-align: right; } .cta .ct b { font: 600 9pt/1.3 'Geist', sans-serif; } .cta .ct span { color: #C9D6F2; }
"""

# ---------------------------------------------------------------- (a) poster: demo day
A_CSS = """
.hero { position: relative; height: 190.5mm; background: #0B1A4A; overflow: hidden; }
.hero img.ph { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 60% 30%; }
.hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(11,26,74,.85) 0, rgba(11,26,74,0) 22%, rgba(11,26,74,.15) 50%, rgba(11,26,74,.94) 86%); }
.hero .top { position: absolute; z-index: 2; top: 9mm; left: 12mm; right: 12mm; display: flex; justify-content: space-between; align-items: center; color: #fff; }
.hero .top .wm { height: 5.2mm; } .hero .mem img { filter: brightness(0) invert(1); } .hero .ml { color: #C9D6F2; }
.hero .copy { position: absolute; z-index: 2; left: 12mm; right: 12mm; bottom: 10mm; color: #fff; }
.hero .k { color: #C9D6F2; } .hero h1 { font-size: 30pt; line-height: 1.06; color: #fff; margin: 2.4mm 0 3mm; letter-spacing: -.01em; }
.hero h1 em { color: #C9D6F2; } .hero .lede { font-size: 10pt; color: rgba(255,255,255,.88); max-width: 150mm; margin: 0; }
.hero .cap { position: absolute; z-index: 2; right: 12mm; top: 18mm; font-size: 7pt; color: rgba(255,255,255,.8); }
.story { display: grid; grid-template-columns: 1fr 1.25fr; gap: 9mm; padding: 9mm 12mm 7mm; align-items: start; }
.story .proj { border-left: 3px solid var(--pro-action); padding-left: 5mm; }
.story .proj b { display: block; font: 500 16pt/1.2 'Newsreader', serif; color: var(--pro-ink); margin-top: 2.4mm; }
.story .proj span { display: block; margin-top: 2.4mm; font-size: 8.6pt; color: #3A4466; }
.keep { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm 6mm; }
.keep div { display: grid; grid-template-columns: 6mm 1fr; gap: 0 2.4mm; align-items: start; }
.keep b { font: 500 11pt/1.25 'Newsreader', serif; color: var(--pro-ink); } .keep span { grid-column: 2; font-size: 8.2pt; color: #3A4466; }
.note { padding: 0 12mm 4mm; font-size: 7pt; color: #4A5578; margin: 0; }
"""


def concept_a():
    keep = ''.join('<div>%s<b>%s</b><span>%s</span></div>' % (B.ic(i, 'ic'), t, l) for i, t, l in KEEP)
    return ('<div class="hero"><img class="ph" src="/photos/isb-2026/pitch-duo-1600.webp" alt="" />'
            '<div class="top">%s%s</div><span class="cap">Demo day at the International School of Beijing, 2026</span>'
            '<div class="copy"><span class="k">For families</span><h1>Five days. One real product. <em>Your child on stage.</em></h1>'
            '<p class="lede">Hands-on AI programs where students build and launch a real product, then pitch it to a panel, with mentors '
            'from Harvard, Caltech, Tsinghua, McKinsey, Goldman Sachs, and Y Combinator.</p></div></div>'
            '<section class="story"><div class="proj"><span class="k">Built in five days</span><b>A sign-language-to-speech app.</b>'
            '<span>A student’s project at Bodley Academy, Hong Kong, 2025: a problem they chose, launched within the five-day course.</span></div>'
            '<div><span class="k">What your child keeps</span><div class="keep" style="margin-top:3.4mm">%s</div></div></section>'
            '<p class="note">%s</p>%s%s' % (WM, MEM, keep, NOTE, TEAMROW, CTA))


# ---------------------------------------------------------------- (b) a week at Arena
B_CSS = """
.hd { background: #0B1A4A; color: #fff; padding: 9mm 12mm 8mm; }
.hd .row { display: flex; justify-content: space-between; align-items: center; } .hd .wm { height: 5mm; }
.hd .mem img { filter: brightness(0) invert(1); } .hd .ml { color: #C9D6F2; }
.hd h1 { font-size: 24pt; line-height: 1.1; margin: 7mm 0 2.4mm; } .hd h1 em { color: #C9D6F2; }
.hd p { margin: 0; font-size: 9.4pt; color: rgba(255,255,255,.86); max-width: 160mm; } .hd .k { color: #C9D6F2; display: block; margin-top: 7mm; }
.week { padding: 7mm 12mm 0; }
.film { display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; margin-top: 3.4mm; }
.d { display: flex; flex-direction: column; } .d .im { height: 58mm; border-radius: 1.6mm; overflow: hidden; background: #E6E9F0; }
.d .im img { width: 100%; height: 100%; object-fit: cover; display: block; }
.d .n { margin-top: 2.6mm; font: 600 7pt/1 'Geist', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: var(--pro-action); }
.d b { font: 500 12.5pt/1.2 'Newsreader', serif; color: var(--pro-ink); margin-top: 1.2mm; } .d span { font-size: 8pt; color: #3A4466; margin-top: 1mm; }
.d.top .im { outline: 2.4px solid #0B1A4A; outline-offset: 1.2mm; }
.arrow { height: 1px; background: linear-gradient(90deg, var(--pro-line-2), var(--pro-action)); margin: 4mm 0 0; position: relative; }
.arrow::after { content: ''; position: absolute; right: 0; top: -1.4mm; border: 1.4mm solid transparent; border-left: 2.4mm solid var(--pro-action); }
.dest { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 4mm; padding: 6mm 12mm 3mm; }
.dest div { padding: 3.4mm; border: 1px solid var(--pro-line); border-top: 3px solid #0B1A4A; border-radius: 0 0 1.6mm 1.6mm; }
.dest b { display: block; font: 500 11pt/1.2 'Newsreader', serif; color: var(--pro-ink); margin: 1.6mm 0 1mm; } .dest span { font-size: 8pt; color: #3A4466; }
.tools { display: flex; align-items: center; gap: 4mm; padding: 2mm 12mm 4mm; } .tools img { height: 5.6mm; border-radius: 1mm; }
.note { padding: 0 12mm 3mm; font-size: 7pt; color: #4A5578; margin: 0; } .op > .grow { flex: 1; }
"""
DAYPH = ['mix/pilot-sticky-800.webp', 'mix/pilot-classroom-noscreen-800.webp', 'isb-2026/demo-laptop-800.webp', 'isb-hq/isb-team-slide-800.webp', 'isb-2026/pitch-podium-800.webp']


def concept_b():
    days = ''.join('<div class="d%s"><div class="im"><img src="/photos/%s" alt="" /></div><span class="n">%s</span><b>%s</b><span>%s</span></div>'
                   % (' top' if k == 4 else '', DAYPH[k], dn, t, dd) for k, (dn, t, dd) in enumerate(PROG['days']))
    dest = ''.join('<div>%s<b>%s</b><span>%s</span></div>' % (B.ic(i, 'ic'), t, l) for i, t, l in KEEP)
    tools = ''.join('<img src="/logos/tools/sm/%s.webp" alt="" />' % t for t in B.TOOLS)
    return ('<header class="hd"><div class="row">%s%s</div><span class="k">For families</span>'
            '<h1>A week at Arena: <em>from a problem to a launched product.</em></h1>'
            '<p>The five-day Entrepreneurship &amp; AI Intensive, at your child’s school, with mentors from Harvard, Caltech, Tsinghua, McKinsey, '
            'Goldman Sachs, and Y Combinator.</p></header>'
            '<section class="week"><span class="k">The five days</span><div class="film">%s</div><div class="arrow"></div></section>'
            '<section><div class="dest">%s</div></section><div class="tools"><span class="k">AI tools they use</span>%s</div>'
            '<p class="note">%s</p><div class="grow"></div>%s%s' % (WM, MEM, days, dest, tools, NOTE, TEAMROW, CTA))


# ---------------------------------------------------------------- (c) editorial
C_CSS = """
.mast { display: flex; justify-content: space-between; align-items: center; padding: 9mm 12mm 4mm; border-bottom: 2px solid #0B1A4A; margin: 0 12mm; padding-left: 0; padding-right: 0; }
.mast .wm { height: 5.2mm; } .mast .ml { color: #4A5578; } .mast .mem img { filter: none; }
.lead { display: grid; grid-template-columns: 1.45fr 1fr; gap: 9mm; padding: 8mm 12mm 0; }
.lead .k { color: var(--pro-action); } .lead h1 { font-size: 34pt; line-height: 1.02; color: var(--pro-ink); margin: 3mm 0 4mm; letter-spacing: -.012em; }
.lead h1 em { color: var(--pro-action); } .lead p { font: 400 11pt/1.45 'Newsreader', serif; color: #3A4466; margin: 0; }
.lead figure { margin: 0; } .lead figure img { width: 100%; height: 74mm; object-fit: cover; border-radius: 1.6mm; display: block; }
.lead figcaption { font-size: 7pt; color: #4A5578; margin-top: 1.6mm; }
.body { display: grid; grid-template-columns: 1.45fr 1fr; gap: 9mm; padding: 9mm 12mm 6mm; flex: 1; }
.ol { display: grid; gap: 5mm; }
.ol > div { display: grid; grid-template-columns: 14mm 1fr; border-top: 1px solid var(--pro-line); padding-top: 3.4mm; }
.ol .n { font: 400 24pt/1 'Newsreader', serif; color: var(--pro-action); }
.ol b { font: 500 15pt/1.2 'Newsreader', serif; color: var(--pro-ink); } .ol span { display: block; font-size: 8.8pt; color: #3A4466; margin-top: 1.2mm; }
.side { background: #F3F5FA; border-radius: 1.6mm; padding: 5mm; display: flex; flex-direction: column; gap: 4mm; }
.side .stat b { display: block; font: 400 36pt/1 'Newsreader', serif; color: var(--pro-action); } .side .stat span { font: 400 10pt/1.4 'Newsreader', serif; color: var(--pro-ink); }
.side ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 2mm; }
.side li { display: grid; grid-template-columns: 11mm 1fr; font-size: 8.4pt; color: #3A4466; } .side li i { font-style: normal; font-weight: 600; color: var(--pro-action); }
.side li b { color: var(--pro-ink); font-weight: 600; } .side li.top b { color: #0B1A4A; text-decoration: underline; text-decoration-color: var(--pro-action); text-underline-offset: 2px; }
.note { padding: 0 12mm 3mm; font-size: 7pt; color: #4A5578; margin: 0; }
"""


def concept_c():
    import depth as D
    st = D.STATS['rand-students']
    ol = ''.join('<div><span class="n">%02d</span><div><b>%s</b><span>%s</span></div></div>' % (k + 1, t, l) for k, (i, t, l) in enumerate(KEEP))
    week = ''.join('<li class="%s"><i>%s</i><span><b>%s.</b> %s</span></li>' % ('top' if k == 4 else '', dn.replace('Day ', 'Day '), t, dd) for k, (dn, t, dd) in enumerate(PROG['days']))
    return ('<div class="mast">%s%s</div>'
            '<section class="lead"><div><span class="k">For families</span><h1>What your child <em>walks away with.</em></h1>'
            '<p>Hands-on AI programs where students build and launch a real product, with mentors from Harvard, Caltech, Tsinghua, '
            'McKinsey, Goldman Sachs, and Y Combinator. Four things they keep, for college, summer program, scholarship, and internship '
            'applications.</p></div><figure><img src="/photos/isb-2026/mentor-feedback-1600.webp" alt="" /><figcaption>Mentors respond to a '
            'student’s work, Beijing 2026</figcaption></figure></section>'
            '<section class="body"><div class="ol">%s</div><aside class="side"><div class="stat"><b>%s</b><span>%s</span></div>'
            '<div><span class="k">How they get there: five days</span><ol style="margin-top:2.4mm">%s</ol></div></aside></section>'
            '<p class="note">%s</p>%s%s' % (WMN, MEM, ol, st['n'], st['en'], week, NOTE, TEAMROW, CTA))


def page(body, css):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8" /><title>Concept</title><link rel="stylesheet" href="/fonts/gf.css" />'
            '<style>%s\n%s\n%s</style></head><body><main class="op">%s</main></body></html>' % (ROOTCSS, BASE, css, body))


JS = r"""
const { chromium } = require('playwright');
(async () => { const [src, pdf] = process.argv.slice(1); const b = await chromium.launch(); const p = await b.newPage();
  await p.emulateMedia({ media: 'print' }); await p.goto(src, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => { const m = document.querySelector('.op'); return [...m.children].reduce((a, k) => a + k.getBoundingClientRect().height, 0) - m.getBoundingClientRect().height; });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true }); console.log(Math.round(over)); await b.close(); })();
"""

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for key, fn, css in (('a', concept_a, A_CSS), ('b', concept_b, B_CSS), ('c', concept_c, C_CSS)):
        html = os.path.join(HERE, 'concept-parent-%s.html' % key)
        open(html, 'w', encoding='utf-8').write(page(fn(), css))
        pdf = os.path.join(out, 'concept-parent-%s.pdf' % key)
        r = subprocess.run(['node', '-e', JS, 'http://127.0.0.1:8931/tools/one-pager/concepts/concept-parent-%s.html' % key, pdf],
                           capture_output=True, text=True, cwd=os.path.join(ROOT, '.ds-sync'))
        if r.returncode:
            sys.exit(r.stderr[-800:])
        pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1)
        subprocess.run(['pdftoppm', '-png', '-r', '150', '-singlefile', pdf, os.path.join(out, 'concept-parent-%s' % key)], check=True)
        print('concept %s: pages %s, overflow %spx' % (key, pages, r.stdout.strip()))
