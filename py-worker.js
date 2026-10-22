// Python del Entrenador: Pyodide corre aquí, aparte de la página,
// para que un bucle infinito no congele la app (se puede detener sin recargar).
const PYO = 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/';
const HARNESS = "import sys, io, json, os, traceback, builtins, random, importlib\n\n_WORK = '/tmp/entrenador_py'\n\n\ndef _norm(s):\n    lines = [l.rstrip() for l in str(s).replace('\\r\\n', '\\n').split('\\n')]\n    while lines and lines[-1] == '':\n        lines.pop()\n    return '\\n'.join(lines)\n\n\ndef _files(files):\n    os.makedirs(_WORK, exist_ok=True)\n    if _WORK not in sys.path:\n        sys.path.insert(0, _WORK)\n    os.chdir(_WORK)\n    for name, src in (files or {}).items():\n        os.makedirs(os.path.dirname(os.path.join(_WORK, name)), exist_ok=True)\n        with open(os.path.join(_WORK, name), 'w', encoding='utf-8') as f:\n            f.write(src)\n        sys.modules.pop(name[:-3] if name.endswith('.py') else name, None)\n    importlib.invalidate_caches()\n\n\ndef _one(code, test, files):\n    _files(files)\n    lines = str(test.get('in', '')).split('\\n') if test.get('in') not in (None, '') else []\n    pos = [0]\n\n    def fake_input(prompt=''):\n        if pos[0] >= len(lines):\n            raise EOFError('input() pidió más datos de los que hay en la entrada')\n        v = lines[pos[0]]\n        pos[0] += 1\n        return v\n\n    g = {'__name__': '__main__', '__builtins__': builtins}\n    out = io.StringIO()\n    old_out, old_in = sys.stdout, builtins.input\n    sys.stdout = out\n    builtins.input = fake_input\n    random.seed(test.get('seed', 0))\n    err = None\n    try:\n        exec(compile(code, 'tu_codigo.py', 'exec'), g)\n        if test.get('run'):\n            exec(compile(test['run'], 'prueba.py', 'exec'), g)\n    except BaseException as e:\n        tb = traceback.extract_tb(e.__traceback__)\n        where = ''\n        for fr in reversed(tb):\n            if fr.filename in ('tu_codigo.py', 'prueba.py') or fr.filename.startswith(_WORK):\n                where = (' (línea %d de tu código)' % fr.lineno) if fr.filename == 'tu_codigo.py' else (\n                    ' (en la prueba)' if fr.filename == 'prueba.py' else ' (en ' + os.path.basename(fr.filename) + ')')\n                break\n        if isinstance(e, SyntaxError):\n            where = ' (línea %s de tu código)' % e.lineno\n        err = type(e).__name__ + (': ' + str(e) if str(e) else '') + where\n    finally:\n        sys.stdout = old_out\n        builtins.input = old_in\n    got = out.getvalue()\n    if len(got) > 20000 and '@@IMG@@' not in got:\n        got = got[:20000] + '\\n…(salida recortada)'\n    r = {'out': got, 'err': err}\n    if 'out' in test:\n        r['ok'] = err is None and _norm(got) == _norm(test['out'])\n    else:\n        r['ok'] = err is None\n    return r\n\n\ndef _clean():\n    if os.path.isdir(_WORK):\n        for n in os.listdir(_WORK):\n            p = os.path.join(_WORK, n)\n            if os.path.isfile(p):\n                os.remove(p)\n                if n.endswith('.py'):\n                    sys.modules.pop(n[:-3], None)\n\n\ndef run_all(code, tests_json, files_json='{}'):\n    _clean()\n    tests = json.loads(tests_json)\n    files = json.loads(files_json) if files_json else {}\n    if not tests:\n        tests = [{}]\n    return json.dumps([_one(code, t, files) for t in tests], ensure_ascii=False)\n";
let py = null;
const ready = (async () => {
  importScripts(PYO + 'pyodide.js');
  py = await loadPyodide({ indexURL: PYO });
  py.runPython(HARNESS);
  postMessage({ t: 'ready' });
})().catch(e => postMessage({ t: 'fail', err: String(e) }));

onmessage = async ev => {
  await ready;
  const { id, code, tests, files } = ev.data;
  if (!py) { postMessage({ id, fatal: 'Python no está disponible' }); return; }
  try {
    if (/\b(numpy|imageio|PIL)\b/.test(code + tests + files) && !self._np) { await py.loadPackage('numpy'); self._np = true; }
    const r = py.globals.get('run_all')(code, tests, files);
    postMessage({ id, res: JSON.parse(r) });
  } catch (e) {
    postMessage({ id, fatal: String(e) });
  }
};
