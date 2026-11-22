import asyncio, subprocess, sys
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/estilos")
from playwright.async_api import async_playwright
from gen import BASE
import music
D, FPS = 12.0, 30
rows="".join(f'<tr id="r{i}"><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for i,(a,b,c) in enumerate([("4 mA","0 %","0,0 bar"),("8 mA","25 %","2,5 bar"),("12 mA","50 %","5,0 bar"),("16 mA","75 %","7,5 bar"),("20 mA","100 %","10,0 bar")]))
body=f'''<div class="num" style="font-size:40px">Ficha #1</div><span class="tag">FICHA DE CAMPO · INSTRUMENTACIÓN</span>
<h1 style="font-size:80px;margin-top:18px">Señal <span class="hl">4-20 <span style="font-family:Kalam;font-weight:700">mA</span></span> a<br>presión real</h1>
<div style="position:relative;margin-top:16px;border:5px solid #FF6B2C;border-radius:14px;background:#FFFDF7;padding:8px">
<canvas id="c" width="860" height="330" style="display:block"></canvas></div>
<div class="card" style="margin-top:16px;padding:14px 22px"><div class="who">FÓRMULA · transmisor 0-10 bar</div>
<p style="font-size:38px;font-family:Marker;line-height:1.2">P = (I − 4) ÷ 16 × Rango</p>
<p style="font-size:31px">12 mA → (12 − 4) ÷ 16 × 10 = <b style="background:#FFE14D;padding:0 8px">5,0 bar</b></p></div>
<table style="width:100%;border-collapse:collapse;margin-top:14px;font-family:Kalam;font-size:27px;text-align:center;background:#FFFDF7">
<tr style="background:#1E1E1E;color:#FFE14D;font-family:Marker"><td>Señal</td><td>% del rango</td><td>Presión</td></tr>{rows}</table>
<style>table td{{border:3px solid #FF6B2C;padding:0}} tr.on td{{background:#FFE14D;font-weight:700}}</style>
<div style="font-family:Kalam;font-size:27px;margin-top:10px;line-height:1.25"><b style="color:#FF6B2C">¿Por qué 4 y no 0?</b> Si lees 0 mA, el lazo está abierto ("cero vivo"). Menos de 3,6 mA o más de 21 mA: revisa (NAMUR NE43).</div>
<div class="card" style="margin-top:10px;padding:10px 22px;border-color:#2F6DB5"><div class="who">PROMPT IA (ChatGPT · Copilot · Gemini)</div>
<p style="font-size:25px">"Tengo un transmisor de [0-10 bar] con salida 4-20 mA. Hazme la tabla de conversión cada 1 mA y dime cómo detectar falla de lazo."</p></div>
<div style="position:absolute;left:0;right:0;bottom:-34px;display:flex;justify-content:space-between;font-family:Kalam;font-weight:700;font-size:27px"><span>Samuel Sánchez · <span style="color:#FF6B2C">IA con Samuel</span></span><span>Guárdala para el taller 📌</span></div>'''
JS = r'''<script>
const c=document.getElementById('c'),x=c.getContext('2d');
const SEQ=[4,8,12,16,20,12],H=1.6,T=0.4;
function I(t){const k=Math.floor(t/(H+T))%SEQ.length,u=t-Math.floor(t/(H+T))*(H+T),a=SEQ[k],b=SEQ[(k+1)%SEQ.length];
 if(u<H)return a;const e=(u-H)/T,s=e*e*(3-2*e);return a+(b-a)*s;}
const P=[[130,40],[740,40],[740,300],[130,300]];let L=[],tot=0;
for(let i=0;i<4;i++){const a=P[i],b=P[(i+1)%4],l=Math.hypot(b[0]-a[0],b[1]-a[1]);L.push(l);tot+=l;}
function at(d){d=((d%tot)+tot)%tot;for(let i=0;i<4;i++){if(d<=L[i]){const a=P[i],b=P[(i+1)%4],f=d/L[i];return[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f]}d-=L[i]}}
function rr(X,Y,W,Hh,r,f,s){x.beginPath();x.roundRect(X,Y,W,Hh,r);x.fillStyle=f;x.fill();if(s){x.lineWidth=5;x.strokeStyle='#1E1E1E';x.stroke()}}
let dist=0,lastT=0;
window.draw=function(t){
 const i=I(t),p=(i-4)/16*10;dist+=(t-lastT)*i*14;lastT=t;
 x.clearRect(0,0,860,330);
 x.lineWidth=9;x.strokeStyle='#1E1E1E';x.beginPath();x.moveTo(...P[0]);P.slice(1).forEach(q=>x.lineTo(...q));x.closePath();x.stroke();
 x.lineWidth=4;x.strokeStyle='#C0392B';x.beginPath();x.moveTo(130,40);x.lineTo(740,40);x.stroke();
 const N=26;for(let k=0;k<N;k++){const q=at(dist+k*tot/N);x.beginPath();x.arc(q[0],q[1],9,0,7);x.fillStyle='rgba(255,107,44,.35)';x.fill();x.beginPath();x.arc(q[0],q[1],5.5,0,7);x.fillStyle='#FF6B2C';x.fill();}
 // fuente
 rr(380,12,190,58,10,'#2B2B2B',1);x.fillStyle='#FFE14D';x.font='700 30px Inter';x.textAlign='center';x.fillText('24 V DC',475,52);
 // flecha
 x.fillStyle='#1E1E1E';x.font='700 24px Kalam';x.fillText('corriente del lazo →',430,290);
 // transmisor
 rr(55,95,150,120,22,'#9FB8D6',1);rr(75,115,110,62,8,'#DFF3FF',1);
 x.fillStyle='#1E1E1E';x.font='700 30px Inter';x.fillText(p.toFixed(1).replace('.',','),130,147);x.font='600 18px Inter';x.fillText('bar',130,168);
 rr(112,215,36,40,0,'#C9CED6',1);rr(92,255,76,28,4,'#E5B85C',1);
 x.fillStyle='#1E1E1E';x.textAlign='left';x.font='700 26px Kalam';x.fillText('Transmisor',220,150);x.fillText('0-10 bar',220,180);x.font='600 20px Kalam';x.fillStyle='#2F6DB5';x.fillText('presión',20,258);x.textAlign='center';
 // presión entrando (flecha que pulsa)
 x.strokeStyle='#2F6DB5';x.lineWidth=6;const a=Math.sin(t*6)*4;x.beginPath();x.moveTo(30,269+a);x.lineTo(88,269);x.stroke();
 // multímetro
 rr(660,75,165,230,20,'#F2C230',1);rr(676,92,133,72,8,'#C8D8C0',1);
 x.fillStyle='#1E1E1E';x.font='700 34px Inter';x.fillText(i.toFixed(2).replace('.',','),742,134);x.font='700 17px Inter';x.fillText('mA DC',742,156);
 x.beginPath();x.arc(742,210,30,0,7);x.fillStyle='#2B2B2B';x.fill();x.save();x.translate(742,210);x.rotate(-0.6);x.fillStyle='#fff';x.fillRect(-3,-28,6,22);x.restore();
 x.beginPath();x.arc(702,275,9,0,7);x.fillStyle='#C0392B';x.fill();x.beginPath();x.arc(782,275,9,0,7);x.fillStyle='#1E1E1E';x.fill();
 x.fillStyle='#1E1E1E';x.textAlign='right';x.font='700 26px Kalam';x.fillText('Multímetro',645,150);x.fillText('en serie',645,180);x.textAlign='center';
 // fila activa
 [4,8,12,16,20].forEach((v,k)=>document.getElementById('r'+k).className=Math.abs(i-v)<0.6?'on':'');
};</script>'''
async def main(static=False):
    open("ficha_anim.html","w").write(BASE.replace("BODY",body).replace("height:1350px","height:1440px").replace("</body>",JS+"</body>"))
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1440})
        await pg.goto("file:///home/claude/bitacora/ficha_anim.html"); await pg.wait_for_timeout(600)
        if static:
            for f in range(0,int(4.3*FPS)): await pg.evaluate(f"draw({f/FPS})")
            await pg.screenshot(path="ficha_4_20mA_v2.jpg",type="jpeg",quality=90); await b.close(); return
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","v.mp4"],stdin=subprocess.PIPE)
        for f in range(int(D*FPS)):
            await pg.evaluate(f"draw({f/FPS})"); ff.stdin.write(await pg.screenshot(type="jpeg",quality=92))
        await b.close(); ff.stdin.close(); ff.wait()
    music.write("m2.wav",music.mix(D,"corporate"))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","v.mp4","-i","m2.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","ficha_4_20mA_animada.mp4"],check=True)
asyncio.run(main(static=len(sys.argv)>1))
