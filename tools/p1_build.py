#!/usr/bin/env python3
"""Construye Programación I (CS6002): cursos/p1-pc3.json (Práctica 3) y cursos/p1-ef.json (Examen final).
Todo se verifica al construir (ver p1_lib.py). Uso: python3 tools/p1_build.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p1_lib import *
import p1_t1, p1_t2, p1_t3

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CON = {}
for m in (p1_t1, p1_t2, p1_t3): CON.update(m.CONCEPTS)

PC3 = [p1_t1.cadenas(), p1_t1.listas(), p1_t1.cortes(), p1_t2.matrices1(), p1_t2.matrices2(), p1_t2.mix()]
EF_NEW = p1_t3.final_topics()          # repaso sem. 1–8 (va primero) y lo nuevo desde la sem. 10
REPASO, NUEVOS = EF_NEW[0], EF_NEW[1:]

def check_ids(topics, simex):
    ids = [e['id'] for t in topics for e in t['ex']] + [e['id'] for e in simex]
    assert len(ids) == len(set(ids)), 'ids repetidos: ' + str([i for i in ids if ids.count(i) > 1])
    return set(ids)

def concepts_for(topics):
    used = {k for t in topics for e in t['ex'] for tg in e['tags'] for k in tg}
    homes = {t['id'] for t in topics}
    out = {}
    for k in used:
        assert k in CON, 'concepto sin definir: ' + k
        out[k] = dict(CON[k])
        if out[k]['home'] not in homes: out[k]['home'] = topics[0]['id']
    return out

def pool(topics, kind=None, tag=None):
    r = []
    for t in topics:
        for e in t['ex']:
            ts = [c.get('t') for c in e['checks']]
            if kind == 'code' and 'code' not in ts: continue
            if tag and e.get('pc') != tag: continue
            r.append(e['id'])
    return r

FORM_PC3 = '<p class="note">Hoja de repaso de la Práctica 3 (semanas 9 y 10): cadenas, listas, cortes y matrices.</p>\n<div class="fgrid">\n' + '\n'.join('<div>' + x + '</div>' for x in [
    '<b>Cadenas</b><br><code>s.lower() · s.upper() · s.split() · s.strip() · s.count(x) · s.find(x) · x in s</code>',
    '<b>Tipo de carácter</b><br><code>isupper() · islower() · isalpha() · isdigit()</code>',
    '<b>Inicio de palabra sin split</b><br><code>i == 0 or s[i-1] == " "</code>',
    '<b>Listas</b><br><code>append(x) · insert(i, x) · pop(i) · remove(x) · del l[i] · index(x) · x in l</code>',
    '<b>Copiar</b><br><code>b = a</code> NO copia · <code>a[:]</code> · <code>a.copy()</code>',
    '<b>Cortes</b><br><code>l[ini:fin:paso]</code> (fin no incluido) · <code>[::-1]</code> invierte · fuera de rango no da error',
    '<b>Matriz</b><br><code>mat[f][c]</code> · filas <code>len(mat)</code> · columnas <code>len(mat[0])</code>',
    '<b>Crear n × m</b><br><code>mat = []</code> y <code>mat.append([0] * m)</code> n veces · nunca <code>[[0]*m]*n</code>',
    '<b>Recorridos</b><br>fila f fija: <code>for c</code> · columna c fija: <code>for f</code> · toda: <code>for f</code> + <code>for c</code>',
    '<b>Borde</b><br><code>f == 0 or f == filas-1 or c == 0 or c == col-1</code>',
    '<b>Vecinos</b><br><code>0 &lt;= f &lt; filas and 0 &lt;= c &lt; col</code> antes de usar <code>mat[f][c]</code>',
    '<b>Imprimir tabla</b><br><code>print("%5d" % x, end="")</code> y <code>print()</code> al final de cada fila']) + '\n</div>'

def build():
    simex = p1_t2.simex_pc3()
    ids = check_ids(PC3, simex)
    sim = {'minutes': 100, 'slots': [
        {'pts': 5, 'name': 'String', 'pool': pool(PC3, 'code', 'str')},
        {'pts': 5, 'name': 'Listas', 'pool': pool(PC3, 'code', 'lis')},
        {'pts': 5, 'name': 'Matrices', 'pool': pool(PC3, 'code', 'mat') + [e['id'] for e in simex if e.get('pc') == 'mat']},
        {'pts': 5, 'name': 'Mix de string, listas y matrices', 'pool': pool(PC3, 'code', 'mix') + [e['id'] for e in simex if e.get('pc') == 'mix']}],
        'intro': 'Como la Práctica 3: <b>4 preguntas de 5 puntos</b> (string, listas, matrices y un mix), <b>100 minutos</b> y en computadora. Cada intento elige al azar un problema de cada bloque; al entregar, tu código se corre con pruebas automáticas (algunas ocultas) y cada pregunta vale según cuántas pasa. Implementa exactamente la función que pide el enunciado y usa <code>return</code>. Puedes usar ▶ Ejecutar para probar.'}
    for s in sim['slots']:
        assert s['pool'] and all(i in ids for i in s['pool']), s
    pc3 = {'id': 'p1-pc3', 'code': 'CS6002', 'tapa': {'p': 'estrellas', 'c': ['#F2C14E', '#FFF1C2', '#8A5A00', '#3A2600']},
           'name': 'Programación I', 'exam': 'Práctica 3 2026-2 (sem. 9–10)', 'short': 'Práctica 3', 'sub': 'Sem. 9–10',
           'intro': '<b>La Práctica 3 es presencial, en el laboratorio (semana 12, sesión 12B)</b>. Temas: string, listas, matrices y un mix de los tres. Cada tema avanza así: teoría → «¿qué imprime?» → <b>completa el código</b> (solo escribes en las cajitas) → <b>encuentra el error</b> → escribe la función completa con pruebas, como en Gradescope. En el 🧪 Interactivo de cada tema hay un ejecutor paso a paso, un cortador de listas y recorridos animados de matrices.',
           'form': FORM_PC3, 'formSim': False, 'formLabel': '📋 Hoja de repaso', 'keyLabel': 'Claves del tema', 'py': True,
           'topics': PC3, 'figs': {}, 'concepts': concepts_for(PC3), 'simEx': simex, 'sim': sim}
    jdump(pc3, os.path.join(R, 'cursos', 'p1-pc3.json'))
    # ---- examen final ----
    eft = [REPASO] + PC3 + NUEVOS
    fsimex = simex + p1_t3.simex_ef()
    fids = check_ids(eft, fsimex)
    teo_pool = [e['id'] for t in eft for e in t['ex'] if all(c.get('t') is None for c in e['checks']) and 'Salida' not in json.dumps(e['checks'][0].get('p', ''))]
    slots = [
        {'pts': 2, 'name': 'Teoría', 'pool': teo_pool},
        {'pts': 2, 'name': 'Sem. 1–8: bucles y cadenas', 'pool': pool([REPASO], 'code')},
        {'pts': 4, 'name': 'Sem. 9: cadenas, listas y cortes', 'pool': pool(PC3[:3], 'code')},
        {'pts': 4, 'name': 'Sem. 9–10: matrices', 'pool': pool(PC3[3:5], 'code') + [e['id'] for e in simex if e.get('pc') == 'mat']},
        {'pts': 3, 'name': 'Sem. 10: NumPy e imágenes', 'pool': list(p1_t3.SIM_NP)},
        {'pts': 5, 'name': 'Sem. 11: diccionarios', 'pool': pool([t for t in NUEVOS if t['id'] in ('d11', 'a11')], 'code') + [e['id'] for e in fsimex if e.get('pc') == 'dic']}]
    for s in slots:
        assert s['pool'] and all(i in fids for i in s['pool']), s
    intro = 'Repaso acumulado del curso con los temas ordenados por semana. <b>El examen final de teoría vale 16 %</b> (semana 16) y es en Python. El simulacro tiene <b>dos modalidades</b> (en computadora o escrito, sin ejecutar) y mezcla teoría, completar código y escribir funciones, con más peso en lo último (diccionarios). Se actualiza cada semana: ya están las semanas 9, 10 y 11.'
    vers = [{'name': '💻 En computadora', 'desc': 'Puedes ejecutar tu código mientras resuelves.', 'minutes': 110, 'slots': slots, 'intro': intro},
            {'name': '✍️ Escrito', 'desc': 'Los mismos bloques a mano: no puedes ejecutar.', 'minutes': 110, 'slots': slots, 'noRun': True,
             'intro': intro + ' <b>Modo escrito:</b> no puedes ejecutar; tu código solo se prueba al entregar, como si el profe lo corrigiera a mano.'}]
    fsim = {'minutes': 110, 'slots': slots, 'intro': intro, 'versions': vers, 'vtitle': '¿Cómo será tu examen final?'}
    form_ef = FORM_PC3.replace('Hoja de repaso de la Práctica 3 (semanas 9 y 10): cadenas, listas, cortes y matrices.', 'Hoja de repaso del examen final: lo de la Práctica 3 y, al final, NumPy, imágenes y diccionarios.').replace('\n</div>', '\n' + '\n'.join('<div>' + x + '</div>' for x in [
        '<b>NumPy</b><br><code>import numpy as np · np.array(l) · arr.shape · arr[f, c] · np.zeros((f, c))</code>',
        '<b>Cortes 2D</b><br><code>arr[filas, columnas]</code> · <code>arr[:, 0]</code> columna 0 · <code>arr[1:, 1:3]</code>',
        '<b>Imagen</b><br>alto × ancho × 3 (R, G, B) · 0 = nada, 255 = máximo · gris: un canal',
        '<b>Diccionario</b><br><code>d = {}</code> · <code>d[k] = v</code> agrega o cambia · <code>k in d</code> · <code>del d[k]</code> · <code>d.pop(k)</code>',
        '<b>Recorrer</b><br><code>for k in d</code> · <code>d.keys()</code> · <code>d.values()</code> · <code>for k, v in d.items()</code>',
        '<b>Contar</b><br><code>if k in d: d[k] += 1</code> · <code>else: d[k] = 1</code> · o <code>d[k] = d.get(k, 0) + 1</code>',
        '<b>Anidados</b><br><code>d[1]["nombre"]</code> · <code>d[3] = {}</code> y luego <code>d[3]["edad"] = 24</code>']) + '\n</div>')
    ef = {'id': 'p1-ef', 'code': 'CS6002', 'name': 'Programación I', 'exam': 'Examen final 2026-2 (todo el curso)', 'short': 'Examen final', 'sub': 'Todo el curso', 'free': True,
          'intro': intro, 'form': form_ef, 'formSim': False, 'formLabel': '📋 Hoja de repaso', 'keyLabel': 'Claves del tema', 'py': True,
          'topics': eft, 'figs': {}, 'concepts': concepts_for(eft), 'simEx': fsimex, 'sim': fsim}
    jdump(ef, os.path.join(R, 'cursos', 'p1-ef.json'))
    # ---- índice ----
    ip = os.path.join(R, 'cursos', 'indice.json'); idx = json.load(open(ip, encoding='utf-8'))
    for k in ('p1-pc3', 'p1-ef'):
        if k not in idx['cursos']:
            i = idx['cursos'].index('p2-ef') + 1 if 'p1-pc3' not in idx['cursos'] else idx['cursos'].index('p1-pc3') + 1
            idx['cursos'].insert(i, k)
    jdump(idx, ip)
    n1 = sum(len(t['ex']) for t in PC3); n2 = sum(len(t['ex']) for t in eft)
    print('p1-pc3:', len(PC3), 'temas,', n1, 'ejercicios,', len(simex), 'simEx · p1-ef:', len(eft), 'temas,', n2, 'ejercicios')

if __name__ == '__main__':
    build()
