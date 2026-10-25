#!/usr/bin/env python3
"""Validador de NotPull.

Uso:
  python3 tools/validar.py                 # revisa todos los cursos
  python3 tools/validar.py cursos/x.json   # solo esos archivos

Sale con código 1 si hay ERRORES (los AVISOS no bloquean).
Lo corre GitHub Actions en cada push y PR (.github/workflows/validar.yml).
"""
import json, re, sys, glob, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

TIPOS = {"hueco", "bug", "slice", "mtx", "traza", "num", "expr", "cls", "code", "mat", "tap", "ptab", "order", "sql", "esc",
         "shift", "vecdraw", "cols", "tlc", "fill", "dcl", "tt", "econf", "fit",
         "fix", "signs", "star", "mem", "acum", "usub", "tri", "lab", "tree", "mkt", "tira", "micro", "espec",
         "val", "ley", "arg", "mundo", "venn", "rel", "heav", "virt", "nash", "qmax"}
OBLIG_CURSO = ["id", "code", "name", "exam", "short", "form", "topics", "concepts", "sim"]
OBLIG_TEMA = ["id", "name", "teo", "form", "lesson", "ex"]
OBLIG_EJ = ["id", "title", "q", "checks", "steps"]

errores, avisos = [], []
def E(f, m): errores.append(f"❌ {f}: {m}")
def A(f, m): avisos.append(f"⚠️  {f}: {m}")

def delims(s):
    """Cuenta \\( \\) y \\[ \\] desbalanceados en un texto."""
    return s.count("\\(") != s.count("\\)") or s.count("\\[") != s.count("\\]")

def textos(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, list):
        for y in x: yield from textos(y)
    elif isinstance(x, dict):
        for y in x.values(): yield from textos(y)

def revisar_formato(f):
    raw = open(f, encoding="utf-8").read()
    try:
        d = json.loads(raw)
    except Exception as ex:
        E(f, f"JSON inválido: {ex}")
        return None
    if not raw.endswith("\n"):
        A(f, "falta salto de línea final")
    if "\\u00" in raw[:5000]:
        A(f, "guardado con ensure_ascii=True (usar ensure_ascii=False)")
    return d

def revisar_ej(f, e, conceptos, com2, donde):
    for k in OBLIG_EJ:
        if k not in e:
            E(f, f"{donde} {e.get('id','?')}: falta «{k}»")
    eid = e.get("id", "?")
    for i, c in enumerate(e.get("checks", [])):
        t = c.get("t")
        if t is None:
            o = c.get("o")
            if not isinstance(o, list):
                E(f, f"{eid} parte {i+1}: pregunta de opciones sin lista «o»")
                continue
            if len(o) < 2:
                E(f, f"{eid} parte {i+1}: menos de 2 opciones")
            if len(set(map(str, o))) != len(o):
                E(f, f"{eid} parte {i+1}: opciones repetidas")
        elif t not in TIPOS:
            E(f, f"{eid} parte {i+1}: tipo «{t}» no existe en index.html")
        elif t == "arg" and not c.get("sol"):
            E(f, f"{eid} parte {i+1}: «arg» sin «sol» (la deducción modelo)")
        elif t == "venn" and not (c.get("a") if c.get("mode", "tap") == "tap" else isinstance(c.get("v"), dict)):
            E(f, f"{eid} parte {i+1}: «venn» sin respuesta («a» en tap, «v» en num)")
        elif t == "mundo" and not c.get("sol"):
            E(f, f"{eid} parte {i+1}: «mundo» sin «sol» (un mundo que cumpla)")
        elif t == "num":
            for fl in c.get("f", []):
                if not isinstance(fl.get("a"), (int, float)):
                    E(f, f"{eid}: casilla num «{fl.get('l')}» sin respuesta numérica «a»")
        elif t == "expr":
            for fl in c.get("f", []):
                if not isinstance(fl.get("a"), str) or not fl["a"].strip():
                    E(f, f"{eid}: casilla expr sin «a»")
        elif t == "cls":
            n = len(c.get("cats", []))
            for it in c.get("items", []):
                if not (isinstance(it.get("c"), int) and 0 <= it["c"] < n):
                    E(f, f"{eid}: tarjeta cls «{str(it.get('x'))[:30]}» con categoría fuera de rango")
    tags = e.get("tags")
    if tags is not None:
        for lst in tags:
            for k in (lst or []):
                if k not in conceptos:
                    E(f, f"{eid}: tag «{k}» no está en «concepts»")
    for s in textos([e.get("q"), e.get("steps"), e.get("checks")]):
        if delims(s):
            E(f, f"{eid}: delimitadores de fórmula \\( \\) desbalanceados")
            break

