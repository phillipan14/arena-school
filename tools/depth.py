"""Depth sections for audience and program pages (DEPTH-BRIEF, Oct 16, 2026), EN and CN.

Per page, between markers, idempotent:
  <!-- depth:a -->  right after the hero: problems -> how Arena answers each (ds-ps), then what the research says (ds-stats)
  <!-- depth:b -->  replaces the thin one-line proof section: case studies from real Arena work (ds-cases) + tools (ds-tools)
  FAQ items appended to the page's FAQ list (marked data-depth).
Only real facts: problems and answers restate what the page and its sources already say; stats come from STATS
(each opened and quoted in STATS-SOURCES.md); cases describe only what existing pages state. No em dashes.
CN is marked for JJ review. Components: css/ds.css. Log of design rounds: DEPTH-LOG.md.
  python3 tools/depth.py PAGE [--check]        pages: teachers, technology, ...
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']


def ic(name):
    return ('<svg class="ds-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % ICONS[name])


STATS = {
    'gallup-hours': dict(
        n='5.9', unit=dict(en='hours', cn='小时'),
        en='a week saved, by their own estimate, among teachers who use AI at least weekly: about six weeks over a school year.',
        cn='每周至少使用一次AI的教师自己估算的每周节省时间，一学年约合六周。',
        src=dict(en='Gallup and Walton Family Foundation, survey of 2,232 U.S. public K-12 teachers, spring 2025',
                 cn='Gallup 与 Walton Family Foundation，2025年春季对2,232名美国公立中小学教师的调查'),
        url='https://news.gallup.com/poll/691967/schools-struggling-keep-teachers-students.aspx'),
    'eef-planning': dict(
        n='31%', unit=None,
        en='less lesson-planning time for teachers in an English trial who used ChatGPT with a guide. An expert panel found no difference in quality.',
        cn='的备课时间平均节省：在英格兰的一项随机试验中，配合使用指南使用ChatGPT的教师做到了这一点；专家评审认为课程资源质量没有差别。',
        src=dict(en='Education Endowment Foundation trial, evaluated by NFER, reported March 2025',
                 cn='Education Endowment Foundation 试验，NFER 评估，2025年3月发布'),
        url='https://www.nfer.ac.uk/blogs/ai-help-or-hindrance/'),
    'rand-use': dict(
        n='53%', unit=None,
        en='of English, math, and science teachers said they used AI for school in 2025, up more than 15 points in one to two years.',
        cn='的英语语言艺术、数学和科学教师表示在2025年将AI用于教学，比一两年前高出15个百分点以上。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-integrity': dict(
        n='34%', unit=None,
        en='of teachers reported school or district policies on AI use related to academic integrity.',
        cn='的教师表示，所在学校或学区有关于AI使用与学术诚信的政策。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-principals': dict(
        n='45%', unit=None,
        en='of principals reported school or district policies or guidance on the use of AI in schools.',
        cn='的校长表示，所在学校或学区有关于在校使用AI的政策或指导。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-districts': dict(
        n='1 in 2', unit=None,
        en='U.S. districts had trained teachers on generative AI by fall 2024, double the year before. Many built the training themselves after struggling to find outside partners.',
        cn='的美国学区到2024年秋已为教师开展生成式AI培训，比前一年翻了一倍；不少学区在找不到合适的外部合作方后，选择自己设计培训。',
        src=dict(en='RAND, More Districts Are Training Teachers on Artificial Intelligence, April 2025',
                 cn='RAND，《更多学区开始为教师开展AI培训》，2025年4月'),
        url='https://www.rand.org/pubs/research_reports/RRA956-31.html'),
    'rand-students': dict(
        n='80%+', unit=None,
        en='of students said their teachers did not explicitly teach them how to use AI for schoolwork.',
        cn='的学生表示，老师没有明确教过他们如何在学习中使用AI。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-students-use': dict(
        n='54%', unit=None,
        en='of U.S. students said they used AI for school in 2025, up more than 15 points in one to two years.',
        cn='的美国学生表示在2025年将AI用于学习，比一两年前高出15个百分点以上。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-parents': dict(
        n='61%', unit=None,
        en='of parents agreed that greater use of AI will harm students’ critical-thinking skills.',
        cn='的家长认为，更多地使用AI会损害学生的批判性思维能力。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
    'rand-false': dict(
        n='1 in 2', unit=None,
        en='students said they are worried they will be falsely accused of using AI to cheat.',
        cn='的学生表示，担心自己会被误认为用AI作弊。',
        src=dict(en='RAND, AI Use in Schools Is Quickly Increasing but Guidance Lags Behind, September 2025',
                 cn='RAND，《学校AI使用快速增长，但指导滞后》，2025年9月'),
        url='https://www.rand.org/pubs/research_reports/RRA4180-1.html'),
}

TOOL_NAMES = {'openai': 'ChatGPT', 'claude': 'Claude', 'deepseek': 'DeepSeek', 'kimi': 'Kimi', 'perplexity': 'Perplexity', 'canva': 'Canva',
              'figma': 'Figma', 'cursor': 'Cursor', 'github': 'GitHub', 'vercel': 'Vercel'}

PAGES = {
 'teachers': dict(stem='programs/teacher-training', en=dict(
   ps_k='What teachers face', ps_h='Four pressures, <em>four answers.</em>',
   ps_l='The questions we hear from teachers before every session, and how each session is built around them.',
   pk='The pressure', sk='How we answer it',
   ps=[('clock', 'No time to learn one more thing', 'Planning, grading, and differentiation already fill the week.',
        'hammer', 'One task, one tool, in the session', 'Each teacher brings a task from a class they teach now and leaves with a tool made with AI.'),
       ('file-text', 'Unclear rules on tools and data', 'Which tools are allowed, and what student data may go into them, is often still being decided.',
        'school', 'Your approved tools, your data rules', 'We work only on the tools your school approves, and agree the data rules with your technology team first.'),
       ('search-check', 'Polished work that hides the thinking', 'Students can hand in work AI helped produce, and the final product alone does not show who did the thinking.',
        'list-checks', 'Assess the process', 'Drafts, reflections, and the reasons students give for each change, so the thinking is visible.'),
       ('refresh-cw', 'Training that does not reach Monday', 'A generic demo is hard to apply to the lesson you teach next week.',
        'route', 'Start from one part of one class', 'Teachers keep the tool and the prompt behind it, and each department gets a follow-up.')],
   st_k='What the research says', st_h='Teachers are already using AI. <em>The rules have not caught up.</em>',
   st_l='Four findings from recent studies. Each links to its source.',
   stats=['gallup-hours', 'eef-planning', 'rand-use', 'rand-integrity'], src_k='Source', research_before='How we work with teachers',
   cs_k='Where we have done this', cs_h='Built with teachers, <em>on their own work.</em>',
   cases=[dict(k='Tsinghua University · Staff training', h='Schwarzman College', p='Training for staff built around their own work, with their judgment in charge. The same format as AI for Educators.',
               dl=[('Who', 'Staff, Schwarzman College'), ('Format', 'Hands-on workshop'), ('Taught by', 'Phillip An')], a=('/results#tsinghua', 'See results')),
          dict(k='Shanghai American School · A teacher’s tools', h='Ben, English teacher', p='Two small tools for his own classes: a poem annotator that marks literary devices, and a view of which students are missing which piece of knowledge.',
               dl=[('Subject', 'English'), ('Tools', 'Poem annotator; Who is missing what')], a=('#tools', 'See the tools')),
          dict(k='Next · ACAMIS Technology Conference', h='Keystone Academy, Beijing', p='A 60-minute hands-on workshop for teachers and tech coaches, built on a case study from the International School of Beijing.',
               dl=[('When', 'Sunday, October 18, 2026'), ('For', 'Teachers and tech coaches')], a=('/events/acamis-tech-2026', 'Session details'), next=True)],
   tl_k='Tools we often work with', tools=['openai', 'claude', 'deepseek', 'kimi', 'perplexity', 'canva'],
   tl_note='Or whatever your school has approved. The tool matters less than the habit of checking every result.',
   faq=[('What do teachers keep afterward?', 'The tool they made and the prompt behind it, to reuse and share with colleagues.'),
        ('Can it be for one department only?', 'Yes. A hands-on workshop for one department is one of the three formats; a school-wide training gives each department its own session and a follow-up.')]),
  cn=dict(
   ps_k='老师面对的难题', ps_h='四个难题，<em>四种做法。</em>',
   ps_l='每次培训前老师们最常提出的问题，以及每次培训如何围绕它们来设计。',
   pk='难题', sk='我们的做法',
   ps=[('clock', '没有时间再学一样新东西', '备课、批改和分层教学已经占满了一周。',
        'hammer', '一项任务，一个工具，当场做好', '每位老师带来自己正在教的一门课里的一项任务，离开时带走一个用AI做出的工具。'),
       ('file-text', '工具和数据规则还不明确', '哪些工具可以用、哪些学生数据可以放进去，很多学校还在商定。',
        'school', '用贵校认可的工具，按贵校的数据规则', '我们只使用贵校认可的工具，并先和贵校技术团队商定数据规则。'),
       ('search-check', '作品光鲜，看不出背后的思考', '学生可以交上AI帮忙做出的作品，只看成品，看不出思考出自谁。',
        'list-checks', '评估过程', '草稿、反思，以及学生每次修改背后的理由，让思考被看见。'),
       ('refresh-cw', '培训到了周一就用不上', '泛泛的演示，很难用到下周要上的那节课。',
        'route', '从一门课里的一小部分出发', '老师留下做好的工具和背后的提示词，每个教研组之后还有跟进。')],
   st_k='研究怎么说', st_h='老师已经在用AI，<em>规则还没跟上。</em>',
   st_l='来自近期研究的四项发现，每一项都附有来源链接。',
   stats=['gallup-hours', 'eef-planning', 'rand-use', 'rand-integrity'], src_k='来源', research_before='How we work with teachers',
   cs_k='我们做过的', cs_h='和老师一起，<em>从他们自己的工作出发。</em>',
   cases=[dict(k='清华大学 · 教职员工培训', h='苏世民书院', p='为苏世民书院教职员工开展的培训，从他们手头的实际工作出发，关键判断始终由他们自己把握。形式与我们的教育者AI培训一致。',
               dl=[('对象', '苏世民书院教职员工'), ('形式', '实操工作坊'), ('主讲', '安广宁')], a=('/results-cn#tsinghua', '查看成果')),
          dict(k='上海美国学校 · 一位老师的工具', h='英文老师 Ben', p='为自己的课堂做的两个小工具：一个在诗歌旁标出修辞手法，一个一眼看出哪些学生还没掌握哪个知识点。',
               dl=[('学科', '英文'), ('工具', '诗歌批注；谁还没掌握哪个知识点')], a=('#tools', '看看这些工具')),
          dict(k='即将举办 · ACAMIS 技术大会', h='北京市鼎石学校', p='面向教师和技术教练的60分钟实操工作坊，以北京顺义国际学校的案例为基础。',
               dl=[('时间', '2026年10月18日（周日）'), ('对象', '教师和技术教练')], a=('/events/acamis-tech-2026-cn', '查看活动'), next=True)],
   tl_k='我们常用的工具', tools=['openai', 'claude', 'deepseek', 'kimi', 'perplexity', 'canva'],
   tl_note='或者贵校已经认可的任何工具。工具本身不如核查每一个结果的习惯重要。',
   faq=[('培训结束后，老师能留下什么？', '自己做好的工具和背后的提示词，可以反复使用，也可以分享给同事。'),
        ('可以只面向一个教研组吗？', '可以。面向一个教研组的动手工作坊就是三种形式之一；全校培训则会为每个教研组各安排一场，之后再跟进。')])),
 'technology': dict(stem='schools/technology', proof_mode='keep_cred', en=dict(
   ps_k='What technology teams face', ps_h='Four risks, <em>four safeguards.</em>',
   ps_l='The concerns IT directors and tech coaches raise first, and how every session is set up around them.',
   pk='The risk', sk='How we handle it',
   ps=[('search', 'Tools arrive faster than you can review them', 'Teachers find new AI tools on their own, and each one is another review.',
        'school', 'No new tools introduced', 'We review your approved list with you before planning. Sessions run on the systems your school already allows.'),
       ('file-text', 'Student data and child protection', 'Every new tool raises the same questions about what data goes in and who sees it.',
        'list-checks', 'No student records in sessions', 'The data rules are agreed with your team first, and teacher sessions use teachers’ own materials, not student records.'),
       ('users', 'Uneven adoption across staff', 'A few teachers move fast while most wait for something they can use in class.',
        'user-check', 'Your coaches in the room', 'Sessions run on your campus with your tech coaches there, so the people who support teachers see the work first-hand.'),
       ('refresh-cw', 'Every tool change restarts training', 'When a product changes or is replaced, the training built around it goes with it.',
        'route', 'What stays when tools change', 'Your coaches keep the session plans, teacher examples, and shared templates, and the method carries to the next tool.')],
   st_k='What the research says', st_h='Use is rising fast. <em>Policy and training lag.</em>',
   st_l='Four findings from RAND’s national surveys of districts, principals, teachers, and students. Each links to its source.',
   stats=['rand-principals', 'rand-districts', 'rand-students', 'rand-integrity'], src_k='Source', research_before='How we plan with you',
   cs_k='Where we have done this', cs_h='Run inside real <em>institutions.</em>',
   cases=[dict(k='Tsinghua University · Staff training', h='Schwarzman College', p='Training for staff built around their own work, with their judgment in charge. The same format as AI for Educators.',
               dl=[('Who', 'Staff, Schwarzman College'), ('Format', 'Hands-on workshop'), ('Taught by', 'Phillip An')], a=('/results#tsinghua', 'See results')),
          dict(k='International School of Beijing · On campus', h='A five-day student program', p='Over five days, students built working websites and apps with AI and presented them to judges, on the school’s campus with mentors in the room.',
               dl=[('Where', 'International School of Beijing'), ('When', 'Summer 2026')], a=('/results', 'See results')),
          dict(k='Next · ACAMIS Technology Conference', h='Keystone Academy, Beijing', p='A 60-minute hands-on workshop for teachers and tech coaches, built on the case study from the International School of Beijing.',
               dl=[('When', 'Sunday, October 18, 2026'), ('For', 'Teachers and tech coaches')], a=('/events/acamis-tech-2026', 'Session details'), next=True)],
   tl_k='Tools we have worked with, when a school approves them', tools=['openai', 'claude', 'deepseek', 'kimi'],
   tl_note='Plus Copilot, Doubao, and others your school allows. We review them with you before planning any session.',
   faq=[('Do teachers need new accounts?', 'No new tools are introduced. Sessions run on the systems your school has already approved.')]),
  cn=dict(
   ps_k='技术团队面对的难题', ps_h='四种风险，<em>四道保障。</em>',
   ps_l='IT负责人和技术教练最先提出的顾虑，以及每次培训如何围绕它们来安排。',
   pk='风险', sk='我们的做法',
   ps=[('search', '新工具出现的速度超过审核的速度', '老师会自己找到新的AI工具，每一个都需要再审核一次。',
        'school', '不引入新工具', '规划之前，我们先和您一起过一遍贵校认可的工具清单；培训只在贵校已经允许的系统上进行。'),
       ('file-text', '学生数据与儿童保护', '每个新工具都会带来同样的问题：放进去什么数据，谁能看到。',
        'list-checks', '培训不涉及学生档案', '数据规则先与贵校团队商定；教师培训使用老师自己的材料，不涉及学生档案。'),
       ('users', '教职员工的使用参差不齐', '少数老师走得很快，多数老师在等一个能直接用到课堂上的东西。',
        'user-check', '技术教练全程在场', '培训在贵校校园进行，技术教练在场，负责支持老师的人第一时间看到做法。'),
       ('refresh-cw', '工具一换，培训就得重来', '产品更新或被替换时，围绕它做的培训也随之作废。',
        'route', '工具更换后留下什么', '技术教练留下培训方案、教师案例和共享模板，这套方法也能用到下一个工具上。')],
   st_k='研究怎么说', st_h='使用快速增长，<em>政策与培训滞后。</em>',
   st_l='来自 RAND 对学区、校长、教师和学生的全国调查的四项发现，每一项都附有来源链接。',
   stats=['rand-principals', 'rand-districts', 'rand-students', 'rand-integrity'], src_k='来源', research_before='How we plan with you',
   cs_k='我们做过的', cs_h='在真实的机构里<em>落地。</em>',
   cases=[dict(k='清华大学 · 教职员工培训', h='苏世民书院', p='为苏世民书院教职员工开展的培训，从他们手头的实际工作出发，关键判断始终由他们自己把握。形式与我们的教育者AI培训一致。',
               dl=[('对象', '苏世民书院教职员工'), ('形式', '实操工作坊'), ('主讲', '安广宁')], a=('/results-cn#tsinghua', '查看成果')),
          dict(k='北京顺义国际学校 · 在校园内', h='为期五天的学生项目', p='五天里，学生借助AI做出可用的网站和应用，并向评委展示；全程在学校校园内进行，导师在场。',
               dl=[('地点', '北京顺义国际学校'), ('时间', '2026年夏天')], a=('/results-cn', '查看成果')),
          dict(k='即将举办 · ACAMIS 技术大会', h='北京市鼎石学校', p='面向教师和技术教练的60分钟实操工作坊，以北京顺义国际学校的案例为基础。',
               dl=[('时间', '2026年10月18日（周日）'), ('对象', '教师和技术教练')], a=('/events/acamis-tech-2026-cn', '查看活动'), next=True)],
   tl_k='经学校认可后我们用过的工具', tools=['openai', 'claude', 'deepseek', 'kimi'],
   tl_note='还有 Copilot、豆包，以及贵校允许的其他工具。规划任何培训之前，我们都会和您一起先审一遍。',
   faq=[('老师需要注册新账号吗？', '不会引入新工具。培训在贵校已经认可的系统上进行。')])),
}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from depth_pages import MORE  # noqa: E402
PAGES.update(MORE)


def head(k, h, l=None):
    return '<header class="ds-head reveal"><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2>%s</header>' % (k, h, '<p class="ds-lede">%s</p>' % l if l else '')


def block_a(c, lang):
    rows = ''.join('<li class="reveal"><div class="ds-ps-p">%s<span class="k">%s</span><h3>%s</h3><p>%s</p></div><span class="ds-ps-arrow" aria-hidden="true"></span>'
                   '<div class="ds-ps-s">%s<span class="k">%s</span><h3>%s</h3><p>%s</p></div></li>'
                   % (ic(pi), c['pk'], ph, pp, ic(si), c['sk'], sh, sp) for pi, ph, pp, si, sh, sp in c.get('ps', []))
    stats = ''
    for sid in c['stats']:
        s = STATS[sid]
        unit = '<small>%s</small>' % s['unit'][lang] if s['unit'] else ''
        stats += ('<li><span class="ds-stat-n">%s%s</span><p class="ds-stat-t">%s</p><p class="ds-stat-src">%s: <a href="%s" rel="noopener" target="_blank">%s</a></p></li>'
                  % (s['n'], unit, s[lang], c['src_k'], s['url'], s['src'][lang]))
    jj = '<!-- JJ review: depth sections CN copy (DEPTH-BRIEF, Oct 16, 2026) -->\n' if lang == 'cn' else ''
    if not c.get('ps'):
        a_html = '<!-- depth:a -->\n%s<!-- /depth:a -->' % jj
    else:
        a_html = None
    return (a_html or ('<!-- depth:a -->\n%s<section class="ds-section" id="pressures" data-screen-label="Pressures"><div class="container">%s<ol class="ds-ps">%s</ol></div></section>\n<!-- /depth:a -->'
            % (jj, head(c['ps_k'], c['ps_h'], c['ps_l']), rows)),
            '' if not c['stats'] else '<!-- depth:r -->\n<section class="ds-section is-alt" id="research" data-screen-label="Research"><div class="container">%s<ul class="ds-stats reveal" style="--n:%d">%s</ul></div></section>\n<!-- /depth:r -->'
            % ((head(c['st_k'], c['st_h'], c['st_l']), len(c['stats']), stats) if c['stats'] else ()))


def block_b(c):
    cases = ''
    for x in c['cases']:
        dl = ''.join('<dt>%s</dt><dd>%s</dd>' % kv for kv in x['dl'])
        cases += ('<li class="ds-case%s reveal"><span class="ds-eyebrow%s">%s</span><h3>%s</h3><p>%s</p><dl>%s</dl><a class="tlink" href="%s">%s →</a></li>'
                  % (' is-next' if x.get('next') else '', ' is-muted' if x.get('next') else '', x['k'], x['h'], x['p'], dl, x['a'][0], x['a'][1]))
    tools = ''.join('<li><img src="/logos/tools/sm/%s.webp" alt="" width="24" height="24" loading="lazy" decoding="async" />%s</li>' % (t, TOOL_NAMES[t]) for t in c.get('tools', []))
    return ('<!-- depth:b -->\n<section class="ds-section" id="cases" data-screen-label="Cases"><div class="container">%s<ul class="ds-cases" style="--n:%d">%s</ul>'
            '%s</div></section>\n<!-- /depth:b -->'
            % (head(c['cs_k'], c['cs_h'], c.get('cs_l')), (2 if len(c['cases']) == 4 else min(len(c['cases']), 3)), cases,
               ('<div class="reveal" style="margin-top:var(--space-8)"><span class="ds-eyebrow" style="margin-bottom:var(--space-4)">%s</span><ul class="ds-tools">%s</ul><p class="ds-tools-note">%s</p></div>'
                % (c['tl_k'], tools, c['tl_note'])) if tools else ''))


def apply(s, c, lang, proof_mode=None):
    (a, r), b = block_a(c, lang), (block_b(c) if c.get('cases') else '<!-- depth:b -->\n<!-- /depth:b -->')
    if not c['stats']:
        r = ''
    # the research section sits before the section labelled c['research_before'] (or right after pressures)
    s = re.sub(r'(?s)<!-- depth:r -->.*?<!-- /depth:r -->\n?', '', s)
    s = re.sub(r'(?s)(<!-- depth:a -->.*?<!-- /depth:a -->)\n<section class="ds-section is-alt" id="research".*?</section>\n', r'\1\n', s)
    if '<!-- depth:a -->' in s:
        s = re.sub(r'(?s)<!-- depth:a -->.*?<!-- /depth:a -->', lambda m: a, s)
        s = re.sub(r'(?s)<!-- depth:b -->.*?<!-- /depth:b -->', lambda m: b, s)
    else:
        i = s.index('</section>', s.index('cine-hero')) + len('</section>')
        s = s[:i] + '\n\n' + a + '\n' + s[i:]
        m = re.search(r'(?s)<section[^>]*data-screen-label="(?:Proof|Proof and team)">.*?</section>', s)
        if m and proof_mode == 'keep_cred':
            # the proof section keeps the credibility strip; its one-line facts move into the cases
            sec = re.sub(r'(?s)\s*<ul class="el-proof reveal">.*?</ul>', '', m.group(0))
            s = s[:m.start()] + b + '\n' + sec + s[m.end():]
        elif m and proof_mode == 'program':
            # program pages: the thin stats row moves into the cases; anything else in the section stays
            sec = m.group(0)
            for rx in (r'(?s)\s*<div class="pc-proof-head[^"]*">.*?</div>', r'(?s)\s*<ul class="pc-stats[^"]*">.*?</ul>', r'(?s)\s*<p class="pc-proof-line[^"]*">.*?</p>'):
                sec = re.sub(rx, '', sec, count=1)
            inner = re.sub(r'(?s)<[^>]+>|\s', '', sec)
            s = s[:m.start()] + b + ('\n' + sec if inner else '') + s[m.end():]
        elif m:
            s = s[:m.start()] + b + s[m.end():]
        else:   # no proof row: the cases go before the FAQ, or before the next step when there is no FAQ
            k = s.find('data-screen-label="%s"' % c['cases_before']) if c.get('cases_before') else -1
            k = k if k > 0 else s.find('data-screen-label="FAQ"')
            k = k if k > 0 else s.find('data-screen-label="Next step"')
            j = s.rfind('<section', 0, k) if k > 0 else s.rfind('</main>')
            s = s[:j] + b + '\n' + s[j:]
    anchor = c.get('research_before')
    j = s.find('data-screen-label="%s"' % anchor) if anchor else -1
    j = s.rfind('<section', 0, j) if j > 0 else s.index('<!-- /depth:a -->') + len('<!-- /depth:a -->') + 1
    if r:
        s = s[:j] + r + '\n' + s[j:]
    # FAQ: the depth items, marked, after the page's own
    s = re.sub(r'<details (?:class="faq-item" )?data-depth>.*?</details>', '', s)
    items = ''.join('<details data-depth><summary>%s</summary><p>%s</p></details>' % qa for qa in c['faq'])
    s = re.sub(r'(?s)<!-- depth:f -->.*?<!-- /depth:f -->\n?', '', s)
    if items and 'data-screen-label="FAQ"' not in s and c.get('faq_title'):
        # pages without a FAQ get one built from facts the page already states
        sec = ('<!-- depth:f -->\n<section class="ds-section" id="faq" data-screen-label="Questions"><div class="container">%s<div class="faq ds-faq reveal">%s</div></div></section>\n<!-- /depth:f -->\n'
               % (head(c['faq_k'], c['faq_title']), items))
        k = s.find('data-screen-label="Next step"')
        j = s.rfind('<section', 0, k) if k > 0 else s.rfind('</main>')
        return s[:j] + sec + s[j:]
    if not items or 'data-screen-label="FAQ"' not in s:
        return s
    k = s.rfind('</details>', 0, s.find('</div>', s.rfind('<details', 0, s.find('data-screen-label="Next step"'))))
    last = s[s.rfind('<details', 0, k):k] if k > 0 else ''
    if 'class="faq-item"' in last:   # match the page's own item markup (question span + toggle)
        items = ''.join('<details class="faq-item" data-depth><summary><span class="faq-q">%s</span><span class="faq-toggle" aria-hidden="true">+</span></summary><p class="faq-a">%s</p></details>' % qa for qa in c['faq'])
    if k > 0:
        k += len('</details>')
        s = s[:k] + items + s[k:]
    return s


if __name__ == '__main__':
    page = sys.argv[1]
    check = '--check' in sys.argv
    cfg = PAGES[page]
    n = 0
    for lang, f in (('en', cfg['stem'] + '.html'), ('cn', cfg['stem'] + '-cn.html')):
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        t = apply(s, cfg[lang], lang, cfg.get('proof_mode'))
        for rx in cfg.get('drop', []):   # legacy rows that the depth sections now cover
            t = re.sub(rx, '', t)
        if t != s:
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
