"""Internal link check over every site HTML file (EDITORIAL-BRIEF, Oct 16, 2026).

Resolves each internal href/src the way the site is served (clean URLs: /about -> about.html, /x/ -> x/index.html,
/ -> index.html; files as-is; ?query and #fragment ignored; #fragment-only links checked against ids on the page).
Skips decks/ and talks/ (their own builds), external links, mailto:, tel:, javascript: and data: URLs.
  python3 tools/link_check.py   prints broken links and exits 1 if any
"""
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'decks', 'talks', 'node_modules', '.git', '.ds-sync', '.design-sync', 'case-study-examples', 'review'}
ATTR = re.compile(r'\s(?:href|src)="([^"]+)"')
# script hooks, not targets: newsletter.js opens the signup sheet on #nl, phone.js opens the menu on #ph-menu
RUNTIME = {'#nl', '#ph-menu'}


def site_pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP and not x.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                yield os.path.relpath(os.path.join(d, f), ROOT)


def resolves(path):
    path = unquote(path.split('#')[0].split('?')[0])
    if path in ('', '/'):
        return os.path.exists(os.path.join(ROOT, 'index.html'))
    rel = path.lstrip('/')
    full = os.path.join(ROOT, rel)
    if os.path.isfile(full):
        return True
    if path.endswith('/'):
        return os.path.isfile(os.path.join(full, 'index.html'))
    return os.path.isfile(full + '.html') or os.path.isfile(os.path.join(full, 'index.html'))


def main():
    broken = []
    pages = sorted(site_pages())
    for page in pages:
        s = open(os.path.join(ROOT, page), encoding='utf-8').read()
        s = re.sub(r'(?s)<script\b[^>]*>.*?</script>', '', s)   # links built in scripts are not markup links
        ids = set(re.findall(r'\sid="([^"]+)"', s))
        for url in ATTR.findall(s):
            if url.startswith(('http:', 'https:', 'mailto:', 'tel:', 'javascript:', 'data:', '//', '{{')):
                continue
            if url in RUNTIME:
                continue
            if url.startswith('#'):
                if len(url) > 1 and url[1:] not in ids:
                    broken.append((page, url))
                continue
            if url.startswith('/'):
                if not resolves(url):
                    broken.append((page, url))
            else:  # relative to the page
                base = os.path.dirname(page)
                if not resolves('/' + os.path.normpath(os.path.join(base, url)).replace(os.sep, '/')):
                    broken.append((page, url))
    for page, url in broken:
        print('BROKEN %-40s %s' % (page, url))
    print('%d pages checked, %d broken internal links' % (len(pages), len(broken)))
    return 1 if broken else 0


if __name__ == '__main__':
    sys.exit(main())
