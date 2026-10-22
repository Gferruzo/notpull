"""Programación I · Sem. 9–10: matrices y mix (Práctica 3)."""
from p1_lib import *

CONCEPTS = {
 'mat': {'n': 'Matriz = lista de listas', 'f': c('mat[f][c]'), 'x': 'Primero la fila, luego la columna. mat[f] es toda la fila f.', 'home': 'm9'},
 'dims': {'n': 'Filas y columnas', 'f': c('len(mat)') + ' filas · ' + c('len(mat[0])') + ' columnas', 'x': 'len(mat[0]) es el largo de la primera fila (todas miden igual).', 'home': 'm9'},
 'recf': {'n': 'Recorrer una fila', 'f': 'fila fija: ' + c('for c in range(len(mat[0]))'), 'x': 'Lo fijo va escrito; lo que cambia es la variable del for.', 'home': 'm9'},
 'recc': {'n': 'Recorrer una columna', 'f': 'columna fija: ' + c('for f in range(len(mat))'), 'x': 'Para una columna, el for avanza por las filas.', 'home': 'm9'},
 'rect': {'n': 'Recorrer toda la matriz', 'f': c('for f …') + ' + ' + c('for c …') + ' anidados', 'x': 'El for de afuera fija la fila; el de adentro recorre sus columnas.', 'home': 'm9'},
 'tabla': {'n': 'Imprimir como tabla', 'f': c('print("%5d" % x, end="")') + ' + ' + c('print()'), 'x': 'end="" deja el cursor en la misma línea; el print() vacío salta de fila.', 'home': 'm9'},
 'crear': {'n': 'Crear una matriz n × m', 'f': c('mat.append([0] * m)') + ' n veces', 'x': 'Cada append agrega una fila distinta.', 'home': 'm10'},
 'trampa': {'n': 'La trampa [[0]*m]*n', 'f': c('[[0] * 3] * 2') + ' = la misma fila 2 veces', 'x': 'Cambiar una casilla cambia esa columna en todas las filas.', 'home': 'm10'},
 'fmut': {'n': 'Funciones que mutan', 'f': c('llenar(mat)') + ' cambia mat', 'x': 'La función recibe la misma lista: si la modifica, no hace falta return.', 'home': 'm10'},
 'borde': {'n': 'Borde', 'f': c('f == 0 or f == filas-1 or c == 0 or c == col-1'), 'x': 'Primera o última fila, o primera o última columna.', 'home': 'm10'},
 'vec': {'n': 'Vecinos sin salirse', 'f': c('0 <= f < filas and 0 <= c < col'), 'x': 'Verifica los límites ANTES de usar mat[f][c]; un índice −1 no da error pero lee el otro extremo.', 'home': 'm10'},
 'serp': {'n': 'Serpiente', 'f': 'fila par → izquierda a derecha · impar → al revés', 'x': 'range(col-1, -1, -1) recorre las columnas al revés.', 'home': 'm10'},
 'nueva': {'n': 'Matriz resultado', 'f': 'crear vacía y llenar ' + c('res[f][c] = …'), 'x': 'Para no modificar las de entrada, se arma una nueva del tamaño adecuado.', 'home': 'm10'},
 'rot': {'n': 'Rotar y transponer', 'f': 'transpuesta: ' + c('t[c][f] = mat[f][c]'), 'x': 'Escribe a mano dónde termina cada casilla y saca la regla de índices.', 'home': 'm10'},
}

M = [[18, 17, 20, 16, 17], [5, 10, 20, 19, 17], [12, 14, 15, 19, 9], [18, 20, 12, 11, 10]]
MS = 'mat = [\n    [18, 17, 20, 16, 17],\n    [ 5, 10, 20, 19, 17],\n    [12, 14, 15, 19,  9],\n    [18, 20, 12, 11, 10]\n]'

T_M1 = """
<p>Python no tiene un tipo «matriz»: se usa una <strong>lista de listas</strong> donde cada lista interna es una <b>fila</b> y todas tienen el mismo largo. <code>mat[f]</code> es la fila <code>f</code> completa y <code>mat[f][c]</code> el elemento de la fila <code>f</code>, columna <code>c</code> (ambos desde 0; el elemento \\(a_{ij}\\) de matemática es <code>mat[i-1][j-1]</code>). La cantidad de filas es <code>len(mat)</code> y la de columnas <code>len(mat[0])</code>.</p>
<p>Recorridos básicos (la regla: <b>lo que queda fijo se escribe; lo que cambia es la variable del for</b>):</p>
<ul><li>Una <b>fila</b> f: <code>for c in range(len(mat[0])): … mat[f][c]</code> (también <code>sum(mat[f])</code>).</li>
<li>Una <b>columna</b> c: <code>for f in range(len(mat)): … mat[f][c]</code>.</li>
<li><b>Toda</b> la matriz: dos for anidados; el de afuera recorre filas y el de adentro columnas (o al revés, para ir columna por columna).</li></ul>
<p>Para imprimirla como tabla: <code>print("%5d" % mat[f][c], end="")</code> dentro del for de columnas (5 espacios por número, sin saltar de línea) y un <code>print()</code> al terminar cada fila.</p>
<p>Las tablas con nombres se arman con <b>listas paralelas</b> (<code>paises[f]</code> ↔ <code>medallas[f]</code>) o poniendo el nombre en la columna 0 (<code>["Russia", 3, 1, 1]</code>; los números empiezan en la columna 1).</p>
"""
L_M1 = """<h3>Idea central</h3><p>Piensa la matriz como una tabla: primero eliges la fila (de arriba abajo) y luego la columna (de izquierda a derecha).</p>
<h3>Conceptos clave</h3><ul><li><code>mat[f][c]</code>: fila primero.</li><li><code>len(mat)</code> filas, <code>len(mat[0])</code> columnas.</li><li>Fijo = escrito; variable = la del for.</li></ul>
<div class="ej"><b>Ejemplo:</b> en la matriz de 4 × 5 de la clase, <code>mat[2][3]</code> es 19 y <code>mat[3][1]</code> es 20.</div>
<div class="err"><b>Error común:</b> usar <code>len(mat)</code> para recorrer columnas: en una matriz no cuadrada se salta columnas o se sale de rango.</div>"""
F_M1 = [c('mat[f][c]') + ' fila, columna', c('len(mat)') + ' filas · ' + c('len(mat[0])') + ' columnas', 'Fila f: ' + c('sum(mat[f])'),
        'Columna c: ' + c('for f in range(len(mat)): s += mat[f][c]'), c('print("%5d" % x, end="")')]

