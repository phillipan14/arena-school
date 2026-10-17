# ACAMIS live build: rules for Claude Code

A room of teachers is watching this screen. They call out a feature or a new tool for the **Teacher Toolbox**, a live site at https://arenaschool.org/talks/2026-10-acamis-tech-workshop/build. You build it, ship it, and everyone's phone shows it within about a minute. Speed matters more than polish: aim for one to two minutes per request.

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
- One self-contained `index.html` per tool: inline CSS and JavaScript, no frameworks, no npm, no CDNs, no external fonts or APIs (China). Keep `<script src="../live.js"></script>` and the "← Teacher Toolbox" link from the template.
- **No AI and no network calls inside a tool.** Use templates, rules, or lists the teacher can edit.
- **Made-up names only** ("Student A", "Ms. Rivera"); never real student data. Save work in `localStorage` and add a Clear button.
- Big readable text, one job per tool, and it must work on a phone (most of the room is on one).
- Don't run git yourself (`ship.sh` does it), don't `cd` (use paths), and don't write tests, plans, or READMEs.
