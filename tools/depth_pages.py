"""Page configurations for tools/depth.py (DEPTH-BRIEF): school-facing pages, program pages, other pages.
Same shape as the entries in depth.PAGES. Every problem and answer restates what the page already says; cases
use only facts stated on the site's own pages (results, events, program pages). No em dashes. CN for JJ review.
"""

BODLEY_EN = dict(k='Bodley Academy · Hong Kong, summer 2025', h='Twenty students, five days', p='A five-day course designed and taught by Phillip An. Each student worked on one real problem they chose.',
                 dl=[('Students', '20'), ('Rating', '9.5 / 10 Net Promoter Score')], a=('/results', 'See results'))
BODLEY_CN = dict(k='Bodley Academy · 香港，2025年夏', h='二十名学生，五天', p='由安广宁设计并亲自讲授的五天课程。每名学生各自选定一个真实的问题。',
                 dl=[('学生', '20名'), ('评价', '净推荐值 9.5 / 10')], a=('/results-cn', '查看成果'))
ISB_EN = dict(k='International School of Beijing · Summer 2026', h='A five-day student program', p='Over five days, students built working websites and apps with AI and presented them to judges, on the school’s campus with mentors in the room.',
              dl=[('Where', 'International School of Beijing'), ('Judges', 'Founders and operators from Harvard, Stanford, Y Combinator, and AI labs')], a=('/results', 'See results'))
ISB_CN = dict(k='北京顺义国际学校 · 2026年夏', h='为期五天的学生项目', p='五天里，学生借助AI做出可用的网站和应用，并向评委展示；全程在学校校园内进行，导师在场。',
              dl=[('地点', '北京顺义国际学校'), ('评委', '来自哈佛、斯坦福、Y Combinator 和AI实验室的创始人与业界人士')], a=('/results-cn', '查看成果'))
SCHWARZMAN_EN = dict(k='Tsinghua University · Staff training', h='Schwarzman College', p='Training for staff built around their own work, with their judgment in charge. The same format as AI for Educators.',
                     dl=[('Who', 'Staff, Schwarzman College'), ('Format', 'Hands-on workshop'), ('Taught by', 'Phillip An')], a=('/results#tsinghua', 'See results'))
SCHWARZMAN_CN = dict(k='清华大学 · 教职员工培训', h='苏世民书院', p='为苏世民书院教职员工开展的培训，从他们手头的实际工作出发，关键判断始终由他们自己把握。形式与我们的教育者AI培训一致。',
                     dl=[('对象', '苏世民书院教职员工'), ('形式', '实操工作坊'), ('主讲', '安广宁')], a=('/results-cn#tsinghua', '查看成果'))

MORE = {
 'schools': dict(stem='schools', drop=[r'(?s)\n    <ul class="el-proof reveal" style="margin-top:56px">.*?</ul>'], en=dict(
   ps_k='What school leaders weigh', ps_h='Four constraints, <em>four ways through.</em>',
   ps_l='The questions leaders ask before saying yes, and what each partnership is built to leave behind.',
   pk='The constraint', sk='How a partnership handles it',
   ps=[('clock', 'Staff time is already spoken for', 'Accreditation and curriculum work fill the year.',
        'route', 'The playbook stays', 'Your teachers co-run the sessions, and the curriculum, rubrics, and demo-day format stay with your team.'),
       ('list-checks', 'Boards ask for evidence', 'A new program has to show what students can do at the end.',
        'presentation', 'Families in the room on the last day', 'Every program ends in a demo day or a live portfolio, with families there to see the work.'),
       ('file-text', 'Tools and child protection', 'Every AI program raises questions about approved tools and student data.',
        'school', 'Your rules, agreed first', 'We use only the tools your school approves and agree the data rules with your technology team before planning.'),
       ('compass', 'A school with its own context', 'Ages, languages, and parent expectations differ from school to school.',
        'users', 'Adapted before it runs', 'Planning starts eight to twelve weeks ahead; we tailor the plan to age and language, with parent letters included.')],
   st_k='What the research says', st_h='Students already use AI. <em>Schools are still writing the rules.</em>',
   st_l='Four findings from RAND’s national surveys. Each links to its source.',
   stats=['rand-students-use', 'rand-principals', 'rand-students', 'rand-parents'], src_k='Source', research_before='How a partnership works',
   cs_k='Where we have done this', cs_h='Programs we have <em>run.</em>',
   cases=[ISB_EN, BODLEY_EN, SCHWARZMAN_EN],
   tl_k='Tools students and staff have learned, when a school approves them', tools=['openai', 'claude', 'deepseek', 'kimi', 'figma', 'canva'],
   tl_note='Or the tools your school allows. What carries over is the method: choose, judge, and finish.',
   faq=[('How far ahead should we plan?', 'Usually eight to twelve weeks before the program dates, starting with one call about your calendar and goals.')]),
  cn=dict(
   ps_k='学校管理者的考量', ps_h='四个限制，<em>四条出路。</em>',
   ps_l='管理者点头之前最常问的问题，以及每次合作要为学校留下什么。',
   pk='限制', sk='合作如何应对',
   ps=[('clock', '教职员工的时间早已排满', '认证和课程工作已经占满了一年。',
        'route', '方法留给学校', '贵校老师共同带课，课程、评估标准和路演日形式都留给贵校团队。'),
       ('list-checks', '董事会需要看到成果', '新项目要能说明学生最后能做到什么。',
        'presentation', '最后一天，家长在场', '每个项目都以路演日或在线作品集收尾，家长到场看学生的作品。'),
       ('file-text', '工具与儿童保护', '每个AI项目都会带来认可工具和学生数据的问题。',
        'school', '先按贵校的规则商定', '我们只使用贵校认可的工具，并在规划前与贵校技术团队商定数据规则。'),
       ('compass', '每所学校都有自己的情况', '年龄、语言和家长期待因校而异。',
        'users', '开始前先做调整', '通常提前八到十二周开始规划；我们按年龄和语言调整方案，并附上家长信。')],
   st_k='研究怎么说', st_h='学生已经在用AI，<em>学校还在制定规则。</em>',
   st_l='来自 RAND 全国调查的四项发现，每一项都附有来源链接。',
   stats=['rand-students-use', 'rand-principals', 'rand-students', 'rand-parents'], src_k='来源', research_before='How a partnership works',
   cs_k='我们做过的', cs_h='我们开展过的<em>项目。</em>',
   cases=[ISB_CN, BODLEY_CN, SCHWARZMAN_CN],
   tl_k='经学校认可后，学生和教职员工学过的工具', tools=['openai', 'claude', 'deepseek', 'kimi', 'figma', 'canva'],
   tl_note='或者贵校允许的工具。真正能延续下去的是方法：选择、判断、做完。',
   faq=[('需要提前多久规划？', '通常在项目日期前八到十二周，从一次关于贵校校历和目标的通话开始。')])),
}
