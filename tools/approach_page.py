"""Approach + Learning Approach page builder (APPROACH-BRIEF, EDITORIAL-BRIEF; Oct 16, 2026), EN and CN.

Two pages from one copy deck (rebalanced NAV-BRIEF 2, Oct 17, 2026; no section appears on both):
  approach(-cn).html            why we teach this way: the three skills (photos), how we teach (principles, who does
                                what, the eight principles, the shape of a day), by audience, then "Next: the framework"
  learning-approach(-cn).html   the framework: wheel with the four strands and their learning goals, one week
                                (editorial matrix, css/ds.css), outcomes, assessment, then "Why we teach this way"
Each body sits between <!-- ap2:start --> and <!-- ap2:end -->; the cine hero above it stays with
tools/hero_markup.py. This tool also writes the hero copy, <title>, descriptions, canonical and language links.
  python3 tools/approach_page.py           write all four pages
  python3 tools/approach_page.py --check   report pages that would change

Sources, nothing invented: the ACAMIS workshop deck in ~/arena-school (framework wheel, learning outcomes, the
assessment slide, the goals-by-day table), the eight principles from the original Approach page, and each
program's own page for the outcomes by audience. No statistics, no ISB numbers, no em dashes. CN is marked for
JJ review. Icons: Lucide (ISC), tools/lucide_icons.json. Design: the Claude Design project (DESIGN-SYSTEM.md).
"""
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from approach_wheel import svg as wheel_svg  # noqa: E402

E = html.escape
ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']


