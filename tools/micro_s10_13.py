#!/usr/bin/env python3
"""Microeconomía Aplicada (AD6002) · semanas 10 a 13, ADELANTADAS SEGÚN EL SÍLABO (el profesor no subió material).
Fuentes: orden de temas del sílabo 2026-2 (6.7 bienes públicos, 6.8 estructuras de mercado, 6.9 oligopolio) y la
bibliografía del sílabo (Krugman, Fundamentos de economía; Pindyck y Rubinfeld, Microeconomía).
Crea el bloque micro-pc2 (sem. 9–13, PC2 en la semana 14) y agrega los temas al final (micro-ef).
Cuando el profesor suba su material: ajustar ejemplos, notación y ejercicios, y quitar la marca 📖.
Uso: python3 tools/micro_s10_13.py   (reejecutable)."""
import json, os
from fractions import Fraction as Fr

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(RAIZ, "cursos", n + ".json")
ADV = ("<div class=\"note\" style=\"border-left:4px solid var(--tan);padding:6px 10px;margin-bottom:.6em\">📖 <b>Adelantado según el sílabo.</b> "
       "El profesor todavía no subió esta clase: este tema se armó con el orden del sílabo y su bibliografía (Krugman y Pindyck). "
       "Cuando suba su material, se ajustarán los ejemplos y la notación.</div>")

def E(i, lvl, title, q, checks, steps, ans, hint, tags, chain=False):
    assert len(tags) == len(steps), i
    e = {"id": i, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans,
         "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}
    if chain: e["chain"] = True
    return e

def O(o, p="Respuesta"):
    assert len(o) == 5 and len(set(o)) == 5, o
    return {"p": p, "o": o}

def NUM(fs, p="Respuesta"): return {"t": "num", "p": p, "f": fs}

def lesson(frase, claves, resumen, err):
    return ("<h3>La idea en una frase</h3><p>" + frase + "</p><h3>Claves</h3><ul>" + "".join("<li>" + c + "</li>" for c in claves) + "</ul>"
            "<div class=\"ej\"><b>En 30 segundos:</b> " + resumen + "</div><div class=\"err\"><b>Error común:</b> " + err + "</div>")

# ---------------------------------------------------------------- gráficos tocables (coordenadas de datos → SVG)
class G:
    def __init__(s, xr, yr, W=300, H=240, L=40, B=40, T=8, R=8):
        s.x0, s.x1 = xr; s.y0, s.y1 = yr; s.W, s.H, s.L, s.Bm, s.T, s.R = W, H, L, B, T, R; s.o = []
    def X(s, x): return s.L + (s.W - s.L - s.R) * (x - s.x0) / (s.x1 - s.x0)
    def Y(s, y): return s.H - s.Bm - (s.H - s.Bm - s.T) * (y - s.y0) / (s.y1 - s.y0)
    def line(s, a, b, color, lab=None, at=None):
        s.o.append(f'<line x1="{s.X(a[0]):.1f}" y1="{s.Y(a[1]):.1f}" x2="{s.X(b[0]):.1f}" y2="{s.Y(b[1]):.1f}" style="stroke:var(--{color});stroke-width:2.4"/>')
        if lab:
            p = at or b; s.o.append(f'<text class="dl" x="{s.X(p[0]) - 4:.1f}" y="{s.Y(p[1]) - 6:.1f}" text-anchor="end">{lab}</text>')
    def curve(s, f, a, b, color, lab=None):
        pts = [(a + (b - a) * k / 60) for k in range(61)]
        d = "M" + "L".join(f"{s.X(x):.1f} {s.Y(f(x)):.1f}" for x in pts)
        s.o.append(f'<path d="{d}" style="fill:none;stroke:var(--{color});stroke-width:2.4"/>')
        if lab: s.o.append(f'<text class="dl" x="{s.X(b) - 2:.1f}" y="{s.Y(f(b)) - 6:.1f}" text-anchor="end">{lab}</text>')
    def dash(s, a, b): s.o.append(f'<line class="dsh" x1="{s.X(a[0]):.1f}" y1="{s.Y(a[1]):.1f}" x2="{s.X(b[0]):.1f}" y2="{s.Y(b[1]):.1f}"/>')
    def text(s, p, t, cls="dm"): s.o.append(f'<text class="{cls}" x="{s.X(p[0]):.1f}" y="{s.Y(p[1]):.1f}" text-anchor="middle">{t}</text>')
    def tick(s, x=None, y=None, lab=""):
        if x is not None: s.o.append(f'<text class="dm" x="{s.X(x):.1f}" y="{s.H - s.Bm + 14}" text-anchor="middle">{lab}</text>')
        if y is not None: s.o.append(f'<text class="dm" x="{s.L - 4}" y="{s.Y(y) + 4:.1f}" text-anchor="end">{lab}</text>')
    def poly(s, pts, z): s.o.append(f'<polygon data-z="{z}" points="' + " ".join(f"{s.X(x):.1f},{s.Y(y):.1f}" for x, y in pts) + '"/>')
    def pt(s, p, z): s.o.append(f'<circle data-z="{z}" cx="{s.X(p[0]):.1f}" cy="{s.Y(p[1]):.1f}" r="9"/>')
    def svg(s, xl="Q", yl="P"):
        ax = f'<path class="gl" d="M{s.L} {s.T}V{s.H - s.Bm}H{s.W - s.R}"/><text class="dl" x="{s.L - 26}" y="{s.T + 12}">{yl}</text><text class="dl" x="{s.W - s.R - 10}" y="{s.H - s.Bm + 30}">{xl}</text>'
        return f'<svg class="dg" viewBox="0 0 {s.W} {s.H}" xmlns="http://www.w3.org/2000/svg">' + ax + "".join(s.o) + "</svg>"

def TAP(svg, a, p, e=None, multi=False):
    c = {"t": "tap", "p": p, "svg": svg, "a": a}
    if multi: c["multi"] = True
    if e: c["e"] = e
    return c

# =====================================================================
# SEMANA 10 · Bienes públicos
# =====================================================================
G10_teo = ADV + (
 "<p>Para clasificar un bien se hacen dos preguntas:</p><ul>"
 "<li><b>¿Es excluible?</b> ¿Se puede impedir que lo use quien no paga? (una entrada al cine sí; el alumbrado de la calle no).</li>"
 "<li><b>¿Es rival?</b> ¿Si yo lo uso, a ti te queda menos? (un pan sí; una señal de radio no).</li></ul>"
 "<div class=\"tbl\"><table><tr><th></th><th>Rival</th><th>No rival</th></tr>"
 "<tr><th>Excluible</th><td><b>Privado</b>: pan, ropa, un menú</td><td><b>De club</b>: Netflix, TV por cable, un gimnasio</td></tr>"
 "<tr><th>No excluible</th><td><b>Recurso común</b>: la anchoveta en el mar, el agua de un río</td><td><b>Público</b>: alumbrado, defensa nacional, un faro</td></tr></table></div>"
 "<p><b>Problema del polizón</b> (free rider): como nadie puede ser excluido de un bien público, a cada uno le conviene que paguen los demás. Si depende de aportes voluntarios, el mercado lo produce de menos o no lo produce. Por eso suele proveerlo el <b>Estado</b>, financiado con impuestos, cuando el beneficio total supera el costo (<b>análisis costo–beneficio</b>: se suman las valoraciones de todos).</p>"
 "<p><b>Tragedia de los comunes:</b> con los recursos comunes pasa lo contrario: cada uno usa de más porque no paga el desgaste que causa a los demás (sobrepesca). Se corrige con cuotas, vedas, permisos o derechos de propiedad.</p>"
 "<p>Igual que las externalidades (semana 9), son <b>fallas de mercado</b>: el mercado solo no llega a la cantidad eficiente.</p>"
)
G10_form = ["Excluible: se puede impedir el uso a quien no paga", "Rival: mi uso reduce el tuyo",
            "Público: no rival y no excluible · común: rival y no excluible", "Polizón: usar sin pagar → se produce de menos",
            "Proveer si Σ valoraciones ≥ costo", "Comunes: se sobreexplotan → cuotas, vedas"]
G10_lesson = lesson("Si no se puede excluir a nadie, nadie quiere pagar: el mercado falla y suele entrar el Estado.",
  ["<b>Dos preguntas</b> (¿excluible?, ¿rival?) dan los cuatro tipos de bienes.",
   "<b>Polizón:</b> disfrutar sin pagar. Lo ves en el juego: cuando uno deja de aportar, los demás también.",
   "<b>Costo–beneficio:</b> un bien público vale la pena si la <i>suma</i> de lo que vale para cada persona supera su costo.",
   "<b>Recursos comunes:</b> la anchoveta peruana se protege con cuotas y vedas del Produce para evitar la tragedia de los comunes."],
  "Bien público = no rival + no excluible → polizón → lo financia el Estado. Recurso común = rival + no excluible → sobreuso → cuotas.",
  "decir que un bien es público porque lo produce el Estado. Lo que importa son sus características: el agua potable de Sedapal es excluible (te pueden cortar) y rival.")
G10 = []
G10.append(E("g10e1", 1, "Calentamiento: semana 9",
  "<p>Recordando la semana pasada: una fábrica contamina un río y los pescadores pierden ingresos. ¿Qué es?</p>",
  [O(["Una externalidad negativa: el mercado produce más que lo óptimo", "Una externalidad positiva: el mercado produce menos", "Un bien público", "El mercado funcionando bien", "Un recurso de club"])],
  ["El pescador es un tercero que pierde sin ser compensado: externalidad negativa.", "El costo social supera al privado y el mercado produce de más. Hoy veremos otra falla de mercado: los bienes públicos."],
  "Externalidad negativa", "¿Hay un tercero afectado?", [["extneg"], ["extneg"]]))
G10.append(E("g10e2", 1, "Los cuatro tipos de bienes",
  "<p>Clasifica cada bien con las dos preguntas: ¿excluible? ¿rival?</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Privado", "De club", "Recurso común", "Público"], "items": [
    {"x": "Un pan francés", "c": 0}, {"x": "Netflix", "c": 1, "e": "Excluible (sin cuenta no lo ves) y no rival (que tú lo veas no me quita nada)."},
    {"x": "La anchoveta en el mar", "c": 2, "e": "No se puede excluir fácilmente a los barcos, pero lo que uno pesca ya no lo pesca otro."},
    {"x": "El alumbrado público", "c": 3}, {"x": "La defensa nacional", "c": 3},
    {"x": "Una autopista con peaje y sin tráfico", "c": 1, "e": "Con peaje es excluible; sin congestión no es rival."},
    {"x": "Un almuerzo en un restaurante", "c": 0}, {"x": "El agua de un río sin control", "c": 2}]}],
  ["Excluible + rival → privado; excluible + no rival → club; no excluible + rival → común; no excluible + no rival → público.",
   "Ojo: una autopista congestionada se vuelve rival (mi auto te quita espacio)."],
  "Clasificación correcta", "Dos preguntas: ¿excluible? ¿rival?", [["tipbien"], ["tipbien"]]))
