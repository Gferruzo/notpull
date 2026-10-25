#!/usr/bin/env python3
"""Matemáticas Discretas I · Semana 11 (Relaciones II: propiedades, equivalencia y orden parcial) → cursos/md-ef.json.

Interactivo nuevo: «completa la relación» (IW.rel): agregar los pares mínimos para que sea reflexiva, simétrica,
transitiva, de equivalencia o de orden parcial. Las respuestas (clausuras) se calculan y comprueban aquí.
Uso: python3 tools/md_s11.py   (reejecutable: reemplaza los temas c11*).
"""
import json, os, math
from itertools import product

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RAIZ, "cursos", "md-ef.json")
d = json.load(open(F, encoding="utf-8"))


def E(i, lvl, title, q, checks, steps, ans, hint, tags, chain=False, fig=None):
    e = {"id": i, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans,
         "hint": hint, "fig": fig, "draw": False, "solfig": None, "tags": tags}
    if chain:
        e["chain"] = True
    return e


def O(o, p="Respuesta"):
    assert len(o) == 5 and len(set(o)) == 5
    return {"p": p, "o": o}


# ---------------------------------------------------------------- propiedades y clausuras
def ref(A, R): return all((a, a) in R for a in A)
def sim(A, R): return all((y, x) in R for x, y in R)
def anti(A, R): return all(not ((y, x) in R and x != y) for x, y in R)
def tra(A, R): return all((x, z) in R for x, y in R for y2, z in R if y == y2)


def clos(A, R, want):
    S = set(R)
    while True:
        n = len(S)
        if "ref" in want: S |= {(a, a) for a in A}
        if "sim" in want: S |= {(y, x) for x, y in S}
        if "tra" in want: S |= {(x, z) for x, y in S for y2, z in S if y == y2}
        if len(S) == n: return S


def props(A, R): return (ref(A, R), sim(A, R), anti(A, R), tra(A, R))


def rel(A, give, want, p, e=""):
    W = want if isinstance(want, list) else {"eq": ["ref", "sim", "tra"], "ord": ["ref", "tra"]}[want]
    S = clos(A, set(give), W)
    if want == "ord":
        assert anti(A, S), "la clausura no es antisimétrica"
    add = sorted(S - set(give))
    return {"t": "rel", "p": p, "A": A, "give": [list(x) for x in sorted(give)], "want": want, "a": [list(x) for x in add], "e": e}, add


def P(R):
    L = [f"({x},{y})" for x, y in sorted(R)]
    ch = [",".join(L[i:i + 4]) for i in range(0, len(L), 4)]
    return "\\(\\{" + ",\\) \\(".join(ch) + "\\}\\)"


