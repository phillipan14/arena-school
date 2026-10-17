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
  python3 tools/one-pager/build.py [general|teacher|parent ...] [--dir A|B|C] [--png DIR]   (B is the chosen direction)   (needs the local server on 127.0.0.1:8931)
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
        'lux': ('/logos/lux/lux-navy-horizontal.png', 6.6), 'schwarzman': ('/logos/cred/schwarzman.png', 4.6), 'bodley': (None, 'Bodley Academy'), 'acamis': (None, 'ACAMIS')}

L = {
 'en': dict(
   member='A member of', anth='Startup Program', oai='Partner Network', studied='Built by a team from', worked='',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='Run with',
   # audience tiles: key -> (icon, label, one line, formats, [proof marks], proof caption)
   T={'students': ('graduation-cap', 'Students', 'Want real AI skills and work to show. They launch a product.', 'Workshops · mentorship', ['isb', 'bodley'], 'Five-day student programs'),
      'schools': ('school', 'Educators', 'Want confident staff and safe use. Each makes a classroom tool.', 'Sessions · workshops', ['tsinghua', 'schwarzman'], 'Staff training, Schwarzman College'),
      'families': ('heart-handshake', 'Families', 'Want their child ready for AI-era work. 1:1 mentors help.', '1:1 mentorship · parent talks', ['pta'], 'Parent talk, ISB PTA'),
      'career': ('briefcase', 'Career', 'Want an edge for internships and jobs. They ship a live product.', 'Bootcamp', ['lux'], 'Jointly hosted with Lux Scholar'),
      # teacher variant
      'teachers': ('wrench', 'Teachers &amp; tech teams', 'Make the tool your class is missing, on your approved systems.', 'Session · workshop · school-wide', ['tsinghua', 'schwarzman'], 'Staff training, Schwarzman College'),
      'tech': ('monitor-cog', 'Tech teams', 'Training on your approved systems.', 'Planning · sessions', [], ''),
      'leaders': ('building-2', 'School leaders', 'Programs for the whole school community.', 'Planned with your team', ['isb'], 'Student program on campus'),
      'conf': ('mic', 'Conferences', 'Talks and hands-on workshops.', 'Keynote · workshop · panel', ['acamis'], 'Next: ACAMIS workshop'),
      # parent variant
      'workshops': ('smartphone', 'Workshops', 'Rebuild an app, or build a portfolio site.', 'At your child’s school', [], ''),
      'intensive': ('rocket', 'Workshops &amp; intensives', 'Two to five days: launch a real product, then pitch it.', 'At your child’s school', ['isb', 'bodley'], 'Five-day student programs'),
      'mentor': ('route', 'Year-long mentorship', 'One project, 1:1, at their own pace.', 'Weekly check-ins, hybrid', ['isb'], 'ISB alumni continue here'),
      'talks': ('messages-square', 'Parent talks', 'How AI is changing work and college.', 'At your child’s school', ['pta'], 'Parent talk, ISB PTA')},
   formats_k='Formats',
   skills=[('compass', 'Choose a real problem', 'And pitch it in three minutes. (Agency)'), ('search-check', 'Test with real users', 'And judge which version works. (Taste)'), ('badge-check', 'Launch and explain it', 'At a live link, every decision defended. (Craft)')],
   loop='Learners decide. AI builds. Real people judge.', strands_k='Four strands, assessed on every project',
   dk='Whose account is it?', personal='Personal account', school='School-approved platform',
   prow=['Consumer terms', 'No data agreement', 'Not for student data'], srow=['Enterprise agreement', 'Agreed by the school', 'Cleared for student data'],
   cta='Bring Arena to your school.', ctap='Planned with your team, run on your campus. Your teachers keep the materials.',
   hub='Arena School',
 ),
 'cn': dict(
   member='成员计划', anth='初创企业计划', oai='合作伙伴网络', studied='<!-- JJ review: 团队成员来自 (TEAMROW-BRIEF) -->团队成员来自', worked='',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='合作',
   T={'students': ('graduation-cap', '学生', '想学真本事、有作品可展示：做出并上线产品。', '工作坊 · 集训营 · 导师计划', ['isb', 'bodley'], '五天学生项目'),
      'schools': ('school', '教师与学校', '想让老师有信心、用得安全：每人做一个课堂工具。', '分享 · 工作坊 · 全校培训', ['tsinghua', 'schwarzman'], '苏世民书院教职员工培训'),
      'families': ('heart-handshake', '家庭', '希望孩子为AI时代的工作做好准备：一对一导师陪伴。', '一对一导师 · 家长讲座', ['pta'], 'ISB PTA 家长讲座'),
      'career': ('briefcase', '大学与职场', '想在实习和求职中脱颖而出：上线一个真实产品。', '训练营', ['lux'], '与千麓学者联合举办'),
      'teachers': ('wrench', '教师与技术团队', '在学校认可的系统上，为课堂做一个正缺的小工具。', '现场分享 · 工作坊 · 全校培训', ['tsinghua', 'schwarzman'], '苏世民书院教职员工培训'),
      'tech': ('monitor-cog', '技术团队', '在学校认可的系统上开展培训。', '规划 · 培训', [], ''),
      'leaders': ('building-2', '校长与管理层', '服务整个学校社群的项目。', '与贵校团队共同规划', ['isb'], '在校园内开展的学生项目'),
      'conf': ('mic', '会议与活动', '主题演讲与动手工作坊。', '演讲 · 工作坊 · 圆桌', ['acamis'], '即将举行：ACAMIS 工作坊'),
      'workshops': ('smartphone', '动手工作坊', '重做一款应用，或做一个作品集网站。', '在孩子的学校', [], ''),
      'intensive': ('rocket', '工作坊与集训营', '两到五天：做出真实的产品，再路演。', '在孩子的学校', ['isb', 'bodley'], '五天学生项目'),
      'mentor': ('route', '学年导师计划', '一个项目，一对一，按自己的节奏。', '每周例会，线上线下结合', ['isb'], 'ISB 营员在此继续'),
      'talks': ('messages-square', '家长讲座', 'AI如何改变工作与升学。', '在孩子的学校', ['pta'], 'ISB PTA 家长讲座')},
   formats_k='形式',
   skills=[('compass', '选一个真实的问题', '三分钟讲清楚。（主动性）'), ('search-check', '拿给真实用户测试', '判断哪个版本真正好用。（审美）'), ('badge-check', '上线并讲清楚', '发布在公开网址，每个决定都讲得出理由。（匠心）')],
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
 'teacher': dict(file='arena-school-teacher-one-pager', tiles=['teachers', 'leaders', 'conf'],
   en=dict(eyebrow='For teachers and school leaders', h1='AI fluency for the whole staff, <em>inside your school’s rules.</em>'),
   cn=dict(eyebrow='面向教师与学校管理层', h1='全体教职员工的AI素养，<em>始终在学校的规则之内。</em>')),
 'parent': dict(file='arena-school-parent-one-pager', tiles=['intensive', 'mentor', 'talks'],
   en=dict(eyebrow='For families', h1='What your child makes, learns, and keeps <em>at Arena School.</em>'),
   cn=dict(eyebrow='写给家长', h1='孩子在 Arena School <em>做什么、学什么、带走什么。</em>')),
}
STUDIED = [('caltech', 2.65), ('harvard', 5.0), ('brown', 5.6), ('tsinghua-lockup', 4.8), ('isb', 4.6)]   # equal ink area per mark (EDGES-BRIEF), from each file's ink; crest + small-caps marks raised to a legible minimum
WORKED = [('mckinsey', 2.8), ('goldman', 4.07), ('yc', 3.84), ('apple', 4.8), ('microsoft-ai', 3.93), ('deloitte', 2.4), ('kimi-wordmark', 2.95)]

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


# ---------------------------------------------------------------- v4 (ONEPAGER3-BRIEF): three strong sections per variant
INTRO = {
 'general': {'en': 'Run at the International School of Beijing, Bodley Academy in Hong Kong, and Schwarzman College, Tsinghua, by a team from Harvard, Caltech, Tsinghua, McKinsey, Goldman Sachs, and Y Combinator.',
             'cn': '曾在北京顺义国际学校、香港 Bodley Academy 和清华大学苏世民书院开展；团队来自哈佛、加州理工、清华、麦肯锡、高盛和 Y Combinator。'},
 'teacher': {'en': 'Each teacher leaves a session with a working tool for their own class, built on your approved systems. From the team that trained staff at Schwarzman College, Tsinghua.',
             'cn': '每位老师都带着一个能在自己课堂上用的工具离开，全部建在贵校认可的系统上。我们曾为清华大学苏世民书院的教职员工开展培训。'},
 'parent': {'en': 'Arena School teaches students to build and launch real AI products, mentored by a team from Harvard, Caltech, Tsinghua, McKinsey, Goldman Sachs, Y Combinator, Apple, and Microsoft AI.',
            'cn': 'Arena School 教学生用AI做出并上线真实的产品，导师团队来自哈佛、加州理工、清华、麦肯锡、高盛、Y Combinator、苹果和微软AI。'},
}
H1 = {'general': {'en': dict(eyebrow='What is Arena School', h1='Students, teachers, and families <em>build real things with AI.</em>'),
                  'cn': dict(eyebrow='认识 Arena School', h1='学生、老师和家庭，<em>用AI做出真实的东西。</em>')},
      'teacher': {'en': dict(eyebrow='For teachers and school leaders', h1='Every teacher confident with AI, <em>inside your school’s rules.</em>'),
                  'cn': dict(eyebrow='面向教师与学校管理层', h1='让每位老师都能自信地用AI，<em>始终在学校的规则之内。</em>')},
      'parent': {'en': dict(eyebrow='For families', h1='Your child builds and launches <em>a real AI product.</em>'),
                 'cn': dict(eyebrow='写给家长', h1='孩子亲手做出并上线<em>一个真实的AI产品。</em>')}}
CAP = {'en': 'Demo day at the International School of Beijing, 2026', 'cn': '<!-- JJ review: 照片说明 (CAPTION-BRIEF) -->北京顺义国际学校路演日'}
# section titles: (title, one-line dek)
SEC = {
 'en': dict(who=('Who we serve, and why they come', 'Each audience, its reason, and where we have run it.'), teach=('What learners actually do', 'The same three moves in every program.'),
            data=('Student data comes first', 'Before which tool, ask whose account it is.'),
            fl=('Five levels of AI fluency', 'A baseline, then every teacher moves up one level a term.'), move=('One session, one working tool', 'Each teacher brings one task from a class they teach now.'),
            whyt=('Why now', 'Teachers already use AI. Few have been trained.'), whyp=('Why it matters now', 'Students use AI already. Schools rarely teach it.'),
            kids=('What your child builds and learns', 'Concrete skills, on a real product.'), lead=('What it leads to', 'Work to show in college, summer, and internship applications.')),
 'cn': dict(who=('我们服务谁，他们为什么来', '每类对象、他们的理由，以及我们在哪里开展过。'), teach=('学习者实际做什么', '每个项目都是同样的三个动作。'),
            data=('学生数据放在第一位', '先别问用哪个工具，先问是谁的账号。'),
            fl=('AI素养的五个层级', '先做基线评估，每位老师每学期提升一级。'), move=('一次培训，一个能用的工具', '每位老师带来自己正在教的一门课里的一项任务。'),
            whyt=('为什么是现在', '老师已经在用AI，受过培训的却不多。'), whyp=('为什么是现在', '学生已经在用AI，学校却很少教。'),
            kids=('孩子做什么、学什么', '在真实产品上练出的具体能力。'), lead=('这会带来什么', '可以写进大学、暑期项目和实习申请的作品。')),
}
# proof marks normalized to one optical height (mm) inside a 7mm slot; text labels in the same serif, no box
PROOF_H = {'isb': 5.0, 'tsinghua': 4.6, 'pta': 4.8, 'lux': 5.2, 'schwarzman': 4.2}


def header(lang, d):
    t = H1[d][lang]
    return ('<header class="top"><div class="g12 topgrid"><div class="c1-7 top-copy">'
            '<img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" />'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p></div></div>'
            '<figure class="photo"><img src="/photos/isb-2026/pitch-duo-1600.webp" alt="" /><figcaption>%s</figcaption></figure></header>'
            % (t['eyebrow'], t['h1'], INTRO[d][lang], CAP[lang]))


def strip(lang):
    """Bottom credentials: "A member of" on one line; "Team from" with twelve marks on two balanced lines of six equal cells."""
    c = L[lang]
    order = ['caltech', 'harvard', 'brown', 'tsinghua-lockup', 'isb', 'apple', 'mckinsey', 'goldman', 'yc', 'microsoft-ai', 'deloitte', 'kimi-wordmark']
    h = dict(STUDIED + WORKED)
    marks = [(k, h[k]) for k in order]
    cell = lambda k, h: '<span class="lc%s"><img src="/logos/cred/%s.png" alt="" style="height:%smm" /></span>' % (' w2' if k == 'mckinsey' else '', k, h)
    return ('<section class="strip">'
            '<div class="g12 row trow"><span class="c1-3 lab tlabel">%s</span><div class="c4-12 team cols-%d">%s</div></div></section>'
            % (c['studied'], TEAMCOLS, ''.join(cell(k, h) for k, h in marks)))


TEAMCOLS = int(os.environ.get('TEAMCOLS', '6'))   # 6 (2 rows) or 4 (3 rows): the logo grid's column count


def memtop(lang):
    """Slim "A member of" strip under the photo header, as on the homepage: a small centred label and two marks."""
    c = L[lang]
    return ('<section class="memtop g12"><span class="c1-3 lab">%s</span><div class="c4-12 mt">'
            '<span class="m"><img src="/logos/partners/anthropic.svg" alt="Anthropic" style="height:2.6mm" /><em>%s</em></span>'
            '<span class="m"><img src="/logos/partners/openai.svg" alt="OpenAI" style="height:4.8mm" /><em>%s</em></span></div></section>'
            % (c['member'], c['anth'], c['oai']))


def shead(n, key, lang, span='c1-12'):
    t, d = SEC[lang][key]
    return ('<div class="sh %s"><span class="num">%02d</span><div class="sht"><h2>%s</h2><p>%s</p></div></div>' % (span, n, t, d))


def sec(n, key, lang, inner, cls=''):
    return '<section class="sec %s"><div class="g12">%s</div>%s</section>' % (cls, shead(n, key, lang), inner)


def mark(k):
    f, v = LOGO[k]
    return ('<img src="%s" alt="" style="height:%smm" />' % (f, PROOF_H[k])) if f else '<span class="wordmark">%s</span>' % v


FACT = {'workshops': {'en': ('2 days', 'At your school, no coding needed'), 'cn': ('两天', '在贵校进行，无需编程基础')},
        'tech': {'en': ('Your systems', 'Locked down is fine'), 'cn': ('贵校的系统', '严格管控的环境也可以')}}


def tiles(lang, keys):
    c = L[lang]
    spans = ['c1-4', 'c5-8', 'c9-12'] if len(keys) == 3 else ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    out = []
    for s, k in zip(spans, keys):
        icon, label, line, fm, marks, cap = c['T'][k]
        if marks:
            pr = '<div class="proof"><div class="marks">%s</div><span class="cap">%s</span></div>' % (''.join(mark(m) for m in marks), cap)
        elif k in FACT:   # no verified past run with a logo: a site fact in the same slot (never an invented proof)
            pr = '<div class="proof"><div class="marks"><span class="fact">%s</span></div><span class="cap">%s</span></div>' % FACT[k][lang]
        else:
            pr = '<div class="proof empty"><div class="marks"></div><span class="cap">&nbsp;</span></div>'
        out.append('<div class="%s card tile"><div class="th">%s<b class="nm">%s</b></div><span class="out">%s</span><span class="fm">%s</span>%s</div>' % (s, ic(icon, 'ic big'), label, line, fm, pr))
    return '<div class="g12 rrow">%s</div>' % ''.join(out)


def teach(lang, wide=True):
    c, t = L[lang], A.T['cn' if lang == 'cn' else 'en']
    dom = ['target', 'search-check', 'hammer', 'messages-square']
    skills = ''.join('<div class="%s sk"><div class="skh">%s<b>%s</b></div><span>%s</span></div>' % (sp, ic(i), a, b)
                     for sp, (i, a, b) in zip(['c4-6', 'c7-9', 'c10-12'], c['skills']))
    strands = ''.join('<div class="%s st">%s<span>%s</span></div>' % (sp, ic(dom[k]), d)
                      for k, (sp, d) in enumerate(zip(['c4-6', 'c7-9', 'c10-12', 'c4-6'], t['domains'])))
    core = '由学习者<br><em>做决定</em>' if lang == 'cn' else 'The<br>learner<br><em>decides</em>'
    sep = '、' if lang == 'cn' else ' · '
    line = '<p class="c4-12 strline"><b>%s</b>%s</p>' % (c['strands_k'] + ('：' if lang == 'cn' else ': '), sep.join(t['domains']))
    return ('<div class="g12 teach"><div class="c1-3 wheel">%s<span class="core">%s</span></div><div class="c4-12 loopc"><p class="loop">%s</p></div>%s%s</div>'
            % (W.svg('cn' if lang == 'cn' else 'en'), core, c['loop'], skills, line))


def statband(lang, ids):
    import depth as D
    cn = lang == 'cn'
    cells = []
    for sp, k in zip(['c1-4', 'c5-8', 'c9-12'], ids):
        st = D.STATS[k]
        unit = (' ' + st['unit']['cn' if cn else 'en']) if st['unit'] else ''
        n = '一半' if cn and st['n'] == '1 in 2' else st['n']
        cells.append('<div class="%s stat"><b>%s%s</b><span>%s</span><small>%s</small></div>' % (sp, n, unit, st['cn' if cn else 'en'], st['src']['cn' if cn else 'en']))
    return '<div class="g12 rrow stats">%s</div>' % ''.join(cells)


def stairs(items, descs=True):
    steps = ''.join('<li style="--s:%d"><i>%d</i><b>%s</b></li>' % (i, i + 1, n) for i, (n, _) in enumerate(items))
    below = ''.join('<span>%s</span>' % d for _, d in items) if descs else ''
    return '<div class="stairs-wrap"><ol class="stairs">%s</ol><div class="stairs-d">%s</div></div>' % (steps, below)


def row4(items, cls='row4'):
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    return '<div class="g12 %s">%s</div>' % (cls, ''.join('<div class="%s it">%s<div><b>%s</b><span>%s</span></div></div>' % (s, ic(i), a, b) for s, (i, a, b) in zip(spans, items)))


def account(lang):
    c = L[lang]
    col = lambda title, rs, ok: ('<div class="acc %s"><div class="acch">%s<b>%s</b></div><ul>%s</ul></div>'
                                 % ('ok' if ok else 'no', ic('school' if ok else 'user-round', 'ic big'), title, ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs)))
    return '<div class="pair">%s<span class="vs">vs</span>%s</div>' % (col(c['personal'], c['prow'], False), col(c['school'], c['srow'], True))


