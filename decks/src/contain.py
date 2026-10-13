"""Containment check: every line of text, image, and boxed element on every slide must sit inside the content box
(padding included) of its nearest boxed ancestor: a pane, card, pill, chip, or anything with a fill or a full border.
Top-level items must sit inside the slide's safe margins.

A slide that fits 1920×1080 can still have a number running past its card, so export.py runs this before any PDF.

Usage:  python3 decks/src/contain.py              (EN and CN; export mode, then live with count-ups, sampled mid-count)
        python3 decks/src/contain.py --georgia    (also with Georgia's wider metrics, as on a phone that missed the web
                                                   fonts; downloads Gelasio, a Georgia-metric font, from Google Fonts)
        python3 decks/src/contain.py --phone      (390×844 portrait player, letterboxed 16:9 stage; default with the rest)
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
 while(tw.nextNode()){const t=tw.currentNode,p=t.parentElement;if(!t.nodeValue.trim()||!p||p.closest('.notes,.ag-fill,svg')||!shown(p))continue;
  if(onlyNums&&!p.closest('.big,.cnt'))continue;
  const c=getComputedStyle(p),k=p.offsetWidth?p.getBoundingClientRect().width/p.offsetWidth:1,lh=(parseFloat(c.lineHeight)||parseFloat(c.fontSize)*1.2)*k;
  const rg=document.createRange();rg.selectNodeContents(t);
  /* horizontally a line starts at its first glyph's ink, not its advance box: a big serif figure pulled left by its own
     side bearing (optical alignment) keeps its ink inside the card */
  const ch=t.nodeValue.trimStart()[0],cv=test.cv||(test.cv=document.createElement('canvas').getContext('2d'));
  cv.font=c.fontStyle+' '+c.fontWeight+' '+c.fontSize+' '+c.fontFamily;const bear=Math.max(0,-cv.measureText(ch).actualBoundingBoxLeft)*k;
  /* vertically a line occupies its line box, not the font's taller content area */
  test([...rg.getClientRects()].map((q,i)=>{const h=Math.min(q.height,lh),y=q.top+(q.height-h)/2,l=q.left+(i?0:bear);return {left:l,right:q.right,width:q.right-l,height:h,top:y,bottom:y+h}}),
       '"'+t.nodeValue.trim().slice(0,30)+'"',p,true)}
 if(!onlyNums)w.querySelectorAll('*').forEach(e=>{if(e.closest('.notes,.ag-fill')||(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')||!shown(e))return;
  const c=getComputedStyle(e);if(c.position==='fixed'||c.display==='inline'||c.display==='contents')return;
  const media=/^(img|video|svg|canvas)$/i.test(e.tagName);
  /* a photo cropped by a frame that hides its overflow (the slow zoom on project photos) is cropped by design */
  if(media&&/hidden|clip/.test(getComputedStyle(boxOf(e,false)).overflow))return;
  if(media||isBox(e)&&e!==w)test([e.getBoundingClientRect()],'<'+nm(e)+'>',e,false)});
 /* sibling / cousin collisions across every element type: text on text, a footnote on a number,
    a bar on its label, a logo on a line. Designed stacks (donut + figure, crop frames) stay skipped. */
 if(!onlyNums){
  const skip=e=>!shown(e)||e.closest('.notes,.ag-fill')||e.closest('svg')&&e.tagName.toLowerCase()!=='svg';
  const media=e=>/^(img|video|svg|canvas)$/i.test(e.tagName);
  const texty=e=>{if(media(e)||e.closest('svg'))return false;const c=getComputedStyle(e);if(c.display==='inline'||c.position==='fixed')return false;return[...e.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim())};
  const bar=e=>e.matches&&e.matches('.hb i,.mb i,.pb-t i,.pb-t');
  const items=[...w.querySelectorAll('img,video,svg,span,b,small,h1,h2,h3,p,dt,dd,li,div,i')].filter(e=>!skip(e)&&(media(e)||texty(e)||bar(e)));
  for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
   const a=items[i],b=items[j];
   if(a.contains(b)||b.contains(a))continue;
   if(a.closest('figure')&&a.closest('figure')===b.closest('figure'))continue;
   if(a.closest('.ring2,.dn,.pg-m')&&a.closest('.ring2,.dn,.pg-m')===b.closest('.ring2,.dn,.pg-m'))continue;
   if(a.closest('.lr')&&a.closest('.lr')===b.closest('.lr')&&media(a)&&media(b))continue;
   if(a.closest('.ag-fill')||b.closest('.ag-fill'))continue;
   if(a.closest('.grow-line')||b.closest('.grow-line'))continue;
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


def phone_stage(pg):
    """The 1920×1080 stage must sit fully inside the 390×844 player, letterboxed, not clipped."""
    box = pg.evaluate("""() => {
      const f=document.getElementById('frame'); if(!f) return {err:'no frame'};
      const r=f.getBoundingClientRect();
      return {w:r.width,h:r.height,t:r.top,l:r.left,b:r.bottom,r:r.right,vw:innerWidth,vh:innerHeight};
    }""")
    if box.get('err'): return [('player', 'stage', box['err'], '')]
    out = []
    if box['l'] < -TOL or box['t'] < -TOL or box['r'] > box['vw'] + TOL or box['b'] > box['vh'] + TOL:
        out.append(('player', 'stage', 'clipped by the phone viewport',
                    f"{round(box['w'])}×{round(box['h'])} at {round(box['l'])},{round(box['t'])}"))
    if abs(box['w'] / max(box['h'], 1) - 1920 / 1080) > 0.02:
        out.append(('player', 'stage', 'not 16:9 letterbox',
                    f"{round(box['w'])}×{round(box['h'])}"))
    return out


PHONE_JS = r"""([idx, scale]) => {
 const s=document.querySelectorAll('#deck section.s')[idx], w=s.querySelector(':scope>.w');
 const shown=e=>e.checkVisibility?e.checkVisibility({opacityProperty:true,visibilityProperty:true}):true;
 const nm=e=>(e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/).filter(x=>!/^(r|vis|in|bld|nt)$/.test(x)).join('.'):'')).slice(0,40);
 const out=[];
 /* titles, evidence paragraphs, big numbers, and footnotes — not chrome, dates, or pills */
 const tw=document.createTreeWalker(w,NodeFilter.SHOW_TEXT);
 while(tw.nextNode()){
  const t=tw.currentNode,p=t.parentElement;if(!t.nodeValue.trim()||!p||!shown(p)||p.closest('.notes,svg'))continue;
  let min=0,kind='';
  if(p.closest('.fn')){min=3.0;kind='footnote'}
  else if(p.closest('h1,h2')){min=8.0;kind='title'}
  else if(p.closest('.st3 .big, .cmp2 .big, .bnx .big, .an .big, .nst .big')&&!p.closest('small')){min=11.5;kind='number'}
  else if(p.matches('p')&&p.closest('.bd')&&!p.closest('.tln,.who3,.agx,.qa,.c123,.qx,.who2,.mb,.where')){min=4.8;kind='body'}
  else continue;
  const vis=parseFloat(getComputedStyle(p).fontSize)*scale;
  if(vis+0.08<min)out.push([nm(p),'too small ('+kind+')',vis.toFixed(1)+'px rendered, min '+min]);
 }
 /* large empty column: evidence children should span the body (quotes and statement slides skipped) */
 const bd=s.querySelector(':scope>.w>.bd');
 if(bd&&shown(bd)&&!s.matches('.bq,.tk,.cover,.toc,.s-src')){
  const R=bd.getBoundingClientRect();
  if(R.width>200&&R.height>80){
   const kids=[...bd.children].filter(e=>shown(e)&&e.getBoundingClientRect().width>2);
   if(kids.length){
    let L=1e9,Rr=-1e9;
    kids.forEach(e=>{const q=e.getBoundingClientRect();L=Math.min(L,q.left);Rr=Math.max(Rr,q.right)});
    const span=(Rr-L)/R.width;
    if(span<0.74)out.push([nm(bd),'empty region','evidence uses '+Math.round(span*100)+'% of body width']);
   }
  }
 }
 return out}"""


def phone_quality(fr, scale):
    """[(slide, item, reason, detail)] for tiny type and unused columns at phone letterbox scale."""
    n = fr.evaluate("document.querySelectorAll('#deck section.s').length")
    found = []
    for i in range(n):
        fr.evaluate(f"document.getElementById('deck').scrollTop=document.querySelectorAll('section.s')[{i}].offsetTop")
        for row in fr.evaluate(PHONE_JS, [i, scale]):
            found.append((i + 1,) + tuple(row))
    return found


def stage_frame(pg):
    for fr in pg.frames:
        if fr is pg.main_frame: continue
        if 'stage' in (fr.url or ''): return fr
    return None


if __name__ == '__main__':
    import subprocess
    from playwright.sync_api import sync_playwright
    SRC = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(SRC, 'build.py')], check=True, stdout=subprocess.DEVNULL)
    base = serve(os.path.abspath(os.path.join(SRC, '..', '..')))
    fonts = ['web'] + (['georgia'] if '--georgia' in sys.argv else [])
    run_phone = '--phone' in sys.argv or '--no-phone' not in sys.argv
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
            if run_phone:
                pg = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
                pg.goto(f'{base}/decks/{deck}.html', wait_until='networkidle')
                pg.wait_for_function("() => { const f=document.getElementById('frame'); return f && f.contentDocument && f.contentDocument.querySelectorAll('#deck section.s').length }")
                pg.wait_for_timeout(400)
                P = phone_stage(pg)
                print(f"{deck}  phone 390×844 player: {len(P)} stage problems")
                for f in P: print('   %s  %s  %s  %s' % f)
                total += len(P)
                fr = stage_frame(pg)
                if fr:
                    fr.evaluate("document.documentElement.classList.add('export');window.__space&&window.__space()")
                    fr.wait_for_timeout(400)
                    F = check(fr, False)
                    print(f"{deck}  phone letterbox stage: {len(F)} outside their container")
                    for f in F: print('   slide %d  in %s  %s  %s' % f)
                    total += len(F)
                    scale = pg.evaluate("window.__ps||0")
                    Q = phone_quality(fr, scale)
                    print(f"{deck}  phone 390×844 quality (scale {scale:.3f}): {len(Q)} size/empty problems")
                    for f in Q: print('   slide %d  %s  %s  %s' % f)
                    total += len(Q)
                else:
                    print(f"{deck}  phone 390×844 player: no ?stage iframe")
                    total += 1
                pg.close()
        b.close()
    sys.exit(1 if total else 0)
