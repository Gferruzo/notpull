"""Programación I · Sem. 9: cadenas, listas y cortes."""
from p1_lib import *

CONCEPTS = {
 'inmut': {'n': 'Cadenas inmutables', 'f': c("s[0] = 'H'") + ' → TypeError', 'x': 'Para «cambiar» una cadena se crea otra: s = s.upper(), s = s[1:] + s[0].', 'home': 'c9'},
 'idx': {'n': 'Índices', 'f': c('s[0]') + ' … ' + c('s[len(s)-1]') + ' = ' + c('s[-1]'), 'x': 'Empiezan en 0; el último es len − 1 o −1.', 'home': 'c9'},
 'recs': {'n': 'Recorrer una cadena', 'f': c('for letra in s:') + ' · ' + c('for i in range(len(s)):'), 'x': 'El primero da cada letra; el segundo, cada posición (sirve si necesitas el vecino o el índice).', 'home': 'c9'},
 'mets': {'n': 'Métodos de cadena', 'f': c('lower() upper() split() strip() replace() count() find()'), 'x': 'Devuelven una cadena (o lista) nueva: hay que guardarla.', 'home': 'c9'},
 'tipos': {'n': 'Tipo de carácter', 'f': c('isupper() islower() isalpha() isdigit()'), 'x': 'Devuelven True o False para una letra o cadena.', 'home': 'c9'},
 'acum': {'n': 'Acumulador / contador', 'f': c('cont = 0') + ' … ' + c('cont = cont + 1'), 'x': 'Se inicia antes del bucle y se actualiza dentro.', 'home': 'c9'},
 'retfor': {'n': 'return dentro de un for', 'f': c('return') + ' termina la función', 'x': 'Un return en la primera vuelta corta el bucle: el «sí» va después del for.', 'home': 'c9'},
 'mut': {'n': 'Listas mutables', 'f': c('l[0] = 5') + ' sí funciona', 'x': 'Los métodos append, insert, remove, pop y sort cambian la misma lista.', 'home': 'l9'},
 'agr': {'n': 'Agregar', 'f': c('l.append(x)') + ' · ' + c('l.insert(i, x)'), 'x': 'append al final; insert en la posición i (lo demás se corre).', 'home': 'l9'},
 'bus': {'n': 'Buscar', 'f': c('x in l') + ' · ' + c('l.index(x)'), 'x': 'in da True/False; index da la primera posición y lanza ValueError si no está.', 'home': 'l9'},
 'bor': {'n': 'Borrar', 'f': c('del l[i]') + ' · ' + c('l.remove(x)') + ' · ' + c('l.pop(i)'), 'x': 'del por posición o porción; remove la primera vez que aparece x; pop quita y devuelve (por defecto el último).', 'home': 'l9'},
 'alias': {'n': '= no copia', 'f': c('b = a') + ' → mismo objeto · ' + c('a[:]') + ', ' + c('a.copy()') + ' → copia', 'x': 'Si cambias la lista por un nombre, se ve por el otro.', 'home': 'l9'},
 'maxmin': {'n': 'Mayor y menor a mano', 'f': c('mayor = l[0]') + ' y comparar con cada elemento', 'x': 'Empezar en l[0] (no en 0) funciona aunque haya negativos.', 'home': 'l9'},
 'par': {'n': 'Listas paralelas', 'f': c('nombres[i]') + ' ↔ ' + c('notas[i]'), 'x': 'La misma posición i relaciona los datos de las dos listas.', 'home': 'l9'},
 'rango': {'n': 'range y vecinos', 'f': c('range(len(l) - 1)') + ' para usar l[i + 1]', 'x': 'Si usas el siguiente, el bucle termina una posición antes.', 'home': 'l9'},
 'sl': {'n': 'Corte (slice)', 'f': c('l[inicio:fin:paso]'), 'x': 'Toma desde inicio hasta fin − 1 (el fin no se incluye), avanzando de paso en paso.', 'home': 'k9'},
 'slom': {'n': 'Valores omitidos', 'f': c('l[:3]') + ' · ' + c('l[2:]') + ' · ' + c('l[::2]'), 'x': 'Sin inicio = desde el borde; sin fin = hasta el otro borde; sin paso = 1.', 'home': 'k9'},
 'slneg': {'n': 'Paso negativo', 'f': c('l[::-1]') + ' invierte', 'x': 'Con paso negativo se recorre de derecha a izquierda: inicio debe ser mayor que fin.', 'home': 'k9'},
 'slerr': {'n': 'Cortes fuera de rango', 'f': c('l[2:100]') + ' no da error · ' + c('l[100]') + ' sí', 'x': 'Un corte se ajusta al tamaño; un índice suelto fuera de rango lanza IndexError.', 'home': 'k9'},
}

