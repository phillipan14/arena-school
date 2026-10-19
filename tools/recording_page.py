"""Gated recording page for the ISB parent talk, EN + CN (RECORDING-BRIEF; redesigned in the site system by
RECORDING-REDESIGN-BRIEF, Oct 19, 2026).
  talks/2026-10-isb-parent-coffee/recording.html     -> /talk/recording
  talks/2026-10-isb-parent-coffee/recording-cn.html  -> /talk/recording-cn
A site page: the shared header and footer (tools/site_nav.py, which lists these pages in INCLUDE), css/pro.css +
css/ds.css tokens and components, and the /schools one-pager gate form (pp-lead el-lead el-form, cohort-form). Page
layout in css/recording.css. The video slot shows the cover slide and "Recording coming soon" until a URL is set;
the gate and its backends are in /recording.js, which also holds the single CONFIG line for the video and download
URLs (data-video-src / data-download-src on .rec override it). Facts come only from the talk page and Past talks.
CN copy is marked for JJ review. Stylesheets and scripts carry content-hash stamps (talks/ is outside pro_markup.py).
  python3 tools/recording_page.py           write both pages
  python3 tools/recording_page.py --check   report pages that would change
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import site_nav  # noqa: E402

DIR = 'talks/2026-10-isb-parent-coffee'
ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']
CSS = ['styles.css', 'riso-theme.css', 'mobile.css', 'css/program-pages.css', 'css/pages.css', 'css/elegance.css',
       'css/pro.css', 'css/ds.css', 'css/recording.css', 'phone.css']
JS = [('motion.js', ''), ('elegance.js', ' defer'), ('recording.js', ' defer')]

C = {
 'en': dict(
   file='recording.html', lang='en', title='Talk recording · Arena School',
   desc='The recording of “Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter?”, ISB PTA Parent Coffee, Oct 14, 2026.',
   ev='Talk recording · ISB PTA Parent Coffee · Oct 14, 2026',
   h1='Our Kids’ Jobs <em>Don’t Exist Yet.</em> So Which Skills Will Matter?',
   line='Which skills will matter when our children’s jobs don’t exist yet, with the case studies we walked through. For ISB parents, hosted by the ISB PTA.',
   by=[('Speakers', 'Jing Jing Yang and Phillip An'), ('Where', 'International School of Beijing'), ('Slides', 'English and Chinese')],
   gate_src=('Fill in the form to watch', 'The full talk, on this page'), gate_soon=('Recording coming soon', 'Fill in the form, and we’ll email you when it’s ready'),
   open_src=('Unlocked', 'Loading the player'), open_soon=('Recording coming soon', 'Unlocked. We’ll email you when it’s ready'),
   alt=('/talks/2026-10-isb-parent-coffee/recording-cn', 'zh-CN', 'The recording is available in Chinese.', 'Watch the Chinese version'),
   fk='Watch the recording', fh='Watch the full talk', fp='Free for families and educators. One short form.',
   name='Name', email='Email', school='School', school_h='your child’s, or yours', role='I am a', role_ph='Pick one',
   roles=[('Parent', 'Parent'), ('Teacher', 'Teacher'), ('School leader', 'School leader'), ('Other', 'Other')],
   wechat='WeChat ID', opt='optional', submit='Unlock the recording', sending='Sending…',
   subject='Arena School · recording request · ISB parent talk',
   note='We’ll also send you Arena Notes, our occasional newsletter. No spam, and you can unsubscribe anytime.',
   dh='Thank you.', ready='The recording is unlocked. Press play, or download it to watch later.', dl='Download the recording',
   later='The recording isn’t up yet. We’ll email you when it’s ready.',
   more=[('/talks/2026-10-isb-parent-coffee/slides-en.pdf', 'Slides', 'PDF, English'), ('/talks/2026-10-isb-parent-coffee/read/en', 'Read slide by slide', 'On your phone'),
         ('/case-study-examples', 'The case studies', 'From the talk')],
   all=('/talks/2026-10-isb-parent-coffee', 'All resources', 'Slides, PDFs, case studies'), jj=''),
 'cn': dict(
   file='recording-cn.html', lang='zh-CN', title='讲座录像 · Arena School',
   desc='“孩子们未来的工作还不存在，那么，哪些能力最重要？”讲座录像，ISB PTA 家长咖啡会，2026年10月14日。',
   ev='讲座录像 · ISB PTA 家长咖啡会 · 2026年10月14日',
   h1='孩子们未来的工作还不存在，<em>那么，哪些能力最重要？</em>',
   line='当孩子们未来的工作还不存在，哪些能力最重要，以及讲座中演示过的案例。面向 ISB 家长，由 ISB PTA 主办。',
   by=[('主讲', '羊筱涵、安广宁'), ('地点', '北京顺义国际学校'), ('幻灯片', '中英文')],
   gate_src=('填写表格即可观看', '讲座全程，在本页观看'), gate_soon=('录像即将上线', '填写表格，上线后我们会发邮件通知您'),
   open_src=('已解锁', '正在加载播放器'), open_soon=('录像即将上线', '已解锁。上线后我们会发邮件通知您'),
   alt=('/talks/2026-10-isb-parent-coffee/recording', 'en', '<!-- JJ review: 只有英文版录像时的提示 (RECORDING-ROUND3-BRIEF) -->目前提供英文版录像。', '观看英文版录像'),
   fk='观看录像', fh='观看讲座全程', fp='家长和教育者均可免费观看，只需填写一张简短的表格。',
   name='姓名', email='邮箱', school='学校', school_h='孩子就读的或您任职的学校', role='身份', role_ph='请选择',
   roles=[('Parent', '家长'), ('Teacher', '老师'), ('School leader', '学校管理者'), ('Other', '其他')],
   wechat='微信号', opt='选填', submit='解锁录像', sending='提交中…',
   subject='Arena School · 录像申请 · ISB 家长讲座',
   note='我们也会为您订阅 Arena 通讯。绝无垃圾邮件，可随时退订。',
   dh='谢谢！', ready='录像已解锁。可直接播放，也可下载稍后观看。', dl='下载录像',
   later='录像尚未上线。上线后我们会发邮件通知您。',
   more=[('/talks/2026-10-isb-parent-coffee/slides-cn.pdf', '幻灯片', 'PDF，中文版'), ('/talks/2026-10-isb-parent-coffee/read/cn', '逐页阅读', '适合手机'),
         ('/case-study-examples', '讲座中的案例', '建议用电脑打开')],
   all=('/talks/2026-10-isb-parent-coffee?lang=zh', '全部资料', '幻灯片、PDF 与案例'),
   jj='<!-- JJ review: 讲座录像页中文文案 (RECORDING-REDESIGN-BRIEF, Oct 19, 2026) -->\n'),
}
POSTER = {'en': '/%s/slides/en/01.jpg' % DIR, 'cn': '/%s/slides/cn/01.jpg' % DIR}


def ic(name):
    return ('<svg class="ds-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % ICONS[name])


LOCK_OPEN = '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>'   # Lucide lock-open


def icon(paths, cls='ds-ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">%s</svg>' % (cls, paths))




def phone_foot(cn):
    """The phone footer, built exactly as tools/phone_markup.py footer() does from tools/phone_pages.json (that tool only
    walks site pages, and importing it rewrites them, so the markup is mirrored here)."""
    import html
    f = json.load(open(os.path.join(ROOT, 'tools', 'phone_pages.json'), encoding='utf-8'))['footer']['cn' if cn else 'en']
    rows = ''.join('<li><a class="ph-row" href="%s"%s><span class="ph-row-t">%s</span>%s<svg class="ph-chev" viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5 13 10l-5.5 5.5"/></svg></a></li>'
                   % (html.escape(r['href']), ' target="_blank" rel="noopener"' if r['href'].startswith('http') else '',
                      html.escape(r['label']), ('<span class="ph-row-v">%s</span>' % html.escape(r['value'])) if r.get('value') else '')
                   for r in f['rows'])
    return ('<!-- phone:start -->\n<footer class="ph-foot" data-phone hidden><img class="ph-foot-lock" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" width="180" height="27">'
            '<p class="ph-foot-tag">%s</p><ul class="ph-list ph-list-dark">%s</ul><p class="ph-foot-c">%s</p></footer>\n'
            '<script src="/phone.js?v=%s" defer data-phone></script>\n<!-- phone:end -->\n'
            % (html.escape(f['tag']), rows, html.escape(f['copy']), ver('phone.js')))


def ver(path):
    return hashlib.sha1(open(os.path.join(ROOT, path), 'rb').read()).hexdigest()[:8]


def page(lang):
    c = C[lang]
    cn = lang == 'cn'
    rel = '%s/%s' % (DIR, c['file'])
    css = ''.join('<link rel="stylesheet" href="/%s?v=%s">\n' % (f, ver(f)) for f in CSS)
    js = ''.join('<script src="/%s?v=%s"%s></script>\n' % (f, ver(f), a) for f, a in JS)
    roles = ''.join('<option value="%s">%s</option>' % (v, t) for v, t in c['roles'])
    by = ''.join('<li>%s <b>%s</b></li>' % (k, v) for k, v in c['by'])
    more = ''.join('<li><a href="%s"><span><b>%s</b><small>%s</small></span><span class="arr" aria-hidden="true">→</span></a></li>' % m
                   for m in c['more'] + [c['all']])
    lock, opened = icon(ICONS['lock']), icon(LOCK_OPEN)
    msgs = ''.join('<p class="rv-msg %s">%s<span><b>%s</b><small>%s</small></span></p>' % (k, i, c[k.replace('m-', '').replace('-', '_')][0], c[k.replace('m-', '').replace('-', '_')][1])
                   for k, i in (('m-gate-src', lock), ('m-gate-soon', lock), ('m-open-src', opened), ('m-open-soon', opened)))
    body = (
        '<main id="top" class="rec is-locked" data-video-src="" data-download-src="">\n'
        '<section class="rc-head" id="recording" data-screen-label="Recording"><div class="container rc-grid">\n'
        '  <div style="grid-column:1/13"><span class="ds-eyebrow">%(ev)s</span></div>\n'
        '  <h1 class="rc-h1">%(h1)s</h1>\n  <p class="rc-line">%(line)s</p>\n  <ul class="rc-by">%(by)s</ul>\n'
        '</div></section>\n'
        '<section class="rc-band"><div class="container rc-grid">\n'
        '  <div class="rc-main">\n'
        '    <figure class="rv" data-poster="%(poster)s"><img src="%(poster)s" alt="" width="1600" height="900" decoding="async" fetchpriority="high">'
        '%(msgs)s</figure>\n'
        '    <p class="rc-alt" hidden>%(alt_t)s <a href="%(alt_h)s" hreflang="%(alt_l)s">%(alt_a)s <span class="arr" aria-hidden="true">→</span></a></p>\n'
        '  </div>\n'
        '  <div class="rc-side"><div class="pp-lead el-lead el-form" id="watch">\n'
        '    <div class="pp-lead-top"><span class="ds-eyebrow">%(fk)s</span><h3>%(fh)s</h3><p>%(fp)s</p></div>\n'
        '    <form class="cohort-form rec-form" action="https://formsubmit.co/ajax/contact@arenaschool.org" method="POST">\n'
        '      <input type="hidden" name="_subject" value="%(subject)s">\n'
        '      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">\n'
        '      <div class="form-row form-row-split"><div><label for="rc-name">%(name)s</label><input id="rc-name" name="name" type="text" required autocomplete="name" maxlength="120"></div>'
        '<div><label for="rc-email">%(email)s</label><input id="rc-email" name="email" type="email" required autocomplete="email" maxlength="200"></div></div>\n'
        '      <div class="form-row form-row-1"><div><label for="rc-school">%(school)s<small>%(school_h)s</small></label><input id="rc-school" name="school" type="text" required autocomplete="organization" maxlength="160"></div></div>\n'
        '      <div class="form-row form-row-split"><div><label for="rc-role">%(role)s</label><select id="rc-role" name="role" required><option value="" disabled selected>%(role_ph)s</option>%(roles)s</select></div>'
        '<div><label for="rc-wechat">%(wechat)s<small>%(opt)s</small></label><input id="rc-wechat" name="wechat" type="text" autocomplete="off" maxlength="120"></div></div>\n'
        '      <button type="submit" class="btn btn-primary cf-submit"><span class="cf-submit-label">%(lk)s%(submit)s</span>'
        '<span class="cf-submit-loading" aria-hidden="true">%(sending)s</span></button>\n'
        '      <p class="cf-status" role="status" aria-live="polite"></p>\n      <p class="rc-note">%(note)s</p>\n'
        '    </form>\n'
        '    <div class="pp-lead-done" hidden tabindex="-1"><b>%(dh)s</b><p class="rec-ready" hidden>%(ready)s</p><p class="pp-lead-later">%(later)s</p>'
        '<a class="btn btn-primary rec-dl" href="#" download hidden>%(dl)s <span class="arr">↓</span></a></div>\n'
        '  </div></div>\n'
        '  <ul class="rc-more">%(more)s</ul>\n'
        '</div></section>\n'
        '</main>\n'
        % dict(c, poster=POSTER[lang], msgs=msgs, lk=icon(ICONS['lock'], 'ds-ic rc-lk'), alt_h=c['alt'][0], alt_l=c['alt'][1], alt_t=c['alt'][2], alt_a=c['alt'][3],
               roles=roles, by=by, more=more))
    head = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n%s<meta charset="UTF-8">\n'
            '<script data-pro>(function(d){d.classList.add("js")})(document.documentElement)</script>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n<meta name="robots" content="noindex, nofollow">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="theme-color" content="#FFFFFF">\n'
            '<link rel="canonical" href="https://arenaschool.org/talk/recording%s">\n'
            '<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=3">\n<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png?v=3">\n'
            '<link rel="shortcut icon" href="/favicon.ico?v=3">\n<link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png?v=2">\n'
            '%s%s</head>\n'
            % (c['lang'], c['jj'], c['title'], c['desc'], '-cn' if cn else '', '<link rel="stylesheet" href="/fonts/zh/zh.css?v=2">\n' if cn else '', css))
    s = (head + '<body class="no-ticker pg el pg-recording">\n<nav class="nav" id="nav"></nav>\n' + body +
         '<footer class="footer"></footer>\n' + js + phone_foot(cn) + '</body>\n</html>\n')
    return site_nav.build(rel, s)


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for lang in ('en', 'cn'):
        p = os.path.join(ROOT, DIR, C[lang]['file'])
        t = page(lang)
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != t:
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
