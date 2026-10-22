/* ================= PROGRAMACIÓN I (CS6002): interactivos =================
   IW.hueco: completa el código con cajitas bloqueadas. ch.code (los huecos se escriben ⟦0⟧, ⟦1⟧…),
             ch.b=[{a:[respuestas aceptadas], h:pista, e:explicación si falla, w:ancho en caracteres}],
             ch.tests (como en «code»: si una cajita no coincide con ninguna aceptada, se corre el código y vale si pasa todas),
             ch.demo (código extra para ▶ Probar, p. ej. un print).
   IW.bug:   encuentra el error. ch.code, ch.l=[líneas con el error, desde 1], ch.o=[motivo correcto, …], ch.out (lo que pasa al ejecutarlo), ch.e.
   IW.slice: cortes. ch.seq (lista o texto), ch.name. mode 'tap': ch.expr y ch.a (índices que toma); mode 'build': ch.goal (lista o texto) y ch.sol=[inicio,fin,paso] (null = vacío).
   IW.mtx:   tocar celdas de una matriz. ch.m, ch.a=[[f,c]…], ch.ord (importa el orden), ch.name.
   IW.traza: tabla de rastreo. ch.code, ch.head, ch.rows (texto fijo o {a:"…" | ["…","…"]}).
   LW.paso:  ejecutar paso a paso (precalculado en tools/p1_build.py). o.code, o.steps=[{l, f:[[marco,[[var,val]…]]…], h:{id:{t,v}}, o:salida}];
             val = repr o «@id» (referencia a un objeto de h). Muestra variables, objetos (listas/diccionarios con etiqueta y color) y salida.
   LW.slice: cortador libre (o.seq, o.name).  LW.mtx: recorridos animados (o.m, o.modes).  LW.img: laboratorio de imágenes con NumPy (o.code, o.target). */
