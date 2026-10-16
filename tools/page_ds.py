"""Page migration onto the design-system components (MIGRATION-BRIEF, Oct 16, 2026), by page group, EN and CN.

Adds css/ds.css classes beside the legacy ones (scripts keep working):
  sections  zl-section / pc-sec / el-sec / team-sec / pc-proof / pp-final ...  -> ds-section (+ is-alt for bands)
  heads     sec-head / pg-head / el-head / hp-cred-head / pc-proof-head        -> ds-head (only when the head sits
            directly in a plain <div class="container"> or <div class="el-wrap">; heads inside layout grids keep
            their grid) with ds-eyebrow / ds-h2 / ds-lede inside
  FAQ       .faq                                                              -> ds-faq
Above 760px the ds rules win; the phone layer keeps phones until each group's phone pass.
  python3 tools/page_ds.py GROUP [--check]     groups: programs, teachers, schools, about, events
Audit: DESIGN-MIGRATION.md.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUPS = {
    'programs': ['programs/product-intensive', 'programs/remake-your-favorite-app', 'programs/website-portfolio-workshop', 'mentorship', 'zero-to-launch'],
    'teachers': ['programs/teacher-training', 'schools/technology', 'programs/conferences', 'programs/community-dialogues'],
    'schools': ['schools', 'partnerships', 'results'],
    'about': ['about', 'contact', 'enroll'],
    'events': ['events/isb-winter-2027', 'events/acamis-tech-2026', 'events/isb-parent-coffee'],
}
BANDS = ('section-alt', 'is-hi')
SECTION_RX = re.compile(r'<section class="((?:zl-section|el-sec|founder-strip|hp-cred|pp-final|who|zl-section-md)\b[^"]*)"')
HEAD_RX = re.compile(r'(<div class="(?:container|el-wrap)">\s*)<div class="((?:sec-head|pg-head|el-head|hp-cred-head|pc-proof-head)\b[^"]*)"')


def fix_head_inner(h):
    h = re.sub(r'<span class="eyebrow">', '<span class="eyebrow ds-eyebrow">', h)
    h = re.sub(r'<h2 class="([^"]*)">', lambda x: x.group(0) if 'ds-h2' in x.group(1) else '<h2 class="%s ds-h2">' % x.group(1), h)
    h = re.sub(r'<p class="(lede[^"]*)">', lambda x: x.group(0) if 'ds-lede' in x.group(1) else '<p class="%s ds-lede">' % x.group(1), h)
    return h


def apply(s):
    def sec(m):
        cls = m.group(1)
        if 'ds-section' in cls.split():
            return m.group(0)
        extra = ' ds-section' + (' is-alt' if any(b in cls.split() for b in BANDS) else '')
        return '<section class="%s%s"' % (cls, extra)
    s = SECTION_RX.sub(sec, s)

    def head(m):
        cls = m.group(2)
        if 'ds-head' in cls.split():
            return m.group(0)
        return '%s<div class="%s"' % (m.group(1), cls.replace('reveal', 'ds-head reveal') if 'reveal' in cls else cls + ' ds-head')
    s = HEAD_RX.sub(head, s)
    s = re.sub(r'(?s)<div class="[^"]*\bds-head\b[^"]*">.*?</div>', lambda m: fix_head_inner(m.group(0)), s)
    s = re.sub(r'class="faq( [^"]*)?"', lambda m: m.group(0) if 'ds-faq' in m.group(0) else 'class="faq%s ds-faq"' % (m.group(1) or ''), s)
    return s


if __name__ == '__main__':
    group = sys.argv[1]
    check = '--check' in sys.argv
    n = 0
    for stem in GROUPS[group]:
        for f in (stem + '.html', stem + '-cn.html'):
            p = os.path.join(ROOT, f)
            if not os.path.exists(p):
                continue
            s = open(p, encoding='utf-8').read()
            t = apply(s)
            if t != s:
                n += 1
                if not check:
                    open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