T_CAD = """
<p>Una <strong>cadena</strong> (<code>str</code>) es una secuencia de caracteres. Cada carácter tiene un <strong>índice</strong>: el primero es <code>s[0]</code> y el último <code>s[len(s) - 1]</code>, que también se escribe <code>s[-1]</code>. Las cadenas son <strong>inmutables</strong>: <code>s[0] = "H"</code> da <code>TypeError</code>. Para «cambiarla» se crea otra y se vuelve a guardar: <code>s = s.upper()</code>.</p>
<p>Hay dos formas de recorrerla: <code>for letra in s:</code> (te da cada carácter) y <code>for i in range(len(s)):</code> (te da cada posición; úsala si necesitas el índice o el carácter vecino <code>s[i - 1]</code>, <code>s[i + 1]</code>).</p>
<p>Métodos que más se usan (todos devuelven algo <em>nuevo</em>):</p>
<ul><li><code>lower()</code>, <code>upper()</code>: todo en minúsculas o mayúsculas. Útil para no distinguir entre <code>"A"</code> y <code>"a"</code>.</li>
<li><code>split()</code>: corta por espacios y devuelve una <strong>lista</strong> de palabras. <code>strip()</code> quita espacios de los bordes.</li>
<li><code>count(x)</code>, <code>find(x)</code> (posición o −1), <code>replace(a, b)</code>, <code>x in s</code> (¿está la subcadena?).</li>
<li><code>isupper()</code>, <code>islower()</code>, <code>isalpha()</code>, <code>isdigit()</code>: preguntan por el tipo de carácter.</li></ul>
<p>Patrones típicos de la práctica: <b>contar</b> (contador que empieza en 0), <b>construir</b> una cadena nueva (<code>nueva = ""</code> y luego <code>nueva = nueva + letra</code>), <b>rotar</b> con cortes (<code>s = s[1:] + s[0]</code>) y <b>detectar el inicio de cada palabra</b> sin <code>split</code>: un carácter es inicio si es el primero o si el anterior es un espacio.</p>
"""
L_CAD = """<h3>Idea central</h3><p>Casi todo problema de cadenas es «recorrer y decidir»: miras cada carácter, preguntas algo (¿es vocal?, ¿es mayúscula?, ¿es inicio de palabra?) y cuentas o construyes.</p>
<h3>Conceptos clave</h3><ul><li>Inmutable: se crea otra cadena, no se modifica.</li><li>Pasa todo a minúsculas antes de comparar si no importa la diferencia.</li><li>El «sí» de una búsqueda va <b>después</b> del for; dentro solo el «no».</li></ul>
<div class="ej"><b>Ejemplo:</b> «¿se puede formar <i>gramo</i> con las letras de la frase?»: recorres <i>gramo</i>; si una letra no está en la frase, retornas «No»; si terminas el for, retornas «Sí».</div>
<div class="err"><b>Error común:</b> poner el <code>return "Sí"</code> dentro del for: la función decide con la primera letra.</div>"""
F_CAD = [c('s[0]') + ' primero · ' + c('s[-1]') + ' último', c('for letra in s:') + ' · ' + c('for i in range(len(s)):'),
         c('s.lower()') + ', ' + c('s.split()') + ' → lista de palabras', c('letra in "aeiou"') + ' → True/False',
         'Inicio de palabra: ' + c('i == 0 or s[i-1] == " "'), 'Rotar: ' + c('s = s[1:] + s[0]')]

