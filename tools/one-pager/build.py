"""One-page PDF "What is Arena School", EN + CN (FLUENCY-BRIEF 2 and its UPDATE, Oct 17, 2026).

Replaces the existing one-pager IN PLACE: onepager/arena-school-one-pager-{en,cn}.pdf and the .jpg thumbnails, so every
link and the gated download in onepager.js keep working. The old source (riso-v2/site-preview/_kit/onepager.html) is not
in this repo; this generator is now the source. What changed vs the old version: ONEPAGER-CHANGES.md.

Copy comes from the site's own sources (no new claims): the case cards (tools/depth_pages.py), the student data
commitments (tools/data_section.py), the fluency levels (tools/fluency_section.py), the approach copy and framework wheel
(tools/approach_page.py, tools/approach_wheel.py), and the nav and footer partials for program names. No stats, no ISB
numbers, no em dashes. CN copy is marked for JJ review in the HTML.

  python3 tools/one-pager/build.py          write tools/one-pager/onepager-{en,cn}.html, render the PDFs (Chrome
                                            headless, A4, exactly one page or it fails), and the 520px .jpg thumbnails
Needs the local server on 127.0.0.1:8931 (absolute /fonts, /logos and /photos paths).
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import approach_page as A  # noqa: E402
import approach_wheel as W  # noqa: E402
import data_section as DS  # noqa: E402
import depth_pages as P  # noqa: E402
import fluency_section as FL  # noqa: E402

E = dict(
    lang='en', eyebrow='What is Arena School',
    h1='Hands-on programs that help students, families, educators, and schools <em>thrive in the age of AI.</em>',
    lede=A.T['en']['a_lede'] + ' Every program builds three skills: <b>agency</b>, choosing what is worth solving; <b>taste</b>, telling which version actually works; and <b>craft</b>, finishing it well.',
    cap='Presenting at demo day, Beijing 2026',
    member='A member of', anth='Startup Program', oai='Partner Network', studied='Our team studied at', worked='Worked at',
    pk='Programs',
    cols=[('For students', [('App Design Workshop', 'Grades 6 to 9 · 2 days'), ('College Portfolio Workshop', 'Grades 10 to 12 · 2 days'),
                            ('Entrepreneurship &amp; AI Intensive', 'Grades 7 to 12 · 5 days'), ('Year-Long Project Mentorship', 'Grades 7 to 12 · 6 months to a year, 1:1')]),
          ('For teachers and schools', [('AI for Educators', 'Teachers make the tool their class is missing'), ('Technology teams', 'Training inside your school’s rules'),
                                        ('School leaders', 'Arena for your whole school community'), ('Conferences', 'Talks and hands-on workshops')]),
          ('For families', [('Year-Long Project Mentorship', 'Families enroll directly'), ('Community Dialogues', 'Parent talks at your school'),
                            ('AI Fundamentals for Students @ International School of Beijing', 'Winter break, Jan 5 to 8, 2027')]),
          ('College and early career', [('AI Advantage Bootcamp', 'Seven days in Guangzhou, Dec 27, 2026 to Jan 2, 2027')])],
    ak='Learning approach', ah=A.T['en']['l_h1'],
    ap='One framework runs every program. The learner sits at the center; four strands of work circle them: ' + ', '.join(d.lower() for d in A.T['en']['domains'][:3]) + ', and ' + A.T['en']['domains'][3].lower() + '.',
    fk='AI fluency for the whole staff', fh='A few early adopters are there. We bring everyone else up.',
    fp='A baseline places every teacher on five levels; we train each group up one level and re-measure each term.',
    dk='Student data comes first', dh='Before which tool, ask: whose account is it?',
    rk='Selected programs we have run', cases=[P.ISB_EN, P.BODLEY_EN, P.SCHWARZMAN_EN],
    ck='Bring Arena to your school.', cp='Programs for schools run on your campus, planned with your team around your calendar. Your teachers keep the materials.',
    mail='phillip@arenaschool.org', web='arenaschool.org',
)
Z = dict(
    lang='zh-CN', eyebrow='认识 Arena School',
    h1='动手实践的项目，陪伴学生、家庭、教育者与学校，<em>从容走进AI时代。</em>',
    lede=A.T['cn']['a_lede'] + '每个项目都培养三种能力：<b>主动性</b>，选出值得解决的问题；<b>审美</b>，判断哪个版本真正好用；<b>匠心</b>，把它做好做完。',
    cap='路演日展示，北京，2026年',
    member='成员计划', anth='初创企业计划', oai='合作伙伴网络', studied='团队成员曾就读于', worked='曾任职于',
    pk='项目',
    cols=[('学生项目', [('应用设计工作坊', '初中生 · 两天'), ('升学作品集工作坊', '高中生 · 两天'), ('创业与AI集训营', '初高中学生 · 五天'), ('学年项目导师计划', '初高中学生 · 六个月到一年，一对一')]),
          ('教师与学校', [('教育者AI培训', '为课堂做一个正缺的小工具'), ('技术团队', '在学校规则之内开展培训'), ('校长与管理层', '把 Arena 带进贵校，服务整个学校社群'), ('会议与活动', '主题演讲与动手工作坊')]),
          ('家庭', [('学年项目导师计划', '一对一指导，家庭可直接报名'), ('家长讲座', '社区对话：请学校邀请我们来讲'), ('学生AI基础营 · 北京顺义国际学校', '寒假，2027年1月5日至8日')]),
          ('大学与职场', [('AI职场先发营', '广州，七天，2026年12月27日至2027年1月2日')])],
    ak='学习方法', ah=A.T['cn']['l_h1'],
    ap='一套框架贯穿每个项目。学习者在中心，四条学习主线围绕着他们：' + '、'.join(A.T['cn']['domains']) + '。',
    fk='全体教职员工的AI素养', fh='少数老师已经走在前面，我们带上其他所有人。',
    fp='通过基线评估确定每位老师在五个层级中的位置；帮助每组老师提升一级，并每学期重新评估。',
    dk='学生数据放在第一位', dh='先别问用哪个工具，先问是谁的账号。',
    rk='我们开展过的项目', cases=[P.ISB_CN, P.BODLEY_CN, P.SCHWARZMAN_CN],
    ck='把 Arena 带进贵校。', cp='面向学校的项目在贵校校园进行，按贵校校历与团队共同规划。老师们可以保留全部材料。',
    mail='phillip@arenaschool.org', web='arenaschool.org',
)
STUDIED = ['caltech', 'harvard', 'brown', 'tsinghua-lockup', 'isb']
WORKED = ['mckinsey', 'goldman', 'yc', 'apple', 'microsoft-ai', 'deloitte', 'kimi-wordmark']
LOGO_H = {'caltech': 3.4, 'harvard': 4.2, 'brown': 4.4, 'tsinghua-lockup': 5.0, 'isb': 5.2, 'mckinsey': 2.7, 'goldman': 4.2, 'yc': 4.0, 'apple': 4.2,
          'microsoft-ai': 3.4, 'deloitte': 2.8, 'kimi-wordmark': 2.9}   # mm, optical balance as in tools/cred_css.py


def tokens():
    css = open(os.path.join(ROOT, 'css', 'pro.css'), encoding='utf-8').read()
    return re.search(r'(?s):root\s*\{.*?\n\}', css).group(0)


def wheel_css():
    css = open(os.path.join(ROOT, 'css', 'approach.css'), encoding='utf-8').read()
    return '\n'.join(l for l in css.splitlines() if l.startswith('.apw'))


def logos(keys, alt):
    return ''.join('<img src="/logos/cred/%s.png" alt="" style="height:%smm" />' % (k, LOGO_H[k]) for k in keys)


def page(t, lang):
    cn = lang == 'cn'
    d = DS.C['cn' if cn else 'en']
    f = FL.C['cn' if cn else 'en']
    cols = ''.join('<div class="col"><h3>%s</h3><ul>%s</ul></div>' % (h, ''.join('<li><b>%s</b><span>%s</span></li>' % x for x in items)) for h, items in t['cols'])
    commits = ''.join('<li><b>%s.</b> %s</li>' % (a.rstrip('.'), b) for _, a, b in d['commit'][:4]) if not cn else ''.join('<li><b>%s。</b>%s</li>' % (a, b) for _, a, b in d['commit'][:4])
    stairs = ''.join('<li style="--s:%d"><i>%d</i><b>%s</b></li>' % (i, i + 1, n) for i, (n, _) in enumerate(f['levels']))
    cases = ''.join('<div class="case"><span class="k">%s</span><b>%s</b><p>%s</p></div>' % (c['k'], c['h'], c['p']) for c in t['cases'])
    jj = '<!-- JJ review: one-pager CN copy (FLUENCY-BRIEF 2, Oct 17, 2026) -->\n' if cn else ''
    fonts = ('<link rel="stylesheet" href="/fonts/gf.css" />' + ('<link rel="stylesheet" href="/fonts/zh/zh.css?v=2" />' if cn else ''))
    serif = "'Newsreader', 'Arena Serif SC', 'Songti SC', 'Noto Serif SC', Georgia, serif" if cn else "'Newsreader', Georgia, serif"
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8" />\n<title>Arena School one-pager</title>\n%s\n%s<style>\n%s\n%s\n%s\n</style>\n</head>\n<body>\n'
            '<main class="op">\n'
            '<header class="top"><div class="top-copy"><div class="brand"><img src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" class="wm" /></div>'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p></div>'
            '<figure class="photo"><img src="/photos/isb-2026/pitch-duo-1600.webp" alt="" /><figcaption>%s</figcaption></figure></header>\n'
            '<section class="cred"><div class="member"><span class="lab">%s</span><span class="m"><img src="/logos/partners/anthropic.svg" alt="Anthropic" class="anth" /><em>%s</em></span>'
            '<span class="m"><img src="/logos/partners/openai.svg" alt="OpenAI" class="oai" /><em>%s</em></span></div>'
            '<div class="team"><div><span class="lab">%s</span><span class="lg">%s</span></div><div><span class="lab">%s</span><span class="lg">%s</span></div></div></section>\n'
            '<section class="progs"><span class="sk">%s</span><div class="cols">%s</div></section>\n'
            '<section class="three">'
            '<div class="p1"><span class="sk">%s</span><div class="wheel">%s</div><div><h2>%s</h2><p>%s</p></div></div>'
            '<div class="p2"><span class="sk">%s</span><h2>%s</h2><ol class="stairs">%s</ol><p>%s</p></div>'
            '<div class="p3"><span class="sk">%s</span><h2>%s</h2><ul class="commit">%s</ul></div></section>\n'
            '<section class="ran"><span class="sk">%s</span><div class="cases">%s</div></section>\n'
            '<footer class="cta"><div><h2>%s</h2><p>%s</p></div><div class="contact"><b>%s</b><span>%s</span></div></footer>\n'
            '</main>\n</body>\n</html>\n'
            % ('zh-CN' if cn else 'en', jj, fonts, tokens(), wheel_css(), CSS.replace('SERIF', serif),
               t['eyebrow'], t['h1'], t['lede'], t['cap'],
               t['member'], t['anth'], t['oai'], t['studied'], logos(STUDIED, t['studied']), t['worked'], logos(WORKED, t['worked']),
               t['pk'], cols,
               t['ak'], W.svg('cn' if cn else 'en'), t['ah'], t['ap'],
               t['fk'], t['fh'], stairs, t['fp'],
               t['dk'], t['dh'], commits,
               t['rk'], cases,
               t['ck'], t['cp'], t['mail'], t['web']))


CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Geist', 'PingFang SC', system-ui, sans-serif; color: #1E2740; font-size: 7.6pt; line-height: 1.42; }
.op { width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; }
.op > * { flex-shrink: 0; }
em { font-style: italic; }
.sk, .eyebrow, .lab, .k { font: 600 6.2pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: var(--pro-action); }
:lang(zh) .sk, :lang(zh) .eyebrow, :lang(zh) .lab, :lang(zh) .k { letter-spacing: .04em; font-size: 7pt; }
h1, h2, h3 { font-family: SERIF; font-weight: 500; color: var(--pro-ink); margin: 0; }
/* header: navy band, crest and wordmark, headline, one real photo */
.top { position: relative; display: grid; grid-template-columns: 1.15fr .85fr; background: #0B1A4A; color: #fff; min-height: 62mm; }
.top-copy { padding: 8mm 0 6.5mm 13mm; position: relative; z-index: 2; }
.brand { display: flex; align-items: center; gap: 2.6mm; margin-bottom: 4.4mm; }
.seal { width: 9mm; height: 9mm; } .wm { height: 5.2mm; width: auto; }
.top .eyebrow { color: #C9D6F2; }
.top h1 { color: #fff; font-size: 17.5pt; line-height: 1.12; margin: 2mm 0 3mm; letter-spacing: -.005em; }
:lang(zh) .top h1 { font-size: 17pt; line-height: 1.3; }
.top h1 em { color: #C9D6F2; }
.lede { margin: 0; font-size: 7.6pt; line-height: 1.5; color: rgba(255,255,255,.86); max-width: 104mm; }
.lede b { color: #fff; font-weight: 600; }
.photo { margin: 0; position: relative; overflow: hidden; }
.photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 62% 30%;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 38%); mask-image: linear-gradient(90deg, transparent 0, #000 38%); }
.photo figcaption { position: absolute; right: 4mm; bottom: 3mm; font-size: 5.8pt; color: rgba(255,255,255,.85); }
/* credibility: member of, then where the team studied and worked */
.cred { display: grid; grid-template-columns: 1fr; gap: 2.6mm; padding: 3.8mm 13mm 3.6mm; border-bottom: 1px solid var(--pro-line); }
.member { display: grid; grid-template-columns: 30mm auto auto 1fr; align-items: center; gap: 6mm; padding-bottom: 2.6mm; border-bottom: 1px solid var(--pro-line); }
.member .lab { color: #4A5578; }
.m { display: flex; align-items: center; gap: 2mm; } .m em { font-style: normal; font-size: 5.8pt; color: #4A5578; }
.anth { height: 2.6mm; } .oai { height: 5mm; }
.team { display: grid; gap: 2.4mm; }
.team > div { display: grid; grid-template-columns: 30mm 1fr; align-items: center; }
.team .lab, .member .lab { color: #4A5578; font-size: 5.6pt; white-space: nowrap; }
.lg { display: flex; align-items: center; gap: 5.6mm; flex-wrap: nowrap; }
.lg img { width: auto; filter: grayscale(1) contrast(1.15); opacity: .8; }
/* programs */
.progs { padding: 4mm 13mm 3.4mm; }
.cols { display: grid; grid-template-columns: 1.15fr 1.05fr 1fr .8fr; gap: 5mm; margin-top: 2.4mm; border-top: 1px solid var(--pro-ink); padding-top: 2.6mm; }
.col h3 { font: 600 7.4pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-ink); margin-bottom: 1.4mm; }
.col ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.6mm; }
.col li b { display: block; font: 500 8.2pt/1.25 SERIF; color: var(--pro-ink); }
.col li span { font-size: 6.6pt; color: #4A5578; }
/* the three panels: approach, staff fluency, student data */
.three { display: grid; grid-template-columns: 1.25fr 1fr 1fr; gap: 0; margin: 0 13mm; border-top: 1px solid var(--pro-line); border-bottom: 1px solid var(--pro-line); }
.three > div { padding: 3.2mm 4.5mm 3.2mm; }
.three > div + div { border-left: 1px solid var(--pro-line); }
.three > div:first-child { padding-left: 0; } .three > div:last-child { padding-right: 0; }
.three h2 { font-size: 9.6pt; line-height: 1.25; margin: 1.6mm 0 1.6mm; }
.three h2 em { color: var(--pro-action); }
.three p { margin: 0; font-size: 6.9pt; color: #3A4466; }
.p1 { display: grid; grid-template-columns: 25mm 1fr; column-gap: 3.6mm; align-items: start; }
.p1 .sk { grid-column: 1 / -1; margin-bottom: 1.6mm; }
.wheel .apw { width: 25mm; height: 25mm; }
.p1 h2 { margin-top: 0; }
.stairs { list-style: none; margin: 1.4mm 0 2mm; padding: 0; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1mm; align-items: end; }
.stairs li { height: calc(5.4mm + var(--s) * 1.7mm); border-top: 1.4px solid var(--pro-action); background: color-mix(in srgb, var(--pro-action) calc(5% + var(--s) * 4%), #fff);
  padding: .8mm .9mm; display: flex; flex-direction: column; justify-content: flex-start; }
.stairs i { font: 400 6.4pt/1 SERIF; color: var(--pro-action); font-style: normal; } .stairs b { font-size: 5.3pt; line-height: 1.15; font-weight: 600; color: var(--pro-ink); }
.commit { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.2mm; font-size: 6.6pt; color: #3A4466; }
.commit b { color: var(--pro-ink); font-weight: 600; }
/* selected programs */
.ran { padding: 3.4mm 13mm 3.6mm; }
.cases { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-top: 2.2mm; }
.case { padding: 2.5mm 3.2mm; border: 1px solid var(--pro-line); border-radius: 2mm; }
.case .k { color: #4A5578; font-size: 5.6pt; } .case b { display: block; margin: 1mm 0 .8mm; font: 500 8.4pt/1.25 SERIF; color: var(--pro-ink); }
.case p { margin: 0; font-size: 6.7pt; color: #3A4466; }
/* closing band */
.cta { display: flex; justify-content: space-between; align-items: center; gap: 8mm; background: #0B1A4A; color: #fff; padding: 6mm 13mm; }
.cta h2 { color: #fff; font-size: 13pt; } .cta p { margin: 1.2mm 0 0; font-size: 7pt; color: rgba(255,255,255,.82); max-width: 112mm; }
.contact { display: grid; gap: 1mm; text-align: right; font-size: 8.4pt; } .contact b { font-weight: 600; } .contact span { color: #C9D6F2; }
"""


