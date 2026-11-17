import asyncio, subprocess, numpy as np, sys
from PIL import Image
from playwright.async_api import async_playwright
O='out'
base_html=open(f'{O}/story.html').read().replace('<img src="lamina_01.png">','')
open(f'{O}/story_base.html','w').write(base_html)
async def r():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file://"+__import__('os').path.abspath(f'{O}/story_base.html'));await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{O}/story_base.png');await b.close()
asyncio.run(r())
base=Image.open(f'{O}/story_base.png').convert('RGB')
sl=[Image.open(f'{O}/lamina_{i:02d}.png').convert('RGB').resize((1000,1250),Image.LANCZOS) for i in range(1,9)]
FPS=30;PER=1.6;TR=0.35;D=8*PER+0.4
N=int(D*FPS)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30','v.mp4'],stdin=subprocess.PIPE)
def zoomed(im,z):
    w,h=int(1000*z),int(1250*z);im2=im.resize((w,h),Image.BILINEAR);l=(w-1000)//2;t=(h-1250)//2;return im2.crop((l,t,l+1000,t+1250))
import io
for f in range(N):
    t=f/FPS;i=min(int(t/PER),7);lt=t-i*PER
    fr=base.copy()
    z=1+0.04*min(lt/PER,1)
    cur=zoomed(sl[i],z)
    if i>0 and lt<TR:
        k=lt/TR;k=1-(1-k)**3
        prev=zoomed(sl[i-1],1.04)
        fr.paste(prev,(int(40-1080*k),190));fr.paste(cur,(int(40+1080*(1-k)),190))
    else: fr.paste(cur,(40,190))
    bio=io.BytesIO();fr.save(bio,'JPEG',quality=92);ff.stdin.write(bio.getvalue())
ff.stdin.close();ff.wait()
sys.path.insert(0,'/home/claude/carrusel-ia/plantillas/estilos')
import music
a=music.mix(D,'corporate')
# sonido ancla: campanita suave al inicio
SR=music.SR;n=int(.8*SR);tt=np.arange(n)/SR;ch=sum(np.sin(2*np.pi*f*tt) for f in (880,1320,1760))*np.exp(-tt/.25)*.25
a[:n]+=ch
music.write('a.wav',a)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','v.mp4','-i','a.wav','-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',f'{O}/historia_01.mp4'],check=True)
print('ok',D)
