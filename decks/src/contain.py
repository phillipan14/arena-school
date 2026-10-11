"""Containment check: every line of text, image, and boxed element on every slide must sit inside the content box
(padding included) of its nearest boxed ancestor: a pane, card, pill, chip, or anything with a fill or a full border.
Top-level items must sit inside the slide's safe margins.

A slide that fits 1920×1080 can still have a number running past its card, so export.py runs this before any PDF.

Usage:  python3 decks/src/contain.py              (EN and CN; export mode, then live with count-ups, sampled mid-count)
        python3 decks/src/contain.py --georgia    (also with Georgia's wider metrics, as on a phone that missed the web
                                                   fonts; downloads Gelasio, a Georgia-metric font, from Google Fonts)
"""
import functools, http.server, os, re, sys, threading, urllib.request

TOL = 2  # slide px: room for glyph side bearings

JS = r"""([idx, tol, onlyNums]) => {
 const s=document.querySelectorAll('#deck section.s')[idx], w=s.querySelector(':scope>.w');
 const filled=c=>c!=='rgba(0, 0, 0, 0)'&&c!=='transparent';
 const BOX='.pane,.card,.pill,.chip,.pl,.pc,.ba-p,.nd,.mm-c,.rw,.person,.pb,.dn,.qr-slides';
 function isBox(e){if(e===w)return true;const c=getComputedStyle(e);if(c.position==='fixed')return false;if(e.matches(BOX))return true;
  /* a fill makes a container when it holds content; empty fills are bars, dots, and rules */
  if(filled(c.backgroundColor)||c.backgroundImage!=='none')return !!(e.children.length||e.textContent.trim());
  return ['Top','Right','Bottom','Left'].every(k=>parseFloat(c['border'+k+'Width'])>0)}
 function boxOf(e,self){let p=self?e:e.parentElement;while(p&&p!==s){if(isBox(p))return p;p=p.parentElement}return w}
 function inner(e){const r=e.getBoundingClientRect(),c=getComputedStyle(e),k=e.offsetWidth?r.width/e.offsetWidth:1,f=n=>parseFloat(c[n])*k;
  return {l:r.left+f('borderLeftWidth')+f('paddingLeft'),r:r.right-f('borderRightWidth')-f('paddingRight'),
          t:r.top+f('borderTopWidth')+f('paddingTop'),b:r.bottom-f('borderBottomWidth')-f('paddingBottom'),k}}
 const shown=e=>e.checkVisibility?e.checkVisibility({opacityProperty:true,visibilityProperty:true}):true;
 const nm=e=>(e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).filter(x=>!/^(r|vis|in|bld|nt)$/.test(x)).join('.'):'')).slice(0,40);
 const out=[],seen=new Set();
 function test(rects,label,el,text){const B=boxOf(el,text),cb=inner(B),key=label+'|'+nm(B);
  rects.forEach(q=>{if(!q.width||!q.height||seen.has(key))return;
   const over=Object.entries({left:cb.l-q.left,right:q.right-cb.r,top:cb.t-q.top,bottom:q.bottom-cb.b}).filter(([,v])=>v>tol*cb.k).map(([k,v])=>k+' '+Math.round(v/cb.k));
   if(over.length){seen.add(key);out.push([nm(B),label,over.join(', ')])}})}
 const tw=document.createTreeWalker(w,NodeFilter.SHOW_TEXT);
 while(tw.nextNode()){const t=tw.currentNode,p=t.parentElement;if(!t.nodeValue.trim()||!p||p.closest('.notes,svg')||!shown(p))continue;
  if(onlyNums&&!p.closest('.big,.cnt'))continue;
  const c=getComputedStyle(p),k=p.offsetWidth?p.getBoundingClientRect().width/p.offsetWidth:1,lh=(parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.2)*k;
  const rg=document.createRange();rg.selectNodeContents(t);
  /* vertically a line occupies its line box, not the font's taller content area */
  test([...rg.getClientRects()].map(q=>{const h=Math.min(q.height,lh),y=q.top+(q.height-h)/2;return {left:q.left,right:q.right,width:q.width,height:h,top:y,bottom:y+h}}),
       '"'+t.nodeValue.trim().slice(0,30)+'"',p,true)}
 if(!onlyNums)w.querySelectorAll('*').forEach(e=>{if(e.closest('.notes')||(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')||!shown(e))return;
  const c=getComputedStyle(e);if(c.position==='fixed'||c.display==='inline'||c.display==='contents')return;
  const media=/^(img|video|svg|canvas)$/i.test(e.tagName);
  /* a photo cropped by a frame that hides its overflow (the slow zoom on project photos) is cropped by design */
  if(media&&/hidden|clip/.test(getComputedStyle(boxOf(e,false)).overflow))return;
  if(media||isBox(e)&&e!==w)test([e.getBoundingClientRect()],'<'+nm(e)+'>',e,false)});
 /* sibling / cousin collisions: a logo sitting on a line of text in the same row, two images covering each other */
 if(!onlyNums){
  const skip=e=>!shown(e)||e.closest('.notes')||e.closest('svg')&&e.tagName.toLowerCase()!=='svg';
  const media=e=>/^(img|video|svg|canvas)$/i.test(e.tagName);
  const texty=e=>{if(media(e)||e.closest('svg'))return false;const c=getComputedStyle(e);if(c.display==='inline'||c.position==='fixed')return false;return[...e.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim())};
  const items=[...w.querySelectorAll('img,video,svg,span,b,small,h3,p,dt,dd,li,div')].filter(e=>!skip(e)&&(media(e)||texty(e)));
  for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
   const a=items[i],b=items[j];
   if(a.contains(b)||b.contains(a))continue;
   if(a.closest('figure')&&a.closest('figure')===b.closest('figure'))continue;
   if(a.closest('.ring2,.dn,.pg-m')&&a.closest('.ring2,.dn,.pg-m')===b.closest('.ring2,.dn,.pg-m'))continue;
   if(a.closest('.lr')&&a.closest('.lr')===b.closest('.lr')&&media(a)&&media(b))continue;
   if(!(media(a)||media(b)))continue;
   const A=a.getBoundingClientRect(),B=b.getBoundingClientRect();
   if(A.width<2||B.width<2||A.height<2||B.height<2)continue;
   const ix=Math.min(A.right,B.right)-Math.max(A.left,B.left),iy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
   const k=A.width/Math.max(a.offsetWidth||A.width,1);
   if(ix>tol*k&&iy>tol*k){const key='overlap|'+nm(a)+'|'+nm(b);if(!seen.has(key)){seen.add(key);out.push([nm(a),'overlaps '+nm(b),Math.round(ix/k)+'×'+Math.round(iy/k)])}}}
 }
 return out}"""