def ic(name, cls='ds-ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % (cls, ICONS[name]))


DOM_ICONS = ['target', 'search-check', 'hammer', 'messages-square']
SKILL_ICONS = ['compass', 'search-check', 'badge-check']
TEACH_ICONS = ['users', 'file-text', 'lightbulb', 'presentation']
DAY_ICONS = ['book-open', 'hammer', 'user-check', 'clock', 'pen-line', 'list-checks', 'mic']
EV_ICONS = ['book-open', 'file-text', 'mic']

T = {'en': dict(
  lang='en', sfx='',
  # ---------- Approach (short) ----------
  a_title='Approach · Arena School',
  a_desc='Arena School’s approach: why learners need agency, taste, and craft when AI can make almost anything, the principles in every room, and how it fits students, teachers, schools, and families.',
  a_eyebrow='Our approach', a_h1='Agency, taste, <em>and craft.</em>',
  a_lede='When AI can make almost anything, learners need to know what is worth making, whether it is good, and how to finish it.',
  a_cta1='Find the right program', a_cta2='Read the learning approach',
  a_sk_k='Three skills', a_sk_h='What AI cannot <em>do for them.</em>',
  a_sk_l='Each skill gets a moment in every program that learners cannot skip.',
  skills=[
   ('I', 'Agency', 'Choose what is worth doing, before anyone assigns it.', 'AI picks the problem, and the learner follows.', 'isb-hq/isb-team-slide-800.webp', 'A team presents the problem it chose to solve',
    'Each learner chooses the problem and pitches it in three minutes, with no slides.',
    [('In school', 'When AI can finish the assignment, the harder skill is setting the question.'), ('At work', 'Work that only follows instructions is the easiest to hand to AI. People who define the problem direct the work.'), ('Over a career', 'A project a learner chose and saw through shows initiative a transcript cannot.')]),
   ('II', 'Taste', 'Judge whether the work is actually good.', 'The first answer AI gives becomes the final one.', 'isb-2026/mentor-feedback-800.webp', 'Mentors respond to a student’s work',
    'A working version goes live at a public link, and real users and mentors react every day.',
    [('In school', 'When every essay can look polished, telling strong work from weak is what teachers need to see.'), ('At work', 'A team can generate ten versions in an hour. The person who picks the right one, and says why, is the one they rely on.'), ('Over a career', 'Judgment compounds. It earns trust with larger decisions.')]),
   ('III', 'Craft', 'Finish the work so people can trust it.', 'The work stays an unchecked first draft.', 'isb-2026/demo-laptop-800.webp', 'Students present a finished product',
    'Building stops at a fixed hour, and on demo day learners explain every decision live.',
    [('In school', 'A first draft is now instant. Revising it into something reliable is where the learning happens.'), ('At work', 'A working product earns trust that a prototype or a slide deck does not.'), ('Over a career', 'A record of finished work, with a live link, speaks for itself.')]),
  ],
  without='Without it', practice='How learners practice it', changes='What it changes',
  ptr_k='Next: the framework', ptr_h='What learners practice, <em>and how we know.</em>',
  ptr_p='The learning approach sets out the framework behind every program: four strands with their learning goals, a worked week, the outcomes, and how we assess the thinking.',
  ptr_items=['The framework wheel', 'A worked week', 'Outcomes by strand', 'How we assess'], ptr_btn='Read the learning approach',
  # ---------- Learning approach ----------
  l_title='Learning approach · Arena School',
  l_desc='Arena School’s learning framework for every program: four strands and their learning goals, a worked week, the outcomes learners reach, and how we assess the thinking.',
  l_og='One learning framework for every Arena School program: learners decide, AI builds, and real people judge the work.',
  l_eyebrow='Learning approach', l_h1='Learners decide. AI builds. <em>Real people judge.</em>',
  l_lede='One framework runs every Arena School program, for students, teachers, school leaders, and parents. Here is what learners practice, what they can do by the end, and how we know.',
  l_cta1='Find the right program', l_cta2='See the framework',
  toc_label='On this page',
  toc=['Framework', 'One week', 'Outcomes', 'Assessment'],
  fw_more=('/approach#principles', 'The teaching principles in full'),
  wy_k='Why we teach this way', wy_h='The skills and principles <em>behind the framework.</em>',
  wy_p='Our approach explains why agency, taste, and craft come first, the principles in every room, and how the framework fits students, teachers, schools, and families.',
  wy_items=['Three skills', 'How we teach', 'Who does what', 'By audience'], wy_btn='Read our approach',
  ph_k='Philosophy', ph_h='Three skills <em>AI cannot supply.</em>',
  ph_l='AI can draft the essay, write the code, and design the logo. It cannot choose the problem, judge the result, or finish the work so people trust it.',
  fw_k='Framework', fw_h='One framework, <em>every program.</em>',
  fw_l='The learner sits at the center. Four strands of work circle them. Four teaching principles hold it in place.',
  fw_center='We say <em>learner</em> on purpose: the same framework runs our student programs, our teacher training, and our sessions for school leaders and parents.',
  fw_mid_k='Four strands', fw_out_k='Four teaching principles',
  domains=['Inquiry and planning', 'Research and evaluation', 'Creating and communicating', 'Collaboration and reflection'],
  principles4=['In person, real-time feedback', 'AI use disclosed and cited', 'Learner voice and choice', 'An authentic audience'],
  fw_q='How did you check it?', fw_q_k='The question at every check-in',
  fw_note='Built on project-based learning and informed by PBLWorks’ Gold Standard PBL. AI can support the feedback. It does not replace it.',
  go_k='Strands', go_h='Four strands, <em>one cycle.</em>',
  go_l='Every project moves through all four, then starts again with what it learned.',
  goals=['Turn an interest into a focused question, and plan the work.', 'Check sources, including AI output, and choose on evidence.', 'Build and test it with AI, and explain it clearly.', 'Use critique from teachers and peers to revise the work.'],
  ex_k='One week', ex_h='Five days, <em>all four strands.</em>',
  ex_l='A five-day student build week, as run at the International School of Beijing in summer 2026. Darker blocks show the day each strand is practiced.',
  ex_goal_col='Strand', ex_ev_col='Evidence',
  days=[('Day 1', 'Pick a problem'), ('Day 2', 'Go public'), ('Day 3', 'The rebuild'), ('Day 4', 'Polish and price'), ('Day 5', 'Demo day')],
  ex_rows=[
   ('Turn an interest into a focused question', 1, 1, {1: 'Pick a problem and a plan'}, 'A plan and a first prototype', 'Day 1'),
   ('Check sources, including AI output', 1, 3, {2: 'Test it with the people it’s for'}, 'Choices backed by what users did', 'Days 1 to 3'),
   ('Build and test a product with AI', 2, 4, {2: 'Ship it', 4: 'Price it'}, 'A live product at a public link', 'Days 2 to 4'),
   ('Use critique to revise the work', 3, 5, {3: 'Rebuild it', 5: 'Defend it'}, 'A rebuilt product, and a pitch to judges', 'Days 3 to 5'),
  ],
  ex_key=('Practiced', 'In progress'),
  ex_foot='No worksheet, no quiz. <b>The work is the evidence.</b>',
  ex_link=('/programs/product-intensive', 'See the five-day Entrepreneurship &amp; AI Intensive'),
  oc_k='What learners will be able to do', oc_h='Outcomes you can <em>assess on any project.</em>',
  oc_l='The same outcomes hold for every learner. The depth grows, from middle school to adults.',
  outcomes=[
   ['Turn a broad interest into a focused, researchable question.', 'Plan a project with milestones, and adjust the plan based on progress.'],
   ['Find, evaluate, and cite sources, including checking the accuracy of AI output.', 'Compare options against criteria, and justify a choice.', 'Explain how AI tools work, where they fail, and the bias and privacy issues they raise.'],
   ['Build and test a product, prototype, or solution, deciding which steps to hand to AI and disclosing how they used it.', 'Structure an argument and write it clearly, in their own words.', 'Present to an authentic audience, and defend their reasoning under questioning.'],
   ['Work in a team, share roles, and contribute to a shared product.', 'Give and use critique from teachers and peers to revise their work.', 'Reflect on their process and on what they would do differently.'],
  ],
  as_k='Assessment', as_h='We assess <em>the thinking behind the work.</em>',
  as_l='The process, not only the product: how a learner chose, checked, and finished.',
  crit_k='Sample criterion · Research and evaluation', crit_h='Evaluates sources, including AI output',
  levels=[('Beginning', 'Accepts sources and AI output as given; cites inconsistently.'), ('Developing', 'Checks some claims against a second source; cites most sources.'), ('Proficient', 'Verifies key claims, including AI output, against reliable sources; discloses AI use.'), ('Extending', 'Explains why sources disagree, corrects AI errors, and judges which evidence to trust.')],
  crit_foot='Used with students in the ISB AI Founders Program, summer 2026. With a school, the rubrics stay with its team.',
  ev_k='Evidence we collect', evidence=['Process journal', 'Drafts', 'Recorded defense'],
  qs_k='Three questions do the coaching',
  qs=[('Agency', 'Why this problem?'), ('Taste', 'How do you know it’s good?'), ('Craft', 'What would make someone trust it?')],
  pr_k='Principles', pr_h='How we <em>teach.</em>',
  pr_l='Four principles in every room, a clear split of the work, and a day with the same shape every time.',
  teach=[('In person, real-time feedback', 'Mentors sit with learners while they build, ask how they checked it, and respond on the spot.'),
         ('AI use disclosed and cited', 'Learners decide which steps to hand to AI, and say how they used it. Student data stays in accounts the school approves.'),
         ('Learner voice and choice', 'Learners choose the problem. Mentors support. They do not assign.'),
         ('An authentic audience', 'Work goes in front of real users, judges, and families.')],
  split_k='Who does what',
  ai_k='AI tools and mentors handle', ai=['Writing the code', 'Putting it online', 'Fixing technical errors'],
  me_k='Learners decide', me=['Which problem, and for whom', 'What to cut after users try it', 'The name, the price, and the pitch'],
  eight_k='Eight principles, grouped by skill',
  eight_groups=[('Agency', [('I', 'Agency from day one.', 'Mentors support; learners choose.'), ('V', 'Reflection, started early.', 'Thirty screen-free minutes a day: which of my goals are my own?'), ('VI', 'Risk early, while it’s cheap.', 'Small, repeated risks make larger ones easier.')]),
                ('Taste', [('II', 'Make things in front of people.', 'Every day ends with a demo.'), ('III', 'Experienced mentors in the room.', 'Founders, engineers, and designers who have made real products.'), ('VIII', 'First-principles thinking.', 'How, why, what principle, when it fails, and how to adapt.')]),
                ('Craft', [('IV', 'AI as a partner learners direct.', 'Learners write the prompts, question the output, and check it.'), ('VII', 'Daily habits, personal systems.', 'Three lines every day: finished, learned, next.')])],
  day_k='The shape of a day', day_l='The same rhythm in every format, from weekend sessions to five-day intensives.',
  day=[('Start', 'Lesson', 'Taught right before learners need it.'), ('Most of the day', 'Build', 'On a problem the team chose.'), ('During the build', 'Mentor 1:1s', 'When a team is stuck.'),
       ('Fixed hour', 'The freeze', 'Building stops. Teams demo what works.'), ('Daily', 'Reflection', 'Thirty minutes, a notebook, no screens.'), ('End of day', 'Standup', 'Finished, learned, next.'), ('Last day', 'Demo day', 'A live pitch to judges and families.')],
  au_k='By audience', au_h='Same framework, <em>four kinds of learner.</em>',
  au_l='The goals hold. The project, the depth, and the format change.',
  tabs_label='Programs by audience', see='See the program',
  audiences=[
   ('Students', 'Grades 6 to 12, plus college and early career. Every program ends in something real, made in front of real people.', [
     ('/programs/remake-your-favorite-app', 'App Design Workshop', 'Two days at school · Grades 6 to 9', ['Learn how software is made by taking a familiar app apart.', 'Direct AI coding tools, then test and judge the results.', 'Publish an app, and build the next tool for a hobby, a club, or a class.']),
     ('/programs/website-portfolio-workshop', 'College Portfolio Workshop', 'Two days at school · Grades 10 to 12', ['Judge which of their own work best represents them.', 'Plan, write, and design a real site. Every word stays theirs.', 'Use it for college, summer program, scholarship, and internship applications.']),
     ('/programs/product-intensive', 'Entrepreneurship &amp; AI Intensive', 'Five days at school · Grades 7 to 12', ['Choose a real problem, talk to users, set a price, and pitch to a panel.', 'Use AI for research, building, and the brand, and decide what stays.', 'Carry the same steps into a passion project, a competition, or a class.']),
     ('/mentorship', 'Year-Long Project Mentorship', '1:1, six months to a year · Grades 7 to 12', ['Choose the problem and answer for the results.', 'Put the product in front of real users.', 'Take it past a first draft: test it, revise it, make it good.']),
     ('/events/isb-winter-2027', 'AI Fundamentals for Students @ International School of Beijing', 'Four days at ISB · Grades 6 to 12 from any school', ['Learn AI tools for research, design, code, and video on their own project.', 'Choose a project worth making. Every decision stays theirs.', 'Finish a working version anyone can open, tested with real people.']),
     ('/zero-to-launch', 'AI Advantage Bootcamp', 'Seven days · College and early career', ['Launch a live AI product with real users.', 'Build a project for the role they want, and a portfolio.', 'Present the work on stage at demo day.'])]),
   ('Teachers', 'Teachers learn the way their students will: on their own work, with feedback in the room.', [
     ('/programs/teacher-training', 'AI for Educators', 'At your school', ['Bring one task from grading, planning, or differentiation. Leave with a tool made with AI.', 'Check every result, on the school’s approved tools.', 'Assess the process as well as the product when students also use AI.']),
     ('/programs/conferences', 'Conferences and Events', 'Talks, workshops, and panels', ['Use AI on their own lessons and materials, with help in the room.', 'See where AI helps, where it falls short, and how teachers keep the decisions.']),
     ('/schools/technology', 'Technology teams', 'For tech coaches and IT', ['Train inside the school’s approved systems and child-protection policy.', 'Keep the session plans and teacher examples, and run them again.'])]),
   ('Schools', 'For school leaders: programs planned around your calendar, with work to show for them.', [
     ('/schools', 'Working with schools', 'Students, teachers, and families', ['Start with one live session at a staff meeting you already hold.', 'Every program has clear learning goals and ends in a demo day or a live portfolio.', 'The curriculum, rubrics, and demo-day format stay with your team.']),
     ('/partnerships', 'Program partners', 'Camps, bootcamps, enrichment', ['Add a product track: problem, user research, building with AI, brand, price, and a final pitch.', 'Products stay live after the program.']),
     ('/programs/community-dialogues', 'Community Dialogues', 'Parent education at your school', ['Parent coffees and talks, agreed with school leaders beforehand.'])]),
   ('Families', 'For parents: what AI means for your child, and how to support the work at home.', [
     ('/programs/community-dialogues', 'Community Dialogues', 'Parent coffees and talks', ['How work is changing, from our team’s own work rather than predictions.', 'What students can now make, from real student projects.', 'Concrete ideas for supporting students in grades 6 to 12 at home.']),
     ('/mentorship', 'Year-Long Project Mentorship', 'Families enroll directly', ['One student, one project they choose, and personalized 1:1 mentorship.']),
     ('/events/isb-winter-2027', 'AI Fundamentals for Students @ International School of Beijing', 'Four days at ISB · Grades 6 to 12 from any school', ['No STEM background or coding needed.'])]),
  ],
  cl_k='Next step', cl_h='See it <em>in a program.</em>',
  cl_p='From two-day workshops to year-long mentorship, every Arena School program runs on this framework.',
  cl_b1='Find the right program', cl_b2='How we work with schools',
  cl_img_alt='Judges test a student product before scoring', cl_cap='Judges test each product before scoring, Beijing 2026',
)}

T['cn'] = dict(T['en'])
T['cn'].update(
  lang='cn', sfx='-cn',
  a_title='教学理念 · Arena School',
  a_desc='Arena School 的教学理念：当AI几乎什么都能做，为什么学习者需要主动性、审美与匠心，每个课堂都遵循的原则，以及它如何用于学生、老师、学校和家庭。',
  a_eyebrow='教学理念', a_h1='主动性、审美 <em>与匠心</em>',
  a_lede='当AI几乎什么都能做出来，学习者需要知道什么值得做、做得好不好，以及怎样把它做完。',
  a_cta1='找到合适的项目', a_cta2='阅读学习方法',
  a_sk_k='三种能力', a_sk_h='AI替代不了的，<em>正是这三样。</em>',
  a_sk_l='每个项目里，每种能力都有一个学习者绕不开的环节。',
  skills=[
   ('I', '主动性', '在任何人布置之前，自己选出值得做的事。', '问题由AI来挑，学习者只是跟着走。', 'isb-hq/isb-team-slide-800.webp', '一个团队介绍自己选定要解决的问题',
    '每位学习者自己选定问题，不用幻灯片，用三分钟讲清楚。',
    [('在学校', '当AI能帮忙完成作业，更难得的能力是提出问题。'), ('在工作中', '只照指令办事的工作最容易交给AI。能界定问题的人，才能主导工作。'), ('在职业生涯中', '一个自己选定并坚持做完的项目，比成绩单更能说明主动性。')]),
   ('II', '审美', '判断作品是否真的好。', 'AI给出的第一个答案，就成了最终答案。', 'isb-2026/mentor-feedback-800.webp', '导师对学生的作品给出反馈',
    '可用的版本上线到公开网址，真实用户和导师每天都给出反馈。',
    [('在学校', '当每篇文章都能做得光鲜，老师真正想看到的，是分辨好坏的能力。'), ('在工作中', '团队一小时能生成十个版本。能挑出对的那个并说清理由的人，才是大家倚重的人。'), ('在职业生涯中', '判断力会不断累积，让人赢得信任，担起更重大的决定。')]),
   ('III', '匠心', '把事情做完，做到让人信得过。', '作品停留在没有检查过的初稿。', 'isb-2026/demo-laptop-800.webp', '学生展示做完的产品',
    '每天到点停手封版；路演日上，学习者现场讲清每一个决定。',
    [('在学校', '初稿如今唾手可得，把它打磨成可靠的作品，才是真正学到东西的过程。'), ('在工作中', '真正能用的产品，比原型和幻灯片更能赢得信任。'), ('在职业生涯中', '一串做完的作品，附上能打开的链接，就是最好的证明。')]),
  ],
  without='缺少它', practice='怎样练', changes='它带来的改变',
  ptr_k='下一步：学习框架', ptr_h='学习者练什么，<em>我们怎样判断。</em>',
  ptr_p='学习方法页介绍每个项目背后的框架：四条主线及其学习目标、一周实例、学习成果，以及我们如何评估背后的思考。',
  ptr_items=['学习框架图', '一周实例', '按主线划分的学习成果', '我们如何评估'], ptr_btn='阅读学习方法',
  l_title='学习方法 · Arena School',
  l_desc='Arena School 每个项目共用的学习框架：四条主线及其学习目标、一周实例、学习者能达到的成果，以及我们如何评估思考。',
  l_og='Arena School 每个项目共用同一套学习框架：学习者做决定，AI动手做，真实的人来评判。',
  l_eyebrow='学习方法', l_h1='学习者做决定，AI动手做，<em>真实的人来评判。</em>',
  l_lede='Arena School 的每个项目，无论面向学生、老师、学校管理者还是家长，都遵循同一套框架。下面是学习者练什么、最后能做到什么，以及我们怎样判断。',
  l_cta1='找到合适的项目', l_cta2='查看学习框架',
  toc_label='本页内容',
  toc=['学习框架', '一周实例', '学习成果', '评估'],
  fw_more=('/approach-cn#principles', '查看完整的教学原则'),
  wy_k='我们为什么这样教', wy_h='框架背后的<em>能力与原则。</em>',
  wy_p='教学理念页说明了为什么主动性、审美与匠心排在最前，每个课堂都遵循的教学原则，以及这套框架如何用于学生、老师、学校和家庭。',
  wy_items=['三种能力', '我们怎样教', '分工', '面向对象'], wy_btn='阅读教学理念',
  ph_k='理念', ph_h='三种能力，<em>AI给不了。</em>',
  ph_l='AI能写文章、写代码、设计标志，却不能替人选问题、判断结果，也不能把作品做到让人信得过。',
  fw_k='学习框架', fw_h='一套框架，<em>贯穿每个项目。</em>',
  fw_l='学习者在中心，四条学习主线围绕着他们，四条教学原则把整体稳住。',
  fw_center='我们特意说<em>学习者</em>：同一套框架贯穿我们的学生项目、教师培训，以及面向学校管理者和家长的活动。',
  fw_mid_k='四条主线', fw_out_k='四条教学原则',
  domains=['探究与规划', '研究与评估', '创作与表达', '协作与反思'],
  principles4=['面对面，即时反馈', '使用AI须说明并注明', '学习者的声音与选择', '真实的受众'],
  fw_q='你是怎么验证的？', fw_q_k='每次检查进度都会问的问题',
  fw_note='以项目式学习为基础，参考 PBLWorks 的 Gold Standard PBL。AI可以辅助反馈，但不能取代它。',
  go_k='四条主线', go_h='四条主线，<em>一个循环。</em>',
  go_l='每个项目都会走完这四步，再带着学到的东西重新开始。',
  goals=['把兴趣聚焦成一个具体的问题，并规划工作。', '核查资料来源，包括AI的输出，依据证据做选择。', '借助AI做出并测试作品，并清楚地讲明白。', '利用老师和同伴的批评意见修改作品。'],
  ex_k='一周实例', ex_h='五天，<em>走完四条主线。</em>',
  ex_l='一个为期五天的学生实战周，2026年夏天在北京顺义国际学校开展。深色色块表示该主线在哪一天得到练习。',
  ex_goal_col='主线', ex_ev_col='证据',
  days=[('第1天', '选定问题'), ('第2天', '公开上线'), ('第3天', '推倒重来'), ('第4天', '打磨与定价'), ('第5天', '路演日')],
  ex_rows=[
   ('把兴趣聚焦成一个具体的问题', 1, 1, {1: '选题，定计划'}, '一份计划和第一个原型', '第1天'),
   ('核查资料来源，包括AI的输出', 1, 3, {2: '拿给真正的用户试用'}, '依据用户真实行为做出的选择', '第1至3天'),
   ('借助AI做出并测试产品', 2, 4, {2: '上线', 4: '定价'}, '一个公开网址上可用的产品', '第2至4天'),
   ('利用批评意见修改作品', 3, 5, {3: '重做', 5: '答辩'}, '重做后的产品，以及面向评委的路演', '第3至5天'),
  ],
  ex_key=('练习', '进行中'),
  ex_foot='没有练习卷，也没有小测验。<b>作品本身就是证据。</b>',
  ex_link=('/programs/product-intensive', '了解为期五天的创业与AI集训营'),
  oc_k='学习者将能够做到', oc_h='在任何项目上，<em>都能评估的学习成果。</em>',
  oc_l='每位学习者的成果目标相同，深度从初中到成人逐步加深。',
  outcomes=[
   ['把宽泛的兴趣转化为一个聚焦、可研究的问题。', '为项目设定里程碑，并根据进展调整计划。'],
   ['查找、评估并注明资料来源，包括核查AI输出的准确性。', '依据标准比较不同方案，并说明选择的理由。', '解释AI工具如何运作、在哪里会出错，以及它带来的偏见和隐私问题。'],
   ['做出并测试一个产品、原型或解决方案，决定哪些步骤交给AI，并说明自己如何使用了AI。', '组织论点，用自己的话清楚地写出来。', '面向真实的受众展示，并在提问中为自己的思路辩护。'],
   ['在团队中分工合作，为共同的作品出力。', '给出并利用老师和同伴的批评意见来修改作品。', '反思自己的过程，以及下次会怎样做得不同。'],
  ],
  as_k='评估', as_h='我们评估的，<em>是作品背后的思考。</em>',
  as_l='评估过程，而不只是结果：学习者如何选择、如何验证、如何把工作做完。',
  crit_k='评估标准示例 · 研究与评估', crit_h='评估资料来源，包括AI的输出',
  levels=[('起步', '照单全收资料和AI的输出；注明来源不一致。'), ('发展', '会用第二个来源核对部分说法；大多数来源有注明。'), ('熟练', '用可靠来源核实关键说法，包括AI的输出；说明自己如何使用AI。'), ('拓展', '能解释不同来源为何说法不一，纠正AI的错误，并判断该相信哪些证据。')],
  crit_foot='2026年夏天用于北京顺义国际学校 ISB AI Founders Program 的学生。与学校合作时，评估标准留给学校团队。',
  ev_k='我们收集的证据', evidence=['过程日志', '各版草稿', '答辩录像'],
  qs_k='三个问题，就是最好的指导',
  qs=[('主动性', '为什么选这个问题？'), ('审美', '你怎么知道它好？'), ('匠心', '怎样才能让别人信得过它？')],
  pr_k='教学原则', pr_h='我们<em>怎样教。</em>',
  pr_l='每个课堂都遵循的四条原则，清楚的分工，以及每天都一样的节奏。',
  teach=[('面对面，即时反馈', '导师在学习者动手时就坐在旁边，问他们是怎么验证的，并当场回应。'),
         ('使用AI须说明并注明', '哪些步骤交给AI由学习者决定，并说明自己如何使用了AI。学生数据只放在学校认可的账号里。'),
         ('学习者的声音与选择', '问题由学习者自己选。导师提供支持，不布置题目。'),
         ('真实的受众', '作品要面对真实的用户、评委和家长。')],
  split_k='分工',
  ai_k='交给AI工具和导师的', ai=['写代码', '把产品上线', '修复技术错误'],
  me_k='由学习者决定的', me=['做哪个问题，为谁而做', '用户试用后砍掉什么', '产品的名字、价格和路演'],
  eight_k='八条原则，按能力归类',
  eight_groups=[('主动性', [('I', '从第一天起自己做主。', '导师提供支持，方向由学习者决定。'), ('V', '尽早开始反思。', '每天三十分钟离开屏幕：哪些目标是我自己真正想要的？'), ('VI', '趁代价小，尽早冒险。', '一次次小冒险，让更大的冒险变得容易。')]),
                ('审美', [('II', '边做边展示。', '每天都以一次演示收尾。'), ('III', '经验丰富的导师就在现场。', '真正做出过产品的创始人、工程师和设计师。'), ('VIII', '从第一性原理出发。', '怎么做、为什么、依据什么原理、何时会失效、如何调整。')]),
                ('匠心', [('IV', 'AI是伙伴，主导权在学习者。', '学习者自己写提示词、追问AI的结果并加以核查。'), ('VII', '养成习惯，建立自己的方法。', '每天三行：完成了什么、学到了什么、下一步做什么。')])],
  day_k='一天的节奏', day_l='从周末课程到五天集训，每种形式都遵循同样的节奏。',
  day=[('开始', '方法课', '赶在学习者用得上之前讲。'), ('大部分时间', '开发', '围绕团队自选的问题。'), ('开发期间', '导师一对一', '团队卡住的时候。'),
       ('固定时刻', '封版', '停止开发，演示已经跑通的部分。'), ('每天', '反思', '三十分钟，一本笔记本，不看屏幕。'), ('一天结束', '站会', '完成了什么、学到了什么、下一步。'), ('最后一天', '路演日', '向评委和家长现场路演。')],
  au_k='面向对象', au_h='同一套框架，<em>四类学习者。</em>',
  au_l='目标不变，变化的是项目、深度和形式。',
  tabs_label='按对象查看项目', see='查看项目',
  audiences=[
   ('学生', '面向6至12年级，以及大学生和职场新人。每个项目都以一件真实的作品收尾，在真实的人面前完成。', [
     ('/programs/remake-your-favorite-app', '应用设计工作坊', '在校两天 · 6至9年级', ['拆解一款熟悉的应用，了解软件是怎样做出来的。', '指挥AI编程工具，再亲自测试和判断结果。', '发布一款应用，并能为爱好、社团或课程做出下一个工具。']),
     ('/programs/website-portfolio-workshop', '升学作品集工作坊', '在校两天 · 10至12年级', ['判断哪些作品最能代表自己。', '规划、撰写并设计一个真正的网站，每个字都出自自己。', '用于大学、暑期项目、奖学金和实习申请。']),
     ('/programs/product-intensive', '创业与AI集训营', '在校五天 · 7至12年级', ['选一个真实的问题，访谈用户，定价，并向评审团路演。', '用AI做调研、开发和品牌，由自己决定留下什么。', '把同样的步骤用到兴趣项目、比赛或课程作业中。']),
     ('/mentorship', '学年项目导师计划', '一对一，六个月到一年 · 7至12年级', ['自己选定问题，并为结果负责。', '把产品放到真实用户面前。', '走过初稿阶段：测试、修改，把它做好。']),
     ('/events/isb-winter-2027', '学生AI基础营 · 北京顺义国际学校', '寒假四天，在北京顺义国际学校，面向任何学校的6至12年级', ['在自己的项目中学习用于调研、设计、编程和视频的AI工具。', '选一个值得做的项目，每个决定都由自己做。', '做出任何人都能打开的可用版本，并经过真实用户测试。']),
     ('/zero-to-launch', 'AI职场先发营', '七天 · 大学生与职场新人', ['上线一款有真实用户的AI产品。', '为想申请的岗位做一个项目，并整理作品集。', '在路演日登台展示自己的作品。'])]),
   ('老师', '老师的学习方式与学生一样：用自己的工作练，现场有人给反馈。', [
     ('/programs/teacher-training', '教育者AI培训', '在贵校开展', ['带来一项批改、备课或分层教学的任务，带走一个用AI做出的工具。', '在学校批准的工具上，核查每一个结果。', '当学生也在用AI时，评估过程，而不只是结果。']),
     ('/programs/conferences', '会议与活动', '主题分享、工作坊和圆桌', ['用自己的课程和教学材料上手AI，现场有专人协助。', '了解AI在哪里有帮助、在哪里力有不逮，以及老师如何守住决定权。']),
     ('/schools/technology', '技术团队', '面向技术教练和IT团队', ['在学校批准的系统和儿童保护政策之内开展培训。', '留下课程方案和教师案例，可以再次开展。'])]),
   ('学校', '面向学校管理者：围绕学校日程规划项目，并有成果可以展示。', [
     ('/schools', '与学校合作', '面向学生、老师和家庭', ['从一次教职工会议上的现场分享开始。', '每个项目都有清晰的学习目标，并以路演日或在线作品集收尾。', '课程、评估标准和路演日形式都留给学校团队。']),
     ('/partnerships', '项目合作', '营地、训练营和素质教育机构', ['加入产品实战模块：选题、用户调研、用AI开发、品牌、定价和最终路演。', '项目结束后，产品依然在线。']),
     ('/programs/community-dialogues', '社区对话', '在贵校开展的家长教育', ['家长咖啡会和主题分享，事先与学校管理者商定。'])]),
   ('家庭', '面向家长：AI对孩子意味着什么，以及在家如何支持孩子。', [
     ('/programs/community-dialogues', '社区对话', '家长咖啡会和主题分享', ['工作正在怎样变化，来自我们团队自己的工作，而不是预测。', '学生现在能做出什么，来自真实的学生项目。', '在家支持6至12年级学生的具体做法。']),
     ('/mentorship', '学年项目导师计划', '家庭直接报名', ['一名学生，一个自己选定的项目，加上一对一的个性化导师指导。']),
     ('/events/isb-winter-2027', '学生AI基础营 · 北京顺义国际学校', '寒假四天，在北京顺义国际学校，面向任何学校的6至12年级', ['不需要理工科背景，也不需要编程基础。'])]),
  ],
  cl_k='下一步', cl_h='在具体项目中，<em>看见这套框架。</em>',
  cl_p='从两天的工作坊到学年项目导师计划，Arena School 的每个项目都运行在这套框架之上。',
  cl_b1='找到合适的项目', cl_b2='了解我们如何与学校合作',
  cl_img_alt='评委在打分前亲自试用学生的产品', cl_cap='评委在打分前逐一试用产品，北京，2026年',
)


def link(t, p):
    return p + t['sfx'] if t['sfx'] else p


def home(t):
    return '/index-cn' if t['sfx'] else '/'


def head(k, h, l=None):
    lede = '<p class="ds-lede">%s</p>' % l if l else ''
    return '<header class="ds-head reveal"><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2>%s</header>' % (k, h, lede)


def jj(t, what):
    return '<!-- JJ review: %s CN copy (EDITORIAL-BRIEF, Oct 16, 2026) -->\n' % what if t['sfx'] else ''


def closing(t):
    # (the newsletter band above it is written by tools/newsletter_markup.py)
    return ('<section class="pp-final" data-screen-label="Next step"><div class="container"><div class="pp-final-top reveal"><div>'
            '<span class="eyebrow">%s</span><h2 class="h2 h2-md">%s</h2><p class="pp-close-sub">%s</p>'
            '<div class="pp-close-cta"><a href="%s#programs" class="btn btn-primary">%s <span class="arr">→</span></a><a href="%s" class="btn btn-ghost">%s</a></div></div>'
            '<figure class="pp-close-photo"><img src="/photos/isb-hq/isb-judges-test-800.webp" srcset="/photos/isb-hq/isb-judges-test-800.webp 800w, /photos/isb-hq/isb-judges-test-1400.webp 1400w" sizes="(max-width: 900px) 100vw, 50vw" alt="%s" loading="lazy" decoding="async" />'
            '<figcaption><img loading="lazy" decoding="async" src="/logos/arena/seal-ivory-256.png" alt="" width="18" height="18" />%s</figcaption></figure></div></div></section>'
            % (t['cl_k'], t['cl_h'], t['cl_p'], home(t), t['cl_b1'], link(t, '/schools'), t['cl_b2'], t['cl_img_alt'], t['cl_cap']))


def section(id_, label, inner, alt=False):
    return '<section class="ds-section ap2%s" id="%s" data-screen-label="%s"><div class="container">%s</div></section>' % (' is-alt' if alt else '', id_, label, inner)


# ---------- Approach: why we teach this way ----------
def approach_body(t):
    """Our approach (NAV-BRIEF 2, Oct 17): the three skills, how we teach (principles, who does what, the eight
    principles, the shape of a day), by audience, then "Next: the framework" to the Learning approach page."""
    cards = []
    for i, (num, name, d, w, img, alt, how, ch) in enumerate(t['skills']):
        lis = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in ch)
        cards.append('<article class="ds-card ap-skill reveal"><figure><img src="/photos/%s" alt="%s" loading="lazy" decoding="async" width="800" height="533" /><span>%s</span></figure>'
                     '<div class="ap-skill-body"><div class="ap-skill-top">%s<h3>%s</h3></div><p class="ap-skill-def">%s</p>'
                     '<dl class="ap-skill-dl"><div><dt>%s</dt><dd>%s</dd></div><div><dt>%s</dt><dd>%s</dd></div></dl>'
                     '<details><summary>%s</summary><ol>%s</ol></details></div></article>'
                     % (img, alt, num, ic(SKILL_ICONS[i]), name, d, t['practice'], how, t['without'], w, t['changes'], lis))
    return ('<!-- ap2:start -->\n' + jj(t, 'Approach page') + '\n'.join([
        section('skills', 'Three skills', head(t['a_sk_k'], t['a_sk_h'], t['a_sk_l']) + '<div class="ds-grid ds-grid-3 ap-skills">%s</div>' % ''.join(cards)),
        principles_sec(t, alt=True),
        audiences_sec(t, alt=False),
        pointer('learning-approach', 'Next: the framework', t['ptr_k'], t['ptr_h'], t['ptr_p'], t['ptr_items'], ['route', 'list-checks', 'search-check', 'users'],
                link(t, '/learning-approach'), t['ptr_btn']),
    ]) + '\n<!-- ap2:end -->')