def cadenas():
    E = []
    E.append(opc('c9_1', 1, 'Cadenas inmutables', pre('s = "hola"\ns[0] = "H"\nprint(s)') + '<p>¿Qué pasa al ejecutarlo?</p>',
        ['Da TypeError: las cadenas no se pueden modificar por índice', 'Imprime Hola', 'Imprime hola', 'Imprime Hhola', 'Da IndexError porque el índice 0 no existe'],
        ['Las cadenas son <b>inmutables</b>: no se puede asignar a <code>s[0]</code>.', 'Para obtener «Hola» se crea otra cadena: <code>s = "H" + s[1:]</code> o <code>s = s.capitalize()</code>.'],
        'Piensa si una cadena se puede cambiar por dentro.', [['inmut'], ['inmut']]))
    E.append(imprime('c9_2', 1, 'Rotaciones', 'frase = "UTEC"\nfor i in range(3):\n    frase = frase[1:] + frase[0]\nprint(frase)',
        ['ECUT', 'TECU', 'UTEC', 'CETU'],
        ['Cada vuelta pasa la primera letra al final: UTEC → TECU → ECUT → CUTE.', 'El print está fuera del for: solo se imprime el resultado final.'],
        'Haz las tres rotaciones a mano.', [['sl'], []]))
    E.append(imprime('c9_3', 2, 'Contar tipos de caracteres',
        'cadena = "Hola, Mundo!"\nmay = 0\nmin_ = 0\notros = 0\nfor ch in cadena:\n    if ch.isupper():\n        may = may + 1\n    elif ch.islower():\n        min_ = min_ + 1\n    else:\n        otros = otros + 1\nprint(may, min_, otros)',
        ['2 7 1', '2 8 2', '1 7 4', '2 10 0'],
        ['Mayúsculas: H y M (2). Minúsculas: o, l, a, u, n, d, o (7).', 'Otros: la coma, el espacio y el signo «!» (3). El espacio también cuenta como «no letra».'],
        'El espacio y los signos van a «otros».', [['tipos', 'acum'], ['tipos']]))
    E.append(hueco('c9_4', 1, 'Contar vocales', '<p>Completa la función para que cuente las vocales de un texto, sin importar si están en mayúscula o minúscula.</p>',
        'def contar_vocales(texto):\n    cont = 0\n    for letra in ⟦0⟧:\n        if letra in ⟦1⟧:\n            cont = cont + 1\n    return ⟦2⟧',
        [(['texto.lower()'], 'Para no distinguir A de a, recorre el texto ya pasado a minúsculas.', 'Si recorres texto tal cual, las vocales en mayúscula no se cuentan.'),
         (['"aeiou"'], '¿Contra qué cadena comparas cada letra?', 'Debe ser la cadena con las cinco vocales en minúscula: "aeiou".'),
         (['cont'], '¿Qué variable guardó la cuenta?', 'Se retorna el contador, no la letra ni el texto.')],
        ['Recorres <code>texto.lower()</code> para tratar igual mayúsculas y minúsculas.', 'Cada letra que esté en <code>"aeiou"</code> suma 1 al contador.', 'Al terminar el for, retornas el contador.'],
        'Contador que empieza en 0 y suma 1 por vocal.', [['mets'], ['acum'], ['acum']],
        tests=mk_tests('def contar_vocales(texto):\n    cont = 0\n    for letra in texto.lower():\n        if letra in "aeiou":\n            cont = cont + 1\n    return cont',
                       ['print(contar_vocales("Hola Mundo"))', 'print(contar_vocales("UTEC"))', 'print(contar_vocales("rtx"))']),
        demo='print(contar_vocales("Programacion en Python"))'))
    E.append(bug('c9_5', 2, '¿Se puede formar la palabra?', '<p>La función debe decir si con las letras de la frase se puede formar la palabra (cada letra se puede usar varias veces). Con «sonido» debería responder «No se puede…», porque la frase no tiene la letra i.</p>',
        'def palabras(frase, palabra):\n    frase = frase.lower()\n    palabra = palabra.lower()\n    for letra in palabra:\n        if letra not in frase:\n            return "No se puede formar la palabra"\n        return "Se puede formar la palabra"\n\nprint(palabras("Hablas como las personas grandes", "sonido"))',
        [7], ['El return «Se puede…» está dentro del for: la función decide con la primera letra', 'Falta convertir la palabra a minúsculas', 'not in no funciona con cadenas, solo con listas', 'lower() no cambia frase porque las cadenas son inmutables', 'El for debería recorrer frase, no palabra'],
        ['Con «sonido», la primera letra <code>s</code> sí está en la frase, así que no entra al if… y en esa misma vuelta llega al <code>return "Se puede…"</code>.', 'Ese return debe ir <b>después</b> del for (sin sangría extra): solo si ninguna letra falló se puede formar.'],
        'Mira qué pasa en la primera vuelta del for.', [['retfor'], ['retfor']],
        fixed='def palabras(frase, palabra):\n    frase = frase.lower()\n    palabra = palabra.lower()\n    for letra in palabra:\n        if letra not in frase:\n            return "No se puede formar la palabra"\n    return "Se puede formar la palabra"\n\nprint(palabras("Hablas como las personas grandes", "sonido"))'))
    E.append(codex('c9_6', 2, 'Siglas sin split',
        '<p>Implementa <code>pregunta_1(nombre)</code>: <code>nombre</code> tiene una o más palabras en minúsculas separadas por <b>un</b> espacio. Retorna las iniciales en mayúscula, un guion y la cantidad de palabras. <b>No uses split()</b>: detecta el inicio de cada palabra recorriendo la cadena.</p>' +
        pre('pregunta_1("laboratorio de quimica")  →  "LDQ-3"\npregunta_1("python")                  →  "P-1"'),
        'def pregunta_1(nombre):\n    # tu código aquí\n    return ""\n',
        'def pregunta_1(nombre):\n    iniciales = ""\n    for i in range(len(nombre)):\n        if i == 0 or nombre[i - 1] == " ":\n            iniciales = iniciales + nombre[i].upper()\n    return iniciales + "-" + str(len(iniciales))\n',
        ['print(pregunta_1("laboratorio de quimica"))', 'print(pregunta_1("python"))', 'print(pregunta_1("a b c d"))'],
        ['Un carácter es inicio de palabra si es el primero (<code>i == 0</code>) o si el anterior es un espacio.', 'Cada inicio se agrega en mayúscula; la cantidad de palabras es la cantidad de iniciales.'],
        'Necesitas el índice para mirar el carácter anterior.', [['recs'], ['acum']],
        hidden=['print(pregunta_1("hola mundo cruel"))'], pc='str'))
    E.append(codex('c9_7', 2, 'Rotaciones antihorarias',
        '<p>Implementa <code>rotaciones(frase, n)</code> que aplique <code>n</code> rotaciones: en cada una, el primer carácter pasa al final (Lab 9A, ejercicio 6).</p>' +
        pre('rotaciones("Domenica", 4)  →  "nicaDome"\nrotaciones("Cusco", 2)     →  "scoCu"\nrotaciones("UTEC", 3)      →  "CUTE"'),
        'def rotaciones(frase, n):\n    # tu código aquí\n    return frase\n',
        'def rotaciones(frase, n):\n    n = n % len(frase)\n    for i in range(n):\n        frase = frase[1:] + frase[0]\n    return frase\n',
        ['print(rotaciones("Domenica", 4))', 'print(rotaciones("Cusco", 2))', 'print(rotaciones("Que calor!", 6))', 'print(rotaciones("UTEC", 7))'],
        ['Cada rotación es <code>frase = frase[1:] + frase[0]</code>.', 'Con <code>n % len(frase)</code> evitas vueltas de más: rotar «UTEC» 7 veces es lo mismo que 3.'],
        'Cortes: todo menos el primero, más el primero.', [['sl'], []], pc='str'))
    E.append(codex('c9_8', 2, 'Suma de dígitos únicos',
        '<p>Implementa <code>pregunta_4(texto)</code> que sume los dígitos que aparecen en el texto, <b>contando cada dígito una sola vez</b> aunque se repita (Tarea de Laboratorio 7).</p>' +
        pre('pregunta_4("El anho es 2024 y tengo 23 anhos")  →  9   (2 + 0 + 4 + 3)\npregunta_4("Mi numero es 777 y naci en 1999")   →  17  (7 + 1 + 9)'),
        'def pregunta_4(texto):\n    # tu código aquí\n    return 0\n',
        'def pregunta_4(texto):\n    vistos = ""\n    suma = 0\n    for ch in texto:\n        if ch.isdigit() and ch not in vistos:\n            vistos = vistos + ch\n            suma = suma + int(ch)\n    return suma\n',
        ['print(pregunta_4("El anho es 2024 y tengo 23 anhos"))', 'print(pregunta_4("Mi numero de la suerte es 777 y naci en 1999"))', 'print(pregunta_4("El costo es 1234 y el codigo es 5678"))', 'print(pregunta_4("sin numeros"))'],
        ['Recorres el texto y te quedas con los caracteres que cumplen <code>isdigit()</code>.', 'Guardas los ya sumados (en una cadena o lista) para no repetirlos; <code>int(ch)</code> convierte el dígito a número.'],
        'Lleva registro de los dígitos que ya sumaste.', [['tipos'], ['acum']], pc='str'))
    E.append(arregla('c9_9', 3, 'Autocorrector de preguntas',
        '<p>Una oración en minúsculas es pregunta si contiene «what do» o «why did». Si lo es y no termina en «?», se le agrega; si ya termina en «?», se retorna «Pregunta correcta»; si no es pregunta, «No es pregunta» (Tarea de Laboratorio 7). El código tiene un error: con «there is a statement» responde como si fuera pregunta. <b>Arréglalo.</b></p>',
        'def pregunta_2(oracion):\n    if "what do" or "why did" in oracion:\n        if oracion[-1] == "?":\n            return "Pregunta correcta"\n        return oracion + "?"\n    return "No es pregunta"\n',
        'def pregunta_2(oracion):\n    if "what do" in oracion or "why did" in oracion:\n        if oracion[-1] == "?":\n            return "Pregunta correcta"\n        return oracion + "?"\n    return "No es pregunta"\n',
        ['print(pregunta_2("what do you want"))', 'print(pregunta_2("why did you leave?"))', 'print(pregunta_2("there is a statement"))'],
        ['<code>"what do" or "why did" in oracion</code> se lee como <code>"what do" or ("why did" in oracion)</code>, y una cadena no vacía es <code>True</code>: el if siempre entra.', 'Cada condición necesita su propio <code>in</code>: <code>"what do" in oracion or "why did" in oracion</code>.'],
        'Lee la condición del if como la lee Python.', [['mets'], []]))
    tools = [paso('frase = "uTeC 2026"\nnueva = ""\nfor letra in frase:\n    if letra.isupper():\n        nueva = nueva + letra.lower()\n    else:\n        nueva = nueva + letra.upper()\nprint(nueva)',
                  'Paso a paso: invertir mayúsculas', 'Avanza línea por línea y mira cómo <code>nueva</code> crece letra por letra (la cadena original no cambia).')]
    return {'id': 'c9', 'name': 'Sem. 9 · Cadenas', 'teo': T_CAD, 'form': F_CAD, 'lesson': L_CAD, 'ex': E, 'tools': tools}

