import re, copy, os, sys
H=os.path.dirname(os.path.abspath(__file__))
R=lambda f: open(os.path.join(H,f),encoding='utf-8').read()
D=sys.argv[1] if len(sys.argv)>1 else os.path.join(H,'..')+'/'  # default: the repo's /decks/ folder
import glob
css=R('shared.css')+''.join('\n/* ---- '+os.path.basename(f)+' ---- */\n'+open(f,encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(H,'css','*.css'))))
js=R('shared.js')+''.join('\n'+open(f,encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(H,'js','*.html'))))
GUARD=R('guard.js')
# {{ic:name}} inlines a Lucide line icon (decks/src/icons, ISC licence) so the deck stays one self-contained file
def icon(m):
    s=re.sub(r'<!--.*?-->','',R('icons/'+m.group(1)+'.svg'),flags=re.S)
    s=re.sub(r'\s*class="[^"]*"|\s*width="24"|\s*height="24"|\s*xmlns="[^"]*"','',s)
    return re.sub(r'\s+',' ',s).replace('> <','><').strip().replace('<svg','<svg class="lic" aria-hidden="true"',1)
bodies={k:re.sub(r'\{\{ic:([\w-]+)\}\}',icon,R(f)) for k,f in (('en','body-en.html'),('cn','body-cn.html'))}
V=[('en','en','conversation.html','Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter?','↓ / → next · ↑ / ← back','Swipe or tap to go on','Slides',''),
   ('cn','zh-CN','conversation-cn.html','孩子们未来的工作还不存在，那么，哪些能力最重要？','↓ / → 下一页 · ↑ / ← 上一页','轻点或滑动翻页','幻灯片','h1,h2,h3,p,li,dd,.quote,.cap,.step b,.t,.mc b')]
# without ?stage the page is the player: it loads itself at ?stage into a 1920×1080 frame (see the player in shared.js).
# export.py and the frame use ?stage directly; without JavaScript the page falls back to the phone reading layout.
MODE="<script>(function(h){var m=document.querySelector('meta[name=viewport]');if(self!==top){h.classList.add('framed');if(m)m.setAttribute('content','width=1920,initial-scale=1')}else if(!/[?&]stage\\b/.test(location.search)){h.classList.add('player');if(m)m.setAttribute('content','width=device-width,initial-scale=1,viewport-fit=cover')}else if(m)m.setAttribute('content','width=1920,initial-scale=1')})(document.documentElement)</script>"
for key,lang,fn,title,hint,phint,ftitle,gsel in V:
    ON=' class="on"'
    pill=''.join('<a href="/decks/%s"%s>%s</a>'%(f,ON if f==fn else '',lab) for f,lab in [('conversation.html','EN'),('conversation-cn.html','中文')])
    guard=GUARD.replace('__SEL__',gsel) if gsel else ''
    html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>{title}</title>
