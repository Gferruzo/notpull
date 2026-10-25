#!/usr/bin/env python3
"""Semana 11 de Programación II (CS1112): herencia, funciones virtuales y clases abstractas → cursos/p2-ef.json.
Compila con g++ cada «¿qué imprime?», cada solución modelo contra sus pruebas y comprueba que los «encuentra el error» de verdad fallen.
Uso: python3 tools/p2_s11.py   (reejecutable: reemplaza los temas w11her y w11vir)."""
import json, subprocess, tempfile, os, html

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(REPO, 'cursos', 'p2-ef.json')
d = json.load(open(F, encoding='utf-8'))

def esc(s): return html.escape(s, quote=False)
def pre(code): return '<pre class="cpp"><code>' + esc(code) + '</code></pre>'
def out(s): return '<code class="out">' + esc(s) + '</code>'

def compile_cpp(src, run=True):
    with tempfile.TemporaryDirectory() as t:
        p = os.path.join(t, 'a.cpp'); open(p, 'w').write(src)
        r = subprocess.run(['g++', '-std=gnu++17', '-O0', '-o', os.path.join(t, 'a'), p], capture_output=True, text=True)
        if r.returncode != 0: return None, r.stderr
        if not run: return '', ''
        r = subprocess.run([os.path.join(t, 'a')], capture_output=True, text=True, timeout=10)
        assert r.returncode == 0, ('exit', r.returncode, r.stderr)
        return r.stdout, ''

def run_cpp(src):
    o, err = compile_cpp(src); assert o is not None, err; return o

def norm(s): return '\n'.join(l.rstrip() for l in s.strip('\n').split('\n'))

def check_code(start, sol, tests):
    for t in tests:
        src = sol + '\n#include <iostream>\nint main(){\n{ using namespace std;\n' + t['main'] + '\n}\nreturn 0;}\n'
        got = run_cpp(src)
        assert norm(got) == norm(t['out']), ('test', t['n'], repr(got), repr(t['out']))
    with tempfile.TemporaryDirectory() as tdir:
        p = os.path.join(tdir, 's.cpp'); open(p, 'w').write(start + '\nint main(){return 0;}\n')
        r = subprocess.run(['g++', '-std=gnu++17', '-fsyntax-only', p], capture_output=True, text=True)
        assert r.returncode == 0, ('start no compila', r.stderr)

def ex(id, lvl, title, q, checks, steps, ans, hint, tags, play=None, chain=False):
    e = {"id": id, "lvl": lvl, "title": title, "q": q, "checks": checks, "steps": steps, "ans": ans, "hint": hint,
         "fig": None, "draw": False, "open": False, "solfig": None, "tags": tags, "lang": "cpp"}
    if play: e["play"] = play
    if chain: e["chain"] = True
    assert len(tags) == len(steps), (id, 'tags/steps')
    return e

def mc(p, opts):
    assert len(opts) == 5 and len(set(opts)) == 5, opts
    return {"p": p, "o": opts}

def code_ex(id, lvl, title, q, start, sol, tests, steps_pre, hint, tags):
    check_code(start, sol, tests)
    steps = steps_pre + ['Una solución posible:' + pre(sol)]
    return ex(id, lvl, title, q, [{"t": "code", "lang": "cpp", "p": "Escribe tu código y compruébalo con las pruebas", "start": start, "tests": tests}],
              steps, "Tu código pasa todas las pruebas", hint, tags + [tags[-1]])

def output_ex(id, lvl, title, prog, outs, steps, hint, tags):
    got = run_cpp(prog)
    assert norm(got) == norm(outs[0]), (id, repr(got), repr(outs[0]))
    assert len(set(norm(o) for o in outs)) == len(outs), (id, 'distractores repetidos')
    return ex(id, lvl, title, pre(prog) + '<p>¿Qué imprime este programa?</p>', [mc('Salida', [out(o) for o in outs])],
              steps, out(outs[0]), hint, tags, play=prog)

def bug_check(code, lines, opts, outtxt, must_fail=True, e=None):
    """El código malo: si must_fail, debe NO compilar; si no, debe compilar (el error es de lógica)."""
    o, err = compile_cpp(code, run=not must_fail)
    if must_fail: assert o is None, ('debía no compilar', code)
    else: assert o is not None, err
    assert len(opts) == 5 and len(set(opts)) == 5
    c = {"t": "bug", "p": "Encuentra el error", "code": code, "l": lines, "o": opts, "out": outtxt}
    if e: c["e"] = e
    return c

def lineof(code, text, k=1):
    L = [i + 1 for i, l in enumerate(code.split('\n')) if text in l]
    return L[k - 1]

def virt(p, want, sol, ini=None, lock=None, e=None, **kw):
    c = {"t": "virt", "p": p, "B": kw.get("B", "Animal"), "D": kw.get("D", "Perro"), "m": kw.get("m", "hablar"), "bo": kw.get("bo", "..."), "do": kw.get("do", "Guau"),
         "ini": ini or {"vm": False, "pure": False, "vd": False, "ptr": "B", "obj": "D"}, "lock": lock or [], "want": want, "sol": sol}
    if e: c["e"] = e
    return c

HDR = '#include <iostream>\n#include <string>\nusing namespace std;\n\n'

