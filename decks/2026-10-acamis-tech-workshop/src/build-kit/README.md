# ACAMIS live build kit: the Teacher Toolbox

The platform is live before the session: **https://arenaschool.org/talks/2026-10-acamis-tech-workshop/build**. It starts with three tested tools. During the session the room calls out features or new tools; one laptop prompts Claude Code; each change ships to the live site, and every phone that has the page open shows "Just shipped … tap to refresh". The hub's "What the room asked for" log fills up as you go.

## What's here

| File | Job |
|---|---|
| `CLAUDE.md` | Rules Claude follows: edit only the Toolbox folder, one-file tools, no questions, no CDNs or AI calls, made-up names only, log each request, ship, and reply in three lines with the live link. |
| `ship.sh` | Commits only the Toolbox folder, pushes to `main`, and waits until the change is live on arenaschool.org (prints `LIVE after Ns`). |
| `start.sh` | Starts Claude Code here with the Toolbox folder attached. **Always launch with this.** |
| `.claude/settings.json` | Pre-approves edits and `./ship.sh`, so nothing stops for permission. |
| `template.html` | Styled shell for new tools (back link and live updates built in). |
| `backups/` | Copies of the three starter tools, in case one gets broken. |

The site itself is `talks/2026-10-acamis-tech-workshop/build/`: `index.html` (hub), `tools.json` (tool list), `changes.txt` (request log; git merges it line by line, so two laptops can ship), `live.js` (the refresh toast), and one folder per tool.

## Set up the driving laptop (tonight)

1. The repo must be a normal clone on `main` with push access: `git clone https://github.com/phillipan14/arena-school` (or `git pull` in yours), then `cd decks/2026-10-acamis-tech-workshop/src/build-kit`.
2. Run `./start.sh` once and accept **"trust this folder"** (otherwise the pre-approved permissions are ignored).
3. Rehearse one request, for example `Add a print button to the lab group maker.` Watch it reach `LIVE`, open the page on your phone, and see the refresh toast. Then ask for it to be taken out again, or keep it.
4. Clear the rehearsal from the log: delete your test lines from `changes.txt` (keep the `Before|…` line) and run `./ship.sh "reset log"`.
5. Test the network you'll have at Keystone (the VPN if Claude Code needs one, plus a phone hotspot).
6. Projector: Terminal (large font) on the left, the hub on the right. Put the hub's URL or QR on a slide.

## Run of show (60 minutes)

| Min | Slides or room |
|---|---|
| 0–5 | Opening and Arena; QR to the Toolbox so phones are on it |
| 5–12 | The ISB case (short) |
| 12–15 | Tour the Toolbox: three starter tools, all live |
| 15–17 | **Request 1** from the room (a feature on a starter tool) |
| 17–25 | Talk while it builds: why it worked (research; agency, taste, and craft) |
| 25–28 | It's live: everyone tries it on their phone |
| 28–30 | **Request 2** (a fix the room found, or a brand-new tool) |
| 30–38 | Talk: is it cheating, the teacher's role, and "How did you check it?" |
| 38–45 | **Requests 3 and 4**, faster: call out, ship, try |
| 45–50 | Look back at the log: what the room built in 30 minutes |
| 50–55 | Take it back, and the offer |
| 55–60 | Q&A |

**Good first requests:** "Add a Chinese version of the parent email." "Let us save our class list in the group maker." "Add a timer to the quiz." **New tools:** a transition timer, a rubric-to-comment helper, or vocabulary flashcards.

## Rules to say out loud

- Made-up names only; no real student data goes into any prompt.
- Each request is one sentence: who it's for and what it should do.
- Claude's "Next idea" line is a ready-made next request if the room goes quiet.

## If something goes wrong

- **A tool breaks:** say "Undo that change to the <tool>," or copy its file back from `backups/` and run `./ship.sh "restore"`.
- **The push fails:** check the network and run `./ship.sh` again. Nothing is lost; the change is committed locally.
- **No network at all:** open the tool file locally (`open ../../../../talks/2026-10-acamis-tech-workshop/build/<tool>/index.html`) and show it on the projector; ship it when the network is back.
