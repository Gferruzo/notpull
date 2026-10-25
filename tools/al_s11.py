#!/usr/bin/env python3
"""Álgebra Lineal (CC6105) · Semana 11: valores y vectores propios → cursos/al-ea3.json y cursos/al-ef.json (tema s11).
Todo se comprueba con sympy (polinomio característico, valores propios, espacios propios, rangos y potencias).
Uso: python3 tools/al_s11.py   (reejecutable: reemplaza el tema s11)."""
import json, os
import sympy as sp

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(RAIZ, "cursos", n + ".json")
L = sp.symbols('lambda')
M = sp.Matrix

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

def tex(A):
    return "\\(\\begin{pmatrix}" + "\\\\".join("&".join(sp.latex(v) for v in A.row(i)) for i in range(A.rows)) + "\\end{pmatrix}\\)"

def charp(A): return sp.expand((A - L * sp.eye(A.rows)).det())

def mults(A, l):
    ma = sp.roots(sp.Poly(charp(A), L))[l]
    mg = A.rows - (A - l * sp.eye(A.rows)).rank()
    return ma, mg

# ---------------------------------------------------------------- datos (todos de la clase y el laboratorio)
A = M([[4, 1], [2, 3]])
assert sp.factor(charp(A)) == (L - 2) * (L - 5)
assert A * M([1, 1]) == 5 * M([1, 1]) and A * M([1, -2]) == 2 * M([1, -2]) and A * M([1, 0]) == M([4, 2])
assert A ** 3 == M([[86, 39], [78, 47]]) and A ** 3 * M([1, 1]) == 125 * M([1, 1])
B = M([[5, -2], [1, 2]])
assert sp.factor(charp(B)) == (L - 3) * (L - 4)
assert B * M([1, 1]) == 3 * M([1, 1]) and B * M([2, 1]) == 4 * M([2, 1])
assert B ** 3 * M([2, 1]) == M([128, 64]) and B ** 3 * M([3, 2]) == M([155, 91])
assert (B ** 2).trace() == 25 and set((B ** 2).eigenvals()) == {9, 16} and set(B.inv().eigenvals()) == {sp.Rational(1, 3), sp.Rational(1, 4)}
assert set(B.rref()[0].eigenvals()) == {1}
R = M([[0, -1], [1, 0]])
assert charp(R) == L ** 2 + 1
F = M([[0, 1], [1, 0]])
assert F * M([1, -1]) == -M([1, -1]) and set(F.eigenvals()) == {1, -1}
A5 = M([[4, -1, 6], [2, 1, 6], [2, -1, 8]])
assert sp.factor(charp(A5)) == -(L - 2) ** 2 * (L - 9) and A5.trace() == 13 and A5.det() == 36
assert mults(A5, 2) == (2, 2) and mults(A5, 9) == (1, 1)
for v in (M([1, 2, 0]), M([-3, 0, 1])): assert A5 * v == 2 * v
assert A5 * M([1, 1, 1]) == 9 * M([1, 1, 1])
C = M([[2, 1, 0], [0, 2, 0], [0, 0, 3]]); D = M([[2, 0, 0], [0, 2, 0], [0, 0, 3]])
assert mults(C, 2) == (2, 1) and mults(D, 2) == (2, 2) and mults(C, 3) == (1, 1)
Bt = M([[2, 0, 0], [1, 2, 0], [0, 0, 3]])
assert mults(Bt, 2) == (2, 1)
A0 = M([[1, 2], [2, 4]])
assert A0 * M([-2, 1]) == M([0, 0]) and sp.factor(charp(A0)) == L * (L - 5)
J = M([[2, 1], [0, 2]]); K = M([[3, 0], [0, 3]])
assert mults(J, 2) == (2, 1) and mults(K, 3) == (2, 2)
Pl = M([[2, 1], [1, 2]])
assert set(Pl.eigenvals()) == {1, 3}
# ejercicio extra: 3×3 con valores 1, 2, 3 (comprobar traza/det)
assert 1 + 2 + 3 == 6 and 1 * 2 * 3 == 6

