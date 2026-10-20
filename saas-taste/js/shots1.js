/* ============================================================
   Plans 1 à 16 : timings recopiés de la réf (numéros d'image de la réf, cf. SPEC.md)
   ============================================================ */
function el(parent,cls='',html='',css=''){ const d=document.createElement('div'); if(cls) d.className=cls; if(html) d.innerHTML=html; if(css) d.style.cssText=css; parent.appendChild(d); return d; }
function canvas(parent,w,h,css=''){ const c=document.createElement('canvas'); c.width=w; c.height=h; c.style.cssText='position:absolute;'+css; parent.appendChild(c); return c; }
const SCENES=[];
function scene(id,f0,f1,render,cls=''){ const s=document.createElement('div'); s.className='scene '+cls; s.id=id; $('stage').insertBefore(s,$('cursor')); const cam=el(s,'cam'); SCENES.push({id,f0,f1,render,el:s}); return {s,cam}; }
// dégradé vertical mélangé en lumière linéaire et tramé à ±1 (triangulaire) : pas de bandes sous x264
function ditherV(stops,h,seed){ const c=document.createElement('canvas'); c.width=8; c.height=h; const x=c.getContext('2d'), im=x.createImageData(8,h), R=rng(seed);
  const st=stops.map(([t,hx])=>[t,hex(hx).map(v=>Math.pow(v/255,2.2))]);
  for(let y=0;y<h;y++){ const t=y/(h-1); let k=0; while(k<st.length-2&&st[k+1][0]<t) k++; const [t0,a]=st[k], [t1,b]=st[k+1], u=clamp((t-t0)/(t1-t0));
    const lin=a.map((v,i)=>lerp(v,b[i],u)); for(let xx=0;xx<8;xx++){ const o=(y*8+xx)*4; lin.forEach((v,i)=>{ im.data[o+i]=clamp(Math.round(Math.pow(v,1/2.2)*255+(R()-R())),0,255); }); im.data[o+3]=255; } }
  x.putImageData(im,0,0); return c.toDataURL(); }
// derrière les écrans cadrés : le ciel de la fenêtre de Ship it (1251), chroma ramené à 12 au plus. Un ciel, un soleil.
const SKY_STOPS=[[0,'#ECE4DC'],[.25,'#F2E3D5'],[.45,'#F6E2D0'],[.6,'#F6E3D0'],[.75,'#E7DACC'],[.98,'#B3CAC9'],[1,'#B3CAC9']];
let SKY_URL=null;
function sky(parent){ SKY_URL=SKY_URL||ditherV(SKY_STOPS,1200,11); el(parent,'sky','',`background:url(${SKY_URL}) 0 0/100% 100%`); }
const push=(cam,f,f0,k=0.001)=>{ cam.style.transform=`scale(${(1+k*(f-f0)).toFixed(4)})`; };
const T=f=>f/FPS;

/* ---------- 1-3 · « Your SaaS is boring. » → caret rouge → « a bit » inséré ; puis l'éclatement de sites ---------- */
const W1=scene('sW',0,119,f=>shotW(f));
// la phrase vit dans l'espace écran (hors caméra) : la coupe de 62 ne change que ce qu'il y a derrière
const wWord=el(W1.s,'abs c word','', 'font-size:60px;z-index:30;text-shadow:0 0 24px rgba(238,233,228,.9)');
wWord.innerHTML='<span class="wa"></span><span class="wi" style="display:inline-block;overflow:hidden;vertical-align:bottom;white-space:pre"></span><span class="wb ar" style="color:var(--blue);font-weight:400"></span>';
const [wA,wI,wB2]=['.wa','.wi','.wb'].map(q=>wWord.querySelector(q));
// états de la phrase (réf : un mot par temps) ; « boring. » est le bleu Arial du fondateur
const WST=[[10,'Your',''],[17,'Your SaaS',''],[23,'Your SaaS is',''],[30,'Your SaaS is ','boring.'],[80,'is ','boring.'],[85,'','boring.'],[94,'','']];
const W_INS='a bit '; let W_INSW=128, W_GAP=[0,0];
function wLayout(){ show(W1.s,true); wA.textContent='Your SaaS is '; wB2.textContent='boring.'; wI.textContent=W_INS; wI.style.width='auto'; W_INSW=wI.offsetWidth;
  wI.textContent=''; wI.style.width='0px'; place(wWord,960,540); const ra=wA.getBoundingClientRect(), rb=wB2.getBoundingClientRect(), st=W1.s.getBoundingClientRect(), k=st.width/W;
  const isEnd=(ra.right-st.left)/k - 0.27*60/2;   // l'espace après « is »
  W_GAP=[(isEnd+(rb.left-st.left)/k)/2, (rb.bottom-st.top)/k]; show(W1.s,false); }
const wInk=inkLayer(W1.s);
const GACC='#FF3D5E', GLIL='#9C86FF', GINK='#151413', GBORN='#C9D9F6';
// Les glyphes s'accumulent jusqu'à 53 (comme dans la réf) ; les deux grands « / » s'écartent de part et d'autre de la phrase.
const GLY=[{ch:[[0,'/'],[24,'<']],pos:[[0,0,0],[8,-18,0],[13,-124,0],[19,-232,0],[30,-450,0]],col:GINK,born:0,big:1},
           {ch:[[8,'/'],[24,'>']],pos:[[8,18,0],[13,124,0],[19,232,0],[30,450,0]],col:GINK,born:8,big:1}];
(()=>{ const r=rng(7), ex=[]; [27,30,30,33,36,36,36,39,42,45,45,45,45,47,49,51,51,51,52,52].forEach(b=>{ let x,y,t=0;
  do{ x=(r()*2-1)*560; y=(r()*2-1)*330; t++; }while(t<500&&((Math.abs(x)<470&&Math.abs(y)<70)||x*x/(560*560)+y*y/(330*330)>1||ex.some(e=>Math.hypot(e[0]-x,e[1]-y)<74)));
  ex.push([x,y]); GLY.push({ch:[[b,['/','/','/','<','>','*','|','\\'][(r()*8)|0]]],pos:[[b,x,y]],col:GINK,born:b}); }); })();
// glyphes épars (prompt, outro) : encre seulement (loi des couleurs : pas de rouge que le stylo n'a pas posé)
function gset(n,seed,rx,ry){ const r=rng(seed), a=[]; let t=0; while(a.length<n&&t++<600){ const x=(r()*2-1)*rx, y=(r()*2-1)*ry; if(Math.abs(x)<70&&Math.abs(y)<46) continue; if(x*x/(rx*rx)+y*y/(ry*ry)>1) continue; if(a.some(g=>Math.hypot(g[1]-x,g[2]-y)<54)) continue;
  r(); a.push([['/','/','/','<','>','*','|','\\'][(r()*8)|0],x,y,GINK]); } return a; }
const wGly=GLY.map(g=>el(W1.cam,'abs c glyph','',g.big?'font-size:64px':''));
function gpos(g,f){ let i=0; for(let k=0;k<g.pos.length;k++) if(f>=g.pos[k][0]) i=k; const c=g.pos[i], p=i?g.pos[i-1]:c, t=approach(f,c[0],5); return [lerp(p[1],c[1],t),lerp(p[2],c[2],t)]; }
function gch(g,f){ let c=g.ch[0][1]; for(const k of g.ch) if(f>=k[0]) c=k[1]; return c; }
// fragments du CSS ennuyeux, dans le bleu du fondateur sur 3 profondeurs ; une grille de 24 px et pas de chevauchement
const FRAGS=['font-family: Arial;','color: #2D6CDF;','box-shadow: 0 6px 10px #000;','border-radius: 4px;','/* TODO: make it pop */','<h1>Welcome back, User!</h1>','lorem ipsum dolor sit','img: stock_handshake.jpg','.btn-primary { }','font-size: 12px;','!important','z-index: 9999;','<marquee>','cursor: pointer;','text-align: center;','Get Started Today!'];
const FRBOX=[]; function fragPos(t,seed,sz){ const r=rng(seed), w=t.length*sz*0.6, h=sz*1.3; let x,y,k=0;
  do{ x=40+Math.round(r()*(1840-w)/24)*24; y=72+Math.round(r()*900/24)*24; k++; }while(k<200&&((Math.abs(x+w/2-960)<w/2+520&&Math.abs(y-540)<100)||FRBOX.some(b=>x<b[2]+12&&x+w+12>b[0]&&y<b[3]+12&&y+h+12>b[1])));
  FRBOX.push([x,y,x+w,y+h]); return [x,y,r]; }
const wFr=FRAGS.map((t,i)=>{ const tier=i===4?0:i%3, sz=i===4?28:[34,30,26][tier]; const d=el(W1.cam,'abs frag','', `font-size:${sz}px`); d._t=t; const [x,y,r]=fragPos(t,500+i,sz); d._x=x; d._y=y; d._d=(r()*6)|0;
  d._tier=tier; d.style.filter=tier===1?'blur(1.2px)':tier===2?'blur(2.5px)':''; d.style.opacity=[1,.55,.3][tier]; d._ty=i%2; d._read=i===4; return d; });
