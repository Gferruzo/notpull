"""Programación I · Examen final: repaso sem. 1–8, NumPy, imágenes y diccionarios (sem. 10–11)."""
from p1_lib import *
import numpy as np, base64, io as _io
from PIL import Image

CONCEPTS = {
 'while': {'n': 'while', 'f': c('while condicion:'), 'x': 'Repite mientras la condición sea verdadera; algo dentro debe cambiarla o no termina.', 'home': 'r18'},
 'forr': {'n': 'for con range', 'f': c('range(a, b)') + ' = a … b − 1', 'x': 'Para una cantidad conocida de vueltas; range(a, b + 1) si b debe entrar.', 'home': 'r18'},
 'dig': {'n': 'Separar dígitos', 'f': c('N % 10') + ' último · ' + c('N // 10') + ' quita el último', 'x': 'En un while N > 0 se sacan los dígitos de derecha a izquierda.', 'home': 'r18'},
 'bis': {'n': 'Año bisiesto', 'f': c('(a % 4 == 0 and a % 100 != 0) or a % 400 == 0'), 'x': 'Múltiplo de 4, salvo los de 100 que no son de 400.', 'home': 'r18'},
 'np': {'n': 'Array de NumPy', 'f': c('import numpy as np') + ' · ' + c('np.array(lista)'), 'x': 'Como una lista, pero con operaciones matemáticas: + suma elemento a elemento.', 'home': 'n10'},
 'shape': {'n': 'shape', 'f': c('arr.shape') + ' → (filas, columnas)', 'x': 'filas, columnas = arr.shape. En una imagen a color: (alto, ancho, 3).', 'home': 'n10'},
 'np2d': {'n': 'Índices en NumPy', 'f': c('arr[f, c]') + ' (también ' + c('arr[f][c]') + ')', 'x': 'Con una coma se indican fila y columna.', 'home': 'n10'},
 'npsl': {'n': 'Cortes 2D', 'f': c('arr[filas, columnas]') + ' · ' + c('arr[:, 0]') + ' · ' + c('arr[1:, 1:3]'), 'x': 'Cada parte del corte es como en listas: inicio:fin:paso; «:» sola = todas.', 'home': 'n10'},
 'zeros': {'n': 'np.zeros', 'f': c('np.zeros((f, c))') + ' · ' + c('dtype=np.uint8'), 'x': 'Crea una matriz de ceros (float por defecto; uint8 para imágenes).', 'home': 'n10'},
 'gris': {'n': 'Escala de grises', 'f': '0 = negro · 255 = blanco', 'x': 'Un byte por píxel: 256 intensidades.', 'home': 'i10'},
 'rgb': {'n': 'Canales RGB', 'f': c('[R, G, B]') + ' · shape (alto, ancho, 3)', 'x': '[255, 0, 0] rojo · [0, 255, 0] verde · [0, 0, 255] azul · [255, 255, 0] amarillo.', 'home': 'i10'},
 'imgsl': {'n': 'Recortar una imagen', 'f': c('img[f1:f2, c1:c2]'), 'x': 'Las filas son el alto (de arriba abajo) y las columnas el ancho.', 'home': 'i10'},
 'u8': {'n': 'Desborde de uint8', 'f': c('np.uint8(250) + 50') + ' → 44', 'x': 'En uint8 la suma da la vuelta (módulo 256): convierte a int antes de comparar.', 'home': 'i10'},
 'dic': {'n': 'Diccionario', 'f': c('d = {clave: valor}'), 'x': 'Pares clave → valor. Las claves son únicas e inmutables (str, int, tupla).', 'home': 'd11'},
 'dacc': {'n': 'Acceder', 'f': c('d[k]') + ' (KeyError si no está) · ' + c('d.get(k, defecto)'), 'x': 'Pregunta con k in d o usa get para no caerte.', 'home': 'd11'},
 'dset': {'n': 'Agregar o cambiar', 'f': c('d[k] = v'), 'x': 'Si la clave no existe, se inserta; si existe, se reemplaza su valor.', 'home': 'd11'},
 'ddel': {'n': 'Borrar', 'f': c('del d[k]') + ' · ' + c('d.pop(k)') + ' · ' + c('d.clear()'), 'x': 'pop además devuelve el valor quitado; clear vacía todo.', 'home': 'd11'},
 'drec': {'n': 'Recorrer', 'f': c('for k in d') + ' · ' + c('d.values()') + ' · ' + c('for k, v in d.items()'), 'x': 'Recorrer el diccionario da las claves.', 'home': 'd11'},
 'dcont': {'n': 'Contar con un diccionario', 'f': c('if k in d: d[k] += 1') + ' · ' + c('else: d[k] = 1'), 'x': 'Patrón de frecuencias: la clave es lo que cuentas.', 'home': 'd11'},
 'dlist': {'n': 'Valores que son listas', 'f': c('d[k].append(x)'), 'x': 'Primero crear la lista: d[k] = [x] si la clave es nueva.', 'home': 'd11'},
 'anid': {'n': 'Diccionario anidado', 'f': c('d[1]["nombre"]'), 'x': 'El primer [] da el diccionario interno; el segundo, su campo.', 'home': 'a11'},
 'anidadd': {'n': 'Agregar a un anidado', 'f': c('d[3] = {}') + ' y luego ' + c('d[3]["edad"] = 24'), 'x': 'El diccionario interno tiene que existir antes de llenarlo.', 'home': 'a11'},
}

def img_uri(arr, size=64):
    im = Image.fromarray(np.asarray(arr, dtype=np.uint8)).resize((size, size), Image.NEAREST)
    b = _io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def imgopt(arr, txt):
    return '<img class="p1oimg" src="' + img_uri(arr) + '" alt="Imagen ' + txt + '">'

T_REP = """
<p>Repaso de lo que se usa en todo el curso.</p>
<ul><li><b>for con range:</b> <code>for i in range(a, b, paso):</code> da a, a + paso, … sin llegar a b. Para incluir b: <code>range(a, b + 1)</code>.</li>
<li><b>while:</b> repite mientras la condición sea verdadera. Sirve cuando no sabes cuántas vueltas habrá (cortar rollos hasta que quede poco, leer datos hasta «fin»). Algo dentro debe acercarse al final; si no, el programa <b>nunca termina</b>.</li>
<li><b>Condiciones compuestas:</b> <code>and</code>, <code>or</code>, <code>not</code> y paréntesis. Bisiesto: <code>(a % 4 == 0 and a % 100 != 0) or a % 400 == 0</code>.</li>
<li><b>Dígitos de un número:</b> <code>N % 10</code> da el último y <code>N // 10</code> lo quita (dentro de <code>while N &gt; 0</code>). Otra forma: recorrer <code>str(N)</code> y convertir cada carácter con <code>int</code>.</li>
<li><b>Funciones:</b> reciben parámetros y <code>return</code> entrega el resultado; para devolver dos valores, <code>return a, b</code> (una tupla). <code>round(x, 1)</code> redondea.</li>
<li><b>Construir cadenas iterando reglas</b> (sistemas-L): en cada iteración se arma una cadena nueva reemplazando cada símbolo.</li></ul>
"""
L_REP = """<h3>Idea central</h3><p>for cuando sabes cuántas vueltas; while cuando depende de una condición. En los dos, piensa qué cambia en cada vuelta.</p>
<h3>Conceptos clave</h3><ul><li><code>range</code> no incluye el final.</li><li>Todo while necesita avanzar.</li><li>Paréntesis en condiciones con and y or.</li></ul>
<div class="ej"><b>Ejemplo:</b> 142425 → dígitos pares 4 + 2 + 4 + 2 = 12, impares 1 + 5 = 6.</div>
<div class="err"><b>Error común:</b> olvidar <code>N = N // 10</code> dentro del while: el bucle no termina.</div>"""