TEO = (
 "<p>Una matriz representa una transformación \\(T(x)=Ax\\). Un <strong>vector propio</strong> es una dirección que \\(A\\) no saca de su recta: solo la estira, encoge o invierte.</p>"
 "<p><b>Definición:</b> \\(\\lambda\\) es <strong>valor propio</strong> de \\(A\\in\\mathbb R^{n\\times n}\\) si existe \\(v\\ne0\\) con \\(Av=\\lambda v\\); \\(v\\) es un vector propio asociado. \\(v=0\\) nunca es vector propio, pero \\(\\lambda=0\\) sí puede ser valor propio. Si \\(v\\) es propio, también \\(cv\\) (\\(c\\ne0\\)).</p>"
 "<p><b>Cálculo:</b> \\(Av=\\lambda v,\\ v\\ne0\\iff(A-\\lambda I)v=0\\) no trivial \\(\\iff\\det(A-\\lambda I)=0\\).</p>"
 "<ol><li>\\(p(\\lambda)=\\det(A-\\lambda I)\\) (polinomio característico, grado n).</li><li>Sus raíces son los valores propios.</li><li>Para cada \\(\\lambda\\), el <b>espacio propio</b> \\(E_\\lambda=\\operatorname{Nul}(A-\\lambda I)\\): se reduce \\(A-\\lambda I\\) (debe salir una fila nula).</li></ol>"
 "<p class=\"ej\"><b>Ejemplo de clase:</b> " + tex(A) + ": \\(p(\\lambda)=\\lambda^2-7\\lambda+10\\) \\(=(\\lambda-2)(\\lambda-5)\\); \\(E_2=\\operatorname{Gen}\\{(1,-2)\\}\\), \\(E_5=\\operatorname{Gen}\\{(1,1)\\}\\).</p>"
 "<p><b>Propiedades</b> (en \\(\\mathbb C\\), contando multiplicidades): \\(\\operatorname{tr}A=\\lambda_1+\\dots+\\lambda_n\\), \\(\\det A=\\lambda_1\\cdots\\lambda_n\\); \\(A\\) invertible \\(\\iff0\\) no es valor propio. Si \\(Av=\\lambda v\\): \\(A^kv=\\lambda^kv\\), \\(A^{-1}v=\\frac1\\lambda v\\), \\((A+cI)v=(\\lambda+c)v\\), con el mismo vector propio. En 2 × 2: \\(p(\\lambda)=\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A\\).</p>"
 "<div class=\"tbl\"><table><tr><th>Matriz</th><th>Valores propios</th></tr><tr><td>Triangular o diagonal</td><td>la diagonal</td></tr><tr><td>Singular</td><td>incluye 0</td></tr><tr><td>Reflexión en \\(\\mathbb R^2\\)</td><td>1 y −1</td></tr><tr><td>Rotación \\(\\theta\\ne0,\\pi\\)</td><td>complejos (ninguno real)</td></tr><tr><td>\\(kI\\)</td><td>k (doble)</td></tr></table></div>"
 "<p><b>Multiplicidades:</b> algebraica \\(m_a(\\lambda)\\) = veces que \\(\\lambda\\) es raíz de \\(p\\); geométrica \\(m_g(\\lambda)=\\dim E_\\lambda=n-\\operatorname{rank}(A-\\lambda I)\\). Siempre \\(1\\le m_g\\le m_a\\).</p>"
 "<p><b>MATLAB:</b> <code>poly(A)</code>, <code>roots(p)</code>, <code>[V,D] = eig(A)</code> (columnas de V normalizadas: múltiplos de tus vectores), <code>null(A - 2*eye(3), 'r')</code>, <code>3 - rank(A - 2*eye(3))</code>.</p>"
)
FORM = ["\\(Av=\\lambda v\\), \\(v\\ne0\\) (λ = 0 sí puede)",
        "\\(p(\\lambda)=\\det(A-\\lambda I)\\) · 2 × 2: \\(\\lambda^2-\\operatorname{tr}A\\,\\lambda+\\det A\\)",
        "\\(E_\\lambda=\\operatorname{Nul}(A-\\lambda I)\\)",
        "\\(\\operatorname{tr}A=\\sum\\lambda_i\\), \\(\\det A=\\prod\\lambda_i\\)",
        "\\(A^kv=\\lambda^kv\\), \\(A^{-1}v=\\frac1\\lambda v\\)",
        "\\(m_g=n-\\operatorname{rank}(A-\\lambda I)\\), \\(1\\le m_g\\le m_a\\)",
        "Triangular: λ en la diagonal (¡nunca leerlos de rref!)"]
