# Arena School proposal design system

The standard for every proposal Arena sends to a school or partner. Distilled from Arena's first school proposal
(Oct 31 to Nov 2, 2026), which JJ reviewed line by line across eight rounds. It replaces the one-pager recipe as the
default for client-facing documents; one-pagers remain only for general, untargeted leave-behinds.

Reference build: the first client proposal, kept in the private Drive Proposals folder (it contains fees).

## Start a new proposal

```bash
cd kits/print
python3 new_proposal.py <folder-slug> "<Client full name>" "<Client short name>" [path/to/client-logo.png]
# e.g. python3 new_proposal.py isb-spring "International School of Beijing" "ISB" ~/Downloads/isb.png
# Client proposals contain fees: keep the finished folder out of git (docs/ is git-ignored) and file the PDF in Drive.
cd ../meeting-kit/<folder-slug>
# fill every yellow [Write: ...] placeholder in proposal.html, then:
python3 build.py      # refuses while placeholders remain; checks fit and orphans; writes the PDF + review/page-N.png
```

Files: `proposal/template.html` (the template), `site/arena-print.css` (all styles), `build.py` (render + checks),
`orphans.py` (one-word last lines), `measure_centering.py` (digits in number squares and circles),
`proposal/Arena-Proposal-Template-sample.pdf` (the template rendered with placeholders showing).

## Who reads it

Every proposal has two readers. Write for both on every page.
1. **The contact** (a teacher or program lead) who asked for it and knows the details.
2. **School leadership**, to whom it will be forwarded, who has never heard of Arena and decides on budget and on
   future work (summer programs, intensives, teacher training).

So: Arena is introduced before the proposal; arenaschool.org is visible on the cover and in the first About paragraph;
nothing would embarrass the contact if forwarded upward.

## Page structure (six A4 pages)