def repaso():
    E = []
    E.append(opc('r18_1', 1, 'for o while', '<p>Un taller corta rollos de una pieza de tela mientras queden al menos 5 m después del corte. ¿Qué bucle conviene?</p>',
        ['while, porque no se sabe de antemano cuántos rollos salen', 'for con range(5), porque son 5 metros', 'for, porque while no puede restar', 'Ninguno: se resuelve solo con un if', 'while True sin condición de salida'],
        ['La cantidad de vueltas depende de la tela que queda: es un caso típico de <code>while</code>.'], '', [['while']]))
    code = 'total = 30.5\nrollo = 7.2\ncont = 0\nwhile total - rollo >= 5.0:\n    total = total - rollo\n    cont = cont + 1\nprint(cont, round(total, 1))'
    E.append(imprime('r18_2', 2, 'Cortando rollos', code, ['4 1.7', '3 5.0', '5 -5.5', '3 1.7'],
        ['30,5 → 23,3 → 16,1 → 8,9 (tres cortes). Un cuarto corte dejaría 1,7 m, menos de 5: el while se detiene.'], 'Haz la tabla de total en cada vuelta.', [['while']]))
    E.append(hueco('r18_3', 1, 'Año bisiesto', '<p>Completa la condición: un año es bisiesto si es múltiplo de 4, pero si es múltiplo de 100 también debe serlo de 400.</p>',
        'def es_bisiesto(a):\n    if (a % 4 == 0 and a % 100 != 0) or ⟦0⟧:\n        return True\n    return False',
        [(['a % 400 == 0', 'a%400==0', '(a % 400 == 0)'], 'El caso que «salva» a los múltiplos de 100.', 'Falta el caso de los múltiplos de 400: a % 400 == 0.')],
        ['Los múltiplos de 4 que no son de 100 son bisiestos; los de 400 también (2000 sí, 1900 no).'], '', [['bis']],
        tests=mk_tests('def es_bisiesto(a):\n    if (a % 4 == 0 and a % 100 != 0) or a % 400 == 0:\n        return True\n    return False',
                       ['print(es_bisiesto(2000), es_bisiesto(1900), es_bisiesto(2024), es_bisiesto(2026))']),
        demo='print([a for a in range(1890, 1920) if es_bisiesto(a)])'))
    fixed = 'def pares_impares(N):\n    pares = 0\n    impares = 0\n    while N > 0:\n        d = N % 10\n        if d % 2 == 0:\n            pares = pares + d\n        else:\n            impares = impares + d\n        N = N // 10\n    return pares, impares\n\nprint(pares_impares(142425))'
    E.append(bug('r18_4', 2, 'Un while que no termina', '<p>La función suma los dígitos pares y los impares de N (Tarea de Laboratorio 6). Al ejecutarla, la app la detiene porque nunca termina.</p>',
        'def pares_impares(N):\n    pares = 0\n    impares = 0\n    while N > 0:\n        d = N % 10\n        if d % 2 == 0:\n            pares = pares + d\n        else:\n            impares = impares + d\n    return pares, impares\n\nprint(pares_impares(142425))',
        [4], ['N nunca cambia dentro del while: falta N = N // 10 y la condición siempre es verdadera', 'd % 2 debería ser d // 2', 'pares e impares deberían empezar en 1', 'Debería ser while N >= 0', 'return no puede devolver dos valores'],
        ['Dentro del while nada cambia <code>N</code>: <code>N &gt; 0</code> es verdadera para siempre.', 'Al final de cada vuelta hay que quitar el último dígito: <code>N = N // 10</code>.'],
        '¿Qué variable debe cambiar para que el while termine?', [['while'], ['dig']], outtxt='⏱ Tu código tardó demasiado y se detuvo. (El bucle nunca termina.)', fixed=fixed))
    E.append(codex('r18_5', 1, 'Años bisiestos en un rango',
        '<p>Implementa <code>pregunta_1(l, r)</code> que cuente los años bisiestos entre <code>l</code> y <code>r</code>, ambos incluidos (Tarea de Laboratorio 6).</p>' + pre('pregunta_1(1900, 2000)  →  25\npregunta_1(2000, 2026)  →  7'),
        'def pregunta_1(l, r):\n    # tu código aquí\n    return 0\n',
        'def pregunta_1(l, r):\n    cont = 0\n    for a in range(l, r + 1):\n        if (a % 4 == 0 and a % 100 != 0) or a % 400 == 0:\n            cont = cont + 1\n    return cont\n',
        ['print(pregunta_1(1900, 2000))', 'print(pregunta_1(2000, 2026))', 'print(pregunta_1(1, 2026))', 'print(pregunta_1(2001, 2003))'],
        ['<code>range(l, r + 1)</code> para incluir <code>r</code>.', 'Se cuenta cada año que cumple la condición de bisiesto.'], '', [['forr'], ['bis']], pc='rep'))
    E.append(codex('r18_6', 2, 'Dígitos pares e impares',
        '<p>Implementa <code>pregunta_4(N)</code> que retorne la tupla <code>(suma de dígitos pares, suma de dígitos impares)</code> (Tarea de Laboratorio 6).</p>' + pre('pregunta_4(142425)  →  (12, 6)\npregunta_4(2468)    →  (20, 0)'),
        'def pregunta_4(N):\n    # tu código aquí\n    return 0, 0\n',
        'def pregunta_4(N):\n    pares = 0\n    impares = 0\n    while N > 0:\n        d = N % 10\n        if d % 2 == 0:\n            pares = pares + d\n        else:\n            impares = impares + d\n        N = N // 10\n    return pares, impares\n',
        ['print(pregunta_4(142425))', 'print(pregunta_4(2468))', 'print(pregunta_4(471852))', 'print(pregunta_4(13286827891))'],
        ['<code>N % 10</code> da el último dígito y <code>N // 10</code> lo quita.', 'Se suma a pares o a impares según <code>d % 2</code>; <code>return pares, impares</code> devuelve la tupla.'], '', [['dig'], ['dig']], pc='rep'))
    E.append(codex('r18_7', 2, 'Sistema-L',
        '<p>Partiendo de <code>"A"</code>, en cada iteración cada A se convierte en AB y cada B en A. Implementa <code>pregunta_3(n)</code> que retorne la cadena tras <code>n</code> iteraciones (Tarea de Laboratorio 7).</p>' + pre('n = 0: A · n = 1: AB · n = 2: ABA · n = 3: ABAAB'),
        'def pregunta_3(n):\n    # tu código aquí\n    return "A"\n',
        'def pregunta_3(n):\n    s = "A"\n    for i in range(n):\n        nueva = ""\n        for ch in s:\n            if ch == "A":\n                nueva = nueva + "AB"\n            else:\n                nueva = nueva + "A"\n        s = nueva\n    return s\n',
        ['print(pregunta_3(2))', 'print(pregunta_3(4))', 'print(pregunta_3(7))', 'print(pregunta_3(0))'],
        ['En cada iteración se arma una cadena <b>nueva</b> leyendo la anterior símbolo por símbolo.', 'Al final de la vuelta, la nueva reemplaza a la anterior.'], 'Construye en otra variable.', [['forr'], ['acum']], pc='rep'))
    E.append(codex('r18_8', 2, 'Rollos de tela',
        '<p>Implementa <code>pregunta_2(longitud_total, longitud_rollo)</code> con un <code>while</code>: un rollo solo se corta si después quedan al menos 5.0 m. Retorna la cantidad de rollos (Tarea de Laboratorio 6).</p>' + pre('pregunta_2(50.0, 10.0)  →  4\npregunta_2(30.5, 7.2)   →  3'),
        'def pregunta_2(longitud_total, longitud_rollo):\n    # tu código aquí\n    return 0\n',
        'def pregunta_2(longitud_total, longitud_rollo):\n    rollos = 0\n    while longitud_total - longitud_rollo >= 5.0:\n        longitud_total = longitud_total - longitud_rollo\n        rollos = rollos + 1\n    return rollos\n',
        ['print(pregunta_2(50.0, 10.0))', 'print(pregunta_2(30.5, 7.2))', 'print(pregunta_2(100.6, 15.2))', 'print(pregunta_2(15.3, 4.1))'],
        ['La condición del while es la regla de seguridad: lo que queda después del corte debe ser ≥ 5.'], '', [['while']], pc='rep'))
    N = 4718; rows = []; pa = im = 0; n = N
    while n > 0:
        d = n % 10
        if d % 2 == 0: pa += d
        else: im += d
        n //= 10; rows.append([str(d), {'a': str(pa)}, {'a': str(im)}, {'a': str(n)}])
    E.append(ex('r18_9', 2, 'Rastreo de un while', '<p>Completa los valores al terminar cada vuelta para <code>N = 4718</code>.</p>',
        [{'t': 'traza', 'p': 'Rastrea el while', 'code': 'pares = 0\nimpares = 0\nwhile N > 0:\n    d = N % 10\n    if d % 2 == 0:\n        pares = pares + d\n    else:\n        impares = impares + d\n    N = N // 10', 'head': ['d', 'pares', 'impares', 'N'], 'rows': rows}],
        ['Los dígitos salen de derecha a izquierda: 8, 1, 7, 4.', 'Pares: 8 + 4 = 12; impares: 1 + 7 = 8. N termina en 0.'], 'pares = 12, impares = 8', '', [['dig'], ['dig']]))
    return {'id': 'r18', 'name': 'Sem. 1–8 · Repaso: bucles, funciones y cadenas', 'teo': T_REP, 'form': [c('range(a, b + 1)') + ' incluye b', c('while cond:') + ' algo debe cambiar', c('N % 10') + ' · ' + c('N // 10'), c('return a, b') + ' → tupla'], 'lesson': L_REP, 'ex': E}