G10.append(E("g10e3", 1, "¿Qué significa «no rival»?",
  "<p>Un faro guía a todos los barcos que pasan. Que sea <strong>no rival</strong> significa que…</p>",
  [O(["Que un barco lo use no reduce lo que pueden usar los demás", "No se puede impedir que un barco lo use", "Lo produce el Estado", "Es gratis", "Nadie lo valora"])],
  ["No rival: el consumo de uno no reduce el de otro. No excluible es otra cosa: no se puede impedir el uso.",
   "El faro es ambas cosas, por eso es el ejemplo clásico de bien público."],
  "Mi uso no reduce el tuyo", "Rival ≠ excluible.", [["tipbien"], ["tipbien"]]))
G10.append(E("g10e4", 2, "El juego del polizón",
  "<p>Imagina que juegas al polizón (arriba, en 🧪): en la primera ronda no aportas, los vecinos sí, y el parque se construye igual. En las rondas siguientes los aportes empiezan a caer. ¿Por qué?</p>",
  [O(["Los vecinos también vieron que les convenía no pagar si igual disfrutan el parque", "El parque se volvió rival", "El parque dejó de ser útil", "El Estado prohibió el parque", "Los vecinos se quedaron sin dinero"])],
  ["Ser polizón te da más en la ronda 1 (te quedas tus S/ 10 y además disfrutas el parque).",
   "Pero los demás razonan igual: bajan sus aportes, no se junta lo necesario y todos terminan peor que si hubieran cooperado. Es el problema del polizón."],
  "Todos quieren que paguen los demás", "Piensa como un vecino más.", [["polizon"], ["polizon"]]))
G10.append(E("g10e5", 2, "¿Vale la pena el alumbrado?",
  "<p>Tres vecinos valoran poner un poste de luz en su pasaje en S/ 40, S/ 30 y S/ 50. El poste cuesta S/ 100.</p>",
  [NUM([{"l": "Beneficio total", "a": 120, "u": "S/"}, {"l": "Beneficio neto social", "a": 20, "u": "S/"}], "Calcula"),
   O(["Sí conviene, pero quizás nadie lo pague solo: ninguno lo valora en S/ 100", "No conviene: cada uno lo valora en menos de S/ 100", "Conviene solo si lo paga el que más lo valora", "No conviene porque es no excluible", "Da igual"], "¿Se debe construir?")],
  ["En un bien público se <b>suman</b> las valoraciones (todos lo disfrutan a la vez): 40 + 30 + 50 = 120.",
   "Beneficio total 120 &gt; costo 100: socialmente conviene (neto +20).",
   "Pero ninguno lo valora en 100 por sí solo y cada uno espera que pague otro (polizón). Una solución: que el municipio lo construya y cobre, por ejemplo, arbitrios."],
  "Total 120, neto 20: conviene", "Suma las valoraciones.", [["costben"], ["costben"], ["polizon"]], chain=True))
G10.append(E("g10e6", 2, "Repartir con un impuesto",
  "<p>Cinco vecinos valoran un parque en S/ 30 cada uno. Cuesta S/ 100 y la municipalidad lo financia cobrando lo mismo a todos.</p>",
  [NUM([{"l": "Pago de cada vecino", "a": 20, "u": "S/"}, {"l": "Ganancia neta de cada uno", "a": 10, "u": "S/"}], "Calcula")],
  ["Cada uno paga 100 / 5 = S/ 20.", "Cada uno recibe un parque que valora en 30: gana 30 − 20 = S/ 10. Todos mejoran, y el impuesto evita que haya polizones."],
  "S/ 20 y S/ 10", "Divide el costo.", [["costben"], ["polizon"]]))
G10.append(E("g10e7", 2, "Tragedia de los comunes",
  "<p>Si nadie controla la pesca de anchoveta, cada barco pesca lo más que puede. ¿Qué medida ataca mejor el problema?</p>",
  [O(["Cuotas de pesca por barco y vedas en época de reproducción", "Subsidiar la compra de más barcos", "Bajar el precio de la anchoveta", "Prohibir exportar harina de pescado", "Dejar que cada barco decida"])],
  ["La anchoveta es un recurso común: rival y no excluible. Cada barco no paga el daño que causa a los demás al agotar el recurso.",
   "Las cuotas y vedas (como las que fija el Produce en el Perú) limitan el uso total. Subsidiar barcos empeoraría la sobrepesca."],
  "Cuotas y vedas", "Rival + no excluible.", [["comunes"], ["comunes"]]))
G10.append(E("g10e8", 1, "¿Por qué el mercado no lo produce?",
  "<p>¿Por qué una empresa privada casi nunca ofrece alumbrado público por su cuenta?</p>",
  [O(["No puede cobrar a quien no paga: todos lo usarían gratis", "Es demasiado barato de producir", "Es rival", "La demanda es cero", "Está prohibido"])],
  ["Si no se puede excluir, la empresa no puede cobrar: cada uno espera usarlo gratis.", "Sin ingresos no hay incentivo a producirlo, aunque la sociedad lo valore: es una falla de mercado."],
  "No puede excluir ni cobrar", "No excluible.", [["polizon"], ["tipbien"]]))
G10.append(E("g10e9", 2, "Ordena el análisis costo–beneficio",
  "<p>Una municipalidad decide si construir un puente peatonal. Ordena los pasos.</p>",
  [{"t": "order", "p": "Toca los pasos en orden", "items": [
    "Estimar cuánto vale el puente para cada grupo de usuarios",
    "Sumar esas valoraciones (beneficio total)",
    "Compararlo con el costo de construirlo y mantenerlo",
    "Construir solo si el beneficio total supera el costo, y financiarlo con impuestos"]}],
  ["Primero se estiman las valoraciones individuales y se suman, porque todos lo usan a la vez.", "Si el total supera el costo, conviene; se financia con impuestos para evitar el polizón."],
  "Valorar → sumar → comparar → decidir", "Empieza por los usuarios.", [["costben"], ["costben"]]))
G10_tools = [{"w": "poliz", "t": "Juego del polizón", "p": "Eres uno de cinco vecinos. Decide cuánto aportas cada ronda y mira qué hacen los demás.", "o": {}}]

