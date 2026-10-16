"""One source for the site header and footer (NAV-BRIEF, Oct 17, 2026).

partials/nav-en.html, nav-cn.html, footer-en.html, footer-cn.html are the only copies. This tool writes them into
every EN and CN site page (card/, decks/, talks/ have their own layouts), then adds the per-page parts:
  - aria-current="page" on every menu link to the current page, and is-current on the first dropdown holding one
  - the language switch, pointing at the page and its twin ({{LANG}} in the partial)
  - the Bootcamp's Lux Scholar co-brand, kept from the page ({{COBRAND}} slot after the lockup)
The phone menu is the same <nav> markup (motion.js opens it), so it can't drift from desktop.
  python3 tools/site_nav.py            write
  python3 tools/site_nav.py --check    lint: exit 1 if any page's header or footer differs from the partials
  python3 tools/site_nav.py --report   per page: Learning approach in the nav menu and footer
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('decks', 'talks', 'card', 'partials', 'node_modules')
NAV_RX = re.compile(r'(?s)<nav class="nav" id="nav">.*?</nav>')
FOOT_RX = re.compile(r'(?s)<footer class="footer">.*?</footer>')
COBRAND_RX = re.compile(r'(?s)\s*<span class="zl-cobrand".*?</span>\s*</span>')


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP and not x.startswith('.'))
        for f in sorted(files):
            if f.endswith('.html'):
                p = os.path.join(d, f)
                if NAV_RX.search(open(p, encoding='utf-8').read()):
                    yield os.path.relpath(p, ROOT)


def urls(rel):
    stem = rel[:-5]
    cn = stem.endswith('-cn')
    en_stem = stem[:-3] if cn else stem
    en = '/' if en_stem == 'index' else '/' + en_stem
    zh = '/' + en_stem + '-cn'
    if not os.path.exists(os.path.join(ROOT, en_stem + '-cn.html')):
        zh = en   # no Chinese twin (pay-mentorship): the switch stays on this page rather than a missing one
    return cn, en, zh, ('/' + stem if stem != 'index' else '/')


def lang(cn, en, zh):
    if cn:
        return ('<div class="lang-switch" role="group" aria-label="语言">\n        <a href="%s">EN</a>\n'
                '        <a href="%s" class="lang-active" aria-current="true">中文</a>\n      </div>') % (en, zh)
    return ('<div class="lang-switch" role="group" aria-label="Language">\n        <a href="%s" class="lang-active" aria-current="true">EN</a>\n'
            '        <a href="%s">中文</a>\n      </div>') % (en, zh)


def mark_current(nav, here):
    link = '<a href="%s">' % here
    nav = nav.replace(link, '<a href="%s" aria-current="page">' % here)
    # the first dropdown that holds a link to this page reads as the current section
    for m in re.finditer(r'(?s)<div class="nav-dd">(.*?)</div></div>', nav):
        if 'aria-current="page"' in m.group(1):
            return nav[:m.start()] + '<div class="nav-dd is-current">' + nav[m.start() + len('<div class="nav-dd">'):]
    return nav


def build(rel, s):
    cn, en, zh, here = urls(rel)
    part = lambda n: open(os.path.join(ROOT, 'partials', '%s-%s.html' % (n, 'cn' if cn else 'en')), encoding='utf-8').read().split('-->', 1)[1].strip()
    old = NAV_RX.search(s).group(0)
    cob = COBRAND_RX.search(old)
    nav = part('nav').replace('{{LANG}}', lang(cn, en, zh)).replace('{{COBRAND}}', cob.group(0) if cob else '')
    nav = mark_current(nav, here)
    s = s.replace(old, nav, 1)
    f = FOOT_RX.search(s)
    if f:
        s = s[:f.start()] + part('footer') + s[f.end():]
    return s


def report():
    bad = 0
    for rel in pages():
        s = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        nav, foot = NAV_RX.search(s).group(0), (FOOT_RX.search(s) or re.search('', '')).group(0)
        cn = rel.endswith('-cn.html')
        href = '/learning-approach-cn' if cn else '/learning-approach'
        menu = ('href="%s"' % href) in re.search(r'(?s)<div class="nav-dd-menu" id="nav-dd-4">.*?</div>', nav).group(0)
        ft = ('href="%s"' % href) in foot
        bad += not (menu and ft)
        print('%-46s nav menu (desktop + phone): %s   footer: %s' % (rel, 'yes' if menu else 'NO', 'yes' if ft else 'NO'))
    print('%d page(s) missing Learning approach' % bad)
    return bad


if __name__ == '__main__':
    if '--report' in sys.argv:
        sys.exit(1 if report() else 0)
    check = '--check' in sys.argv
    n = 0
    for rel in pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding='utf-8').read()
        t = build(rel, s)
        if t != s:
            n += 1
            if check:
                print('differs from partials:', rel)
            else:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
    sys.exit(1 if check and n else 0)
