#!/usr/bin/env python3
"""POO (CS6004) · semanas 10 (polimorfismo y clases abstractas) y 11 (excepciones) → cursos/poo-ef.json.
También agrega a la semana 9 el ejercicio de ordenar el recorrido del MRO del diamante (m9).
Cada «¿qué imprime?» se ejecuta aquí y cada solución modelo se prueba con el mismo arnés de py-worker.js.
Uso: python3 tools/poo_s10_11.py   (reejecutable: reemplaza w10pol, w11exc y m9)."""
import json, os, re, sys, html, subprocess, tempfile, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p1_lib import paso

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(REPO, 'cursos', 'poo-ef.json')
d = json.load(open(F, encoding='utf-8'))
H = json.loads(re.search(r'const HARNESS = (".*?");\n', open(os.path.join(REPO, 'py-worker.js')).read(), re.S).group(1))

def esc(s): return html.escape(s, quote=False)
def pre(code): return '<pre class="py"><code>' + esc(code) + '</code></pre>'
def out(s): return '<code class="out">' + esc(s) + '</code>'
def perr(prev, name): return '<code class="out">' + esc(prev) + '<b class="perr">💥 ' + name + '</b></code>'

def runpy(code, tests, files):
    src = H + '\nimport json,sys\nprint("@@R@@"+run_all(sys.argv[1],sys.argv[2],sys.argv[3]))'
    with tempfile.TemporaryDirectory() as t:
        f = os.path.join(t, 'h.py'); open(f, 'w').write(src)
        r = subprocess.run([sys.executable, f, code, json.dumps(tests), json.dumps(files or {})], capture_output=True, text=True, timeout=60, cwd=t)
    return json.loads(r.stdout.split('@@R@@')[-1])

def run(code, files=None):
    """(salida, nombre de la excepción o None)"""
    with tempfile.TemporaryDirectory() as t:
        for n, s in (files or {}).items(): open(os.path.join(t, n), 'w').write(s)
        p = os.path.join(t, 'm.py'); open(p, 'w').write(code)
        r = subprocess.run([sys.executable, p], capture_output=True, text=True, timeout=30, cwd=t)
    exc = None
    if r.returncode:
        last = r.stderr.strip().split('\n')[-1]
        exc = last.split(':')[0].strip()
    return r.stdout, exc

def ex(id, lvl, title, q, checks, steps, ans, hint, tags, play=None, fig=None, chain=False):
    assert len(tags) == len(steps), (id, 'tags/steps')
    e = {"id": id, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans, "hint": hint,
         "fig": fig, "draw": False, "open": False, "solfig": None, "tags": tags}
    if play: e["play"] = play
    if chain: e["chain"] = True
    return e

def mc(p, opts):
    assert len(opts) == 5 and len(set(opts)) == 5, opts
    return {"p": p, "o": opts}

def output_ex(id, lvl, title, prog, outs, steps, hint, tags, files=None, intro=''):
    """outs[0] es la salida correcta; puede ser ('texto previo', 'TipoError') para una excepción."""
    got, exc = run(prog, files)
    o0 = outs[0]
    if isinstance(o0, tuple):
        assert exc == o0[1] and got.rstrip('\n') == o0[0].rstrip('\n'), (id, got, exc)
    else:
        assert exc is None and got.rstrip('\n') == o0.rstrip('\n'), (id, repr(got), exc)
    fo = [perr(o[0], o[1]) if isinstance(o, tuple) else out(o.rstrip('\n')) for o in outs]
    return ex(id, lvl, title, intro + pre(prog) + '<p>¿Qué imprime este programa?</p>', [mc('Salida', fo)], steps, fo[0], hint, tags, play=prog)

def code_ex(id, lvl, title, q, start, sol, tests, steps_pre, hint, tags, files=None):
    r = runpy(sol, tests, files)
    for t, x in zip(tests, r): assert x['ok'], (id, t['n'], x)
    r0 = runpy(start, tests, files)
    assert not all(x['ok'] for x in r0), (id, 'la plantilla ya pasa')
    ch = {"t": "code", "p": "Escribe tu código y compruébalo con las pruebas", "start": start, "tests": tests}
    if files: ch["files"] = files
    return ex(id, lvl, title, q, [ch], steps_pre + ['Una solución posible:' + pre(sol)], "Tu código pasa todas las pruebas", hint, tags + [tags[-1]] * (len(steps_pre) + 1 - len(tags)))

def bug(code, line, opts, outtxt, e=None):
    _, exc = run(code)
    assert exc, 'el código del bug debía fallar'
    assert len(opts) == 5 and len(set(opts)) == 5
    c = {"t": "bug", "p": "Encuentra el error", "code": code, "l": [line], "o": opts, "out": outtxt}
    if e: c["e"] = e
    return c

def lineof(code, text, k=1):
    return [i + 1 for i, l in enumerate(code.split('\n')) if text in l][k - 1]

# =====================================================================
# Semana 9 · MRO del diamante (ordenar)
# =====================================================================
DIAM = '''class Raiz:
    def ping(self):
        print("ping desde Raiz")

class RamaA(Raiz):
    def ping(self):
        print("ping desde RamaA")
        super().ping()

class RamaB(Raiz):
    def ping(self):
        print("ping desde RamaB")
        super().ping()

class Hoja(RamaA, RamaB):
    def ping(self):
        print("ping desde Hoja")
        super().ping()

Hoja().ping()'''
o, e = run(DIAM); assert e is None
LINES = o.strip().split('\n'); assert LINES == ["ping desde Hoja", "ping desde RamaA", "ping desde RamaB", "ping desde Raiz"]
M9 = ex("m9", 2, "Ordena el recorrido del diamante",
  pre(DIAM) + "<p>Ordena las líneas tal como las imprime <code>Hoja().ping()</code>.</p>",
  [{"t": "order", "p": "Toca las líneas en el orden en que salen", "items": LINES}],
  ["El MRO de Hoja es <code>Hoja → RamaA → RamaB → Raiz → object</code> (la madre de la izquierda primero, y la raíz común al final).",
   "Cada <code>super().ping()</code> llama a la <b>siguiente clase del MRO</b>, no a la madre directa: por eso desde RamaA se pasa a RamaB (¡que no es su madre!) y recién al final a Raiz, que se imprime una sola vez."],
  "Hoja → RamaA → RamaB → Raiz", "super() sigue el MRO.", [["mro"], ["mro", "super"]], fig="umldiam")

# =====================================================================
# Semana 10 · Polimorfismo y clases abstractas
# =====================================================================
LIBSCREEN = '''class Pixel:
    unicode = "\\u2B1B\\u2B1C"

    def __init__(self, activo=False, x=None, y=None):
        self.activo = activo
        self.x = x
        self.y = y

    def encender(self):
        self.activo = True

    def apagar(self):
        self.activo = False

    def invertir(self):
        self.activo = not self.activo

    def __str__(self):
        return self.unicode[self.activo]


class RegionRectangular:
    def __init__(self, x1, x2, y1, y2):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2

    def __contains__(self, pixel):
        return self.x1 <= pixel.x <= self.x2 and self.y1 <= pixel.y <= self.y2


class Pantalla:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.pixeles = []
        for i in range(n):
            fila = []
            for j in range(m):
                fila.append(Pixel(False, i, j))
            self.pixeles.append(fila)

    def __getitem__(self, key):
        return self.pixeles[key]

    def encender_region(self, region):
        for fila in self.pixeles:
            for p in fila:
                if p in region:
                    p.encender()

    def __str__(self):
        return "\\n".join("".join(str(p) for p in fila) for fila in self.pixeles)
'''
FILES_SCR = {"libScreen.py": LIBSCREEN}

