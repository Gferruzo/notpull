/* ================= SEMANA 11 (2026-2): relaciones, Heaviside, Riemann y funciones virtuales =================
   IW.rel   «completa la relación»: {"t":"rel","A":[1,2,3],"give":[[1,2],…] (pares dados, fijos),"want":"eq"|"ord"|["ref","sim","tra","anti"],
            "a":[[x,y],…] (pares que hay que agregar: la clausura mínima),"e"}. Matriz A×A para tocar pares + digrafo en vivo.
            Nota 1 si agrega exactamente los pares mínimos; 0,5 si cumple las propiedades pero sobran pares.
   IW.heav  Heaviside (tapar el factor): {"t":"heav","num":[coef. del numerador, de mayor a menor grado],"r":[raíces distintas del denominador],
            "lab":["A","B",…],"k":coef. principal del denominador (opcional, 1)}. Se toca cada factor, se tapa y se escribe el coeficiente (acepta a/b).
            Herramienta {"w":"heav","o":{num,r,k}}: tocar un factor muestra la cuenta completa.
   LW.riem  sumas de Riemann: {"w":"riem","o":{"f":"x^2","a":0,"b":2,"n":4,"m":"L"|"R"|"M","xr":[…],"yr":[…],"ex":valor exacto (opcional),"exl":TeX}}.
   IW.virt / LW.virt  ¿qué método se llama? Base* p = new Derivada; con interruptores: virtual en el método, = 0, virtual en el destructor,
            tipo del puntero y del objeto. {"B":"Animal","D":"Perro","m":"hablar","bo":"...","do":"Guau","ini":{vm,pure,vd,ptr:'B'|'D',obj:'B'|'D'},
            "lock":["ptr","obj"],"want":{"out":"Guau","leak":false},"sol":{…}} (pregunta: dejar el programa con la salida pedida). */
const s11Frac=(p,q)=>{if(q<0){p=-p;q=-q}const g=(a,b)=>b?g(b,a%b):Math.abs(a);const d=g(p,q)||1;return[p/d,q/d]};
const s11FS=([p,q])=>q===1?String(p):p+'/'+q;
const s11FT=([p,q])=>q===1?String(p):(p<0?'-':'')+'\\frac{'+Math.abs(p)+'}{'+q+'}';
const s11Num=s=>{s=String(s).trim().replace(/[−–]/g,'-').replace(/\s/g,'');const m=s.match(/^(-?\d+(?:[.,]\d+)?)\/(-?\d+(?:[.,]\d+)?)$/);if(m){const b=+m[2].replace(',','.');return b?+m[1].replace(',','.')/b:NaN}if(!/^-?(\d+([.,]\d*)?|[.,]\d+)$/.test(s))return NaN;return +s.replace(',','.')};
/* ---------- relaciones: propiedades ---------- */
const relKey=(x,y)=>x+'|'+y;
function relProps(A,S){const has=(x,y)=>S.has(relKey(x,y));const W={};
  const r=A.find(x=>!has(x,x));W.ref=r===undefined?null:'falta \\(('+r+','+r+')\\)';
  W.sim=null;W.anti=null;W.tra=null;
  outer:for(const x of A)for(const y of A){if(has(x,y)&&!has(y,x)){W.sim='está \\(('+x+','+y+')\\) pero falta \\(('+y+','+x+')\\)';break outer}}
  outer2:for(const x of A)for(const y of A){if(x!==y&&has(x,y)&&has(y,x)){W.anti='están \\(('+x+','+y+')\\) y \\(('+y+','+x+')\\) con \\('+x+'\\ne'+y+'\\)';break outer2}}
  outer3:for(const x of A)for(const y of A)if(has(x,y))for(const z of A)if(has(y,z)&&!has(x,z)){W.tra='están \\(('+x+','+y+')\\) y \\(('+y+','+z+')\\) pero falta \\(('+x+','+z+')\\)';break outer3}
  return W}
const REL_N={ref:'reflexiva',sim:'simétrica',anti:'antisimétrica',tra:'transitiva'};
function relDigraph(A,S){const n=A.length,R=n<=3?52:n<=5?62:72,W=200,H=170,cx=W/2,cy=H/2+4;const P={};
  A.forEach((x,i)=>{const t=-Math.PI/2+2*Math.PI*i/n;P[x]=[cx+R*Math.cos(t),cy+R*Math.sin(t)]});
  let s='<svg class="reldg" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg"><defs><marker id="relar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="relah"/></marker></defs>';
  A.forEach(x=>A.forEach(y=>{if(!S.has(relKey(x,y)))return;const [x1,y1]=P[x],[x2,y2]=P[y];
    if(x===y){const dx=x1-cx,dy=y1-cy,L=Math.hypot(dx,dy)||1,ux=dx/L,uy=dy/L;const bx=x1+ux*13,by=y1+uy*13;
      s+='<circle class="rele" cx="'+(bx+ux*9).toFixed(1)+'" cy="'+(by+uy*9).toFixed(1)+'" r="9"/>';return}
    const both=S.has(relKey(y,x));const dx=x2-x1,dy=y2-y1,L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L;const off=both?5:0;const nx=-uy*off,ny=ux*off;
    s+='<line class="rele" x1="'+(x1+ux*13+nx).toFixed(1)+'" y1="'+(y1+uy*13+ny).toFixed(1)+'" x2="'+(x2-ux*14+nx).toFixed(1)+'" y2="'+(y2-uy*14+ny).toFixed(1)+'" marker-end="url(#relar)"/>'}));
  A.forEach(x=>{const [px,py]=P[x];s+='<circle class="reln" cx="'+px.toFixed(1)+'" cy="'+py.toFixed(1)+'" r="12"/><text class="relt" x="'+px.toFixed(1)+'" y="'+(py+4.5).toFixed(1)+'" text-anchor="middle">'+x+'</text>'});
  return s+'</svg>'}
