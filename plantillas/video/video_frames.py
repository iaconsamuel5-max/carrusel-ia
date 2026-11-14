from assets import *
from playwright.sync_api import sync_playwright
A="#FF8A3D"; S="#C9CED6"; T="#F4F1EA"
css=f'''*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;font-family:Inter,sans-serif;color:{T};padding:180px 96px 420px;display:flex;flex-direction:column;position:relative;overflow:hidden;
background:radial-gradient(circle at 85% 8%,#2E343B 0%,transparent 50%),radial-gradient(circle at 0% 100%,#2E343B 0%,transparent 45%),#15181C}}
body:before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,138,61,.07) 2px,transparent 2px);background-size:40px 40px}}
body>*{{position:relative;z-index:1}}
.chip{{align-self:flex-start;border:3px solid {A};color:{A};font-weight:700;font-size:36px;letter-spacing:5px;padding:14px 32px;border-radius:999px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:48px}}
h1{{font-weight:800;font-size:110px;line-height:1.05;letter-spacing:-2px}}
h2{{font-weight:700;font-size:84px;line-height:1.08}}
.acc{{color:{A}}} .sub{{font-size:52px;line-height:1.35;color:{S}}}
.num{{font-size:46px;font-weight:700;letter-spacing:4px;color:{S}}}
.card{{background:#23282E;border-radius:32px;padding:56px 60px;font-size:54px;line-height:1.3}}
.foot{{display:flex;justify-content:space-between;font-size:36px;color:{S};border-top:2px solid #23282E;padding-top:36px}} .foot b{{color:{A}}}'''
def big(ic): return ic.replace('width="64" height="64"','width="220" height="220"')
foot='<div class="foot"><span>Samuel Sánchez · Datos &amp; IA</span><b>#IAconSamuel</b></div>'
scenes=[
 f'<div class="chip">MECÁNICA</div><div class="main"><svg width="420" height="420" viewBox="0 0 420 420">{bearing(210,210,190,T,10)}</svg><h1>Tu máquina te avisa <span class="acc">antes de fallar.</span></h1><div class="sub">¿La estás escuchando?</div></div>{foot}',
 f'<div class="chip">MECÁNICA</div><div class="main"><div class="num">SEÑAL 1 DE 3</div>{big(ic_sound(A))}<h2 class="acc">Ruido</h2><div class="card">Zumbido, chirrido o golpeteo que antes no estaba.</div></div>{foot}',
 f'<div class="chip">MECÁNICA</div><div class="main"><div class="num">SEÑAL 2 DE 3</div>{big(ic_vib(A))}<h2 class="acc">Vibración</h2><div class="card">Aumenta poco a poco y se siente en la carcasa.</div></div>{foot}',
 f'<div class="chip">MECÁNICA</div><div class="main"><div class="num">SEÑAL 3 DE 3</div>{big(ic_temp(A))}<h2 class="acc">Temperatura</h2><div class="card">El alojamiento se calienta más de lo normal.</div></div>{foot}',
 f'<div class="chip">TOQUE IA</div><div class="main"><h1>Sensores + IA lo detectan <span class="acc">antes</span> que el oído humano.</h1><div class="card">Eso se llama <b class="acc">mantenimiento predictivo</b>: reparar antes de que se dañe.</div></div>{foot}',
 f'<div class="chip">IA CON SAMUEL</div><div class="main"><svg width="360" height="400" viewBox="0 0 360 400">{wrench(170,190,2.1,A,10,35)}</svg><h1>¿Te sirvió? <span class="acc">Guárdalo</span> y compártelo.</h1><div class="sub">Sígueme para más IA aplicada a la industria.<br><b style="color:#F4F1EA">@samuelsanchez1407</b></div></div>{foot}',
]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_page(viewport={"width":1080,"height":1920})
    for i,s in enumerate(scenes,1):
        pg.set_content(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{s}</body></html>'); pg.wait_for_timeout(250)
        pg.screenshot(path=f"video/bg{i}.png")
    # transparent gears
    for name,svg,w in [("gbig",gear(400,400,390,330,20,120,A,10,op=.12),800),("gsmall",gear(150,150,140,118,12,44,S,8,op=.35),300)]:
        pg.set_viewport_size({"width":w,"height":w})
        pg.set_content(f'<html><body style="margin:0;background:transparent"><svg width="{w}" height="{w}">{svg}</svg></body></html>')
        pg.screenshot(path=f"video/{name}.png",omit_background=True)
    b.close()