# ---------- Learning approach ----------
def matrix(t):
    """The editorial matrix (css/ds.css .ds-mx, BAND-BRIEF): hairline grid, faint day guides, one tinted band per
    strand across its days; inside it, practiced days in the stronger tint with the activity, the rest in the base
    tint. Phones: one card per strand with the days as chips in the same tints."""
    ths = ''.join('<th scope="col"><span class="ds-mx-k">%s</span>%s</th>' % d for d in t['days'])
    rows = []
    for i, (goal, a, b, labels, ev, dayk) in enumerate(t['ex_rows']):
        n = b - a + 1
        days = []
        for d in range(a, b + 1):
            k = '<b class="k">%s</b>' % t['days'][d - 1][0]
            if d in labels:
                days.append('<span class="on">%s<span>%s</span></span>' % (k, labels[d]))
            else:
                days.append('<span>%s<span class="vh">%s</span></span>' % (k, t['ex_key'][1]))
        cells = ['<td></td>'] * (a - 1) + ['<td class="band" colspan="%d"><div class="ds-band" style="--n:%d">%s</div></td>' % (n, n, ''.join(days))] + ['<td></td>'] * (5 - b)
        rows.append('<tr><th scope="row"><span class="ds-mx-n">0%d</span><b>%s</b><span>%s</span><em class="ds-mx-span">%s</em></th>%s<td class="ev"><span class="ds-mx-k">%s</span>%s</td></tr>'
                    % (i + 1, t['domains'][i], goal, dayk, ''.join(cells), t['ex_ev_col'], ev))
    key = '<p class="ds-mx-key" aria-hidden="true"><span><i class="on"></i>%s</span><span><i></i>%s</span></p>' % t['ex_key']
    return ('<div class="ds-mx-wrap reveal"><table class="ds-mx"><colgroup><col style="width:24%%" /><col span="5" /><col style="width:19%%" /></colgroup>'
            '<thead><tr><th scope="col">%s</th>%s<th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>%s'
            % (t['ex_goal_col'], ths, t['ex_ev_col'], ''.join(rows), key))


