"""Arena School one-pagers, v3 (ONEPAGER2-BRIEF and UPDATES 1 to 4, Oct 17, 2026): general, teacher, parent; EN + CN.

Outputs (A4, exactly one page each; the general one keeps its old paths so onepager.js and every link keep working):
  onepager/arena-school-one-pager-{en,cn}.pdf          general
  onepager/arena-school-teacher-one-pager-{en,cn}.pdf  teachers and school leaders
  onepager/arena-school-parent-one-pager-{en,cn}.pdf   families
  + a 520px .jpg thumbnail next to each PDF; HTML sources in tools/one-pager/
The build fails unless each PDF is one page, nothing is taller than the page, every grid item's left and right edges sit
on the 12-column grid, cards in a row have equal heights, and no text is under 7pt (checked in the browser).

Layout: one 12-column grid (10mm side margins, 4mm gutters) on every row; thirds, halves and quarters only; numbered
section headers in one position. Offer and proof are one section (UPDATES 3 and 4): abstracted audience tiles (icon,
short label, one line, formats in a few words; no grades, dates or program names) with a proof line of real partner
logos from the repo and a 3 to 5 word caption (a plain text label where no logo file exists; never a recreated logo).
Diagrams: the learning wheel, the fluency staircase, the mentorship ladder, a personal vs school account pair.
Copy: the site's own sources (tools/approach_page.py, tools/fluency_section.py, tools/data_section.py, the program pages,
PAST-TALKS-SOURCES.md). No stats, no ISB numbers, no em dashes. CN marked for JJ review. Changes: ONEPAGER-CHANGES.md.
  python3 tools/one-pager/build.py [general|teacher|parent ...] [--who A|B|C]   (needs the local server on 127.0.0.1:8931)
"""
import json
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
import fluency_section as FL  # noqa: E402

ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']


