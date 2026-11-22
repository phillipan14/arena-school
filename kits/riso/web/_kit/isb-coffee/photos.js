/* In-circle portraits, matched by measured face size.
   Circle diameter = SCALE face widths; the top of the hair sits HEAD_GAP of the diameter below the circle top;
   the face is centered horizontally (data-cx). Everything is clipped to the circle. */
const SCALE=2.05, HEAD_GAP=0.05;
document.querySelectorAll('.ph').forEach(el=>{
  const D=el.offsetWidth, f=+el.dataset.face, d=(+(el.dataset.scale||SCALE))*f, s=D/d, gap=+(el.dataset.gap||HEAD_GAP);
  const disc=document.createElement('div'); disc.className='disc'; el.appendChild(disc);
  const img=new Image(); img.src=el.dataset.src; img.alt='';
  img.style.width=(+el.dataset.w*s)+'px';
  img.style.left=(D/2 - (+el.dataset.cx)*s)+'px';
  img.style.top=(gap*D - (+el.dataset.hair)*s)+'px';
  disc.appendChild(img);
});
document.querySelectorAll('.box').forEach(b=>{
  const s=document.createElement('span'); s.className='t-in';
  [...b.childNodes].filter(n=>!(n.nodeType===1&&n.tagName==='I')).forEach(n=>s.appendChild(n));
  b.appendChild(s);
});
