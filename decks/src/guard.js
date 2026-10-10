<script>
/* CJK orphan guard: keep the last 3 characters (plus closing punctuation) of each text block together */
(function(){var sel='__SEL__';var re=/([\u3400-\u9fff][\u3400-\u9fff\u3000-\u303f\uff00-\uffef“”‘’」』]{0,2}[\u3400-\u9fff][\u3000-\u303f\uff00-\uffef“”‘’」』?？。，、！]*\s*)$/;
document.querySelectorAll(sel).forEach(function(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,last=null;while(n=w.nextNode()){if(n.nodeValue.trim())last=n}
 if(!last)return;var m=last.nodeValue.match(re);if(!m)return;var t=last.nodeValue;var sp=document.createElement('span');sp.style.whiteSpace='nowrap';sp.textContent=m[1];last.nodeValue=t.slice(0,t.length-m[1].length);last.parentNode.insertBefore(sp,last.nextSibling)})})();
</script>