def digraph(A, R):
    n = len(A); W, H = 220, 180; cx, cy = W / 2, H / 2 + 4; Rr = 64
    pos = {x: (cx + Rr * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + Rr * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i, x in enumerate(A)}
    s = [f'<svg class="dg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="mdar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="gl2h"/></marker></defs>']
    for x, y in sorted(R):
        x1, y1 = pos[x]; x2, y2 = pos[y]
        if x == y:
            dx, dy = x1 - cx, y1 - cy; L = math.hypot(dx, dy) or 1; ux, uy = dx / L, dy / L
            s.append(f'<circle class="gl" cx="{x1 + ux * 22:.1f}" cy="{y1 + uy * 22:.1f}" r="9"/>')
            continue
        both = (y, x) in R
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; off = 5 if both else 0
        nx, ny = -uy * off, ux * off
        s.append(f'<line class="gl" x1="{x1 + ux * 13 + nx:.1f}" y1="{y1 + uy * 13 + ny:.1f}" x2="{x2 - ux * 14 + nx:.1f}" y2="{y2 - uy * 14 + ny:.1f}" marker-end="url(#mdar)"/>')
    for x in A:
        px, py = pos[x]
        s.append(f'<circle class="bx" cx="{px:.1f}" cy="{py:.1f}" r="12"/><text class="dl" x="{px:.1f}" y="{py + 4.5:.1f}" text-anchor="middle">{x}</text>')
    s.append("</svg>")
    return "".join(s)


# ---------------------------------------------------------------- comprobaciones de la clase
A3 = [1, 2, 4]
R_e1 = {(1, 1), (2, 4), (4, 4), (2, 1), (2, 2)}
assert ref(A3, R_e1) and not sim(A3, R_e1)
A5 = [0, 1, 2, 3, 4]
R_le4 = {(x, y) for x in A5 for y in A5 if x + y <= 4}
assert [a for a in A5 if (a, a) not in R_le4] == [3, 4]
A6 = [1, 2, 3, 4, 5, 6]
R1 = {(x, y) for x in A6 for y in A6 if x + y == 7}
R3 = {(x, y) for x in A6 for y in A6 if abs(x - y) == 1}
R4 = {(x, y) for x in A6 for y in A6 if x * x + y * y == 25}
assert sim(A6, R1) and sim(A6, R3) and sim(A6, R4) and len(R1) == 6 and not tra(A6, R1) and R4 == {(3, 4), (4, 3)}
At = [1, 2, 3, 4]
R_t = {(1, 1), (1, 3), (3, 1), (3, 3), (3, 2), (3, 4), (2, 4), (1, 2), (1, 4)}
assert props(At, R_t) == (False, False, False, True)
A123 = [1, 2, 3]
R_s = {(1, 1), (1, 3), (3, 1), (2, 2), (2, 3), (3, 2)}
assert sim(A123, R_s) and not tra(A123, R_s)
R_a = {(1, 1), (3, 1), (2, 2), (3, 2)}
assert anti(A123, R_a) and tra(A123, R_a) and not ref(A123, R_a)
# x > y en un conjunto finito de reales: transitiva y antisimétrica (por vacuidad), no reflexiva ni simétrica
Ag = [1, 2, 3, 4]
Rg = {(x, y) for x in Ag for y in Ag if x - y > 0}
assert props(Ag, Rg) == (False, False, True, True)
# divisibilidad en {1,…,12}
Dv = [1, 2, 3, 4, 6, 12]
Rd = {(x, y) for x in Dv for y in Dv if y % x == 0}
assert props(Dv, Rd) == (True, False, True, True)
incomp = [(x, y) for i, x in enumerate(Dv) for y in Dv[i + 1:] if (x, y) not in Rd and (y, x) not in Rd]
assert incomp == [(2, 3), (3, 4), (4, 6)]
# 3 | (x − y) en {0,…,8}: equivalencia con 3 clases
Z9 = list(range(9))
R3m = {(x, y) for x in Z9 for y in Z9 if (x - y) % 3 == 0}
assert props(Z9, R3m)[0:2] == (True, True) and tra(Z9, R3m) and len(R3m) == 27

# ejemplos para la clasificación simétrica/antisimétrica (A = {1,2,3})
CL = [
    ({(1, 1), (2, 2)}, "Simétrica y antisimétrica"),
    ({(1, 2), (2, 1), (3, 3)}, "Solo simétrica"),
    ({(1, 2), (2, 3), (1, 3)}, "Solo antisimétrica"),
    ({(1, 2), (2, 1), (2, 3)}, "Ni simétrica ni antisimétrica"),
    (set(), "Simétrica y antisimétrica"),
    ({(1, 3), (3, 1)}, "Solo simétrica"),
    ({(2, 1), (3, 1), (3, 3)}, "Solo antisimétrica"),
]
CATS = ["Simétrica y antisimétrica", "Solo simétrica", "Solo antisimétrica", "Ni simétrica ni antisimétrica"]
for R, c in CL:
    s, a = sim(A123, R), anti(A123, R)
    assert c == CATS[0 if s and a else 1 if s else 2 if a else 3], (R, c)


def setT(R):
    return "\\(\\varnothing\\)" if not R else P(R)


# ---------------------------------------------------------------- interactivos «completa»
ch_ref, add_ref = rel([1, 2, 3, 4], {(1, 2), (2, 2), (3, 1)}, ["ref"], "Agrega los pares mínimos para que R sea reflexiva.",
                      "Reflexiva: cada elemento de A debe relacionarse consigo mismo (toda la diagonal).")
assert add_ref == [(1, 1), (3, 3), (4, 4)]
ch_sim, add_sim = rel([1, 2, 3], {(1, 1), (1, 3), (2, 3)}, ["sim"], "Agrega los pares mínimos para que R sea simétrica.",
                      "Simétrica: si está \\((x,y)\\), debe estar \\((y,x)\\). La matriz debe quedar igual a su reflejo en la diagonal.")
assert add_sim == [(3, 1), (3, 2)]
ch_tra, add_tra = rel([1, 2, 3, 4], {(1, 2), (2, 3), (3, 4)}, ["tra"], "Agrega los pares mínimos para que R sea transitiva.",
                      "Transitiva: si hay camino \\(x\\to y\\to z\\), debe haber flecha directa \\(x\\to z\\). Ojo: los atajos nuevos también generan atajos.")
assert add_tra == [(1, 3), (1, 4), (2, 4)]
ch_eq1, add_eq1 = rel([1, 2, 3, 4], {(1, 2), (2, 2), (3, 4)}, "eq", "Agrega los pares mínimos para que R sea de equivalencia.",
                      "Equivalencia = reflexiva + simétrica + transitiva: A se parte en bloques y dentro de cada bloque todos se relacionan con todos.")
assert add_eq1 == [(1, 1), (2, 1), (3, 3), (4, 3), (4, 4)]
ch_eq2, add_eq2 = rel([1, 2, 3, 4, 5], {(1, 2), (2, 3), (4, 4)}, "eq", "Agrega los pares mínimos para que R sea de equivalencia.",
                      "Como \\(1R2\\) y \\(2R3\\), el 1, el 2 y el 3 quedan en el mismo bloque. El 5 no se relaciona con nadie, pero igual necesita su bucle.")
assert len(add_eq2) == 8 and (5, 5) in add_eq2
ch_ord, add_ord = rel([1, 2, 3, 4], {(1, 2), (2, 4), (1, 3)}, "ord", "Agrega los pares mínimos para que R sea de orden parcial.",
                      "Orden parcial = reflexiva + antisimétrica + transitiva. No agregues pares de vuelta: rompen la antisimetría.")
assert add_ord == [(1, 1), (1, 4), (2, 2), (3, 3), (4, 4)]

CONC = {
    "refl": {"n": "Relación reflexiva", "f": "\\(\\forall x\\in A:(x,x)\\in R\\)", "x": "Toda la diagonal; en el digrafo, un bucle en cada elemento. Basta un \\((a,a)\\notin R\\) para que no lo sea.", "home": "c11prop"},
    "simr": {"n": "Relación simétrica", "f": "\\((x,y)\\in R\\Rightarrow(y,x)\\in R\\)", "x": "Matriz simétrica respecto de la diagonal; en el digrafo, toda flecha tiene su flecha de vuelta.", "home": "c11prop"},
    "antir": {"n": "Relación antisimétrica", "f": "\\((x,y)\\in R\\wedge(y,x)\\in R\\Rightarrow x=y\\)", "x": "Nunca hay ida y vuelta entre elementos distintos. No es lo contrario de simétrica: puede ser ambas o ninguna.", "home": "c11prop"},
    "trar": {"n": "Relación transitiva", "f": "\\((x,y),(y,z)\\in R\\Rightarrow(x,z)\\in R\\)", "x": "Todo camino de dos flechas tiene su atajo directo.", "home": "c11prop"},
    "releq": {"n": "Relación de equivalencia", "f": "Reflexiva + simétrica + transitiva", "x": "Parte el conjunto en bloques (clases) donde todos se relacionan con todos.", "home": "c11eq"},
    "ordp": {"n": "Orden parcial", "f": "Reflexiva + antisimétrica + transitiva", "x": "\\((A,R)\\) es un conjunto parcialmente ordenado (CPO). Ejemplos: \\(\\le\\), \\(\\subseteq\\), divisibilidad en \\(\\mathbb Z^+\\).", "home": "c11eq"},
    "compar": {"n": "Elementos comparables", "f": "\\(a,b\\) comparables si \\(aRb\\vee bRa\\)", "x": "En un CPO puede haber elementos incomparables: ni \\(aRb\\) ni \\(bRa\\).", "home": "c11eq"},
}

# ---------------------------------------------------------------- Tema 1
T1 = {
 "id": "c11prop",
 "name": "Sem. 11 · Relaciones II: reflexiva, simétrica, antisimétrica y transitiva",
 "teo": (
  "<p>Sea R una relación sobre un conjunto A (\\(R\\subseteq A\\times A\\)).</p>"
  "<div class=\"tbl\"><table><tr><th>Propiedad</th><th>Definición</th><th>En el digrafo</th></tr>"
  "<tr><td>Reflexiva</td><td>\\(\\forall x\\in A:(x,x)\\in R\\)</td><td>bucle en cada elemento</td></tr>"
  "<tr><td>Simétrica</td><td>\\((x,y)\\in R\\Rightarrow(y,x)\\in R\\)</td><td>toda flecha tiene vuelta</td></tr>"
  "<tr><td>Antisimétrica</td><td>\\((x,y),(y,x)\\in R\\Rightarrow x=y\\)</td><td>nunca ida y vuelta entre distintos</td></tr>"
  "<tr><td>Transitiva</td><td>\\((x,y),(y,z)\\in R\\Rightarrow(x,z)\\in R\\)</td><td>todo camino de 2 flechas tiene atajo</td></tr></table></div>"
  "<p class=\"ej\"><b>Ejemplos de la clase:</b> en \\(A=\\{1,2,4\\}\\), \\(R=\\{(1,1),(2,4),(4,4),(2,1),(2,2)\\}\\) es reflexiva. \\(x\\le y\\) en \\(\\mathbb R\\) es reflexiva. «Misma paridad» en \\(\\mathbb Z\\) es reflexiva, simétrica y transitiva. \\(x\\mid y\\) en \\(\\mathbb Z^+\\) es reflexiva y transitiva, pero no simétrica (\\(2\\mid4\\), \\(4\\nmid2\\)).</p>"
  "<p>Para que R <b>no</b> sea reflexiva basta <b>un</b> \\(a\\in A\\) con \\((a,a)\\notin R\\): \\(x+y\\le4\\) en \\(\\{0,\\dots,4\\}\\) falla en \\((4,4)\\) (y en \\((3,3)\\)).</p>"
  "<p>Forma equivalente de antisimétrica: si \\((x,y)\\in R\\) y \\(x\\ne y\\), entonces \\((y,x)\\notin R\\).</p>"
 ),
 "form": [
  "Reflexiva: \\((x,x)\\in R\\) para todo \\(x\\) · bucles",
  "Simétrica: \\(xRy\\Rightarrow yRx\\) · flechas de ida y vuelta",
  "Antisimétrica: \\(xRy\\wedge yRx\\Rightarrow x=y\\)",
  "Transitiva: \\(xRy\\wedge yRz\\Rightarrow xRz\\) · atajos",
  "No simétrica \\(\\not\\Rightarrow\\) antisimétrica",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Cada propiedad es un <strong>para todo</strong>: para afirmarla hay que revisar todos los casos, pero para negarla basta <strong>un contraejemplo</strong> (un bucle que falta, un par sin su vuelta, un camino sin atajo).</p>"
  "<h3>Cómo revisar una relación finita</h3><ol><li><b>Reflexiva:</b> mira la diagonal de la matriz (o los bucles).</li><li><b>Simétrica:</b> la matriz debe coincidir con su reflejo en la diagonal.</li><li><b>Antisimétrica:</b> fuera de la diagonal, nunca dos ● reflejados.</li><li><b>Transitiva:</b> por cada par de flechas encadenadas \\(x\\to y\\to z\\), busca \\(x\\to z\\) (también cuando \\(x=z\\): \\((1,3),(3,1)\\) exige \\((1,1)\\)).</li></ol>"
  "<div class=\"err\"><b>Errores frecuentes:</b> creer que «no simétrica» significa «antisimétrica» (son independientes: \\(\\{(1,1)\\}\\) es ambas y \\(\\{(1,2),(2,1),(2,3)\\}\\) no es ninguna); olvidar que una propiedad que no tiene casos que revisar se cumple por vacuidad (\\(x>y\\) es antisimétrica porque nunca pasan \\(x>y\\) y \\(y>x\\) a la vez); y en la transitividad olvidar el caso \\(x\\to y\\to x\\), que exige el bucle \\((x,x)\\).</div>"
 ),
 "ex": [
  E("rp1", 1, "¿Por qué no es reflexiva?",
    "<p>En \\(A=\\{0,1,2,3,4\\}\\) se define \\(R=\\{(x,y)\\in A\\times A: x+y\\le4\\}\\). ¿Cuál es una justificación correcta de que R <strong>no</strong> es reflexiva?</p>",
    [O(["\\((3,3)\\notin R\\), porque \\(3+3=6>4\\)", "\\((0,4)\\in R\\) pero \\((4,0)\\notin R\\)", "\\((2,2)\\notin R\\), porque \\(2+2>4\\)", "Hay pares \\((x,y)\\) con \\(x\\ne y\\)", "\\((4,4)\\in R\\)"])],
    ["Reflexiva exige \\((a,a)\\in R\\) para <b>todo</b> \\(a\\in A\\); para negarla basta un \\(a\\) que falle.",
     "\\(3+3=6>4\\) y \\(4+4=8>4\\): \\((3,3)\\) y \\((4,4)\\) no están. Con uno solo basta. \\((2,2)\\) sí está (\\(2+2=4\\le4\\)) y \\((4,0)\\) también está, así que esas opciones son falsas."],
    "\\((3,3)\\notin R\\)", "Busca un elemento sin bucle.", [["refl"], ["refl"]]),
  E("rp2", 1, "Completa: reflexiva",
    "<p>\\(A=\\{1,2,3,4\\}\\) y \\(R=\\{(1,2),(2,2),(3,1)\\}\\). Agrega lo mínimo para que R sea reflexiva.</p>",
    [ch_ref],
    ["Reflexiva: hacen falta todos los \\((a,a)\\) con \\(a\\in A\\). Ya está \\((2,2)\\).",
     "Faltan \\((1,1),(3,3),(4,4)\\). Los pares \\((1,2)\\) y \\((3,1)\\) no molestan: la reflexividad solo mira la diagonal."],
    P(add_ref), "Mira la diagonal.", [["refl"], ["refl"]]),
  E("rp3", 2, "Completa: simétrica",
    "<p>\\(A=\\{1,2,3\\}\\) y \\(R=\\{(1,1),(1,3),(2,3)\\}\\). Agrega lo mínimo para que R sea simétrica.</p>",
    [ch_sim],
    ["Por cada par \\((x,y)\\) con \\(x\\ne y\\) hace falta su vuelta \\((y,x)\\). El bucle \\((1,1)\\) ya es su propia vuelta.",
     "\\((1,3)\\to\\) falta \\((3,1)\\); \\((2,3)\\to\\) falta \\((3,2)\\). Se agregan " + P(add_sim) + "."],
    P(add_sim), "Refleja cada ● en la diagonal.", [["simr"], ["simr"]]),
  E("rp4", 2, "Completa: transitiva",
    "<p>\\(A=\\{1,2,3,4\\}\\) y \\(R=\\{(1,2),(2,3),(3,4)\\}\\) (una cadena \\(1\\to2\\to3\\to4\\)). Agrega lo mínimo para que R sea transitiva.</p>",
    [ch_tra],
    ["\\(1\\to2\\to3\\) exige \\((1,3)\\); \\(2\\to3\\to4\\) exige \\((2,4)\\).",
     "Con los nuevos atajos aparece \\(1\\to3\\to4\\), que exige \\((1,4)\\). Se repite hasta que no aparezca nada nuevo: " + P(add_tra) + ". No hacen falta bucles porque no hay ida y vuelta."],
    P(add_tra), "Atajos de los atajos.", [["trar"], ["trar"]]),
  E("rp5", 2, "Simétrica vs. antisimétrica",
    "<p>En \\(A=\\{1,2,3\\}\\), clasifica cada relación. ¿Es cierto que si una relación no es simétrica, entonces es antisimétrica?</p>",
    [{"t": "cls", "p": "Clasifica cada relación", "cats": CATS,
      "items": [{"x": setT(R), "c": CATS.index(c)} for R, c in CL[:4]] + [{"x": setT(CL[4][0]), "c": 0, "e": "La vacía cumple ambas por vacuidad: no hay pares que revisar."}] + [{"x": setT(R), "c": CATS.index(c)} for R, c in CL[5:]]},
     O(["No: una relación puede no ser simétrica ni antisimétrica", "Sí, siempre", "Sí, salvo si es vacía", "Solo si además es reflexiva", "Solo en conjuntos finitos"], "Entonces, ¿no simétrica ⇒ antisimétrica?")],
    ["Simétrica: toda flecha tiene vuelta. Antisimétrica: ninguna flecha entre distintos tiene vuelta.",
     "Las relaciones que solo tienen bucles (o ninguna flecha) cumplen las dos. \\(\\{(1,2),(2,1),(2,3)\\}\\) no es simétrica (falta \\((3,2)\\)) ni antisimétrica (\\(1\\to2\\to1\\)).",
     "Por eso la respuesta es <b>no</b>: son propiedades independientes."],
    "No: son independientes", "Busca un par de ida y vuelta y una flecha sin vuelta.", [["simr", "antir"], ["simr", "antir"], ["antir"]], chain=True),
  E("rp6", 2, "\\(x-y>0\\) en \\(\\mathbb R\\)",
    "<p>En \\(\\mathbb R\\) se define \\(xRy\\iff x-y>0\\). ¿Qué propiedades tiene?</p>",
    [O(["Transitiva y antisimétrica, pero no reflexiva ni simétrica", "Solo transitiva", "Reflexiva y transitiva", "Simétrica y transitiva", "Ninguna"])],
    ["No reflexiva: \\(x-x=0\\not>0\\). No simétrica: \\(3R1\\) pero \\(1-3<0\\).",
     "Transitiva: si \\(x-y>0\\) y \\(y-z>0\\), entonces \\(x-z=(x-y)+(y-z)\\) \\(>0\\).",
     "Antisimétrica por vacuidad: nunca ocurren a la vez \\(x>y\\) y \\(y>x\\), así que la implicación no tiene casos que la falseen. (La clase solo menciona transitiva; la antisimetría también vale.)"],
    "Transitiva y antisimétrica", "La antisimetría puede cumplirse por vacuidad.", [["refl", "simr"], ["trar"], ["antir"]]),
  E("rp7", 2, "\\(x+y=7\\) en \\(\\{1,\\dots,6\\}\\)",
    "<p>\\(A=\\{1,2,3,4,5,6\\}\\) y \\(R_1=\\{(x,y)\\in A\\times A: x+y=7\\}\\).</p>",
    [{"t": "num", "p": "Parte 1", "f": [{"l": "\\(|R_1|=\\)", "a": len(R1), "e": "Para cada x hay exactamente un y = 7 − x en A."}]},
     O(["No: \\((1,6)\\) y \\((6,1)\\) exigirían \\((1,1)\\)", "Sí, porque es simétrica", "Sí, porque no hay bucles", "No, porque \\((3,4)\\notin R_1\\)", "Sí, por vacuidad"], "Parte 2: ¿es transitiva?")],
    ["\\(R_1=\\{(1,6),(2,5),(3,4),\\) \\((4,3),(5,2),(6,1)\\}\\): 6 pares. Es simétrica (si \\(x+y=7\\), también \\(y+x=7\\)).",
     "Transitividad: \\(1R6\\) y \\(6R1\\) exigirían \\(1R1\\), pero \\(1+1\\ne7\\). No es transitiva. (\\((3,4)\\) sí está.)"],
    "6 pares; no es transitiva", "Encadena una ida y su vuelta.", [["simr"], ["trar"]], chain=True),
  E("rp8", 1, "Divisibilidad en \\(\\mathbb Z^+\\)",
    "<p>En \\(\\mathbb Z^+\\), \\(xRy\\iff x\\mid y\\). ¿Qué propiedad <strong>no</strong> tiene?</p>",
    [O(["Simétrica", "Reflexiva", "Transitiva", "Antisimétrica", "Las tiene todas"])],
    ["Reflexiva: \\(x\\mid x\\). Transitiva: \\(x\\mid y\\) y \\(y\\mid z\\Rightarrow y=kx,\\ z=my\\Rightarrow z=(km)x\\).",
     "Antisimétrica en \\(\\mathbb Z^+\\): si \\(x\\mid y\\) y \\(y\\mid x\\), entonces \\(x\\le y\\le x\\), luego \\(x=y\\).",
     "No simétrica: \\(2\\mid4\\) pero \\(4\\nmid2\\)."],
    "Simétrica", "Prueba con 2 y 4.", [["refl", "trar"], ["antir"], ["simr"]]),
  E("rp9", 3, "Lee el digrafo",
    "<p>El digrafo muestra la relación \\(R=\\{(1,1),(1,3),(3,1),(3,3),\\) \\((3,2),(3,4),(2,4),(1,2),(1,4)\\}\\) sobre \\(A=\\{1,2,3,4\\}\\). ¿Qué propiedades tiene?</p>",
    [O(["Solo transitiva", "Transitiva y reflexiva", "Transitiva y antisimétrica", "Simétrica y transitiva", "Ninguna"])],
    ["No reflexiva: faltan los bucles en 2 y 4. No simétrica: \\((3,2)\\in R\\) y \\((2,3)\\notin R\\).",
     "No antisimétrica: \\((1,3)\\) y \\((3,1)\\) con \\(1\\ne3\\).",
     "Transitiva: cada camino de dos flechas tiene atajo; por ejemplo \\(3\\to1\\to2\\) con \\((3,2)\\), \\(1\\to3\\to1\\) con \\((1,1)\\) y \\(1\\to2\\to4\\) con \\((1,4)\\)."],
    "Solo transitiva", "Revisa los bucles y la ida y vuelta 1 ↔ 3.", [["refl", "simr"], ["antir"], ["trar"]], fig="md_rp9"),
 ],
}

# ---------------------------------------------------------------- Tema 2
T2 = {
 "id": "c11eq",
 "name": "Sem. 11 · Relaciones de equivalencia y de orden parcial",
 "teo": (
  "<p><strong>Relación de equivalencia:</strong> reflexiva, simétrica y transitiva. Ejemplos: «misma paridad» en \\(\\mathbb Z\\), \\(3\\mid(x-y)\\) en \\(\\mathbb Z\\), la igualdad.</p>"
  "<p><strong>Relación de orden parcial:</strong> reflexiva, <b>anti</b>simétrica y transitiva. El par \\((A,R)\\) se llama <strong>conjunto parcialmente ordenado</strong> (CPO). Ejemplos: \\(\\le\\) en \\(\\mathbb R\\), \\(\\subseteq\\) en \\(\\mathcal P(S)\\), \\(\\mid\\) en \\(\\mathbb Z^+\\).</p>"
  "<p>En un CPO, \\(a\\) y \\(b\\) son <strong>comparables</strong> si \\(aRb\\vee bRa\\), e <strong>incomparables</strong> si \\((a,b)\\notin R\\) y \\((b,a)\\notin R\\). Se llama «parcial» justamente porque puede haber incomparables: \\(\\{a\\}\\) y \\(\\{b\\}\\) con \\(\\subseteq\\), o 2 y 3 con \\(\\mid\\).</p>"
  "<p class=\"ej\"><b>Ejercicios de la clase:</b> (1) \\(\\subseteq\\) en \\(\\mathcal P(S)\\) es orden parcial. (2) \\(x-y\\ge0\\) en \\(\\mathbb R\\) es orden parcial. (3) \\(3\\mid(x-y)\\) en \\(\\mathbb Z\\) es de equivalencia.</p>"
 ),
 "form": [
  "Equivalencia: reflexiva + simétrica + transitiva",
  "Orden parcial: reflexiva + antisimétrica + transitiva → CPO \\((A,R)\\)",
  "Comparables: \\(aRb\\vee bRa\\) · incomparables: ninguno",
  "\\(3\\mid(x-y)\\): \\(x-z=(x-y)+(y-z)\\)",
 ],
 "lesson": (
  "<h3>Idea central</h3><p>Las dos relaciones «estrella» comparten reflexiva y transitiva; las separa la tercera: <strong>simétrica</strong> (equivalencia: «se parecen») o <strong>antisimétrica</strong> (orden: «va antes que»).</p>"
  "<h3>Cómo demostrar que es de equivalencia</h3><ol><li>Reflexiva: muestra que \\(xRx\\) siempre (\\(3\\mid0\\)).</li><li>Simétrica: de \\(xRy\\) deduce \\(yRx\\) (\\(y-x=-(x-y)\\)).</li><li>Transitiva: de \\(xRy\\) y \\(yRz\\) deduce \\(xRz\\) (suma: \\(x-z=(x-y)+(y-z)\\)).</li></ol>"
  "<p>Una equivalencia sobre un conjunto finito se ve como <strong>bloques</strong>: dentro de cada bloque, todos con todos (incluidos los bucles); entre bloques, nada.</p>"
  "<div class=\"err\"><b>Errores frecuentes:</b> olvidar los bucles de los elementos que no se relacionan con nadie (siguen necesitando \\((a,a)\\)); confundir antisimétrica con «no simétrica»; decir que \\(<\\) es orden parcial (no es reflexiva); y pensar que en un orden parcial todos los pares son comparables.</div>"
 ),
 "ex": [
  E("re1", 2, "Completa: equivalencia",
    "<p>\\(A=\\{1,2,3,4\\}\\) y \\(R=\\{(1,2),(2,2),(3,4)\\}\\). Agrega lo mínimo para que R sea de equivalencia.</p>",
    [ch_eq1],
    ["Los bloques salen de los pares dados: \\(\\{1,2\\}\\) y \\(\\{3,4\\}\\).",
     "Dentro de cada bloque, todos con todos: \\((1,1),(2,1)\\) para el primero y \\((3,3),(4,3),(4,4)\\) para el segundo (ya estaban \\((1,2),(2,2),(3,4)\\)).",
     "Resultado: \\(R=\\{(1,1),(1,2),(2,1),(2,2),\\) \\((3,3),(3,4),(4,3),(4,4)\\}\\)."],
    P(add_eq1), "Piensa en bloques.", [["releq"], ["refl", "simr"], ["releq"]]),
  E("re2", 3, "Completa: equivalencia con cadena",
    "<p>\\(A=\\{1,2,3,4,5\\}\\) y \\(R=\\{(1,2),(2,3),(4,4)\\}\\). Agrega lo mínimo para que R sea de equivalencia.</p>",
    [ch_eq2],
    ["\\(1R2\\) y \\(2R3\\) ponen a 1, 2 y 3 en el mismo bloque (transitividad + simetría).",
     "Bloques: \\(\\{1,2,3\\}\\) (9 pares), \\(\\{4\\}\\) y \\(\\{5\\}\\) (un bucle cada uno). El 5 no aparece en R, pero la reflexividad igual exige \\((5,5)\\).",
     "Hay que agregar " + str(len(add_eq2)) + " pares: " + P(add_eq2) + "."],
    str(len(add_eq2)) + " pares", "No te olvides del 5.", [["releq"], ["refl"], ["releq"]]),
  E("re3", 2, "Completa: orden parcial",
    "<p>\\(A=\\{1,2,3,4\\}\\) y \\(R=\\{(1,2),(2,4),(1,3)\\}\\). Agrega lo mínimo para que R sea de orden parcial.</p>",
    [ch_ord],
    ["Reflexiva: los cuatro bucles. Transitiva: \\(1\\to2\\to4\\) exige \\((1,4)\\).",
     "Antisimétrica: no se agrega ninguna flecha de vuelta; el resultado no tiene ida y vuelta entre distintos.",
     "Se agregan " + P(add_ord) + ". Ojo: 3 y 4 (y 2 y 3) quedan <b>incomparables</b>, y eso está permitido."],
    P(add_ord), "Bucles + atajos, sin vueltas.", [["refl", "trar"], ["antir"], ["ordp", "compar"]]),
  E("re4", 2, "¿Equivalencia, orden parcial o ninguna?",
    "<p>Clasifica cada relación.</p>",
    [{"t": "cls", "p": "Clasifica", "cats": ["Equivalencia", "Orden parcial", "Ninguna de las dos"], "items": [
      {"x": "\\(3\\mid(x-y)\\) en \\(\\mathbb Z\\)", "c": 0},
      {"x": "\\(X\\subseteq Y\\) en \\(\\mathcal P(S)\\)", "c": 1},
      {"x": "\\(x-y\\ge0\\) en \\(\\mathbb R\\)", "c": 1, "e": "\\(x-y\\ge0\\) es \\(x\\ge y\\): reflexiva, antisimétrica y transitiva."},
      {"x": "«misma paridad» en \\(\\mathbb Z\\)", "c": 0},
      {"x": "\\(x\\mid y\\) en \\(\\mathbb Z^+\\)", "c": 1},
      {"x": "\\(x<y\\) en \\(\\mathbb R\\)", "c": 2, "e": "No es reflexiva: \\(x<x\\) es falso."},
      {"x": "\\(|x-y|=1\\) en \\(\\{1,\\dots,6\\}\\)", "c": 2, "e": "No es reflexiva ni transitiva (\\(1R2\\), \\(2R1\\) pero no \\(1R1\\))."}]}],
    ["Equivalencia: reflexiva, simétrica y transitiva → \\(3\\mid(x-y)\\), misma paridad.",
     "Orden parcial: reflexiva, antisimétrica y transitiva → \\(\\subseteq\\), \\(\\ge\\), divisibilidad en \\(\\mathbb Z^+\\).",
     "\\(<\\) falla en la reflexividad y \\(|x-y|=1\\) falla en reflexividad y transitividad."],
    "Ver clasificación", "Primero revisa la reflexividad.", [["releq"], ["ordp"], ["refl", "trar"]]),
  E("re5", 2, "Ordena: \\(3\\mid(x-y)\\) es transitiva",
    "<p>Ordena la demostración de que \\(xRy\\iff3\\mid(x-y)\\) es transitiva en \\(\\mathbb Z\\).</p>",
    [{"t": "order", "p": "Toca los pasos en orden.", "items": [
      "Sean \\(x,y,z\\in\\mathbb Z\\) con \\(xRy\\) y \\(yRz\\).",
      "Entonces \\(x-y=3k\\) y \\(y-z=3m\\) con \\(k,m\\in\\mathbb Z\\).",
      "Sumando: \\(x-z=(x-y)+(y-z)=3k+3m\\).",
      "Así \\(x-z=3(k+m)\\) con \\(k+m\\in\\mathbb Z\\).",
      "Luego \\(3\\mid(x-z)\\), es decir \\(xRz\\). \\(\\blacksquare\\)"]}],
    ["Se parte de las hipótesis \\(xRy\\), \\(yRz\\) y se traducen con la definición de divisibilidad.",
     "El truco es sumar: \\(x-z=(x-y)+(y-z)\\). Se factoriza el 3 y se concluye \\(xRz\\).",
     "Con reflexiva (\\(x-x=0=3\\cdot0\\)) y simétrica (\\(y-x=3(-k)\\)) se completa que es de equivalencia (ejercicio 3 de la clase)."],
    "Hipótesis → definición → suma → factorizar → concluir", "Suma las dos diferencias.", [["releq"], ["trar"], ["releq"]]),
  E("re6", 2, "\\(x-y\\ge0\\): ¿por qué antisimétrica?",
    "<p>Ejercicio 2 de la clase: en \\(\\mathbb R\\), \\(xRy\\iff x-y\\ge0\\). ¿Qué argumento prueba la antisimetría?</p>",
    [O(["Si \\(x-y\\ge0\\) y \\(y-x\\ge0\\), entonces \\(x-y\\ge0\\) y \\(x-y\\le0\\), luego \\(x=y\\)",
        "Si \\(x-y\\ge0\\), entonces \\(y-x\\ge0\\)",
        "\\(x-x=0\\ge0\\)",
        "Si \\(x-y\\ge0\\) y \\(y-z\\ge0\\), entonces \\(x-z\\ge0\\)",
        "Como \\(2-1\\ge0\\) y \\(1-2<0\\), no es simétrica"])],
    ["Antisimétrica: hay que suponer \\(xRy\\) y \\(yRx\\) y llegar a \\(x=y\\).",
     "\\(y-x\\ge0\\iff x-y\\le0\\). Junto con \\(x-y\\ge0\\) queda \\(x-y=0\\). Las otras opciones prueban reflexividad, transitividad o «no simétrica», que no es lo pedido."],
    "\\(x-y\\ge0\\) y \\(x-y\\le0\\Rightarrow x=y\\)", "Supón las dos direcciones.", [["antir"], ["ordp"]]),
  E("re7", 1, "Incomparables con \\(\\subseteq\\)",
    "<p>En el CPO \\((\\mathcal P(\\{a,b,c\\}),\\subseteq)\\), ¿qué par es <strong>incomparable</strong>?</p>",
    [O(["\\(\\{a,b\\}\\) y \\(\\{b,c\\}\\)", "\\(\\{a\\}\\) y \\(\\{a,b\\}\\)", "\\(\\varnothing\\) y \\(\\{c\\}\\)", "\\(\\{b\\}\\) y \\(\\{a,b,c\\}\\)", "\\(\\{a,c\\}\\) y \\(\\{a,c\\}\\)"])],
    ["Comparables: uno está contenido en el otro. \\(\\varnothing\\) está contenido en todo y todo está contenido en \\(\\{a,b,c\\}\\).",
     "\\(\\{a,b\\}\\not\\subseteq\\{b,c\\}\\) (falta a) y \\(\\{b,c\\}\\not\\subseteq\\{a,b\\}\\) (falta c): son incomparables."],
    "\\(\\{a,b\\}\\) y \\(\\{b,c\\}\\)", "¿Alguno está dentro del otro?", [["compar"], ["compar"]]),
  E("re8", 2, "Divisores de 12",
    "<p>En \\(D=\\{1,2,3,4,6,12\\}\\) con la relación \\(x\\mid y\\) (un orden parcial), ¿cuántos pares <strong>no ordenados</strong> \\(\\{a,b\\}\\) de elementos distintos son incomparables?</p>",
    [{"t": "num", "p": "Respuesta", "f": [{"l": "Pares incomparables", "a": len(incomp), "e": "Busca pares donde ninguno divide al otro."}]}],
    ["1 divide a todos y todos dividen a 12: esos nunca son incomparables.",
     "Entre 2, 3, 4 y 6: \\(2\\mid4\\), \\(2\\mid6\\), \\(3\\mid6\\). No se relacionan \\(\\{2,3\\}\\), \\(\\{3,4\\}\\) y \\(\\{4,6\\}\\): son 3."],
    "3", "Revisa 2, 3, 4 y 6 entre sí.", [["compar"], ["compar"]]),
  E("re9", 2, "Clases de \\(3\\mid(x-y)\\)",
    "<p>En \\(A=\\{0,1,\\dots,8\\}\\) se define \\(xRy\\iff3\\mid(x-y)\\).</p>",
    [{"t": "num", "p": "Parte 1", "f": [{"l": "Número de bloques (clases)", "a": 3, "e": "Dos números están en el mismo bloque si dejan el mismo resto al dividir entre 3."},
                                         {"l": "\\(|R|=\\)", "a": len(R3m), "e": "Cada bloque de k elementos aporta k² pares."}]},
     O(["\\(\\{2,5,8\\}\\)", "\\(\\{2,4,6,8\\}\\)", "\\(\\{1,2\\}\\)", "\\(\\{0,3,6,8\\}\\)", "\\(\\{2\\}\\)"], "Parte 2: ¿cuál es el bloque del 2?")],
    ["\\(3\\mid(x-y)\\iff x\\) e \\(y\\) dejan el mismo resto entre 3. Bloques: \\(\\{0,3,6\\}\\), \\(\\{1,4,7\\}\\), \\(\\{2,5,8\\}\\).",
     "Cada bloque tiene 3 elementos y aporta \\(3^2=9\\) pares: \\(|R|=27\\).",
     "El bloque del 2 es \\(\\{2,5,8\\}\\)."],
    "3 bloques, 27 pares; \\(\\{2,5,8\\}\\)", "Agrupa por el resto.", [["releq"], ["releq"], ["releq"]], chain=True),
 ],
}

NUEVOS = [T1, T2]
d.setdefault("figs", {})["md_rp9"] = digraph(At, R_t)

# ---------------------------------------------------------------- ensamblar
d["concepts"].update(CONC)
for t in NUEVOS:
    for e in t["ex"]:
        assert len(e["tags"]) == len(e["steps"]), e["id"]
        for l in e["tags"]:
            for k in l:
                assert k in d["concepts"], (e["id"], k)

top = [t for t in d["topics"] if not t["id"].startswith("c11")]
pos = next(i for i, t in enumerate(top) if t["id"] == "c10rel") + 1
d["topics"] = top[:pos] + NUEVOS + top[pos:]

d["intro"] = ("Repaso acumulado con todos los temas abiertos: primero los temas del parcial, luego <b>la semana 9: conjuntos I</b> "
  "(definición y notación, cardinal, subconjuntos e igualdad con demostraciones, diagramas de Venn y operaciones), <b>la semana 10: conjuntos II y relaciones</b> "
  "(producto cartesiano, conjunto potencia, cardinalidad, álgebra de conjuntos, relaciones, inversa y digrafo) y <b>la semana 11: relaciones II</b> "
  "(reflexiva, simétrica, antisimétrica y transitiva; relaciones de equivalencia y de orden parcial), que pesa más en el simulacro. "
  "En el examen real debes justificar todo: aquí marcas y luego revisas la justificación en «Ver solución». Se actualiza cada semana.")

CARDS = ('<div><b>Propiedades</b><br>reflexiva (bucles) · simétrica (vuelta) · antisimétrica (sin ida y vuelta) · transitiva (atajos)</div>'
  '<div><b>Equivalencia</b><br>reflexiva + simétrica + transitiva → bloques</div>'
  '<div><b>Orden parcial</b><br>reflexiva + antisimétrica + transitiva → CPO; puede haber incomparables</div>')
f = d["form"]
if "Orden parcial</b>" not in f:
    assert f.endswith("</div></div>")
    d["form"] = f[:-len("</div>")] + CARDS + "</div>"

d["sim"]["slots"] = [
 {"pts": 1, "name": "Repaso parcial: lógica y cuantificadores", "pool": ["q9", "q10", "q11", "i9", "i10"]},
 {"pts": 1, "name": "Repaso parcial: demostraciones", "pool": ["t8", "t9", "t10", "dv6", "dv7"]},
 {"pts": 1, "name": "Sem. 9: definición y cardinal", "pool": ["cj3", "cj5", "cj7", "cx2"]},
 {"pts": 2, "name": "Sem. 9: subconjuntos e igualdad", "pool": ["cs3", "cs4", "cs5", "cs7", "cx1"]},
 {"pts": 1, "name": "Sem. 9: operaciones y Venn", "pool": ["co3", "co5", "co6", "co7", "cx3", "co8", "co9", "co10"]},
 {"pts": 2, "name": "Sem. 10: producto cartesiano y potencia", "pool": ["cp2", "cp4", "cp5", "cp6", "cp7"]},
 {"pts": 3, "name": "Sem. 10: álgebra de conjuntos", "pool": ["ca2", "ca3", "ca5", "ca7"]},
 {"pts": 3, "name": "Sem. 10: relaciones", "pool": ["cr2", "cr4", "cr5", "cr8", "cr9"]},
 {"pts": 3, "name": "Sem. 11: propiedades de las relaciones", "pool": ["rp3", "rp4", "rp6", "rp7", "rp9"]},
 {"pts": 3, "name": "Sem. 11: equivalencia y orden parcial", "pool": ["re1", "re2", "re3", "re5", "re8", "re9"]},
]
todos = {e["id"] for t in d["topics"] for e in t["ex"]} | {e["id"] for e in d.get("simEx", [])}
for s in d["sim"]["slots"]:
    for i in s["pool"]:
        assert i in todos, i
assert sum(s["pts"] for s in d["sim"]["slots"]) == 20
assert len(todos) == sum(len(t["ex"]) for t in d["topics"]) + len(d.get("simEx", [])), "ids repetidos"

with open(F, "w", encoding="utf-8") as o:
    json.dump(d, o, indent=1, ensure_ascii=False)
    o.write("\n")
print("ok:", [t["id"] for t in d["topics"]])