def commits(lang, pick):
    d = DS.C['cn' if lang == 'cn' else 'en']
    return '<ul class="commit">%s</ul>' % ''.join('<li>%s<b>%s</b></li>' % (ic(d['commit'][k][0]), d['commit'][k][1]) for k in pick)


def data(lang, pick=(0, 1, 2, 4)):
    """Account cards on columns 1-3 and 4-6 (vs badge centred in the gutter), commitments on 7-12, tops and bottoms aligned."""
    c = L[lang]
    col = lambda span, title, rs, ok: ('<div class="%s acc %s"><div class="acch">%s<b>%s</b></div><ul>%s</ul>%s</div>'
                                       % (span, 'ok' if ok else 'no', ic('school' if ok else 'user-round', 'ic big'), title,
                                          ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs), ''))
    return ('<div class="g12 data">%s%s<div class="c7-12">%s</div></div>'
            % (col('c1-3', c['personal'], c['prow'], False), col('c4-6', c['school'], c['srow'], True), commits(lang, pick)))


PCTA = {'en': ('Two ways to start.', 'Ask your child’s school to bring Arena, or enroll in the Year-Long Project Mentorship directly.'),
        'cn': ('两种开始方式。', '请孩子的学校邀请 Arena，或直接报名学年项目导师计划。')}