def matrices1():
    E = []
    E.append(opc('m9_1', 1, 'Filas y columnas', pre(MS + '\nprint(len(mat), len(mat[0]))') + '<p>¿Qué imprime?</p>',
        ['4 5', '5 4', '4 4', '20 5', '5 5'], ['<code>mat</code> tiene 4 listas internas (filas) → <code>len(mat) = 4</code>.', 'Cada fila tiene 5 números → <code>len(mat[0]) = 5</code>.'],
        '', [['dims'], ['dims']], p='Salida', play=MS + '\nprint(len(mat), len(mat[0]))'))
    E.append(imprime('m9_2', 1, 'Acceder a elementos', MS + '\nprint(mat[2][3], mat[3][1])\nprint(mat[1])',
        ['15 12\n[17, 10, 20, 15, 18]', '19 20\n[18, 17, 20, 16, 17]', '19 20\n17', '15 18\n[5, 10, 20, 19, 17]'],
        ['<code>mat[2][3]</code>: fila 2, columna 3 → 19. <code>mat[3][1]</code>: fila 3, columna 1 → 20.', '<code>mat[1]</code> es toda la fila 1: [5, 10, 20, 19, 17].'],
        'Fila primero, columna después.', [['mat'], ['mat']]))
    code = 'suma = 0\nfor f in range(len(mat)):\n    suma = suma + mat[f][2]'
    E.append(ex('m9_3', 1, '¿Qué celdas suma?', '<p>Toca las celdas que suma este código.</p>' + pre(code),
        [{'t': 'mtx', 'p': 'Toca las celdas', 'm': M, 'a': [[f, 2] for f in range(4)], 'name': 'mat'}],
        ['La columna 2 queda fija; <code>f</code> recorre las filas 0 a 3.'], 'Toda la columna 2 (20 + 20 + 15 + 12 = 67)', 'Lo fijo es lo que está escrito.', [['recc']], play=MS + '\n' + code + '\nprint(suma)'))
    code = 'suma = 0\nfor c in range(1, 4):\n    suma = suma + mat[2][c]'
    E.append(ex('m9_4', 2, 'Parte de una fila', '<p>Toca las celdas que suma este código.</p>' + pre(code),
        [{'t': 'mtx', 'p': 'Toca las celdas', 'm': M, 'a': [[2, c_] for c_ in range(1, 4)], 'name': 'mat'}],
        ['La fila 2 queda fija; <code>c</code> va de 1 a 3 (el 4 no se incluye).'], 'mat[2][1], mat[2][2] y mat[2][3] (14 + 15 + 19 = 48)', '', [['recf']], play=MS + '\n' + code + '\nprint(suma)'))
    med = 'paises = ["Canada", "Italy", "Japan", "Russia"]\nmedallas = [\n    [0, 3, 0],\n    [0, 0, 1],\n    [1, 0, 0],\n    [3, 1, 1]\n]'
    E.append(imprime('m9_5', 2, 'Medallero', med + '\nfor f in range(len(paises)):\n    total = 0\n    for c in range(3):\n        total = total + medallas[f][c]\n    if total > 1:\n        print(paises[f], total)',
        ['Russia 5', 'Canada 3\nItaly 1\nJapan 1\nRussia 5', 'Canada 0\nRussia 3', 'Canada 3\nJapan 1\nRussia 5'],
        ['Para cada país (fila) se suman sus 3 columnas: Canada 3, Italy 1, Japan 1, Russia 5.', 'Solo se imprimen los que tienen más de 1: Canada y Russia.'],
        '<code>total</code> se reinicia en cada fila.', [['par', 'rect'], []]))
    E.append(hueco('m9_6', 1, 'Suma de una columna', '<p>Completa la función que suma la columna <code>c</code>.</p>',
        'def suma_columna(mat, c):\n    suma = 0\n    for f in range(⟦0⟧):\n        suma = suma + ⟦1⟧\n    return suma',
        [(['len(mat)', '0, len(mat)', '0, len(mat), 1'], '¿Cuántas filas hay que recorrer?', 'Para una columna se recorren todas las filas: range(len(mat)).'),
         (['mat[f][c]'], 'La fila cambia, la columna c queda fija.', 'Primero va la fila: mat[f][c], no mat[c][f].')],
        ['La columna <code>c</code> está fija; el for avanza por las filas con <code>f</code>.', 'Cada vuelta suma <code>mat[f][c]</code>.'],
        '', [['recc'], ['mat']],
        tests=mk_tests('def suma_columna(mat, c):\n    suma = 0\n    for f in range(len(mat)):\n        suma = suma + mat[f][c]\n    return suma',
                       ['print(suma_columna(' + repr(M) + ', 2))', 'print(suma_columna([[1, 2], [3, 4], [5, 6]], 1))']),
        demo=MS + '\nprint(suma_columna(mat, 3))'))
    E.append(bug('m9_7', 2, 'Suma de toda la matriz', '<p>Debería imprimir la suma de los 20 números (304), pero imprime otra cosa.</p>',
        MS + '\nsuma = 0\nfor f in range(len(mat)):\n    for c in range(len(mat)):\n        suma = suma + mat[f][c]\nprint(suma)',
        [9], ['El for de columnas usa len(mat) (filas) en vez de len(mat[0]) (columnas)', 'suma debería reiniciarse dentro del primer for', 'mat[f][c] debería ser mat[c][f]', 'El print debería estar dentro de los for', 'range necesita empezar en 1'],
        ['La matriz es de 4 × 5: <code>range(len(mat))</code> en el for interno solo llega a la columna 3 y se salta la última (17 + 17 + 9 + 10 = 53 de diferencia).', 'Las columnas se cuentan con <code>len(mat[0])</code>.'],
        '¿Cuántas columnas recorre el for de adentro?', [['dims'], ['dims']],
        fixed=MS + '\nsuma = 0\nfor f in range(len(mat)):\n    for c in range(len(mat[0])):\n        suma = suma + mat[f][c]\nprint(suma)'))
    E.append(codex('m9_8', 1, 'Puntajes por competencia',
        '<p>Cada fila es un estudiante y cada columna una competencia. Implementa <code>pregunta_4(puntajes)</code> que retorne una lista con el total de cada columna (Tarea de Laboratorio 9).</p>' +
        pre('pregunta_4([[5, 10, 15], [2, 8, 6], [3, 12, 9]])  →  [10, 30, 30]'),
        'def pregunta_4(puntajes):\n    # tu código aquí\n    return []\n',
        'def pregunta_4(puntajes):\n    totales = []\n    for c in range(len(puntajes[0])):\n        s = 0\n        for f in range(len(puntajes)):\n            s = s + puntajes[f][c]\n        totales.append(s)\n    return totales\n',
        ['print(pregunta_4([[5, 10, 15], [2, 8, 6], [3, 12, 9]]))', 'print(pregunta_4([[0, 0, 0], [1, 2, 3], [4, 5, 6]]))', 'print(pregunta_4([[100], [50], [25]]))'],
        ['El for de afuera recorre las <b>columnas</b>; para cada una se suma toda la columna con el for de las filas.', 'Al terminar cada columna, se agrega su total a la lista.'],
        'Columna por columna.', [['recc', 'rect'], ['agr']], hidden=['print(pregunta_4([[1, 2, 3, 4]]))'], pc='mat'))
    E.append(codex('m9_9', 2, 'Estanterías en estado crítico',
        '<p>Cada celda de <code>almacen</code> es la cantidad de un producto. Implementa <code>pregunta_3(almacen, stock_minimo)</code> que cuente cuántas celdas tienen una cantidad <b>menor o igual</b> al mínimo (Tarea de Laboratorio 9).</p>' +
        pre('pregunta_3([[10, 5, 20], [2, 15, 0], [30, 8, 12]], 5)  →  3'),
        'def pregunta_3(almacen, stock_minimo):\n    # tu código aquí\n    return 0\n',
        'def pregunta_3(almacen, stock_minimo):\n    cont = 0\n    for f in range(len(almacen)):\n        for c in range(len(almacen[0])):\n            if almacen[f][c] <= stock_minimo:\n                cont = cont + 1\n    return cont\n',
        ['print(pregunta_3([[10, 5, 20], [2, 15, 0], [30, 8, 12]], 5))', 'print(pregunta_3([[100, 50], [75, 120]], 20))', 'print(pregunta_3([[0, 0, 1], [0, 5, 0]], 1))', 'print(pregunta_3([[5, 10, 3, 7]], 8))'],
        ['Se recorre toda la matriz con dos for.', 'Cada celda con <code>&lt;= stock_minimo</code> suma 1 al contador.'],
        'Ojo: menor o igual.', [['rect'], ['acum']], hidden=['print(pregunta_3([[10, 25, 5, 18, 0], [22, 1, 30, 7, 15], [40, 50, 2, 0, 11], [9, 13, 28, 4, 19], [6, 35, 17, 3, 21]], 10))'], pc='mat'))
    pob = 'poblacion = [\n    [106, 107, 111, 133, 221, 767, 1766],\n    [502, 635, 809, 947, 1402, 3634, 5268],\n    [2, 2, 2, 6, 13, 30, 46],\n    [163, 203, 276, 408, 547, 729, 628],\n    [2, 7, 26, 82, 172, 307, 392],\n    [16, 24, 38, 74, 167, 511, 809]\n]\ncontinentes = ["Africa", "Asia", "Australia", "Europe", "North America", "South America"]'
    E.append(codex('m9_10', 2, 'Población mundial',
        '<p>Con los datos de la clase (cada fila es un continente y cada columna un año, de 1750 a 2050), implementa <code>mas_poblado(poblacion, continentes, anio)</code>: retorna el continente con más habitantes en la columna <code>anio</code>.</p>' + pre(pob),
        'def mas_poblado(poblacion, continentes, anio):\n    # tu código aquí\n    return ""\n',
        'def mas_poblado(poblacion, continentes, anio):\n    imax = 0\n    for f in range(len(poblacion)):\n        if poblacion[f][anio] > poblacion[imax][anio]:\n            imax = f\n    return continentes[imax]\n',
        [pob + '\nprint(mas_poblado(poblacion, continentes, 6))', pob + '\nprint(mas_poblado(poblacion, continentes, 0))', 'print(mas_poblado([[1, 9], [5, 2]], ["A", "B"], 0))', 'print(mas_poblado([[1, 9], [5, 2]], ["A", "B"], 1))'],
        ['La columna <code>anio</code> queda fija y se recorren las filas buscando la posición del mayor.', 'Con esa posición se saca el nombre de la lista paralela.'],
        'Mayor de una columna, pero guardando la fila.', [['recc', 'maxmin'], ['par']],
        names=['Año 2050 (columna 6)', 'Año 1750 (columna 0)', 'Matriz pequeña, columna 0', 'Matriz pequeña, columna 1'], pc='mat'))
    tools = [{'w': 'mtx', 't': 'Recorridos animados', 'p': 'Elige un recorrido y dale ▶ Animar o Paso. El número naranja es el orden en que se visita cada celda.', 'o': {'m': M, 'modes': ['fila', 'col', 'filas', 'cols']}},
             paso('mat = [[18, 17, 20], [5, 10, 20]]\nfor f in range(len(mat)):\n    for c in range(len(mat[0])):\n        print("%4d" % mat[f][c], end="")\n    print()', 'Paso a paso: imprimir como tabla', 'Mira la salida: <code>end=""</code> no salta de línea; el <code>print()</code> vacío sí.')]
    return {'id': 'm9', 'name': 'Sem. 9 · Matrices: listas de listas', 'teo': T_M1, 'form': F_M1, 'lesson': L_M1, 'ex': E, 'tools': tools}

