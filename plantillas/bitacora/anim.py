import asyncio, subprocess, sys
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/estilos")
from playwright.async_api import async_playwright
from gen import BASE, mascot, foot, ARROW
import music

D, FPS = 9.0, 30
REPLY = "¡Hola, vecino! Hoy hay empanadas de carne y de pollo, recién hechas. 3 por $6.000 hasta las 7 p. m. ¿Te aparto unas?"

body = f'''<div class="num">3/8</div><span class="tag">PROMPT 1 · WHATSAPP</span>
<h1 style="font-size:92px"><span class="hl">La IA te escribe</span><br>los WhatsApp</h1>
<div style="font-family:Kalam;font-weight:700;font-size:36px;margin-top:10px">Tú solo copias, pegas y envías.</div>
<div style="position:absolute;left:0;right:0;top:390px;height:560px;border:6px solid #FF6B2C;border-radius:14px;background:#FFFDF7;padding:14px">
 <canvas id="c" width="808" height="520" style="display:block;border-radius:8px"></canvas>
</div>
<div style="position:absolute;left:-20px;bottom:30px">{mascot("thumbs",210)}</div>
<div style="position:absolute;left:250px;bottom:110px;width:640px;font-family:Kalam;font-size:31px;line-height:1.3;background:#FFE14D;border-radius:12px;padding:16px 20px;transform:rotate(-1deg)">
 <b>Prompt:</b> "Escribe un mensaje corto y amable para ofrecer [producto] hoy a mis clientes de [barrio]."</div>
{foot()}'''

JS = r'''<script>
const R = REPLY_JSON;
const c=document.getElementById('c'),x=c.getContext('2d');
function rr(X,Y,W,H,r,f){x.beginPath();x.roundRect(X,Y,W,H,r);x.fillStyle=f;x.fill();}
function wrap(t,X,Y,W,lh){let w=t.split(' '),l='',y=Y;for(const s of w){const tt=l?l+' '+s:s;if(x.measureText(tt).width>W){x.fillText(l,X,y);l=s;y+=lh}else l=tt}if(l)x.fillText(l,X,y);return y}
window.draw=function(t){
 x.fillStyle='#E9DDCF';x.fillRect(0,0,808,520);
 for(let i=0;i<40;i++){x.fillStyle='rgba(0,0,0,.035)';x.beginPath();x.arc((i*97)%808,(i*53)%520,14,0,7);x.fill()}
 rr(0,0,808,76,0,'#1F7A5C');x.fillStyle='#fff';x.font='700 26px Inter';x.fillText('Empanadas Doña Rosa',80,34);
 x.beginPath();x.arc(42,38,22,0,7);x.fillStyle='#FFE14D';x.fill();
 x.font='500 18px Inter';x.fillStyle='#CFEDE2';x.fillText((t>1.3&&t<5.6)?'escribiendo...':'en línea',80,64);
 // cliente
 if(t>0.4){const a=Math.min(1,(t-.4)/.3);x.globalAlpha=a;rr(24,90,420,62,14,'#fff');x.fillStyle='#1E1E1E';x.font='500 26px Inter';x.fillText('¿Tienen empanadas hoy?',44,130);x.globalAlpha=1}
 // puntos escribiendo
 if(t>1.3&&t<2.6){rr(560,180,110,52,14,'#D9FDD3');for(let i=0;i<3;i++){const y=206+Math.sin(t*9+i)*5;x.beginPath();x.arc(590+i*25,y,7,0,7);x.fillStyle='#7A8B85';x.fill()}}
 // respuesta tecleada
 if(t>=2.6){const n=Math.min(R.length,Math.floor((t-2.6)*34));const s=R.slice(0,n);
  x.font='500 26px Inter';rr(250,180,534,200,14,'#D9FDD3');x.fillStyle='#1E1E1E';
  wrap(s+(n<R.length&&Math.floor(t*4)%2?'|':''),272,220,490,36);
  if(n>=R.length){x.font='500 18px Inter';x.fillStyle='#4FA3F7';x.fillText('7:02 p. m. ✓✓',650,368)}}
 // etiqueta IA
 if(t>2.6){const p=Math.min(1,(t-2.6)/.4);rr(560,400,220,54,27,'rgba(255,107,44,'+p+')');x.fillStyle='rgba(255,255,255,'+p+')';x.font='700 22px Inter';x.fillText('Escrito con IA',592,434)}
 // pedido entra al final
 if(t>7.3){const a=Math.min(1,(t-7.3)/.3);x.globalAlpha=a;rr(24,400,330,62,14,'#fff');x.fillStyle='#1E1E1E';x.font='500 26px Inter';x.fillText('¡Sí! Apártame 6',44,440);x.globalAlpha=1}
};
</script>'''.replace("REPLY_JSON", repr(REPLY))

async def main():
    page_html = BASE.replace("BODY", body).replace("</body>", JS + "</body>")
    open("anim.html", "w").write(page_html)
    ff = subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-i","-",
        "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","video.mp4"], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        await pg.goto("file:///home/claude/bitacora/anim.html"); await pg.wait_for_timeout(600)
        for f in range(int(D*FPS)):
            await pg.evaluate(f"draw({f/FPS})")
            ff.stdin.write(await pg.screenshot(type="jpeg", quality=92))
        await b.close()
    ff.stdin.close(); ff.wait()
    music.write("m.wav", music.mix(D, "funky"))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","video.mp4","-i","m.wav","-map","0:v","-map","1:a",
        "-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","lamina_03_animada.mp4"], check=True)
asyncio.run(main())
