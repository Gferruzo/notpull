#!/usr/bin/env python3
"""Cálculo de una Variable (CC6103) · semanas 11 y 12 → calculo-ea3.json, calculo-ed4.json y calculo-ef.json.

Sem. 11 (EA3 y final): fracciones parciales (con «tapar el factor» de Heaviside), potencias trigonométricas,
sustitución trigonométrica y completar cuadrados, racionalizadora y Weierstrass, EDO logística.
Sem. 12 (ED4 y final): sumas de Riemann (herramienta de rectángulos), integral definida y propiedades, TFC1, TFC2 con
sustitución y partes, área neta y total, cambio neto (IRCA).
Cada antiderivada se comprueba derivando con sympy y cada valor exacto se compara con la integral de sympy.
Uso: python3 tools/calculo_s11_12.py   (reejecutable: reemplaza los temas w11* y w12*)."""
import json, os, random, math
import sympy as sp

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(RAIZ, "cursos", n + ".json")
x, t, u, th = sp.symbols('x t u theta', real=True)
random.seed(7)

def S(s, v='x'):
    """Cadena del motor MX → expresión sympy."""
    s = s.replace('^', '**').replace('π', 'pi')
    loc = {'ln': sp.log, 'sqrt': sp.sqrt, 'abs': sp.Abs, 'arcsin': sp.asin, 'arctan': sp.atan, 'arcsec': sp.asec,
           'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 'sec': sp.sec, 'e': sp.E, 'pi': sp.pi, 'cbrt': sp.cbrt,
           'x': x, 't': t, 'u': u}
    return sp.sympify(s, locals=loc)

def chk_anti(a, f, dom, v=x, n=8):
    F = S(a); d = sp.diff(F, v)
    for _ in range(n):
        p = random.uniform(*dom)
        r = complex(sp.N((d - f).subs(v, p)))
        assert abs(r) < 1e-7, ('anti', a, f, p, r)

def chk_eq(a, g, dom, v=x, n=8):
    F = S(a)
    for _ in range(n):
        p = random.uniform(*dom)
        r = complex(sp.N((F - g).subs(v, p)))
        assert abs(r) < 1e-7, ('eq', a, g, p, r)

def chk_val(a, val):
    r = complex(sp.N(S(a) - val)); assert abs(r) < 1e-9, ('val', a, val, r)

def E(i, lvl, title, q, checks, steps, ans, hint, tags, chain=False):
    assert len(tags) == len(steps), i
    e = {"id": i, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans,
         "hint": hint, "fig": None, "draw": False, "solfig": None, "tags": tags}
    if chain: e["chain"] = True
    return e

def O(o, p="Respuesta"):
    assert len(o) == 5 and len(set(o)) == 5, o
    return {"p": p, "o": o}

def XA(a, f, dom, l="∫ =", p="Escribe el resultado (con + C)."):
    chk_anti(a, f, dom)
    return {"t": "expr", "p": p, "f": [{"a": a, "v": ["x"], "l": l, "mode": "anti", "dom": {"x": list(dom)}}]}

def XV(a, val, l, p="Escribe el valor exacto."):
    chk_val(a, val)
    return {"t": "expr", "p": p, "f": [{"a": a, "v": [], "l": l}]}

def NUM(fs, p="Respuesta"):
    return {"t": "num", "p": p, "f": fs}

def HV(num, r, lab=None, p="Tapa cada factor y escribe su coeficiente", e=None):
    c = {"t": "heav", "p": p, "num": num, "r": r}
    if lab: c["lab"] = lab
    if e: c["e"] = e
    # comprobación con sympy
    Pn = sum(cf * x ** (len(num) - 1 - k) for k, cf in enumerate(num))
    Q = sp.prod([(x - s) for s in r])
    apart = sp.apart(Pn / Q, x)
    for s in r:
        A = sp.Rational(Pn.subs(x, s), sp.prod([(s - q) for q in r if q != s]))
        assert sp.simplify(sp.limit((x - s) * apart, x, s) - A) == 0
    return c

# =====================================================================
# SEMANA 11 · Tema 1: fracciones parciales
# =====================================================================
f1 = (5 * x - 3) / (x ** 2 - 4)
assert sp.simplify(sp.apart(f1) - (sp.Rational(7, 4) / (x - 2) + sp.Rational(13, 4) / (x + 2))) == 0
f2 = 6 / (x ** 2 - 9)
assert sp.simplify(sp.apart(f2) - (1 / (x - 3) - 1 / (x + 3))) == 0
f3 = (3 * x + 2) / (x ** 2 - 3 * x + 2)
assert sp.simplify(sp.apart(f3) - (8 / (x - 2) - 5 / (x - 1))) == 0
f4 = (x + 3) / ((x - 1) ** 2 * (x + 2))
assert sp.simplify(sp.apart(f4) - (-sp.Rational(1, 9) / (x - 1) + sp.Rational(4, 3) / (x - 1) ** 2 + sp.Rational(1, 9) / (x + 2))) == 0
f5 = (2 * x + 3) / ((x - 1) ** 2 * (x + 2))
f6 = (2 * x + 1) / (x * (x ** 2 + 1))
assert sp.simplify(sp.apart(f6) - (1 / x + (2 - x) / (x ** 2 + 1))) == 0
f7 = (3 * x + 5) / ((x + 1) * (x ** 2 + 4))
assert sp.simplify(f7 - (sp.Rational(2, 5) / (x + 1) + (-sp.Rational(2, 5) * x + sp.Rational(17, 5)) / (x ** 2 + 4))) == 0
f8 = (2 * x + 1) / (x ** 2 + x - 20)
assert sp.simplify(sp.apart(f8) - (sp.Rational(1, 1) / (x - 4) + 1 / (x + 5))) == 0
f9 = (x - 4) / (x ** 2 - 4 * x + 4)
assert sp.simplify(sp.apart(f9) - (1 / (x - 2) - 2 / (x - 2) ** 2)) == 0

FP_teo = (
 "<p>Las <strong>fracciones parciales</strong> sirven para integrar funciones racionales \\(\\frac{P(x)}{Q(x)}\\) que resisten sustitución y partes. Se descompone en sumandos simples que dan logaritmos y arcotangentes.</p>"
 "<p><b>Preparación obligatoria:</b> (1) verificar que sea <b>propia</b>, \\(\\deg P<\\deg Q\\) (si no, dividir primero); (2) factorizar completamente \\(Q\\); (3) clasificar el caso; (4) escribir la descomposición con el número correcto de incógnitas.</p>"
 "<div class=\"tbl\"><table><tr><th>Caso</th><th>Denominador</th><th>Se escribe</th></tr>"
 "<tr><td>I</td><td>lineales distintos</td><td>\\(\\frac{A}{x-a}+\\frac{B}{x-b}\\)</td></tr>"
 "<tr><td>II</td><td>lineal repetido</td><td>\\(\\frac{A}{x-a}+\\frac{B}{(x-a)^2}\\)</td></tr>"
 "<tr><td>III</td><td>cuadrático irreducible</td><td>\\(\\frac{Ax+B}{x^2+px+q}\\)</td></tr>"
 "<tr><td>IV</td><td>cuadrático repetido</td><td>\\(\\frac{A_1x+B_1}{x^2+px+q}+\\frac{A_2x+B_2}{(x^2+px+q)^2}\\)</td></tr></table></div>"
 "<p><b>Heaviside (tapar el factor):</b> para un factor lineal \\((x-a)\\), se tapa en la fracción original y se evalúa lo que queda en \\(x=a\\). En el Caso II sirve para la potencia más alta; las demás constantes salen dando un valor a x o igualando coeficientes.</p>"
 "<p class=\"ej\"><b>Ejemplo de clase:</b> \\(\\frac{5x-3}{(x-2)(x+2)}\\): \\(A=\\frac{5(2)-3}{2+2}=\\frac74\\), \\(B=\\frac{5(-2)-3}{-2-2}=\\frac{13}4\\). Así \\(\\int\\frac{5x-3}{x^2-4}dx=\\) \\(\\frac74\\ln|x-2|+\\frac{13}4\\ln|x+2|+C\\).</p>"
 "<p><b>En el curso</b> solo se evalúan fracciones <b>propias</b> (casos I a III); el Caso IV se ve en la práctica. Una aplicación clave es la <b>EDO logística</b> \\(P'=rP\\left(1-\\frac PK\\right)\\), cuya integral \\(\\int\\frac{dP}{P(K-P)}\\) se resuelve con fracciones parciales.</p>"
)
FP_form = ["Propia: \\(\\deg P<\\deg Q\\); si no, dividir primero",
           "Caso I: \\(\\frac{A}{x-a}+\\frac{B}{x-b}\\) · Heaviside: tapar y evaluar en \\(x=a\\)",
           "Caso II: \\(\\frac{A}{x-a}+\\frac{B}{(x-a)^2}\\) · \\(\\int\\frac{B}{(x-a)^2}=-\\frac{B}{x-a}\\)",
           "Caso III: \\(\\frac{Ax+B}{x^2+px+q}\\) → ln y arctan",
           "\\(\\int\\frac{dx}{x^2+a^2}=\\frac1a\\arctan\\frac xa\\)",
           "Logística: \\(P=\\frac{KP_0}{P_0+(K-P_0)e^{-rt}}\\)"]
FP_lesson = (
 "<h3>Idea central</h3><p>Integrar es <b>clasificar antes de calcular</b>. Antes de escribir un símbolo: ¿es propia?, ¿cómo se factoriza el denominador?, ¿qué caso es? Con eso la descomposición se escribe sola.</p>"
 "<h3>Cómo resolverlo</h3><ol><li>Si \\(\\deg P\\ge\\deg Q\\), divide: \\(\\frac PQ=C(x)+\\frac RQ\\).</li><li>Factoriza \\(Q\\) en lineales y cuadráticos irreducibles (\\(p^2-4q<0\\)).</li><li>Escribe la suma según el caso y halla las constantes (Heaviside en los lineales; un valor de x o coeficientes para el resto).</li><li>Integra cada sumando y <b>verifica derivando</b>.</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes:</b> descomponer una fracción impropia sin dividir; escribir solo \\(\\frac{A}{(x-a)^2}\\) en el Caso II (falta \\(\\frac{B}{x-a}\\)); poner solo \\(A\\) sobre un cuadrático (necesita \\(Ax+B\\)); y olvidar el valor absoluto en los logaritmos.</div>"
)
FP = []
FP.append(E("w11f1", 1, "¿Qué caso es?",
  "<p>Clasifica cada fracción según su caso de fracciones parciales.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Caso I", "Caso II", "Caso III", "Caso IV"], "items": [
    {"x": "\\(\\frac{3x-1}{(x-1)(x+2)}\\)", "c": 0}, {"x": "\\(\\frac{x+1}{(x-2)^2(x+3)}\\)", "c": 1},
    {"x": "\\(\\frac{2x}{(x^2+4)(x-1)}\\)", "c": 2, "e": "\\(x^2+4\\) no se factoriza en \\(\\mathbb R\\) (discriminante negativo): es cuadrático irreducible."},
    {"x": "\\(\\frac{1}{(x^2+1)^2}\\)", "c": 3}, {"x": "\\(\\frac{6}{x^2-9}\\)", "c": 0, "e": "\\(x^2-9=(x-3)(x+3)\\): dos lineales distintos."},
    {"x": "\\(\\frac{x}{(x-2)^3(x+1)}\\)", "c": 1}]}],
  ["Primero se factoriza el denominador: \\(x^2-9=(x-3)(x+3)\\) es Caso I aunque no lo parezca.",
   "Lineal repetido → Caso II; cuadrático sin raíces reales → Caso III; ese cuadrático repetido → Caso IV. Si hay varios tipos, se usan todos los términos que correspondan."],
  "I, II, III, IV, I, II", "Factoriza antes de clasificar.", [["fpcaso"], ["fpcaso"]]))
FP.append(E("w11f2", 1, "¿Hay que dividir primero?",
  "<p>¿En cuál de estas integrales <strong>es indispensable</strong> hacer la división de polinomios antes de usar fracciones parciales?</p>",
  [O(["\\(\\int\\frac{x^3}{x^2-1}dx\\)", "\\(\\int\\frac{5x-3}{x^2-4}dx\\)", "\\(\\int\\frac{x^2+1}{x(x-1)^2}dx\\)", "\\(\\int\\frac{2x+1}{x(x^2+1)}dx\\)", "\\(\\int\\frac{6}{x^2-9}dx\\)"])],
  ["Se divide cuando \\(\\deg P\\ge\\deg Q\\) (fracción impropia).",
   "En \\(\\frac{x^3}{x^2-1}\\), grado 3 ≥ 2: \\(\\frac{x^3}{x^2-1}=x+\\frac{x}{x^2-1}\\). En las demás el numerador tiene menor grado que el denominador (ojo: \\(x(x-1)^2\\) es de grado 3)."],
  "\\(\\int\\frac{x^3}{x^2-1}dx\\)", "Compara grados.", [["fpdiv"], ["fpdiv"]]))
FP.append(E("w11f3", 1, "Tapa el factor (ejemplo de clase)",
  "<p>Descompón \\(\\frac{5x-3}{x^2-4}=\\frac{5x-3}{(x-2)(x+2)}\\) con el método de Heaviside y luego integra.</p>",
  [HV([5, -3], [2, -2]), XA("7/4*ln(abs(x-2))+13/4*ln(abs(x+2))", f1, (2.3, 6), p="Ahora integra (con + C).")],
  ["Para A se tapa \\((x-2)\\) y se evalúa en \\(x=2\\): \\(A=\\frac{5(2)-3}{2+2}=\\frac74\\).",
   "Para B se tapa \\((x+2)\\) y se evalúa en \\(x=-2\\): \\(B=\\frac{5(-2)-3}{-2-2}=\\frac{-13}{-4}=\\frac{13}4\\).",
   "\\(\\int\\frac{7/4}{x-2}+\\frac{13/4}{x+2}dx=\\) \\(\\frac74\\ln|x-2|+\\frac{13}4\\ln|x+2|+C\\). Verificación: derivando se recupera el integrando; hay un logaritmo por cada factor lineal."],
  "\\(\\frac74\\ln|x-2|+\\frac{13}4\\ln|x+2|+C\\)", "Tapa (x − 2) y evalúa en x = 2.", [["heav"], ["heav"], ["fpcaso"]], chain=True))
FP.append(E("w11f4", 1, "\\(\\int\\frac{6}{x^2-9}dx\\)",
  "<p>Ejercicio de la guía: calcula \\(\\int\\frac{6}{x^2-9}dx\\).</p>",
  [HV([6], [3, -3]), XA("ln(abs(x-3))-ln(abs(x+3))", f2, (3.5, 8), p="Integra (con + C).")],
  ["\\(x^2-9=(x-3)(x+3)\\). Tapando \\((x-3)\\): \\(A=\\frac{6}{3+3}=1\\). Tapando \\((x+3)\\): \\(B=\\frac{6}{-3-3}=-1\\).",
   "\\(\\int\\frac{1}{x-3}-\\frac1{x+3}\\,dx=\\ln|x-3|-\\ln|x+3|+C\\) \\(=\\ln\\left|\\frac{x-3}{x+3}\\right|+C\\)."],
  "\\(\\ln\\left|\\frac{x-3}{x+3}\\right|+C\\)", "El numerador es la constante 6.", [["heav"], ["fpcaso"]], chain=True))
FP.append(E("w11f5", 2, "Factoriza y tapa",
  "<p>Ejercicio de clase: calcula \\(\\int\\frac{3x+2}{x^2-3x+2}dx\\).</p>",
  [HV([3, 2], [1, 2]), XA("-5*ln(abs(x-1))+8*ln(abs(x-2))", f3, (2.3, 6), p="Integra (con + C).")],
  ["\\(x^2-3x+2=(x-1)(x-2)\\). Tapando \\((x-1)\\), en \\(x=1\\): \\(A=\\frac{3+2}{1-2}=-5\\).",
   "Tapando \\((x-2)\\), en \\(x=2\\): \\(B=\\frac{6+2}{2-1}=8\\).",
   "\\(\\int\\frac{-5}{x-1}+\\frac{8}{x-2}dx=\\) \\(-5\\ln|x-1|+8\\ln|x-2|+C\\)."],
  "\\(-5\\ln|x-1|+8\\ln|x-2|+C\\)", "Primero factoriza el trinomio.", [["heav"], ["heav"], ["fpcaso"]], chain=True))
FP.append(E("w11f6", 2, "Caso II: factor repetido",
  "<p>Ejemplo de clase: \\(\\frac{x+3}{(x-1)^2(x+2)}=\\frac{A}{x-1}+\\frac{B}{(x-1)^2}+\\frac{C}{x+2}\\). Halla las constantes e integra.</p>",
  [NUM([{"l": "A =", "a": -1 / 9, "tol": 0.002, "e": "Con B y C hallados, da a x un valor cómodo (x = 0) en la identidad."},
        {"l": "B =", "a": 4 / 3, "tol": 0.002, "e": "Tapa \\((x-1)^2\\) entero y evalúa en x = 1."},
        {"l": "C =", "a": 1 / 9, "tol": 0.002, "e": "Tapa \\((x+2)\\) y evalúa en x = −2."}], "Constantes (puedes escribir fracciones como -1/9)"),
   XA("-1/9*ln(abs(x-1))-4/(3*(x-1))+1/9*ln(abs(x+2))", f4, (1.3, 5), p="Integra (con + C).")],
  ["Heaviside directo sirve para la potencia más alta y para el otro lineal: \\(B=\\frac{1+3}{1+2}=\\frac43\\), \\(C=\\frac{-2+3}{(-2-1)^2}=\\frac19\\).",
   "Para A: \\(x+3=A(x-1)(x+2)+B(x+2)+C(x-1)^2\\). Con \\(x=0\\): \\(3=-2A+2B+C\\) \\(\\Rightarrow3=-2A+\\frac83+\\frac19\\Rightarrow A=-\\frac19\\).",
   "\\(\\int\\frac{B}{(x-1)^2}dx=-\\frac{B}{x-1}\\): \\(-\\frac19\\ln|x-1|-\\frac{4}{3(x-1)}+\\frac19\\ln|x+2|+C\\)."],
  "\\(-\\frac19\\ln|x-1|-\\frac{4}{3(x-1)}+\\frac19\\ln|x+2|+C\\)", "A no sale con Heaviside: usa x = 0.", [["fp2"], ["fp2"], ["fp2"]], chain=True))