def footer(lang, doc='general'):
    c = L[lang]
    h, p = PCTA[lang] if doc == 'parent' else (c['cta'], c['ctap'])
    return ('<footer class="cta g12"><div class="c1-8"><h2>%s</h2><p>%s</p></div><div class="c9-12 contact"><b>%s</b><span>%s</span></div></footer>'
            % (h, p, c['mail'], c['web']))


def general(lang, d):
    return (sec(1, 'who', lang, tiles(lang, DOCS['general']['tiles'])) + sec(2, 'teach', lang, teach(lang)) + sec(3, 'data', lang, data(lang, (0, 1, 2))))


def teacher(lang, d):
    f = FL.C['cn' if lang == 'cn' else 'en']
    x = X[lang]
    move = '<div class="g12 rrow">%s</div>' % ''.join('<div class="c%d-%d card step"><div class="sthead"><i>%d</i>%s</div><b class="nm">%s</b><span class="out">%s</span></div>'
                                                       % (1 + 3 * k, 3 + 3 * k, k + 1, ic(i, 'ic big'), a, b) for k, (i, a, b) in enumerate(x['move']))
    return (sec(1, 'whyt', lang, statband(lang, ['rand-use', 'rand-districts', 'gallup-hours'])) +
            sec(2, 'fl', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % stairs(f['levels'], False) +
                '<div class="g12 pk"><span class="c1-12 k">%s</span></div>' % SEC[lang]['move'][0] + move) +
            sec(3, 'data', lang, data(lang, (0, 1, 2))))


