# ACAMIS build session kit (Claude Code, two laptops)

Teachers build a small tool for their own school week by prompting Claude Code in two groups, one laptop per group. This folder makes every prompt end with a working page in the browser in about one to two minutes. In tests, a first build took 66 to 132 seconds, and follow-up edits are faster.

- `CLAUDE.md` contains the build rules Claude follows: one self-contained HTML file, no setup, no questions, no CDNs (China), no real student data, and a reply of three lines for the projector.
- `.claude/settings.json` pre-approves file edits and `open`, so nothing stops for permission mid-build.
- `.claude/skills/school-tool/` is the same rules as a `/school-tool` skill.
- `template.html` is a styled page shell, so tools look finished and Claude only writes the logic.
- `backups/` holds three tested tools (a parent email writer, a group maker, and a quiz maker). If a live build fails, open one and keep going.
- `builds/` is where each group's tools land (git-ignored).

## Set up each laptop (tonight, about 10 minutes)

1. Copy this folder to `~/Desktop/acamis-build`. **Not** under `~/.claude`, which Claude Code protects, so writes there get blocked.
2. In Terminal: `cd ~/Desktop/acamis-build && claude`. Accept the **"trust this folder"** prompt; without it, the pre-approved permissions are ignored and Claude stops to ask before every file.
3. Warm-up: type `Build a countdown timer for class transitions with big numbers.` It should open in the browser on its own in about a minute.
4. Check the network on what you'll have at Keystone (the VPN if you need one, plus a phone hotspot as backup). Claude Code needs it; the finished tools don't.
5. Presentation setup: Terminal font large (Cmd and +), Terminal on the left half and the browser on the right. The laptop on the projector is group 1's.

## Run of show (60 minutes)

| Min | Slides or room |
|---|---|
| 0–5 | Opening and Arena |
| 5–12 | The ISB case (short) |
| 12–15 | Split into two groups around the laptops. Each group picks a chore (cards below) and a **typist**. |
| 15–17 | **Prompt 1:** build it |
| 17–25 | Talk: why it worked (research; agency, taste, and craft) |
| 25–30 | Groups try the tool. One person tries to break it, and the group agrees on one fix. |
| 30–31 | **Prompt 2:** the fix |
| 31–38 | Talk: is it cheating, the teacher's role, and "How did you check it?" |
| 38–42 | **Prompt 3:** make it yours |
| 42–48 | Each group shows its tool on the projector (3 minutes each) |
| 48–55 | Take it back, and the offer |
| 55–60 | Q&A |

## Prompt cards

**The formula for prompt 1:** "We're **[grade or subject]** teachers. Build a tool that **[does one job]** for **[who uses it]**. It should **[two or three specifics]**. It never **[touches student names or grades / sends anything anywhere]**."

Chores that work well (all tested or close to it):
- Rewrite the weekly parent email from the topics covered, due dates, and a tone. *(tested, 66s)*
- Random, balanced groups from a pasted class list, with a projector view. *(tested, 84s)*
- A reading-check quiz from a pasted passage, with a printable answer key. *(tested, 132s)*
- A countdown or transition timer with big numbers and sounds.
- A rubric-to-feedback helper: tick the rubric levels, get a short comment to edit.
- A vocabulary flashcard game from a pasted word list.

**Prompt 2 (fix) examples:** "Make the buttons bigger." "It gets confused when the list has blank lines; fix that." "Add a column for due dates."

**Prompt 3 (make it yours) examples:** "Use our school colors, navy and gold." "Add a Chinese version underneath for families." "Add a print button."

## Facilitator rules

- The typist types the group's words. The facilitator helps only with phrasing, using the formula above.
- Placeholder names only ("Student A", "Ms. Rivera"). Say it out loud before prompt 1.
- Read Claude's three-line reply aloud. Its "Next prompt idea" is a ready-made prompt 2 if the group is stuck.
- If a build fails or the network drops: open the closest tool in `backups/` and keep the conversation going.