IW.rel=(ch,o)=>{const A=ch.A;const give=new Set((ch.give||[]).map(p=>relKey(p[0],p[1])));const ans=new Set((ch.a||[]).map(p=>relKey(p[0],p[1])));
  const want=ch.want==='eq'?['ref','sim','tra']:ch.want==='ord'?['ref','anti','tra']:ch.want;let lk=false;const sel=new Set();
  const w=el('div','relw');const t=el('table','relt');const dg=el('div','reldgw');w.append(el('p','relh','Filas: 1.ª componente · columnas: 2.ª'),t,dg);
  t.innerHTML='<tr><th>R</th>'+A.map(y=>'<th>'+y+'</th>').join('')+'</tr>';const B={};
  A.forEach(x=>{const tr=el('tr');tr.append(el('th',null,String(x)));A.forEach(y=>{const td=el('td');const k=relKey(x,y);const b=el('button','relc'+(give.has(k)?' giv':''),give.has(k)?'●':'');b.type='button';
      b.setAttribute('aria-label','Par ('+x+', '+y+')');if(give.has(k))b.disabled=true;else b.onclick=()=>{if(lk)return;sel.has(k)?sel.delete(k):sel.add(k);paint();o.on&&o.on()};B[k]=b;td.append(b);tr.append(td)});t.append(tr)});
  const cur=()=>new Set([...give,...sel]);
  const paint=()=>{for(const k in B){if(give.has(k))continue;B[k].textContent=sel.has(k)?'●':'';B[k].classList.toggle('on',sel.has(k));B[k].classList.remove('good','bad','rev')}dg.innerHTML=relDigraph(A,cur())};paint();
  const nm=want.map(k=>REL_N[k]).join(', ');
  return{el:w,note:'Toca las casillas para agregar o quitar pares (los ● grises ya vienen dados). Agrega solo los pares indispensables para que la relación sea '+nm+'.',
   need:'Agrega al menos un par.',okMsg:'¡Exacto! Esos son los pares mínimos.',filled:()=>sel.size>0||ans.size===0,
   grade(){const S=cur();const W=relProps(A,S);const fails=want.filter(k=>W[k]);
    if(fails.length)return{f:0,msg:'Todavía no es '+fails.map(k=>REL_N[k]).join(' ni ')+': '+fails.map(k=>W[k]).join('; ')+'.'+(ch.e?'<br>'+ch.e:'')};
    const extra=[...sel].filter(k=>!ans.has(k));if(extra.length)return{f:0.5,msg:'Cumple, pero sobran pares: '+extra.map(k=>'\\(('+k.replace('|',',')+')\\)').join(', ')+'. Se pide la relación más pequeña que contenga a los dados.'};
    return{f:1,msg:''}},
   mark(){for(const k in B){if(give.has(k))continue;B[k].classList.toggle('good',sel.has(k)&&ans.has(k));B[k].classList.toggle('bad',sel.has(k)!==ans.has(k)&&sel.has(k))}},
   reveal(){for(const k in B){if(give.has(k))continue;const was=sel.has(k);if(ans.has(k))sel.add(k);else sel.delete(k)}paint();for(const k in B){if(give.has(k))continue;if(ans.has(k))B[k].classList.add('rev')}},
   lock(){lk=true;for(const k in B)B[k].disabled=true},reset(){sel.clear();paint();o.on&&o.on()}}};
/* ---------- Heaviside: tapar el factor ---------- */
function heavPolyT(c){const n=c.length-1;let s='';c.forEach((a,i)=>{if(!a)return;const p=n-i;const ab=Math.abs(a);const co=(ab===1&&p>0)?'':String(ab);const v=p===0?'':p===1?'x':'x^{'+p+'}';s+=(a<0?(s?'-':'-'):(s?'+':''))+co+v});return s||'0'}
const heavFacT=r=>r===0?'x':'x'+(r>0?'-':'+')+Math.abs(r);
function heavCoef(num,r,i,k){const ev=x=>num.reduce((a,c)=>a*x+c,0);let q=k||1;r.forEach((s,j)=>{if(j!==i)q*=(r[i]-s)});return s11Frac(ev(r[i]),q)}
function heavUI(ch,ask,on){const r=ch.r,lab=ch.lab||'ABCDEF'.split('').slice(0,r.length),k=ch.k||1;const w=el('div','hvw');let lk=false;
  const den=(k!==1?k:'')+r.map(s=>'('+heavFacT(s)+')').join('');
  w.append(el('div','hvint','\\(\\dfrac{'+heavPolyT(ch.num)+'}{'+den+'}=\\)'+r.map((s,i)=>'\\(\\dfrac{'+lab[i]+'}{'+heavFacT(s)+'}\\)').join(' + ')));
  w.append(el('p','note',ask?'Toca un factor para taparlo; evalúa lo que queda en su raíz y escribe el coeficiente (puedes escribir fracciones como -1/3).':'Toca un factor: se tapa y lo demás se evalúa en su raíz.'));
  const row=el('div','hvfac');const lines=el('div','hvlines');w.append(row,lines);const cov=new Set();const ins={};const L={};
  r.forEach((s,i)=>{const b=el('button','hvb','\\(('+heavFacT(s)+')\\)');b.type='button';b.onclick=()=>{if(lk)return;cover(i);on&&on()};row.append(b);L[i]={b}});
  function cover(i){if(cov.has(i)){return}cov.add(i);L[i].b.classList.add('on');const s=r[i];
    const rest=r.map((t,j)=>j===i?'':'('+s+(t<0?'+'+(-t):'-'+t)+')').join('');const kk=k!==1?k+'\\cdot':'';
    const ln=el('div','hvln');const C=heavCoef(ch.num,r,i,k);
    ln.innerHTML='<span>\\('+lab[i]+'\\): tapa \\(('+heavFacT(s)+')\\) y evalúa en \\(x='+s+'\\): \\(\\dfrac{'+heavPolyT(ch.num).replace(/x/g,'('+s+')')+'}{'+kk+(rest||'1')+'}\\)</span>';
    if(ask){const inp=el('input','fin');inp.placeholder='?';inp.autocomplete='off';inp.setAttribute('aria-label','Coeficiente '+lab[i]);inp.oninput=()=>{inp.classList.remove('good','bad');on&&on()};const g=el('span','hveq','= ');g.append(inp);ln.append(g);ins[i]=inp}
    else ln.append(el('b','hveq','\\(='+s11FT(C)+'\\)'));
    const pos=[...lines.children].findIndex(c=>+c.dataset.i>i);ln.dataset.i=i;pos<0?lines.append(ln):lines.insertBefore(ln,lines.children[pos]);(ln.isConnected?typeset:tsL)(ln)}
  tsL(w);return{el:w,cov,ins,cover,lab,lk(){lk=true}}}