# =====================================================================
# TEMA A · Herencia
# =====================================================================
A_teo = (
 "<p><b>Herencia</b> es la relación <b>«es un»</b>: una <i>subclase</i> (clase derivada, hija) hereda todos los atributos y métodos de una <i>superclase</i> (clase base, padre) y puede agregar los suyos. Sirve para no repetir código. Se valida con la frase: un pájaro <i>es un</i> animal, un ingeniero <i>es una</i> persona, un autobús <i>es un</i> medio de transporte terrestre (y, a su vez, un medio de transporte).</p>"
 "<p>En UML se dibuja con una línea y un <b>triángulo vacío</b> que apunta a la clase base.</p>"
 "<p><b>Sintaxis:</b> <code>class Ingeniero : public Persona { … };</code>. El nivel de acceso de la herencia (<code>public</code>, <code>protected</code> o <code>private</code>) limita cómo quedan los miembros heredados; con <code>public</code> (el habitual) conservan su visibilidad.</p>"
 "<div class=\"tbl\"><table><tr><th>Miembro en la base</th><th>¿Lo usa la derivada?</th><th>¿Lo usa el main?</th></tr>"
 "<tr><td><code>public</code></td><td>sí</td><td>sí</td></tr><tr><td><code>protected</code></td><td>sí</td><td>no</td></tr><tr><td><code>private</code></td><td>no (solo con getters)</td><td>no</td></tr></table></div>"
 "<p><b>Constructores:</b> la subclase define los suyos. Al crear un objeto derivado, <b>primero se construye la parte de la base</b>: el constructor de la derivada llama al de la base en la <b>lista de inicialización</b>: <code>Ingeniero(string n, int e, string t) : Persona(n, e) { titulo = t; }</code>. Si no lo llamas, el compilador llama al constructor por defecto de la base (y si no existe, no compila). Los destructores corren al revés: primero el de la derivada y luego el de la base.</p>"
 "<p>Para usar la versión de la base de un método que la derivada sobrescribe: <code>Persona::mostrar();</code> (operador de resolución de ámbito).</p>"
 "<div class=\"err\"><b>Ojo con las láminas:</b> en el ejemplo, el constructor de <code>Persona</code> aparece como <code>CPersona(…)</code> (un constructor debe llamarse igual que su clase), <code>Ingeniero</code> declara otra vez <code>string nombre</code> (esconde el de la base y queda vacío), el constructor asigna a <code>título</code> con tilde aunque el atributo es <code>titulo</code>, y <code>get_nombre() const</code> se define con <code>const</code> pero se declara sin él. Ninguno de esos códigos compila o funciona tal cual: abajo están corregidos.</div>"
)
A_form = ["Herencia: «es un» · <code>class D : public B { … };</code> · triángulo △ hacia la base",
          "Constructor: <code>D(…) : B(…) { … }</code> · primero la base, luego la derivada",
          "Destructores: al revés (derivada, luego base)",
          "<code>protected</code>: lo ve la derivada, no el main · <code>private</code>: solo la base",
          "Versión de la base: <code>B::metodo()</code>"]
A_lesson = (
 "<h3>Idea central</h3><p>Un objeto derivado <b>contiene</b> un objeto base adentro: por eso la base se construye primero y se destruye al final, y por eso un <code>Ingeniero</code> puede usarse donde se pide una <code>Persona</code>.</p>"
 "<h3>Receta para escribir una subclase</h3><ol><li><code>class Hija : public Padre {</code> con solo los atributos nuevos.</li><li>Constructor con lista de inicialización: <code>Hija(…) : Padre(…), nuevo(x) {}</code>.</li><li>Sobrescribe lo que cambia (mismo nombre y parámetros) y reutiliza lo de la base con <code>Padre::metodo()</code>.</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes:</b> volver a declarar en la hija un atributo que ya está en la base (queda duplicado y el de la base nunca se llena); querer usar un atributo <code>private</code> de la base desde la hija (hazlo <code>protected</code> o usa un getter); y olvidar llamar al constructor de la base cuando esta no tiene constructor por defecto.</div>"
)

P_BASE = '''class Persona {
private:
    string nombre;
protected:
    int edad;
public:
    Persona(string n, int e) : nombre(n), edad(e) {}
    string getNombre() const { return nombre; }
};'''

A_ex = []
A_ex.append(ex("p11h1", 1, "¿Herencia u otra relación?",
  "<p>Clasifica cada pareja con las frases «es un», «es parte de» y «usa un».</p>",
  [{"t": "cls", "cats": ["Herencia («es un»)", "Composición («es parte de»)", "Asociación («usa un»)"], "items": [
    {"x": "Gato – Mamífero", "c": 0}, {"x": "Ingeniero – Persona", "c": 0}, {"x": "Lancha – Medio de transporte marítimo", "c": 0},
    {"x": "Motor – Auto", "c": 1, "e": "El motor es parte del auto, no «es un» auto."}, {"x": "Fecha – Evento", "c": 1},
    {"x": "Chofer – Taxi", "c": 2, "e": "El taxi usa un chofer; ninguno «es un» el otro."}, {"x": "Futbolista – Persona", "c": 0}]}],
  ["Herencia solo si la frase «X es un Y» tiene sentido: un gato es un mamífero, un ingeniero es una persona.",
   "Si X es una pieza de Y, es composición (semana 10); si solo trabajan juntos, asociación."],
  "Clasificación correcta", "Prueba la frase «es un».", [["her"], ["her"]]))

A_ex.append(ex("p11h2", 1, "Sintaxis de la herencia",
  "<p>¿Cuál es la forma correcta de declarar que <code>Ingeniero</code> hereda públicamente de <code>Persona</code>?</p>",
  [mc("Respuesta", ["<code>class Ingeniero : public Persona { … };</code>", "<code>class Ingeniero extends Persona { … };</code>",
                     "<code>class Persona : public Ingeniero { … };</code>", "<code>class Ingeniero(Persona) { … };</code>", "<code>class Ingeniero :: Persona { … };</code>"])],
  ["La derivada va primero y después de los dos puntos el nivel de acceso y la base: <code>class Derivada : public Base</code>.",
   "<code>extends</code> es de Java y <code>class Ingeniero(Persona)</code> es de Python; <code>::</code> es el operador de ámbito, no de herencia."],
  "<code>class Ingeniero : public Persona</code>", "La hija va a la izquierda.", [["her"], ["her"]]))

PROG3 = HDR + '''class Vehiculo {
public:
    Vehiculo() { cout << "V+ "; }
    ~Vehiculo() { cout << "V- "; }
};

class Terrestre : public Vehiculo {
public:
    Terrestre() { cout << "T+ "; }
    ~Terrestre() { cout << "T- "; }
};

class Bus : public Terrestre {
public:
    Bus() { cout << "B+ "; }
    ~Bus() { cout << "B- "; }
};

int main() {
    Bus b;
    cout << "| ";
    return 0;
}'''
A_ex.append(output_ex("p11h3", 2, "Constructores en cadena", PROG3,
  ["V+ T+ B+ | B- T- V- ", "B+ T+ V+ | V- T- B- ", "V+ T+ B+ | V- T- B- ", "B+ | B- ", "B+ T+ V+ | B- T- V- "],
  ["Un <code>Bus</code> es un <code>Terrestre</code> que es un <code>Vehiculo</code>: para construirlo se construye primero la base más alta. Orden: V+, T+, B+.",
   "Al terminar el main se destruye en orden inverso: B-, T-, V-. Es lo mismo que con la composición: lo que se construye primero muere último."],
  "La base se construye primero.", [["ctorher"], ["ctorher"]]))

