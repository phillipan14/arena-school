"""Check the frames from tools/xfade_frames.mjs: every frame must show word ink in the slot, and the headline
box must never move or resize. Writes OUT_DIR/xfade-report.txt and a contact sheet per run; exit 1 on failure.
Ink = pixels that differ from the empty-slot reference by more than 48 (any channel). A frame passes when its ink
is at least 30% of the run's median ink (one whole word), so a blank or near-blank frame fails.
  python3 tools/xfade_check.py OUT_DIR [--sheet RUN_NAME:PATH ...]
"""
import json
import os
import sys
from PIL import Image, ImageChops, ImageDraw


def ink(a, b):
    d = ImageChops.difference(a, b).convert('RGB')
    data = d.get_flattened_data() if hasattr(d, "get_flattened_data") else d.getdata()
    return sum(1 for px in data if max(px) > 48)


def run(dirpath):
    meta = json.load(open(os.path.join(dirpath, 'frames.json')))
    empty = Image.open(os.path.join(dirpath, 'empty.png')).convert('RGB')
    vals = []
    for f in meta['frames']:
        im = Image.open(os.path.join(dirpath, 'f%03d.png' % f['n'])).convert('RGB')
        vals.append(ink(im, empty) if im.size == empty.size else 0)
    med = sorted(vals)[len(vals) // 2]
    thr = 0.30 * med
    low = [(f['n'], f['t'], v) for f, v in zip(meta['frames'], vals) if v < thr]
    h1s = {tuple(f['h1']) for f in meta['frames']}
    slots = {tuple(f['slot']) for f in meta['frames']}
    changes = sum(1 for a, b in zip(meta['frames'], meta['frames'][1:]) if a['on'] != b['on'])
    return meta, vals, med, thr, low, h1s, slots, changes


def sheet(dirpath, meta, vals, thr, out, cols=12):
    frames = meta['frames']
    ims = [Image.open(os.path.join(dirpath, 'f%03d.png' % f['n'])).convert('RGB') for f in frames]
    w, h = ims[0].size
    sc = min(1.0, 220 / w)
    tw, th = int(w * sc), int(h * sc) + 14
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * tw, rows * th), 'white')
    d = ImageDraw.Draw(S)
    for k, (im, f, v) in enumerate(zip(ims, frames, vals)):
        x, y = (k % cols) * tw, (k // cols) * th
        S.paste(im.resize((tw, int(h * sc))), (x, y))
        d.text((x + 3, y + int(h * sc)), '%dms ink %d' % (f['t'], v), fill=(200, 0, 0) if v < thr else (40, 40, 40))
    S.save(out)


if __name__ == '__main__':
    out = sys.argv[1]
    sheets = dict(a.split(':', 1) for a in sys.argv[2:] if ':' in a)
    lines, ok = [], True
    for name in sorted(os.listdir(out)):
        dp = os.path.join(out, name)
        if not os.path.exists(os.path.join(dp, 'frames.json')):
            continue
        meta, vals, med, thr, low, h1s, slots, changes = run(dp)
        gaps = [b['t'] - a['t'] for a, b in zip(meta['frames'], meta['frames'][1:])]
        good = not low and len(h1s) == 1 and len(slots) == 1 and changes >= 3
        ok &= good
        lines.append('%-18s %s  frames %d (mean every %dms, max gap %dms), word changes %d' % (name, 'PASS' if good else 'FAIL', len(vals), sum(gaps) / len(gaps), max(gaps), changes))
        lines.append('   ink per frame: min %d, median %d, threshold %d (30%% of median); frames below: %d %s' % (min(vals), med, thr, len(low), low[:6]))
        lines.append('   headline box (x, y, w, h): %s distinct value(s) %s' % (len(h1s), sorted(h1s)[:3]))
        lines.append('   word slot (x, y, w, h): %s distinct value(s) %s' % (len(slots), sorted(slots)[:3]))
        if name in sheets:
            sheet(dp, meta, vals, thr, sheets[name])
    rep = '\n'.join(lines + ['', 'RESULT: %s' % ('PASS' if ok else 'FAIL')])
    open(os.path.join(out, 'xfade-report.txt'), 'w').write(rep + '\n')
    print(rep)
    sys.exit(0 if ok else 1)
