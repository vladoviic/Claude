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

/* Champ irisé (WebGL, rendu à mi-résolution) */
const IRI=(()=>{
  const c=document.createElement('canvas'); c.width=960; c.height=540;
  const gl=c.getContext('webgl',{preserveDrawingBuffer:true,antialias:false,premultipliedAlpha:false});
  if(!gl) return null;
  const vs=`attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}`;
  const fs=`precision highp float;
  uniform vec2 R; uniform float T,S,Z,HOT,BANDS,TH;
  vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return -1.+2.*fract(sin(p)*43758.5453);}
  float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);
    return mix(mix(dot(h2(i),f),dot(h2(i+vec2(1,0)),f-vec2(1,0)),u.x),mix(dot(h2(i+vec2(0,1)),f-vec2(0,1)),dot(h2(i+vec2(1,1)),f-vec2(1,1)),u.x),u.y);}
  float fbm(vec2 p){float v=0.,a=.55;for(int i=0;i<4;i++){v+=a*n(p);p=p*2.02+vec2(1.7,9.2);a*=.45;}return v;}
  vec3 ramp(float x){
    x=fract(x)*6.;
    vec3 c0=vec3(.99,.95,.91),c1=vec3(1.,.78,.62),c2=vec3(1.,.67,.76),c3=vec3(1.,.86,.74),c4=vec3(.72,.90,.95),c5=vec3(.84,.79,1.);
    vec3 a=c0,b=c1; float t=fract(x);
    if(x<1.){a=c0;b=c1;}else if(x<2.){a=c1;b=c2;}else if(x<3.){a=c2;b=c3;}else if(x<4.){a=c3;b=c4;}else if(x<5.){a=c4;b=c5;}else{a=c5;b=c0;}
    return mix(a,b,smoothstep(0.,1.,t));
  }
  vec3 therm(float x){
    x=fract(x)*6.;
    vec3 w=vec3(1.,.985,.97),pe=vec3(1.,.74,.52),co=vec3(1.,.38,.40),li=vec3(.83,.76,1.),cy=vec3(.70,.92,.99);
    vec3 a=w,b=pe; float t=fract(x);
    if(x<1.){a=w;b=pe;}else if(x<2.){a=pe;b=co;}else if(x<3.){a=co;b=w;}else if(x<4.){a=w;b=li;}else if(x<5.){a=li;b=cy;}else{a=cy;b=w;}
    return mix(a,b,smoothstep(.25,.75,t));
  }
  void main(){
    vec2 p=(gl_FragCoord.xy-.5*R)/R.y*Z + vec2(S*3.1,S*1.7);
    float t=T*.16;
    vec2 q=vec2(fbm(p+vec2(0.,t)),fbm(p+vec2(5.2,1.3)-t*.8));
    vec2 r=vec2(fbm(p+1.7*q+vec2(1.7,9.2)+.5*t),fbm(p+1.7*q+vec2(8.3,2.8)-.35*t));
    float v=fbm(p+1.5*r);
    float x=v*.95+r.x*.45+q.y*.3+.4;
    vec3 col=ramp(x);
    col=mix(col,vec3(.99,.95,.91),.12);
    float hot=smoothstep(.18,.62,r.y*1.2+v*.8);
    col=mix(col,vec3(1.,.31,.42),hot*HOT);
    float b=abs(fract(x*6.)-.5)*2.;
    col=mix(col,min(vec3(1.),col*1.04+.07),(1.-smoothstep(0.,.16,b))*BANDS);
    col=mix(col,therm(x*1.9+v*.6),TH);
    gl_FragColor=vec4(col,1.);
  }`;
  function sh(t,src){const s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(s);return s;}
  const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
  const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const U={};for(const k of ['R','T','S','Z','HOT','BANDS','TH'])U[k]=gl.getUniformLocation(pr,k);
  gl.viewport(0,0,960,540); gl.uniform2f(U.R,960,540);
  return {canvas:c,draw(o){gl.uniform1f(U.T,o.t||0);gl.uniform1f(U.S,o.seed||0);gl.uniform1f(U.Z,(o.zoom||1.5)*.62);gl.uniform1f(U.HOT,o.hot??.18);gl.uniform1f(U.BANDS,o.bands??.35);gl.uniform1f(U.TH,o.therm||0);gl.drawArrays(gl.TRIANGLES,0,3);gl.finish();}};
})();
function iriTo(cv,o,src){ // src = [sx,sy,sw,sh] dans le canvas 960×540
  const ctx=cv.getContext('2d');
  if(IRI){ IRI.draw(o); const s=src||[0,0,960,540]; ctx.drawImage(IRI.canvas,s[0],s[1],s[2],s[3],0,0,cv.width,cv.height); }
  else { const g=ctx.createLinearGradient(0,0,cv.width,cv.height); g.addColorStop(0,'#FFC7A1');g.addColorStop(.5,'#FFA6C9');g.addColorStop(1,'#A9E7F2'); ctx.fillStyle=g; ctx.fillRect(0,0,cv.width,cv.height); }
}

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