# =====================================================================
# SEMANA 11 · Maximización de beneficios y competencia perfecta
# =====================================================================
import math
# tabla de una empresa precio-aceptante (P = 10)
TQ = [0, 1, 2, 3, 4, 5, 6]; TCT = [10, 15, 18, 22, 28, 37, 49]; PT = 10
TIT = [PT * q for q in TQ]; TB = [a - b for a, b in zip(TIT, TCT)]
CMgT = [TCT[k] - TCT[k - 1] for k in range(1, len(TQ))]
assert CMgT == [5, 3, 4, 6, 9, 12] and TB == [-10, -5, 2, 8, 12, 13, 11]
qstar = TQ[TB.index(max(TB))]; assert qstar == 5 and TB.count(max(TB)) == 1
# P = 40, CT = 50 + 4Q + Q² → CMg = 4 + 2Q = 40 → Q = 18
q1 = Fr(36, 2); b1 = 40 * q1 - (50 + 4 * q1 + q1 ** 2); assert q1 == 18 and b1 == 274
assert Fr(60 - 10, 5) == 10
# gráfico de la empresa: CT = 12 + 3Q + 0,75Q² → CMg = 3 + 1,5Q, CMe = 12/Q + 3 + 0,75Q (mínimo en Q = 4, CMe = 9 = CMg)
cmg = lambda q: 3 + 1.5 * q; cme = lambda q: 12 / q + 3 + 0.75 * q
assert abs(cmg(4) - cme(4)) < 1e-12
qs = (10 - 3) / 1.5; r1 = (7 - math.sqrt(13)) / 1.5; r2 = (7 + math.sqrt(13)) / 1.5
assert abs(cme(r1) - 10) < 1e-9 and abs(cme(r2) - 10) < 1e-9 and cme(qs) < 10
g = G((0, 8), (0, 14))
g.curve(cmg, 0.2, 7.3, "bad", "CMg"); g.curve(cme, 1.3, 8, "tan", "CMe"); g.line((0, 10), (8, 10), "curve", "P = IMg", at=(2.2, 10))
g.dash((qs, 0), (qs, 10)); g.tick(y=10, lab="10")
for p_, z in (((qs, 10), "opt"), ((r1, 10), "x1"), ((r2, 10), "x2"), ((4, 9), "x3")): g.pt(p_, z)
SVG_PC = g.svg()

M11_teo = ADV + (
 "<p><b>Beneficio</b> = ingreso total − costo total: \\(\\pi=IT-CT\\), con \\(IT=P\\cdot Q\\) (y, como viste en la semana 7, el costo incluye el costo de oportunidad).</p>"
 "<p>Para decidir cuánto producir se mira <b>la próxima unidad</b>: el <b>ingreso marginal</b> \\(IMg\\) (cuánto suma al ingreso) y el <b>costo marginal</b> \\(CMg\\) (cuánto suma al costo). Si \\(IMg\\gt CMg\\), conviene producir más; si \\(IMg\\lt CMg\\), menos. El beneficio es máximo donde \\(IMg=CMg\\).</p>"
 "<p><b>Competencia perfecta:</b> muchos compradores y vendedores, producto homogéneo, información completa y libre entrada y salida (se acerca: limones o papas en el mercado mayorista). Cada empresa es <b>precio-aceptante</b>: vende lo que quiera al precio del mercado, así que \\(IMg=P\\) y produce donde \\(P=CMg\\).</p>"
 "<ul><li>Gana si \\(P\\gt CMe\\): beneficio \\(=(P-CMe)\\cdot Q\\). Pierde si \\(P\\lt CMe\\).</li>"
 "<li>Corto plazo: si \\(P\\) no cubre ni el costo variable medio mínimo, conviene <b>cerrar</b> (solo pierde el costo fijo).</li>"
 "<li>Largo plazo: si hay beneficios, entran empresas, el precio baja hasta \\(P=CMe\\) mínimo y el <b>beneficio económico es cero</b>.</li></ul>"
)
M11_form = ["\\(\\pi=IT-CT\\), \\(IT=P\\cdot Q\\)", "Máximo beneficio: \\(IMg=CMg\\)", "Competencia perfecta: \\(IMg=P\\Rightarrow P=CMg\\)",
            "Beneficio \\(=(P-CMe)\\cdot Q\\)", "Cerrar (corto plazo): \\(P\\lt CVMe\\) mínimo", "Largo plazo: \\(P=CMe\\) mínimo, beneficio 0"]
M11_lesson = lesson("Produce una unidad más mientras sume más de lo que cuesta: el máximo está donde IMg = CMg.",
  ["<b>Piensa en lo marginal:</b> lo ya gastado no cambia la decisión sobre la próxima unidad.",
   "<b>Precio-aceptante:</b> el mercado pone el precio, así que cada unidad extra te da exactamente P.",
   "<b>En el gráfico:</b> el beneficio es el rectángulo entre P y CMe, de ancho Q (en la herramienta: verde si ganas, rojo si pierdes).",
   "<b>Largo plazo:</b> la libre entrada se come los beneficios hasta que P = CMe mínimo."],
  "Máximo beneficio con IMg = CMg; en competencia perfecta IMg = P, así que P = CMg. Ganancia = (P − CMe)·Q. Con libre entrada, a largo plazo el beneficio es cero.",
  "elegir la Q donde el beneficio <i>por unidad</i> (P − CMe) es máximo: lo que se maximiza es el beneficio total.")
M11 = []
M11.append(E("m11e1", 1, "Calentamiento: semana 10",
  "<p>¿Qué tipo de bien es la señal de una radio abierta?</p>",
  [O(["Público: no rival y no excluible", "Privado", "De club", "Recurso común", "Depende del precio"])],
  ["Que tú escuches no me quita señal (no rival) y no se puede impedir que alguien la sintonice (no excluible).", "Por eso las radios abiertas viven de la publicidad: no pueden cobrarle al oyente."],
  "Público", "¿Excluible? ¿Rival?", [["tipbien"], ["polizon"]]))
M11.append(E("m11e2", 1, "¿Competencia perfecta?",
  "<p>Clasifica cada mercado.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Se acerca a competencia perfecta", "No es competencia perfecta"], "items": [
    {"x": "Limones en el mercado mayorista", "c": 0}, {"x": "Papa blanca en Lima", "c": 0}, {"x": "Huevos a granel", "c": 0},
    {"x": "Agua potable de la ciudad", "c": 1, "e": "Una sola empresa: monopolio (natural)."},
    {"x": "Telefonía móvil", "c": 1, "e": "Pocas empresas grandes: oligopolio."},
    {"x": "Zapatillas de marca", "c": 1, "e": "Producto diferenciado por marca: no es homogéneo."}]}],
  ["Competencia perfecta: muchos vendedores pequeños, producto homogéneo y libre entrada; nadie puede poner su precio.",
   "Si hay una sola empresa, pocas, o productos diferenciados por marca, ya no lo es (semanas 12 y 13)."],
  "Clasificación correcta", "¿Muchos vendedores con el mismo producto?", [["compperf"], ["compperf"]]))
M11.append(E("m11e3", 2, "Tabla: ¿cuánto producir?",
  "<p>Una empresa precio-aceptante vende a \\(P=10\\). Completa el costo marginal y el beneficio, y elige la cantidad.</p>",
  [{"t": "fill", "p": "Completa (CMg = CT de esa fila − CT de la anterior; beneficio = 10·Q − CT)", "head": ["Q", "CT", "CMg", "Beneficio"],
    "rows": [[str(TQ[k]), str(TCT[k]), ({"a": CMgT[k - 1]} if k else "—"), {"a": TB[k]}] for k in range(len(TQ))]},
   NUM([{"l": "Q que maximiza el beneficio", "a": qstar}], "Decisión")],
  ["CMg: " + ", ".join(map(str, CMgT)) + ". Beneficio: " + ", ".join(map(str, TB)) + ".",
   "Regla marginal: la 5.ª unidad cuesta 9 &lt; 10 (conviene); la 6.ª cuesta 12 &gt; 10 (no conviene). Q = 5, con el mayor beneficio (13). Fíjate que con Q = 0 se pierde el costo fijo (10)."],
  "Q = 5 (beneficio 13)", "Compara cada CMg con P = 10.", [["maxben"], ["maxben"]], chain=True))
M11.append(E("m11e4", 2, "Busca la Q del beneficio máximo",
  "<p>Una empresa en competencia perfecta vende a S/ 40 y su costo es \\(CT=50+4Q+Q^2\\). Mueve Q hasta maximizar el beneficio.</p>",
  [{"t": "qmax", "p": "Mueve Q", "mode": "pc", "P": 40, "F": 50, "c": 4, "d": 1, "qmax": 30, "q0": 6, "ans": 18, "tol": 0.51, "e": "Busca donde la recta P cruza al CMg."},
   NUM([{"l": "Beneficio máximo", "a": int(b1), "u": "S/"}], "Calcula")],
  ["\\(CMg=4+2Q\\). Con \\(P=CMg\\): \\(40=4+2Q\\Rightarrow Q=18\\).",
   "\\(\\pi=40\\cdot18-(50+72+324)\\) \\(=720-446=274\\). En la herramienta: a la izquierda de 18, IMg &gt; CMg (conviene más); a la derecha, al revés."],
  "Q = 18, beneficio 274", "P = CMg.", [["maxben"], ["maxben"]], chain=True))
