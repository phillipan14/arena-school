"""Approach page builder (APPROACH-BRIEF, Oct 16, 2026): Arena School's sitewide learning framework, EN and CN.

Writes the page body between <!-- ap2:start --> and <!-- ap2:end --> in approach.html and approach-cn.html (the
cine hero above it stays with tools/hero_markup.py), plus the hero copy, <title> and descriptions. Idempotent:
  python3 tools/approach_page.py           write both pages
  python3 tools/approach_page.py --check   report pages that would change

Sources, nothing invented: the ACAMIS workshop deck in ~/arena-school (framework wheel, learning outcomes, the
assessment slide, the goals-by-day table), the eight principles already on this page, and each program's own page
for the outcomes by audience. No statistics, no ISB numbers. CN copy is marked for JJ review in the page.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from approach_wheel import svg as wheel_svg  # noqa: E402

E = html.escape
DOM_COLORS = ['#22458A', '#2F55A8', '#1E3F86', '#3A63B8']

T = {
 'en': dict(
  link=lambda p: p,
  title='Approach · Arena School',
  desc='Arena School’s learning framework: the learner does the thinking. Philosophy, four learning-goal domains, outcomes, assessment, teaching principles, and how it applies to students, teachers, schools, and families.',
  og='One learning framework for every Arena School program: learners make every decision, AI is a tool, and teachers and peers give the feedback.',
  hero_eyebrow='Our approach',
  h1='The learner does <em>the thinking.</em>',
  lede='One learning framework runs every Arena School program, for students, teachers, school leaders, and families. Learners make every decision, AI is a tool, and teachers and peers give the feedback.',
  cta1='Find the right program', cta2='See the framework',
  toc_label='On this page',
  toc=['Philosophy', 'Framework', 'Learning goals', 'Worked example', 'Outcomes', 'Assessment', 'Principles', 'By audience'],
  # 1
  ph_k='Philosophy', ph_h='Three human skills, <em>so AI does not do the thinking.</em>',
  ph_l='When AI can write an essay or code in seconds, what must learners still do? Three skills that AI cannot supply, and that learners have to practice.',
  skills=[
   ('I', 'Agency', 'Choosing what is worth doing, before anyone assigns it.', 'AI picks the problem, and learners follow.', 'isb-hq/isb-team-slide-800.webp', 'A team presents the problem it chose to solve',
    [('In school', 'When AI can help finish an assignment, the harder skill is setting the question, not answering it.'), ('At work', 'Tasks that only follow instructions are the easiest to hand to AI; people who define the problem direct the work.'), ('Over a career', 'A project a learner chose and saw through shows initiative in a way a transcript cannot.')]),
   ('II', 'Taste', 'Judging whether the output is actually good.', 'Learners accept the first answer AI gives.', 'isb-2026/mentor-feedback-800.webp', 'Mentors respond to a student’s work',
    [('In school', 'When every essay and project can look polished, telling strong work from weak becomes what teachers need to see.'), ('At work', 'Teams can generate ten versions in an hour; the person who picks the right one, and can say why, is the one they rely on.'), ('Over a career', 'Judgment compounds: it is what earns trust with larger decisions over time.')]),
   ('III', 'Craft', 'Finishing the work so people can trust it.', 'The work stays an unchecked first draft.', 'isb-2026/demo-laptop-800.webp', 'Students present a finished product',
    [('In school', 'A first draft is now instant; revising it into something reliable is where the learning happens.'), ('At work', 'Working products earn trust in a way prototypes and slide decks do not.'), ('Over a career', 'A record of finished work, with a live link, speaks for itself in applications and interviews.')]),
  ],
  without='Without it', changes='What it changes',
  ph_every='This is how we teach every learner: students, teachers, school leaders, and parents.',
  # 2
  fw_k='Framework', fw_h='The Arena School <em>learning framework.</em>',
  fw_l='Learners do the thinking, AI is a tool, and teachers and peers give the feedback.',
  fw_center='At the center, <em>the learner does the thinking.</em> We say learner on purpose: the same framework runs our student programs, our teacher training, and our sessions for school leaders and parents.',
  fw_mid_k='Four strands, in every program', fw_out_k='Four teaching principles',
  domains=['Inquiry and planning', 'Research and evaluation', 'Creating and communicating', 'Collaboration and reflection'],
  principles4=['In person, real-time feedback', 'AI use disclosed and cited', 'Learner voice and choice', 'An authentic audience'],
  fw_note='Built on project-based learning, informed by PBLWorks’ Gold Standard PBL: every strand gets a real purpose and a real audience, and AI speeds up the building. At every check-in, the teacher asks <q>How did you check it?</q> and responds in real time. AI can support that feedback, not replace it.',
  # 3
  go_k='Learning goals', go_h='Four domains, <em>in every program.</em>',
  go_l='The strands form a cycle, not a checklist: a project moves through all four, and back again.',
  goals=['Turn an interest into a focused question, and plan the work.', 'Check sources, including AI output, and choose on evidence.', 'Build and test a product with AI, and explain it clearly.', 'Use critique from teachers and peers to revise the work.'],
  # 4
  ex_k='Worked example', ex_h='Every learning goal, practiced on <em>real work for real people.</em>',
  ex_l='How a five-day student build week covers all four domains, as run at the International School of Beijing in summer 2026.',
  ex_goal_col='Learning goal', ex_ev_col='What students showed',
  days=[('Day 1', 'Pick a problem'), ('Day 2', 'Go public'), ('Day 3', 'The rebuild'), ('Day 4', 'Polish and price'), ('Day 5', 'Demo day')],
  ex_rows=[
   ('Turn an interest into a focused question', 1, 1, [(1, 'Pick a problem and a plan')], 'A plan and a first prototype', 'Day 1'),
   ('Check sources, including AI output', 1, 3, [(2, 'Test it with the people it’s for')], 'Choices backed by what users did', 'Days 1 to 3'),
   ('Build and test a product with AI', 2, 4, [(1, 'Ship it'), (3, 'Price it')], 'A live product at a public link', 'Days 2 to 4'),
   ('Use critique to revise the work', 3, 5, [(1, 'Rebuild it'), (3, 'Defend it')], 'A rebuilt product, and a pitch to judges', 'Days 3 to 5'),
  ],
  ex_foot='<b>No worksheet and no quiz.</b> The evidence is the work itself.',
  ex_link=('/programs/product-intensive', 'See the five-day Entrepreneurship &amp; AI Intensive'),
  # 5
  oc_k='Learning outcomes', oc_h='What learners <em>will be able to do.</em>',
  oc_l='Across every program, learners will be able to do the following.',
  outcomes=[
   ['Turn a broad interest into a focused, researchable question.', 'Plan a project with milestones, and adjust the plan based on progress.'],
   ['Find, evaluate, and cite sources, including checking the accuracy of AI output.', 'Compare options against criteria, and justify a choice.', 'Explain how AI tools work, where they fail, and the bias and privacy issues they raise.'],
   ['Build and test a product, prototype, or solution, deciding which steps to hand to AI and disclosing how they used it.', 'Structure an argument and write it clearly, in their own words.', 'Present to an authentic audience, and defend their reasoning under questioning.'],
   ['Work in a team, share roles, and contribute to a shared product.', 'Give and use critique from teachers and peers to revise their work.', 'Reflect on their process and on what they would do differently.'],
  ],
  oc_depth='Learners are whoever a program is for: students, teachers, school leaders, or parents. The outcomes stay the same; the depth grows.',
  # 6
  as_k='Assessment', as_h='We assess <em>the thinking behind it.</em>',
  as_l='We assess the process, not only the product: how a learner chose, checked, and finished the work.',
  crit_k='Sample criterion · Research and evaluation', crit_h='Evaluates sources, including AI output',
  levels=[('Beginning', 'Accepts sources and AI output as given; cites inconsistently.'), ('Developing', 'Checks some claims against a second source; cites most sources.'), ('Proficient', 'Verifies key claims, including AI output, against reliable sources; discloses AI use.'), ('Extending', 'Explains why sources disagree, corrects AI errors, and judges which evidence to trust.')],
  crit_foot='In practice: used with students in the ISB AI Founders Program, summer 2026. With a school, the rubrics stay with its team.',
  ev_k='Evidence we collect', evidence=['Process journal', 'Drafts', 'Recorded defense'],
  qs_k='Three questions do the coaching',
  qs=[('Agency', 'Why this problem?'), ('Taste', 'How do you know it’s good?'), ('Craft', 'What would make someone trust it?')],
  # 7
  pr_k='Principles', pr_h='How we teach, <em>in every program.</em>',
  pr_l='Four teaching principles from the framework, the split between AI and the learner, and the eight principles behind the three skills.',
  teach=[('In person, real-time feedback', 'Mentors and teachers sit with learners while they build, ask how they checked it, and respond on the spot.'),
         ('AI use disclosed and cited', 'Learners decide which steps to hand to AI, and say how they used it.'),
         ('Learner voice and choice', 'Learners choose the problem. Mentors support; they do not assign.'),
         ('An authentic audience', 'Work goes in front of real users, judges, and families, not a simulated audience.')],
  ai_k='AI tools and mentors handle', ai=['Writing the code', 'Putting it online', 'Fixing technical errors'],
  me_k='Learners decide', me=['Which problem, and for whom', 'What to cut after users try it', 'The name, the price, and the pitch'],
  eight_k='The eight principles behind the three skills',
  eight=[('I', 'Agency from day one.', 'Mentors support; learners choose.'), ('II', 'Make things in front of people.', 'Every day ends with a demo.'),
         ('III', 'Experienced mentors in the room.', 'Mentors are founders, engineers, and designers who have made real products.'),
         ('IV', 'AI as a partner learners direct.', 'Learners write the prompts, question the output, and check it for mistakes.'),
         ('V', 'Reflection, started early.', 'Thirty screen-free minutes a day on one question: which of my goals are my own?'),
         ('VI', 'Risk early, while it’s cheap.', 'Small, repeated risks make larger ones easier.'),
         ('VII', 'Daily habits, personal systems.', 'A three-line update every day: finished, learned, next.'),
         ('VIII', 'First-principles thinking.', 'Learners are assessed on asking how, why, what principle, when it fails, and how to adapt.')],
  day_k='The rhythm of a program day', day_l='The same rhythm runs in every format, from weekend sessions to five-day intensives.',
  day=[('Start', 'Lesson', 'Taught right before learners need it.'), ('Most of the day', 'Build', 'On a problem the team chose.'), ('During the build', 'Mentor 1:1s', 'Mentors sit with teams when they are stuck.'),
       ('Fixed hour', 'The freeze', 'Building stops; teams demo what works.'), ('Daily', 'Reflection', 'Thirty minutes with a notebook, no screens.'), ('End of day', 'Standup', 'Finished, learned, and next.'), ('Last day', 'Demo day', 'A live pitch to judges and families.')],
  # 8
  au_k='By audience', au_h='One framework, <em>four audiences.</em>',
  au_l='The goals and principles stay the same. What changes is the project, the depth, and the format.',
  tabs_label='Programs by audience', see='See the program',
  audiences=[
   ('Students', 'Grades 6 to 12, plus college and early career. Every student program ends in something real, made in front of real people.', [
     ('/programs/remake-your-favorite-app', 'App Design Workshop', 'Two days at school · Grades 6 to 9', ['Learn how software is made by taking a familiar app apart.', 'Direct AI coding tools, then test and judge the results.', 'Publish an app, and build the next tool for a hobby, a club, or a class.']),
     ('/programs/website-portfolio-workshop', 'College Portfolio Workshop', 'Two days at school · Grades 10 to 12', ['Judge which of their own work best represents them.', 'Plan, write, and design a real site; every word stays theirs.', 'Use it for college, summer program, scholarship, and internship applications.']),
     ('/programs/product-intensive', 'Entrepreneurship &amp; AI Intensive', 'Five days at school · Grades 7 to 12', ['Choose a real problem, talk to users, set a price, and pitch to a panel.', 'Use AI for research, building, and the brand, and decide what stays.', 'Carry the same steps into a passion project, a competition, or a class.']),
     ('/mentorship', 'Year-Long Project Mentorship', '1:1, six months to a year · Grades 7 to 12', ['Choose the problem and answer for the results.', 'Put the product in front of real users.', 'Take it past a first draft: test it, revise it, and make it good.']),
     ('/events/isb-winter-2027', 'AI Fundamentals for Students @ International School of Beijing', 'Four days, winter break', ['Learn AI tools for research, design, code, and video on their own project.', 'Choose a project worth making; every decision stays theirs.', 'Finish a working version anyone can open, tested with real people.']),
     ('/zero-to-launch', 'AI Advantage Bootcamp', 'Seven days · College and early career', ['Launch a live AI product with real users.', 'Build a project for the role they are applying to, and a portfolio.', 'Present the work on stage at demo day.'])]),
   ('Teachers', 'Teachers learn the way their students will: on their own work, with feedback in the room.', [
     ('/programs/teacher-training', 'AI for Educators', 'At your school', ['Bring one task from grading, planning, or differentiation, and leave with a tool made with AI.', 'Check every result, on the school’s approved tools.', 'Assess the process as well as the product when students also use AI.']),
     ('/programs/conferences', 'Conferences and Events', 'Talks, workshops, and panels', ['Use AI on their own lessons and materials, with help in the room.', 'See where AI helps, where it falls short, and how teachers keep decisions about teaching and assessment.']),
     ('/schools/technology', 'Technology teams', 'For tech coaches and IT', ['Train inside the school’s approved systems and child-protection policy.', 'Keep the session plans and teacher examples, to run again with the school’s coaches.'])]),
   ('Schools', 'For school leaders: programs planned around your calendar, with work to show for them.', [
     ('/schools', 'Working with schools', 'Students, teachers, and families', ['Start with one live session at a staff meeting you already hold.', 'Every program has clear learning goals and ends in a demo day or a live portfolio.', 'The curriculum, rubrics, and demo-day format stay with your team.']),
     ('/partnerships', 'Program partners', 'Camps, bootcamps, enrichment', ['Add a product track: problem selection, user research, building with AI, brand, pricing, and a final pitch.', 'Products stay live after the program.']),
     ('/programs/community-dialogues', 'Community Dialogues', 'Parent education at your school', ['A series of parent coffees and talks, agreed with school leaders beforehand.'])]),
   ('Families', 'For parents: what AI means for your child, and how to support the work at home.', [
     ('/programs/community-dialogues', 'Community Dialogues', 'Parent coffees and talks', ['How work is changing, from our team’s own work rather than predictions.', 'What students can now make, from real student projects.', 'Concrete ideas for supporting students in grades 6 to 12 at home.']),
     ('/mentorship', 'Year-Long Project Mentorship', 'Families enroll directly', ['One student, one project they choose, and personalized 1:1 mentorship.']),
     ('/events/isb-winter-2027', 'AI Fundamentals for Students @ International School of Beijing', 'Four days, winter break', ['No STEM background or coding needed.'])]),
  ],
  # close
  cl_k='Next step', cl_h='See the framework <em>in a program.</em>',
  cl_p='From two-day workshops to year-long mentorship, every Arena School program is built on this framework.',
  cl_b1='Find the right program', cl_b2='How we work with schools',
  cl_img_alt='Judges test a student product before scoring', cl_cap='Judges test each product before scoring, Beijing 2026',
 ),
}

# ---------- Chinese (JJ review) ----------
T['cn'] = dict(T['en'])
T['cn'].update(
  link=lambda p: (p + '-cn') if p not in ('/',) else '/index-cn',
  title='教学理念 · Arena School',
  desc='Arena School 的学习框架：思考由学习者自己完成。理念、四个学习目标领域、学习成果、评估方式、教学原则，以及它如何用于学生、老师、学校和家庭。',
  og='Arena School 每个项目都遵循同一套学习框架：决定由学习者来做，AI是工具，老师和同伴给出反馈。',
  hero_eyebrow='教学理念',
  h1='思考，<em>由学习者自己完成。</em>',
  lede='Arena School 的每一个项目，无论面向学生、老师、学校管理者还是家庭，都遵循同一套学习框架：决定由学习者来做，AI是工具，老师和同伴给出反馈。',
  cta1='找到合适的项目', cta2='查看学习框架',
  toc_label='本页内容',
  toc=['理念', '学习框架', '学习目标', '实例', '学习成果', '评估', '教学原则', '面向对象'],
  ph_k='理念', ph_h='三种人的能力，<em>让AI不替人思考。</em>',
  ph_l='当AI几秒钟就能写文章、写代码，学习者还必须会做什么？答案是三种AI给不了、必须亲手练出来的能力。',
  skills=[
   ('I', '主动性', '在任何人布置之前，自己选出值得做的事。', '问题由AI来挑，学习者只是跟着走。', 'isb-hq/isb-team-slide-800.webp', '一个团队介绍自己选定要解决的问题',
    [('在学校', '当AI能帮学生完成作业，更难得的能力是提出问题，而不是回答问题。'), ('在工作中', '只会照指令办事的工作最容易被AI接手；能界定问题的人，才能主导工作。'), ('在职业生涯中', '一个自己选定并坚持做完的项目，比成绩单更能说明一个人的主动性。')]),
   ('II', '审美', '判断做出来的东西是否真的好。', '学习者照单全收AI给出的第一个答案。', 'isb-2026/mentor-feedback-800.webp', '导师对学生的作品给出反馈',
    [('在学校', '当每篇文章、每个项目都能做得光鲜，老师真正想看到的，是分辨好坏的能力。'), ('在工作中', '团队一小时就能生成十个版本；能挑出对的那一个并说清理由的人，才是大家倚重的人。'), ('在职业生涯中', '判断力会不断累积：久而久之，它让一个人赢得信任，担起更重大的决定。')]),
   ('III', '匠心', '把事情做完，做到让人信得过。', '作品停留在没有检查过的初稿。', 'isb-2026/demo-laptop-800.webp', '学生展示做完的产品',
    [('在学校', '初稿如今唾手可得；把它反复打磨成可靠的作品，才是真正学到东西的过程。'), ('在工作中', '真正能用的产品，比原型和幻灯片更能赢得信任。'), ('在职业生涯中', '一串做完的作品，附上能打开的链接，在申请和面试中就是最好的证明。')]),
  ],
  without='缺少它', changes='它带来的改变',
  ph_every='我们用同样的方式教每一位学习者：学生、老师、学校管理者和家长。',
  fw_k='学习框架', fw_h='Arena School <em>学习框架</em>',
  fw_l='思考由学习者完成，AI是工具，老师和同伴给出反馈。',
  fw_center='框架的中心，<em>是学习者自己思考。</em>我们特意说“学习者”：同一套框架贯穿我们的学生项目、教师培训，以及面向学校管理者和家长的活动。',
  fw_mid_k='每个项目都培养的四条主线', fw_out_k='四条教学原则',
  domains=['探究与规划', '研究与评估', '创作与表达', '协作与反思'],
  principles4=['面对面，即时反馈', '使用AI须说明并注明', '学习者的声音与选择', '真实的受众'],
  fw_note='以项目式学习为基础，参考 PBLWorks 的 Gold Standard PBL：每条主线都有真实的目的和真实的受众，AI让动手做的过程更快。每次检查进度，老师都会问：<q>你是怎么验证的？</q>并当场回应。AI可以辅助这样的反馈，但不能取代它。',
  go_k='学习目标', go_h='四个领域，<em>贯穿每个项目。</em>',
  go_l='四条主线是一个循环，而不是一张清单：一个项目会走完这四步，再回到起点。',
  goals=['把兴趣聚焦成一个具体的问题，并规划工作。', '核查资料来源，包括AI的输出，依据证据做选择。', '借助AI做出并测试产品，并清楚地讲明白。', '利用老师和同伴的批评意见修改作品。'],
  ex_k='实例', ex_h='每个学习目标，<em>都在为真实的人做真实的事中练习。</em>',
  ex_l='一个为期五天的学生实战周如何覆盖全部四个领域：2026年夏天在北京顺义国际学校的实践。',
  ex_goal_col='学习目标', ex_ev_col='学生拿出的成果',
  days=[('第1天', '选定问题'), ('第2天', '公开上线'), ('第3天', '推倒重来'), ('第4天', '打磨与定价'), ('第5天', '路演日')],
  ex_rows=[
   ('把兴趣聚焦成一个具体的问题', 1, 1, [(1, '选题，定计划')], '一份计划和第一个原型', '第1天'),
   ('核查资料来源，包括AI的输出', 1, 3, [(2, '拿给真正的用户试用')], '依据用户真实行为做出的选择', '第1至3天'),
   ('借助AI做出并测试产品', 2, 4, [(1, '上线'), (3, '定价')], '一个公开网址上可用的产品', '第2至4天'),
   ('利用批评意见修改作品', 3, 5, [(1, '重做'), (3, '答辩')], '重做后的产品，以及面向评委的路演', '第3至5天'),
  ],
  ex_foot='<b>没有练习卷，也没有小测验。</b>作品本身就是证据。',
  ex_link=('/programs/product-intensive', '了解为期五天的创业与AI集训营'),
  oc_k='学习成果', oc_h='学习者<em>将能够做到</em>',
  oc_l='在每一个项目中，学习者将能够：',
  outcomes=[
   ['把宽泛的兴趣转化为一个聚焦、可研究的问题。', '为项目设定里程碑，并根据进展调整计划。'],
   ['查找、评估并注明资料来源，包括核查AI输出的准确性。', '依据标准比较不同方案，并说明选择的理由。', '解释AI工具如何运作、在哪里会出错，以及它带来的偏见和隐私问题。'],
   ['做出并测试一个产品、原型或解决方案，决定哪些步骤交给AI，并说明自己如何使用了AI。', '组织论点，用自己的话清楚地写出来。', '面向真实的受众展示，并在提问中为自己的思路辩护。'],
   ['在团队中分工合作，为共同的作品出力。', '给出并利用老师和同伴的批评意见来修改作品。', '反思自己的过程，以及下次会怎样做得不同。'],
  ],
  oc_depth='“学习者”指项目面向的任何人：学生、老师、学校管理者或家长。学习成果不变，深度逐步加深。',
  as_k='评估', as_h='我们评估的，<em>是背后的思考。</em>',
  as_l='我们评估过程，而不只是结果：学习者如何选择、如何验证、如何把工作做完。',
  crit_k='评估标准示例 · 研究与评估', crit_h='评估资料来源，包括AI的输出',
  levels=[('起步', '照单全收资料和AI的输出；注明来源不一致。'), ('发展', '会用第二个来源核对部分说法；大多数来源有注明。'), ('熟练', '用可靠来源核实关键说法，包括AI的输出；说明自己如何使用AI。'), ('拓展', '能解释不同来源为何说法不一，纠正AI的错误，并判断该相信哪些证据。')],
  crit_foot='实践：2026年夏天用于北京顺义国际学校 ISB AI Founders Program 的学生。与学校合作时，评估标准留给学校团队。',
  ev_k='我们收集的证据', evidence=['过程日志', '各版草稿', '答辩录像'],
  qs_k='三个问题，就是最好的指导',
  qs=[('主动性', '为什么选这个问题？'), ('审美', '你怎么知道它好？'), ('匠心', '怎样才能让别人信得过它？')],
  pr_k='教学原则', pr_h='我们怎样教，<em>每个项目都一样。</em>',
  pr_l='学习框架中的四条教学原则、AI与学习者之间的分工，以及支撑三种能力的八条原则。',
  teach=[('面对面，即时反馈', '导师和老师在学习者动手时就坐在旁边，问他们是怎么验证的，并当场回应。'),
         ('使用AI须说明并注明', '哪些步骤交给AI由学习者决定，并说明自己如何使用了AI。'),
         ('学习者的声音与选择', '问题由学习者自己选。导师提供支持，不布置题目。'),
         ('真实的受众', '作品要面对真实的用户、评委和家长，而不是模拟的观众。')],
  ai_k='交给AI工具和导师的', ai=['写代码', '把产品上线', '修复技术错误'],
  me_k='由学习者决定的', me=['做哪个问题，为谁而做', '用户试用后砍掉什么', '产品的名字、价格和路演'],
  eight_k='支撑三种能力的八条原则',
  eight=[('I', '从第一天起自己做主。', '导师提供支持，方向由学习者决定。'), ('II', '边做边展示。', '每天都以一次演示收尾。'),
         ('III', '经验丰富的导师就在现场。', '导师是真正做出过产品的创始人、工程师和设计师。'),
         ('IV', 'AI是伙伴，主导权在学习者。', '学习者自己写提示词、追问AI给出的结果，并找出其中的错误。'),
         ('V', '尽早开始反思。', '每天三十分钟离开屏幕，只思考一个问题：哪些目标是我自己真正想要的？'),
         ('VI', '趁代价小，尽早冒险。', '一次次小冒险，会让更大的冒险变得容易。'),
         ('VII', '养成习惯，建立自己的方法。', '每天写三行进度：完成了什么、学到了什么、下一步做什么。'),
         ('VIII', '从第一性原理出发。', '评估看的是学习者能否追问：怎么做、为什么、依据什么原理、何时会失效、如何调整。')],
  day_k='项目中典型的一天', day_l='从周末课程到五天集训，每种形式都遵循同样的节奏。',
  day=[('开始', '方法课', '赶在学习者用得上之前讲。'), ('一天的大部分时间', '开发', '围绕团队自选的问题。'), ('开发期间', '导师一对一', '团队卡住时，导师坐下来一起分析。'),
       ('固定时刻', '封版', '停止开发，各队演示已经跑通的部分。'), ('每天', '反思', '三十分钟，一本笔记本，不看屏幕。'), ('一天结束', '站会', '完成了什么、学到了什么、下一步做什么。'), ('最后一天', '路演日', '向评委和家长现场路演。')],
  au_k='面向对象', au_h='一套框架，<em>四类学习者。</em>',
  au_l='目标和原则不变，变化的是项目、深度和形式。',
  tabs_label='按对象查看项目', see='查看项目',
  audiences=[
   ('学生', '面向6至12年级，以及大学生和职场新人。每个学生项目都以一件真实的作品收尾，在真实的人面前完成。', [
     ('/programs/remake-your-favorite-app', '应用设计工作坊', '在校两天 · 6至9年级', ['拆解一款熟悉的应用，了解软件是怎样做出来的。', '指挥AI编程工具，再亲自测试和判断结果。', '发布一款应用，并能为爱好、社团或课程做出下一个工具。']),
     ('/programs/website-portfolio-workshop', '升学作品集工作坊', '在校两天 · 10至12年级', ['判断哪些作品最能代表自己。', '规划、撰写并设计一个真正的网站，每个字都出自自己。', '用于大学、暑期项目、奖学金和实习申请。']),
     ('/programs/product-intensive', '创业与AI集训营', '在校五天 · 7至12年级', ['选一个真实的问题，访谈用户，定价，并向评审团路演。', '用AI做调研、开发和品牌，由自己决定留下什么。', '把同样的步骤用到兴趣项目、比赛或课程作业中。']),
     ('/mentorship', '学年项目导师计划', '一对一，六个月到一年 · 7至12年级', ['自己选定问题，并为结果负责。', '把产品放到真实用户面前。', '走过初稿阶段：测试、修改，把它做好。']),
     ('/events/isb-winter-2027', '学生AI基础营 · 北京顺义国际学校', '寒假四天', ['在自己的项目中学习用于调研、设计、编程和视频的AI工具。', '选一个值得做的项目，每个决定都由自己做。', '做出任何人都能打开的可用版本，并经过真实用户测试。']),
     ('/zero-to-launch', 'AI职场先发营', '七天 · 大学生与职场新人', ['上线一款有真实用户的AI产品。', '为想申请的岗位做一个项目，并整理作品集。', '在路演日登台展示自己的作品。'])]),
   ('老师', '老师的学习方式与学生一样：用自己的工作练，现场有人给反馈。', [
     ('/programs/teacher-training', '教育者AI培训', '在贵校开展', ['带来一项批改、备课或分层教学的任务，带走一个用AI做出的工具。', '在学校批准的工具上，核查每一个结果。', '当学生也在用AI时，评估过程，而不只是结果。']),
     ('/programs/conferences', '会议与活动', '主题分享、工作坊和圆桌', ['用自己的课程和教学材料上手AI，现场有专人协助。', '了解AI在哪里有帮助、在哪里力有不逮，以及老师如何守住教学和评估的决定权。']),
     ('/schools/technology', '技术团队', '面向技术教练和IT团队', ['在学校批准的系统和儿童保护政策之内开展培训。', '留下课程方案和教师案例，由学校的技术教练再次开展。'])]),
   ('学校', '面向学校管理者：围绕学校日程规划项目，并有成果可以展示。', [
     ('/schools', '与学校合作', '面向学生、老师和家庭', ['从一次教职工会议上的现场分享开始。', '每个项目都有清晰的学习目标，并以路演日或在线作品集收尾。', '课程、评估标准和路演日形式都留给学校团队。']),
     ('/partnerships', '项目合作', '营地、训练营和素质教育机构', ['加入产品实战模块：选题、用户调研、用AI开发、品牌、定价和最终路演。', '项目结束后，产品依然在线。']),
     ('/programs/community-dialogues', '社区对话', '在贵校开展的家长教育', ['家长咖啡会和主题分享系列，事先与学校管理者商定。'])]),
   ('家庭', '面向家长：AI对孩子意味着什么，以及在家如何支持孩子。', [
     ('/programs/community-dialogues', '社区对话', '家长咖啡会和主题分享', ['工作正在怎样变化，来自我们团队自己的工作，而不是预测。', '学生现在能做出什么，来自真实的学生项目。', '在家支持6至12年级学生的具体做法。']),
     ('/mentorship', '学年项目导师计划', '家庭直接报名', ['一名学生，一个自己选定的项目，加上一对一的个性化导师指导。']),
     ('/events/isb-winter-2027', '学生AI基础营 · 北京顺义国际学校', '寒假四天', ['不需要理工科背景，也不需要编程基础。'])]),
  ],
  cl_k='下一步', cl_h='在具体项目中，<em>看见这套框架。</em>',
  cl_p='从两天的工作坊到学年项目导师计划，Arena School 的每一个项目都建立在这套框架之上。',
  cl_b1='找到合适的项目', cl_b2='了解我们如何与学校合作',
  cl_img_alt='评委在打分前亲自试用学生的产品', cl_cap='评委在打分前逐一试用产品，北京，2026年',
)


def head(t, k, h, l=None, cls='sec-head pg-head reveal'):
    lede = '<p class="lede">%s</p>' % l if l else ''
    return '<div class="%s"><span class="eyebrow">%s</span><h2 class="h2 h2-md">%s</h2>%s</div>' % (cls, k, h, lede)


def body(lang):
    t = T[lang]
    L = t['link']
    ids = ['philosophy', 'framework', 'goals', 'example', 'outcomes', 'assessment', 'principles', 'audiences']
    o = []
    jj = '<!-- JJ review: Approach page CN copy (APPROACH-BRIEF, Oct 16, 2026) -->\n' if lang == 'cn' else ''
    o.append(jj + '<nav class="ap-toc" aria-label="%s"><div class="container"><ol>%s</ol></div></nav>' % (
        t['toc_label'], ''.join('<li><a href="#%s"><b>%d</b>%s</a></li>' % (i, n + 1, x) for n, (i, x) in enumerate(zip(ids, t['toc'])))))
    # 1 philosophy
    cards = []
    for num, name, d, w, img, alt, ch in t['skills']:
        lis = ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in ch)
        cards.append('<article class="ap-skill reveal"><figure><img src="/photos/%s" alt="%s" loading="lazy" decoding="async" width="800" height="533" /><span>%s</span></figure>'
                     '<div class="ap-skill-body"><h3>%s</h3><p class="ap-skill-def">%s</p><p class="ap-without"><b>%s:</b> %s</p>'
                     '<details><summary>%s</summary><ol>%s</ol></details></div></article>' % (img, alt, num, name, d, t['without'], w, t['changes'], lis))
    o.append('<section class="zl-section ap2" id="philosophy" data-screen-label="Philosophy"><div class="container">%s<div class="ap-skills">%s</div><p class="ap-every reveal">%s</p></div></section>'
             % (head(t, t['ph_k'], t['ph_h'], t['ph_l']), ''.join(cards), t['ph_every']))
    # 2 framework
    mid = ''.join('<li><i aria-hidden="true" style="background:%s"></i>%s</li>' % (DOM_COLORS[i], x) for i, x in enumerate(t['domains']))
    out = ''.join('<li><i aria-hidden="true"></i>%s</li>' % x for x in t['principles4'])
    o.append('<section class="zl-section section-alt ap2" id="framework" data-screen-label="Framework"><div class="container">%s'
             '<div class="ap-fw"><div class="ap-wheel reveal">%s</div><div class="ap-fw-text reveal"><p class="ap-fw-center">%s</p>'
             '<div class="ap-fw-lists"><div><span class="ap-k">%s</span><ol>%s</ol></div><div class="is-out"><span class="ap-k">%s</span><ol>%s</ol></div></div>'
             '<p class="ap-fw-note">%s</p></div></div></div></section>'
             % (head(t, t['fw_k'], t['fw_h'], t['fw_l']), wheel_svg(lang), t['fw_center'], t['fw_mid_k'], mid, t['fw_out_k'], out, t['fw_note']))
    # 3 goals
    doms = ''.join('<li class="ap-domain reveal" style="--dom:%s"><span class="ap-num" aria-hidden="true">0%d</span><h3>%s</h3><p>%s</p></li>'
                   % (DOM_COLORS[i], i + 1, t['domains'][i], g) for i, g in enumerate(t['goals']))
    o.append('<section class="zl-section ap2" id="goals" data-screen-label="Learning goals"><div class="container">%s<ol class="ap-domains" style="list-style:none;margin:0;padding:0">%s</ol></div></section>'
             % (head(t, t['go_k'], t['go_h'], t['go_l']), doms))
    # 4 worked example (a real table; it stacks into cards on phones)
    ths = ''.join('<th scope="col"><b>%s</b>%s</th>' % d for d in t['days'])
    rows = []
    for i, (goal, a, b, labels, ev, dayk) in enumerate(t['ex_rows']):
        pre = ''.join('<td class="pad"></td>' for _ in range(a - 1))
        post = ''.join('<td class="pad"></td>' for _ in range(5 - b))
        ems = ''.join('<em style="--c:%d">%s</em>' % (c, x) for c, x in labels)
        rows.append('<tr><th scope="row"><b>%s</b><span>%s</span></th>%s<td colspan="%d"><div class="ap-span" style="--n:%d"><span class="ap-days">%s</span>%s</div></td>%s<td class="ev" data-k="%s">%s</td></tr>'
                    % (t['domains'][i], goal, pre, b - a + 1, b - a + 1, dayk, ems, post, t['ex_ev_col'], ev))
    o.append('<section class="zl-section section-alt ap2" id="example" data-screen-label="Worked example"><div class="container">%s'
             '<div class="ap-ex-wrap reveal"><table class="ap-ex"><colgroup><col class="c-goal" /><col /><col /><col /><col /><col /><col class="c-ev" /></colgroup>'
             '<thead><tr><th scope="col">%s</th>%s<th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>'
             '<p class="ap-ex-foot reveal"><span>%s</span><a class="tlink" href="%s">%s →</a></p></div></section>'
             % (head(t, t['ex_k'], t['ex_h'], t['ex_l']), t['ex_goal_col'], ths, t['ex_ev_col'], ''.join(rows), t['ex_foot'], L(t['ex_link'][0]), t['ex_link'][1]))
    # 5 outcomes
    cols = ''.join('<div><h3>%s</h3><ul>%s</ul></div>' % (t['domains'][i], ''.join('<li>%s</li>' % x for x in items)) for i, items in enumerate(t['outcomes']))
    o.append('<section class="zl-section ap2" id="outcomes" data-screen-label="Outcomes"><div class="container">%s<div class="ap-outcomes reveal">%s</div><p class="ap-depth reveal">%s</p></div></section>'
             % (head(t, t['oc_k'], t['oc_h'], t['oc_l']), cols, t['oc_depth']))
    # 6 assessment
    lv = ''.join('<li style="--l:%d"><b>%s</b><i aria-hidden="true"></i>%s</li>' % (i + 1, a, b) for i, (a, b) in enumerate(t['levels']))
    ev = ''.join('<li>%s</li>' % x for x in t['evidence'])
    qs = ''.join('<li><b>%s</b><q>%s</q></li>' % q for q in t['qs'])
    o.append('<section class="zl-section section-alt ap2" id="assessment" data-screen-label="Assessment"><div class="container">%s<div class="ap-assess">'
             '<div class="ap-crit reveal"><div class="ap-crit-head"><span class="ap-k">%s</span><h3>%s</h3></div><ol>%s</ol><p class="ap-crit-foot">%s</p></div>'
             '<div class="ap-side reveal"><div class="ap-card"><span class="ap-k">%s</span><ul class="ap-ev">%s</ul></div><div class="ap-card"><span class="ap-k">%s</span><ul class="ap-qs">%s</ul></div></div>'
             '</div></div></section>' % (head(t, t['as_k'], t['as_h'], t['as_l']), t['crit_k'], t['crit_h'], lv, t['crit_foot'], t['ev_k'], ev, t['qs_k'], qs))
    # 7 principles (+ the existing day timeline, approach-extra.js animates it)
    teach = ''.join('<li class="reveal"><h3>%s</h3><p>%s</p></li>' % x for x in t['teach'])
    eight = ''.join('<li><b>%s</b><span><strong>%s</strong> %s</span></li>' % x for x in t['eight'])
    day = ''.join('<li class="ap-tl-item" style="--i:%d"><span class="ap-tl-time">%s</span><span class="ap-tl-node" aria-hidden="true"></span><span class="ap-tl-title">%s</span><p class="ap-tl-desc">%s</p></li>'
                  % (i, a, b, c) for i, (a, b, c) in enumerate(t['day']))
    o.append('<section class="zl-section ap2" id="principles" data-screen-label="Principles"><div class="container">%s<ol class="ap-teach">%s</ol>'
             '<div class="ap-split reveal"><div><span class="ap-k">%s</span><ul>%s</ul></div><div class="is-learner"><span class="ap-k">%s</span><ul>%s</ul></div></div>'
             '<div class="ap-eight-wrap reveal"><span class="ap-k">%s</span><ol class="ap-eight">%s</ol></div>'
             '<div class="ap-day-head reveal"><span class="ap-k">%s</span><p class="ap-p" style="margin-top:6px">%s</p></div>'
             '<div class="ap-timeline-wrap reveal"><ol class="ap-timeline" data-ap-timeline style="--n:7">%s</ol></div></div></section>'
             % (head(t, t['pr_k'], t['pr_h'], t['pr_l']), teach, t['ai_k'], ''.join('<li>%s</li>' % x for x in t['ai']), t['me_k'], ''.join('<li>%s</li>' % x for x in t['me']),
                t['eight_k'], eight, t['day_k'], t['day_l'], day))
    # 8 by audience (tabs)
    tabs, panels = [], []
    for n, (name, intro, progs) in enumerate(t['audiences']):
        sel = n == 0
        tabs.append('<button type="button" class="el-tab" role="tab" id="ap-t%d" aria-controls="ap-p%d" aria-selected="%s"%s><small>0%d</small>%s</button>'
                    % (n, n, 'true' if sel else 'false', '' if sel else ' tabindex="-1"', n + 1, name))
        cards = ''.join('<li class="ap-prog"><span class="ap-k">%s</span><h3>%s</h3><ul>%s</ul><a class="tlink" href="%s">%s →</a></li>'
                        % (fmt, title, ''.join('<li>%s</li>' % x for x in outs), L(href), t['see']) for href, title, fmt, outs in progs)
        panels.append('<div class="el-tabpanel" role="tabpanel" id="ap-p%d" aria-labelledby="ap-t%d" style="padding-top:24px"%s><p class="ap-aud-intro">%s</p><ul class="ap-progs">%s</ul></div>'
                      % (n, n, '' if sel else ' hidden', intro, cards))
    o.append('<section class="zl-section section-alt ap2" id="audiences" data-screen-label="By audience"><div class="container">%s'
             '<div class="el-tabs reveal" role="tablist" aria-label="%s" data-el-tabs>%s</div>%s</div></section>'
             % (head(t, t['au_k'], t['au_h'], t['au_l']), t['tabs_label'], ''.join(tabs), ''.join(panels)))
    # newsletter band + close
    o.append('<section class="nl-band" data-nl="approach"></section>')
    o.append('<section class="pp-final" data-screen-label="Next step"><div class="container"><div class="pp-final-top reveal"><div>'
             '<span class="eyebrow">%s</span><h2 class="h2 h2-md">%s</h2><p class="pp-close-sub">%s</p>'
             '<div class="pp-close-cta"><a href="%s#programs" class="btn btn-primary">%s <span class="arr">→</span></a><a href="%s" class="btn btn-ghost">%s</a></div></div>'
             '<figure class="pp-close-photo"><img src="/photos/isb-hq/isb-judges-test-800.webp" srcset="/photos/isb-hq/isb-judges-test-800.webp 800w, /photos/isb-hq/isb-judges-test-1400.webp 1400w" sizes="(max-width: 900px) 100vw, 50vw" alt="%s" loading="lazy" decoding="async" />'
             '<figcaption><img loading="lazy" decoding="async" src="/logos/arena/seal-ivory-256.png" alt="" width="18" height="18" />%s</figcaption></figure></div></div></section>'
             % (t['cl_k'], t['cl_h'], t['cl_p'], '/index-cn' if lang == 'cn' else '/', t['cl_b1'], L('/schools'), t['cl_b2'], t['cl_img_alt'], t['cl_cap']))
    return '<!-- ap2:start -->\n' + '\n'.join(o) + '\n<!-- ap2:end -->'


def apply(path, lang):
    t = T[lang]
    s = open(path, encoding='utf-8').read()
    n0 = s
    # body: everything after the hero section up to </main>
    if '<!-- ap2:start -->' in s:
        s = re.sub(r'(?s)<!-- ap2:start -->.*?<!-- ap2:end -->', lambda m: body(lang), s)
    else:
        i = s.index('</section>', s.index('cine-hero')) + len('</section>')
        j = s.index('</main>')
        s = s[:i] + '\n\n' + body(lang) + '\n\n' + s[j:]
    # hero copy
    s = re.sub(r'(<div class="hero-eyebrow-row reveal"><span class="eyebrow">)[^<]*(</span>)', lambda m: m.group(1) + t['hero_eyebrow'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<h1 class="display reveal cs-h1">).*?(</h1>)', lambda m: m.group(1) + t['h1'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<p class="lede sub reveal lede-56">).*?(</p>)', lambda m: m.group(1) + t['lede'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<div class="pp-hero-cta reveal">).*?(</div>)', lambda m: m.group(1) + '<a href="%s#programs" class="btn btn-primary">%s <span class="arr">→</span></a><a href="#framework" class="btn btn-ghost">%s</a>'
               % ('/index-cn' if lang == 'cn' else '/', t['cta1'], t['cta2']) + m.group(2), s, count=1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % t['title'], s, count=1)
    for attr, val in (('name="description"', t['desc']), ('property="og:description"', t['og']), ('name="twitter:description"', t['og'])):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + E(val) + m.group(2), s, count=1)
    # stylesheets and the tabs script
    if '/css/approach.css' not in s:
        s = s.replace('<link rel="stylesheet" href="/css/approach-extra.css', '<link rel="stylesheet" href="/css/elegance.css?v=1" />\n<link rel="stylesheet" href="/css/approach.css?v=1" />\n<link rel="stylesheet" href="/css/approach-extra.css', 1)
    if '/elegance.js' not in s:
        import hashlib
        v = hashlib.md5(open(os.path.join(ROOT, 'elegance.js'), 'rb').read()).hexdigest()[:8]
        s = s.replace('<script src="/approach-extra.js', '<script src="/elegance.js?v=%s" defer></script>\n<script src="/approach-extra.js' % v, 1)
    return s, s != n0


if __name__ == '__main__':
    check = '--check' in sys.argv
    changed = 0
    for path, lang in (('approach.html', 'en'), ('approach-cn.html', 'cn')):
        p = os.path.join(ROOT, path)
        s, ch = apply(p, lang)
        if ch:
            changed += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(s)
    print(('Would change' if check else 'Changed') + ' %d pages' % changed)
