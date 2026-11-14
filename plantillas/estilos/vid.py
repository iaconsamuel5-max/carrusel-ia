import subprocess,sys
from playwright.sync_api import sync_playwright
style,D=sys.argv[1],float(sys.argv[2]);FPS=30;N=int(D*FPS)
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-vf","fade=in:st=0:d=0.4,fade=out:st=%.2f:d=0.4"%(D-0.4),"-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",f"tmp_{style}.mp4"],stdin=subprocess.PIPE)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file:///home/claude/estilos/styles.html");pg.wait_for_timeout(500)
    for i in range(N):
        pg.evaluate(f"render('{style}',{i/FPS},1080,1920)");ff.stdin.write(pg.locator("canvas").screenshot(type="jpeg",quality=92))
    b.close()
ff.stdin.close();ff.wait()