NP0 = 'import numpy as np\nnotas = [[18, 17, 20, 16], [5, 10, 20, 19]]\nnotas_np = np.array(notas)'
T_NP = """
<p><strong>NumPy</strong> es la librería de cálculo numérico de Python (la usan pandas, matplotlib, scikit-learn…). Se importa con un alias: <code>import numpy as np</code>. Un <strong>array</strong> se parece a una lista, pero pensado para matemática:</p>
<ul><li><code>np.array([5, 10, 20])</code> crea un array 1D; <code>np.array([[18, 17], [5, 10]])</code>, uno 2D (una matriz).</li>
<li><code>arr.shape</code> da las dimensiones como tupla: <code>(2, 4)</code> = 2 filas y 4 columnas. Por eso <code>filas, columnas = arr.shape</code>.</li>
<li>Se accede con <code>arr[f, c]</code> (también vale <code>arr[f][c]</code>).</li>
<li><code>np.zeros((3, 4))</code> crea una matriz de ceros (decimales: se imprimen como <code>0.</code>); con <code>dtype=np.uint8</code> son enteros de 0 a 255.</li>
<li><code>arr1 + arr2</code> <b>suma elemento a elemento</b> (con listas, <code>+</code> concatena). Lo mismo con <code>*</code>, <code>-</code>…</li></ul>
<p><strong>Cortes en 2D:</strong> <code>arr[filas, columnas]</code>, cada parte con la sintaxis <code>inicio:fin:paso</code> de siempre y <code>:</code> sola para «todas». Ejemplos con <code>notas_np</code> de 2 × 4: <code>notas_np[1:2]</code> → la fila 1 (como matriz); <code>notas_np[:, :1]</code> → la columna 0; <code>notas_np[:, 1:3]</code> → columnas 1 y 2; <code>notas_np[1:, 1:3]</code> → fila 1, columnas 1 y 2; <code>notas_np[:, columnas-1:]</code> → la última columna.</p>
<p>Un array se imprime sin comas: <code>[[18 17]<br>&nbsp;[ 5 10]]</code>. Con <code>arr.tolist()</code> vuelve a ser una lista de Python.</p>
"""
L_NP = """<h3>Idea central</h3><p>Un corte 2D es elegir un rectángulo: primero las filas, después de la coma las columnas.</p>
<h3>Conceptos clave</h3><ul><li><code>arr.shape</code> = (filas, columnas).</li><li><code>:</code> sola = todas.</li><li>+ entre arrays suma; entre listas une.</li></ul>
<div class="ej"><b>Ejemplo:</b> <code>notas_np[:, 1:3]</code> → <code>[[17 20] [10 20]]</code>.</div>
<div class="err"><b>Error común:</b> escribir <code>notas_np[1:3]</code> creyendo que son columnas: sin coma, el corte es de filas.</div>"""

def numpy_t():
    E = []
    E.append(opc('n10_1', 1, 'Listas vs arrays', pre('import numpy as np\na = [1, 2]\nb = [3, 4]\nprint(a + b)\nprint(np.array(a) + np.array(b))') + '<p>¿Qué imprime?</p>',
        ['[1, 2, 3, 4] y luego [4 6]', '[4, 6] y luego [4 6]', '[1, 2, 3, 4] y luego [1 2 3 4]', '[4, 6] y luego [1 2 3 4]', 'Da error: no se pueden sumar listas'],
        ['Con listas, <code>+</code> <b>concatena</b>: [1, 2, 3, 4].', 'Con arrays, <code>+</code> suma elemento a elemento: [4 6] (sin comas).'], '', [['np'], ['np']], p='Salida',
        play='import numpy as np\na = [1, 2]\nb = [3, 4]\nprint(a + b)\nprint(np.array(a) + np.array(b))'))
    E.append(imprime('n10_2', 1, 'shape e índices', NP0 + '\nprint(notas_np.shape)\nprint(notas_np[1, 2])', ['(4, 2)\n20', '(2, 4)\n10', '8\n20', '(2, 4)\n17'],
        ['2 filas y 4 columnas → <code>(2, 4)</code>.', '<code>notas_np[1, 2]</code> es fila 1, columna 2 → 20.'], '', [['shape'], ['np2d']]))
    NM = [[18, 17, 20, 16], [5, 10, 20, 19]]
    def tapnp(id, lvl, title, expr, cells, steps, tags, m=NM, src=NP0):
        arr = np.arange(len(m) * len(m[0])).reshape(len(m), len(m[0]))
        got = eval(expr.replace('notas_np', 'arr').replace('mat_np', 'arr'))
        exp = sorted(int(x) for x in np.atleast_1d(got).ravel())
        assert exp == sorted(f * len(m[0]) + cc for f, cc in cells), (id, exp, cells)
        return ex(id, lvl, title, '<p>Toca las celdas que toma <code>' + esc(expr) + '</code>.</p>',
                  [{'t': 'mtx', 'p': 'Toca las celdas', 'm': m, 'a': cells, 'name': 'notas_np' if m is NM else 'mat_np'}],
                  steps, str(len(cells)) + ' celdas', '', tags, play=src + '\nprint(' + expr + ')')
    E.append(tapnp('n10_3', 1, 'Corte de una columna', 'notas_np[:, :1]', [[0, 0], [1, 0]], ['<code>:</code> = todas las filas; <code>:1</code> = columnas desde 0 hasta antes de 1 → solo la columna 0.'], [['npsl']]))
    E.append(tapnp('n10_4', 2, 'Rectángulo', 'notas_np[1:, 1:3]', [[1, 1], [1, 2]], ['Filas desde la 1 (solo la 1); columnas 1 y 2 (el 3 no entra).'], [['npsl']]))
    M = [[18, 17, 20, 16, 17], [5, 10, 20, 19, 17], [12, 14, 15, 19, 9], [18, 20, 12, 11, 10]]
    E.append(tapnp('n10_5', 2, 'Con paso', 'mat_np[::2, 1::2]', [[0, 1], [0, 3], [2, 1], [2, 3]], ['Filas 0 y 2 (de 2 en 2); columnas 1 y 3 (impares).'], [['npsl']], m=M,
                   src='import numpy as np\nmat_np = np.array(' + repr(M) + ')'))
    E.append(hueco('n10_6', 2, 'La última columna', '<p>Completa para imprimir la última columna, sea cual sea el tamaño del array.</p>',
        NP0 + '\nfilas, columnas = notas_np.⟦0⟧\nprint(notas_np[:, ⟦1⟧])',
        [(['shape'], '¿Qué atributo da (filas, columnas)?', 'shape da la tupla (filas, columnas).'),
         (['columnas-1:', 'columnas - 1:', '-1:', 'columnas-1:columnas'], 'Desde la última columna hasta el final.', 'La última columna es columnas − 1; con «:» después queda como columna (2D).')],
        ['<code>shape</code> se desempaqueta en dos variables.', '<code>notas_np[:, columnas-1:]</code>: todas las filas, desde la última columna.'], '', [['shape'], ['npsl']],
        tests=[{'n': 'Imprime la última columna', 'out': out(NP0 + '\nfilas, columnas = notas_np.shape\nprint(notas_np[:, columnas-1:])')}]))
    E.append(imprime('n10_7', 1, 'np.zeros', 'import numpy as np\nm = np.zeros((2, 3))\nm[1, 2] = 7\nprint(m)', ['[[0 0 0]\n [0 0 7]]', '[[0. 0. 0.]\n [0. 7. 0.]]', '[[0, 0, 0], [0, 0, 7]]', '[[0. 0.]\n [0. 0.]\n [0. 7.]]'],
        ['<code>np.zeros((2, 3))</code>: 2 filas, 3 columnas de decimales (por eso «0.»).', 'Se cambia la fila 1, columna 2.'], '', [['zeros'], ['np2d']]))
    E.append(codex('n10_8', 2, 'Quitar el marco',
        '<p>Implementa <code>centro(arr)</code> que retorne el array sin la primera ni la última fila, ni la primera ni la última columna. Usa un corte de NumPy.</p>' + pre('centro(np.array([[1, 1, 1, 1], [1, 5, 6, 1], [1, 1, 1, 1]]))  →  [[5 6]]'),
        'import numpy as np\n\ndef centro(arr):\n    # tu código aquí\n    return arr\n',
        'import numpy as np\n\ndef centro(arr):\n    return arr[1:-1, 1:-1]\n',
        ['print(centro(np.array([[1, 1, 1, 1], [1, 5, 6, 1], [1, 1, 1, 1]])).tolist())', 'print(centro(np.arange(25).reshape(5, 5)).tolist())', 'print(centro(np.ones((3, 3))).shape)'],
        ['<code>1:-1</code> va desde la segunda hasta antes de la última; se aplica a filas y a columnas.'], '', [['npsl']]))
    E.append(codex('n10_9', 2, 'Recortar una ventana',
        '<p>Implementa <code>ventana(arr, f, c, alto, ancho)</code>: retorna el pedazo que empieza en la fila <code>f</code>, columna <code>c</code>, con <code>alto</code> filas y <code>ancho</code> columnas.</p>',
        'import numpy as np\n\ndef ventana(arr, f, c, alto, ancho):\n    # tu código aquí\n    return arr\n',
        'import numpy as np\n\ndef ventana(arr, f, c, alto, ancho):\n    return arr[f:f + alto, c:c + ancho]\n',
        ['a = np.arange(30).reshape(5, 6)\nprint(ventana(a, 1, 2, 2, 3).tolist())', 'a = np.arange(30).reshape(5, 6)\nprint(ventana(a, 0, 0, 5, 1).tolist())', 'a = np.zeros((720, 960, 3))\nprint(ventana(a, 400, 400, 200, 400).shape)'],
        ['El fin de cada corte es inicio + tamaño (porque el fin no se incluye).'], '', [['npsl']]))
    tools = [{'w': 'img', 't': 'NumPy en el navegador', 'p': 'Escribe y ejecuta código con NumPy (la primera vez descarga la librería). Si guardas una matriz en <code>matrix</code>, se dibuja.',
              'o': {'code': NP0 + '\nprint(notas_np.shape)\nprint(notas_np[:, 1:3])\n\nmatrix = np.zeros((4, 4), dtype=np.uint8)\nmatrix[1:3, 1:3] = 255\nprint(matrix)'}}]
    return {'id': 'n10', 'name': 'Sem. 10 · NumPy: arrays y cortes en matrices', 'teo': T_NP, 'form': [c('arr.shape') + ' (filas, columnas)', c('arr[f, c]'), c('arr[:, c]') + ' columna · ' + c('arr[f, :]') + ' fila', c('arr[1:, 1:3]') + ' rectángulo', c('np.zeros((f, c), dtype=np.uint8)')], 'lesson': L_NP, 'ex': E, 'tools': tools}