<link rel="icon" href="/favicon.svg">
{MODE}
<style>{css}</style></head><body>
<div class="lang">{pill}</div><nav class="nav" id="nav"></nav><div class="hint">{hint}</div>
<div class="stage" id="stage"><iframe id="frame" title="{ftitle}" allow="autoplay; fullscreen"></iframe></div><div class="phint">{phint}</div>
<main class="deck" id="deck">
{bodies[key]}
</main>
{js}
{guard}
</body></html>'''
    open(os.path.join(D,fn),'w',encoding='utf-8').write(html); print(fn,len(html))

# Phone reader (/talk/en, /talk/cn): the same slides, reflowed for a phone held upright, one slide per screen.
# The deck above never reflows (DESIGN.md §10.2); this is the separate phone view the /talk language chooser opens.
# Same body files, minus speaker notes, styled by reader/reader.css and driven by reader/reader.js.
T=os.path.join(H,'..','..','talk') if len(sys.argv)<=1 else D
TOOLS=re.search(r"var L='([^']+)'\.split\('\|'\)",R('shared.js')).group(1)  # the market-map tool names, shared with the deck
rcss,rjs=R('reader/reader.css'),R('reader/reader.js').replace('__TOOLS__',TOOLS.replace('\\','\\\\'))
ICO={'prev':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
     'next':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
     'list':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
     'x':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
     'down':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
     'dl':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 20h14" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
     'copy':'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8.5" y="8.5" width="11" height="11" rx="2.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M15.5 8.5V6.7a2.2 2.2 0 0 0-2.2-2.2H6.7a2.2 2.2 0 0 0-2.2 2.2v6.6a2.2 2.2 0 0 0 2.2 2.2h1.8" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'}
# the reader's last slide (contact + PDF download) lives only in the reader: reader/end-en.html, reader/end-cn.html.
# {{br:name}} inlines a brand glyph from reader/brand (Simple Icons, CC0); {{ico:name}} one of the ICO icons above.
def endslide(key):
    s=R('reader/end-%s.html'%key)
    s=re.sub(r'\{\{br:([\w-]+)\}\}',lambda m:R('reader/brand/'+m.group(1)+'.svg').strip(),s)
    return re.sub(r'\{\{ico:(\w+)\}\}',lambda m:ICO[m.group(1)],s)
RV=[('en','en','en.html','/talk/cn','<span>中文</span>','中文','Previous slide','Next','All slides','Close','Talk resources · Arena School','',
     'Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter? · Arena School'),
    ('cn','zh-CN','cn.html','/talk/en','EN','English','上一页','下一页','全部幻灯片','关闭','讲座资料 · Arena School','<link rel="stylesheet" href="/fonts/zh/zh.css?v=2"><link rel="stylesheet" href="/fonts/zh/zh-fallback.css">',
     '孩子们未来的工作还不存在，那么，哪些能力最重要？ · Arena School')]
for key,lang,fn,other,olab,oname,lprev,lnext,lall,lclose,lhome,zh,title in RV:
    body=re.sub(r'\s*<aside class="notes">.*?</aside>','',bodies[key],flags=re.S)+'\n\n'+endslide(key)
    gsel=dict((v[0],v[7]) for v in V)[key]; guard=GUARD.replace('__SEL__',gsel) if gsel else ''
    html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#F3E9DD">
<meta name="format-detection" content="telephone=no">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=3"><link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png?v=2">
<link rel="stylesheet" href="/fonts/fonts.css">{zh}
<style>{rcss}</style></head><body>
<header class="top"><a class="home" href="/talk" aria-label="{lhome}"><img class="wm n" src="/logos/arena/wordmark-navy-1600.png" alt="Arena School" width="1600" height="242"><img class="wm i" src="/logos/arena/wordmark-ivory-1600.png" alt="" width="1600" height="242"></a>
 <div class="tools"><a class="lng" href="{other}" data-base="{other}" hreflang="{'zh-CN' if key=='en' else 'en'}" aria-label="{oname}">{olab}</a><button type="button" class="lst" aria-label="{lall}">{ICO['list']}</button></div>
 <div class="prog" aria-hidden="true"><i></i></div></header>
<main class="rd" id="deck" tabindex="-1">
{body}
</main>
<nav class="bot" aria-label="{lall}"><button type="button" class="pv" aria-label="{lprev}">{ICO['prev']}</button><button type="button" class="ctr" aria-label="{lall}"><b></b><small></small></button><button type="button" class="nx"><span>{lnext}</span>{ICO['next']}</button></nav>
<button type="button" class="more-cue" aria-hidden="true" tabindex="-1">{ICO['down']}</button><div class="tip" role="status"></div>
<div class="sheet" hidden role="dialog" aria-modal="true" aria-label="{lall}"><div class="sh-p"><div class="sh-h"><b>{lall}</b><button type="button" class="sh-x" aria-label="{lclose}">{ICO['x']}</button></div><nav class="sh-l"></nav></div></div>
<script>{rjs}</script>
{guard}
</body></html>'''
    os.makedirs(T,exist_ok=True)
    open(os.path.join(T,fn),'w',encoding='utf-8').write(html); print('talk/'+fn,len(html))
