"""Ayudas para construir Programación I (CS6002). Todo se verifica ejecutando Python:
salidas de «¿qué imprime?», soluciones modelo contra sus pruebas, cajitas de «completa el código»,
errores de «encuentra el error», rastreos y pasos del visualizador."""
import io, sys, json, random, re, builtins, html, copy, os, contextlib, tempfile, importlib

def esc(s): return html.escape(str(s), quote=False)
def pre(code): return '<pre class="py"><code>' + esc(code.rstrip('\n')) + '</code></pre>'
def c(s): return '<code>' + esc(s) + '</code>'
def outc(s): return '<code class="out">' + esc(s).replace('\n', '<br>') + '</code>'

def norm(s):
    ls = [l.rstrip() for l in str(s).replace('\r\n', '\n').split('\n')]
    while ls and ls[-1] == '': ls.pop()
    return '\n'.join(ls)

class _Inp:
    def __init__(self, data): self.l = [] if data in (None, '') else str(data).split('\n'); self.p = 0
    def __call__(self, prompt=''):
        if self.p >= len(self.l): raise EOFError('input() pidió más datos')
        v = self.l[self.p]; self.p += 1; return v

FILES_DIR = tempfile.mkdtemp(prefix='p1files_')
def _files(files):
    for n, src in (files or {}).items():
        p = os.path.join(FILES_DIR, n); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(src)
        sys.modules.pop(n[:-3].replace('/', '.') if n.endswith('.py') else n, None)
    if FILES_DIR not in sys.path: sys.path.insert(0, FILES_DIR)
    importlib.invalidate_caches()

def run(code, inp=None, extra=None, seed=0, files=None):
    """Ejecuta como la app: devuelve (salida, error o None)."""
    _files(files)
    g = {'__name__': '__main__', '__builtins__': builtins}
    buf = io.StringIO(); old = builtins.input; builtins.input = _Inp(inp); random.seed(seed); err = None
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, 'tu_codigo.py', 'exec'), g)
            if extra: exec(compile(extra, 'prueba.py', 'exec'), g)
    except BaseException as e:
        err = type(e).__name__ + (': ' + str(e) if str(e) else '')
    finally:
        builtins.input = old
    return buf.getvalue(), err

def out(code, inp=None, files=None):
    o, e = run(code, inp, files=files)
    assert e is None, 'El código del enunciado falla: ' + e + '\n' + code
    return norm(o)

def passes(code, tests, files=None):
    res = []
    for t in tests:
        o, e = run(code, t.get('in'), t.get('run'), t.get('seed', 0), files)
        res.append(e is None and ('out' not in t or norm(o) == norm(t['out'])))
    return res

def mk_tests(sol, calls, files=None, names=None):
    """calls: lista de código de prueba (p. ej. 'print(pregunta_1([1,2]))'); la salida esperada sale de la solución modelo."""
    T = []
    for i, cl in enumerate(calls):
        o, e = run(sol, None, cl, files=files)
        assert e is None, 'La solución modelo falla en ' + cl + ': ' + e
        T.append({'n': (names[i] if names else cl.replace('print(', '').rstrip(')')[:70]), 'run': cl, 'out': norm(o)})
    return T

# ---------------- ejercicios ----------------
def ex(id, lvl, title, q, checks, steps, ans, hint='', tags=None, play=None, **kw):
    e = {'id': id, 'lvl': lvl, 'title': title, 'q': q, 'checks': checks, 'steps': steps, 'ans': ans, 'hint': hint,
         'fig': None, 'draw': False, 'open': False, 'solfig': None, 'tags': tags or [[] for _ in steps]}
    assert len(e['tags']) == len(steps), id + ': tags y steps no coinciden'
    if play: e['play'] = play
    e.update(kw)
    return e

def opc(id, lvl, title, q, opts, steps, hint='', tags=None, p='Elige la respuesta', play=None):
    assert len(set(opts)) == len(opts), id + ': opciones repetidas'
    return ex(id, lvl, title, q, [{'p': p, 'o': opts}], steps, opts[0], hint, tags, play)

def imprime(id, lvl, title, code, wrong, steps, hint='', tags=None, intro='', inp=None, files=None):
    """«¿Qué imprime?»: la correcta sale de ejecutar el código."""
    right = out(code, inp, files)
    opts = [outc(right)] + [outc(norm(w)) for w in wrong]
    for w in wrong: assert norm(w) != right, id + ': un distractor es igual a la salida real'
    q = (intro or '') + pre(code) + '<p>¿Qué imprime este programa?</p>'
    e = opc(id, lvl, title, q, opts, steps, hint, tags, 'Salida', play=code)
    if inp: e['playIn'] = inp
    return e