T_IMG = """
<p>Una <strong>imagen</strong> es una matriz de píxeles. En <b>escala de grises</b> cada píxel es un número de 0 (negro) a 255 (blanco): un byte, 2⁸ = 256 intensidades. En una imagen a <b>color</b>, cada píxel tiene tres <b>canales</b> <code>[R, G, B]</code> (rojo, verde, azul), así que la matriz tiene forma <code>(alto, ancho, 3)</code>.</p>
<p>Colores útiles: <code>[255, 0, 0]</code> rojo · <code>[0, 255, 0]</code> verde · <code>[0, 0, 255]</code> azul · <code>[255, 255, 0]</code> amarillo · <code>[255, 255, 255]</code> blanco · <code>[0, 0, 0]</code> negro.</p>
<p>Crear una imagen: <code>matrix = np.zeros([fils, cols, 3], dtype=np.uint8)</code> (negra) y pintar píxel por píxel con <code>matrix[i][j] = [r, g, b]</code>, o zonas enteras con cortes: <code>matrix[:, :100] = [255, 0, 0]</code> pinta las primeras 100 columnas. Para verla: <code>plt.imshow(matrix)</code> y <code>plt.show()</code> (matplotlib). Para abrir una foto: <code>np.array(Image.open("foto.jpg"))</code> o <code>imageio.imread("foto.png")</code>.</p>
<p><strong>Recortes:</strong> la primera parte del corte son las filas (el alto, de arriba abajo) y la segunda las columnas (el ancho): <code>matrix[:400]</code> es la franja de arriba, <code>matrix[400:]</code> la de abajo y <code>matrix[400:600, 400:800]</code> un rectángulo de 200 × 400 píxeles.</p>
<p><strong>Transformaciones:</strong> espejo horizontal <code>nueva[i][cols - j - 1] = img[i][j]</code> (o <code>img[:, ::-1]</code>); brillo: sumar a cada canal sin pasar de 255.</p>
<div class="bqwarn">⚠️ <b>Ojo con el material:</b> en el ejemplo de «Brillo» de la clase, <code>new_img[i][j][0] + 50</code> se calcula en <code>uint8</code> (0–255), así que 250 + 50 «da la vuelta» y queda 44: el <code>if red &lt;= 255</code> nunca lo detecta. Hay que convertir antes: <code>int(new_img[i][j][0]) + 50</code> (o usar <code>min(255, …)</code>).</div>
"""
L_IMG = """<h3>Idea central</h3><p>Pintar una imagen es llenar una matriz: la fila es la altura (y) y la columna el ancho (x); el color son tres números.</p>
<h3>Conceptos clave</h3><ul><li>shape = (alto, ancho, 3).</li><li>Cortes: filas primero.</li><li>uint8 va de 0 a 255 y da la vuelta.</li></ul>
<div class="ej"><b>Ejemplo:</b> <code>matrix[i][j] = [0, 0, i]</code> hace un degradado azul de arriba (negro) hacia abajo (azul).</div>
<div class="err"><b>Error común:</b> confundir alto y ancho: <code>matrix[:, :100]</code> son columnas (una franja vertical), no filas.</div>"""

