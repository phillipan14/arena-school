import math, re, sys, os
# Framework wheel. Run with no arguments to regenerate both copies and paste them into body-en.html:
# slide 8 (class p9-wheel, rotated so strand 01 sits top left like its card, ids prefixed w8) and the
# backup wheel (class fx-wheel). Override any parameter as key=value (e.g. ofs=32 rcyc=382). Then run build.py.
SRC=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON=os.path.join(SRC,'icons')+'/'
A=dict({'w': '800', 'rout': '348', 'rsec': '266', 'rcore': '110', 'rcyc': '380', 'fs': '35', 'l1': '211', 'l2': '169', 'ofs': '31', 'cfs': '33', 'clh': '36', 'oh': '47'})
A.update(a.split('=',1) for a in sys.argv[1:])
def g(k,d): return float(A.get(k,d))
def inner(n):
    s=open(ICON+n+'.svg').read(); s=re.sub(r'<!--.*?-->','',s,flags=re.S); return re.search(r'<svg[^>]*>(.*)</svg>',s,re.S).group(1).strip()
def icon(n,x,y,size,col):
    k=size/24; return f'<g transform="translate({x-size/2:.1f},{y-size/2:.1f}) scale({k:.3f})" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{inner(n)}</g>'
W=g('w',800);C=W/2;R_OUT=g('rout',334);R_SEC=g('rsec',258);R_CORE=g('rcore',100);R_CYC=g('rcyc',351)
FS=g('fs',32);L1=g('l1',203);L2=g('l2',163);RI=g('ri',137);IS=g('is',32);CFS=g('cfs',31);CDY=g('cdy',0);CLH=g('clh',33);OFS=g('ofs',22)
RING=A.get('ring','#F5F7FA');CORE=A.get('core','#FFFFFF')
def P(a,r): a=math.radians(a); return C+r*math.cos(a),C+r*math.sin(a)
def ann(a0,a1,r0,r1,fill):
    x0,y0=P(a0,r1);x1,y1=P(a1,r1);x2,y2=P(a1,r0);x3,y3=P(a0,r0)
    return f'<path d="M{x0:.1f},{y0:.1f} A{r1},{r1} 0 0 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 0 0 {x3:.1f},{y3:.1f}Z" fill="{fill}"/>'
def arc(pid,a,r,half,flip):
    s0,e0=(a+half,a-half) if flip else (a-half,a+half); x0,y0=P(s0,r);x1,y1=P(e0,r)
    return f'<path id="{pid}" d="M{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 0 {0 if flip else 1} {x1:.1f},{y1:.1f}" fill="none"/>'
def wheel(cls,X,ROT,label):
    o=[f'<defs><marker id="{X}cyc" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2F55A8"/></marker>']
    strands=[('target',['Inquiry and','planning'],'#2F55A8'),('search',['Research and','evaluation'],'#0B1A4A'),('file-text',['Creating and','communicating'],'#3D5FA6'),('messages-square',['Collaboration','and reflection'],'#5670B0')]
    # text arcs: a visual baseline radius chosen so the x-height band sits on L1/L2 (ink-centered radii)
    XH=0.46*FS
    OH=g('oh',44)
    for i,(ic,lines,col) in enumerate(strands):
        am=ROT-90+i*90+45; flip=0<(am%360)<180
        # top half: glyphs grow outward from baseline; bottom: grow inward
        rs=[L2+XH/2+g('db',3.2), L1+XH/2+g('db',3.2)] if flip else [L1-XH/2+g('dt',-5), L2-XH/2+g('dt',-5)]
        for j,r in enumerate(rs): o.append(arc(f'{X}st{i}{j}',am,r,44,flip))
    conds=[('In person, real-time feedback',ROT-45),('AI use disclosed and cited',ROT+45),('Learner voice and choice',ROT+135),('An authentic audience',ROT+225)]
    rc=(R_SEC+R_OUT)/2; OX=0.46*OFS
    for i,(t,a) in enumerate(conds):
        flip=0<(a%360)<180; r=rc+OX/2+g('odb',2.8) if flip else rc-OX/2+g('odt',-2.8)
        o.append(arc(f'{X}cd{i}',a,r,OH,flip))
    o.append('</defs>')
    o.append(f'<circle cx="{C}" cy="{C}" r="{R_OUT}" fill="{RING}" stroke="#0B1A4A" stroke-opacity=".2" stroke-width="1.2"/>')
    for k in range(4):
        a0=ROT-90+k*90+8;a1=a0+74;x0,y0=P(a0,R_CYC);x1,y1=P(a1,R_CYC)
        o.append(f'<path d="M{x0:.1f},{y0:.1f} A{R_CYC},{R_CYC} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="#2F55A8" stroke-width="2.4" stroke-linecap="round" marker-end="url(#{X}cyc)"/>')
    for a in (-90,0,90,180):
        x0,y0=P(a,R_SEC);x1,y1=P(a,R_OUT);o.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#0B1A4A" stroke-opacity=".18" stroke-width="1.2"/>')
    for i,(ic,lines,col) in enumerate(strands):
        a0=ROT-90+i*90;a1=a0+90
        o.append(ann(a0+.7,a1-.7,R_CORE+6,R_SEC,col))
        am=(a0+a1)/2
        if A.get('icons','0')=='1':
            x,y=P(am,RI); o.append(icon(ic,x,y,IS,'#FFFFFF'))
        for j,t in enumerate(lines):
            o.append(f'<text class="fx-st" font-size="{FS:g}" fill="#fff"><textPath href="#{X}st{i}{j}" startOffset="50%" text-anchor="middle">{t}</textPath></text>')
    o.append(f'<circle cx="{C}" cy="{C}" r="{R_CORE}" fill="{CORE}" stroke="#0B1A4A" stroke-opacity=".2"/>')
    # three lines, ink-centered: middle line x-height centered on C+CDY
    CAP=g('cap',0.64)*CFS
    bl=C+CDY+CAP/2+CLH
    cy=bl-CLH
    o.append(f'<text x="{C}" y="{cy-CLH:.1f}" text-anchor="middle" font-size="{CFS:g}" fill="#0B1A4A">The learner</text><text x="{C}" y="{cy:.1f}" text-anchor="middle" font-size="{CFS:g}" fill="#0B1A4A">does the</text><text x="{C}" y="{cy+CLH:.1f}" text-anchor="middle" font-size="{CFS:g}" fill="#2F55A8" font-style="italic">thinking</text>')
    for i,(t,a) in enumerate(conds):
        o.append(f'<text font-size="{OFS:g}" fill="#0B1A4A"><textPath href="#{X}cd{i}" startOffset="50%" text-anchor="middle">{t}</textPath></text>')
    return f'<svg class="{cls}" viewBox="0 0 {W:g} {W:g}" role="img" aria-label="{label}" font-family="Newsreader, Georgia, serif">'+''.join(o)+'</svg>'
LABEL='Arena School learning framework: the learner does the thinking; four strands; four conditions'
p=os.path.join(SRC,'body-en.html'); s=open(p).read()
for cls,X,ROT in (('fx-wheel p9-wheel','w8',-90),('fx-wheel','',0)):
    svg=wheel(cls,X,ROT,LABEL)
    s,n=re.subn(r'<svg class="'+cls+r'".*?</svg>',lambda m:svg,s,count=1,flags=re.S)
    assert n==1,cls+' wheel not found in body-en.html'
open(p,'w').write(s); print('wheels updated in body-en.html; now run build.py')
