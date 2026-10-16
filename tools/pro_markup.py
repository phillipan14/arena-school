"""Pro pass (2026-10-16): link /css/pro.css on every site page (just before the newsletter/promo/phone
links, which their tools keep at the end of <head>), and stamp every
shared stylesheet href with a content hash so browsers pick up recolored files. Site pages only
(decks/, talks/, review/ are never touched). Run after newsletter_markup.py and phone_markup.py:
    python3 tools/pro_markup.py          # rewrite
    python3 tools/pro_markup.py --check  # report"""
import hashlib, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = '--check' in sys.argv
LOCAL_CSS = re.compile(r'href="/((?:styles|riso-theme|mobile)\.css|css/[a-z0-9-]+\.css)(?:\?v=[^"]*)?"')


def ver(path):
    return hashlib.sha1(open(os.path.join(ROOT, path), 'rb').read()).hexdigest()[:8]


def pages():
    out = subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return [f for f in out if not re.match(r'(decks|talks|review|case-study-examples|onepager)/', f)]


def stamp(m):
    path = m.group(1)
    if not os.path.exists(os.path.join(ROOT, path)):
        return m.group(0)
    return 'href="/%s?v=%s"' % (path, ver(path))


JS_FLAG = ('<script data-pro>(function(d){d.classList.add("js");'
           # reserve the winter banner's 40px from the first paint (promo.js fills it): no layout shift
           'try{if(self===top&&sessionStorage.getItem("arena.promo.bar")!=="x"&&new Date(Date.now()+288e5).toISOString().slice(0,10)<="2027-01-08")d.classList.add("promo-pending")}catch(e){}'
           '})(document.documentElement)</script>')
DEAD = re.compile(r'<script src="/(?:riso-field|hero-options|riso-interact|riso-particles)\.js[^"]*"[^>]*></script>\n')


def lazy_imgs(seg):
    """Below-the-fold <img> without a loading attribute: lazy and async-decoded."""
    def fix(m):
        tag = m.group(0)
        if 'loading=' in tag:
            return tag
        return tag[:4] + ' loading="lazy" decoding="async"' + tag[4:] if 'decoding=' not in tag else tag[:4] + ' loading="lazy"' + tag[4:]
    return re.sub(r'<img\b[^>]*>', fix, seg)


def polish(s):
    """Perf/UX polish (RES-BRIEF, Oct 16) for pages with the cine hero: an html.js flag so scroll reveals
    never hide content when JS fails, no scripts whose targets are gone, and lazy images after the hero."""
    if 'cine-hero' not in s:
        return s
    s = re.sub(r'<script data-pro>.*?</script>\n', '', s)
    s = re.sub(r'(<meta charset="[^"]*"\s*/?>\n)', lambda m: m.group(1) + JS_FLAG + '\n', s, count=1)
    s = DEAD.sub('', s)
    a = s.find('</section>', s.find('cine-hero'))
    z = s.find('<!-- phone:start -->')   # the phone block belongs to phone_markup.py
    z = z if z != -1 else len(s)
    if a != -1 and a < z:
        s = s[:a] + lazy_imgs(s[a:z]) + s[z:]
    return s


if __name__ == '__main__':
    os.chdir(ROOT)
    # pro.css (tokens + polish) then ds.css (the component layer, MIGRATION-BRIEF), on every site page
    link = ('<link rel="stylesheet" href="/css/pro.css?v=%s" data-pro>\n<link rel="stylesheet" href="/css/ds.css?v=%s" data-ds>'
            % (ver('css/pro.css'), ver('css/ds.css')))
    changed = 0
    for page in pages():
        s = open(page, encoding='utf-8').read()
        if '</head>' not in s:
            continue
        o = s
        s = re.sub(r'\n?<link rel="stylesheet" href="/css/pro\.css[^"]*" data-pro>', '', s)
        s = re.sub(r'\n?<link rel="stylesheet" href="/css/ds\.css[^"]*"( data-ds| /)?>', '', s)
        s = LOCAL_CSS.sub(stamp, s)
        # before the newsletter/promo pair and phone.css, which their own tools re-insert just before phone.css
        at = -1
        for anchor in ('<link rel="stylesheet" href="/newsletter.css', '<link rel="stylesheet" href="/phone.css', '</head>'):
            at = s.find(anchor)
            if at != -1:
                break
        s = s[:at] + link + '\n' + s[at:]
        s = polish(s)
        if s != o:
            changed += 1
            if not CHECK:
                open(page, 'w', encoding='utf-8').write(s)
    print(('Would change' if CHECK else 'Changed'), changed, 'pages | pro.css', ver('css/pro.css'))
