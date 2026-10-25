#!/usr/bin/env python3
"""Inyecta tools/s11_widgets.js y tools/s11.css en index.html (interactivos de la semana 11: rel, heav, riem, virt).
Reemplaza lo que haya entre /* S11-JS-START */…/* S11-JS-END */ y /* S11-CSS-START */…/* S11-CSS-END */;
si los marcadores no existen, los crea justo después de los de Programación I."""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(R, 'index.html')
s = open(p, encoding='utf-8').read()
js = open(os.path.join(R, 'tools', 's11_widgets.js'), encoding='utf-8').read().rstrip('\n')
css = open(os.path.join(R, 'tools', 's11.css'), encoding='utf-8').read().rstrip('\n')
def put(s, a, b, body, after):
    blk = a + '\n' + body + '\n' + b
    if a in s:
        i, j = s.index(a), s.index(b) + len(b)
        return s[:i] + blk + s[j:]
    k = s.index(after) + len(after)
    return s[:k] + '\n' + blk + s[k:]
s = put(s, '/* S11-JS-START */', '/* S11-JS-END */', js, '/* P1-JS-END */')
s = put(s, '/* S11-CSS-START */', '/* S11-CSS-END */', css, '/* P1-CSS-END */')
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(js), len(css))
