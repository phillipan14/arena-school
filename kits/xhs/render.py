"""Render Arena carousel slides: python3 render.py [post numbers]  -> out/post-XX/slide-YY.png (1080x1440)"""
import asyncio, os, sys, pathlib
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).parent.resolve()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1440})
        await pg.goto((ROOT/"slide.html").as_uri()+"?p=1&s=0"); await pg.wait_for_function("window.__ready===true", timeout=60000)
        counts=await pg.evaluate("window.__counts")
        want=[int(a) for a in sys.argv[1:]] or list(range(1,len(counts)+1))
        for n in want:
            d=ROOT/"out"/f"post-{n:02d}"; d.mkdir(parents=True, exist_ok=True)
            for f in d.glob("slide-*.png"): f.unlink()
            for s in range(counts[n-1]):
                await pg.goto((ROOT/"slide.html").as_uri()+f"?p={n}&s={s}"); await pg.wait_for_function("window.__ready===true", timeout=60000); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(d/f"slide-{s+1:02d}.png"))
            print(f"post {n}: {counts[n-1]} slides")
        await b.close()
asyncio.run(main())
