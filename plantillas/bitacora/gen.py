import asyncio, html
from playwright.async_api import async_playwright

FONTS = "node_modules/@fontsource"
INK = "#1E1E1E"

def mascot(pose="point", w=330):
    s = f'stroke="{INK}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
    skin = "#E9B48C"
    # arms by pose (right arm = viewer's right)
    if pose == "point":
        rarm = f'<path d="M205 205 Q250 170 282 122" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round"/><path d="M205 205 Q250 170 282 122" fill="none" stroke="#2F6DB5" stroke-width="24" stroke-linecap="round"/><circle cx="286" cy="114" r="16" fill="{skin}" {s}/><path d="M294 104 L314 80" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M294 104 L314 80" stroke="{skin}" stroke-width="7" stroke-linecap="round"/>'
        larm = f'<path d="M95 210 Q70 260 85 300" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><circle cx="86" cy="305" r="15" fill="{skin}" {s}/>'
    elif pose == "think":
        rarm = f'<path d="M205 210 Q235 250 195 190" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><circle cx="183" cy="175" r="15" fill="{skin}" {s}/>'
        larm = f'<path d="M95 210 Q70 260 85 300" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><circle cx="86" cy="305" r="15" fill="{skin}" {s}/>'
    elif pose == "thumbs":
        rarm = f'<path d="M205 210 Q255 215 262 160" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><rect x="246" y="128" width="32" height="30" rx="10" fill="{skin}" {s}/><rect x="252" y="100" width="12" height="32" rx="6" fill="{skin}" {s}/>'
        larm = f'<path d="M95 210 Q70 260 85 300" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><circle cx="86" cy="305" r="15" fill="{skin}" {s}/>'
    else:  # tablet
        rarm = f'<path d="M205 210 Q230 260 190 280" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/>'
        larm = f'<path d="M95 210 Q75 260 115 280" fill="none" stroke="#2F6DB5" stroke-width="26" stroke-linecap="round"/><rect x="105" y="240" width="95" height="70" rx="8" fill="#2B2B2B" {s}/><rect x="113" y="248" width="79" height="54" rx="4" fill="#9FE3FF"/><path d="M122 290 L140 272 L155 282 L180 258" fill="none" stroke="#FF6B2C" stroke-width="5"/><circle cx="117" cy="283" r="13" fill="{skin}" {s}/><circle cx="190" cy="283" r="13" fill="{skin}" {s}/>'
    return f'''<svg viewBox="0 0 330 430" width="{w}" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="150" cy="415" rx="110" ry="12" fill="#000" opacity=".12"/>
  <rect x="108" y="300" width="38" height="100" rx="10" fill="#33415C" {s}/>
  <rect x="154" y="300" width="38" height="100" rx="10" fill="#33415C" {s}/>
  <path d="M100 400 h52 v14 h-60 z" fill="#5A3A22" {s}/><path d="M150 400 h52 v14 h-60 z" fill="#5A3A22" {s}/>
  {larm}
  <path d="M92 200 Q100 175 150 172 Q200 175 208 200 L212 310 L88 310 Z" fill="#2F6DB5" {s}/>
  <path d="M118 176 L150 215 L182 176" fill="#EAF2FB" {s} stroke-width="4"/>
  <path d="M95 255 H205" stroke="#FFB020" stroke-width="10"/><path d="M95 275 H205" stroke="#E8EEF5" stroke-width="6"/>
  <rect x="166" y="222" width="26" height="22" rx="3" fill="none" {s} stroke-width="3"/><path d="M174 218 v10" stroke="#FF6B2C" stroke-width="4"/>
  {rarm}
  <rect x="136" y="148" width="28" height="28" fill="{skin}" {s} stroke-width="4"/>
  <circle cx="98" cy="112" r="13" fill="{skin}" {s}/><circle cx="202" cy="112" r="13" fill="{skin}" {s}/>
  <ellipse cx="150" cy="110" rx="52" ry="58" fill="{skin}" {s}/>
  <path d="M112 140 Q150 182 188 140 Q186 166 150 172 Q114 166 112 140Z" fill="#4A3426" opacity=".85"/>
  <circle cx="130" cy="108" r="15" fill="#fff" stroke="{INK}" stroke-width="5"/><circle cx="170" cy="108" r="15" fill="#fff" stroke="{INK}" stroke-width="5"/>
  <path d="M145 108 h10" stroke="{INK}" stroke-width="5"/>
  <circle cx="132" cy="110" r="4.5" fill="{INK}"/><circle cx="172" cy="110" r="4.5" fill="{INK}"/>
  <path d="M120 88 q10 -6 20 0 M160 88 q10 -6 20 0" fill="none" stroke="{INK}" stroke-width="5"/>
  <path d="M136 140 Q150 150 164 140" fill="none" stroke="{INK}" stroke-width="5"/>
  <path d="M94 74 Q96 22 150 20 Q204 22 206 74 Z" fill="#FFFFFF" {s}/>
  <path d="M80 78 Q150 62 220 78 L222 90 Q150 76 78 90 Z" fill="#FFFFFF" {s}/>
  <path d="M150 22 V72" stroke="{INK}" stroke-width="4"/><rect x="138" y="44" width="24" height="18" rx="4" fill="#FF6B2C" stroke="{INK}" stroke-width="3"/>
</svg>'''

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Marker;src:url(FONTS/permanent-marker/files/permanent-marker-latin-400-normal.woff2)}
@font-face{font-family:Kalam;font-weight:400;src:url(FONTS/kalam/files/kalam-latin-400-normal.woff2)}
@font-face{font-family:Kalam;font-weight:700;src:url(FONTS/kalam/files/kalam-latin-700-normal.woff2)}
@font-face{font-family:Inter;font-weight:500;src:url(FONTS/inter/files/inter-latin-500-normal.woff2)}
@font-face{font-family:Inter;font-weight:700;src:url(FONTS/inter/files/inter-latin-700-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:Kalam;color:#1E1E1E;
 background:#F7F3EA;
 background-image:linear-gradient(#DCE6F2 1.5px,transparent 1.5px),linear-gradient(90deg,#DCE6F2 1.5px,transparent 1.5px);
 background-size:45px 45px;position:relative}
.margin{position:absolute;left:92px;top:0;bottom:0;width:3px;background:#F2A0A0}
.rings{position:absolute;left:18px;top:40px;bottom:40px;width:44px;
 background:repeating-linear-gradient(#0000 0 34px,#3A3A3A 34px 46px,#0000 46px 72px);border-radius:8px}
.wrap{position:absolute;left:130px;right:70px;top:70px;bottom:60px}
.num{position:absolute;right:0;top:-12px;font-family:Marker;font-size:52px}
.tag{display:inline-block;font-family:Inter;font-weight:700;font-size:24px;letter-spacing:3px;color:#FF6B2C;border:3px solid #FF6B2C;border-radius:40px;padding:8px 22px;transform:rotate(-1.5deg)}
.hl{background:linear-gradient(transparent 18%,#FFE14D 18% 88%,transparent 88%);padding:0 10px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
h1{font-family:Marker;font-weight:400;line-height:1.08;margin-top:26px}
.u{border-bottom:9px solid #FF6B2C;border-radius:4px}
.foot{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:flex-end;font-family:Kalam;font-weight:700;font-size:30px}
.foot .h{color:#FF6B2C}
.card{border:4px solid #FF6B2C;border-radius:16px;background:#FFFDF7;padding:22px 26px;margin-top:22px;position:relative}
.card b.n{font-family:Marker;font-size:46px;color:#1E1E1E;background:#FFE14D;border-radius:10px;padding:0 12px;margin-right:12px;float:left;line-height:1.15}
.card p{font-family:Kalam;font-size:35px;line-height:1.3}
.card .who{font-family:Inter;font-weight:700;font-size:21px;color:#2F6DB5;letter-spacing:1px;margin-bottom:6px}
.arrow{position:absolute}
</style></head><body><div class="rings"></div><div class="margin"></div><div class="wrap">BODY</div></body></html>""".replace("FONTS", FONTS)

def foot(right="Desliza →"):
    return f'<div class="foot"><span>Samuel Sánchez · <span class="h">#IAconSamuel</span></span><span style="border-bottom:6px solid #FF6B2C">{right}</span></div>'

ARROW = '<svg class="arrow" style="{st}" width="150" height="90" viewBox="0 0 150 90"><path d="M8 70 Q70 10 130 30" fill="none" stroke="#FF6B2C" stroke-width="8" stroke-linecap="round"/><path d="M108 14 L134 30 L110 48" fill="none" stroke="#FF6B2C" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SPARK = '<svg class="arrow" style="{st}" width="90" height="90" viewBox="0 0 90 90"><g stroke="#FF6B2C" stroke-width="7" stroke-linecap="round"><path d="M45 8v18M45 64v18M8 45h18M64 45h18M18 18l12 12M60 60l12 12M72 18L60 30M30 60L18 72"/></g></svg>'

def prompts_slide(n, total, tag, title, items):
    cards = "".join(f'<div class="card"><b class="n">{i}</b><div class="who">{html.escape(w)}</div><p>{html.escape(t)}</p></div>' for i, w, t in items)
    return f'''<div class="num">{n}/{total}</div><span class="tag">PROMPTS {items[0][0]} AL {items[-1][0]} · {tag}</span>
<h1 style="font-size:84px"><span class="hl">{title}</span></h1>
{cards}
<div style="position:absolute;right:-40px;bottom:30px">{mascot("tablet",250)}</div>
{foot()}'''

T = 8
slides = []
# 1 portada
slides.append(f'''<div class="num">1/{T}</div><span class="tag">BITÁCORA DEL INGENIERO · IA</span>
<h1 style="font-size:122px;margin-top:40px"><span class="hl">15 prompts</span><br>para que tu<br>negocio <span class="u">venda más</span></h1>
<div style="font-family:Kalam;font-weight:700;font-size:40px;margin-top:34px">Copia y pega en <span style="color:#2F6DB5">ChatGPT</span> · <span style="color:#2F6DB5">Claude</span> · <span style="color:#2F6DB5">Gemini</span></div>
<div style="font-family:Kalam;font-size:32px;margin-top:8px;color:#555">Tienda, empanadas, peluquería o taller. Gratis.</div>
{ARROW.format(st="left:470px;top:860px;transform:rotate(15deg)")}
{SPARK.format(st="left:690px;top:300px")}
<div style="position:absolute;left:560px;top:760px">{mascot("point",330)}</div>
{foot()}''')
# 2 cómo usarlos
slides.append(f'''<div class="num">2/{T}</div><span class="tag">ANTES DE EMPEZAR</span>
<h1 style="font-size:96px"><span class="hl">Así se usan</span><br>(30 segundos)</h1>
<div class="card"><b class="n">1</b><p style="font-size:34px">Abre ChatGPT, Claude o Gemini en tu celular. La versión gratis sirve.</p></div>
<div class="card"><b class="n">2</b><p style="font-size:34px">Copia el prompt y cambia lo que está entre <b style="background:#FFE14D">[CORCHETES]</b> por los datos de tu negocio.</p></div>
<div class="card"><b class="n">3</b><p style="font-size:34px">Si la respuesta no te gusta, escríbele: "más corto", "más cercano" o "dame 3 opciones".</p></div>
<div style="font-family:Kalam;font-size:30px;margin-top:26px;color:#555">Ejemplo: [negocio] = "venta de empanadas en Bello"</div>
<div style="position:absolute;right:-20px;bottom:50px">{mascot("think",230)}</div>
{foot()}''')
slides.append(prompts_slide(3, T, "VENDER POR WHATSAPP", "Vender por WhatsApp", [
 (1, "MENSAJE DE BIENVENIDA", "Escribe un saludo corto y amable para WhatsApp de mi [negocio] que muestre el menú del día y los precios: [lista]."),
 (2, "OFERTA DEL DÍA", "Dame 5 mensajes de máximo 2 líneas para ofrecer [producto] hoy a mis clientes de [barrio]. Tono cercano, sin presionar."),
 (3, "CLIENTE QUE NO VOLVIÓ", "Escribe un mensaje para un cliente que no compra hace un mes en mi [negocio], invitándolo a volver con [beneficio]."),
]))
slides.append(prompts_slide(4, T, "REDES SOCIALES", "Publicar sin pensar tanto", [
 (4, "IDEAS DE LA SEMANA", "Dame 7 ideas de publicaciones para Instagram de mi [negocio], una por día, con texto corto y una pregunta para comentar."),
 (5, "TEXTO PARA UNA FOTO", "Tengo una foto de [producto]. Escríbeme 3 textos cortos para publicarla, con un llamado a pedir por WhatsApp."),
 (6, "RESPONDER COMENTARIOS", "Ayúdame a responder este comentario de forma amable y profesional: [comentario]."),
]))
slides.append(prompts_slide(5, T, "INVENTARIO Y COMPRAS", "Que no te falte nada", [
 (7, "CUÁNDO PEDIR", "Vendo [cantidad] de [producto] al día y el proveedor tarda [días] en traerlo. ¿Cuándo debo hacer el pedido? Explícamelo fácil."),
 (8, "LISTA DE COMPRAS", "Con estas ventas de la semana [datos], arma mi lista de compras para la próxima semana sin que sobre ni falte."),
 (9, "PRODUCTO QUIETO", "Tengo [producto] que no se vende. Dame 5 ideas para moverlo esta semana sin perder plata."),
]))
slides.append(prompts_slide(6, T, "PRECIOS Y COSTOS", "Cobrar lo justo", [
 (10, "COSTO REAL", "Ayúdame a calcular el costo de una [unidad de producto] con estos ingredientes y precios: [lista]. Muéstralo en una tabla."),
 (11, "PRECIO DE VENTA", "Si mi costo es [costo] y quiero ganar [porcentaje] %, ¿a cuánto debo vender? Compara con [precio de la competencia]."),
 (12, "COMBO GANADOR", "Arma 3 combos con mis productos [lista] que suban la venta promedio sin regalar la ganancia."),
]))
slides.append(prompts_slide(7, T, "ATENCIÓN AL CLIENTE", "Clientes felices", [
 (13, "QUEJA", "Un cliente se quejó por [problema]. Escríbeme una respuesta que pida disculpas y ofrezca una solución concreta."),
 (14, "PREGUNTAS FRECUENTES", "Haz una lista de las 10 preguntas que más me harían en mi [negocio] con respuestas cortas para copiar y pegar."),
 (15, "PEDIR UNA RESEÑA", "Escribe un mensaje corto para pedirle a un cliente feliz que me deje una reseña en Google Maps."),
]))
slides.append(f'''<div class="num">8/{T}</div><span class="tag">ANTES DE IRTE</span>
<h1 style="font-size:110px"><span class="hl">Guárdalo</span> para<br>usarlo mañana</h1>
<div style="font-family:Kalam;font-weight:700;font-size:44px;margin-top:40px;line-height:1.55">
✔ <span class="u">Envíaselo</span> a ese amigo que tiene negocio<br>
✔ Comenta <b style="background:#FFE14D;padding:0 8px">PROMPTS</b> y te digo cuál usar primero<br>
✔ Sígueme: <span style="color:#2F6DB5">@samuelsanchez1407</span></div>
{SPARK.format(st="left:60px;top:1010px")}
<div style="position:absolute;right:20px;bottom:70px">{mascot("thumbs",300)}</div>
{foot("IA con Samuel")}''')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for i, body in enumerate(slides, 1):
            open(f"s{i}.html","w").write(BASE.replace("BODY", body))
            await pg.goto(f"file:///home/claude/bitacora/s{i}.html")
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"lamina_{i:02d}.jpg", type="jpeg", quality=90)
        await b.close()
if __name__ == "__main__":
    asyncio.run(main())