LESSON = (
 "<h3>Idea central</h3><p>El polinomio característico da los \\(\\lambda\\); el espacio nulo de \\(A-\\lambda I\\) da los vectores. Traza, determinante y potencias sirven para <b>anticipar y verificar</b> sin rehacer cálculos.</p>"
 "<h3>Receta</h3><ol><li>\\(p(\\lambda)=\\det(A-\\lambda I)\\) y sus raíces (en 2 × 2 busca dos números con suma tr A y producto det A).</li><li>Comprueba: \\(\\sum\\lambda=\\operatorname{tr}A\\), \\(\\prod\\lambda=\\det A\\).</li><li>Para cada \\(\\lambda\\): reduce \\(A-\\lambda I\\); si no aparece una fila nula, el \\(\\lambda\\) está mal.</li><li>Base de \\(E_\\lambda\\) con las variables libres; \\(m_g\\) = número de libres.</li><li>Verifica \\(Av=\\lambda v\\).</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes (caza de errores del lab):</b> escalonar \\(A\\) y leer la diagonal (las operaciones por fila cambian los valores propios: \\(\\operatorname{rref}(B)=I\\) daría 1 y 1, pero son 3 y 4); decir que \\(\\lambda=0\\) no puede ser valor propio (lo prohibido es \\(v=0\\)); y suponer que una raíz doble da dos vectores propios independientes (\\(m_g\\) puede ser 1).</div>"
)
EX = []
EX.append(E("s11e1", 1, "¿Es o no es vector propio?",
  "<p>Ejemplo guiado 1: \\(A=\\)" + tex(A) + ". Clasifica cada candidato y luego da su valor propio.</p>",
  [{"t": "cls", "p": "Calcula Av para cada uno", "cats": ["Vector propio", "No es vector propio"], "items": [
     {"x": "\\(u=(1,1)\\)", "c": 0}, {"x": "\\(w=(1,-2)\\)", "c": 0}, {"x": "\\(z=(1,0)\\)", "c": 1, "e": "\\(Az=(4,2)\\): cambia de recta (la 2.ª componente pasa de 0 a 2)."},
     {"x": "\\(3u=(3,3)\\)", "c": 0, "e": "Todo múltiplo no nulo de un vector propio también lo es."}, {"x": "\\((0,0)\\)", "c": 1, "e": "El vector cero nunca es vector propio."}]},
   NUM([{"l": "λ de u", "a": 5}, {"l": "λ de w", "a": 2}], "Valores propios")],
  ["\\(Au=(5,5)=5u\\) y \\(Aw=(2,-4)=2w\\); \\(Az=(4,2)\\ne cz\\).",
   "Comprobación: \\(5+2=7=\\operatorname{tr}A\\) y \\(5\\cdot2=10=\\det A\\): no falta ningún valor propio."],
  "u y w (λ = 5 y 2); z no", "Calcula Av y compara con v.", [["vprop"], ["trdet"]], chain=True))
EX.append(E("s11e2", 1, "Si \\(Av=0\\) con \\(v\\ne0\\)…",
  "<p>Checkpoint de clase: se sabe que \\(Av=0\\) para cierto \\(v\\ne0\\). ¿Qué se puede afirmar con certeza?</p>",
  [O(["\\(\\lambda=0\\) es valor propio y \\(A\\) no es invertible", "\\(A\\) es la matriz nula", "\\(v\\) no puede ser vector propio porque \\(Av=0\\)", "\\(A\\) no tiene valores propios", "\\(\\det A\\ne0\\)"])],
  ["\\(Av=0=0\\cdot v\\) con \\(v\\ne0\\): \\(\\lambda=0\\) es valor propio y \\(v\\) es vector propio.",
   "\\(\\operatorname{Nul}A\\ne\\{0\\}\\Rightarrow\\det A=0\\): A no es invertible. Lo prohibido es \\(v=0\\), no \\(\\lambda=0\\)."],
  "λ = 0 es valor propio; A singular", "Lo prohibido es v = 0.", [["vprop"], ["trdet"]]))
EX.append(E("s11e3", 1, "Polinomio característico",
  "<p>Ejemplo guiado 2: halla \\(p(\\lambda)=\\det(A-\\lambda I)\\) para \\(A=\\)" + tex(A) + " y sus raíces.</p>",
  [NUM([{"l": "p(λ) = λ² + bλ + c:  b =", "a": -7}, {"l": "c =", "a": 10}], "Coeficientes"),
   NUM([{"l": "λ₁ (menor) =", "a": 2}, {"l": "λ₂ (mayor) =", "a": 5}], "Valores propios")],
  ["\\(\\det\\begin{pmatrix}4-\\lambda&1\\\\2&3-\\lambda\\end{pmatrix}=(4-\\lambda)(3-\\lambda)-2\\) \\(=\\lambda^2-7\\lambda+10\\).",
   "\\(=(\\lambda-2)(\\lambda-5)\\). Fíjate: \\(7=\\operatorname{tr}A\\) y \\(10=\\det A\\); en 2 × 2 siempre \\(p(\\lambda)=\\lambda^2-\\operatorname{tr}A\\,\\lambda+\\det A\\)."],
  "λ² − 7λ + 10; λ = 2 y 5", "det de A − λI.", [["polcar"], ["trdet"]], chain=True))