LW.heav=(b,o)=>{b.append(heavUI(o,false).el)};
IW.heav=(ch,o)=>{const u=heavUI(ch,true,()=>o.on&&o.on());const n=ch.r.length;const C=ch.r.map((_,i)=>heavCoef(ch.num,ch.r,i,ch.k));
  const ok=i=>{const v=s11Num(u.ins[i]&&u.ins[i].value);const a=C[i][0]/C[i][1];return Math.abs(v-a)<=(C[i][1]===1?1e-9:0.006)};
  return{el:u.el,note:'',need:'Tapa cada factor y escribe todos los coeficientes.',okMsg:'¡Coeficientes correctos!',
   filled:()=>u.cov.size===n&&Object.values(u.ins).every(i=>i.value.trim()!==''),
   grade(){const bad=ch.r.map((_,i)=>i).filter(i=>!ok(i));return{f:(n-bad.length)/n,msg:bad.length?(bad.length===1?'Un coeficiente no está bien (en rojo).':bad.length+' coeficientes no están bien (en rojo).')+' Revisa la resta en cada factor que queda: \\((r_i-r_j)\\).'+(ch.e?'<br>'+ch.e:''):''}},
   mark(){for(const i in u.ins){const k=ok(+i);u.ins[i].classList.toggle('good',k);u.ins[i].classList.toggle('bad',!k)}},
   reveal(){ch.r.forEach((_,i)=>u.cover(i));for(const i in u.ins){if(!ok(+i)){u.ins[i].value=s11FS(C[i]);u.ins[i].classList.remove('bad');u.ins[i].classList.add('rev')}else u.ins[i].classList.add('good')}},
   lock(){u.lk();Object.values(u.ins).forEach(i=>i.disabled=true)}}};