M11.append(E("m11e5", 1, "P = CMg con números",
  "<p>El precio de mercado es S/ 60 y el costo marginal de una empresa es \\(CMg=10+5Q\\).</p>",
  [NUM([{"l": "Q óptima", "a": 10}, {"l": "Ingreso total", "a": 600, "u": "S/"}], "Calcula")],
  ["Precio-aceptante: \\(IMg=P=60\\). \\(60=10+5Q\\Rightarrow Q=10\\).", "\\(IT=60\\cdot10=600\\)."],
  "Q = 10, IT = 600", "Iguala P y CMg.", [["maxben"], ["compperf"]]))
M11.append(E("m11e6", 2, "Toca el gráfico de la empresa",
  "<p>El gráfico muestra una empresa precio-aceptante (P = 10) con sus curvas de costo marginal y costo medio.</p>",
  [TAP(SVG_PC, ["opt"], "Toca el punto donde la empresa maximiza su beneficio.", "Es donde la recta del precio corta al costo marginal (no al costo medio).")],
  ["La regla es \\(P=CMg\\): el cruce de la recta de precio con la curva CMg (Q ≈ 4,7).",
   "Los cruces con el CMe solo marcan dónde el beneficio sería cero; el mínimo del CMe (Q = 4) es donde lo corta el CMg. Como en Q* el precio está por encima del CMe, la empresa gana."],
  "El cruce de P con CMg", "P = CMg.", [["maxben"], ["compperf"]]))
M11.append(E("m11e7", 2, "¿Cerrar o seguir?",
  "<p>En el corto plazo, el precio bajó a S/ 6. El costo variable medio mínimo de la empresa es S/ 8 y tiene costos fijos. ¿Qué le conviene?</p>",
  [O(["Cerrar: con P menor que el CVMe mínimo, ni siquiera cubre los costos variables", "Seguir produciendo para cubrir el costo fijo", "Subir su precio a S/ 8", "Producir el doble", "Da igual"])],
  ["Si produce, cada unidad pierde costo variable además del fijo. Si cierra, solo pierde el costo fijo.",
   "Regla de corto plazo: cerrar si \\(P\\lt CVMe\\) mínimo. Subir el precio no es opción: es precio-aceptante."],
  "Cerrar", "Compara P con el CVMe mínimo.", [["cierre"], ["cierre"]]))
M11.append(E("m11e8", 2, "El largo plazo",
  "<p>Las empresas de un mercado de competencia perfecta ganan beneficios económicos. ¿Qué pasa a largo plazo?</p>",
  [O(["Entran empresas, el precio baja y el beneficio económico llega a cero (P = CMe mínimo)", "Los beneficios crecen para siempre", "Salen empresas y el precio sube", "El Estado fija el precio", "Las empresas se fusionan en un monopolio"])],
  ["Con libre entrada, los beneficios atraen nuevas empresas: la oferta del mercado aumenta y el precio baja.",
   "Se detiene cuando \\(P=CMe\\) mínimo: beneficio económico cero (las empresas siguen cubriendo su costo de oportunidad)."],
  "Beneficio económico cero", "Libre entrada.", [["cierre"], ["compperf"]]))
M11.append(E("m11e9", 1, "Beneficio con el rectángulo",
  "<p>Una empresa precio-aceptante vende 5 unidades a S/ 10 y su costo medio en esa cantidad es S/ 8.</p>",
  [NUM([{"l": "Beneficio", "a": 10, "u": "S/"}], "Calcula")],
  ["Beneficio = \\((P-CMe)\\cdot Q\\).", "\\((10-8)\\cdot5=10\\): el rectángulo de altura 2 y ancho 5."],
  "S/ 10", "(P − CMe)·Q.", [["maxben"], ["maxben"]]))
M11_tools = [{"w": "qmax", "t": "Busca el beneficio máximo", "p": "Mueve Q y mira cuándo IMg = CMg y cómo cambia el rectángulo de beneficio.",
              "o": {"presets": [["Competencia perfecta (P = 40)", {"mode": "pc", "P": 40, "F": 50, "c": 4, "d": 1, "qmax": 30, "q0": 6}],
                                ["Precio bajo (P = 15): pierde", {"mode": "pc", "P": 15, "F": 50, "c": 4, "d": 1, "qmax": 20, "q0": 3}]]}}]

# =====================================================================
# SEMANA 12 · Monopolio y competencia monopolística
# =====================================================================
a_, b_, c_ = 100, 2, 20
Qm = Fr(a_ - c_, 2 * b_); Pm = a_ - b_ * Qm; Qc = Fr(a_ - c_, b_)
assert (Qm, Pm, Qc) == (20, 60, 40)
pim = (Pm - c_) * Qm; dwl = Fr(1, 2) * (Pm - c_) * (Qc - Qm); ecm = Fr(1, 2) * (a_ - Pm) * Qm
assert (pim, dwl, ecm) == (800, 400, 400)
# segundo: P = 50 − Q, CT = 10Q + Q² → IMg = 50 − 2Q = 10 + 2Q → Q = 10
Q2 = Fr(40, 4); P2 = 50 - Q2; pi2 = P2 * Q2 - (10 * Q2 + Q2 ** 2); assert (Q2, P2, pi2) == (10, 40, 200)
g = G((0, 52), (0, 105))
g.line((0, 100), (50, 0), "curve", "D", at=(47, 6)); g.line((0, 100), (25, 0), "exe", "IMg", at=(24, 6)); g.line((0, 20), (52, 20), "bad", "CMg", at=(52, 20))
g.dash((20, 0), (20, 60)); g.dash((0, 60), (20, 60)); g.tick(x=20, lab="20"); g.tick(x=40, lab="40"); g.tick(y=60, lab="60"); g.tick(y=20, lab="20")
g.poly([(0, 100), (0, 60), (20, 60)], "ec"); g.poly([(0, 60), (20, 60), (20, 20), (0, 20)], "ben"); g.poly([(20, 60), (20, 20), (40, 20)], "dwl"); g.poly([(0, 20), (20, 20), (20, 0), (0, 0)], "ct")
SVG_MON = g.svg()
M12_teo = ADV + (
 "<p><b>Monopolio:</b> un solo vendedor de un producto sin sustitutos cercanos, protegido por <b>barreras de entrada</b>: legales (patentes, concesiones), control de un recurso clave o <b>economías de escala</b> tan grandes que una sola empresa produce más barato que varias (<b>monopolio natural</b>: el agua potable de una ciudad).</p>"
 "<p>El monopolista es <b>precio-decisor</b>, pero enfrenta toda la demanda: para vender una unidad más debe bajar el precio a <i>todas</i>. Por eso \\(IMg\\lt P\\). Con demanda lineal \\(P=a-bQ\\): \\(IMg=a-2bQ\\) (misma ordenada, doble pendiente).</p>"
 "<p><b>Receta:</b> (1) \\(IMg=CMg\\) da la cantidad; (2) el precio se lee en la <b>demanda</b>; (3) beneficio \\(=(P-CMe)\\cdot Q\\).</p>"
 "<p>Comparado con la competencia perfecta, el monopolio produce <b>menos</b> y cobra <b>más</b>. Las unidades que se dejan de producir (valen más de lo que cuestan) son la <b>pérdida irrecuperable de eficiencia</b>: el triángulo entre la demanda y el CMg. Por eso se regula (en el Perú, por ejemplo, Sunass fija las tarifas del agua) y se vigila la competencia (Indecopi).</p>"
 "<p><b>Competencia monopolística:</b> muchas empresas con productos <b>diferenciados</b> (bodegas, chifas, peluquerías) y libre entrada. Cada una tiene un poco de poder de precio (su demanda tiene pendiente), así que en el corto plazo se comporta como un pequeño monopolio. En el largo plazo entran competidores hasta que el <b>beneficio es cero</b> (\\(P=CMe\\)), pero con \\(P\\gt CMg\\) y algo de <b>exceso de capacidad</b>.</p>"
)
M12_form = ["Monopolio: \\(IMg\\lt P\\); lineal \\(IMg=a-2bQ\\)", "\\(IMg=CMg\\) → Q; el precio sale de la demanda",
            "Monopolio: menos Q y más P que la competencia", "Pérdida irrecuperable: triángulo entre D y CMg",
            "Monopolio natural: economías de escala → se regula", "Comp. monopolística: diferenciado + libre entrada → beneficio 0 a largo plazo"]