def imagenes():
    E = []
    E.append(opc('i10_1', 1, 'Colores RGB', '<p>¿Qué color es el píxel <code>[255, 255, 0]</code>?</p>', ['Amarillo', 'Blanco', 'Celeste', 'Magenta', 'Verde'],
        ['Rojo al máximo + verde al máximo + nada de azul = amarillo.'], 'Mezcla de luz, no de pintura.', [['rgb']]))
    I = np.arange(256).reshape(256, 1); J = np.arange(256).reshape(1, 256); Z = np.zeros((256, 256), dtype=int)
    def rgb(r, g, b): return np.stack([np.broadcast_to(r, (256, 256)), np.broadcast_to(g, (256, 256)), np.broadcast_to(b, (256, 256))], axis=2)
    opts = [imgopt(rgb(I, Z, J), 'A'), imgopt(rgb(I, J, Z), 'B'), imgopt(rgb(Z, Z, I), 'C'), imgopt(rgb(J, Z, I), 'D'), imgopt(rgb(Z, I, J), 'E')]
    E.append(opc('i10_2', 2, '¿Qué imagen sale?', pre('fils = 255\ncols = 255\nmatrix = np.zeros([fils, cols, 3], dtype=np.uint8)\nfor i in range(fils):\n    for j in range(cols):\n        matrix[i][j] = [i, 0, j]') + '<p>¿Qué imagen produce?</p>',
        opts, ['El rojo crece hacia abajo (depende de la fila <code>i</code>) y el azul hacia la derecha (columna <code>j</code>).', 'Arriba a la izquierda es negro; abajo a la derecha, magenta (rojo + azul).'],
        'Arriba-izquierda: i = 0, j = 0.', [['rgb'], ['rgb']], p='Elige la imagen'))
    E.append(opc('i10_3', 1, 'Tamaño de un recorte', '<p>Una foto tiene <code>shape = (720, 960, 3)</code>. ¿Qué <code>shape</code> tiene <code>matrix[400:600, 400:800]</code>?</p>',
        ['(200, 400, 3)', '(400, 200, 3)', '(200, 400)', '(600, 800, 3)', '(400, 400, 3)'],
        ['Filas 400 a 599 → 200; columnas 400 a 799 → 400; los 3 canales se mantienen.'], '', [['imgsl']]))
    E.append(opc('i10_4', 1, 'Escala de grises', '<p>En una imagen en escala de grises con <code>dtype=np.uint8</code>, ¿qué es cierto?</p>',
        ['Cada píxel va de 0 (negro) a 255 (blanco): 256 intensidades', 'Cada píxel tiene 3 canales', 'Cada píxel va de 0 (blanco) a 255 (negro)', 'Cada píxel va de 0 a 100 (porcentaje de luz)', 'Los píxeles son decimales entre 0 y 1'],
        ['Un byte (8 bits) por píxel: 2⁸ = 256 valores, de 0 = negro a 255 = blanco. Un solo canal.'], '', [['gris']]))
    flag = 'import numpy as np\nmatrix = np.zeros([100, 300, 3], dtype=np.uint8)\nmatrix[:, ⟦0⟧] = [255, 0, 0]\nmatrix[:, 100:200] = [255, 255, 255]\nmatrix[:, ⟦1⟧] = [255, 0, 0]'
    E.append(hueco('i10_5', 1, 'Bandera con cortes', '<p>Completa para pintar la bandera del Perú (rojo, blanco, rojo) en una imagen de 100 × 300.</p>', flag,
        [(([':100', '0:100']), 'Las primeras 100 columnas.', 'Desde el inicio hasta antes de 100: :100.'), (['200:', '200:300'], 'Desde la columna 200 hasta el final.', 'La última franja es 200:.')],
        ['Antes de la coma van las filas (todas, <code>:</code>); después, las columnas de cada franja.'], '', [['imgsl']],
        tests=[{'n': 'Colores de las tres franjas', 'run': 'print(matrix[50, 50].tolist(), matrix[50, 150].tolist(), matrix[50, 250].tolist(), matrix[0, 99].tolist(), matrix[99, 200].tolist())',
                'out': '[255, 0, 0] [255, 255, 255] [255, 0, 0] [255, 0, 0] [255, 0, 0]'}],
        demo='print(matrix.shape)'))
    E.append(bug('i10_6', 3, 'El brillo que oscurece', '<p>Este es el ejemplo de «Brillo» de la clase reducido a un píxel. Debería dejar el rojo en 250 (porque 300 se pasa de 255), pero imprime otra cosa.</p>',
        'import numpy as np\nimg = np.array([[[250, 100, 20]]], dtype=np.uint8)\nnew_img = img.copy()\nrojo = new_img[0][0][0] + 50\nif rojo <= 255:\n    new_img[0][0][0] = rojo\nprint(new_img[0][0])',
        [4], ['La suma se hace en uint8 (0–255): 250 + 50 da la vuelta a 44, y el if no lo detecta', 'img.copy() no copia la imagen', 'El if debería ser rojo < 255', 'new_img[0][0][0] no existe: debería ser new_img[0, 0]', 'np.array no acepta dtype'],
        ['<code>new_img[0][0][0]</code> es un <code>np.uint8</code>; en NumPy 2, <code>uint8 + 50</code> sigue siendo uint8 y 300 se guarda como 300 − 256 = 44.', 'Como 44 ≤ 255, el if pinta 44: la imagen se oscurece. Se arregla con <code>int(new_img[0][0][0]) + 50</code>.'],
        '¿De qué tipo es new_img[0][0][0]?', [['u8'], ['u8']],
        fixed='import numpy as np\nimg = np.array([[[250, 100, 20]]], dtype=np.uint8)\nnew_img = img.copy()\nrojo = int(new_img[0][0][0]) + 50\nif rojo <= 255:\n    new_img[0][0][0] = rojo\nprint(new_img[0][0])'))
    E.append(codex('i10_7', 2, 'Espejo horizontal',
        '<p>Implementa <code>espejo(img)</code> que retorne la imagen reflejada de izquierda a derecha (la columna 0 pasa a ser la última). Puedes usar un corte.</p>',
        'import numpy as np\n\ndef espejo(img):\n    # tu código aquí\n    return img\n',
        'import numpy as np\n\ndef espejo(img):\n    return img[:, ::-1]\n',
        ['print(espejo(np.array([[1, 2, 3], [4, 5, 6]])).tolist())', 'a = np.zeros((2, 3, 3), dtype=np.uint8)\na[0, 0] = [255, 0, 0]\nprint(espejo(a)[0, 2].tolist(), espejo(a)[0, 0].tolist())'],
        ['Todas las filas (<code>:</code>) y las columnas al revés (<code>::-1</code>). Con bucles: <code>nueva[i][cols - j - 1] = img[i][j]</code>.'], '', [['imgsl', 'slneg']]))
    E.append(codex('i10_8', 2, 'Negativo en grises (con listas)',
        '<p>Implementa <code>negativo(img)</code>: <code>img</code> es una lista de listas de enteros 0–255 (grises). Retorna una matriz <b>nueva</b> con <code>255 - valor</code> en cada píxel.</p>' + pre('negativo([[0, 255], [100, 30]])  →  [[255, 0], [155, 225]]'),
        'def negativo(img):\n    # tu código aquí\n    return img\n',
        'def negativo(img):\n    res = []\n    for f in range(len(img)):\n        fila = []\n        for c in range(len(img[0])):\n            fila.append(255 - img[f][c])\n        res.append(fila)\n    return res\n',
        ['print(negativo([[0, 255], [100, 30]]))', 'print(negativo([[128]]))', 'a = [[10, 20, 30]]\nr = negativo(a)\nprint(a, r)'],
        ['Se arma la matriz nueva fila por fila con <code>255 - img[f][c]</code>, sin tocar la original.'], '', [['gris', 'nueva']]))
    tools = [{'w': 'img', 't': 'Construye una imagen', 'p': 'Cambia el código y dale ▶ Dibujar. Prueba <code>[i, 0, j]</code>, <code>[i, j, 0]</code> o la cuadrícula con <code>i % 5 == 0 or j % 5 == 0</code>.',
              'o': {'code': 'import numpy as np\nimport matplotlib.pyplot as plt\n\nfils = 255\ncols = 255\nmatrix = np.zeros([fils, cols, 3], dtype=np.uint8)\nfor i in range(fils):\n    for j in range(cols):\n        matrix[i][j] = [0, 0, i]\n\nplt.imshow(matrix)\nplt.show()'}},
             {'w': 'img', 't': 'Reto: la cuadrícula', 'p': 'Escribe el código que produce la imagen objetivo (26 × 26, líneas blancas cada 5 píxeles).',
              'o': {'code': 'import numpy as np\nimport matplotlib.pyplot as plt\n\nfils = 26\ncols = 26\nmatrix = np.zeros([fils, cols, 3], dtype=np.uint8)\n# tu código aquí\n\nplt.imshow(matrix)\nplt.show()',
                    'target': 'import numpy as np\nfils = 26\ncols = 26\nmatrix = np.zeros([fils, cols, 3], dtype=np.uint8)\nfor i in range(fils):\n    for j in range(cols):\n        if i % 5 == 0 or j % 5 == 0:\n            matrix[i][j] = [255, 255, 255]'}},
             {'w': 'img', 't': 'Recortes de una foto', 'p': 'La «foto» es un paisaje dibujado con NumPy (720 × 960). Prueba <code>matrix[:400]</code>, <code>matrix[400:]</code> y <code>matrix[400:600, 400:800]</code>.',
              'o': {'code': 'import numpy as np\nimport matplotlib.pyplot as plt\nfrom PIL import Image\n\nimage = Image.open("machupicchu.jpg")\nmatrix = np.array(image)\nprint(matrix.shape)\nplt.imshow(matrix[400:600, 400:800])\nplt.show()'}},
             {'w': 'img', 't': 'Espejo y brillo', 'p': 'Prueba el espejo con un corte y el brillo sin desborde (convertir a int).',
              'o': {'code': 'import numpy as np\nimport imageio\nimport matplotlib.pyplot as plt\n\nimg = imageio.imread("mascota.png")\nnew_img = img[:, ::-1].copy()          # espejo\nfor i in range(new_img.shape[0]):\n    for j in range(new_img.shape[1]):\n        for k in range(3):\n            v = int(new_img[i][j][k]) + 50   # brillo\n            new_img[i][j][k] = min(255, v)\nplt.imshow(new_img)\nplt.show()'}}]
    return {'id': 'i10', 'name': 'Sem. 10 · Imágenes como matrices', 'teo': T_IMG, 'form': [c('(alto, ancho, 3)'), '0 negro · 255 blanco', c('matrix[i][j] = [r, g, b]'), c('matrix[:, :100] = [255, 0, 0]'), 'Espejo: ' + c('img[:, ::-1]'), 'Brillo: ' + c('min(255, int(v) + 50)')], 'lesson': L_IMG, 'ex': E, 'tools': tools}

T_DIC = """
<p>Un <strong>diccionario</strong> guarda pares <b>clave → valor</b>: <code>inventario = {"apples": 430, "bananas": 312}</code>. Se busca por clave, no por posición: <code>inventario["bananas"]</code> → 312. Las <b>claves</b> son únicas y de un tipo <b>inmutable</b> (cadena, número, tupla); los valores pueden ser de cualquier tipo (también listas u otros diccionarios). Si escribes una clave dos veces al crearlo, se queda el último valor.</p>
<ul><li><b>Crear:</b> <code>d = {}</code>, <code>{"nombre": "Juan", "edad": 18}</code> o <code>dict([("a", 1), ("b", 2)])</code>.</li>
<li><b>Agregar o cambiar:</b> <code>d[k] = v</code> (si la clave no existe, se inserta; si existe, se reemplaza).</li>
<li><b>Leer:</b> <code>d[k]</code> da <code>KeyError</code> si la clave no está; pregunta antes con <code>k in d</code> (o <code>k in d.keys()</code>) o usa <code>d.get(k, defecto)</code>.</li>
<li><b>Borrar:</b> <code>del d[k]</code>, <code>d.pop(k)</code> (además devuelve el valor), <code>d.clear()</code> (vacía todo).</li>
<li><b>Recorrer:</b> <code>for k in d:</code> (claves), <code>d.keys()</code>, <code>d.values()</code> y <code>for k, v in d.items():</code>. <code>sum(d.values())</code> suma los valores.</li></ul>
<p>Patrones de examen: <b>contar frecuencias</b> (la clave es la palabra; si ya está, +1; si no, 1), <b>agrupar</b> (la clave es la longitud o la categoría y el valor una lista a la que se hace <code>append</code>), <b>tabla de búsqueda</b> (tipo de cambio, precios) y <b>resumir</b> (promedio de la lista de cada clave).</p>
"""
L_DIC = """<h3>Idea central</h3><p>Una lista se indexa por posición; un diccionario, por un nombre (la clave). Es la estructura natural para contar y para buscar.</p>
<h3>Conceptos clave</h3><ul><li><code>d[k] = v</code> inserta o reemplaza.</li><li>Leer una clave que no está → KeyError.</li><li><code>items()</code> da clave y valor juntos.</li></ul>
<div class="ej"><b>Ejemplo:</b> «cuentos cuentas cuentos» → <code>{"cuentos": 2, "cuentas": 1}</code>.</div>
<div class="err"><b>Error común:</b> <code>d[p] = d[p] + 1</code> sin haber creado antes la clave.</div>"""