T_LIS = """
<p>Una <strong>lista</strong> guarda varios valores en orden: <code>notas = [18, 16, 20, 16]</code>. Se accede por índice (<code>notas[0]</code>, <code>notas[-1]</code>), <code>len(notas)</code> da cuántos hay y el último índice es <code>len(notas) - 1</code>. A diferencia de las cadenas, las listas son <strong>mutables</strong>: <code>notas[3] = 18</code> cambia la misma lista. Pueden tener valores repetidos y de distintos tipos (incluso otras listas).</p>
<table class="fillt"><tr><th>Para…</th><th>Usa</th><th>Ojo</th></tr>
<tr><td>Agregar</td><td><code>l.append(x)</code>, <code>l.insert(i, x)</code></td><td>append al final; insert corre a los demás</td></tr>
<tr><td>Buscar</td><td><code>x in l</code>, <code>l.index(x)</code></td><td>index da la <b>primera</b> posición; si no está, <b>ValueError</b></td></tr>
<tr><td>Borrar</td><td><code>del l[i]</code>, <code>l.remove(x)</code>, <code>l.pop(i)</code></td><td>remove borra la primera aparición; pop devuelve lo que quita (sin i, el último)</td></tr>
<tr><td>Unir</td><td><code>l1 + l2</code></td><td>crea una lista <b>nueva</b></td></tr>
<tr><td>Resumir</td><td><code>sum(l)</code>, <code>max(l)</code>, <code>min(l)</code>, <code>len(l)</code></td><td>sum/len = promedio</td></tr></table>
<p>Recorridos: <code>for x in l:</code> (cada valor), <code>for i in range(len(l)):</code> (cada posición) o <code>for i, x in enumerate(l):</code> (las dos cosas). Con asignación múltiple, <code>a, b, c = [1, 2, 3]</code>.</p>
<p><strong>El operador = no copia.</strong> <code>b = a</code> hace que <code>b</code> sea otro nombre para la <em>misma</em> lista: si cambias una, cambias «las dos». Para copiar: <code>b = a[:]</code> o <code>b = a.copy()</code>. Por eso una función que hace <code>lista.append(...)</code> sobre su parámetro modifica la lista original.</p>
<p><strong>Listas paralelas:</strong> si <code>nombres[i]</code> corresponde a <code>notas[i]</code>, recorre con el índice <code>i</code> para usar ambas.</p>
"""
L_LIS = """<h3>Idea central</h3><p>Una lista es una fila de casilleros numerados desde 0. Casi todos los ejercicios son: recorrer, preguntar algo de cada elemento y armar una lista nueva con <code>append</code> o devolver un número.</p>
<h3>Conceptos clave</h3><ul><li>Mayor y menor a mano: empezar en <code>l[0]</code>, no en 0.</li><li>Si usas <code>l[i + 1]</code>, el bucle va hasta <code>len(l) - 1</code>.</li><li><code>b = a</code> no copia.</li></ul>
<div class="ej"><b>Ejemplo:</b> «vecino más fuerte» de <code>[2, 4, 5, 2]</code> → <code>[4, 5, 5]</code>: compara cada par <code>l[i]</code>, <code>l[i + 1]</code>.</div>
<div class="err"><b>Error común:</b> <code>for i in range(len(l)):</code> y usar <code>l[i + 1]</code> → <code>IndexError</code> en la última vuelta.</div>"""
F_LIS = [c('l.append(x)') + ' · ' + c('l.insert(i, x)'), c('del l[i]') + ' · ' + c('l.remove(x)') + ' · ' + c('l.pop()'),
         c('x in l') + ' · ' + c('l.index(x)') + ' (ValueError si no está)', c('b = a') + ' = misma lista; ' + c('a[:]') + ' = copia',
         c('sum(l) / len(l)') + ' promedio', c('for i, x in enumerate(l):')]