EX.append(E("s11e4", 2, "Del polinomio a los vectores",
  "<p>Ejercicio guiado 2 del lab: \\(B=\\)" + tex(B) + ".</p>",
  [NUM([{"l": "λ₁ (menor) =", "a": 3}, {"l": "λ₂ (mayor) =", "a": 4}], "Parte 1: valores propios (tr B = 7, det B = 12)"),
   {"t": "esc", "p": "Parte 2: reduce \\(B-3I\\) hasta la forma escalonada reducida", "m": [[2, -2], [1, -1]], "na": 2, "goal": "red", "e": "Debe aparecer una fila de ceros."},
   NUM([{"l": "Si v = (x, 1) ∈ E₃, x =", "a": 1}, {"l": "Si v = (x, 1) ∈ E₄, x =", "a": 2}], "Parte 3: vectores propios")],
  ["Dos números con suma 7 y producto 12: 3 y 4. \\(p(\\lambda)=(5-\\lambda)(2-\\lambda)+2=\\lambda^2-7\\lambda+12\\).",
   "\\(B-3I=\\begin{pmatrix}2&-2\\\\1&-1\\end{pmatrix}\\sim\\begin{pmatrix}1&-1\\\\0&0\\end{pmatrix}\\): \\(x_1=x_2\\), \\(E_3=\\operatorname{Gen}\\{(1,1)\\}\\).",
   "\\(B-4I=\\begin{pmatrix}1&-2\\\\1&-2\\end{pmatrix}\\sim\\begin{pmatrix}1&-2\\\\0&0\\end{pmatrix}\\): \\(x_1=2x_2\\), \\(E_4=\\operatorname{Gen}\\{(2,1)\\}\\). Verificación: \\(B(2,1)=(8,4)=4(2,1)\\)."],
  "λ = 3: (1, 1); λ = 4: (2, 1)", "Suma 7, producto 12.", [["polcar"], ["eesp"], ["eesp"]], chain=True))
EX.append(E("s11e5", 1, "La rotación de 90°",
  "<p>\\(R=\\)" + tex(R) + " (rotación de 90°). ¿Qué pasa con sus valores propios?</p>",
  [O(["\\(p(\\lambda)=\\lambda^2+1\\): no tiene valores propios reales (son \\(\\pm i\\))", "Tiene \\(\\lambda=1\\) doble", "Tiene \\(\\lambda=1\\) y \\(\\lambda=-1\\)", "Tiene \\(\\lambda=0\\) porque la diagonal es nula", "Todo vector es propio"])],
  ["\\(p(\\lambda)=\\det\\begin{pmatrix}-\\lambda&-1\\\\1&-\\lambda\\end{pmatrix}=\\lambda^2+1\\), sin raíces reales.",
   "Geometría: girar 90° saca a todo vector no nulo de su recta. Los valores propios existen, pero en \\(\\mathbb C\\): \\(\\pm i\\)."],
  "Ninguno real (±i)", "¿Alguna recta queda fija al girar 90°?", [["patron"], ["polcar"]]))
EX.append(E("s11e6", 1, "Patrones sin calcular",
  "<p>Clasifica cada matriz según sus valores propios (patrones de la clase).</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["1 y −1", "Ninguno real", "Incluye 0", "Se leen en la diagonal"], "items": [
     {"x": tex(F), "c": 0, "e": "Reflexión en y = x: fija esa recta (λ = 1) e invierte la perpendicular (λ = −1)."},
     {"x": tex(R), "c": 1}, {"x": tex(A0), "c": 2, "e": "Las filas son proporcionales: det = 0."},
     {"x": tex(M([[3, 5], [0, -2]])), "c": 3}, {"x": tex(M([[1, 0], [0, -1]])), "c": 0},
     {"x": tex(M([[2, 4], [1, 2]])), "c": 2}]}],
  ["Reflexiones → ±1; rotaciones de 90° → complejos; matrices singulares → 0.",
   "Triangulares: \\(\\det(A-\\lambda I)=\\prod(a_{ii}-\\lambda)\\), así que los λ son la diagonal (¡solo si la matriz original ya es triangular!)."],
  "Clasificación correcta", "Piensa en la geometría.", [["patron"], ["patron"]]))
EX.append(E("s11e7", 1, "Traza y determinante",
  "<p>Una matriz 2 × 2 tiene \\(\\operatorname{tr}A=6\\) y \\(\\det A=8\\). Y una 3 × 3 tiene valores propios 1, 2 y \\(\\lambda_3\\) con \\(\\operatorname{tr}A=6\\).</p>",
  [O(["2 y 4", "1 y 8", "3 y 3", "−2 y −4", "6 y 8"], "Valores propios de la 2 × 2"),
   NUM([{"l": "λ₃ =", "a": 3}, {"l": "det A (3 × 3) =", "a": 6}], "La 3 × 3")],
  ["Suma 6 y producto 8: \\(p(\\lambda)=\\lambda^2-6\\lambda+8=(\\lambda-2)(\\lambda-4)\\).",
   "\\(1+2+\\lambda_3=6\\Rightarrow\\lambda_3=3\\); \\(\\det A=1\\cdot2\\cdot3=6\\)."],
  "2 y 4; λ₃ = 3, det = 6", "Suma = traza, producto = det.", [["trdet"], ["trdet"]], chain=True))
