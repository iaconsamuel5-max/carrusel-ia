import subprocess,sys
from playwright.sync_api import sync_playwright
style,D,offset,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4];FPS=30
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file:///home/claude/estilos/styles.html");pg.wait_for_timeout(500)
    for i in range(int(D*FPS)):
        pg.evaluate(f"render('{style}',{offset+i/FPS},1080,1350)");ff.stdin.write(pg.locator("canvas").screenshot(type="jpeg",quality=92))
    b.close()
ff.stdin.close();ff.wait()