def render(src, pdf):
    js = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, pdf] = process.argv.slice(1);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto(src, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: 'print' });
  const over = await p.evaluate(() => { const m = document.querySelector('.op'); const kids = [...m.children]; return Math.round(kids.reduce((a, k) => a + k.getBoundingClientRect().height, 0) - m.getBoundingClientRect().height); });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log(JSON.stringify({ overflowPx: over })); await b.close();
})();
"""
    out = subprocess.run(['node', '-e', js, src, pdf], capture_output=True, text=True, cwd=os.path.join(ROOT, '.ds-sync'))
    if out.returncode:
        sys.exit(out.stderr)
    return out.stdout.strip()


if __name__ == '__main__':
    for lang, t in (('en', E), ('cn', Z)):
        html_path = os.path.join(HERE, 'onepager-%s.html' % lang)
        open(html_path, 'w', encoding='utf-8').write(page(t, lang))
        pdf = os.path.join(ROOT, 'onepager', 'arena-school-one-pager-%s.pdf' % lang)
        info = render('http://127.0.0.1:8931/tools/one-pager/onepager-%s.html' % lang, pdf)
        pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1)
        jpg = pdf[:-4] + '.jpg'
        subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=86', '-singlefile', '-scale-to-x', '520', '-scale-to-y', '-1', pdf, jpg[:-4]], check=True)
        print('%s: %s page(s), overflow %s' % (os.path.relpath(pdf, ROOT), pages, info))
        if pages != '1' or int(re.search(r'-?\d+', info).group(0)) > 0:
            sys.exit('not one page, or content taller than the page')
