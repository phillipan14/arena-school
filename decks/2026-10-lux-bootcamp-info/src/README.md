# Lux Scholar info session deck (圣诞AI产品训练营说明会)

Chinese only, six slides, converted 1:1 from the approved PowerPoint (Christmas-AI-Product-Bootcamp_v04.pptx).
Embedded on the AI Advantage Bootcamp pages (zero-to-launch.html, zero-to-launch-cn.html, section `#slides`).

- `body-cn.html`: the slides. Each slide is an absolute 1920×1080 frame (`.lx-f`) with the pptx geometry
  (1in = 144px, 1pt = 2px). Text sizes, colors, and positions match the deck; centered text has been nudged
  so its ink is centered in its pill, band, or row within 1px (measured, not guessed).
- `css/zz-lux.css`: Lux styles (frame, text boxes, bar growth, cover entrance, page number on the footer-logo baseline).
- Builds: `data-s` groups (days, mentors, bar then cards, outcomes then summary, feedback cards); `.cnt` counts up.
- Images: `/decks/img/lux-bootcamp-info/` (Lux and Arena lockups, mentor photos, university logos).

Publish: `python3 decks/2026-10-lux-bootcamp-info/src/build.py`, then `export.py` for `slides-cn.pdf` and
`slides/cn/NN.jpg` (the phone reader at `/talks/2026-10-lux-bootcamp-info/read/cn` shows these images,
so rerun export.py after any slide change).

Out:
- `/talks/2026-10-lux-bootcamp-info/deck` (desktop, click or arrow keys to step)
- `/talks/2026-10-lux-bootcamp-info/read/cn` (phones)
