import asyncio, subprocess, sys
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/estilos")
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/bitacora")
from playwright.async_api import async_playwright
from gen import BASE
import music, numpy as np
D, FPS = 13.0, 30
rows="".join(f'<tr id="r{i}"><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for i,(a,b,c,d) in enumerate([
 ("Directo (DOL)","7,0 × In","343 A","2,0 × Tn"),
 ("Estrella (Y)","2,3 × In","114 A","0,67 × Tn"),
 ("Triángulo (Δ) en marcha","1,0 × In","49 A","1,0 × Tn")]))
body=f'''<div class="num" style="font-size:40px">Ficha #5</div><span class="tag">FICHA DE CAMPO · ELÉCTRICA</span>
<h1 style="font-size:50px;margin-top:16px;white-space:nowrap">Arranque <span class="hl">estrella-triángulo</span></h1>
<div style="font-family:Kalam;font-size:29px;margin-top:2px">Arranca con 1/3 de la corriente… y también con 1/3 del par.</div>
<div style="position:relative;margin-top:8px;border:5px solid #FF6B2C;border-radius:14px;background:#FFFDF7;padding:6px">
<canvas id="c" width="866" height="440" style="display:block"></canvas></div>
<div class="card" style="margin-top:10px;padding:10px 22px"><div class="who">PRINCIPIO · en Y cada bobina recibe V ÷ √3</div>
<p style="font-size:32px;font-family:Inter;font-weight:700;line-height:1.3">I<sub>Y</sub> = I<sub>directo</sub> ÷ 3 &nbsp;·&nbsp; T<sub>Y</sub> = T<sub>directo</sub> ÷ 3</p>
<p style="font-size:26px">Motor 30 kW · 440 V · In ≈ 49 A · directo ≈ 7 × In = 343 A<br>En Y: 440 ÷ √3 = 254 V por bobina → 343 ÷ 3 = <b style="background:#FFE14D;padding:0 8px">114 A</b></p></div>
<table style="width:100%;border-collapse:collapse;margin-top:10px;font-family:Kalam;font-size:26px;text-align:center;background:#FFFDF7">
<tr style="background:#1E1E1E;color:#FFE14D;font-family:Marker;font-size:24px"><td>Conexión</td><td>Corriente</td><td>Ejemplo</td><td>Par de arranque</td></tr>{rows}</table>
<style>table td{{border:3px solid #FF6B2C;padding:0}} tr.on td{{background:#FFE14D;font-weight:700}}</style>
<div style="font-family:Kalam;font-size:25px;margin-top:10px;line-height:1.22"><b style="color:#FF6B2C">Lección:</b> el motor debe ser Δ a la tensión de la red (placa 440 V Δ / 760 V Y). Si la carga pide al arrancar casi el par que da la Y (aquí 0,67 × Tn), no acelera y el cambio a Δ trae un pico casi de directo. Ajusta KT para cambiar cerca de la velocidad nominal.</div>
<div class="card" style="margin-top:8px;padding:8px 22px;border-color:#2F6DB5"><div class="who">PROMPT IA (ChatGPT · Copilot · Gemini)</div>
<p style="font-size:23px;line-height:1.25">"Con la placa de mi motor [kW, V, In, Ia/In, Ta/Tn] y el par que pide mi carga al arrancar, dime si sirve estrella-triángulo o necesito arrancador suave o variador."</p></div>
<div style="position:absolute;left:0;right:0;bottom:-36px;display:flex;justify-content:space-between;font-family:Kalam;font-weight:700;font-size:27px"><span>Samuel Sánchez · <span style="color:#FF6B2C">IA con Samuel</span></span><span>Guárdala para el taller 📌</span></div>'''
JS = r'''<script>
const c=document.getElementById('c'),x=c.getContext('2d');
const T0=1.0,TS=6.2,TE=11.6; // cierre KM1+KM2, cambio a delta, fin del barrido
const fmt=(v,d)=>v.toFixed(d).replace('.',',');
function rr(X,Y,W,H,r,f,s){x.beginPath();x.roundRect(X,Y,W,H,r);x.fillStyle=f;x.fill();if(s){x.lineWidth=4;x.strokeStyle='#1E1E1E';x.stroke()}}
function sm(e){e=Math.max(0,Math.min(1,e));return e*e*(3-2*e)}
// modelo didactico de corriente y velocidad (no es una medicion)
function cur(t){ if(t<T0)return 0;
 if(t<TS){const u=(t-T0)/(TS-T0);return 114-56*sm(u*1.15);}            // Y: 114 A -> ~58 A
 const u=t-TS; return 49+ (150-49)*Math.exp(-u/0.35);}                   // pico de transicion y luego In
function spd(t){ if(t<T0)return 0; if(t<TS)return 82*sm((t-T0)/(TS-T0)*1.1);
 return 82+16*sm((t-TS)/1.2);}
function dol(t){ if(t<T0)return 0; const u=t-T0; return u<2.2?343-40*u/2.2:49+254*Math.exp(-(u-2.2)/0.25);}
let ang=0,lastT=0;
const GX=70,GY=222,GW=760,GH=190,IMAX=360,TMAX=TE;
const gx=t=>GX+GW*Math.min(t,TMAX)/TMAX, gy=i=>GY+GH-GH*i/IMAX;
function contactor(X,Y,label,sub,on,col){
 rr(X,Y,120,128,12,on?'#FFF3C4':'#F2F2F2',1);
 x.fillStyle='#1E1E1E';x.font='700 26px Inter';x.textAlign='center';x.fillText(label,X+60,Y+30);
 x.font='700 17px Kalam';x.fillStyle=col;x.fillText(sub,X+60,Y+52);
 for(let k=0;k<3;k++){const cx=X+24+k*36;
  x.strokeStyle='#1E1E1E';x.lineWidth=4;x.beginPath();x.moveTo(cx,Y+62);x.lineTo(cx,Y+78);x.moveTo(cx,Y+104);x.lineTo(cx,Y+120);x.stroke();
  x.strokeStyle=on?'#FF6B2C':'#1E1E1E';x.lineWidth=5;x.beginPath();x.moveTo(cx,Y+104);
  if(on)x.lineTo(cx,Y+78);else x.lineTo(cx-13,Y+82);x.stroke();}
 x.fillStyle=on?'#2E9E4F':'#B9B9B9';x.beginPath();x.arc(X+104,Y+18,7,0,7);x.fill();
}
window.draw=function(t){
 const tt=t%D_; const dt=tt<lastT?0:tt-lastT; lastT=tt;
 const km1=tt>=T0, km2=tt>=T0&&tt<TS, km3=tt>=TS+0.05;
 const s=spd(tt); ang+=dt*s*0.25;
 x.clearRect(0,0,866,440);
 // linea L1 L2 L3
 x.fillStyle='#1E1E1E';x.font='700 22px Inter';x.textAlign='left';x.fillText('L1 L2 L3 · 440 V',14,28);
 contactor(14,44,'KM1','línea',km1,'#1E1E1E');
 contactor(146,44,'KM2','estrella',km2,'#2F6DB5');
 contactor(278,44,'KM3','triángulo',km3,'#C0392B');
 // temporizador
 rr(410,44,118,128,12,'#2B2B2B',1);x.fillStyle='#FFE14D';x.font='700 22px Inter';x.textAlign='center';x.fillText('KT',469,72);
 let rem=tt<T0?5.2:Math.max(0,TS-tt);x.font='700 34px Inter';x.fillText(fmt(rem,1)+' s',469,116);
 x.font='600 16px Inter';x.fillStyle='#ddd';x.fillText(tt<TS?'cambio Y→Δ':'en Δ',469,148);
 // motor con ventilador que gira
 const MX=640,MY=108;
 rr(MX-58,MY-52,150,104,16,'#9FB8D6',1);
 x.save();x.translate(MX+17,MY);x.rotate(ang);x.fillStyle='#1E1E1E';
 for(let k=0;k<4;k++){x.rotate(Math.PI/2);x.beginPath();x.ellipse(0,-20,8,20,0,0,7);x.fill();}
 x.restore();x.beginPath();x.arc(MX+17,MY,7,0,7);x.fillStyle='#FF6B2C';x.fill();
 rr(MX+92,MY-8,40,16,3,'#C9CED6',1);
 // conexion Y o Delta dibujada
 const cx2=816,cy2=118;x.strokeStyle=km3?'#C0392B':'#2F6DB5';x.lineWidth=6;x.beginPath();
 if(!km1){} else if(!km3){x.moveTo(cx2,cy2);x.lineTo(cx2,cy2-34);x.moveTo(cx2,cy2);x.lineTo(cx2-30,cy2+18);x.moveTo(cx2,cy2);x.lineTo(cx2+30,cy2+18);}
 else{x.moveTo(cx2,cy2-34);x.lineTo(cx2-32,cy2+22);x.lineTo(cx2+32,cy2+22);x.closePath();}
 x.stroke();
 x.fillStyle=km3?'#C0392B':'#2F6DB5';x.font='700 22px Kalam';x.textAlign='center';
 x.fillText(!km1?'parado':(km3?'Δ · 440 V':'Y · 254 V'),cx2-18,cy2+56);
 x.fillStyle='#1E1E1E';x.font='700 24px Inter';x.fillText(fmt(s,0)+' % rpm',MX+17,MY+82);
 // grafica corriente
 x.strokeStyle='#1E1E1E';x.lineWidth=3;x.beginPath();x.moveTo(GX,GY-6);x.lineTo(GX,GY+GH);x.lineTo(GX+GW+10,GY+GH);x.stroke();
 x.font='600 17px Inter';x.textAlign='right';x.fillStyle='#555';
 [0,100,200,300].forEach(v=>{x.fillText(v,GX-8,gy(v)+6);x.strokeStyle='#E6E1D6';x.lineWidth=1;x.beginPath();x.moveTo(GX+2,gy(v));x.lineTo(GX+GW,gy(v));x.stroke();});
 x.save();x.translate(18,GY+GH/2);x.rotate(-Math.PI/2);x.textAlign='center';x.fillStyle='#1E1E1E';x.font='700 18px Inter';x.fillText('Corriente (A)',0,0);x.restore();
 x.textAlign='right';x.fillStyle='#1E1E1E';x.font='700 18px Inter';x.fillText('tiempo →',GX+GW,GY+GH+22);
 // In
 x.setLineDash([8,6]);x.strokeStyle='#2E9E4F';x.lineWidth=2;x.beginPath();x.moveTo(GX,gy(49));x.lineTo(GX+GW,gy(49));x.stroke();x.setLineDash([]);
 x.fillStyle='#2E9E4F';x.textAlign='left';x.font='700 18px Kalam';x.fillText('In = 49 A',GX+GW-92,gy(49)-6);
 // curva directo (fantasma)
 x.setLineDash([6,6]);x.strokeStyle='#999';x.lineWidth=3;x.beginPath();
 for(let k=0;k<=Math.min(tt,TMAX)*30;k++){const q=k/30;const X=gx(q),Y=gy(dol(q));k?x.lineTo(X,Y):x.moveTo(X,Y);}x.stroke();x.setLineDash([]);
 if(tt>T0+0.3){x.fillStyle='#777';x.font='700 19px Kalam';x.fillText('directo: 343 A',gx(T0+2.3)+14,gy(300));}
 // curva Y-Delta
 x.lineWidth=5;x.beginPath();let px,py;
 for(let k=0;k<=Math.min(tt,TMAX)*60;k++){const q=k/60;const X=gx(q),Y=gy(cur(q));px=X;py=Y;
  x.strokeStyle=q<TS?'#2F6DB5':'#C0392B';if(k==0)x.moveTo(X,Y);else x.lineTo(X,Y);}
 x.strokeStyle='#FF6B2C';x.stroke();
 if(tt<=TMAX){x.beginPath();x.arc(px,py,9,0,7);x.fillStyle='#FF6B2C';x.fill();}
 if(tt>T0+0.3){x.fillStyle='#2F6DB5';x.font='700 19px Kalam';x.fillText('Y: 114 A',gx(T0)+12,gy(114)-10);}
 if(tt>TS+0.2){x.fillStyle='#C0392B';x.fillText('pico al cambiar a Δ',gx(TS)+14,gy(150)-6);}
 // lectura en vivo
 rr(GX+GW-200,GY+4,196,46,10,'#F2C230',1);x.fillStyle='#1E1E1E';x.font='700 26px Inter';x.textAlign='center';
 x.fillText(fmt(cur(tt),0)+' A',GX+GW-102,GY+37);
 // fila activa
 const row=!km1?-1:(km3?2:1);
 for(let k=0;k<3;k++)document.getElementById('r'+k).className=(k==row)?'on':'';
};
const D_=13.0;
</script>'''
async def main(static=None):
    open("/home/claude/bitacora/ficha_anim.html","w").write(BASE.replace("BODY",body).replace("height:1350px","height:1440px").replace("</body>",JS+"</body>"))
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1440})
        await pg.goto("file:///home/claude/bitacora/ficha_anim.html"); await pg.wait_for_timeout(800)
        if static is not None:
            for f in range(0,int(static*FPS)+1): await pg.evaluate(f"draw({f/FPS})")
            await pg.screenshot(path=f"/home/claude/bitacora/frame_{static}.jpg",type="jpeg",quality=90); await b.close(); return
        ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","/home/claude/bitacora/v.mp4"],stdin=subprocess.PIPE)
        for f in range(int(D*FPS)):
            await pg.evaluate(f"draw({f/FPS})"); ff.stdin.write(await pg.screenshot(type="jpeg",quality=92))
        await b.close(); ff.stdin.close(); ff.wait()
    SR=music.SR; s=np.zeros(int(D*SR))
    for tk in (1.0,6.2):
        cl=music.clank(); i=int(tk*SR); s[i:i+len(cl)]+=cl[:len(s)-i]
    music.write("/home/claude/bitacora/m.wav",music.mix(D,"corporate",sfx=s))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/home/claude/bitacora/v.mp4","-i","/home/claude/bitacora/m.wav","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart","/home/claude/bitacora/video_linkedin.mp4"],check=True)
asyncio.run(main(static=float(sys.argv[1]) if len(sys.argv)>1 else None))