T_M2 = """
<p><strong>Crear una matriz de n × m.</strong> Se empieza con una lista vacía y se agregan n filas, cada una nueva: <code>mat = []</code> y luego <code>for f in range(n): mat.append([0] * m)</code>. <b>Nunca</b> con <code>[[0] * m] * n</code>: eso repite la <em>misma</em> fila n veces, y al cambiar <code>mat[0][0]</code> cambia la columna 0 de todas las filas.</p>
<p><strong>Funciones con matrices.</strong> Como las listas son mutables, una función que recibe la matriz y la cambia (<code>llenar(mat)</code>, <code>multiplicar(mat, k)</code>) modifica la original y no necesita <code>return</code>. Si se pide una matriz <b>nueva</b> (suma, rotación, coincidencias), se crea del tamaño adecuado dentro de la función y se retorna. Para leer datos: <code>mat[f][c] = int(input("mat[%d][%d] = " % (f, c)))</code>.</p>
<p>Recorridos de práctica:</p>
<ul><li><b>Borde:</b> la celda está en el borde si <code>f == 0 or f == filas - 1 or c == 0 or c == col - 1</code>.</li>
<li><b>Serpiente:</b> filas pares de izquierda a derecha y filas impares de derecha a izquierda (<code>range(col - 1, -1, -1)</code>).</li>
<li><b>Vecinos de (F, C):</b> recorrer <code>f</code> de F − 1 a F + 1 y <code>c</code> de C − 1 a C + 1, saltando la propia celda y verificando <code>0 &lt;= f &lt; filas and 0 &lt;= c &lt; col</code> <b>antes</b> de leer. Ojo: <code>mat[-1]</code> no da error, ¡lee la última fila!</li>
<li><b>Diagonal:</b> <code>mat[i][i]</code>. <b>Transpuesta:</b> <code>t[c][f] = mat[f][c]</code>. Para otras transformaciones (rotar, espejo), escribe a mano dónde termina cada casilla y saca la regla.</li></ul>
<p>En la práctica pueden pedirte combinar con listas: devolver una lista con los máximos de cada fila, el índice de la fila con mayor suma, etc.</p>
"""
L_M2 = """<h3>Idea central</h3><p>Primero decide <b>qué celdas</b> visitas (todas, borde, serpiente, vecinos) y <b>qué haces</b> con cada una (sumar, contar, copiar a otra matriz).</p>
<h3>Conceptos clave</h3><ul><li>Crear con append, no con <code>*</code>.</li><li>Verifica los límites antes de leer.</li><li>Matriz nueva = crear vacía + llenar + retornar.</li></ul>
<div class="ej"><b>Ejemplo:</b> serpiente de <code>[[6, 9, 2], [5, 6, 7], [3, 2, 8]]</code> → <code>[6, 9, 2, 7, 6, 5, 3, 2, 8]</code>.</div>
<div class="err"><b>Error común:</b> buscar vecinos sin verificar límites: en la fila 0, <code>f - 1 = -1</code> lee la última fila sin dar error.</div>"""
F_M2 = [c('mat.append([0] * m)') + ' en un for (n filas)', 'Borde: ' + c('f in (0, filas-1) or c in (0, col-1)'), 'Serpiente: ' + c('range(col-1, -1, -1)') + ' en filas impares',
        'Vecinos: ' + c('0 <= f < filas and 0 <= c < col'), 'Transpuesta: ' + c('t[c][f] = mat[f][c]')]

