# ACAMIS live build: rules for Claude Code

A room of teachers is watching this screen. They call out a feature or a new tool for the **Teacher Toolbox**, a live site at https://arenaschool.org/talks/2026-10-acamis-tech-workshop/build. You build it and ship it, and we show it on the projector as soon as it's live (usually a few minutes). Speed matters more than polish: aim for one to two minutes per request.

## Before the room starts
If the presenter asks whether you're ready (for example "Are you ready to build a Teacher Toolbox now?"), don't build anything yet. Reply in one or two short lines, warmly and plainly, for example: "Ready. Hit me with whatever the room wants: a feature for one of the three starter tools, or a brand-new tool." Then wait for the first request.

## Where you work
- The site lives in `../../../../talks/2026-10-acamis-tech-workshop/build/` (call it BUILD). Edit **only** files in BUILD. Never touch anything else in the repo.
- BUILD has: `index.html` (the hub; don't edit it), `tools.json` (the list of tools), `changes.txt` (the log of requests), `live.js` (don't edit), and one folder per tool (`BUILD/<slug>/index.html`).

## Every request
1. **Decide:** is it a change to an existing tool, or a new tool? If it's unclear, pick the closest existing tool.
2. **Change a tool:** edit `BUILD/<slug>/index.html`. Keep what works; change only what was asked.
3. **New tool:** pick a short slug, copy `template.html` (in this folder) to `BUILD/<slug>/index.html`, and build the tool in it. Then add an entry to the end of `BUILD/tools.json`: `{"slug": "...", "name": "...", "what": "one line", "by": "room"}`.
4. **Log it:** use the Edit tool (not the shell) to append one line to `BUILD/changes.txt`, in the form `HH:MM|the room's request in their words (max 12 words)|what changed (max 12 words)|slug`. Use the current local time.
5. **Ship it:** run exactly `./ship.sh "short summary"` as its own command, from this folder. Never `cd` anywhere and never chain it with `&&`. It pushes and waits until the change is live, then prints LIVE. If it says "still deploying", that's fine; say so.
6. **Reply** in at most three short lines: what changed in plain English, the tool's live link (`https://arenaschool.org/talks/2026-10-acamis-tech-workshop/build/<slug>`), and "Next idea:" with one improvement the room could ask for.

## Rules for every tool
- **Never ask clarifying questions.** Make sensible assumptions and mention one if it matters.
- One self-contained `index.html` per tool: inline CSS and JavaScript, no frameworks, no npm, no CDNs, no external fonts or APIs (China). Keep `<script src="/talks/2026-10-acamis-tech-workshop/build/live.js"></script>` and the "← Teacher Toolbox" link (`href="/talks/2026-10-acamis-tech-workshop/build"`) from the template. Always use these absolute paths: the site drops trailing slashes, so relative paths like `../live.js` break.
- **No AI and no other network calls inside a tool.** Use templates, rules, or lists the teacher can edit.
- **Many phones, one screen** (anonymous feedback, exit tickets, live polls, a Q&A wall): use the shared board, and nothing else. Add `<script src="/talks/2026-10-acamis-tech-workshop/build/board.js"></script>` and use `var b = Board('<slug>')`, `b.post(text, tag)`, and `b.watch(function (items) { ... }, 3000)` (items newest first: `{id, t, text, tag}`; text up to 500 characters, tag up to 40). Build two views in the same file and show **only one at a time** (check `location.hash` on load and on `hashchange`): the **phone view** (default) is only the form (big buttons; say "Anonymous" on screen; after sending, show "Thanks, sent"), with no results on it; the **projector view** (`#screen`) is only the live results, full width with large text, as cards or bars with counts, plus a one-line "Answer at <short link>" so the room knows where to go. Give the phone view a small "Teacher? Open the projector view" link. Never ask for or send names, emails, or student details. Responses delete themselves after three days.
- **Made-up names only** ("Student A", "Ms. Rivera"); never real student data. Save work in `localStorage` and add a Clear button.
- Big readable text (it's shown on a projector), one job per tool, and it should also work on a phone.
- Don't run git yourself (`ship.sh` does it), don't `cd` (use paths), and don't write tests, plans, or READMEs.
