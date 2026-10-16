"""Find dead CSS classes: classes a stylesheet styles that appear nowhere in the site (MIGRATION-BRIEF).

A class is alive if its name appears anywhere in any site HTML file (decks/ and talks/ excluded: they have their
own CSS) or in any site JS file (scripts add classes at runtime, so any occurrence counts). Conservative by design:
a false "alive" only leaves a rule in place.
  python3 tools/css_dead.py styles.css css/index.css ...        prints dead classes per file
  python3 tools/css_dead.py --list styles.css ...               comma list for tools/css_prune.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'decks', 'talks', 'node_modules', '.git', '.ds-sync', '.design-sync'}


def corpus():
    text = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP and not x.startswith('.')]
        for f in files:
            if f.endswith(('.html', '.js')) and not f.endswith('.min.js'):
                text.append(open(os.path.join(d, f), encoding='utf-8', errors='ignore').read())
    return '\n'.join(text)


def classes(css):
    css = re.sub(r'(?s)/\*.*?\*/', '', css)
    sels = re.findall(r'([^{}]+)\{', css)
    out = set()
    for s in sels:
        if s.strip().startswith('@'):
            continue
        out.update(re.findall(r'\.([A-Za-z_][\w-]*)', s))
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--list']
    text = corpus()
    words = set(re.findall(r'[A-Za-z_][\w-]*', text))
    dead_all = set()
    for f in args:
        cls = classes(open(os.path.join(ROOT, f), encoding='utf-8').read())
        dead = sorted(c for c in cls if c not in words)
        dead_all.update(dead)
        if '--list' not in sys.argv:
            print('%-26s %4d classes, %4d dead' % (f, len(cls), len(dead)))
    if '--list' in sys.argv:
        print(','.join(sorted(dead_all)))
