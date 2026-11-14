from playwright.sync_api import sync_playwright
from PIL import Image
themes = {
 "humor":      dict(bg1="#1E1240", bg2="#3A1C6E", card="#2C1B57", acc="#7CF0C8", txt="#F7F3FF", sub="#CFC4EE", dots="rgba(124,240,200,.10)"),
 "motivacion": dict(bg1="#0E1726", bg2="#16304A", card="#17233A", acc="#F2B544", txt="#F4F1EA", sub="#C5CEDA", dots="rgba(242,181,68,.08)"),
 "pareja":     dict(bg1="#3A0E24", bg2="#6E1F3F", card="#4E1430", acc="#FF8FA8", txt="#FFF1F4", sub="#F5C9D4", dots="rgba(255,143,168,.10)"),
}
base = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Inter,sans-serif;color:{txt};padding:96px 88px;display:flex;flex-direction:column;position:relative;overflow:hidden;
background:radial-gradient(circle at 85% 10%, {bg2} 0%, transparent 55%), radial-gradient(circle at 0% 100%, {bg2} 0%, transparent 45%), {bg1}}
body:before{content:"";position:absolute;inset:0;background-image:radial-gradient({dots} 2px, transparent 2px);background-size:36px 36px;z-index:0}
body>*{position:relative;z-index:1}
.chip{align-self:flex-start;border:2px solid {acc};color:{acc};font-weight:700;font-size:28px;letter-spacing:4px;padding:12px 26px;border-radius:999px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px}
h1{font-weight:700;font-size:84px;line-height:1.08;letter-spacing:-1.5px}
.acc{color:{acc}}
.card{background:{card};border-radius:24px;padding:48px 52px;font-size:46px;line-height:1.3;font-weight:600}
.sub{font-size:36px;line-height:1.45;color:{sub}}
.lbl{font-size:28px;font-weight:700;letter-spacing:3px;color:{sub};margin-bottom:14px}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:{sub};border-top:2px solid {card};padding-top:32px}
.foot b{color:{acc}}
</style></head><body>BODY
<div class="foot"><span>Samuel Sánchez · Datos &amp; IA</span><b>#IAconSamuel</b></div></body></html>"""

tabs=''.join(f'<path d="M{8+i*26} 30l5-14h16l5 14"/>' for i in range(8))
humor = f"""<div class="chip">HUMOR</div><div class="main">
<svg width="230" height="130" viewBox="0 0 230 130" fill="none" stroke="#7CF0C8" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"><rect x="4" y="30" width="200" height="96" rx="10"/>{tabs}<path d="M4 48h200"/><circle cx="196" cy="22" r="20" fill="#7CF0C8" stroke="none"/><text x="196" y="30" text-anchor="middle" font-family="Inter" font-weight="700" font-size="22" fill="#1E1240" stroke="none">47</text></svg>
<div><div class="lbl">YO</div><div class="card">IA, por favor, organízame la vida.</div></div>
<div><div class="lbl" style="color:#7CF0C8">LA IA</div><div class="card" style="border:2px solid #7CF0C8">Con gusto. Primero cierra las <span class="acc">47 pestañas</span> que tienes abiertas.</div></div>
<div class="sub">Etiqueta a alguien que necesita leer esto.</div></div>"""

motiv = """<div class="chip">MOTIVACIÓN</div><div class="main">
<svg width="120" height="120" viewBox="0 0 120 120" fill="none" stroke="#F2B544" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 95l30-30 20 20 35-45"/><path d="M80 40h25v25"/></svg>
<h1>La IA no te va a reemplazar.</h1>
<h1 class="acc">Alguien que sepa usarla, tal vez sí.</h1>
<div class="card" style="font-size:38px;font-weight:500">Empieza hoy: <b>15 minutos al día</b> aprendiendo una herramienta nueva. En un año serás otra persona.</div>
</div>"""

pareja = """<div class="chip">PAREJA</div><div class="main">
<svg width="170" height="150" viewBox="0 0 170 150" fill="none" stroke="#FF8FA8" stroke-width="5" stroke-linejoin="round"><path d="M85 140C30 104 6 74 6 46 6 22 24 6 46 6c17 0 30 10 39 24 9-14 22-24 39-24 22 0 40 16 40 40 0 28-24 58-79 94z" fill="rgba(255,143,168,.12)"/><text x="85" y="78" text-anchor="middle" font-family="Inter" font-weight="800" font-size="40" fill="#FF8FA8" stroke="none">404</text></svg>
<h1>Le pedí a la IA que describiera a mi pareja.</h1>
<div class="card">Respuesta: <span class="acc">"Error 404: no encuentro palabras suficientes."</span></div>
<div class="sub">Y eso que leyó todo internet. Hay cosas que ningún algoritmo logra explicar.</div>
</div>"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width":1080,"height":1350})
    for name, body in [("humor",humor),("motivacion",motiv),("pareja",pareja)]:
        html = base.replace("BODY", body)
        for k,v in themes[name].items(): html = html.replace("{"+k+"}", v)
        pg.set_content(html); pg.wait_for_timeout(300)
        pg.screenshot(path=f"{name}.png")
        Image.open(f"{name}.png").convert("RGB").save(f"{name}.jpg", quality=92)
    b.close()