EX.append(E("s11e8", 2, "Potencias e inversa sin calcular",
  "<p>Ejemplo guiado 4: \\(A=\\)" + tex(A) + " tiene valores propios 2 y 5, y \\(u=(1,1)\\in E_5\\).</p>",
  [NUM([{"l": "A³u: 1.ª comp.", "a": 125}, {"l": "A³u: 2.ª comp.", "a": 125}], "Calcula sin hallar A³"),
   NUM([{"l": "menor valor propio de A⁻¹", "a": 0.2, "tol": 0.002}, {"l": "mayor valor propio de A⁻¹", "a": 0.5, "tol": 0.002}], "Valores propios de A⁻¹")],
  ["\\(A^3u=5^3u=(125,125)\\). (Con \\(A^3=\\begin{pmatrix}86&39\\\\78&47\\end{pmatrix}\\) da lo mismo: \\(86+39=125\\).)",
   "Si \\(Av=\\lambda v\\), \\(A^{-1}v=\\frac1\\lambda v\\): los valores propios de \\(A^{-1}\\) son \\(\\frac12\\) y \\(\\frac15\\), con los mismos vectores propios."],
  "(125, 125); 1/5 y 1/2", "\\(A^kv=\\lambda^kv\\).", [["potp"], ["potp"]], chain=True))
EX.append(E("s11e9", 2, "Un proceso que se repite",
  "<p>Ejercicio guiado 3 del lab: \\(x_{k+1}=Bx_k\\) con \\(B=\\)" + tex(B) + " (valores propios 3 y 4, vectores \\((1,1)\\) y \\((2,1)\\)).</p>",
  [NUM([{"l": "x₃ con x₀ = (2, 1): 1.ª comp.", "a": 128}, {"l": "2.ª comp.", "a": 64}], "Parte 1"),
   NUM([{"l": "y₃ con y₀ = (3, 2): 1.ª comp.", "a": 155}, {"l": "2.ª comp.", "a": 91}], "Parte 2: y₀ = (1, 1) + (2, 1)"),
   O(["Solo x₀: es vector propio y el sistema solo lo escala", "Solo y₀", "Ambos", "Ninguno", "Depende de k"], "Parte 3: ¿cuál conserva su dirección?")],
  ["\\(x_0=(2,1)\\in E_4\\): \\(x_3=4^3(2,1)=(128,64)\\).",
   "\\(y_3=3^3(1,1)+4^3(2,1)\\) \\(=(27,27)+(128,64)\\) \\(=(155,91)\\).",
   "\\(y_0\\) mezcla dos direcciones que crecen a ritmos distintos (\\(3^k\\) y \\(4^k\\)): su dirección cambia y se acerca a la de \\(\\lambda=4\\). Míralo en la herramienta «Aplicar A una y otra vez»."],
  "(128, 64); (155, 91); solo x₀", "Descompón en vectores propios.", [["potp"], ["potp"], ["potp"]], chain=True))
EX.append(E("s11e10", 3, "Matriz 3 × 3 (ejemplo guiado 5)",
  "<p>\\(A=\\)" + tex(A5) + " con \\(p(\\lambda)=-(\\lambda-2)^2(\\lambda-9)\\).</p>",
  [NUM([{"l": "tr A =", "a": 13}, {"l": "det A =", "a": 36}], "Parte 1: autocontrol del polinomio"),
   {"t": "fill", "p": "Parte 2: multiplicidades", "head": ["λ", "m_a", "rank(A − λI)", "m_g"], "rows": [["2", {"a": 2}, {"a": 1}, {"a": 2}], ["9", {"a": 1}, {"a": 2}, {"a": 1}]]},
   O(["\\(E_2=\\operatorname{Gen}\\{(1,2,0),(-3,0,1)\\}\\)", "\\(E_2=\\operatorname{Gen}\\{(1,1,1)\\}\\)", "\\(E_2=\\operatorname{Gen}\\{(1,2,0)\\}\\)", "\\(E_2=\\{0\\}\\)", "\\(E_2=\\mathbb R^3\\)"], "Parte 3: base de E₂")],
  ["\\(\\operatorname{tr}A=4+1+8=13=2+2+9\\) y \\(\\det A=36=2\\cdot2\\cdot9\\) ✓.",
   "\\(A-2I\\) tiene las tres filas iguales a \\((2,-1,6)\\): rango 1, \\(m_g(2)=3-1=2\\). \\(A-9I\\) tiene rango 2: \\(m_g(9)=1\\).",
   "\\(2x_1-x_2+6x_3=0\\) con \\(x_1,x_3\\) libres: \\(E_2=\\operatorname{Gen}\\{(1,2,0),(-3,0,1)\\}\\); \\(E_9=\\operatorname{Gen}\\{(1,1,1)\\}\\). En total, 3 vectores propios independientes."],
  "13 y 36; m_g(2) = 2, m_g(9) = 1", "mg = 3 − rank.", [["trdet"], ["multip"], ["eesp"]], chain=True))