| Page | Content | Reuse |
|---|---|---|
| 1 · Cover | Short navy band (no photo): Arena wordmark and "A member of" Anthropic Startup Program / OpenAI Partner Network; school-year eyebrow; headline "Proposed … for {client} *{program}*" with one italic accent; one-line lede. Meta row: **Prepared for** (client logo, no personal names) · **Prepared by** (Arena wordmark + arenaschool.org) · **Date**. Then a full-width **Summary** and a ruled **Contents** list with page numbers. | Client-specific |
| 2 · 01 About Arena School | Intro paragraph (agency, taste, craft; based in Beijing; arenaschool.org), the five-day intensive as a 5-step strip, seasonal programs table (summer and winter), "Also during the school year" cards. | Standard: keep; update programs and dates as they change |
| 3 · Team and proof | Co-founder cards (bios match about.html), "Taught at" and "Team from" logo rows, "What students have built" project cards, "Why this matters now" stats with source. | Standard: approved wording only |
| 4 · 02 Proposal, part 1 | "What we understood" and "Objectives" side by side, then Part 1 as a run-of-show table (time, segment, content), then any student resource. | Client-specific |
| 5 · Proposal, part 2 | Part 2 intro (what we lead vs what stays with the client's staff), a `.flag` box for the open question that blocks scheduling, what each day would cover (no times), a light "While we are on campus" note, outcomes and what the client provides, "Looking ahead" as one paragraph. | Client-specific |
| 6 · 03 Fees, terms, and next steps | "How we normally charge" (per student, no number; the standard day rate per facilitator (kept in the private Drive Proposals folder, not in this public repo)), the fee table, Terms and Next steps side by side, navy contact band with both co-founders' emails. | Client-specific numbers |

## Components (classes in `site/arena-print.css`)

- **Page:** `.pg` (A4), `.rh` running header (navy wordmark + "Proposal for {client} · {Month Year}"), `.rf` footer
  ("Arena School · Confidential proposal for {client}" + page number), `.in` content area.
- **Section head:** `.sh` with `.num` navy square (01, 02, 03) + `h2` + one-line dek.
- **Blocks:** every child of `.in` is a `.block`; blocks are separated by a hairline with a fixed rhythm.
  Rhythm classes on `.in`: base 4.6mm, `.roomy` 6mm, `.airy` 7.4mm, `.airy.airier` 9.5mm. Choose per page so every page
  ends roughly 8 to 25mm above the footer. Never stretch gaps with space-between.
- **Text:** `.lead` (intro paragraph), `.copy` (body), `h3` (block title), `.k` (small-caps label), `.sub` (secondary line).
- **Lists:** `ul.tick` (dot bullets; `.cols2` for two columns), `ol.num-list` (numbered circles, digits centered).
- **Cards:** `.card` (hairline), `.card.alt` (tint, no border), `.card.person`, `.proj` (photo + label + title + caption),
  `.day` (five-step strip). Sibling cards in one row share a style.
- **Tables:** `table.t` (hairline rows, caps headers); `td.when` / `td.what` for run-of-show; `tr.total` for fee totals;
  `.toc-list` for the cover contents; `.seasonal` for the programs table.
- **Callouts:** `.flag` (thin navy border) for a question the reader must answer; `.note` (blue left rule, tint) for a
  light aside. Neither is decorated further.
- **Credentials:** `.logorow` with greyscale marks at one darkness.
- **Close:** `.contact` navy band.
- **Utilities:** `.nw` (keep a name or stat on one line), `a.pl` (brand-blue link, no underline), `.ph` (yellow
  placeholder; the build refuses to export while any remain).

## Copy rules

- **Tone:** a business document, not a pitch. No hype, no retail-discount theatrics, at most one mention of future work
  ("Looking ahead"), and the on-campus meeting note stays light, never a formal ask.
- **The client's own material:** follow their outline and titles; add Arena's angle as plain sentences (no
  "Our addition" labels); don't repeat their specific examples back verbatim; describe at the level of the format.
- **Never:** mention students' finances or scholarships; call the client's program "ungraded" or similar;
  name the contact on the cover; write "line managers"; promise free tools, tools "tested to work in China", or
  accounts (point students to options, such as DeepSeek and Kimi, and say we do not provide accounts); lay out a timed
  on-site schedule before contact time is confirmed; ask for anything already agreed (such as a confirmed date).
- **Fees:** never publish per-student prices ("priced per student" only). Value on-campus days at the standard day rate per facilitator (kept in the private Drive Proposals folder). A short online session (30 to 60 minutes) gets a dash in the Standard column and "Included" in
  the package column; never value it at a day rate. State the discount in words ("more than two-thirds below our
  standard day rates"). No fee number on the cover. No "valid until".
- **Approved proof only** (see `meeting-kit/CLAIMS.md`, `CONTENT-RULES.md`): Hong Kong 2025 is a five-day course
  "taught by Phillip An for Bodley Academy"; ISB judges are "founders and operators from Harvard, Stanford,
  Y Combinator, and AI labs"; never state the ISB cohort size, prize amounts, or "100% launched"; "A member of" (never
  "partnered with") Anthropic Startup Program and OpenAI Partner Network; unverified claims (for example the
  Cursor/SpaceX sale figure) stay out.
- **House style:** American spelling, Oxford comma, no em dashes, curly quotes, sentence-case headings,
  "Y&nbsp;Combinator" never split.

## Layout rules

- Paragraphs span the full divider width (no max-width on body copy).
- No one-word last lines anywhere (`text-wrap: pretty` is on; `orphans.py` must show only date/city lines).
- Digits optically centered in `.num` squares and numbered circles (`measure_centering.py`, within 0.5px).
- Navy bands bleed past the page edge (no white hairline); the PDF uses the CSS page size (210 by 297mm).
- One table or card row never ends in a double hairline.
- Client logos: get a high-resolution file from the client; logos pulled from school websites are often too small and print soft.

## Before sending

1. `python3 build.py` passes on all six pages, with no placeholders left.
2. `orphans.py` lists only date and city lines.
3. Look at every `review/page-N.png`.
4. Read it once as the contact and once as the head of school.
5. For anything high-stakes, run parallel read-only audits (visual format, audience and tone, facts against sources,
   regression against the client's and JJ's feedback), then apply fixes in one pass in the single source file.