def ic(name, cls='ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, ICONS[name]))


# real partner marks in the repo (logo file) or a text label where none exists
LOGO = {'isb': ('/logos/cred/isb.png', 6.4), 'tsinghua': ('/logos/cred/tsinghua-lockup.png', 6.4), 'pta': ('/decks/img/conversation/pta-logo.png', 6.2),
        'lux': ('/logos/lux/lux-navy-horizontal.png', 6.6), 'bodley': (None, 'Bodley Academy'), 'acamis': (None, 'ACAMIS')}

L = {
 'en': dict(
   member='A member of', anth='Startup Program', oai='Partner Network', studied='Our team studied at', worked='Our team worked at',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='Run with',
   # audience tiles: key -> (icon, label, one line, formats, [proof marks], proof caption)
   T={'students': ('graduation-cap', 'Students', 'Build and launch real products with AI.', 'Workshops · intensives · mentorship', ['isb', 'bodley'], 'Five-day student programs'),
      'schools': ('school', 'Teachers &amp; schools', 'Make the tools classes need, inside school rules.', 'Sessions · workshops · school-wide', ['tsinghua'], 'Staff training, Schwarzman College'),
      'families': ('heart-handshake', 'Families', 'One project with a mentor, and parent talks.', '1:1 mentorship · parent talks', ['pta'], 'Parent talk, ISB PTA'),
      'career': ('briefcase', 'University &amp; career', 'Launch a live AI product, ready for work.', 'Bootcamp', ['lux'], 'Jointly hosted with Lux Scholar'),
      # teacher variant
      'teachers': ('wrench', 'Teachers', 'Make the tool your class is missing.', 'Session · workshop · school-wide', ['tsinghua'], 'Staff training, Schwarzman College'),
      'tech': ('monitor-cog', 'Technology teams', 'Training on your approved systems.', 'Planning · sessions', [], ''),
      'leaders': ('building-2', 'School leaders', 'Programs for the whole school community.', 'Planned with your team', ['isb'], 'Student program on campus'),
      'conf': ('mic', 'Conferences', 'Talks and hands-on workshops.', 'Keynote · workshop · panel', ['acamis'], 'Next: ACAMIS workshop'),
      # parent variant
      'workshops': ('smartphone', 'Hands-on workshops', 'Rebuild an app, or build a portfolio site.', 'At your child’s school', [], ''),
      'intensive': ('rocket', 'Intensives', 'Teams launch a real product and pitch it.', 'With mentors in the room', ['isb', 'bodley'], 'Five-day student programs'),
      'mentor': ('route', 'Year-long mentorship', 'One project, 1:1, at their own pace.', 'Weekly check-ins, hybrid', ['isb'], 'ISB alumni continue here'),
      'talks': ('messages-square', 'Parent talks', 'How AI is changing work and college.', 'At your child’s school', ['pta'], 'Parent talk, ISB PTA')},
   formats_k='Formats',
   skills=[('compass', 'Agency', 'Choose what is worth doing.'), ('search-check', 'Taste', 'Judge whether it is actually good.'), ('badge-check', 'Craft', 'Finish it so people can trust it.')],
   loop='Learners decide. AI builds. Real people judge.', strands_k='Four strands, assessed on every project',
   dk='Whose account is it?', personal='Personal account', school='School-approved platform',
   prow=['Consumer terms', 'No data agreement', 'Not for student data'], srow=['Enterprise agreement', 'Agreed by the school', 'Approved for student data'],
   cta='Bring Arena to your school.', ctap='Planned with your team, run on your campus. Your teachers keep the materials.',
   hub='Arena School',
 ),
 'cn': dict(
   member='成员计划', anth='初创企业计划', oai='合作伙伴网络', studied='团队就读于', worked='团队曾任职于',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='合作',
   T={'students': ('graduation-cap', '学生', '借助AI做出并上线真实的产品。', '工作坊 · 集训营 · 导师计划', ['isb', 'bodley'], '五天学生项目'),
      'schools': ('school', '教师与学校', '在学校规则之内，做出课堂需要的工具。', '分享 · 工作坊 · 全校培训', ['tsinghua'], '苏世民书院教职员工培训'),
      'families': ('heart-handshake', '家庭', '与导师一起完成一个项目，以及家长讲座。', '一对一导师 · 家长讲座', ['pta'], 'ISB PTA 家长讲座'),
      'career': ('briefcase', '大学与职场', '做出上线的AI产品，为工作做好准备。', '训练营', ['lux'], '与千麓学者联合举办'),
      'teachers': ('wrench', '教师', '为课堂做一个正缺的小工具。', '现场分享 · 工作坊 · 全校培训', ['tsinghua'], '苏世民书院教职员工培训'),
      'tech': ('monitor-cog', '技术团队', '在学校认可的系统上开展培训。', '规划 · 培训', [], ''),
      'leaders': ('building-2', '校长与管理层', '服务整个学校社群的项目。', '与贵校团队共同规划', ['isb'], '在校园内开展的学生项目'),
      'conf': ('mic', '会议与活动', '主题演讲与动手工作坊。', '演讲 · 工作坊 · 圆桌', ['acamis'], '即将举行：ACAMIS 工作坊'),
      'workshops': ('smartphone', '动手工作坊', '重做一款应用，或做一个作品集网站。', '在孩子的学校', [], ''),
      'intensive': ('rocket', '集训营', '团队做出真实的产品并路演。', '导师全程在场', ['isb', 'bodley'], '五天学生项目'),
      'mentor': ('route', '学年导师计划', '一个项目，一对一，按自己的节奏。', '每周例会，线上线下结合', ['isb'], 'ISB 营员在此继续'),
      'talks': ('messages-square', '家长讲座', 'AI如何改变工作与升学。', '在孩子的学校', ['pta'], 'ISB PTA 家长讲座')},
   formats_k='形式',
   skills=[('compass', '主动性', '选出值得做的事。'), ('search-check', '审美', '判断它是否真的好。'), ('badge-check', '匠心', '把它做好做完，让人信得过。')],
   loop='学习者做决定，AI动手做，真实的人来评判。', strands_k='四条学习主线，每个项目都评估',
   dk='这是谁的账号？', personal='个人账号', school='学校认可的平台',
   prow=['面向消费者的条款', '与学校没有数据协议', '不可用于学生数据'], srow=['企业协议', '由学校签订', '获准用于学生数据'],
   cta='把 Arena 带进贵校。', ctap='与贵校团队共同规划，在贵校校园开展。老师们保留全部材料。',
   hub='Arena School',
 ),
}
LOGO_CN = {'bodley': 'Bodley Academy', 'acamis': 'ACAMIS'}

DOCS = {
 'general': dict(file='arena-school-one-pager', tiles=['students', 'schools', 'families', 'career'],
   en=dict(eyebrow='What is Arena School', h1='Hands-on programs that help students, families, educators, and schools <em>thrive in the age of AI.</em>'),
   cn=dict(eyebrow='认识 Arena School', h1='动手实践的项目，陪伴学生、家庭、教育者与学校，<em>从容走进AI时代。</em>')),
 'teacher': dict(file='arena-school-teacher-one-pager', tiles=['teachers', 'tech', 'leaders', 'conf'],
   en=dict(eyebrow='For teachers and school leaders', h1='AI fluency for the whole staff, <em>inside your school’s rules.</em>'),
   cn=dict(eyebrow='面向教师与学校管理层', h1='全体教职员工的AI素养，<em>始终在学校的规则之内。</em>')),
 'parent': dict(file='arena-school-parent-one-pager', tiles=['workshops', 'intensive', 'mentor', 'talks'],
   en=dict(eyebrow='For families', h1='What your child makes, learns, and keeps <em>at Arena School.</em>'),
   cn=dict(eyebrow='写给家长', h1='孩子在 Arena School <em>做什么、学什么、带走什么。</em>')),
}
STUDIED = [('caltech', 3.2), ('harvard', 4.0), ('brown', 4.2), ('tsinghua-lockup', 4.6), ('isb', 4.6)]
WORKED = [('mckinsey', 2.6), ('goldman', 4.0), ('yc', 3.8), ('apple', 4.0), ('microsoft-ai', 3.2), ('deloitte', 2.7), ('kimi-wordmark', 2.8)]

S = {
 'en': dict(who='Who we serve, and where we’ve run it', who_t='Who we work with, and where we’ve run it', who_p='What your child can do, and where we’ve run it',
            teach='How we teach', learn='How your child learns', fluency='Staff AI fluency', fluency_s='Five levels; every teacher moves up one a term',
            data='Student data first', guard='Student data guardrails', safe='Safety and student data',
            move='How a teacher moves up one level', outcomes='Learning outcomes', tools='Tools teachers made', tools_by='Made by Ben, an English teacher at Shanghai American School (SAS)',
            ladder='Year-long mentorship: the milestone ladder'),
 'cn': dict(who='我们服务谁，在哪里开展过', who_t='我们与谁合作，在哪里开展过', who_p='孩子可以做什么，我们在哪里开展过',
            teach='我们如何教', learn='孩子如何学习', fluency='教职员工AI素养', fluency_s='五个层级，每位老师每学期提升一级',
            data='学生数据放在第一位', guard='学生数据保护规则', safe='安全与学生数据',
            move='老师如何提升一级', outcomes='学习成果', tools='老师们做的工具', tools_by='由上海美国学校（SAS）英文老师 Ben 制作',
            ladder='学年项目导师计划：里程碑'),
}
X = {
 'en': dict(
   move=[('book-open', 'Before', 'Each teacher brings one task from a class they teach now.'), ('presentation', 'Show', 'We make one tool live from a plain-language description.'),
         ('hammer', 'Make', 'Each teacher makes theirs on your approved tools and checks every result.'), ('check', 'Keep', 'Teachers keep the tool and the prompt, to reuse and share.')],
   tools=[('file-text', 'Poem annotator', 'Literary devices marked in a poem’s margin.'), ('list-checks', 'Who is missing what', 'Which students are missing which piece of knowledge.'),
          ('pen-line', 'Feedback helper', 'Comment ideas against your own rubric; you edit each one.')],
   model=[('list-checks', 'Baseline', 'A short self-assessment places every teacher.'), ('users', 'One level up', 'Each group trains up one level.'),
          ('search-check', 'Each term', 'Re-measure, so leaders see the curve shift.'), ('user-check', 'Coaches', 'Level 5 teachers coach colleagues.')],
   ladder=['Launch', 'Traction', 'Revenue', 'Impact', 'Recognition'], ladder_d=['A working product at a public link', 'Users from outside their circle', 'First income from paying users', 'Many users, press, or a final', 'A national win, or a company'],
   ladder_l='Each student sets a target with their mentor, then moves up at their own pace, judged on the work.',
   mfacts=[('calendar', 'Weekly', '25-minute check-ins, hybrid'), ('users', 'Solo or a team', 'Up to four students'), ('flag', 'Start', 'Rolling'), ('repeat', 'Length', 'Six months to a year')]),
 'cn': dict(
   move=[('book-open', '培训前', '每位老师带来自己正在教的一门课里的一项任务。'), ('presentation', '演示', '我们现场演示，从一段文字描述做出一个工具。'),
         ('hammer', '动手', '每位老师用学校认可的工具做出自己的版本，并检查每个结果。'), ('check', '带走', '老师留下工具和背后的提示词，可反复使用和分享。')],
   tools=[('file-text', '诗歌批注', '在诗歌旁边标出修辞手法。'), ('list-checks', '谁还没掌握哪个知识点', '一眼看出哪些学生还没掌握哪个知识点。'),
          ('pen-line', '评语助手', '按您的评分标准给出评语建议，每条都由您修改。')],
   model=[('list-checks', '基线', '简短的自我评估确定每位老师的层级。'), ('users', '各升一级', '每组老师提升一级。'),
          ('search-check', '每学期', '重新评估，让管理层看到曲线移动。'), ('user-check', '教练', '第五层级的老师带动同事。')],
   ladder=['上线', '用户增长', '收入', '影响力', '认可'], ladder_d=['可用的产品，发布在公开网址', '来自自己圈子以外的用户', '第一笔付费收入', '大量用户、媒体报道或进入决赛', '全国性比赛获奖，或注册公司'],
   ladder_l='每名学生和导师定好目标，按自己的节奏一级级往上走，看的是做出来的成果。',
   mfacts=[('calendar', '每周', '25分钟例会，线上线下结合'), ('users', '单人或团队', '4人以内'), ('flag', '开始', '滚动入学'), ('repeat', '周期', '六个月到一年')]),
}


# ---------------------------------------------------------------- components
def header(lang, d):
    t, c = DOCS[d][lang], L[lang]
    return ('<header class="top g12"><div class="c1-3 brand"><img src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" /></div>'
            '<div class="c4-10 title"><span class="eyebrow">%s</span><h1>%s</h1></div>'
            '<div class="c11-12 contact"><b>%s</b><span>%s</span></div></header>' % (t['eyebrow'], t['h1'], c['web'], c['mail']))


def strip(lang):
    """Three thin rows, each on one line: member of; studied at; worked at. Labels share column 1-2."""
    c = L[lang]
    lg = lambda items: ''.join('<img src="/logos/cred/%s.png" alt="" style="height:%smm" />' % (k, h) for k, h in items)
    return ('<section class="strip">'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos member">'
            '<span class="m"><img src="/logos/partners/anthropic.svg" alt="Anthropic" style="height:2.4mm" /><em>%s</em></span>'
            '<span class="m"><img src="/logos/partners/openai.svg" alt="OpenAI" style="height:4.4mm" /><em>%s</em></span></div></div>'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos">%s</div></div>'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos">%s</div></div></section>'
            % (c['member'], c['anth'], c['oai'], c['studied'], lg(STUDIED), c['worked'], lg(WORKED)))


def sh(n, title, sub='', grid='g12'):
    return '<div class="sh %s"><div class="c1-%d"><b>%02d</b><h2>%s</h2>%s</div></div>' % (grid, 12 if grid == 'g12' else 6, n, title, '<span>%s</span>' % sub if sub else '')


def mark(k, big=False):
    f, v = LOGO[k]
    return ('<img src="%s" alt="" style="height:%smm" />' % (f, v * (1 if big else .66))) if f else '<span class="wordmark">%s</span>' % v


def proof(lang, marks, cap):
    if not marks:
        return '<div class="proof none"></div>'
    return '<div class="proof"><span class="marks">%s</span><span class="cap">%s</span></div>' % (''.join(mark(m) for m in marks), cap)


def tiles(lang, keys, option):
    c = L[lang]
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    if option == 'A':   # tiles, each with its own proof line
        return '<div class="g12 rrow tiles">%s</div>' % ''.join(
            '<div class="%s card tile">%s<b class="nm">%s</b><span class="out">%s</span><span class="fm">%s</span>%s</div>'
            % (s, ic(t[0], 'ic big'), t[1], t[2], t[3], proof(lang, t[4], t[5])) for s, t in zip(spans, [c['T'][k] for k in keys]))
    if option == 'B':   # hub: Arena at the center, audiences, then formats, with one proof strip
        aud = ''.join('<div class="%s hubaud">%s<b class="nm">%s</b><span class="fm">%s</span></div>' % (s, ic(t[0], 'ic big'), t[1], t[3])
                      for s, t in zip(spans, [c['T'][k] for k in keys]))
        strip_ = ''.join('<div class="%s pstrip">%s</div>' % (s, proof(lang, t[4], t[5])) for s, t in zip(spans, [c['T'][k] for k in keys]))
        return ('<div class="g12"><div class="c1-12 hub"><span class="hubdot">%s</span></div></div><div class="g12 hubrow">%s</div><div class="g12 hubproof">%s</div>'
                % (c['hub'], aud, strip_))
    # C: slim audience row, then a captioned logo strip
    row = ''.join('<div class="%s slim">%s<div><b class="nm">%s</b><span class="out">%s</span></div></div>' % (s, ic(t[0], 'ic big'), t[1], t[2])
                  for s, t in zip(spans, [c['T'][k] for k in keys]))
    marks = [(m, c['T'][k][5]) for k in keys for m in c['T'][k][4][:1]]
    st = ''.join('<div class="c%d-%d pmark">%s<span class="cap">%s</span></div>' % (1 + 3 * i, 3 + 3 * i, mark(m, True), cap) for i, (m, cap) in enumerate(marks[:4]))
    return '<div class="g12 rrow">%s</div><div class="g12 pline"><span class="c1-12 k">%s</span></div><div class="g12 rrow">%s</div>' % (row, c['proof'], st)


def teach(lang):
    c, t = L[lang], A.T['cn' if lang == 'cn' else 'en']
    skills = ''.join('<li>%s<b>%s</b><span>%s</span></li>' % (ic(i), a, b) for i, a, b in c['skills'])
    outs = ''.join('<li><b>%s</b><span>%s</span></li>' % (d, g) for d, g in zip(t['domains'], t['goals']))
    return ('<div class="g12 teach"><div class="c1-3 wheelbox"><div class="wheel">%s</div><p class="loop">%s</p></div>'
            '<div class="c4-6"><ul class="skills">%s</ul></div><div class="c7-12"><span class="k">%s</span><ul class="outs">%s</ul></div></div>'
            % (W.svg('cn' if lang == 'cn' else 'en'), c['loop'], skills, c['strands_k'], outs))


def stairs(items):
    return '<ol class="stairs">%s</ol>' % ''.join('<li style="--s:%d"><i>%d</i><b>%s</b><span>%s</span></li>' % (i, i + 1, n, d) for i, (n, d) in enumerate(items))


def rows(items, cls='model'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ic(i), a, b) for i, a, b in items))


