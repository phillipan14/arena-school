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


if __name__ == '__main__':
    os.chdir(ROOT)
    link = '<link rel="stylesheet" href="/css/pro.css?v=%s" data-pro>' % ver('css/pro.css')
    changed = 0
    for page in pages():
        s = open(page, encoding='utf-8').read()
        if '</head>' not in s:
            continue
        o = s
        s = re.sub(r'\n?<link rel="stylesheet" href="/css/pro\.css[^"]*" data-pro>', '', s)
        s = LOCAL_CSS.sub(stamp, s)
        # before the newsletter/promo pair and phone.css, which their own tools re-insert just before phone.css
        at = -1
        for anchor in ('<link rel="stylesheet" href="/newsletter.css', '<link rel="stylesheet" href="/phone.css', '</head>'):
            at = s.find(anchor)
            if at != -1:
                break
        s = s[:at] + link + '\n' + s[at:]
        if s != o:
            changed += 1
            if not CHECK:
                open(page, 'w', encoding='utf-8').write(s)
    print(('Would change' if CHECK else 'Changed'), changed, 'pages | pro.css', ver('css/pro.css'))