def principles_sec(t, alt):
    teach = ''.join('<li class="ap-teach-i reveal">%s<h3>%s</h3><p>%s</p></li>' % (ic(TEACH_ICONS[i], 'ds-ic lg'), a, b) for i, (a, b) in enumerate(t['teach']))
    groups = ''.join('<div class="ap-eg"><span class="ds-eyebrow">%s</span><ol>%s</ol></div>'
                     % (g, ''.join('<li><b>%s</b><span><strong>%s</strong>%s</span></li>' % x for x in items)) for g, items in t['eight_groups'])
    flow = ''.join('<li style="--i:%d">%s<span class="ap-fl-t">%s</span><b>%s</b><span class="ap-fl-d">%s</span></li>'
                   % (i, ic(DAY_ICONS[i]), a, b, c) for i, (a, b, c) in enumerate(t['day']))
    return section('principles', 'Principles', head(t['pr_k'], t['pr_h'], t['pr_l']) +
                   '<ol class="ds-grid ds-grid-4 ap-teach">%s</ol>'
                   '<div class="ap-block reveal"><span class="ds-eyebrow">%s</span><div class="ap-split"><div>%s<span class="ap-split-k">%s</span><ul>%s</ul></div><div class="is-learner">%s<span class="ap-split-k">%s</span><ul>%s</ul></div></div></div>'
                   '<div class="ap-block reveal"><span class="ds-eyebrow">%s</span><div class="ds-grid ds-grid-3 ap-eight">%s</div></div>'
                   '<div class="ap-block reveal"><span class="ds-eyebrow">%s</span><p class="ds-lede">%s</p><ol class="ap-flow">%s</ol></div>'
                   % (teach, t['split_k'], ic('bot'), t['ai_k'], ''.join('<li>%s</li>' % x for x in t['ai']), ic('user-round'), t['me_k'], ''.join('<li>%s</li>' % x for x in t['me']),
                      t['eight_k'], groups, t['day_k'], t['day_l'], flow), alt=alt)