const P1N=s=>String(s==null?'':s).replace(/\s+/g,'').replace(/"/g,"'");
const p1R=v=>typeof v==='string'?"'"+v+"'":String(v);
const p1Rl=(seq,ix)=>typeof seq==='string'?"'"+ix.map(i=>seq[i]).join('')+"'":'['+ix.map(i=>p1R(seq[i])).join(', ')+']';
function p1Sl(n,a,b,c){c=c==null?1:c;const r=[];
  if(c>0){const s=a==null?0:a<0?Math.max(0,a+n):Math.min(a,n);const e=b==null?n:b<0?Math.max(0,b+n):Math.min(b,n);for(let i=s;i<e;i+=c)r.push(i)}
  else{const s=a==null?n-1:a<0?Math.max(-1,a+n):Math.min(a,n-1);const e=b==null?-1:b<0?Math.max(-1,b+n):Math.min(b,n-1);for(let i=s;i>e;i+=c)r.push(i)}return r}
const p1Ex=(a,b,c)=>(a==null?'':a)+':'+(b==null?'':b)+(c==null?'':':'+c);
/* ---------- Completa el código (cajitas) ---------- */
IW.hueco=(ch,o)=>{const w=el('div','p1hw');const pre=el('pre','py p1hc');pre.dataset.hl=1;const code=el('code');pre.append(code);w.append(pre);
  const ins=[];let lk=false,cache=null;
  ch.code.split(/⟦(\d+)⟧/).forEach((p,i)=>{if(i%2===0){const s=el('span');s.innerHTML=hlPy(p);code.append(s);return}
    const k=+p,b=ch.b[k];const x=el('input','p1in');x.type='text';x.placeholder=String(k+1);x.spellcheck=false;x.autocomplete='off';['autocapitalize','autocorrect'].forEach(a=>x.setAttribute(a,'off'));
    x.setAttribute('aria-label','Cajita '+(k+1));const w0=Math.max(3,b.w||(String(b.a[0]).length+2))+1;const grow=()=>{x.style.width=Math.max(w0,x.value.length+2)+'ch'};grow();
    x.oninput=()=>{grow();x.classList.remove('good','bad','rev');cache=null;o.on&&o.on()};x.__g=grow;code.append(x);ins[k]={i:x,b,k}});
  const okB=x=>x.b.a.some(a=>P1N(a)===P1N(x.i.value));
  const full=()=>ch.code.replace(/⟦(\d+)⟧/g,(m,k)=>ins[+k].i.value);
  const cur=()=>ins.map(x=>x.i.value).join('\u0001');
  const out=el('div','cout');out.hidden=true;let help=null;
  if(!o.sim&&!o.pre){help=el('div','p1help');const hb=el('div','p1hb');help.append(el('span','p1hl','💡 Ayuda por cajita:'),hb);const tip=el('div','p1tip');tip.hidden=true;help.append(tip);let open=-1;
    ins.forEach(x=>{const b=el('button','p1chip',String(x.k+1));b.type='button';b.onclick=()=>{if(open===x.k){tip.hidden=true;open=-1;return}open=x.k;tip.hidden=false;tip.innerHTML='';
        tip.append(el('p',null,'<b>Cajita '+(x.k+1)+':</b> '+(x.b.h||'Fíjate qué valor necesita esa parte del código.')));const rv=el('button','p1rv','Ver la respuesta de la cajita '+(x.k+1));rv.type='button';
        rv.onclick=()=>{if(lk)return;x.i.value=x.b.a[0];x.i.__g();x.i.classList.remove('bad','good');x.i.classList.add('rev');cache=null;o.on&&o.on()};tip.append(rv)};hb.append(b)});
    w.append(help);
    if(ch.demo||ch.tests){const pb=el('button','p1try','▶ Probar mi código');pb.type='button';const ps=el('span','pyst');const row=el('div','p1acts');row.append(pb,ps);w.append(row,out);
      pb.onclick=async()=>{if(ins.some(x=>!x.i.value.trim())){out.hidden=false;out.innerHTML='';out.append(el('p','fb bad','Llena todas las cajitas para poder ejecutar.'));return}
        pb.disabled=true;ps.textContent='⏳ Ejecutando…';const src=full()+(ch.demo?'\n'+ch.demo:'');const m=await pyRun(src,[{}]);pb.disabled=false;ps.textContent='';out.hidden=false;out.innerHTML='';
        if(m.fail){out.append(el('p','fb bad',PYFAIL));return}if(m.timeout){out.append(el('p','fb bad',PYTO));return}
        const r=(m.res||[])[0]||{};out.append(kvBox('Salida',r.out||''));if(r.err)out.append(el('p','cerr','💥 '+escH(r.err)))}}}
  const sync=()=>{const bad=ins.filter(x=>!okB(x));return{f:(ins.length-bad.length)/ins.length,bad:bad.map(x=>x.k),
    msg:bad.length?(bad.length===1?'Una cajita no está bien (en rojo).':bad.length+' cajitas no están bien (en rojo).')+bad.filter(x=>x.b.e).slice(0,3).map(x=>'<br>• <b>Cajita '+(x.k+1)+':</b> '+x.b.e).join(''):''}};
  const agrade=async()=>{const k=cur();if(cache&&cache.k===k)return cache.g;let g=sync();
    if(g.f<1&&ch.tests&&ch.tests.length){const m=await pyRun(full(),ch.tests);
      if(m.res&&m.res.length&&m.res.every(r=>r.ok))g={f:1,all:true,msg:''};
      else if(m.res){const p=m.res.filter(r=>r.ok).length;g.msg+='<br>Al ejecutarlo, pasa '+p+' de '+m.res.length+' pruebas.';const e=m.res.find(r=>r.err);if(e)g.msg+='<br>💥 '+escH(e.err)}}
    cache={k,g};return g};
  return{el:w,note:'Escribe solo dentro de las cajitas. Cada una se corrige por separado.',need:'Completa todas las cajitas antes de comprobar.',okMsg:'¡Código completo y correcto!',
    filled:()=>ins.every(x=>x.i.value.trim()!==''),
    grade(){const k=cur();if(cache&&cache.k===k)return cache.g;return sync()},agrade,prep:agrade,
    mark(g){ins.forEach(x=>{if(x.i.classList.contains('rev')&&okB(x))return;const k=g.all||okB(x);x.i.classList.toggle('good',k);x.i.classList.toggle('bad',!k)})},
    reveal(){ins.forEach(x=>{if(!okB(x)){x.i.value=x.b.a[0];x.i.__g();x.i.classList.remove('bad');x.i.classList.add('rev')}else x.i.classList.add('good')});cache=null},
    lock(){lk=true;ins.forEach(x=>x.i.disabled=true);if(help)help.hidden=true}}};
/* ---------- Encuentra el error ---------- */
IW.bug=(ch,o)=>{const w=el('div','p1bug');const L=ch.code.split('\n');let sel=-1,rs=-1,lk=false;
  if(ch.out){w.append(el('p','clab',ch.outLabel||'Al ejecutarlo pasa esto:'));const p=el('pre','cons p1bout');p.textContent=ch.out;w.append(p)}
  w.append(el('p','p1bq','<b>1.</b> Toca la línea que tiene el error.'));
  const box=el('div','p1bl');const lines=L.map((s,i)=>{const b=el('button','p1ln');b.type='button';b.innerHTML='<span class="p1no">'+(i+1)+'</span><code>'+(hlPy(s)||' ')+'</code>';
    b.onclick=()=>{if(lk)return;sel=i;lines.forEach((x,j)=>{x.classList.toggle('on',j===i);x.classList.remove('good','bad')});o.on&&o.on()};box.append(b);return b});w.append(box);
  w.append(el('p','p1bq','<b>2.</b> ¿Por qué falla?'));const og=el('div','p1bo');const ord=perm((o.key||'')+'#bug',ch.o.length);
  const ob=ord.map(i=>{const b=el('button','opt',ch.o[i]);b.type='button';b.dataset.i=i;b.onclick=()=>{if(lk)return;rs=i;ob.forEach(x=>{x.classList.toggle('on',x===b);x.classList.remove('good','bad')});o.on&&o.on()};og.append(b);return b});w.append(og);
  return{el:w,need:'Elige la línea y el motivo antes de comprobar.',okMsg:'¡Encontraste el error!',
    filled:()=>sel>=0&&rs>=0,
    grade(){const a=ch.l.includes(sel+1),b=rs===0;return{f:(a?.5:0)+(b?.5:0),a,b,msg:[a?'':'La línea marcada no es la del error.',b?'':'El motivo no es ese.'].filter(Boolean).join(' ')+(!(a&&b)&&ch.e?'<br>'+ch.e:'')}},
    mark(g){if(sel>=0)lines[sel].classList.add(g.a?'good':'bad');ob.forEach(x=>{if(+x.dataset.i===rs)x.classList.add(g.b?'good':'bad')})},
    reveal(){sel=ch.l[0]-1;rs=0;lines.forEach((x,j)=>{x.classList.toggle('on',j===sel);x.classList.remove('bad');x.classList.toggle('good',ch.l.includes(j+1))});ob.forEach(x=>{x.classList.toggle('on',+x.dataset.i===0);x.classList.remove('bad');x.classList.toggle('good',+x.dataset.i===0)})},
    lock(){lk=true;lines.forEach(x=>x.disabled=true);ob.forEach(x=>x.disabled=true)}}};
/* ---------- Celdas de una lista o cadena (con índices positivos y negativos) ---------- */
function p1Cells(seq,onTap){const n=seq.length;const w=el('div','p1cells');const t=el('div','p1crow');const cells=[];
  for(let i=0;i<n;i++){const c=el(onTap?'button':'div','p1cell');if(onTap)c.type='button';c.innerHTML='<i>'+i+'</i><b>'+escH(typeof seq==='string'?(seq[i]===' '?'␣':seq[i]):String(seq[i]))+'</b><i>'+(i-n)+'</i><u></u>';if(onTap)c.onclick=()=>onTap(i);t.append(c);cells.push(c)}
  w.append(t);return{el:w,cells,show(ix,cls){cells.forEach((c,i)=>{const k=ix.indexOf(i);c.classList.toggle(cls||'on',k>=0);c.querySelector('u').textContent=k>=0?String(k+1):''})}}}
function p1Sel(lbl,vals,v,on){const d=el('label','p1sel');d.append(el('span',null,lbl));const s=el('select');vals.forEach(x=>{const op=el('option',null,x==null?'(vacío)':String(x));op.value=x==null?'':String(x);s.append(op)});
  s.value=v==null?'':String(v);s.onchange=()=>on(s.value===''?null:+s.value);d.append(s);return{el:d,s,set(x){s.value=x==null?'':String(x)}}}
function p1Builder(seq,name,on,step){const n=seq.length;const idx=[null];for(let i=-n;i<=n;i++)idx.push(i);const st=[null];for(let i=-3;i<=3;i++)if(i)st.push(i);
  const v=[null,null,null];const row=el('div','p1slr');const ex=el('div','p1slx');
  const S=[p1Sel('inicio',idx,null,x=>{v[0]=x;on(v)}),p1Sel('fin',idx,null,x=>{v[1]=x;on(v)}),p1Sel('paso',step===false?[null]:st,null,x=>{v[2]=x;on(v)})];S.forEach(x=>row.append(x.el));
  return{el:row,v,set(a){a.forEach((x,i)=>{v[i]=x;S[i].set(x)});on(v)},dis(){S.forEach(x=>x.s.disabled=true)}}}
IW.slice=(ch,o)=>{const w=el('div','p1slw');const seq=ch.seq,n=seq.length,name=ch.name||'l';let lk=false;
  w.append(preCode(name+' = '+(typeof seq==='string'?"'"+seq+"'":'['+seq.map(p1R).join(', ')+']')));
  if((ch.mode||'tap')==='tap'){const sel=[];const A=ch.a;w.append(el('p','p1bq','Toca, en orden, los elementos que toma <code>'+escH(ch.expr)+'</code>.'));
    const C=p1Cells(seq,i=>{if(lk)return;const k=sel.indexOf(i);if(k>=0)sel.splice(k,1);else sel.push(i);C.show(sel);res();o.on&&o.on()});w.append(C.el);
    const ro=el('p','p1ro');w.append(ro);const res=()=>{ro.innerHTML=sel.length?'Tu respuesta: <code>'+escH(p1Rl(seq,sel))+'</code>':'Aún no tocas ningún elemento.'};res();
    const same=()=>sel.length===A.length&&sel.every((x,i)=>x===A[i]);
    return{el:w,need:A.length?'Toca al menos un elemento.':'',okMsg:'¡Corte correcto!',
      filled:()=>sel.length>0||A.length===0,
      grade(){if(same())return{f:1};const sa=new Set(A),ss=new Set(sel);const set=sa.size===ss.size&&[...sa].every(x=>ss.has(x));
        return{f:0,msg:set?'Son esos elementos, pero en otro orden: revisa el signo del paso.':'No son esos elementos. Recuerda: el fin no se incluye y el paso indica cuánto avanzar.'}},
      mark(g){C.cells.forEach((c,i)=>{c.classList.remove('good','bad');if(sel.includes(i))c.classList.add(g.f>=1||A.includes(i)?'good':'bad')})},
      reveal(){sel.length=0;A.forEach(x=>sel.push(x));C.show(sel);C.cells.forEach((c,i)=>{c.classList.remove('bad');c.classList.toggle('good',A.includes(i))});res()},
      lock(){lk=true;C.cells.forEach(c=>c.disabled=true)}}}
  const goal=ch.goal;const gs=typeof goal==='string'?"'"+goal+"'":'['+goal.map(p1R).join(', ')+']';
  w.append(el('p','p1bq','Arma el corte de <code>'+escH(name)+'</code> que da <code>'+escH(gs)+'</code>.'));
  const C=p1Cells(seq);const ro=el('p','p1ro');let cur=[null,null,null],touched=false;
  const B=p1Builder(seq,name,v=>{cur=v.slice();touched=true;const ix=p1Sl(n,v[0],v[1],v[2]);C.show(ix);ro.innerHTML='<code>'+escH(name+'['+p1Ex(v[0],v[1],v[2])+']')+'</code> → <code>'+escH(p1Rl(seq,ix))+'</code>';o.on&&o.on()},ch.step);
  w.append(B.el,C.el,ro);ro.innerHTML='Elige inicio, fin y paso.';
  const got=()=>p1Rl(seq,p1Sl(n,cur[0],cur[1],cur[2]));
  return{el:w,need:'Elige al menos un valor.',okMsg:'¡Ese corte funciona!',filled:()=>touched,
    grade(){return got()===gs?{f:1}:{f:0,msg:'Tu corte da <code>'+escH(got())+'</code>, no <code>'+escH(gs)+'</code>.'}},
    mark(g){ro.classList.toggle('good',g.f>=1);ro.classList.toggle('bad',g.f<1)},
    reveal(){B.set(ch.sol);ro.classList.remove('bad');ro.classList.add('good')},lock(){lk=true;B.dis()}}};
LW.slice=(b,o)=>{const seq=o.seq||[18,17,20,16,15,19],n=seq.length,name=o.name||'notas';const w=el('div','p1slw');
  w.append(preCode(name+' = '+(typeof seq==='string'?"'"+seq+"'":'['+seq.map(p1R).join(', ')+']')));
  const C=p1Cells(seq);const ro=el('p','p1ro');const B=p1Builder(seq,name,v=>{const ix=p1Sl(n,v[0],v[1],v[2]);C.show(ix);
    ro.innerHTML='<code>'+escH(name+'['+p1Ex(v[0],v[1],v[2])+']')+'</code> → <code>'+escH(p1Rl(seq,ix))+'</code>'+(ix.length?'':' (vacío: con ese paso nunca llega)')});
  const pr=el('div','p1pres');(o.presets||[[1,3,null],[null,null,2],[1,null,2],[null,null,-1],[-3,null,null],[null,-1,null]]).forEach(p=>{const x=el('button','p1chip',escH('['+p1Ex(p[0],p[1],p[2])+']'));x.type='button';x.onclick=()=>B.set(p);pr.append(x)});
  w.append(B.el,C.el,ro,el('p','note','Arriba de cada casilla está su índice positivo y abajo el negativo. El número rojo indica en qué orden la toma el corte.'),pr);b.append(w);B.set([null,null,null])};
/* ---------- Matrices: tocar celdas ---------- */
function p1Grid(m,onTap,name){const t=el('table','p1mt');const nr=m.length,nc=m[0].length;const hd=el('tr');hd.append(el('th','p1mn',escH(name||'')));for(let c=0;c<nc;c++)hd.append(el('th',null,'['+c+']'));t.append(hd);
  const cells=[];for(let f=0;f<nr;f++){const tr=el('tr');tr.append(el('th',null,'['+f+']'));const row=[];for(let c=0;c<nc;c++){const td=el('td');const b=el(onTap?'button':'span','p1mc');if(onTap)b.type='button';b.innerHTML='<b>'+escH(String(m[f][c]))+'</b><u></u>';if(onTap)b.onclick=()=>onTap(f,c);td.append(b);tr.append(td);row.push(b)}t.append(tr);cells.push(row)}
  const sc=el('div','p1msc');sc.append(t);return{el:sc,cells,show(seq,num){cells.flat().forEach(b=>{b.classList.remove('on','cur');b.querySelector('u').textContent=''});seq.forEach(([f,c],k)=>{const b=cells[f][c];b.classList.add('on');if(num)b.querySelector('u').textContent=String(k+1)})}}}
IW.mtx=(ch,o)=>{const w=el('div','p1mw');const A=ch.a.map(x=>x[0]+','+x[1]);const sel=[];let lk=false;
  const G=p1Grid(ch.m,(f,c)=>{if(lk)return;const k=sel.findIndex(x=>x[0]===f&&x[1]===c);if(k>=0)sel.splice(ch.ord?k:k,ch.ord?sel.length-k:1);else sel.push([f,c]);G.show(sel,ch.ord);o.on&&o.on()},ch.name||'mat');w.append(G.el);
  if(ch.ord)w.append(el('p','note','Tócalas en el orden en que las visita el código. Tocar una celda ya marcada borra desde ahí.'));
  const keys=()=>sel.map(x=>x[0]+','+x[1]);
  return{el:w,need:'Toca al menos una celda.',okMsg:'¡Celdas correctas!',filled:()=>sel.length>0,
    grade(){const k=keys();if(ch.ord){let i=0;while(i<k.length&&i<A.length&&k[i]===A[i])i++;return i===A.length&&k.length===A.length?{f:1}:{f:0,bad:i,msg:i<k.length?'La celda número '+(i+1)+' no va ahí.':'Faltan celdas: el recorrido sigue.'}}
      const S=new Set(k);const tp=A.filter(x=>S.has(x)).length,fp=k.length-tp,fn=A.length-tp;return{f:Math.max(0,(tp-fp)/A.length),msg:fp||fn?[fn?'Te faltan '+fn+' celda(s).':'',fp?'Sobran '+fp+' (en rojo).':''].filter(Boolean).join(' '):''}},
    mark(g){const S=new Set(A);sel.forEach(([f,c],i)=>{const b=G.cells[f][c];const ok=ch.ord?(g.f>=1||i<(g.bad==null?0:g.bad)):S.has(f+','+c);b.classList.toggle('good',ok);b.classList.toggle('bad',!ok)})},
    reveal(){sel.length=0;ch.a.forEach(x=>sel.push([x[0],x[1]]));G.show(sel,ch.ord);sel.forEach(([f,c])=>{G.cells[f][c].classList.remove('bad');G.cells[f][c].classList.add('good')})},
    lock(){lk=true;G.cells.flat().forEach(b=>b.disabled=true)},reset(){sel.length=0;G.show(sel,ch.ord);G.cells.flat().forEach(b=>b.classList.remove('good','bad'));o.on&&o.on()}}};
const P1MODES={
  fila:{n:'Una fila (fila fija)',k:'f',code:k=>'suma = 0\nfor c in range(len(mat[0])):\n    suma = suma + mat['+k+'][c]',seq:(m,k)=>m[0].map((_,c)=>[k,c]),acc:'suma'},
  col:{n:'Una columna (columna fija)',k:'c',code:k=>'suma = 0\nfor f in range(len(mat)):\n    suma = suma + mat[f]['+k+']',seq:(m,k)=>m.map((_,f)=>[f,k]),acc:'suma'},
  filas:{n:'Toda la matriz, fila por fila',code:()=>'suma = 0\nfor f in range(len(mat)):\n    for c in range(len(mat[0])):\n        suma = suma + mat[f][c]',seq:m=>m.flatMap((r,f)=>r.map((_,c)=>[f,c])),acc:'suma'},
  cols:{n:'Toda la matriz, columna por columna',code:()=>'suma = 0\nfor c in range(len(mat[0])):\n    for f in range(len(mat)):\n        suma = suma + mat[f][c]',seq:m=>m[0].flatMap((_,c)=>m.map((r,f)=>[f,c])),acc:'suma'},
  serp:{n:'Serpiente',code:()=>'lista = []\nfor f in range(len(mat)):\n    if f % 2 == 0:\n        cols = range(0, len(mat[0]), 1)\n    else:\n        cols = range(len(mat[0]) - 1, -1, -1)\n    for c in cols:\n        lista.append(mat[f][c])',seq:m=>m.flatMap((r,f)=>{const s=r.map((_,c)=>[f,c]);return f%2?s.reverse():s}),acc:'lista'},
  borde:{n:'Solo el borde',code:()=>'filas, col = len(mat), len(mat[0])\nsuma = 0\nfor f in range(filas):\n    for c in range(col):\n        if f == 0 or f == filas-1 or c == 0 or c == col-1:\n            suma = suma + mat[f][c]',seq:m=>m.flatMap((r,f)=>r.map((_,c)=>[f,c])).filter(([f,c])=>f===0||f===m.length-1||c===0||c===m[0].length-1),acc:'suma'},
  diag:{n:'Diagonal principal',code:()=>'suma = 0\nfor i in range(min(len(mat), len(mat[0]))):\n    suma = suma + mat[i][i]',seq:m=>[...Array(Math.min(m.length,m[0].length)).keys()].map(i=>[i,i]),acc:'suma'},
  vec:{n:'Vecinos de una celda',k:'fc',code:k=>'F, C = '+k[0]+', '+k[1]+'\nvecinos = []\nfor f in range(F-1, F+2):\n    for c in range(C-1, C+2):\n        if 0 <= f < len(mat) and 0 <= c < len(mat[0]) and (f, c) != (F, C):\n            vecinos.append(mat[f][c])',seq:(m,k)=>{const r=[];for(let f=k[0]-1;f<=k[0]+1;f++)for(let c=k[1]-1;c<=k[1]+1;c++)if(f>=0&&f<m.length&&c>=0&&c<m[0].length&&!(f===k[0]&&c===k[1]))r.push([f,c]);return r},acc:'lista'}};
LW.mtx=(b,o)=>{const m=o.m||[[18,17,20,16,17],[5,10,20,19,17],[12,14,15,19,9],[18,20,12,11,10]];const modes=o.modes||Object.keys(P1MODES);const w=el('div','p1mtw');
  let mode=modes[0],k=1,kc=[1,1],seq=[],pos=0,timer=null;
  const top=el('div','p1slr');const ms=el('select');modes.forEach(x=>{const op=el('option',null,P1MODES[x].n);op.value=x;ms.append(op)});const ml=el('label','p1sel');ml.append(el('span',null,'Recorrido'),ms);top.append(ml);
  const ks=el('label','p1sel');const kss=el('select');ks.append(el('span',null,''),kss);top.append(ks);
  const G=p1Grid(m,(f,c)=>{if(P1MODES[mode].k==='fc'){kc=[f,c];setup()}},'mat');const cd=el('div');const ro=el('p','p1ro');
  const acts=el('div','p1acts');const bp=el('button','p1try','▶ Animar'),bs=el('button',null,'Paso ›'),br=el('button',null,'↺');[bp,bs,br].forEach(x=>{x.type='button';acts.append(x)});
  w.append(top,G.el,acts,ro,cd);b.append(w);
  const fillK=()=>{const P=P1MODES[mode];kss.innerHTML='';ks.hidden=!P.k||P.k==='fc';if(P.k==='f'){ks.firstChild.textContent='Fila';m.forEach((_,i)=>{const op=el('option',null,String(i));op.value=i;kss.append(op)})}
    if(P.k==='c'){ks.firstChild.textContent='Columna';m[0].forEach((_,i)=>{const op=el('option',null,String(i));op.value=i;kss.append(op)})}k=Math.min(1,P.k==='f'?m.length-1:m[0].length-1);kss.value=k};
  const stop=()=>{clearInterval(timer);timer=null;bp.textContent='▶ Animar'};
  const draw=()=>{const P=P1MODES[mode];const done=seq.slice(0,pos);G.show(done,true);G.cells.flat().forEach(x=>x.classList.remove('ctr'));if(P.k==='fc')G.cells[kc[0]][kc[1]].classList.add('ctr');
    if(pos>0){const [f,c]=seq[pos-1];G.cells[f][c].classList.add('cur')}
    const vals=done.map(([f,c])=>m[f][c]);const last=pos>0?seq[pos-1]:null;
    ro.innerHTML=(last?'<code>f = '+last[0]+', c = '+last[1]+'</code> · ':'')+(P.acc==='suma'?'<code>suma = '+vals.reduce((a,x)=>a+(+x||0),0)+'</code>':'<code>'+(mode==='vec'?'vecinos':'lista')+' = ['+vals.join(', ')+']</code>')+' · paso '+pos+' de '+seq.length+(P.k==='fc'?'<br><small>Toca otra celda para cambiar el centro.</small>':'')};
  const setup=()=>{stop();const P=P1MODES[mode];const key=P.k==='fc'?kc:k;seq=P.seq(m,key);pos=0;cd.innerHTML='';cd.append(preCode(P.code(key)));draw()};
  ms.onchange=()=>{mode=ms.value;fillK();setup()};kss.onchange=()=>{k=+kss.value;setup()};
  bs.onclick=()=>{stop();if(pos<seq.length){pos++;draw()}};br.onclick=()=>{pos=0;stop();draw()};
  bp.onclick=()=>{if(timer){stop();return}if(pos>=seq.length)pos=0;bp.textContent='⏸ Pausa';timer=setInterval(()=>{if(!w.isConnected||pos>=seq.length){stop();return}pos++;draw()},o.ms||550)};
  fillK();setup()};
/* ---------- Tabla de rastreo ---------- */
IW.traza=(ch,o)=>{const w=el('div','p1tz');if(ch.code)w.append(preCode(ch.code));const t=el('table','fillt p1tzt');t.innerHTML='<tr>'+ch.head.map(h=>'<th>'+h+'</th>').join('')+'</tr>';const ins=[];
  ch.rows.forEach(r=>{const tr=el('tr');r.forEach(c=>{const td=el('td');if(c!==null&&typeof c==='object'){const i=el('input','fin p1tin');i.placeholder='?';i.autocomplete='off';i.spellcheck=false;i.setAttribute('autocapitalize','off');
      const A=[].concat(c.a);i.style.width=(Math.max(4,String(A[0]).length+2))+'ch';i.oninput=()=>{i.classList.remove('bad','good','rev');o.on&&o.on()};td.append(i);ins.push({i,A})}else td.innerHTML='<code>'+escH(String(c))+'</code>';tr.append(td)});t.append(tr)});
  const sc=el('div','tbl');sc.append(t);w.append(sc);const ok=x=>x.A.some(a=>P1N(a)===P1N(x.i.value));
  return{el:w,note:'Escribe el valor de cada variable después de ejecutar esa vuelta (las listas con corchetes y los textos con comillas).',need:'Completa todas las celdas.',okMsg:'¡Rastreo correcto!',
    filled:()=>ins.every(x=>x.i.value.trim()!==''),
    grade(){const bad=ins.filter(x=>!ok(x)).length;return{f:(ins.length-bad)/ins.length,msg:bad?(bad===1?'Una celda no está bien (en rojo).':bad+' celdas no están bien (en rojo).')+(ch.e?'<br>'+ch.e:''):''}},
    mark(){ins.forEach(x=>{const k=ok(x);x.i.classList.toggle('good',k);x.i.classList.toggle('bad',!k)})},
    reveal(){ins.forEach(x=>{if(!ok(x)){x.i.value=x.A[0];x.i.classList.remove('bad');x.i.classList.add('rev')}else x.i.classList.add('good')})},
    lock(){ins.forEach(x=>x.i.disabled=true)}}};
/* ---------- Paso a paso: variables, objetos y salida ---------- */
LW.paso=(b,o)=>{const S=o.steps||[];if(!S.length){b.textContent='Sin pasos.';return}const L=o.code.split('\n');const w=el('div','p1ps');
  const tag={};let nl=0,nd=0,nt=0;S.forEach(s=>Object.keys(s.h||{}).forEach(id=>{if(tag[id])return;const t=s.h[id].t;const lt=t==='dict'?'D'+(++nd):t==='tuple'?'T'+(++nt):'L'+(++nl);tag[id]={t:lt,c:'p1c'+((nl+nd+nt-1)%6)}}));
  const chip=id=>{const g=tag[id]||{t:'?',c:''};return'<span class="p1ref '+g.c+'">'+g.t+'</span>'};
  const prim=v=>typeof v==='string'&&v[0]!=='@';
  const cw=el('div','p1pc');const lines=L.map((s,i)=>{const d=el('div','p1pl');d.innerHTML='<span class="p1no">'+(i+1)+'</span><code>'+(hlPy(s)||' ')+'</code>';cw.append(d);return d});
  const nav=el('div','p1acts');const B=['⏮','◀ Atrás','Siguiente ▶','⏭'].map(t=>{const x=el('button',t.includes('Sig')?'p1try':null,t);x.type='button';nav.append(x);return x});const cnt=el('span','pyst');nav.append(cnt);
  const panel=el('div','p1pp');const vb=el('div','p1pv'),hb=el('div','p1ph'),ob=el('div','p1po');panel.append(vb,hb,ob);
  w.append(cw,nav,panel,el('p','note','➜ marca la línea que se va a ejecutar. Las etiquetas de color (L1, D1…) son objetos: si dos variables muestran la misma etiqueta, son <b>el mismo</b> objeto.'));b.append(w);
  let k=0;
  const val=(v,h)=>{if(v==null)return'';if(!prim(v)){const id=v.slice(1),x=h[id];if(x&&(x.t==='list'||x.t==='tuple')&&x.v.every(prim))return chip(id)+' <code>'+escH(x.t==='tuple'?'('+x.v.join(', ')+(x.v.length===1?',':'')+')':'['+x.v.join(', ')+']')+'</code>';return chip(id)}return'<code>'+escH(v)+'</code>'};
  const inl=(v,h)=>{if(prim(v))return false;const x=h[v.slice(1)];return x&&(x.t==='list'||x.t==='tuple')&&x.v.every(prim)};
  const objHTML=(id,h)=>{const x=h[id];const hd='<div class="p1oh">'+chip(id)+' <small>'+(x.t==='dict'?'diccionario':x.t==='tuple'?'tupla':'lista')+' · '+x.v.length+(x.t==='dict'?' pares':' elementos')+'</small></div>';
    if(x.t==='dict')return hd+'<table class="p1dt"><tr><th>clave</th><th>valor</th></tr>'+x.v.map(([kk,vv])=>'<tr><td><code>'+escH(kk)+'</code></td><td>'+val(vv,h)+'</td></tr>').join('')+'</table>';
    const rows=x.v.length&&x.v.every(v=>!prim(v)&&h[v.slice(1)]&&h[v.slice(1)].t==='list'&&h[v.slice(1)].v.every(prim));
    if(rows){const nc=Math.max(...x.v.map(v=>h[v.slice(1)].v.length));return hd+'<div class="p1msc"><table class="p1mt p1ma"><tr><th></th>'+[...Array(nc).keys()].map(c=>'<th>['+c+']</th>').join('')+'</tr>'+x.v.map((v,f)=>'<tr><th>['+f+'] '+chip(v.slice(1))+'</th>'+h[v.slice(1)].v.map(c=>'<td><span class="p1mc"><b>'+escH(c)+'</b></span></td>').join('')+'</tr>').join('')+'</table></div>'}
    return hd+'<div class="p1cells"><div class="p1crow">'+x.v.map((v,i)=>'<div class="p1cell"><i>'+i+'</i><b>'+(prim(v)?escH(v):chip(v.slice(1)))+'</b></div>').join('')+'</div></div>'};
  const draw=()=>{const s=S[k];lines.forEach((d,i)=>{d.classList.toggle('cur',s.l===i+1);d.classList.toggle('prev',k>0&&S[k-1].l===i+1&&s.l!==i+1)});
    const cl=lines[s.l-1];if(cl){const top=cl.offsetTop-cw.offsetTop;if(top<cw.scrollTop||top>cw.scrollTop+cw.clientHeight-24)cw.scrollTop=Math.max(0,top-40)}
    cnt.textContent='Paso '+(k+1)+' de '+S.length+(s.end?' · terminó':'');const h=s.h||{};
    vb.innerHTML='<h5>Variables</h5>'+(s.f||[]).map(([fn,vs])=>'<div class="p1fr"><div class="p1fn">'+escH(fn)+'</div>'+(vs.length?'<table class="p1vt">'+vs.map(([n,v])=>'<tr><th>'+escH(n)+'</th><td>'+val(v,h)+'</td></tr>').join('')+'</table>':'<small>(sin variables aún)</small>')+'</div>').join('');
    const seen=new Set(),q=[];(s.f||[]).forEach(([,vs])=>vs.forEach(([,v])=>{if(!prim(v)&&!inl(v,h))q.push(v.slice(1))}));const order=[];
    while(q.length){const id=q.shift();if(seen.has(id)||!h[id])continue;seen.add(id);order.push(id);const x=h[id];const kids=x.t==='dict'?x.v.map(p=>p[1]):x.v;const rows=x.t!=='dict'&&x.v.length&&x.v.every(v=>inl(v,h));kids.forEach(v=>{if(!prim(v)&&!(rows||inl(v,h)))q.push(v.slice(1))})}
    hb.innerHTML=order.length?'<h5>Objetos</h5>'+order.map(id=>'<div class="p1ob">'+objHTML(id,h)+'</div>').join(''):'';
    ob.innerHTML='<h5>Salida</h5><pre class="cons">'+escH(s.o||'')+'</pre>';
    B[0].disabled=B[1].disabled=k===0;B[2].disabled=B[3].disabled=k===S.length-1};
  B[0].onclick=()=>{k=0;draw()};B[1].onclick=()=>{if(k>0){k--;draw()}};B[2].onclick=()=>{if(k<S.length-1){k++;draw()}};B[3].onclick=()=>{k=S.length-1;draw()};draw()};
/* ---------- Laboratorio de imágenes (NumPy en el navegador) ---------- */
const P1IMGF={'matplotlib/__init__.py':'','matplotlib/pyplot.py':'import builtins\ndef imshow(a, *x, **k):\n    builtins._P1IMG = a\ndef show(*a, **k):\n    pass\ndef title(*a, **k):\n    pass\ndef axis(*a, **k):\n    pass\ndef figure(*a, **k):\n    pass\n',
  'PIL/__init__.py':'','PIL/Image.py':'from _p1fotos import foto\ndef open(nombre):\n    return foto(nombre)\n','imageio.py':'from _p1fotos import foto\ndef imread(nombre):\n    return foto(nombre)\n',
  '_p1fotos.py':'import numpy as np\n_C = {}\ndef _paisaje():\n    H, W = 720, 960\n    y = np.arange(H).reshape(H, 1, 1)\n    x = np.arange(W).reshape(1, W, 1)\n    cielo = np.array([70, 140, 220]) + (np.array([185, 215, 245]) - np.array([70, 140, 220])) * (y / 420)\n    img = np.broadcast_to(cielo, (H, W, 3)).copy()\n    sol = (x - 760) ** 2 + (y - 120) ** 2 < 55 ** 2\n    img[sol[:, :, 0]] = [255, 225, 120]\n    xs = np.arange(W)\n    m1 = 330 + 120 * np.abs(np.sin(xs / 150.0)) - 160 * np.exp(-((xs - 300) / 110.0) ** 2)\n    m2 = 470 - 210 * np.exp(-((xs - 640) / 95.0) ** 2) + 18 * np.sin(xs / 23.0)\n    Y = np.arange(H).reshape(H, 1)\n    img[Y > m1] = [96, 112, 104]\n    img[Y > m2] = [58, 92, 60]\n    for k in range(5):\n        t = 560 + 32 * k\n        img[t:t + 26, :, :] = [70 + 12 * k, 128 + 10 * k, 64]\n        img[t + 26:t + 32, :, :] = [150, 140, 120]\n    for c0 in range(80, 900, 140):\n        img[600:690, c0:c0 + 70] = [168, 160, 146]\n        img[600:612, c0:c0 + 70] = [120, 92, 70]\n    return img.astype(np.uint8)\ndef _mascota():\n    H = W = 240\n    y, x = np.mgrid[0:H, 0:W]\n    img = np.zeros((H, W, 3), dtype=np.uint8)\n    img[:, :] = [176, 196, 170]\n    cab = (x - 120) ** 2 + ((y - 110) * 1.15) ** 2 < 70 ** 2\n    img[cab] = [244, 170, 140]\n    for c in range(55, 200, 29):\n        pata = (abs(x - c) < 9) & (y > 150) & (y < 222)\n        img[pata] = [236, 150, 120]\n    for cx in (95, 145):\n        ojo = (x - cx) ** 2 + (y - 100) ** 2 < 14 ** 2\n        img[ojo] = [255, 255, 255]\n        pu = (x - cx - 3) ** 2 + (y - 102) ** 2 < 6 ** 2\n        img[pu] = [40, 30, 40]\n    img[40:52, 80:160] = [110, 30, 50]\n    img[28:42, 100:140] = [110, 30, 50]\n    return img\ndef foto(nombre=""):\n    k = "m" if any(s in str(nombre).lower() for s in ("gato", "pika", "masc", "pulp", ".png")) else "p"\n    if k not in _C:\n        _C[k] = _paisaje() if k == "p" else _mascota()\n    return _C[k].copy()\n'};
const P1IMGT="import builtins as _bi, base64 as _b6\nimport numpy as _np\n_a = getattr(_bi, '_P1IMG', None)\n_bi._P1IMG = None\nif _a is None:\n    _g = globals()\n    for _n in ('matrix', 'img', 'imagen', 'new_img', 'matriz'):\n        if _n in _g:\n            _a = _g[_n]\n            break\nif _a is None:\n    print('@@NOIMG@@')\nelse:\n    _a = _np.asarray(_a)\n    _sh = ','.join(map(str, _a.shape))\n    if _a.dtype != _np.uint8:\n        _a = _np.clip(_a, 0, 255).astype(_np.uint8)\n    _k = max(1, -(-max(_a.shape[0], _a.shape[1] if _a.ndim > 1 else 1) // 480))\n    _a = _a[::_k, ::_k] if _a.ndim > 1 else _a\n    print('@@IMG@@' + _sh + '@@' + ','.join(map(str, _a.shape)) + '@@' + _b6.b64encode(_np.ascontiguousarray(_a).tobytes()).decode())\n";
async function p1Img(code){const m=await pyRun(code,[{run:P1IMGT}],P1IMGF,90000);if(m.fail)return{err:PYFAIL};if(m.timeout)return{err:PYTO};const r=(m.res||[])[0]||{};
  const out=r.out||'';const k=out.indexOf('@@IMG@@');const txt=(k>=0?out.slice(0,k):out.replace('@@NOIMG@@','')).replace(/\n$/,'');
  if(r.err)return{err:r.err,txt};if(k<0)return{txt,err:'No encontré la imagen: usa plt.imshow(...) o guarda la matriz en una variable llamada matrix.'};
  const [sh0,sh,b64]=out.slice(k+7).trim().split('@@');const shape=sh.split(',').map(Number),real=sh0.split(',').map(Number);const bin=atob(b64);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return{shape,real,data:u,txt}}
function p1Paint(cv,im){const [H,W,Ch]=[im.shape[0],im.shape[1]||1,im.shape[2]||1];cv.width=W;cv.height=H;const g=cv.getContext('2d');const d=g.createImageData(W,H);
  for(let i=0;i<H*W;i++){if(Ch>=3){d.data[4*i]=im.data[Ch*i];d.data[4*i+1]=im.data[Ch*i+1];d.data[4*i+2]=im.data[Ch*i+2]}else{const v=im.data[i];d.data[4*i]=d.data[4*i+1]=d.data[4*i+2]=v}d.data[4*i+3]=255}g.putImageData(d,0,0)}
LW.img=(b,o)=>{const w=el('div','p1img');const start=o.code||'import numpy as np\nimport matplotlib.pyplot as plt\n\nmatrix = np.zeros([100, 100, 3], dtype=np.uint8)\nplt.imshow(matrix)\nplt.show()';
  const ta=el('textarea','ced');ta.spellcheck=false;ta.setAttribute('wrap','off');['autocapitalize','autocomplete','autocorrect'].forEach(a=>ta.setAttribute(a,'off'));ta.value=start;const fit=()=>{ta.rows=Math.min(22,Math.max(6,ta.value.split('\n').length+1))};fit();ta.oninput=fit;edKeys(ta,'py');
  const acts=el('div','p1acts');const bd=el('button','p1try','▶ Dibujar'),bz=el('button',null,'↺ Reiniciar');[bd,bz].forEach(x=>{x.type='button';acts.append(x)});const stt=el('span','pyst');acts.append(stt);
  const pics=el('div','p1pics');const mine=el('figure','p1fig');const cv=el('canvas','p1cv');mine.append(cv,el('figcaption',null,'Tu imagen'));mine.hidden=true;pics.append(mine);
  let tgt=null;const tf=el('figure','p1fig');const tcv=el('canvas','p1cv');tf.append(tcv,el('figcaption',null,'Objetivo'));if(o.target){pics.prepend(tf);tf.hidden=true}
  const msg=el('div','cout');msg.hidden=true;w.append(ta,acts,pics,msg);b.append(w);
  ta.addEventListener('runkey',()=>bd.click());bz.onclick=()=>{ta.value=start;fit()};
  const loadT=async()=>{if(!o.target||tgt)return;const r=await p1Img(o.target);if(r.shape){tgt=r;p1Paint(tcv,r);tf.hidden=false}};
  if(o.target){tf.hidden=false;tcv.width=tcv.height=1;const lt=el('button','p1chip','Ver la imagen objetivo');lt.type='button';tf.querySelector('figcaption').append(' ',lt);lt.onclick=async()=>{lt.disabled=true;stt.textContent='⏳ Cargando Python y NumPy (la primera vez tarda)…';await loadT();stt.textContent='';lt.remove()}}
  bd.onclick=async()=>{bd.disabled=true;stt.textContent='⏳ Ejecutando (la primera vez carga NumPy)…';const r=await p1Img(ta.value);await loadT();bd.disabled=false;stt.textContent='';msg.innerHTML='';msg.hidden=false;
    if(r.txt)msg.append(kvBox('Lo que imprimió tu código',r.txt));
    if(r.err){msg.append(el('p','cerr','💥 '+escH(r.err)));return}
    mine.hidden=false;p1Paint(cv,r);msg.append(el('p','note','Forma de la matriz (shape): <code>('+r.real.join(', ')+')</code>'+(r.real.join()!==r.shape.join()?' · se muestra reducida':'')));
    if(tgt){const same=tgt.real.join()===r.real.join()&&tgt.shape.join()===r.shape.join()&&tgt.data.length===r.data.length&&tgt.data.every((v,i)=>v===r.data[i]);msg.append(el('p','fb '+(same?'good':'bad'),same?'✓ ¡Igual a la imagen objetivo!':'Todavía no es igual al objetivo'+(tgt.real.join()!==r.real.join()?' (tamaño distinto: el objetivo es ('+tgt.real.join(', ')+')).':'.')))}}};