PX = {
 'en': dict(practical=[('hammer', 'Building with AI', 'Directing AI coding tools, then testing the results.'), ('users', 'Talking to users', 'Interviewing the people they want to help.'),
                       ('mic', 'Pitching', 'Presenting to a panel, and answering questions.'), ('search-check', 'Research and judgment', 'Checking sources, including AI output.')],
            keep=[('rocket', 'A live product', 'At its own link, with their name.'), ('file-text', 'A documented record', 'To describe in an application.'),
                  ('users', 'People who know their work', 'Mentors and reviewers.'), ('mic', 'Experience presenting it', 'To people who ask hard questions.')],
            proof=[(mark('isb'), 'Students built working apps with AI and presented them to judges from Harvard, Stanford, Y Combinator, and AI labs.'), ('<span class="wordmark">Bodley Academy</span>', 'A student launched a sign-language-to-speech app in five days.')],
            prac_k='Practical skills', keep_k='What they keep, for college, summer, and internship applications', note='Admissions decisions rest with each university; we do not promise an outcome.'),
 'cn': dict(practical=[('hammer', '用AI做产品', '指挥AI编程工具，再亲自测试结果。'), ('users', '访谈用户', '访谈自己想帮助的人。'),
                       ('mic', '路演', '向评审团展示，并回答提问。'), ('search-check', '研究与判断', '核查资料来源，包括AI的输出。')],
            keep=[('rocket', '一个上线的产品', '在自己的网址上，署着自己的名字。'), ('file-text', '有据可查的成果记录', '可以写进申请材料。'),
                  ('users', '了解他作品的人', '导师和评审。'), ('mic', '公开展示的经验', '面对尖锐的提问。')],
            proof=[(mark('isb'), '学生借助AI做出可用的应用，并向来自哈佛、斯坦福、Y Combinator 和AI实验室的评委展示。'), ('<span class="wordmark">Bodley Academy</span>', '一名学生在五天里上线了一款手语转语音的应用。')],
            prac_k='实用技能', keep_k='带走什么：可用于大学、暑期项目和实习申请', note='录取的决定权在每所大学自己手里，我们不对结果作任何承诺。'),
}


def parent(lang, d):
    x, px, c = X[lang], PX[lang], L[lang]
    build = '<div class="g12 rrow">%s</div>' % ''.join('<div class="%s sk3"><div class="th">%s<b class="nm">%s</b></div><span class="out">%s</span></div>' % (sp, ic(i, 'ic big'), a, b)
                                                        for sp, (i, a, b) in zip(['c1-4', 'c5-8', 'c9-12'], c['skills']))
    prac = '<div class="g12 prac">%s</div>' % ''.join('<div class="%s pi">%s<b>%s</b></div>' % (sp, ic(i), a) for sp, (i, a, _) in zip(['c1-3', 'c4-6', 'c7-9', 'c10-12'], px['practical']))
    keep = '<div class="g12 prac">%s</div>' % ''.join('<div class="%s pi">%s<b>%s</b></div>' % (sp, ic(i), a) for sp, (i, a, _) in zip(['c1-3', 'c4-6', 'c7-9', 'c10-12'], px['keep']))
    proof = '<div class="g12 rrow">%s</div>' % ''.join('<div class="%s pf"><div class="marks">%s</div><span>%s</span></div>' % (sp, mk, t) for sp, (mk, t) in zip(['c1-6', 'c7-12'], px['proof']))
    return (sec(1, 'whyp', lang, statband(lang, ['rand-students', 'rand-students-use', 'rand-parents'])) +
            sec(2, 'kids', lang, build + '<div class="g12 pk"><span class="c1-12 k">%s</span></div>' % px['prac_k'] + prac) +
            sec(3, 'lead', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % stairs(list(zip(x['ladder'], x['ladder_d'])), False) +
                '<div class="g12 keepk"><span class="c1-12 k">%s</span></div>' % px['keep_k'] + keep + proof +
                '<div class="g12"><p class="c1-12 note">%s</p></div>' % px['note']))


