#!/usr/bin/env python3
"""Microeconomía Aplicada · semana 15 (economía del bienestar), ADELANTADA SEGÚN EL SÍLABO.
Ejecuta primero tools/micro_s10_13.py (reconstruye micro-pc2 y micro-ef) y luego agrega el tema b15 solo a micro-ef
(la semana 15 va después de la PC2) y rehace su simulacro. Verifica las cuentas con sympy.
Uso: python3 tools/micro_s15.py   (reejecutable)."""
import json, os, runpy
import sympy as sp

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = runpy.run_path(os.path.join(RAIZ, "tools", "micro_s10_13.py"))
E, O, NUM, lesson, G, TAP, ADV, P = M["E"], M["O"], M["NUM"], M["lesson"], M["G"], M["TAP"], M["ADV"], M["P"]

# ------------------------------------------------------------- cuentas (mercado base: D P = 100 − 2Q, O P = 10 + Q)
q = sp.symbols("q", nonnegative=True)
a, b, c, d = 100, 2, 10, 1
D = lambda x: a - b * x
S = lambda x: c + d * x
Qe = sp.solve(sp.Eq(D(q), S(q)), q)[0]; Pe = D(Qe)
assert (Qe, Pe) == (30, 40)
def surplus(Q, Pb, Ps):
    ec = sp.integrate(D(q) - Pb, (q, 0, Q)); ep = sp.integrate(Ps - S(q), (q, 0, Q)); rec = (Pb - Ps) * Q
    pi = sp.integrate(D(q) - S(q), (q, Q, Qe)); return ec, ep, rec, pi
W0 = sp.integrate(D(q) - S(q), (q, 0, Qe))
assert surplus(Qe, Pe, Pe)[:2] == (900, 450) and W0 == 1350
# impuesto t = 15
Qt = sp.solve(sp.Eq(D(q), S(q) + 15), q)[0]; Pc = D(Qt); Pv = Pc - 15
assert (Qt, Pc, Pv) == (25, 50, 35)
assert surplus(Qt, Pc, Pv) == (625, sp.Rational(625, 2), 375, sp.Rational(75, 2))
# precio máximo 30
Qmax = sp.solve(sp.Eq(S(q), 30), q)[0]; Qdmax = sp.solve(sp.Eq(D(q), 30), q)[0]
assert (Qmax, Qdmax) == (20, 35) and surplus(Qmax, 30, 30) == (1000, 200, 0, 150)
# precio mínimo 50
Qmin = sp.solve(sp.Eq(D(q), 50), q)[0]; Qsmin = sp.solve(sp.Eq(S(q), 50), q)[0]
assert (Qmin, Qsmin) == (25, 40) and surplus(Qmin, 50, 50) == (625, sp.Rational(1375, 2), 0, sp.Rational(75, 2))
for k in (surplus(Qt, Pc, Pv), surplus(Qmax, 30, 30), surplus(Qmin, 50, 50)): assert sum(k) == W0
# feria de chocotejas (herramienta feria)
BU = [10, 9, 8, 7, 5, 4, 3, 2]; SE = [2, 3, 4, 5, 7, 8, 9, 10]
def feria(p):
    wb = [x for x in BU if x >= p]; ws = [x for x in SE if x <= p]; n = min(len(wb), len(ws))
    return n, sum(x - p for x in wb[:n]), sum(p - x for x in ws[:n])
MAXW = sum(x - y for x, y in zip(BU, SE) if x >= y)
assert MAXW == 20 and feria(6) == (4, 10, 10) and feria(4) == (3, 15, 3)
# calentamiento con valoraciones sueltas
assert (10 - 6) + (8 - 6) + (7 - 6) == 7 and (6 - 3) + (6 - 5) == 4

# ------------------------------------------------------------- gráficos tocables
def g_base():
    g = G((0, 40), (0, 105), H=300)
    g.line((0, 100), (40, 20), "curve", "D"); g.line((0, 10), (40, 50), "bad", "O", at=(39, 51))
    return g
