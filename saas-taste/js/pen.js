/* ============================================================
   Le stylo rouge : chaque marque est un geste de Vladan enregistré (page « Prises au stylo »,
   fichiers pen/G01.json…G09.json). Tant qu'une prise manque, la marque est un brouillon de synthèse
   (PEN.draft) : le rendu final le refuse (render.mjs ?final).
   Encre : contour perfect-freehand piloté par la pression, feutre sur papier (multiply, fibres qui
   transparaissent, bord plus dense, flaque aux extrémités, bord dentelé par la dent du papier),
   humide 6 images puis mat. Sur fond sombre : normal, pleine densité.
   ============================================================ */
const PEN={red:'#FF3D5E', takes:{}, draft:new Set(), ms:1000/FPS};
// cibles des prises dans la page de capture (coordonnées 1920×1080 de la planche) : x0,y0,x1,y1
const PEN_GUIDE={G01:[930,575,990,635],G02:[660,340,1320,790],G03:[0,0,0,0],G04:[342,520,1210,652],G05:[0,0,0,0],
  G06:[750,400,1170,680],G07:[560,470,1360,640],G08:[574,254,1346,826],G09:[0,0,0,0]};

/* ---------- prises : fichiers enregistrés, sinon brouillon de synthèse ---------- */
function penSynth(id){
  const R=rng(7000+parseInt(id.slice(1))); const n=(a=1)=>(R()-0.5)*2*a; const pts=[]; let t=0;
  const add=(x,y,p,dt)=>{ t+=dt; pts.push([x,y,p,t]); };
  const line=(x0,y0,x1,y1,ms,{bow=0,wob=1.2,p0=.35,p1=.75,pe=.3}={})=>{ const N=Math.max(6,Math.round(ms/4)); const s=[];
    for(let i=0;i<=N;i++){ const u=i/N, e=u*u*(3-2*u); const px=-(y1-y0), py=x1-x0, L=Math.hypot(px,py)||1;
      const b=Math.sin(Math.PI*u)*bow; const x=x0+(x1-x0)*e+px/L*(b+n(wob)), y=y0+(y1-y0)*e+py/L*(b+n(wob));
      const p=u<.2?lerp(p0,p1,u/.2):u>.8?lerp(p1,pe,(u-.8)/.2):p1+n(.04); s.push([x,y,clamp(p,.05,1),i?ms/N:0]); } return s; };
  const strokes=[]; const push=s=>{ const o=[]; for(const [x,y,p,dt] of s){ t+=dt; o.push([x,y,p,t]); } strokes.push(o); };
  if(id==='G01'){ push([...line(935,630,960,582,70,{bow:-2,p0:.3,p1:.7}),...line(960,582,986,628,63,{bow:2,p1:.6,pe:.2}).slice(1)]); }
  if(id==='G02'){ push(line(1310,350,672,780,233,{bow:-18,wob:1.6,p0:.5,p1:.9,pe:.35})); }
  // marques sur un texte : tracées en px sur 100 px, puis x ramené à 0..1 (penPlace les pose sur le mot)
  const norm=s=>s.map(([x,y,p,dt])=>[x/100,y,p,dt]);
  if(id==='G03'){ push(norm(line(0,3,100,-1,167,{bow:1,wob:.35,p0:.45,p1:.8,pe:.4}))); }
  if(id==='G04'){ const s=[]; const N=58; for(let i=0;i<=N;i++){ const u=i/N, e=u*u*(3-2*u); const x=lerp(350,1205,e); const y=586-Math.sin(e*Math.PI*2)*58+n(1);
      s.push([x,y,clamp(.4+.45*Math.sin(Math.PI*u)+n(.03),.05,1),i?233/N:0]); } push(s); }
  if(id==='G05'){ push(norm(line(0,3,100,-2,133,{bow:-1,wob:.35,p0:.5,p1:.85,pe:.35}))); }
  if(id==='G06'){ push(line(760,410,1160,670,83,{bow:6,p0:.6,p1:.9})); t+=40; push(line(1158,414,764,664,83,{bow:-5,p0:.6,p1:.9})); }
  if(id==='G07'){ push(line(575,560,1345,548,200,{bow:-10,wob:2.5,p0:.7,p1:1,pe:.6})); }
  if(id==='G08'){ const s=[]; const rows=6; let dt=0;
    for(let r=0;r<rows;r++){ const y=290+r*100, L2R=r%2==0; const xa=L2R?585:1335, xb=L2R?1335:585; const N=26;
      for(let i=0;i<=N;i++){ if(r&&!i) continue; const u=i/N; const x=lerp(xa,xb,u)+n(3), yy=y+Math.sin(u*Math.PI*7)*9+n(3)+(u>.92?(L2R?1:-1)*0:0);
        s.push([x,yy+(u>.9?(u-.9)*10*50:0),clamp(.55+n(.12),.1,1),i||r?20:0]); } }
    const hx=1210, hy=790; for(let i=0;i<10;i++) s.push([hx+n(1.5),hy+n(1.5),.15,6]);          // dwell sur la poignée de main
    for(let i=0;i<=26;i++){ const a=i/26*Math.PI*2.2; s.push([hx+18+Math.cos(a+Math.PI)*22+i*1.6,hy-10+Math.sin(a+Math.PI)*20-i*.6,clamp(.6-.4*i/26,.08,1),8]); }
    push(s); }
  if(id==='G09'){ push(norm(line(0,2,100,-3,267,{bow:2,wob:.4,p0:.5,p1:.8,pe:.25}))); }
  return {gesture:id,strokes,durationMs:t,draft:true};
}
function penLoad(id){
  return fetch(`pen/${id}.json`).then(r=>{ if(!r.ok) throw 0; return r.json(); })
    .then(j=>{ PEN.takes[id]=j; }).catch(()=>{ PEN.takes[id]=penSynth(id); PEN.draft.add(id); });
}
ASYNC.push(...['G01','G02','G03','G04','G05','G06','G07','G08','G09'].map(penLoad));

