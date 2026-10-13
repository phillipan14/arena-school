"""Phone layer markup: run from the site root after editing phone.css / phone.js / phone-blocks.

    python3 tools/phone_markup.py           # apply to every page (idempotent; safe to re-run)
    python3 tools/phone_markup.py --check   # report what would change, write nothing

What it does to each page (and nothing else):
  1. adds viewport-fit=cover to the viewport meta (no effect on desktop),
  2. links /phone.css as the LAST thing in <head> and /phone.js before </body>, both with ?v=<content hash>,
  3. inserts phone-only blocks (compact footer; phone.js builds the bottom bar from the hero button) between <!-- phone:start/end --> markers.
Everything it adds is hidden above 760px by phone.css, so desktop renders exactly as before.
Existing markup, ids, classes, and form name= attributes are never changed.
"""
import hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import subprocess; subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'phone_build.py')], check=True)
CHECK = '--check' in sys.argv
PAGES = sorted([f for f in os.listdir(ROOT) if f.endswith('.html')] +
               ['programs/' + f for f in os.listdir(os.path.join(ROOT, 'programs')) if f.endswith('.html')])
CFG = json.load(open(os.path.join(ROOT, 'tools', 'phone_pages.json'), encoding='utf-8'))

def ver(*names):
    h = hashlib.sha1()
    for n in names:
        p = os.path.join(ROOT, n)
        if os.path.exists(p): h.update(open(p, 'rb').read())
    return h.hexdigest()[:8]

V_CSS, V_JS = ver('phone.css'), ver('phone.js')
HEAD_RE = re.compile(r'\n?<link rel="stylesheet" href="/phone\.css[^"]*" data-phone>')
TAIL_RE = re.compile(r'\n?<!-- phone:start -->.*?<!-- phone:end -->', re.S)

def bar(page, cfg, zh):
    a = cfg.get('bar')
    if not a: return ''
    return ('<div class="ph-bar" data-phone hidden><a class="ph-bar-btn" href="%s"%s>%s</a></div>'
            % (html.escape(a['href']), ' data-sheet="lead"' if a.get('sheet') else '', html.escape(a['label'])))

def footer(zh):
    f = CFG['footer']['cn' if zh else 'en']
    rows = ''.join('<li><a class="ph-row" href="%s"%s><span class="ph-row-t">%s</span>%s<svg class="ph-chev" viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5 13 10l-5.5 5.5"/></svg></a></li>'
                   % (html.escape(r['href']), ' target="_blank" rel="noopener"' if r['href'].startswith('http') else '',
                      html.escape(r['label']), ('<span class="ph-row-v">%s</span>' % html.escape(r['value'])) if r.get('value') else '')
                   for r in f['rows'])
    return ('<footer class="ph-foot" data-phone hidden><img class="ph-foot-lock" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" width="180" height="27">'
            '<p class="ph-foot-tag">%s</p><ul class="ph-list ph-list-dark">%s</ul><p class="ph-foot-c">%s</p></footer>'
            % (html.escape(f['tag']), rows, html.escape(f['copy'])))

def process(page):
    path = os.path.join(ROOT, page); s = open(path, encoding='utf-8').read(); o = s
    zh = page.endswith('-cn.html')
    key = page[:-5]; key = key[:-3] if zh else key
    cfg = CFG['pages'].get(key, {})
    # 1. viewport-fit=cover
    s = re.sub(r'(<meta name="viewport" content=")([^"]*)(")',
               lambda m: m.group(1) + (m.group(2) if 'viewport-fit' in m.group(2) else m.group(2).rstrip() + ', viewport-fit=cover') + m.group(3), s, count=1)
    # 2. head link, last in <head>
    s = HEAD_RE.sub('', s)
    i = s.lower().find('</head>')
    s = s[:i] + '<link rel="stylesheet" href="/phone.css?v=%s" data-phone>\n' % V_CSS + s[i:]
    # 3. phone-only blocks + script, just before </body>
    s = TAIL_RE.sub('', s)
    block = '\n<!-- phone:start -->\n%s\n<script src="/phone.js?v=%s" defer data-phone></script>\n<!-- phone:end -->' % (
        footer(zh), V_JS)
    i = s.lower().rfind('</body>')
    s = s[:i].rstrip('\n') + block + '\n' + s[i:]
    if s != o:
        if not CHECK: open(path, 'w', encoding='utf-8').write(s)
        return True
    return False

changed = [p for p in PAGES if process(p)]
print(('Would change' if CHECK else 'Changed'), len(changed), 'of', len(PAGES), 'pages', '| css', V_CSS, 'js', V_JS)