A_ex.append(ex("p11h4", 1, "Ordena las llamadas",
  "<p>Con <code>class Ingeniero : public Persona</code>, ordena lo que pasa en este bloque:</p>" + pre('{\n    Ingeniero ing("Ana", 25, "Electrónica");\n}   // aquí termina el bloque'),
  [{"t": "order", "p": "Toca los pasos en orden", "items": [
    "Se ejecuta el constructor de Persona (desde la lista de inicialización)",
    "Se ejecuta el cuerpo del constructor de Ingeniero",
    "Al cerrar la llave se ejecuta ~Ingeniero()",
    "Se ejecuta ~Persona()"]}],
  ["El constructor de Ingeniero llama primero a <code>Persona(n, e)</code> en su lista de inicialización y recién después corre su cuerpo.",
   "Al salir del bloque el objeto se destruye al revés: primero la parte derivada y luego la base."],
  "Base → derivada → ~derivada → ~base", "Piensa en una muñeca rusa.", [["ctorher"], ["ctorher"]]))

BUG5 = HDR + '''class Persona {
    string nombre;
protected:
    int edad;
public:
    CPersona(string n, int e) {
        nombre = n;
        edad = e;
    }
};

int main() {
    Persona p("Ana", 20);
    return 0;
}'''
A_ex.append(ex("p11h5", 1, "Encuentra el error (de la lámina)",
  "<p>Este código viene del ejemplo de la clase y no compila.</p>",
  [bug_check(BUG5, [lineof(BUG5, "CPersona(")], ["El constructor debe llamarse igual que la clase: Persona(…), no CPersona(…)", "Falta poner public: antes de string nombre",
     "edad no puede ser protected", "Un constructor debe devolver void", "Hay que crear el objeto con new"],
     "error: ISO C++ forbids declaration of 'CPersona' with no type")],
  ["Un constructor no tiene tipo de retorno y se llama exactamente como la clase. <code>CPersona</code> el compilador lo lee como un método sin tipo: error.",
   "Corregido: <code>Persona(string n, int e) : nombre(n), edad(e) {}</code>. Lo demás está bien: los atributos pueden ser private o protected y el objeto puede crearse en el stack."],
  "El constructor se llama como la clase", "Compara el nombre de la clase con el del constructor.", [["ctorher"], ["ctorher"]]))

BUG6 = HDR + P_BASE + '''

class Ingeniero : public Persona {
    string nombre;
    string titulo;
public:
    Ingeniero(string n, int e, string t) : Persona(n, e) { titulo = t; }
    string getNombre() const { return nombre; }
};

int main() {
    Ingeniero i("Ana", 25, "Electronica");
    cout << "[" << i.getNombre() << "]" << endl;
    return 0;
}'''
o6 = run_cpp(BUG6); assert o6 == "[]\n", repr(o6)
A_ex.append(ex("p11h6", 2, "¿Por qué sale vacío?",
  "<p>Versión corregida de la lámina: compila, pero el nombre sale vacío.</p>",
  [bug_check(BUG6, [lineof(BUG6, "string nombre;", 2)], ["Ingeniero vuelve a declarar string nombre: esconde el de Persona y nunca se llena",
     "Falta llamar a Persona(n, e) en el constructor", "getNombre() no puede ser const", "titulo debería ser protected", "Hay que imprimir con printf"],
     "[]", must_fail=False,
     e="Quita el segundo string nombre y el getNombre() de Ingeniero: se usará el de Persona.")],
  ["<code>Persona(n, e)</code> sí guarda «Ana», pero en el <code>nombre</code> de la base. Ingeniero declara <b>otro</b> <code>nombre</code> propio, vacío.",
   "Su <code>getNombre()</code> devuelve el atributo de Ingeniero (el de más adentro), por eso imprime <code>[]</code>. Solución: no repetir atributos de la base y no sobrescribir <code>getNombre()</code>."],
  "El atributo duplicado esconde el de la base", "¿Cuántos «nombre» tiene un Ingeniero?", [["her"], ["her"]]))

A_ex.append(ex("p11h7", 1, "¿Qué puede usar la derivada?",
  "<p>Con la clase <code>Persona</code> de abajo y <code>class Ingeniero : public Persona</code>, ¿qué puede escribir un método de <code>Ingeniero</code>?</p>" + pre(P_BASE),
  [mc("Respuesta", ["<code>edad + 1</code> y <code>getNombre()</code>, pero no <code>nombre</code>", "<code>nombre</code>, <code>edad</code> y <code>getNombre()</code>",
                     "Solo <code>getNombre()</code>", "<code>nombre</code> y <code>edad</code>, pero no <code>getNombre()</code>", "Nada: lo heredado solo lo usa el main"])],
  ["<code>protected</code> (edad) y <code>public</code> (getNombre) son accesibles desde la derivada.",
   "<code>private</code> (nombre) existe dentro del objeto, pero solo lo toca la propia Persona: la hija debe usar <code>getNombre()</code>."],
  "edad y getNombre(), no nombre", "private es solo de la base.", [["acceso"], ["acceso"]]))

PROG8 = HDR + '''class Persona {
protected:
    string nombre;
public:
    Persona(string n) : nombre(n) {}
    void mostrar() { cout << nombre; }
};

class Medico : public Persona {
    string esp;
public:
    Medico(string n, string e) : Persona(n), esp(e) {}
    void mostrar() {
        cout << "Dr. ";
        Persona::mostrar();
        cout << " (" << esp << ")";
    }
};

int main() {
    Medico m("Rosa", "pediatra");
    m.mostrar();
    cout << endl;
    Persona p = m;
    p.mostrar();
    return 0;
}'''
A_ex.append(output_ex("p11h8", 2, "Reutilizar el método de la base", PROG8,
  ["Dr. Rosa (pediatra)\nRosa", "Dr. Rosa (pediatra)\nDr. Rosa (pediatra)", "Rosa (pediatra)\nRosa", "Dr. (pediatra)\nRosa", "Dr. Rosa (pediatra)\nRosa (pediatra)"],
  ["<code>m.mostrar()</code> usa la versión de Medico, que imprime «Dr. », llama a <code>Persona::mostrar()</code> (el nombre) y luego la especialidad.",
   "<code>Persona p = m;</code> copia solo la parte Persona del médico (se «rebana»). Como <code>mostrar()</code> no es virtual y p es una Persona, imprime solo «Rosa»."],
  "Persona:: llama a la versión de la base.", [["her"], ["her", "virt"]]))