T10_teo = (
 "<p><strong>Polimorfismo</strong> («muchas formas»): el mismo mensaje produce comportamientos distintos según la clase del objeto que lo recibe. Si <code>DogeCard</code> y <code>DogeCardGold</code> tienen un método <code>pagar</code>, el código <code>tarjeta.pagar(producto)</code> funciona con cualquiera de las dos y cada una aplica <b>su</b> versión.</p>"
 "<p>En Python no hace falta declarar nada: basta que los objetos tengan el método (<i>duck typing</i>: «si camina como pato…»). Por eso <code>pagar</code> acepta cualquier objeto que tenga <code>obtener_precio()</code>, aunque no sea un <code>Producto</code>.</p>"
 "<p>La hija <b>sobrescribe</b> el método y puede reutilizar el de la madre con <code>super().pagar(…)</code>. Así la DogeCardGold solo agrega el descuento y deja que la DogeCard haga el cobro.</p>"
 "<p><strong>Métodos mágicos y polimorfismo:</strong> <code>pixel in region</code> llama a <code>region.__contains__(pixel)</code>. Cada región (rectangular, cuadrada, circular, semiplano) implementa su propio <code>__contains__</code> y la pantalla las enciende todas con el mismo código.</p>"
 "<p><strong>Clase abstracta:</strong> una superclase que solo define la «forma» que deben tener sus hijas. Con <code>from abc import ABC, abstractmethod</code>:</p>"
 + pre('from abc import ABC, abstractmethod\n\nclass Region(ABC):\n    @abstractmethod\n    def __contains__(self, pixel):\n        ...\n\nclass RegionCircular(Region):\n    def __init__(self, x, y, radio):\n        self.x, self.y, self.radio = x, y, radio\n    def __contains__(self, pixel):\n        return (self.x - pixel.x)**2 + (self.y - pixel.y)**2 <= self.radio**2')
 + "<p><code>Region()</code> da <code>TypeError</code> (no se puede instanciar una clase abstracta), y una hija que no implemente todos los métodos abstractos tampoco se puede crear.</p>"
 "<div class=\"err\"><b>Ojo con el lab 10B:</b> en el constructor de <code>Pantalla</code> que aparece en las diapositivas falta <code>self.pixeles.append(fila)</code>: sin esa línea la lista queda vacía y cualquier <code>self[i][j]</code> da <code>IndexError</code>. Y la condición del semiplano viene escrita como \\(0\\le a\\,y+b\\,x+c\\) (primero la y): respétala tal cual en el lab, o el semiplano saldrá «girado».</div>"
)
T10_form = ["Polimorfismo: mismo método, cada clase con su versión",
            "Reutilizar a la madre: <code>super().metodo(…)</code>",
            "<code>x in obj</code> → <code>obj.__contains__(x)</code>",
            "Abstracta: <code>class R(ABC)</code> + <code>@abstractmethod</code> · <code>R()</code> → TypeError",
            "Círculo: \\((x-x')^2+(y-y')^2\\le r^2\\)"]
T10_lesson = (
 "<h3>Idea central</h3><p>El polimorfismo te deja escribir código que no pregunta «¿qué clase eres?»: le habla a todos igual (<code>pagar</code>, <code>in</code>, <code>area</code>) y cada objeto responde a su manera. Si te descubres escribiendo <code>if isinstance(…)</code> para elegir el comportamiento, probablemente ese comportamiento debería ser un método sobrescrito.</p>"
 "<h3>Receta</h3><ol><li>Define en la madre el método común (o abstracto si no hay versión por defecto).</li><li>En cada hija, sobrescríbelo con el mismo nombre y parámetros.</li><li>Usa <code>super()</code> para no repetir lo que la madre ya hace.</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes:</b> cambiar el nombre o los parámetros del método en la hija (deja de ser el mismo mensaje); copiar y pegar el código de la madre en vez de llamar a <code>super()</code>; y olvidar implementar un método abstracto (la hija no se puede crear).</div>"
)

DOGE_START = '''class DogeCard:
    def __init__(self, saldo):
        self.saldo = saldo

    def pagar(self, producto):
        # completa: descuenta el precio solo si alcanza y devuelve True/False
        pass
'''
DOGE_SOL = '''class DogeCard:
    def __init__(self, saldo):
        self.saldo = saldo

    def pagar(self, producto):
        precio = producto.obtener_precio()
        if precio <= self.saldo:
            self.saldo -= precio
            return True
        return False
'''
ITEM = 'class Item:\n    def __init__(self, p):\n        self.p = p\n    def obtener_precio(self):\n        return self.p\n'
T_DOGE = [{"n": "Compra que alcanza", "run": ITEM + 'd = DogeCard(777)\nprint(d.pagar(Item(500)), d.saldo)', "out": "True 277"},
          {"n": "No alcanza", "run": ITEM + 'd = DogeCard(100)\nprint(d.pagar(Item(150.5)), d.saldo)', "out": "False 100"},
          {"n": "Varias compras", "run": ITEM + 'd = DogeCard(777)\nr = [d.pagar(Item(p)) for p in [300, 400, 100, 77]]\nprint(r, d.saldo)', "out": "[True, True, False, True] 0"}]
GOLD_START = DOGE_SOL + '''

class DogeCardGold(DogeCard):
    # completa: 10 % de descuento en las compras pares (la 2.ª, la 4.ª, …)
    pass
'''
GOLD_SOL = DOGE_SOL + '''

class DogeCardGold(DogeCard):
    def __init__(self, saldo):
        super().__init__(saldo)
        self.compras = 0

    def pagar(self, producto):
        self.compras += 1
        if self.compras % 2 == 0:
            return super().pagar(Descuento(producto))
        return super().pagar(producto)


class Descuento:
    def __init__(self, producto):
        self.producto = producto

    def obtener_precio(self):
        return round(self.producto.obtener_precio() * 0.9, 1)
'''
T_GOLD = [{"n": "Alterna el descuento", "run": ITEM + 'g = DogeCardGold(1000)\nfor p in [100, 100, 100, 100]:\n    g.pagar(Item(p))\nprint(g.saldo)', "out": "620.0"},
          {"n": "Es una DogeCard", "run": ITEM + 'g = DogeCardGold(50)\nprint(isinstance(g, DogeCard), g.pagar(Item(60)))', "out": "True False"},
          {"n": "Con el descuento alcanza justo", "run": ITEM + 'g = DogeCardGold(100)\nprint(g.pagar(Item(10)), g.pagar(Item(100)), g.saldo)', "out": "True True 0.0"}]