def audiences_sec(t, alt):
    tabs, panels = [], []
    for n, (name, intro, progs) in enumerate(t['audiences']):
        sel = n == 0
        tabs.append('<button type="button" class="el-tab" role="tab" id="ap-t%d" aria-controls="ap-p%d" aria-selected="%s"%s><small>0%d</small>%s</button>'
                    % (n, n, 'true' if sel else 'false', '' if sel else ' tabindex="-1"', n + 1, name))
        cards = ''.join('<li class="ds-card ap-prog"><span class="ds-eyebrow is-muted">%s</span><h3>%s</h3><ul>%s</ul><a class="tlink" href="%s"><span class="tl">%s</span> <span class="arr">→</span></a></li>'
                        % (fmt, title, ''.join('<li>%s</li>' % x for x in outs), link(t, href), t['see']) for href, title, fmt, outs in progs)
        panels.append('<div class="el-tabpanel" role="tabpanel" id="ap-p%d" aria-labelledby="ap-t%d"%s><p class="ap-aud-intro">%s</p><ul class="ds-grid ds-grid-3 ap-progs">%s</ul></div>'
                      % (n, n, '' if sel else ' hidden', intro, cards))
    return section('audiences', 'By audience', head(t['au_k'], t['au_h'], t['au_l']) +
                   '<div class="el-tabs reveal" role="tablist" aria-label="%s" data-el-tabs>%s</div>%s' % (t['tabs_label'], ''.join(tabs), ''.join(panels)), alt=alt)


