"""Report for tools/hero_motion_check.mjs: each 2s pair of frames must differ visibly in the hero photo, and the
photo on screen must change within 4s; sharpness = source px per CSS px at the max zoom (1x and 2x screens).
  python3 tools/hero_motion_check.py OUT_DIR   (writes OUT_DIR/hero2-report.txt; exit 1 on failure)"""
import json
import os
import sys
from PIL import Image, ImageChops

out = sys.argv[1]
rows = json.load(open(os.path.join(out, 'motion.json')))
lines, ok = [], True
for (page, mode) in sorted({(r['page'], r['mode']) for r in rows}):
    rs = [r for r in rows if r['page'] == page and r['mode'] == mode]
    tag = 'reduce' if mode == 'reduce' else 'nopref'
    name = page.replace('.html', '').replace('/', '_')
    ims = [Image.open(os.path.join(out, '%s-%s-%ds.png' % (name, tag, r['t']))).convert('L').crop((560, 0, 1440, 900)) for r in rs]
    diffs = []
    for a, b in zip(ims, ims[1:]):
        h = ImageChops.difference(a, b).histogram()
        diffs.append(sum(h[12:]) / (a.size[0] * a.size[1]) * 100)
    changed4 = rs[0]['on'] != rs[2]['on'] or rs[0]['on'] != rs[1]['on']
    good = all(d > 2 for d in diffs) and changed4
    ok &= good
    kb = 1.12 if mode != 'reduce' else 1.05
    r0 = rs[0]
    dppx = r0['natural'] / (r0['base'] * kb)
    lines.append('%-28s %-13s %s' % (page, mode, 'PASS' if good else 'FAIL'))
    lines.append('   photo on screen at 0/2/4/6s: %s; opacities %s' % (' '.join(str(r['on'] + 1) for r in rs), ' | '.join(r['op'] for r in rs)))
    lines.append('   zoom at 0/2/4/6s: %s; share of hero-photo pixels changed between 2s frames: %s%%' % (' '.join(str(r['scale']) for r in rs), ' '.join('%.0f' % d for d in diffs)))
    lines.append('   sharpness: source %s (%dpx wide) on a %dpx box at x%.2f max zoom = %.2f source px per CSS px: 1x screen %.2f (>= 1 is sharp), 2x screen %.2f'
                 % (r0['src'], r0['natural'], r0['base'], kb, dppx, dppx, dppx / 2))
rep = '\n'.join(lines + ['', 'RESULT: %s' % ('PASS' if ok else 'FAIL')])
open(os.path.join(out, 'hero2-report.txt'), 'w').write(rep + '\n')
print(rep)
sys.exit(0 if ok else 1)
