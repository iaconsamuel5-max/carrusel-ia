import asyncio, subprocess, sys
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/estilos")
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/bitacora")
from playwright.async_api import async_playwright
from gen import BASE
import music, numpy as np
D, FPS = 12.6, 30
rows="".join(f'<tr id="r{i}"><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for i,(a,b,c,d) in enumerate([("Abierta","66,7 m³/h","27,8 m","0 m"),("A medias","51,6 m³/h","36,7 m","16,0 m"),("Estrangulada","36,5 m³/h","43,3 m","28,0 m")]))
body=f'''<div class="num" style="font-size:40px">Ficha #4</div><span class="tag">FICHA DE CAMPO · BOMBAS</span>
<h1 style="font-size:64px;margin-top:16px">¿Dónde trabaja <span class="hl">tu bomba</span>?</h1>
<div style="font-family:Kalam;font-size:29px;margin-top:4px">Donde se cruzan la curva de la bomba y la del sistema.</div>
<div style="position:relative;margin-top:10px;border:5px solid #FF6B2C;border-radius:14px;background:#FFFDF7;padding:6px">
<canvas id="c" width="866" height="400" style="display:block"></canvas></div>
<div class="card" style="margin-top:12px;padding:12px 22px"><div class="who">FÓRMULA · bomba H = 50 − 0,005·Q² · sistema H = 10 + r·Q²</div>
<p style="font-size:33px;font-family:Inter;font-weight:700;line-height:1.3">Q = √[(Hmáx − Hest) ÷ (k + r)]</p>
<p style="font-size:27px">Válvula abierta (r = 0,004): √(40 ÷ 0,009) = <b style="background:#FFE14D;padding:0 8px">66,7 m³/h a 27,8 m</b></p></div>
<table style="width:100%;border-collapse:collapse;margin-top:12px;font-family:Kalam;font-size:26px;text-align:center;background:#FFFDF7">
<tr style="background:#1E1E1E;color:#FFE14D;font-family:Marker;font-size:24px"><td>Válvula</td><td>Caudal</td><td>Altura bomba</td><td>Se pierde en válvula</td></tr>{rows}</table>
<style>table td{{border:3px solid #FF6B2C;padding:0}} tr.on td{{background:#FFE14D;font-weight:700}}</style>
<div style="font-family:Kalam;font-size:27px;margin-top:12px;line-height:1.25"><b style="color:#FF6B2C">Lección:</b> cerrar la válvula no cambia la bomba, cambia el sistema: baja el caudal, sube la presión y esa energía se quema en la válvula. Si siempre trabaja estrangulada, evalúa un variador o recortar el impulsor.</div>
<div class="card" style="margin-top:8px;padding:8px 22px;border-color:#2F6DB5"><div class="who">PROMPT IA (ChatGPT · Copilot · Gemini)</div>
<p style="font-size:24px;line-height:1.25">"Con estos puntos de la curva de mi bomba [Q, H] y mi sistema (altura estática [m], un punto de operación medido), calcula el punto de operación y cuánta energía pierdo en la válvula."</p></div>
<div style="position:absolute;left:0;right:0;bottom:-36px;display:flex;justify-content:space-between;font-family:Kalam;font-weight:700;font-size:27px"><span>Samuel Sánchez · <span style="color:#FF6B2C">IA con Samuel</span></span><span>Guárdala para el taller 📌</span></div>'''
JS = r'''<script>
const c=document.getElementById('c'),x=c.getContext('2d');
const SEQ=[0.004,0.010,0.025],HD=3.4,TR=0.8;
function R(t){const P=HD+TR,k=Math.floor(t/P)%3,u=t-Math.floor(t/P)*P,a=SEQ[k],b=SEQ[(k+1)%3];
 if(u<HD)return a;const e=(u-HD)/TR,s=e*e*(3-2*e);return a+(b-a)*s;}
const fmt=(v,d)=>v.toFixed(d).replace('.',',');
function rr(X,Y,W,H,r,f,s){x.beginPath();x.roundRect(X,Y,W,H,r);x.fillStyle=f;x.fill();if(s){x.lineWidth=4;x.strokeStyle='#1E1E1E';x.stroke()}}
// tubería
const PATH=[[60,300],[120,300],[150,300],[300,300],[300,190],[300,90],[372,90]];let L=[],tot=0;
for(let i=0;i<PATH.length-1;i++){const l=Math.hypot(PATH[i+1][0]-PATH[i][0],PATH[i+1][1]-PATH[i][1]);L.push(l);tot+=l;}
function at(d){d=((d%tot)+tot)%tot;for(let i=0;i<L.length;i++){if(d<=L[i]){const a=PATH[i],b=PATH[i+1],f=d/L[i];return[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f]}d-=L[i]}}
// gráfica
const GX=530,GY=40,GW=305,GH=300,QM=90,HM=60;
const px=q=>GX+q/QM*GW,py=h=>GY+GH-h/HM*GH;
let dist=0,lastT=0,ang=0;
window.draw=function(t){
 const r=R(t),Q=Math.sqrt(40/(0.005+r)),H=50-0.005*Q*Q,loss=(r-0.004)*Q*Q;
 const dt=t-lastT;dist+=dt*Q*2.6;ang+=dt*14;lastT=t;
 x.clearRect(0,0,866,380);x.textAlign='center';
 // tanques
 rr(10,250,90,110,6,'#DCEBF7',1);x.fillStyle='#7FB3E0';x.fillRect(12,285,86,73);
 rr(345,30,110,110,6,'#DCEBF7',1);x.fillStyle='#7FB3E0';x.fillRect(347,62,106,76);
 x.fillStyle='#1E1E1E';x.font='700 20px Kalam';x.fillText('succión',55,245);x.fillText('descarga',400,25);
 // tubería
 x.lineCap='round';x.lineJoin='round';x.lineWidth=20;x.strokeStyle='#1E1E1E';x.beginPath();x.moveTo(...PATH[0]);PATH.slice(1).forEach(q=>x.lineTo(...q));x.stroke();
 x.lineWidth=13;x.strokeStyle='#CFE6F7';x.stroke();
 for(let k=0;k<22;k++){const q=at(dist+k*tot/22);x.beginPath();x.arc(q[0],q[1],5,0,7);x.fillStyle='#2F6DB5';x.fill();}
 // bomba
 x.beginPath();x.arc(150,300,40,0,7);x.fillStyle='#FF6B2C';x.fill();x.lineWidth=4;x.strokeStyle='#1E1E1E';x.stroke();
 x.save();x.translate(150,300);x.rotate(ang);x.strokeStyle='#1E1E1E';x.lineWidth=5;for(let k=0;k<5;k++){x.rotate(Math.PI*2/5);x.beginPath();x.moveTo(5,0);x.quadraticCurveTo(18,10,28,4);x.stroke();}x.restore();
 x.fillStyle='#1E1E1E';x.font='700 22px Kalam';x.fillText('bomba',150,365);
 // válvula
 const vy=190,op=(0.025-r)/0.021; // 1 abierta, 0 estrangulada
 x.fillStyle='#FFFDF7';x.strokeStyle='#1E1E1E';x.lineWidth=4;
 x.beginPath();x.moveTo(278,vy-26);x.lineTo(322,vy-26);x.lineTo(278,vy+26);x.lineTo(322,vy+26);x.closePath();x.fill();x.stroke();
 x.beginPath();x.moveTo(300,vy);x.lineTo(340,vy);x.stroke();
 x.fillStyle='#C0392B';x.fillRect(340,vy-8-(1-op)*0,10,16);x.beginPath();x.arc(352,vy,14,0,7);x.fill();
 x.fillStyle='#1E1E1E';x.textAlign='left';x.font='700 21px Kalam';x.fillText('válvula',372,vy-6);
 x.fillStyle='#C0392B';x.fillText(op>0.8?'abierta':op>0.4?'a medias':'estrangulada',372,vy+20);
 // lectura
 rr(172,105,112,62,8,'#2B2B2B',1);x.fillStyle='#FFE14D';x.textAlign='center';x.font='700 24px Inter';x.fillText(fmt(Q,1),228,133);x.font='600 15px Inter';x.fillText('m³/h',228,155);
 x.fillStyle='#1E1E1E';x.font='700 18px Kalam';x.fillText('caudalímetro',228,98);
 // gráfica
 x.strokeStyle='#1E1E1E';x.lineWidth=3;x.beginPath();x.moveTo(GX,GY-10);x.lineTo(GX,GY+GH);x.lineTo(GX+GW+10,GY+GH);x.stroke();
 x.font='600 16px Inter';x.fillStyle='#555';x.textAlign='center';
 [0,30,60,90].forEach(q=>x.fillText(q,px(q),GY+GH+20));x.textAlign='right';[0,20,40,60].forEach(h=>x.fillText(h,GX-8,py(h)+6));
 x.fillStyle='#1E1E1E';x.font='700 19px Kalam';x.textAlign='center';x.fillText('Q (m³/h)',GX+GW/2,GY+GH+42);
 x.textAlign='left';x.fillText('H (m)',GX+10,GY-14);
 // curva bomba
 x.lineWidth=5;x.strokeStyle='#FF6B2C';x.beginPath();for(let q=0;q<=QM;q+=1){const h=50-0.005*q*q;q?x.lineTo(px(q),py(h)):x.moveTo(px(q),py(h));}x.stroke();
 x.fillStyle='#FF6B2C';x.textAlign='left';x.font='700 20px Kalam';x.textAlign='right';x.fillText('bomba',px(90),py(3));x.textAlign='left';
 // curva sistema
 x.strokeStyle='#2F6DB5';let qe=0,he=10;x.beginPath();for(let q=0;q<=QM;q+=1){const h=10+r*q*q;if(h>HM)break;qe=q;he=h;q?x.lineTo(px(q),py(h)):x.moveTo(px(q),py(h));}x.stroke();
 x.fillStyle='#2F6DB5';x.textAlign=qe>80?'right':'left';x.fillText('sistema',px(qe)+(qe>80?-4:8),py(he)+(qe>80?-12:16));x.textAlign='left';
 // pérdida en la válvula (diferencia)
 if(loss>0.5){const h0=10+0.004*Q*Q;x.strokeStyle='#C0392B';x.lineWidth=3;x.setLineDash([6,5]);x.beginPath();x.moveTo(px(Q),py(H));x.lineTo(px(Q),py(h0));x.stroke();x.setLineDash([]);
  x.strokeStyle='rgba(47,109,181,.35)';x.beginPath();for(let q=0;q<=QM;q+=1){const h=10+0.004*q*q;q?x.lineTo(px(q),py(h)):x.moveTo(px(q),py(h));}x.stroke();}
 // punto
 const pu=1+0.15*Math.sin(t*6);x.beginPath();x.arc(px(Q),py(H),13*pu,0,7);x.fillStyle='rgba(255,225,77,.8)';x.fill();
 x.beginPath();x.arc(px(Q),py(H),7,0,7);x.fillStyle='#1E1E1E';x.fill();
 const lx=Math.min(px(Q)+14,GX+GW-150);x.textAlign='left';const lab=fmt(Q,1)+' m³/h · '+fmt(H,1)+' m';x.font='700 18px Inter';const w=x.measureText(lab).width;const bx=Math.min(px(Q)-w/2,GX+GW-w);rr(bx-8,py(H)-48,w+16,30,6,'#FFFDF7',1);x.fillStyle='#1E1E1E';x.fillText(lab,bx,py(H)-27);
 if(loss>0.5){x.fillStyle='#C0392B';x.font='700 18px Kalam';x.fillText('se quema: '+fmt(loss,1)+' m',px(Q)+6,py(10+0.004*Q*Q)+26);}
 [0.004,0.010,0.025].forEach((v,k)=>document.getElementById('r'+k).className=Math.abs(r-v)<0.0015?'on':'');
};</script>'''
async def main(static=None):
    open("/home/claude/bitacora/ficha4.html","w").write(BASE.replace("BODY",body).replace("height:1350px","height:1440px").replace("</body>",JS+"</body>"))
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1440})
        await pg.goto("file:///home/claude/bitacora/ficha4.html"); await pg.wait_for_timeout(800)
        if static is not None:
            for f in range(0,int(float(static)*FPS)+1): await pg.evaluate(f"draw({f/FPS})")
            await pg.screenshot(path=f"/home/claude/bitacora/frame_{static}.jpg",type="jpeg",quality=90); await b.close(); return
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","/home/claude/bitacora/v.mp4"],stdin=subprocess.PIPE)
        for f in range(int(D*FPS)):
            await pg.evaluate(f"draw({f/FPS})"); ff.stdin.write(await pg.screenshot(type="jpeg",quality=92))
        await b.close(); ff.stdin.close(); ff.wait()
    SR=music.SR; s=np.zeros(int(D*SR))
    for k in range(3):
        cl=music.clank(); i=int((k*4.2+3.4)*SR); s[i:i+len(cl)]+=cl[:len(s)-i]
    music.write("/home/claude/bitacora/m.wav",music.mix(D,"corporate",sfx=s))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/bitacora/v.mp4","-i","/home/claude/bitacora/m.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","/home/claude/bitacora/video_linkedin.mp4"],check=True)
asyncio.run(main(static=sys.argv[1] if len(sys.argv)>1 else None))