M12_lesson = lesson("El monopolista también iguala IMg y CMg, pero como su IMg está debajo de la demanda, produce menos y cobra más.",
  ["<b>IMg &lt; P</b> porque para vender una más baja el precio a todas.",
   "<b>Dos pasos:</b> la cantidad con IMg = CMg; el precio subiendo hasta la demanda (no hasta el IMg).",
   "<b>Pérdida irrecuperable:</b> el triángulo de unidades que la sociedad valora más que su costo y no se producen.",
   "<b>Competencia monopolística:</b> como la bodega de tu barrio: tiene clientes fieles (poder de precio), pero si gana mucho, abren otras."],
  "Monopolio: Q donde IMg = CMg, P en la demanda; produce menos y cobra más que la competencia; triángulo de pérdida irrecuperable. Competencia monopolística: diferenciación + libre entrada → beneficio cero a largo plazo.",
  "leer el precio del monopolista en la curva de IMg o en el CMg. El precio se lee en la demanda, a la cantidad elegida.")
M12 = []
M12.append(E("m12e1", 1, "Calentamiento: semana 11",
  "<p>En competencia perfecta, ¿dónde produce la empresa para maximizar su beneficio?</p>",
  [O(["Donde P = CMg", "Donde P = CMe", "Donde el CMe es mínimo", "Donde el ingreso total es máximo", "Donde CMg = 0"])],
  ["La regla general es IMg = CMg, y en competencia perfecta IMg = P.", "Hoy verás que el monopolista usa la misma regla, pero su IMg ya no es igual al precio."],
  "P = CMg", "IMg = P.", [["maxben"], ["monop"]]))
M12.append(E("m12e2", 2, "El monopolista con números",
  "<p>Un monopolista enfrenta la demanda \\(P=100-2Q\\) y tiene costo marginal constante \\(CMg=20\\) (sin costo fijo).</p>",
  [NUM([{"l": "Q del monopolio", "a": 20}, {"l": "P del monopolio", "a": 60, "u": "S/"}, {"l": "Beneficio", "a": 800, "u": "S/"}], "Monopolio"),
   NUM([{"l": "Q si fuera competencia perfecta", "a": 40}, {"l": "Pérdida irrecuperable", "a": 400, "u": "S/"}], "Comparación")],
  ["\\(IMg=100-4Q\\). Con \\(IMg=CMg\\): \\(100-4Q=20\\Rightarrow Q=20\\); en la demanda: \\(P=100-40=60\\).",
   "Beneficio \\(=(60-20)\\cdot20=800\\).",
   "En competencia: \\(P=CMg\\Rightarrow100-2Q=20\\Rightarrow Q=40\\). Pérdida irrecuperable = triángulo \\(\\frac12(60-20)(40-20)=400\\)."],
  "Q = 20, P = 60, π = 800; competencia Q = 40; pérdida 400", "IMg tiene el doble de pendiente.", [["monop"], ["monop"], ["dwl"]], chain=True))
M12.append(E("m12e3", 2, "Busca la Q del monopolista",
  "<p>Con la misma demanda \\(P=100-2Q\\) y \\(CMg=20\\), mueve Q hasta el beneficio máximo. Fíjate en el punto de la demanda (el precio).</p>",
  [{"t": "qmax", "p": "Mueve Q", "mode": "mon", "a": 100, "b": 2, "F": 0, "c": 20, "d": 0, "qmax": 50, "q0": 8, "ans": 20, "tol": 0.51, "e": "Busca donde el IMg (punteado) corta al CMg."}],
  ["La línea punteada es el IMg: está debajo de la demanda. Cuando IMg = CMg (Q = 20), el beneficio es máximo.",
   "El precio se lee en la demanda: 60. Si sigues hasta Q = 40 (donde D corta al CMg) el beneficio cae: el monopolista no llega ahí."],
  "Q = 20", "IMg = CMg.", [["monop"], ["monop"]]))
M12.append(E("m12e4", 2, "Toca la pérdida irrecuperable",
  "<p>Mismo monopolio: \\(D\\): \\(P=100-2Q\\), \\(CMg=20\\). El monopolista produce 20 y cobra 60.</p>",
  [TAP(SVG_MON, ["dwl"], "Toca el área de la pérdida irrecuperable de eficiencia.", "Es lo que se pierde por las unidades entre 20 y 40 que no se producen."),
   TAP(SVG_MON, ["ben"], "Ahora toca el beneficio del monopolista.")],
  ["Las unidades entre Q = 20 y Q = 40 valen más para los consumidores (demanda) de lo que cuestan (CMg) y no se producen: ese triángulo es la pérdida irrecuperable.",
   "El beneficio es el rectángulo entre el precio (60) y el costo (20), de ancho 20. Arriba queda el excedente del consumidor."],
  "El triángulo entre 20 y 40", "Busca las unidades que faltan.", [["dwl"], ["monop"]], chain=True))
M12.append(E("m12e5", 2, "Monopolio con costo creciente",
  "<p>Demanda \\(P=50-Q\\) y costo total \\(CT=10Q+Q^2\\).</p>",
  [NUM([{"l": "Q", "a": 10}, {"l": "P", "a": 40, "u": "S/"}, {"l": "Beneficio", "a": 200, "u": "S/"}], "Calcula")],
  ["\\(IMg=50-2Q\\) y \\(CMg=10+2Q\\). Igualando: \\(50-2Q=10+2Q\\Rightarrow Q=10\\).",
   "\\(P=50-10=40\\); \\(\\pi=40\\cdot10-(100+100)=200\\)."],
  "Q = 10, P = 40, π = 200", "Deriva CT para el CMg.", [["monop"], ["monop"]]))
M12.append(E("m12e6", 1, "¿Qué estructura es?",
  "<p>Clasifica cada mercado (pensando en el Perú).</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Competencia perfecta", "Competencia monopolística", "Oligopolio", "Monopolio"], "items": [
    {"x": "Limones en el mercado mayorista", "c": 0}, {"x": "Bodegas de un barrio", "c": 1}, {"x": "Chifas de una avenida", "c": 1},
    {"x": "Telefonía móvil", "c": 2}, {"x": "Agua potable de la ciudad", "c": 3, "e": "Una sola empresa con enormes economías de escala: monopolio natural (regulado)."},
    {"x": "Un medicamento con patente vigente", "c": 3, "e": "La patente es una barrera legal."}, {"x": "Peluquerías", "c": 1}]}],
  ["Muchos con producto igual → competencia perfecta; muchos con producto diferenciado → competencia monopolística.",
   "Pocos grandes que se vigilan entre sí → oligopolio (semana 13); uno solo con barreras → monopolio."],
  "Clasificación correcta", "¿Cuántos vendedores y qué tan distinto es el producto?", [["compmon"], ["monop"]]))
M12.append(E("m12e7", 1, "¿Por qué IMg < P?",
  "<p>¿Por qué el ingreso marginal del monopolista es menor que el precio?</p>",
  [O(["Para vender una unidad más debe bajar el precio de todas las que vende", "Porque el Estado le cobra impuestos", "Porque sus costos son altos", "Porque es precio-aceptante", "No es cierto: IMg = P"])],
  ["Si vende 10 a S/ 50 y para vender 11 debe bajar a S/ 48, gana 48 por la nueva unidad pero pierde S/ 2 en cada una de las 10 anteriores.",
   "IMg = 48 − 20 = 28 &lt; 48. En competencia perfecta no pasa porque el precio no depende de cuánto venda una empresa."],
  "Baja el precio a todas", "Piensa en la unidad 11.", [["monop"], ["monop"]]))
M12.append(E("m12e8", 2, "Monopolio natural",
  "<p>Una ciudad tiene una sola empresa de agua potable porque construir dos redes de tuberías sería carísimo. ¿Qué se suele hacer?</p>",
  [O(["Regularla: un organismo (Sunass en el Perú) fija tarifas para que no cobre como monopolista", "Obligar a que entren más empresas con otra red", "Dejarla cobrar lo que quiera", "Prohibirla", "Convertirla en competencia perfecta por ley"])],
  ["Es un monopolio natural: por las economías de escala, una sola red es lo más barato. Dividirla subiría los costos.",
   "Para evitar precios de monopolio y la pérdida irrecuperable, se regula la tarifa."],
  "Regular la tarifa", "Economías de escala.", [["monop"], ["dwl"]]))