REG_START = '''from libScreen import Pixel


class RegionCircular:
    def __init__(self, x, y, radio):
        self.x, self.y, self.radio = x, y, radio
    # completa __contains__


class RegionSemiplanar:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
    # completa __contains__: el pixel está si 0 <= a*y + b*x + c
'''
REG_SOL = '''from libScreen import Pixel


class RegionCircular:
    def __init__(self, x, y, radio):
        self.x, self.y, self.radio = x, y, radio

    def __contains__(self, pixel):
        return (self.x - pixel.x) ** 2 + (self.y - pixel.y) ** 2 <= self.radio ** 2


class RegionSemiplanar:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def __contains__(self, pixel):
        return 0 <= self.a * pixel.y + self.b * pixel.x + self.c
'''
T_REG = [{"n": "Círculo", "run": 'r = RegionCircular(2, 2, 2)\nprint(Pixel(False, 2, 4) in r, Pixel(False, 4, 4) in r, Pixel(False, 0, 2) in r)', "out": "True False True"},
         {"n": "Semiplano", "run": 's = RegionSemiplanar(1, -1, 0)\nprint(Pixel(False, 1, 3) in s, Pixel(False, 3, 1) in s, Pixel(False, 2, 2) in s)', "out": "True False True"},
         {"n": "En la pantalla", "run": 'from libScreen import Pantalla\np = Pantalla(3, 5)\np.encender_region(RegionCircular(1, 2, 1))\nprint(p)', "out": "⬛⬛⬜⬛⬛\n⬛⬜⬜⬜⬛\n⬛⬛⬜⬛⬛"}]

ABS_START = '''from abc import ABC, abstractmethod


class Region(ABC):
    # completa: __contains__ abstracto
    pass


class RegionCuadrada(Region):
    def __init__(self, x, y, lado):
        self.x, self.y, self.lado = x, y, lado
    # completa __contains__: x <= pixel.x <= x + lado - 1 (igual con y)
'''
ABS_SOL = '''from abc import ABC, abstractmethod


class Region(ABC):
    @abstractmethod
    def __contains__(self, pixel):
        ...


class RegionCuadrada(Region):
    def __init__(self, x, y, lado):
        self.x, self.y, self.lado = x, y, lado

    def __contains__(self, pixel):
        return (self.x <= pixel.x <= self.x + self.lado - 1 and
                self.y <= pixel.y <= self.y + self.lado - 1)
'''
T_ABS = [{"n": "Region es abstracta", "run": 'try:\n    Region()\n    print("se pudo crear")\nexcept TypeError:\n    print("TypeError")', "out": "TypeError"},
         {"n": "Cuadrada", "run": 'from libScreen import Pixel\nq = RegionCuadrada(1, 1, 2)\nprint(Pixel(False, 1, 1) in q, Pixel(False, 2, 2) in q, Pixel(False, 3, 1) in q, isinstance(q, Region))', "out": "True True False True"},
         {"n": "Una hija sin __contains__ no se puede crear", "run": 'class Mala(Region):\n    pass\ntry:\n    Mala()\nexcept TypeError:\n    print("TypeError")', "out": "TypeError"}]

V2_START = '''from libScreen import Pantalla


class PantallaV2(Pantalla):
    # completa: encender_todo, apagar_todo, invertir_todo
    pass
'''
V2_SOL = '''from libScreen import Pantalla


class PantallaV2(Pantalla):
    def encender_todo(self):
        for fila in self.pixeles:
            for p in fila:
                p.encender()

    def apagar_todo(self):
        for fila in self.pixeles:
            for p in fila:
                p.apagar()

    def invertir_todo(self):
        for fila in self.pixeles:
            for p in fila:
                p.invertir()
'''
T_V2 = [{"n": "Encender y apagar", "run": 'p = PantallaV2(2, 3)\np.encender_todo()\nprint(p)\np.apagar_todo()\nprint(p)', "out": "⬜⬜⬜\n⬜⬜⬜\n⬛⬛⬛\n⬛⬛⬛"},
        {"n": "Invertir", "run": 'from libScreen import RegionRectangular\np = PantallaV2(2, 4)\np.encender_region(RegionRectangular(0, 0, 1, 2))\np.invertir_todo()\nprint(p)', "out": "⬜⬛⬛⬜\n⬜⬜⬜⬜"},
        {"n": "Sigue siendo una Pantalla", "run": 'p = PantallaV2(1, 1)\nprint(isinstance(p, Pantalla), str(p[0][0]))', "out": "True ⬛"}]

BUGSCR = '''class Pixel:
    def __init__(self, activo=False, x=None, y=None):
        self.activo, self.x, self.y = activo, x, y

class Pantalla:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.pixeles = []
        for i in range(n):
            fila = []
            for j in range(m):
                fila.append(Pixel(False, i, j))

    def __getitem__(self, key):
        return self.pixeles[key]

p = Pantalla(4, 8)
print(p[0][0].activo)'''

POLY_LOOP = '''class DogeCard:
    def __init__(self, saldo):
        self.saldo = saldo
    def pagar(self, precio):
        if precio <= self.saldo:
            self.saldo -= precio
            return True
        return False

class DogeCardGold(DogeCard):
    def pagar(self, precio):
        return super().pagar(precio * 0.5)

tarjetas = [DogeCard(100), DogeCardGold(100)]
for t in tarjetas:
    ok = t.pagar(120)
    print(type(t).__name__, ok, t.saldo)'''

T10 = []
T10.append(ex("pl1", 1, "¿Cómo saber si se pudo comprar?",
  "<p>En el lab 10A, <code>pagar(producto)</code> descuenta el precio solo si hay saldo. ¿Qué cambio permite que <code>main.py</code> sepa si la compra se hizo?</p>",
  [mc("Respuesta", ["Que pagar devuelva True si se compró y False si no", "Imprimir el saldo dentro de pagar", "Que pagar devuelva el producto siempre",
                     "Hacer que el saldo sea un atributo de clase", "Llamar a isinstance(producto, Producto)"])],
  ["Un método que «a veces funciona» debe <b>avisar</b> a quien lo llama: lo natural es devolver un booleano.",
   "Imprimir dentro del método no sirve para que el programa decida (por ejemplo, contar cuántas compras se hicieron). En la semana 11 verás otra opción: lanzar una excepción."],
  "Devolver True/False", "El llamador necesita una respuesta.", [["poli"], ["poli"]]))
T10.append(code_ex("pl2", 1, "DogeCard",
  "<p>Completa <code>pagar(producto)</code>: toma <code>producto.obtener_precio()</code>; si hay saldo suficiente lo descuenta y devuelve <code>True</code>, si no, no cambia nada y devuelve <code>False</code>.</p><p class=\"note\">Las pruebas usan un objeto <code>Item</code> que no es un <code>Producto</code> pero tiene <code>obtener_precio()</code>: eso también es polimorfismo.</p>",
  DOGE_START, DOGE_SOL, T_DOGE,
  ["Pide el precio con <code>producto.obtener_precio()</code> (no accedas a <code>__precio</code>: es privado de Producto).",
   "Compara con el saldo; si alcanza, resta y devuelve <code>True</code>; si no, devuelve <code>False</code> sin tocar el saldo."],
  "Usa obtener_precio().", [["poli"]]))
T10.append(code_ex("pl3", 2, "DogeCardGold con super()",
  "<p><code>DogeCardGold</code> hereda de <code>DogeCard</code> y da <b>10 % de descuento en la mitad de las compras</b>. En el lab es al azar; aquí, para poder probarlo, el descuento va en las compras pares (2.ª, 4.ª, …), y el precio con descuento se redondea a 1 decimal. Reutiliza <code>pagar</code> de la madre con <code>super()</code>.</p>",
  GOLD_START, GOLD_SOL, T_GOLD,
  ["La hija necesita contar las compras: su <code>__init__</code> llama a <code>super().__init__(saldo)</code> y agrega <code>self.compras = 0</code>.",
   "En <code>pagar</code> no se repite el cobro: se llama a <code>super().pagar(…)</code> con el producto original o con uno «envuelto» que devuelve el 90 % del precio (otra vez polimorfismo: basta con tener <code>obtener_precio()</code>)."],
  "super().pagar(…) hace el cobro.", [["super", "poli"]]))
