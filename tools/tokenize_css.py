"""Move a stylesheet's literal values onto the design-system tokens (MIGRATION-BRIEF), value for value.

Exact matches only, so nothing moves on screen:
  spacing (padding, margin, gap, inset, top/right/bottom/left): 4 8 12 16 24 32 48 64 96 128px -> var(--space-1..10)
  colour: the brand hexes -> var(--pro-*) tokens
  44px in min-height/min-width/height/width -> var(--tap)
  python3 tools/tokenize_css.py phone/00-base.css ... [--check] [--snap]
--snap also moves off-scale spacing to the nearest step (2-3px visual change) and exact type sizes
(12 14 16 17 19px) onto --text-* tokens: the deliberate part of putting a layer on the system.
"""
import re
import sys

SPACE = {'4': 1, '8': 2, '12': 3, '16': 4, '24': 5, '32': 6, '48': 7, '64': 8, '96': 9, '128': 10}
COLOURS = {'#0b1a4a': 'var(--pro-ink)', '#2f55a8': 'var(--pro-ink-2)', '#22458a': 'var(--pro-action)', '#111827': 'var(--pro-text)',
           '#465066': 'var(--pro-soft)', '#5d6677': 'var(--pro-muted)', '#f5f7fa': 'var(--pro-alt)', '#eef1f6': 'var(--pro-sunk)',
           '#e2e6ee': 'var(--pro-line)', '#cdd3df': 'var(--pro-line-2)', '#c9d6f2': 'var(--pro-tint)'}
SPACE_PROPS = re.compile(r'^(padding|margin|gap|row-gap|column-gap|inset|top|right|bottom|left|padding-[a-z-]+|margin-[a-z-]+|scroll-margin-top)$')
TAP_PROPS = re.compile(r'^(min-height|min-width|height|width)$')
TEXT = {'12': 'xs', '14': 'sm', '16': 'base', '17': 'md', '19': 'lg'}
SNAP = '--snap' in sys.argv


def nearest(n):
    v = float(n)
    if v < 3:
        return None
    k = min(SPACE, key=lambda x: abs(int(x) - v))
    return 'var(--space-%d)' % SPACE[k]


def tokenize(css):
    n = [0]

    def decl(m):
        prop, val = m.group(1), m.group(2)
        if prop.startswith('--'):
            return m.group(0)
        v = val
        if SPACE_PROPS.match(prop):
            v = re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)px\b', lambda x: 'var(--space-%d)' % SPACE[x.group(1)] if x.group(1) in SPACE
                       else ((nearest(x.group(1)) or x.group(0)) if SNAP else x.group(0)), v)
        if SNAP and prop == 'font-size':
            v = re.sub(r'(?<![\w.-])(\d+)px\b', lambda x: 'var(--text-%s)' % TEXT[x.group(1)] if x.group(1) in TEXT else x.group(0), v)
        if TAP_PROPS.match(prop):
            v = re.sub(r'(?<![\w.-])44px\b', 'var(--tap)', v)
        v = re.sub(r'#[0-9a-fA-F]{6}\b', lambda x: COLOURS.get(x.group(0).lower(), x.group(0)), v)
        if v != val:
            n[0] += 1
        return '%s:%s' % (prop, v)
    out = re.sub(r'(?<=[{;\s])([a-z-]+)\s*:\s*([^;{}]+)', decl, css)
    return out, n[0]


if __name__ == '__main__':
    check = '--check' in sys.argv
    for f in [a for a in sys.argv[1:] if a not in ('--check', '--snap')]:
        s = open(f, encoding='utf-8').read()
        t, n = tokenize(s)
        if not check and t != s:
            open(f, 'w', encoding='utf-8').write(t)
        print('%-28s %4d declarations %s' % (f, n, 'would change' if check else 'tokenized'))
