# Homepage Design Brief

_Started 2026-05-29 08:16 UTC_

---

## User

<system-info comment="Only acknowledge these if relevant">
Project title is now "Arena School"
Project is currently empty (no files)
Current date is now May 29, 2026
</system-info>

<pasted_text name="Pasted text (300 lines)">
# Arena — Website Design Brief

*A prompt to hand to Claude (or claude.ai design / Stitch) to generate the Arena website end-to-end. Modeled on the design DNA Phillip built across **Quartz Labs** (quartzlabs.ai) and **Allston Labs** (allstonlabs.vercel.app) — but tailored for Arena's voice (warmer, more editorial-literary, education-rooted).*

---

## 1. Context — what Arena is

You are building the homepage for **Arena**, the world's first AI-native school, going to be open-sourced from day one.

The thesis: every kid is about to have a tutor smarter than their teacher. School has spent twelve years on the one thing AI now does better than any teacher — transferring foundational knowledge — and almost no time on the things that actually decide a life: **agency, taste, creativity, judgment, the courage to build something real and the discipline to make it good**. Arena uses AI to clear the foundational floor fast, so the rest of the day is finally free for what school never taught.

The structure that worked in pilot (HK Summer 2025, **9.5/10 NPS** with Bodley Academy / Rhodes House at Oxford, 20 students):

- **Mornings** — AI tutor that knows the student, moves them through curriculum at their own pace (Alpha School-style: 2.6× faster in two hours)
- **Afternoons** — building real things (a company, a book, a song, a managed property, a campaign) with a human mentor who knows their name
- **Rotating hubs** — cohorts rotate between **San Francisco** (building & shipping), **Shenzhen** (making & manufacturing), and **Bali** (reflection & balance). A portable learning hub — a WeWork for kids building the future — not a single campus

**Founder:** Phillip An. Caltech CS → McKinsey → Harvard MS/MBA → YC W21 founder (Homebase, scaled to 80+ across 4 SEA markets, $50M+ raised, Forbes 30U30 Asia) → Schwarzman Scholar at Tsinghua → building Skylarq AI on Anthropic's Claude API. Chinese-immigrant parents who cleaned houses in South Africa before they could afford America so their son could go to the right schools. Their whole life was a bet on education. It worked. But the institutions that produced him will not produce the next generation. This is the personal debt that motivates Arena.

**Site goals (in order):**
1. Make the reader feel that AI just changed school forever and Arena has the structure for what comes next.
2. Prove the pilot worked (9.5/10 NPS, the 10-year-old who shipped a sign-language-to-speech AI in 5 days, two kids → Stanford / elite UK boarding schools).
3. Recruit Cohort Zero applicants (25 in-person + 250 virtual).
4. Recruit external operators to launch hubs ("the protocol is open-source — start your own").
5. Make a case strong enough that a thoughtful founder, an aligned philanthropist, or a fellow operator wants to meet.

---

## 2. Visual system — design tokens

Inherit the design DNA of Quartz Labs and Allston Labs (premium, institutional, editorial), but make Arena **warmer and more human** — this is about children, learning, hope, and ambition, not infrastructure.

### Color tokens

```
/* Light editorial primary (Arena's home) */
--bg-paper:        #F4EFE3  /* warm cream, never #fff */
--bg-paper-soft:   #EDE6D6  /* subtle alternate band */
--text-ink:        #1A1A1D
--text-ink-soft:   #52525B
--text-ink-muted:  #88857B
--border-paper:    #D6CFBC

/* Dark contrast (for hero / closing / case sections) */
--bg-dark:         #0F0E0C
--bg-dark-surface: #16140F
--text-cream:      #F0EEE8
--text-cream-soft: #A6A39A
--border-dark:     #2A2620

/* Arena accent — saffron/ember (from the existing Arena brand on the action plan) */
--accent:          #C45D35
--accent-soft:     rgba(196, 93, 53, 0.12)
--accent-strong:   #A24A26

/* Optional secondary accent for the rotating-hubs map / data visuals */
--accent-blue:     #1E3A5F  /* deep institutional, used sparingly */
```

**Default mode is cream/paper**, with dark sections punctuating (hero anchor, Manifesto quote, closing CTA). This inverts the Quartz/Allston "dark default" — appropriate because Arena is hopeful/aspirational, not infrastructure/serious.

### Typography

```
/* Families */
--font-display: 'Newsreader', 'Source Serif 4', Georgia, serif;     /* editorial weight, italic-capable */
--font-body:    'Geist', 'Inter', system-ui, -apple-system, sans-serif;
--font-mono:    'Geist Mono', 'JetBrains Mono', ui-monospace, monospace;

/* Scale (fluid, clamp-based, mirrors Allston Labs) */
--text-hero:        clamp(56px, 6.5vw, 112px);  /* the headline; light-weight italic Newsreader */
--text-h2:          clamp(40px, 4.2vw, 72px);   /* section headers */
--text-h3:          clamp(24px, 2.4vw, 32px);
--text-body-lg:     clamp(19px, 1.4vw, 22px);
--text-body:        17px;
--text-small:       15px;
--text-eyebrow:     11px;                       /* tracked +0.14em, uppercase */

/* Weights */
--w-display:        300;                        /* light Newsreader for hero */
--w-body:           400;
--w-emphasis:       500;

/* Tracking */
--tr-display:       -0.018em;                   /* tight on display */
--tr-eyebrow:       0.14em;                     /* loose on small caps */
```