T10.append(ex("pl4", 2, "Sin isinstance",
  "<p>Ejercicio 2 de la DogeCardGold: tienes un objeto que puede ser <code>DogeCard</code> o <code>DogeCardGold</code>. Sin usar <code>isinstance</code>, ¿qué forma lo distingue bien?</p>",
  [mc("Respuesta", ["Comparar type(t) con DogeCardGold (o mirar type(t).__name__)", "Comparar t == DogeCardGold",
                     "Revisar si t tiene el método pagar", "Mirar si t.saldo es mayor que 0", "Hacer print(t) y leer lo que sale"])],
  ["<code>type(t)</code> devuelve la clase exacta del objeto: <code>type(t) is DogeCardGold</code> o <code>type(t).__name__ == \"DogeCardGold\"</code>.",
   "Las dos tarjetas tienen <code>pagar</code> (por herencia) y cualquier saldo es posible, así que eso no distingue nada. También serviría preguntar por algo que solo tiene la Gold (por ejemplo <code>hasattr(t, \"compras\")</code>), pero comparar un objeto con una clase (<code>t == DogeCardGold</code>) siempre da False."],
  "type(t) is DogeCardGold", "¿Qué función devuelve la clase exacta?", [["inst"], ["inst", "poli"]]))
T10.append(output_ex("pl5", 2, "Mismo mensaje, dos tarjetas", POLY_LOOP,
  ["DogeCard False 100\nDogeCardGold True 40.0", "DogeCard False 100\nDogeCardGold False 100", "DogeCard True -20\nDogeCardGold True 40.0",
   "DogeCard False 100\nDogeCard True 40.0", "DogeCardGold True 40.0\nDogeCard False 100"],
  ["El bucle llama a <code>t.pagar(120)</code> igual para las dos; cada objeto usa su versión.",
   "La DogeCard no alcanza (120 &gt; 100): False y saldo 100. La Gold llama a <code>super().pagar(60.0)</code>: alcanza, True, saldo 40.0. <code>type(t).__name__</code> muestra la clase real de cada una."],
  "Cada objeto responde con su método.", [["poli"], ["poli", "super"]]))
T10.append(ex("pl6", 1, "Encuentra el error (lab 10B)",
  "<p>Este es el constructor de <code>Pantalla</code> tal como aparece en las diapositivas.</p>",
  [bug(BUGSCR, lineof(BUGSCR, "fila.append(Pixel"), ["Falta self.pixeles.append(fila): cada fila se arma pero nunca se guarda",
       "range(n) debería ser range(n + 1)", "Pixel(False, i, j) debería ser Pixel(i, j)", "self.pixeles debería ser un diccionario", "__getitem__ debería devolver self[key]"],
       "IndexError: list index out of range",
       e="Fíjate qué pasa con la lista fila al terminar cada vuelta del for de afuera.")],
  ["El for interno llena <code>fila</code>, pero al terminar la vuelta esa lista se pierde: nadie la agrega a <code>self.pixeles</code>.",
   "Falta <code>self.pixeles.append(fila)</code> dentro del primer for (después del for interno). Sin eso <code>self.pixeles</code> queda <code>[]</code> y <code>p[0]</code> da IndexError."],
  "Falta self.pixeles.append(fila)", "¿Dónde termina guardada cada fila?", [["poli"], ["poli"]]))
T10.append(ex("pl7", 1, "¿Qué llama a __contains__?",
  "<p><code>RegionRectangular</code> define <code>__contains__(self, pixel)</code>. ¿Cuál de estas expresiones lo usa?</p>",
  [mc("Respuesta", ["<code>pixel in region</code>", "<code>region in pixel</code>", "<code>region.contains(pixel)</code>", "<code>len(region)</code>", "<code>pixel == region</code>"])],
  ["El operador <code>in</code> llama al <code>__contains__</code> del objeto de la <b>derecha</b>: <code>pixel in region</code> ⇔ <code>region.__contains__(pixel)</code>.",
   "Por eso <code>encender_region</code> puede preguntar <code>if self[i][j] in region</code> sin saber qué tipo de región es: polimorfismo con un método mágico."],
  "pixel in region", "El objeto de la derecha decide.", [["dunop", "poli"], ["poli"]]))
T10.append(code_ex("pl8", 2, "Regiones circular y semiplano",
  "<p>Completa <code>__contains__</code> en las dos regiones del lab 10B (el archivo <code>libScreen.py</code> trae <code>Pixel</code> y <code>Pantalla</code>):</p><ul>"
  "<li><code>RegionCircular(x, y, radio)</code>: el pixel está si \\((x-x')^2+(y-y')^2\\le r^2\\).</li>"
  "<li><code>RegionSemiplanar(a, b, c)</code>: con la condición del lab, \\(0\\le a\\,y+b\\,x+c\\).</li></ul>",
  REG_START, REG_SOL, T_REG,
  ["Compara el cuadrado de la distancia con <code>radio ** 2</code> (así no hace falta raíz).",
   "El semiplano es una sola desigualdad. Con eso, <code>Pantalla.encender_region</code> funciona con cualquier región sin cambiar nada."],
  "Usa pixel.x y pixel.y.", [["dunop", "poli"]], files=FILES_SCR))
T10.append(code_ex("pl9", 2, "Superclase abstracta Region",
  "<p>Reimplementa las regiones como en la Fig. 4 del lab: una superclase abstracta <code>Region</code> con <code>__contains__</code> abstracto, y <code>RegionCuadrada(x, y, lado)</code> como hija concreta (incluye los pixeles con <code>x ≤ pixel.x ≤ x + lado − 1</code>, igual en y).</p>",
  ABS_START, ABS_SOL, T_ABS,
  ["<code>Region</code> hereda de <code>ABC</code> y marca <code>__contains__</code> con <code>@abstractmethod</code>: ya no se puede hacer <code>Region()</code>.",
   "Toda hija debe implementar <code>__contains__</code>; si no, Python tampoco deja crearla (TypeError)."],
  "from abc import ABC, abstractmethod", [["abc"]], files=FILES_SCR))
T10.append(output_ex("pl10", 2, "Instanciar una abstracta",
  '''from abc import ABC, abstractmethod

class Tarjeta(ABC):
    def __init__(self, saldo):
        self.saldo = saldo
    @abstractmethod
    def pagar(self, precio):
        ...

class Basica(Tarjeta):
    def pagar(self, precio):
        self.saldo -= precio

b = Basica(10)
b.pagar(4)
print(b.saldo)
t = Tarjeta(5)
print(t.saldo)''',
  [("6\n", "TypeError"), "6\n5", ("", "TypeError"), "6\nNone", ("6\n", "AttributeError")],
  ["<code>Basica</code> implementa <code>pagar</code>, así que es concreta: se crea, paga 4 e imprime 6.",
   "<code>Tarjeta(5)</code> intenta instanciar la clase abstracta: <code>TypeError: Can't instantiate abstract class Tarjeta…</code>. Lo que ya se imprimió (6) se queda."],
  "Una clase con @abstractmethod no se instancia.", [["abc"], ["abc"]]))