def hueco(id, lvl, title, q, code, blanks, steps, hint='', tags=None, tests=None, demo=None, extra_ok=None):
    """blanks: [(respuestas aceptadas, pista, explicación)]. Verifica que con la primera respuesta pase las pruebas
    y que cada respuesta aceptada también las pase."""
    n = len(re.findall(r'⟦(\d+)⟧', code)); assert n == len(blanks), id + ': cajitas y huecos no coinciden'
    def fill(sel):
        return re.sub(r'⟦(\d+)⟧', lambda m: sel[int(m.group(1))], code)
    base = [b[0][0] for b in blanks]
    full = fill(base)
    if tests:
        assert all(passes(full, tests)), id + ': la solución de las cajitas no pasa sus pruebas\n' + full
        for k, b in enumerate(blanks):
            for a in b[0][1:]:
                s = base[:]; s[k] = a
                assert all(passes(fill(s), tests)), id + ': la respuesta aceptada «' + a + '» no pasa'
    else:
        o, e = run(full + ('\n' + demo if demo else ''))
        assert e is None, id + ': ' + e
    ch = {'t': 'hueco', 'p': 'Completa las cajitas', 'code': code,
          'b': [dict(a=b[0], h=b[1], e=b[2]) for b in blanks]}
    if tests: ch['tests'] = tests
    if demo: ch['demo'] = demo
    return ex(id, lvl, title, q, [ch], steps + ['Código completo:' + pre(full)], 'Código completo y correcto', hint,
              (tags or [[] for _ in steps]) + [[]])

def bug(id, lvl, title, q, code, lines, reasons, steps, hint='', tags=None, outtxt=None, inp=None, fixed=None, e=None, extra=None):
    """Encuentra el error. Si no se da outtxt, se ejecuta el código y se muestra lo que pasa.
    fixed = versión corregida (se verifica que corra y, si hay extra, que imprima algo distinto)."""
    assert len(set(reasons)) == len(reasons)
    if outtxt is None:
        o, er = run(code, inp, extra)
        outtxt = (norm(o) + ('\n' if norm(o) else '') + ('💥 ' + er if er else '')).strip() or '(no imprime nada)'
    if fixed:
        o2, er2 = run(fixed, inp, extra)
        assert er2 is None, id + ': la versión corregida falla: ' + er2
    L = code.split('\n')
    for l in lines: assert 1 <= l <= len(L)
    ch = {'t': 'bug', 'p': 'Encuentra el error', 'code': code, 'l': lines, 'o': reasons, 'out': outtxt}
    if e: ch['e'] = e
    st = steps + (['Versión corregida:' + pre(fixed)] if fixed else [])
    tg = (tags or [[] for _ in steps]) + ([[]] if fixed else [])
    return ex(id, lvl, title, q, [ch], st, 'Línea ' + ', '.join(map(str, lines)) + ': ' + reasons[0], hint, tg, play=fixed or code)

def codex(id, lvl, title, q, start, sol, calls, steps, hint='', tags=None, names=None, hidden=None, files=None, pc=None):
    """Escribir código: las pruebas salen de la solución modelo; la plantilla no debe pasar todas."""
    tests = mk_tests(sol, calls, files, names)
    if hidden:
        for t in mk_tests(sol, hidden, files): t['hidden'] = True; t['n'] = 'Prueba oculta'; tests.append(t)
    assert not all(passes(start, tests, files)), id + ': la plantilla ya pasa las pruebas'
    ch = {'t': 'code', 'p': 'Escribe tu código y compruébalo con las pruebas', 'start': start, 'tests': tests}
    if files: ch['files'] = files
    e = ex(id, lvl, title, q, [ch], steps + ['Una solución posible:' + pre(sol)], 'Tu código pasa todas las pruebas', hint,
           (tags or [[] for _ in steps]) + [[]])
    if pc: e['pc'] = pc
    return e

def arregla(id, lvl, title, q, buggy, sol, calls, steps, hint='', tags=None, names=None):
    """Arréglalo en el editor: la plantilla es el código con error."""
    return codex(id, lvl, title, q, buggy, sol, calls, steps, hint, tags, names)

def chk(e, *extra):
    e['checks'] += list(extra); return e

# ---------------- rastreo y visualizador ----------------
def _enc(v, h, keep, depth=0):
    if isinstance(v, (list, dict)) or (isinstance(v, tuple) and any(isinstance(x, (list, dict)) for x in v)):
        keep.append(v); k = str(id(v))
        if k not in h:
            if isinstance(v, dict):
                h[k] = {'t': 'dict', 'v': []}; h[k]['v'] = [[repr(a), _enc(b, h, keep, depth + 1)] for a, b in v.items()]
            else:
                h[k] = {'t': 'tuple' if isinstance(v, tuple) else 'list', 'v': []}; h[k]['v'] = [_enc(x, h, keep, depth + 1) for x in v]
        return '@' + k
    if callable(v): return None
    r = repr(v)
    return r if len(r) <= 70 else r[:67] + '…'

