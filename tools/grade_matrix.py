"""Homepage "Where each program fits" as an editorial matrix (EDITORIAL-BRIEF, Oct 16, 2026), EN and CN.

Replaces the old pill/Gantt lanes with a real table on the ds-mx component (css/ds.css + css/grades.css): grade
columns grouped under school stages, a filled mark for every grade a program serves, a hairline joining them, the
program name and grade range in the first column (a link to the program). grade-map.js spotlights rows
(.gmx-row). Phones: one block per program with an 8-column mark strip under the name.
  python3 tools/grade_matrix.py           write index.html and index-cn.html
  python3 tools/grade_matrix.py --check   report pages that would change
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA = {
 'index.html': dict(
   k='Where each program fits', note='Grades 6 to 12, plus college and early career', aria='Which grades each program serves', col='Program',
   stages=[('Middle school', 3), ('High school', 4), ('After high school', 1)], grades=['6', '7', '8', '9', '10', '11', '12', 'College'],
   rows=[('remake', '/programs/remake-your-favorite-app', 1, 4, 'App Design Workshop', 'Grades 6 to 9'),
         ('portfolio', '/programs/website-portfolio-workshop', 5, 7, 'College Portfolio Workshop', 'Grades 10 to 12'),
         ('intensive', '/programs/product-intensive', 2, 7, 'Entrepreneurship &amp; AI Intensive', 'Grades 7 to 12'),
         ('mentorship', '/mentorship', 2, 7, 'Year-Long Project Mentorship', 'Grades 7 to 12'),
         ('bootcamp', '/zero-to-launch', 8, 8, 'AI Advantage Bootcamp', 'College &amp; early career')]),
 'index-cn.html': dict(
   k='各项目适合的阶段', note='初中到高中，以及大学生与职场新人', aria='各项目适合的年级', col='项目',
   stages=[('初中', 3), ('高中', 4), ('毕业后', 1)], grades=['6', '7', '8', '9', '10', '11', '12', '大学'],
   rows=[('remake', '/programs/remake-your-favorite-app-cn', 1, 4, '应用设计工作坊', '6至9年级'),
         ('portfolio', '/programs/website-portfolio-workshop-cn', 5, 7, '升学作品集工作坊', '10至12年级'),
         ('intensive', '/programs/product-intensive-cn', 2, 7, '创业与AI集训营', '7至12年级'),
         ('mentorship', '/mentorship-cn', 2, 7, '学年项目导师计划', '7至12年级'),
         ('bootcamp', '/zero-to-launch-cn', 8, 8, 'AI职场先发营', '大学生与职场新人')]),
}


def build(d):
    stage_row = '<tr class="gmx-stages"><td></td>%s</tr>' % ''.join('<th scope="colgroup" colspan="%d">%s</th>' % (n, s) for s, n in d['stages'])
    head = '<tr><th scope="col">%s</th>%s</tr>' % (d['col'], ''.join('<th scope="col">%s</th>' % g for g in d['grades']))
    rows = []
    for i, (prog, href, a, b, name, span) in enumerate(d['rows']):
        cells = []
        for c in range(1, 9):
            cls = []
            if a <= c <= b:
                cls += ['in', 'on']
                if c == a: cls.append('first')
                if c == b: cls.append('last')
                cells.append('<td class="%s"><i class="ds-mk" aria-hidden="true"></i><span class="vh">%s</span></td>' % (' '.join(cls), d['grades'][c - 1]))
            else:
                cells.append('<td></td>')
        rows.append('<tr class="gmx-row" data-prog="%s" style="--i:%d"><th scope="row"><a href="%s"><b>%s</b><span>%s</span></a></th>%s</tr>'
                    % (prog, i, href, name, span, ''.join(cells)))
    return ('<!-- gmx:start -->\n<div class="gmap gmx reveal" data-lint-skip aria-label="%s" data-gmap><div class="gm-head"><span class="ds-eyebrow">%s</span><span class="gm-note">%s</span></div>'
            '<div class="ds-mx-wrap"><table class="ds-mx ds-gmx"><colgroup><col class="c-name" /><col span="7" /><col class="c-col" /></colgroup><thead>%s%s</thead><tbody>%s</tbody></table></div></div>\n<!-- gmx:end -->'
            % (d['aria'], d['k'], d['note'], stage_row, head, ''.join(rows)))


def apply(s, d):
    block = build(d)
    if '<!-- gmx:start -->' in s:
        return re.sub(r'(?s)<!-- gmx:start -->.*?<!-- gmx:end -->', lambda m: block, s)
    i = s.find('<div class="gmap')
    j = s.find('</div></div>', s.find('data-prog="bootcamp" href', i)) + len('</div></div>')
    return s[:i] + block + s[j:]


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for f, d in DATA.items():
        p = os.path.join(ROOT, f)
        s = open(p, encoding='utf-8').read()
        t = apply(s, d)
        if t != s:
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