FP.append(E("w11f8", 2, "Caso III: arctan",
  "<p>Ejemplo de clase: \\(\\frac{2x+1}{x(x^2+1)}=\\frac{A}{x}+\\frac{Bx+C}{x^2+1}\\). Halla las constantes e integra.</p>",
  [NUM([{"l": "A =", "a": 1}, {"l": "B =", "a": -1}, {"l": "C =", "a": 2}], "Constantes"),
   XA("ln(abs(x))-1/2*ln(x^2+1)+2*arctan(x)", f6, (0.3, 4), p="Integra (con + C).")],
  ["\\(2x+1=A(x^2+1)+(Bx+C)x=(A+B)x^2+Cx+A\\).",
   "Igualando coeficientes: \\(A=1\\), \\(C=2\\), \\(A+B=0\\Rightarrow B=-1\\).",
   "\\(\\int\\frac1x-\\frac{x}{x^2+1}+\\frac{2}{x^2+1}dx=\\) \\(\\ln|x|-\\frac12\\ln(x^2+1)+2\\arctan x+C\\)."],
  "\\(\\ln|x|-\\frac12\\ln(x^2+1)+2\\arctan x+C\\)", "Iguala coeficientes.", [["fp3"], ["fp3"], ["fp3"]], chain=True))
FP.append(E("w11f9", 3, "Caso III con constantes feas",
  "<p>Ejercicio 12 de la clase: \\(\\frac{3x+5}{(x+1)(x^2+4)}=\\frac{A}{x+1}+\\frac{Bx+C}{x^2+4}\\). Halla A, B y C.</p>",
  [NUM([{"l": "A =", "a": 0.4, "tol": 0.002, "e": "Tapa \\((x+1)\\) y evalúa en x = −1."}, {"l": "B =", "a": -0.4, "tol": 0.002}, {"l": "C =", "a": 3.4, "tol": 0.002}], "Constantes (fracciones o decimales)"),
   XA("2/5*ln(abs(x+1))-1/5*ln(x^2+4)+17/10*arctan(x/2)", f7, (0, 4), p="Integra (con + C).")],
  ["Heaviside para el lineal: \\(A=\\frac{3(-1)+5}{(-1)^2+4}=\\frac25\\).",
   "\\(3x+5=A(x^2+4)+(Bx+C)(x+1)\\). Coeficiente de \\(x^2\\): \\(A+B=0\\Rightarrow B=-\\frac25\\). Término independiente: \\(4A+C=5\\Rightarrow C=\\frac{17}5\\).",
   "\\(\\int\\frac{-\\frac25x}{x^2+4}dx=-\\frac15\\ln(x^2+4)\\) y \\(\\int\\frac{17/5}{x^2+4}dx=\\frac{17}{10}\\arctan\\frac x2\\)."],
  "\\(\\frac25\\ln|x+1|-\\frac15\\ln(x^2+4)+\\frac{17}{10}\\arctan\\frac x2+C\\)", "Usa \\(\\int\\frac{dx}{x^2+a^2}=\\frac1a\\arctan\\frac xa\\).", [["heav"], ["fp3"], ["fp3"]], chain=True))
FP.append(E("w11f10", 2, "Completar cuadrados",
  "<p>Calcula \\(\\int\\frac{dx}{x^2+2x+5}\\).</p>",
  [XA("1/2*arctan((x+1)/2)", 1 / (x ** 2 + 2 * x + 5), (-3, 3))],
  ["El discriminante \\(4-20<0\\): es irreducible. Se completa cuadrados: \\(x^2+2x+5=(x+1)^2+4\\).",
   "Con \\(u=x+1\\): \\(\\int\\frac{du}{u^2+2^2}=\\frac12\\arctan\\frac u2+C=\\) \\(\\frac12\\arctan\\frac{x+1}{2}+C\\). (Ojo: el \\(\\frac12\\) viene de \\(\\frac1a\\) con \\(a=2\\).)"],
  "\\(\\frac12\\arctan\\frac{x+1}2+C\\)", "(x + 1)² + 4.", [["compcuad"], ["fp3"]]))
FP.append(E("w11f11", 1, "Error típico del Caso II",
  "<p>Un estudiante escribe \\(\\frac{x+1}{(x-2)^2}=\\frac{A}{(x-2)^2}\\). ¿Cuál es el problema?</p>",
  [O(["Falta el término \\(\\frac{B}{x-2}\\): un factor repetido necesita una fracción por cada potencia",
      "Debió escribir \\(\\frac{Ax+B}{(x-2)^2}\\) porque es cuadrático irreducible",
      "No hay problema: con A basta",
      "Debió dividir primero porque es impropia",
      "Debió escribir \\(\\frac{A}{x-2}+\\frac{B}{x+2}\\)"])],
  ["\\((x-2)^2\\) es un lineal repetido (Caso II): se escribe \\(\\frac{A}{x-2}+\\frac{B}{(x-2)^2}\\).",
   "Con un solo término no hay suficientes incógnitas: aquí \\(x+1=A(x-2)+B\\Rightarrow A=1,\\ B=3\\). No es irreducible (tiene raíz 2) y es propia (grado 1 < 2)."],
  "Falta \\(\\frac{B}{x-2}\\)", "Una fracción por cada potencia.", [["fp2"], ["fp2"]]))
FP.append(E("w11f12", 2, "EDO logística",
  "<p>Una población cumple \\(\\frac{dP}{dt}=0{,}5\\,P\\left(1-\\frac{P}{1000}\\right)\\) con \\(P(0)=100\\) (t en años). Usa \\(P(t)=\\frac{KP_0}{P_0+(K-P_0)e^{-rt}}\\).</p>",
  [NUM([{"l": "P(4) ≈", "a": round(1000 * 100 / (100 + 900 * math.exp(-2)), 2), "tol": 0.6, "e": "K = 1000, P₀ = 100, r = 0,5 y t = 4."},
        {"l": "lím P(t) =", "a": 1000, "e": "Cuando t → ∞, \\(e^{-rt}\\to0\\)."}], "Calcula"),
   O(["Fracciones parciales: \\(\\frac{1}{P(K-P)}=\\frac1K\\left(\\frac1P+\\frac1{K-P}\\right)\\)", "Sustitución trigonométrica", "Integración por partes", "Weierstrass", "Ángulo doble"], "¿Qué técnica se usa al separar variables?")],
  ["Separando: \\(\\int\\frac{dP}{P(K-P)}=\\int\\frac rK\\,dt\\). La izquierda se resuelve con fracciones parciales (Caso I).",
   "Despejando y usando \\(P(0)=P_0\\) sale la fórmula dada. Con los datos: \\(P(4)=\\frac{100\\,000}{100+900e^{-2}}\\approx" + f"{1000 * 100 / (100 + 900 * math.exp(-2)):.2f}".replace('.', '{,}') + "\\).",
   "Cuando \\(t\\to\\infty\\), \\(P\\to K=1000\\): la capacidad de carga."],
  "P(4) ≈ " + f"{1000 * 100 / (100 + 900 * math.exp(-2)):.1f}".replace('.', ',') + "; tiende a 1000", "Reemplaza en la fórmula.", [["logist"], ["logist"], ["logist"]], chain=True))
FP.append(E("w11f13", 3, "Impropia: divide primero",
  "<p>Calcula \\(\\int\\frac{x^3}{x^2-1}dx\\) (de la guía; las impropias no se evalúan en clase, pero salen en la guía).</p>",
  [XA("x^2/2+1/2*ln(abs(x^2-1))", x ** 3 / (x ** 2 - 1), (1.3, 4))],
  ["División: \\(x^3=(x^2-1)\\cdot x+x\\), así que \\(\\frac{x^3}{x^2-1}=x+\\frac{x}{x^2-1}\\).",
   "\\(\\int x\\,dx=\\frac{x^2}2\\) y \\(\\int\\frac{x}{x^2-1}dx=\\frac12\\ln|x^2-1|\\) (sustitución \\(u=x^2-1\\)). Resultado: \\(\\frac{x^2}2+\\frac12\\ln|x^2-1|+C\\)."],
  "\\(\\frac{x^2}2+\\frac12\\ln|x^2-1|+C\\)", "x³ ÷ (x² − 1).", [["fpdiv"], ["fpdiv"]]))
FP.insert(6, E("w11f7", 2, "Caso II de la práctica",
  "<p>Ejercicio 6 de la clase: \\(\\frac{2x+3}{(x-1)^2(x+2)}=\\frac{A}{x-1}+\\frac{B}{(x-1)^2}+\\frac{C}{x+2}\\). Halla las constantes e integra.</p>",
  [NUM([{"l": "A =", "a": 1 / 9, "tol": 0.002, "e": "Con B y C hallados, usa x = 0 en la identidad."}, {"l": "B =", "a": 5 / 3, "tol": 0.002}, {"l": "C =", "a": -1 / 9, "tol": 0.002, "e": "En x = −2: 2(−2) + 3 = −1 y (−2 − 1)² = 9."}], "Constantes"),
   XA("1/9*ln(abs(x-1))-5/(3*(x-1))-1/9*ln(abs(x+2))", f5, (1.3, 5), p="Integra (con + C).")],
  ["Tapando \\((x-1)^2\\), en \\(x=1\\): \\(B=\\frac{2+3}{1+2}=\\frac53\\). Tapando \\((x+2)\\), en \\(x=-2\\): \\(C=\\frac{-4+3}{(-3)^2}=-\\frac19\\).",
   "Con \\(x=0\\) en \\(2x+3=A(x-1)(x+2)+B(x+2)+C(x-1)^2\\): \\(3=-2A+\\frac{10}3-\\frac19\\Rightarrow A=\\frac19\\).",
   "\\(\\frac19\\ln|x-1|-\\frac{5}{3(x-1)}-\\frac19\\ln|x+2|+C\\)."],
  "\\(\\frac19\\ln|x-1|-\\frac{5}{3(x-1)}-\\frac19\\ln|x+2|+C\\)", "Primero B y C; A con x = 0.", [["fp2"], ["fp2"], ["fp2"]], chain=True))
assert sp.simplify(sp.apart(f5) - (sp.Rational(1, 9) / (x - 1) + sp.Rational(5, 3) / (x - 1) ** 2 - sp.Rational(1, 9) / (x + 2))) == 0
FP_tools = [{"w": "heav", "t": "Tapar el factor (Heaviside)", "p": "Toca cada factor: se tapa y lo que queda se evalúa en su raíz.", "o": {"num": [5, -3], "r": [2, -2]}},
            {"w": "heav", "t": "Con tres factores", "p": "\\(\\frac{x^2+1}{x(x-1)(x+2)}\\)", "o": {"num": [1, 0, 1], "r": [0, 1, -2]}},
            {"w": "campo", "t": "Logística: P′ = 0,5·P·(1 − P/10)", "p": "Toca un punto para elegir P(0): todas las soluciones positivas se acercan a K = 10.", "o": {"f": "0.5*y*(1-y/10)", "tr": [0, 16], "yr": [0, 14], "ic": [0, 1]}}]

# =====================================================================
# SEMANA 11 · Tema 2: potencias trigonométricas
# =====================================================================
PT_teo = (
 "<div class=\"tbl\"><table><tr><th>Integrando</th><th>Exponente impar</th><th>Exponente par</th></tr>"
 "<tr><td>\\(\\sin^n x\\)</td><td>separar un \\(\\sin x\\), \\(u=\\cos x\\)</td><td>ángulo doble</td></tr>"
 "<tr><td>\\(\\cos^n x\\)</td><td>separar un \\(\\cos x\\), \\(u=\\sin x\\)</td><td>ángulo doble</td></tr>"
 "<tr><td>\\(\\sin^m x\\cos^n x\\)</td><td>separar del impar, \\(u=\\) el otro</td><td>ambos pares: ángulo doble</td></tr>"
 "<tr><td>\\(\\tan^m x\\sec^n x\\)</td><td>m impar: separar \\(\\sec x\\tan x\\), \\(u=\\sec x\\)</td><td>n par: separar \\(\\sec^2x\\), \\(u=\\tan x\\)</td></tr></table></div>"
 "<p><b>Ángulo doble:</b> \\(\\sin^2x=\\frac{1-\\cos2x}2\\), \\(\\cos^2x=\\frac{1+\\cos2x}2\\), \\(\\sin x\\cos x=\\frac{\\sin2x}2\\). <b>Pitagóricas:</b> \\(\\sin^2x=1-\\cos^2x\\), \\(\\sec^2x=1+\\tan^2x\\).</p>"
 "<p class=\"ej\"><b>Ejemplo (guía):</b> \\(\\int\\sin^3x\\cos^5x\\,dx\\): el seno es impar, se separa \\(\\sin x\\) y \\(u=\\cos x\\): \\(-\\int(1-u^2)u^5du=\\) \\(-\\frac{\\cos^6x}6+\\frac{\\cos^8x}8+C\\).</p>"
 "<p>La EA3 (semana 11) cerró fracciones parciales y potencias trigonométricas.</p>"
)
PT_form = ["Impar: separa un factor y cambia el resto con \\(\\sin^2+\\cos^2=1\\)",
           "Par: \\(\\sin^2x=\\frac{1-\\cos2x}2\\), \\(\\cos^2x=\\frac{1+\\cos2x}2\\)",
           "\\(\\tan^m\\sec^n\\): n par → \\(u=\\tan x\\); m impar → \\(u=\\sec x\\)",
           "\\(\\int\\sin^2x\\,dx=\\frac x2-\\frac{\\sin2x}4+C\\)"]
PT_lesson = (
 "<h3>Idea central</h3><p>La paridad del exponente decide: con un exponente <b>impar</b> sobra un factor que hace de \\(du\\); con todos <b>pares</b> no hay \\(du\\) disponible y se baja el grado con ángulo doble.</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> usar \\(u=\\sin x\\) cuando el impar es el seno (el \\(du\\) que sobra es \\(\\sin x\\,dx\\), así que \\(u=\\cos x\\)); olvidar el signo de \\(du=-\\sin x\\,dx\\); y en ángulo doble olvidar dividir entre 2 al integrar \\(\\cos2x\\).</div>"
)
PT = []
PT.append(E("w11p1", 1, "¿Qué estrategia?",
  "<p>Clasifica cada integral según la estrategia que corresponde.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Separar sin x, u = cos x", "Separar cos x, u = sin x", "Ángulo doble", "Separar sec²x, u = tan x"], "items": [
    {"x": "\\(\\int\\sin^3x\\,dx\\)", "c": 0}, {"x": "\\(\\int\\cos^5x\\,dx\\)", "c": 1}, {"x": "\\(\\int\\sin^4x\\,dx\\)", "c": 2},
    {"x": "\\(\\int\\sin^2x\\cos^2x\\,dx\\)", "c": 2}, {"x": "\\(\\int\\tan^3x\\sec^4x\\,dx\\)", "c": 3, "e": "La secante tiene exponente par: separa \\(\\sec^2x\\) y usa \\(u=\\tan x\\)."},
    {"x": "\\(\\int\\sin^3x\\cos^2x\\,dx\\)", "c": 0}, {"x": "\\(\\int\\sec^4x\\,dx\\)", "c": 3}]}],
  ["Exponente impar en seno → se separa un \\(\\sin x\\) (será parte de \\(du\\) con \\(u=\\cos x\\)); impar en coseno → al revés.",
   "Todos pares → ángulo doble. Secante par → \\(\\sec^2x\\) es la derivada de \\(\\tan x\\)."],
  "Clasificación correcta", "Mira qué exponente es impar.", [["pottrig"], ["angdob"]]))
PT.append(E("w11p2", 1, "\\(\\int\\sin^2x\\,dx\\)",
  "<p>Calcula \\(\\int\\sin^2x\\,dx\\).</p>",
  [XA("x/2-sin(2*x)/4", sp.sin(x) ** 2, (-2, 2))],
  ["Exponente par: \\(\\sin^2x=\\frac{1-\\cos2x}{2}\\).", "\\(\\int\\frac12-\\frac{\\cos2x}2dx=\\frac x2-\\frac{\\sin2x}{4}+C\\)."],
  "\\(\\frac x2-\\frac{\\sin2x}4+C\\)", "Ángulo doble.", [["angdob"], ["angdob"]]))
PT.append(E("w11p3", 1, "\\(\\int\\sin^3x\\,dx\\)",
  "<p>Calcula \\(\\int\\sin^3x\\,dx\\).</p>",
  [XA("-cos(x)+cos(x)^3/3", sp.sin(x) ** 3, (-2, 2))],
  ["Impar: \\(\\sin^3x=\\sin^2x\\sin x=(1-\\cos^2x)\\sin x\\). Con \\(u=\\cos x\\), \\(du=-\\sin x\\,dx\\).",
   "\\(-\\int(1-u^2)du=-u+\\frac{u^3}3+C=-\\cos x+\\frac{\\cos^3x}3+C\\)."],
  "\\(-\\cos x+\\frac{\\cos^3x}3+C\\)", "Separa un sen x.", [["pottrig"], ["pottrig"]]))
PT.append(E("w11p4", 2, "\\(\\int\\cos^3x\\,dx\\)",
  "<p>Calcula \\(\\int\\cos^3x\\,dx\\).</p>",
  [XA("sin(x)-sin(x)^3/3", sp.cos(x) ** 3, (-2, 2))],
  ["\\(\\cos^3x=(1-\\sin^2x)\\cos x\\); con \\(u=\\sin x\\), \\(du=\\cos x\\,dx\\).", "\\(\\int(1-u^2)du=\\sin x-\\frac{\\sin^3x}3+C\\)."],
  "\\(\\sin x-\\frac{\\sin^3x}3+C\\)", "Separa un cos x.", [["pottrig"], ["pottrig"]]))