M12.append(E("m12e9", 2, "Competencia monopolística a largo plazo",
  "<p>Las pollerías de un distrito ganan mucho este año. Si hay libre entrada, ¿qué pasa a largo plazo?</p>",
  [O(["Abren más pollerías, a cada una le quedan menos clientes y el beneficio económico llega a cero", "Las pollerías ganan cada vez más", "Se forma un monopolio", "El precio baja hasta el costo marginal", "Todas cierran"])],
  ["Los beneficios atraen nuevas pollerías: la demanda de cada una se reduce.", "Se detiene cuando P = CMe (beneficio cero). A diferencia de la competencia perfecta, P sigue siendo mayor que el CMg y queda capacidad ociosa."],
  "Beneficio cero, con P > CMg", "Libre entrada.", [["compmon"], ["compmon"]]))
M12_tools = [{"w": "qmax", "t": "Monopolio vs. competencia", "p": "Mueve Q: el monopolista se detiene donde IMg = CMg (Q = 20). En Q = 40 (donde la demanda corta al CMg) produciría la competencia.",
              "o": {"presets": [["Monopolio: P = 100 − 2Q, CMg = 20", {"mode": "mon", "a": 100, "b": 2, "F": 0, "c": 20, "d": 0, "qmax": 50, "q0": 8}],
                                ["P = 50 − Q, CT = 10Q + Q²", {"mode": "mon", "a": 50, "b": 1, "F": 0, "c": 10, "d": 1, "qmax": 30, "q0": 4}]]}}]

# =====================================================================
# SEMANA 13 · Oligopolio y teoría de juegos
# =====================================================================
PD = {"pn": ["Empresa A", "Empresa B"], "rows": ["Precio alto", "Precio bajo"], "cols": ["Precio alto", "Precio bajo"], "pay": [[[60, 60], [10, 80]], [[80, 10], [30, 30]]]}
CO = {"pn": ["Ana", "Beto"], "rows": ["Estándar A", "Estándar B"], "cols": ["Estándar A", "Estándar B"], "pay": [[[50, 50], [0, 0]], [[0, 0], [40, 40]]]}
PU = {"pn": ["Empresa A", "Empresa B"], "rows": ["Publicidad", "Sin publicidad"], "cols": ["Publicidad", "Sin publicidad"], "pay": [[[20, 30], [50, 20]], [[10, 40], [30, 45]]]}
def ne(pay):
    R, C = len(pay), len(pay[0]); out = []
    for i in range(R):
        for j in range(C):
            if pay[i][j][0] == max(pay[k][j][0] for k in range(R)) and pay[i][j][1] == max(pay[i][k][1] for k in range(C)): out.append((i, j))
    return out
assert ne(PD["pay"]) == [(1, 1)] and ne(CO["pay"]) == [(0, 0), (1, 1)] and ne(PU["pay"]) == [(0, 0)]
# cartel: P = 100 − Q, CMg = 0
assert (100 - 50) * 25 == 1250 and (100 - 60) * 35 == 1400 and (100 - 60) * 25 == 1000 and (100 - 70) * 35 == 1050
O13_teo = ADV + (
 "<p><b>Oligopolio:</b> pocas empresas grandes (telefonía móvil, cerveza, cemento) y barreras de entrada. Lo clave es la <b>interdependencia</b>: lo que le conviene a una depende de lo que haga la otra. Por eso se analiza con <b>teoría de juegos</b>.</p>"
 "<p><b>Cooperar o competir.</b> Si se ponen de acuerdo (<b>colusión</b> o <b>cartel</b>), pueden actuar como un monopolio y repartirse un beneficio grande. Pero cada una tiene incentivo a romper el acuerdo (bajar un poco su precio o producir más) para quedarse con más clientes. En el Perú los acuerdos de precios están prohibidos y los sanciona Indecopi.</p>"
 "<p><b>Matriz de pagos:</b> filas = estrategias del jugador 1, columnas = las del jugador 2; en cada casilla, (pago de 1, pago de 2).</p><ul>"
 "<li><b>Mejor respuesta:</b> lo mejor que puedo hacer dado lo que hace el otro (se subraya mi mejor pago en cada columna o fila).</li>"
 "<li><b>Estrategia dominante:</b> la que es mejor respuesta a todo lo que haga el otro.</li>"
 "<li><b>Equilibrio de Nash:</b> casilla donde ambos están en su mejor respuesta: nadie gana cambiando solo.</li></ul>"
 "<p><b>Dilema del prisionero:</b> ambos tienen una estrategia dominante (traicionar, bajar el precio) que los lleva a un resultado peor para los dos que si cooperaran. Es la misma lógica del polizón de la semana 10. Cuando el juego se <b>repite</b> muchas veces, la cooperación puede sostenerse con estrategias como <b>ojo por ojo</b> (coopero mientras tú cooperes).</p>"
)
O13_form = ["Oligopolio: pocas empresas, interdependencia", "Cartel: actuar como monopolio; inestable por el incentivo a romperlo",
            "Mejor respuesta: subraya tu mejor pago dado lo del otro", "Nash: ambos en su mejor respuesta", "Dominante: mejor respuesta a todo",
            "Dilema del prisionero: dominante → peor para ambos"]
O13_lesson = lesson("En un oligopolio cada empresa decide pensando en la otra; la tentación de traicionar el acuerdo hace que cooperar sea difícil.",
  ["<b>Matriz de pagos:</b> primer número para la fila, segundo para la columna.",
   "<b>Para hallar el equilibrio:</b> subraya las mejores respuestas de cada uno; la casilla con los dos subrayados es un equilibrio de Nash.",
   "<b>Dilema del prisionero:</b> lo racional para cada uno (precio bajo) deja a ambos peor que el acuerdo (precio alto).",
   "<b>Repetición:</b> si juegan muchas veces, castigar la traición (ojo por ojo) puede sostener la cooperación."],
  "Oligopolio = pocas empresas interdependientes. Nash = nadie quiere cambiar solo. En el dilema del prisionero la estrategia dominante lleva a un resultado peor para todos; por eso los carteles se rompen (y además son ilegales).",
  "creer que el equilibrio de Nash es el mejor resultado para los dos. En el dilema del prisionero es justamente el peor conjunto: solo es estable.")
O13 = []
O13.append(E("o13e1", 1, "Calentamiento: semana 12",
  "<p>¿Dónde lee el monopolista su precio?</p>",
  [O(["En la demanda, a la cantidad donde IMg = CMg", "En el IMg", "En el CMg", "Donde la demanda corta al CMg", "En el CMe mínimo"])],
  ["Primero la cantidad (IMg = CMg); luego sube hasta la demanda para ver cuánto pagan los consumidores por esa cantidad.", "Hoy: ¿qué pasa cuando no hay una empresa, sino pocas que se vigilan?"],
  "En la demanda", "Dos pasos.", [["monop"], ["oligop"]]))
O13.append(E("o13e2", 2, "Dilema del prisionero: precios",
  "<p>Dos empresas eligen precio alto o bajo. La tabla muestra sus beneficios (en miles de soles).</p>",
  [dict({"t": "nash", "p": "Parte 1: subraya las mejores respuestas", "step": "br"}, **PD),
   dict({"t": "nash", "p": "Parte 2: toca el equilibrio de Nash", "step": "ne"}, **PD),
   O(["Ambas ganarían más con precio alto (60 cada una), pero ninguna se fía de la otra", "El equilibrio es lo mejor para las dos", "A gana más que B en el equilibrio", "No hay equilibrio", "Les conviene precio alto a ambas como estrategia dominante"], "Parte 3: ¿por qué es un «dilema»?")],
  ["Si B pone precio alto, a A le conviene bajo (80 &gt; 60); si B pone bajo, también bajo (30 &gt; 10). Precio bajo es <b>dominante</b> para A, y lo mismo para B.",
   "Ambos eligen precio bajo: equilibrio de Nash (30, 30).",
   "Si cooperaran con precio alto ganarían 60 cada uno: el equilibrio es peor para ambos. Esa es la lógica de por qué los carteles son difíciles de sostener."],
  "Nash: (precio bajo, precio bajo) = (30, 30)", "Mira columna por columna.", [["nash"], ["nash"], ["cartel"]], chain=True))
O13.append(E("o13e3", 2, "¿Por qué los carteles se rompen?",
  "<p>Dos empresas acuerdan repartirse el mercado como un monopolio. ¿Por qué el acuerdo suele durar poco?</p>",
  [O(["Cada una gana más si rompe el acuerdo mientras la otra lo cumple", "Porque el monopolio da pérdidas", "Porque los consumidores lo exigen", "Porque cooperar es una estrategia dominante", "Porque sus costos suben"])],
  ["Si la otra respeta el precio alto, vender un poco más barato te lleva sus clientes: hay incentivo a traicionar.",
   "Como ambas lo saben, el acuerdo es inestable (además es ilegal: Indecopi sanciona la colusión)."],
  "Incentivo a traicionar", "Mira la matriz del ejercicio anterior.", [["cartel"], ["cartel"]]))
