import re
P=' pathLength="1"'
def pth(d,c=''): return '<path d="%s"%s%s/>'%(d,P,(' class="%s"'%c) if c else '')
def cir(x,y,r,c=''): return '<circle cx="%s" cy="%s" r="%s"%s%s/>'%(x,y,r,P,(' class="%s"'%c) if c else '')
def rec(x,y,w,h,rx=2,c=''): return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s"%s%s/>'%(x,y,w,h,rx,P,(' class="%s"'%c) if c else '')
def g(inner,c): return '<g class="%s">%s</g>'%(c,inner)
I={
# I  choosing your own path: fork, chosen branch in blue with a flag that waves
'icon-agency': pth('M32 58 V40')+pth('M32 40 L50 20','ic-faint')+pth('M32 40 V16','ic-faint')+pth('M32 40 L16 20','ic-acc')
   +g(pth('M16 20 V6')+pth('M16 7 H28 L25 11 L28 15 H16','ic-acc'),'ic-m ic-wave'),
# II make things in front of people: screen with a rising chart, audience below
'icon-make': rec(10,8,44,30,3)+g(pth('M16 32 L25 24 L32 28 L46 15','ic-acc')+pth('M41 15 H46 V20','ic-acc'),'ic-m ic-redraw')
   +cir(20,50,4)+cir(32,50,4)+cir(44,50,4)+pth('M13 60 Q20 54 27 60')+pth('M25 60 Q32 54 39 60')+pth('M37 60 Q44 54 51 60'),
# III practitioners: a person next to a shipped box with a check
'icon-practitioners': cir(18,18,6)+pth('M6 46 Q6 30 18 30 Q30 30 30 46')+rec(34,26,24,22,2)+pth('M34 33 H58')+pth('M46 26 V33')
   +g(pth('M40 42 L45 46 L53 37','ic-acc'),'ic-m ic-redraw'),
# IV leverage: fulcrum, beam, small weight lifting a big block
'icon-leverage': pth('M28 56 L34 44 L40 56 Z')+g(pth('M6 40 L60 48')+cir(10,34,5,'ic-acc')+rec(44,28,16,16,2),'ic-m ic-tilt'),
# V reflection: notebook with lines being written and a pen
'icon-examined': rec(12,8,34,48,3)+pth('M18 8 V56','ic-faint')+g(pth('M24 20 H40')+pth('M24 28 H40')+pth('M24 36 H34'),'ic-m ic-redraw')
   +g(pth('M44 50 L56 26 L60 28 L48 52 L43 54 Z','ic-acc'),'ic-m2 ic-scribble'),
# VI risk early: small steps rising, a dot hopping up them
'icon-risk': pth('M4 58 H18 V48 H32 V36 H46 V22 H60')+g(cir(11,52,4,'ic-acc'),'ic-m ic-hop'),
# VII daily habits: calendar with checks appearing
'icon-systems': rec(8,12,48,44,3)+pth('M8 24 H56')+pth('M20 6 V16')+pth('M44 6 V16')
   +g(pth('M14 34 L17 37 L22 31','ic-acc c1')+pth('M28 34 L31 37 L36 31','ic-acc c2')+pth('M42 34 L45 37 L50 31','ic-acc c3')
      +pth('M14 46 L17 49 L22 43','ic-acc c4')+pth('M28 46 L31 49 L36 43','ic-acc c5'),'ic-m ic-seq'),
# VIII first principles: magnifier examining a question mark
'icon-water': pth('M22 20 Q22 12 30 12 Q38 12 38 19 Q38 25 30 27 V32')+cir(30,39,1.5)
   +g(cir(40,40,11,'ic-acc')+pth('M48 48 L58 58','ic-acc'),'ic-m ic-scan'),
# cascade: just-in-time teaching: clock, hand turns
'icon-morning': cir(32,34,22)+pth('M32 14 V18')+pth('M32 50 V54')+pth('M12 34 H16')+pth('M48 34 H52')+pth('M24 6 H40','ic-faint')
   +g(pth('M32 34 V21','ic-acc'),'ic-m ic-spin')+pth('M32 34 L41 39'),
# build blocks: code window, cursor blinks
'icon-afternoon': rec(6,10,52,44,3)+pth('M6 20 H58')+cir(12,15,1)+cir(17,15,1)+pth('M22 30 L15 37 L22 44','ic-acc')+pth('M34 28 L28 46')
   +g(pth('M42 38 V46','ic-acc'),'ic-m ic-blink'),
# practitioner 1:1s: two people, speech bubble pops
'icon-mentor': cir(18,30,6)+pth('M6 56 Q6 42 18 42 Q30 42 30 56')+cir(44,32,5)+pth('M34 56 Q34 44 44 44 Q54 44 54 56')
   +g(pth('M34 6 H56 Q59 6 59 9 V17 Q59 20 56 20 H44 L39 25 V20 H34 Q31 20 31 17 V9 Q31 6 34 6 Z','ic-acc'),'ic-m ic-pop'),
# the freeze: hourglass flips
'icon-quiet': g(pth('M18 8 H46')+pth('M18 56 H46')+pth('M21 8 Q21 24 32 32 Q43 24 43 8')+pth('M21 56 Q21 40 32 32 Q43 40 43 56')
   +pth('M26 50 Q32 44 38 50 Z','ic-acc'),'ic-m ic-flip'),
# daily standups: kanban board, a card moves across
'icon-commits': rec(6,10,52,44,3)+pth('M23 10 V54')+pth('M41 10 V54')+rec(9,18,11,7,1)+rec(9,29,11,7,1)+rec(44,18,11,7,1)
   +g(rec(26,18,12,7,1,'ic-acc'),'ic-m ic-move'),
# demo day: stage with a speaker and spotlight rays
'icon-demo': pth('M6 56 H58')+pth('M12 56 V48 H52 V56')+cir(32,30,5)+pth('M25 48 Q25 38 32 38 Q39 38 39 48')
   +g(pth('M32 6 V14','ic-acc')+pth('M18 10 L22 17','ic-acc')+pth('M46 10 L42 17','ic-acc'),'ic-m ic-pulse'),
# formats around school: calendar with the break week highlighted
'icon-travel': rec(8,12,48,44,3)+pth('M8 24 H56')+pth('M20 6 V16')+pth('M44 6 V16')+pth('M14 34 H50','ic-faint')+pth('M14 46 H50','ic-faint')
   +g(rec(12,30,16,8,2,'ic-acc'),'ic-m ic-slide'),
}
def svg(key, cls): return '<svg class="%s ic" viewBox="0 0 64 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">%s</svg>'%(cls,I[key])