def account(lang):
    c = L[lang]
    col = lambda title, rs, ok: ('<div class="acc %s">%s<b>%s</b><ul>%s</ul></div>'
                                 % ('ok' if ok else 'no', ic('school' if ok else 'user-round'), title, ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs)))
    return '<div class="accs"><span class="k">%s</span><div class="pair">%s%s</div></div>' % (c['dk'], col(c['personal'], c['prow'], False), col(c['school'], c['srow'], True))


def commits(lang, n=4, pick=None):
    d = DS.C['cn' if lang == 'cn' else 'en']
    items = [d['commit'][k] for k in pick] if pick else d['commit'][:n]
    return rows([(i, a, b) for i, a, b in items], 'commit')


def data_row(lang, n, title, k=3, pick=None):
    return (sh(n, title) + '<div class="g12 datarow"><div class="c1-6">%s</div><div class="c7-12">%s</div></div>' % (account(lang), commits(lang, k, pick)))


PCTA = {'en': ('Two ways to start.', 'Ask your child’s school to bring Arena, or enroll in the Year-Long Project Mentorship directly.'),
        'cn': ('两种开始方式。', '请孩子的学校邀请 Arena，或直接报名学年项目导师计划。')}


def footer(lang, doc='general'):
    c = L[lang]
    h, p = PCTA[lang] if doc == 'parent' else (c['cta'], c['ctap'])
    return ('<footer class="cta g12"><div class="c1-8"><h2>%s</h2><p>%s</p></div><div class="c9-12 contact"><b>%s</b><span>%s</span></div></footer>'
            % (h, p, c['mail'], c['web']))