T10.append(code_ex("pl11", 2, "PantallaV2",
  "<p>Crea <code>PantallaV2</code>, que hereda de <code>Pantalla</code> (en <code>libScreen.py</code>) y agrega <code>encender_todo()</code>, <code>apagar_todo()</code> e <code>invertir_todo()</code>.</p>",
  V2_START, V2_SOL, T_V2,
  ["Hereda todo de <code>Pantalla</code> (constructor, <code>__str__</code>, <code>encender_region</code>) y solo agrega los tres métodos.",
   "Cada uno recorre <code>self.pixeles</code> fila por fila y le pide a cada <code>Pixel</code> que se encienda, apague o invierta: la pantalla no toca <code>activo</code> directamente."],
  "Recorre self.pixeles.", [["her", "poli"]], files=FILES_SCR))

TOOLS10 = [paso(POLY_LOOP, "Polimorfismo paso a paso", "Avanza línea por línea: el mismo t.pagar(120) entra a métodos distintos según la tarjeta.")]

# =====================================================================
# Semana 11 · Excepciones
# =====================================================================
T11_teo = (
 "<p>Una <strong>excepción</strong> es un error que ocurre mientras el programa corre. Si nadie la atiende, el programa se detiene y muestra el <i>traceback</i>. Las más comunes:</p>"
 "<div class=\"tbl\"><table><tr><th>Excepción</th><th>Cuándo aparece</th><th>Ejemplo</th></tr>"
 "<tr><td>ZeroDivisionError</td><td>división entre cero</td><td><code>5 / 0</code></td></tr>"
 "<tr><td>ValueError</td><td>tipo correcto pero valor inválido</td><td><code>int(\"hola\")</code></td></tr>"
 "<tr><td>TypeError</td><td>tipo de dato incorrecto</td><td><code>\"3\" + 4</code></td></tr>"
 "<tr><td>IndexError</td><td>índice fuera de rango</td><td><code>[1, 2][5]</code></td></tr>"
 "<tr><td>KeyError</td><td>clave inexistente en un diccionario</td><td><code>{\"a\": 1}[\"b\"]</code></td></tr>"
 "<tr><td>FileNotFoundError</td><td>ruta inexistente</td><td><code>open(\"no.csv\")</code></td></tr>"
 "<tr><td>ModuleNotFoundError</td><td>importar algo que no existe</td><td><code>import numpi</code></td></tr>"
 "<tr><td>StopIteration</td><td>un iterador sin más elementos</td><td><code>next(iter([]))</code></td></tr></table></div>"
 "<p><strong>Gestionarlas:</strong></p>"
 + pre('try:\n    x = int(texto)          # código que puede fallar\nexcept ValueError:\n    print("no es número")   # solo si falló con ValueError\nexcept (TypeError, KeyError) as e:\n    print("otro error:", e)\nelse:\n    print("todo bien")       # solo si NO hubo excepción\nfinally:\n    print("siempre")         # pase lo que pase')
 + "<p>Se revisan los <code>except</code> de arriba hacia abajo y entra al <b>primero</b> que coincide (también coincide con una clase madre: <code>except Exception</code> atrapa casi todo). Si ninguno coincide, la excepción sigue subiendo a quien llamó a la función.</p>"
 "<p><strong>Lanzarlas:</strong> <code>raise ValueError(\"el nombre no puede estar vacío\")</code>. <strong>Propias:</strong> se crean heredando de <code>Exception</code>: <code>class SaldoInsuficiente(Exception): pass</code>.</p>"
)
T11_form = ["<code>try / except Tipo / else / finally</code>",
            "Entra al primer except que coincide (las madres también coinciden)",
            "else: si no hubo error · finally: siempre",
            "<code>raise ValueError(\"mensaje\")</code>",
            "Propia: <code>class MiError(Exception): pass</code>",
            "<code>except Tipo as e</code> → <code>str(e)</code> es el mensaje"]
T11_lesson = (
 "<h3>Idea central</h3><p>Las excepciones separan el camino normal del camino de error: el método que detecta el problema lo <b>lanza</b> (<code>raise</code>) y quien sabe qué hacer lo <b>atiende</b> (<code>try/except</code>), aunque esté varias llamadas más arriba.</p>"
 "<h3>Cuándo usar cada parte</h3><ul><li><b>raise</b> en tus clases para rechazar datos inválidos (nombre vacío, puntaje no entero).</li><li><b>try/except</b> donde puedes reaccionar: pedir otro dato, usar un valor por defecto, avisar al usuario.</li><li><b>finally</b> para cerrar archivos o liberar algo pase lo que pase.</li></ul>"
 "<div class=\"err\"><b>Errores frecuentes:</b> poner <code>except Exception</code> antes de los específicos (los de abajo nunca se alcanzan); atrapar un tipo equivocado (el programa igual se cae); usar un <code>except:</code> vacío que esconde errores de verdad; y confundir <code>raise</code> (lanza) con <code>return</code> (devuelve).</div>"
)

FLOW = '''def dividir(a, b):
    try:
        r = a // b
    except ZeroDivisionError:
        print("division entre cero")
        r = None
    else:
        print("ok")
    finally:
        print("fin")
    return r

print(dividir(7, 2))
print(dividir(7, 0))'''
ORD = '''def convertir(s):
    try:
        return int(s)
    except Exception:
        return "otro"
    except ValueError:
        return "valor"

print(convertir("12"), convertir("doce"), convertir(None))'''
PROP = '''def leer(d, k):
    print("leyendo", k)
    return d[k]

def total(d):
    try:
        return leer(d, "a") + leer(d, "b")
    except KeyError as e:
        print("falta", e)
        return 0
    finally:
        print("listo")

print(total({"a": 1, "b": 2}))
print(total({"a": 1}))'''
BUGEXC = '''def pedir_edad(texto):
    try:
        edad = int(texto)
    except TypeError:
        print("Escribe un numero")
        return None
    return edad

print(pedir_edad("20"))
print(pedir_edad("veinte"))'''

JUG_START = '''class Jugador:
    def __init__(self, nombre, puntaje=0):
        # completa: valida y guarda
        self.nombre = nombre
        self.puntaje = puntaje

    def get_puntaje(self):
        return self.puntaje

    def set_puntaje(self, p):
        self.puntaje = p

    def aumentar(self, p):
        self.puntaje += p

    def reducir(self, p):
        self.puntaje -= p
'''
JUG_SOL = '''class Jugador:
    def __init__(self, nombre, puntaje=0):
        if not isinstance(nombre, str):
            raise TypeError("el nombre debe ser una cadena")
        if nombre == "":
            raise ValueError("el nombre no puede estar vacio")
        self.nombre = nombre
        self.set_puntaje(puntaje)

    @staticmethod
    def _entero(p):
        if not isinstance(p, int) or isinstance(p, bool):
            raise TypeError("el puntaje debe ser un entero")

    def get_puntaje(self):
        return self.puntaje

    def set_puntaje(self, p):
        self._entero(p)
        self.puntaje = p

    def aumentar(self, p):
        self._entero(p)
        self.puntaje += p

    def reducir(self, p):
        self._entero(p)
        self.puntaje -= p
'''
PROBE = 'def prueba(f):\n    try:\n        f()\n        print("ok")\n    except Exception as e:\n        print(type(e).__name__)\n'
T_JUG = [{"n": "Nombre", "run": PROBE + 'prueba(lambda: Jugador(5))\nprueba(lambda: Jugador(""))\nprueba(lambda: Jugador("Ana"))', "out": "TypeError\nValueError\nok"},
         {"n": "Puntaje entero", "run": PROBE + 'prueba(lambda: Jugador("Ana", 2.5))\nj = Jugador("Ana", 10)\nprueba(lambda: j.aumentar("3"))\nprueba(lambda: j.set_puntaje(None))\nprint(j.get_puntaje())', "out": "TypeError\nTypeError\nTypeError\n10"},
         {"n": "Sin errores", "run": 'j = Jugador("Luis", 5)\nj.aumentar(10)\nj.reducir(3)\nprint(j.get_puntaje())', "out": "12"}]

