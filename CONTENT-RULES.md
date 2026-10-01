# Arena website content rules

Every page, every new program, every edit. `python3 tools/content_lint.py` enforces the rules it can measure. A page that fails the lint does not ship.

## 1. What the website is for
A visitor should, in under a minute:
1. understand what Arena does and why it matters now;
2. find the one offer meant for them;
3. contact us.

Anything that doesn't serve those three jobs belongs in the **meeting kit** (one-pagers, PDFs and decks we send or show in meetings), not on the site.

| On the website | In the meeting kit (never on the site) |
|---|---|
| The promise, and who it's for | Hour-by-hour schedules; day-by-day detail beyond one line per day |
| How it works, as one compact visual | Full curriculum and principle essays (archived in Drive 02) |
| One proof line plus a link to Results | Sample builds per industry or per role |
| Format, length, where, price in one line | Staffing ratios, logistics minutiae, materials lists |
| Up to 6 FAQs, in an accordion | Long FAQs, policies, edge cases |
| One call to action | Case narratives told a second time |

## 2. The section admission test
A section earns a place only if it passes all four questions:
1. **Decision:** does it help this page's reader decide or act? If not, cut it.
2. **Unique:** is it said anywhere else on the site? If yes, keep it in its **canonical home** (section 6) and link there.
3. **Specific:** does it contain a fact, a number or a concrete example? Pure framing ("Here's why this matters…") is cut.
4. **Compact:** can it be one visual, a 3-up row or one sentence? If yes, it must be.

## 3. Page budgets (lint-enforced)

"Words" means visible words, excluding the nav, footer and hover details.

| Page type | Max words | Max sections |
|---|---|---|
| Homepage | 600 | 7 |
| Program page (Mentorship, Bootcamp, the four student programs, any new program) | 700 | 7 |
| How-we-work page (Student programs, Portfolio workshop, Community dialogues, Teacher training) | 550 | 6 |
| How-we-work hub (Schools) | 500 | 6 |
| Approach | 650 | 5 |
| About | 650 | 5 |
| Results | 750 | 6 |
| Partners | 450 | 5 |
| Contact | 100 | 2 |

**Per-block limits:**
- hero lede: 30 words
- section intro: 25 words
- card body: 25 words
- hover detail: 30 words
- FAQ answer: 45 words

## 4. Layout rules: save vertical space
- **Horizontal first:** any sequence or set of 3 or more items (days, steps, phases, milestones, pillars, audiences, tools, formats) is a horizontal track or a 3-up/4-up row, never a vertical list. On phones it becomes a swipeable row.
- **One schedule per program:** one horizontal track, with details in the hover/tap panel. Never a day-by-day list *and* a week overview.
- **Depth on demand:** anything a visitor might want but most don't goes behind a hover panel, an accordion or a link, never on the scroll.
- **Line length:** text boxes are wide enough that a subtitle's last line has 5 or more words. If a short last line is left dangling and there's room, widen the box (lede max about 64ch) before adding lines. `text-wrap: pretty` is on everywhere.
- **Visual order on each page:**
  1. hero (inverted riso)
  2. promise (3-up)
  3. how it works (track)
  4. proof (one line + link)
  5. logistics/FAQ (accordion)
  6. CTA

  Skip any step that the page doesn't need.
- **No decorative sections.** Photo bands, pull quotes and restated headings don't count as content.