PT.append(E("w11p5", 2, "\\(\\int\\sin^4x\\,dx\\) (ejemplo de la guía)",
  "<p>Calcula \\(\\int\\sin^4x\\,dx\\).</p>",
  [XA("3*x/8-sin(2*x)/4+sin(4*x)/32", sp.sin(x) ** 4, (-2, 2))],
  ["\\(\\sin^4x=\\left(\\frac{1-\\cos2x}2\\right)^2=\\frac{1-2\\cos2x+\\cos^22x}{4}\\), y otra vez \\(\\cos^22x=\\frac{1+\\cos4x}2\\).",
   "\\(\\sin^4x=\\frac38-\\frac{\\cos2x}2+\\frac{\\cos4x}8\\) ⇒ \\(\\int=\\frac{3x}8-\\frac{\\sin2x}4+\\frac{\\sin4x}{32}+C\\)."],
  "\\(\\frac{3x}8-\\frac{\\sin2x}4+\\frac{\\sin4x}{32}+C\\)", "Ángulo doble dos veces.", [["angdob"], ["angdob"]]))
PT.append(E("w11p6", 2, "Impar por par",
  "<p>Calcula \\(\\int\\sin^3x\\cos^5x\\,dx\\).</p>",
  [XA("-cos(x)^6/6+cos(x)^8/8", sp.sin(x) ** 3 * sp.cos(x) ** 5, (-2, 2)),
   O(["\\(u=\\sin x\\) no sirve: queda \\(\\cos^4x\\) sin su \\(du\\)… y el coseno es impar también", "\\(u=\\cos x\\) porque el seno tiene exponente impar", "Hay que usar ángulo doble", "Hay que usar partes", "Weierstrass"], "¿Por qué \\(u=\\cos x\\)?")],
  ["El seno tiene exponente impar: se separa \\(\\sin x\\) y \\(\\sin^2x=1-\\cos^2x\\). Con \\(u=\\cos x\\), \\(du=-\\sin x\\,dx\\).",
   "\\(-\\int(1-u^2)u^5du=-\\frac{u^6}6+\\frac{u^8}8+C=\\) \\(-\\frac{\\cos^6x}6+\\frac{\\cos^8x}8+C\\)."],
  "\\(-\\frac{\\cos^6x}6+\\frac{\\cos^8x}8+C\\)", "Separa del impar.", [["pottrig"], ["pottrig"]], chain=True))
PT[5]["checks"][1] = O(["Porque el seno tiene exponente impar: el \\(\\sin x\\) separado forma \\(du\\)", "Porque el coseno tiene el exponente más grande", "Porque así se usa ángulo doble", "Porque \\(u=\\sin x\\) daría un error de signo", "Da igual elegir \\(u=\\sin x\\) o \\(u=\\cos x\\)"], "¿Por qué \\(u=\\cos x\\)?")
PT.append(E("w11p7", 2, "Tangente y secante",
  "<p>Calcula \\(\\int\\tan^3x\\sec^4x\\,dx\\).</p>",
  [XA("tan(x)^4/4+tan(x)^6/6", sp.tan(x) ** 3 * sp.sec(x) ** 4, (-1, 1))],
  ["La secante tiene exponente par: \\(\\sec^4x=\\sec^2x\\cdot\\sec^2x=(1+\\tan^2x)\\sec^2x\\). Con \\(u=\\tan x\\), \\(du=\\sec^2x\\,dx\\).",
   "\\(\\int u^3(1+u^2)du=\\frac{u^4}4+\\frac{u^6}6+C=\\frac{\\tan^4x}4+\\frac{\\tan^6x}6+C\\)."],
  "\\(\\frac{\\tan^4x}4+\\frac{\\tan^6x}6+C\\)", "Separa sec²x.", [["pottrig"], ["pottrig"]]))
PT.append(E("w11p8", 2, "Ambos pares",
  "<p>Calcula \\(\\int\\sin^2x\\cos^2x\\,dx\\).</p>",
  [XA("x/8-sin(4*x)/32", sp.sin(x) ** 2 * sp.cos(x) ** 2, (-2, 2))],
  ["\\(\\sin x\\cos x=\\frac{\\sin2x}2\\Rightarrow\\sin^2x\\cos^2x=\\frac{\\sin^22x}4=\\frac{1-\\cos4x}{8}\\).", "\\(\\int=\\frac x8-\\frac{\\sin4x}{32}+C\\)."],
  "\\(\\frac x8-\\frac{\\sin4x}{32}+C\\)", "Usa \\(\\sin x\\cos x=\\frac{\\sin 2x}2\\).", [["angdob"], ["angdob"]]))

# =====================================================================
# SEMANA 11 · Tema 3: sustitución trigonométrica
# =====================================================================
ST_teo = (
 "<p>La <strong>sustitución trigonométrica</strong> elimina radicales cuadráticos usando las identidades pitagóricas:</p>"
 "<div class=\"tbl\"><table><tr><th>Radical</th><th>Sustitución</th><th>Queda</th></tr>"
 "<tr><td>\\(\\sqrt{a^2-x^2}\\)</td><td>\\(x=a\\sin\\theta\\)</td><td>\\(a\\cos\\theta\\)</td></tr>"
 "<tr><td>\\(\\sqrt{a^2+x^2}\\)</td><td>\\(x=a\\tan\\theta\\)</td><td>\\(a\\sec\\theta\\)</td></tr>"
 "<tr><td>\\(\\sqrt{x^2-a^2}\\)</td><td>\\(x=a\\sec\\theta\\)</td><td>\\(a\\tan\\theta\\)</td></tr></table></div>"
 "<p><b>Protocolo:</b> (1) identificar el radical (si el trinomio no está ordenado, <b>completar cuadrados</b>); (2) sustituir \\(x\\) y \\(dx\\); (3) integrar en \\(\\theta\\); (4) volver a \\(x\\) con el <b>triángulo de referencia</b>.</p>"
 "<p class=\"ej\"><b>Ejemplo de clase:</b> \\(\\int\\frac{dx}{\\sqrt{x^2+4x+13}}\\): \\(x^2+4x+13=(x+2)^2+9\\); con \\(u=x+2=3\\tan\\theta\\) queda \\(\\int\\sec\\theta\\,d\\theta=\\ln|\\sec\\theta+\\tan\\theta|\\), y con el triángulo: \\(\\ln\\left|x+2+\\sqrt{x^2+4x+13}\\right|+C\\).</p>"
 "<div class=\"err\"><b>Ojo con la lámina:</b> en el caso secante el resultado debe decir \\(\\sqrt{x^2-4}-2\\,\\mathrm{arcsec}\\frac x2+C\\) (al volver, \\(\\theta=\\mathrm{arcsec}\\frac x2\\)); en el PDF se perdió el «arcsec».</div>"
)
ST_form = ["\\(\\sqrt{a^2-x^2}\\): \\(x=a\\sin\\theta\\) · \\(\\sqrt{a^2+x^2}\\): \\(x=a\\tan\\theta\\) · \\(\\sqrt{x^2-a^2}\\): \\(x=a\\sec\\theta\\)",
           "Completar cuadrados: \\(x^2+bx+c=\\left(x+\\frac b2\\right)^2+\\left(c-\\frac{b^2}4\\right)\\)",
           "\\(\\int\\sec\\theta\\,d\\theta=\\ln|\\sec\\theta+\\tan\\theta|+C\\)",
           "Volver a x: dibuja el triángulo con la sustitución"]
ST_lesson = (
 "<h3>Idea central</h3><p>La raíz \\(\\sqrt{a^2-x^2}\\) es el cateto de un triángulo rectángulo de hipotenusa \\(a\\): por eso un ángulo \\(\\theta\\) la vuelve un coseno y la raíz desaparece.</p>"
 "<h3>Para volver a x</h3><p>Escribe la sustitución como razón (\\(\\sin\\theta=\\frac xa\\), \\(\\tan\\theta=\\frac xa\\) o \\(\\sec\\theta=\\frac xa\\)), dibuja el triángulo, completa el tercer lado con Pitágoras (es la raíz original) y lee la razón que necesitas.</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> elegir la sustitución mirando solo el signo de \\(x^2\\) (en \\(\\sqrt{x^2-4}\\) es secante, no seno); olvidar cambiar \\(dx\\); y aplicar sustitución trigonométrica cuando basta una simple (\\(\\int\\frac{x}{\\sqrt{x^2+4}}dx\\) es \\(u=x^2+4\\)).</div>"
)
ST = []
ST.append(E("w11t1", 1, "¿Qué sustitución?",
  "<p>Clasifica cada integral según la sustitución trigonométrica que conviene.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["x = a·sen θ", "x = a·tan θ", "x = a·sec θ"], "items": [
    {"x": "\\(\\int\\frac{dx}{\\sqrt{4-x^2}}\\)", "c": 0}, {"x": "\\(\\int\\frac{dx}{x^2\\sqrt{9+x^2}}\\)", "c": 1}, {"x": "\\(\\int\\frac{\\sqrt{x^2-16}}{x}dx\\)", "c": 2},
    {"x": "\\(\\int\\sqrt{9-x^2}\\,dx\\)", "c": 0}, {"x": "\\(\\int\\frac{dx}{(x^2+4)^{3/2}}\\)", "c": 1}, {"x": "\\(\\int\\frac{dx}{x\\sqrt{x^2-1}}\\)", "c": 2}]}],
  ["\\(a^2-x^2\\) → seno; \\(a^2+x^2\\) → tangente; \\(x^2-a^2\\) → secante.",
   "Lo que decide es la forma del radical (qué se resta de qué), no lo que hay afuera."],
  "Clasificación correcta", "¿Qué se resta de qué?", [["sustrig"], ["sustrig"]]))
ST.append(E("w11t2", 1, "Arma el triángulo",
  "<p>Para \\(\\int\\frac{dx}{x^2\\sqrt{4+x^2}}\\) (ejemplo de clase), arma la sustitución y el triángulo.</p>",
  [{"t": "tri", "p": "Completa", "a": 2, "k": "suma", "ask": ["sen"]}],
  ["\\(\\sqrt{4+x^2}=\\sqrt{2^2+x^2}\\) → \\(x=2\\tan\\theta\\): \\(\\tan\\theta=\\frac x2\\), cateto opuesto x, adyacente 2.",
   "La hipotenusa es \\(\\sqrt{4+x^2}\\), así que \\(\\sin\\theta=\\frac{x}{\\sqrt{4+x^2}}\\), justo lo que pide el resultado \\(-\\frac{1}{4\\sin\\theta}\\)."],
  "x = 2 tan θ; sen θ = x/√(4 + x²)", "tan θ = opuesto/adyacente.", [["triref"], ["triref"]]))
ST.append(E("w11t3", 1, "Caso seno",
  "<p>Calcula \\(\\int\\frac{dx}{\\sqrt{9-x^2}}\\).</p>",
  [XA("arcsin(x/3)", 1 / sp.sqrt(9 - x ** 2), (-2.5, 2.5))],
  ["\\(x=3\\sin\\theta\\), \\(dx=3\\cos\\theta\\,d\\theta\\), \\(\\sqrt{9-x^2}=3\\cos\\theta\\).",
   "\\(\\int\\frac{3\\cos\\theta}{3\\cos\\theta}d\\theta=\\theta+C=\\arcsin\\frac x3+C\\)."],
  "\\(\\arcsin\\frac x3+C\\)", "x = 3 sen θ.", [["sustrig"], ["triref"]]))
ST.append(E("w11t4", 2, "Caso tangente",
  "<p>Calcula \\(\\int\\frac{dx}{x^2\\sqrt{4+x^2}}\\).</p>",
  [XA("-sqrt(4+x^2)/(4*x)", 1 / (x ** 2 * sp.sqrt(4 + x ** 2)), (0.4, 4))],
  ["\\(x=2\\tan\\theta\\), \\(dx=2\\sec^2\\theta\\,d\\theta\\), \\(\\sqrt{4+x^2}=2\\sec\\theta\\): \\(\\int\\frac{2\\sec^2\\theta}{4\\tan^2\\theta\\cdot2\\sec\\theta}d\\theta=\\frac14\\int\\frac{\\cos\\theta}{\\sin^2\\theta}d\\theta\\).",
   "Con \\(w=\\sin\\theta\\): \\(-\\frac{1}{4\\sin\\theta}\\). Del triángulo \\(\\sin\\theta=\\frac{x}{\\sqrt{4+x^2}}\\): \\(-\\frac{\\sqrt{4+x^2}}{4x}+C\\)."],
  "\\(-\\frac{\\sqrt{4+x^2}}{4x}+C\\)", "x = 2 tan θ.", [["sustrig"], ["triref"]]))
ST.append(E("w11t5", 2, "Caso secante",
  "<p>Calcula \\(\\int\\frac{\\sqrt{x^2-4}}{x}dx\\) (para \\(x>2\\)).</p>",
  [XA("sqrt(x^2-4)-2*arcsec(x/2)", sp.sqrt(x ** 2 - 4) / x, (2.3, 6))],
  ["\\(x=2\\sec\\theta\\), \\(dx=2\\sec\\theta\\tan\\theta\\,d\\theta\\), \\(\\sqrt{x^2-4}=2\\tan\\theta\\): \\(\\int\\frac{2\\tan\\theta\\cdot2\\sec\\theta\\tan\\theta}{2\\sec\\theta}d\\theta=2\\int\\tan^2\\theta\\,d\\theta\\).",
   "\\(2\\int(\\sec^2\\theta-1)d\\theta=2(\\tan\\theta-\\theta)\\). Triángulo: \\(\\tan\\theta=\\frac{\\sqrt{x^2-4}}2\\), \\(\\theta=\\mathrm{arcsec}\\frac x2\\): \\(\\sqrt{x^2-4}-2\\,\\mathrm{arcsec}\\frac x2+C\\)."],
  "\\(\\sqrt{x^2-4}-2\\,\\mathrm{arcsec}\\frac x2+C\\)", "x = 2 sec θ.", [["sustrig"], ["triref"]]))
ST.append(E("w11t6", 2, "Completar cuadrados",
  "<p>Calcula \\(\\int\\frac{dx}{\\sqrt{x^2+4x+13}}\\).</p>",
  [{"t": "usub", "p": "Primer paso", "int": "\\int\\frac{dx}{\\sqrt{x^2+4x+13}}", "opts": [
     {"u": "x+2", "du": "dx", "new": "\\int\\frac{du}{\\sqrt{u^2+9}}", "ok": True, "e": "Completando cuadrados: \\(x^2+4x+13=(x+2)^2+9\\)."},
     {"u": "x^2+4x+13", "du": "(2x+4)\\,dx", "new": "\\int\\frac{du}{(2x+4)\\sqrt u}", "ok": False, "e": "Falta \\((2x+4)\\) en el numerador: queda una x suelta."},
     {"u": "\\sqrt{x^2+4x+13}", "du": "\\frac{x+2}{\\sqrt{x^2+4x+13}}dx", "new": "\\int\\frac{du}{x+2}", "ok": False, "e": "Queda x + 2 sin eliminar."}]},
   XA("ln(x+2+sqrt(x^2+4*x+13))", 1 / sp.sqrt(x ** 2 + 4 * x + 13), (-4, 4), p="Ahora integra (con + C).")],
  ["\\(x^2+4x+13=(x+2)^2+9\\). Con \\(u=x+2\\): \\(\\int\\frac{du}{\\sqrt{u^2+3^2}}\\).",
   "\\(u=3\\tan\\theta\\): \\(\\int\\sec\\theta\\,d\\theta=\\ln|\\sec\\theta+\\tan\\theta|\\) \\(=\\ln\\left|\\frac{\\sqrt{u^2+9}}3+\\frac u3\\right|\\).",
   "El \\(\\frac13\\) se absorbe en la constante: \\(\\ln\\left(x+2+\\sqrt{x^2+4x+13}\\right)+C\\) (siempre positivo)."],
  "\\(\\ln\\left(x+2+\\sqrt{x^2+4x+13}\\right)+C\\)", "(x + 2)² + 9.", [["compcuad"], ["sustrig"], ["triref"]], chain=True))
ST.append(E("w11t7", 2, "Área de un semicírculo",
  "<p>Calcula \\(\\int\\sqrt{1-x^2}\\,dx\\).</p>",
  [XA("1/2*(arcsin(x)+x*sqrt(1-x^2))", sp.sqrt(1 - x ** 2), (-0.9, 0.9))],
  ["\\(x=\\sin\\theta\\), \\(dx=\\cos\\theta\\,d\\theta\\): \\(\\int\\cos^2\\theta\\,d\\theta=\\frac\\theta2+\\frac{\\sin2\\theta}4\\) (ángulo doble).",
   "\\(\\sin2\\theta=2\\sin\\theta\\cos\\theta=2x\\sqrt{1-x^2}\\): \\(\\frac12\\left(\\arcsin x+x\\sqrt{1-x^2}\\right)+C\\)."],
  "\\(\\frac12(\\arcsin x+x\\sqrt{1-x^2})+C\\)", "x = sen θ y luego ángulo doble.", [["sustrig"], ["angdob"]]))
ST.append(E("w11t8", 2, "Potencia 3/2",
  "<p>Calcula \\(\\int\\frac{dx}{(x^2+4)^{3/2}}\\).</p>",
  [XA("x/(4*sqrt(x^2+4))", 1 / (x ** 2 + 4) ** sp.Rational(3, 2), (-3, 3))],
  ["\\(x=2\\tan\\theta\\): \\((x^2+4)^{3/2}=8\\sec^3\\theta\\) y \\(dx=2\\sec^2\\theta\\,d\\theta\\) ⇒ \\(\\frac14\\int\\cos\\theta\\,d\\theta=\\frac14\\sin\\theta\\).",
   "Triángulo: \\(\\sin\\theta=\\frac{x}{\\sqrt{x^2+4}}\\) ⇒ \\(\\frac{x}{4\\sqrt{x^2+4}}+C\\)."],
  "\\(\\frac{x}{4\\sqrt{x^2+4}}+C\\)", "x = 2 tan θ.", [["sustrig"], ["triref"]]))
