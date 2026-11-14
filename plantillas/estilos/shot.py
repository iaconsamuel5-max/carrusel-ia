import sys,subprocess
from playwright.sync_api import sync_playwright
from PIL import Image
def go(jobs):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1080,"height":1920})
        pg.goto("file:///home/claude/estilos/styles.html");pg.wait_for_timeout(500)
        for style,t,w,h,out in jobs:
            pg.set_viewport_size({"width":w,"height":h});pg.evaluate(f"render('{style}',{t},{w},{h})")
            pg.locator("canvas").screenshot(path=out,type="jpeg",quality=92)
        b.close()
if __name__=="__main__":
    go([("radar",3.2,1080,1350,"img_radar.jpg"),("blueprint",9,1080,1350,"img_blueprint.jpg"),("comic",9,1080,1350,"img_comic.jpg")])