def revisar_curso(f, d):
    for k in OBLIG_CURSO:
        if k not in d:
            E(f, f"falta «{k}» en el curso")
    esperado_id = os.path.basename(f)[:-5]
    if d.get("id") != esperado_id:
        E(f, f"id «{d.get('id')}» no coincide con el nombre del archivo «{esperado_id}»")
    com2 = esperado_id.startswith("com2")
    conceptos = d.get("concepts", {}) or {}
    ids_tema, ids_ej = set(), set()
    for t in d.get("topics", []):
        for k in OBLIG_TEMA:
            if k not in t:
                E(f, f"tema {t.get('id','?')}: falta «{k}»")
        if t.get("id") in ids_tema:
            E(f, f"tema repetido: {t.get('id')}")
        ids_tema.add(t.get("id"))
        nom = t.get("name", "")
        if not com2 and not re.match(r"^(Sem\. \d+(–\d+)? · |Repaso · |PC\d · |Tipo PC\d · |E[AD]\d · )", nom):
            A(f, f"tema «{nom}» no sigue el formato «Sem. N · …»")
        for e in t.get("ex", []):
            if e.get("id") in ids_ej:
                E(f, f"ejercicio repetido: {e.get('id')}")
            ids_ej.add(e.get("id"))
            revisar_ej(f, e, conceptos, com2, f"tema {t.get('id')}")
    for e in d.get("simEx", []) or []:
        if e.get("id") in ids_ej:
            E(f, f"ejercicio repetido (simEx): {e.get('id')}")
        ids_ej.add(e.get("id"))
        revisar_ej(f, e, conceptos, com2, "simEx")
    figs = d.get("figs", {}) or {}
    for t in d.get("topics", []):
        for e in t.get("ex", []):
            if e.get("fig") and e["fig"] not in figs:
                E(f, f"{e['id']}: fig «{e['fig']}» no está en «figs»")
    sim = d.get("sim") or {}
    if not d.get("soon"):
        slots = sim.get("slots", [])
        if not slots:
            A(f, "simulacro sin slots")
        for s in slots:
            for pid in s.get("pool", []):
                if pid not in ids_ej:
                    E(f, f"sim «{s.get('name')}»: id «{pid}» del pool no existe")
    for s in textos([d.get("form"), [t.get("teo") for t in d.get("topics", [])]]):
        if delims(s):
            A(f, "teoría u hoja de repaso con \\( \\) desbalanceados")
            break

def main():
    archivos = sys.argv[1:] or sorted(glob.glob("cursos/*.json"))
    try:
        indice = json.load(open("cursos/indice.json", encoding="utf-8"))["cursos"]
    except Exception as ex:
        E("cursos/indice.json", f"no se pudo leer: {ex}")
        indice = []
    for cid in indice:
        if not os.path.exists(f"cursos/{cid}.json"):
            E("cursos/indice.json", f"«{cid}» está en el índice pero no existe cursos/{cid}.json")
    for f in archivos:
        b = os.path.basename(f)
        d = revisar_formato(f)
        if d is None or b in ("indice.json", "novedades.json"):
            continue
        if b[:-5] not in indice:
            E(f, "no está en cursos/indice.json")
        revisar_curso(f, d)
    for m in avisos: print(m)
    for m in errores: print(m)
    print(f"\n{len(errores)} errores · {len(avisos)} avisos · {len(archivos)} archivos")
    sys.exit(1 if errores else 0)

if __name__ == "__main__":
    main()