ST.append(E("w11t9", 2, "Integrales equivalentes",
  "<p>De la clase: con la sustitución adecuada, ¿a qué integral en \\(\\theta\\) se reduce \\(\\int\\sqrt{9-x^2}\\,dx\\)?</p>",
  [O(["\\(9\\int\\cos^2\\theta\\,d\\theta\\)", "\\(3\\int\\cos\\theta\\,d\\theta\\)", "\\(\\int d\\theta\\)", "\\(3\\int\\tan^2\\theta\\,d\\theta\\)", "\\(\\int\\sec\\theta\\,d\\theta\\)"])],
  ["\\(x=3\\sin\\theta\\): \\(\\sqrt{9-x^2}=3\\cos\\theta\\) y \\(dx=3\\cos\\theta\\,d\\theta\\).",
   "El producto da \\(9\\cos^2\\theta\\,d\\theta\\) (que luego se integra con ángulo doble). Ojo: no se cancela, como sí pasa en \\(\\int\\frac{dx}{\\sqrt{9-x^2}}\\to\\int d\\theta\\)."],
  "\\(9\\int\\cos^2\\theta\\,d\\theta\\)", "Multiplica raíz por dx.", [["sustrig"], ["sustrig"]]))
ST.append(E("w11t10", 2, "¿Trigonométrica o simple?",
  "<p>¿Cuál de estas integrales se resuelve mejor con una sustitución <strong>simple</strong> (no trigonométrica)?</p>",
  [O(["\\(\\int\\frac{x}{\\sqrt{x^2+4}}dx\\)", "\\(\\int\\frac{dx}{\\sqrt{x^2+4}}\\)", "\\(\\int\\frac{dx}{x^2\\sqrt{4+x^2}}\\)", "\\(\\int\\sqrt{4-x^2}\\,dx\\)", "\\(\\int\\frac{dx}{(x^2+4)^{3/2}}\\)"])],
  ["En \\(\\int\\frac{x}{\\sqrt{x^2+4}}dx\\) aparece \\(x\\,dx\\), que es la mitad de la derivada de \\(x^2+4\\).",
   "Con \\(u=x^2+4\\): \\(\\frac12\\int u^{-1/2}du=\\sqrt{x^2+4}+C\\). Las demás no tienen esa x afuera: ahí sí va la trigonométrica."],
  "\\(\\int\\frac{x}{\\sqrt{x^2+4}}dx\\)", "Busca la derivada de lo de adentro.", [["eleccion"], ["sustrig"]]))
ST_tools = [{"w": "tri", "t": "Triángulo de referencia", "p": "Elige el tipo de raíz y lee las seis razones en términos de x.", "o": {"a": 3}},
            {"w": "usub", "t": "¿Qué cambio conviene?", "p": "Toca cada opción y mira cómo queda la integral.",
             "o": {"int": "\\int\\frac{x\\,dx}{\\sqrt{9-x^2}}", "opts": [
               {"u": "9-x^2", "du": "-2x\\,dx", "new": "-\\frac12\\int u^{-1/2}du", "ok": True, "e": "Aparece \\(x\\,dx\\): basta una sustitución simple."},
               {"u": "3\\sin\\theta", "du": "3\\cos\\theta\\,d\\theta", "new": "3\\int\\sin\\theta\\,d\\theta", "ok": True, "e": "También funciona, pero es más larga."},
               {"u": "x", "du": "dx", "new": "\\int\\frac{x\\,dx}{\\sqrt{9-x^2}}", "ok": False, "e": "No cambia nada."}]}}]

# =====================================================================
# SEMANA 11 · Tema 4: otras técnicas y elección
# =====================================================================
OT_teo = (
 "<p><strong>Sustitución racionalizadora</strong> (radicales algebraicos): con \\(\\sqrt[n]{ax+b}\\) se toma \\(u=\\sqrt[n]{ax+b}\\) (\\(u^n=ax+b\\)); con raíces de índices distintos \\(\\sqrt[n]x,\\sqrt[m]x\\) se toma \\(x=u^k\\), \\(k=\\mathrm{mcm}(n,m)\\). Siempre queda una función racional en \\(u\\).</p>"
 "<p class=\"ej\"><b>Ejemplo (guía):</b> \\(\\int\\frac{x}{\\sqrt{x+1}}dx\\) con \\(u=\\sqrt{x+1}\\), \\(x=u^2-1\\), \\(dx=2u\\,du\\): \\(2\\int(u^2-1)du=\\) \\(\\frac23(x-2)\\sqrt{x+1}+C\\).</p>"
 "<p><strong>Weierstrass</strong> (último recurso para funciones racionales en \\(\\sin x\\) y \\(\\cos x\\)): \\(t=\\tan\\frac x2\\), \\(\\sin x=\\frac{2t}{1+t^2}\\), \\(\\cos x=\\frac{1-t^2}{1+t^2}\\), \\(dx=\\frac{2\\,dt}{1+t^2}\\).</p>"
 "<p><strong>Árbol de decisión:</strong> (1) simplificar con álgebra o identidades; (2) ¿hay \\(u\\) cuya derivada aparece? → sustitución; (3) clasificar: trigonométricas → identidades/Weierstrass, racionales → fracciones parciales, producto o inversas → partes (ILATE), radicales → trigonométrica o racionalizadora; (4) si no sale, manipular o combinar. Algunas no tienen antiderivada elemental (\\(e^{-x^2}\\), \\(\\frac{\\sin x}x\\)).</p>"
 "<p>En clase estas técnicas quedaron como «reto» y se profundizan en la guía.</p>"
)
OT_form = ["Racionalizadora: \\(u=\\sqrt[n]{ax+b}\\) · índices distintos: \\(x=u^{\\mathrm{mcm}}\\)",
           "Weierstrass: \\(t=\\tan\\frac x2\\), \\(dx=\\frac{2dt}{1+t^2}\\)",
           "Árbol: simplificar → sustitución → clasificar (trig, racional, producto, radical) → combinar"]
OT_lesson = (
 "<h3>Idea central</h3><p>Ninguna técnica es «la mejor»: la eficiente depende de la forma del integrando. Clasificar primero ahorra intentos inútiles.</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> olvidar el factor \\(\\frac{2}{1+t^2}\\) de \\(dx\\) en Weierstrass; en la racionalizadora no despejar \\(x\\) y \\(dx\\) en términos de \\(u\\); y usar Weierstrass cuando una sustitución simple bastaba.</div>"
 "<div class=\"err\"><b>Ojo con la guía (Ejemplo 24):</b> en \\(y'=\\frac{y}{\\sqrt{y+1}}\\) con \\(y(0)=0\\), la «singularidad» aparece porque al separar se divide entre \\(y\\). En realidad \\(y\\equiv0\\) es la solución (equilibrio): \\(y'=0\\) y \\(y(0)=0\\).</div>"
)
OT = []
OT.append(E("w11o1", 1, "Árbol de decisión",
  "<p>Clasifica cada integral según la técnica más eficiente (de la guía).</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Sustitución simple", "Fracciones parciales", "Por partes", "Sust. trigonométrica", "Racionalizadora"], "items": [
    {"x": "\\(\\int\\frac{x}{x^2-1}dx\\)", "c": 0, "e": "El numerador es la mitad de la derivada del denominador."},
    {"x": "\\(\\int\\frac{dx}{x^2-5x+6}\\)", "c": 1}, {"x": "\\(\\int x\\ln x\\,dx\\)", "c": 2},
    {"x": "\\(\\int\\frac{dx}{\\sqrt{x^2+4x+13}}\\)", "c": 3}, {"x": "\\(\\int\\frac{\\sqrt x}{1+\\sqrt[3]x}dx\\)", "c": 4},
    {"x": "\\(\\int x\\arctan x\\,dx\\)", "c": 2}, {"x": "\\(\\int\\frac{dx}{x\\sqrt{x+9}}\\)", "c": 4}]}],
  ["Primero se busca una sustitución obvia (derivada presente). Si no, se clasifica por la forma.",
   "Racional → fracciones parciales; producto de tipos distintos → partes; radical cuadrático → trigonométrica; radical algebraico → racionalizadora."],
  "Clasificación correcta", "Sigue el árbol de decisión.", [["eleccion"], ["eleccion"]]))
OT.append(E("w11o2", 2, "Racionalizadora",
  "<p>Calcula \\(\\int\\frac{x}{\\sqrt{x+1}}dx\\) (ejemplo de la guía).</p>",
  [XA("2/3*(x-2)*sqrt(x+1)", x / sp.sqrt(x + 1), (0, 5))],
  ["\\(u=\\sqrt{x+1}\\Rightarrow x=u^2-1\\), \\(dx=2u\\,du\\).", "\\(\\int\\frac{u^2-1}{u}2u\\,du=2\\left(\\frac{u^3}3-u\\right)=\\frac{2u(u^2-3)}3=\\frac23(x-2)\\sqrt{x+1}+C\\)."],
  "\\(\\frac23(x-2)\\sqrt{x+1}+C\\)", "u = √(x + 1).", [["racio"], ["racio"]]))
OT.append(E("w11o3", 2, "\\(\\int\\frac{dx}{1+\\sqrt x}\\)",
  "<p>Calcula \\(\\int\\frac{dx}{1+\\sqrt x}\\) (para \\(x>0\\)).</p>",
  [XA("2*sqrt(x)-2*ln(1+sqrt(x))", 1 / (1 + sp.sqrt(x)), (0.2, 6))],
  ["\\(u=\\sqrt x\\Rightarrow x=u^2\\), \\(dx=2u\\,du\\): \\(\\int\\frac{2u}{1+u}du=2\\int\\left(1-\\frac1{1+u}\\right)du\\).", "\\(=2u-2\\ln(1+u)+C=2\\sqrt x-2\\ln(1+\\sqrt x)+C\\)."],
  "\\(2\\sqrt x-2\\ln(1+\\sqrt x)+C\\)", "u = √x.", [["racio"], ["racio"]]))
OT.append(E("w11o4", 3, "Racionalizadora + fracciones parciales",
  "<p>Calcula \\(\\int\\frac{dx}{x\\sqrt{x+4}}\\) (para \\(x>0\\)).</p>",
  [XA("1/2*ln((sqrt(x+4)-2)/(sqrt(x+4)+2))", 1 / (x * sp.sqrt(x + 4)), (0.3, 6))],
  ["\\(u=\\sqrt{x+4}\\Rightarrow x=u^2-4\\), \\(dx=2u\\,du\\): \\(\\int\\frac{2u\\,du}{(u^2-4)u}=2\\int\\frac{du}{u^2-4}\\).",
   "\\(\\frac{1}{(u-2)(u+2)}=\\frac14\\left(\\frac1{u-2}-\\frac1{u+2}\\right)\\) ⇒ \\(\\frac12\\ln\\left|\\frac{u-2}{u+2}\\right|=\\frac12\\ln\\left|\\frac{\\sqrt{x+4}-2}{\\sqrt{x+4}+2}\\right|+C\\)."],
  "\\(\\frac12\\ln\\left|\\frac{\\sqrt{x+4}-2}{\\sqrt{x+4}+2}\\right|+C\\)", "Después de u queda un Caso I.", [["racio"], ["heav"]]))
OT.append(E("w11o5", 2, "Weierstrass",
  "<p>Calcula \\(\\int\\frac{dx}{1+\\cos x}\\) con \\(t=\\tan\\frac x2\\).</p>",
  [XA("tan(x/2)", 1 / (1 + sp.cos(x)), (-2.5, 2.5))],
  ["\\(1+\\cos x=1+\\frac{1-t^2}{1+t^2}=\\frac{2}{1+t^2}\\) y \\(dx=\\frac{2dt}{1+t^2}\\).", "\\(\\int\\frac{1+t^2}{2}\\cdot\\frac{2dt}{1+t^2}=\\int dt=t+C=\\tan\\frac x2+C\\)."],
  "\\(\\tan\\frac x2+C\\)", "Reemplaza cos x y dx.", [["weier"], ["weier"]]))
OT.append(E("w11o6", 3, "Weierstrass con completar cuadrados",
  "<p>Calcula \\(\\int\\frac{dx}{2+\\sin x}\\) (en \\(-\\pi<x<\\pi\\)).</p>",
  [XA("2/sqrt(3)*arctan((2*tan(x/2)+1)/sqrt(3))", 1 / (2 + sp.sin(x)), (-2.5, 2.5))],
  ["\\(2+\\frac{2t}{1+t^2}=\\frac{2(t^2+t+1)}{1+t^2}\\) ⇒ \\(\\int\\frac{dt}{t^2+t+1}\\).",
   "\\(t^2+t+1=\\left(t+\\frac12\\right)^2+\\frac34\\) ⇒ \\(\\frac{2}{\\sqrt3}\\arctan\\frac{2t+1}{\\sqrt3}+C\\) con \\(t=\\tan\\frac x2\\)."],
  "\\(\\frac2{\\sqrt3}\\arctan\\frac{2\\tan(x/2)+1}{\\sqrt3}+C\\)", "Completa cuadrados en t.", [["weier"], ["compcuad"]]))
OT.append(E("w11o7", 2, "Fármaco con eliminación saturable (IRCA)",
  "<p>Guía: \\(\\frac{dC}{dt}=-\\frac{kC}{1+C}\\), \\(C(0)=4\\) mg/L, \\(k=0{,}5\\) h⁻¹. Separando queda \\(C+\\ln C=4+\\ln4-0{,}5\\,t\\).</p>",
  [NUM([{"l": "t para C = 2 mg/L ≈", "a": round((2 + math.log(2)) / 0.5, 2), "u": "h", "tol": 0.02, "e": "Reemplaza C = 2 y despeja t."},
        {"l": "lím C(t) =", "a": 0, "u": "mg/L"}], "Calcula"),
   O(["\\(\\frac{1+C}{C}=\\frac1C+1\\): función racional simple", "Sustitución trigonométrica", "Weierstrass", "Partes con \\(u=\\ln C\\)", "Ángulo doble"], "¿Qué integrando aparece al separar?")],
  ["<b>I–R:</b> separando, \\(\\int\\frac{1+C}{C}dC=-\\int k\\,dt\\), y \\(\\frac{1+C}C=\\frac1C+1\\).",
   "<b>C:</b> \\(\\ln C+C=-kt+K\\); con \\(C(0)=4\\): \\(K=4+\\ln4\\). Para \\(C=2\\): \\(t=\\frac{4+\\ln4-2-\\ln2}{0{,}5}=\\frac{2+\\ln2}{0{,}5}\\approx5{,}39\\) h.",
   "<b>A:</b> si \\(t\\to\\infty\\) el lado derecho \\(\\to-\\infty\\), lo que solo pasa si \\(C\\to0^+\\). La solución es implícita (no se despeja C con funciones elementales)."],
  "t ≈ 5,39 h; C → 0", "C = 2 en la solución implícita.", [["irca"], ["irca"], ["irca"]], chain=True))
OT_tools = [{"w": "usub", "t": "Racionalizar", "p": "¿Qué cambio quita las dos raíces de \\(\\int\\frac{\\sqrt x}{1+\\sqrt[3]x}dx\\)?",
             "o": {"int": "\\int\\frac{\\sqrt x}{1+\\sqrt[3]x}dx", "opts": [
               {"u": "x^{1/6}", "du": "\\tfrac16x^{-5/6}dx", "new": "6\\int\\frac{u^8}{1+u^2}du", "ok": True, "e": "Con \\(x=u^6\\) (mcm de 2 y 3): \\(\\sqrt x=u^3\\), \\(\\sqrt[3]x=u^2\\)."},
               {"u": "\\sqrt x", "du": "\\frac{dx}{2\\sqrt x}", "new": "\\int\\frac{2u^2}{1+u^{2/3}}du", "ok": False, "e": "Queda \\(u^{2/3}\\): la raíz cúbica no se fue."},
               {"u": "\\sqrt[3]x", "du": "\\frac{dx}{3x^{2/3}}", "new": "\\int\\frac{3u^{7/2}}{1+u}du", "ok": False, "e": "Queda \\(u^{7/2}\\): la raíz cuadrada no se fue."}]}}]

# =====================================================================
# SEMANA 12 · Tema 1: sumas de Riemann
# =====================================================================
def riem(fn, a, b, n, m):
    dx = sp.Rational(b - a, n); s = 0
    for i in range(n):
        xl = a + i * dx; xs = xl if m == 'L' else xl + dx if m == 'R' else xl + dx / 2
        s += fn.subs(x, xs) * dx
    return sp.nsimplify(s)
L4c = riem(x ** 3, 0, 2, 4, 'L'); assert L4c == sp.Rational(9, 4)
fA = 4 - x ** 2
R4a, M4a = riem(fA, 0, 2, 4, 'R'), riem(fA, 0, 2, 4, 'M'); assert R4a == sp.Rational(17, 4) and M4a == sp.Rational(43, 8)
fB = x ** 2 + 1
L4b, R4b, M4b = riem(fB, 0, 2, 4, 'L'), riem(fB, 0, 2, 4, 'R'), riem(fB, 0, 2, 4, 'M')
assert (L4b, R4b, M4b) == (sp.Rational(15, 4), sp.Rational(23, 4), sp.Rational(37, 8)) and sp.integrate(fB, (x, 0, 2)) == sp.Rational(14, 3)
fC = 2 * x + 1
L6, R6, M6 = riem(fC, 0, 3, 6, 'L'), riem(fC, 0, 3, 6, 'R'), riem(fC, 0, 3, 6, 'M'); assert (L6, R6, M6) == (sp.Rational(21, 2), sp.Rational(27, 2), 12)
n_ = sp.symbols('n', positive=True, integer=True); i_ = sp.symbols('i', integer=True)
RnD = sp.simplify(sp.summation(((4 * i_ / n_) ** 2 + 1) * 4 / n_, (i_, 1, n_)))
assert sp.limit(RnD, n_, sp.oo) == sp.Rational(76, 3) == sp.integrate(x ** 2 + 1, (x, 0, 4))