EX.append(E("s11e11", 2, "Mismo polinomio, distinta multiplicidad",
  "<p>Ejercicio guiado 4: \\(C=\\)" + tex(C) + " y \\(D=\\)" + tex(D) + ". Ambas tienen \\(p(\\lambda)=(\\lambda-2)^2(\\lambda-3)\\).</p>",
  [{"t": "fill", "p": "Completa", "head": ["", "m_a(2)", "m_g(2)", "m_a(3)", "m_g(3)"], "rows": [["C", {"a": 2}, {"a": 1}, {"a": 1}, {"a": 1}], ["D", {"a": 2}, {"a": 2}, {"a": 1}, {"a": 1}]]},
   O(["\\(\\operatorname{Gen}\\{(1,0,0)\\}\\)", "\\(\\operatorname{Gen}\\{e_1,e_2\\}\\)", "\\(\\operatorname{Gen}\\{(0,1,0)\\}\\)", "\\(\\operatorname{Gen}\\{(0,0,1)\\}\\)", "\\(\\{0\\}\\)"], "E₂ de C")],
  ["\\(C-2I=\\begin{pmatrix}0&1&0\\\\0&0&0\\\\0&0&1\\end{pmatrix}\\): rango 2, así que \\(m_g(2)=1\\); \\(x_2=x_3=0\\), \\(E_2=\\operatorname{Gen}\\{(1,0,0)\\}\\).",
   "\\(D-2I\\) solo tiene la fila \\((0,0,1)\\): rango 1, \\(m_g(2)=2\\), \\(E_2=\\operatorname{Gen}\\{e_1,e_2\\}\\). El polinomio no decide cuántas direcciones hay: lo decide la reducción."],
  "C: 2, 1, 1, 1 · D: 2, 2, 1, 1", "Cuenta las variables libres.", [["multip"], ["multip"]], chain=True))
EX.append(E("s11e12", 2, "Relaciona el rango con la conclusión",
  "<p>Checkpoint de clase: para un valor \\(\\lambda\\) y \\(A\\in\\mathbb R^{3\\times3}\\), relaciona cada dato con lo que se concluye.</p>",
  [{"t": "cls", "p": "Clasifica", "cats": ["m_g(λ) = 2", "dim E_λ = 1", "λ no es valor propio"], "items": [
     {"x": "\\(\\operatorname{rank}(A-\\lambda I)=1\\)", "c": 0}, {"x": "\\(\\operatorname{rank}(A-\\lambda I)=2\\)", "c": 1},
     {"x": "\\(\\operatorname{rank}(A-\\lambda I)=3\\)", "c": 2, "e": "A − λI es invertible: solo la solución trivial."},
     {"x": "\\(m_a(\\lambda)=1\\)", "c": 1, "e": "\\(1\\le m_g\\le m_a=1\\)."}, {"x": "\\(\\det(A-\\lambda I)\\ne0\\)", "c": 2}]}],
  ["\\(m_g=3-\\operatorname{rank}(A-\\lambda I)\\): rango 1 → 2; rango 2 → 1; rango 3 → 0 (no es valor propio).",
   "Si \\(m_a=1\\), la desigualdad \\(1\\le m_g\\le m_a\\) obliga a \\(m_g=1\\)."],
  "Clasificación correcta", "mg = n − rank.", [["multip"], ["multip"]]))
EX.append(E("s11e13", 2, "Caza de errores: reducir antes",
  "<p>Un estudiante reduce \\(B=\\)" + tex(B) + " por filas, obtiene \\(\\operatorname{rref}(B)=I\\) y concluye que los valores propios son 1 y 1. ¿Qué está mal?</p>",
  [O(["Las operaciones por fila cambian la transformación (\\(\\operatorname{tr}I=2\\ne7\\)): no conservan los valores propios",
      "Nada: \\(I\\) es triangular y sus valores propios son la diagonal",
      "Debió reducir hasta la escalonada, no la reducida",
      "Los valores propios son 1 y 1, pero los vectores cambian",
      "Debió reducir \\(B^T\\)"])],
  ["Las operaciones por fila conservan el rango y \\(\\operatorname{Nul}B\\), pero no \\(Bv=\\lambda v\\). Los valores correctos son 3 y 4.",
   "Se reduce \\(B-\\lambda I\\) (después de hallar \\(\\lambda\\)) para los vectores; leer la diagonal solo vale si la matriz original ya es triangular."],
  "Reducir cambia los valores propios", "Compara las trazas.", [["patron"], ["eesp"]]))
EX.append(E("s11e14", 1, "Caza de errores: λ = 0",
  "<p>Un estudiante afirma: «λ = 0 no puede ser valor propio, porque el vector propio no puede ser cero». Con \\(A_0=\\)" + tex(A0) + " y \\(w=(-2,1)\\):</p>",
  [NUM([{"l": "A₀w: 1.ª comp.", "a": 0}, {"l": "2.ª comp.", "a": 0}], "Calcula"),
   O(["w es vector propio con λ = 0: el estudiante confunde λ = 0 (permitido) con v = 0 (prohibido)", "w no es vector propio porque A₀w = 0", "A₀ no tiene valores propios", "λ = 0 solo vale si A₀ es la matriz nula", "w es vector propio con λ = 5"], "Conclusión")],
  ["\\(A_0w=(-2+2,\\ -4+4)=(0,0)=0\\cdot w\\) con \\(w\\ne0\\).",
   "\\(p(\\lambda)=\\lambda(\\lambda-5)\\), \\(\\det A_0=0\\) y \\(E_0=\\operatorname{Nul}A_0=\\operatorname{Gen}\\{(-2,1)\\}\\): el espacio propio de 0 es el núcleo."],
  "λ = 0 sí; v = 0 no", "Lo prohibido es el vector cero.", [["vprop"], ["eesp"]], chain=True))
