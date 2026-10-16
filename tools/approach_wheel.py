"""Approach page: the Arena School learning framework wheel as inline SVG (EN and CN).

Center: the learner does the thinking. Inner ring: the four learning-goal domains, a cycle (arrowheads
between segments). Outer ring: the four teaching principles, offset 45 degrees. Labels run on arcs and
read upright on both halves. css/approach.css stages the reveal and turns the dashed cycle orbit slowly.
The SVG is decorative for assistive tech (aria-hidden): the page lists the same eight items as text.

  python3 tools/approach_wheel.py en|cn   prints the <svg> element
"""
import math
import sys

C = 300                      # center (viewBox 0 0 600 600)
OUT = (226, 292)             # outer ring radii
MID = (140, 218)             # inner ring radii
CORE = 126
GAP = 1.6                    # degrees left empty between segments

LABELS = {
    'en': {
        'core': ['The learner', 'does the', 'thinking'],
        'mid': ['Inquiry and planning', 'Research and evaluation', 'Creating and communicating', 'Collaboration and reflection'],
        'out': ['In person, real-time feedback', 'AI use disclosed and cited', 'Learner voice and choice', 'An authentic audience'],
        'mid_size': 13.5, 'out_size': 13, 'core_size': 27,
    },
    'cn': {
        'core': ['思考', '由学习者', '自己完成'],
        'mid': ['探究与规划', '研究与评估', '创作与表达', '协作与反思'],
        'out': ['面对面，即时反馈', '使用AI须说明并注明', '学习者的声音与选择', '真实的受众'],
        'mid_size': 15, 'out_size': 14, 'core_size': 27,
    },
}
MID_FILL = ['#22458A', '#2F55A8', '#1E3F86', '#3A63B8']


def pt(r, deg):
    a = math.radians(deg)
    return C + r * math.cos(a), C + r * math.sin(a)


def sector(r0, r1, a0, a1):
    (x0, y0), (x1, y1) = pt(r1, a0), pt(r1, a1)
    (x2, y2), (x3, y3) = pt(r0, a1), pt(r0, a0)
    large = 1 if a1 - a0 > 180 else 0
    return ('M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z'
            % (x0, y0, r1, r1, large, x1, y1, x2, y2, r0, r0, large, x3, y3))


def arc(r, a0, a1):
    """Text baseline arc: clockwise on the upper half; counter-clockwise on the lower half so text stays upright."""
    mid = (a0 + a1) / 2 % 360
    if 0 < mid < 180:
        (x0, y0), (x1, y1) = pt(r, a1), pt(r, a0)
        return 'M%.1f %.1f A%d %d 0 0 0 %.1f %.1f' % (x0, y0, r, r, x1, y1)
    (x0, y0), (x1, y1) = pt(r, a0), pt(r, a1)
    return 'M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (x0, y0, r, r, x1, y1)


def svg(lang):
    L = LABELS[lang]
    defs, out, mid, core = [], [], [], []
    # outer ring: principles centered on top, right, bottom, left
    for i, label in enumerate(L['out']):
        c = -90 + 90 * i
        a0, a1 = c - 45 + GAP, c + 45 - GAP
        out.append('<path class="apw-out" d="%s"/>' % sector(*OUT, a0, a1))
        rid = 'apw-%s-o%d' % (lang, i)
        r = (OUT[0] + OUT[1]) / 2
        defs.append('<path id="%s" d="%s"/>' % (rid, arc(r, a0, a1)))
        out.append('<text class="apw-out-t" font-size="%s"><textPath href="#%s" startOffset="50%%" text-anchor="middle" dominant-baseline="central">%s</textPath></text>'
                    % (L['out_size'], rid, label))
    # inner ring: the four domains, centered on the diagonals
    for i, label in enumerate(L['mid']):
        c = -45 + 90 * i
        a0, a1 = c - 45 + GAP, c + 45 - GAP
        mid.append('<path class="apw-mid" fill="%s" d="%s"/>' % (MID_FILL[i], sector(*MID, a0, a1)))
        rid = 'apw-%s-m%d' % (lang, i)
        r = (MID[0] + MID[1]) / 2
        defs.append('<path id="%s" d="%s"/>' % (rid, arc(r, a0 + 4, a1 - 4)))
        mid.append('<text class="apw-mid-t" font-size="%s"><textPath href="#%s" startOffset="50%%" text-anchor="middle" dominant-baseline="central">%s</textPath></text>'
                    % (L['mid_size'], rid, label))
        # a small arrowhead at the clockwise end of each segment: the strands are a cycle
        x, y = pt((MID[0] + MID[1]) / 2, a1 + GAP / 2)
        mid.append('<path class="apw-arrow" transform="translate(%.1f %.1f) rotate(%.1f)" d="M-5 -6 L4 0 L-5 6 Z"/>' % (x, y, a1 + GAP / 2 + 90))
    # the cycle orbit, a slowly turning dashed ring just inside the domains
    core.append('<g class="apw-orbit"><circle cx="%d" cy="%d" r="%d"/></g>' % (C, C, CORE + 7))
    core.append('<circle class="apw-core" cx="%d" cy="%d" r="%d"/>' % (C, C, CORE))
    n = len(L['core'])
    for j, line in enumerate(L['core']):
        y = C + (j - (n - 1) / 2) * (L['core_size'] * 1.12)
        cls = 'apw-core-t is-em' if j == n - 1 else 'apw-core-t'
        core.append('<text class="%s" x="%d" y="%.1f" font-size="%s" text-anchor="middle" dominant-baseline="central">%s</text>'
                    % (cls, C, y, L['core_size'], line))
    return ('<svg class="apw" viewBox="0 0 600 600" aria-hidden="true" focusable="false"><defs>%s</defs>'
            '<g class="apw-g apw-g-out">%s</g><g class="apw-g apw-g-mid">%s</g><g class="apw-g apw-g-core">%s</g></svg>'
            % (''.join(defs), ''.join(out), ''.join(mid), ''.join(core)))


if __name__ == '__main__':
    print(svg(sys.argv[1] if len(sys.argv) > 1 else 'en'))