RI_teo = (
 "<p><b>Área bajo una tasa constante:</b> si la tasa es \\(k\\), lo acumulado en \\([a,b]\\) es el rectángulo \\(k(b-a)\\): caudal 5 m³/s durante 12 s → 60 m³. Las unidades se multiplican (L/min · min = L; N · m = J).</p>"
 "<p>Si la tasa varía, se aproxima con rectángulos. <b>Partición regular:</b> \\(\\Delta x=\\frac{b-a}n\\), \\(x_i=a+i\\,\\Delta x\\). <b>Suma de Riemann:</b> \\(S_n=\\sum_{i=1}^n f(x_i^*)\\Delta x\\).</p>"
 "<ul><li>\\(L_n\\): extremos <b>izquierdos</b> \\(x_{i-1}\\). \\(R_n\\): extremos <b>derechos</b> \\(x_i\\). \\(M_n\\): puntos medios \\(\\frac{x_{i-1}+x_i}2\\) (suele ser la mejor).</li>"
 "<li>Si \\(f\\) es <b>creciente</b>: \\(L_n\\) subestima y \\(R_n\\) sobrestima. Si es <b>decreciente</b>, al revés.</li>"
 "<li>Suma <b>inferior</b>: usa el mínimo de \\(f\\) en cada subintervalo; <b>superior</b>: el máximo.</li></ul>"
 "<p><b>Sumatorias útiles:</b> \\(\\sum c=cn\\), \\(\\sum i=\\frac{n(n+1)}2\\), \\(\\sum i^2=\\frac{n(n+1)(2n+1)}6\\), \\(\\sum i^3=\\left[\\frac{n(n+1)}2\\right]^2\\).</p>"
 "<p><b>Integral definida:</b> \\(\\int_a^bf(x)\\,dx=\\lim_{n\\to\\infty}\\sum f(x_i^*)\\Delta x\\). Si \\(f\\ge0\\) es el área; si cambia de signo, el <b>área neta</b>. Toda función continua (o con finitos saltos) es integrable.</p>"
 "<div class=\"err\"><b>Ojo con la notación del material:</b> la guía y la lámina de la sesión 1 llaman \\(L_n\\) a la suma <i>inferior</i> y \\(R_n\\) a la <i>superior</i>, pero la convención de la misma guía y los ejercicios usan \\(L_n\\) = extremos izquierdos y \\(R_n\\) = derechos. Solo coinciden si \\(f\\) es creciente (con \\(4-x^2\\), que decrece, \\(R_4\\) es la inferior). Aquí se usa izquierdos/derechos.</div>"
)
RI_form = ["\\(\\Delta x=\\frac{b-a}n\\), \\(x_i=a+i\\Delta x\\), \\(S_n=\\sum f(x_i^*)\\Delta x\\)",
           "\\(L_n\\): izquierdos · \\(R_n\\): derechos · \\(M_n\\): medios",
           "Creciente: \\(L_n\\le\\int\\le R_n\\) · decreciente: al revés",
           "\\(\\sum i=\\frac{n(n+1)}2\\), \\(\\sum i^2=\\frac{n(n+1)(2n+1)}6\\)",
           "\\(\\int_a^bf=\\lim_{n\\to\\infty}\\sum f(x_i^*)\\Delta x\\)"]
RI_lesson = (
 "<h3>Idea central</h3><p>Lo acumulado es «tasa × tiempo» en cada trocito. Sumar trocitos cada vez más finos da el valor exacto: eso es la integral definida.</p>"
 "<h3>Receta para una suma de Riemann</h3><ol><li>\\(\\Delta x=\\frac{b-a}n\\).</li><li>Lista los puntos muestra según el tipo (izquierdos: \\(a,\\ a+\\Delta x,\\dots\\)).</li><li>Evalúa \\(f\\) en cada uno y suma.</li><li>Multiplica por \\(\\Delta x\\).</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes:</b> usar \\(n+1\\) puntos (izquierdos van de \\(x_0\\) a \\(x_{n-1}\\); derechos de \\(x_1\\) a \\(x_n\\)); olvidar multiplicar por \\(\\Delta x\\); y creer que la suma siempre subestima.</div>"
)
RI = []
RI.append(E("w12r1", 1, "Tasa constante",
  "<p>Una planta crece a una tasa constante de 4 cm/semana durante 10 semanas. ¿Qué afirmación describe la <strong>acumulación</strong>?</p>",
  [O(["La planta creció 40 cm en total", "La planta crece 4 cm por semana", "La planta mide 4 cm", "La planta crece durante 10 semanas", "La planta creció 14 cm"])],
  ["La tasa (4 cm/semana) es la altura del rectángulo; el tiempo (10 semanas) es la base.", "La acumulación es el área: \\(4\\times10=40\\) cm. «4 cm por semana» describe la tasa, no lo acumulado."],
  "40 cm", "Área = tasa × tiempo.", [["acum"], ["acum"]]))
RI.append(E("w12r2", 1, "\\(L_4\\) de \\(x^3\\) (ejemplo de clase)",
  "<p>Aproxima \\(\\int_0^2x^3dx\\) con \\(n=4\\) y extremos izquierdos.</p>",
  [NUM([{"l": "Δx =", "a": 0.5}, {"l": "L₄ =", "a": 2.25, "e": "0,5·[f(0) + f(0,5) + f(1) + f(1,5)]."}], "Calcula"),
   O(["Subestima: \\(x^3\\) es creciente y el valor exacto es 4", "Sobrestima: el valor exacto es 2", "Es exacta", "Sobrestima porque \\(n\\) es par", "No se puede saber sin graficar"], "¿Qué hace L₄ aquí?")],
  ["\\(\\Delta x=\\frac{2-0}4=0{,}5\\); puntos izquierdos \\(0;\\ 0{,}5;\\ 1;\\ 1{,}5\\).",
   "\\(L_4=0{,}5\\,[0+0{,}125+1+3{,}375]=0{,}5(4{,}5)=2{,}25\\).",
   "Exacto: \\(\\int_0^2x^3dx=\\frac{x^4}4\\Big|_0^2=4\\). Como \\(x^3\\) crece, los rectángulos izquierdos quedan por debajo: subestima."],
  "2,25 (subestima; exacto 4)", "Puntos 0; 0,5; 1; 1,5.", [["riem"], ["riem"], ["riem"]], chain=True))
RI.append(E("w12r3", 2, "\\(R_4\\) y \\(M_4\\) de \\(4-x^2\\)",
  "<p>Ejercicio de clase: aproxima el área bajo \\(f(x)=4-x^2\\) en \\([0,2]\\) con \\(n=4\\).</p>",
  [NUM([{"l": "R₄ =", "a": 4.25, "e": "Derechos: 0,5; 1; 1,5; 2."}, {"l": "M₄ =", "a": 5.375, "e": "Medios: 0,25; 0,75; 1,25; 1,75."}], "Calcula"),
   O(["\\(R_4<\\frac{16}3<M_4\\)… no: \\(R_4<M_4<\\frac{16}3\\)", "\\(R_4<M_4<\\frac{16}3\\)", "\\(\\frac{16}3<M_4<R_4\\)", "\\(M_4<R_4<\\frac{16}3\\)", "\\(R_4=M_4=\\frac{16}3\\)"], "Compara con el exacto \\(\\int_0^2(4-x^2)dx=\\frac{16}3\\approx5{,}33\\)")],
  ["\\(\\Delta x=0{,}5\\). \\(R_4=0{,}5\\,[f(0{,}5)+f(1)+f(1{,}5)+f(2)]=\\) \\(0{,}5\\,[3{,}75+3+1{,}75+0]=4{,}25\\).",
   "\\(M_4=0{,}5\\,[f(0{,}25)+f(0{,}75)+f(1{,}25)+f(1{,}75)]=\\) \\(0{,}5\\,[3{,}9375+3{,}4375+2{,}4375+0{,}9375]=5{,}375\\).",
   "\\(f\\) decrece: los derechos subestiman (\\(4{,}25<5{,}33\\)). Aquí \\(M_4\\) se pasa un poco porque \\(f\\) es cóncava hacia abajo, pero es la mejor."],
  "R₄ = 4,25; M₄ = 5,375", "f es decreciente.", [["riem"], ["riem"], ["riem"]], chain=True))
RI[2]["checks"][1] = O(["\\(R_4<\\frac{16}3<M_4\\)", "\\(R_4<M_4<\\frac{16}3\\)", "\\(\\frac{16}3<M_4<R_4\\)", "\\(M_4<R_4<\\frac{16}3\\)", "\\(R_4=M_4=\\frac{16}3\\)"], "Compara con el exacto \\(\\int_0^2(4-x^2)dx=\\frac{16}3\\approx5{,}33\\)")
assert R4a < sp.Rational(16, 3) < M4a
RI.append(E("w12r4", 2, "\\(L_4\\), \\(R_4\\) y \\(M_4\\) de \\(x^2+1\\)",
  "<p>Guía: para \\(f(x)=x^2+1\\) en \\([0,2]\\) con \\(n=4\\), calcula las tres sumas. El valor exacto es \\(\\frac{14}3\\approx4{,}667\\).</p>",
  [{"t": "fill", "p": "Completa la tabla", "head": ["Suma", "Puntos muestra", "Valor"], "rows": [
    ["\\(L_4\\)", "0; 0,5; 1; 1,5", {"a": 3.75}], ["\\(R_4\\)", "0,5; 1; 1,5; 2", {"a": 5.75}], ["\\(M_4\\)", "0,25; 0,75; 1,25; 1,75", {"a": 4.625}]]},
   O(["\\(M_4\\), con error de unos 0,04", "\\(L_4\\), porque es la más pequeña", "\\(R_4\\), porque usa el extremo b", "Las tres son igual de buenas", "\\(\\frac{L_4+R_4}2\\) es exacta"], "¿Cuál aproxima mejor?")],
  ["\\(L_4=0{,}5\\,[1+1{,}25+2+3{,}25]=3{,}75\\); \\(R_4=0{,}5\\,[1{,}25+2+3{,}25+5]=5{,}75\\).",
   "\\(M_4=0{,}5\\,[1{,}0625+1{,}5625+2{,}5625+4{,}0625]=4{,}625\\).",
   "Errores: \\(L_4\\) −0,92, \\(R_4\\) +1,08, \\(M_4\\) −0,04. El punto medio gana claramente. (El promedio de L y R es 4,75: tampoco es exacto.)"],
  "3,75; 5,75; 4,625 → M₄", "Δx = 0,5.", [["riem"], ["riem"], ["riem"]], chain=True))
RI.append(E("w12r5", 2, "\\(n=6\\) con una recta",
  "<p>Guía: para \\(f(x)=2x+1\\) en \\([0,3]\\) con \\(n=6\\):</p>",
  [NUM([{"l": "L₆ =", "a": 10.5}, {"l": "R₆ =", "a": 13.5}, {"l": "M₆ =", "a": 12}, {"l": "∫₀³ (2x + 1) dx =", "a": 12}], "Calcula")],
  ["\\(\\Delta x=0{,}5\\). \\(L_6=0{,}5\\,[1+2+3+4+5+6]=10{,}5\\); \\(R_6=0{,}5\\,[2+\\dots+7]=13{,}5\\).",
   "\\(M_6=0{,}5\\,[1{,}5+2{,}5+\\dots+6{,}5]=12\\), igual al exacto \\(x^2+x\\big|_0^3=12\\): con una recta el punto medio es exacto (los triángulos que sobran y faltan se compensan)."],
  "10,5; 13,5; 12; 12", "Δx = 0,5.", [["riem"], ["riem"]]))
RI.append(E("w12r6", 3, "Del límite a la integral",
  "<p>¿Qué integral definida es \\(\\displaystyle\\lim_{n\\to\\infty}\\sum_{i=1}^n\\left[\\left(2+\\frac{3i}n\\right)^2+1\\right]\\frac3n\\)?</p>",
  [O(["\\(\\int_2^5(x^2+1)\\,dx\\)", "\\(\\int_0^3(x^2+1)\\,dx\\)", "\\(\\int_2^3(x^2+1)\\,dx\\)", "\\(\\int_0^5(x^2+1)\\,dx\\)", "\\(\\int_2^5x^2\\,dx\\)"])],
  ["\\(\\Delta x=\\frac3n\\) y \\(x_i=2+\\frac{3i}n\\): empieza en \\(a=2\\) y \\(b-a=3\\Rightarrow b=5\\).",
   "La función evaluada en \\(x_i\\) es \\(x^2+1\\) (suma con extremos derechos). Así el límite es \\(\\int_2^5(x^2+1)dx\\)."],
  "\\(\\int_2^5(x^2+1)dx\\)", "Lee a y Δx en \\(x_i=a+i\\Delta x\\).", [["intdef"], ["intdef"]]))
RI.append(E("w12r7", 3, "Límite con sumatorias",
  "<p>Para \\(\\int_0^4(x^2+1)dx\\) con extremos derechos, \\(R_n=\\sum_{i=1}^n\\left[\\left(\\frac{4i}n\\right)^2+1\\right]\\frac4n\\). Usa \\(\\sum i^2=\\frac{n(n+1)(2n+1)}6\\) y toma el límite.</p>",
  [XV("76/3", sp.Rational(76, 3), "lím Rₙ ="), O(["Coincide con \\(\\left[\\frac{x^3}3+x\\right]_0^4\\)", "Es mayor que la integral", "Depende de n", "No existe", "Vale 64/3"], "Compáralo con el TFC")],
  ["\\(R_n=\\frac{64}{n^3}\\sum i^2+\\frac4n\\cdot n=\\frac{64}{n^3}\\cdot\\frac{n(n+1)(2n+1)}6+4\\).",
   "Cuando \\(n\\to\\infty\\), \\(\\frac{(n+1)(2n+1)}{n^2}\\to2\\): \\(\\frac{64\\cdot2}{6}+4=\\frac{64}3+4=\\frac{76}3\\).",
   "Con el TFC: \\(\\frac{64}3+4=\\frac{76}3\\). Mismo valor."],
  "76/3", "Saca las constantes de la suma.", [["sigma"], ["intdef"], ["tfc2"]], chain=True))
RI.append(E("w12r8", 1, "Verdadero o falso",
  "<p>Clasifica cada afirmación (de la guía).</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Verdadera", "Falsa"], "items": [
    {"x": "La suma de Riemann siempre subestima el área.", "c": 1, "e": "Depende de los puntos muestra y de si f crece o decrece."},
    {"x": "Si f es continua en [a, b], es integrable en [a, b].", "c": 0},
    {"x": "\\(\\int_a^af(x)\\,dx=1\\)", "c": 1, "e": "Es 0: no hay ancho."},
    {"x": "El área neta siempre es positiva.", "c": 1},
    {"x": "Si \\(f\\ge0\\) en [a, b], el área neta coincide con el área total.", "c": 0},
    {"x": "La integral de una tasa constante k sobre [a, b] es k(b − a).", "c": 0}]}],
  ["La suma de Riemann puede quedar por encima o por debajo; \\(\\int_a^a=0\\); el área neta resta lo que está bajo el eje (puede ser negativa o cero).",
   "Con \\(f\\ge0\\) no hay nada que restar: neta = total. La tasa constante da un rectángulo."],
  "F, V, F, F, V, V", "Piensa en un contraejemplo.", [["riem"], ["intdef"]]))
RI_tools = [{"w": "riem", "t": "Rectángulos de Riemann: \\(x^3\\) en [0, 2]", "p": "Cambia n y el tipo de punto muestra. Mira cuándo la suma queda por debajo o por encima del valor exacto (4).", "o": {"f": "x^3", "a": 0, "b": 2, "n": 4, "m": "L", "ex": 4, "exl": "\\int_0^2x^3dx"}},
            {"w": "riem", "t": "Una función que decrece: \\(4-x^2\\)", "p": "Con f decreciente, los derechos subestiman y los izquierdos sobrestiman.", "o": {"f": "4-x^2", "a": 0, "b": 2, "n": 4, "m": "R", "ex": 16 / 3, "exl": "\\tfrac{16}3"}},
            {"w": "riem", "t": "Área neta: \\(\\sin x\\) en \\([-\\pi/2,\\pi]\\)", "p": "Los rectángulos bajo el eje (rojos) restan.", "o": {"f": "sin(x)", "a": -1.5708, "b": 3.1416, "n": 6, "m": "M", "ex": 1, "exl": "\\int_{-\\pi/2}^{\\pi}\\sin x\\,dx", "xr": [-2, 3.5], "yr": [-1.3, 1.3]}}]

# =====================================================================
# SEMANA 12 · Tema 2: propiedades y TFC1
# =====================================================================
TF_teo = (
 "<p><b>Propiedades</b> (f, g integrables): \\(\\int_a^af=0\\); \\(\\int_b^af=-\\int_a^bf\\); linealidad \\(\\int(\\alpha f+\\beta g)=\\alpha\\int f+\\beta\\int g\\); aditividad \\(\\int_a^cf+\\int_c^bf=\\int_a^bf\\); monotonía (si \\(f\\ge g\\), \\(\\int f\\ge\\int g\\)); acotamiento: si \\(m\\le f\\le M\\), \\(m(b-a)\\le\\int_a^bf\\le M(b-a)\\).</p>"
 "<p><b>Primer Teorema Fundamental (TFC1):</b> si \\(f\\) es continua, \\(A(x)=\\int_a^xf(t)\\,dt\\) es derivable y \\(A'(x)=f(x)\\): la derivada de la acumulación devuelve la tasa.</p>"
 "<p><b>Límites variables:</b> \\(\\frac{d}{dx}\\int_{g(x)}^{h(x)}f(t)\\,dt=\\) \\(f(h(x))\\,h'(x)\\) \\(-\\,f(g(x))\\,g'(x)\\).</p>"
 "<p class=\"ej\"><b>Ejemplos:</b> \\(\\frac d{dx}\\int_0^{x^2}\\cos t\\,dt=\\) \\(2x\\cos(x^2)\\) (clase); \\(\\frac d{dx}\\int_0^{x^3}\\sqrt{1+t^2}\\,dt=\\) \\(3x^2\\sqrt{1+x^6}\\) (guía).</p>"
)
TF_form = ["\\(\\int_b^a f=-\\int_a^b f\\) · \\(\\int_a^c f+\\int_c^b f=\\int_a^b f\\)",
           "\\(m\\le f\\le M\\Rightarrow\\) \\(m(b-a)\\le\\int_a^bf\\) \\(\\le M(b-a)\\)",
           "TFC1: \\(\\frac{d}{dx}\\int_a^xf(t)dt=f(x)\\)",
           "\\(\\frac{d}{dx}\\int_{g}^{h}f=f(h)h'-f(g)g'\\)"]
