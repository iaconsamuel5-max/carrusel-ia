import asyncio, sys, os
sys.path.insert(0, "/home/claude/carrusel-ia/plantillas/bitacora")
import gen
from playwright.async_api import async_playwright

ACC = "#0E6E78"   # verde petróleo industrial
HL = "#FFC20E"    # amarillo seguridad
BASE = gen.BASE.replace("#FF6B2C", ACC).replace("#FFE14D", HL)
BASE = BASE.replace("</style>", """
.hazard{position:absolute;left:0;right:0;top:0;height:22px;background:repeating-linear-gradient(-45deg,#1E1E1E 0 22px,#FFC20E 22px 44px)}
.big{font-family:Marker;font-size:150px;line-height:1;color:#1E1E1E}
.stat{display:flex;align-items:center;gap:26px;margin-top:26px;border:4px solid #0E6E78;border-radius:16px;background:#FFFDF7;padding:18px 26px}
.stat .v{white-space:nowrap;font-family:Marker;font-size:70px;min-width:250px;text-align:center;background:#FFC20E;border-radius:12px;padding:4px 10px}
.stat p{font-family:Kalam;font-size:33px;line-height:1.25}
.src{font-family:Inter;font-weight:500;font-size:20px;color:#555;margin-top:20px}
.bar{display:flex;align-items:center;gap:18px;margin-top:20px;font-family:Kalam;font-size:32px}
.bar .b{height:46px;background:#0E6E78;border-radius:8px;border:3px solid #1E1E1E}
.bar .p{font-family:Marker;font-size:40px;width:110px}
</style>""")
SH = gen.SPARK.replace("#FF6B2C", ACC)
AR = gen.ARROW.replace("#FF6B2C", ACC)
foot = lambda r="Desliza →": gen.foot(r).replace("#FF6B2C", ACC)
m = gen.mascot
T = 6
S = []
S.append(f'''<div class="num">1/{T}</div><span class="tag">BITÁCORA DEL INGENIERO · MANTENIMIENTO</span>
<h1 style="font-size:104px;margin-top:40px">La IA ya llegó<br>al mantenimiento.<br><span class="hl">Lo que falta</span><br><span class="u">es la gente.</span></h1>
<div style="font-family:Kalam;font-weight:700;font-size:38px;margin-top:34px;max-width:560px">Lo que dice una encuesta a 600 líderes de mantenimiento y lo que aprendí en 18 años en planta.</div>
{AR.format(st="left:420px;top:900px;transform:rotate(15deg)")}
{SH.format(st="left:40px;top:1000px")}
<div style="position:absolute;left:570px;top:740px">{m("point",330)}</div>
{foot()}''')
S.append(f'''<div class="num">2/{T}</div><span class="tag">LOS DATOS</span>
<h1 style="font-size:88px"><span class="hl">En un año</span> cambió<br>el mantenimiento</h1>
<div class="stat"><span class="v">9→18 %</span><p>de las empresas ya hace <b>mantenimiento predictivo</b>. Se duplicó.</p></div>
<div class="stat"><span class="v">36 %</span><p>sigue siendo <b>reactivo</b>: "se dañó, lo arreglamos". No se movió.</p></div>
<div class="stat"><span class="v">72 %</span><p>destina entre el <b>16 y el 30 %</b> del presupuesto de mantenimiento a nuevas tecnologías.</p></div>
<div class="src">Fuente: Encuesta Fluke / Censuswide, mayo 2026. 600+ encuestados en EE. UU., Reino Unido y Alemania.</div>
{foot()}''')
bars = [(23,"Falta de experiencia"),(19,"Brecha de personal calificado"),(18,"Falta de conocimiento"),(17,"Escasez de habilidades")]
bh = "".join(f'<div class="bar"><span class="p">{v} %</span><div class="b" style="width:{v*14}px"></div><span>{t}</span></div>' for v,t in bars)
S.append(f'''<div class="num">3/{T}</div><span class="tag">EL VERDADERO OBSTÁCULO</span>
<h1 style="font-size:90px">No es la plata.<br><span class="hl">Son las habilidades.</span></h1>
<div style="display:flex;align-items:center;gap:30px;margin-top:30px"><span class="big">≈78 %</span><p style="font-family:Kalam;font-size:36px;line-height:1.25;max-width:420px">de los obstáculos reportados tienen que ver con <b>habilidades</b>.</p></div>
{bh}
<div class="src">Fuente: Encuesta Fluke / Censuswide, mayo 2026.</div>
<div style="position:absolute;right:-30px;bottom:40px">{m("think",210)}</div>
{foot()}''')
S.append(f'''<div class="num">4/{T}</div><span class="tag">LO QUE APRENDÍ EN PLANTA</span>
<h1 style="font-size:84px">Una alarma que nadie<br><span class="hl">sabe interpretar</span><br>es solo ruido</h1>
<div class="card"><b class="n">1</b><p>El sensor mide. <b>El técnico entiende</b> por qué vibra, por qué se descalibró, por qué se congela.</p></div>
<div class="card"><b class="n">2</b><p>La IA aprende de tus datos. Si las órdenes de trabajo dicen "se arregló", <b>no aprende nada</b>.</p></div>
<div class="card"><b class="n">3</b><p>Una herramienta sin criterio técnico termina <b>apagada en un rincón</b>.</p></div>
<div style="position:absolute;right:190px;bottom:20px">{m("tablet",180)}</div>
{foot()}''')
S.append(f'''<div class="num">5/{T}</div><span class="tag">POR DÓNDE EMPEZAR</span>
<h1 style="font-size:88px"><span class="hl">4 pasos</span> sin gastar<br>una fortuna</h1>
<div class="card"><b class="n">1</b><p><b>Ordena la bitácora:</b> falla, causa, acción y tiempo en cada orden de trabajo.</p></div>
<div class="card"><b class="n">2</b><p><b>Mide lo básico:</b> MTBF, MTTR y disponibilidad en un tablero de Power BI.</p></div>
<div class="card"><b class="n">3</b><p><b>Forma a tu gente:</b> el técnico que entiende sus datos usa mejor la IA.</p></div>
<div class="card"><b class="n">4</b><p><b>Piloto pequeño:</b> 1 equipo crítico, 1 variable, 90 días. Luego escalas.</p></div>
{foot()}''')
S.append(f'''<div class="num">6/{T}</div><span class="tag">PARA CONVERSAR</span>
<h1 style="font-size:96px">¿Qué frena más<br>en tu planta: <span class="hl">la tecnología</span><br>o <span class="u">la formación</span>?</h1>
<div style="font-family:Kalam;font-weight:700;font-size:42px;margin-top:40px;line-height:1.55">
✔ Déjame tu respuesta en comentarios<br>
✔ Compártelo con tu jefe de mantenimiento<br>
✔ Sigue la página <span style="color:{ACC}">IA con Samuel</span></div>
{SH.format(st="left:40px;top:1020px")}
<div style="position:absolute;right:20px;bottom:70px">{m("thumbs",290)}</div>
{foot("IA con Samuel")}''')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i, body in enumerate(S, 1):
            open(f"s{i}.html","w").write(BASE.replace("BODY", '<div class="hazard" style="left:-130px;right:-70px;top:-70px"></div>' + body))
            await pg.goto(f"file://{os.getcwd()}/s{i}.html")
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f"p{i}.jpg", type="jpeg", quality=90)
        await b.close()
asyncio.run(main())