def general(lang, opt):
    s = S[lang]
    f = FL.C['cn' if lang == 'cn' else 'en']
    return (sh(1, s['who']) + tiles(lang, DOCS['general']['tiles'], opt) +
            sh(2, s['teach']) + teach(lang) +
            sh(3, s['fluency'], s['fluency_s']) + '<div class="g12"><div class="c1-8">%s</div><div class="c9-12">%s</div></div>' % (stairs(f['levels']), rows(X[lang]['model'])) +
            data_row(lang, 4, s['data']))


def teacher(lang, opt):
    s, x = S[lang], X[lang]
    f = FL.C['cn' if lang == 'cn' else 'en']
    t = A.T['cn' if lang == 'cn' else 'en']
    move = ''.join('<div class="c%d-%d card step"><div class="sthead"><i>%02d</i>%s<b class="nm">%s</b></div><span class="out">%s</span></div>' % (1 + 3 * k, 3 + 3 * k, k + 1, ic(i), a, b) for k, (i, a, b) in enumerate(x['move']))
    dom_icons = ['target', 'search-check', 'hammer', 'messages-square']
    outs = ''.join('<div class="c%d-%d card oc">%s<div><b class="nm">%s</b><span class="out">%s</span></div></div>' % (1 + 3 * k, 3 + 3 * k, ic(dom_icons[k]), d, g)
                   for k, (d, g) in enumerate(zip(t['domains'], t['goals'])))
    tl = ''.join('<div class="c%d-%d card tool">%s<div><b class="nm">%s</b><span class="out">%s</span></div></div>' % (1 + 4 * k, 4 + 4 * k, ic(i), a, b) for k, (i, a, b) in enumerate(x['tools']))
    return (sh(1, s['who_t']) + tiles(lang, DOCS['teacher']['tiles'], opt) +
            sh(2, s['fluency'], s['fluency_s']) + '<div class="g12"><div class="c1-8">%s</div><div class="c9-12">%s</div></div>' % (stairs(f['levels']), rows(x['model'])) +
            sh(3, s['move']) + '<div class="g12 rrow">%s</div>' % move +
            sh(4, s['outcomes']) + '<div class="g12 rrow">%s</div>' % outs +
            data_row(lang, 5, s['guard'], 3))