def matrices2():
    E = []
    E.append(imprime('m10_1', 2, 'La trampa de [[0]*3]*2', 'm = [[0] * 3] * 2\nm[0][0] = 5\nprint(m)\n\nk = []\nfor f in range(2):\n    k.append([0] * 3)\nk[0][0] = 5\nprint(k)',
        ['[[5, 0, 0], [0, 0, 0]]\n[[5, 0, 0], [0, 0, 0]]', '[[5, 0, 0], [5, 0, 0]]\n[[5, 0, 0], [5, 0, 0]]', '[[5, 5, 5], [0, 0, 0]]\n[[5, 0, 0], [0, 0, 0]]', '[[5, 0, 0], [0, 0, 0]]\n[[5, 0, 0], [5, 0, 0]]'],
        ['<code>[[0] * 3] * 2</code> crea UNA fila y la pone dos veces: <code>m[0]</code> y <code>m[1]</code> son la misma lista, así que el 5 aparece en las dos.', 'Con append dentro del for, cada vuelta crea una fila nueva: solo cambia la primera.'],
        'Abre el 🧪 Interactivo: el paso a paso muestra las etiquetas de cada fila.', [['trampa'], ['crear']]))
    S3 = [[1, 7, 3, 2], [6, 2, 4, 4], [5, 7, 7, 4]]
    sp = []
    for f in range(3):
        cs = range(4) if f % 2 == 0 else range(3, -1, -1)
        sp += [[f, cc] for cc in cs]
    E.append(ex('m10_2', 2, 'Recorrido de la serpiente', '<p>Toca las celdas <b>en el orden</b> en que las recorre la serpiente: fila 0 de izquierda a derecha, fila 1 de derecha a izquierda, y así.</p>',
        [{'t': 'mtx', 'p': 'Toca en orden', 'm': S3, 'a': sp, 'ord': True, 'name': 'mat'}],
        ['Fila 0 → [1, 7, 3, 2]; fila 1 al revés → [4, 4, 2, 6]; fila 2 → [5, 7, 7, 4].'], '[1, 7, 3, 2, 4, 4, 2, 6, 5, 7, 7, 4]', 'Alterna el sentido en cada fila.', [['serp']]))
    bd = [[f, cc] for f in range(4) for cc in range(5) if f in (0, 3) or cc in (0, 4)]
    E.append(ex('m10_3', 1, 'Celdas del borde', '<p>Toca las celdas que cumplen la condición del borde.</p>' + pre('if f == 0 or f == filas - 1 or c == 0 or c == col - 1:'),
        [{'t': 'mtx', 'p': 'Toca las celdas', 'm': M, 'a': bd, 'name': 'mat'}],
        ['Primera y última fila completas, más la primera y la última columna: 14 celdas.'], '14 celdas del contorno', '', [['borde']]))
    V = [[4, 5, 6, 3], [1, 4, 6, 7], [8, 2, 3, 6], [3, 5, 4, 9], [3, 4, 5, 3]]
    vc = [[f, cc] for f in range(1, 4) for cc in range(0, 2) if not (f == 2 and cc == 0)]
    E.append(ex('m10_4', 2, 'Vecinos sin salirse', '<p>Toca los vecinos de la celda <code>(2, 0)</code> (fila 2, columna 0): las hasta 8 celdas que la rodean y que existen.</p>',
        [{'t': 'mtx', 'p': 'Toca los vecinos', 'm': V, 'a': vc, 'name': 'mat'}],
        ['Las filas van de 1 a 3 y las columnas de −1 a 1; la columna −1 no existe y la propia celda no cuenta.', 'Quedan 5 vecinos: 1, 4, 2, 3, 5 (3 de ellos impares: 1, 3, 5).'],
        'mat[1][0], mat[1][1], mat[2][1], mat[3][0] y mat[3][1]', 'En el borde izquierdo no hay columna −1.', [['vec'], ['vec']]))
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    T_ = [[A[f][cc] for f in range(3)] for cc in range(3)]
    E.append(ex('m10_5', 2, 'Arma la transpuesta', '<p>Escribe la transpuesta de ' + c('[[1, 2, 3], [4, 5, 6], [7, 8, 9]]') + ': lo que era la fila f pasa a ser la columna f.</p>',
        [{'t': 'mat', 'p': 'Completa la matriz', 'a': T_, 'l': 't ='}],
        ['La fila 0 (1, 2, 3) pasa a ser la columna 0; en general <code>t[c][f] = mat[f][c]</code>.'], c(str(T_)), '', [['rot']], play='mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nt = []\nfor c in range(3):\n    t.append([0] * 3)\nfor f in range(3):\n    for c in range(3):\n        t[c][f] = mat[f][c]\nprint(t)'))
    R_ = [[A[f][2 - cc] for f in range(3)] for cc in range(3)]
    E.append(ex('m10_6', 3, 'Rotar 90° en sentido antihorario', '<p>Rota ' + c('[[1, 2, 3], [4, 5, 6], [7, 8, 9]]') + ' 90° en sentido <b>antihorario</b> (la última columna pasa a ser la primera fila).</p>',
        [{'t': 'mat', 'p': 'Completa la matriz', 'a': R_, 'l': 'r ='}],
        ['La columna 2 (3, 6, 9) queda arriba como fila 0; la columna 0 (1, 4, 7) queda abajo.', 'Regla: <code>r[c][f] = mat[f][n - 1 - c]</code>… o, más fácil, <code>r[i][j] = mat[j][n - 1 - i]</code>.'],
        c(str(R_)), 'Gira la hoja hacia la izquierda.', [['rot'], ['rot']]))
    m1 = [[4, 2, 3], [1, 4, 1], [2, 3, 5]]; m2 = [[2, 3, 3], [1, 5, 4], [2, 1, 2]]
    co = [[1 if m1[f][cc] == m2[f][cc] else 0 for cc in range(3)] for f in range(3)]
    E.append(ex('m10_7', 1, 'Matriz de coincidencias', '<p>Escribe la matriz que tiene 1 donde ' + c('m1') + ' y ' + c('m2') + ' coinciden en valor y posición, y 0 donde no (Evaluación continua 10, 2024-2).</p>' + pre('m1 = [[4, 2, 3], [1, 4, 1], [2, 3, 5]]\nm2 = [[2, 3, 3], [1, 5, 4], [2, 1, 2]]'),
        [{'t': 'mat', 'p': 'Completa la matriz', 'a': co, 'l': 'res ='}],
        ['Se compara celda por celda: coinciden (0,2), (1,0) y (2,0).'], c(str(co)), '', [['nueva']]))
    E.append(hueco('m10_8', 1, 'Suma del borde', '<p>Completa la condición para sumar solo las celdas del borde.</p>',
        'def suma_borde(mat):\n    filas = len(mat)\n    col = len(mat[0])\n    suma = 0\n    for f in range(filas):\n        for c in range(col):\n            if f == 0 or f == ⟦0⟧ or c == 0 or c == ⟦1⟧:\n                suma = suma + mat[f][c]\n    return suma',
        [(['filas - 1', 'filas-1', 'len(mat) - 1', 'len(mat)-1'], '¿Cuál es el índice de la última fila?', 'La última fila es filas − 1 (los índices empiezan en 0).'),
         (['col - 1', 'col-1', 'len(mat[0]) - 1', 'len(mat[0])-1'], '¿Cuál es el índice de la última columna?', 'La última columna es col − 1.')],
        ['La última fila tiene índice <code>filas - 1</code> y la última columna <code>col - 1</code>.'], '', [['borde']],
        tests=mk_tests('def suma_borde(mat):\n    filas = len(mat)\n    col = len(mat[0])\n    suma = 0\n    for f in range(filas):\n        for c in range(col):\n            if f == 0 or f == filas - 1 or c == 0 or c == col - 1:\n                suma = suma + mat[f][c]\n    return suma',
                       ['print(suma_borde(' + repr(M) + '))', 'print(suma_borde([[1, 1, 1], [1, 9, 1], [1, 1, 1]]))']),
        demo=MS + '\nprint(suma_borde(mat))'))
    E.append(hueco('m10_9', 2, 'Crear y llenar con funciones', '<p>Completa: <code>dimensionar</code> crea una matriz de ceros y <code>llenar</code> pone en cada celda <code>f * 10 + c</code> (sin retornar nada).</p>',
        'def dimensionar(filas, col):\n    mat = []\n    for f in range(filas):\n        mat.⟦0⟧\n    return mat\n\ndef llenar(mat):\n    for f in range(len(mat)):\n        for c in range(⟦1⟧):\n            ⟦2⟧ = f * 10 + c',
        [(['append([0] * col)', 'append([0]*col)'], 'Cada vuelta agrega una fila nueva de col ceros.', 'Se agrega una fila: mat.append([0] * col).'),
         (['len(mat[0])', '0, len(mat[0])'], 'El for de adentro recorre columnas.', 'Las columnas se cuentan con len(mat[0]).'),
         (['mat[f][c]'], '¿Qué celda se escribe?', 'Se escribe en mat[f][c]; como la lista es mutable, no hace falta return.')],
        ['<code>append([0] * col)</code> crea una fila nueva en cada vuelta (no la misma repetida).', '<code>llenar</code> modifica la matriz que recibe: no necesita <code>return</code>.'],
        '', [['crear'], ['fmut']],
        tests=mk_tests('def dimensionar(filas, col):\n    mat = []\n    for f in range(filas):\n        mat.append([0] * col)\n    return mat\n\ndef llenar(mat):\n    for f in range(len(mat)):\n        for c in range(len(mat[0])):\n            mat[f][c] = f * 10 + c',
                       ['m = dimensionar(2, 3)\nprint(m)\nllenar(m)\nprint(m)', 'm = dimensionar(3, 2)\nllenar(m)\nm[0][0] = 99\nprint(m)']),
        demo='m = dimensionar(3, 4)\nllenar(m)\nfor fila in m:\n    print(fila)'))
    E.append(bug('m10_10', 2, 'Vecinos impares', '<p>La función cuenta los impares alrededor de <code>(fila, col)</code>. Para la celda (0, 0) de la matriz debería dar 1 (solo el 5 de al lado), pero da otro número y no sale ningún error.</p>',
        'def vecinos_impares(mat, fila, col):\n    cont = 0\n    for f in range(fila - 1, fila + 2):\n        for c in range(col - 1, col + 2):\n            if (f, c) != (fila, col) and mat[f][c] % 2 == 1:\n                cont = cont + 1\n    return cont\n\nmat = [[4, 5, 6], [2, 4, 6], [8, 3, 9]]\nprint(vecinos_impares(mat, 0, 0))',
        [5], ['No verifica que f y c estén dentro de la matriz: con −1 lee la última fila o columna', 'El range debería ser range(fila - 1, fila + 1)', 'Debería comparar con % 2 == 0', 'cont debería empezar en 1', 'Falta convertir mat[f][c] a int'],
        ['Con fila = 0, <code>f</code> toma el valor −1 y <code>mat[-1]</code> es la <b>última</b> fila: no hay error, pero cuenta el 3 y el 9 que no son vecinos.', 'Hay que agregar <code>0 &lt;= f &lt; len(mat) and 0 &lt;= c &lt; len(mat[0])</code> antes de leer <code>mat[f][c]</code>.'],
        '¿Qué valores toma f cuando fila = 0?', [['vec'], ['vec']],
        fixed='def vecinos_impares(mat, fila, col):\n    cont = 0\n    for f in range(fila - 1, fila + 2):\n        for c in range(col - 1, col + 2):\n            if 0 <= f < len(mat) and 0 <= c < len(mat[0]) and (f, c) != (fila, col) and mat[f][c] % 2 == 1:\n                cont = cont + 1\n    return cont\n\nmat = [[4, 5, 6], [2, 4, 6], [8, 3, 9]]\nprint(vecinos_impares(mat, 0, 0))'))
    E.append(arregla('m10_11', 2, 'Matriz de ceros que se repite',
        '<p><code>crear(filas, col)</code> debería devolver una matriz de ceros independiente, pero al cambiar una casilla cambian varias. <b>Arréglalo.</b></p>',
        'def crear(filas, col):\n    return [[0] * col] * filas\n',
        'def crear(filas, col):\n    mat = []\n    for f in range(filas):\n        mat.append([0] * col)\n    return mat\n',
        ['m = crear(3, 2)\nm[0][1] = 7\nprint(m)', 'm = crear(2, 4)\nm[1][0] = 1\nprint(m)'],
        ['<code>[[0] * col] * filas</code> repite la misma fila; cada fila tiene que ser una lista nueva.', 'Con un for y <code>append([0] * col)</code> se crea una fila distinta por vuelta.'],
        '', [['trampa'], ['crear']]))
    E.append(codex('m10_12', 2, 'Serpiente',
        '<p>Implementa <code>pregunta_2(mat)</code> que retorne la lista de valores en el orden de la serpiente: fila 0 de izquierda a derecha, fila 1 de derecha a izquierda, y así (Evaluación continua 10, 2024-2).</p>' +
        pre('pregunta_2([[6, 9, 2], [5, 6, 7], [3, 2, 8]])  →  [6, 9, 2, 7, 6, 5, 3, 2, 8]'),
        'def pregunta_2(mat):\n    # tu código aquí\n    return []\n',
        'def pregunta_2(mat):\n    lista = []\n    for f in range(len(mat)):\n        if f % 2 == 0:\n            for c in range(0, len(mat[0]), 1):\n                lista.append(mat[f][c])\n        else:\n            for c in range(len(mat[0]) - 1, -1, -1):\n                lista.append(mat[f][c])\n    return lista\n',
        ['print(pregunta_2([[6, 9, 2], [5, 6, 7], [3, 2, 8]]))', 'print(pregunta_2([[1, 7, 3, 2, 3, 5], [6, 2, 4, 4, 5, 7], [5, 7, 7, 4, 4, 8], [4, 9, 2, 7, 8, 6]]))', 'print(pregunta_2([[6, 9, 1, 4, 8, 2, 6], [7, 8, 1, 2, 5, 1, 8], [9, 5, 4, 7, 4, 2, 9]]))'],
        ['En las filas pares se recorre <code>range(0, col)</code>; en las impares, <code>range(col - 1, -1, -1)</code>.', 'Cada valor visitado se agrega a la lista.'],
        'f % 2 decide el sentido.', [['serp'], ['agr']], pc='mat'))
    E.append(codex('m10_13', 2, 'Matriz de coincidencias',
        '<p>Implementa <code>pregunta_1(m1, m2)</code> (matrices cuadradas del mismo orden): retorna una matriz <b>nueva</b> con 1 donde los valores coinciden en la misma posición y 0 donde no (Evaluación continua 10, 2024-2).</p>' +
        pre('pregunta_1([[4, 2, 3], [1, 4, 1], [2, 3, 5]],\n           [[2, 3, 3], [1, 5, 4], [2, 1, 2]])\n→  [[0, 0, 1], [1, 0, 0], [1, 0, 0]]'),
        'def pregunta_1(m1, m2):\n    # tu código aquí\n    return []\n',
        'def pregunta_1(m1, m2):\n    n = len(m1)\n    res = []\n    for f in range(n):\n        res.append([0] * n)\n    for f in range(n):\n        for c in range(n):\n            if m1[f][c] == m2[f][c]:\n                res[f][c] = 1\n    return res\n',
        ['print(pregunta_1([[4, 2, 3], [1, 4, 1], [2, 3, 5]], [[2, 3, 3], [1, 5, 4], [2, 1, 2]]))', 'print(pregunta_1([[4, 2, 3, 1], [4, 1, 2, 3], [5, 2, 3, 3], [1, 5, 4, 2]], [[1, 2, 3, 2], [2, 4, 3, 5], [3, 1, 3, 4], [3, 1, 5, 3]]))', 'a = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]\nr = pregunta_1(a, a)\nprint(r, r is a)'],
        ['Primero se crea la matriz resultado llena de ceros (con append, no con *).', 'Luego, celda por celda, se pone 1 donde <code>m1[f][c] == m2[f][c]</code>.'],
        'Crea, recorre y retorna.', [['crear', 'nueva'], ['rect']], names=['Ejemplo 3 × 3', 'Ejemplo 4 × 4', 'Retorna una matriz nueva'], pc='mat'))
    E.append(codex('m10_14', 2, 'Fila con mayor suma',
        '<p>Implementa <code>pregunta_4(mat)</code> que retorne el índice de la fila cuya suma es la mayor. Si hay empate, la primera (Evaluación continua 10, 2024-2).</p>' +
        pre('pregunta_4([[14, 38, 1, 3, 14], [44, 3, 28, 27, 20], [44, 19, 2, 46, 23], [34, 14, 2, 20, 21]])  →  2'),
        'def pregunta_4(mat):\n    # tu código aquí\n    return 0\n',
        'def pregunta_4(mat):\n    imax = 0\n    for f in range(len(mat)):\n        if sum(mat[f]) > sum(mat[imax]):\n            imax = f\n    return imax\n',
        ['print(pregunta_4([[14, 38, 1, 3, 14], [44, 3, 28, 27, 20], [44, 19, 2, 46, 23], [34, 14, 2, 20, 21]]))', 'print(pregunta_4([[39, 36, 5, 19, 18, 43, 38, 8], [37, 34, 49, 39, 32, 43, 37, 3], [33, 6, 13, 5, 8, 44, 7, 9], [19, 8, 10, 14, 3, 42, 10, 50]]))',
         'print(pregunta_4([[49, 21, 1, 6], [21, 27, 41, 41], [40, 34, 14, 41], [20, 20, 40, 24], [19, 39, 48, 8], [1, 8, 25, 10], [36, 19, 10, 28], [46, 50, 17, 34]]))', 'print(pregunta_4([[1, 1], [2, 0], [0, 2]]))'],
        ['<code>sum(mat[f])</code> suma la fila f completa.', 'Se guarda el índice del mayor; con <code>&gt;</code> estricto, en un empate se queda el primero.'],
        'Guarda el índice, no la suma.', [['recf', 'maxmin'], ['maxmin']], pc='mat'))
    E.append(codex('m10_15', 2, 'Filas impares y columnas pares',
        '<p>Implementa <code>pregunta_2(mat)</code>: retorna una matriz nueva con los valores donde se cruzan las filas «impares» y las columnas «pares», <b>contando desde 1</b> como en el enunciado del laboratorio (es decir, filas de índice 0, 2, 4… y columnas de índice 1, 3, 5…) (Tarea de Laboratorio 9).</p>' +
        pre('pregunta_2([[4, 56, 9, 12], [15, 18, 21, 24], [27, 34, 33, 35], [18, 21, 45, 65], [23, 54, 17, 23]])\n→  [[56, 12], [34, 35], [54, 23]]'),
        'def pregunta_2(mat):\n    # tu código aquí\n    return []\n',
        'def pregunta_2(mat):\n    res = []\n    for f in range(0, len(mat), 2):\n        fila = []\n        for c in range(1, len(mat[0]), 2):\n            fila.append(mat[f][c])\n        res.append(fila)\n    return res\n',
        ['print(pregunta_2([[2, 71], [34, 9], [10, 15], [34, 21]]))', 'print(pregunta_2([[4, 56, 9, 12], [15, 18, 21, 24], [27, 34, 33, 35], [18, 21, 45, 65], [23, 54, 17, 23]]))', 'print(pregunta_2([[20, 4, 60, 81, 2, 40, 63], [50, 3, 9, 82, 1, 93, 9]]))'],
        ['«Primera fila» = índice 0, así que las filas impares del enunciado son las de índice par: <code>range(0, filas, 2)</code>.', 'Las columnas pares del enunciado son las de índice impar: <code>range(1, col, 2)</code>. Con cortes: <code>mat[f][1::2]</code>.'],
        'Cuidado: el enunciado cuenta desde 1.', [['rect'], ['slom']], pc='mat'))
    tools = [{'w': 'mtx', 't': 'Recorridos de práctica', 'p': 'Serpiente, borde, diagonal y vecinos (en «Vecinos», toca otra celda para cambiar el centro).', 'o': {'m': M, 'modes': ['serp', 'borde', 'diag', 'vec', 'filas', 'cols']}},
             paso('m = [[0] * 3] * 2\nm[0][0] = 5\n\nk = []\nfor f in range(2):\n    k.append([0] * 3)\nk[0][0] = 5\nprint(m)\nprint(k)', 'Paso a paso: [[0]*3]*2 vs. append', 'En <code>m</code> las dos filas tienen la <b>misma</b> etiqueta: son la misma lista. En <code>k</code> cada fila es distinta.')]
    return {'id': 'm10', 'name': 'Sem. 10 · Matrices II: crear, funciones y recorridos', 'teo': T_M2, 'form': F_M2, 'lesson': L_M2, 'ex': E, 'tools': tools}