// l'éclatement : onze sites recréés (js/sites.js), cinq en grand puis six qui rejoignent le collage
const BR=[[0,0],[1180,0],[0,587],[330,783],[1090,640]].map(([x,y],i)=>[x,y,SITES[i].w,SITES[i].h,i]);
const BCL=[[-200,-95,560,0],[210,-120,430,0],[-360,60,200,0],[-80,120,390,0],[260,95,470,0]];
const BDR=[[-50,-20],[40,-5],[-45,10],[35,40],[100,45]], BST=[84,89,90,89,91], BSW=[[110,0],[-90,1.3],[140,2.2],[-80,3.1],[120,4.4]];
const BXT=[5,6,7,8,9,10].map(i=>[i,SITES[i].w,SITES[i].h]);
const BXC=[[40,-30,300,-3,-1,-1],[-330,-180,270,4,-1,-1],[360,-10,300,-2,1,0],[-40,170,280,3,0,1],[150,-190,200,2,1,-1],[-260,150,240,-4,-1,1]];
const wCol=el(W1.cam,'abs','', 'inset:0;width:1920px;height:1080px'); let wColB=null;
const wB=BR.map(([x,y,w,h,si])=>{ const d=el(wCol,'bshot',SITES[si].html, `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0;background:${SITES[si].color}`); d._r=[x,y,w,h]; d._si=si; return d; });
const wX=BXT.map(([si,w,h])=>{ const d=el(wCol,'bshot',SITES[si].html, `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0;background:${SITES[si].color}`); d._w=w; d._h=h; d._si=si; return d; });
const ease3=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
[10,17,23,30].forEach((f,i)=>cue(f,'pluck',{n:[64,67,69,71][i],v:.3})); cue(8,'tick',{v:.4}); cue(37,'scratch',{v:.45,end:41}); [43,44,45,46,47].forEach(f=>cue(f,'tick',{v:.16}));
[27,33,36,42,49].forEach(f=>cue(f,'tick',{v:.2})); cue(53,'shimmer',{v:.3,end:61}); cue(104,'riser',{v:.4,end:119}); cue(62,'swish',{v:.45,peak:64,dur:6}); cue(89,'whoosh',{v:.4,peak:99,dur:14}); [64,66,67,70].forEach(f=>cue(f,'tick',{v:.2})); cue(96,'swish',{v:.45,peak:97,dur:4}); cue(104,'scratch',{v:.9,end:111}); cue(113,'tear',{v:.6,end:121}); cue(114,'reel',{v:.35,end:127});
function wState(f){ let st=['','']; for(const [wf,a,b] of WST) if(f>=wf) st=[a,b]; return st; }
function shotW(f){ push(W1.cam,f,0,0.0009);
  // la phrase
  const [ta,tb]=wState(f); show(wWord,!!(ta||tb)); const ins=f>=43&&f<85;
  wA.textContent=f>=80&&f<85?'is ':ta; wB2.textContent=tb;
  const k=approach(f,43,6,0.2); wI.textContent=ins?W_INS.slice(0,clamp(f-42,0,6)):''; wI.style.width=ins?(W_INSW*k).toFixed(1)+'px':'0px';
  if(f>=85) wI.style.width='0px';
  if(ta||tb) place(wWord,960,540);
  // M1 : le caret rouge sous l'espace entre « is » et « boring. » ; ses jambes rentrent dans la pointe pendant l'insertion
  const cx=inkClear(wInk);
  if(f>=37&&f<48){ const st=penPlace('G01',[W_GAP[0]-30,W_GAP[1]+2,W_GAP[0]+30,W_GAP[1]+62]); const r=approach(f,43,4,0.25);
    penDraw(cx,st,f,37,{size:5.5,u0:0.5*r,u1:1-0.5*r}); }
  const grow=f<45?1:f<51?1.2:1.35;
  GLY.forEach((g,i)=>{ const d=wGly[i]; const on=f>=g.born&&f<53; show(d,on); if(!on) return; let [x,y]=gpos(g,f);
    if(!g.big){ const r=rng(90+i*7+(f>=51?2:f>=45?1:0)); x=x*grow+(f>=45?(r()-0.5)*40:0); y=y*grow+(f>=45?(r()-0.5)*30:0); }
    const rot=i>=2&&i%2==1&&gch(g,f)!=='*'; d.textContent=rot?['/','|','\\','-'][(Math.floor(f/2)+i)%4]:gch(g,f);
    d.style.color=mixc(GBORN,GINK,approach(f,g.born,8));   // les glyphes naissent bleu pâle et sèchent à l'encre
    place(d,960+x,540+y,g.born===0?1:back(f,g.born-1,4)); });
  wFr.forEach((d,i)=>{ const st=53+d._d; const on=f>=st&&f<(d._read?86:(i<5?64:62)); show(d,on); if(!on) return;
    d.textContent=d._ty?d._t.slice(0,Math.max(3,(f-st+1)*2)):d._t; d.style.color=mixc(GBORN,'#2D6CDF',approach(f,st,4)); placeTL(d,d._x+(f-53)*0.6,d._y,back(f,st-1,4)); });
  // collage : accélère progressivement à partir de 89 (comme la réf) ; à 113 il se déchire le long du trait M2
  const g=1;
  const tinted=(f>=62&&f<70)||(f>=114&&f<117);   // les teintes de la réf, en camaïeu de la couleur de chaque site
  const sway=f<98?0:Math.sin(2*Math.PI*(f-98)/13.33);
  wB.forEach((d,i)=>{ if(f<62){ show(d,false); return; } show(d,true); const [x,y,w,h]=d._r, [cx,cy,cw]=BCL[i];
    const pc=ease3(clamp((f-BST[i])/18)), dr=approach(f,62,27,0.08);
    const s0=1+0.0012*(f-62), X=lerp(x+w/2+BDR[i][0]*dr,960+cx+BSW[i][0]*Math.sin(2*Math.PI*(f-98)/13.33+BSW[i][1])*(f>=98?1:0),pc), Y=lerp(y+h/2+BDR[i][1]*dr,540+cy,pc), S=lerp(s0,cw/w,pc);
    const Xg=960+(X-960)*g, Yg=540+(Y-540)*g, Sg=S*g; d.style.zIndex=f<104?i:f<108?(5-i):f<113?((i*3)%5):i;
    mblur(d,f>=84&&f<100?vel(t=>lerp(x+w/2,960+cx,ease3(clamp((t-BST[i])/18))),f)*BLUR*0.6:0,0);
    d.style.transform=`translate(${(Xg-w*Sg/2).toFixed(1)}px,${(Yg-h*Sg/2).toFixed(1)}px) scale(${Sg.toFixed(4)})`;
    d.style.boxShadow=pc>0?`0 ${(20*pc).toFixed(0)}px ${(50*pc).toFixed(0)}px -20px rgba(40,30,30,${(.35*pc).toFixed(2)})`:''; d.style.borderRadius=(10*pc)+'px';
    const bl=f>=116?` blur(${(accel(f,116,5,1.6)*18).toFixed(1)}px)`:''; d.style.filter=((tinted?DUO(d._si):'')+bl).trim(); });
  wX.forEach((d,i)=>{ const st=96+(i%2); if(f<st){ show(d,false); return; } show(d,true); const [cx,cy,cw,rot,ox,oy]=BXC[i]; const p=approach(f,st,10);
    const sx=(i%2?-1:1)*90*sway; const X=lerp(960+ox*1400+cx,960+cx+sx,p), Y=lerp(540+oy*900+cy,540+cy,p), S=cw/d._w; const Xg=960+(X-960)*g, Yg=540+(Y-540)*g, Sg=S*g; d.style.zIndex=10+((i+(f>=104)+(f>=108)*2)%6);
    d.style.transform=`translate(${(Xg-d._w*Sg/2).toFixed(1)}px,${(Yg-d._h*Sg/2).toFixed(1)}px) rotate(${rot}deg) scale(${Sg.toFixed(4)})`; d.style.borderRadius='10px'; d.style.boxShadow='0 20px 50px -20px rgba(40,30,30,.35)';
    mblur(d,vel(t=>lerp(960+ox*1400+cx,960+cx,approach(t,st,12)),f)*BLUR,vel(t=>lerp(540+oy*900+cy,540+cy,approach(t,st,12)),f)*BLUR);
    d.style.filter=(f>=114&&f<117?DUO(d._si):''); });
  // M2 : la barre oblique traverse toute la pile (104-111), la pile se déchire le long du trait (113-119)
  if(f>=104&&f<120){ const st=M2(); if(f<114) penDraw(cx,st,f,104,{size:13}); else slashThread(cx,f); }
  tear(f);
}
const M2=()=>penPlace('G02',[652,312,1262,770]);
// la droite du trait (moindres carrés sur ses extrémités) et la déchirure : deux moitiés qui glissent de ±60 px, tombent et s'effacent
function tear(f){ if(f<113){ if(wColB){ wColB.remove(); wColB=null; } wCol.style.clipPath=''; wCol.style.transform=''; wCol.style.opacity=''; return; }
  const st=M2().flat(), a=st[0], b=st[st.length-1]; const dx=b[0]-a[0], dy=b[1]-a[1], L=Math.hypot(dx,dy), ux=dx/L, uy=dy/L, nx=-uy, ny=ux;
  const far=4000, P=[a[0]-ux*far,a[1]-uy*far], Q=[b[0]+ux*far,b[1]+uy*far];
  const half=sg=>`polygon(${[P,Q,[Q[0]+nx*far*sg,Q[1]+ny*far*sg],[P[0]+nx*far*sg,P[1]+ny*far*sg]].map(p=>p[0].toFixed(0)+'px '+p[1].toFixed(0)+'px').join(',')})`;
  if(wColB) wColB.remove(); wColB=wCol.cloneNode(true); wCol.parentNode.appendChild(wColB);
  const k=clamp((f-113)/6), fall=k*k*80;
  [[wCol,1],[wColB,-1]].forEach(([c,sg])=>{ c.style.clipPath=half(sg); c.style.transform=`translate(${(nx*60*sg*k).toFixed(1)}px,${(ny*60*sg*k+fall).toFixed(1)}px)`; c.style.opacity=(1-k).toFixed(3); });
}
// le trait devient la barre du logo : il pivote sur 56,3° et raccourcit jusqu'à la fente de la marque (114-127), tête en premier
const LG_A=[943.5,564.75], LG_B=[976.5,515.25];
function slashThread(cx,f,col=null){ const base=penResample(M2().flat(),72); const t=clamp((f-114)/13); const N=base.length;
  const pts=base.map((p,i)=>{ const u=i/(N-1); const e=vladan(clamp((t-0.25*u)/0.75)); const tx=lerp(LG_B[0],LG_A[0],u), ty=lerp(LG_B[1],LG_A[1],u);
    return [lerp(p[0],tx,e),lerp(p[1],ty,e),lerp(p[2],.6,e),p[3]]; });
  penDraw(cx,[pts],1e6,0,{size:lerp(13,12.4,vladan(t)),uniform:vladan(t),color:col,wetFrames:0});
}