GEORGIA = None


def georgia_css():
    """Gelasio has Georgia's metrics; renaming it stands in for a phone that fell back to Georgia"""
    global GEORGIA
    if GEORGIA is None:
        req = urllib.request.Request('https://fonts.googleapis.com/css2?family=Gelasio:ital,wght@0,400..700;1,400..700',
                                     headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 Chrome/120 Safari/537.36'})
        css = urllib.request.urlopen(req, timeout=20).read().decode().replace("font-family: 'Gelasio'", "font-family: 'GeorgiaMetrics'")
        GEORGIA = css + ":root,html[lang]{--serif:'GeorgiaMetrics',serif!important}"
    return GEORGIA


def check(pg, motion=False):
    """[(slide, container, item, overflow)] for the page's deck. The page must be at ?stage, fonts loaded.
    motion=False checks the fully built export layout; motion=True scrolls through with motion on, sampling
    every counter while it counts up and checking each slide again once its animations end."""
    n = pg.evaluate("document.querySelectorAll('#deck section.s').length")
    found = []
    for i in range(n):
        F = []
        if motion:
            pg.evaluate(f"document.getElementById('deck').scrollTop=document.querySelectorAll('section.s')[{i}].offsetTop")
            for t in range(40):
                pg.wait_for_timeout(100)
                counting = pg.evaluate(f"[...document.querySelectorAll('section.s')[{i}].querySelectorAll('.big,.cnt')].some(e=>e.style.minWidth)")
                if counting:
                    F += [(c, w, o + ' (while counting)') for c, w, o in pg.evaluate(JS, [i, TOL, True])]
                busy = pg.evaluate("document.getAnimations().some(a=>a.playState==='running')")
                if t > 6 and not counting and not busy: break
        F += [tuple(f) for f in pg.evaluate(JS, [i, TOL, False])]
        found += [(i + 1,) + f for f in dict.fromkeys(map(tuple, F))]
    return found


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=root))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_address[1]}'


if __name__ == '__main__':
    import subprocess
    from playwright.sync_api import sync_playwright
    SRC = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(SRC, 'build.py')], check=True, stdout=subprocess.DEVNULL)
    base = serve(os.path.abspath(os.path.join(SRC, '..', '..')))
    fonts = ['web'] + (['georgia'] if '--georgia' in sys.argv else [])
    total = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for deck in ('conversation', 'conversation-cn'):
            for font in fonts:
                for motion in (False, True):
                    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
                    pg.goto(f'{base}/decks/{deck}.html?stage', wait_until='networkidle')
                    if font == 'georgia': pg.add_style_tag(content=georgia_css())
                    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
                    if not motion:
                        pg.evaluate("document.documentElement.classList.add('export');window.__space&&window.__space()"); pg.wait_for_timeout(400)
                    F = check(pg, motion)
                    print(f"{deck}  {font} fonts  {'live, with count-ups' if motion else 'export'}: {len(F)} outside their container")
                    for f in F: print('   slide %d  in %s  %s  %s' % f)
                    total += len(F); pg.close()
        b.close()
    sys.exit(1 if total else 0)
