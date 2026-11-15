import subprocess,sys,http.server,threading,functools
from playwright.sync_api import sync_playwright
srv=http.server.ThreadingHTTPServer(("127.0.0.1",8765),functools.partial(http.server.SimpleHTTPRequestHandler,directory="/home/claude/tresd",))
threading.Thread(target=srv.serve_forever,daemon=True).start()
D=float(sys.argv[1]) if len(sys.argv)>1 else 0;FPS=30
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    pg=b.new_page(viewport={"width":1080,"height":1350});pg.goto("http://127.0.0.1:8765/scene_valve.html");pg.wait_for_function("window.ready===true",timeout=30000);pg.wait_for_timeout(500)
    if D==0:
        for t in (0,2,5):pg.evaluate(f"draw({t})");pg.screenshot(path=f"v{t}.jpg",type="jpeg",quality=90)
    else:
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","tmp_valve.mp4"],stdin=subprocess.PIPE)
        for i in range(int(D*FPS)):pg.evaluate(f"draw({i/FPS})");ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
        ff.stdin.close();ff.wait()
    b.close()
srv.shutdown()
