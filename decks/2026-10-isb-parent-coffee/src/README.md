# Parent talk deck: source

Source for the Oct 14, 2026 ISB PTA Parent Coffee deck, "Our Kids' Jobs Don't Exist Yet. So Which Skills Will Matter?"

## Where everything lives (one permanent folder per talk)

Every talk gets its own dated slug, `<yyyy-mm>-<host>-<format>`, and its address never changes or gets reused. This talk's slug is `2026-10-isb-parent-coffee` (taken from this folder's name by `site_paths.py`).

| What | Public address | File in the repo |
|---|---|---|
| Landing page (QR target) | arenaschool.org/talks/2026-10-isb-parent-coffee | `talks/<slug>/index.html` (hand-edited; export.py only updates its slide counts) |
| HTML deck (noindex) | …/deck and …/deck-cn | `talks/<slug>/deck.html`, `deck-cn.html` (built) |
| Phone reader | …/read/en and …/read/cn | `talks/<slug>/read/en.html`, `read/cn.html` (built) |
| PDFs | …/slides-en.pdf, …/slides-cn.pdf | `talks/<slug>/slides-*.pdf` (export.py) |
| Slide images | …/slides/{en,cn}/NN.jpg | `talks/<slug>/slides/` (export.py) |
| Source (not deployed) | none | `decks/<slug>/src/` (this folder; see `.vercelignore`) |

The old addresses (`/talk`, `/talk/en`, `/talk/cn`, `/decks/conversation`, `/decks/conversation-cn`, and the old PDF and gallery links) redirect here permanently in `vercel.json`, so QR codes already scanned keep working.

### Starting a new talk

1. Copy `decks/<old-slug>/` to `decks/<new-slug>/` and copy `talks/<old-slug>/index.html` to `talks/<new-slug>/index.html`.
2. In the new landing page, replace the old slug in its links (search for `/talks/<old-slug>`), and update the title, date, and text.
3. Make the QR images for the new address (they encode `site_paths.URL`; see how `qr-isb-parent-coffee-*.png` in `decks/img/conversation/` were made: navy #0B1A4A modules on transparent, error correction M, a 1-module margin for the `-clear` version and none for `-tight`) and point `body-en/cn.html` at them.
4. Edit the slides, then run `build.py` and `export.py` from the new folder. Nothing in an older talk's folder changes.

## Editing workflow

1. Pull `main`.
2. Edit the content:
   - English slides: `body-en.html`. Chinese slides: `body-cn.html`. Each slide is a `<section class="s">`.
   - **Keep the two languages in step:** add, cut, or reorder a slide in both files.
3. Edit the styles: `shared.css` for shared styles, `css/sNN.css` for per-slide overrides. Behavior lives in `shared.js` and `js/*.html`.
4. Rebuild with `python3 decks/<slug>/src/build.py`. This rewrites `talks/<slug>/deck.html`, `deck-cn.html`, and the phone reader `talks/<slug>/read/en.html` and `read/cn.html`. Never edit those four files directly; the next build overwrites them. In `body-*.html`, `__URL__`, `__DISPLAY__`, and `__DISPLAY_HTML__` become this talk's address at build time.
5. Check locally:
   - From the repo root, run `python3 -m http.server 8780` and open http://127.0.0.1:8780/talks/<slug>/deck.html.
   - Keys: arrows or space to move. The EN · 中文 pill at top right switches language.
   - Every screen shows the real 1920×1080 slide, scaled to fit and letterboxed: the page loads itself at `?stage` into a fixed 1920×1080 frame, so phones never reflow. On touch screens a swipe or a tap moves one step (a tap on the left third goes back). Open `?stage` to see the bare deck at the window's own size (export.py uses it); add `?read` to show every step at once.
   - Speaker notes live in each slide's `<aside class="notes">`. Add `?notes` to show them in a bar along the bottom; they never appear otherwise or in the PDF.
6. Commit the source and the rebuilt HTML together, then push to `main`. Vercel deploys within about a minute.

## The phone reader (read/en, read/cn)

Parents scan the QR code to the landing page. On a phone (under 960px wide) the first screen is a language chooser; one tap opens the reader, a phone-first view of the same slides: one slide per screen, swipe or the big Next / Previous buttons at the bottom (arrow keys and space on a keyboard), a progress line, and an "All slides" list. `#12` opens slide 12; the EN · 中文 pill keeps the slide. Each slide builds once the first time it is reached (steps, bars, counters, the market map); reduced motion shows everything at once. Speaker notes are left out.

- Source: `reader/reader.css` (layout for every slide component, phone first) and `reader/reader.js`. The content is `body-en.html` / `body-cn.html`, so editing a slide updates the deck and the reader together. If you add a new component class to a slide, give it a phone layout in `reader.css`.
- The market-map tool names are read from `shared.js` at build time, so the two views never drift.
- Check: `python3 decks/<slug>/src/reader_check.py` loads both readers at 390×844 and 844×390 and fails on sideways overflow, text under 10px, or missing images; it writes a screenshot of every slide to `/tmp/reader-shots` (`--shots DIR` to change).
- Locally, open http://127.0.0.1:8780/talks/<slug>/read/en.html (the dev server has no clean URLs; Vercel serves `/talks/<slug>/read/en`).

House rules (full detail in `/DESIGN.md` and `/CONTENT-RULES.md`):
- English and Chinese only. The bilingual deck is retired.
- Never write "X年级" in Chinese.
- No student names or counts, prize amounts, or fees.
- Every slide must fit 1920×1080. Fix overflow by tightening spacing, never by shrinking the type.

## Finalizing: publish the PDFs on the landing page

**Status (Oct 14, 2026): finalized and moved to talks/2026-10-isb-parent-coffee.** Both PDFs and the slide images are on main.

Run this only once the slides are final:

```
pip install playwright pillow pypdf && python3 -m playwright install chromium   # first time only
python3 decks/<slug>/src/export.py
```

The script:
- rebuilds the deck;
- aborts if any slide is taller than 1080px in export mode;
- aborts if any text, image, or card sits outside its own card, pane, or pill (`contain.py`; run it alone with `python3 decks/<slug>/src/contain.py`, add `--georgia` to also test the wider Georgia metrics a phone shows when the web fonts fail to load);
- writes `talks/<slug>/slides-en.pdf` and `slides-cn.pdf` (no QR); each PDF is kept under 6 MB for phones and WeChat by lowering the JPEG quality step by step (it prints the quality used);
- regenerates the slide images (`talks/<slug>/slides/{en,cn}/NN.jpg`) and the landing page's slide counts;
- writes a presenting copy with the QR to `decks/<slug>/src/exports/` (git-ignored, not deployed).

Then:
- open http://127.0.0.1:8780/talks/<slug>/ and check that both PDF buttons work;
- commit and push. The PDFs go live on arenaschool.org/talks/<slug>.

To try it without touching the published files, run `python3 decks/<slug>/src/export.py --out /tmp/deck-test`.