## 5. Voice (see TONE-BRIEF.md)
- **Stance:** we work alongside educators. Never "unlike school" or "school never".
- **Writing:** plain, specific, American English. **Always use the Oxford comma** ("students, families, and educators"). No em dashes, no slogans, no "Not X. Not Y.".
- **The core message is used identically everywhere.**
  - Core idea: "When AI can make almost anything, students need to know what's worth making, whether it's good, and how to finish it."
  - Pillars: **Agency** (choosing what's worth solving), **Taste** (telling which version actually works), **Craft** (finishing it well).
  - CN pillars (identical everywhere): **主动性**（选出真正值得解决的问题。）、**审美**（分辨哪个版本真正行得通。）与 **匠心**（把事情做完，并且做好。）. Names in a sentence: 主动性、审美与匠心. Never 自主判断力 / 审美判断力 / 完成力.
  - Never add "creativity", "courage" or "judgment" as extra headline skills.
- **The team:** "our team", "the Arena team", and "co-founders" for Jing Jing Yang and Phillip An (list Jing Jing first). Never imply a two-person company (no "our two co-founders run Arena"). CN 我们的团队、联合创始人. Never "builders" (CN 创造者、建造者、动手派、做产品的人), "practitioners who build/ship", "we build with AI every day" or startup/hustle vocabulary about the founders or the company. Arena is a warm partner to schools, parents, families and administrators.
- **Students making things:** students may build and make; that is the program. Don't stack several "build" words in one line, don't label students "builders", and use "launch" or "publish" rather than "ship" slang.
- **Terminology:** "How we work" / 工作方式 · "Community dialogues" / 社区对话 · "Portfolio workshop" · "AI Advantage Bootcamp".
- **Chinese:** every edit is made to the EN and CN pages together.

## 5a. How we frame AI (applies to every example, card, hover and FAQ)
AI **aids** people. It never does the work *for* them. People stay the authors and the decision-makers.

- **Frame AI as:** a thinking partner, a tool, a way to try more ideas, test sooner, reach more students, or get feedback faster.
- **The human verbs belong to people:** students and teachers decide, judge, choose, build, finish and own the result.
- **Never frame AI as:** replacing, erasing or taking over someone's work. No "instead of writing", "you just review", "AI does X for you", "hours of work in minutes", "type less", "never mark again".
- **Teachers' professional work** (feedback, marking, planning, report writing) is never described as automated. Say how AI helps teachers do it their way, with the teacher's judgment in charge.
- **Students' learning** is never shortcut. AI speeds up trying and testing; students still learn the skill and make the calls. Prefer "students use AI coding tools to build…" over "AI builds it while you watch".
- **Time claims:** only real, observed ones, never a promise of time saved. Frame benefits as outcomes: better materials, more time with students, work that fits their class.
- **Balanced, never alarmist:** no fear-based framing ("AI will replace you", "the job market is collapsing").
- **Formats for flexible offers** (teacher training, community dialogues) are described by outcome and audience, not length. Length is agreed with each school.
- **Never compare Arena with schools:** No lines comparing Arena with schools or implying schools are behind; frame as things families can do alongside school. (No "faster than schools can update a syllabus", no "the rules for school were written before AI".)
- **Approved rewrites (Oct 2026), reuse these instead of the old lines:**
  - "AI tools can generate a working app in minutes." → "With AI as a helper, students can get a first working version of an app running quickly." (CN 有了AI的帮助，学生可以很快做出能运行的第一版应用。)
  - "Anyone can generate a product now." → "With AI's help, more people than ever can build a product." (CN 有了AI的帮助，能做出产品的人比以往都多。)
  - "Anyone can now write a polished essay." → "With AI's help, polished essays are now common." (CN 有了AI的帮助，文笔流畅的文书如今随处可见，)
  - "Polished words, which AI can now produce for anyone." → "Polished words, which AI now helps anyone produce." (CN 打磨过的文字，如今AI能帮任何人写出来。)
  - "AI can build a first version of almost anything." → "With AI, a first version of almost anything comes together faster." (CN 有了AI，几乎什么都能更快做出第一版。)
  - "When AI can complete an assignment" → "When AI can help finish an assignment" (CN 当AI能帮学生完成作业)
  - Phillip's quote "AI is rewriting jobs faster than schools can update a syllabus…" → "AI is changing work quickly. The habits students build now, in class and at home, are what carry over." (CN AI正在快速改变工作。孩子们现在养成的习惯，无论在课堂还是在家里，都会一直陪着他们。)
  - "The rules for school, jobs, and careers were written before AI." → "Much of how we prepare young people for work took shape before AI." (CN 很多帮年轻人走向职场的做法，都是在AI出现之前形成的。)
  - "The assumptions that shaped school and careers no longer hold." → "AI is changing what careers ask of young people." (CN AI正在改变职场对年轻人的要求。)

## 6. Canonical homes (each fact lives once)

| Fact | Lives on | Everywhere else |
|---|---|---|
| Hong Kong 2025, Beijing 2026 and Tsinghua staff training stories, numbers, quotes | **Results** | One line plus a link |
| Founder bios | **About** | Name plus "Read bio →" |
| Agency / taste / craft (why and how) | **Approach** (full) · **Home** (short) | Pillar names only |
| The daily structure of a program | Its own program page (one track) | Not repeated |
| Mentorship facts: 6 months to a year of personalized 1:1 mentorship, rolling start · weekly hybrid check-ins (fee is NOT published; only on the unlinked payment page) | **Mentorship** | Not repeated |
| Bootcamp facts: Guangzhou · Dec 27, 2026 to Jan 2, 2027 · with Lux Scholar | **Bootcamp** | Not repeated (Lux Scholar only appears on bootcamp pages) |

## 7. Claims policy
- Only claims on the **verified list** (`CLAIMS.md`, status "confirmed") may appear.
- Unconfirmed claims stay as currently worded (no strengthening) until a founder confirms them, then they are updated in one place.
- Never state the Beijing cohort student count. No student or product names. Judges are named by institution only.
- Never mention unannounced sessions or events publicly.

## 8. Adding a new program (checklist)
1. Copy the program page template (the Bootcamp page structure):
   1. hero
   2. who it's for + what you leave with (3-up)
   3. how it runs (one track)
   4. tools (one strip, if relevant)
   5. proof (one line)
   6. logistics + FAQ (accordion, up to 6)
   7. CTA
2. Write EN and CN together, inside the budgets.
3. Put the extra detail (schedule by hour, sample builds, staffing) in the meeting kit, in `arena-school-tools/meeting-kit/`.
4. Add a one-line card to the Programs menu and the homepage program row. Don't write a new section anywhere else.
5. After the cohort runs, add it to **Results**, not to the program page.
6. Run `python3 tools/content_lint.py` until it passes.


## 9. Proof and program names (Oct 2026)
- Never use "6 of 6" or "100% launched" as proof. Use: 9.5/10 NPS (Hong Kong, 20 students), a ten-year-old launched a sign-language-to-speech app in five days (Hong Kong), judges from Harvard, Stanford, Y Combinator, and AI labs, Tsinghua Schwarzman College staff training.
- No prize or seed-money amounts anywhere (founder, Oct 2026): do not mention US$1,980, ¥8,888, 种子资金/种子基金, or 奖金.
- Framing (founder, Oct 2026): never call Arena "AI programs", "AI courses", or an "AI camp". Arena runs programs that help people thrive in the age of AI. The audience is the whole school community: students, families, educators, and schools.
- Results are selected examples, not a complete list.
- No tuition or fee amounts on marketing pages.
- Program names: App Design Workshop, College Portfolio Workshop, Entrepreneurship & AI Intensive, Year-Long Project Mentorship, AI Advantage Bootcamp, AI for Educators, Community dialogues (parent education series).

## 10. Chinese style (Oct 2026, JJ: "write how a Chinese parent or educator would actually say it")
- **No grade numbers in prose, menus, cards, or labels.** Say 初中生 (grades 6 to 9), 高中生 (grades 10 to 12), 初高中学生 (grades 7 to 12), 大学生与职场新人. Where one specific year matters, use the Chinese school-year name (高一, 高二, 高三, 准高三学生), never 10年级 / 11年级. Hero fact key is 对象, not 年级. "Tell us the grades" becomes 告诉我们学生年龄段. Numbers stay only where they are literal data: the 6 to 12 tick marks on the homepage grade map axis and the free-text 年级与学校 field on the enroll form.
- **Tagline (site footer, meta, one-pager):** 陪伴学生、家庭、教育者与学校，从容走进AI时代。 Homepage hero: 陪伴[学生/家庭/教育者/学校]，从容走进AI时代。 Never 茁壮成长, 赋能, 在……的时代里, stacked 我们相信.
- **Spacing:** no space between Chinese and "AI" or digits (AI时代, 用AI做出, 2026年, 25分钟, 30岁以下), matching the program names 创业与AI集训营, AI职场先发营, 教育者AI培训. Brand and proper names in Latin script keep a space (Arena 领导团队, Kimi 团队, Y Combinator 投资).
- **Punctuation:** full-width Chinese punctuation (，。：；？！（）“”). Quotes use “ ” not ‘ ’. Date ranges use 至 in prose (2026年12月27日至2027年1月2日). No em dashes.
- **Menu groups:** 短期课程 · 两天 (two workshops), 五天项目 (创业与AI集训营), 长期项目 (学年项目导师计划), 大学与职场 (AI职场先发营).
- **Write it the way it is said, not translated:** no English list order, no noun piles (日常习惯，个人系统), no calques such as "学习真正发生的地方", "自会说话", "被托付更大的决定", "值得存在". Read every CN line aloud; if a parent at a school coffee morning would not say it, rewrite it.

## 11. Confirmed facts (founder-confirmed)
- 9.5/10 NPS (Hong Kong 2025, 20 students): confirmed real by JJ, 2026-10-01.
- Mentorship length: "6 months to a year, rolling start" (CN 六个月到一年，滚动入学/随时可以开始) is correct as on the site. Confirmed 2026-10-01.
- EARCOS: Mar 17 to 20, 2027, Bangkok. Confirmed.
- The bootcamp page (zero-to-launch) is noindex on purpose.
- "Enrollment opens in October" (CN 十月开放报名) is correct.
- College admissions may be discussed in Community dialogues generally, but are avoided in the ISB parent talk (Oct 14, 2026).
- Co-founder quotes ("In her words" / "In his words") are final, approved by JJ 2026-10-01; the placeholder comments were removed.