/* ---------- placement : la cible de la prise posée sur la cible du film ---------- */
// rect = [x0,y0,x1,y1] de la cible dans la scène ; pour les marques sur un texte (G03/G05/G09), la prise
// est normalisée (0..1 en x) et posée sur la ligne du texte : y = milieu de la hauteur d'x.
function penPlace(id,rect,{mode='box'}={}){
  const tk=PEN.takes[id]; const g=PEN_GUIDE[id];
  let fx;
  if(tk.draft&&(id==='G03'||id==='G05'||id==='G09')){ const w=rect[2]-rect[0]; fx=([x,y])=>[rect[0]+x*w, rect[1]+y]; }
  else if(id==='G03'||id==='G05'||id==='G09'){ // prise réelle : on cale ses extrémités sur la cible
    const all=tk.strokes.flat(); const xs=all.map(p=>p[0]), ys=all.map(p=>p[1]); const a=Math.min(...xs), b=Math.max(...xs), my=ys.reduce((s,v)=>s+v,0)/ys.length;
    const k=(rect[2]-rect[0])/Math.max(1,b-a); fx=([x,y])=>[rect[0]+(x-a)*k, rect[1]+(y-my)*Math.min(k,1.3)]; }
  else { const sx=(rect[2]-rect[0])/(g[2]-g[0]), sy=(rect[3]-rect[1])/(g[3]-g[1]); const s=mode==='fit'?Math.min(sx,sy):Math.sqrt(sx*sy);
    const cx=(g[0]+g[2])/2, cy=(g[1]+g[3])/2, tx=(rect[0]+rect[2])/2, ty=(rect[1]+rect[3])/2; fx=([x,y])=>[tx+(x-cx)*(mode==='stretch'?sx:s), ty+(y-cy)*(mode==='stretch'?sy:s)]; }
  return tk.strokes.map(s=>s.map(p=>{ const [x,y]=fx(p); return [x,y,p[2],p[3]]; }));
}
const penDur=id=>PEN.takes[id].durationMs/PEN.ms;   // en images

/* ---------- géométrie ---------- */
function penArc(pts){ const a=[0]; for(let i=1;i<pts.length;i++) a.push(a[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1])); return a; }
// sous-tracé entre deux abscisses curvilignes (fractions 0..1)
function penSlice(pts,u0,u1){ const A=penArc(pts), L=A[A.length-1]||1, a=u0*L, b=u1*L; const out=[];
  const at=s=>{ let i=1; while(i<A.length-1&&A[i]<s) i++; const t=(s-A[i-1])/Math.max(1e-6,A[i]-A[i-1]); const p=pts[i-1], q=pts[i]; return [lerp(p[0],q[0],t),lerp(p[1],q[1],t),lerp(p[2],q[2],t),lerp(p[3],q[3],t)]; };
  out.push(at(a)); for(let i=0;i<pts.length;i++) if(A[i]>a&&A[i]<b) out.push(pts[i]); out.push(at(b)); return out; }

/* ---------- matière : dent du papier (une tuile de bruit anisotrope 4:1, calculée une fois) ---------- */
const PAPER_N=(()=>{ const S=256, c=document.createElement('canvas'); c.width=c.height=S; const x=c.getContext('2d'), im=x.createImageData(S,S); const R=rng(91);
  const g=[]; for(let i=0;i<64*16;i++) g.push(R());
  const v=(X,Y)=>{ const xi=Math.floor(X), yi=Math.floor(Y), fx=X-xi, fy=Y-yi; const h=(a,b)=>g[((a&63)+(b&15)*64)];
    const s=t=>t*t*(3-2*t); return lerp(lerp(h(xi,yi),h(xi+1,yi),s(fx)),lerp(h(xi,yi+1),h(xi+1,yi+1),s(fx)),s(fy)); };
  for(let j=0;j<S;j++) for(let i=0;i<S;i++){ let a=0, w=.5, fr=1; for(let o=0;o<5;o++){ a+=w*v(i/S*64*fr/4, j/S*16*fr); w*=.5; fr*=2; } const k=(j*S+i)*4; const val=Math.round(a/0.97*255);
    im.data[k]=im.data[k+1]=im.data[k+2]=255; im.data[k+3]=val; }
  x.putImageData(im,0,0); return c; })();

