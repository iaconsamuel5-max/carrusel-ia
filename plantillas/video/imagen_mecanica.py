from assets import *
from playwright.sync_api import sync_playwright
from PIL import Image
A="#FF8A3D"; S="#C9CED6"
illus=f'''<svg width="904" height="270" viewBox="0 0 904 300">
{gear(150,150,130,108,14,40,A,6)}
{bearing(420,150,110,"#F4F1EA",6)}
{wrench(680,150,1.9,A,6,35)}
{gear(820,70,52,42,10,16,S,4,op=.7)}
</svg>'''
bg=f'''<svg style="position:absolute;inset:0;z-index:0" width="1080" height="1350">{gear(1040,1300,220,185,18,70,A,4,op=.07)}{gear(30,760,150,125,14,45,A,4,op=.06)}{gear(1000,560,90,75,10,28,S,3,op=.06)}</svg>'''
row=lambda ic,k,v:f'<div class="row">{ic}<div><div class="k">{k}</div><div class="v">{v}</div></div></div>'
html=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:Inter,sans-serif;color:#F4F1EA;padding:96px 88px;display:flex;flex-direction:column;position:relative;overflow:hidden;
background:radial-gradient(circle at 85% 10%,#2E343B 0%,transparent 55%),radial-gradient(circle at 0% 100%,#2E343B 0%,transparent 45%),#15181C}}
body:before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,138,61,.07) 2px,transparent 2px);background-size:36px 36px}}
body>*{{position:relative;z-index:1}}
.chip{{align-self:flex-start;border:2px solid {A};color:{A};font-weight:700;font-size:28px;letter-spacing:4px;padding:12px 26px;border-radius:999px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:26px}}
h1{{font-weight:700;font-size:66px;line-height:1.08;letter-spacing:-1.2px}}
.acc{{color:{A}}}
.card{{background:#23282E;border-radius:24px;padding:34px 44px;display:flex;flex-direction:column;gap:24px}}
.row{{display:flex;gap:26px;align-items:center}}
.k{{font-weight:700;font-size:36px;color:{A}}}
.v{{font-size:31px;line-height:1.3;color:#F4F1EA}}
.ia{{font-size:32px;line-height:1.4;color:{S}}} .ia b{{color:{A}}}
.foot{{display:flex;justify-content:space-between;font-size:28px;color:{S};border-top:2px solid #23282E;padding-top:30px}} .foot b{{color:{A}}}
</style></head><body>{bg}
<div class="chip">MECÁNICA</div><div class="main">{illus}
<h1>3 señales de que un <span class="acc">rodamiento</span> va a fallar</h1>
<div class="card">
{row(ic_sound(A),"Ruido","Zumbido, chirrido o golpeteo que antes no estaba.")}
{row(ic_vib(A),"Vibración","Aumenta poco a poco y se siente en la carcasa.")}
{row(ic_temp(A),"Temperatura","El alojamiento se calienta más de lo normal.")}
</div>
<div class="ia"><b>Toque IA:</b> sensores + IA detectan estos cambios antes de que el oído los note. Eso es mantenimiento predictivo.</div>
</div><div class="foot"><span>Samuel Sánchez · Datos &amp; IA</span><b>#IAconSamuel</b></div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path="mecanica.png"); b.close()
Image.open("mecanica.png").convert("RGB").save("mecanica_muestra.jpg",quality=92)