A_ex.append(ex("p11h9", 2, "Herencia protected",
  "<p><code>class B { public: void f(); };</code> y <code>class D : protected B { };</code>. En el <code>main</code>, con <code>D d;</code>, ¿qué pasa con <code>d.f();</code>?</p>",
  [mc("Respuesta", ["No compila: con herencia protected, f() queda protected en D", "Compila y llama a B::f()", "Compila solo si f() es virtual",
                     "No compila porque B no tiene constructor", "Compila, pero f() hace nada"])],
  ["El nivel de acceso de la herencia es un <b>tope</b>: con <code>protected</code>, lo que era public en B pasa a ser protected en D.",
   "Desde el main no se puede llamar a algo protected. Con <code>class D : public B</code> sí compilaría."],
  "No compila", "El nivel de la herencia es un tope.", [["acceso"], ["acceso"]]))

START_H10 = HDR + '''class Persona {
protected:
    string nombre;
    int edad;
public:
    Persona(string n, int e) : nombre(n), edad(e) {}
    string getNombre() { return nombre; }
};

// completa la clase Estudiante: hereda de Persona y agrega string carrera
// - Estudiante(string n, int e, string c)
// - string ficha(): devuelve "Ana (19) - Electronica"
// - bool esMayor(): true si edad >= 18
'''
SOL_H10 = START_H10 + '''class Estudiante : public Persona {
    string carrera;
public:
    Estudiante(string n, int e, string c) : Persona(n, e), carrera(c) {}
    string ficha() { return nombre + " (" + to_string(edad) + ") - " + carrera; }
    bool esMayor() { return edad >= 18; }
};
'''
START_H10 = START_H10 + '''class Estudiante : public Persona {
    // ...
};
'''
T_H10 = [{"n": "Ficha", "main": 'Estudiante e("Ana", 19, "Electronica");\ncout << e.ficha() << endl;', "out": "Ana (19) - Electronica"},
         {"n": "Hereda getNombre", "main": 'Estudiante e("Luis", 17, "Mecatronica");\ncout << e.getNombre() << " " << e.esMayor() << endl;', "out": "Luis 0"},
         {"n": "Mayor de edad", "main": 'Estudiante e("Rosa", 18, "Bioingenieria");\ncout << e.esMayor() << endl;', "out": "1"}]
A_ex.append(code_ex("p11h10", 2, "Estudiante es una Persona",
  "<p>Completa la clase <code>Estudiante</code>, que <b>hereda</b> de <code>Persona</code> y agrega <code>carrera</code>:</p><ul>"
  "<li>Constructor <code>Estudiante(string n, int e, string c)</code> usando la lista de inicialización.</li>"
  "<li><code>string ficha()</code>: devuelve <code>Ana (19) - Electronica</code> (usa <code>to_string</code>).</li>"
  "<li><code>bool esMayor()</code>: <code>true</code> si la edad es al menos 18.</li></ul>",
  START_H10, SOL_H10, T_H10,
  ["La clase empieza con <code>class Estudiante : public Persona</code> y solo declara lo nuevo (<code>carrera</code>).",
   "El constructor llama a <code>Persona(n, e)</code> en la lista de inicialización; nombre y edad son protected, así que los métodos los usan directo."],
  "Lista de inicialización: : Persona(n, e), carrera(c)", [["ctorher"], ["acceso"]]))

START_H11 = HDR + '''class Cuenta {
protected:
    string titular;
    double saldo;
public:
    Cuenta(string t, double s) : titular(t), saldo(s) {}
    void depositar(double m) { if (m > 0) saldo += m; }
    double getSaldo() { return saldo; }
};

class CuentaAhorro : public Cuenta {
    double tasa;  // por ejemplo 0.05 = 5 %
public:
    // completa: constructor CuentaAhorro(string t, double s, double tasa)
    // completa: void aplicarInteres()  -> saldo aumenta saldo * tasa
    // completa: bool retirar(double m) -> solo si m > 0 y deja al menos 100 de saldo; devuelve si pudo
};
'''
SOL_H11 = START_H11.replace('''    // completa: constructor CuentaAhorro(string t, double s, double tasa)
    // completa: void aplicarInteres()  -> saldo aumenta saldo * tasa
    // completa: bool retirar(double m) -> solo si m > 0 y deja al menos 100 de saldo; devuelve si pudo
''', '''    CuentaAhorro(string t, double s, double tasa) : Cuenta(t, s), tasa(tasa) {}
    void aplicarInteres() { saldo += saldo * tasa; }
    bool retirar(double m) {
        if (m <= 0 || saldo - m < 100) return false;
        saldo -= m;
        return true;
    }
''')
T_H11 = [{"n": "Interés", "main": 'CuentaAhorro c("Ana", 1000, 0.05);\nc.aplicarInteres();\ncout << c.getSaldo() << endl;', "out": "1050"},
         {"n": "Deposita (heredado) y retira", "main": 'CuentaAhorro c("Luis", 300, 0.1);\nc.depositar(200);\ncout << c.retirar(350) << " " << c.getSaldo() << endl;', "out": "1 150"},
         {"n": "No deja menos de 100", "main": 'CuentaAhorro c("Rosa", 300, 0.1);\ncout << c.retirar(250) << " " << c.retirar(-5) << " " << c.getSaldo() << endl;', "out": "0 0 300"}]
A_ex.append(code_ex("p11h11", 3, "Cuenta de ahorro",
  "<p><code>CuentaAhorro</code> hereda de <code>Cuenta</code> (como en el lab de POO, pero en C++). Completa el constructor, <code>aplicarInteres()</code> y <code>retirar(m)</code> según los comentarios.</p>",
  START_H11, SOL_H11, T_H11,
  ["El constructor reenvía titular y saldo a <code>Cuenta(t, s)</code> y guarda su propia tasa.",
   "<code>saldo</code> es protected: la hija lo modifica directo. <code>depositar</code> y <code>getSaldo</code> se heredan sin escribirlos."],
  "saldo es protected: úsalo directo.", [["ctorher"], ["acceso"]]))