def dicts():
    E = []
    E.append(ex('d11_1', 1, '¿Sirve como clave?', '<p>Clasifica: ¿se puede usar como clave de un diccionario?</p>',
        [{'t': 'cls', 'p': 'Clasifica', 'cats': ['Sí', 'No'], 'items': [{'x': c('"nombre"'), 'c': 0}, {'x': c('25'), 'c': 0}, {'x': c('3.5'), 'c': 0}, {'x': c('(1, 2)'), 'c': 0, 'e': 'Una tupla es inmutable.'},
            {'x': c('[1, 2]'), 'c': 1, 'e': 'Una lista es mutable: no puede ser clave.'}, {'x': c('{"a": 1}'), 'c': 1, 'e': 'Un diccionario es mutable.'}, {'x': c('"20258765"'), 'c': 0}]}],
        ['Las claves deben ser inmutables: cadenas, números y tuplas sí; listas y diccionarios no (dan <code>TypeError: unhashable type</code>).'],
        'Cadenas, números y tuplas sí; listas y diccionarios no', '', [['dic']]))
    code = 'frutas = {"mango": 75, "pera": 24, "manzana": 20}\nfrutas["sandia"] = 17\nfrutas["manzana"] = 500\nprint(frutas)\nprint(frutas["pera"] + frutas["sandia"])'
    E.append(imprime('d11_2', 1, 'Insertar y modificar', code,
        ["{'mango': 75, 'pera': 24, 'manzana': 20, 'sandia': 17, 'manzana': 500}\n41", "{'mango': 75, 'pera': 24, 'manzana': 520, 'sandia': 17}\n41", "{'mango': 75, 'pera': 24, 'manzana': 500}\n24", "{'sandia': 17, 'mango': 75, 'pera': 24, 'manzana': 500}\n41"],
        ['«sandia» no existía: se <b>inserta</b> al final. «manzana» ya existía: se <b>reemplaza</b> su valor por 500.', '24 + 17 = 41.'], '', [['dset'], ['dacc']]))
    E.append(imprime('d11_3', 2, 'Claves repetidas', 'da = {"20258765": "Luis",\n      "20259876": "Ana",\n      "20258765": "Pedro"}\nprint(da)\nprint(len(da))',
        ["{'20258765': 'Luis', '20259876': 'Ana', '20258765': 'Pedro'}\n3", "{'20258765': 'Luis', '20259876': 'Ana'}\n2", "{'20259876': 'Ana', '20258765': 'Pedro'}\n2", 'Da error por la clave repetida'],
        ['Las claves son únicas: la segunda vez, «20258765» reemplaza «Luis» por «Pedro» y conserva su lugar.', 'Quedan 2 pares.'], 'Una clave no puede estar dos veces.', [['dic'], ['dset']]))
    E.append(opc('d11_4', 1, 'del, pop y clear', pre('p = {"nombre": "Juan", "edad": 18, "hijos": False}\nx = p.pop("edad")\ndel p["hijos"]\nprint(p, x)') + '<p>¿Qué imprime?</p>',
        ["{'nombre': 'Juan'} 18", "{'nombre': 'Juan'} None", "{} 18", "{'nombre': 'Juan', 'hijos': False} 18", 'Da KeyError'],
        ['<code>pop("edad")</code> quita el par y devuelve 18; <code>del p["hijos"]</code> quita otro par.', 'Solo queda «nombre». (<code>clear()</code> lo habría vaciado todo.)'], '', [['ddel'], ['ddel']], p='Salida',
        play='p = {"nombre": "Juan", "edad": 18, "hijos": False}\nx = p.pop("edad")\ndel p["hijos"]\nprint(p, x)'))
    E.append(hueco('d11_5', 1, 'Contar palabras', '<p>Completa para contar cuántas veces aparece cada palabra (sin distinguir mayúsculas).</p>',
        'def frecuencias(texto):\n    d = {}\n    for p in texto.lower().split():\n        if ⟦0⟧:\n            d[p] = d[p] + 1\n        else:\n            ⟦1⟧\n    return d',
        [(['p in d', 'p in d.keys()'], '¿Cuándo se puede sumar 1?', 'Solo si la palabra ya es clave: p in d.'), (['d[p] = 1', 'd[p]=1'], 'Primera vez que aparece la palabra.', 'Se crea la clave con valor 1.')],
        ['Si la palabra ya está, se suma 1; si no, se crea con 1.'], '', [['dcont']],
        tests=mk_tests('def frecuencias(texto):\n    d = {}\n    for p in texto.lower().split():\n        if p in d:\n            d[p] = d[p] + 1\n        else:\n            d[p] = 1\n    return d',
                       ['print(frecuencias("Cuando cuentes cuentos cuenta cuantos cuentos cuentas"))', 'print(frecuencias("a A a b"))']),
        demo='print(frecuencias("Cuando cuentes cuentos cuenta cuantos cuentos cuentas porque si cuentas cuantos cuentos cuentas sabras cuantos cuentos sabes contar"))'))
    E.append(bug('d11_6', 2, 'KeyError al contar', '<p>Debería contar las letras de una palabra.</p>',
        'def contar_letras(palabra):\n    d = {}\n    for letra in palabra:\n        d[letra] = d[letra] + 1\n    return d\n\nprint(contar_letras("casa"))',
        [4], ['La primera vez que aparece una letra, d[letra] no existe y leerla da KeyError', 'Las letras no pueden ser claves', 'Debería ser d.append(letra)', 'Falta convertir la palabra a lista', 'El diccionario debería crearse con dict()'],
        ['En la primera vuelta, <code>d["c"]</code> no existe: leerlo da <code>KeyError</code>.', 'Solución: <code>d[letra] = d.get(letra, 0) + 1</code> o el if/else de siempre.'],
        '¿Qué hay en d en la primera vuelta?', [['dacc'], ['dcont']],
        fixed='def contar_letras(palabra):\n    d = {}\n    for letra in palabra:\n        d[letra] = d.get(letra, 0) + 1\n    return d\n\nprint(contar_letras("casa"))'))
    prec = {"manzana": 0.5, "banana": 0.3, "leche": 1.2, "pan": 1.0, "huevos": 0.2}
    car = {"manzana": 4, "huevos": 10, "pan": 3}
    rows = []; tot = 0
    for k, u in car.items():
        tot = round(tot + u * prec[k], 2); rows.append(['"' + k + '"', str(u), {'a': [str(tot), str(tot).replace('.0', '') if str(tot).endswith('.0') else str(tot)]}])
    E.append(ex('d11_7', 2, 'Rastreo de items()', '<p>Completa el total al terminar cada vuelta.</p>',
        [{'t': 'traza', 'p': 'Rastrea el for', 'code': 'precios = ' + repr(prec).replace("'", '"') + '\ncarrito = ' + repr(car).replace("'", '"') + '\ntotal = 0\nfor producto, unidades in carrito.items():\n    total = total + unidades * precios[producto]', 'head': ['producto', 'unidades', 'total'], 'rows': rows}],
        ['items() da los pares en orden de inserción: manzana (4 × 0,5 = 2), huevos (10 × 0,2 = 2 → 4), pan (3 × 1 = 3 → 7).'], 'total = 7.0', '', [['drec']]))
    E.append(codex('d11_8', 1, 'Tipo de cambio',
        '<p>Con <code>tasas = {"USD": 3.86, "EUR": 4.10, "GBP": 4.71, "JPY": 0.026}</code>, implementa <code>a_soles(monto, moneda)</code>: retorna el monto en soles redondeado a 2 decimales, o <code>"Moneda no encontrada"</code> si no está (Lab 11A).</p>' + pre('a_soles(100, "USD")   →  386.0\na_soles(25.6, "JPY")  →  0.67'),
        'def a_soles(monto, moneda):\n    tasas = {"USD": 3.86, "EUR": 4.10, "GBP": 4.71, "JPY": 0.026}\n    # tu código aquí\n    return 0\n',
        'def a_soles(monto, moneda):\n    tasas = {"USD": 3.86, "EUR": 4.10, "GBP": 4.71, "JPY": 0.026}\n    if moneda in tasas:\n        return round(monto * tasas[moneda], 2)\n    return "Moneda no encontrada"\n',
        ['print(a_soles(100, "USD"))', 'print(a_soles(25.6, "JPY"))', 'print(a_soles(200, "CAD"))', 'print(a_soles(10, "EUR"))'],
        ['Primero se pregunta <code>moneda in tasas</code>; si está, se multiplica por su tasa.'], '', [['dacc']], pc='dic'))
    E.append(codex('d11_9', 2, 'Carrito con descuento',
        '<p>Implementa <code>pregunta_3(carrito, precios)</code>: <code>carrito</code> = {producto: unidades}, <code>precios</code> = {producto: precio}. Retorna el total; si pasa de 50, aplica 10 % de descuento. Redondea a 2 decimales (Lab 11A).</p>',
        'def pregunta_3(carrito, precios):\n    # tu código aquí\n    return 0\n',
        'def pregunta_3(carrito, precios):\n    total = 0\n    for producto, unidades in carrito.items():\n        total = total + unidades * precios[producto]\n    if total > 50:\n        total = total * 0.9\n    return round(total, 2)\n',
        ['p = {"manzana": 0.5, "banana": 0.3, "leche": 1.2, "pan": 1.0, "huevos": 0.2}\nprint(pregunta_3({"manzana": 4, "huevos": 10}, p))', 'p = {"manzana": 0.5, "banana": 0.3, "leche": 1.2, "pan": 1.0, "huevos": 0.2}\nprint(pregunta_3({"leche": 50}, p))', 'print(pregunta_3({}, {"pan": 1.0}))'],
        ['Con <code>items()</code> recorres producto y unidades; el precio sale de <code>precios[producto]</code>.', 'El descuento se aplica una sola vez, al final.'], '', [['drec'], []], pc='dic'))
    E.append(codex('d11_10', 2, 'Palabras por longitud',
        '<p>Implementa <code>longitudes(frase)</code>: retorna un diccionario cuya clave es la longitud y cuyo valor es la lista de palabras (en minúsculas, sin repetir) con esa longitud (Teoría, semana 11).</p>' +
        pre('longitudes("Es un helicoptero o es un avion o es un cohete")\n→  {2: ["es", "un"], 11: ["helicoptero"], 1: ["o"], 5: ["avion"], 6: ["cohete"]}'),
        'def longitudes(frase):\n    # tu código aquí\n    return {}\n',
        'def longitudes(frase):\n    d = {}\n    for p in frase.lower().split():\n        n = len(p)\n        if n not in d:\n            d[n] = [p]\n        elif p not in d[n]:\n            d[n].append(p)\n    return d\n',
        ['print(longitudes("Es un helicoptero o es un avion o es un cohete"))', 'print(longitudes("El Principito se sorprendio al no ver a nadie pero a nadie"))', 'print(longitudes("Lo interesante del desierto es que esconde un pozo en cualquier parte"))'],
        ['Si la longitud es nueva, se crea su lista con la palabra; si no, se agrega solo si no estaba.'], '', [['dlist']], pc='dic'))
    E.append(codex('d11_11', 1, 'Promedios del equipo',
        '<p>Implementa <code>pregunta_1(rendimiento)</code>: recibe {nombre: lista de puntajes} y retorna {nombre: promedio redondeado a 2 decimales} (Lab 11A).</p>' + pre('pregunta_1({"Pedro": [60, 65, 70], "Lucia": [80, 82, 79]})  →  {"Pedro": 65.0, "Lucia": 80.33}'),
        'def pregunta_1(rendimiento):\n    # tu código aquí\n    return {}\n',
        'def pregunta_1(rendimiento):\n    nuevo = {}\n    for nombre, lista in rendimiento.items():\n        nuevo[nombre] = round(sum(lista) / len(lista), 2)\n    return nuevo\n',
        ['print(pregunta_1({"Pedro": [60, 65, 70], "Lucia": [80, 82, 79], "Marcos": [90, 88, 92], "Maria": [75, 70, 78]}))', 'print(pregunta_1({"Solo": [10]}))', 'print(pregunta_1({}))'],
        ['Cada valor es una lista: su promedio es <code>sum(lista) / len(lista)</code>.'], '', [['drec']], pc='dic'))
    E.append(codex('d11_12', 2, 'La palabra más frecuente',
        '<p>Implementa <code>mas_frecuente(texto)</code>: retorna la palabra (en minúsculas) que más se repite; si hay empate, la que apareció primero.</p>',
        'def mas_frecuente(texto):\n    # tu código aquí\n    return ""\n',
        'def mas_frecuente(texto):\n    d = {}\n    for p in texto.lower().split():\n        d[p] = d.get(p, 0) + 1\n    mejor = ""\n    for p, n in d.items():\n        if mejor == "" or n > d[mejor]:\n            mejor = p\n    return mejor\n',
        ['print(mas_frecuente("Cuando cuentes cuentos cuenta cuantos cuentos cuentas porque si cuentas cuantos cuentos cuentas"))', 'print(mas_frecuente("b a b a"))', 'print(mas_frecuente("Hola"))'],
        ['Primero se cuentan las frecuencias; luego se busca la clave con el valor más alto.', 'Como el diccionario guarda el orden de inserción y se usa <code>&gt;</code> estricto, en un empate gana la primera.'], '', [['dcont'], ['drec']], pc='dic'))
    tools = [paso('texto = "si cuentas cuantos cuentos cuentas"\nd = {}\nfor p in texto.split():\n    if p in d:\n        d[p] = d[p] + 1\n    else:\n        d[p] = 1\nprint(d)', 'Diccionario en vivo: contar palabras', 'Mira cómo aparece cada clave la primera vez y cómo sube su valor cuando se repite.'),
             paso('frase = "el sol se va al mar"\nd = {}\nfor p in frase.split():\n    n = len(p)\n    if n not in d:\n        d[n] = [p]\n    else:\n        d[n].append(p)\nprint(d)', 'Diccionario en vivo: agrupar por longitud', 'Los valores son listas (L1, L2…): a cada una se le hace append.')]
    return {'id': 'd11', 'name': 'Sem. 11 · Diccionarios', 'teo': T_DIC, 'form': [c('d[k] = v') + ' inserta o cambia', c('k in d') + ' · ' + c('d.get(k, 0)'), c('del d[k]') + ' · ' + c('d.pop(k)') + ' · ' + c('d.clear()'), c('for k, v in d.items():'), 'Contar: ' + c('d[p] = d.get(p, 0) + 1')], 'lesson': L_DIC, 'ex': E, 'tools': tools}