g3 = g_base()
g3.poly([(0, 100), (0, 40), (30, 40)], "A"); g3.poly([(0, 40), (30, 40), (0, 10)], "B"); g3.poly([(30, 40), (40, 50), (40, 20)], "C")
g3.line((0, 100), (40, 20), "curve"); g3.line((0, 10), (40, 50), "bad")
g3.dash((0, 40), (30, 40)); g3.dash((30, 40), (30, 0)); g3.tick(y=40, lab="40"); g3.tick(x=30, lab="30")
for p_, t_ in (((8, 58), "A"), ((8, 29), "B"), ((37, 36), "C")): g3.text(p_, t_, "dl")
SVG3 = g3.svg()
g4 = g_base()
g4.poly([(0, 100), (0, 50), (25, 50)], "1"); g4.poly([(0, 50), (25, 50), (25, 40), (0, 40)], "2")
g4.poly([(25, 50), (30, 40), (25, 40)], "3"); g4.poly([(0, 40), (25, 40), (25, 35), (0, 35)], "4")
g4.poly([(25, 40), (30, 40), (25, 35)], "5"); g4.poly([(0, 35), (25, 35), (0, 10)], "6")
g4.line((0, 100), (40, 20), "curve"); g4.line((0, 10), (40, 50), "bad")
g4.dash((0, 50), (25, 50)); g4.dash((0, 40), (30, 40)); g4.dash((0, 35), (25, 35)); g4.dash((25, 50), (25, 0))
g4.tick(y=50, lab="50"); g4.tick(y=40, lab="40"); g4.tick(y=35, lab="35"); g4.tick(x=25, lab="25"); g4.tick(x=30, lab="30")
for p_, t_ in (((6, 62), "1"), ((10, 47), "2"), ((26.6, 42.3), "3"), ((10, 39.3), "4"), ((26.6, 37.0), "5"), ((6, 24), "6")): g4.text(p_, t_, "dl")
SVG4 = g4.svg()

# ------------------------------------------------------------- teoría
B15_teo = ADV + (
 "<p>Hasta ahora viste <b>cuánto</b> se produce y a qué precio. Esta semana la pregunta es otra: <b>¿qué tan bien le va a la sociedad</b> con ese resultado?</p>"
 "<h3>Excedente del consumidor (EC)</h3>"
 "<p>Cada comprador tiene una <b>disposición a pagar</b>: lo máximo que pagaría. Si Ana pagaría S/ 10 por una chocoteja y la compra a S/ 6, gana S/ 4. "
 "Esa diferencia es su excedente. Sumando a todos, el EC es el <b>área bajo la demanda y sobre el precio</b>.</p>"
 "<h3>Excedente del productor (EP)</h3>"
 "<p>Cada vendedor tiene un <b>costo</b>: lo mínimo que aceptaría. Si a un puesto le cuesta S/ 2 hacerla y la vende a S/ 6, gana S/ 4. "
 "El EP es el <b>área sobre la oferta y bajo el precio</b>.</p>"
 "<p>Con demanda y oferta lineales son triángulos: \\(EC=\\tfrac12\\,Q\\,(P_{máx}-P)\\) y \\(EP=\\tfrac12\\,Q\\,(P-P_{mín})\\), "
 "donde \\(P_{máx}\\) y \\(P_{mín}\\) son los cortes de la demanda y la oferta con el eje del precio.</p>"
 "<h3>Bienestar y eficiencia</h3>"
 "<p><b>Bienestar total = EC + EP</b> (más la recaudación del Estado, si hay impuesto). En el <b>equilibrio competitivo</b> el bienestar es el máximo posible: "
 "se hacen todos los intercambios en que alguien valora el bien más de lo que cuesta producirlo, y ninguno más. Eso es ser <b>eficiente</b>.</p>"
 "<h3>¿Qué rompe la eficiencia?</h3><ul>"
 "<li><b>Impuesto por unidad:</b> el comprador paga más, el vendedor recibe menos y se vende menos. Parte del excedente pasa al Estado (recaudación) y otra parte se pierde: la <b>pérdida irrecuperable</b>.</li>"
 "<li><b>Precio máximo</b> (por debajo del equilibrio): se ofrece menos, hay <b>escasez</b>. Los que sí compran ganan, los productores pierden y se pierden intercambios.</li>"
 "<li><b>Precio mínimo</b> (por encima del equilibrio): se compra menos, <b>sobra</b> producto. Los productores que venden ganan, los consumidores pierden.</li>"
 "<li><b>Monopolio</b> (semana 12): produce menos para cobrar más → pérdida irrecuperable.</li>"
 "<li><b>Externalidades</b> (semana 9): el mercado no cuenta el costo para terceros, así que el equilibrio ya no es eficiente.</li></ul>"
 "<p>Un precio máximo o mínimo que está del lado «equivocado» del equilibrio (tope por encima, piso por debajo) <b>no es efectivo</b>: no cambia nada.</p>")