def pointer(id_, label, k, h, p_, items, icons, href, btn):
    lis = ''.join('<li>%s%s</li>' % (ic(n), x) for n, x in zip(icons, items))
    return section(id_, label, '<div class="ap-ptr reveal"><div><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2><p class="ap-ptr-p">%s</p></div>'
                   '<div class="ap-ptr-side"><ul>%s</ul><a class="btn btn-primary" href="%s">%s <span class="arr">→</span></a></div></div>'
                   % (k, h, p_, lis, href, btn), alt=True)


def learning_body(t):
    """The framework (NAV-BRIEF 2, Oct 17): wheel with the four strands and their learning goals, a worked week,
    outcomes, assessment, then a pointer back to Our approach (skills, principles, audiences live there)."""
    ids = ['framework', 'week', 'outcomes', 'assessment']
    o = [jj(t, 'Learning approach page') + '<nav class="ap-toc" aria-label="%s"><div class="container"><ol>%s</ol></div></nav>' % (
        t['toc_label'], ''.join('<li><a href="#%s"><b>%02d</b>%s</a></li>' % (i, n + 1, x) for n, (i, x) in enumerate(zip(ids, t['toc']))))]
    # learning-goal domains: each strand with its goal, beside the wheel
    mid = ''.join('<li>%s<span><b>%s</b>%s</span></li>' % (ic(DOM_ICONS[i]), x, t['goals'][i]) for i, x in enumerate(t['domains']))
    out = ''.join('<li>%s<span>%s</span></li>' % (ic(TEACH_ICONS[i]), x) for i, x in enumerate(t['principles4']))
    o.append(section('framework', 'Framework', head(t['fw_k'], t['fw_h'], t['fw_l']) +
             '<div class="ap-fw"><div class="ap-wheel reveal">%s</div><div class="ap-fw-text reveal">'
             '<div class="ap-fw-lists"><div class="is-goals"><span class="ds-eyebrow">%s</span><ol>%s</ol></div><div class="is-out"><span class="ds-eyebrow">%s</span><ol>%s</ol>'
             '<a class="tlink ap-fw-more" href="%s"><span class="tl">%s</span> <span class="arr">→</span></a></div></div>'
             '<blockquote class="ap-fw-q"><span class="ds-eyebrow">%s</span><p>%s</p></blockquote><p class="ap-fw-note">%s %s</p></div></div>'
             % (wheel_svg(t['lang']), t['fw_mid_k'], mid, t['fw_out_k'], out, link(t, '/approach').split('#')[0] + '#principles', t['fw_more'][1],
                t['fw_q_k'], t['fw_q'], t['fw_center'], t['fw_note']), alt=True))
    o.append(section('week', 'One week', head(t['ex_k'], t['ex_h'], t['ex_l']) + matrix(t) +
             '<p class="ap-ex-foot reveal"><span>%s</span><a class="tlink" href="%s"><span class="tl">%s</span> <span class="arr">→</span></a></p>' % (t['ex_foot'], link(t, t['ex_link'][0]), t['ex_link'][1])))
    cols = ''.join('<div>%s<h3>%s</h3><ul>%s</ul></div>' % (ic(DOM_ICONS[i]), t['domains'][i], ''.join('<li>%s</li>' % x for x in items))
                   for i, items in enumerate(t['outcomes']))
    o.append(section('outcomes', 'Outcomes', head(t['oc_k'], t['oc_h'], t['oc_l']) + '<div class="ap-outcomes reveal">%s</div>' % cols, alt=True))
    lv = ''.join('<li style="--l:%d"><b>%s</b><i aria-hidden="true"></i>%s</li>' % (i + 1, a, b) for i, (a, b) in enumerate(t['levels']))
    ev = ''.join('<li>%s<span>%s</span></li>' % (ic(EV_ICONS[i]), x) for i, x in enumerate(t['evidence']))
    qs = ''.join('<li><b>%s</b><q>%s</q></li>' % q for q in t['qs'])
    o.append(section('assessment', 'Assessment', head(t['as_k'], t['as_h'], t['as_l']) +
             '<div class="ap-assess"><div class="ds-card ap-crit reveal"><div class="ap-crit-head"><span class="ds-eyebrow">%s</span><h3>%s</h3></div><ol>%s</ol><p class="ap-crit-foot">%s</p></div>'
             '<div class="ap-side reveal"><div class="ds-card"><span class="ds-eyebrow">%s</span><ul class="ap-ev">%s</ul></div><div class="ds-card"><span class="ds-eyebrow">%s</span><ul class="ap-qs">%s</ul></div></div></div>'
             % (t['crit_k'], t['crit_h'], lv, t['crit_foot'], t['ev_k'], ev, t['qs_k'], qs)))
    o.append(pointer('why', 'Why we teach this way', t['wy_k'], t['wy_h'], t['wy_p'], t['wy_items'], ['compass', 'users', 'user-round', 'route'],
                     link(t, '/approach'), t['wy_btn']))
    return '<!-- ap2:start -->\n' + '\n'.join(o) + '\n<!-- ap2:end -->'