def listas():
    E = []
    E.append(opc('l9_1', 1, 'Mutable', '<p>¿Qué quiere decir que una lista sea <b>mutable</b>?</p>',
        ['Que se pueden cambiar, agregar o quitar sus elementos sin crear otra lista', 'Que sus elementos siempre son del mismo tipo', 'Que al asignarla a otra variable se copia automáticamente', 'Que no se puede acceder a sus elementos por índice', 'Que su tamaño se fija al crearla'],
        ['Mutable = se puede modificar «por dentro»: <code>l[0] = 5</code>, <code>l.append(7)</code>, <code>l.pop()</code>.', 'Las cadenas y las tuplas son inmutables; las listas y los diccionarios, mutables.'],
        '', [['mut'], ['mut', 'inmut']]))
    E.append(ex('l9_2', 2, '¿Cambia la lista o crea otra?', '<p>Con <code>l = [4, 1, 3]</code>, clasifica cada instrucción.</p>',
        [{'t': 'cls', 'p': 'Clasifica', 'cats': ['Modifica l', 'Crea una lista nueva'],
          'items': [{'x': c('l.append(5)'), 'c': 0}, {'x': c('l + [5]'), 'c': 1, 'e': '+ arma una lista nueva; l queda igual.'}, {'x': c('l.insert(0, 9)'), 'c': 0},
                    {'x': c('l.pop()'), 'c': 0}, {'x': c('sorted(l)'), 'c': 1, 'e': 'sorted devuelve una lista nueva ordenada.'}, {'x': c('l.sort()'), 'c': 0, 'e': 'sort ordena la misma lista (y devuelve None).'},
                    {'x': c('l[:]'), 'c': 1, 'e': 'Un corte siempre es una lista nueva.'}, {'x': c('l.remove(4)'), 'c': 0}, {'x': c('l.copy()'), 'c': 1}]}],
        ['Los métodos que cambian la lista: append, insert, pop, remove, sort (y <code>del</code>).', 'Crean otra: <code>+</code>, cortes, <code>sorted</code>, <code>copy</code>.'],
        'append, insert, pop, sort y remove modifican l; +, sorted, los cortes y copy crean otra lista', '¿Después de la instrucción, l cambió?', [['mut', 'agr', 'bor'], ['alias']]))
    E.append(imprime('l9_3', 2, '= no copia', 'a = [1, 2, 3]\nb = a\nb.append(4)\nc = a[:]\nc.append(5)\nprint(a)\nprint(c)',
        ['[1, 2, 3]\n[1, 2, 3, 5]', '[1, 2, 3, 4]\n[1, 2, 3, 5]', '[1, 2, 3, 4, 5]\n[1, 2, 3, 4, 5]', '[1, 2, 3]\n[1, 2, 3, 4, 5]'],
        ['<code>b = a</code>: b es otro nombre de la misma lista, así que <code>b.append(4)</code> también cambia a → [1, 2, 3, 4].', '<code>c = a[:]</code> es una copia: el 5 solo va a c → [1, 2, 3, 4, 5].'],
        'Dibuja cajas: ¿cuántas listas hay en memoria?', [['alias'], ['alias']]))
    E.append(imprime('l9_4', 2, 'remove, pop y del', 'l = [5, 8, 4, 7, 8]\nl.remove(8)\nx = l.pop()\ndel l[0]\nprint(l, x)',
        ['[5, 4, 7] 8', '[4, 7, 8] 8', '[4, 7] 7', '[5, 4] 8'],
        ['<code>remove(8)</code> borra el <b>primer</b> 8 → [5, 4, 7, 8].', '<code>pop()</code> quita y devuelve el último (8) → [5, 4, 7].', '<code>del l[0]</code> borra la posición 0 → [4, 7].'],
        'Aplica las tres instrucciones en orden.', [['bor'], ['bor'], ['bor']]))
    sol_may = 'notas = [14, 18, 11, 17]\nmayor = notas[0]\nmenor = notas[0]\nfor n in notas:\n    if n > mayor:\n        mayor = n\n    if n < menor:\n        menor = n'
    rows = []; mayor = menor = 14
    for n in [14, 18, 11, 17]:
        mayor = max(mayor, n); menor = min(menor, n); rows.append([str(n), {'a': str(mayor)}, {'a': str(menor)}])
    E.append(ex('l9_5', 2, 'Rastreo: mayor y menor', '<p>Completa la tabla con los valores <b>al terminar cada vuelta</b> del for.</p>',
        [{'t': 'traza', 'p': 'Rastrea el bucle', 'code': sol_may, 'head': ['n', 'mayor', 'menor'], 'rows': rows}],
        ['Empiezan en <code>notas[0] = 14</code>.', 'Vuelta 2: 18 > 14 → mayor = 18. Vuelta 3: 11 < 14 → menor = 11. La vuelta 4 (17) no cambia nada.'],
        'mayor = 18 y menor = 11 al final', 'Compara cada n con los valores actuales.', [['maxmin'], ['maxmin']], play=sol_may + '\nprint(mayor, menor)'))
    E.append(hueco('l9_6', 2, 'Posiciones de un número', '<p>La función retorna una lista con todas las posiciones donde aparece <code>numero</code> (Lab 9A, ejercicio 1). Con <code>[8, 4, 3, 2, 1, 5, 6, 2]</code> y 2 → <code>[3, 7]</code>.</p>',
        'def posiciones(lista, numero):\n    pos = []\n    for i in range(⟦0⟧):\n        if ⟦1⟧ == numero:\n            pos.⟦2⟧\n    return pos',
        [(['len(lista)', '0, len(lista)', '0, len(lista), 1'], 'Necesitas recorrer todas las posiciones de la lista.', 'range(len(lista)) da 0, 1, …, len − 1.'),
         (['lista[i]'], '¿Qué valor está en la posición i?', 'Se compara el elemento lista[i], no la posición i.'),
         (['append(i)'], '¿Qué guardas: la posición o el valor?', 'Se pide la posición: pos.append(i).')],
        ['El for recorre las posiciones <code>i</code> de 0 a <code>len(lista) − 1</code>.', 'Si <code>lista[i]</code> es el número buscado, se agrega la posición <code>i</code>.'],
        'Recorre por índice.', [['rango'], ['agr']],
        tests=mk_tests('def posiciones(lista, numero):\n    pos = []\n    for i in range(len(lista)):\n        if lista[i] == numero:\n            pos.append(i)\n    return pos',
                       ['print(posiciones([8, 4, 3, 2, 1, 5, 6, 2, 1, 4, 5, 8, 9], 2))', 'print(posiciones([1, 1, 1], 1))', 'print(posiciones([5, 6], 9))']),
        demo='print(posiciones([8, 4, 3, 2, 1, 5, 6, 2], 2))'))
    E.append(bug('l9_7', 2, 'Vecino más fuerte', '<p>Para cada par de elementos seguidos, la función debe guardar el mayor (Lab 9A, ejercicio 2): <code>[2, 4, 5, 2]</code> → <code>[4, 5, 5]</code>.</p>',
        'def vecino_mas_fuerte(lista):\n    res = []\n    for i in range(len(lista)):\n        if lista[i] >= lista[i + 1]:\n            res.append(lista[i])\n        else:\n            res.append(lista[i + 1])\n    return res\n\nprint(vecino_mas_fuerte([2, 4, 5, 2]))',
        [3], ['El for llega hasta el último índice y lista[i + 1] se sale de la lista', 'Debería ser > y no >=', 'res debería crearse dentro del for', 'Falta un return dentro del for', 'append no funciona dentro de un if'],
        ['En la última vuelta, <code>i = 3</code> y <code>lista[4]</code> no existe → <code>IndexError</code>.', 'Como cada vuelta usa el siguiente, el rango debe ser <code>range(len(lista) - 1)</code>.'],
        '¿Cuál es el último i y existe lista[i + 1]?', [['rango'], ['rango']],
        fixed='def vecino_mas_fuerte(lista):\n    res = []\n    for i in range(len(lista) - 1):\n        if lista[i] >= lista[i + 1]:\n            res.append(lista[i])\n        else:\n            res.append(lista[i + 1])\n    return res\n\nprint(vecino_mas_fuerte([2, 4, 5, 2]))'))
    E.append(codex('l9_8', 2, 'El mayor al inicio',
        '<p>Implementa <code>pregunta_1(lista)</code> que retorne una lista <b>nueva</b> con el valor más alto al inicio y los demás en su orden original. Si el mayor se repite, solo se mueve el primero (Tarea de Laboratorio 8).</p>' +
        pre('pregunta_1([12, 19, 16, 15])       →  [19, 12, 16, 15]\npregunta_1([12, 15, 16, 16, 15, 12]) →  [16, 12, 15, 16, 15, 12]'),
        'def pregunta_1(lista):\n    # tu código aquí\n    return lista\n',
        'def pregunta_1(lista):\n    mayor = max(lista)\n    resto = lista[:]\n    resto.remove(mayor)\n    return [mayor] + resto\n',
        ['print(pregunta_1([12, 19, 16, 15]))', 'print(pregunta_1([1, 2, 3, 4, 5, 6, 7, 8, 9]))', 'print(pregunta_1([12, 15, 16, 16, 15, 12]))', 'l = [3, 7, 1]\nr = pregunta_1(l)\nprint(l, r)'],
        ['<code>max</code> da el mayor; una copia <code>lista[:]</code> evita modificar la original.', '<code>remove</code> borra solo la primera aparición; luego se une <code>[mayor] + resto</code>.'],
        'Copia, quita el mayor y únelo adelante.', [['maxmin', 'alias'], ['bor']],
        names=['Ejemplo 1', 'Ejemplo 2', 'Mayor repetido', 'No modifica la lista original'], pc='lis'))
    E.append(codex('l9_9', 3, 'Descubriendo la información',
        '<p>Implementa <code>pregunta_4(posiciones)</code>: retorna una lista de largo <code>max(posiciones) + 1</code> donde cada posición marcada tiene su propio número y el resto es 0 (Tarea de Laboratorio 8).</p>' +
        pre('pregunta_4([0, 2, 4, 2, 5])      →  [0, 0, 2, 0, 4, 5]\npregunta_4([0, 0, 0, 0, 0, 0, 1]) →  [0, 1]'),
        'def pregunta_4(posiciones):\n    # tu código aquí\n    return []\n',
        'def pregunta_4(posiciones):\n    res = [0] * (max(posiciones) + 1)\n    for p in posiciones:\n        res[p] = p\n    return res\n',
        ['print(pregunta_4([0, 2, 4, 2, 5]))', 'print(pregunta_4([0, 0, 0, 0, 0, 0, 1]))', 'print(pregunta_4([0, 1, 2, 3, 4, 1, 5, 2, 2, 4, 4, 5, 6]))', 'print(pregunta_4([3]))'],
        ['El tamaño lo fija la posición más grande: <code>[0] * (max + 1)</code>.', 'Cada posición <code>p</code> de la entrada se marca con <code>res[p] = p</code> (los repetidos no molestan).'],
        'Crea primero la lista llena de ceros.', [['agr'], ['mut']], pc='lis'))
    E.append(codex('l9_10', 2, 'Mejor y peor categoría',
        '<p>Implementa <code>pregunta_2(categorias, puntuaciones)</code> (listas paralelas de 4 elementos). Retorna <code>"categoriaMax_categoriaMin"</code>; si hay empates, la primera que aparece (Tarea de Laboratorio 8).</p>' +
        pre('pregunta_2(["Frescos", "Despensa", "Mascotas", "Bebidas"], [10, 20, 0, 5])\n→  "Despensa_Mascotas"'),
        'def pregunta_2(categorias, puntuaciones):\n    # tu código aquí\n    return ""\n',
        'def pregunta_2(categorias, puntuaciones):\n    imax = 0\n    imin = 0\n    for i in range(len(puntuaciones)):\n        if puntuaciones[i] > puntuaciones[imax]:\n            imax = i\n        if puntuaciones[i] < puntuaciones[imin]:\n            imin = i\n    return categorias[imax] + "_" + categorias[imin]\n',
        ['print(pregunta_2(["Frescos", "Despensa", "Mascotas", "Bebidas"], [10, 20, 0, 5]))', 'print(pregunta_2(["Frescos", "Despensa", "Mascotas", "Bebidas"], [10, 5, 0, 19]))',
         'print(pregunta_2(["Frescos", "Despensa", "Mascotas", "Bebidas"], [0, 1, 2, 3]))', 'print(pregunta_2(["Frescos", "Despensa", "Mascotas", "Bebidas"], [7, 7, 7, 7]))'],
        ['Guarda la <b>posición</b> del mayor y del menor, no el valor: así sacas el nombre con <code>categorias[imax]</code>.', 'Con <code>&gt;</code> y <code>&lt;</code> estrictos, en un empate se queda la primera. Otra forma: <code>puntuaciones.index(max(puntuaciones))</code>.'],
        'Listas paralelas: la misma posición en las dos.', [['par', 'maxmin'], ['bus']], pc='lis'))
    tools = [paso('a = [1, 2, 3]\nb = a\nb.append(4)\nc = a[:]\nc.append(5)\nprint(a, b, c)', 'Paso a paso: ¿copia o la misma lista?', 'Fíjate en las etiquetas: <code>a</code> y <code>b</code> muestran la misma (L1); <code>c</code> es otra lista.'),
             paso(sol_may + '\nprint(mayor, menor)', 'Paso a paso: mayor y menor sin max ni min')]
    return {'id': 'l9', 'name': 'Sem. 9 · Listas', 'teo': T_LIS, 'form': F_LIS, 'lesson': L_LIS, 'ex': E, 'tools': tools}