/* ---------- 4 · le trait devient la marque : disque rouge derrière la barre, fantôme du geste, puis « vladan » ---------- */
const L1=scene('sLogo',120,173,f=>shotLogo(f));
const lgGhost=inkLayer(L1.s,{ground:'dark'}); lgGhost.style.mixBlendMode='multiply';
const lgBlob=el(L1.cam,'abs','', 'overflow:hidden;border-radius:50%'); const lgG3=el(lgBlob,'full','', 'background:#FF3D5E');
const lgSlash=el(lgBlob,'full','<svg viewBox="0 0 96 96" width="100%" height="100%"><path d="M36 66 L60 30" stroke="#EEE9E4" stroke-width="9" stroke-linecap="round"/></svg>');
const lgInk=inkLayer(L1.s);
const lgWord=el(L1.cam,'abs','vladan','font-size:84px;font-weight:600;letter-spacing:-0.04em;line-height:1');
let LGW=330; function logoLayout(){ show(lgWord,true); LGW=lgWord.offsetWidth; show(lgWord,false); }
// le mot sort de la marque en 2-3 images, bord adouci ; il naît rose pâle et sèche à l'encre
function revealWord(d,f,f0){ const p=approach(f,f0,3), e=lerp(-15,118,p);
  d.style.webkitMaskImage=d.style.maskImage=p<1?`linear-gradient(90deg,#000 ${(e-14).toFixed(1)}%,transparent ${(e+14).toFixed(1)}%)`:'';
  d.style.background=''; d.style.webkitBackgroundClip=d.style.backgroundClip=''; d.style.color=mixc('#FFC2CD','#151413',approach(f,f0,8)); }
cue(120,'drop',{}); cue(132,'boom',{v:.95}); cue(139,'shimmer',{v:.45,end:147});
function shotLogo(f){ push(L1.cam,f,140,0.0007);
  const S=f<128?132*vl(f,119,9):f<137?132:lerp(132,81,vl(f,137,4));
  const ww=LGW, gap=24, tot=81+gap+ww, slide=vl(f,137,4);
  const x=lerp(960,960-tot/2+40.5,slide);
  show(lgBlob,S>0.5); Object.assign(lgBlob.style,{width:S+'px',height:S+'px'}); lgBlob.style.transform=`translate(${(x-S/2).toFixed(1)}px,${(540-S/2).toFixed(1)}px)`;
  // 120-127 : le trait finit de rentrer dans la fente ; la barre passe au papier quand le disque dépasse 60 %
  const ix=inkClear(lgInk); const crisp=f>=128; lgSlash.style.opacity=crisp?1:0;
  if(!crisp){ const paper=S>132*0.6; lgInk.style.mixBlendMode=paper?'normal':'multiply'; slashThread(ix,f,paper?'#EEE9E4':null); }
  // le geste d'origine, fantôme graphite à 7 % : main libre → marque nette
  const gx=inkClear(lgGhost); const ga=0.07*vl(f,124,6)*(1-vl(f,137,4)); if(ga>0.002){ lgGhost.style.display='block'; penDraw(gx,M2(),1e6,0,{size:13,color:`rgba(21,20,19,${(ga/0.07).toFixed(3)})`,alpha:0.07}); }
  show(lgWord,f>=139); if(f>=139){ placeTL(lgWord,x+40.5+gap,540-42,1+0.07*approach(f,139,16)); revealWord(lgWord,f,139); }
  L1.cam.style.translate=`0 ${(-12*accel(f,167,6,2)).toFixed(1)}px`;
}

/* ---------- 5-6 · le brief du fondateur : il survole « Envoyer » sans cliquer ; le stylo biffe « Arial, », la caméra plonge dans l'encre ---------- */
const P1=scene('sPrompt',174,227,f=>shotPrompt(f));
const prBox=el(P1.cam,'pbox','', 'left:450px;top:396px');
const prText=el(prBox,'ptext ar'); const prSend=el(prBox,'psend','<svg viewBox="0 0 72 72" width="72" height="72"><path d="M36 50 V22 M24 33 L36 21 L48 33" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>');
el(prBox,'picon','+','left:40px;bottom:26px');
el(prBox,'pctx m','⌁ velvetly.app · room planner for furniture brands','left:96px;bottom:24px');
el(prBox,'pmodel','vladan <svg viewBox="0 0 18 18" width="18" height="18"><path d="M4 7 L9 12 L14 7" stroke="#5C5650" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>','right:36px;bottom:22px');
const prInk=inkLayer(P1.cam);   // l'encre vit dans la caméra : elle colle au texte
const PROMPT='Make my SaaS less boring. It’s blue, it’s Arial, and there’s a stock handshake.';
// frappe : 36 caractères à 174, « handshake. » après 5 images de honte (le fondateur efface un « k » et le retape)
const PR_INC=[3,2,3,2,2, 2,3,2,2,3,2,2,2,2, 0,0,-1,0,1, 2,2,3,2,2];
const PR_N=(()=>{ const a=[36]; for(const k of PR_INC) a.push(a[a.length-1]+k); return a; })();
for(let i=0;i<PR_INC.length;i++) if(PR_INC[i]) cue(175+i,'key',{v:.2+Math.abs(PR_INC[i])*0.08});
const prGly=gset(12,33,640,250).map(g=>{ const d=el(P1.cam,'abs c glyph'); d._g=g; return d; });
cue(207,'scratch',{v:.8,end:212}); cue(212,'rub',{v:.7,peak:226,dur:16});
let PR_ARIAL=[0,0,0,0], PR_XH=15.6;
function prLayout(){ show(P1.s,true); prText.innerHTML=prSeg(PROMPT.length); const sp=prText.querySelector('.ari'), r=sp.getBoundingClientRect(), st=P1.s.getBoundingClientRect(), k=st.width/W;
  PR_ARIAL=[(r.left-st.left)/k,(r.top-st.top)/k,(r.right-st.left)/k,(r.bottom-st.top)/k]; show(P1.s,false); }
// le brief en segments : « blue » dans le bleu du fondateur, « Arial, » repérable pour le trait
function prSeg(n){ const t=PROMPT.slice(0,n); const iB=PROMPT.indexOf('blue'), iA=PROMPT.indexOf('Arial,');
  const seg=(a,b,cls)=>{ const x=t.slice(a,Math.min(b,n)); return x?(cls?`<span class="${cls}">${x}</span>`:x):''; };
  return seg(0,iB)+seg(iB,iB+4,'blu')+seg(iB+4,iA)+seg(iA,iA+6,'ari')+seg(iA+6,PROMPT.length); }
// la caméra : poussée lente, puis plongée exponentielle ×2,4/image dans le trait (219-227), l'origine glisse sur le centre du trait
function prCam(f){ const base=1+0.0008*(f-174), ty=-23*approach(f,174,20);
  const sp=M3().flat(), C=sp[Math.floor(sp.length*0.55)];
  let k=base, t=[960-960*base,540-540*base+ty];
  if(f>219){ const Z=Math.pow(2.4,f-219); k=base*Z; const sc=[t[0]+C[0]*base,t[1]+C[1]*base]; const m=clamp(Math.log(Z)/Math.log(30));
    const Cs=[lerp(sc[0],960,m),lerp(sc[1],540,m)]; t=[Cs[0]-C[0]*k,Cs[1]-C[1]*k]; }
  return {k,t}; }