def trace(code, inp=None, maxsteps=140):
    """Pasos para LW.paso: línea por ejecutar, variables por marco, objetos y salida acumulada."""
    steps = []; keep = []; buf = io.StringIO(); FN = '<p1>'
    def snap(frame, end=False):
        fr = []; f = frame; stack = []
        while f is not None:
            if f.f_code.co_filename == FN: stack.append(f)
            f = f.f_back
        stack.reverse(); h = {}
        for f in stack:
            name = 'Global' if f.f_code.co_name == '<module>' else f.f_code.co_name + '()'
            src = f.f_globals if name == 'Global' else f.f_locals
            vs = []
            for k, v in list(src.items()):
                if k.startswith('_') or type(v).__name__ in ('module', 'function', 'builtin_function_or_method', 'type'): continue
                ev = _enc(v, h, keep)
                if ev is not None: vs.append([k, ev])
            fr.append([name, vs])
        return {'l': frame.f_lineno, 'f': fr, 'h': h, 'o': buf.getvalue()} | ({'end': True} if end else {})
    last = [None]
    def tr(frame, event, arg):
        if frame.f_code.co_filename != FN: return None
        if event == 'line' and len(steps) < maxsteps:
            steps.append(snap(frame))
        last[0] = frame
        return tr
    g = {'__name__': '__main__'}
    old = builtins.input; builtins.input = _Inp(inp)
    try:
        with contextlib.redirect_stdout(buf):
            sys.settrace(tr)
            try: exec(compile(code, FN, 'exec'), g)
            finally: sys.settrace(None)
    finally:
        builtins.input = old
    assert len(steps) < maxsteps, 'demasiados pasos'
    # paso final: estado global al terminar
    h = {}; vs = []
    for k, v in g.items():
        if k.startswith('_') or type(v).__name__ in ('module', 'function', 'builtin_function_or_method', 'type'): continue
        ev = _enc(v, h, keep)
        if ev is not None: vs.append([k, ev])
    steps.append({'l': len(code.rstrip('\n').split('\n')) + 1, 'f': [['Global', vs]], 'h': h, 'o': buf.getvalue(), 'end': True})
    # ids cortos y estables
    mp = {}
    def sid(x):
        if x not in mp: mp[x] = str(len(mp) + 1)
        return mp[x]
    def fix(v): return '@' + sid(v[1:]) if isinstance(v, str) and v.startswith('@') else v
    for s in steps:
        nh = {}
        for k, o in s['h'].items():
            nv = [[a, fix(b)] for a, b in o['v']] if o['t'] == 'dict' else [fix(x) for x in o['v']]
            nh[sid(k)] = {'t': o['t'], 'v': nv}
        s['h'] = nh
        s['f'] = [[n, [[a, fix(b)] for a, b in vs]] for n, vs in s['f']]
    return steps

def paso(code, t, p='', inp=None):
    return {'w': 'paso', 't': t, 'p': p, 'o': {'code': code.rstrip('\n'), 'steps': trace(code, inp)}}

def rastreo(code, var_names, upto=None):
    """Valores de las variables al final de cada vuelta del bucle principal (línea del for)."""
    steps = trace(code)
    # se toma el estado cada vez que se vuelve a la línea del primer for
    L = code.split('\n'); fl = next(i + 1 for i, l in enumerate(L) if l.lstrip().startswith('for ') or l.lstrip().startswith('while '))
    rows = []
    for s in steps:
        if s['l'] == fl or s.get('end'):
            env = {}
            for n, vs in s['f']:
                for k, v in vs: env[k] = v
            rows.append([_val(env.get(v), s['h']) for v in var_names])
    return rows

def _val(v, h):
    if v is None: return '—'
    if isinstance(v, str) and v.startswith('@'):
        o = h[v[1:]]
        if o['t'] == 'dict': return '{' + ', '.join(a + ': ' + _val(b, h) for a, b in o['v']) + '}'
        return '[' + ', '.join(_val(x, h) for x in o['v']) + ']'
    return v

# ---------------- cortes ----------------
def py_slice_ix(n, a, b, c):
    return list(range(n))[slice(a, b, c)]

def jdump(obj, path):
    s = json.dumps(obj, ensure_ascii=False, indent=1)
    open(path, 'w', encoding='utf-8').write(s + '\n')
