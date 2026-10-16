"""Homepage migration onto the design-system components (MIGRATION-BRIEF, Oct 16, 2026), EN and CN.

Adds css/ds.css component classes to the homepage sections, keeping the legacy classes that scripts depend on
(grade-map.js, phone.js, logo-marquee.js, xpand.js). Above 760px the ds components style these sections; at
760px and below the phone layer (phone.css) keeps its own, token-aligned layout. Idempotent:
  python3 tools/home_ds.py           write index.html and index-cn.html
  python3 tools/home_ds.py --check   report pages that would change
Audit: DESIGN-MIGRATION.md.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (section opening class attribute, extra ds classes)
SECTIONS = [('film-sec', 'ds-section is-alt'), ('programs', 'ds-section'), ('founder-strip hp-lead hp-cred', 'ds-section is-alt'),
            ('pillars', 'ds-section'), ('zl-section-md cf-up hp-next', 'ds-section is-alt'), ('partners', 'ds-section')]
# (exact class attribute, replacement) applied anywhere in main
CLASSES = [
    ('class="sec-head reveal"', 'class="sec-head ds-head reveal"'),
    ('class="hp-cred-head reveal"', 'class="hp-cred-head ds-head reveal"'),
    ('class="film-head reveal"', 'class="film-head ds-head is-center reveal"'),
    ('class="who-row reveal"', 'class="who-row ds-doors reveal"'),
    ('class="who-k"', 'class="who-k ds-eyebrow"'),
    ('class="who-door"', 'class="who-door ds-door"'),
    ('class="prog-grid prog-grid-4"', 'class="prog-grid prog-grid-4 ds-grid ds-grid-4"'),
    ('class="prog-card reveal"', 'class="prog-card ds-card is-media reveal"'),
    ('class="prog-ph"', 'class="prog-ph ds-card-media"'),
    ('class="prog-h"', 'class="prog-h ds-card-h"'),
    ('class="prog-p"', 'class="prog-p ds-card-p"'),
    ('class="prog-grid pillar-row"', 'class="prog-grid pillar-row ds-grid ds-grid-3"'),
    ('class="prog-card pillar-card reveal"', 'class="prog-card pillar-card ds-card reveal"'),
    ('class="cf-evs reveal"', 'class="cf-evs ds-list reveal"'),
    ('class="cf-ev"', 'class="cf-ev ds-list-row"'),
    ('class="hp-cred-grid reveal"', 'class="hp-cred-grid ds-logos reveal"'),
    ('class="reveal partners-lede"', 'class="reveal partners-lede ds-stack"'),
]


def fix_head_inner(s):
    """Inside every ds-head (and the contact lede), the eyebrow, h2 and lede get their ds classes."""
    def inner(m):
        h = m.group(0)
        h = h.replace('<span class="eyebrow">', '<span class="eyebrow ds-eyebrow">')
        h = re.sub(r'<h2 class="h2( [^"]*)?">', lambda x: x.group(0) if 'ds-h2' in x.group(0) else '<h2 class="h2%s ds-h2">' % (x.group(1) or ''), h)
        h = re.sub(r'<p class="lede( [^"]*)?">', lambda x: x.group(0) if 'ds-lede' in x.group(0) else '<p class="lede%s ds-lede">' % (x.group(1) or ''), h)
        return h
    s = re.sub(r'(?s)<div class="[^"]*ds-head[^"]*">.*?</div>', inner, s)
    s = re.sub(r'(?s)<div class="reveal partners-lede ds-stack">.*?<h2[^>]*>.*?</p>', inner, s)
    # cards: the eyebrow inside a ds-card
    s = re.sub(r'(?s)(<article class="prog-card ds-card is-media reveal">.*?)<span class="eyebrow">', lambda m: m.group(1) + '<span class="eyebrow ds-eyebrow">', s)
    return s


def apply(s):
    for legacy, extra in SECTIONS:
        s = re.sub(r'<section class="%s"' % re.escape(legacy), '<section class="%s %s"' % (legacy, extra), s, count=1)
    for a, b in CLASSES:
        s = s.replace(a, b)
    return fix_head_inner(s)


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for f in ('index.html', 'index-cn.html'):
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        t = apply(s)
        if t != s:
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