const M3=()=>penPlace('G03',[PR_ARIAL[0]-6,PR_ARIAL[3]-PR_XH*0.5-7,PR_ARIAL[2]+10,0]);
function shotPrompt(f){
  const {k,t}=prCam(f); P1.cam.style.transformOrigin='0 0'; P1.cam.style.translate=''; P1.cam.style.transform=`translate(${t[0].toFixed(2)}px,${t[1].toFixed(2)}px) scale(${k.toFixed(5)})`;
  const n=Math.min(PROMPT.length,PR_N[clamp(f-174,0,PR_N.length-1)]); const done=n>=PROMPT.length;
  const blink=f>=189&&f<194?Math.floor((f-189)/1)%2==0:(!done||Math.floor(f/7)%2==0);
  prText.innerHTML=prSeg(n)+(blink&&f<207?'<span class="pcaret"></span>':'');
  // le curseur du fondateur : linéaire, sur deux images, jusqu'au bouton ; il devient une main et reste en survol. Pas de clic.
  const hov=f>=204; prSend.classList.toggle('hover',hov);
  const cf=twos(f,199), cp=clamp((cf-199)/5);
  const sx=450+1020-30-36, sy=396+30+36;   // centre du bouton dans la caméra
  const px=lerp(1290,sx-4,cp), py=lerp(640,sy+4,cp), scr=[t[0]+px*k,t[1]+py*k];
  cursor(scr[0],scr[1],0,f>=199,f>219?Math.min(k,60):1,hov?'hand':'arrow');
  prGly.forEach((d,i)=>{ const st=204+i; const on=f>=st&&f<224; show(d,on); if(!on) return; const g=d._g; const drift=1+(f-st)*0.012;
    d.textContent=i%2?['/','|','\\','-'][(Math.floor(f/2)+i)%4]:g[0]; d.style.color=mixc(GBORN,GINK,approach(f,st,6)); place(d,960+g[1]*drift,546+g[2]*drift,back(f,st,4)); });
  // M3 : le trait biffe « Arial, » (207-212) ; au-delà de ×3, le champ d'encre plein cadre prend le relais
  const ix=inkClear(prInk); const st=M3();
  if(f>=207&&k<3) penDraw(ix,st,f,207,{size:3.6});
  if(INK&&k>=3){ show(INK.canvas,true); P1.s.appendChild(INK.canvas); INK.draw({O:[(960-t[0])/k,(540-t[1])/k],Z:k,mode:0,wet:clamp(1-(f-212)/6)},inkSpine(st.flat(),3.6)); }
  else if(INK&&INK.canvas.parentNode===P1.s) show(INK.canvas,false);
}

/* ---------- 7 · la landing velvetly (vidéo Cycles), recul qui ralentit, accélération dans la coupe, « › Taste Files » ---------- */
const LA=scene('sLand',228,299,f=>shotLand(f)); sky(LA.cam);
const laFrame=el(LA.cam); const laD=framed(laFrame,tplVLanding(),1440,900,1240,730,VINK);
const laLabel=el(LA.cam,'abs','<span style="font-family:JB;margin-right:22px">›</span>Taste Files','font-size:84px;font-weight:400;color:#3A3633;letter-spacing:-0.01em');
const laSeq=q1(laD,'.vseq'), laPills=qa(laD,'.vpill'), laTiles=qa(laD,'.vtile');
const laShop=el(q1(laD,'.full'),'m','Live','position:absolute;top:688px;height:22px;line-height:22px;padding:0 10px;border-radius:6px;background:#151413;color:#F3EFEA;font-size:11px');
const PH_COL=['#3A3633','#4A4542','#2E2B28'];   // squelettes de chargement (gris), pas de couleurs
// l'icône du carré se dessine 234-238
qa(laD,'.vmk svg path').forEach(p=>{ p.setAttribute('pathLength','1'); p.style.strokeDasharray='1'; });
const laMark=q1(laD,'.vmk');
cue(234,'impact',{v:.5}); cue(244,'tick',{v:.25}); cue(256,'tick',{v:.25}); cue(259,'swish',{v:.25,peak:262,dur:6}); cue(276,'whoosh',{v:.5,peak:281,dur:6}); cue(281,'tick',{v:.45}); cue(294,'shimmer',{v:.35,end:300});
function laLayout(f){ // accordéon des tuiles (réf 259-270) : la tuile large passe à sa voisine
  const p=approach(f,259,11); const W=[236,lerp(236,330,p),236,lerp(250,156,p),236]; let x=12;
  laTiles.forEach((t,i)=>{ t.style.left=x+'px'; t.style.width=W[i]+'px'; x+=W[i]+8; });
  laShop.style.left=lerp(12+3*244+150-60,12+244+330-70,p).toFixed(1)+'px'; }
function shotLand(f){
  // 228-233 : l'encre de la plongée sèche à travers les fibres du papier ; la dernière qui reste est le carré de la landing
  const fl=Math.max(f,234);
  // réf : recul qui ralentit (235-273), accélération dans la coupe (274-280), puis petit écran qui se pose (281+)
  let sc,x=960,y=540;
  if(f<235) sc=1.08; else if(f<274) sc=lerp(1.08,0.915,approach(f,235,38,0.09));
  else if(f<281){ const a=accel(f,274,6.5,2.6); sc=lerp(0.915,0.823,a); x=960+40*a; }
  else { const p=approach(f,281,14,0.25); sc=lerp(0.683,0.632,p); x=1588-720*sc+lerp(16,0,p); y=548; }
  const gone=f>=294?approach(f,294,5):0;
  place(laFrame,x,y,sc); laFrame.style.filter=gone>0?`blur(${(10*gone).toFixed(1)}px) brightness(${(1+0.35*gone).toFixed(2)})`:''; laFrame.style.opacity=(1-0.85*clamp((f-297)/3)).toFixed(3);
  mblur(LA.cam,f>=276&&f<281?vel(t=>40*accel(t,274,6.5,2.6),f):0,0);
  seqDraw(laSeq,SEQ.land,fl-234);
  q1(laD,'.lnh').style.transform=`translateX(${(-290*approach(f,235,36,0.10)).toFixed(1)}px)`;
  qa(laMark,'svg path').forEach(p=>p.style.strokeDashoffset=(1-vl(f,234,4)).toFixed(3));
  if(INK&&f<234){ show(INK.canvas,true); LA.s.appendChild(INK.canvas); const r=laMark.getBoundingClientRect(), st=LA.s.getBoundingClientRect(), k=st.width/W;
    const cx=((r.left+r.right)/2-st.left)/k, cy=((r.top+r.bottom)/2-st.top)/k, hw=(r.right-r.left)/2/k, hh=(r.bottom-r.top)/2/k;
    const d=0.5-0.5*Math.cos(Math.PI*clamp((f-227.6)/5.8)); INK.draw({O:[960,540],Z:1,mode:1,dry:d,sig:70*Math.pow(2.5/70,d),rect:[cx,cy,hw,hh],rr:hw*0.52}); }
  else if(INK&&INK.canvas.parentNode===LA.s) show(INK.canvas,false);
  // boutons d'abord en blocs de couleur qui changent toutes les 4 images, puis le logo (244) et les boutons (256)
  // (les couleurs d'origine sont gardées : remettre style.color à '' effaçait le texte clair de « Book a demo »)
  laPills.forEach((pl,i)=>{ const ready=f>=(i==0?244:256); if(pl._c===undefined){ pl._c=pl.style.color; pl._b=pl.style.background; }
    pl.style.color=ready?pl._c:'transparent'; pl.style.background=ready?pl._b:PH_COL[(Math.floor((fl-234)/4)+i)%3];
    pl.querySelectorAll('span').forEach(sp=>sp.style.visibility=ready?'visible':'hidden'); });
  q1(laD,'.full>.m').style.visibility=f>=242?'visible':'hidden';
  laLayout(f);
  show(laLabel,f>=281); if(f>=281) placeTL(laLabel,150,300-10*approach(f,281,12));
}

/* ---------- 8 · l'arborescence « Taste Files » : défilement par paliers, couleurs qui passent cyan → lilas → pêche → gris ---------- */
const TR=scene('sTree',300,347,f=>shotTree(f));
const TREE=[[300,'▾ Taste Files',150,0,'title'],[305,'Brand.ts',380,1,'file'],[308,'Typography.ts',380,2,'file'],[312,'Components',380,3,'dir'],
  [317,'NoMoreArial.tsx',610,4,'file'],[320,'OneAccent.tsx',610,5,'file'],[322,'EaseOut.tsx',610,6,'file'],[329,'Taste.tsx',840,7,'last']];