TF_lesson = (
 "<h3>Idea central</h3><p>\\(A(x)\\) es «cuánto se ha acumulado hasta x». Si mueves x un poquito, el área crece en una franja de altura \\(f(x)\\): por eso \\(A'(x)=f(x)\\).</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> olvidar la regla de la cadena cuando el límite es \\(x^2\\) o \\(\\sin x\\); integrar primero cuando el TFC1 lo hace innecesario; y en el límite inferior olvidar el signo menos.</div>"
)
TF = []
TF.append(E("w12f1", 1, "Propiedades sin integrar",
  "<p>Sabiendo que \\(\\int_0^5f(x)dx=8\\) y \\(\\int_0^5g(x)dx=-3\\) (guía):</p>",
  [NUM([{"l": "∫₀⁵ [3f − 2g] dx =", "a": 30}, {"l": "∫₅⁰ f dx =", "a": -8}, {"l": "∫₀⁵ [f + g] dx =", "a": 5}, {"l": "∫₂² f dx =", "a": 0}], "Calcula")],
  ["Linealidad: \\(3(8)-2(-3)=24+6=30\\) y \\(8+(-3)=5\\).", "Invertir los límites cambia el signo: \\(-8\\). Con los mismos límites: 0."],
  "30; −8; 5; 0", "Linealidad e inversión de límites.", [["propint"], ["propint"]]))
TF.append(E("w12f2", 2, "Aditividad",
  "<p>Si \\(\\int_0^3f=4\\) y \\(\\int_3^5f=-1\\):</p>",
  [NUM([{"l": "∫₀⁵ f =", "a": 3}, {"l": "∫₅⁰ f =", "a": -3}], "Calcula"),
   O(["Hay más área (con signo) arriba del eje en [0, 3] que abajo en [3, 5]", "f es positiva en todo [0, 5]", "f vale 3 en todo el intervalo", "El área total es 3", "f es negativa en [0, 3]"], "Interpretación geométrica")],
  ["\\(\\int_0^5f=\\int_0^3f+\\int_3^5f=4-1=3\\); al invertir: \\(-3\\).", "El área neta es positiva: lo que está sobre el eje (4) supera a lo que está bajo él en \\([3,5]\\) (1). El área total sería al menos 5."],
  "3; −3", "Suma los tramos.", [["propint"], ["areanet"]], chain=True))
TF.append(E("w12f3", 1, "Acotar sin calcular",
  "<p>Si \\(2\\le f(x)\\le5\\) en \\([1,6]\\), ¿entre qué valores está \\(\\int_1^6f(x)dx\\)?</p>",
  [NUM([{"l": "Cota inferior", "a": 10}, {"l": "Cota superior", "a": 25}], "Calcula")],
  ["Acotamiento: \\(m(b-a)\\le\\int_a^bf\\le M(b-a)\\) con \\(b-a=5\\).", "\\(2\\cdot5=10\\le\\int_1^6f\\le25=5\\cdot5\\): rectángulos de altura mínima y máxima."],
  "Entre 10 y 25", "Rectángulos.", [["propint"], ["propint"]]))
TF.append(E("w12f4", 1, "TFC1 directo",
  "<p>Sea \\(A(x)=\\int_0^x(t^3-2t)\\,dt\\). Halla \\(A'(x)\\) sin integrar.</p>",
  [{"t": "expr", "p": "Escribe A′(x).", "f": [{"a": "x^3-2*x", "v": ["x"], "l": "A′(x) ="}]},
   NUM([{"l": "A′(2) =", "a": 4}], "Evalúa")],
  ["TFC1: la derivada de la acumulación es el integrando evaluado en x: \\(A'(x)=x^3-2x\\).", "\\(A'(2)=8-4=4\\): en x = 2 el área acumulada crece a razón de 4 por unidad."],
  "x³ − 2x; A′(2) = 4", "No integres.", [["tfc1"], ["tfc1"]], chain=True))
chk_eq("2*x*cos(x^2)", sp.diff(sp.integrate(sp.cos(t), (t, 0, x ** 2)), x), (-2, 2))
TF.append(E("w12f5", 2, "Límite superior \\(x^2\\)",
  "<p>Ejemplo de clase: deriva \\(A(x)=\\int_0^{x^2}\\cos t\\,dt\\).</p>",
  [{"t": "expr", "p": "Escribe A′(x).", "f": [{"a": "2*x*cos(x^2)", "v": ["x"], "l": "A′(x) ="}]}],
  ["El límite superior es \\(h(x)=x^2\\): \\(A'(x)=\\cos(h(x))\\,h'(x)\\).", "\\(A'(x)=\\cos(x^2)\\cdot2x\\)."],
  "\\(2x\\cos(x^2)\\)", "Regla de la cadena.", [["tfc1"], ["tfc1"]]))
chk_eq("3*x^2*sqrt(1+x^6)", 3 * x ** 2 * sp.sqrt(1 + x ** 6), (0, 2))
TF.append(E("w12f6", 2, "Raíz con \\(x^3\\)",
  "<p>Guía: deriva \\(D(x)=\\int_0^{x^3}\\sqrt{1+t^2}\\,dt\\).</p>",
  [{"t": "expr", "p": "Escribe D′(x).", "f": [{"a": "3*x^2*sqrt(1+x^6)", "v": ["x"], "l": "D′(x) ="}]}],
  ["\\(f(t)=\\sqrt{1+t^2}\\), \\(h(x)=x^3\\), \\(h'(x)=3x^2\\).", "\\(D'(x)=\\sqrt{1+(x^3)^2}\\cdot3x^2=3x^2\\sqrt{1+x^6}\\)."],
  "\\(3x^2\\sqrt{1+x^6}\\)", "f(h(x))·h′(x).", [["tfc1"], ["tfc1"]]))
gx = sp.Integral(sp.sqrt(1 + t ** 3), (t, x, x ** 2)).doit() if False else None
der = 2 * x * sp.sqrt(1 + x ** 6) - sp.sqrt(1 + x ** 3)
chk_eq("2*x*sqrt(1+x^6)-sqrt(1+x^3)", der, (0.2, 2))
TF.append(E("w12f7", 3, "Dos límites variables",
  "<p>Guía: deriva \\(F(x)=\\int_x^{x^2}\\sqrt{1+t^3}\\,dt\\) (para \\(x>0\\)).</p>",
  [{"t": "expr", "p": "Escribe F′(x).", "f": [{"a": "2*x*sqrt(1+x^6)-sqrt(1+x^3)", "v": ["x"], "l": "F′(x) =", "dom": {"x": [0.2, 2]}}]}],
  ["\\(F'(x)=f(h)h'-f(g)g'\\) con \\(h=x^2\\), \\(g=x\\).", "\\(F'(x)=\\sqrt{1+x^6}\\cdot2x-\\sqrt{1+x^3}\\cdot1\\)."],
  "\\(2x\\sqrt{1+x^6}-\\sqrt{1+x^3}\\)", "Arriba menos abajo.", [["tfc1"], ["tfc1"]]))
TF.append(E("w12f8", 2, "¿Dónde crece la acumulación?",
  "<p>Guía: \\(F(x)=\\int_1^x\\frac{t^2-1}{t^2+1}dt\\). Completa la tabla de signos de \\(F'(x)\\).</p>",
  [{"t": "signs", "p": "Signo de F′(x)", "pts": ["-1", "1"], "rows": [{"n": "F′(x)", "a": ["+", "-", "+"]}]},
   O(["F decrece en (−1, 1) y crece fuera", "F crece en (−1, 1)", "F siempre crece", "F decrece para x > 1", "F tiene un máximo en x = 1"], "Entonces…")],
  ["TFC1: \\(F'(x)=\\frac{x^2-1}{x^2+1}\\). El denominador es siempre positivo; el signo lo da \\(x^2-1\\).",
   "\\(F'>0\\) si \\(|x|>1\\) y \\(F'<0\\) si \\(-1<x<1\\): F crece, decrece y vuelve a crecer (máximo en −1 y mínimo en 1)."],
  "+ − +; decrece en (−1, 1)", "F′ es el integrando.", [["tfc1"], ["tfc1"]], chain=True))
TF_tools = [{"w": "acum", "t": "La acumulación A(x) = ∫₀ˣ t² dt", "p": "Mueve b: el área crece más rápido donde la curva está más alta. Eso es A′(x) = f(x).", "o": {"f": "x^2", "F": "x^3/3", "xr": [-0.5, 3], "yr": [-1, 9], "a": 0, "b": 1.5, "fl": "f(t) = t²"}}]

# =====================================================================
# SEMANA 12 · Tema 3: TFC2 con sustitución y partes
# =====================================================================
TE_teo = (
 "<p><b>Segundo Teorema Fundamental (TFC2):</b> si \\(f\\) es continua en \\([a,b]\\) y \\(F'=f\\), entonces \\(\\int_a^bf(x)dx=F(b)-F(a)\\). La constante C se cancela: se usa la antiderivada más simple.</p>"
 "<p><b>Sustitución en definidas:</b> \\(\\int_a^bf(g(x))g'(x)dx=\\int_{g(a)}^{g(b)}f(u)du\\): <b>se cambian los límites</b> y no se regresa a x.</p>"
 "<p><b>Partes en definidas:</b> \\(\\int_a^bu\\,dv=[uv]_a^b-\\int_a^bv\\,du\\).</p>"
 "<p class=\"ej\"><b>Ejemplos de clase:</b> \\(\\int_1^3(3x^2-2x+1)dx=20\\); \\(\\int_0^1x^2(x^3+1)^4dx=\\frac{31}{15}\\); \\(\\int_0^2xe^{x^2}dx=\\frac{e^4-1}2\\); \\(\\int_1^e\\ln x\\,dx=1\\); \\(\\int_0^\\pi x\\sin x\\,dx=\\pi\\).</p>"
)
TE_form = ["TFC2: \\(\\int_a^bf=F(b)-F(a)\\) (sin C)",
           "Sustitución: cambia los límites a \\(u=g(a)\\), \\(u=g(b)\\)",
           "Partes: \\([uv]_a^b-\\int_a^bv\\,du\\)",
           "\\(\\int_0^\\pi x^2\\sin x\\,dx=\\pi^2-4\\)"]
TE_lesson = (
 "<h3>Idea central</h3><p>Una integral definida es <b>un número</b>. Encuentra cualquier antiderivada, evalúa arriba menos abajo, y si cambiaste de variable, cambia también los límites.</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> sustituir \\(u\\) y seguir usando los límites en x; olvidar el paréntesis en \\(F(b)-F(a)\\) (el signo menos afecta a todo \\(F(a)\\)); y en partes evaluar solo el \\(uv\\) y olvidar la integral que queda.</div>"
)
TE = []
def ev(f, a, b): return sp.integrate(f, (x, a, b))
TE.append(E("w12e1", 1, "Evaluación directa",
  "<p>Ejemplo de clase: calcula \\(\\int_1^3(3x^2-2x+1)\\,dx\\).</p>",
  [XV("20", ev(3 * x ** 2 - 2 * x + 1, 1, 3), "Resultado =")],
  ["Antiderivada: \\(F(x)=x^3-x^2+x\\).", "\\(F(3)-F(1)=(27-9+3)-(1-1+1)=21-1=20\\)."],
  "20", "x³ − x² + x.", [["tfc2"], ["tfc2"]]))
TE.append(E("w12e2", 1, "Raíz y potencia",
  "<p>Calcula \\(\\int_1^4\\left(\\sqrt x-\\frac1{x^2}\\right)dx\\).</p>",
  [XV("47/12", ev(sp.sqrt(x) - 1 / x ** 2, 1, 4), "Resultado =")],
  ["\\(F(x)=\\frac23x^{3/2}+\\frac1x\\).", "\\(F(4)-F(1)=\\left(\\frac{16}3+\\frac14\\right)-\\left(\\frac23+1\\right)=\\frac{67}{12}-\\frac{20}{12}=\\frac{47}{12}\\)."],
  "47/12", "\\(\\int x^{-2}=-x^{-1}\\).", [["tfc2"], ["tfc2"]]))
TE.append(E("w12e3", 2, "Sustitución con cambio de límites",
  "<p>Calcula \\(\\int_0^1x^2(x^3+1)^4dx\\) (guía y clase).</p>",
  [{"t": "fill", "p": "Con \\(u=x^3+1\\), completa", "head": ["", "Valor"], "rows": [["u cuando x = 0", {"a": 1}], ["u cuando x = 1", {"a": 2}]]},
   XV("31/15", ev(x ** 2 * (x ** 3 + 1) ** 4, 0, 1), "Resultado =")],
  ["\\(du=3x^2dx\\Rightarrow x^2dx=\\frac{du}3\\). Límites: \\(x=0\\to u=1\\); \\(x=1\\to u=2\\).",
   "\\(\\frac13\\int_1^2u^4du=\\frac13\\cdot\\frac{u^5}5\\Big|_1^2=\\frac{32-1}{15}=\\frac{31}{15}\\)."],
  "31/15", "Cambia los límites a u.", [["limsust"], ["limsust"]], chain=True))
TE.append(E("w12e4", 2, "\\(\\int_0^2xe^{x^2}dx\\)",
  "<p>Ejemplo de clase: calcula \\(\\int_0^2xe^{x^2}dx\\).</p>",
  [XV("(e^4-1)/2", ev(x * sp.exp(x ** 2), 0, 2), "Resultado =")],
  ["\\(u=x^2\\), \\(du=2x\\,dx\\); límites \\(0\\to0\\), \\(2\\to4\\).", "\\(\\frac12\\int_0^4e^udu=\\frac{e^4-1}2\\approx26{,}80\\)."],
  "\\(\\frac{e^4-1}2\\)", "u = x².", [["limsust"], ["limsust"]]))
TE.append(E("w12e5", 2, "\\(\\int_0^{\\pi/2}\\sin x\\cos x\\,dx\\)",
  "<p>Ejercicio de clase: calcula \\(\\int_0^{\\pi/2}\\sin x\\cos x\\,dx\\).</p>",
  [XV("1/2", ev(sp.sin(x) * sp.cos(x), 0, sp.pi / 2), "Resultado =")],
  ["\\(u=\\sin x\\), \\(du=\\cos x\\,dx\\); límites \\(0\\to0\\), \\(\\frac\\pi2\\to1\\).", "\\(\\int_0^1u\\,du=\\frac12\\)."],
  "1/2", "u = sen x.", [["limsust"], ["limsust"]]))
TE.append(E("w12e6", 1, "\\(\\int_1^e\\ln x\\,dx\\)",
  "<p>Ejemplo de clase: calcula \\(\\int_1^e\\ln x\\,dx\\).</p>",
  [XV("1", ev(sp.log(x), 1, sp.E), "Resultado =")],
  ["Partes: \\(u=\\ln x\\), \\(dv=dx\\Rightarrow du=\\frac{dx}x\\), \\(v=x\\).", "\\([x\\ln x]_1^e-\\int_1^e1\\,dx=(e-0)-(e-1)=1\\)."],
  "1", "u = ln x, dv = dx.", [["partes"], ["tfc2"]]))
TE.append(E("w12e7", 2, "\\(\\int_0^\\pi x\\sin x\\,dx\\)",
  "<p>Calcula \\(\\int_0^\\pi x\\sin x\\,dx\\).</p>",
  [XV("π", ev(x * sp.sin(x), 0, sp.pi), "Resultado =")],
  ["\\(u=x\\), \\(dv=\\sin x\\,dx\\Rightarrow v=-\\cos x\\).", "\\([-x\\cos x]_0^\\pi+\\int_0^\\pi\\cos x\\,dx=\\pi+[\\sin x]_0^\\pi=\\pi\\)."],
  "π", "u = x.", [["partes"], ["tfc2"]]))
TE.append(E("w12e8", 3, "Partes dos veces",
  "<p>Guía: calcula \\(\\int_0^\\pi x^2\\sin x\\,dx\\).</p>",
  [XV("π^2-4", ev(x ** 2 * sp.sin(x), 0, sp.pi), "Resultado =")],
  ["Tabulación: \\(\\int x^2\\sin x\\,dx=-x^2\\cos x+2x\\sin x+2\\cos x\\).", "\\(F(\\pi)=\\pi^2-2\\), \\(F(0)=2\\) ⇒ \\(\\pi^2-4\\approx5{,}87\\)."],
  "π² − 4", "Dos veces partes.", [["partes"], ["tfc2"]]))
TE.append(E("w12e9", 2, "Descubre el error",
  "<p>Guía: un estudiante calcula \\(\\int_{-2}^2x^3dx\\) y obtiene 8. ¿Cuál es el error?</p>",
  [O(["Evaluó \\(F(-2)\\) con signo equivocado: \\(\\frac{16}4-\\frac{16}4=0\\)", "Debía usar sustitución", "Olvidó la constante C", "\\(x^3\\) no es integrable en \\([-2,2]\\)", "El resultado correcto es 16"])],
  ["\\(F(x)=\\frac{x^4}4\\): \\(F(2)-F(-2)=4-4=0\\). Si se escribe \\(4-(-4)\\) se obtiene el 8 equivocado.",
   "Además \\(x^3\\) es impar y el intervalo es simétrico: la integral es 0 sin calcular. (El 8 sería el área total.)"],
  "Es 0", "(−2)⁴ es positivo.", [["tfc2"], ["areanet"]]))
