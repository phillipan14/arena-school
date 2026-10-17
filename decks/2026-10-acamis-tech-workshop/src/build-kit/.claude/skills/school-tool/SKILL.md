---
name: school-tool
description: Build a small single-page tool for a teacher's school week from a plain-English description, fast, for the ACAMIS build session. Use for any request to build, make, or create a tool, page, or app in this folder.
---

# Build a school tool

Follow `CLAUDE.md` in this folder. In short:

1. Pick a short slug from the request (for example `parent-email`, `quiz-maker`).
2. `mkdir -p builds/<slug>` and `cp template.html builds/<slug>/index.html`.
3. Replace the title, the one-line description, and the `<main>` content with the tool. Use the template's ready-made classes (`card`, `row`, `btn`, `btn-ghost`, `field`, `out`, `pill`, `grid2`) so it looks finished without new CSS.
4. Fill in realistic placeholder data, save state in `localStorage`, and add a Clear button.
5. `open builds/<slug>/index.html`.
6. Reply in at most three short lines: what it does, "Try this:", and "Next prompt idea:".

For a follow-up ("make the buttons bigger", "add a column for due dates"), edit the same file, then open it again. Don't start over.