// chaque nom arrive en faisant ce qu'il dit : NoMoreArial change de police lettre à lettre, OneAccent sèche à l'encre,
// EaseOut arrive sur la courbe vladan (+ son tracé) ; les autres se posent à l'encre
const glyphs=t=>[...t].map(c=>`<span class="g">${c}</span>`).join('');
const trEls=TREE.map(([f0,t,x,row,kind])=>{ const d=el(TR.cam,'titem'); d._k=kind; d._x=x; d._row=row; d._f=f0; d._t=t;
  d.innerHTML=kind==='title'?`<span style="font-family:JB;margin-right:16px">▾</span>Taste Files`:kind==='dir'?`<span class="chev" style="font-family:JB;display:inline-block;margin-right:16px">›</span>${t}`
    :kind==='last'?`<span class="fi"></span><em style="font-size:82px">Taste</em>.tsx`:`<span class="fi"></span>${/NoMoreArial|EaseOut/.test(t)?glyphs(t):t}`;
  Object.assign(d.style,{fontSize:kind==='title'?'84px':kind==='last'?'84px':'72px',color:'#151413'}); if(kind==='title') d.style.color='#3A3633'; return d; });
const trEase=el(TR.cam,'abs','', 'display:flex;align-items:center;gap:18px'); 
trEase.innerHTML=`<svg width="120" height="44" viewBox="0 0 120 44"><path d="M2 42 ${Array.from({length:41},(_,i)=>`L${(2+i*2.9).toFixed(1)} ${(42-40*vladan(i/40)).toFixed(1)}`).join(' ')}" fill="none" stroke="#151413" stroke-width="1.75" stroke-linecap="round"/></svg><span class="m" style="font-size:22px;color:#151413">ease: vladan</span>`;
const trLines=[[360,1,3],[590,4,6]].map(([x,a,b])=>{ const l=el(TR.cam,'tline'); l._x=x; l._a=a; l._b=b; return l; });
TREE.forEach(([f0],i)=>cue(f0,i==TREE.length-1?'pluck':'tick',{v:i==TREE.length-1?.5:.3,n:79}));
const TR_STEPS=[[305,232],[312,219],[317,175],[322,149],[329,107]];
function trY(f){ let y=313; for(const [s,t] of TR_STEPS) y=lerp(y,t,approach(f,s,s==329?9:4,0.3)); return y; }
function shotTree(f){
  // pas de push continu : on tient, puis recul + léger roulis avant la coupe (340-346)
  const pb=accel(f,339,7,2.2); TR.cam.style.transform=`scale(${(1-0.025*pb).toFixed(4)}) rotate(${(1.2*pb).toFixed(3)}deg)`;
  const ty=trY(f), LH=100;
  trEls.forEach(d=>{ const on=f>=d._f; show(d,on); if(!on) return;
    placeTL(d,d._x,ty+d._row*LH+(d._row?14:0));
    const a=f-d._f;
    if(/NoMoreArial/.test(d._t)) qa(d,'.g').forEach((g,i)=>{ g.style.fontFamily=a>=4+i?'ID':'AR'; });
    else if(/OneAccent/.test(d._t)) d.style.color=a<3?'rgba(21,20,19,.25)':mixc('#C5C0BB','#151413',clamp((a-3)/4));
    else if(/EaseOut/.test(d._t)) qa(d,'.g').forEach((g,i)=>{ const dx=[18,10,5,2,1,0][Math.min(5,Math.max(0,a-i))]; g.style.display='inline-block'; g.style.transform=`translateX(${dx}px)`; g.style.opacity=a>=i?1:0; });
    if(d._k==='dir'){ const ch=q1(d,'.chev'); ch.style.transform=`rotate(${(90*approach(f,317,4)).toFixed(1)}deg)`; } });
  const eo=trEls[6]; show(trEase,f>=325); if(f>=325){ placeTL(trEase,eo._x+eo.offsetWidth+40,ty+6*LH+14+14); trEase.style.opacity=vl(f,325,4).toFixed(3); }
  trLines.forEach(l=>{ const on=f>=TREE[l._a][0]; show(l,on); if(!on) return; const last=Math.max(...TREE.filter(t=>t[3]>=l._a&&t[3]<=l._b&&f>=t[0]).map(t=>t[3]));
    Object.assign(l.style,{left:l._x+'px',top:(ty+(l._a-0.25)*LH+14)+'px',height:((last-l._a+0.7)*LH)+'px'}); });
}

/* ---------- 9 · « Build your Room » : arrive en mouvement, se remplit vite, dérive, puis accélère vers le point ---------- */
const cR9=cueAt(1);
const DA=scene('sDash',348,380,f=>shotDash(f)); sky(DA.cam);
const daFrame=el(DA.cam); const daD=framed(daFrame,tplVRoom(),1440,900,1240,730,'#F2EDE6');
const daPw=qa(daD,'.pw'), daPf=qa(daD,'.pf path,.pf rect,.pf circle'), daRoute=q1(daD,'.vroute'), daDot=q1(daD,'.vdot'), daFi=qa(daD,'.vside > *'), daTx=qa(daD,'.vplan text'), daPlan=q1(daD,'.vplan');
daPw.forEach(p=>{ p.style.strokeDasharray='1'; });
daPf.forEach(p=>{ p.style.transformBox='fill-box'; p.style.transformOrigin='50% 50%'; });
DA.cam.style.transformOrigin='1383px 563px';   // le point du plan à l'écran : la poussée finale va vers lui (raccord avec l'aérien)
cR9(347,'impact',{v:.55}); cR9(350,'swish',{v:.3,peak:353,dur:6}); for(let k=0;k<5;k++) cR9(352+k*2,'tick',{v:.2}); cR9(358,'shimmer',{v:.3,end:366}); cR9(362,'pop',{v:.4,n:84}); cR9(374,'whoosh',{v:.5,peak:379,dur:6});
function shotDash(F){ const f=F-1;   // numéros de la réf (REMAP +1)
  const arr=approach(f,347,15,0.2); place(daFrame,960-100*(1-arr)-(f-362>0?(f-362)*1:0),540);
  daPlan.style.transform=`translateX(${(80*(1-arr)).toFixed(1)}px)`; daPlan.style.filter=`saturate(${lerp(0.4,1,approach(f,348,13)).toFixed(3)})`;
  daFi.forEach((d,i)=>{ const p=approach(f,348+i*0.6,5); d.style.opacity=p.toFixed(3); d.style.transform=`translateY(${((1-p)*12).toFixed(1)}px)`; });
  daPw.forEach((p,i)=>{ p.style.strokeDashoffset=(1-approach(f,348+i,8)).toFixed(4); });
  daPf.forEach((p,i)=>{ const k=back(f,351+i*1.0,5); p.style.transform=`scale(${k.toFixed(3)})`; p.style.opacity=clamp(k*2).toFixed(2); });
  daTx.forEach((t,i)=>{ t.style.opacity=approach(f,354+i,4).toFixed(2); });
  daRoute.setAttribute('stroke-dashoffset',(1-approach(f,352,10)).toFixed(4));
  daDot.style.transform=`scale(${back(f,360,5).toFixed(3)})`;
  // poussée qui accélère dans la coupe : +0,1 · +0,5 · +1 · +3 %/image (375-378)
  DA.cam.style.transform=`scale(${(1+0.046*accel(f,374,4,3.2)).toFixed(4)})`;
}

/* ---------- 10 · le salon en vol plongeant (séquence Cycles) : tracé, point et plan au sol accrochés à l'image ---------- */
const cR10=cueAt(1);
const HE=scene('sHero',381,419,f=>shotHero(f));
const heSeq=canvas(HE.cam,1280,720,'left:0;top:0;width:1920px;height:1080px');
const heSvg=el(HE.cam,'',`<svg width="1920" height="1080" viewBox="0 0 1920 1080"><g class="hplan" fill="none" stroke="#F3EFEA" stroke-width="1.5"></g><g class="htick" stroke="#F3EFEA" stroke-width="1.5" fill="none"></g>
  <path class="hers" fill="none" stroke="rgba(21,20,19,.35)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" style="filter:blur(8px)"/><path class="her" fill="none" stroke="#151413" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle class="hp1" r="14" fill="none" stroke="#F3EFEA" stroke-width="2"/><circle class="hp2" r="14" fill="none" stroke="#F3EFEA" stroke-width="2"/>
  <text class="hlab" font-family="JB" font-size="15" fill="#F3EFEA">83 × 57 cm</text></svg>`,'position:absolute;left:0;top:0');
