import re, copy, os, sys
H=os.path.dirname(os.path.abspath(__file__))
R=lambda f: open(os.path.join(H,f),encoding='utf-8').read()
D=sys.argv[1] if len(sys.argv)>1 else os.path.join(H,'..')+'/'  # default: the repo's /decks/ folder
import glob
css=R('shared.css')+''.join('\n/* ---- '+os.path.basename(f)+' ---- */\n'+open(f,encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(H,'css','*.css'))))
js=R('shared.js')+''.join('\n'+open(f,encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(H,'js','*.html'))))
GUARD=R('guard.js')
bodies={'en':R('body-en.html'),'cn':R('body-cn.html')}
V=[('en','en','conversation.html','Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter?','↓ / → next · ↑ / ← back',''),
   ('cn','zh-CN','conversation-cn.html','孩子们未来的工作还不存在，那么，哪些能力最重要？','↓ / → 下一页 · ↑ / ← 上一页','h1,h2,h3,p,li,.quote,.cap,.step b,.t,.mc b')]
for key,lang,fn,title,hint,gsel in V:
    ON=' class="on"'
    pill=''.join('<a href="/decks/%s"%s>%s</a>'%(f,ON if f==fn else '',lab) for f,lab in [('conversation.html','EN'),('conversation-cn.html','中文')])
    guard=GUARD.replace('__SEL__',gsel) if gsel else ''
    html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<link rel="icon" href="/favicon.svg">
<style>{css}</style></head><body>
<div class="lang">{pill}</div><nav class="nav" id="nav"></nav><div class="hint">{hint}</div>
<main class="deck" id="deck">
{bodies[key]}
</main>
{js}
{guard}
</body></html>'''
    open(os.path.join(D,fn),'w',encoding='utf-8').write(html); print(fn,len(html))