def parent(lang, opt):
    s, x = S[lang], X[lang]
    return (sh(1, s['who_p']) + tiles(lang, DOCS['parent']['tiles'], opt) +
            sh(2, s['ladder']) + '<div class="g12"><div class="c1-8">%s<p class="note">%s</p></div><div class="c9-12">%s</div></div>'
            % (stairs(list(zip(x['ladder'], x['ladder_d']))), x['ladder_l'], rows(x['mfacts'])) +
            sh(3, s['learn']) + teach(lang) +
            data_row(lang, 4, s['safe'], pick=[1, 3, 0]))


BODY = {'general': general, 'teacher': teacher, 'parent': parent}
SPANS = '\n'.join('.c%d-%d { grid-column: %d / %d; }' % (a, b, a, b + 1) for a in range(1, 13) for b in range(a, 13))


def page(doc, lang, opt):
    cn = lang == 'cn'
    jj = '<!-- JJ review: %s one-pager CN copy (ONEPAGER2-BRIEF, Oct 17, 2026) -->\n' % doc if cn else ''
    fonts = '<link rel="stylesheet" href="/fonts/gf.css" />' + ('<link rel="stylesheet" href="/fonts/zh/zh.css?v=2" />' if cn else '')
    serif = "'Newsreader', 'Arena Serif SC', 'Songti SC', 'Noto Serif SC', Georgia, serif" if cn else "'Newsreader', Georgia, serif"
    root = re.search(r'(?s):root\s*\{.*?\n\}', open(os.path.join(ROOT, 'css', 'pro.css'), encoding='utf-8').read()).group(0)
    wcss = '\n'.join(l for l in open(os.path.join(ROOT, 'css', 'approach.css'), encoding='utf-8').read().splitlines() if l.startswith('.apw'))
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8" />\n<title>Arena School one-pager</title>\n%s%s\n<style>\n%s\n%s\n%s\n</style>\n</head>\n<body>\n'
            '<main class="op %s who-%s">\n%s\n%s\n<div class="body">%s</div>\n%s\n</main>\n</body>\n</html>\n'
            % ('zh-CN' if cn else 'en', jj, fonts, root, wcss, CSS.replace('SERIF', serif), doc, opt, header(lang, doc), strip(lang), BODY[doc](lang, opt), footer(lang, doc)))


CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Geist', 'PingFang SC', system-ui, sans-serif; color: #1E2740; font-size: 7.6pt; line-height: 1.38; }
.op { width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; }
.op > * { flex-shrink: 0; }
.g12 { display: grid; column-gap: 4mm; grid-template-columns: repeat(12, minmax(0, 1fr)); padding: 0 10mm; }
SPANS
h1, h2, .nm, .loop { font-family: SERIF; font-weight: 500; color: var(--pro-ink); margin: 0; }
em { font-style: italic; }
.ic { width: 4.2mm; height: 4.2mm; color: var(--pro-action); flex: none; } .ic.big { width: 6mm; height: 6mm; }
.k, .lab, .eyebrow { font: 600 7pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #4A5578; }
:lang(zh) .k, :lang(zh) .lab, :lang(zh) .eyebrow { letter-spacing: .04em; }
/* header band: short */
.top { background: #0B1A4A; color: #fff; align-items: center; padding-top: 5.5mm; padding-bottom: 5.5mm; }
.brand img { height: 5mm; width: auto; display: block; }
.title .eyebrow { color: #C9D6F2; }
.top h1 { color: #fff; font-size: 14pt; line-height: 1.2; margin-top: 1.2mm; }
:lang(zh) .top h1 { font-size: 12.5pt; } :lang(zh) .top h1 em { white-space: nowrap; }
.top h1 em { color: #C9D6F2; }
.top .contact { text-align: right; display: grid; gap: .8mm; font-size: 7.6pt; } .top .contact b { font-weight: 600; } .top .contact span { color: #C9D6F2; }
/* credentials strip: two single-line rows */
.strip { padding: 2.4mm 0; border-bottom: 1px solid var(--pro-line); display: grid; gap: 1.6mm; }
.strip .lab { white-space: nowrap; }
.strip .row { align-items: center; }
.logos { display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; min-width: 0; }
.logos img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
.member { justify-content: flex-start; gap: 10mm; } .member img { filter: none; opacity: 1; }
.m { display: inline-flex; align-items: center; gap: 1.6mm; white-space: nowrap; } .m em { font-style: normal; font-size: 7pt; color: #4A5578; }
/* body: sections spread down the page */
.body { flex: 1; display: flex; flex-direction: column; padding: 0 0 3.6mm; }
.body > .sh { margin-top: auto; padding-top: 2.2mm; }
.sh > div { display: flex; align-items: baseline; gap: 2.4mm; border-bottom: 1px solid var(--pro-ink); padding-bottom: 1.2mm; margin-bottom: 2.4mm; }
.sh b { font: 400 11pt/1 SERIF; color: var(--pro-action); }
.sh h2 { font-size: 11.5pt; line-height: 1.1; }
.sh span { margin-left: auto; font-size: 7pt; color: #4A5578; }
.card { border: 1px solid var(--pro-line); border-radius: 1.6mm; padding: 2.6mm 2.8mm; background: #fff; display: flex; gap: 2mm; align-items: flex-start; min-width: 0; }
.nm { display: block; font-size: 9pt; line-height: 1.2; }
.out { display: block; font-size: 7.6pt; line-height: 1.32; color: #3A4466; margin-top: .6mm; }
.fm { display: block; font: 600 7pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-action); margin-top: 1mm; }
.rrow { align-items: stretch; }
/* option A: audience tiles with proof */
.tile { flex-direction: column; gap: 1mm; }
.tile .proof { margin-top: auto; width: 100%; padding-top: 2mm; border-top: 1px solid var(--pro-line); }
.proof { display: flex; flex-direction: column; gap: 1mm; min-height: 11mm; }
.proof.none { border-top-color: transparent !important; }
.marks { display: flex; align-items: center; gap: 2.4mm; min-height: 5.6mm; flex-wrap: nowrap; }
.marks img { width: auto; display: block; }
.wordmark { font: 600 7pt/1.1 SERIF; color: var(--pro-ink); white-space: nowrap; padding: .6mm 1.2mm; border: 1px solid var(--pro-line-2); border-radius: 1mm; }
.cap { font-size: 7pt; color: #4A5578; }
/* option B: hub */
.hub { display: flex; justify-content: center; position: relative; height: 9mm; }
.hub::after { content: ""; position: absolute; left: 12.5%; right: 12.5%; top: 9mm; border-top: 1px solid var(--pro-action); }
.hubdot { background: #0B1A4A; color: #fff; font: 500 9pt/1 SERIF; padding: 2mm 4mm; border-radius: 6mm; align-self: flex-start; }
.hubrow { margin-top: 3mm; } .hubaud { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 1mm; padding-top: 2.6mm; border-top: 2px solid var(--pro-action); }
.hubproof { margin-top: 2.6mm; } .pstrip .proof { align-items: center; text-align: center; }
/* option C: slim row + logo strip */
.slim { display: flex; gap: 2mm; align-items: flex-start; padding: 2mm 0; border-top: 2px solid var(--pro-action); }
.pline { margin-top: 2.6mm; } .pline .k { display: block; margin-bottom: 1.4mm; }
.pmark { display: flex; flex-direction: column; gap: 1mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); }
/* how we teach */
.teach { align-items: center; }
.wheelbox { display: flex; flex-direction: column; align-items: flex-start; gap: 1.6mm; }
.wheel .apw { width: 28mm; height: 28mm; }
.loop { font-size: 9pt; line-height: 1.25; }
.skills, .outs, .commit, .model { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.6mm; }
.skills li { display: grid; grid-template-columns: 4.2mm 1fr; column-gap: 1.8mm; align-items: center; padding: 1.4mm 0; border-top: 1px solid var(--pro-line); }
.skills li span { grid-column: 2; }
.skills b { font: 600 8.4pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
.skills span, .outs span { font-size: 7.6pt; color: #3A4466; }
.outs { margin-top: 1.2mm; grid-template-columns: 1fr 1fr; gap: 2mm 4mm; } .outs li { display: grid; gap: .2mm; } .outs b { font-weight: 600; font-size: 7.6pt; color: var(--pro-ink); }
/* staircase */
.stairs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, 1fr); gap: 1.4mm; align-items: end; }
.stairs li { height: calc(22mm + var(--s) * 3mm); border-top: 2px solid var(--pro-action); background: color-mix(in srgb, var(--pro-action) calc(6% + var(--s) * 4%), #fff); padding: 1.6mm 1.8mm; }
.stairs i { font: 400 9pt/1 SERIF; color: var(--pro-action); font-style: normal; display: block; }
.stairs b { display: block; font-size: 8pt; line-height: 1.2; font-weight: 600; color: var(--pro-ink); margin-top: .6mm; }
.stairs span { display: block; font-size: 7pt; line-height: 1.25; color: #3A4466; margin-top: .6mm; }
.note { margin: 1.6mm 0 0; font-size: 7.4pt; color: #3A4466; }
.model li, .commit li { display: flex; gap: 2mm; align-items: flex-start; padding-top: 1.4mm; border-top: 1px solid var(--pro-line); }
.model b, .commit b { display: block; font-weight: 600; font-size: 7.8pt; color: var(--pro-ink); } .model span, .commit span { font-size: 7.4pt; color: #3A4466; }
/* illustrative fluency curve (tools/fluency_section.py chart): shape only, labeled not data */
.fl-chart { margin: 2mm 0 0; } .fl-chart svg { display: block; width: 100%; height: 13mm; }
.fl-axis { stroke: var(--pro-line-2); stroke-width: 1; } .fl-area-a { fill: color-mix(in srgb, #4A5578 12%, transparent); } .fl-line-a { fill: none; stroke: #4A5578; stroke-width: 1.4; stroke-dasharray: 4 4; }
.fl-area-b { fill: color-mix(in srgb, var(--pro-action) 16%, transparent); } .fl-line-b { fill: none; stroke: var(--pro-action); stroke-width: 1.8; }
.fl-ticks { display: none; }
.fl-chart figcaption { display: flex; gap: 3mm; margin-top: .8mm; font-size: 7pt; color: #4A5578; } .fl-key { display: inline-flex; align-items: center; gap: 1.2mm; }
.fl-key i { width: 4mm; border-top: 1.4px dashed #4A5578; } .fl-key i.b { border-top: 1.8px solid var(--pro-action); } .fl-cap { margin-left: auto; }
/* account pair */
.accs .k { display: block; margin-bottom: 1.4mm; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.acc { border: 1px solid var(--pro-line); border-radius: 1.6mm; padding: 2mm 2.4mm; } .acc.ok { border-color: var(--pro-ink); box-shadow: inset 0 2px 0 var(--pro-action); }
.acc > .ic { color: #4A5578; } .acc.ok > .ic { color: var(--pro-action); }
.acc > b { display: block; font: 600 8pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); margin: .8mm 0 1mm; }
.acc ul { list-style: none; margin: 0; padding: 0; display: grid; gap: .8mm; } .acc li { display: flex; gap: 1.2mm; align-items: center; font-size: 7.4pt; color: #3A4466; }
.mk { width: 3.2mm; height: 3.2mm; flex: none; } .acc.no .mk { color: #9A3B2E; } .acc.ok .mk { color: var(--pro-action); }
.datarow { align-items: start; }
.step { flex-direction: column; gap: .8mm; } .sthead { display: flex; align-items: center; gap: 1.6mm; } .step i { font: 400 9pt/1 SERIF; color: var(--pro-action); font-style: normal; }
.oc { flex-direction: row; }
/* teacher page: six sections, so a little tighter */
.teacher .stairs li { height: calc(21mm + var(--s) * 3mm); }
.teacher .card { padding: 2.1mm 2.4mm; }
.teacher .sh > div { margin-bottom: 2mm; }
.teacher .body { padding: 0 0 2.4mm; }
.teacher .top { padding-top: 4.6mm; padding-bottom: 4.6mm; }
.teacher .strip { padding: 2mm 0; gap: 1.4mm; }
.teacher .proof { min-height: 9mm; }
.teacher .tile .proof { padding-top: 1.6mm; }
/* closing band */
.cta { background: #0B1A4A; color: #fff; padding-top: 4.6mm; padding-bottom: 4.6mm; align-items: center; }
.cta h2 { color: #fff; font-size: 12pt; } .cta p { margin: 1mm 0 0; font-size: 7.6pt; color: rgba(255,255,255,.84); }
.cta .contact { text-align: right; display: grid; gap: .8mm; font-size: 8.4pt; } .cta .contact span { color: #C9D6F2; }
""".replace('SPANS', SPANS)

RENDER_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, pdf] = process.argv.slice(1);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.emulateMedia({ media: 'print' });
  await p.goto(src, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => {
    const m = document.querySelector('.op'), H = m.getBoundingClientRect().height;
    const over = Math.round([...m.children].reduce((a, k) => a + k.getBoundingClientRect().height, 0) - H);
    const g = document.querySelector('.g12'), gr = g.getBoundingClientRect(), cs = getComputedStyle(g);
    const cols = cs.gridTemplateColumns.split(' ').map(parseFloat), gap = parseFloat(cs.columnGap), pl = parseFloat(cs.paddingLeft);
    const starts = [], ends = []; let x = gr.left + pl; cols.forEach(w => { starts.push(x); ends.push(x + w); x += w + gap; });
    const bad = [];
    document.querySelectorAll('.g12 > *').forEach(c => { const r = c.getBoundingClientRect(); if (!r.width) return;
      if (!starts.some(s => Math.abs(s - r.left) < .6) || !ends.some(e => Math.abs(e - r.right) < .6)) bad.push((c.className || c.tagName) + ' ' + r.left.toFixed(1) + '-' + r.right.toFixed(1)); });
    const uneven = [];
    document.querySelectorAll('.rrow').forEach(row => { const hs = [...row.children].map(c => Math.round(c.getBoundingClientRect().height)); if (Math.max(...hs) - Math.min(...hs) > 1) uneven.push(hs.join('/')); });
    const tops = []; document.querySelectorAll('.sh > div').forEach(d => tops.push(Math.round(d.getBoundingClientRect().left)));
    let min = 99; document.querySelectorAll('.op *').forEach(e => { if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg')) min = Math.min(min, parseFloat(getComputedStyle(e).fontSize)); });
    const wrapped = []; document.querySelectorAll('.logos, .marks').forEach(l => { const ys = [...l.children].map(c => Math.round(c.getBoundingClientRect().top + c.getBoundingClientRect().height / 2)); if (Math.max(...ys) - Math.min(...ys) > 4) wrapped.push(l.className); });
    return { over, nbad: bad.length, bad: bad.slice(0, 4), uneven, shLeft: [...new Set(tops)], minPt: +(min * .75).toFixed(2), wrapped,
             cols: starts.map((s, i) => [Math.round(s), Math.round(ends[i])]) };
  });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log(JSON.stringify(r)); await b.close();
})();
"""


def overlay(png, out):
    """The 12-column grid (10mm margins, 4mm gutters) drawn over a 150dpi render; blue lines mark the thirds."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert('RGB')
    d = ImageDraw.Draw(im, 'RGBA')
    px = im.size[0] / 210.0
    col = (210 - 20 - 11 * 4) / 12.0
    for i in range(12):
        x0 = (10 + i * (col + 4)) * px
        x1 = x0 + col * px
        d.rectangle([x0, 0, x1, im.size[1]], fill=(255, 0, 80, 20))
        d.line([x0, 0, x0, im.size[1]], fill=(255, 0, 80, 140))
        d.line([x1, 0, x1, im.size[1]], fill=(255, 0, 80, 140))
    for k in (4, 8):
        x = (10 + k * (col + 4) - 2) * px
        d.line([x, 0, x, im.size[1]], fill=(0, 110, 255, 220), width=2)
    im.save(out)


def build(doc, lang, opt, pngdir=None):
    name = '%s-%s' % (DOCS[doc]['file'], lang)
    open(os.path.join(HERE, name + '.html'), 'w', encoding='utf-8').write(page(doc, lang, opt))
    pdf = os.path.join(ROOT, 'onepager', name + '.pdf')
    out = subprocess.run(['node', '-e', RENDER_JS, 'http://127.0.0.1:8931/tools/one-pager/%s.html' % name, pdf],
                         capture_output=True, text=True, cwd=os.path.join(ROOT, '.ds-sync'))
    if out.returncode:
        sys.exit(out.stderr)
    r = json.loads(out.stdout.strip().splitlines()[-1])
    pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1)
    subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=86', '-singlefile', '-scale-to-x', '520', '-scale-to-y', '-1', pdf, pdf[:-4]], check=True)
    if pngdir:
        base = os.path.join(pngdir, name)
        subprocess.run(['pdftoppm', '-png', '-r', '150', '-singlefile', pdf, base], check=True)
        overlay(base + '.png', base + '-grid.png')
    ok = pages == '1' and r['over'] <= 0 and r['nbad'] == 0 and not r['uneven'] and r['minPt'] >= 6.95 and not r['wrapped'] and len(r['shLeft']) <= 1
    print('%-40s pages %s | overflow %spx | off-grid %d %s | uneven %s | header lefts %s | logo rows wrapped %s | min %spt | %s'
          % (name, pages, r['over'], r['nbad'], r['bad'][:2], r['uneven'], r['shLeft'], r['wrapped'], r['minPt'], 'OK' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = sys.argv[sys.argv.index('--who') + 1] if '--who' in sys.argv else 'A'
    args = [a for a in args if a != opt]
    pngdir = sys.argv[sys.argv.index('--png') + 1] if '--png' in sys.argv else None
    if pngdir:
        args = [a for a in args if a != pngdir]
    docs = args or list(DOCS)
    fails = [d + '-' + l for d in docs for l in ('en', 'cn') if not build(d, l, opt, pngdir)]
    if fails:
        sys.exit('FAILED: ' + ', '.join(fails))