T_MIX = """
<p>La cuarta pregunta de la práctica mezcla los tres temas. Suelen ser de este tipo:</p>
<ul><li><b>Cadena → lista:</b> <code>frase.lower().split()</code> y luego filtrar o contar palabras.</li>
<li><b>Lista → matriz:</b> repartir una lista en filas (el elemento <code>k</code> va a la fila <code>k // m</code>, columna <code>k % m</code>).</li>
<li><b>Matriz → lista:</b> resumir cada fila o columna (máximo, suma, promedio) en una lista.</li>
<li><b>Matriz de cadenas:</b> cada celda es una letra; <code>"".join(mat[f])</code> une una fila en una palabra.</li></ul>
<p>Estrategia para la práctica: lee las firmas (<code>def pregunta_N(…)</code>), prueba primero con el ejemplo del enunciado, usa <code>return</code> (nunca <code>input</code> ni <code>print</code> dentro de la función) y <b>no modifiques</b> las listas que recibes si el enunciado no lo pide (trabaja con una copia o arma una nueva).</p>
"""
L_MIX = """<h3>Idea central</h3><p>Divide el problema: ¿qué estructura recibo?, ¿cuál retorno?, ¿qué recorrido convierte una en otra?</p>
<h3>Conceptos clave</h3><ul><li><code>split()</code> pasa de cadena a lista.</li><li><code>k // m</code> y <code>k % m</code> pasan de posición lineal a (fila, columna).</li><li>Retorna; no imprimas.</li></ul>
<div class="ej"><b>Ejemplo:</b> <code>[1, 2, 3, 4, 5, 6]</code> en 2 filas de 3 → <code>[[1, 2, 3], [4, 5, 6]]</code>.</div>
<div class="err"><b>Error común:</b> dejar un <code>print</code> en vez de <code>return</code>: el autocalificador recibe <code>None</code>.</div>"""
F_MIX = [c('frase.lower().split()'), 'Posición k → fila ' + c('k // m') + ', columna ' + c('k % m'), c('"".join(lista_de_letras)'), 'No modificar la entrada: ' + c('copia = l[:]')]