REG_FILES = {"jugadores.csv": "Ana,30\nLuis,20\nRosa,40\n"}
REGI_START = JUG_SOL + '''

class Registro:
    def __init__(self):
        self.jugadores = []

    # completa: agregar(jugador), cargar_csv(ruta), promediar_puntajes(), __str__
'''
REGI_SOL = JUG_SOL + '''

class Registro:
    def __init__(self):
        self.jugadores = []

    def agregar(self, jugador):
        if not isinstance(jugador, Jugador):
            raise TypeError("solo se agregan objetos Jugador")
        self.jugadores.append(jugador)

    def cargar_csv(self, ruta):
        try:
            with open(ruta) as f:
                for linea in f:
                    nombre, puntaje = linea.strip().split(",")
                    self.agregar(Jugador(nombre, int(puntaje)))
            return True
        except FileNotFoundError:
            return False

    def promediar_puntajes(self):
        try:
            return sum(j.get_puntaje() for j in self.jugadores) / len(self.jugadores)
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return "\\n".join(f"{j.nombre}: {j.get_puntaje()}" for j in self.jugadores)
'''
T_REGI = [{"n": "Cargar y promediar", "run": 'r = Registro()\nprint(r.cargar_csv("jugadores.csv"))\nprint(r)\nprint(r.promediar_puntajes())', "out": "True\nAna: 30\nLuis: 20\nRosa: 40\n30.0"},
          {"n": "Ruta inexistente y lista vacía", "run": 'r = Registro()\nprint(r.cargar_csv("no_existe.csv"), r.promediar_puntajes())', "out": "False 0"},
          {"n": "Agregar algo que no es Jugador", "run": 'r = Registro()\ntry:\n    r.agregar("Ana")\nexcept TypeError:\n    print("TypeError")\nr.agregar(Jugador("Beto", 7))\nprint(r)', "out": "TypeError\nBeto: 7"}]

SALDO_START = '''class SaldoInsuficiente(Exception):
    pass


class DogeCard:
    def __init__(self, saldo):
        self.saldo = saldo

    def pagar(self, precio):
        # completa: si no alcanza, lanza SaldoInsuficiente con el mensaje "faltan X"
        self.saldo -= precio


def comprar(tarjeta, precios):
    # completa: intenta pagar cada precio; cuenta las compras hechas y
    # por cada fallo imprime el mensaje de la excepción; devuelve cuántas se hicieron
    pass
'''
SALDO_SOL = '''class SaldoInsuficiente(Exception):
    pass


class DogeCard:
    def __init__(self, saldo):
        self.saldo = saldo

    def pagar(self, precio):
        if precio > self.saldo:
            raise SaldoInsuficiente(f"faltan {precio - self.saldo}")
        self.saldo -= precio


def comprar(tarjeta, precios):
    hechas = 0
    for p in precios:
        try:
            tarjeta.pagar(p)
            hechas += 1
        except SaldoInsuficiente as e:
            print(e)
    return hechas
'''
T_SALDO = [{"n": "Lanza la excepción propia", "run": 'd = DogeCard(50)\ntry:\n    d.pagar(80)\nexcept SaldoInsuficiente as e:\n    print("Atrapada:", e, d.saldo)', "out": "Atrapada: faltan 30 50"},
           {"n": "Es una Exception", "run": 'print(issubclass(SaldoInsuficiente, Exception))', "out": "True"},
           {"n": "Comprar varias", "run": 'd = DogeCard(100)\nprint(comprar(d, [60, 50, 30, 20]), d.saldo)', "out": "faltan 10\nfaltan 10\n2 10"}]

VAL_START = '''def validar(texto):
    # completa:
    #  - TypeError si texto no es str
    #  - ValueError("vacio") si está vacío (o solo espacios)
    #  - ValueError("largo") si tiene más de 10 caracteres
    #  - si es válido, devuelve el texto en mayúsculas
    pass
'''
VAL_SOL = '''def validar(texto):
    if not isinstance(texto, str):
        raise TypeError("se esperaba texto")
    if texto.strip() == "":
        raise ValueError("vacio")
    if len(texto) > 10:
        raise ValueError("largo")
    return texto.upper()
'''
T_VAL = [{"n": "Válido", "run": 'print(validar("utec"))', "out": "UTEC"},
         {"n": "Errores", "run": 'for x in [123, "   ", "programacion"]:\n    try:\n        validar(x)\n    except (TypeError, ValueError) as e:\n        print(type(e).__name__, e)', "out": "TypeError se esperaba texto\nValueError vacio\nValueError largo"}]

T11 = []
T11.append(ex("ex1", 1, "¿Qué excepción sale? (1)",
  "<p>Clasifica cada línea según la excepción que lanza.</p>",
  [{"t": "cls", "cats": ["ZeroDivisionError", "ValueError", "TypeError", "IndexError"], "items": [
    {"x": "<code>10 % 0</code>", "c": 0}, {"x": "<code>float(\"3,5\")</code>", "c": 1, "e": "Es un texto (tipo correcto) con un valor que no se puede convertir: ValueError."},
    {"x": "<code>len(5)</code>", "c": 2}, {"x": "<code>\"abc\"[3]</code>", "c": 3}, {"x": "<code>[0] * \"2\"</code>", "c": 2},
    {"x": "<code>int(\"\")</code>", "c": 1}, {"x": "<code>(1, 2)[-3]</code>", "c": 3}]}],
  ["ValueError: el tipo es el que la función espera, pero el <b>valor</b> no sirve (<code>int(\"\")</code>, <code>float(\"3,5\")</code>).",
   "TypeError: el <b>tipo</b> no sirve para esa operación (<code>len(5)</code>, lista por texto). IndexError: posición fuera de rango, también con negativos."],
  "Clasificación correcta", "¿Falla el tipo o el valor?", [["exc"], ["exc"]]))
o_ = []
for code, nm in [('{"a": 1}["A"]', "KeyError"), ('open("datos_2026.csv")', "FileNotFoundError"), ('import matplotlibb', "ModuleNotFoundError"), ('next(iter([]))', "StopIteration"), ('{}.pop("x")', "KeyError")]:
    _, exc = run(code); assert exc == nm, (code, exc)
T11.append(ex("ex2", 1, "¿Qué excepción sale? (2)",
  "<p>Clasifica cada línea según la excepción que lanza.</p>",
  [{"t": "cls", "cats": ["KeyError", "FileNotFoundError", "ModuleNotFoundError", "StopIteration"], "items": [
    {"x": "<code>{\"a\": 1}[\"A\"]</code>", "c": 0, "e": "Las claves distinguen mayúsculas: \"A\" no existe."}, {"x": "<code>open(\"datos_2026.csv\")</code>", "c": 1},
    {"x": "<code>import matplotlibb</code>", "c": 2}, {"x": "<code>next(iter([]))</code>", "c": 3}, {"x": "<code>{}.pop(\"x\")</code>", "c": 0}]}],
  ["KeyError: clave inexistente (también con <code>pop</code>). FileNotFoundError: abrir para leer un archivo que no existe.",
   "ModuleNotFoundError: importar un módulo mal escrito o no instalado. StopIteration: pedir <code>next</code> a un iterador agotado (el for la atrapa solo)."],
  "Clasificación correcta", "Mira qué se está pidiendo.", [["exc"], ["exc"]]))