# =====================================================================
# TEMA B · Funciones virtuales y clases abstractas
# =====================================================================
B_teo = (
 "<p>Un puntero (o referencia) a la base puede apuntar a un objeto derivado: <code>Animal* p = new Perro;</code>. La pregunta es qué versión de un método corre con <code>p-&gt;hablar()</code>.</p>"
 "<ul><li><b>Sin <code>virtual</code></b> (ligadura estática): manda el <b>tipo del puntero</b> → <code>Animal::hablar()</code>.</li>"
 "<li><b>Con <code>virtual</code></b> en la base (ligadura dinámica): manda el <b>objeto real</b> → <code>Perro::hablar()</code>. Esto es el <b>polimorfismo</b>.</li></ul>"
 "<p>Un método virtual de la base es virtual en <b>todas</b> las subclases. Al sobrescribirlo hay que mantener la misma lista de parámetros (se recomienda escribir <code>override</code>).</p>"
 "<p><b>Constructores:</b> no pueden ser virtuales (no se heredan). <b>Destructores:</b> si la clase va a ser base, su destructor debe ser <code>virtual</code>; si no, <code>delete p</code> con <code>Animal* p = new Perro</code> solo ejecuta <code>~Animal()</code> y lo que Perro pidió con <code>new</code> nunca se libera. Las funciones <code>friend</code> no pueden ser virtuales (no son miembros).</p>"
 "<p><b>Función virtual pura:</b> <code>virtual void ProduceSonido(ostream&amp; os) = 0;</code> (sin cuerpo; la implementa la subclase). Una clase con al menos una virtual pura es <b>abstracta</b>: no se puede instanciar, solo sirve como base. La subclase debe implementar <b>todas</b> las virtuales puras para ser concreta.</p>"
 "<p><b>Herencia múltiple:</b> <code>class C : public A, public B</code>; las bases se construyen en el orden en que se escriben.</p>"
)
B_form = ["<code>virtual</code> en la base → manda el objeto real (ligadura dinámica)",
          "Sin virtual → manda el tipo del puntero (ligadura estática)",
          "Destructor de una base: <code>virtual ~B()</code> (si no, fuga)",
          "Virtual pura: <code>virtual void f() = 0;</code> → clase abstracta, no se instancia",
          "Constructores y friend: nunca virtuales",
          "Herencia múltiple: <code>class C : public A, public B</code> → A, B, C"]
B_lesson = (
 "<h3>Idea central</h3><p>Con <code>virtual</code>, una lista de <code>Figura*</code> puede tener rectángulos y círculos y cada uno calcula <b>su</b> área: escribes el código una vez para la base y funciona para todas las hijas.</p>"
 "<h3>Para decidir qué se imprime</h3><ol><li>¿El método es virtual en la base? Si no: tipo del puntero.</li><li>Si es virtual: el tipo del objeto creado con <code>new</code>.</li><li>Al hacer <code>delete</code> con un puntero a la base: ¿el destructor es virtual? Si no, solo corre el de la base.</li></ol>"
 "<div class=\"err\"><b>Errores frecuentes:</b> olvidar <code>virtual</code> y sorprenderse de que se llame la versión de la base; intentar <code>new Figura</code> cuando Figura es abstracta; cambiar los parámetros al sobrescribir (eso crea otro método, no sobrescribe); y no hacer virtual el destructor de la base.</div>"
)
B_tools = [{"w": "virt", "t": "¿Qué método se llama?", "p": "Activa o quita <code>virtual</code>, <code>= 0</code> y el destructor virtual, cambia el tipo del puntero y del objeto, y mira la salida y la memoria.",
            "o": {"B": "Animal", "D": "Perro", "m": "hablar", "bo": "...", "do": "Guau"}}]

B_ex = []
B_ex.append(ex("p11v1", 1, "Haz que ladre",
  "<p>El puntero es <code>Animal*</code> y apunta a un <code>Perro</code>. Activa lo necesario para que <code>p-&gt;hablar()</code> imprima <b>Guau</b>.</p>",
  [virt("Haz que imprima Guau", {"out": "Guau"}, {"vm": True, "pure": False, "vd": False, "ptr": "B", "obj": "D"}, lock=["ptr", "obj"],
        e="Sin virtual manda el tipo del puntero (Animal).")],
  ["Sin <code>virtual</code>, el compilador decide por el tipo del puntero: <code>Animal::hablar()</code> → «...».",
   "Con <code>virtual void hablar()</code> en Animal, se decide en ejecución por el objeto real (Perro): «Guau»."],
  "virtual en hablar()", "¿Quién decide: el puntero o el objeto?", [["virt"], ["virt"]]))
B_ex.append(ex("p11v2", 2, "Sin fugas",
  "<p>Ya ladra, pero hay un problema al hacer <code>delete p</code>. Déjalo ladrando y <b>sin fuga de memoria</b>.</p>",
  [virt("Arregla la fuga", {"out": "Guau", "leak": False}, {"vm": True, "pure": False, "vd": True, "ptr": "B", "obj": "D"},
        ini={"vm": True, "pure": False, "vd": False, "ptr": "B", "obj": "D"}, lock=["ptr", "obj"], e="Mira qué destructores se ejecutan.")],
  ["Con <code>~Animal()</code> no virtual, <code>delete p</code> (un Animal*) solo llama a <code>~Animal()</code>: el <code>delete[] datos</code> de Perro nunca corre.",
   "Con <code>virtual ~Animal()</code> se ejecuta <code>~Perro()</code> y luego <code>~Animal()</code>: no hay fuga. Regla: toda clase base lleva destructor virtual."],
  "virtual en el destructor", "Mira los destructores en la salida.", [["dvirt"], ["dvirt"]]))
B_ex.append(ex("p11v3", 2, "Animal abstracto",
  "<p>Haz que <code>Animal</code> sea una <b>clase abstracta</b>, que <code>p-&gt;hablar()</code> imprima <b>Guau</b> y que no haya fugas. (Ahora sí puedes cambiar el objeto: ¿qué pasa con <code>new Animal</code>?)</p>",
  [virt("Abstracta, ladrando y sin fugas", {"out": "Guau", "leak": False, "abs": True}, {"vm": True, "pure": True, "vd": True, "ptr": "B", "obj": "D"},
        lock=["ptr"], e="Una función virtual pura se marca con = 0.")],
  ["<code>virtual void hablar() = 0;</code> hace que Animal sea abstracta: ya no se puede hacer <code>new Animal</code> (prueba elegirlo: no compila).",
   "Con <code>new Perro</code>, el puntero Animal* llama a <code>Perro::hablar()</code>, y con el destructor virtual no hay fuga."],
  "= 0, virtual ~Animal() y new Perro", "= 0 y destructor virtual.", [["abst"], ["abst", "dvirt"]]))