const hePlan=q1(heSvg,'.hplan'), heRoute=q1(heSvg,'.her'), heRouteS=q1(heSvg,'.hers'), heTick=q1(heSvg,'.htick'), heLab=q1(heSvg,'.hlab'), heP=[q1(heSvg,'.hp1'),q1(heSvg,'.hp2')];
const HE_SH=['rug','sofa','pouf','table','plant','chair'];
const heShapes=HE_SH.map(()=>{ const p=document.createElementNS('http://www.w3.org/2000/svg','path'); hePlan.appendChild(p); return p; });
el(HE.cam,'','', 'position:absolute;left:-100px;right:-100px;top:-60px;height:390px;backdrop-filter:blur(12px);-webkit-mask-image:linear-gradient(#000 40%,transparent);mask-image:linear-gradient(#000 40%,transparent)');
el(HE.cam,'','', 'position:absolute;left:-100px;right:-100px;bottom:-60px;height:330px;backdrop-filter:blur(12px);-webkit-mask-image:linear-gradient(transparent,#000 60%);mask-image:linear-gradient(transparent,#000 60%)');
const heDot=el(HE.cam,'vdot','', 'width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:15px;box-shadow:0 0 0 7px #fff,0 6px 18px rgba(0,0,0,.3)');
cR10(380,'impact',{v:.6}); cR10(384,'shimmer',{v:.3,end:400});
const pth=pts=>'M'+pts.map(([x,y])=>`${(x*1920).toFixed(1)} ${(y*1080).toFixed(1)}`).join(' L');
function shotHero(F){ const f=F-1, i=clamp(f-380,0,38);
  // la réf : sursaut d'entrée (+3,3 · +2,1 · +1,7 · +1 %), puis le vol du drone (rendu)
  HE.cam.style.transform=`scale(${(1.08-0.08*approach(f,380,6,0.3)).toFixed(4)})`;
  seqDraw(heSeq,SEQ.aerial,i);
  const P=AERIAL[i]; if(!P) return;
  heRoute.setAttribute('d',pth(P.route)); heRouteS.setAttribute('d',pth(P.route));
  let tk='';
  HE_SH.forEach((k,j)=>{ heShapes[j].setAttribute('d',pth(P[k])+' Z'); const o=vl(f,383+j*2,6); heShapes[j].style.opacity=o.toFixed(3);
    // équerres de 10 px aux coins de la boîte englobante
    if(o>0.5){ const xs=P[k].map(p=>p[0]*1920), ys=P[k].map(p=>p[1]*1080); const a=Math.min(...xs), b=Math.max(...xs), c=Math.min(...ys), d=Math.max(...ys);
      tk+=`M${a} ${c+10}V${c}H${a+10} M${b-10} ${c}H${b}V${c+10} M${b} ${d-10}V${d}H${b-10} M${a+10} ${d}H${a}V${d-10} `;
      if(k==='chair'){ heLab.setAttribute('x',(b+12).toFixed(0)); heLab.setAttribute('y',(c+16).toFixed(0)); } } });
  heTick.innerHTML=`<path d="${tk}"/>`; heLab.style.opacity=vl(f,394,5).toFixed(3);
  const d=P.route[P.route.length-1]; heDot.style.left=(d[0]*1920)+'px'; heDot.style.top=(d[1]*1080)+'px';
  heP.forEach((c,j)=>{ const ph=((f-381)/14+j*0.5)%1; c.setAttribute('cx',d[0]*1920); c.setAttribute('cy',d[1]*1080); c.setAttribute('r',(14+20*ph).toFixed(1)); c.style.opacity=((1-ph)*0.8).toFixed(3); });
}

/* ---------- 11 · pills « Lemme give it · fauteuil · taste » : couleurs à l'arrivée, resserrage décalé, fonte sur place ---------- */
const cR11=cueAt(2);
const PI=scene('sPills',420,467,f=>shotPills(f));
const piL=el(PI.cam,'pill','Lemme give it'), piR=el(PI.cam,'pill acc','<em>taste</em>'), piI=el(PI.cam,'picn','');
const piMelt=el(PI.cam,'','', 'position:absolute;left:0;top:467px;height:146px;border-radius:73px;background:#FFC2CD;filter:blur(14px);display:none');
// ce que vend Vladan, dans la fente de l'icône : marque (Aa), interface (panneaux), mouvement ; puis la fente se remplit d'encre avec la barre de la marque
const PI_ICO=[c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>`,
  c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`,
  c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h3l3-8 6 16 3-8h3"/></svg>`,
  c=>`<svg viewBox="0 0 96 96" width="60" height="60"><path d="M36 66 L60 30" stroke="${c}" stroke-width="9" stroke-linecap="round"/></svg>`];
let PIL={};
function pillsLayout(){ const wl=piL.offsetWidth, wr=piR.offsetWidth, ic=90; const sp=69, tg=4;
  const t1=wl+ic+wr+2*sp, t2=wl+ic+wr+2*tg;
  PIL={wl,wr, l1:960-t1/2+wl/2, i1:960-t1/2+wl+sp+ic/2, r1:960+t1/2-wr/2, l2:960-t2/2+wl/2, i2:960-t2/2+wl+tg+ic/2, r2:960+t2/2-wr/2}; }
cR11(418,'pop',{v:.55,n:72}); cR11(424,'swish',{v:.4,peak:426,dur:6}); cR11(430,'pop',{v:.6,n:77}); cR11(444,'tick',{v:.4}); cR11(451,'swish',{v:.3,peak:454,dur:6}); cR11(460,'whoosh',{v:.9,peak:465,dur:8});
// couleur d'arrivée : jaune pâle / pêche → orange → encre en 8 images
const arrive=(f,f0,from)=>{ const a=f-f0; return a<0?from:a<3?mixc(from,'#FF9A4D',a/3):mixc('#FF9A4D','#151413',clamp((a-3)/5)); };
function shotPills(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  push(PI.cam,f,418,0.0009); const L=PIL;
  // resserrage décalé : pill gauche +73 px (444-447), icône pleine (446), pill droite −73 px (451-456), le groupe se recentre −15 px (455-459)
  const gl=approach(f,444,4,0.3), gr=approach(f,451,6,0.3), rc=-15*approach(f,455,5,0.3);
  const xl=L.l1+(L.l2-L.l1)*gl+rc, xr=L.r1+(L.r2-L.r1)*gr+rc, xi=L.i1+(L.i2-L.i1)*(0.5*gl+0.5*gr)+rc;
  // la fonte : un front flou rose → orange → jaune part du bord gauche (≈190 px/image) et avale pill, icône, pill (460-466)
  const melt=f>=460, x0=xl-L.wl/2-30, front=melt?x0+(f-460)*190:-1e4;
  show(piI,true); const filled=f>=446; piI.style.background=filled?'#151413':'#EEE9E4';
  const ic=(f>=427)+(f>=436)+(f>=446); piI.innerHTML=`<div style="position:absolute;inset:0;display:grid;place-items:center">${PI_ICO[ic](filled?'#EEE9E4':'#151413')}</div>`;
  place(piI,xi,540,back(f,418,4)); piI.style.borderColor='#151413';
  show(piL,f>=424); piL.style.opacity=approach(f,424,3).toFixed(3); place(piL,xl,540); piL.style.color=piL.style.borderColor='#151413';
  show(piR,f>=430); place(piR,xr,540,back(f,430,6));
  [[piL,xl-L.wl/2],[piI,xi-45],[piR,xr-L.wr/2]].forEach(([e,left])=>{ const k=front-left; e.style.webkitMaskImage=e.style.maskImage=melt?`linear-gradient(90deg,transparent ${k.toFixed(0)}px,#000 ${(k+60).toFixed(0)}px)`:''; });
  show(piMelt,melt); if(melt){ piMelt.style.left=x0+'px'; piMelt.style.width=Math.max(146,front-x0+40)+'px'; }
}