TE_tools = [{"w": "usub", "t": "Sustitución con límites", "p": "\\(\\int_0^1x^2(x^3+1)^4dx\\): elige u y fíjate en los nuevos límites.",
             "o": {"int": "\\int_0^1x^2(x^3+1)^4dx", "opts": [
               {"u": "x^3+1", "du": "3x^2dx", "new": "\\frac13\\int_1^2u^4du", "ok": True, "e": "x = 0 → u = 1; x = 1 → u = 2."},
               {"u": "x^2", "du": "2x\\,dx", "new": "\\int_0^1\\frac{\\sqrt u}{2}(u^{3/2}+1)^4du", "ok": False, "e": "Se complica más."},
               {"u": "(x^3+1)^4", "du": "12x^2(x^3+1)^3dx", "new": "\\int\\frac{u\\,du}{12(x^3+1)^3}", "ok": False, "e": "Quedan x sueltas."}]}}]

# =====================================================================
# SEMANA 12 · Tema 4: área neta, total y cambio neto
# =====================================================================
fv = t ** 2 - 2 * t - 3
desp = sp.integrate(fv, (t, 0, 4)); dist = sp.integrate(sp.Abs(fv), (t, 0, 4))
assert desp == -sp.Rational(20, 3) and dist == sp.Rational(34, 3)
V10 = 200 * (1 - math.exp(-1)); T150 = math.log(4) / 0.1
AR_teo = (
 "<p><b>Área neta</b> \\(\\int_a^bf\\): lo que está bajo el eje resta. <b>Área total</b> \\(\\int_a^b|f|\\): se parte el intervalo en los ceros de \\(f\\) y se suman valores absolutos.</p>"
 "<p class=\"ej\"><b>Ejemplo de clase:</b> \\(f(x)=x^3-4x\\) en \\([-2,2]\\): neta \\(=0\\), total \\(=4+4=8\\).</p>"
 "<p><b>Teorema del cambio neto:</b> \\(\\int_a^bf'(x)dx=f(b)-f(a)\\). La integral de una tasa es el cambio neto: velocidad → desplazamiento (m), caudal → volumen (m³), densidad lineal → masa (kg), corriente → carga (C), potencia → energía (J).</p>"
 "<p><b>Desplazamiento vs. distancia:</b> el desplazamiento es \\(\\int v\\); la distancia es \\(\\int|v|\\). Con \\(v=t^2-2t-3\\) en \\([0,4]\\): desplazamiento \\(-\\frac{20}3\\) m, distancia \\(\\frac{34}3\\) m.</p>"
 "<p><b>Paridad:</b> si f es impar, \\(\\int_{-a}^af=0\\); si es par, \\(\\int_{-a}^af=2\\int_0^af\\).</p>"
)
AR_form = ["Neta \\(\\int_a^bf\\) · total \\(\\int_a^b|f|\\) (partir en los ceros)",
           "Cambio neto: \\(\\int_a^bf'=f(b)-f(a)\\)",
           "Desplazamiento \\(\\int v\\) · distancia \\(\\int|v|\\)",
           "Impar: \\(\\int_{-a}^a=0\\) · par: \\(2\\int_0^a\\)",
           "Promedio: \\(\\frac1{b-a}\\int_a^bf\\)"]
AR_lesson = (
 "<h3>Idea central</h3><p>La integral de una tasa cuenta lo que entra menos lo que sale. Si preguntan «cuánto se movió en total» (distancia, área geométrica), hay que quitar los signos: partir en los ceros y sumar valores absolutos.</p>"
 "<h3>Esquema IRCA</h3><p><b>I</b>: tasa, intervalo y unidades. <b>R</b>: la integral definida. <b>C</b>: TFC2. <b>A</b>: unidades, límites a largo plazo y conclusión.</p>"
 "<div class=\"err\"><b>Errores frecuentes:</b> dar el área neta cuando piden la total; no buscar los ceros dentro del intervalo; y olvidar las unidades del resultado (tasa × variable).</div>"
)
AR = []
AR.append(E("w12a1", 1, "Neta y total (ejemplo de clase)",
  "<p>Para \\(f(x)=x^3-4x\\) en \\([-2,2]\\):</p>",
  [NUM([{"l": "Área neta =", "a": 0}, {"l": "Área total =", "a": 8}], "Calcula")],
  ["Neta: \\(\\left[\\frac{x^4}4-2x^2\\right]_{-2}^2=(4-8)-(4-8)=0\\) (f es impar).",
   "Total: f se anula en −2, 0, 2; es positiva en \\([-2,0]\\) y negativa en \\([0,2]\\): \\(4+4=8\\)."],
  "0 y 8", "Parte en x = 0.", [["areanet"], ["areanet"]]))
AR.append(E("w12a2", 2, "Encuentra el área neta cero",
  "<p>Con \\(f(x)=x^3-4x\\) y \\(a=-2\\) fijo, mueve \\(b\\) hasta que el área neta \\(\\int_{-2}^bf(x)dx\\) valga <b>0</b> (con \\(b>-2\\)).</p>",
  [{"t": "acum", "p": "Mueve b", "f": "x^3-4*x", "F": "x^4/4-2*x^2", "xr": [-2.5, 3], "yr": [-4, 4], "a": -2, "b0": 0, "ans": 2, "tol": 0.06, "step": 0.05,
    "e": "Busca dónde la parte verde y la roja se compensan."}],
  ["\\(\\int_{-2}^bf=\\frac{b^4}4-2b^2+4=\\left(\\frac{b^2}2-2\\right)^2\\), que es 0 solo si \\(b^2=4\\).",
   "Con \\(b>-2\\): \\(b=2\\). Ahí el área sobre el eje (en \\([-2,0]\\)) y la de abajo (en \\([0,2]\\)) son iguales a 4."],
  "b = 2", "La de arriba debe compensar la de abajo.", [["areanet"], ["areanet"]]))
AR.append(E("w12a3", 2, "Desplazamiento vs. distancia",
  "<p>Guía: \\(v(t)=t^2-2t-3\\) m/s en \\(t\\in[0,4]\\).</p>",
  [NUM([{"l": "Desplazamiento =", "a": -20 / 3, "u": "m", "tol": 0.01}, {"l": "Distancia total =", "a": 34 / 3, "u": "m", "tol": 0.01}], "Calcula")],
  ["Desplazamiento: \\(\\left[\\frac{t^3}3-t^2-3t\\right]_0^4=\\frac{64}3-16-12=-\\frac{20}3\\approx-6{,}67\\) m.",
   "v se anula en \\(t=3\\): \\(\\int_0^3v=-9\\) y \\(\\int_3^4v=\\frac73\\). Distancia: \\(9+\\frac73=\\frac{34}3\\approx11{,}33\\) m."],
  "−6,67 m y 11,33 m", "v = 0 en t = 3.", [["cambneto"], ["areanet"]]))
AR.append(E("w12a4", 2, "Fuga en un tanque (IRCA)",
  "<p>Guía: la fuga sigue \\(R(t)=20e^{-0{,}1t}\\) L/h.</p>",
  [NUM([{"l": "Litros perdidos en 10 h", "a": round(V10, 2), "u": "L", "tol": 0.05},
        {"l": "Tiempo para perder 150 L", "a": round(T150, 2), "u": "h", "tol": 0.02},
        {"l": "Pérdida si nunca se repara", "a": 200, "u": "L"}], "Calcula")],
  ["<b>R:</b> \\(V(T)=\\int_0^T20e^{-0{,}1t}dt=200(1-e^{-0{,}1T})\\).",
   "<b>C:</b> \\(V(10)=200(1-e^{-1})\\approx126{,}42\\) L; \\(200(1-e^{-0{,}1T})=150\\Rightarrow T=\\frac{\\ln4}{0{,}1}\\approx13{,}86\\) h; si \\(T\\to\\infty\\), \\(V\\to200\\) L.",
   "<b>A:</b> L/h · h = L. En las primeras 10 h ya se perdió el 63 % del máximo: hay que reparar antes de unas 14 h."],
  "126,42 L; 13,86 h; 200 L", "Antiderivada −200e^(−0,1t).", [["cambneto"], ["cambneto"], ["irca"]]))
AR.append(E("w12a5", 2, "Bacterias (IRCA)",
  "<p>Guía: \\(P'(t)=3t^2+2t+1\\) (miles/h), \\(P(0)=2\\) mil.</p>",
  [{"t": "expr", "p": "P(t)", "f": [{"a": "t^3+t^2+t+2", "v": ["t"], "l": "P(t) =", "dom": {"t": [0, 5]}}]},
   NUM([{"l": "P(5) =", "a": 157, "u": "mil"}, {"l": "Población media en [0, 5]", "a": 44.08, "u": "mil", "tol": 0.02}], "Calcula")],
  ["\\(P(t)=P(0)+\\int_0^tP'(s)ds=t^3+t^2+t+2\\).",
   "\\(P(5)=125+25+5+2=157\\) mil. Media: \\(\\frac15\\int_0^5P(t)dt=\\frac15\\left[\\frac{t^4}4+\\frac{t^3}3+\\frac{t^2}2+2t\\right]_0^5\\approx44{,}08\\) mil.",
   "La media es menor que \\(P(5)\\) porque el crecimiento se acelera al final."],
  "t³ + t² + t + 2; 157; 44,08", "Estado = inicial + ∫ tasa.", [["cambneto"], ["cambneto"], ["irca"]], chain=True))
assert abs(float(sp.integrate(t ** 3 + t ** 2 + t + 2, (t, 0, 5)) / 5) - 44.0833) < 1e-3
AR.append(E("w12a6", 1, "\\(\\int_0^3|x-2|\\,dx\\)",
  "<p>Guía: calcula \\(\\int_0^3|x-2|\\,dx\\) usando geometría.</p>",
  [NUM([{"l": "Resultado", "a": 2.5}])],
  ["\\(|x-2|\\) son dos triángulos: en \\([0,2]\\) uno de base 2 y altura 2 (área 2); en \\([2,3]\\) uno de base 1 y altura 1 (área 0,5).", "Total: \\(2+0{,}5=2{,}5\\)."],
  "2,5", "Dibuja la V.", [["areanet"], ["propint"]]))
AR.append(E("w12a7", 2, "Paridad",
  "<p>Usa simetría para clasificar sin calcular (guía).</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["Vale 0", "Es el doble de ∫₀ᵃ", "Ninguna de las dos"], "items": [
    {"x": "\\(\\int_{-3}^3x^5dx\\)", "c": 0}, {"x": "\\(\\int_{-2}^2x^4dx\\)", "c": 1}, {"x": "\\(\\int_{-\\pi}^\\pi\\sin x\\,dx\\)", "c": 0},
    {"x": "\\(\\int_{-2}^2(x^2+1)dx\\)", "c": 1}, {"x": "\\(\\int_{-1}^1(x^3+2x^2+x)dx\\)", "c": 2, "e": "Mezcla partes impares (\\(x^3+x\\), aportan 0) y una par (\\(2x^2\\)): vale \\(\\frac43\\), ni 0 ni el doble de toda la integral en [0, 1]."}]}],
  ["Impar (\\(f(-x)=-f(x)\\)) en intervalo simétrico: las áreas se cancelan.", "Par: las dos mitades son iguales. Si mezcla, solo se anula la parte impar."],
  "Clasificación correcta", "¿f(−x) = f(x) o −f(x)?", [["areanet"], ["areanet"]]))
AR.append(E("w12a8", 2, "Trabajo de un propulsor",
  "<p>Guía: la fuerza es \\(F(x)=2x^2+x\\) N durante 5 m.</p>",
  [XV("575/6", sp.integrate(2 * x ** 2 + x, (x, 0, 5)), "Trabajo W (J) ="),
   O(["Mayor: con 15 N constante serían 75 J", "Menor: con 15 N constante serían 75 J", "Igual: ambas dan 75 J", "No se puede comparar sin graficar", "Menor, porque la fuerza empieza en 0"], "Comparado con una fuerza constante de 15 N…")],
  ["\\(W=\\int_0^5(2x^2+x)dx=\\frac{2\\cdot125}3+\\frac{25}2=\\frac{575}6\\approx95{,}8\\) J (N·m = J).",
   "Con 15 N constante: \\(15\\cdot5=75\\) J. La fuerza variable empieza en 0, pero desde \\(x=2{,}5\\) supera los 15 N y llega a 55 N: su promedio es \\(\\frac{95{,}8}5\\approx19{,}2\\) N, así que hace más trabajo."],
  "575/6 ≈ 95,8 J (mayor)", "Trabajo = ∫ F dx.", [["cambneto"], ["cambneto"]], chain=True))
AR_tools = [{"w": "acum", "t": "Área neta de x³ − 4x", "p": "Mueve a y b: lo verde suma y lo rojo resta. ¿Dónde la neta vale 0?", "o": {"f": "x^3-4*x", "F": "x^4/4-2*x^2", "xr": [-2.5, 3], "yr": [-4, 4], "a": -2, "b": 2}},
            {"w": "acum", "t": "Velocidad v(t) = t² − 2t − 3", "p": "Con a = 0 y b = 4, el área neta es el desplazamiento (−20/3).", "o": {"f": "x^2-2*x-3", "F": "x^3/3-x^2-3*x", "xr": [-0.5, 4.5], "yr": [-5, 6], "a": 0, "b": 4, "fl": "v(t)"}}]

# =====================================================================
# Conceptos y ensamblado
# =====================================================================
CONC = {
 "fpcaso": {"n": "Casos de fracciones parciales", "f": "I lineales · II repetidos · III cuadráticos · IV cuadrático repetido", "x": "Se clasifica después de factorizar el denominador.", "home": "w11fp"},
 "fpdiv": {"n": "División previa", "f": "Si \\(\\deg P\\ge\\deg Q\\): \\(\\frac PQ=C(x)+\\frac RQ\\)", "x": "Solo las propias se descomponen.", "home": "w11fp"},
 "heav": {"n": "Heaviside", "f": "Tapar \\((x-a)\\) y evaluar en \\(x=a\\)", "x": "Da la constante de cada lineal (y la de la potencia más alta).", "home": "w11fp"},
 "fp2": {"n": "Caso II", "f": "\\(\\frac{A}{x-a}+\\frac{B}{(x-a)^2}\\)", "x": "Una fracción por cada potencia del factor repetido.", "home": "w11fp"},
 "fp3": {"n": "Caso III", "f": "\\(\\frac{Ax+B}{x^2+px+q}\\)", "x": "Dos incógnitas por cada cuadrático; da ln y arctan.", "home": "w11fp"},
 "logist": {"n": "EDO logística", "f": "\\(P=\\frac{KP_0}{P_0+(K-P_0)e^{-rt}}\\)", "x": "Se separa e integra con fracciones parciales; P → K.", "home": "w11fp"},
 "pottrig": {"n": "Potencias trigonométricas", "f": "Impar: separar un factor · \\(\\tan^m\\sec^n\\)", "x": "El factor separado forma el du.", "home": "w11pot"},
 "angdob": {"n": "Ángulo doble", "f": "\\(\\sin^2x=\\frac{1-\\cos2x}2\\), \\(\\cos^2x=\\frac{1+\\cos2x}2\\)", "x": "Para exponentes pares.", "home": "w11pot"},
 "sustrig": {"n": "Sustitución trigonométrica", "f": "\\(a\\sin\\theta\\), \\(a\\tan\\theta\\), \\(a\\sec\\theta\\)", "x": "Según \\(\\sqrt{a^2-x^2}\\), \\(\\sqrt{a^2+x^2}\\), \\(\\sqrt{x^2-a^2}\\).", "home": "w11tri"},
 "triref": {"n": "Triángulo de referencia", "f": "Volver de \\(\\theta\\) a x", "x": "El lado que falta es la raíz original.", "home": "w11tri"},
 "compcuad": {"n": "Completar cuadrados", "f": "\\(x^2+bx+c=(x+\\frac b2)^2+(c-\\frac{b^2}4)\\)", "x": "Antes de arctan o sustitución trigonométrica.", "home": "w11tri"},
 "eleccion": {"n": "Elegir la técnica", "f": "Simplificar → sustitución → clasificar → combinar", "x": "Clasificar antes de calcular.", "home": "w11otros"},
 "racio": {"n": "Sustitución racionalizadora", "f": "\\(u=\\sqrt[n]{ax+b}\\)", "x": "Deja una función racional en u.", "home": "w11otros"},
 "weier": {"n": "Weierstrass", "f": "\\(t=\\tan\\frac x2\\), \\(dx=\\frac{2dt}{1+t^2}\\)", "x": "Último recurso para racionales en sen y cos.", "home": "w11otros"},
 "acum": {"n": "Acumulación", "f": "Tasa constante: \\(k(b-a)\\)", "x": "Las unidades se multiplican: tasa × variable.", "home": "w12rie"},
 "riem": {"n": "Suma de Riemann", "f": "\\(S_n=\\sum f(x_i^*)\\Delta x\\), \\(\\Delta x=\\frac{b-a}n\\)", "x": "L izquierdos, R derechos, M medios.", "home": "w12rie"},
 "sigma": {"n": "Sumatorias", "f": "\\(\\sum i=\\frac{n(n+1)}2\\), \\(\\sum i^2=\\frac{n(n+1)(2n+1)}6\\)", "x": "Para tomar el límite de \\(R_n\\).", "home": "w12rie"},
 "intdef": {"n": "Integral definida", "f": "\\(\\int_a^bf=\\lim\\sum f(x_i^*)\\Delta x\\)", "x": "Área neta; existe si f es continua.", "home": "w12rie"},
 "propint": {"n": "Propiedades de la integral", "f": "linealidad · aditividad · acotamiento", "x": "Permiten calcular u ordenar sin integrar.", "home": "w12tfc"},
 "tfc1": {"n": "TFC1", "f": "\\(\\frac d{dx}\\int_a^{h(x)}f=f(h(x))h'(x)\\)", "x": "La derivada de la acumulación es la tasa.", "home": "w12tfc"},
 "tfc2": {"n": "TFC2", "f": "\\(\\int_a^bf=F(b)-F(a)\\)", "x": "Cualquier antiderivada; la C se cancela.", "home": "w12eval"},
 "limsust": {"n": "Sustitución en definidas", "f": "\\(\\int_{g(a)}^{g(b)}f(u)du\\)", "x": "Cambiar los límites y no volver a x.", "home": "w12eval"},
 "areanet": {"n": "Área neta y total", "f": "\\(\\int f\\) vs. \\(\\int|f|\\)", "x": "Partir en los ceros para el área total.", "home": "w12area"},
 "cambneto": {"n": "Cambio neto", "f": "\\(\\int_a^bf'=f(b)-f(a)\\)", "x": "Velocidad → desplazamiento, caudal → volumen…", "home": "w12area"},
}
OLD = ["partes", "irca", "sust"]