PROG4 = HDR + '''class Figura {
public:
    void nombre() { cout << "Figura "; }
    virtual void dibujar() { cout << "? "; }
    virtual ~Figura() {}
};

class Circulo : public Figura {
public:
    void nombre() { cout << "Circulo "; }
    void dibujar() override { cout << "O "; }
};

int main() {
    Figura* f = new Circulo;
    f->nombre();
    f->dibujar();
    Circulo c;
    c.nombre();
    delete f;
    return 0;
}'''
B_ex.append(output_ex("p11v4", 2, "Virtual vs. no virtual", PROG4,
  ["Figura O Circulo ", "Circulo O Circulo ", "Figura ? Circulo ", "Circulo ? Figura ", "Figura O Figura "],
  ["<code>nombre()</code> no es virtual: con un <code>Figura*</code> se llama <code>Figura::nombre()</code> → «Figura ».",
   "<code>dibujar()</code> sí es virtual: manda el objeto real (Circulo) → «O ». Con <code>c</code>, que es un Circulo (no puntero a base), se llama <code>Circulo::nombre()</code>."],
  "Solo lo virtual mira el objeto real.", [["virt"], ["virt"]]))

B_ex.append(ex("p11v5", 1, "¿Qué no puede ser virtual?",
  "<p>Según la clase, ¿qué de esto <strong>no</strong> puede declararse <code>virtual</code>?</p>",
  [mc("Respuesta", ["El constructor", "El destructor", "Un método que devuelve void", "Un método con parámetros", "Un método que se sobrescribe en la hija"])],
  ["El constructor no se hereda: cada clase define el suyo y llama al de su base. Por eso no puede ser virtual (tampoco una función friend, que no es miembro).",
   "El destructor <b>sí</b> puede y <b>debe</b> ser virtual en una clase base; cualquier método normal puede ser virtual."],
  "El constructor", "¿Qué no se hereda?", [["virt"], ["dvirt"]]))

BUG6V = HDR + '''class Figura {
public:
    virtual double area() = 0;
    virtual ~Figura() {}
};

class Cuadrado : public Figura {
    double l;
public:
    Cuadrado(double l) : l(l) {}
    double area() override { return l * l; }
};

int main() {
    Figura* a = new Cuadrado(2);
    Figura* b = new Figura;
    cout << a->area() << endl;
    delete a;
    delete b;
    return 0;
}'''
B_ex.append(ex("p11v6", 2, "Encuentra el error: abstracta",
  "<p>Este programa no compila.</p>",
  [bug_check(BUG6V, [lineof(BUG6V, "new Figura;")], ["Figura es abstracta (area() = 0): no se puede crear con new Figura", "Un Figura* no puede apuntar a un Cuadrado",
     "Falta virtual en area() de Cuadrado", "El destructor no puede ser virtual", "override no existe en C++"],
     "error: invalid new-expression of abstract class type 'Figura'")],
  ["<code>area() = 0</code> es virtual pura, así que <code>Figura</code> es abstracta y no se puede instanciar: falla <code>new Figura</code>.",
   "Lo demás está bien: un puntero a la base sí puede apuntar a un Cuadrado (es una Figura), y en la hija <code>virtual</code> es opcional porque ya es virtual en la base."],
  "No se instancia una clase abstracta", "¿Cuál de las clases tiene = 0?", [["abst"], ["abst"]]))

B_ex.append(ex("p11v7", 1, "¿Abstracta o concreta?",
  "<p>Clasifica cada clase (supón <code>class Ave { public: virtual void volar() = 0; virtual void comer() = 0; };</code>).</p>",
  [{"t": "cls", "cats": ["Abstracta (no se puede instanciar)", "Concreta (sí se puede)"], "items": [
    {"x": "<code>Ave</code>", "c": 0},
    {"x": "<code>class Buho : public Ave { void volar() override; void comer() override; };</code>", "c": 1},
    {"x": "<code>class Gallina : public Ave { void comer() override; };</code>", "c": 0, "e": "Le falta implementar volar(): sigue teniendo una virtual pura."},
    {"x": "<code>class Animal { public: virtual void sonido() { } };</code>", "c": 1, "e": "Virtual no es lo mismo que virtual pura: esta tiene cuerpo."},
    {"x": "<code>class Felino { public: virtual void cazar() = 0; void dormir(); };</code>", "c": 0}]}],
  ["Una clase es abstracta si tiene (o hereda sin implementar) al menos una función virtual pura <code>= 0</code>.",
   "Para que una hija sea concreta debe implementar <b>todas</b> las virtuales puras; si le falta una, sigue siendo abstracta."],
  "Clasificación correcta", "Busca = 0 sin implementar.", [["abst"], ["abst"]]))

START_V8 = HDR + '''#include <vector>

class Figura {
public:
    virtual double area() = 0;
    virtual string nombre() = 0;
    virtual ~Figura() {}
};

// completa: class Rectangulo (base b, altura h) y class Circulo (radio r, usa 3.14)
// completa: double areaTotal(vector<Figura*> v) -> suma de las areas
'''
SOL_V8 = START_V8 + '''class Rectangulo : public Figura {
    double b, h;
public:
    Rectangulo(double b, double h) : b(b), h(h) {}
    double area() override { return b * h; }
    string nombre() override { return "Rectangulo"; }
};

class Circulo : public Figura {
    double r;
public:
    Circulo(double r) : r(r) {}
    double area() override { return 3.14 * r * r; }
    string nombre() override { return "Circulo"; }
};

double areaTotal(vector<Figura*> v) {
    double s = 0;
    for (Figura* f : v) s += f->area();
    return s;
}
'''
T_V8 = [{"n": "Áreas", "main": 'Rectangulo r(3, 4);\nCirculo c(1);\ncout << r.area() << " " << c.area() << endl;', "out": "12 3.14"},
        {"n": "Polimorfismo", "main": 'vector<Figura*> v = {new Rectangulo(2, 5), new Circulo(2)};\nfor (Figura* f : v) cout << f->nombre() << " ";\ncout << areaTotal(v) << endl;\nfor (Figura* f : v) delete f;', "out": "Rectangulo Circulo 22.56"},
        {"n": "Vacío", "main": 'vector<Figura*> v;\ncout << areaTotal(v) << endl;', "out": "0"}]
