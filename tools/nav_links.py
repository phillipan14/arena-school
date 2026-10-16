"""Sitewide nav + footer links for the Learning approach page (EDITORIAL-BRIEF, Oct 16, 2026).

Adds "Learning approach" under About in the desktop nav dropdown (also the phone menu, which reuses the same
markup) and in the footer About column, on every EN and CN site page (decks/, talks/ and card/ are left alone).
Idempotent:
  python3 tools/nav_links.py           write
  python3 tools/nav_links.py --check   report pages that would change
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('decks', 'talks', 'card', 'node_modules', '.ds-sync', '.design-sync')

EN = [('<a href="/approach"><b>Our approach</b><span>Agency, taste, and craft</span></a>',
       '<a href="/learning-approach"><b>Learning approach</b><span>Framework, outcomes, assessment</span></a>'),
      ('<a href="/approach">Our approach</a>', '<a href="/learning-approach">Learning approach</a>')]
CN = [('<a href="/approach-cn"><b>教学理念</b><span>主动性、审美与匠心</span></a>',
       '<a href="/learning-approach-cn"><b>学习方法</b><span>框架、成果与评估</span></a>'),
      ('<a href="/approach-cn">教学理念</a>', '<a href="/learning-approach-cn">学习方法</a>')]


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP and not x.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(d, f)


def fix(s):
    for anchor, add in EN + CN:
        if anchor in s and add not in s:
            s = s.replace(anchor, anchor + add)
    return s


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for p in pages():
        s = open(p, encoding='utf-8').read()
        t = fix(s)
        if t != s:
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