PEOPLE = 'people = {1: {"nombre": "Juan", "edad": 27, "sexo": "M"},\n          2: {"nombre": "Maria", "edad": 22, "sexo": "F"}}'
T_AN = """
<p>Un <strong>diccionario anidado</strong> tiene diccionarios como valores: <code>people = {1: {"nombre": "Juan", "edad": 27}, 2: {"nombre": "Maria", "edad": 22}}</code>. Sirve para registros: la clave de afuera identifica (un código, un DNI) y el diccionario de adentro guarda sus campos.</p>
<ul><li><b>Leer:</b> <code>people[1]["nombre"]</code> → "Juan" (primero el registro, luego el campo).</li>
<li><b>Agregar un registro:</b> completo, <code>people[3] = {"nombre": "Luna", "edad": 24}</code>, o campo por campo creando antes el interno: <code>people[3] = {}</code> y luego <code>people[3]["nombre"] = "Luna"</code>.</li>
<li><b>Borrar:</b> un campo con <code>del people[3]["edad"]</code>; un registro entero con <code>del people[3]</code>.</li>
<li><b>Recorrer:</b> <code>for pid, info in people.items():</code> y adentro <code>for campo in info:</code> (o <code>info.items()</code>).</li></ul>
<p>También se combinan con listas: <code>{"Pedro": [60, 65, 70]}</code>, o un diccionario con dos «sub-diccionarios» como <code>{"palabras": {…}, "letras": {…}}</code>.</p>
"""
L_AN = """<h3>Idea central</h3><p>Cada corchete baja un nivel: <code>d[a]</code> es un diccionario; <code>d[a][b]</code>, un valor de ese diccionario.</p>
<h3>Conceptos clave</h3><ul><li>Crea el interno antes de llenarlo.</li><li><code>items()</code> en los dos niveles.</li></ul>
<div class="ej"><b>Ejemplo:</b> <code>cursos["CS6002"]["creditos"]</code> → 4.</div>
<div class="err"><b>Error común:</b> <code>people[3]["nombre"] = "Luna"</code> sin <code>people[3] = {}</code> antes → KeyError: 3.</div>"""

