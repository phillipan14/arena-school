"""Build preview.html from out/ and data.js captions."""
import json, re, glob, html, pathlib, subprocess
ROOT=pathlib.Path(__file__).parent
js=(ROOT/"data.js").read_text()
posts=json.loads(subprocess.run(["node","-e",js.replace("window.","globalThis.")+";console.log(JSON.stringify(POSTS))"],capture_output=True,text=True).stdout)
rows=[]
for p in posts:
    fs=sorted(glob.glob(str(ROOT/f"out/post-{p['n']:02d}/slide-*.png")))
    imgs="".join(f'<figure><img src="out/post-{p["n"]:02d}/{pathlib.Path(f).name}" loading="lazy"><figcaption>{k+1}/{len(fs)}</figcaption></figure>' for k,f in enumerate(fs))
    c=p["caption"]
    rows.append(f'''<section><div class="meta"><span class="n">POST {p["n"]:02d} · {html.escape(p["tag"])} · {len(fs)} 张</span>
<h2>{html.escape(c["title"])}</h2><pre>{html.escape(c["body"] + chr(10)*2 + " ".join(c["tags"]))}</pre></div><div class="rail">{imgs}</div></section>''')
page=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arena School · 小红书 carousels</title><link rel="stylesheet" href="assets/fonts-cjk.css"><link rel="stylesheet" href="assets/fonts-site.css">
<style>
:root{{--paper:#EFE3D4;--card:#F6EDE2;--ink:#0E1729;--ink2:#3B4660;--blue:#22458A;--coral:#E59375}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Geist","Noto Sans SC",sans-serif}}
header{{padding:34px 36px 14px;display:flex;align-items:center;gap:18px;border-bottom:2px solid var(--ink)}}
header img{{width:54px}}header h1{{margin:0;font-family:"Noto Serif SC",serif;font-size:28px}}header p{{margin:4px 0 0;color:var(--ink2);font-size:14px}}
section{{display:grid;grid-template-columns:340px 1fr;gap:26px;padding:28px 36px;border-bottom:1px solid rgba(14,23,41,.18)}}
.n{{font:12px "Geist Mono",monospace;letter-spacing:.12em;color:var(--blue)}}.meta h2{{font-family:"Noto Serif SC",serif;font-size:21px;margin:8px 0 10px}}
pre{{white-space:pre-wrap;font:14px/1.75 "Noto Sans SC",sans-serif;background:var(--card);border:2px solid var(--ink);box-shadow:5px 5px 0 var(--blue);padding:14px 16px;margin:0;max-height:440px;overflow:auto}}
.tags{{font-size:13px;color:var(--blue);margin:14px 0 0}}
.rail{{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:4px 4px 12px}}
figure{{margin:0;flex:0 0 auto;scroll-snap-align:start}}figure img{{height:560px;aspect-ratio:3/4;display:block;border:2px solid var(--ink);cursor:zoom-in;background:#fff}}
figcaption{{font:11px "Geist Mono",monospace;color:var(--ink2);margin-top:6px;text-align:center}}
#z{{position:fixed;inset:0;background:rgba(14,23,41,.88);display:none;place-items:center;z-index:9}}#z img{{max-height:95vh;max-width:95vw}}
@media (max-width:760px){{section{{grid-template-columns:1fr}}figure img{{height:440px}}}}
</style>
<header><img src="assets/seal-halo-720.png"><div><h1>Arena School · 小红书 carousels · 草稿 1</h1><p>6 posts · 3:4 (1080×1440) · 左右滑动每一行 · 点击放大 · 左侧是配文草稿</p></div></header>
{"".join(rows)}
<div id="z" onclick="this.style.display='none'"><img></div>
<script>document.querySelectorAll('figure img').forEach(i=>i.onclick=()=>{{const z=document.getElementById('z');z.querySelector('img').src=i.src;z.style.display='grid'}})</script></html>'''
(ROOT/"preview.html").write_text(page); print("ok")