B15_form = ["EC: área bajo D y sobre P · \\(\\tfrac12 Q(P_{máx}-P)\\)", "EP: área sobre O y bajo P · \\(\\tfrac12 Q(P-P_{mín})\\)",
            "Eficiencia: equilibrio competitivo → EC + EP máximo", "Impuesto t: \\(P_c-P_v=t\\) · recaudación \\(t\\cdot Q\\) · triángulo perdido",
            "Precio máximo debajo del equilibrio → escasez", "Precio mínimo encima del equilibrio → sobra"]
B15_lesson = lesson(
  "El excedente mide cuánto gana cada lado al intercambiar, y el mercado competitivo hace la «torta» lo más grande posible.",
  ["<b>EC:</b> lo que el comprador estaba dispuesto a pagar menos lo que pagó. En el gráfico: entre la demanda y el precio.",
   "<b>EP:</b> lo que cobra el vendedor menos su costo. En el gráfico: entre el precio y la oferta.",
   "<b>Eficiencia:</b> en el equilibrio se hacen justo los intercambios que valen la pena; ni uno más, ni uno menos.",
   "<b>Pérdida irrecuperable:</b> el triángulo de intercambios que valían la pena y ya no se hacen (por un impuesto, un tope, un piso o un monopolio)."],
  "EC + EP = bienestar. El equilibrio competitivo lo maximiza. Impuesto: una parte va al Estado y un triángulo se pierde. Tope bajo → escasez; piso alto → sobra. En los dos casos se pierde un triángulo.",
  "pensar que un precio máximo siempre ayuda a los consumidores. Los que consiguen comprar ganan, pero otros se quedan sin el producto, y la sociedad pierde el triángulo de intercambios que ya no ocurren.")

# ------------------------------------------------------------- ejercicios
B15 = []
B15.append(E("b15e1", 1, "Calentamiento: semana 13",
  "<p>Dos empresas de cemento forman un cartel y suben el precio. ¿Qué les pasa a los consumidores?</p>",
  [O(["Pagan más y compran menos: pierden excedente", "No les pasa nada: el precio lo deciden las empresas", "Ganan, porque el producto es de más calidad", "Compran más, porque hay menos competencia", "Pierden solo si el cartel se rompe"])],
  ["Un cartel actúa como un monopolio: menos cantidad y precio más alto (semana 13).",
   "Hoy verás cómo medir esa pérdida: el excedente del consumidor baja y aparece una pérdida irrecuperable."],
  "Pagan más y compran menos", "Piensa en el monopolio.", [["cartel"], ["exccons"]]))
B15.append(E("b15e2", 1, "¿Cuánto gana cada uno?",
  "<p>Tres compradores valoran una chocoteja en S/ 10, S/ 8 y S/ 7, y la compran a S/ 6. Dos puestos la venden a S/ 6; producirla les cuesta S/ 3 y S/ 5.</p>",
  [NUM([{"l": "Excedente del que la valora en S/ 10", "a": 4, "u": "S/"}, {"l": "EC de los tres", "a": 7, "u": "S/"}, {"l": "EP de los dos puestos", "a": 4, "u": "S/"}], "Calcula")],
  ["Cada comprador gana su valoración menos el precio: 10 − 6 = 4, 8 − 6 = 2 y 7 − 6 = 1. EC = 4 + 2 + 1 = S/ 7.",
   "Cada puesto gana el precio menos su costo: 6 − 3 = 3 y 6 − 5 = 1. EP = S/ 4."],
  "4, 7 y 4", "Valoración − precio; precio − costo.", [["exccons"], ["excprod"]]))
B15.append(E("b15e3", 1, "Toca el excedente",
  "<p>El gráfico muestra un mercado en equilibrio (P = 40, Q = 30).</p>",
  [TAP(SVG3, ["A"], "Parte 1: toca el excedente del consumidor", "El EC está entre la demanda y el precio, a la izquierda de Q."),
   TAP(SVG3, ["B"], "Parte 2: toca el excedente del productor", "El EP está entre el precio y la oferta.")],
  ["A: entre la demanda (lo que pagarían) y el precio (lo que pagan) → excedente del consumidor.",
   "B: entre el precio y la oferta (su costo) → excedente del productor. C no es excedente: ahí producir cuesta más de lo que vale para los compradores."],
  "A y B", "Arriba del precio: consumidores.", [["exccons"], ["excprod"]], chain=True))