EX.append(E("s11e15", 1, "MATLAB: ¿por qué no sale (2, 1)?",
  "<p>Con <code>[V, D] = eig(B)</code> para \\(B=\\)" + tex(B) + ", la columna de V asociada a 4 es aproximadamente <code>(0.8944, 0.4472)</code>. ¿Por qué es correcta aunque no sea \\((2,1)\\)?</p>",
  [O(["eig normaliza: es \\((2,1)/\\sqrt5\\), un múltiplo de \\((2,1)\\), y la recta es la misma", "MATLAB redondea mal", "Es otro valor propio", "Porque B no es simétrica", "Porque D está desordenada"])],
  ["Un vector propio no es único: cualquier múltiplo no nulo sirve. MATLAB elige el de norma 1: \\(\\frac{1}{\\sqrt5}(2,1)\\approx(0{,}894;\\ 0{,}447)\\).",
   "Para verlo como en clase: <code>V(:,k)/V(2,k)</code>. Y <code>norm(B*V - V*D)</code> ≈ 0 confirma \\(BV=VD\\). MATLAB verifica; el razonamiento decide."],
  "Es múltiplo de (2, 1)", "Divide entre la 2.ª componente.", [["eesp"], ["eesp"]]))
TOOLS = [
 {"w": "pot", "t": "Aplicar A una y otra vez", "p": "Toca ▶: si x₀ es vector propio, Aᵏx₀ nunca sale de su recta. Si mezcla dos direcciones, se va girando hacia la recta del λ más grande (punteadas: rectas propias).",
  "o": {"a": [[5, -2], [1, 2]], "x0": [3, 2], "presets": [["B, y₀ = (3, 2)", {"a": [[5, -2], [1, 2]], "x0": [3, 2]}], ["B, x₀ = (2, 1)", {"a": [[5, -2], [1, 2]], "x0": [2, 1]}],
         ["Placa [2 1; 1 2]", {"a": [[2, 1], [1, 2]], "x0": [1, 0]}], ["Rotación 90°", {"a": [[0, -1], [1, 0]], "x0": [1, 0]}], ["[2 1; 0 2]", {"a": [[2, 1], [0, 2]], "x0": [0, 1]}]]}},
 {"w": "rref", "t": "Escalonador: A − 2I del ejemplo 5", "p": "Rango 1: dos variables libres, así que \\(m_g(2)=2\\).", "o": {"m": [[2, -1, 6], [2, -1, 6], [2, -1, 6]], "mode": "mat"}},
 {"w": "tl", "t": "Visualizador: la placa deformada", "p": "Con A = [[2, 1], [1, 2]], el vector (1, 1) solo se estira (λ = 3) y (1, −1) queda igual (λ = 1).", "o": {"a": [[2, 1], [1, 2]], "v": [1, 1]}}]
CONC = {
 "vprop": {"n": "Valor y vector propio", "f": "\\(Av=\\lambda v\\), \\(v\\ne0\\)", "x": "v marca una dirección que A solo escala; λ = 0 está permitido, v = 0 no.", "home": "s11"},
 "polcar": {"n": "Polinomio característico", "f": "\\(p(\\lambda)=\\det(A-\\lambda I)\\)", "x": "Sus raíces son los valores propios. En 2 × 2: \\(\\lambda^2-\\operatorname{tr}A\\,\\lambda+\\det A\\).", "home": "s11"},
 "eesp": {"n": "Espacio propio", "f": "\\(E_\\lambda=\\operatorname{Nul}(A-\\lambda I)\\)", "x": "Se reduce A − λI (no A); debe salir una fila nula.", "home": "s11"},
 "trdet": {"n": "Traza y determinante", "f": "\\(\\operatorname{tr}A=\\sum\\lambda_i\\), \\(\\det A=\\prod\\lambda_i\\)", "x": "Sirven para anticipar y verificar. A invertible ⇔ 0 no es valor propio.", "home": "s11"},
 "potp": {"n": "Potencias e inversa", "f": "\\(A^kv=\\lambda^kv\\), \\(A^{-1}v=\\frac1\\lambda v\\)", "x": "Mismos vectores propios. Base de los sistemas dinámicos (S12).", "home": "s11"},
 "multip": {"n": "Multiplicidades", "f": "\\(m_g=n-\\operatorname{rank}(A-\\lambda I)\\), \\(1\\le m_g\\le m_a\\)", "x": "m_a se lee en el polinomio; m_g exige un rango.", "home": "s11"},
 "patron": {"n": "Patrones", "f": "triangular → diagonal · reflexión → ±1 · rotación → complejos", "x": "Nunca leer los λ de rref(A).", "home": "s11"},
}
TOPIC = {"id": "s11", "name": "Sem. 11 · Valores y vectores propios: polinomio, propiedades y multiplicidades", "teo": TEO, "form": FORM, "lesson": LESSON, "ex": EX, "tools": TOOLS}
CARDS = ('<div><b>Valores propios</b><br>\\(Av=\\lambda v\\), \\(v\\ne0\\) · \\(p(\\lambda)=\\det(A-\\lambda I)\\)</div>'
         '<div><b>Espacio propio</b><br>\\(E_\\lambda=\\operatorname{Nul}(A-\\lambda I)\\) · reduce A − λI, no A</div>'
         '<div><b>Verificar</b><br>\\(\\operatorname{tr}A=\\sum\\lambda\\), \\(\\det A=\\prod\\lambda\\), \\(A^kv=\\lambda^kv\\)</div>'
         '<div><b>Multiplicidades</b><br>\\(m_g=n-\\operatorname{rank}(A-\\lambda I)\\), \\(1\\le m_g\\le m_a\\)</div>')

