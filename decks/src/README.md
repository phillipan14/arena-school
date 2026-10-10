# Parent talk deck: source

Source for the Oct 14, 2026 ISB PTA Parent Coffee deck, "Our Kids' Jobs Don't Exist Yet. So Which Skills Will Matter?"

| What | Where |
|---|---|
| HTML deck (live, noindex) | arenaschool.org/decks/conversation and /decks/conversation-cn |
| Talk landing page (QR target) | arenaschool.org/talk (`talk/index.html`) |
| Source (this folder, not deployed) | `decks/src/` |

## Editing workflow

1. Pull `main`.
2. Edit the content:
   - English slides: `body-en.html`. Chinese slides: `body-cn.html`. Each slide is a `<section class="s">`.
   - **Keep the two languages in step:** add, cut, or reorder a slide in both files.
3. Edit the styles: `shared.css` for shared styles, `css/sNN.css` for per-slide overrides. Behavior lives in `shared.js` and `js/*.html`.
4. Rebuild with `python3 decks/src/build.py`. This rewrites `decks/conversation.html` and `decks/conversation-cn.html`. Never edit those two files directly; the next build overwrites them.
5. Check locally:
   - From the repo root, run `python3 -m http.server 8780` and open http://127.0.0.1:8780/decks/conversation.html.
   - Keys: arrows or space to move. The EN · 中文 pill at top right switches language.
6. Commit the source and the rebuilt HTML together, then push to `main`. Vercel deploys within about a minute.

House rules (full detail in `/DESIGN.md` and `/CONTENT-RULES.md`):
- English and Chinese only. The bilingual deck is retired.
- Never write "X年级" in Chinese.
- No student names or counts, prize amounts, or fees.
- Every slide must fit 1920×1080. Fix overflow by tightening spacing, never by shrinking the type.

## Finalizing: publish the PDFs on /talk

**Status (Oct 10, 2026): not finalized.** Phillip is reviewing. The two PDF buttons on /talk return 404 until this step runs.

Run this only once the slides are final:

```
pip install playwright pillow pypdf && python3 -m playwright install chromium   # first time only
python3 decks/src/export.py
```

The script:
- rebuilds the deck;
- aborts if any slide is taller than 1080px in export mode;
- writes `talk/Arena-Parent-Conversation-EN.pdf` and `talk/Arena-Parent-Conversation-CN.pdf` (no QR, about 5MB each);
- regenerates the /talk swipe gallery (`talk/slides/{en,cn}/NN.jpg`) and its slide counts;
- writes a presenting copy with the QR to `decks/src/exports/` (git-ignored, not deployed).

Then:
- open http://127.0.0.1:8780/talk and check that both PDF buttons work and the gallery matches;
- commit and push. The PDFs go live on arenaschool.org/talk.

To try it without touching /talk, run `python3 decks/src/export.py --out /tmp/deck-test`.
