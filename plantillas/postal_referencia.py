from playwright.sync_api import sync_playwright
from PIL import Image
t=dict(bg1="#0E2F3A",bg2="#1E6B73",card="#144652",acc="#FF9E7A",txt="#F3FBFB",sub="#C3DFE0",dots="rgba(255,158,122,.09)")
html="""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Inter,sans-serif;color:{txt};padding:96px 88px;display:flex;flex-direction:column;position:relative;overflow:hidden;
background:radial-gradient(circle at 85% 10%,{bg2} 0%,transparent 55%),radial-gradient(circle at 0% 100%,{bg2} 0%,transparent 45%),{bg1}}
body:before{content:"";position:absolute;inset:0;background-image:radial-gradient({dots} 2px,transparent 2px);background-size:36px 36px}
.frame{position:absolute;inset:36px;border:3px dashed rgba(255,158,122,.45);border-radius:28px}
body>*{position:relative;z-index:1}
.chip{align-self:flex-start;border:2px solid {acc};color:{acc};font-weight:700;font-size:28px;letter-spacing:4px;padding:12px 26px;border-radius:999px}
.stamp{position:absolute;top:80px;right:80px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px}
.pre{font-size:34px;color:{sub};font-weight:500;letter-spacing:1px}
h1{font-weight:700;font-size:80px;line-height:1.06;letter-spacing:-1.5px}
.acc{color:{acc}}
.card{background:{card};border-radius:24px;padding:40px 48px;display:flex;flex-direction:column;gap:26px}
.row{display:flex;gap:28px;align-items:baseline}
.k{min-width:220px;white-space:nowrap;font-weight:800;font-size:44px;color:{acc}}
.v{font-size:34px;line-height:1.3}
.ia{font-size:34px;line-height:1.4;color:{sub}}
.ia b{color:{acc}}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:{sub};border-top:2px solid {card};padding-top:32px}
.foot b{color:{acc}}
</style></head><body><div class="frame"></div>
<svg class="stamp" width="150" height="180" viewBox="0 0 150 180"><rect x="6" y="6" width="138" height="168" rx="6" fill="none" stroke="#FF9E7A" stroke-width="4" stroke-dasharray="8 6"/><rect x="20" y="20" width="110" height="110" rx="4" fill="rgba(255,158,122,.15)"/>
<path d="M40 118 C48 70 60 46 75 42 C92 46 102 72 110 118 Z" fill="none" stroke="#FF9E7A" stroke-width="4" stroke-linejoin="round"/>
<path d="M70 118 l8-10 -8-10 8-10 -8-10 8-10 -6-8" fill="none" stroke="#F3FBFB" stroke-width="3" stroke-linejoin="round"/>
<path d="M24 124c10-5 20 5 30 0s20 5 30 0 20 5 30 0 10 3 12 2" fill="none" stroke="#9EE6E8" stroke-width="3"/>
<text x="75" y="158" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" fill="#FF9E7A">COLOMBIA</text></svg>
<div class="chip">POSTAL · ANTIOQUIA</div>
<div class="main">
<div class="pre">Saludos desde</div>
<h1>La Piedra del Peñol, <span class="acc">Guatapé</span></h1>
<div class="card">
<div class="row"><div class="k">220 m</div><div class="v">de altura: como un edificio de unos 60 pisos.</div></div>
<div class="row"><div class="k">1954</div><div class="v">año en que alguien llegó por primera vez a la cima.</div></div>
<div class="row"><div class="k">Años 70</div><div class="v">se crea el embalse que la rodea, para generar energía.</div></div>
</div>
<div class="ia"><b>Toque IA:</b> hoy los embalses hidroeléctricos se vigilan con sensores y modelos de datos que anticipan su nivel.</div>
</div>
<div class="foot"><span>Samuel Sánchez · Datos &amp; IA</span><b>#IAconSamuel</b></div></body></html>"""
for k,v in t.items(): html=html.replace("{"+k+"}",v)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path="postal.png"); b.close()
Image.open("postal.png").convert("RGB").save("postal_muestra.jpg",quality=92)
