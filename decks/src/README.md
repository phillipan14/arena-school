# Parent talk deck: source

Source for the Oct 14, 2026 ISB PTA Parent Coffee deck, "Our Kids' Jobs Don't Exist Yet. So Which Skills Will Matter?"

| What | Where |
|---|---|
| HTML deck (live, noindex) | arenaschool.org/decks/conversation and /decks/conversation-cn |
| Talk landing page (QR target) | arenaschool.org/talk (`talk/index.html`): on phones the first screen is a one-tap English / 中文 chooser |
| Phone reader (built) | arenaschool.org/talk/en and /talk/cn (`talk/en.html`, `talk/cn.html`), opened from the chooser |
| Source (this folder, not deployed) | `decks/src/` |

## Editing workflow

1. Pull `main`.
2. Edit the content:
   - English slides: `body-en.html`. Chinese slides: `body-cn.html`. Each slide is a `<section class="s">`.
   - **Keep the two languages in step:** add, cut, or reorder a slide in both files.
3. Edit the styles: `shared.css` for shared styles, `css/sNN.css` for per-slide overrides. Behavior lives in `shared.js` and `js/*.html`.
4. Rebuild with `python3 decks/src/build.py`. This rewrites `decks/conversation.html` and `decks/conversation-cn.html`, and the phone reader `talk/en.html` and `talk/cn.html`. Never edit those four files directly; the next build overwrites them.
5. Check locally:
   - From the repo root, run `python3 -m http.server 8780` and open http://127.0.0.1:8780/decks/conversation.html.
   - Keys: arrows or space to move. The EN · 中文 pill at top right switches language.
   - Every screen shows the real 1920×1080 slide, scaled to fit and letterboxed: the page loads itself at `?stage` into a fixed 1920×1080 frame, so phones never reflow. On touch screens a swipe or a tap moves one step (a tap on the left third goes back). Open `?stage` to see the bare deck at the window's own size (export.py uses it); add `?read` to show every step at once.
   - Speaker notes live in each slide's `<aside class="notes">`. Add `?notes` to show them in a bar along the bottom; they never appear otherwise or in the PDF.
6. Commit the source and the rebuilt HTML together, then push to `main`. Vercel deploys within about a minute.

## The phone reader (/talk/en, /talk/cn)

Parents scan the QR code to `/talk`. On a phone (under 960px wide) the first screen is a language chooser; one tap opens the reader, a phone-first view of the same slides: one slide per screen, swipe or the big Next / Previous buttons at the bottom (arrow keys and space on a keyboard), a progress line, and an "All slides" list. `#12` opens slide 12; the EN · 中文 pill keeps the slide. Each slide builds once the first time it is reached (steps, bars, counters, the market map); reduced motion shows everything at once. Speaker notes are left out.

- Source: `reader/reader.css` (layout for every slide component, phone first) and `reader/reader.js`. The content is `body-en.html` / `body-cn.html`, so editing a slide updates the deck and the reader together. If you add a new component class to a slide, give it a phone layout in `reader.css`.
- The market-map tool names are read from `shared.js` at build time, so the two views never drift.
- The reader's last slide (contact Jing Jing on WhatsApp or WeChat, download the PDF, email fallback) is reader-only: `reader/end-en.html` and `reader/end-cn.html`, appended by `build.py` after the appendix. The deck never shows it. `{{br:whatsapp}}` / `{{br:wechat}}` inline the brand glyphs from `reader/brand/` (Simple Icons, CC0); the Copy button uses the clipboard API with an `execCommand` fallback for in-app browsers such as WeChat's.
- Check: `python3 decks/src/reader_check.py` loads both readers at 390×844 and 844×390 and fails on sideways overflow, text under 10px, or missing images; it writes a screenshot of every slide to `/tmp/reader-shots` (`--shots DIR` to change).
- Locally, open http://127.0.0.1:8780/talk/en.html (the dev server has no clean URLs; Vercel serves `/talk/en`).

House rules (full detail in `/DESIGN.md` and `/CONTENT-RULES.md`):
- English and Chinese only. The bilingual deck is retired.
- Never write "X年级" in Chinese.
- No student names or counts, prize amounts, or fees.
- Every slide must fit 1920×1080. Fix overflow by tightening spacing, never by shrinking the type.

## Finalizing: publish the PDFs on /talk

**Status (Oct 11, 2026): finalized.** Both PDFs and the /talk gallery are on main.

Run this only once the slides are final:

```
pip install playwright pillow pypdf && python3 -m playwright install chromium   # first time only
python3 decks/src/export.py
```

The script:
- rebuilds the deck;
- aborts if any slide is taller than 1080px in export mode;
- aborts if any text, image, or card sits outside its own card, pane, or pill (`contain.py`; run it alone with `python3 decks/src/contain.py`, add `--georgia` to also test the wider Georgia metrics a phone shows when the web fonts fail to load);
- writes `talk/Arena-Parent-Conversation-EN.pdf` and `talk/Arena-Parent-Conversation-CN.pdf` (no QR); each PDF is kept under 6 MB for phones and WeChat by lowering the JPEG quality step by step (it prints the quality used);
- regenerates the /talk swipe gallery (`talk/slides/{en,cn}/NN.jpg`) and its slide counts;
- writes a presenting copy with the QR to `decks/src/exports/` (git-ignored, not deployed).

Then:
- open http://127.0.0.1:8780/talk and check that both PDF buttons work and the gallery matches;
- commit and push. The PDFs go live on arenaschool.org/talk.

To try it without touching /talk, run `python3 decks/src/export.py --out /tmp/deck-test`.
