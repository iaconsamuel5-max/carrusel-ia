import subprocess,sys
from playwright.sync_api import sync_playwright
D=12.0; FPS=30; N=int(D*FPS)
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","tmp_video.mp4"],stdin=subprocess.PIPE)
only=[float(a) for a in sys.argv[1:]]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file:///home/claude/hud/hud.html");pg.wait_for_timeout(500)
    if only:
        for t in only:
            pg.evaluate(f"draw({t})");pg.screenshot(path=f"prev_{t}.jpg",type="jpeg",quality=90)
        ff.stdin.close();b.close();sys.exit()
    for i in range(N):
        pg.evaluate(f"draw({i/FPS})");ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
    b.close()
ff.stdin.close();ff.wait()