/* ---------- sumas de Riemann ---------- */
LW.riem=(b,o)=>{const f=mxF(o.f);const a=o.a,bb=o.b;const [x0,x1]=o.xr||[a-(bb-a)*.1,bb+(bb-a)*.1];let ymin=0,ymax=0;for(let i=0;i<=200;i++){const v=f(a+(bb-a)*i/200);if(isFinite(v)){ymin=Math.min(ymin,v);ymax=Math.max(ymax,v)}}
  const [y0,y1]=o.yr||[Math.min(0,ymin)-(ymax-ymin)*.1,ymax+(ymax-ymin)*.12];let n=o.n||4,m=o.m||'L';const uid='rm'+Math.random().toString(36).slice(2,7);
  const ex=o.ex!=null?o.ex:(()=>{const N=800,h=(bb-a)/N;let s=f(a)+f(bb);for(let i=1;i<N;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3})();
  const w=el('div','rmw');const top=el('div','plctl');const fig=el('div','plfig');const ctl=el('div','plctl');const ro=el('div','acro');w.append(top,fig,ctl,ro);b.append(w);
  [['L','Izquierdo (Lₙ)'],['R','Derecho (Rₙ)'],['M','Punto medio (Mₙ)']].forEach(([k,l])=>{const bt=el('button','lwb'+(k===m?' on':''),l);bt.type='button';bt.onclick=()=>{m=k;top.querySelectorAll('.lwb').forEach(x=>x.classList.toggle('on',x===bt));draw()};top.append(bt)});
  const r=el('label','acsl');r.append(el('span','plrl','n ='));const i=el('input','plrg');i.type='range';i.min=1;i.max=o.nmax||60;i.step=1;i.value=n;i.setAttribute('aria-label','Número de rectángulos');const v=el('b',null,String(n));
  i.oninput=()=>{n=+i.value;v.textContent=n;draw()};r.append(i,v);ctl.append(r);
  const W=320,H=240,L=30,R=10,T=10,B=24,X=x=>L+(W-L-R)*(x-x0)/(x1-x0),Y=y=>T+(H-T-B)*(y1-y)/(y1-y0);
  const fmt=x=>fmtV(Math.round(x*10000)/10000);
  function draw(){const dx=(bb-a)/n;let S=0,rp='',rn='';const z=Y(Math.max(y0,Math.min(y1,0)));
    for(let k=0;k<n;k++){const xl=a+k*dx,xr=xl+dx,xs=m==='L'?xl:m==='R'?xr:(xl+xr)/2,h=f(xs);if(!isFinite(h))continue;S+=h*dx;const yy=Math.max(T,Math.min(H-B,Y(h)));
      const rect='<rect x="'+X(xl).toFixed(1)+'" y="'+Math.min(yy,z).toFixed(1)+'" width="'+Math.max(0.6,X(xr)-X(xl)).toFixed(1)+'" height="'+Math.abs(z-yy).toFixed(1)+'"/>';h>=0?rp+=rect:rn+=rect;
      if(n<=12)rp+='<circle class="rmpt" cx="'+X(xs).toFixed(1)+'" cy="'+yy.toFixed(1)+'" r="2.6"/>'}
    let svg=plotSVG({xr:[x0,x1],yr:[y0,y1],fs:[{f:o.f,cl:'f',l:o.fl||''}],id:uid});
    svg=svg.replace('<path class="plf','<g class="rmr">'+rp+'</g><g class="rmr neg">'+rn+'</g><path class="plf');fig.innerHTML=svg;
    const err=S-ex;const nm={L:'L',R:'R',M:'M'}[m];
    ro.innerHTML='<p>\\(\\Delta x=\\dfrac{'+fmtV(bb-a).replace(',','{,}')+'}{'+n+'}='+fmt(dx).replace(',','{,}')+'\\)</p><p>\\('+nm+'_{'+n+'}\\) = <b>'+fmt(S)+'</b> · integral exacta '+(o.exl?'\\('+o.exl+'\\) ':'')+'= <b>'+fmt(ex)+'</b></p><p>Error: '+fmt(err)+' → '+(Math.abs(err)<5e-5?'coinciden':err>0?'la suma <b>sobrestima</b>':'la suma <b>subestima</b>')+'</p>';
    (ro.isConnected?typeset:tsL)(ro);w.dataset.s=S}
  draw()};
/* ---------- funciones virtuales ---------- */
function virtRun(o,c){const B=o.B||'Animal',D=o.D||'Perro';const pure=!!c.pure,vm=!!c.vm||pure;
  if(c.obj==='B'&&pure)return{err:'error: no se puede crear un objeto de la clase abstracta '+B+' (tiene una función virtual pura).'};
  if(c.ptr==='D'&&c.obj==='B')return{err:'error: no se puede convertir '+B+'* a '+D+'* (un '+B+' no es necesariamente un '+D+').'};
  const out=[B+'()'];if(c.obj==='D')out.push(D+'()');
  const who=c.ptr==='D'?'D':(vm?c.obj:'B');out.push(who==='D'?(o.do||'Guau'):(o.bo||'...'));
  let leak=false;if(c.obj==='D'){if(c.ptr==='B'&&!c.vd){out.push('~'+B+'()');leak=true}else out.push('~'+D+'()','~'+B+'()')}else out.push('~'+B+'()');
  const dyn=c.ptr==='B'&&vm;return{out,leak,who,dyn,line:out[c.obj==='D'?2:1]}}
function virtUI(o,on){const B=o.B||'Animal',D=o.D||'Perro',m=o.m||'hablar';const c=Object.assign({vm:false,pure:false,vd:false,ptr:'B',obj:'D'},o.ini||{});const lock=new Set(o.lock||[]);let lk=false;
  const w=el('div','vtw');const ctl=el('div','vtctl');const code=el('pre','vtcode');const outp=el('div','vtout');w.append(ctl,code,outp);
  const tg=(k,l)=>{const b=el('button','lwb','');b.type='button';b.dataset.k=k;b.onclick=()=>{if(lk||lock.has(k))return;c[k]=!c[k];if(k==='pure'&&c.pure)c.vm=true;if(k==='vm'&&!c.vm)c.pure=false;draw();on&&on()};b.__l=l;ctl.append(b);return b};
  const sl=(k,l,opts)=>{const r=el('label','vtsel');r.append(el('span',null,l));const s=document.createElement('select');opts.forEach(([v,t])=>{const q=document.createElement('option');q.value=v;q.textContent=t;s.append(q)});s.value=c[k];s.disabled=lock.has(k);
    s.onchange=()=>{c[k]=s.value;draw();on&&on()};r.append(s);ctl.append(r);return s};
  const T={vm:tg('vm','virtual en '+m+'()'),pure:tg('pure','= 0 (virtual pura)'),vd:tg('vd','virtual en ~'+B+'()')};
  const S={ptr:sl('ptr','Puntero:',[['B',B+'*'],['D',D+'*']]),obj:sl('obj','Objeto:',[['B','new '+B],['D','new '+D]])};
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');const kw=(on,t)=>on?'<b class="vtk">'+t+'</b>':'';
  function draw(){for(const k in T){T[k].textContent=(c[k]?'✔ ':'')+T[k].__l;T[k].classList.toggle('on',!!c[k]);T[k].disabled=lk||lock.has(k)}
    for(const k in S){S[k].value=c[k];S[k].disabled=lk||lock.has(k)}
    const vm=c.vm||c.pure;
    code.innerHTML='class '+B+' {\npublic:\n  '+B+'() { cout &lt;&lt; "'+B+'()\\n"; }\n  '+kw(vm,'virtual ')+'void '+m+'() '+(c.pure?kw(1,'= 0;')+'\n':'{ cout &lt;&lt; "'+esc(o.bo||'...')+'\\n"; }\n')+'  '+kw(c.vd,'virtual ')+'~'+B+'() { cout &lt;&lt; "~'+B+'()\\n"; }\n};\n'+
      'class '+D+' : public '+B+' {\n  int* datos;\npublic:\n  '+D+'() { datos = new int[100]; cout &lt;&lt; "'+D+'()\\n"; }\n  void '+m+'()'+(vm?' override':'')+' { cout &lt;&lt; "'+esc(o.do||'Guau')+'\\n"; }\n  ~'+D+'() { delete[] datos; cout &lt;&lt; "~'+D+'()\\n"; }\n};\n'+
      'int main() {\n  <b class="vtm">'+(c.ptr==='B'?B:D)+'* p = new '+(c.obj==='B'?B:D)+';</b>\n  p-&gt;'+m+'();\n  delete p;\n}';
    const R=virtRun(o,c);
    if(R.err){outp.innerHTML='<p class="vterr">❌ No compila</p><p>'+esc(R.err)+'</p>';return}
    outp.innerHTML='<p class="vth">Salida</p><pre class="vtpre">'+R.out.map(esc).join('\n')+'</pre>'+
      '<p>'+(c.ptr==='D'?'El puntero es '+D+'*: se llama '+D+'::'+m+'() directamente.':R.dyn?'🔀 <b>Ligadura dinámica</b>: como '+m+'() es virtual, se mira el objeto real ('+(c.obj==='D'?D:B)+').':'📌 <b>Ligadura estática</b>: '+m+'() no es virtual, así que manda el tipo del puntero ('+B+'*).')+'</p>'+
      (R.leak?'<p class="vterr">⚠️ Fuga de memoria: ~'+B+'() no es virtual, así que delete p solo llama a ~'+B+'(). El destructor de '+D+' nunca corre y el arreglo datos no se libera.</p>':'<p class="vtok">✅ Sin fugas: se ejecutan todos los destructores necesarios.</p>')}
  draw();return{el:w,c,draw,set(x){Object.assign(c,x);draw()},lock(){lk=true;draw()}}}
LW.virt=(b,o)=>{b.append(virtUI(o).el)};
IW.virt=(ch,o)=>{let touched=false;const u=virtUI(ch,()=>{touched=true;o.on&&o.on()});const W=ch.want||{};
  const okR=()=>{const R=virtRun(ch,u.c);if(R.err)return{f:0,msg:'Así no compila. '+R.err};const bad=[];
    if(W.out!=null&&R.line!==W.out)bad.push('p->'+(ch.m||'hablar')+'() imprime «'+R.line+'» y se pide «'+W.out+'»');
    if(W.leak===false&&R.leak)bad.push('hay fuga de memoria');if(W.dyn!=null&&R.dyn!==W.dyn)bad.push(W.dyn?'la llamada debe resolverse por ligadura dinámica':'la llamada debe ser estática');
    if(W.abs&&!u.c.pure)bad.push('la clase base debe ser abstracta');
    return bad.length?{f:0,msg:'Todavía no: '+bad.join('; ')+'.'+(ch.e?'<br>'+ch.e:'')}:{f:1,msg:''}};
  return{el:u.el,note:'Usa los interruptores y mira la salida del programa.',need:'Cambia algo primero.',okMsg:'¡Así se comporta como se pide!',filled:()=>touched||!!ch.free,
   grade:okR,mark(){},reveal(){u.set(ch.sol||{})},lock(){u.lock()}}};
/* ---------- potencias: aplicar A una y otra vez (Álgebra Lineal, valores propios) ----------
   LW.pot {"w":"pot","o":{"a":[[5,-2],[1,2]],"x0":[2,1],"presets":[[etiqueta,{"a":…,"x0":…}],…]}}: ▶ calcula x_{k+1} = A x_k; dibuja la dirección de cada x_k
   (normalizada), las rectas propias reales (punteadas) y una tabla con los valores reales. Muestra si x_k sigue en la recta de x_0. */
function potEig(A){const a=A[0][0],b=A[0][1],c=A[1][0],d=A[1][1];if(Math.abs(b)<1e-12&&Math.abs(c)<1e-12)return a===d?[{l:a,v:[1,0]},{l:a,v:[0,1]}]:[{l:a,v:[1,0]},{l:d,v:[0,1]}];const tr=a+d,de=a*d-b*c,D=tr*tr-4*de;if(D<-1e-12)return[];
  const ls=D<1e-12?[tr/2]:[(tr+Math.sqrt(D))/2,(tr-Math.sqrt(D))/2];const out=[];
  ls.forEach(l=>{let v=Math.abs(b)>1e-12?[b,l-a]:Math.abs(c)>1e-12?[l-d,c]:null;if(!v){out.push({l,v:[1,0]},{l,v:[0,1]});return}out.push({l,v})});return out}
function potUI(o){const w=el('div','potw');const top=el('div','plctl');const fig=el('div','plfig');const ctl=el('div','plctl');const ro=el('div','acro');w.append(top,fig,ctl,ro);
  let A=o.a,x0=o.x0,xs=[x0];const fmtN=v=>Math.abs(v)>=1e5?v.toExponential(2):fmtV(Math.round(v*1000)/1000);
  const W=260,C=130,R=110,uid='pt'+Math.random().toString(36).slice(2,7);
  function draw(){const ev=potEig(A);let s='<svg class="potsvg" viewBox="0 0 '+W+' '+W+'" xmlns="http://www.w3.org/2000/svg"><defs><marker id="'+uid+'" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" class="potah"/></marker></defs>';
    s+='<line class="potax" x1="0" y1="'+C+'" x2="'+W+'" y2="'+C+'"/><line class="potax" x1="'+C+'" y1="0" x2="'+C+'" y2="'+W+'"/><circle class="potax" cx="'+C+'" cy="'+C+'" r="'+R+'" fill="none"/>';
    ev.forEach(e=>{const n=Math.hypot(...e.v);const ux=e.v[0]/n,uy=e.v[1]/n;s+='<line class="potei" x1="'+(C-ux*W)+'" y1="'+(C+uy*W)+'" x2="'+(C+ux*W)+'" y2="'+(C-uy*W)+'"/><text class="potl" x="'+(C+ux*(R+8)+4)+'" y="'+(C-uy*(R+8))+'">λ='+fmtN(e.l)+'</text>'});
    xs.forEach((x,k)=>{const n=Math.hypot(x[0],x[1])||1;const ux=x[0]/n,uy=x[1]/n;const last=k===xs.length-1;
      s+='<line class="potv'+(last?' last':'')+'" style="opacity:'+(last?1:Math.max(.18,.6-.1*(xs.length-1-k)))+'" x1="'+C+'" y1="'+C+'" x2="'+(C+ux*R)+'" y2="'+(C-uy*R)+'" marker-end="url(#'+uid+')"/>';
      if(last)s+='<text class="potl b" x="'+(C+ux*R*.6+6)+'" y="'+(C-uy*R*.6-6)+'">x'+(k?'<tspan baseline-shift="sub" font-size="9">'+k+'</tspan>':'<tspan baseline-shift="sub" font-size="9">0</tspan>')+'</text>'});
    fig.innerHTML=s+'</svg>';
    const x=xs[xs.length-1],cr=x0[0]*x[1]-x0[1]*x[0],same=Math.abs(cr)<1e-9*Math.max(1,Math.hypot(...x)*Math.hypot(...x0));
    ro.innerHTML='<div class="tbl"><table class="pott"><tr><th>k</th><th>x<sub>k</sub> = A<sup>k</sup>x<sub>0</sub></th></tr>'+xs.map((v,k)=>'<tr><td>'+k+'</td><td>('+fmtN(v[0])+', '+fmtN(v[1])+')</td></tr>').join('')+'</table></div>'+
      '<p>'+(xs.length<2?'Toca ▶ para aplicar A.':same?'✅ x<sub>'+(xs.length-1)+'</sub> sigue en la recta de x<sub>0</sub>: '+(ev.length?'x<sub>0</sub> es un vector propio y A solo lo escala.':'')+'':'↪️ x<sub>'+(xs.length-1)+'</sub> ya no está en la recta de x<sub>0</sub>'+(ev.length?': se va acercando a la recta del λ de mayor valor absoluto.':': sin valores propios reales, ninguna dirección se conserva.'))+'</p>';
    nx.disabled=xs.length>12}
  const nx=el('button','lwb on','▶ Aplicar A');nx.type='button';nx.onclick=()=>{const x=xs[xs.length-1];xs.push([A[0][0]*x[0]+A[0][1]*x[1],A[1][0]*x[0]+A[1][1]*x[1]]);draw()};
  const rs=el('button','lwb','⟲ Reiniciar');rs.type='button';rs.onclick=()=>{xs=[x0];draw()};ctl.append(nx,rs);
  (o.presets||[]).forEach(([l,p],i)=>{const b=el('button','lwb'+(i?'':' on'),l);b.type='button';b.onclick=()=>{top.querySelectorAll('.lwb').forEach(z=>z.classList.toggle('on',z===b));A=p.a;x0=p.x0;xs=[x0];draw()};top.append(b)});
  draw();return{el:w}}
LW.pot=(b,o)=>{b.append(potUI(o).el)};
/* ================= MICROECONOMÍA (sem. 10–13): matriz de pagos, beneficio máximo y juego del polizón =================
   IW.nash  matriz de pagos 2 jugadores. {"t":"nash","pn":["Fila","Columna"],"rows":[…],"cols":[…],"pay":[[[a,b],…],…],"step":"br"|"ne","e"}
            step "br": tocar los pagos que son mejor respuesta (subrayar); step "ne": tocar la(s) casilla(s) que son equilibrio de Nash.
            LW.nash {"w":"nash","o":{pn,rows,cols,pay,presets:[[etiqueta,{…}]]}}: con «mostrar mejores respuestas».
   IW.qmax  {"t":"qmax","mode":"pc"|"mon","P":precio (pc),"a","b" (demanda P = a − bQ),"F","c","d" (CT = F + cQ + dQ²),"qmax","ans":Q*,"tol","e"}:
            mover Q hasta el beneficio máximo. LW.qmax igual, con presets. Muestra IMg vs CMg, P, CMe, rectángulo de beneficio y tabla.
   LW.poliz juego del polizón: 5 rondas, S/ 10 por ronda, el parque se hace con S/ 30 y da S/ 15 a cada uno. {"w":"poliz","o":{}} */
function nashBR(pay){const R=pay.length,C=pay[0].length;const br=new Set();
  for(let j=0;j<C;j++){const m=Math.max(...pay.map(r=>r[j][0]));for(let i=0;i<R;i++)if(pay[i][j][0]===m)br.add(i+','+j+',0')}
  for(let i=0;i<R;i++){const m=Math.max(...pay[i].map(c=>c[1]));for(let j=0;j<C;j++)if(pay[i][j][1]===m)br.add(i+','+j+',1')}
  const ne=new Set();for(let i=0;i<R;i++)for(let j=0;j<C;j++)if(br.has(i+','+j+',0')&&br.has(i+','+j+',1'))ne.add(i+','+j);return{br,ne}}
function nashUI(o,mode,on){const pn=o.pn||['Jugador 1','Jugador 2'];const w=el('div','nsw');let lk=false;const sel=new Set();
  const t=el('table','nst');const B={},Cl={};
  t.innerHTML='<tr><th class="nsc">'+pn[0]+' ↓ · '+pn[1]+' →</th>'+o.cols.map(c=>'<th>'+c+'</th>').join('')+'</tr>';
  o.rows.forEach((r,i)=>{const tr=el('tr');tr.append(el('th',null,r));o.cols.forEach((c,j)=>{const td=el('td','nscell');Cl[i+','+j]=td;
      const [a,b]=o.pay[i][j];const pa=el('button','nsp p1',String(a)),pb=el('button','nsp p2',String(b));pa.type=pb.type='button';
      B[i+','+j+',0']=pa;B[i+','+j+',1']=pb;td.append('(',pa,', ',pb,')');
      if(mode==='br'){[[pa,0],[pb,1]].forEach(([bt,k])=>bt.onclick=()=>{if(lk)return;const key=i+','+j+','+k;sel.has(key)?sel.delete(key):sel.add(key);paint();on&&on()})}
      else{pa.disabled=pb.disabled=mode!=='ne';if(mode==='ne'){td.onclick=()=>{if(lk)return;const key=i+','+j;sel.has(key)?sel.delete(key):sel.add(key);paint();on&&on()};td.classList.add('nstap')}}
      tr.append(td)});t.append(tr)});
  const tb=el('div','tbl');tb.append(t);w.append(el('p','nsleg','<span class="p1">primer número: '+pn[0]+'</span> · <span class="p2">segundo: '+pn[1]+'</span>'),tb);
  function paint(show){for(const k in B)B[k].classList.toggle('on',mode==='br'&&sel.has(k));for(const k in Cl)Cl[k].classList.toggle('on',mode==='ne'&&sel.has(k));
    if(show){const S=nashBR(o.pay);for(const k in B)B[k].classList.toggle('br',S.br.has(k));for(const k in Cl)Cl[k].classList.toggle('ne',S.ne.has(k))}}
  return{el:w,sel,B,Cl,paint,lock(){lk=true}}}
IW.nash=(ch,o)=>{const mode=ch.step||'ne';const u=nashUI(ch,mode,()=>o.on&&o.on());const S=nashBR(ch.pay);const A=mode==='br'?S.br:S.ne;
  return{el:u.el,note:mode==='br'?'Para cada columna, toca el mejor pago del primer jugador; para cada fila, el mejor pago del segundo (empates: tócalos todos).':'Toca la(s) casilla(s) donde ninguno quiere cambiar de estrategia.',
   need:'Toca al menos una opción.',okMsg:mode==='br'?'¡Mejores respuestas correctas!':'¡Ese es el equilibrio de Nash!',filled:()=>u.sel.size>0,
   grade(){const wr=[...u.sel].filter(k=>!A.has(k)).length,mi=[...A].filter(k=>!u.sel.has(k)).length;
     const f=mode==='br'?Math.max(0,(A.size-mi-wr)/A.size):(wr||mi?0:1);
     return{f,msg:f>=1?'':(wr?(wr===1?'Una marca no va':wr+' marcas no van')+'. ':'')+(mi?(mi===1?'Te falta una':'Te faltan '+mi)+'.':'')+(ch.e?'<br>'+ch.e:'')}},
   mark(){if(mode==='br')for(const k in u.B){const s=u.sel.has(k);u.B[k].classList.toggle('good',s&&A.has(k));u.B[k].classList.toggle('bad',s&&!A.has(k))}
     else for(const k in u.Cl){const s=u.sel.has(k);u.Cl[k].classList.toggle('good',s&&A.has(k));u.Cl[k].classList.toggle('bad',s&&!A.has(k))}},
   reveal(){u.sel.clear();A.forEach(k=>u.sel.add(k));u.paint(true)},lock(){u.lock()}}};
LW.nash=(b,o)=>{const w=el('div','nsw0');const top=el('div','plctl');const box=el('div');const bt=el('button','lwb','Mostrar mejores respuestas');bt.type='button';let cur=o,u;
  const draw=()=>{box.innerHTML='';u=nashUI(cur,'show');box.append(u.el);if(cur.txt)box.append(el('p','note',cur.txt));if(bt.classList.contains('on'))u.paint(true)};
  bt.onclick=()=>{bt.classList.toggle('on');u.paint(bt.classList.contains('on'));if(!bt.classList.contains('on'))draw()};
  (o.presets||[]).forEach(([l,p],i)=>{const x=el('button','lwb'+(i?'':' on'),l);x.type='button';x.onclick=()=>{top.querySelectorAll('.lwb').forEach(z=>z.classList.toggle('on',z===x));cur=Object.assign({},o,p);bt.classList.remove('on');draw()};top.append(x)});
  if(o.presets&&o.presets.length)cur=Object.assign({},o,o.presets[0][1]);w.append(top,box,bt);b.append(w);draw()};
/* ---------- beneficio máximo ---------- */
function qmaxUI(o,on){const w=el('div','qmw');const fig=el('div','plfig'),ctl=el('div','plctl'),ro=el('div','acro');w.append(fig,ctl,ro);
  const pc=o.mode==='pc';const F=o.F||0,c=o.c||0,d=o.d||0;const Qm=o.qmax||(pc?Math.max(10,2*(o.P-c)/(2*d||1)):o.a/o.b);
  const P=q=>pc?o.P:o.a-o.b*q,IMg=q=>pc?o.P:o.a-2*o.b*q,CT=q=>F+c*q+d*q*q,CMg=q=>c+2*d*q,CMe=q=>q>0?CT(q)/q:NaN;
  let q=o.q0!=null?o.q0:Qm*0.2;const st=o.step||(Qm<=20?0.5:1);
  const r=el('label','acsl');r.append(el('span','plrl','Q ='));const i=el('input','plrg');i.type='range';i.min=st;i.max=Qm;i.step=st;i.value=q;i.setAttribute('aria-label','Cantidad');const v=el('b',null,fmtV(q));
  i.oninput=()=>{q=+i.value;v.textContent=fmtV(q);draw();on&&on()};r.append(i,v);ctl.append(r);
  let ymax=0;for(let k=1;k<=40;k++){const x=Qm*k/40;[P(x),CMg(x),CMe(x)].forEach(y=>{if(isFinite(y))ymax=Math.max(ymax,y)})}ymax=Math.min(ymax*1.08,(pc?o.P:o.a)*1.8);
  const W=320,H=240,L=34,R=10,T=10,B=24,X=x=>L+(W-L-R)*x/Qm,Y=y=>T+(H-T-B)*(1-Math.max(-0.05*ymax,Math.min(ymax,y))/ymax);
  const path=(f,cl,a0,a1)=>{let s='';const e1=a1!=null?Math.min(a1,Qm):Qm;for(let k=0;k<=80;k++){const x=(a0||0)+(e1-(a0||0))*k/80,y=f(x);if(!isFinite(y))continue;s+=(s?'L':'M')+X(x).toFixed(1)+' '+Y(y).toFixed(1)}return '<path class="qm '+cl+'" d="'+s+'"/>'};
  const fmt=x=>fmtV(Math.round(x*100)/100);
  function draw(){const p=P(q),cme=CMe(q),pr=p*q-CT(q);
    let s='<svg class="pls" viewBox="0 0 '+W+' '+H+'" xmlns="http://www.w3.org/2000/svg"><path class="gl" d="M'+L+' '+T+'V'+(H-B)+'H'+(W-R)+'" style="fill:none;stroke:var(--ink)"/>';
    s+='<rect class="qmr '+(pr>=0?'pos':'neg')+'" x="'+X(0)+'" y="'+Math.min(Y(p),Y(cme))+'" width="'+(X(q)-X(0))+'" height="'+Math.abs(Y(p)-Y(cme))+'"/>';
    s+=path(CMe,'cme',Qm*0.04)+path(CMg,'cmg');if(pc)s+=path(P,'dd');else s+=path(P,'dd')+path(IMg,'img',0,o.a/(2*o.b));
    s+='<line class="qmq" x1="'+X(q)+'" y1="'+T+'" x2="'+X(q)+'" y2="'+(H-B)+'"/><circle class="qmp" cx="'+X(q)+'" cy="'+Y(p)+'" r="3.5"/>';
    const lab=(t,x,y,cl)=>'<text class="qml '+cl+'" x="'+X(x)+'" y="'+Math.max(T+9,Math.min(H-B-3,Y(y)-4))+'" text-anchor="end">'+t+'</text>';
    s+=lab('CMg',Qm*.98,CMg(Qm*.98),'cmg')+lab('CMe',Qm*.98,CMe(Qm*.98),'cme')+(pc?lab('P = IMg',Qm*.98,o.P,'dd'):lab('D',Qm*.98,P(Qm*.98),'dd')+lab('IMg',Math.min(Qm*.98,o.a/(2*o.b)*0.95),IMg(Math.min(Qm*.98,o.a/(2*o.b)*0.95)),'img'));
    s+='<text class="qml" x="'+(W-R)+'" y="'+(H-6)+'" text-anchor="end">Q</text><text class="qml" x="4" y="'+(T+8)+'">S/</text></svg>';fig.innerHTML=s;
    const im=IMg(q),cm=CMg(q);
    ro.innerHTML='<div class="tbl"><table class="pott"><tr><th>Q</th><th>P</th><th>IT</th><th>CT</th><th>Beneficio</th></tr><tr><td>'+fmt(q)+'</td><td>'+fmt(p)+'</td><td>'+fmt(p*q)+'</td><td>'+fmt(CT(q))+'</td><td><b>'+fmt(pr)+'</b></td></tr></table></div>'+
      '<p>IMg = '+fmt(im)+' · CMg = '+fmt(cm)+' → '+(Math.abs(im-cm)<1e-6?'<b>IMg = CMg: beneficio máximo</b>':im>cm?'IMg &gt; CMg: <b>conviene producir más</b> (la próxima unidad suma más de lo que cuesta)':'IMg &lt; CMg: <b>conviene producir menos</b> (la última unidad cuesta más de lo que aporta)')+'</p>'+
      '<p class="note">'+(pr>=0?'Rectángulo verde: beneficio = (P − CMe) · Q.':'Rectángulo rojo: pérdida = (CMe − P) · Q.')+'</p>';w.dataset.q=q}
  draw();return{el:w,get q(){return q},set q(x){q=x;i.value=x;v.textContent=fmtV(x);draw()},lock(){i.disabled=true}}}
LW.qmax=(b,o)=>{const w=el('div');const top=el('div','plctl');const box=el('div');w.append(top,box);b.append(w);
  const show=p=>{box.innerHTML='';box.append(qmaxUI(p).el)};
  (o.presets||[]).forEach(([l,p],i)=>{const x=el('button','lwb'+(i?'':' on'),l);x.type='button';x.onclick=()=>{top.querySelectorAll('.lwb').forEach(z=>z.classList.toggle('on',z===x));show(p)};top.append(x)});
  show(o.presets&&o.presets.length?o.presets[0][1]:o)};
IW.qmax=(ch,o)=>{let touched=false;const u=qmaxUI(ch,()=>{touched=true;o.on&&o.on()});const ok=()=>Math.abs(u.q-ch.ans)<=(ch.tol!=null?ch.tol:0.51);
  return{el:u.el,note:'Mueve Q con el deslizador hasta el beneficio máximo.',need:'Mueve el deslizador primero.',okMsg:'¡Ahí IMg = CMg y el beneficio es el máximo!',filled:()=>touched,
   grade(){return{f:ok()?1:0,msg:ok()?'':'Todavía no es el máximo: compara IMg con CMg. '+(ch.e||'')}},mark(){},reveal(){u.q=ch.ans},lock(){u.lock()}}};
/* ---------- juego del polizón ---------- */
LW.poliz=(b,o)=>{const N=5,R=5,E=10,TH=30,BEN=15;const w=el('div','pzw');b.append(w);let bots,hist,mine,tot;
  const reset=()=>{bots=[10,10,10,5];hist=[];mine=0;tot=[0,0,0,0];draw()};
  const nextBots=allc=>bots.map((bv,i)=>{const others=allc.filter((_,j)=>j!==i+1);const avg=others.reduce((a,x)=>a+x,0)/4;return Math.max(0,Math.min(E,5*Math.round((avg-1)/5)))});
  function play(u){const allc=[u,...bots];const t=allc.reduce((a,x)=>a+x,0);const built=t>=TH;hist.push({u,b:bots.slice(),t,built});
    mine+=E-u+(built?BEN:0);bots.forEach((x,i)=>tot[i]+=E-x+(built?BEN:0));bots=nextBots(allc);draw()}
  function draw(){const r=hist.length;let h='<p class="pzh">Ronda '+Math.min(r+1,R)+' de '+R+' · cada ronda recibes <b>S/ 10</b>. Si entre los 5 juntan <b>S/ 30</b>, se construye el parque y <b>todos</b> ganan S/ 15, hayan aportado o no.</p>';
    if(hist.length){h+='<div class="tbl"><table class="pott pzt"><tr><th>Ronda</th><th>Tú</th><th>Vecinos</th><th>Total</th><th>Parque</th></tr>'+hist.map((x,k)=>'<tr><td>'+(k+1)+'</td><td><b>'+x.u+'</b></td><td>'+x.b.join(' · ')+'</td><td>'+x.t+'</td><td>'+(x.built?'🌳 sí':'❌ no')+'</td></tr>').join('')+'</table></div>'+
      '<p>Tu plata: <b>S/ '+mine+'</b> · vecinos: '+tot.map(x=>'S/ '+x).join(', ')+'</p>'}
    w.innerHTML=h;
    if(r<R){const row=el('div','plctl');row.append(el('span','plrl','¿Cuánto aportas?'));[0,5,10].forEach(x=>{const bt=el('button','lwb','S/ '+x);bt.type='button';bt.onclick=()=>play(x);row.append(bt)});w.append(row)}
    else{const best=Math.max(...tot);w.append(el('div','pzend','<p><b>Fin del juego.</b> Si los 5 aportaran S/ 10 siempre, cada uno ganaría <b>S/ 75</b> (S/ 15 por ronda). '+
      (hist.filter(x=>x.built).length<R?'Pero cuando alguien deja de aportar, los demás también reducen sus aportes y el parque deja de hacerse: todos terminan peor.':'Aportaste y el parque se mantuvo: todos ganaron.')+'</p>'+
      '<p>Eso es el <b>problema del polizón</b>: como nadie puede ser excluido del parque, a cada uno le conviene que paguen los otros. Por eso los bienes públicos suelen financiarse con <b>impuestos</b>.</p>'));
      const rs=el('button','lwb on','⟲ Jugar otra vez');rs.type='button';rs.onclick=reset;w.append(rs)}}
  reset()};