B_ex.append(code_ex("p11v8", 2, "Figuras polimórficas",
  "<p><code>Figura</code> es abstracta. Escribe <code>Rectangulo(b, h)</code> y <code>Circulo(r)</code> (con π = 3.14) que implementen <code>area()</code> y <code>nombre()</code>, y la función <code>areaTotal</code> que suma las áreas de un <code>vector&lt;Figura*&gt;</code>.</p>",
  START_V8, SOL_V8, T_V8,
  ["Cada hija hereda públicamente de Figura e implementa las <b>dos</b> virtuales puras; si falta una, sigue siendo abstracta y no se puede crear.",
   "<code>areaTotal</code> no sabe qué figura es cada una: llama <code>f-&gt;area()</code> y la ligadura dinámica elige la versión correcta."],
  "Implementa las dos virtuales puras en cada hija.", [["abst"], ["virt"]]))

START_V9 = HDR + '''#include <vector>

class Empleado {
protected:
    string nombre;
public:
    Empleado(string n) : nombre(n) {}
    virtual double sueldo() = 0;
    string boleta() { return nombre + ": " + to_string((int)sueldo()); }
    virtual ~Empleado() {}
};

// completa: class Planilla (sueldo fijo mensual)
//           class PorHoras (horas trabajadas y pago por hora)
// completa: double planillaTotal(vector<Empleado*> v)
'''
SOL_V9 = START_V9 + '''class Planilla : public Empleado {
    double fijo;
public:
    Planilla(string n, double f) : Empleado(n), fijo(f) {}
    double sueldo() override { return fijo; }
};

class PorHoras : public Empleado {
    int horas;
    double pago;
public:
    PorHoras(string n, int h, double p) : Empleado(n), horas(h), pago(p) {}
    double sueldo() override { return horas * pago; }
};

double planillaTotal(vector<Empleado*> v) {
    double s = 0;
    for (Empleado* e : v) s += e->sueldo();
    return s;
}
'''
T_V9 = [{"n": "Boletas", "main": 'Planilla a("Ana", 3000);\nPorHoras b("Luis", 40, 25);\ncout << a.boleta() << " | " << b.boleta() << endl;', "out": "Ana: 3000 | Luis: 1000"},
        {"n": "Total", "main": 'vector<Empleado*> v = {new Planilla("Ana", 3000), new PorHoras("Luis", 10, 30), new PorHoras("Rosa", 5, 20)};\ncout << planillaTotal(v) << endl;\nfor (Empleado* e : v) delete e;', "out": "3400"}]
B_ex.append(code_ex("p11v9", 3, "Planilla de empleados",
  "<p><code>Empleado</code> es abstracta y su <code>boleta()</code> usa <code>sueldo()</code>, que es virtual pura. Escribe <code>Planilla(nombre, fijo)</code>, <code>PorHoras(nombre, horas, pagoPorHora)</code> y <code>planillaTotal</code>.</p>",
  START_V9, SOL_V9, T_V9,
  ["Cada subclase llama a <code>Empleado(n)</code> en su lista de inicialización y solo implementa <code>sueldo()</code>.",
   "<code>boleta()</code> está escrita una sola vez en la base, pero como llama a una función virtual, cada empleado muestra su propio sueldo."],
  "La base ya tiene boleta(): solo falta sueldo().", [["ctorher", "abst"], ["virt"]]))

B_ex.append(ex("p11v10", 1, "¿Por qué destructor virtual?",
  "<p>¿Cuándo es necesario declarar <code>virtual ~Base()</code>?</p>",
  [mc("Respuesta", ["Cuando se borra un objeto derivado a través de un puntero a la base", "Siempre que la clase tenga constructor",
                     "Solo si la clase es abstracta", "Cuando la clase no tiene atributos", "Nunca: los destructores no se pueden heredar"])],
  ["<code>delete p</code> con <code>Base* p = new Derivada</code> llama al destructor según el tipo del puntero si no es virtual: solo corre <code>~Base()</code>.",
   "Si la derivada liberaba memoria en su destructor, esa memoria se pierde. Con <code>virtual ~Base()</code> se ejecutan ambos (derivada y luego base)."],
  "Al borrar por un puntero a la base", "Piensa en delete p con p de tipo Base*.", [["dvirt"], ["dvirt"]]))

PROG11 = HDR + '''class Volador {
public:
    Volador() { cout << "V "; }
};

class Nadador {
public:
    Nadador() { cout << "N "; }
};

class Pato : public Nadador, public Volador {
public:
    Pato() { cout << "P "; }
};

int main() {
    Pato p;
    return 0;
}'''
B_ex.append(output_ex("p11v11", 2, "Herencia múltiple", PROG11,
  ["N V P ", "V N P ", "P N V ", "P V N ", "N P V "],
  ["Con herencia múltiple <code>class Pato : public Nadador, public Volador</code>, las bases se construyen <b>en el orden en que se escriben</b>: primero Nadador, luego Volador.",
   "El cuerpo del constructor de Pato corre al final. (El orden de las clases en el archivo no importa: importa el de la lista de herencia.)"],
  "El orden de la lista de herencia.", [["hmult"], ["hmult"]]))

# =====================================================================
# Ensamblar
# =====================================================================
topA = {"id": "w11her", "name": "Sem. 11 · Herencia: clase base, derivada y constructores", "teo": A_teo, "form": A_form, "ex": A_ex, "lesson": A_lesson}
topB = {"id": "w11vir", "name": "Sem. 11 · Funciones virtuales, clases abstractas y herencia múltiple", "teo": B_teo, "form": B_form, "ex": B_ex, "lesson": B_lesson, "tools": B_tools}