T11.append(output_ex("ex3", 2, "try, except, else y finally", FLOW,
  ["ok\nfin\n3\ndivision entre cero\nfin\nNone", "ok\n3\ndivision entre cero\nNone", "fin\n3\ndivision entre cero\nfin\nNone",
   "ok\nfin\n3\ndivision entre cero\nok\nfin\nNone", "ok\nfin\n3\ndivision entre cero\nNone\nfin"],
  ["<code>dividir(7, 2)</code>: no hay error → corre <code>else</code> («ok») y luego <code>finally</code> («fin»); devuelve 3.",
   "<code>dividir(7, 0)</code>: <code>7 // 0</code> lanza ZeroDivisionError → entra al except, <b>no</b> al else, y el <code>finally</code> corre igual antes del return; devuelve None."],
  "finally siempre; else solo sin error.", [["exc"], ["finally"]]))
T11.append(output_ex("ex4", 2, "El orden de los except", ORD,
  ["12 otro otro", "12 valor otro", "12 valor valor", "12 otro valor", ("", "TypeError")],
  ["Los <code>except</code> se revisan de arriba hacia abajo. <code>ValueError</code> es hija de <code>Exception</code>, así que el primero ya la atrapa: <code>\"doce\"</code> → «otro».",
   "<code>int(None)</code> da TypeError, que también atrapa <code>except Exception</code>. El <code>except ValueError</code> nunca se alcanza: los específicos van <b>antes</b> que los generales."],
  "El primero que coincide gana.", [["exc"], ["exc"]]))
T11.append(output_ex("ex5", 3, "La excepción sube", PROP,
  ["leyendo a\nleyendo b\nlisto\n3\nleyendo a\nleyendo b\nfalta 'b'\nlisto\n0",
   "leyendo a\nleyendo b\nlisto\n3\nleyendo a\nfalta 'b'\nlisto\n0",
   "leyendo a\nleyendo b\n3\nleyendo a\nleyendo b\nfalta 'b'\n0",
   ("leyendo a\nleyendo b\nlisto\n3\nleyendo a\nleyendo b\n", "KeyError"),
   "leyendo a\nleyendo b\nlisto\n3\nleyendo a\nleyendo b\nfalta b\nlisto\n0"],
  ["<code>leer</code> no tiene try: el KeyError de <code>d[\"b\"]</code> <b>sube</b> hasta <code>total</code>, que sí lo atrapa. Antes, «leyendo b» ya se imprimió.",
   "<code>print(\"falta\", e)</code> muestra la clave entre comillas (<code>'b'</code>, así es el texto de un KeyError) y el <code>finally</code> imprime «listo» en los dos casos."],
  "Una excepción sale de la función hasta un try.", [["exc"], ["finally"]]))
T11.append(ex("ex6", 2, "Encuentra el error",
  "<p>Este programa se cae con el segundo <code>print</code>.</p>",
  [bug(BUGEXC, lineof(BUGEXC, "except TypeError"), ["int(\"veinte\") lanza ValueError, no TypeError: ese except no la atrapa",
       "Falta un else después del except", "return None no se puede usar dentro de except", "int() no puede recibir texto", "Hay que poner finally para que no se caiga"],
       "20\nValueError: invalid literal for int() with base 10: 'veinte'",
       e="¿Qué excepción lanza int con un texto que no es número?")],
  ["<code>int(\"veinte\")</code> recibe un texto (tipo correcto) con un valor imposible: lanza <b>ValueError</b>.",
   "El <code>except TypeError</code> no coincide, así que el error sigue subiendo y el programa se detiene. Corrección: <code>except ValueError:</code>."],
  "except ValueError", "Tipo correcto, valor malo.", [["exc"], ["exc"]]))
T11.append(ex("ex7", 1, "raise vs. return",
  "<p>¿Qué hace <code>raise ValueError(\"vacío\")</code> dentro de un método?</p>",
  [mc("Respuesta", ["Detiene el método y lanza la excepción hacia quien lo llamó, hasta que un try la atrape", "Devuelve el texto \"vacío\" como resultado",
                     "Imprime \"vacío\" y sigue con la siguiente línea", "Solo funciona dentro de un try", "Crea una variable ValueError con el valor \"vacío\""])],
  ["<code>raise</code> interrumpe la función en esa línea; no devuelve nada. La excepción viaja hacia arriba por las llamadas.",
   "Si algún <code>try</code> la atrapa, el programa sigue desde su <code>except</code>; si nadie lo hace, el programa termina con el traceback y el mensaje «vacío»."],
  "Lanza la excepción hacia arriba", "raise no es return.", [["raise"], ["raise"]]))
T11.append(code_ex("ex8", 2, "Jugador con validaciones (lab 11B)",
  "<p>Modifica <code>Jugador</code> para que lance excepciones:</p><ul>"
  "<li><code>TypeError</code> si el nombre no es una cadena; <code>ValueError</code> si es la cadena vacía.</li>"
  "<li><code>TypeError</code> si el puntaje (en el constructor, <code>set_puntaje</code>, <code>aumentar</code> o <code>reducir</code>) no es un <code>int</code>.</li></ul>",
  JUG_START, JUG_SOL, T_JUG,
  ["Valida el nombre con <code>isinstance(nombre, str)</code> y luego que no sea <code>\"\"</code>; el orden importa (primero el tipo).",
   "Para no repetir la validación del puntaje en cuatro métodos, ponla en un método auxiliar y llámalo desde todos (también desde el constructor, usando <code>set_puntaje</code>)."],
  "raise TypeError(\"…\") cuando el tipo no sirve.", [["raise"], ["raise"]]))
T11.append(code_ex("ex9", 3, "Registro de jugadores",
  "<p>Completa <code>Registro</code> (el <code>Jugador</code> del ejercicio anterior ya está):</p><ul>"
  "<li><code>agregar(j)</code>: lanza <code>TypeError</code> si <code>j</code> no es un <code>Jugador</code>.</li>"
  "<li><code>cargar_csv(ruta)</code>: lee líneas <code>nombre,puntaje</code>; devuelve <code>True</code>, o <code>False</code> si el archivo no existe (try/except).</li>"
  "<li><code>promediar_puntajes()</code>: el promedio, o <code>0</code> si no hay jugadores (atrapa <code>ZeroDivisionError</code>).</li>"
  "<li><code>__str__</code>: una línea <code>Ana: 30</code> por jugador.</li></ul>",
  REGI_START, REGI_SOL, T_REGI,
  ["<code>cargar_csv</code> envuelve el <code>open</code> en un try con <code>except FileNotFoundError</code>; cada línea se separa con <code>split(\",\")</code> y el puntaje se convierte con <code>int</code>.",
   "El promedio divide entre <code>len(self.jugadores)</code>: con la lista vacía lanza ZeroDivisionError, que se atrapa para devolver 0."],
  "Un try por cada fuente de error.", [["exc", "file"], ["exc"]], files=REG_FILES))