**Voice on the page:** Newsreader italic for emotional/editorial moments (the manifesto quote, the parents-bet paragraph). Geist for body, navigation, all UI chrome. Geist Mono for stats, milestones, and data labels.

### Spacing & layout

```
--section-py:      clamp(120px, 14vh, 200px);  /* generous vertical rhythm */
--section-px:      clamp(24px, 4vw, 80px);
--container-max:   1240px;
--container-narrow: 720px;     /* for proposal-like prose */
--container-essay:  640px;     /* for the manifesto / debt paragraph */
```

Use whitespace generously. Allston-style breathing room is non-negotiable — this is editorial, not a SaaS landing page.

### Motion

- Reveal-on-scroll with IntersectionObserver (mirror Allston's `useReveal`); content elements fade-up 24px, 80ms stagger.
- Number count-ups on the proof stats (e.g., "9.5/10 NPS", "250 virtual cohort", "50+ schools by 2031") — animate from 0 over ~1200ms when scrolled into view.
- Hover states: subtle (4px lift on cards, accent underline grow on links).
- No parallax. No bouncy easings. Cubic-bezier(0.2, 0, 0, 1) only.

---

## 3. Voice & tone

- **Literary, plain, ambitious.** Read like Phillip's manifesto (`tomyfuture.kids`) — sentences carry conviction; metaphors are vivid but earned; no SaaS-deck speak.
- **Honest about stakes.** "The path that worked for me will not work for the generation behind me." "If the open tutor underperforms, that's the result and I'll publish it."
- **Anti-credential.** Don't open with credentials. Open with the insight. Credentials show up later as ground truth, not as the pitch.
- **Concrete numbers.** Every claim has a number or a name behind it (9.5/10 NPS, Bodley Academy / Rhodes House, two students → Stanford, 10-year-old shipped in 5 days, 2.6× faster).
- **First person plural / first person singular** — "I built the pilot," "We rotate between SF, Shenzhen, Bali" — never marketing third person.
- **No marketing-speak taglines.** Avoid "The protocol is the product. The cohort is the proof." That kind of mirrored parallel structure reads as forced.

---

## 4. Site structure (single-page first, multi-page later)

Start with a single-page homepage. Sections, in order:

1. **Nav** — `Arena` wordmark left (Newsreader italic), thin links right (Manifesto · Pilot · Cohort Zero · Operators · Apply), CTA button "Apply for Cohort Zero →"
2. **Hero** — the inversion thesis
3. **Pilot proof band** — HK 9.5/10 + the 10-year-old story
4. **The structure** — Morning AI / Afternoon build / Rotating hubs (3-column or 3-row)
5. **The rotating hubs map** — illustrated globe or stylized map: SF · Shenzhen · Bali, with each city's "what's taught here"
6. **The manifesto** — the personal arc paragraph (dark inversion band, editorial italic)
7. **The open-source protocol** — what's being shipped on GitHub (ArenaTutor v0, Virtual Cohort, Protocol bundle)
8. **The bet** — 10 hubs by 2031, 1,000+ students, protocol forked by 50+ schools (count-up stats)
9. **Cohort Zero application strip** — eligibility, dates, "Apply" CTA
10. **For operators** — "Run an Arena hub" — what we hand over, who we want
11. **Closing CTA** — dark band, "Build it with us." with two paths: apply / operate
12. **Footer** — wordmark, links, contact, license note ("Arena Protocol is MIT-licensed")

---

## 5. Section-by-section spec

### 5.1 Hero (paper background)

**Headline (Newsreader italic, light, ~104px):**
> *Every kid is about to have a tutor smarter than their teacher.*

**Subhead (Geist 500, 22px):**
> Arena is the school for that world — open-source, so a charter in Detroit or a village in Bihar can run it too.

**Beneath, one line of mono eyebrow:** `Cohort Zero · 25 students + 250 virtual · 4 continents · Fall 2026`

**CTA pair:** "Apply for Cohort Zero" (filled, accent) + "Read the Manifesto" (ghost).

**Right-side visual:** A subtle, slowly drifting Arena monogram (suggested: a circle bisected by a slim vertical — the "arena" — or three small hub-dots arranged in a triangle representing SF/Shenzhen/Bali). Single-color accent stroke on cream.

### 5.2 Pilot proof band (paper, slight cream-soft alternate)

A stat bar with **3 numbers + a vignette:**

```
9.5/10  pilot NPS                 5 days        2 students
Bodley Academy ·                  built a real    → Stanford
Rhodes House at Oxford             AI product       → elite UK boarding schools
Hong Kong, Summer 2025             at age 10        
```

Below the bar, a 2-column block: **left** a photo from the pilot (sticky-notes, kids collaborating, classroom — same b-roll the EV video uses); **right** a short editorial paragraph (~80 words) telling the 10-year-old's story in Phillip's voice.

### 5.3 The structure (paper)

Three full-width rows (or three columns on desktop, stacked on mobile):

- **Mornings — the tutor that knows them.**
  Body: AI tutor that knows the student moves them through foundational knowledge at their own pace. Alpha School-style: 2.6× faster in two hours.

- **Afternoons — building things that matter.**
  Body: A company, a book, a song, a managed property, a public campaign — with a mentor who knows their name. Through the doing: agency, taste, creativity, judgment, the courage to build, and the discipline to make it good.

- **Rotating hubs — a school that follows the work.**
  Body: SF (building & shipping), Shenzhen (making & manufacturing), Bali (reflection & balance). A portable learning hub — a WeWork for kids building the future — not one campus locking every kid into one zip code.

Each row has a small accent glyph (sun-pulse / hammer-spark / globe-dot) and a thin divider.

### 5.4 Rotating hubs map (dark inversion band)

A single hero-scale illustration: stylized world arc with 3 large dots (SF / Shenzhen / Bali) connected by a slim accent line tracing the cohort's path. Each city: 1-line caption beneath the dot ("Build & ship" / "Make & manufacture" / "Reflect & balance"). Below, a sentence of editorial italic: *"The most important things a person learns aren't all taught in one room."*

### 5.5 The manifesto (dark band, editorial)

The personal-arc paragraph from the EV proposal, set in Newsreader italic ~32-40px:

> *My parents were Chinese immigrants who spent years in South Africa, cleaning houses and scrubbing toilets, because they could not speak English. They moved us to America so I could go to the right schools. Their whole life was a bet that if education worked out, the rest would follow. It worked. But the institutions that produced me will not produce the generation behind me. The system that made me trained compliant high-scorers for a world that paid for compliance. That world is gone.*

Below, a small mono attribution: `— Phillip An, founder` and a link to read the full manifesto on tomyfuture.kids.

### 5.6 The open-source protocol (paper)

A 3-card row:

- **ArenaTutor v0** — open base model fine-tuned on K-12 + college curriculum and the learning-science corpus, benchmarked in public against a frontier model. GitHub link. License badge: MIT.
- **Free Virtual Cohort** — 250 learners, 4+ continents, no tuition. On the same tutor. Apply card.
- **Arena Protocol** — tutor weights + curriculum + mentor playbook + admissions handbook + hub-launch handbook. The "fork to start your own Arena" bundle. GitHub link.

Each card has a small mono milestone line (e.g., `Shipping Month 4` / `250 enrolled by Month 9` / `Permissive license · Month 12`).

### 5.7 The bet (paper, with count-up stats)

A bold editorial paragraph on the 2031 vision, then **four count-up stats** in a row:

```
10           1,000+       50+              4
hubs by      students     schools forking  continents
2031         rotating     the protocol     by Year 2
             annually     by 2031
```

### 5.8 Cohort Zero application strip (cream-soft band)

Two-column: **left** a brief eligibility line ("Ages 16–22 · ≥50% low- and middle-income · ≥4 continents · 12 months full-time · Tuition-free for accepted students"); **right** a large "Apply for Cohort Zero →" CTA + a small "Applications close [date]" mono line.

### 5.9 For operators (paper)

A pitch directed at people who would launch their own hub. Short. Two CTAs: "Read the hub-launch handbook" + "Tell us you're interested."

### 5.10 Closing CTA (dark band)

A single editorial line, large:
> *Build it with us.*

Below: two buttons side by side — "Apply for Cohort Zero" (filled accent) + "Run an Arena Hub" (ghost).

### 5.11 Footer (dark)

Four columns: Arena wordmark + tagline / Manifesto links / Apply links / License + email. License: "Arena Protocol is MIT-licensed. Fork it."

---

## 6. Voice samples (copy verbatim where helpful)

- "AI doesn't just hand every kid a better tutor. It clears the floor — fast — so the whole day is finally free for the things school was never built to teach."
- "AI handles knowledge transfer; humans handle judgment, taste, courage, and the felt experience of being believed in."
- "The kids who most need this aren't all in the Bay Area, and neither is the edge of the AI century."
- "If the open tutor underperforms badly enough that no operator wants to run it, that's the result and I'll publish it."

---

## 7. Reference style anchors

- **Quartz Labs** (`~/quartz-labs/index.html` + `styles.css`) — the dark editorial design system, news ticker, comparison tables, modality grids, count-up stats, cream band breaks, audit-scored sections. Inherit the *rigor* and *spatial logic*. Invert the palette to paper-primary.
- **Allston Labs** (`~/skylarq-site/index.html` + `app.jsx`) — the fluid clamp-based type scale, the section padding rhythm, the Cal.com booking integration, the reveal-on-scroll motion. Inherit the *rhythm* and *interaction grammar*.

---

## 8. Technical constraints

- **Stack:** static HTML + a single CSS file + minimal vanilla JS (or React via the Allston-style single-file `app.jsx` pattern if it makes sense). No Next.js, no Tailwind. Treat this like a long-form editorial site.
- **Fonts:** Geist + Newsreader from Google Fonts, single `link` tag (mirror Quartz/Allston).
- **Deploy target:** Vercel, single `vercel.json` like the other two repos.
- **Mobile first.** Single column at narrow widths; dropdown nav.
- **Accessibility:** real heading hierarchy (h1 once), prefers-reduced-motion guard, proper alt text on photos.
- **No third-party trackers.** Plausible at most.

---

## 9. Evaluation — iterate R1 → R5 like Quartz

Once a draft is built, audit it like the `~/quartz-labs/AUDIT.md` pattern. Score each section 1-10 on:

- Visual hierarchy
- Whitespace rhythm
- Editorial voice
- Concreteness (numbers, names, dates present)
- Motion polish (subtle, not gimmicky)
- Mobile parity
- Information density (dense without crowding)

Target ≥9.0 average by R5. Each round, write 2-3 lines per section on what improved and what still needs work. Phillip will read the audit alongside the page.

---

## 10. Out of scope (for first draft)

- Multi-page (labs / network / cases). Single homepage first.
- Authenticated apply flow. Use a Typeform or simple `mailto:` for v1.
- Internationalization. English only for v1.
- Newsletter sign-up. Hold for v2.

---

## 11. Deliverable

A working `index.html` + `styles.css` (+ minimal `motion.js` if needed), in a folder layout that mirrors `~/quartz-labs/`. Deploy-ready for Vercel. Include a 1-page `AUDIT.md` scoring R1 against the above dimensions, with a short note on what to push for in R2.

---

*Generate it now. Treat it as if it's going live next week to recruit Cohort Zero.*

</pasted_text>

<!-- The user explicitly selected the following skills for this project, as attachments to their message. These are not optional context — they define how you work. Use them. -->
<attached-skill name="Hi-fi design">
Create a high-fidelity, polished design.

Follow this general design process (use the todo list to remember):
(1) ask questions, (2) find existing UI kits and collect design context — copy ALL relevant components and read ALL relevant examples; ask the user if you can't find them, (3) start your file with assumptions + context + design reasoning (as if you are a junior designer and the user is your manager), with placeholders for the designs, and show it to the user early, (4) build out the designs and show the user again ASAP; append some next steps, (5) use your tools to check, verify and iterate on the design.

Good hi-fi designs do not start from scratch — they are rooted in existing design context. Ask the user to Import their codebase, or find a suitable UI kit / design resources, or ask for screenshots of existing UI. You MUST spend time trying to acquire design context, including components. If you cannot find them, ask the user for them. In the Import menu, they can link a local codebase, provide screenshots or Figma links; they can also link another project. Mocking a full product from scratch is a LAST RESORT and will lead to poor design. If stuck, try listing design assets and ls'ing design system files — be proactive! Some designs may need multiple design systems — get them all. Use the starter components (device frames, design canvas) to get high-quality scaffolding for free.

When designing, asking many good questions is ESSENTIAL.

Give options: try to give 3+ variations across several dimensions. Mix by-the-book designs that match existing patterns with new and novel interactions, including interesting layouts, metaphors, and visual styles. Have some options that use color or advanced CSS; some with iconography and some without. Start your variations basic and get more advanced and creative as you go! Try remixing the brand assets and visual DNA in interesting ways — play with scale, fills, texture, visual rhythm, layering, novel layouts, type treatments. The goal is not the perfect option; it's exploring atomic variations the user can mix and match.

CSS, HTML, JS and SVG are amazing. Users often don't know what they can do. Surprise the user.

If you do not have an icon, asset or component, draw a placeholder: in hi-fi design, a placeholder is better than a bad attempt at the real thing.
</attached-skill>

<attached-skill name="Interactive prototype">
Create a fully interactive prototype with realistic state management and transitions. Use React useState/useEffect for dynamic behavior. Include hover states, click interactions, form validation, animated transitions, and multi-step navigation flows. It should feel like a real working app, not a static mockup.
</attached-skill>

<attached-skill name="Skylarq Design System (design system)">
[Design System] This project uses the **Skylarq Design System** design system. This is a binding choice for visual style — every visual must follow it. Don't invent colors, type, spacing, or components not grounded here.

Scope: the design system is a visual style reference only. Its guide may describe example products, brands, or people that are unrelated to the user and unrelated to the subject of this conversation. Never treat anything in the design system as a fact about the user, their work, or the topic they asked about.

    Explore it to find what you need:
    - Always copy out the fonts and colors you need
    - For prototypes and designs, always copy out any relevant components
    - If the design system contains existing mocks of products, and you were asked to design or prototype something similar, copy and fork those mocks to start your design. This helps you make high-quality designs.

    Explore it quickly to find relevant UI kits (e.g. mocks of existing products you can copy and fork)

Full system at `/projects/22ebc918-9a72-461a-a514-610092f19b07/`. Its guide is reproduced below so you don't need to fetch it:

<design-system-guide>
# Skylarq Design System

**Brand**: Skylarq Desktop Assistant
**Source**: `redesign/local-ui-improvements` branch (extracted 2026-04-20)
**Snapshot as of**: 2026-04-20

---

## What is Skylarq?

Skylarq is a **desktop assistant** — a native macOS-first app that sits alongside your work and runs a roster of specialized AI agents (CEO, Sales, Outreach, Meeting, Growth, Workflow, Research, Generalist, Network). You summon them through a global **command bar**, chat with them in a focused conversation surface, and hand off work between agents. The app is built for knowledge workers who live in their inbox, CRM, and LinkedIn all day — Skylarq is the always-on co-pilot threaded through all of it.

The visual character is **warm, quiet, and specifically "not a chat app"**. Where most AI products lean on cool blue/purple gradients and heavy glass, Skylarq commits to a warm off-white paper background (`#FFFCF9`), a single rust-orange accent (`#C45D35`), and generous use of `Plus Jakarta Sans` at tight negative tracking. The product feels like a high-end native tool, not a web app.

### Products represented

This design system covers a **single product surface**: the Skylarq desktop app (macOS). Within the app there are several surfaces:
- **Command bar** — global, blurred-overlay invocation
- **Chat / conversation** — the primary work surface
- **Agent switcher** — colored agent chips, detail panels
- **Sidebar** — collapsible nav (48px ↔ 180px)
- **Settings / preferences** — standard native-style forms

There is no marketing site, mobile app, or docs site in this snapshot.

---

## Sources

| Source | Path / Reference |
|---|---|
| Codebase (primary) | `redesign/local-ui-improvements` branch — raw token extraction was provided inline at 2026-04-20. Full codebase was not attached to this project; tokens, layout dimensions, and component patterns were lifted from the extraction document. |
| Figma | Not provided |
| Slide deck template | Not provided (no slides created) |
| Brand assets (logos, marks) | Not provided — a placeholder wordmark + icon were synthesized and are flagged for the user to replace. |

> **Caveat for the reader:** the UI kit in `ui_kits/desktop/` is a high-fidelity recreation built from the token spec, not a 1:1 port of the production source. Component implementations are cosmetic approximations; visual values (colors, radii, shadows, spacing, type) are exact.

---

## Content fundamentals

Skylarq's copy is **quiet, direct, and human**. It speaks with the confidence of a good native app, not the eager hand-waving of an AI chatbot.

### Voice & tone
- **Second-person, active**. "Ask an agent." "Summon the command bar." Never "Let's get started!" or "I'll help you…".
- **Sentence case everywhere** — titles, buttons, menu items. Never Title Case. Never ALL CAPS except for the `.sk-overline` micro-label style (tracking +0.06em, 11px).
- **No exclamation points.** No "✨", no "Woohoo". The product confidence comes from restraint.
- **No emoji in product chrome.** Emoji appear only when a user types them. Agent identities use **colored dots or monogram chips**, not emoji avatars.
- **Agents speak in first person**, tersely. "Drafting the reply." "Found 3 matches in your inbox." Not "I've gone ahead and drafted…".
- **Errors are factual, not apologetic.** "Couldn't reach LinkedIn. Retry?" — not "Oops! Something went wrong 😔".

### Casing & rhythm
- UI labels: `Sentence case`
- Button text: verb-first, 1–3 words — `Send`, `Connect account`, `Try again`
- Placeholder text: ends without a period — `Ask Skylarq anything`
- Empty states: one short headline + one short line — `No conversations yet.` / `Summon the command bar with ⌘K to start one.`

### Examples pulled from the product

| Surface | Copy |
|---|---|
| Command bar placeholder | `Ask Skylarq, or pick an agent…` |
| New chat empty state headline | `What are we working on?` |
| Agent handoff toast | `Handed to Sales.` |
| Connection error | `LinkedIn disconnected. Reconnect to keep syncing.` |
| Destructive confirm | `Delete this conversation? This can't be undone.` |
| Settings section label | `Connections` (overline, tracking +0.06em) |
| Shortcut hints | `⌘K`, `⌘↵`, `Esc` — rendered in the mono face at 12px |

### Vibe

Think: **Linear's restraint** meets **Things 3's warmth** meets **Raycast's keyboard-first density**. Not chatty. Not cute. Competent.

---

## Visual foundations

### Palette

The palette is **warm-paper + rust accent**. Backgrounds are never pure white; the canonical `#FFFCF9` is noticeably cream. Text is never pure black; body text is `#1A1815` (warm near-black), secondary is `#3D3A36`. The dark theme inverts to a **warm near-black** `#0F0E0D` with the same accent logic.

- **One accent, one shade**: `#C45D35` (rust/terracotta). Used for primary CTAs, focus rings, and active-state indicators. Never used as a background fill for large surfaces — only for small hits of color.
- **Semantic colors are desaturated** in light mode (`#2D9164` success, `#C4860C` warning) and brighter in dark mode for legibility.
- **Agent colors are a 9-hue spectrum** used only as identifier chips / dots / borders at low saturation — never as backgrounds.
- **Borders are extremely subtle**: `rgba(26,24,21,0.06)` in light mode. The UI is mostly border-less; separation comes from background shade-shifts (`bg` → `bg-subtle` → `bg-hover`).

### Typography

- **Body**: Plus Jakarta Sans at weights 300/400/500/600/700.
- **Mono**: JetBrains Mono for shortcuts, code, and IDs.
- **Tracking**: `-0.01em` globally (tighter on headings: `-0.015em` to `-0.02em`).
- **Sizes**: a granular ramp from 11px (`2xs`) to 32px (`3xl`). The workhorse is **14px (`sm`)** — most body UI sits there. 16px (`base`) is the comfortable reading size for chat transcripts.
- **Antialiased** + `optimizeLegibility` globally.

### Spacing

Strict **4-px grid** with named tokens (`xs`–`2xl`) plus a few off-grid escape hatches: `18px`, `22px`, `52px`, `56px`, `60px`. The off-grid values exist for specific composite components (e.g. 44-px input + 8-px gap = 52px row).

### Backgrounds, textures, imagery

- **No full-bleed imagery** in the product chrome. No gradient hero backdrops.
- **No illustrations**. No hand-drawn elements, no mascots, no spot art.
- **No repeating patterns or textures**.
- **Glass/blur appears only on overlays** — the command bar overlay (`blur(8px)` + `rgba(0,0,0,0.5)`), the sticky header (`blur(12px)`), and connection tooltips (`blur(20px)`). Everywhere else is flat.
- Imagery, when it appears (e.g. user avatars, contact photos), is rendered in circular crops with no filter. Warm, natural, no grain.

### Motion

Motion is **short, spring-out, and purposeful**. The default easing is the "spring" curve `cubic-bezier(0.16, 1, 0.3, 1)` — feels like a soft landing, never bouncy.

- **Durations cluster at 150ms and 250ms.** Hover/press is 150ms default; entrance animations are 250–300ms.
- **Ambient animations** (shimmer, gentlePulse, breathe) run at 2–4s and are reserved for loading and "agent is thinking" states.
- **Bounce easing exists but is rarely used** — only on celebratory confirmations.
- No parallax, no scroll-jack, no page transitions.

### Interactions

- **Hover**: backgrounds shift from `bg` → `bg-hover` (~3% darker); borders deepen from 6% to 12% opacity. Text stays put.
- **Press (active)**: `scale(0.97)` on buttons — that subtle squeeze is the signature. No color flip.
- **Focus**: 2-px outer ring at 20% accent opacity (`0 0 0 2px rgba(17,24,39,0.2)` default, or accent-tinted on inputs).
- **Disabled**: `text-faint` color, no background change, `cursor: not-allowed`.

### Borders, corners, elevation

- **Corners**: `xl` (16px) is the default for buttons, cards, modals. `lg` (12px) for nav items. `md` (8px) for inputs and dropdowns. `full` (9999px) for badges, pills, avatars. The **bottom sheet** is the only surface that uses `2xl` (24px).
- **Borders**: mostly omitted. When present, always the 6%/8% semi-transparent warm-black/white — never a solid mid-gray.
- **Shadow ladder** (8 tiers): `soft` (ambient) → `card` → `card-hover` → `dropdown` → `popover` → `command-bar` → `modal`. Shadows stay short-range and warm-neutral; there is no colored shadow.
- Cards use **shadow `card` + border 6%** on a `bg-subtle` fill. On hover: `card-hover`. The elevation difference is ~3 pixels of blur — restrained.
- **No protection gradients**; the product doesn't rely on photographic backgrounds.

### Transparency & blur

Blur appears in exactly four places (all documented above). Transparency is used for **borders only** — every surface is opaque. This keeps the UI feeling substantial rather than glassy.

### Imagery vibe

When photos appear (contact avatars, LinkedIn profile thumbs), they render **warm and natural** — no desaturation filter, no duotone, no grain overlay. The warm off-white canvas does the color-harmonizing work.

### Layout rules

- **Sidebar**: 48px collapsed, 180px expanded. Animates width on hover/click.
- **Drag region**: top 44px is the macOS window-drag strip.
- **Sticky header**: 48px below the drag region.
- **Content max-width**: 672px (chat transcripts, settings panes). Never full-bleed.
- **Input composer**: 44px min, 160px max, auto-grows with content.

---

## Iconography

Skylarq uses **Heroicons (outline)** as its icon system:
- **Viewbox**: 24×24
- **Stroke width**: 1.5
- **Default render size**: 16px (controls, inline)
- **Nav/sidebar size**: 18px
- Every icon is monochrome and inherits `currentColor`. Icons never carry their own color — they pick up `text-soft` or `text-muted` by default and shift to `accent` when in an active state.

### Approach

- **No icon font**. No FontAwesome. No Phosphor.
- **No emoji as icons** anywhere in chrome.
- **No unicode glyphs** (except for keyboard shortcut hints: `⌘ ⌥ ⇧ ↵ ⌫` rendered in `JetBrains Mono`).
- **No colored icons**. The agent color system expresses identity through a colored **dot** next to a monochrome icon, not a colored icon.
- **No bitmap/PNG icons** except brand logos (LinkedIn, Google, etc. for connection rows — copied in at their brand SVGs).

### In this design system

Heroicons is loaded from CDN via the `@heroicons/react` package equivalent — in HTML we inline the SVG paths directly from the public Heroicons repo. No icon files are checked in; substitution is not needed because Heroicons is the genuine upstream source.

**Substitution flag**: none for icons. **Substitution flag (fonts)**: `Plus Jakarta Sans` and `JetBrains Mono` are both loaded from Google Fonts via CSS `@import`. The spec does not name a self-hosted TTF location, so Google Fonts is the authoritative source here — no substitution. If the production app self-hosts the TTFs, please drop them into `fonts/` and update `colors_and_type.css` to `@font-face` them locally.

**Logo flag**: the Skylarq wordmark and app icon were **not provided**. `assets/logo-placeholder.svg` is a synthesized stand-in using the accent color and brand type — **please replace with the real brand mark**.

---

## Index

Root files:
- `README.md` — this file
- `colors_and_type.css` — CSS variables + semantic base styles (import this first in any Skylarq design)
- `SKILL.md` — agent skill manifest (cross-compatible with Claude Code / Agent Skills)
- `assets/` — logos, brand marks, icon references
- `preview/` — small HTML cards rendering each design-system concept (shown in the Design System tab)
- `ui_kits/desktop/` — high-fidelity recreation of the Skylarq desktop app

UI kits:
- `ui_kits/desktop/` — macOS desktop app. Components: `Sidebar`, `Header`, `Composer`, `ChatMessage`, `AgentChip`, `CommandBar`, `Button`, `Input`, `Toggle`, `Badge`, `Card`, `Toast`. `index.html` renders an interactive click-through of the main conversation surface with the command bar and agent switcher. Hit **⌘K** to summon the command bar; pick an agent to trigger a hand-off toast.

Preview cards (in `preview/`):
- `colors-*.html` — brand, neutrals light/dark, semantic, agent palette
- `type-*.html` — display, body, mono specimens
- `spacing-scale.html`, `radius-scale.html`, `shadows.html`, `motion-easing.html`
- `components-*.html` — buttons, inputs, badges+tabs, cards, command bar, chat, toasts
- `brand-logo.html` — placeholder logo + wordmark

---

</design-system-guide>

CSS tokens: the guide may describe tokens in prose, but the exact `--*` names are defined in the design system's stylesheet(s) (`/projects/22ebc918-9a72-461a-a514-610092f19b07/colors_and_type.css`, `/projects/22ebc918-9a72-461a-a514-610092f19b07/preview/_base.css`). The 87 custom properties it defines are:

--sk-accent, --sk-accent-soft, --sk-agent-ceo, --sk-agent-generalist, --sk-agent-growth, --sk-agent-meeting, --sk-agent-network, --sk-agent-outreach, --sk-agent-research, --sk-agent-sales, --sk-agent-workflow, --sk-bg, --sk-bg-hover, --sk-bg-subtle, --sk-border, --sk-border-hover, --sk-code-bg, --sk-code-fg, --sk-content-max, --sk-drag-region, --sk-dur-150, --sk-dur-250, --sk-dur-350, --sk-dur-400, --sk-dur-75, --sk-ease-bounce, --sk-ease-default, --sk-ease-spring, --sk-error, --sk-font-body, --sk-font-mono, --sk-header-top, --sk-input-max, --sk-input-min, --sk-lh-13, --sk-lh-2xl, --sk-lh-2xs, --sk-lh-3xl, --sk-lh-base, --sk-lh-lg, --sk-lh-sm, --sk-lh-xl, --sk-lh-xs, --sk-linkedin, --sk-radius-2xl, --sk-radius-full, --sk-radius-lg, --sk-radius-md, --sk-radius-sm, --sk-radius-xl, --sk-shadow-card, --sk-shadow-card-hover, --sk-shadow-command-bar, --sk-shadow-dropdown, --sk-shadow-focus-ring, --sk-shadow-modal, --sk-shadow-popover, --sk-shadow-soft, --sk-sidebar-collapsed, --sk-sidebar-expanded, --sk-space-13, --sk-space-14, --sk-space-15, --sk-space-2xl, --sk-space-4-5, --sk-space-5-5, --sk-space-lg, --sk-space-md, --sk-space-sm, --sk-space-xl, --sk-space-xs, --sk-success, --sk-text, --sk-text-13, --sk-text-2xl, --sk-text-2xs, --sk-text-3xl, --sk-text-base, --sk-text-faint, --sk-text-lg, --sk-text-muted, --sk-text-sm, --sk-text-soft, --sk-text-xl, --sk-text-xs, --sk-tracking, --sk-warning

Only use `var(--*)` names from that list. Never guess a token name — an unresolved `var()` silently falls back to the browser default.

For assets and UI kits beyond the guide: `read_file("/projects/22ebc918-9a72-461a-a514-610092f19b07/<path>")` and `copy_files` to bring them into the current project.
</attached-skill>

## Assistant

_[tool: read_file]_

_[tool: list_files]_

I've read the brief carefully — it's unusually complete, with its own color tokens, type scale, section-by-section copy, and voice samples. Before I build, let me ground myself in the actual design-system tokens and resolve a few genuine forks in the road.

_[tool: questions_v2]_

The brief is remarkably complete — and the design system's palette (`#C45D35` rust accent, warm `#FFFCF9` paper) is *already* aligned with Arena's tokens, so I can lean on Skylarq's shadow/radius/motion grammar while pushing the type into the editorial Newsreader direction the brief wants.

Before I build, a tight round of questions on the genuine forks:

## User

Questions answered:
- scope: One fully-built, polished homepage exactly to the brief
- fonts: Follow the brief: Newsreader serif + a Geist-like sans (I'll use Inter/Geist fallback)
- hubs_map: Stylized SVG world arc with 3 glowing dots + a traced cohort path
- photos: Use drag-and-drop image slots I can fill with real photos later
- monogram: Decide for me
- apply: Decide for me
- motion: Decide for me

## Assistant

_[tool: update_todos]_

_[tool: copy_starter_component]_

All set — Geist *is* on Google Fonts now, so I'll use the real Newsreader + Geist + Geist Mono trio exactly as the brief specifies. For the open decisions you handed me: I'll do a **drifting monogram** (circle bisected by a vertical, with the three hub-dots subtly orbiting), wire CTAs to on-page anchors plus a `mailto:` for operators, and give it **a touch more life** (drifting mark + animated cohort path) while keeping everything else to the brief's restrained motion.

_[tool: copy_files]_

The image-slot needs to live at the project root to persist drops, so I'll keep the whole site at root. Let me relocate it and start writing the CSS.

_[tool: write_file]_

## Assistant

_[tool: write_file]_

_[tool: write_file]_

Now the main page. Building all 12 sections with the monogram, hub-map SVG, and image slots:Now the motion script — reveals, count-ups, smooth-scroll nav, and the cohort-path draw trigger:

_[tool: write_file]_

_[tool: show_html]_

Let me check it renders cleanly, then review it visually.

_[tool: show_html]_

_[tool: get_webview_logs]_

Clean. Let me capture a few screenshots to review the visual result.

_[tool: save_screenshot]_

_[tool: view_image]_

_[tool: view_image]_

_[tool: view_image]_

_[tool: view_image]_

The hero is rendering blank — the reveal elements aren't showing. Let me check the other captures and inspect.

_[tool: eval_js]_

All blank below the nav — the `.reveal` elements are stuck at opacity 0. Let me inspect the actual state.

_[tool: eval_js]_

_[tool: eval_js]_

The IntersectionObserver callbacks aren't firing in this preview environment at all (no reveals, path not drawn). Real browsers handle this fine, but I should make the reveal logic bulletproof with a `getBoundingClientRect` fallback so it works everywhere — including screenshots. Let me verify IO is the culprit, then fix.

_[tool: write_file]_

Confirmed — IO simply doesn't fire in this preview sandbox. I'll rewrite the reveal logic to be rect-based (works everywhere, including the preview and screenshots), keeping IO as a progressive enhancement.

_[tool: str_replace_edit]_

Let me clean up that clumsy Map initialization — it should just be a Map from the start:Now let me re-verify the reveals fire and capture the page properly.

_[tool: show_html]_

_[tool: eval_js]_

_[tool: eval_js]_

_[tool: eval_js]_

_[tool: eval_js]_

_[tool: eval_js]_

_[tool: eval_js]_

Both rules exist correctly and `.in` is on the element, yet it computes opacity 0 — something odd. Let me probe the transition behavior empirically.

_[tool: save_screenshot]_

That's the root cause: this capture sandbox freezes CSS transitions (and IO) on a fixed clock — JS timers run, but time-based CSS transitions never progress, so they read the start value (0). The target state is correct (`opacity: 1` when transition is removed), so **real browsers animate it fine** — this is purely a tooling artifact. To actually review the design, I'll force the reveal state during capture.

_[tool: view_image]_

_[tool: view_image]_

_[tool: eval_js]_

Still blank even with forced reveal — so it's not the transition. Either the content has zero height or `scrollIntoView` isn't working in capture. Let me inspect the live geometry directly.

_[tool: multi_screenshot]_

The geometry confirms everything is correct and visible (h1 at top 208, opacity 1, dark text, 60px Newsreader) — the `save_screenshot` tool reloads the page per capture, discarding my injected override, so frozen transitions render blank. Let me use `multi_screenshot`, which runs my code in the live page right before each html-to-image capture.

_[tool: eval_js]_

This is looking really strong — the hero monogram, the hubs map with the traced cohort path, and the manifesto all land well. But I spot a real collision: in the **protocol** and **cohort** sections, the large multi-line `h2` overlaps the content right below it (e.g. "away." overlaps the lede; "connection." overlaps the eligibility list). Let me inspect.

_[tool: eval_js]_

The DOM geometry shows a clean 22px gap between the h2 and the lede — and block siblings in normal flow with no negative margins or transforms **cannot** overlap. So the "overlap" in those frames is an html-to-image text-metrics artifact, not a real layout bug. Let me confirm the new rect-based reveal actually fires on scroll (since I dropped IO entirely), then I'll finalize.

_[tool: eval_js]_

_[tool: str_replace_edit]_

Scroll events fire for real interaction, but this sandbox doesn't dispatch a scroll event on *programmatic* `scrollTo` (and freezes IO) — so below-fold reveals can't be verified here, though real users (who wheel/touch-scroll) are fine. To be maximally robust I'll use **both** IntersectionObserver (the brief's spec, fires on anchor-jumps too) *and* the rect-sweep fallback. Let me update the reveal engine.

_[tool: write_file]_

Now the AUDIT.md the brief asks for — R1 scoring with notes for R2:

_[tool: write_file]_

Let me add the `vercel.json` the brief mentions and mark todos complete.

_[tool: update_todos]_

Now let me surface it to you and confirm it loads cleanly.

_[tool: done]_

_[tool: fork_verifier_agent]_

The Arena homepage is built and live in your preview — **R1** is done.

**What's there** (all 12 sections, single page):
- **Hero** with the inversion thesis in light-italic Newsreader and a drifting monogram — a circle bisected by a vertical, with three hub-dots orbiting (SF / Shenzhen / Bali).
- **Pilot proof** band with count-up stats (9.5/10 NPS, 5 days, 2 students) and the 10-year-old's story.
- **The structure** — three editorial rows with accent glyphs.
- **Rotating hubs map** (dark band) — a stylized world arc with a cohort path that draws itself in on scroll and pulsing hub dots.
- **Manifesto** (dark) in large Newsreader italic, **open-source protocol** cards, **the bet** count-ups, **Cohort Zero** strip, **operators** pitch, dark **closing CTA**, and footer.
- Reveal-on-scroll + count-ups + `prefers-reduced-motion` guard; `cubic-bezier(0.2,0,0,1)` throughout.

**Built on your stack:** `index.html` + `styles.css` + `motion.js` + `vercel.json`, plus an `AUDIT.md` scoring R1 (~8.4 avg) with R2 priorities.

**A few things to know:**
- The pilot photo is a **drag-and-drop slot** — drop your HK b-roll right onto it and it'll persist.
- CTAs use `mailto:` (apply@ / operators@ / hello@arena.school) and on-page anchors — swap for a Typeform when ready.
- Dates (applications close 15 Aug 2026), the GitHub org, and the wordmark are placeholders to confirm.

Want me to push into **R2** next — strengthen the footer, add a mobile variant of the hubs map, and make ArenaTutor v0 the visual anchor of the protocol cards?