def anidados():
    E = []
    E.append(imprime('a11_1', 1, 'Leer un anidado', PEOPLE + '\nprint(people[2]["nombre"], people[1]["edad"] + 1)', ['Juan 28', 'Maria 27', 'Maria 23', '2 28'],
        ['<code>people[2]</code> es el diccionario de Maria; <code>["nombre"]</code> da «Maria».', '<code>people[1]["edad"]</code> es 27; más 1 → 28.'], '', [['anid'], ['anid']]))
    E.append(imprime('a11_2', 2, 'Recorrer dos niveles', PEOPLE + '\nfor pid, info in people.items():\n    for campo in info:\n        if campo != "sexo":\n            print(pid, info[campo])',
        ['1 Juan\n2 Maria', '1 nombre\n1 edad\n2 nombre\n2 edad', 'Juan 27\nMaria 22', '1 Juan\n2 Maria\n1 27\n2 22'],
        ['El for de afuera da cada registro; el de adentro, sus campos (nombre, edad, sexo).', 'Se imprime el id y el valor de cada campo, menos el sexo.'], '', [['anid', 'drec'], []]))
    E.append(hueco('a11_3', 1, 'Registrar un curso', '<p>Completa para agregar un curso nuevo campo por campo.</p>',
        'def agregar(cursos, codigo, nombre, creditos):\n    cursos[codigo] = ⟦0⟧\n    cursos[codigo]["nombre"] = nombre\n    cursos[codigo][⟦1⟧] = creditos',
        [(['{}', 'dict()'], 'Antes de llenar los campos, el diccionario interno debe existir.', 'Se crea vacío: {}.'), (['"creditos"'], 'El nombre del campo, como cadena.', 'La clave del campo es la cadena "creditos".')],
        ['Primero <code>cursos[codigo] = {}</code>; luego cada campo con <code>cursos[codigo]["campo"] = valor</code>.'], '', [['anidadd']],
        tests=mk_tests('def agregar(cursos, codigo, nombre, creditos):\n    cursos[codigo] = {}\n    cursos[codigo]["nombre"] = nombre\n    cursos[codigo]["creditos"] = creditos',
                       ['c = {}\nagregar(c, "CS6002", "Programacion I", 4)\nprint(c)', 'c = {"X": {"nombre": "x", "creditos": 1}}\nagregar(c, "Y", "y", 2)\nprint(c["Y"]["creditos"], len(c))']),
        demo='c = {}\nagregar(c, "CS6002", "Programacion I", 4)\nagregar(c, "CC6301", "Quimica", 3)\nprint(c)'))
    E[-1]['checks'][0]['b'][1]['a'] = ['"creditos"']
    E.append(bug('a11_4', 2, 'Registro que no existe', '<p>Se quiere agregar a Luna como persona 3.</p>',
        PEOPLE + '\npeople[3]["nombre"] = "Luna"\npeople[3]["edad"] = 24\nprint(people[3])',
        [3], ['people[3] no existe todavía: hay que crear people[3] = {} antes de asignar sus campos', 'Las claves numéricas no se pueden usar', 'Debería ser people.append(3)', '"nombre" debería ir sin comillas', 'people[3] debería ser people["3"]'],
        ['<code>people[3]["nombre"]</code> primero <b>lee</b> <code>people[3]</code>, que no existe → <code>KeyError: 3</code>.', 'Se crea antes: <code>people[3] = {}</code> (o todo junto: <code>people[3] = {"nombre": "Luna", "edad": 24}</code>).'],
        '', [['anidadd'], ['anidadd']],
        fixed=PEOPLE + '\npeople[3] = {}\npeople[3]["nombre"] = "Luna"\npeople[3]["edad"] = 24\nprint(people[3])'))
    E.append(codex('a11_5', 3, 'Contar palabras y letras',
        '<p>Implementa <code>contar(texto)</code>: retorna <code>{"palabras": {…}, "letras": {…}}</code> con la frecuencia de cada palabra y de cada letra (en minúsculas, sin contar espacios) (Teoría, semana 11).</p>' + pre('contar("Si si no")\n→  {"palabras": {"si": 2, "no": 1}, "letras": {"s": 2, "i": 2, "n": 1, "o": 1}}'),
        'def contar(texto):\n    # tu código aquí\n    return {}\n',
        'def contar(texto):\n    d = {"palabras": {}, "letras": {}}\n    for palabra in texto.lower().split():\n        d["palabras"][palabra] = d["palabras"].get(palabra, 0) + 1\n        for letra in palabra:\n            d["letras"][letra] = d["letras"].get(letra, 0) + 1\n    return d\n',
        ['print(contar("Si si no"))', 'print(contar("Cuando cuentes cuentos cuenta cuantos cuentos cuentas porque si cuentas cuantos cuentos cuentas sabras cuantos cuentos sabes contar"))'],
        ['Se crean los dos diccionarios internos al inicio.', 'Para cada palabra se suma en <code>d["palabras"]</code> y, recorriendo sus letras, en <code>d["letras"]</code>.'], '', [['anid'], ['dcont']], pc='dic'))
    E.append(codex('a11_6', 2, 'Créditos por ciclo',
        '<p><code>cursos</code> = {código: {"nombre": …, "ciclo": …, "creditos": …}}. Implementa <code>por_ciclo(cursos)</code> que retorne {ciclo: total de créditos}.</p>',
        'def por_ciclo(cursos):\n    # tu código aquí\n    return {}\n',
        'def por_ciclo(cursos):\n    tot = {}\n    for codigo, info in cursos.items():\n        ciclo = info["ciclo"]\n        tot[ciclo] = tot.get(ciclo, 0) + info["creditos"]\n    return tot\n',
        ['c = {"CS6002": {"nombre": "Prog I", "ciclo": 1, "creditos": 4}, "CC6103": {"nombre": "Calculo", "ciclo": 1, "creditos": 4}, "CS1112": {"nombre": "Prog II", "ciclo": 2, "creditos": 4}}\nprint(por_ciclo(c))',
         'print(por_ciclo({"A": {"nombre": "a", "ciclo": 3, "creditos": 2}}))', 'print(por_ciclo({}))'],
        ['Se recorre cada registro; el ciclo es la clave del resultado y se acumulan sus créditos.'], '', [['anid', 'dcont']], pc='dic'))
    E.append(codex('a11_7', 3, 'Mejor nota por curso',
        '<p><code>notas</code> = {alumno: {curso: nota}}. Implementa <code>mejores(notas)</code> que retorne {curso: alumno con la mayor nota}; en empate, el primero que aparece.</p>' + pre('mejores({"Ana": {"mate": 15, "prog": 18}, "Luis": {"mate": 17, "prog": 12}})\n→  {"mate": "Luis", "prog": "Ana"}'),
        'def mejores(notas):\n    # tu código aquí\n    return {}\n',
        'def mejores(notas):\n    mejor = {}\n    for alumno, cursos in notas.items():\n        for curso, nota in cursos.items():\n            if curso not in mejor or nota > notas[mejor[curso]][curso]:\n                mejor[curso] = alumno\n    return mejor\n',
        ['print(mejores({"Ana": {"mate": 15, "prog": 18}, "Luis": {"mate": 17, "prog": 12}}))', 'print(mejores({"A": {"x": 10}, "B": {"x": 10, "y": 5}}))'],
        ['Dos for: alumnos y, dentro, sus cursos.', 'Se guarda el alumno; para comparar se busca su nota con <code>notas[mejor[curso]][curso]</code>.'], '', [['anid'], ['anid']], pc='dic'))
    tools = [paso(PEOPLE + '\npeople[3] = {}\npeople[3]["nombre"] = "Luna"\npeople[3]["edad"] = 24\ndel people[1]["sexo"]\nfor pid, info in people.items():\n    print(pid, info["nombre"])', 'Paso a paso: diccionario anidado', 'Cada registro es otro diccionario (D2, D3…) dentro de <code>people</code> (D1).')]
    return {'id': 'a11', 'name': 'Sem. 11 · Diccionarios anidados', 'teo': T_AN, 'form': [c('d[1]["nombre"]'), c('d[3] = {}') + ' antes de llenar', c('del d[3]["campo"]') + ' · ' + c('del d[3]'), c('for k, info in d.items():')], 'lesson': L_AN, 'ex': E, 'tools': tools}

SIM_NP = ['n10_2', 'n10_6', 'n10_8', 'n10_9', 'i10_3', 'i10_5', 'i10_7', 'i10_8']

def final_topics():
    return [repaso(), numpy_t(), imagenes(), dicts(), anidados()]

def simex_ef():
    return [codex('sx_reniec', 2, 'Registro de DNI',
        '<p>Implementa <code>pregunta_2(pares, buscar)</code>: <code>pares</code> es una lista de [dni, nombre] (si un DNI se repite, se queda el <b>primero</b>). Retorna el nombre del DNI <code>buscar</code> o <code>"No existe ese dato"</code> (Teoría, semana 11).</p>',
        'def pregunta_2(pares, buscar):\n    # tu código aquí\n    return ""\n',
        'def pregunta_2(pares, buscar):\n    reniec = {}\n    for dni, nombre in pares:\n        if dni not in reniec:\n            reniec[dni] = nombre\n    if buscar in reniec:\n        return reniec[buscar]\n    return "No existe ese dato"\n',
        ['print(pregunta_2([["1223", "Luis"], ["3456", "Sandra"], ["3456", "Delsy"], ["5656", "Fernando"]], "3456"))', 'print(pregunta_2([["1", "A"]], "2"))', 'print(pregunta_2([], "1"))'],
        ['Se arma el diccionario solo con DNI nuevos; luego se busca con <code>in</code>.'], '', [['dset', 'dacc']], pc='dic')]