BODY = {'general': general, 'teacher': teacher, 'parent': parent}
SPANS = '\n'.join('.c%d-%d { grid-column: %d / %d; }' % (a, b, a, b + 1) for a in range(1, 13) for b in range(a, 13))


def page(doc, lang, d):
    cn = lang == 'cn'
    jj = '<!-- JJ review: %s one-pager CN copy (ONEPAGER3-BRIEF, Oct 17, 2026) -->\n' % doc if cn else ''
    fonts = '<link rel="stylesheet" href="/fonts/gf.css" />' + ('<link rel="stylesheet" href="/fonts/zh/zh.css?v=2" />' if cn else '')
    serif = "'Newsreader', 'Arena Serif SC', 'Songti SC', 'Noto Serif SC', Georgia, serif" if cn else "'Newsreader', Georgia, serif"
    root = re.search(r'(?s):root\s*\{.*?\n\}', open(os.path.join(ROOT, 'css', 'pro.css'), encoding='utf-8').read()).group(0)
    wcss = '\n'.join(l for l in open(os.path.join(ROOT, 'css', 'approach.css'), encoding='utf-8').read().splitlines() if l.startswith('.apw'))
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8" />\n<title>Arena School one-pager</title>\n%s%s\n<style>\n%s\n%s\n%s\n</style>\n</head>\n<body>\n'
            '<main class="op %s dir-%s">\n%s\n%s\n<div class="body">%s</div>\n%s\n%s\n</main>\n</body>\n</html>\n'
            % ('zh-CN' if cn else 'en', jj, fonts, root, wcss, CSS.replace('SERIF', serif), doc, d, header(lang, doc), memtop(lang), BODY[doc](lang, d), strip(lang), footer(lang, doc)))


CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Geist', 'PingFang SC', system-ui, sans-serif; color: #1E2740; font-size: 8.2pt; line-height: 1.4; }
.op { width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; }
.op > * { flex-shrink: 0; }
.g12 { display: grid; column-gap: 4mm; grid-template-columns: repeat(12, minmax(0, 1fr)); padding: 0 10mm; }
SPANS
h1, h2, .nm, .loop { font-family: SERIF; font-weight: 500; color: var(--pro-ink); margin: 0; }
em { font-style: italic; }
.ic { width: 4.4mm; height: 4.4mm; color: var(--pro-action); flex: none; } .ic.big { width: 6.2mm; height: 6.2mm; }
.k, .lab, .eyebrow { font: 600 7.2pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4A5578; }
:lang(zh) .k, :lang(zh) .lab, :lang(zh) .eyebrow { letter-spacing: .04em; font-size: 7.6pt; }
/* header: the v2 band (navy, wordmark, large headline with italic accent, intro, demo-day photo right) */
.top { position: relative; background: #0B1A4A; color: #fff; height: 52mm; overflow: hidden; }
.topgrid { position: relative; z-index: 2; height: 100%; align-items: center; }
.top-copy { padding: 0 4mm 0 0; }
.wm { height: 5mm; width: auto; display: block; margin-bottom: 3.4mm; }
.top .eyebrow { color: #C9D6F2; }
.top h1 { color: #fff; font-size: 19pt; line-height: 1.1; margin: 1.6mm 0 2.6mm; letter-spacing: -.006em; }
:lang(zh) .top h1 { font-size: 18.5pt; line-height: 1.26; }
.general:lang(en) .top h1, .general .top h1:lang(en) { font-size: 17.5pt; }
.top h1 em { color: #C9D6F2; white-space: nowrap; }
.lede { margin: 0; font-size: 8.6pt; line-height: 1.5; color: rgba(255,255,255,.86); max-width: 112mm; }
.photo { position: absolute; top: 0; right: 0; bottom: 0; left: 92mm; margin: 0; }
/* a soft left-to-right fade from the navy into the photo (as on the site's hero); the headline area stays solid navy */
.photo::before { content: ''; position: absolute; top: 0; bottom: 0; right: 0; left: -1mm; z-index: 1; background: linear-gradient(90deg, #0B1A4A 0, #0B1A4A 18%, rgba(11,26,74,.6) 30%, rgba(11,26,74,0) 44%); }
.photo img { width: 100%; height: 100%; object-fit: cover; object-position: 68% 30%; display: block;
  }
.photo::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 14mm; background: linear-gradient(180deg, rgba(11,26,74,0), rgba(11,26,74,.78)); }
.photo figcaption { position: absolute; z-index: 2; right: 10mm; bottom: 3.4mm; font-size: 7pt; color: #fff; white-space: nowrap; text-shadow: 0 1px 4px rgba(8,15,38,.85); }
/* body: three sections, equal gaps */
.body { flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 2mm 0; }
/* section header: a navy number block, a serif title, a one-line dek */
.sh { display: flex; align-items: center; gap: 3.4mm; margin-bottom: 3mm; }
.num { flex: none; width: 9mm; height: 9mm; display: grid; place-items: center; background: #0B1A4A; color: #fff; font: 400 12pt/1 SERIF; border-radius: 1.2mm; }
.sht h2 { font-size: 14.5pt; line-height: 1.1; }
.sht p { margin: .8mm 0 0; font-size: 8.4pt; color: #4A5578; }
/* cards */
.card { border: 1px solid var(--pro-line); border-radius: 2mm; padding: 3mm 3.2mm; background: #fff; display: flex; flex-direction: column; gap: 1.6mm; min-width: 0; }
.nm { display: block; font-size: 11.5pt; line-height: 1.2; margin-top: 1mm; }
.out { display: block; font-size: 8.4pt; line-height: 1.4; color: #3A4466; }
.fm { display: block; font: 600 7.6pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-action); }
.rrow { align-items: stretch; }
.tile .proof { margin-top: auto; height: 17mm; align-content: start; padding-top: 2.4mm; border-top: 1px solid var(--pro-line); display: grid; gap: 1.4mm; }
.tile .proof.empty { border-top-color: transparent; }
.marks { height: 6mm; display: flex; align-items: center; gap: 2.6mm; overflow: visible; }
.marks img { width: auto; display: block; filter: grayscale(1) contrast(1.1); opacity: .85; }
.wordmark { font: 600 7.6pt/1.05 SERIF; color: #3A4466; white-space: normal; max-width: 15mm; }
.cap { font-size: 7.4pt; color: #4A5578; }
.fact { font: 500 12pt/1 SERIF; color: var(--pro-ink); }
/* tile and skill heads: icon inline with the name */
.th { display: flex; align-items: center; gap: 2.2mm; } .th .nm { margin: 0; }
.skh { display: flex; align-items: center; gap: 1.6mm; }
/* wheel at print size: ring labels would be under 7pt, so only the core text shows (strands are listed beside) */
.wheel .apw-out-t, .wheel .apw-mid-t { display: none; }
/* how we teach */
.teach { row-gap: 3mm; align-items: start; } .teach .wheel { grid-row: 1 / span 3; position: relative; align-self: center; }
.strline { margin: 0; font-size: 7.6pt; color: #3A4466; padding-top: 2mm; border-top: 1px solid var(--pro-line); } .strline b { font-weight: 600; color: var(--pro-ink); } .teach .sk { align-self: start; }
.wheel .apw-core-t { display: none; }
.wheel .core { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-align: center; font: 500 7pt/1.12 SERIF; color: #fff; width: 38%; }
.wheel .core em { color: #C9D6F2; }
.strow { margin-top: 3mm; row-gap: 1.4mm; align-items: center; } .strow .k { grid-row: 1 / span 2; align-self: center; }
:lang(zh) .wheel .apw { max-width: 38mm; }
.strow .st { display: flex; align-items: center; gap: 2mm; padding-top: 1.8mm; border-top: 1px solid var(--pro-line); font-size: 8.6pt; font-weight: 500; color: var(--pro-ink); }
.wheel .apw { width: 100%; max-width: 38mm; height: auto; display: block; margin: 0 auto; }
.loop { font-size: 13pt; line-height: 1.22; margin: 0; }
.skills { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-bottom: 3.4mm; }
.sk { display: grid; gap: 1mm; padding-top: 2.4mm; border-top: 2px solid var(--pro-action); }
.sk b { font: 600 10pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); } .sk span { font-size: 8.4pt; color: #3A4466; }
.strands { list-style: none; margin: 1.6mm 0 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm 4mm; }
.strands li { display: flex; align-items: center; gap: 2mm; font-size: 8.6pt; font-weight: 500; color: var(--pro-ink); }
/* staircase: steps carry the number and name; descriptions sit below, one column each */
.stairs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; align-items: end; }
.stairs li { height: calc(15mm + var(--s) * 3mm); border-top: 2.4px solid var(--pro-action); background: color-mix(in srgb, var(--pro-action) calc(7% + var(--s) * 5%), #fff);
  padding: 2.4mm 2.6mm; display: flex; flex-direction: column; justify-content: flex-start; border-radius: 0 0 1.2mm 1.2mm; }
.stairs li > * { flex: none; }
.stairs i { font: 400 13pt/1 SERIF; color: var(--pro-action); font-style: normal; }
.stairs b { font: 600 9pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); margin-top: 1mm; }
.stairs-d { display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; margin-top: 2.4mm; }
.stairs-d span { font-size: 8pt; line-height: 1.38; color: #3A4466; padding: 0 2.6mm; }
.row4 { margin-top: 3.4mm; }
.row4 .it { display: flex; gap: 2.4mm; align-items: flex-start; padding-top: 2.6mm; border-top: 1px solid var(--pro-line); }
.row4 b { display: block; font: 600 8.8pt/1.25 'Geist', system-ui, sans-serif; color: var(--pro-ink); } .row4 span { font-size: 8pt; color: #3A4466; }
.step .sthead { display: flex; align-items: center; justify-content: space-between; } .step i { font: 400 15pt/1 SERIF; color: var(--pro-action); font-style: normal; }
/* data: account pair + commitments */
.data { align-items: stretch; } .data .acc { position: relative; } .data .vs { position: absolute; right: -2mm; top: 50%; transform: translate(50%, -50%); z-index: 2; background: #fff; border: 1px solid var(--pro-line-2); border-radius: 50%; width: 7mm; height: 7mm; display: grid; place-items: center; font-size: 7pt; }
.data .c7-12 { display: flex; } .data .commit { flex: 1; display: grid; grid-auto-rows: 1fr; } .data .commit li { padding: 0; }
.pair { display: grid; grid-template-columns: 1fr auto 1fr; gap: 2.4mm; align-items: stretch; }
.vs { align-self: center; font: 600 7.4pt/1 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #4A5578; }
.acc { border: 1px solid var(--pro-line); border-radius: 2mm; padding: 3mm; } .acc.ok { border-color: #0B1A4A; box-shadow: inset 0 3px 0 var(--pro-action); }
.acch { display: flex; align-items: center; gap: 2mm; margin-bottom: 2mm; } .acch b { font: 600 9.4pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
.acc.no .acch .ic { color: #4A5578; }
.acc ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.2mm; } .acc li { display: flex; gap: 1.4mm; align-items: center; font-size: 8pt; color: #3A4466; white-space: nowrap; }
.mk { width: 3.6mm; height: 3.6mm; flex: none; } .acc.no .mk { color: #9A3B2E; } .acc.ok .mk { color: var(--pro-action); }
.commit { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }
.commit li { display: flex; align-items: center; gap: 2.6mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); }
.commit li:last-child { border-bottom: 1px solid var(--pro-line); }
:lang(zh) .commit li { padding: 1.7mm 0; }
.commit b { font: 600 9pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
/* "A member of" under the header: centred label, two marks with captions */
.memtop { align-items: center; padding-top: 2.6mm; padding-bottom: 2.6mm; border-bottom: 1px solid var(--pro-line); }
.memtop .mt { display: flex; align-items: center; justify-content: flex-end; gap: 9mm; }
.memtop .m { display: inline-flex; align-items: center; gap: 2mm; white-space: nowrap; } .memtop .m em { font-style: normal; font-size: 7.4pt; color: #4A5578; }
/* bottom credentials strip */
.strip { padding: 2.4mm 0; border-top: 1px solid var(--pro-line); display: grid; gap: 2.2mm; background: #F6F7FA; }
.strip .row { align-items: center; }
.strip .lab { white-space: nowrap; }
.logos { display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; min-width: 0; }
/* one 6-column grid for both credential rows: every logo centred in its column */
.six { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); row-gap: 1.4mm; align-items: center; }
.six .lc { display: flex; align-items: center; justify-content: center; height: 6.2mm; min-width: 0; }
/* columns stay aligned row to row; the outer columns sit on the content edges */
.six.member { gap: 0; column-gap: 0; justify-content: stretch; }
.six .m { flex-direction: column; height: auto; gap: .8mm; } .six .m em { font-style: normal; font-size: 7pt; color: #4A5578; white-space: nowrap; }
.team img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
/* one greyscale darkness for every mark */
.team img, .team img[src*='/brown.'], .team img[src*='/harvard.'] { filter: grayscale(1) brightness(0); opacity: .72; }
.trow { align-items: center; } .tlabel { align-self: center; }
/* the logo block: equal cells, every mark centred in its cell, the block ends on the right content edge */
.team { display: grid; row-gap: 1.8mm; column-gap: 0; align-items: center; }
.team.cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); } .team.cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.team .lc { display: flex; align-items: center; justify-content: center; height: 6.2mm; min-width: 0; }
.logos img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
.logos img[src*='/brown.'], .logos img[src*='/harvard.'] { filter: grayscale(1) contrast(1.6) brightness(.72); opacity: 1; }
.member { justify-content: flex-start; gap: 12mm; } .member img { filter: none; opacity: 1; }
.m { display: inline-flex; align-items: center; gap: 2mm; white-space: nowrap; } .m em { font-style: normal; font-size: 7.6pt; color: #4A5578; }
.sk3 { display: flex; flex-direction: column; gap: 1.2mm; padding-top: 2.4mm; border-top: 2px solid var(--pro-action); }
.pk { margin-top: 3.4mm; } .pk .k { display: block; margin-bottom: 1.4mm; }
.prac .pi { display: flex; align-items: center; gap: 2mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); border-bottom: 1px solid var(--pro-line); } .prac b { font: 600 8.2pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); white-space: nowrap; }
.parent .stairs li { height: calc(15mm + var(--s) * 2mm); }
.dir-B.parent .sec { padding: 2.3mm 0; }
.keepk { margin-top: 3.4mm; }
.pf { display: flex; align-items: center; gap: 3mm; margin-top: 2.4mm; padding: 2mm 2.4mm; background: #F3F5FA; border-radius: 1.6mm; } .pf .marks { flex: none; height: 6mm; } .pf span { font-size: 7.8pt; line-height: 1.35; color: #3A4466; } .keepk .k { margin-bottom: 1.6mm; } .keepk .k { display: block; } .keep { margin-top: 1.4mm; } .note { margin: 2.4mm 0 0; padding: 0; font-size: 7.2pt; color: #4A5578; }
/* why-now stats: big figure, one line, source in small type */
.stats .stat { display: flex; flex-direction: column; gap: 1mm; padding-top: 2.2mm; border-top: 2px solid var(--pro-action); }
.stats .stat b { font: 400 18pt/1 SERIF; color: var(--pro-ink); }
.stats .stat span { font-size: 7.8pt; line-height: 1.35; color: #3A4466; }
.stats .stat small { margin-top: auto; font-size: 7pt; line-height: 1.3; color: #4A5578; }
/* closing band */
.cta { background: #0B1A4A; color: #fff; padding-top: 4.4mm; padding-bottom: 4.4mm; align-items: center; }
.cta h2 { color: #fff; font-size: 13pt; } .cta p { margin: 1mm 0 0; font-size: 8.2pt; color: rgba(255,255,255,.84); }
.cta .contact { text-align: right; display: grid; gap: .8mm; font-size: 9pt; } .cta .contact span { color: #C9D6F2; }
/* direction B: alternating full-bleed bands, header without the block */
.dir-B .body { padding: 0; justify-content: stretch; }
.dir-B .sec { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; padding: 3mm 0; }
.dir-B .sec:nth-child(2) { background: #F3F5FA; }
.dir-B .num { background: none; color: var(--pro-action); width: auto; height: auto; font-size: 22pt; border-right: 1px solid var(--pro-line-2); padding-right: 3.4mm; border-radius: 0; }
/* direction C: magazine halves */
.halves { align-items: start; } .g6h .sh { margin-bottom: 3mm; }
.teach.narrow .wheel .apw { max-width: 34mm; } .teach.narrow { display: grid; grid-template-columns: 34mm 1fr; column-gap: 4mm; align-items: center; }
.teach.narrow .skills { grid-column: 1 / -1; margin-top: 3mm; } .teach.narrow .loop { font-size: 12pt; margin: 0; }
.halves .pair { margin-bottom: 3mm; }
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
    const bd = document.querySelector('.body'); const inner = Math.round([...bd.children].reduce((a, k) => a + k.scrollHeight, 0) + parseFloat(getComputedStyle(bd).paddingTop) + parseFloat(getComputedStyle(bd).paddingBottom) - bd.clientHeight);
    const secOver = [...document.querySelectorAll('.sec')].map(x => x.scrollHeight - x.clientHeight).filter(v => v > 1);
    const g = document.querySelector('.g12'), gr = g.getBoundingClientRect(), cs = getComputedStyle(g);
    const cols = cs.gridTemplateColumns.split(' ').map(parseFloat), gap = parseFloat(cs.columnGap), pl = parseFloat(cs.paddingLeft);
    const starts = [], ends = []; let x = gr.left + pl; cols.forEach(w => { starts.push(x); ends.push(x + w); x += w + gap; });
    const bad = [];
    document.querySelectorAll('.g12 > *').forEach(c => { const r = c.getBoundingClientRect(); if (!r.width) return;
      if (!starts.some(s => Math.abs(s - r.left) < .6) || !ends.some(e => Math.abs(e - r.right) < .6)) bad.push((c.className || c.tagName) + ' ' + r.left.toFixed(1) + '-' + r.right.toFixed(1)); });
    const uneven = [];
    document.querySelectorAll('.rrow').forEach(row => { const hs = [...row.children].map(c => Math.round(c.getBoundingClientRect().height)); if (Math.max(...hs) - Math.min(...hs) > 1) uneven.push(hs.join('/')); });
    document.querySelectorAll('.rrow').forEach(row => { const th = [...row.querySelectorAll('.th')].map(t => Math.round(t.getBoundingClientRect().height)); if (th.length && Math.max(...th) - Math.min(...th) > 1) uneven.push('titles ' + th.join('/')); });
    const stepBad = []; document.querySelectorAll('.stairs li').forEach(li => { const r = li.getBoundingClientRect(), pad = parseFloat(getComputedStyle(li).paddingBottom); [...li.children].forEach(c => { if (c.getBoundingClientRect().bottom > r.bottom - pad + .5) stepBad.push(c.textContent); }); });
    const stepTops = [...new Set([...document.querySelectorAll('.stairs li i')].map(i => Math.round((i.getBoundingClientRect().top - i.parentElement.getBoundingClientRect().top) * 10) / 10))];
    let svgMin = 99; document.querySelectorAll('svg.apw text').forEach(t => { if (getComputedStyle(t).display === 'none') return; const sv = t.ownerSVGElement; const k = sv.getBoundingClientRect().width / sv.viewBox.baseVal.width; svgMin = Math.min(svgMin, parseFloat(t.getAttribute('font-size') || getComputedStyle(t).fontSize) * k); });
    const hb = document.querySelector('.top').getBoundingClientRect(), hc = document.querySelector('.top-copy').getBoundingClientRect();
    if (hc.top < hb.top + 8 || hc.bottom > hb.bottom - 8) stepBad.push('header copy outside band');
    document.querySelectorAll('.rrow').forEach(row => { const pt = [...row.querySelectorAll('.tile .proof')].map(t => Math.round(t.getBoundingClientRect().top)); if (pt.length && Math.max(...pt) - Math.min(...pt) > 1) uneven.push('proof ' + pt.join('/')); });
    const cents = sel => [...document.querySelectorAll(sel)].map(e => { const r = e.getBoundingClientRect(); return Math.round(r.left + r.width / 2); });
    const tc = cents('.team .lc'), mc = cents('.member .lc');
    const nc = getComputedStyle(document.querySelector('.team')).gridTemplateColumns.split(' ').length;
    for (let i = nc; i < tc.length; i++) if (Math.abs(tc[i] - tc[i - nc]) > 1) uneven.push('team col ' + i);
    document.querySelectorAll('.acc li').forEach(li => { if (li.getBoundingClientRect().height > 16) uneven.push('acc wrap: ' + li.textContent); });
    const fc = document.querySelector('.photo figcaption'); if (fc.getBoundingClientRect().height > 14) stepBad.push('caption wraps');
    const g0 = document.querySelector('.body .g12'), g0r = g0.getBoundingClientRect(), gcs = getComputedStyle(g0);
    const L0 = g0r.left + parseFloat(gcs.paddingLeft), R0 = g0r.right - parseFloat(gcs.paddingRight);
    const edges = [];
    const lefts = ['.top-copy', '.memtop .lab', '.sh', '.rrow > :first-child', '.data > :first-child', '.tlabel', '.cta > :first-child'];
    const rights = ['.memtop .mt > :last-child', '.rrow > :last-child', '.data > :last-child', '.team', '.cta .contact', '.stairs-wrap', '.row4 > :last-child'];
    lefts.forEach(sel => document.querySelectorAll(sel).forEach(e => { const x = e.getBoundingClientRect().left; if (Math.abs(x - L0) > 1) edges.push('L ' + sel + ' ' + Math.round(x - L0)); }));
    rights.forEach(sel => document.querySelectorAll(sel).forEach(e => { const x = e.getBoundingClientRect().right; if (Math.abs(x - R0) > 1) edges.push('R ' + sel + ' ' + Math.round(x - R0)); }));
    const tops = []; document.querySelectorAll('.sh').forEach(d => tops.push(Math.round(d.getBoundingClientRect().left)));
    let min = 99; document.querySelectorAll('.op *').forEach(e => { if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg')) min = Math.min(min, parseFloat(getComputedStyle(e).fontSize)); });
    const clipped = []; document.querySelectorAll('.marks, .logos, .team .tl, .prac .pi, .memtop .mt').forEach(l => { const p = l.closest('.card, .row, .prac, .memtop, .pf'); const pr = p.getBoundingClientRect(); [...l.children].forEach(c => { const r = c.getBoundingClientRect(); if (r.right > pr.right - 1 || r.left < pr.left) clipped.push(c.textContent || c.getAttribute('src')); }); });
    const wrapped = []; document.querySelectorAll('.logos, .marks').forEach(l => { const ys = [...l.children].map(c => Math.round(c.getBoundingClientRect().top + c.getBoundingClientRect().height / 2)); if (Math.max(...ys) - Math.min(...ys) > 4) wrapped.push(l.className); });
    return { over: Math.max(over, inner), edges, stepBad, stepTops, svgPt: +(svgMin * .75).toFixed(2), secOver, clipped, nbad: bad.length, bad: bad.slice(0, 4), uneven, shLeft: [...new Set(tops)], minPt: +(min * .75).toFixed(2), wrapped,
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
    ok = not r['edges'] and not r['stepBad'] and len(r['stepTops']) <= 1 and r['svgPt'] >= 6.95 and not r['secOver'] and not r['clipped'] and pages == '1' and r['over'] <= 1 and r['nbad'] == 0 and not r['uneven'] and r['minPt'] >= 6.95 and not r['wrapped'] and len(r['shLeft']) <= 1
    print('%-40s edges %s | steps %s tops %s | svg %spt | clipped %s | pages %s | overflow %spx | off-grid %d %s | uneven %s | header lefts %s | logo rows wrapped %s | min %spt | %s'
          % (name, r['edges'], r['stepBad'], r['stepTops'], r['svgPt'], r['clipped'], pages, r['over'], r['nbad'], r['bad'][:2], r['uneven'], r['shLeft'], r['wrapped'], r['minPt'], 'OK' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = sys.argv[sys.argv.index('--dir') + 1] if '--dir' in sys.argv else 'B'
    args = [a for a in args if a != opt]
    pngdir = sys.argv[sys.argv.index('--png') + 1] if '--png' in sys.argv else None
    if pngdir:
        args = [a for a in args if a != pngdir]
    docs = args or list(DOCS)
    fails = [d + '-' + l for d in docs for l in ('en', 'cn') if not build(d, l, opt, pngdir)]
    if fails:
        sys.exit('FAILED: ' + ', '.join(fails))
