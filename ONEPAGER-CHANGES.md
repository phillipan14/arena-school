# One-pager: what changed (FLUENCY-BRIEF 2 and UPDATE, Oct 17, 2026)

Files replaced in place, same paths and names, so every link and the gated download (onepager.js, the `#onepager`
form on program and school pages) keep working: `onepager/arena-school-one-pager-{en,cn}.pdf` and the 520px `.jpg`
thumbnails. Link cache stamps moved from `?v=20261002` to `?v=20261017` on every page so browsers fetch the new files.
Source: `tools/one-pager/build.py` (writes `tools/one-pager/onepager-{en,cn}.html`, renders with Chrome headless to A4,
fails unless the PDF is exactly one page and nothing is clipped). The old source (`riso-v2/site-preview/_kit/`) is not
in this repo; the old PDFs were the base.

## Kept from the old version
- Structure: headline and mission, the three skills (agency, taste, craft), the team's schools and employers, programs
  by audience, "What we've run" with ISB, Bodley Academy, and Schwarzman College, and a closing "Bring Arena to your
  school" band.
- One A4 page, EN and CN.

## Changed
- **Design:** from the cream riso style (watermark, dotted grid, tinted cards, highlighted keywords) to the site's design
  system: a navy header with the ivory wordmark and one real photo (presenting at demo day, Beijing 2026), white
  ground, Newsreader and Geist, hairlines, one accent blue, greyscale logo rows, and the framework wheel.
- **Credibility:** added "A member of" with the Anthropic Startup Program and OpenAI Partner Network, exactly as on the
  site; team logos split into "Our team studied at" and "Worked at" rows; Kimi is the wordmark without the K icon.
- **Programs:** grouped as on the site's nav: for students; for teachers and schools (AI for Educators, Technology
  teams, School leaders, Conferences); for families (Mentorship, Community Dialogues, AI Fundamentals for Students @
  International School of Beijing); college and early career (AI Advantage Bootcamp).
- **New panels:** Learning approach (the wheel, "Learners decide. AI builds. Real people judge.", the four strands);
  AI fluency for the whole staff (the five levels); Student data comes first ("whose account is it?" and four
  commitments).
- **Selected programs:** copy now matches the site's case cards word for word.
- **Removed:** the "9.5/10 NPS" figure (no stats on the one-pager), per-program grade/length chips (folded into one
  line each), and the program descriptions that no longer match the site.
- **Contact:** phillip@arenaschool.org and arenaschool.org (was contact@arenaschool.org and a LinkedIn path that did
  not match the site's).
- **Links to it:** a "Download one-pager" link in the footer (partials, EN + CN), the phone footer, the About page's
  closing section, and beside the Schools page's Programs heading; all go to the existing gated form (`/schools#onepager`).