B15.append(E("b15e4", 2, "Toca las áreas con impuesto",
  "<p>En el mercado del gráfico se pone un impuesto de S/ 15 por unidad. La cantidad baja de 30 a 25; el comprador paga S/ 50 y el vendedor recibe S/ 35.</p>",
  [TAP(SVG4, ["1"], "Parte 1: toca el excedente del consumidor con impuesto"),
   TAP(SVG4, ["2", "4"], "Parte 2: toca la recaudación del Estado (puede ser más de una zona)", "La recaudación es t × Q: el rectángulo entre 50 y 35 hasta Q = 25.", multi=True),
   TAP(SVG4, ["3", "5"], "Parte 3: toca la pérdida irrecuperable", "Son las unidades entre 25 y 30 que ya no se venden.", multi=True)],
  ["Con impuesto el EC queda sobre el precio que paga el comprador (50): solo la zona 1.",
   "Recaudación = 15 × 25 = S/ 375: los rectángulos 2 (lo pone el comprador) y 4 (lo pone el vendedor).",
   "3 + 5: unidades entre 25 y 30 que se valoraban más que su costo y ya no se venden. No lo gana nadie: es la pérdida irrecuperable."],
  "1 · 2 + 4 · 3 + 5", "Ubica los dos precios: 50 y 35.", [["exccons"], ["impexc"], ["dwl"]], chain=True))
B15.append(E("b15e5", 2, "El balón de gas, paso a paso",
  "<p>Imagina el mercado de balones de gas de un distrito (miles de balones al mes): demanda \\(P=100-2Q\\) y oferta \\(P=10+Q\\), en soles.</p>",
  [NUM([{"l": "Q de equilibrio", "a": 30}, {"l": "P de equilibrio", "a": 40, "u": "S/"}], "Parte 1: equilibrio"),
   NUM([{"l": "EC", "a": 900, "u": "S/"}, {"l": "EP", "a": 450, "u": "S/"}, {"l": "Bienestar total", "a": 1350, "u": "S/"}], "Parte 2: excedentes (miles de soles)"),
   NUM([{"l": "Q con impuesto", "a": 25}, {"l": "Recaudación", "a": 375, "u": "S/"}, {"l": "Pérdida irrecuperable", "a": 37.5, "u": "S/", "tol": 0.06}], "Parte 3: impuesto de S/ 15 por balón")],
  ["Igualando: \\(100-2Q=10+Q\\Rightarrow Q=30\\), \\(P=40\\).",
   "\\(EC=\\tfrac12\\cdot30\\cdot(100-40)=900\\) · \\(EP=\\tfrac12\\cdot30\\cdot(40-10)=450\\) · total 1350.",
   "Con impuesto la oferta sube 15: \\(100-2Q=25+Q\\Rightarrow Q=25\\); paga 50, recibe 35. Recaudación \\(15\\cdot25=375\\); pérdida \\(\\tfrac12\\cdot(30-25)\\cdot15=37{,}5\\). "
   "Chequeo: EC 625 + EP 312,5 + 375 + 37,5 = 1350."],
  "30 y 40 · 900, 450, 1350 · 25, 375, 37,5", "Triángulos: ½ · base · altura.", [["exccons"], ["exccons", "excprod"], ["impexc"]], chain=True))
