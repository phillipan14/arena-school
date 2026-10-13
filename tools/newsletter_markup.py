"""Arena Notes placements: run from anywhere, BEFORE tools/phone_markup.py (which keeps phone.css last).
    python3 tools/newsletter_markup.py
Adds (idempotently) to every page: newsletter.css in <head> (before phone.css), newsletter.js before the
phone block; and on the pages below, an empty <section class="nl-band" data-nl="KEY"> placeholder that
newsletter.js fills. Program pages get a closing-block button from newsletter.js instead of a band."""
import hashlib, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sorted([f for f in os.listdir(ROOT) if f.endswith('.html')] + ['programs/' + f for f in os.listdir(os.path.join(ROOT, 'programs')) if f.endswith('.html')])
# page (without -cn) -> (band key, regex of the element the band goes BEFORE)
BANDS = {
    'index': ('home', r'<section class="partners" id="contact"'),
    'about': ('about', r'<section[^>]*class="pp-final'),
    'approach': ('approach', r'<section[^>]*class="pp-final'),
    'results': ('results', r'<section[^>]*class="pp-final'),
    'programs/community-dialogues': ('parents', r'<section[^>]*class="pp-final'),
    'programs/conferences': ('conferences', r'<section[^>]*class="pp-final'),
}
def ver(n): return hashlib.sha1(open(os.path.join(ROOT, n), 'rb').read()).hexdigest()[:8]
VC, VJ = ver('newsletter.css'), ver('newsletter.js')
n = 0
for page in PAGES:
    p = os.path.join(ROOT, page); s = open(p, encoding='utf-8').read(); o = s
    key = page[:-5]; key = key[:-3] if key.endswith('-cn') else key
    s = re.sub(r'\n?<link rel="stylesheet" href="/newsletter\.css[^"]*" data-nl>', '', s)
    s = re.sub(r'\n?<script src="/newsletter\.js[^"]*" defer data-nl></script>', '', s)
    s = re.sub(r'<section class="nl-band" data-nl="[a-z]+"></section>\n', '', s)
    link = '<link rel="stylesheet" href="/newsletter.css?v=%s" data-nl>' % VC
    i = s.find('<link rel="stylesheet" href="/phone.css'); i = i if i >= 0 else s.lower().find('</head>')
    s = s[:i] + link + '\n' + s[i:]
    scr = '<script src="/newsletter.js?v=%s" defer data-nl></script>' % VJ
    i = s.find('<!-- phone:start -->'); i = i if i >= 0 else s.lower().rfind('</body>')
    s = s[:i] + scr + '\n' + s[i:]
    if key in BANDS:
        band, rx = BANDS[key]; m = re.search(rx, s)
        if m: s = s[:m.start()] + '<section class="nl-band" data-nl="%s"></section>\n' % band + s[m.start():]
        else: print('WARNING: no anchor for band on', page)
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('newsletter markup: changed', n, 'of', len(PAGES), 'pages | css', VC, 'js', VJ)