def apply(path, t, kind, src):
    exists = os.path.exists(path)
    s = open(path if exists else src, encoding='utf-8').read()
    n0 = s if exists else None
    body = approach_body(t) if kind == 'approach' else learning_body(t)
    # the closing section is its own block, so the newsletter band (tools/newsletter_markup.py) can sit between
    close = '<!-- ap2c:start -->\n' + closing(t) + '\n<!-- ap2c:end -->'
    if '<!-- ap2c:start -->' in s:
        s = re.sub(r'(?s)(<!-- JJ review: [^>]*-->\n)?<!-- ap2:start -->.*?<!-- ap2:end -->', lambda m: body, s)
        def keep_band(m):  # the newsletter tool's band sits right before pp-final, inside this block: keep it
            band = re.search(r'<section class="nl-band"[^>]*></section>\n', m.group(0))
            return close.replace('<section class="pp-final"', (band.group(0) if band else '') + '<section class="pp-final"', 1)
        s = re.sub(r'(?s)<!-- ap2c:start -->.*?<!-- ap2c:end -->', keep_band, s)
    else:  # first build: everything between the hero and </main> is replaced
        i = s.index('</section>', s.index('cine-hero')) + len('</section>')
        j = s.index('</main>')
        s = s[:i] + '\n\n' + body + '\n' + close + '\n\n' + s[j:]
    p = 'a_' if kind == 'approach' else 'l_'
    slug = 'approach' if kind == 'approach' else 'learning-approach'
    cta2 = link(t, '/learning-approach') if kind == 'approach' else '#framework'
    s = re.sub(r'(<div class="hero-eyebrow-row reveal"><span class="eyebrow">)[^<]*(</span>)', lambda m: m.group(1) + t[p + 'eyebrow'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<h1 class="display reveal cs-h1">).*?(</h1>)', lambda m: m.group(1) + t[p + 'h1'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<p class="lede sub reveal lede-56">).*?(</p>)', lambda m: m.group(1) + t[p + 'lede'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<div class="pp-hero-cta reveal">).*?(</div>)', lambda m: m.group(1) + '<a href="%s#programs" class="btn btn-primary">%s <span class="arr">→</span></a><a href="%s" class="btn btn-ghost">%s</a>'
               % (home(t), t[p + 'cta1'], cta2, t[p + 'cta2']) + m.group(2), s, count=1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % t[p + 'title'], s, count=1)
    og = t.get(p + 'og', t[p + 'desc'])
    for attr, val in (('name="description"', t[p + 'desc']), ('property="og:description"', og), ('name="twitter:description"', og)):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + E(val) + m.group(2), s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + E(t[p + 'title']) + m.group(2), s, count=1)
    url = 'https://arenaschool.org/%s%s' % (slug, t['sfx'])
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<div class="lang-switch"[^>]*>).*?(</div>)', lambda m: m.group(1) + (
        '\n        <a href="/%s" class="lang-active" aria-current="true">EN</a>\n        <a href="/%s-cn">中文</a>\n      ' % (slug, slug) if not t['sfx'] else
        '\n        <a href="/%s">EN</a>\n        <a href="/%s-cn" class="lang-active" aria-current="true">中文</a>\n      ' % (slug, slug)) + m.group(2), s, count=1)
    if kind == 'learning':
        s = re.sub(r'<body class=" no-ticker pg pg-approach">', '<body class=" no-ticker pg pg-approach pg-learning">', s, count=1)
    for css in ('elegance', 'approach'):  # ds.css is linked sitewide by tools/pro_markup.py
        if '/css/%s.css' % css not in s:
            s = s.replace('<link rel="stylesheet" href="/css/approach-extra.css', '<link rel="stylesheet" href="/css/%s.css?v=1" />\n<link rel="stylesheet" href="/css/approach-extra.css' % css, 1)
    if '/elegance.js' not in s:
        v = hashlib.md5(open(os.path.join(ROOT, 'elegance.js'), 'rb').read()).hexdigest()[:8]
        s = s.replace('<script src="/approach-extra.js', '<script src="/elegance.js?v=%s" defer></script>\n<script src="/approach-extra.js' % v, 1)
    return s, s != n0


JOBS = [('approach.html', 'en', 'approach'), ('approach-cn.html', 'cn', 'approach'),
        ('learning-approach.html', 'en', 'learning'), ('learning-approach-cn.html', 'cn', 'learning')]

if __name__ == '__main__':
    check = '--check' in sys.argv
    changed = 0
    for path, lang, kind in JOBS:
        p = os.path.join(ROOT, path)
        src = os.path.join(ROOT, 'approach.html' if lang == 'en' else 'approach-cn.html')
        s, ch = apply(p, T[lang], kind, src)
        if ch:
            changed += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(s)
    print(('Would change' if check else 'Changed') + ' %d pages' % changed)