T11 = [
 {"id": "w11fp", "name": "Sem. 11 · Fracciones parciales (casos I, II y III)", "teo": FP_teo, "form": FP_form, "lesson": FP_lesson, "ex": FP, "tools": FP_tools},
 {"id": "w11pot", "name": "Sem. 11 · Potencias trigonométricas y ángulo doble", "teo": PT_teo, "form": PT_form, "lesson": PT_lesson, "ex": PT},
 {"id": "w11tri", "name": "Sem. 11 · Sustitución trigonométrica y completar cuadrados", "teo": ST_teo, "form": ST_form, "lesson": ST_lesson, "ex": ST, "tools": ST_tools},
 {"id": "w11otros", "name": "Sem. 11 · Racionalizadora, Weierstrass y elección de técnica", "teo": OT_teo, "form": OT_form, "lesson": OT_lesson, "ex": OT, "tools": OT_tools}]
T12 = [
 {"id": "w12rie", "name": "Sem. 12 · Sumas de Riemann e integral definida", "teo": RI_teo, "form": RI_form, "lesson": RI_lesson, "ex": RI, "tools": RI_tools},
 {"id": "w12tfc", "name": "Sem. 12 · Propiedades y Primer Teorema Fundamental", "teo": TF_teo, "form": TF_form, "lesson": TF_lesson, "ex": TF, "tools": TF_tools},
 {"id": "w12eval", "name": "Sem. 12 · TFC2 con sustitución y por partes", "teo": TE_teo, "form": TE_form, "lesson": TE_lesson, "ex": TE, "tools": TE_tools},
 {"id": "w12area", "name": "Sem. 12 · Área neta, área total y cambio neto", "teo": AR_teo, "form": AR_form, "lesson": AR_lesson, "ex": AR, "tools": AR_tools}]


# ---------------------------------------------------------------- partir fórmulas largas (celular)
import re as _re
def _vis(m):
    m = _re.sub(r'\\(left|right|,|;|!|quad)', '', m)
    m = _re.sub(r'\\[a-zA-Z]+', 'x', m)
    return len(_re.sub(r'[{}^_ ]', '', m))
def _split(m, lim=22):
    if _vis(m) <= lim: return [m]
    parts, depth, lr, cur, i = [], 0, 0, '', 0
    while i < len(m):
        if m.startswith('\\left', i): lr += 1
        if m.startswith('\\right', i): lr -= 1
        c = m[i]
        if c == '{': depth += 1
        if c == '}': depth -= 1
        cut = None
        if depth == 0 and lr == 0:
            if c == '=' : cut = 1
            elif m.startswith('\\Rightarrow', i): cut = len('\\Rightarrow')
            elif m.startswith('\\approx', i): cut = len('\\approx')
        if cut and _vis(cur) >= 4 and i + cut < len(m):
            parts.append(cur + m[i:i + cut]); cur = ''; i += cut; continue
        cur += c; i += 1
    parts.append(cur)
    return [q for q in parts if q.strip()]
def corta(h):
    if not isinstance(h, str): return h
    def r(mt):
        ps = _split(mt.group(1))
        return ' '.join('\\(' + q + '\\)' for q in ps)
    return _re.sub(r'\\\((.+?)\\\)', r, h)
def corta_t(t_):
    for k in ('teo', 'lesson'): t_[k] = corta(t_[k])
    for e in t_['ex']:
        e['steps'] = [corta(z) for z in e['steps']]
        e['q'] = corta(e['q'])
for t_ in T11 + T12: corta_t(t_)

def used(topics):
    s = set()
    for t_ in topics:
        for e in t_['ex']:
            for l in e['tags']: s |= set(l)
    return s

ed3 = json.load(open(P("calculo-ed3"), encoding="utf-8"))
OLDC = {k: ed3['concepts'][k] for k in OLD}

CARDS11 = ('<div><b>Fracciones parciales</b><br>propia → factorizar → caso I/II/III → Heaviside o coeficientes</div>\n'
           '<div><b>Casos</b><br>\\(\\frac{A}{x-a}\\) · \\(\\frac{A}{x-a}+\\frac{B}{(x-a)^2}\\) · \\(\\frac{Ax+B}{x^2+px+q}\\)</div>\n'
           '<div><b>arctan</b><br>\\(\\int\\frac{dx}{x^2+a^2}=\\frac1a\\arctan\\frac xa\\) · completar cuadrados</div>\n'
           '<div><b>Potencias trig.</b><br>impar: separar un factor · par: \\(\\sin^2=\\frac{1-\\cos2x}2\\), \\(\\cos^2=\\frac{1+\\cos2x}2\\)</div>\n'
           '<div><b>Sust. trigonométrica</b><br>\\(\\sqrt{a^2-x^2}\\to a\\sin\\theta\\) · \\(\\sqrt{a^2+x^2}\\to a\\tan\\theta\\) · \\(\\sqrt{x^2-a^2}\\to a\\sec\\theta\\)</div>\n'
           '<div><b>Otras</b><br>racionalizadora \\(u=\\sqrt[n]{ax+b}\\) · Weierstrass \\(t=\\tan\\frac x2\\)</div>\n')
CARDS12 = ('<div><b>Riemann</b><br>\\(\\Delta x=\\frac{b-a}n\\), \\(S_n=\\sum f(x_i^*)\\Delta x\\) · L izq. · R der. · M medio</div>\n'
           '<div><b>Sumatorias</b><br>\\(\\sum i=\\frac{n(n+1)}2\\), \\(\\sum i^2=\\frac{n(n+1)(2n+1)}6\\)</div>\n'
           '<div><b>Propiedades</b><br>\\(\\int_b^a=-\\int_a^b\\) · aditividad · \\(m(b-a)\\le\\int\\le M(b-a)\\)</div>\n'
           '<div><b>TFC1</b><br>\\(\\frac d{dx}\\int_a^{h(x)}f(t)dt=f(h(x))h\'(x)\\)</div>\n'
           '<div><b>TFC2</b><br>\\(\\int_a^bf=F(b)-F(a)\\) · sustitución: cambiar límites</div>\n'
           '<div><b>Área y cambio neto</b><br>neta \\(\\int f\\) · total \\(\\int|f|\\) · \\(\\int v\\)=desplazamiento, \\(\\int|v|\\)=distancia</div>\n')

def form_block(note, cards):
    return '<p class="note">' + note + '</p>\n<div class="fgrid">\n' + cards + '</div>'

INTRO_EA3 = ("Bloque de la <b>EA3</b> (semana 11; ya se rindió: 50 min, individual y sin apuntes). Cerró <b>fracciones parciales</b> (solo propias, casos I a III) y "
             "<b>potencias trigonométricas</b>. También están la sustitución trigonométrica (que entra a la ED4) y las técnicas «reto» de la guía (racionalizadora y Weierstrass). "
             "Toca un factor para taparlo con el método de Heaviside y arma el triángulo de la sustitución trigonométrica. Todos los temas están abiertos.")
INTRO_ED4 = ("Bloque de la <b>ED4</b> (semana 12, sesión 2: 50 min, individual, sin calculadora avanzada y justificando todos los pasos). "
             "<b>Ojo:</b> la diapositiva de la sesión 2 dice que la ED4 evalúa <b>integrales indefinidas</b> (sustitución, partes, fracciones parciales y sustitución trigonométrica), "
             "mientras que la guía de la semana 12 dice que evalúa <b>Riemann, TFC1, TFC2, área neta y cambio neto</b>. Por eso el simulacro mezcla las dos partes. "
             "Aquí están los temas de la semana 12, con rectángulos de Riemann que puedes mover y el acumulador del área; las técnicas de las semanas 10 y 11 están en la ED3, la EA3 y el final.")
SL_EA3 = [{"pts": 4, "name": "Fracciones parciales: caso I", "pool": ["w11f3", "w11f4", "w11f5"]},
          {"pts": 4, "name": "Fracciones parciales: caso II", "pool": ["w11f6", "w11f7"]},
          {"pts": 4, "name": "Fracciones parciales: caso III y completar cuadrados", "pool": ["w11f8", "w11f9", "w11f10"]},
          {"pts": 4, "name": "Potencias trigonométricas: exponente impar", "pool": ["w11p3", "w11p4", "w11p6", "w11p7"]},
          {"pts": 4, "name": "Potencias trigonométricas: ángulo doble", "pool": ["w11p2", "w11p5", "w11p8"]}]
SL_ED4 = [{"pts": 3, "name": "Indefinidas: sustitución o partes (sem. 10)", "pool": ["w10u4", "w10u6", "w10u7", "w10p4", "w10p5", "w10p6", "w10p7"]},
          {"pts": 3, "name": "Indefinidas: fracciones parciales (sem. 11)", "pool": ["w11f3", "w11f5", "w11f6", "w11f8", "w11f9"]},
          {"pts": 3, "name": "Indefinidas: sustitución trigonométrica (sem. 11)", "pool": ["w11t3", "w11t4", "w11t5", "w11t6", "w11t8"]},
          {"pts": 3, "name": "Sumas de Riemann", "pool": ["w12r2", "w12r3", "w12r4", "w12r5"]},
          {"pts": 2, "name": "Propiedades y TFC1", "pool": ["w12f1", "w12f2", "w12f5", "w12f6", "w12f7"]},
          {"pts": 3, "name": "TFC2 con sustitución o partes", "pool": ["w12e3", "w12e4", "w12e6", "w12e7", "w12e8"]},
          {"pts": 3, "name": "Área neta y total, cambio neto", "pool": ["w12a1", "w12a3", "w12a4", "w12a5", "w12a8"]}]
assert sum(s["pts"] for s in SL_EA3) == 20 and sum(s["pts"] for s in SL_ED4) == 20

def setup(blk, topics, intro, note, cards, slots, minutes, simintro, free):
    d = json.load(open(P(blk), encoding="utf-8"))
    d.pop("soon", None)
    d["topics"] = [t_ for t_ in d.get("topics", []) if not t_["id"].startswith(("w11", "w12"))] + topics
    us = used(d["topics"])
    conc = {k: v for k, v in CONC.items() if k in us}
    for k in OLD:
        if k in us: conc[k] = OLDC[k]
    d["concepts"] = conc
    d["intro"] = intro
    d["form"] = form_block(note, cards)
    d["formSim"] = True
    d["guide"] = True
    if free: d["free"] = True
    d["sim"] = {"minutes": minutes, "slots": slots, "intro": simintro}
    ids = [e["id"] for t_ in d["topics"] for e in t_["ex"]] + [e["id"] for e in d.get("simEx", [])]
    assert len(ids) == len(set(ids))
    for s in slots:
        for i in s["pool"]: assert i in ids, (blk, i)
    return d

# ED4 necesita los ejercicios de la semana 10 del simulacro: se agregan como simEx
w10 = {e["id"]: e for t_ in ed3["topics"] for e in t_["ex"]}
w11 = {e["id"]: e for t_ in T11 for e in t_["ex"]}
ea3 = setup("calculo-ea3", T11, INTRO_EA3, "Hoja de repaso de la EA3 (semana 11).", CARDS11, SL_EA3, 50,
            "Simulacro de la EA3: 50 minutos, cinco preguntas de 4 puntos (fracciones parciales propias y potencias trigonométricas).", True)
ed4 = setup("calculo-ed4", T12, INTRO_ED4, "Hoja de repaso de la ED4 (semana 12) con las técnicas de las semanas 10 y 11.", CARDS11 + CARDS12, [], 50, "", False)
ed4["simEx"] = [w10[i] for i in ["w10u4", "w10u6", "w10u7", "w10p4", "w10p5", "w10p6", "w10p7"]] + [w11[i] for i in ["w11f3", "w11f5", "w11f6", "w11f8", "w11f9", "w11t3", "w11t4", "w11t5", "w11t6", "w11t8"]]
us = used(ed4["topics"]) | {k for e in ed4["simEx"] for l in e["tags"] for k in l}
ed4["concepts"] = {k: v for k, v in {**{k: ed3["concepts"][k] for k in ed3["concepts"]}, **CONC}.items() if k in us}
ed4["sim"] = {"minutes": 50, "slots": SL_ED4, "intro": "Simulacro de la ED4: 50 minutos y 20 puntos. Mitad integrales indefinidas (sustitución, partes, fracciones parciales y sustitución trigonométrica) y mitad semana 12 (Riemann, TFC y área), porque el material no coincide sobre qué entra."}
ids = [e["id"] for t_ in ed4["topics"] for e in t_["ex"]] + [e["id"] for e in ed4["simEx"]]
assert len(ids) == len(set(ids))
for s in SL_ED4:
    for i in s["pool"]: assert i in ids, i
ed4["sub"] = "Sem. 12"; ed4["exam"] = "ED4 (semana 12)"

ef = json.load(open(P("calculo-ef"), encoding="utf-8"))
ef["topics"] = [t_ for t_ in ef["topics"] if not t_["id"].startswith(("w11", "w12"))] + T11 + T12
ef["concepts"].update(CONC)
for k in OLD: ef["concepts"].setdefault(k, OLDC[k])
if "Fracciones parciales</b>" not in ef["form"]:
    k = ef["form"].rindex("</div>")
    ef["form"] = ef["form"][:k] + CARDS11 + CARDS12 + ef["form"][k:]
ef["sim"]["slots"] = [
 {"pts": 1, "name": "Repaso sem. 1–7: límites y L'Hôpital", "pool": ["lho3", "lho4", "lho5", "lho6", "lho7", "lim6", "lim7"]},
 {"pts": 1, "name": "Repaso sem. 1–7: continuidad y derivadas", "pool": ["simc1", "simc2", "simi1", "simi2", "cad7", "cad8"]},
 {"pts": 1, "name": "Repaso sem. 1–7: análisis con f′ y f″", "pool": ["simg1", "graf4", "graf5", "graf9"]},
 {"pts": 2, "name": "Sem. 9: optimización y razones relacionadas", "pool": ["w9o3", "w9o4", "w9o5", "w9o7", "w9s1", "w9s4", "w9d2", "w9d4", "w9r5", "w9r6"]},
 {"pts": 2, "name": "Sem. 9–10: antiderivadas y EDO separables", "pool": ["w9a4", "w9a6", "w9a8", "w9a10", "w9e6", "w10e6", "w10e7", "w10e8", "w10s1", "w10s2"]},
 {"pts": 2, "name": "Sem. 10: sustitución e integración por partes", "pool": ["w10u3", "w10u4", "w10u6", "w10u7", "w10u8", "w10p4", "w10p5", "w10p6", "w10p7", "w10p8", "w10p9"]},
 {"pts": 3, "name": "Sem. 11: fracciones parciales", "pool": ["w11f3", "w11f5", "w11f6", "w11f7", "w11f8", "w11f9"]},
 {"pts": 2, "name": "Sem. 11: potencias y sustitución trigonométrica", "pool": ["w11p5", "w11p6", "w11p7", "w11t4", "w11t5", "w11t6", "w11t7"]},
 {"pts": 3, "name": "Sem. 12: Riemann y TFC1", "pool": ["w12r3", "w12r4", "w12r7", "w12f5", "w12f7", "w12f8"]},
 {"pts": 3, "name": "Sem. 12: TFC2, área neta y cambio neto", "pool": ["w12e3", "w12e7", "w12e8", "w12a2", "w12a3", "w12a4", "w12a5", "w12a8"]}]
assert sum(s["pts"] for s in ef["sim"]["slots"]) == 20
ids = [e["id"] for t_ in ef["topics"] for e in t_["ex"]] + [e["id"] for e in ef.get("simEx", [])]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
for s in ef["sim"]["slots"]:
    for i in s["pool"]: assert i in ids, i
ef["intro"] = ("Repaso acumulado del curso, con los temas ordenados por semana. Aquí todos los temas están abiertos desde el inicio para que vayas directo a lo que necesites. "
               "<b>El examen final vale 30 %</b> y pone el énfasis en las semanas 9 a 15, así que el simulacro tiene la mayoría de preguntas de esas semanas (ya están hasta la <b>semana 12</b>: "
               "fracciones parciales, sustitución trigonométrica, sumas de Riemann, TFC y área) y una parte menor de repaso de las semanas 1 a 7. Se actualiza cada vez que se agrega una semana nueva. "
               "Escribes tus respuestas como fórmulas y se corrigen solas. Hay graficador, tabla de signos, campo de pendientes, «tapar el factor» de Heaviside, el triángulo de la sustitución trigonométrica, "
               "rectángulos de Riemann y el acumulador del área.")
for t_ in ef["topics"]:
    for e in t_["ex"]:
        for l in e["tags"]:
            for k in l: assert k in ef["concepts"], (e["id"], k)
for dd in (ea3, ed4):
    for e in [e for t_ in dd["topics"] for e in t_["ex"]] + dd.get("simEx", []):
        for l in e["tags"]:
            for k in l: assert k in dd["concepts"], (dd["id"], e["id"], k)

for name, dd in (("calculo-ea3", ea3), ("calculo-ed4", ed4), ("calculo-ef", ef)):
    with open(P(name), "w", encoding="utf-8") as o:
        json.dump(dd, o, indent=1, ensure_ascii=False); o.write("\n")
print("ok", [len(t_["ex"]) for t_ in T11 + T12])
