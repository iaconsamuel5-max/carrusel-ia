import os, asyncio
from playwright.async_api import async_playwright
OUT = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(OUT, exist_ok=True)
A = "#F2B544"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;background:#0E1726;font-family:Inter,sans-serif;color:#F4F1EA;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:96px 88px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-size:28px;color:#C5CEDA;font-weight:600;position:relative;z-index:2}
.top b{color:#F2B544}
.bot{position:absolute;left:88px;right:88px;bottom:80px;border-top:2px solid #1d2b45;padding-top:26px;display:flex;justify-content:space-between;font-size:28px;color:#A9B4C2;z-index:2}
.bot b{color:#F2B544}
.main{position:relative;z-index:2;flex:1;display:flex;flex-direction:column;margin-top:56px}
.tag{align-self:flex-start;background:#F2B544;color:#0E1726;font-weight:800;font-size:28px;letter-spacing:1.5px;padding:10px 22px;border-radius:40px;margin-bottom:26px}
h1{font-weight:700;font-size:84px;line-height:1.04;letter-spacing:-1.5px}
h1 em,h2 em{font-style:normal;color:#F2B544}
h2{font-weight:700;font-size:80px;line-height:1.05;letter-spacing:-1.2px;margin-bottom:34px}
.card{background:#17233A;border-radius:24px;padding:34px 38px}
.p{font-size:31px;line-height:1.38;color:#F4F1EA}
.mut{color:#C5CEDA}
.small{font-size:28px;color:#A9B4C2;line-height:1.35}
.row{display:flex;gap:26px;align-items:flex-start}
.ic{flex:0 0 64px;height:64px}
.bg{position:absolute;z-index:1;opacity:.07}
.prompt{background:#17233A;border-radius:24px;padding:34px 38px;border-left:8px solid #F2B544;font-size:31px;line-height:1.42}
.prompt .q{color:#F2B544;font-weight:700}
.k{color:#F2B544;font-weight:700}
.lbl{font-size:28px;font-weight:800;color:#F2B544;letter-spacing:1.5px;margin-bottom:14px}
"""

def ic(path, size=64, sw=4, col=A):
    return f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'

I = {
 "hand": '<path d="M14 34l10 10 26-26"/><circle cx="32" cy="32" r="28"/>',
 "moon": '<path d="M44 40A20 20 0 0 1 24 12a22 22 0 1 0 28 28 20 20 0 0 1-8 0z"/>',
 "bolt": '<path d="M36 6L14 36h16l-4 22 24-32H34z"/>',
 "chat": '<path d="M8 12h48v30H26l-12 10V42H8z"/><path d="M18 24h28M18 32h18"/>',
 "x": '<circle cx="32" cy="32" r="28"/><path d="M22 22l20 20M42 22L22 42"/>',
 "tag": '<path d="M8 8h24l26 26-24 24L8 32z"/><circle cx="20" cy="20" r="4"/>',
 "lock": '<rect x="12" y="28" width="40" height="28" rx="5"/><path d="M20 28v-8a12 12 0 0 1 24 0v8"/>',
 "list": '<path d="M22 16h34M22 32h34M22 48h34"/><circle cx="10" cy="16" r="3"/><circle cx="10" cy="32" r="3"/><circle cx="10" cy="48" r="3"/>',
 "build": '<path d="M6 58h52M12 58V26l14-8v40M26 58V10l26 12v36"/><path d="M34 30h8M34 40h8"/>',
}

def phone_big():
    return f'''<svg width="500" height="440" viewBox="0 0 560 520" fill="none" stroke-linecap="round" stroke-linejoin="round">
 <rect x="170" y="20" width="220" height="440" rx="34" stroke="{A}" stroke-width="7"/>
 <path d="M250 46h60" stroke="{A}" stroke-width="7"/>
 <rect x="196" y="90" width="130" height="54" rx="18" stroke="#C5CEDA" stroke-width="5"/>
 <path d="M214 112h80M214 126h50" stroke="#C5CEDA" stroke-width="4"/>
 <rect x="236" y="170" width="130" height="70" rx="18" stroke="{A}" stroke-width="5" fill="{A}" fill-opacity=".12"/>
 <path d="M254 192h92M254 208h92M254 224h56" stroke="{A}" stroke-width="4"/>
 <rect x="196" y="266" width="110" height="54" rx="18" stroke="#C5CEDA" stroke-width="5"/>
 <path d="M214 288h70M214 302h40" stroke="#C5CEDA" stroke-width="4"/>
 <rect x="236" y="346" width="130" height="54" rx="18" stroke="{A}" stroke-width="5" fill="{A}" fill-opacity=".12"/>
 <path d="M254 368h92M254 382h60" stroke="{A}" stroke-width="4"/>
 <circle cx="280" cy="430" r="11" stroke="{A}" stroke-width="5"/>
 <path d="M70 120l10 24 24 10-24 10-10 24-10-24-24-10 24-10z" stroke="{A}" stroke-width="5"/>
 <path d="M470 60l7 16 16 7-16 7-7 16-7-16-16-7 16-7z" stroke="#F4F1EA" stroke-width="4"/>
 <path d="M60 330c30-40 70-50 100-40" stroke="#C5CEDA" stroke-width="4" stroke-dasharray="10 12"/>
 <path d="M420 250c50 10 80 50 80 100" stroke="#C5CEDA" stroke-width="4" stroke-dasharray="10 12"/>
 <path d="M440 380h76v52h-48l-14 14v-14h-14z" stroke="#F4F1EA" stroke-width="5"/>
 <path d="M454 400h44M454 414h28" stroke="#F4F1EA" stroke-width="4"/>
 <path d="M36 380h88v56H70l-16 14v-14H36z" stroke="{A}" stroke-width="5"/>
 <path d="M54 402l12 12 26-26" stroke="{A}" stroke-width="5"/>
</svg>'''

def bg(svg, x, y, w):
    return f'<div class="bg" style="left:{x}px;top:{y}px;width:{w}px">{svg}</div>'

EMP = '<svg viewBox="0 0 200 120" width="100%" fill="none" stroke="#F4F1EA" stroke-width="6" stroke-linecap="round"><path d="M10 100Q100-40 190 100Z"/><path d="M30 90l10-10M55 70l12-8M85 55l14-4M115 55l12 6M145 70l12 10"/></svg>'
PH = '<svg viewBox="0 0 120 200" width="100%" fill="none" stroke="#F4F1EA" stroke-width="5"><rect x="10" y="5" width="100" height="190" rx="16"/><path d="M45 20h30"/></svg>'
BUB = '<svg viewBox="0 0 120 100" width="100%" fill="none" stroke="#F4F1EA" stroke-width="5" stroke-linejoin="round"><path d="M5 5h110v65H40L15 95V70H5z"/></svg>'

def page(n, body, extra=""):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s">{extra}
<div class="top"><span>Samuel Sánchez · Datos &amp; IA</span><b>{n:02d} / 08</b></div>
<div class="main">{body}</div>
<div class="bot"><span>Guárdalo para tu negocio</span><b>#IAconSamuel</b></div></div></body></html>'''

S = {}
S[1] = page(1, f'''<div style="display:flex;justify-content:center;margin-top:-10px">{phone_big()}</div>
<div class="tag" style="margin-top:6px">PROMPTS PARA COPIAR</div>
<h1 style="font-size:96px">Que ChatGPT te escriba los <em>WhatsApp</em></h1>
<p class="p mut" style="margin-top:28px;font-size:34px">4 prompts + 3 funciones gratis de WhatsApp Business. En 8 láminas lo aplicas hoy.</p>''')

bubbles = "".join(f'<div style="align-self:{a};background:{bgc};border-radius:22px;padding:16px 26px;font-size:31px;margin-bottom:14px;{c}">{t}</div>'
    for t,a,bgc,c in [("¿A cómo la empanada?","flex-start","#22314d",""),("¿Hacen domicilio?","flex-start","#22314d",""),
                    ("¿Hasta qué hora abren?","flex-start","#22314d",""),("¿Reciben transferencia?","flex-start","#22314d","")])
S[2] = page(2, f'''<div class="tag">EL CASO</div>
<h2>Doña Marta y sus <em>empanadas</em></h2>
<div class="card" style="display:flex;flex-direction:column"><div class="small" style="margin-bottom:18px">Le preguntan lo mismo todo el día:</div>{bubbles}</div>
<div class="row" style="margin-top:34px">{ic(I["bolt"])}<p class="p">La IA le redacta las respuestas <span class="k">una sola vez</span>. WhatsApp Business las guarda y ella las envía con <span class="k">dos toques</span>.</p></div>
<p class="small" style="margin-top:24px;font-style:italic">Ejemplo ilustrativo. Sirve igual para la tienda, la peluquería o el taller.</p>''',
 bg(EMP, 700, 1000, 360))

feat = [("hand","Mensaje de bienvenida","Saluda al cliente nuevo o al que llevaba tiempo sin escribir."),
        ("moon","Mensaje de ausencia","Responde por ti cuando estás cerrado o fuera del horario que elijas."),
        ("bolt","Respuestas rápidas","Guardas un texto con un atajo. En el chat escribes <span class=\"k\">/</span> y lo eliges.")]
S[3] = page(3, '<div class="tag">GRATIS EN LA APP</div><h2 style="font-size:72px;margin-bottom:28px">3 funciones de <em>WhatsApp Business</em></h2>' +
 "".join(f'<div class="card row" style="margin-bottom:18px;padding:28px 36px">{ic(I[k])}<div><div style="font-size:36px;font-weight:700;margin-bottom:8px">{t}</div><div class="p mut">{d}</div></div></div>' for k,t,d in feat) +
 '<p class="small" style="margin-top:8px">Están en la app, en Herramientas para la empresa. La IA escribe el texto; la app lo envía.</p>',
 bg(PH, 900, 1000, 220))

def prompt_slide(n, tag, title, ptxt, after):
    return page(n, f'''<div class="tag">{tag}</div><h2>{title}</h2>
<div class="prompt"><span class="q">“</span>{ptxt}<span class="q">”</span></div>{after}''', bg(BUB, 790, 880, 240))

S[4] = prompt_slide(4, "PROMPT 1", "Bienvenida y <em>ausencia</em>",
 'Tengo un negocio de <span class="k">[EMPANADAS]</span> en <span class="k">[BELLO]</span>. Atiendo de <span class="k">[10 A.M. A 8 P.M.]</span>. Escríbeme un mensaje de bienvenida y uno de ausencia para WhatsApp: máximo 3 líneas cada uno, tono cercano y colombiano, que invite a hacer el pedido.',
 f'<div class="row" style="margin-top:34px">{ic(I["chat"])}<p class="p">Copia, cambia lo que está entre <span class="k">[corchetes]</span> y pégalo en ChatGPT, Gemini, Claude o Copilot.</p></div>')

tbl = "".join(f'<div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:2px solid #22314d;font-size:30px"><span class="k">{a}</span><span class="mut">{b}</span></div>'
  for a,b in [("/precios","lista de precios"),("/domicilio","zonas y valor"),("/horario","días y horas"),("/pago","cómo pagar")])
S[5] = prompt_slide(5, "PROMPT 2", "Tus <em>respuestas rápidas</em>",
 'Estas son las preguntas que más me hacen: <span class="k">[PÉGALAS]</span>. Mis datos: <span class="k">[PRECIOS, DOMICILIO, PAGOS]</span>. Escribe una respuesta corta para cada una y sugiere un atajo de una palabra.',
 f'<div class="card" style="margin-top:28px;padding:22px 38px">{tbl}</div>')

S[6] = page(6, f'''<div class="tag">PROMPTS 3 Y 4</div><h2>Catálogo y <em>volver a vender</em></h2>
<div class="lbl">PROMPT 3 · CATÁLOGO</div>
<div class="prompt" style="margin-bottom:30px"><span class="q">“</span>Describe estos productos para mi catálogo de WhatsApp, máximo 2 líneas cada uno, destacando sabor y tamaño: <span class="k">[LISTA CON PRECIOS]</span>.<span class="q">”</span></div>
<div class="lbl">PROMPT 4 · NOVEDAD DEL DÍA</div>
<div class="prompt"><span class="q">“</span>Escribe un mensaje corto para contarles a mis clientes que hoy hay <span class="k">[EMPANADAS DE PIPIÁN]</span>. Termina con una sola pregunta fácil de responder.<span class="q">”</span></div>''',
 bg(EMP, 760, 1040, 300))

err = [("x","Copiar sin revisar","La IA no conoce tus precios ni horarios. Léelo antes de guardarlo."),
       ("lock","Pegar datos de clientes","No pongas nombres ni celulares en la IA. Usa [CLIENTE]."),
       ("chat","Escribir a quien no lo pidió","Manda novedades solo a quien te dio permiso. Si no, es spam."),
       ("list","Textos largos","En WhatsApp: máximo 3 líneas y una sola pregunta.")]
S[7] = page(7, '<div class="tag">ERRORES COMUNES</div><h2>4 errores que <em>espantan clientes</em></h2>' +
 "".join(f'<div class="row" style="margin-bottom:26px">{ic(I[k])}<div><div style="font-size:34px;font-weight:700;margin-bottom:4px">{t}</div><div class="p mut" style="font-size:30px">{d}</div></div></div>' for k,t,d in err) +
 f'<div class="card row" style="margin-top:6px;padding:26px 34px">{ic(I["build"])}<p class="p" style="font-size:30px"><span class="k">¿Empresa grande?</span> Lo mismo escala con la API de WhatsApp Business y un asistente de IA conectado.</p></div>')

S[8] = page(8, f'''<div class="tag">TU TURNO</div>
<h1 style="font-size:96px;margin-bottom:44px">Hoy dejas tu <em>WhatsApp</em> trabajando por ti</h1>
<div class="card" style="font-size:36px;line-height:1.6">
<div class="row" style="align-items:center">{ic(I["tag"],52)}<span><b>Guárdalo</b> para configurarlo hoy</span></div>
<div class="row" style="align-items:center;margin-top:10px">{ic(I["chat"],52)}<span><b>Compártelo</b> con quien tiene negocio</span></div>
<div class="row" style="align-items:center;margin-top:10px">{ic(I["bolt"],52)}<span>Comenta <span class="k">WHATSAPP</span> y te envío los 4 prompts en un solo texto</span></div>
</div>
<p style="margin-top:40px;font-size:40px;font-weight:700">Escríbeme <span class="k">INFO</span> por DM · <span class="k">#IAconSamuel</span></p>''',
 bg(PH, 840, 220, 200))

STORY = '''<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0}html,body{width:1080px;height:1920px;background:#0E1726;font-family:Inter;overflow:hidden}
.t{position:absolute;top:70px;width:100%;text-align:center;color:#F2B544;font-weight:800;font-size:64px;letter-spacing:4px}
img{position:absolute;left:40px;top:190px;width:1000px;height:1250px;border-radius:24px}
.b{position:absolute;top:1490px;width:100%;text-align:center;color:#F4F1EA;font-size:40px;font-weight:600;line-height:1.5;padding:0 60px;box-sizing:border-box}.b span{color:#F2B544}</style></head>
<body><div class="t">NUEVO CARRUSEL</div><img src="lamina_01.png"><div class="b">Desliza las 8 láminas en mi perfil<br><span>@samuelsanchez1407</span></div></body></html>'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for n, h in S.items():
            f = f"{OUT}/l{n}.html"; open(f,"w").write(h)
            await pg.goto("file://"+f); await pg.wait_for_timeout(300)
            # overflow check
            ov = await pg.evaluate("""()=>{const m=document.querySelector('.main');const bt=document.querySelector('.bot');let mx=0;m.querySelectorAll('*').forEach(e=>{mx=Math.max(mx,e.getBoundingClientRect().bottom)});return [mx,bt.getBoundingClientRect().top]}""")
            print(n, ov)
            await pg.screenshot(path=f"{OUT}/lamina_{n:02d}.png")
        pg2 = await b.new_page(viewport={"width":1080,"height":1920})
        open(f"{OUT}/story.html","w").write(STORY)
        await pg2.goto("file://"+OUT+"/story.html"); await pg2.wait_for_timeout(300)
        await pg2.screenshot(path=f"{OUT}/historia_01.png")
        await b.close()
asyncio.run(main())
