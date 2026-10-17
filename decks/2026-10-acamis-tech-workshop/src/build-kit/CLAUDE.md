# ACAMIS build session: rules for Claude Code

A room of teachers is watching this screen. A group of them describes a small tool for their own school week, and you build it **fast**. Every prompt should end with a working page open in the browser in about two minutes.

## How to build
- **Never ask clarifying questions.** Make sensible assumptions, then state them in one short line at the end.
- **One file per tool:** `builds/<short-slug>/index.html`. Start by copying `template.html` there, then fill it in. Everything (HTML, CSS, and JavaScript) stays inline in that file.
- **No setup:** no npm, no frameworks, no build step, no server. No external CDNs, fonts, or APIs (this is China; they may not load). Plain JavaScript only.
- **Open it when done:** run `open builds/<short-slug>/index.html`. On a later prompt about the same tool, edit that same file and open it again.
- **Keep it small:** one screen, one job, big readable text (a projector is showing it). It must work on a phone too.
- **Save the user's work** in `localStorage` so a refresh doesn't lose it, and add a "Clear" button.
- **Sample data:** fill the tool with realistic placeholder content so it works the moment it opens. Make up names like "Student A" or "Ms. Rivera"; **never** use real student names or data.
- **No AI inside the tool.** The tool itself must not call any AI or network service. If the job needs language smarts, use templates, rules, or a word list the teacher can edit.
- Don't write tests, plans, READMEs, or extra files. Don't read files outside this folder.

## How to reply (the room reads it on the projector)
At most three short lines:
1. What you built, in plain English (no code words).
2. "Try this:" one thing to click or type.
3. "Next prompt idea:" one improvement the group could ask for.
Then one line of assumptions, if you made any.
