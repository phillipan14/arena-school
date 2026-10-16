"""Pixel diff of two screenshot folders from tools/pixel_shots.mjs: prints, per page, the share of pixels that
changed (channel difference > 24) and the changed area's bounding box. Exit 1 if any page changed.
  python3 tools/pixel_diff.py BEFORE_DIR AFTER_DIR [--tol 0.0001] [--out DIFF_DIR]
"""
import os
import sys
from PIL import Image, ImageChops


def main(a, b, tol=0.0, outdir=None):
    bad = 0
    for f in sorted(os.listdir(a)):
        if not f.endswith('.png'):
            continue
        if not os.path.exists(os.path.join(b, f)):
            print('%-44s missing after' % f); bad += 1; continue
        x, y = Image.open(os.path.join(a, f)).convert('RGB'), Image.open(os.path.join(b, f)).convert('RGB')
        if x.size != y.size:
            print('%-44s size %s -> %s' % (f, x.size, y.size)); bad += 1; continue
        d = ImageChops.difference(x, y).convert('L').point(lambda v: 255 if v > 24 else 0)
        n = sum(d.histogram()[255:])
        share = n / (x.size[0] * x.size[1])
        if share > tol:
            bad += 1
            print('%-44s %.4f%% changed, box %s' % (f, share * 100, d.getbbox()))
            if outdir:
                os.makedirs(outdir, exist_ok=True)
                d.save(os.path.join(outdir, f))
    print('%d page(s) differ' % bad)
    return bad


if __name__ == '__main__':
    args = sys.argv[1:]
    tol = float(args[args.index('--tol') + 1]) if '--tol' in args else 0.0
    out = args[args.index('--out') + 1] if '--out' in args else None
    sys.exit(1 if main(args[0], args[1], tol, out) else 0)