/* ---------- dessin d'une marque ---------- */
// strokes : [[x,y,p,tMs]…] en coordonnées de la scène ; f : image courante ; f0 : image du toucher.
// opts : size (px), ground 'paper'|'dark', u0/u1 (tranche d'abscisse pour les marques consommées), lift (force la levée),
// uniform (0..1 : largeur rendue uniforme), alpha.
function penOutline(pts,size,uniform=0,last=true){
  const P=pts.map(p=>[p[0],p[1],lerp(p[2],0.6,uniform)]);
  return PF.getStroke(P,{size,thinning:lerp(.55,0,uniform),smoothing:.62,streamline:.38,simulatePressure:false,
    start:{taper:lerp(5,0,uniform),cap:true},end:{taper:lerp(Math.min(30,size*3),0,uniform),cap:true},last});
}
function penPath(poly){ const p=new Path2D(); if(!poly.length) return p; p.moveTo(poly[0][0],poly[0][1]); for(let i=1;i<poly.length;i++) p.lineTo(poly[i][0],poly[i][1]); p.closePath(); return p; }
function penVisible(strokes,f,f0){ const ms=(f-f0)*PEN.ms; const out=[];
  for(const s of strokes){ if(!s.length||s[0][3]>ms) continue; const v=s.filter(p=>p[3]<=ms); if(v.length) out.push({pts:v,done:v.length===s.length}); } return out; }
function penDraw(ctx,strokes,f,f0,{size=4,ground='paper',u0=0,u1=1,uniform=0,alpha=1,wetFrames=6,color=null}={}){
  const vis=penVisible(strokes,f,f0); if(!vis.length) return; ctx.canvas.style.display='block';
  const lastT=Math.max(...strokes.map(s=>s[s.length-1][3]))/PEN.ms+f0; const wet=clamp(1-(f-lastT)/wetFrames);
  ctx.save(); ctx.globalAlpha=alpha;
  for(const {pts,done} of vis){
    const p=(u0>0||u1<1)?penSlice(pts,u0,u1):pts; if(p.length<2) continue;
    const path=penPath(penOutline(p,size,uniform,done));
    if(ground==='dark'||color){ ctx.fillStyle=color||PEN.red; ctx.fill(path); continue; }
    // feutre sur papier : aplat, bord plus dense, fibres qui transparaissent
    ctx.fillStyle=wet>0?mixHex('#FF3D5E','#FF6A82',0.18*wet):'#FF3D5E'; ctx.fill(path);
    ctx.save(); ctx.clip(path);
    ctx.strokeStyle='rgba(176,18,52,0.32)'; ctx.lineWidth=Math.min(3,size*.45); ctx.stroke(path);
    ctx.globalCompositeOperation='destination-out'; ctx.globalAlpha=alpha*0.16;
    const pat=ctx.createPattern(PAPER_N,'repeat'); pat.setTransform(new DOMMatrix([0.9,0,0,0.9,(p[0][0]*7)%256,0])); ctx.fillStyle=pat;
    const b=penBounds(p,size); ctx.fillRect(b[0],b[1],b[2]-b[0],b[3]-b[1]);
    ctx.restore();
  }
  ctx.restore();
}
function penBounds(pts,pad=0){ let a=1e9,b=1e9,c=-1e9,d=-1e9; for(const p of pts){ a=Math.min(a,p[0]); b=Math.min(b,p[1]); c=Math.max(c,p[0]); d=Math.max(d,p[1]); } return [a-pad,b-pad,c+pad,d+pad]; }
function mixHex(a,b,t){ const A=hex(a), B=hex(b); return 'rgb('+A.map((v,i)=>Math.round(lerp(v,B[i],t))).join(',')+')'; }

/* ---------- calque d'encre d'une scène : un canvas plein cadre au-dessus de la caméra ---------- */
function inkLayer(scene,{ground='paper'}={}){ const c=document.createElement('canvas'); c.width=W; c.height=H; c.className='ink';
  c.style.cssText=`position:absolute;inset:0;width:${W}px;height:${H}px;pointer-events:none;mix-blend-mode:${ground==='dark'?'normal':'multiply'}`;
  scene.appendChild(c); return c; }
// le calque est masqué tant que rien n'y est dessiné (Chromium ne recompose pas toujours un canvas en multiply vidé)
function inkClear(c){ const x=c.getContext('2d'); x.setTransform(1,0,0,1,0,0); x.clearRect(0,0,W,H); c.style.display='none'; return x; }

/* ---------- un trait ré-échantillonné (N points à pas constant) : base des morphoses et du fil tiré ---------- */
function penResample(pts,N){ const A=penArc(pts), L=A[A.length-1]||1; const out=[]; let i=1;
  for(let k=0;k<N;k++){ const s=k/(N-1)*L; while(i<A.length-1&&A[i]<s) i++; const t=(s-A[i-1])/Math.max(1e-6,A[i]-A[i-1]); const p=pts[i-1], q=pts[i];
    out.push([lerp(p[0],q[0],t),lerp(p[1],q[1],t),lerp(p[2],q[2],t),lerp(p[3],q[3],t)]); } return out; }
