# Arena School — arenaschool.org

Bilingual (EN/中文) site for Arena School: AI-native programs for students, early career, and educators.

## How editing works
1. Edit any `.html` file (on github.com: open the file → pencil icon → commit).
2. Committing to `main` auto-deploys to **arenaschool.org** within ~1 minute (Vercel).
3. Check the live page after a minute. Hard-refresh (Cmd+Shift+R) if it looks stale.

## Page map
Nav: Programs ▾ · Case studies ▾ · Curriculum · About · EN/中文 toggle · Contact us button. Shared nav and footer markup lives in every page; keep them identical across pages.

| Page | File | 中文版 |
|---|---|---|
| Homepage (hero, testimonials, founding team, programs, proof, contact) | `index.html` | `index-cn.html` |
| About (co-founder bios, why builders, agency · taste · craft) | `about.html` | `about-cn.html` |
| Contact form | `contact.html` | `contact-cn.html` |
| For schools (links to the four case-study categories) | `schools.html` | `schools-cn.html` |
| Case studies · Student programs | `case-studies/student-programs.html` | `case-studies/student-programs-cn.html` |
| Case studies · Skill workshops (portfolio) | `case-studies/skill-workshops.html` | `case-studies/skill-workshops-cn.html` |
| Case studies · Parent talks | `case-studies/parent-talks.html` | `case-studies/parent-talks-cn.html` |
| Case studies · Teacher training (was `/teachers`) | `case-studies/teacher-training.html` | `case-studies/teacher-training-cn.html` |
| Case study deep dives · Hong Kong, Beijing | `case-study-hong-kong.html`, `case-study-beijing.html` | `-cn` versions |
| School-Year Mentorship · enrollment · payment | `mentorship.html`, `enroll.html`, `pay-mentorship.html` | `-cn` versions (payment is bilingual) |
| AI Advantage Bootcamp (Guangzhou) | `zero-to-launch.html` | `zero-to-launch-cn.html` |
| Curriculum & philosophy | `curriculum.html` | `curriculum-cn.html` |
| Footer only: partnerships, speaking menu | `partnerships.html`, `speaking.html` | `-cn` versions |

Pages under `case-studies/` must use absolute paths (`/styles.css`, `/photos/...`). Old URLs such as `/teachers` and `/case-studies` redirect in `vercel.json`.

Testimonials: the homepage and the Student programs page each contain a hidden testimonials section. Fill in the quotes and delete the `hidden` attribute. Never name minors; attribute by role, grade, city and year.

Shared: `styles.css` (all styling), `motion.js` (animations), `photos/`, `logos/`, `fonts/` (self-hosted — do not replace with Google Fonts links; they are blocked in mainland China).

## Brand assets
- The Arena seal and wordmark live in `logos/arena/` (source: the September 2026 brand package; master files are in the Drive folder `04 Marketing, Brand & Media`).
- Use `seal-navy-*.png` on paper backgrounds and `seal-ivory-*.png` on dark bands (footer, manifesto). Nav uses 256, footer 256, manifesto 512, homepage hero 1024.
- Favicons, app icons (`icons/`), `favicon.ico`, `favicon.svg` and `og-image.png` are all generated from the same seal. Keep them in sync if the seal changes.
- Partner and credential logos stay in `logos/` (`orgs/`, `tools/`, `lux/`, institution SVGs).

## House rules (please keep)
- **Edit EN and CN together** — every content change should land in both versions of a page.
- **No em dashes** anywhere, English or Chinese. Use commas, colons, or 、·。
- **ISB's Chinese name is 北京顺义国际学校** (never 北京国际学校 or 北京京西学校).
- **Never state the Beijing cohort's student count.** Say "every team shipped, grades 7 to 12." Hong Kong's "20 students" is fine.
- No student names or product names on public pages (minors). Judges/mentors by institution only (Harvard, YC, ...), not personal names.
- Fee/date facts: mentorship = ¥20,000 for six months (Oct–Mar), weekly hybrid check-ins; Guangzhou camp = Dec 27–Jan 2.
- Winter camp partner (Lux Scholar) appears ONLY on the zero-to-launch pages.

## Forms & payments
- Contact (homepage and `/contact`) and enrollment forms submit via formsubmit.co → phillipan14@gmail.com. Do not change form field `name=` attributes.
- **One email list.** Every form that asks for an email also adds it to the Arena Notes newsletter (Resend segment "Arena Notes"): POST `/api/subscribe` with `{ email, role, lang, source, page, quiet: true }` (`quiet` skips the welcome email and Slack ping). `onepager.js` (all `.pp-lead-form` forms), `motion.js` (`#partnerForm`), and the enroll pages already do this. Any new form with an email field must do the same and show the notice under its button: "We’ll also send you Arena Notes, our occasional newsletter. No spam, and you can unsubscribe anytime." / "我们也会为您订阅 Arena 通讯。绝无垃圾邮件，可随时退订。" Never promise "no newsletter".
- `pay-mentorship.html` holds the WeChat Pay QR (`pay/wechat-qr.png`).

## Deploys
Auto: any push to `main`. Manual (if needed): `vercel deploy --prod --yes` from repo root.