def mix():
    E = []
    E.append(opc('x_1', 1, 'return vs print', pre('def doble(x):\n    print(x * 2)\n\nr = doble(4)\nprint(r)') + '<p>¿Qué imprime?</p>',
        ['8 y luego None', '8 y luego 8', 'Solo 8', 'Solo None', 'Da error porque la función no tiene return'],
        ['Dentro de la función se imprime 8, pero no hay <code>return</code>: la función devuelve <code>None</code>.', 'Por eso en la práctica, si imprimes en vez de retornar, las pruebas reciben <code>None</code>.'],
        '', [['retfor'], []], p='Salida', play='def doble(x):\n    print(x * 2)\n\nr = doble(4)\nprint(r)'))
    E.append(hueco('x_2', 2, 'De lista a matriz', '<p>Completa para repartir <code>lista</code> en una matriz de <code>m</code> columnas (fila por fila).</p>',
        'def a_matriz(lista, m):\n    mat = []\n    for k in range(len(lista)):\n        if k % m == 0:\n            mat.append(⟦0⟧)\n        mat[⟦1⟧].append(lista[k])\n    return mat',
        [(['[]'], 'Cuando empieza una fila nueva, ¿qué agregas?', 'Se agrega una fila vacía [] y luego se llena.'),
         (['k // m', '-1', 'len(mat) - 1', 'len(mat)-1'], '¿En qué fila cae el elemento k?', 'El elemento k va a la fila k // m (también sirve la última fila, -1).')],
        ['Cada <code>m</code> elementos empieza una fila nueva (<code>k % m == 0</code>).', 'El elemento <code>k</code> va a la fila <code>k // m</code>.'], '', [['crear'], []],
        tests=mk_tests('def a_matriz(lista, m):\n    mat = []\n    for k in range(len(lista)):\n        if k % m == 0:\n            mat.append([])\n        mat[k // m].append(lista[k])\n    return mat',
                       ['print(a_matriz([1, 2, 3, 4, 5, 6], 3))', 'print(a_matriz([1, 2, 3, 4, 5, 6], 2))', 'print(a_matriz([7], 1))']),
        demo='print(a_matriz(list(range(12)), 4))'))
    E.append(bug('x_3', 2, 'No modifiques la entrada', '<p>La función debe retornar las palabras de <code>palabras</code> ordenadas, sin cambiar la lista original. Pero la original también queda ordenada.</p>',
        'def ordenadas(palabras):\n    res = palabras\n    res.sort()\n    return res\n\nl = ["pera", "mango", "kiwi"]\nr = ordenadas(l)\nprint(r)\nprint(l)',
        [2], ['res = palabras no copia: res y palabras son la misma lista y sort la cambia', 'sort() devuelve una lista nueva', 'Falta un for para ordenar', 'return res debería ser return palabras', 'Las cadenas no se pueden ordenar'],
        ['<code>res = palabras</code> solo crea otro nombre para la misma lista; <code>sort()</code> la ordena «en el sitio».', 'Solución: <code>res = palabras[:]</code> o directamente <code>return sorted(palabras)</code>.'],
        '¿Cuántas listas hay en memoria?', [['alias'], ['alias']],
        fixed='def ordenadas(palabras):\n    res = palabras[:]\n    res.sort()\n    return res\n\nl = ["pera", "mango", "kiwi"]\nr = ordenadas(l)\nprint(r)\nprint(l)'))
    E.append(codex('x_4', 2, 'Palabras largas sin repetir',
        '<p>Implementa <code>pregunta_4(frase, n)</code>: retorna la lista de palabras de la frase (en minúsculas) con <b>más de</b> <code>n</code> letras, sin repetir y en el orden en que aparecen.</p>' +
        pre('pregunta_4("El Principito se sorprendio al no ver a nadie pero a NADIE", 4)\n→  ["principito", "sorprendio", "nadie"]'),
        'def pregunta_4(frase, n):\n    # tu código aquí\n    return []\n',
        'def pregunta_4(frase, n):\n    res = []\n    for p in frase.lower().split():\n        if len(p) > n and p not in res:\n            res.append(p)\n    return res\n',
        ['print(pregunta_4("El Principito se sorprendio al no ver a nadie pero a NADIE", 4))', 'print(pregunta_4("Lo interesante del desierto es que esconde un pozo", 6))', 'print(pregunta_4("a b c", 3))'],
        ['<code>frase.lower().split()</code> da la lista de palabras en minúsculas.', 'Se agrega cada palabra larga que todavía no esté en el resultado.'],
        'split + filtro + not in.', [['mets'], ['bus']], hidden=['print(pregunta_4("Es un helicoptero o es un avion o es un cohete", 2))'], pc='mix'))
    E.append(codex('x_5', 2, 'Máximo de cada fila con su nombre',
        '<p>Implementa <code>pregunta_3(nombres, notas)</code>: <code>notas</code> es una matriz (fila f = notas de <code>nombres[f]</code>). Retorna una lista de cadenas <code>"nombre: mayor"</code> con la mayor nota de cada estudiante.</p>' +
        pre('pregunta_3(["Ana", "Luis"], [[12, 18, 15], [9, 11, 14]])\n→  ["Ana: 18", "Luis: 14"]'),
        'def pregunta_3(nombres, notas):\n    # tu código aquí\n    return []\n',
        'def pregunta_3(nombres, notas):\n    res = []\n    for f in range(len(notas)):\n        mayor = notas[f][0]\n        for c in range(len(notas[0])):\n            if notas[f][c] > mayor:\n                mayor = notas[f][c]\n        res.append(nombres[f] + ": " + str(mayor))\n    return res\n',
        ['print(pregunta_3(["Ana", "Luis"], [[12, 18, 15], [9, 11, 14]]))', 'print(pregunta_3(["A", "B", "C"], [[1], [5], [3]]))', 'print(pregunta_3(["Pedro"], [[60, 65, 70, 20]]))'],
        ['Para cada fila se busca su mayor (o <code>max(notas[f])</code>).', 'Se arma el texto con <code>nombres[f] + ": " + str(mayor)</code> y se agrega a la lista.'],
        'Listas paralelas + mayor de cada fila.', [['par', 'recf'], ['maxmin']], pc='mix'))
    E.append(codex('x_6', 3, 'Palabras escondidas en las filas',
        '<p>Implementa <code>pregunta_4(sopa, palabra)</code>: <code>sopa</code> es una matriz de letras. Retorna la lista de índices de las filas que, unidas como texto, contienen <code>palabra</code> (sin distinguir mayúsculas).</p>' +
        pre('sopa = [["x", "s", "o", "l"],\n        ["L", "u", "n", "a"],\n        ["m", "a", "r", "z"]]\npregunta_4(sopa, "luna")  →  [1]\npregunta_4(sopa, "ar")    →  [2]'),
        'def pregunta_4(sopa, palabra):\n    # tu código aquí\n    return []\n',
        'def pregunta_4(sopa, palabra):\n    res = []\n    for f in range(len(sopa)):\n        texto = ""\n        for letra in sopa[f]:\n            texto = texto + letra\n        if palabra.lower() in texto.lower():\n            res.append(f)\n    return res\n',
        ['s = [["x", "s", "o", "l"], ["L", "u", "n", "a"], ["m", "a", "r", "z"]]\nprint(pregunta_4(s, "luna"))', 's = [["x", "s", "o", "l"], ["L", "u", "n", "a"], ["m", "a", "r", "z"]]\nprint(pregunta_4(s, "ar"))', 's = [["a", "b"], ["b", "a"], ["a", "b"]]\nprint(pregunta_4(s, "AB"))', 's = [["a", "b"], ["c", "d"]]\nprint(pregunta_4(s, "z"))'],
        ['Cada fila se une en un texto (con un for o con <code>"".join(sopa[f])</code>).', 'Se compara en minúsculas con <code>in</code> y se guarda el índice de la fila.'],
        'Une las letras de cada fila.', [['rect', 'acum'], ['mets']], pc='mix'))
    E.append(codex('x_7', 3, 'Apilar matrices',
        '<p>Implementa <code>pregunta_4(mat1, mat2)</code> que retorne una matriz <b>nueva</b> con las filas de <code>mat1</code> y debajo las de <code>mat2</code>. Si no tienen la misma cantidad de columnas, retorna <code>mat1</code>. No modifiques las de entrada.</p>' +
        pre('pregunta_4([[7, 0], [0, 7]], [[1, 2]])  →  [[7, 0], [0, 7], [1, 2]]'),
        'def pregunta_4(mat1, mat2):\n    # tu código aquí\n    return mat1\n',
        'def pregunta_4(mat1, mat2):\n    if len(mat1[0]) != len(mat2[0]):\n        return mat1\n    res = []\n    for fila in mat1:\n        res.append(fila[:])\n    for fila in mat2:\n        res.append(fila[:])\n    return res\n',
        ['print(pregunta_4([[7, 0], [0, 7]], [[1, 2]]))', 'print(pregunta_4([[3], [5]], [[6], [3], [5]]))', 'print(pregunta_4([[1, 2]], [[1, 2, 3]]))', 'a = [[1, 1]]\nb = [[2, 2]]\nr = pregunta_4(a, b)\nr[0][0] = 9\nprint(a, r)'],
        ['Primero se comparan las columnas (<code>len(mat[0])</code>).', 'Se copia cada fila con <code>fila[:]</code> para que el resultado no comparta filas con las de entrada.'],
        'Copia fila por fila.', [['dims'], ['alias', 'nueva']], names=['Ejemplo', 'Una columna', 'Columnas distintas', 'No comparte filas con la entrada'], pc='mix'))
    return {'id': 'mx', 'name': 'Sem. 9–10 · Mix: cadenas, listas y matrices', 'teo': T_MIX, 'form': F_MIX, 'lesson': L_MIX, 'ex': E}