B15.append(E("b15e6", 2, "Precio tope al balón",
  "<p>En el mismo mercado (\\(P=100-2Q\\), \\(P=10+Q\\)) imagina que se fija un <b>precio máximo de S/ 30</b>.</p>",
  [NUM([{"l": "Q ofrecida", "a": 20}, {"l": "Q demandada", "a": 35}, {"l": "Escasez", "a": 15}], "Parte 1: cantidades"),
   NUM([{"l": "EC", "a": 1000, "u": "S/"}, {"l": "EP", "a": 200, "u": "S/"}, {"l": "Pérdida irrecuperable", "a": 150, "u": "S/"}], "Parte 2: excedentes"),
   O(["Los consumidores que consiguen balón ganan, los productores pierden y la sociedad pierde S/ 150", "Todos ganan, porque el gas es más barato", "Solo pierden los productores; la sociedad no pierde nada",
      "Los consumidores pierden todo su excedente", "No cambia nada, porque el tope es menor que el equilibrio"], "Parte 3: ¿quién gana y quién pierde?")],
  ["Los productores ofrecen hasta donde \\(10+Q=30\\): \\(Q=20\\). Los consumidores quieren \\(100-2Q=30\\): \\(Q=35\\). Faltan 15.",
   "Solo se venden 20. EC: el área entre la demanda y 30 hasta Q = 20, un trapecio de \\(\\tfrac{(70+30)}{2}\\cdot20=1000\\). EP: \\(\\tfrac12\\cdot20\\cdot(30-10)=200\\). "
   "Pérdida: \\(\\tfrac12\\cdot(30-20)\\cdot(60-30)=150\\). Chequeo: 1000 + 200 + 150 = 1350.",
   "El EC sube de 900 a 1000 (para quien consigue balón), el EP cae de 450 a 200 y se pierden 150. Además, 15 mil familias se quedan sin balón."],
  "Escasez 15 · 1000, 200, 150", "Con tope, manda la oferta.", [["intervp"], ["exccons", "excprod", "dwl"], ["intervp"]], chain=True))
B15.append(E("b15e7", 2, "¿De quién es cada área?",
  "<p>Clasifica cada área según quién se la queda.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Consumidores", "Productores", "Estado", "Nadie (se pierde)"], "items": [
    {"x": "El área bajo la demanda y sobre el precio", "c": 0},
    {"x": "El área sobre la oferta y bajo el precio", "c": 1},
    {"x": "Impuesto por unidad × cantidad vendida", "c": 2},
    {"x": "El triángulo de unidades que dejan de venderse por un impuesto", "c": 3},
    {"x": "Con un precio máximo, el ahorro de quienes sí consiguen comprar", "c": 0},
    {"x": "Con un precio mínimo, lo que cobran de más los que sí venden", "c": 1},
    {"x": "Lo que la sociedad deja de ganar porque un monopolio produce menos", "c": 3, "e": "Es la pérdida irrecuperable del monopolio (semana 12)."},
    {"x": "Lo que gana el monopolista por cobrar más que en competencia", "c": 1, "e": "Ese rectángulo pasa del consumidor al productor."}]}],
  ["El EC es de los consumidores y el EP de los productores; con impuesto aparece la recaudación (Estado).",
   "La pérdida irrecuperable no la gana nadie: son intercambios que ya no ocurren, por impuestos, topes, pisos o monopolio."],
  "Clasificación correcta", "¿Alguien se lo queda?", [["exccons", "excprod"], ["dwl"]]))
B15.append(E("b15e8", 1, "¿Por qué es eficiente?",
  "<p>¿Por qué se dice que el equilibrio de un mercado competitivo es <b>eficiente</b>?</p>",
  [O(["Porque maximiza EC + EP: se hacen todos los intercambios que valen más de lo que cuestan, y ninguno más",
      "Porque el precio es el más bajo posible", "Porque los consumidores tienen el máximo excedente posible", "Porque todas las empresas ganan lo mismo", "Porque no hay impuestos"])],
  ["A la izquierda del equilibrio, cada unidad vale para algún comprador más de lo que cuesta: conviene producirla.",
   "A la derecha, cuesta más de lo que vale. El equilibrio deja justo las que suman: el bienestar total es el máximo. No significa que el precio sea el más bajo ni que el reparto sea «justo»."],
  "Maximiza EC + EP", "Compara valor y costo de cada unidad.", [["eficien"], ["eficien"]]))