O13.append(E("o13e4", 3, "Cartel con números",
  "<p>Dos empresas venden un producto con demanda total \\(P=100-Q\\) y costo cero. Acuerdan producir 25 cada una (lo que haría un monopolista: Q = 50).</p>",
  [NUM([{"l": "Precio del acuerdo", "a": 50, "u": "S/"}, {"l": "Beneficio de cada una", "a": 1250, "u": "S/"}], "Parte 1: el acuerdo"),
   NUM([{"l": "Precio si A produce 35 y B 25", "a": 40, "u": "S/"}, {"l": "Beneficio de A", "a": 1400, "u": "S/"}, {"l": "Beneficio de B", "a": 1000, "u": "S/"}], "Parte 2: A rompe el acuerdo"),
   NUM([{"l": "Beneficio de cada una si ambas producen 35", "a": 1050, "u": "S/"}], "Parte 3: ambas rompen")],
  ["Acuerdo: Q = 50 → P = 50; cada una \\(50\\cdot25=1250\\).",
   "Si A produce 35: Q = 60 → P = 40. A gana \\(40\\cdot35=1400\\) (más que 1250) y B \\(40\\cdot25=1000\\).",
   "Si ambas traicionan: Q = 70 → P = 30 → \\(30\\cdot35=1050\\) cada una: peor que el acuerdo. Es un dilema del prisionero con números."],
  "1250; 1400 y 1000; 1050", "Suma las cantidades y usa la demanda.", [["cartel"], ["cartel"], ["nash"]], chain=True))
O13.append(E("o13e5", 2, "Dos equilibrios: coordinación",
  "<p>Ana y Beto deben elegir el mismo estándar de cargador para su negocio; si eligen distinto, nadie gana.</p>",
  [dict({"t": "nash", "p": "Toca todos los equilibrios de Nash", "step": "ne"}, **CO)],
  ["Si Beto elige A, a Ana le conviene A (50 &gt; 0); si Beto elige B, le conviene B (40 &gt; 0). Igual para Beto.",
   "Hay <b>dos</b> equilibrios: (A, A) y (B, B). Ninguno tiene estrategia dominante: lo importante es coordinarse."],
  "(A, A) y (B, B)", "Puede haber más de uno.", [["nash"], ["nash"]]))
O13.append(E("o13e6", 2, "Publicidad",
  "<p>Dos empresas deciden si hacen publicidad (beneficios en miles).</p>",
  [dict({"t": "nash", "p": "Parte 1: subraya las mejores respuestas", "step": "br"}, **PU),
   dict({"t": "nash", "p": "Parte 2: toca el equilibrio de Nash", "step": "ne"}, **PU),
   O(["Solo A tiene estrategia dominante (publicidad)", "Ambas tienen estrategia dominante", "Solo B tiene estrategia dominante", "Ninguna tiene", "Las dos: no hacer publicidad"], "Parte 3: estrategias dominantes")],
  ["A: si B hace publicidad, 20 &gt; 10; si no, 50 &gt; 30 → publicidad siempre (dominante).",
   "B: si A hace publicidad, le conviene publicidad (30 &gt; 20); si A no, le conviene no hacer (45 &gt; 40): no tiene dominante.",
   "B anticipa que A hará publicidad y responde con publicidad: equilibrio (Publicidad, Publicidad) = (20, 30)."],
  "Nash: (publicidad, publicidad); solo A tiene dominante", "Revisa cada columna y cada fila.", [["nash"], ["domin"], ["domin"]], chain=True))
O13.append(E("o13e7", 1, "Estrategia dominante",
  "<p>¿Qué es una estrategia dominante?</p>",
  [O(["La que es la mejor respuesta sin importar lo que haga el otro", "La que da el mayor pago posible de la tabla", "La que elige la empresa más grande", "La que hace ganar a ambos", "La del equilibrio de Nash siempre"])],
  ["Es mejor para mí en <b>cada</b> columna (o fila): no necesito adivinar al otro.", "Si ambos tienen una, ese par es el equilibrio de Nash; pero puede haber equilibrio sin estrategias dominantes (como en la coordinación)."],
  "Mejor respuesta a todo", "«Sin importar».", [["domin"], ["nash"]]))
O13.append(E("o13e8", 2, "Juegos que se repiten",
  "<p>Dos empresas compiten en precios todos los meses durante años. ¿Qué estrategia puede sostener la cooperación (precio alto)?</p>",
  [O(["Ojo por ojo: coopero este mes si tú cooperaste el anterior; si traicionas, te castigo", "Bajar siempre el precio", "Subir el precio sin mirar al otro", "Cambiar al azar cada mes", "Nunca castigar"])],
  ["En un juego que se repite, traicionar hoy trae castigo mañana: la ganancia de un mes se pierde en los siguientes.",
   "«Ojo por ojo» premia la cooperación y castiga la traición, y por eso puede sostener precios altos (y por eso las autoridades vigilan los mercados con pocas empresas)."],
  "Ojo por ojo", "Piensa en el futuro.", [["cartel"], ["oligop"]]))
O13.append(E("o13e9", 1, "Rasgos del oligopolio",
  "<p>Clasifica cada rasgo.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Oligopolio", "Competencia perfecta"], "items": [
    {"x": "Pocas empresas grandes", "c": 0}, {"x": "Muchas empresas pequeñas", "c": 1}, {"x": "Cada empresa mira lo que hacen las otras", "c": 0},
    {"x": "Nadie puede influir en el precio", "c": 1}, {"x": "Barreras de entrada importantes", "c": 0}, {"x": "Libre entrada y salida", "c": 1}]}],
  ["La interdependencia es lo que define al oligopolio: por eso se usa teoría de juegos.", "En competencia perfecta cada empresa es tan pequeña que no necesita pensar en las demás."],
  "Clasificación correcta", "¿Pocas o muchas?", [["oligop"], ["oligop"]]))
O13_tools = [{"w": "nash", "t": "Matriz de pagos", "p": "Elige un juego y toca «Mostrar mejores respuestas»: la casilla con borde verde es el equilibrio de Nash.",
              "o": {"presets": [["Dilema: precios", dict(PD, txt="Precio bajo es dominante para ambos: el equilibrio (30, 30) es peor que cooperar (60, 60).")],
                                ["Coordinación", dict(CO, txt="Dos equilibrios: lo importante es coordinarse.")],
                                ["Publicidad", dict(PU, txt="Solo A tiene estrategia dominante; B responde a lo que anticipa de A.")]]}}]

# =====================================================================
# Conceptos, bloques y simulacros
# =====================================================================
CONC = {
 "tipbien": {"n": "Tipos de bienes", "f": "¿Excluible? ¿Rival? → privado, club, común, público", "x": "Bien público: no rival y no excluible (alumbrado, defensa).", "home": "g10"},
 "polizon": {"n": "Problema del polizón", "f": "Usar sin pagar", "x": "Con bienes no excluibles cada uno espera que paguen los demás: el mercado produce de menos.", "home": "g10"},
 "costben": {"n": "Costo–beneficio", "f": "Proveer si Σ valoraciones ≥ costo", "x": "En un bien público se suman las valoraciones de todos.", "home": "g10"},
 "comunes": {"n": "Tragedia de los comunes", "f": "Rival + no excluible → sobreuso", "x": "Se corrige con cuotas, vedas, permisos o derechos de propiedad.", "home": "g10"},
 "maxben": {"n": "Maximización de beneficios", "f": "\\(IMg=CMg\\); \\(\\pi=(P-CMe)Q\\)", "x": "Producir mientras la próxima unidad sume más de lo que cuesta.", "home": "m11"},
 "compperf": {"n": "Competencia perfecta", "f": "Precio-aceptante: \\(IMg=P\\Rightarrow P=CMg\\)", "x": "Muchas empresas, producto homogéneo, libre entrada.", "home": "m11"},
 "cierre": {"n": "Cierre y largo plazo", "f": "Cerrar si \\(P\\lt CVMe\\) mín. · largo plazo \\(P=CMe\\) mín.", "x": "Con libre entrada el beneficio económico tiende a cero.", "home": "m11"},
 "monop": {"n": "Monopolio", "f": "\\(IMg\\lt P\\); \\(IMg=CMg\\), P en la demanda", "x": "Produce menos y cobra más que la competencia; barreras de entrada.", "home": "m12"},
 "dwl": {"n": "Pérdida irrecuperable", "f": "Triángulo entre D y CMg", "x": "Unidades que valen más de lo que cuestan y no se producen.", "home": "m12"},
 "compmon": {"n": "Competencia monopolística", "f": "Diferenciación + libre entrada", "x": "Poder de precio a corto plazo; beneficio cero a largo plazo, con P > CMg.", "home": "m12"},
 "oligop": {"n": "Oligopolio", "f": "Pocas empresas interdependientes", "x": "Se analiza con teoría de juegos.", "home": "o13"},
 "nash": {"n": "Equilibrio de Nash", "f": "Ambos en su mejor respuesta", "x": "Nadie gana cambiando solo; puede no ser el mejor resultado conjunto.", "home": "o13"},
 "domin": {"n": "Estrategia dominante", "f": "Mejor respuesta a todo", "x": "No hace falta adivinar al otro.", "home": "o13"},
 "cartel": {"n": "Cartel y dilema del prisionero", "f": "Cooperar conviene a ambos, traicionar a cada uno", "x": "Por eso los carteles son inestables; repetir el juego puede sostener la cooperación.", "home": "o13"},
}
NEW = [
 {"id": "g10", "name": "Sem. 10 · 📖 Bienes públicos y el problema del polizón", "teo": G10_teo, "form": G10_form, "lesson": G10_lesson, "ex": G10, "tools": G10_tools},
 {"id": "m11", "name": "Sem. 11 · 📖 Maximización de beneficios y competencia perfecta", "teo": M11_teo, "form": M11_form, "lesson": M11_lesson, "ex": M11, "tools": M11_tools},
 {"id": "m12", "name": "Sem. 12 · 📖 Monopolio y competencia monopolística", "teo": M12_teo, "form": M12_form, "lesson": M12_lesson, "ex": M12, "tools": M12_tools},
 {"id": "o13", "name": "Sem. 13 · 📖 Oligopolio y teoría de juegos", "teo": O13_teo, "form": O13_form, "lesson": O13_lesson, "ex": O13, "tools": O13_tools}]
