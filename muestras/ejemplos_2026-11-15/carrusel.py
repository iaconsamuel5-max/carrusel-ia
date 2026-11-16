from playwright.sync_api import sync_playwright
from PIL import Image
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1350px;background:#0E1726;color:#F4F1EA;font-family:Inter,sans-serif;padding:96px 88px;display:flex;flex-direction:column;position:relative;overflow:hidden}
.bg{position:absolute;inset:0;z-index:0;opacity:.07}body>*{position:relative;z-index:1}
.top{display:flex;justify-content:space-between;font-size:26px;color:#A9B4C2;font-weight:600}.top b{color:#F2B544}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px}
h1{font-size:96px;line-height:1.02;font-weight:800;letter-spacing:-2px}h2{font-size:72px;line-height:1.05;font-weight:800;letter-spacing:-1px}
.a{color:#F2B544}.s{font-size:36px;line-height:1.4;color:#C5CEDA}
.card{background:#17233A;border-radius:24px;padding:40px 48px;font-size:36px;line-height:1.4}
.f{font-size:52px;font-weight:800;text-align:center;line-height:1.3}.f small{display:block;font-size:30px;font-weight:500;color:#A9B4C2;margin-top:10px}
.tag{align-self:flex-start;background:#F2B544;color:#0E1726;font-weight:800;font-size:26px;padding:8px 18px;border-radius:999px;letter-spacing:1px}
.row{display:flex;gap:26px;align-items:flex-start;font-size:34px;line-height:1.35}.row svg{flex:none;margin-top:4px}
.ej{font-size:24px;color:#A9B4C2;font-style:italic}
.p{background:#0B1220;border:2px dashed #F2B544;border-radius:20px;padding:30px 36px;font-size:32px;line-height:1.45;font-family:Inter}
.foot{display:flex;justify-content:space-between;font-size:26px;color:#A9B4C2;border-top:2px solid #17233A;padding-top:26px}.foot b{color:#F2B544}"""
def ico(d,s=56): return f'<svg width="{s}" height="{s}" viewBox="0 0 64 64" fill="none" stroke="#F2B544" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
FRIDGE='<rect x="14" y="4" width="36" height="56" rx="5"/><path d="M14 24h36M20 12v6M20 30v10"/>'
GEAR='<circle cx="32" cy="32" r="9"/><path d="M32 6v8M32 50v8M6 32h8M50 32h8M13 13l6 6M45 45l6 6M13 51l6-6M45 19l6-6"/>'
CLOCK='<circle cx="32" cy="32" r="24"/><path d="M32 18v15l10 6"/>'
WRENCH='<path d="M40 8a14 14 0 0 0-14 18L8 44l12 12 18-18A14 14 0 0 0 56 24l-9 9-8-2-2-8z"/>'
NOTE='<rect x="12" y="6" width="40" height="52" rx="4"/><path d="M20 20h24M20 30h24M20 40h14"/>'
CHIP='<rect x="16" y="16" width="32" height="32" rx="4"/><path d="M24 8v8M32 8v8M40 8v8M24 48v8M32 48v8M40 48v8M8 24h8M8 32h8M8 40h8M48 24h8M48 32h8M48 40h8"/>'
big=lambda d:f'<svg width="300" height="300" viewBox="0 0 64 64" fill="none" stroke="#F2B544" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
bg=lambda d:f'<svg class="bg" width="1080" height="1350" viewBox="0 0 1080 1350"><g transform="translate(700,850) scale(9)" fill="none" stroke="#F2B544" stroke-width="1.5">{d}</g></svg>'
def slide(n,body,b=GEAR): return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{bg(b)}<div class="top"><span>Samuel Sánchez · Datos &amp; IA</span><b>{n:02d} / 08</b></div><div class="main">{body}</div><div class="foot"><span>Guárdalo para tu negocio</span><b>#IAconSamuel</b></div></body></html>'
S=[
 slide(1,f'{big(FRIDGE)}<h1>¿Cada cuánto se te <span class="a">daña la nevera?</span></h1><div class="s">Hay una fórmula que usan las grandes plantas… y tu tienda también la puede usar.</div>',FRIDGE),
 slide(2,f'<div class="tag">MTBF</div><h2>Tiempo promedio <span class="a">entre fallas</span></h2><div class="card f">MTBF = Tiempo funcionando ÷ Número de fallas<small>Mientras más alto, más confiable es el equipo.</small></div>',CLOCK),
 slide(3,f'<div class="tag">TU TIENDA</div><h2>La nevera de <span class="a">gaseosas</span></h2><div class="card"><div class="row">{ico(CLOCK)}<span>Funcionó 6 meses ≈ <b class="a">4.380 horas</b></span></div><br><div class="row">{ico(WRENCH)}<span>Se dañó <b class="a">3 veces</b></span></div><br><div class="row">{ico(FRIDGE)}<span>MTBF ≈ <b class="a">1.460 h</b> → falla más o menos cada <b class="a">2 meses</b></span></div></div><div class="ej">Ejemplo ilustrativo</div>',FRIDGE),
 slide(4,f'<div class="tag">MTTR</div><h2>Tiempo promedio <span class="a">de reparación</span></h2><div class="card f">MTTR = Tiempo total reparando ÷ Número de reparaciones<small>Ejemplo: 3 reparaciones que sumaron 18 h → 6 h cada una</small></div><div class="s">Cada hora con la nevera dañada son productos que se calientan y ventas que se pierden.</div>',WRENCH),
 slide(5,f'<div class="tag">LA PLANTA</div><h2>Misma fórmula, <span class="a">otra escala</span></h2><div class="card"><div class="row">{ico(GEAR)}<span>Una bomba trabaja todo el año: <b class="a">8.760 h</b></span></div><br><div class="row">{ico(WRENCH)}<span>Falla <b class="a">4 veces</b> → MTBF ≈ <b class="a">2.190 h</b></span></div><br><div class="row">{ico(CLOCK)}<span>Cada falla puede parar toda la línea de producción</span></div></div><div class="ej">Ejemplo ilustrativo</div>',GEAR),
 slide(6,f'<h2>Cómo <span class="a">subir</span> tu MTBF</h2><div class="card"><div class="row">{ico(NOTE)}<span>Anota cada falla: fecha, qué pasó y cuánto duró</span></div><br><div class="row">{ico(WRENCH)}<span>Haz mantenimiento preventivo: limpieza, revisión de empaques y conexiones</span></div><br><div class="row">{ico(CLOCK)}<span>Revisa tus números cada mes y compara</span></div></div>',NOTE),
 slide(7,f'<div class="tag">CON IA</div><h2>Deja que la IA <span class="a">haga las cuentas</span></h2><div class="p">"Te paso mi registro de fallas: [pega la lista]. Calcula el MTBF y el MTTR de cada equipo y dime cuál me está costando más y qué debería revisar primero."</div><div class="s">En empresas grandes: sensores + modelos de IA avisan <b class="a">antes</b> de la falla.</div>',CHIP),
 slide(8,f'<h1>¿Te <span class="a">sirvió?</span></h1><div class="card" style="font-size:38px;line-height:1.6">Dale me gusta<br>Guárdalo para tu próximo mantenimiento<br>Envíaselo a ese amigo que tiene negocio</div><div class="s">¿Quieres aplicarlo en tu negocio o empresa? <b class="a">Escríbeme INFO</b> por mensaje directo.</div>',CHIP),
]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1080,"height":1350})
    for i,h in enumerate(S,1):
        pg.set_content(h);pg.wait_for_timeout(200);pg.screenshot(path=f"c{i}.png");Image.open(f"c{i}.png").convert("RGB").save(f"carrusel_{i:02d}.jpg",quality=90)
    b.close()
ims=[Image.open(f"carrusel_{i:02d}.jpg").resize((360,450)) for i in range(1,9)]
m=Image.new("RGB",(1440,900))
for i,im in enumerate(ims): m.paste(im,((i%4)*360,(i//4)*450))
m.save("hoja_carrusel.jpg",quality=88)