/* ---------- 12-13 · barres floues → « Delivery & Install Status » → une seule poussée sur les 3 recadrages ---------- */
const cR12=cueAt(2);
const PL=scene('sPlan',468,560,f=>shotPlan(f));
const plRoot=el(PL.cam,'','', 'position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0'); plRoot.innerHTML=tplPlan();
const plChips=qa(plRoot,'.pchip'), plDays=qa(plRoot,'.day'), plDn=qa(plRoot,'.dname'), plCols=qa(plRoot,'.col'), plSide=q1(plRoot,'.side'), plTitle=[q1(plRoot,'.ptitle'),q1(plRoot,'.psub')], plX=qa(plRoot,'.plx');
// vague 1 : grosses barres floues (≈140 px), qui poussent vers la droite puis se rattrapent et s'éteignent (réf 466-480)
// barres floues nées dans des teintes du bleu du fondateur, qui sèchent en teintes d'encre (488-500)
const PL_BLUE=['#C6D8F7','#A9C4F2','#D9E5FA','#B8CEF4','#CBDCF8','#9DBBEF'], PL_INK=[.06,.10,.16,.08,.12,.10];
const PL_BARS=[[466,467],[466,180],[470,720],[472,300],[474,610],[474,850]].map(([st,y],i)=>{ const c=PL_BLUE[i]; const d=el(PL.cam,'','', `position:absolute;top:${y}px;height:${138+(i%3)*4}px;border-radius:70px;background:${c};filter:blur(14px);display:none`); const r=rng(810+i); d._st=st; d._i=i; d._x=i==0?600:80+r()*900; d._g=25+r()*65; d._c=100+r()*70; return d; });
plChips.forEach((c,i)=>{ c._st=504+i*1.3; c._x0=parseFloat(c.style.left); c._y0=parseFloat(c.style.top); });
const plInk=inkLayer(plRoot);
// M4 : le S d'inversion relie « Ship » (lundi) et « Taste Check » (vendredi) ; chacun part sur un lobe du S (523-529)
const PL_SHIP=plChips[0], PL_TC=plChips[4];
const M4=()=>penPlace('G04',[PL_SHIP._x0+150,PL_SHIP._y0+20,PL_TC._x0+40,PL_TC._y0+52],{mode:'stretch'});
cR12(514,'scratch',{v:.8,end:521}); cR12(523,'glide',{v:.4,end:529});
for(let k=0;k<7;k++) cR12(494+k*2.4,'tick',{v:.2}); PL_BARS.forEach(b=>cR12(b._st,'swish',{v:.18,peak:b._st+3,dur:6}));
cR12(532,'impact',{v:.45}); cR12(541,'swish',{v:.35,peak:542,dur:5}); cR12(550,'swish',{v:.35,peak:551,dur:5}); cR12(555,'whoosh',{v:.4,peak:559,dur:5});
function shotPlan(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // zooms 532-558 : UNE poussée qui ralentit à travers les 3 coupes ; la puce grandit à la fin (raccord téléphone)
  let zs=1, zx=960, zy=540; if(f>=532){ const Z=[[532,760,470],[541,1280,560],[550,960,770]]; let z=Z[0]; for(const q of Z) if(f>=q[0]) z=q;
    zs=2.15*(1+0.032*approach(f,532,27,0.09)); zx=z[1]; zy=z[2]; }
  plRoot.style.transform=`translate(${(960-zx*zs).toFixed(1)}px,${(540-zy*zs).toFixed(1)}px) scale(${zs})`;
  // caméra : recul qui ralentit (499-516), puis parfaitement immobile jusqu'à la coupe
  PL.cam.style.transform=f<532?`scale(${(1.04-0.04*approach(f,499,17,0.1)).toFixed(4)})`:'';
  plRoot.firstChild.style.background=mixc('#EEE9E4','#F6F2EE',approach(f,490,16));
  PL_BARS.forEach(b=>{ const a=f-b._st; const on=a>=0&&a<14&&f<532; show(b,on); if(!on) return; const grow=Math.min(a,5)*b._g, tail=Math.max(0,a-5)*b._c;
    const dr=vladan(clamp((f-488)/12)); b.style.background=dr>0?`rgba(${hex(PL_BLUE[b._i]).map(v=>Math.round(lerp(v,21,dr))).join(',')},${lerp(1,PL_INK[b._i]*4,dr).toFixed(3)})`:PL_BLUE[b._i];
    b.style.left=(b._x+tail)+'px'; b.style.width=Math.max(10,180+grow-tail)+'px'; b.style.opacity=(1-clamp((a-8)/6)).toFixed(3); });
  plChips.forEach((c,i)=>{ const blob=f>=486+(i%6)*1.4, sharp=approach(f,c._st,3,0.3);
    c.style.visibility=blob?'visible':'hidden'; c.style.transform=f>=555&&i==3?`scaleY(${(1+0.4*accel(f,555,4,2)).toFixed(3)})`:''; if(i==3) c.style.transformOrigin='50% 0';
    c.style.filter=sharp<1?`blur(${(14*(1-sharp)).toFixed(1)}px)`:''; c.firstChild.style.opacity=c.lastChild.style.opacity=sharp.toFixed(2); });
  // l'inversion : « Taste Check » prend le lobe du haut vers lundi, « Ship » le lobe du bas vers vendredi ; l'encre de chaque lobe se rétracte derrière sa puce
  const sw=vl(f,523,6); const sx=PL_TC._x0-PL_SHIP._x0, sy=PL_TC._y0-PL_SHIP._y0;
  [[PL_TC,-1,-140],[PL_SHIP,1,140]].forEach(([c,dir,bow])=>{ const u=sw; const dx=-dir*sx*u*-1, dy=dir*sy*u*-1;
    const ox=dir>0?sx*u:-sx*u, oy=(dir>0?sy:-sy)*u+bow*Math.sin(Math.PI*u)*(dir>0?1:-1)*0.5; c.style.translate=`${ox.toFixed(1)}px ${oy.toFixed(1)}px`; c.style.zIndex=u>0?5:''; });
  const ix=inkClear(plInk); if(f>=514&&f<530){ const r=vl(f,523,6); penDraw(ix,M4(),f,514,{size:5,u0:0.5*r,u1:1-0.5*r}); }
  plDays.forEach((d,i)=>{ const st=494+i*2.4; d.style.visibility=f>=st?'visible':'hidden'; d.style.color=f<st+4?mixc('#C6D8F7','#151413',clamp((f-st)/4)):(i>=5?'#B3ABA4':'#151413'); });
  plDn.forEach((d,i)=>{ d.style.visibility=f>=497+i*2.4?'visible':'hidden'; });
  plCols.forEach((c,i)=>{ c.style.transformOrigin='0 0'; c.style.transform=`scaleY(${approach(f,488+i,10).toFixed(3)})`; });
  show(plSide,f>=498); plSide.style.background=mixc('#3A3633','#151413',approach(f,498,14));
  [...plSide.children].forEach(e=>{ e.style.opacity=approach(f,505,6).toFixed(2); });
  plTitle.forEach((t,i)=>{ t.style.visibility=f>=506+i*2?'visible':'hidden'; if(i==0) t.style.color=mixc('#C5C0BB','#3A3633',approach(f,506,10)); });
  plX.forEach((t,i)=>{ t.style.visibility=f>=508+i?'visible':'hidden'; });
}

/* ---------- 14 · téléphone : se déplie en hauteur, écran irisé balayé par le bas, vidéo en grue, rubans plein cadre ---------- */
const cR14=cueAt(2);
const PH=scene('sPhone',561,641,f=>shotPhone(f));
// le téléphone : anneau de métal, île, boutons, reflet du verre qui glisse, ombre de contact ; l'app velvetly AR démarre comme une caméra
const phShadow=el(PH.cam,'','', 'position:absolute;left:820px;top:952px;width:280px;height:18px;border-radius:50%;background:radial-gradient(closest-side,rgba(40,30,30,.45),rgba(40,30,30,0))');
const phone=el(PH.cam,'phone'); el(phone,'ring'); [[-6,210,60],[-6,290,60],[408,250,96]].forEach(([x,y,h])=>el(phone,'pbtn','', `left:${x}px;top:${y}px;height:${h}px`));
const phScr=el(phone,'scr');
const phSeq=canvas(phScr,612,1260,'left:0;top:0;width:384px;height:816px');
el(phScr,'','', 'position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 48%,rgba(10,9,8,.86) 78%)');
el(phScr,'island');
el(phScr,'glass',`${VMARK(18)}<span style="margin-left:8px">velvetly AR</span>`,'position:absolute;left:22px;top:58px;height:38px;line-height:38px;padding:0 14px;border-radius:12px;color:#fff;font-size:15px;display:flex;align-items:center');
el(phScr,'abs','Living room','left:24px;top:108px;font-size:46px;color:#fff;letter-spacing:-0.04em');
el(phScr,'abs m','▪ ROOM FIT','left:26px;top:478px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)');
const phNum=el(phScr,'abs','92%','left:22px;top:498px;font-size:104px;color:#fff;letter-spacing:-0.05em;line-height:1');
el(phScr,'abs m','▪ TIME TO FIRST ROOM','left:26px;top:612px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)');
const phTime=el(phScr,'abs','2:59','left:22px;top:632px;font-size:58px;color:#fff;letter-spacing:-0.04em;line-height:1');
el(phScr,'abs m','chair 0.83 m · sofa 2.19 m','left:26px;top:700px;font-size:12px;color:rgba(255,255,255,.55)');
el(phScr,'','Share this room →','position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#151413;box-shadow:inset 0 0 0 1px rgba(243,239,234,.2);color:#F3EFEA;font-size:20px;line-height:62px;padding-left:22px');
const phSheen=el(phScr,'','', 'position:absolute;left:-120px;top:-40px;width:160px;height:900px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.10),rgba(255,255,255,0));transform:rotate(18deg)');
const phDone=el(phScr,'','', 'position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,rgba(18,17,16,0),#121110 26%)');
phDone.innerHTML=`<div style="position:absolute;left:24px;top:96px;width:44px;height:44px;border-radius:12px;background:#F3EFEA;color:#151413;font-size:26px;line-height:44px;text-align:center">✓</div>
  <div style="position:absolute;left:24px;top:156px;font-size:54px;color:#fff;letter-spacing:-0.045em;line-height:.98">Fits<br>perfectly</div>
  <div class="m" style="position:absolute;left:26px;top:280px;font-size:12px;color:#8E877F">sofa 2.19 m · chair 0.83 m · 24 m²</div>
  <div style="position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#F3EFEA;color:#151413;font-size:20px;line-height:62px;text-align:center">Share this room →</div>`;
cR14(559,'impact',{v:.55}); cR14(566,'shimmer',{v:.35,end:578}); [588,603].forEach(f=>cR14(f,'tick',{v:.3})); cR14(606,'swish',{v:.45,peak:609,dur:8}); cR14(608,'pop',{v:.5,n:84});
function shotPhone(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // dépli en hauteur seulement (478 → 861 px), largeur fixe ; pas de poussée ensuite
  place(phone,960,540,1,0,1); phone.style.transform+=` scaleY(${lerp(0.555,1,approach(f,559,13,0.25)).toFixed(4)})`;
  seqDraw(phSeq,SEQ.phone,f-559);
  // démarrage d'une caméra AR : la mise au point cherche (22 → 0 → 4 → 0 px) et l'exposition se pose (+0,6 IL → 0), en 6 images
  const b=f<561?22:f<563?lerp(22,0,(f-561)/2):f<565?lerp(0,4,(f-563)/2):f<567?lerp(4,0,(f-565)/2):0, ev=0.6*(1-vl(f,561,6));
  phSeq.style.filter=(b>0.05?`blur(${b.toFixed(1)}px) `:'')+(ev>0.01?`brightness(${Math.pow(2,ev).toFixed(3)})`:'');
  phNum.textContent=Math.round(lerp(92,98,clamp((f-573)/30)))+'%';
  const secs=Math.round(lerp(179,42,vladan(clamp((f-580)/25)))); phTime.textContent=`${Math.floor(secs/60)}:${String(secs%60).padStart(2,'0')}`;
  phSheen.style.translate=`${(140*clamp((f-559)/80)).toFixed(1)}px 0`;
  const dp=approach(f,606,10); phDone.style.transform=`translateY(${((1-dp)*440).toFixed(1)}px)`;
}

