# Arena School print kit

> **Proposals:** use the proposal design system in `proposal/` (spec: `proposal/DESIGN-SYSTEM.md`; start one with
> `python3 new_proposal.py <slug> "<Client full name>" "<Client short name>" [logo.png]`). It is the default for any
> client-facing document. The recipe below is the shared visual foundation and applies to one-pagers too.

The default for every new Arena PDF (proposals, one-pagers, briefs, leave-behinds), starting Oct 31, 2026.
It matches arenaschool.org's **pro style** (live since Oct 16, 2026). The riso recipe (beige `#F3E9DD` paper, dot grid,
seal watermark, serif-only, `riso-v2/site-preview/_kit/onepager.html`) is **retired for new documents**.

Start new proposals with `new_proposal.py` (see `proposal/DESIGN-SYSTEM.md`).

## Files
- `site/arena-print.css`: the system (tokens copied from the site's `css/pro.css`, components below).
- `site/fonts/gf.css` + `site/fonts/files/`: Geist and Newsreader, served locally (Google Fonts is unreliable from Beijing).
- `site/logos/`, `site/photos/`: mirrored from the live repo (phillipan14/arena-school). Refresh with
  `gh api repos/phillipan14/arena-school/contents/<path> -H "Accept: application/vnd.github.raw" > site/<path>`.
- `build.py <doc.html> <out.pdf>`: renders A4, writes `review/page-N.png`, and fails if any page runs into its footer.

## Recipe
1. **Ground:** white pages, `#F5F7FA` for tinted cards. No paper texture, dot grid, or watermark.
2. **Type:** Geist for body (8.8pt / 1.5), labels, and tables; Newsreader 500 for headings, names, and numbers.
   Labels are Geist 600, 7.2pt, caps, 0.12em tracking, `#4A5578`. One italic accent per headline at most.
3. **Color:** navy `#0B1A4A` ink, action blue `#22458A` / `#2F55A8`, light accent `#C9D6F2` on navy, hairlines `#E2E6EE`.
4. **Cover (multi-page) or header band (one-pager):** navy band, a real program photo on the right fading into the navy
   from the left, ivory wordmark, then "A member of" + Anthropic *Startup Program* + OpenAI *Partner Network*.
   Photo captions must say exactly what and where (e.g. "Demo day at the International School of Beijing, 2026").
5. **Sections:** a navy number block (`01`, `02`) with a Newsreader title and a one-line dek.
6. **Blocks:** hairline cards with a 2mm radius, tables with hairline rows and caps headers, `.note` (blue left rule)
   for context, `.flag` (thin navy border, no thick top rule) for anything the reader must answer.
7. **Credentials:** "Programs run at" and "Team from" logo rows, all marks greyscale at one darkness.
8. **Inner pages:** running header (navy wordmark plus the document title) and a footer with the page number.
9. **Close:** a navy contact band with named people and their arenaschool.org addresses.
10. **Rhythm:** every block inside `.in` is separated by a hairline divider with fixed padding (4.6mm; `.in.airy` = 6mm
    for a lighter page). Never stretch gaps with space-between. A table ending a block drops its last rule so lines never double.
    Balance pages by moving whole blocks or using `.airy`, not by leaving a band at the foot.
11. **Proof of work:** prefer `.proj` cards (photo, label, project, honest caption) over a large decorative photo.
    Approved project lines (ISB parent talk, Oct 2026): five games built to publish on Steam (ISB 2026); an all-in-one
    productivity tool tracking progress, sleep, and working time (ISB 2026); a sign-language-to-speech app built by a
    ten-year-old (Hong Kong 2025). No student names, prizes, or admissions claims; photos show presenting, not the product.
12. **Checks:** no em dashes, Oxford commas, American spelling, curly quotes, no orphaned words in headings, no
    dead bands at the foot of a page (rebalance per item 10), and `build.py` passes on every page.

## Writing a proposal (vs. a sales one-pager)
Business tone, not a pitch. Cover (JJ, Oct 31): a short navy band with no photo (`.cover-top.plain`), then
"Prepared for" / "Prepared by" as LOGOS (client logo in `site/logos/clients/`, Arena navy wordmark), no personal names,
the date, and no "valid until"; arenaschool.org under the Arena logo; then a full-width summary paragraph and a ruled
contents list with page numbers (NO "At a glance" table: it duplicated the contents); then who we
are, what we understood, objectives, the plan, open questions flagged in a `.flag` box, fees against our standard
rates, terms, and next steps. Don't publish per-student prices; state the discount against the day rate instead
(the day rate is kept in the private Drive Proposals folder).

Never promise free tools or tools "tested to work in China" (JJ, Oct 31): describe the TYPES of AI (chatbots, coding
agents, image/voice/video generation) and refer students to low-cost options such as DeepSeek and Kimi, stating that we
point to options rather than provide accounts. Don't lay out a timed on-campus schedule before the school confirms
contact time; list what the days would cover instead. A light "while we are on campus" note on who we'd like to meet
(leadership, program team) is welcome; never a formal ask.

## Audience and copy rules (JJ, Nov 1, 2026)
- Proposals are read twice: by the program lead AND forwarded to school leadership who don't know Arena. Put
  arenaschool.org on the cover and in the first About paragraph. Nothing that embarrasses the contact if forwarded
  (no "line managers", no internal notes, no individual names on the cover).
- Never mention students' finances (scholarships, "low-cost because…"). Don't describe a client program as "ungraded".
- Don't repeat the client's own examples back verbatim; describe sessions at the level of the format.
- Every paragraph spans the divider width (no max-width on body copy); no one-word last lines (`orphans.py` checks);
  digits optically centered in number squares and circles (`measure_centering.py` checks).
- Rhythm classes: base 4.6mm, `.roomy` 6mm, `.airy` 7.4mm, `.airy.airier` 9.5mm; pick per page so every page ends
  roughly 8 to 25mm above the footer.