T11.append(code_ex("ex10", 2, "Una excepción propia",
  "<p>Crea la excepción <code>SaldoInsuficiente</code> y úsala en la DogeCard:</p><ul>"
  "<li><code>pagar(precio)</code> lanza <code>SaldoInsuficiente(\"faltan X\")</code> si el precio supera el saldo (X = lo que falta); si no, descuenta.</li>"
  "<li><code>comprar(tarjeta, precios)</code> intenta pagar cada precio, imprime el mensaje de cada fallo y devuelve cuántas compras se hicieron.</li></ul>",
  SALDO_START, SALDO_SOL, T_SALDO,
  ["Una excepción propia es una clase que hereda de <code>Exception</code>; con <code>pass</code> basta.",
   "<code>pagar</code> la lanza con <code>raise</code>; <code>comprar</code> la atrapa con <code>except SaldoInsuficiente as e</code> y sigue con el siguiente precio."],
  "class SaldoInsuficiente(Exception): pass", [["excprop"], ["excprop", "raise"]]))
T11.append(code_ex("ex11", 2, "Lanzando excepciones (lab 11A)",
  "<p>Escribe <code>validar(texto)</code>: lanza <code>TypeError</code> si no es <code>str</code>, <code>ValueError(\"vacio\")</code> si está vacío o solo tiene espacios y <code>ValueError(\"largo\")</code> si tiene más de 10 caracteres. Si es válido, devuelve el texto en mayúsculas.</p>",
  VAL_START, VAL_SOL, T_VAL,
  ["Revisa primero el tipo (si no es texto, <code>strip</code> y <code>len</code> ni siquiera tendrían sentido).",
   "Cada condición inválida termina con su <code>raise</code>; al final, el camino feliz devuelve <code>texto.upper()</code>."],
  "Un if con raise por cada condición.", [["raise"], ["raise"]]))

TOOLS11 = [paso(FLOW, "try / except / else / finally paso a paso", "Mira por dónde pasa la ejecución con 7 // 2 y con 7 // 0."),
           paso(PROP, "Una excepción que sube", "El KeyError nace en leer() y lo atrapa total().")]

# =====================================================================
# Ensamblar
# =====================================================================
d['concepts'].update({
 "abc": {"n": "Clase abstracta (abc)", "f": "<code>class R(ABC)</code> + <code>@abstractmethod</code>", "x": "No se instancia; las hijas deben implementar todos los métodos abstractos.", "home": "w10pol"},
 "exc": {"n": "Excepciones", "f": "<code>try / except Tipo</code>", "x": "Se atrapa con el primer except que coincide; si no, sube a quien llamó.", "home": "w11exc"},
 "finally": {"n": "else y finally", "f": "else: sin error · finally: siempre", "x": "finally corre incluso si hay return o una excepción.", "home": "w11exc"},
 "raise": {"n": "raise", "f": "<code>raise ValueError(\"mensaje\")</code>", "x": "Interrumpe la función y lanza la excepción hacia arriba.", "home": "w11exc"},
 "excprop": {"n": "Excepciones propias", "f": "<code>class MiError(Exception): pass</code>", "x": "Se lanzan con raise y se atrapan por su nombre.", "home": "w11exc"}})
d['concepts']['poli']['home'] = 'w10pol'

T10top = {"id": "w10pol", "name": "Sem. 10 · Polimorfismo y clases abstractas", "teo": T10_teo, "form": T10_form, "lesson": T10_lesson, "ex": T10, "tools": TOOLS10}
T11top = {"id": "w11exc", "name": "Sem. 11 · Excepciones: try, except, raise y excepciones propias", "teo": T11_teo, "form": T11_form, "lesson": T11_lesson, "ex": T11, "tools": TOOLS11}
for t in d['topics']:
    if t['id'] == 'w9mul':
        t['ex'] = [e for e in t['ex'] if e['id'] != 'm9']
        k = next(i for i, e in enumerate(t['ex']) if e['id'] == 'm4')
        t['ex'].insert(k, M9)
d['topics'] = [t for t in d['topics'] if t['id'] not in ('w10pol', 'w11exc')] + [T10top, T11top]
allc = set(d['concepts'])
for t in d['topics']:
    for e in t['ex']:
        for s in e['tags']:
            for k in s: assert k in allc, (e['id'], k)

CARDS = ('<div><b>Polimorfismo</b><br>mismo método, cada clase con su versión · <code>super().metodo()</code> · <code>x in obj</code> → <code>__contains__</code></div>'
         '<div><b>Abstracta</b><br><code>class R(ABC)</code> · <code>@abstractmethod</code> · <code>R()</code> → TypeError</div>'
         '<div><b>Excepciones</b><br><code>try / except T as e / else / finally</code> · el primer except que coincide · <code>raise T(\"msg\")</code> · <code>class E(Exception)</code></div>')
if 'Excepciones</b>' not in d['form']:
    k = d['form'].rindex('</div>')
    d['form'] = d['form'][:k] + CARDS + d['form'][k:]

d['intro'] = ('<b>El simulacro puede ser escrito o en computadora</b> y todas sus preguntas son de escribir código. Repaso acumulado del curso, con los temas ordenados por semana y todos abiertos desde el inicio. '
              '<b>El examen final (teoría) vale 30 %</b> y es en la semana 16; el simulacro pone el énfasis en las semanas 9 en adelante (herencia, polimorfismo y clases abstractas, y excepciones) '
              'y una parte menor de repaso de las semanas 1 a 8. Se actualiza cada vez que se agrega una semana nueva.')
SL = [{"pts": 4, "name": "Repaso sem. 1–8: sobrecarga y relaciones", "pool": ["fop9", "fre6", "fre9"]},
      {"pts": 5, "name": "Sem. 9: herencia, super() y herencia múltiple", "pool": ["h7", "h8", "fx_emp", "m8", "fx_fig"]},
      {"pts": 5, "name": "Sem. 10: polimorfismo y clases abstractas", "pool": ["pl3", "pl8", "pl9", "pl11"]},
      {"pts": 6, "name": "Sem. 11: excepciones", "pool": ["ex8", "ex9", "ex10", "ex11"]}]
assert sum(s['pts'] for s in SL) == 20
INTRO = "Todas las preguntas son de <b>escribir código</b>. Simulacro acumulativo del examen final: una pregunta de repaso de las semanas 1 a 8 y tres de las semanas 9 a 11 (herencia, polimorfismo y excepciones). Se actualiza cada semana."
d['sim']['slots'] = SL; d['sim']['intro'] = INTRO
v0, v1 = d['sim']['versions']
v0.update({"slots": SL, "intro": INTRO, "desc": "Cuatro problemas de código; puedes ejecutar mientras resuelves."})
v1.update({"slots": SL, "intro": INTRO + " <b>Modo escrito:</b> no puedes ejecutar; se prueba al entregar."})
allex = [e['id'] for t in d['topics'] for e in t['ex']] + [e['id'] for e in d.get('simEx', [])]
assert len(allex) == len(set(allex)), 'ids repetidos'
for v in [d['sim']] + d['sim']['versions']:
    for s in v['slots']:
        for i in s['pool']: assert i in allex, i

with open(F, 'w', encoding='utf-8') as o:
    json.dump(d, o, indent=1, ensure_ascii=False); o.write('\n')
print('ok', len(T10), len(T11))