/* ---------- 15-16 · l'avant/après : la v1 exacte du fondateur, deux marques au stylo, puis la v2 en une vague ; gros plan de la barre d'outils ---------- */
const CL=scene('sClients',642,694,f=>shotClients(f)); sky(CL.cam);
const LU={branch:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/><path d="M6 9v6M18 9a9 9 0 0 1-9 9"/>',activity:'<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
  terminal:'<path d="M4 17l6-6-6-6M12 19h8"/>',code:'<path d="M10 9l-3 3 3 3M14 15l3-3-3-3"/><rect x="3" y="3" width="18" height="18" rx="2"/>'};
const lu=(k,sz,c='#151413',w=2)=>`<svg viewBox="0 0 24 24" width="${sz}" height="${sz}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round">${LU[k]}</svg>`;
const clCard=el(CL.cam,'','', 'position:absolute;left:0;top:0;width:1400px;height:880px;border-radius:18px;overflow:hidden;background:#F7F4F0;box-shadow:0 50px 100px -40px rgba(40,30,30,.5)');
clCard.innerHTML=`<div style="position:absolute;left:0;right:0;top:0;height:60px;background:#ECE8E3;box-shadow:0 1px 0 #DDD6CE">
  ${[0,1,2].map(i=>`<span style="position:absolute;left:${22+i*22}px;top:24px;width:12px;height:12px;border-radius:6px;background:#CFC8C0"></span>`).join('')}
  <div class="m" style="position:absolute;left:520px;top:14px;width:360px;height:32px;border-radius:9px;background:#F7F4F0;font-size:14px;line-height:32px;text-align:center;color:#5C5650">velvetly.app/overview</div>
  <div style="position:absolute;right:120px;top:16px;display:flex;gap:26px">${['branch','activity','terminal','code'].map(k=>lu(k,26)).join('')}</div>
  <div style="position:absolute;right:16px;top:12px;height:36px;line-height:36px;padding:0 16px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #DDD6CE;font-size:15px">Share</div></div>
  <div class="clD" style="position:absolute;left:20px;top:70px;width:1360px;height:800px;transform-origin:0 0"></div>`;
const clDash=buildDash(q1(clCard,'.clD'));
// la photo de stock se fend le long des deux diagonales de la croix : quatre triangles qui glissent et s'effacent
const CL_TRI=[['0 0,100% 0,50% 50%',0,-1],['100% 0,100% 100%,50% 50%',1,0],['100% 100%,0 100%,50% 50%',0,1],['0 100%,0 0,50% 50%',-1,0]];
const clTri=CL_TRI.map(([poly,dx,dy])=>{ const c=clDash.ph1.cloneNode(true); c.style.clipPath=`polygon(${poly})`; c._d=[dx,dy]; clDash.ph1.parentNode.insertBefore(c,clDash.ph1.nextSibling); return c; }); show(clDash.ph1,false);
CL.cam.style.transformOrigin='1500px 150px';   // la barre d'outils : la poussée finale va vers elle
const clInk=inkLayer(CL.s);
// les centres des composants dans le dashboard (1360×800) : la vague y arrive depuis les deux marques
const CL_C={0:i=>i<4?[150,150+i*52]:i<8?[380+(i-4)*350,186]:[366+(i-8)*46,730],1:()=>[680,400],2:i=>[130,150+i*52],3:i=>i?[420,127]:[560,77],4:i=>[460+i*350,245],
  5:i=>i===0?[400,370]:i<=12?[366+(i-1)*46,650]:[900,500],6:()=>[1235,75],7:()=>[1150,555]};
let CL_S=[560,77], CL_X=[1150,555];
function clFront(k,i,f){ const c=(CL_C[k]||(()=>[680,400]))(i); const t=Math.min(659+Math.hypot(c[0]-CL_S[0],c[1]-CL_S[1])/300, 661+Math.hypot(c[0]-CL_X[0],c[1]-CL_X[1])/300);
  return vladan(clamp((f-t)/4)); }
const M5a=()=>{ const r=clRect(clDash.usr); return penPlace('G05',[r[0]-4,r[1]+(r[3]-r[1])*0.55,r[2]+6,0]); };
const M5b=()=>{ const r=clRect(clDash.img); return penPlace('G06',[r[0]+8,r[1]+8,r[2]-8,r[3]-8],{mode:'stretch'}); };
function clRect(e){ const r=e.getBoundingClientRect(), st=CL.s.getBoundingClientRect(), k=st.width/W; return [(r.left-st.left)/k,(r.top-st.top)/k,(r.right-st.left)/k,(r.bottom-st.top)/k]; }
const clZoom=el(CL.s,'','', 'position:absolute;inset:0;display:none;background:#F6F2EE');
const clBand=el(clZoom,'','', 'position:absolute;left:-40px;right:-200px;top:300px;height:360px;background:#ECE8E3;box-shadow:0 1px 0 #DDD6CE;transform-origin:50% 50%');
const CL_IC=[['branch',560],['activity',830],['terminal',1100],['code',1370]];
const clIcons=CL_IC.map(([k,x])=>{ const d=el(clBand,'','', `position:absolute;left:${x}px;top:95px;width:170px;height:170px;border-radius:34px`); el(d,'',lu(k,120,'#151413',1.6),'position:absolute;inset:25px'); return d; });
el(clBand,'abs','Share','left:1640px;top:96px;height:170px;line-height:166px;padding:0 60px;border-radius:30px;background:#fff;box-shadow:0 0 0 3px #DDD6CE;font-size:84px');
cue(642,'impact',{v:.5}); cue(646,'scratch',{v:.6,end:650}); cue(651,'scratch',{v:.6,end:656}); cue(659,'glide',{v:.5,end:665}); cue(668,'whoosh',{v:.45,peak:671,dur:4}); cue(676,'tick',{v:.25}); cue(690,'click',{v:.95}); cue(687,'whoosh',{v:.4,peak:694,dur:7});
function shotClients(f){ const z=f>=672; show(clZoom,z); show(CL.cam,!z);
  if(!z){ const y=60+40*(1-approach(f,642,4,0.3)); placeTL(clCard,260,y,1.0);
    CL.cam.style.transform=`scale(${(1+0.058*accel(f,668,4,3)).toFixed(4)})`;
    updateDash(clDash,(k,i)=>clFront(k,i,f),f);
    // la salutation : la v1 s'efface, « Morning, Léa. » se tape ; pas de glissement
    const pg=clFront(3,0,f); const sa=clDash.greet.parentNode.parentNode; sa.children[0].style.transform=''; sa.children[0].style.opacity=(1-pg).toFixed(3);
    sa.children[1].style.transform=''; sa.children[1].style.clipPath=`inset(0 ${(100*(1-pg)).toFixed(1)}% 0 0)`;
    const pi=clFront(7,0,f); clTri.forEach(t=>{ t.style.translate=`${(t._d[0]*14*pi).toFixed(1)}px ${(t._d[1]*14*pi).toFixed(1)}px`; t.style.opacity=(1-pi).toFixed(3); });
    const ix=inkClear(clInk);
    if(f>=646&&f<663){ const r=clamp((f-659)/3); penDraw(ix,M5a(),f,646,{size:4.5,u0:r}); }
    if(f>=651&&f<665){ const r=clamp((f-661)/3); penDraw(ix,M5b(),f,651,{size:6,u0:0,u1:1-r}); }
    cursor(0,0,0,false); return; }
  // la poussée continue à travers la coupe et ralentit (672-680), on tient (680-686), puis panoramique qui accélère vers la gauche (687-694)
  const zp=approach(f,672,8,0.25), pan=-60*accel(f,686,8,2.8);
  clBand.style.transform=`translate(${(pan-(f-672)*0.3).toFixed(1)}px,${(30*(1-zp)).toFixed(1)}px) scale(${(1.06-0.06*zp).toFixed(4)})`;
  mblur(clBand,f>=689?vel(t=>-60*accel(t,686,8,2.8),f)*BLUR:0,0);
  const hov=f>=680; clIcons[2].style.background=hov?(f>=688&&f<691?'#DDD6CE':'#E4DFD9'):'transparent';
  // le curseur du fondateur clique le terminal (690) : c'est lui qui ouvre le terminal du plan suivant
  const cf=twos(f,672), cp=clamp((cf-672)/10); cursor(lerp(760,1100+85-40,cp)+pan,lerp(820,300+180,cp),f>=688&&f<691?1:0,true,3);
}
