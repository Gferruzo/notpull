#!/usr/bin/env python3
"""Inyecta tools/p1_widgets.js y tools/p1.css en index.html (Programación I).
Reemplaza lo que haya entre /* P1-JS-START */…/* P1-JS-END */ y /* P1-CSS-START */…/* P1-CSS-END */;
si los marcadores no existen, los crea justo después de los de Análisis Bioquímico."""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(R, 'index.html')
s = open(p, encoding='utf-8').read()
js = open(os.path.join(R, 'tools', 'p1_widgets.js'), encoding='utf-8').read().rstrip('\n')
css = open(os.path.join(R, 'tools', 'p1.css'), encoding='utf-8').read().rstrip('\n')
def put(s, a, b, body, after):
    blk = a + '\n' + body + '\n' + b
    if a in s:
        i, j = s.index(a), s.index(b) + len(b)
        return s[:i] + blk + s[j:]
    k = s.index(after) + len(after)
    return s[:k] + '\n' + blk + s[k:]
s = put(s, '/* P1-JS-START */', '/* P1-JS-END */', js, '/* BQ-JS-END */')
s = put(s, '/* P1-CSS-START */', '/* P1-CSS-END */', css, '/* BQ-CSS-END */')
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(js), len(css))