T_COR = """
<p>Un <strong>corte</strong> (<em>slice</em>) saca una parte de una lista o cadena: <code>l[inicio:fin:paso]</code>, que es lo mismo que <code>l[slice(inicio, fin, paso)]</code>. Toma desde <code>inicio</code> <b>hasta fin − 1</b> (el fin no se incluye), avanzando <code>paso</code> posiciones cada vez. El resultado es siempre una lista (o cadena) <b>nueva</b>.</p>
<ul><li>Si omites el inicio, empieza en el borde; si omites el fin, llega al otro borde; si omites el paso, es 1. <code>l[:]</code> es una copia completa.</li>
<li><code>l[:2]</code> = los dos primeros · <code>l[2:]</code> = desde la posición 2 · <code>l[::2]</code> = posiciones pares · <code>l[1::2]</code> = posiciones impares.</li>
<li>Índices negativos cuentan desde el final: <code>l[-1]</code> es el último, <code>l[-3:]</code> son los tres últimos.</li>
<li>Con <b>paso negativo</b> se va de derecha a izquierda: <code>l[::-1]</code> invierte; <code>l[5:1:-2]</code> toma las posiciones 5 y 3. El inicio debe estar a la derecha del fin; si no, sale vacío.</li>
<li>Un corte <b>no da error</b> si te pasas: <code>l[2:100]</code> llega hasta donde haya. En cambio un índice suelto fuera de rango, <code>l[100]</code>, lanza <code>IndexError</code>.</li></ul>
<p>Con cadenas funciona igual: <code>"Domenica"[::-1]</code> → <code>"acinemoD"</code>; rotar es <code>s[1:] + s[0]</code>.</p>
"""
L_COR = """<h3>Idea central</h3><p>Imagina un «cursor» que empieza en <code>inicio</code>, salta de <code>paso</code> en <code>paso</code> y se detiene <b>antes</b> de llegar a <code>fin</code>.</p>
<h3>Conceptos clave</h3><ul><li>El fin nunca se incluye.</li><li>Lo omitido se completa con el borde (según el sentido del paso).</li><li>Un corte nunca da IndexError.</li></ul>
<div class="ej"><b>Ejemplo:</b> <code>notas = [18, 17, 20, 16]</code>: <code>notas[1:3]</code> → [17, 20]; <code>notas[::3]</code> → [18, 16]; <code>notas[::-1]</code> → [16, 20, 17, 18].</div>
<div class="err"><b>Error común:</b> esperar que <code>notas[1:3]</code> incluya la posición 3.</div>"""
F_COR = [c('l[inicio:fin:paso]') + ' (fin no incluido)', c('l[:k]') + ' primeros k · ' + c('l[-k:]') + ' últimos k', c('l[::2]') + ' pares · ' + c('l[1::2]') + ' impares',
         c('l[::-1]') + ' al revés', c('l[:]') + ' copia', c('l[2:100]') + ' sin error · ' + c('l[100]') + ' IndexError']