NEWIDS = {t["id"] for t in NEW}
CARDS = ('<div><b>Tipos de bienes</b><br>¿excluible? ¿rival? · público: no y no → polizón</div>'
         '<div><b>Costo–beneficio</b><br>proveer si Σ valoraciones ≥ costo</div>'
         '<div><b>Máximo beneficio</b><br>\\(IMg=CMg\\) · \\(\\pi=(P-CMe)Q\\)</div>'
         '<div><b>Competencia perfecta</b><br>\\(P=CMg\\) · largo plazo beneficio 0</div>'
         '<div><b>Monopolio</b><br>\\(IMg=a-2bQ\\) · Q con IMg = CMg, P en la demanda · pérdida irrecuperable</div>'
         '<div><b>Comp. monopolística</b><br>diferenciado + libre entrada → beneficio 0, P &gt; CMg</div>'
         '<div><b>Teoría de juegos</b><br>subraya mejores respuestas → Nash · dominante · dilema del prisionero</div>')

ef = json.load(open(P("micro-ef"), encoding="utf-8"))
used = lambda ts: {k for t in ts for e in t["ex"] for l in e["tags"] for k in l}

ef["topics"] = [t for t in ef["topics"] if t["id"] not in NEWIDS] + NEW
ef["concepts"].update(CONC)
if "Tipos de bienes</b>" not in ef["form"]:
    j = ef["form"].rindex("</div>"); ef["form"] = ef["form"][:j] + CARDS + ef["form"][j:]
ef["intro"] = ("Repaso acumulado con todos los temas abiertos: primero los 4 bloques del parcial, luego <b>la semana 9: externalidades</b> y las semanas 10 a 13: "
               "bienes públicos, maximización de beneficios y competencia perfecta, monopolio y competencia monopolística, y oligopolio con teoría de juegos. "
               "<b>📖 Las semanas 10 a 13 están adelantadas según el sílabo</b> (el profesor aún no sube esas clases): se hicieron con su bibliografía y se ajustarán cuando llegue su material. "
               "Hay juego del polizón, buscador del beneficio máximo y matriz de pagos interactiva. Se actualiza cada semana.")
ef["sim"]["slots"] = [
 {"pts": 2, "name": "Repaso parcial: conceptos y mercado", "pool": ["mis5", "mis4", "mb1", "me10", "mis6", "me9", "me12"]},
 {"pts": 2, "name": "Repaso parcial: producción y costos", "pool": ["mp10", "mis7", "mk9", "mis8", "mk8"]},
 {"pts": 3, "name": "Sem. 9: externalidades", "pool": ["xg3", "xg4", "xg5", "xs2", "xs4", "xg9", "xp4", "xp5"]},
 {"pts": 3, "name": "Sem. 10: bienes públicos", "pool": ["g10e2", "g10e5", "g10e6", "g10e7", "g10e9"]},
 {"pts": 3, "name": "Sem. 11: maximización y competencia perfecta", "pool": ["m11e3", "m11e4", "m11e5", "m11e6", "m11e7"]},
 {"pts": 4, "name": "Sem. 12: monopolio y competencia monopolística", "pool": ["m12e2", "m12e3", "m12e4", "m12e5", "m12e9"]},
 {"pts": 3, "name": "Sem. 13: oligopolio y teoría de juegos", "pool": ["o13e2", "o13e4", "o13e5", "o13e6"]}]

pc2 = {k: ef[k] for k in ("formSim", "code", "name", "guide")}
pc2.update({"id": "micro-pc2", "exam": "Práctica Calificada 2 (semana 14)", "short": "PC2", "sub": "Sem. 9 a 13",
            "intro": ("Bloque de la <b>Práctica Calificada 2</b> (semana 14, 20 % de la nota): externalidades (semana 9) y las semanas 10 a 13. "
                      "<b>📖 Las semanas 10 a 13 están adelantadas según el sílabo</b>, porque el profesor aún no sube esas clases: se armaron con la bibliografía del curso (Krugman y Pindyck) y se ajustarán cuando llegue su material. "
                      "Cada tema empieza con un calentamiento de la semana anterior para que no se te olvide. Hay juego del polizón, buscador del beneficio máximo y matriz de pagos interactiva.")})
# hoja de repaso del PC2: tarjetas de externalidades + nuevas
fg = ef["form"]; k0 = fg.index("<div><b>Externalidad</b>"); k1 = fg.index("<div><b>Tipos de bienes</b>")
pc2["form"] = '<p class="note">Hoja de repaso de la PC2: semana 9 y las semanas 10 a 13 (adelantadas según el sílabo).</p><div class="fgrid">' + fg[k0:k1] + CARDS + "</div>"
pc2["topics"] = [t for t in ef["topics"] if t["id"].startswith("x9")] + NEW
pc2["figs"] = ef.get("figs", {})
pc2["simEx"] = [e for e in ef["simEx"] if e["id"].startswith("xs")]
uu = used(pc2["topics"]) | {k for e in pc2["simEx"] for l in e["tags"] for k in l}
pc2["concepts"] = {k: v for k, v in ef["concepts"].items() if k in uu}
pc2["sim"] = {"minutes": 90, "intro": "Simulacro de la PC2: 90 minutos y 20 puntos, una pregunta por semana (9 a 13). Las semanas 10 a 13 están adelantadas según el sílabo.", "slots": [
 {"pts": 4, "name": "Sem. 9: externalidades", "pool": ["xg3", "xg4", "xg5", "xs2", "xp4", "xp5"]},
 {"pts": 4, "name": "Sem. 10: bienes públicos", "pool": ["g10e2", "g10e5", "g10e6", "g10e7", "g10e9"]},
 {"pts": 4, "name": "Sem. 11: maximización y competencia perfecta", "pool": ["m11e3", "m11e4", "m11e5", "m11e6", "m11e9"]},
 {"pts": 4, "name": "Sem. 12: monopolio y competencia monopolística", "pool": ["m12e2", "m12e3", "m12e4", "m12e5"]},
 {"pts": 4, "name": "Sem. 13: oligopolio y teoría de juegos", "pool": ["o13e2", "o13e4", "o13e5", "o13e6"]}]}

for d in (ef, pc2):
    ids = [e["id"] for t in d["topics"] for e in t["ex"]] + [e["id"] for e in d.get("simEx", [])]
    assert len(ids) == len(set(ids)), d["id"]
    assert sum(s["pts"] for s in d["sim"]["slots"]) == 20
    for s in d["sim"]["slots"]:
        for i in s["pool"]: assert i in ids, (d["id"], i)
    for t in d["topics"]:
        for e in t["ex"]:
            for l in e["tags"]:
                for k in l: assert k in d["concepts"], (d["id"], e["id"], k)

for name, d in (("micro-ef", ef), ("micro-pc2", pc2)):
    with open(P(name), "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False); f.write("\n")
ix = json.load(open(P("indice"), encoding="utf-8"))
if "micro-pc2" not in ix["cursos"]:
    ix["cursos"].insert(ix["cursos"].index("micro-ep") + 1, "micro-pc2")
    with open(P("indice"), "w", encoding="utf-8") as f:
        json.dump(ix, f, indent=1, ensure_ascii=False); f.write("\n")
print("ok", [len(t["ex"]) for t in NEW])
