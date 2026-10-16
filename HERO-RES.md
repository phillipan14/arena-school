# Hero photo resolution (RES-BRIEF, Oct 16, 2026)

Goal: full-bleed retina needs about 2400px; brief floor about 1920px sharp.

## Where I looked
- This repo, including git history (every photo blob ever committed): the largest version of every hero photo is **1600px wide**.
- `~/Pictures`, `~/Downloads`, `~/Desktop`, `~/Documents` (images over 700KB, plus camera-style names like IMG_/DSC_, HEIC and RAW). The Photos library database was not opened. Nothing matched: the only large images are phone screenshots (1290x2796, May 2026) and unrelated documents.
- Other worktrees: `~/arena-school` (and its `.claude/worktrees/*`), `~/arena-icp`, `~/arena-icp2`, `~/arena-site-popup`: the same files, at most 1600px.
- Videos: `photos/pilot-collab.mp4` is 1280x2276 (portrait), `photos/steps/collab-stage.mp4` is 1024x768.

**No original reaches 1920px, let alone 2400px.** The full-resolution originals are probably in the shared Drive (04 Marketing, Brand & Media) or with the photographer; ask for the camera originals and rerun `python3 tools/hero_images.py` with the new sources.

## Decision per photo

| Key | Source (largest found) | Source size | Decision |
|---|---|---|---|
| duo | `photos/isb-2026/pitch-duo.jpg` | 1600x1067 | **Kept** (borderline). Exported 800/1280/1600 AVIF, WebP, JPEG. |
| gesture | `photos/isb-pitch-gesture.jpg` | 1600x1200 | **Kept** (borderline). Same exports. |
| mentors | `photos/isb-2026/mentor-feedback.jpg` | 1600x1067 | **Kept** (borderline). Same exports. |
| hands | `photos/steps/collab-stage-poster.webp` (video still; the clip is 1024x768) | 1024x768 | **Dropped** from every hero: cannot get near 1920px. |

How the kept 1600px photos stay as sharp as they can:
- Desktop no longer stretches them across the full window and zooms in (that showed about 1830 CSS px from 1600 source px, under 1x at retina). The photo is now right-anchored at the hero's height (about 1170 CSS px wide at 1440x900), so a 1600px source gives about 1.4 device px per CSS px, with motion capped at scale 1.07.
- 2560/1920 exports were not made: upscaling a 1600px original adds no detail.
- Exports: `photos/hero/<key>-{800,1280,1600}.{avif,webp,jpg}` (AVIF CRF 30 via SVT-AV1, WebP q80, JPEG q~85), served with `<picture>` (AVIF, then WebP, then JPEG). Only the first photo is preloaded.