d['concepts'].update({
 "her": {"n": "Herencia", "f": "«es un» · <code>class D : public B</code>", "x": "La derivada hereda atributos y métodos de la base y agrega los suyos.", "home": "w11her"},
 "ctorher": {"n": "Constructores en herencia", "f": "<code>D(…) : B(…) { … }</code>", "x": "Primero se construye la base; los destructores van al revés.", "home": "w11her"},
 "acceso": {"n": "public, protected y private", "f": "protected: lo ve la hija, no el main", "x": "private es solo de la base; el nivel de la herencia es un tope.", "home": "w11her"},
 "virt": {"n": "Función virtual", "f": "<code>virtual void f();</code> → ligadura dinámica", "x": "Con un puntero a la base, manda el objeto real; sin virtual, el tipo del puntero.", "home": "w11vir"},
 "dvirt": {"n": "Destructor virtual", "f": "<code>virtual ~Base()</code>", "x": "Sin él, delete por un puntero a la base no ejecuta el destructor de la hija (fuga).", "home": "w11vir"},
 "abst": {"n": "Clase abstracta", "f": "<code>virtual void f() = 0;</code>", "x": "Tiene una virtual pura: no se instancia; la hija concreta implementa todas.", "home": "w11vir"},
 "hmult": {"n": "Herencia múltiple", "f": "<code>class C : public A, public B</code>", "x": "Las bases se construyen en el orden de la lista.", "home": "w11vir"}})
allc = set(d['concepts'])
for t in (topA, topB):
    for e in t['ex']:
        for s in e['tags']:
            for k in s: assert k in allc, (e['id'], k)

d['topics'] = [t for t in d['topics'] if t['id'] not in ('w11her', 'w11vir')] + [topA, topB]

card = ('<div><b>Herencia</b><br>«es un» · <code>class D : public B</code> · <code>D(…) : B(…) {}</code> · base primero, destructores al revés · protected lo ve la hija</div>\n'
        '<div><b>Virtual</b><br><code>virtual</code> → manda el objeto real · <code>virtual ~B()</code> · <code>= 0</code> → abstracta (no se instancia)</div>\n')
if 'Herencia</b>' not in d['form']:
    k = d['form'].rindex('</div>')
    d['form'] = d['form'][:k] + card + d['form'][k:]

d['intro'] = ('Repaso acumulado con los temas ordenados por semana y todos abiertos desde el inicio. El examen final pone el énfasis en las semanas 9 en adelante (POO en C++): '
              'ya están la semana 9 (clases, constructores y destructores), la 10 (arreglos de objetos, punteros dobles y relaciones entre clases, con un mapa de memoria) '
              'y la 11 (herencia, funciones virtuales y clases abstractas, con un simulador de «¿qué método se llama?»). '
              'El simulacro tiene la mayoría de preguntas de esas semanas y una parte de repaso. Se actualiza cada vez que se agrega una semana nueva. Igual que en el parcial, elige si practicar en computadora o escrito.')

INTRO = "Simulacro acumulativo del examen final: la mayor parte es de las semanas 9 a 11 y una pregunta de repaso. Se actualiza cada semana."
comp = {"name": "💻 En computadora", "desc": "Cinco programas en 100 minutos, con compilador.", "minutes": 100, "slots": [
    {"pts": 3, "name": "Clases: atributos, constructores y métodos (sem. 9)", "pool": ["oo10", "oo11"]},
    {"pts": 4, "name": "Objetos dinámicos, arreglos de objetos y punteros dobles (sem. 9–10)", "pool": ["oo12", "oo13", "p10c1"]},
    {"pts": 5, "name": "Relaciones entre clases (sem. 10)", "pool": ["p10c2", "p10c3", "p10c4"]},
    {"pts": 6, "name": "Herencia y polimorfismo (sem. 11)", "pool": ["p11h10", "p11h11", "p11v8", "p11v9"]},
    {"pts": 2, "name": "Repaso: arreglos dinámicos y punteros", "pool": ["fpc_temps", "fpc_consumo", "far8"]}], "intro": INTRO}
writ = {"name": "✍️ Escrito", "desc": "Opción múltiple (lectura de código y teoría) y dos programas sin compilar.", "minutes": 100, "slots": [
    {"pts": 1, "name": "Constructores sobrecargados y orden de destrucción", "pool": ["oo2", "oo3"]},
    {"pts": 1, "name": "Objetos dinámicos y this", "pool": ["oo4", "oo6", "p10t1"]},
    {"pts": 1, "name": "Memoria: new, delete y delete[] (sem. 10)", "pool": ["p10m1", "p10m2", "p10m3", "p10t4"]},
    {"pts": 1, "name": "Arreglos de objetos y punteros dobles (sem. 10)", "pool": ["p10t2", "p10t3", "p10t5", "p10o1"]},
    {"pts": 1, "name": "Relaciones entre clases (sem. 10)", "pool": ["p10r1", "p10r2", "p10r3", "p10r4", "p10r5", "p10r6", "p10r7"]},
    {"pts": 1, "name": "Herencia: constructores y acceso (sem. 11)", "pool": ["p11h3", "p11h4", "p11h6", "p11h7", "p11h8", "p11h9"]},
    {"pts": 2, "name": "Virtual, abstractas y herencia múltiple (sem. 11)", "pool": ["p11v2", "p11v3", "p11v4", "p11v6", "p11v7", "p11v11"]},
    {"pts": 1, "name": "Repaso: funciones, punteros, arreglos y vectores", "pool": ["ffu1", "fpu2", "fpu5", "fpu6", "far4", "fma3", "fve3", "fve4"]},
    {"pts": 5, "name": "Clases, arreglos de objetos o relaciones (a mano)", "pool": ["oo10", "oo11", "oo12", "oo13", "p10c1", "p10c2", "p10c3", "p10c4"]},
    {"pts": 6, "name": "Herencia y polimorfismo (a mano)", "pool": ["p11h10", "p11h11", "p11v8", "p11v9"]}],
    "intro": "Modalidad en papel: no puedes compilar. Al entregar se compila y se prueba tu código.", "noRun": True}
for v in (comp, writ): assert sum(s['pts'] for s in v['slots']) == 20
d['sim']['slots'] = comp['slots']; d['sim']['intro'] = comp['intro']; d['sim']['minutes'] = 100; d['sim']['versions'] = [comp, writ]
allex = [e['id'] for t in d['topics'] for e in t['ex']] + [e['id'] for e in (d.get('simEx') or [])]
assert len(allex) == len(set(allex)), 'ids repetidos'
for v in d['sim']['versions']:
    for s in v['slots']:
        for i in s['pool']: assert i in allex, ('pool', i)

with open(F, 'w', encoding='utf-8') as o:
    json.dump(d, o, indent=1, ensure_ascii=False); o.write('\n')
print('ok', len(A_ex), len(B_ex))