def put(name, intro, slots):
    d = json.load(open(P(name), encoding="utf-8"))
    d["topics"] = [t for t in d["topics"] if t["id"] != "s11"]
    k = next((i for i, t in enumerate(d["topics"]) if t["id"] == "s10"), len(d["topics"]) - 1) + 1
    d["topics"].insert(k, TOPIC)
    d["concepts"].update(CONC)
    if "Valores propios</b>" not in d["form"]:
        j = d["form"].rindex("</div>")
        d["form"] = d["form"][:j] + CARDS + d["form"][j:]
    d["intro"] = intro
    d["sim"]["slots"] = slots
    assert abs(sum(s["pts"] for s in slots) - 20) < 1e-9
    ids = [e["id"] for t in d["topics"] for e in t["ex"]] + [e["id"] for e in d.get("simEx", [])]
    assert len(ids) == len(set(ids))
    for s in slots:
        for i in s["pool"]: assert i in ids, (name, i)
    for t in d["topics"]:
        for e in t["ex"]:
            for l in e["tags"]:
                for c in l: assert c in d["concepts"], (e["id"], c)
    return d

ea3 = json.load(open(P("al-ea3"), encoding="utf-8"))
old = ea3["sim"]["slots"]
SL3 = [dict(old[0], pts=3), dict(old[1], pts=3), dict(old[2], pts=5), dict(old[3], pts=4),
       {"pts": 5, "name": "Sem. 11: valores y vectores propios", "pool": ["s11e3", "s11e4", "s11e7", "s11e8", "s11e10", "s11e11"]}]
INTRO3 = ("Resuelve en papel y toca «Verificar respuesta». La solución se desbloquea después de tu primer intento; la pista está siempre disponible. "
          "<b>La EA3 fue en el laboratorio de la semana 11 (30 min, individual y sin MATLAB)</b>. Están la semana 9 (linealidad y matriz estándar), la semana 10 "
          "(transformaciones comunes, núcleo, imagen y rango–nulidad) y la <b>semana 11</b> (valores y vectores propios: polinomio característico, traza, determinante, potencias y multiplicidades), "
          "con una herramienta para aplicar A una y otra vez. Como la evaluación fue al final de la sesión de valores propios, el simulacro incluye una pregunta de la semana 11.")
ea3n = put("al-ea3", INTRO3, SL3)
ea3n["free"] = True

ef = json.load(open(P("al-ef"), encoding="utf-8"))
o = ef["sim"]["slots"]
SLF = [dict(o[0], pts=2), dict(o[1], pts=2), dict(o[2], pts=2), dict(o[3], pts=2), dict(o[4], pts=2), dict(o[5], pts=3), dict(o[6], pts=3),
       {"pts": 4, "name": "Sem. 11: valores y vectores propios", "pool": ["s11e4", "s11e8", "s11e9", "s11e10", "s11e11", "s11e13"]}]
INTROF = ("Repaso acumulado del curso, con los temas ordenados por semana. Aquí todos los temas están abiertos desde el inicio. <b>El examen final vale 30 %</b> (100 min, semana 16). "
          "Por ahora están las semanas 1 a 7, 9, 10 y 11 (valores y vectores propios); las semanas 12 a 15 se agregan a medida que lleguen sus guías y tendrán más peso en el simulacro.")
efn = put("al-ef", INTROF, SLF)

for name, d in (("al-ea3", ea3n), ("al-ef", efn)):
    with open(P(name), "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False); f.write("\n")
print("ok", len(EX))
