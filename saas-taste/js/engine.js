/* ============================================================
   Moteur : chaque image est une fonction pure de f (frame).
   ============================================================ */
const W=1920,H=1080,FPS=30,TOTAL=1560;   // 52 s : la réf (50,5 s) + 1,5 s de tenue pour l'e-mail
const BPM=135, BEAT0=10;                  // grille de la réf : 135 BPM, premier temps à 0,33 s (image 10)
const BEATF=FPS*60/BPM;                   // 13,33 images par temps
const NS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id);
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const lerp=(a,b,t)=>a+(b-a)*t;
// Arrivée rapide, fin douce : décroissance exponentielle (k de la distance restante par image)
// multipliée par (1-t)² pour arriver pile à dur avec une vitesse nulle (jamais d'arrêt sec).
function approach(f,f0,dur,k=0.12){ if(f<=f0) return 0; if(f>=f0+dur) return 1; const n=f-f0, t=n/dur; return 1-Math.pow(1-k,n)*(1-t)*(1-t); }
// Sortie : accélère (pour les éléments qui quittent le cadre).
function accel(f,f0,dur,pw=2.6){ return Math.pow(clamp((f-f0)/dur),pw); }
// « vladan » : la courbe de vitesse du trait de Vladan (départ humain lognormal, arrivée rapide, atterrissage doux, zéro dépassement).
// En attendant la prise G02 : CDF lognormale μ=ln(0,22), σ=0,5 (remplacée par la table tirée de la prise quand elle existe).
const ERF=x=>{ const t=1/(1+0.3275911*Math.abs(x)); const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x); return x>=0?y:-y; };
const VL_MU=Math.log(0.22), VL_SG=0.5, VL_N=0.5*(1+ERF((0-VL_MU)/(VL_SG*Math.SQRT2)));
let VL_LUT=null;
function vladan(t){ t=clamp(t); if(t<=0) return 0; if(t>=1) return 1;
  if(VL_LUT){ const x=t*(VL_LUT.length-1), i=Math.floor(x); return lerp(VL_LUT[i],VL_LUT[Math.min(i+1,VL_LUT.length-1)],x-i); }
  return 0.5*(1+ERF((Math.log(t)-VL_MU)/(VL_SG*Math.SQRT2)))/VL_N; }
const vl=(f,f0,dur,t0=0)=>f<=f0?0:vladan(t0+(1-t0)*clamp((f-f0)/dur));
// l'ancien « pop » avec dépassement (Lottie) : remplacé par vladan, sans rebond
function back(f,f0,dur){ return vl(f,f0,dur); }
// la voix du fondateur bouge en linéaire, sur deux images
const twos=(f,f0)=>f0+2*Math.floor((f-f0)/2);
function rng(seed){ return ()=>{ seed|=0; seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function hex(c){ c=c.replace('#',''); return [0,2,4].map(i=>parseInt(c.slice(i,i+2),16)); }
function mixc(a,b,t){ const A=hex(a),B=hex(b); return `rgb(${A.map((v,i)=>Math.round(lerp(v,B[i],t))).join(',')})`; }
function mixa(a,b,t){ return a.map((v,i)=>lerp(v,b[i],t)); }
function rgba(a){ return `rgba(${Math.round(a[0])},${Math.round(a[1])},${Math.round(a[2])},${a[3].toFixed(3)})`; }
function show(el,on){ el.style.display=on?'block':'none'; }
// Place un élément centré en (x,y).
function place(el,x,y,s=1,r=0,sx=1){ el.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px) translate(-50%,-50%) rotate(${r.toFixed(2)}deg) scale(${(s*sx).toFixed(4)},${s.toFixed(4)})`; }
function placeTL(el,x,y,s=1){ el.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px) scale(${s.toFixed(4)})`; }

/* Flou de mouvement directionnel (SVG feGaussianBlur anisotrope) */
const fxDefs=$('fx'); const blurMap=new Map(); let blurN=0;
function mblur(el,bx,by){
  bx=Math.min(60,Math.abs(bx)); by=Math.min(60,Math.abs(by));
  if(bx<0.35&&by<0.35){ el.style.filter=''; return; }
  let g=blurMap.get(el);
  if(!g){ const fl=document.createElementNS(NS,'filter'); fl.id='mb'+(blurN++);
    for(const [k,v] of [['x','-80%'],['y','-80%'],['width','260%'],['height','260%'],['color-interpolation-filters','sRGB']]) fl.setAttribute(k,v);
    g=document.createElementNS(NS,'feGaussianBlur'); fl.appendChild(g); fxDefs.appendChild(fl); blurMap.set(el,g); g._id=fl.id; }
  g.setAttribute('stdDeviation',`${bx.toFixed(2)} ${by.toFixed(2)}`);
  el.style.filter=`url(#${g._id})`;
}
const BLUR=0.32; // px de flou par px/image de vitesse
function vel(fn,f){ return fn(f+0.5)-fn(f-0.5); }

/* Curseur */
const CUR=$('cursor');
// le seul curseur du film : celui du fondateur (flèche ou main, bleu #2D6CDF, drapeau « You »)
function cursor(x,y,press=0,on=true,size=1,shape='arrow'){ show(CUR,on); if(!on) return; CUR.dataset.shape=shape;
  CUR.style.transform=`translate(${(x-4).toFixed(1)}px,${(y-4).toFixed(1)}px) scale(${(size*(1-0.14*press)).toFixed(3)})`; }

/* Cues son : chaque bruitage est déclaré à côté de son action */
const CUES=[]; const cue=(f,k,o={})=>CUES.push(Object.assign({},o,{f,k}));
const R=rng(44);

/* images (rendus Cycles) à décoder avant le premier rendu */
const PRELOAD=[], ASYNC=[];   // ASYNC : données (JSON) à attendre aussi
function preload(src){ const im=new Image(); im.src=src; PRELOAD.push(im); return im; }

/* séquences rendues (Cycles, img/<dossier>/) : toutes les images préchargées, on dessine celle du numéro demandé,
   recadrée en « cover » comme un object-fit */
function seqLoad(dir,prefix,n,ext='jpg',from=0){ const a=[]; for(let i=from;i<n;i++) a[i]=preload(`img/${dir}/${prefix}_${String(i).padStart(2,'0')}.${ext}`); return a; }
function seqDraw(cv,frames,i,px=0.5,py=0.5,zoom=1){ const k=frames.length-1; let j=clamp(Math.round(i),0,k); while(!frames[j]&&j<k) j++; const im=frames[j];
  const W=cv.width,H=cv.height,iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height, s=Math.max(W/iw,H/ih)*zoom, sw=W/s, sh=H/s;
  cv.getContext('2d').drawImage(im,(iw-sw)*px,(ih-sh)*py,sw,sh,0,0,W,H); }

// cue écrit en numéros de la réf pour une scène recalée de d images (le REMAP le ramènera)
function cueAt(d){ return (f,k,o={})=>{ const q={...o}; if('peak' in q) q.peak+=d; if('end' in q) q.end+=d; cue(f+d,k,q); }; }
function seqDrawRaw(cv,im){ cv.getContext('2d').drawImage(im,0,0,cv.width,cv.height); }