B15.append(E("b15e9", 2, "Precio mínimo a la papa",
  "<p>En el mercado \\(P=100-2Q\\), \\(P=10+Q\\) imagina que se fija un <b>precio mínimo de S/ 50</b> para apoyar a los productores.</p>",
  [NUM([{"l": "Q que se compra", "a": 25}, {"l": "Q que se ofrece", "a": 40}, {"l": "Excedente de oferta (sobra)", "a": 15}], "Parte 1: cantidades"),
   NUM([{"l": "EC", "a": 625, "u": "S/"}, {"l": "Pérdida irrecuperable", "a": 37.5, "u": "S/", "tol": 0.06}], "Parte 2: excedentes"),
   O(["Los consumidores pierden; los productores que venden ganan, pero sobran 15 y se pierde bienestar", "Ganan todos los productores, incluso los que no venden",
      "No hay pérdida, porque el dinero se queda en el país", "Los consumidores ganan, porque hay más producto", "No es efectivo"], "Parte 3: balance")],
  ["Los consumidores compran donde \\(100-2Q=50\\): \\(Q=25\\). Los productores querrían vender donde \\(10+Q=50\\): \\(Q=40\\). Sobran 15.",
   "Se venden 25. \\(EC=\\tfrac12\\cdot25\\cdot(100-50)=625\\) (antes 900). EP = 687,5 (antes 450). Pérdida \\(\\tfrac12\\cdot(30-25)\\cdot(50-35)=37{,}5\\).",
   "Los consumidores pierden 275; los productores que logran vender ganan, pero el producto que sobra nadie lo compra. Chequeo: 625 + 687,5 + 37,5 = 1350."],
  "Compran 25, sobran 15 · 625 y 37,5", "Con piso, manda la demanda.", [["intervp"], ["exccons", "dwl"], ["intervp"]], chain=True))
B15.append(E("b15e10", 2, "Eficiencia y externalidades",
  "<p>Una fábrica contamina un río y no paga por ese daño (semana 9). ¿El equilibrio del mercado es eficiente?</p>",
  [O(["No: la oferta solo cuenta el costo privado, así que se produce más de lo eficiente", "Sí: todo equilibrio competitivo es eficiente",
      "No: se produce menos de lo eficiente", "Sí, si la empresa es pequeña", "Depende solo del precio"])],
  ["La «máxima torta» del equilibrio supone que la oferta refleja todo el costo. Con contaminación, el costo social es mayor que el privado.",
   "Se producen unidades cuyo costo social supera lo que valen: hay pérdida de bienestar. Por eso se corrige con impuestos o regulación (Pigou)."],
  "No: se produce de más", "Costo privado vs. social.", [["eficien"], ["eficien"]]))
B15.append(E("b15e11", 2, "La feria de chocotejas",
  "<p>Imagina que en la feria (el juego de arriba, en 🧪) los compradores valoran la chocoteja en S/ 10, 9, 8, 7, 5, 4, 3 y 2, y los puestos tienen costos de S/ 2, 3, 4, 5, 7, 8, 9 y 10. "
  "Se fija el precio en <b>S/ 4</b>.</p>",
  [NUM([{"l": "Chocotejas que se venden", "a": 3}, {"l": "Bienestar total", "a": 18, "u": "S/"}, {"l": "Pérdida frente al máximo", "a": 2, "u": "S/"}], "Calcula")],
  ["A S/ 4 quieren comprar 6 personas (10, 9, 8, 7, 5, 4), pero solo venden 3 puestos (costos 2, 3, 4): se venden 3.",
   "Compran los que más la valoran: excedente (10 − 4) + (9 − 4) + (8 − 4) = 15; puestos (4 − 2) + (4 − 3) + 0 = 3. Total 18.",
   "El máximo es 20 (en el equilibrio, con precio entre 5 y 7, se venden 4). Se pierde el intercambio entre quien la valoraba en 7 y el puesto de costo 5: S/ 2."],
  "3 · 18 · 2", "Cuenta quién quiere comprar y quién quiere vender.", [["intervp"], ["exccons", "excprod"], ["dwl"]]))
B15_tools = [
 {"w": "feria", "t": "¿Quién compra? La feria de chocotejas", "p": "Mueve el precio y cumple los retos. Luego toca «Ver como gráfico»: los escalones son las curvas de demanda y oferta.", "o": {}},
 {"w": "exc", "t": "Excedentes en vivo", "p": "Elige un modo y mueve el deslizador: mira cómo cambian los excedentes y la pérdida irrecuperable (rojo).",
  "o": {"a": 100, "b": 2, "c": 10, "d": 1, "mode": "q"}}]

