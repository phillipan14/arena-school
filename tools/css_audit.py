"""Design-system audit: how much of a stylesheet runs on tokens (EDITORIAL-BRIEF item 6, MIGRATION-BRIEF).

For each file: declarations, declarations that use a token (var(--...)), and raw px values that are not a token
(hairlines of 1px or 1.5px are allowed; token definitions on :root and fallbacks inside var() are not counted).
  python3 tools/css_audit.py css/ds.css css/approach.css ...
"""
import re
import sys


def audit(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'(?s)/\*.*?\*/', '', s)
    decls = re.findall(r'(?<=[{;])\s*([a-z-]+)\s*:\s*([^;{}]+)', s)
    decls = [(p, v) for p, v in decls if not p.startswith('--')]
    tok = sum(1 for p, v in decls if 'var(--' in v)
    raw = []
    for p, v in decls:
        v2 = re.sub(r'var\(--[a-z0-9-]+(?:,[^()]*(?:\([^()]*\)[^()]*)*)?\)', '', v)
        for n in re.findall(r'(?<![\w.-])(\d+(?:\.\d+)?)px', v2):
            if n not in ('1', '1.5', '0'):
                raw.append('%s: %s' % (p, v.strip()[:60]))
                break
    return len(decls), tok, raw


if __name__ == '__main__':
    tot = [0, 0, 0]
    for path in sys.argv[1:]:
        n, t, raw = audit(path)
        tot[0] += n; tot[1] += t; tot[2] += len(raw)
        print('%-26s %4d declarations  %4d use tokens (%3d%%)  %3d raw px' % (path, n, t, 100 * t // max(n, 1), len(raw)))
        for r in raw:
            print('    ' + r)
    print('%-26s %4d declarations  %4d use tokens (%3d%%)  %3d raw px' % ('TOTAL', tot[0], tot[1], 100 * tot[1] // max(tot[0], 1), tot[2]))
