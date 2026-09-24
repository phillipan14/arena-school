# Arena School — arenaschool.org

Bilingual (EN/中文) site for Arena School: AI-native programs for students, early career, and educators.

## How editing works
1. Edit any `.html` file (on github.com: open the file → pencil icon → commit).
2. Committing to `main` auto-deploys to **arenaschool.org** within ~1 minute (Vercel).
3. Check the live page after a minute. Hard-refresh (Cmd+Shift+R) if it looks stale.

## Page map
| Page | File | 中文版 |
|---|---|---|
| Homepage | `index.html` | `index-cn.html` |
| For schools | `schools.html` | `schools-cn.html` |
| AI training for teachers | `teachers.html` | `teachers-cn.html` |
| Speaking & workshops | `speaking.html` | `speaking-cn.html` |
| Mentorship program | `mentorship.html` | `mentorship-cn.html` |
| Enrollment form | `enroll.html` | `enroll-cn.html` |
| Payment (WeChat QR) | `pay-mentorship.html` | (bilingual, single page) |
| Guangzhou bootcamp | `zero-to-launch.html` | `zero-to-launch-cn.html` |
| Case study · Hong Kong | `case-study-hong-kong.html` | `case-study-hong-kong-cn.html` |
| Case study · Beijing | `case-study-beijing.html` | `case-study-beijing-cn.html` |
| Curriculum & philosophy | `curriculum.html` | `curriculum-cn.html` |
| Partnerships (operators) | `partnerships.html` | `partnerships-cn.html` |

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
- Contact + enrollment forms submit via formsubmit.co → phillipan14@gmail.com. Do not change form field `name=` attributes.
- `pay-mentorship.html` holds the WeChat Pay QR (`pay/wechat-qr.png`).

## Deploys
Auto: any push to `main`. Manual (if needed): `vercel deploy --prod --yes` from repo root.
