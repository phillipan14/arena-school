# ACAMIS Tech workshop deck: source

Source for "From Lab to Classroom: Running an AI Student Program Inside a School", Arena School's workshop at the ACAMIS Technology Conference (Sun Oct 18, 2026, 11:20 to 12:20, Breakout D, Keystone Academy). English only, 29 slides.

**This folder on `main` is the one copy of the deck.** Edit here, push to `main`, and Vercel deploys to arenaschool.org. Don't keep edits in other folders, branches, or local copies.

## Where everything lives

Slug: `2026-10-acamis-tech-workshop` (read from this folder's name by `site_paths.py`).

| What | Public address | File in the repo |
|---|---|---|
| Session page (QR target) | arenaschool.org/talks/2026-10-acamis-tech-workshop | `talks/<slug>/index.html` (hand-edited; export.py only updates its slide count) |
| HTML deck (noindex) | …/deck | `talks/<slug>/deck.html` (built) |
| Phone reader | …/read/en | `talks/<slug>/read/en.html` (built) |
| Slides PDF | …/slides-en.pdf | `talks/<slug>/slides-en.pdf` (export.py) |
| Slide images | …/slides/en/NN.jpg | `talks/<slug>/slides/en/` (export.py) |
| China AI tool guide PDF | …/china-ai-tool-guide.pdf | built by `guide/build_guide.py` from `guide/tools.json` |
| Build-session page (placeholder) | …/build/ | `talks/<slug>/build/index.html` (hand-edited) |
| Presenting PDF (with QR) | not deployed | `src/exports/` (git-ignored; export.py writes it) |
| Source | not deployed | this folder (`decks/*/src` is in `.vercelignore`) |

## Edit, check, deploy

1. `git pull` on `main`.
2. Edit:
   - Slides: `body-en.html`. Each slide is a `<!-- n · name -->` comment plus one `<section class="s …">`. Speaker notes are the `<aside class="notes">` inside it.
   - Styles: `shared.css`, then `css/*.css`, loaded in alphabetical order (the later file wins). Put new rules in the **last** file (`css/s99zzzzzzzzzzzzzzzzzzzz-r6.css` today) or a new file that sorts after it, and scope them to the slide's own class.
   - Phone reader layout for any new component: append to `reader/reader.css`.
   - Slide 7 wheel: don't hand-edit the SVG. Run `python3 tools/wheel.py` (key=value to change sizes), then build.
3. Build: `python3 decks/2026-10-acamis-tech-workshop/src/build.py` (rewrites `deck.html` and `read/en.html`; never edit those directly).
4. Look: `python3 -m http.server 8780` from the repo root, then open http://127.0.0.1:8780/talks/2026-10-acamis-tech-workshop/deck.html. Add `?notes` for speaker notes. Browsers cache hard: add `?v=1`, `?v=2`… or press Cmd+Shift+R.
5. Check (all must pass):
   - `python3 decks/2026-10-acamis-tech-workshop/src/contain.py --georgia` → every line says 0.
   - `python3 decks/2026-10-acamis-tech-workshop/src/reader_check.py --shots /tmp/reader` → "reader OK".
   - `python3 decks/2026-10-acamis-tech-workshop/src/tools/shots.py /tmp/shots 7,25` → "taller than 1080: none". Look at the PNGs.
6. Export: `python3 decks/2026-10-acamis-tech-workshop/src/export.py` (rebuilds, refuses to run if a slide is too tall or anything overflows, then writes the PDFs, slide images, and slide count).
7. Commit the source and the built files together, then push to `main`. Vercel deploys in about a minute.

First time on a machine: `pip install playwright pillow pypdf numpy && python3 -m playwright install chromium`.

## Tools (`tools/`)

| Script | What it does |
|---|---|
| `shots.py OUTDIR [7,25]` | Screenshots slides in their final state; reports slides taller than 1080px and page errors. |
| `sheet.py SHOTDIR 6,7,8 OUT.png` | Contact sheet of those screenshots, two per row. |
| `ink.py SLIDE "selector" [--inset 30]` | Measures how centered the visible ink is inside each matching box (top/bottom, left/right). Aim for a difference within 1.5px. |
| `wheel.py [key=value…]` | Regenerates the slide 7 framework wheel SVG and pastes it into `body-en.html`. |

## Research (`research/`)

Verified sources behind the deck's claims: the framework references (`frameworks-verified-2026-10-16.json`), the research stats on slides 17 and 24 (`evidence-framework.json`, `evidence-teachers.json`), and the China tool facts (`china-tools-verified-2026-10-15.json`). Check a new number at its source and add it here before it goes on a slide.

## House rules

See `CLAUDE.md` in this folder (also loaded automatically by Claude Code), `PRINCIPLES.md`, `/DESIGN.md`, and `/CONTENT-RULES.md`.