def simex_pc3():
    """Problemas extra del simulacro (tipo práctica)."""
    S = []
    S.append(codex('sx_borde', 2, 'Borde aleatorio',
        '<p>Implementa <code>pregunta_3(filas, col)</code>: retorna una matriz de <code>filas × col</code> con valores al azar entre 20 y 40 (con <code>randint</code>) <b>solo en el borde</b> y 0 en el resto (Evaluación continua 10, 2024-2). Puedes importar <code>randint</code>.</p>',
        'from random import randint\n\ndef pregunta_3(filas, col):\n    # tu código aquí\n    return []\n',
        'from random import randint\n\ndef pregunta_3(filas, col):\n    mat = []\n    for f in range(filas):\n        mat.append([0] * col)\n    for f in range(filas):\n        for c in range(col):\n            if f == 0 or f == filas - 1 or c == 0 or c == col - 1:\n                mat[f][c] = randint(20, 40)\n    return mat\n',
        ['m = pregunta_3(5, 8)\nprint(len(m), len(m[0]))', 'm = pregunta_3(5, 8)\nprint(all(20 <= m[f][c] <= 40 for f in range(5) for c in range(8) if f in (0, 4) or c in (0, 7)))',
         'm = pregunta_3(4, 5)\nprint(all(m[f][c] == 0 for f in range(1, 3) for c in range(1, 4)))', 'm = pregunta_3(3, 3)\nm[0][0] = -1\nprint(m[1][0] != -1)'],
        ['Primero la matriz de ceros (con append); luego solo las celdas del borde reciben <code>randint(20, 40)</code>.'],
        '', [['crear', 'borde']], names=['Tamaño 5 × 8', 'Borde entre 20 y 40', 'Interior en 0', 'Filas independientes'], pc='mat'))
    S.append(codex('sx_maxfc', 2, 'Mínimos de filas y columnas',
        '<p>Implementa <code>pregunta_1(mat)</code> que retorne <b>dos listas</b>: los mínimos de cada fila y los mínimos de cada columna.</p>' +
        pre('pregunta_1([[3, 8, 7], [2, 5, 1], [6, 9, 4]])  →  ([3, 1, 4], [2, 5, 1])'),
        'def pregunta_1(mat):\n    # tu código aquí\n    return [], []\n',
        'def pregunta_1(mat):\n    filas = []\n    for f in range(len(mat)):\n        filas.append(min(mat[f]))\n    cols = []\n    for c in range(len(mat[0])):\n        m = mat[0][c]\n        for f in range(len(mat)):\n            if mat[f][c] < m:\n                m = mat[f][c]\n        cols.append(m)\n    return filas, cols\n',
        ['print(pregunta_1([[3, 8, 7], [2, 5, 1], [6, 9, 4]]))', 'print(pregunta_1([[10, 20], [30, 40], [15, 25]]))', 'print(pregunta_1([[-3, -8, -7], [-2, -5, -1]]))'],
        ['Mínimo de la fila f: <code>min(mat[f])</code>.', 'Para cada columna se recorren las filas desde <code>mat[0][c]</code>. Se retornan las dos listas separadas por coma (una tupla).'],
        '', [['recf'], ['recc']], pc='mat'))
    S.append(codex('sx_vocal', 2, 'Palabras con todas las vocales',
        '<p>Implementa <code>pregunta_1(frase)</code>: retorna la lista de palabras (en minúsculas) que contienen las <b>cinco</b> vocales al menos una vez.</p>' + pre('pregunta_1("Murcielago y euforia van a la escuela")  →  ["murcielago", "euforia"]'),
        'def pregunta_1(frase):\n    # tu código aquí\n    return []\n',
        'def pregunta_1(frase):\n    res = []\n    for p in frase.lower().split():\n        tiene = True\n        for v in "aeiou":\n            if v not in p:\n                tiene = False\n        if tiene:\n            res.append(p)\n    return res\n',
        ['print(pregunta_1("Murcielago y euforia van a la escuela"))', 'print(pregunta_1("hola mundo"))', 'print(pregunta_1("ESQUIVALO ESQUIVALO"))'],
        ['Para cada palabra se revisa que cada vocal esté (<code>v in p</code>).', 'Si falta alguna, la bandera queda en False.'],
        '', [['mets'], ['bus']], pc='mix'))
    return S