def cortes():
    E = []
    notas = [18, 17, 20, 16]
    def tap(id, lvl, title, seq, name, expr, steps, hint, tags):
        a = eval(expr.replace(name, 'list(range(' + str(len(seq)) + '))'))
        return ex(id, lvl, title, '<p>Toca los elementos que toma el corte, en el orden en que salen.</p>',
                  [{'t': 'slice', 'p': 'Toca los elementos', 'mode': 'tap', 'seq': seq, 'name': name, 'expr': expr, 'a': a}],
                  steps, c(p1rl(seq, a)), hint, tags, play=name + ' = ' + repr(seq) + '\nprint(' + expr + ')')
    def build(id, lvl, title, seq, name, goal_ix, sol, steps, hint, tags):
        goal = ''.join(seq[i] for i in goal_ix) if isinstance(seq, str) else [seq[i] for i in goal_ix]
        assert py_slice_ix(len(seq), *sol) == goal_ix
        return ex(id, lvl, title, '<p>Elige inicio, fin y paso (puede quedar vacío) para obtener lo pedido. Hay más de una respuesta posible.</p>',
                  [{'t': 'slice', 'p': 'Arma el corte', 'mode': 'build', 'seq': seq, 'name': name, 'goal': goal, 'sol': sol}],
                  steps, c(name + '[' + ':'.join('' if x is None else str(x) for x in sol) + ']') + ' (u otro equivalente)', hint, tags)
    E.append(tap('k9_1', 1, 'Corte básico', notas, 'notas', 'notas[1:3]', ['Empieza en la posición 1 y se detiene antes de la 3: posiciones 1 y 2.'], 'El fin no se incluye.', [['sl']]))
    E.append(tap('k9_2', 1, 'Con paso', notas, 'notas', 'notas[::3]', ['Sin inicio ni fin recorre toda la lista; con paso 3 toma las posiciones 0 y 3.'], 'Salta de 3 en 3 desde el inicio.', [['slom']]))
    lista = [144, 145, 146, 147, 201, 202, 203, 204]
    E.append(tap('k9_3', 2, 'Paso negativo', lista, 'lista', 'lista[6:1:-2]', ['Con paso −2 va hacia la izquierda: 6, 4, 2. Se detiene antes de llegar a 1.'], 'Empieza en la posición 6 y retrocede de 2 en 2.', [['slneg']]))
    E.append(tap('k9_4', 2, 'Índices negativos', lista, 'lista', 'lista[-3:]', ['−3 es la antepenúltima posición (5); sin fin, llega hasta el final: 5, 6, 7.'], 'Mira los números rojos de abajo: son los índices negativos.', [['slom']]))
    E.append(build('k9_5', 2, 'Arma el corte', notas, 'notas', [1, 3], [1, None, 2], ['Se quieren las posiciones 1 y 3: empezar en 1 y saltar de 2 en 2 → <code>notas[1::2]</code>.'], 'Son las posiciones impares.', [['slom']]))
    E.append(build('k9_6', 2, 'Al revés', 'Domenica', 'nombre', list(range(7, -1, -1)), [None, None, -1], ['Paso −1 sin inicio ni fin recorre toda la cadena de derecha a izquierda.'], 'Paso negativo.', [['slneg']]))
    E.append(imprime('k9_7', 2, 'Cortes en una lista larga', 'lista = [144, 145, 146, 147, 201, 202, 203, 204, 205]\nprint(lista[4:7])\nprint(lista[-9::-1])\nprint(lista[7:2:-2])',
        ['[201, 202, 203]\n[]\n[204, 202, 147]', '[201, 202, 203, 204]\n[144]\n[204, 202, 147]', '[201, 202, 203]\n[144]\n[204, 202]', '[147, 201, 202]\n[205, 204, 203, 202, 201, 147, 146, 145, 144]\n[204, 202, 147]'],
        ['<code>[4:7]</code>: posiciones 4, 5 y 6 → [201, 202, 203].', '<code>-9</code> es la posición 0 (hay 9 elementos); con paso −1 y sin fin solo queda ese → [144].', '<code>[7:2:-2]</code>: 7, 5, 3 (se detiene antes de 2) → [204, 202, 147].'],
        'Cuenta los elementos para traducir el −9.', [['sl'], ['slneg'], ['slneg']]))
    E.append(opc('k9_8', 2, 'Corte vs índice', pre('notas = [18, 17, 20, 16]\nprint(notas[2:10])\nprint(notas[10])') + '<p>¿Qué pasa?</p>',
        ['Imprime [20, 16] y luego da IndexError', 'Da IndexError en la primera línea', 'Imprime [20, 16] y luego None', 'Imprime [20, 16, 0, 0, 0, 0, 0, 0] y luego 0', 'Imprime [] y luego da IndexError'],
        ['Un corte se ajusta al tamaño de la lista: <code>notas[2:10]</code> → [20, 16].', 'Un índice suelto fuera de rango sí falla: <code>notas[10]</code> → <code>IndexError</code>.'],
        '', [['slerr'], ['slerr']]))
    E.append(hueco('k9_9', 1, 'Rotar con cortes', '<p>Completa para que cada vuelta pase el primer carácter al final.</p>',
        'def rotar(frase, n):\n    for i in range(n):\n        frase = frase[⟦0⟧] + frase[⟦1⟧]\n    return frase',
        [(['1:', '1::', '1:len(frase)'], 'Todo menos el primero: ¿desde qué posición?', 'Desde la posición 1 hasta el final: frase[1:].'),
         (['0', ':1', '0:1', '-len(frase)'], 'Solo el primer carácter.', 'El primero es frase[0].')],
        ['<code>frase[1:]</code> es todo menos el primer carácter; <code>frase[0]</code> es el primero.', 'Unidos, el primero queda al final.'],
        '', [['sl'], []],
        tests=mk_tests('def rotar(frase, n):\n    for i in range(n):\n        frase = frase[1:] + frase[0]\n    return frase', ['print(rotar("Barranco", 5))', 'print(rotar("UTEC", 1))']),
        demo='print(rotar("Maravilloso", 5))'))
    E.append(codex('k9_10', 2, '¿Es palíndromo?',
        '<p>Implementa <code>es_palindromo(palabra)</code>: retorna <code>True</code> si se lee igual al derecho y al revés, sin distinguir mayúsculas. Usa un corte.</p>' + pre('es_palindromo("Reconocer")  →  True\nes_palindromo("UTEC")       →  False'),
        'def es_palindromo(palabra):\n    # tu código aquí\n    return False\n',
        'def es_palindromo(palabra):\n    p = palabra.lower()\n    return p == p[::-1]\n',
        ['print(es_palindromo("Reconocer"))', 'print(es_palindromo("UTEC"))', 'print(es_palindromo("Ana"))', 'print(es_palindromo("ab"))'],
        ['Primero <code>lower()</code> para que «R» y «r» sean iguales.', '<code>p[::-1]</code> es la cadena al revés: basta compararlas.'],
        'Corte con paso −1.', [['mets'], ['slneg']], pc='str'))
    E.append(codex('k9_11', 2, 'Intercambiar mitades',
        '<p>Implementa <code>mitades(l)</code>: retorna una lista nueva con la segunda mitad primero y luego la primera. Si el largo es impar, la mitad de adelante es la más corta (<code>len(l) // 2</code> elementos).</p>' + pre('mitades([1, 2, 3, 4])     →  [3, 4, 1, 2]\nmitades([1, 2, 3, 4, 5])  →  [3, 4, 5, 1, 2]'),
        'def mitades(l):\n    # tu código aquí\n    return l\n',
        'def mitades(l):\n    m = len(l) // 2\n    return l[m:] + l[:m]\n',
        ['print(mitades([1, 2, 3, 4]))', 'print(mitades([1, 2, 3, 4, 5]))', 'print(mitades([7]))', 'print(mitades([]))'],
        ['La mitad es <code>m = len(l) // 2</code>.', '<code>l[m:]</code> es la segunda parte y <code>l[:m]</code> la primera.'],
        'Dos cortes y un +.', [['slom'], ['slom']], pc='lis'))
    tools = [{'w': 'slice', 't': 'Cortador de listas', 'p': 'Elige inicio, fin y paso, o toca un ejemplo. Prueba pasos negativos e índices negativos.', 'o': {'seq': [18, 17, 20, 16, 15, 19], 'name': 'notas'}},
             {'w': 'slice', 't': 'Cortador de cadenas', 'o': {'seq': 'Maravilloso', 'name': 'frase', 'presets': [[1, None, None], [None, 3, None], [None, None, -1], [1, None, 2], [-4, None, None], [5, None, None]]}}]
    return {'id': 'k9', 'name': 'Sem. 9 · Cortes (slices)', 'teo': T_COR, 'form': F_COR, 'lesson': L_COR, 'ex': E, 'tools': tools}

def p1rl(seq, ix):
    return "'" + ''.join(seq[i] for i in ix) + "'" if isinstance(seq, str) else '[' + ', '.join(repr(seq[i]) for i in ix) + ']'