CONC = {
 "exccons": {"n": "Excedente del consumidor", "f": "Disposición a pagar − precio", "x": "Área bajo la demanda y sobre el precio.", "home": "b15"},
 "excprod": {"n": "Excedente del productor", "f": "Precio − costo", "x": "Área sobre la oferta y bajo el precio.", "home": "b15"},
 "eficien": {"n": "Eficiencia", "f": "Equilibrio competitivo → EC + EP máximo", "x": "Se hacen todos los intercambios que valen más de lo que cuestan.", "home": "b15"},
 "impexc": {"n": "Impuesto y bienestar", "f": "Recaudación \\(t\\cdot Q\\) + triángulo perdido", "x": "El comprador paga más, el vendedor recibe menos y se vende menos.", "home": "b15"},
 "intervp": {"n": "Precios máximos y mínimos", "f": "Tope bajo → escasez · piso alto → sobra", "x": "Ambos reducen la cantidad vendida y causan pérdida irrecuperable.", "home": "b15"},
}
B15_TOPIC = {"id": "b15", "name": "Sem. 15 · 📖 Economía del bienestar: excedentes y eficiencia", "teo": B15_teo, "form": B15_form, "lesson": B15_lesson, "ex": B15, "tools": B15_tools}
CARD = '<div><b>Bienestar</b><br>EC bajo D sobre P · EP sobre O bajo P · equilibrio = eficiente · impuesto: recaudación + triángulo perdido</div>'

ef = json.load(open(P("micro-ef"), encoding="utf-8"))
ef["topics"] = [t for t in ef["topics"] if t["id"] != "b15"] + [B15_TOPIC]
ef["concepts"].update(CONC)
if "<b>Bienestar</b>" not in ef["form"]:
    j = ef["form"].rindex("</div>"); ef["form"] = ef["form"][:j] + CARD + ef["form"][j:]
ef["intro"] = ("Repaso acumulado con todos los temas abiertos: primero los 4 bloques del parcial, luego <b>la semana 9: externalidades</b>, las semanas 10 a 13 "
               "(bienes públicos, maximización y competencia perfecta, monopolio y competencia monopolística, oligopolio y teoría de juegos) y la semana 15: "
               "<b>economía del bienestar</b> (excedentes y eficiencia). "
               "<b>📖 Las semanas 10 a 15 están adelantadas según el sílabo</b> (el profesor aún no sube esas clases): se hicieron con su bibliografía y se ajustarán cuando llegue su material. "
               "Hay juego del polizón, feria de chocotejas, excedentes en vivo, buscador del beneficio máximo y matriz de pagos interactiva.")
ef["sim"]["slots"] = [
 {"pts": 2, "name": "Repaso parcial: conceptos y mercado", "pool": ["mis5", "mis4", "mb1", "me10", "mis6", "me9", "me12"]},
 {"pts": 2, "name": "Repaso parcial: producción y costos", "pool": ["mp10", "mis7", "mk9", "mis8", "mk8"]},
 {"pts": 2, "name": "Sem. 9: externalidades", "pool": ["xg3", "xg4", "xg5", "xs2", "xs4", "xg9", "xp4", "xp5"]},
 {"pts": 2, "name": "Sem. 10: bienes públicos", "pool": ["g10e2", "g10e5", "g10e6", "g10e7", "g10e9"]},
 {"pts": 3, "name": "Sem. 11: maximización y competencia perfecta", "pool": ["m11e3", "m11e4", "m11e5", "m11e6", "m11e7"]},
 {"pts": 3, "name": "Sem. 12: monopolio y competencia monopolística", "pool": ["m12e2", "m12e3", "m12e4", "m12e5", "m12e9"]},
 {"pts": 3, "name": "Sem. 13: oligopolio y teoría de juegos", "pool": ["o13e2", "o13e4", "o13e5", "o13e6"]},
 {"pts": 3, "name": "Sem. 15: economía del bienestar", "pool": ["b15e4", "b15e5", "b15e6", "b15e9", "b15e11"]}]

ids = [e["id"] for t in ef["topics"] for e in t["ex"]] + [e["id"] for e in ef.get("simEx", [])]
assert len(ids) == len(set(ids)) and sum(s["pts"] for s in ef["sim"]["slots"]) == 20
for s in ef["sim"]["slots"]:
    for i in s["pool"]: assert i in ids, i
for e in B15:
    for l in e["tags"]:
        for k in l: assert k in ef["concepts"], (e["id"], k)
with open(P("micro-ef"), "w", encoding="utf-8") as f:
    json.dump(ef, f, indent=1, ensure_ascii=False); f.write("\n")
print("ok b15", len(B15))
