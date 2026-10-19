/* ============================================================
   Plans 1 à 16 : timings recopiés de la réf (numéros d'image de la réf, cf. SPEC.md)
   ============================================================ */
function el(parent,cls='',html='',css=''){ const d=document.createElement('div'); if(cls) d.className=cls; if(html) d.innerHTML=html; if(css) d.style.cssText=css; parent.appendChild(d); return d; }
function canvas(parent,w,h,css=''){ const c=document.createElement('canvas'); c.width=w; c.height=h; c.style.cssText='position:absolute;'+css; parent.appendChild(c); return c; }
const SCENES=[];
function scene(id,f0,f1,render,cls=''){ const s=document.createElement('div'); s.className='scene '+cls; s.id=id; $('stage').insertBefore(s,$('iriFull')); const cam=el(s,'cam'); SCENES.push({id,f0,f1,render,el:s}); return {s,cam}; }
function sky(parent){ el(parent,'sky'); el(parent,'haze','','top:520px;height:120px;background:rgba(255,236,226,.55)'); el(parent,'haze','','top:690px;height:160px;background:rgba(200,226,236,.5)'); }
const push=(cam,f,f0,k=0.001)=>{ cam.style.transform=`scale(${(1+k*(f-f0)).toFixed(4)})`; };
const T=f=>f/FPS;
function setTint(c,o,a){ if(a<=0.003){ c.style.display='none'; return; } c.style.display='block'; c.style.opacity=a.toFixed(3); iriTo(c,o); }

/* ---------- 1-3 · « Your SaaS is a bit boring. » + glyphes, code, écrans fades, collage ---------- */
const W1=scene('sW',0,119,f=>shotW(f));
const wWord=el(W1.cam,'abs c word');
const WORDS=[[18,'Your'],[24,'Your SaaS'],[45,'is'],[51,'is a'],[54,'is a bit'],[63,'a bit <span style="color:var(--accent)">boring.</span>'],[81,'bit <span style="color:var(--accent)">boring.</span>'],[87,'<span style="color:var(--accent)">boring.</span>'],[93,'']];
const GACC='#FF3D5E', GLIL='#9C86FF', GINK='#151413';
function gset(n,seed,rx,ry){ const r=rng(seed), a=[]; let t=0; while(a.length<n&&t++<600){ const x=(r()*2-1)*rx, y=(r()*2-1)*ry; if(Math.abs(x)<70&&Math.abs(y)<46) continue; if(x*x/(rx*rx)+y*y/(ry*ry)>1) continue; if(a.some(g=>Math.hypot(g[1]-x,g[2]-y)<54)) continue;
  const q=r(); a.push([['/','/','/','<','>','*','|','\\'][(r()*8)|0],x,y,q<.14?GACC:q<.26?GLIL:GINK]); } return a; }
const GK=[[0,[['/',0,0,GINK]]],[9,[['/',-9,0,GINK],['/',9,0,GINK]]],[18,[['/',-78,0,GINK],['/',78,0,GINK]]],
  [24,[['<',-128,0,GINK],['>',128,0,GINK]]],[27,[['<',-128,0,GINK],['>',128,0,GINK],['/',-112,62,GACC]]],
  [30,[['<',-128,0,GINK],['>',128,0,GINK],['/',-112,62,GACC],['|',112,-44,GINK],['/',110,40,GINK]]],
  [36,gset(8,7,260,110)],[45,gset(14,11,330,150)],[51,gset(16,19,380,165)]];
const wGly=Array.from({length:16},()=>el(W1.cam,'abs c glyph'));
const FRAGS=['font-family: Arial;','color: #2D6CDF;','box-shadow: 0 6px 10px #000;','border-radius: 4px;','/* TODO: make it pop */','<h1>Welcome back, User!</h1>','lorem ipsum dolor sit','img: stock_handshake.jpg','.btn-primary { }','font-size: 12px;','!important','z-index: 9999;','● ○','●','○ ●','<marquee>','cursor: pointer;','text-align: center;','#2D6CDF','Get Started Today!'];
const wFr=FRAGS.map((t,i)=>{ const d=el(W1.cam,'abs frag'); d.textContent=t; const r=rng(500+i); let x,y; do{ x=60+r()*1660; y=110+r()*860; }while(Math.abs(x+120-960)<380&&Math.abs(y-540)<90);
  d._x=x; d._y=y; d._d=(r()*3)|0; d.style.color=r()<.38?GACC:r()<.7?GINK:'#9A928A'; return d; });
const wHeat=canvas(W1.cam,240,180,'left:40px;top:720px;width:330px;height:250px;border-radius:6px;display:none');
const BR=[[0,0,884,405,'dash'],[1180,0,740,480,tplBoringStock()],[0,587,320,493,tplBoringMobile()],[330,783,550,297,tplBoringReport()],[1090,640,830,440,tplBoringLanding()]];
const BCL=[[-250,-110,560],[250,-120,420],[-470,70,190],[-110,140,380],[330,120,470]]; // collage : centre relatif + largeur
const wB=BR.map(([x,y,w,h,html],i)=>{ const d=el(W1.cam,'bshot','', `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0`);
  if(html==='dash'){ const dd=el(d,'','', 'position:absolute;left:0;top:0;width:1360px;height:800px;transform-origin:0 0;transform:scale(0.65)'); d._D=buildDash(dd); } else d.innerHTML=html;
  d._tint=canvas(d,160,100,'inset:0;width:100%;height:100%;mix-blend-mode:hard-light;display:none'); d._r=[x,y,w,h]; return d; });
cue(0,'tick',{v:.4}); cue(9,'tick',{v:.4}); [18,24,45,51,54,63].forEach((f,i)=>cue(f,'pluck',{n:[64,67,69,71,72,76][i],v:.4}));
[27,30,36].forEach(f=>cue(f,'tick',{v:.3})); cue(54,'shimmer',{v:.4,end:62}); cue(63,'swish',{v:.45,peak:65,dur:6}); cue(96,'whoosh',{v:.5,peak:112,dur:22});
function shotW(f){ push(W1.cam,f,0,0.0009);
  let w=''; for(const [wf,t] of WORDS) if(f>=wf) w=t; show(wWord,!!w); if(w){ wWord.innerHTML=w; place(wWord,960,540); }
  let gk=null; for(const k of GK) if(f>=k[0]) gk=k;
  wGly.forEach((g,i)=>{ const d=gk&&f<54?gk[1][i]:null; if(!d){ show(g,false); return; } show(g,true);
    const born=(GK.filter(k=>k[0]<=f&&k[1][i]&&k[1][i][1]===d[1]&&k[1][i][2]===d[2]).map(k=>k[0])[0])??gk[0];
    g.textContent=d[0]; g.style.color=d[3]; place(g,960+d[1],540+d[2],back(f,born+((i*0.7)%3),4)); });
  wFr.forEach(d=>{ const on=f>=54+d._d&&f<63; show(d,on); if(on) placeTL(d,d._x+(f-54)*0.6,d._y,back(f,54+d._d,4)); });
  if(f>=60&&f<63){ show(wHeat,true); iriTo(wHeat,{t:T(f),seed:4.4,zoom:1.4,hot:.7,bands:.6}); } else show(wHeat,false);
  // écrans fades : teintés irisé 9 images, puis normaux ; puis collage qui converge et rétrécit
  const pc=approach(f,93,16), g=1-0.62*accel(f,104,15,2.2);
  wB.forEach((d,i)=>{ if(f<63){ show(d,false); return; } show(d,true); const [x,y,w,h]=d._r, [cx,cy,cw]=BCL[i];
    const s0=1+0.0012*(f-63), x0=x+w/2, y0=y+h/2, s1=cw/w;
    const X=lerp(x0,960+cx,pc), Y=lerp(y0,540+cy,pc), S=lerp(s0,s1,pc);
    const Xg=960+(X-960)*g, Yg=540+(Y-540)*g, Sg=S*g;
    d.style.transform=`translate(${(Xg-w*Sg/2).toFixed(1)}px,${(Yg-h*Sg/2).toFixed(1)}px) scale(${Sg.toFixed(4)})`;
    d.style.boxShadow=pc>0?`0 ${(20*pc).toFixed(0)}px ${(50*pc).toFixed(0)}px -20px rgba(40,30,30,${(.35*pc).toFixed(2)})`:'';
    d.style.borderRadius=(10*pc)+'px';
    const tint=f<72?1-approach(f,68,4):approach(f,110,7); setTint(d._tint,{t:T(f),seed:1.7+i,zoom:1.1,hot:.55,bands:.5},tint);
    d.style.filter=f>=113?`blur(${(accel(f,113,7,1.6)*18).toFixed(1)}px)`:'';
    if(d._D) updateDash(d._D,()=>0,f); });
}

/* ---------- 4 · blob → cercle → marque → « vladan » ---------- */
const L1=scene('sLogo',120,173,f=>shotLogo(f));
const lgBlob=el(L1.cam,'abs','', 'overflow:hidden'); const lgIri=canvas(lgBlob,200,200,'inset:0;width:100%;height:100%');
const lgG1=el(lgBlob,'full','', 'background:linear-gradient(135deg,#C7B8FF,#A9E7F2)'), lgG2=el(lgBlob,'full','', 'background:linear-gradient(135deg,#FFA6C9,#FFC7A1)'), lgG3=el(lgBlob,'full','', 'background:#FF3D5E');
const lgSlash=el(lgBlob,'full','<svg viewBox="0 0 96 96" width="100%" height="100%"><path d="M36 66 L60 30" stroke="#EEE9E4" stroke-width="9" stroke-linecap="round"/></svg>');
const lgWord=el(L1.cam,'abs','vladan','font-size:64px;font-weight:600;letter-spacing:-0.04em;line-height:1');
cue(120,'drop',{}); cue(132,'boom',{v:.95}); cue(141,'shimmer',{v:.45,end:150});
function shotLogo(f){ push(L1.cam,f,140,0.0007);
  const S=f<123?lerp(330,210,approach(f,120,3)):f<126?lerp(210,170,approach(f,123,3)):f<132?lerp(170,132,approach(f,126,6)):f<138?132:lerp(132,78,approach(f,138,7));
  const ww=lgWord.offsetWidth||250, tot=78+22+ww; const slide=approach(f,139,9);
  const x=lerp(960,960-tot/2+39,slide);
  Object.assign(lgBlob.style,{width:S+'px',height:S+'px',borderRadius:(f<123?28:50)+'%',filter:f<123?`blur(${lerp(22,6,approach(f,120,3)).toFixed(1)}px)`:''});
  lgBlob.style.transform=`translate(${(x-S/2).toFixed(1)}px,${(540-S/2).toFixed(1)}px)`;
  if(f<124) iriTo(lgIri,{t:T(f),seed:2.2,zoom:1.6,hot:.3,bands:.4});
  lgG1.style.opacity=clamp((f-121)/2)*(1-clamp((f-125)/2)); lgG2.style.opacity=clamp((f-124)/2)*(1-clamp((f-130)/2)); lgG3.style.opacity=clamp((f-129)/3);
  lgSlash.style.opacity=f>=132?1:0; lgSlash.style.transform=`scale(${back(f,132,6).toFixed(3)})`;
  show(lgWord,f>=141); if(f>=141){ placeTL(lgWord,x+39+22-(1-approach(f,141,8))*40,540-34); lgWord.style.clipPath=`inset(-20px ${((1-approach(f,141,8))*100).toFixed(1)}% -20px 0)`; }
}

/* ---------- 5-6 · le prompt, l'envoi, l'irisé qui avale tout ---------- */
const P1=scene('sPrompt',174,233,f=>shotPrompt(f));
const prIri=canvas(P1.cam,960,540,'inset:0;width:1920px;height:1080px;display:none');
const prBox=el(P1.cam,'pbox','', 'left:450px;top:396px');
const prText=el(prBox,'ptext'); const prSend=el(prBox,'psend','<svg viewBox="0 0 72 72" width="72" height="72"><path d="M36 50 V22 M24 33 L36 21 L48 33" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>');
el(prBox,'picon','+','left:40px;bottom:26px'); el(prBox,'picon','◉','right:36px;bottom:28px;font-size:26px');
const PROMPT='Make my SaaS less boring. It’s blue, it’s Arial, and there’s a stock handshake.';
const prGly=gset(12,33,640,250).map(g=>{ const d=el(P1.cam,'abs c glyph'); d._g=g; return d; });
const prGhost=['const taste = {','font: "Inter Display",','arial: false','accent: "#FF3D5E"','ease: "out"'].map((t,i)=>{ const d=el(P1.cam,'abs m',t,`font-size:30px;color:rgba(255,255,255,.75)`); d._x=[180,1300,420,1180,760][i]; d._y=[120,150,860,820,980][i]; return d; });
for(let i=0;i<18;i++) cue(174+i,'key',{v:.25+((i*7)%5)/20});
cue(205,'click',{v:1}); cue(207,'shimmer',{v:.5,end:215}); cue(210,'whoosh',{v:.7,peak:226,dur:22});
function shotPrompt(f){ push(P1.cam,f,174,0.0008);
  const n=Math.round(lerp(46,PROMPT.length,clamp((f-174)/18))); const done=n>=PROMPT.length;
  prText.innerHTML=PROMPT.slice(0,n)+((!done||Math.floor(f/7)%2==0)&&f<210?'<span class="pcaret"></span>':'');
  const pr=f>=205&&f<209; prSend.style.background=f>=207?'#FF3D5E':'#151413'; prSend.style.transform=`scale(${pr?0.9:1})`;
  const cp=approach(f,195,9); cursor(lerp(1720,1404,cp),lerp(880,470,cp),pr?1:0,f>=195&&f<214);
  prGly.forEach((d,i)=>{ const st=207+(i%6); const on=f>=st&&f<224; show(d,on); if(!on) return; const g=d._g; const drift=1+(f-st)*0.012;
    d.textContent=g[0]; d.style.color=f>=216?'#fff':g[3]; place(d,960+g[1]*drift,546+g[2]*drift,back(f,st,4)); });
  // l'irisé part du bouton et envahit le fond, puis avale le champ
  if(f>=210){ show(prIri,true); const hot=lerp(.2,.75,approach(f,218,12)); iriTo(prIri,{t:T(f),seed:3.1,zoom:1.2,hot,bands:lerp(.35,.8,approach(f,220,10))});
    const rr=approach(f,210,9)*2600; prIri.style.webkitMaskImage=prIri.style.maskImage=`radial-gradient(circle at 1404px 470px,#000 ${Math.max(0,rr-300).toFixed(0)}px,transparent ${rr.toFixed(0)}px)`; } else show(prIri,false);
  const dz=approach(f,220,9); prBox.style.opacity=(1-dz).toFixed(3); prBox.style.filter=dz>0?`blur(${(dz*14).toFixed(1)}px)`:''; prBox.style.transform=`scale(${(1+dz*0.04).toFixed(4)})`;
  prGhost.forEach((d,i)=>{ const on=f>=222; show(d,on); if(on){ placeTL(d,d._x-(f-222)*2,d._y); d.style.opacity=(0.8*approach(f,222+i,5)).toFixed(2); } });
}

/* ---------- 7 · la landing générée, recul caméra, « › Taste Files » ---------- */
const LA=scene('sLand',234,299,f=>shotLand(f)); sky(LA.cam);
const laFrame=el(LA.cam); const laD=framed(laFrame,tplLanding(),1440,900,1240,730,'#F3EFEA');
const laTint=canvas(laFrame,240,150,'inset:0;width:100%;height:100%;border-radius:18px;mix-blend-mode:hard-light;display:none');
const laLabel=el(LA.cam,'abs','<span style="font-family:JB;margin-right:18px">›</span>Taste Files','font-size:52px;font-weight:400;color:#8E877F;letter-spacing:-0.01em');
cue(234,'impact',{v:.5}); cue(279,'swish',{v:.4,peak:283,dur:8}); cue(294,'shimmer',{v:.35,end:300});
function shotLand(f){
  const zIn=f<237?1.22:lerp(1.0,0.92,approach(f,237,42)); const mv=approach(f,279,8);
  const s=lerp(zIn,0.667,mv), x=lerp(960,1362,mv), y=lerp(540,552,mv);
  const gone=accel(f,296,3,1.5);
  place(laFrame,x,y,s*(1-0.3*gone)); laFrame.style.opacity=(1-gone).toFixed(3); mblur(laFrame,vel(t=>lerp(960,1362,approach(t,279,8)),f)*BLUR,0);
  q1(laD,'.lh1').style.transform=`translateX(${(-50*approach(f,237,50)).toFixed(1)}px)`; q1(laD,'.lh2').style.transform=`translateX(${(-30*approach(f,237,50)).toFixed(1)}px)`;
  const tint=f<237?1-approach(f,234,3):approach(f,293,4); setTint(laTint,{t:T(f),seed:5.2,zoom:1.2,hot:.6,bands:.6},tint);
  if(window.T3D) T3D.shaker(q1(laD,'.lshaker'),{t:T(f),spin:T(f)*0.6+2.0,tilt:-0.62+0.14*Math.sin(T(f)*19),drop:1,zoom:0.92,lookY:0.15,sprinkle:1,shadow:0,camX:0.2});
  show(laLabel,f>=282); if(f>=282){ const p=approach(f,282,6); placeTL(laLabel,156-(1-p)*24,540-30); laLabel.style.clipPath=`inset(-10px ${((1-p)*100).toFixed(0)}% -10px 0)`; }
}

/* ---------- 8 · l'arborescence « Taste Files » ---------- */
const TR=scene('sTree',300,347,f=>shotTree(f));
const TREE=[[300,'▾ Taste Files',156,0,'title'],[303,'Brand.ts',426,1,'file'],[306,'Typography.ts',426,2,'file'],[309,'Components',672,3,'dir'],
  [315,'NoMoreArial.tsx',900,4,'file'],[321,'OneAccent.tsx',900,5,'file'],[324,'EaseOut.tsx',900,6,'file'],[330,'Taste.tsx',1278,7,'last']];
const trEls=TREE.map(([f0,t,x,row,kind])=>{ const d=el(TR.cam,'titem'); d._k=kind; d._x=x; d._row=row; d._f=f0;
  d.innerHTML=kind==='title'?`<span style="font-family:JB;margin-right:16px">▾</span>Taste Files`:kind==='dir'?`<span class="chev" style="font-family:JB;display:inline-block;margin-right:16px">›</span>${t}`:`<span class="fi"></span>${t}`;
  if(kind==='title') Object.assign(d.style,{fontSize:'56px',color:'#8E877F'}); if(kind==='last') Object.assign(d.style,{color:'#151413',fontSize:'50px'}); return d; });
const trLines=[[360,1,2],[612,3,3],[834,4,6]].map(([x,a,b])=>{ const l=el(TR.cam,'tline'); l._x=x-22; l._a=a; l._b=b; return l; });
TREE.forEach(([f0],i)=>cue(f0,i==TREE.length-1?'pluck':'tick',{v:i==TREE.length-1?.5:.3,n:79}));
function shotTree(f){ push(TR.cam,f,300,0.0011);
  const ty=lerp(342,226,approach(f,300,44)), LH=112;
  trEls.forEach(d=>{ const on=f>=d._f; show(d,on); if(!on) return; const p=approach(f,d._f,6);
    placeTL(d,d._x-(1-p)*16,ty+d._row*LH-28);
    if(d._k!=='title'&&d._k!=='last') d.style.color=f<d._f+4?(d._row%2?'#FF8FB0':'#7FD3E6'):'#B3ABA4';
    if(d._k==='dir'){ const ch=q1(d,'.chev'); ch.style.transform=`rotate(${(90*approach(f,315,5)).toFixed(1)}deg)`; } });
  trLines.forEach(l=>{ const on=f>=TREE[l._a][0]; show(l,on); if(!on) return; const last=Math.max(...TREE.filter(t=>t[3]>=l._a&&t[3]<=l._b&&f>=t[0]).map(t=>t[3]));
    Object.assign(l.style,{left:l._x+'px',top:(ty+(l._a-0.4)*LH)+'px',height:((last-l._a+0.8)*LH)+'px'}); });
}

/* ---------- 9 · le dashboard soigné qui se remplit ---------- */
const DA=scene('sDash',348,380,f=>shotDash(f)); sky(DA.cam);
const daFrame=el(DA.cam); daFrame.className='frame'; Object.assign(daFrame.style,{width:'1440px',height:'900px'});
const daScr=el(daFrame,'scr'); const daDash=el(daScr,'','', 'position:absolute;left:0;top:0;width:1360px;height:800px;transform-origin:0 0'); const DAD=buildDash(daDash);
daDash.style.transform=`translate(0px,${((880-800*1420/1360)/2).toFixed(1)}px) scale(${(1420/1360).toFixed(4)})`; daScr.style.background='#F7F4F0';
cue(348,'impact',{v:.55}); cue(352,'swish',{v:.3,peak:355,dur:6});
function shotDash(f){ push(DA.cam,f,348,0.001); place(daFrame,960,540);
  updateDash(DAD,()=>1,f); iriTo(DAD.imgc,{t:T(f),seed:2.1,zoom:1.2,hot:.2,bands:.35});
  qa(DAD.root,'.sw').forEach((s,i)=>{ const p=approach(f,349+(i%8),7); s.style.clipPath=`inset(0 -3000px ${((1-p)*100).toFixed(0)}% -3000px)`; });
  DAD.kpis.forEach((k,i)=>{ const p=approach(f,351+i*2,9); k.style.transform=`translateY(${((1-p)*40).toFixed(1)}px)`; });
  DAD.bars.forEach((b,i)=>{ const p=approach(f,352+i,10); b.style.height=(parseFloat(b.style.height)*p).toFixed(1)+'px'; });
}

/* ---------- 10 · la salière 3D plein cadre ---------- */
const HE=scene('sHero',381,419,f=>shotHero(f));
const heBg=canvas(HE.cam,960,540,'inset:0;width:1920px;height:1080px');
const he3=canvas(HE.cam,1440,810,'inset:0;width:1920px;height:1080px');
el(HE.cam,'','', 'position:absolute;left:0;right:0;top:0;height:260px;backdrop-filter:blur(10px);-webkit-mask-image:linear-gradient(#000,transparent);mask-image:linear-gradient(#000,transparent)');
el(HE.cam,'','', 'position:absolute;left:0;right:0;bottom:0;height:300px;backdrop-filter:blur(12px);-webkit-mask-image:linear-gradient(transparent,#000);mask-image:linear-gradient(transparent,#000)');
const heDot=el(HE.cam,'abs','', 'width:26px;height:26px;border-radius:13px;background:#FF3D5E;box-shadow:0 0 0 6px rgba(255,255,255,.9)');
cue(381,'impact',{v:.6});
function shotHero(f){ const z=lerp(1,1.07,(f-381)/38); HE.cam.style.transform=`scale(${z.toFixed(4)})`;
  iriTo(heBg,{t:T(f),seed:6.3,zoom:0.75,hot:.22,bands:.5});
  if(window.T3D) T3D.shaker(he3,{t:T(f),spin:T(f)*0.35+0.6,tilt:-0.5+0.1*Math.sin(T(f)*16),drop:1,zoom:1.35,lookY:0.6,camY:0.4,camX:-0.6,sprinkle:1,shadow:0.8});
  place(heDot,880,880);
}

/* ---------- 11 · pills « Lemme give it · salière · taste » ---------- */
const PI=scene('sPills',420,467,f=>shotPills(f));
const piL=el(PI.cam,'pill','Lemme give it'), piR=el(PI.cam,'pill acc','<em>taste</em>'), piI=el(PI.cam,'picn',`<div style="position:absolute;inset:6px">${SHAKER_SVG('#151413',4)}</div>`);
let PIL={};
function pillsLayout(){ const wl=piL.offsetWidth, wr=piR.offsetWidth, ic=84; const sp=34, tg=4;
  const t1=wl+ic+wr+2*sp, t2=wl+ic+wr+2*tg;
  PIL={wl,wr, l1:960-t1/2+wl/2, i1:960-t1/2+wl+sp+ic/2, r1:960+t1/2-wr/2, l2:960-t2/2+wl/2, i2:960-t2/2+wl+tg+ic/2, r2:960+t2/2-wr/2}; }
cue(420,'pop',{v:.55,n:72}); cue(426,'swish',{v:.4,peak:428,dur:6}); cue(432,'pop',{v:.6,n:77}); cue(444,'tick',{v:.4}); cue(447,'swish',{v:.3,peak:451,dur:8}); cue(462,'whoosh',{v:.9,peak:465,dur:10});
function shotPills(f){ push(PI.cam,f,420,0.0009); const L=PIL; const tg=approach(f,447,12);
  const ex=accel(f,462,6,2.2);
  show(piI,f>=420); const filled=f>=444; piI.style.background=filled?'#151413':'#EEE9E4'; piI.innerHTML=`<div style="position:absolute;inset:6px">${SHAKER_SVG(filled?'#EEE9E4':'#151413',4)}</div>`;
  place(piI,lerp(L.i1,L.i2,tg)-ex*500,540,back(f,420,6)); piI.style.opacity=(1-0.6*ex).toFixed(3); mblur(piI,vel(t=>accel(t,462,6,2.2)*500,f)*BLUR,0);
  const inL=approach(f,426,8); show(piL,f>=426); const lx=lerp(L.l1-260,L.l1,inL); place(piL,lerp(lx,L.l2,tg)-ex*1600,540,1,0,1+ex*0.6);
  piL.style.color=f<429||f>=462?'#FF3D5E':'#151413'; piL.style.borderColor=f>=462?'#FF3D5E':'#151413';
  mblur(piL,(vel(t=>lerp(L.l1-260,L.l1,approach(t,426,8)),f)+vel(t=>accel(t,462,6,2.2)*1600,f))*BLUR,0);
  show(piR,f>=432); place(piR,lerp(L.r1,L.r2,tg)-ex*200,540,back(f,432,6)); mblur(piR,ex*30,0); piR.style.opacity=(1-ex).toFixed(3);
}

/* ---------- 12-13 · barres floues → planning « Taste plan » → zooms ---------- */
const PL=scene('sPlan',468,560,f=>shotPlan(f));
const plRoot=el(PL.cam,'','', 'position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0'); plRoot.innerHTML=tplPlan();
const plChips=qa(plRoot,'.pchip'), plDays=qa(plRoot,'.day'), plDn=qa(plRoot,'.dname'), plCols=qa(plRoot,'.col'), plSide=q1(plRoot,'.side'), plTitle=[q1(plRoot,'.ptitle'),plRoot.querySelector('.m')];
const STREAK_COL=['#FF3D5E','#FFC7A1','#C7B8FF','#A9E7F2','#FFF0B5','#FFA6C9','#FF3D5E','#151413','#E4DED7','#A9E7F2'];
plChips.forEach((c,i)=>{ const r=rng(800+i); c._st=468+r()*10; c._from=1500+r()*900; c._bg=c.style.background; });
for(let k=0;k<7;k++) cue(489+k*2,'tick',{v:.22});
cue(468,'whoosh',{v:.6,peak:474,dur:14}); cue(534,'impact',{v:.45}); cue(543,'swish',{v:.35,peak:544,dur:5}); cue(552,'swish',{v:.35,peak:553,dur:5});
function shotPlan(f){
  // zooms (534-560) : 3 recadrages coupés
  let zs=1, zx=960, zy=540; if(f>=534){ const Z=[[534,620,470,40],[543,1280,560,-50],[552,940,770,40]]; let z=Z[0]; for(const q of Z) if(f>=q[0]) z=q;
    zs=2.15; zx=z[1]+z[3]*approach(f,z[0],9); zy=z[2]; }
  plRoot.style.transform=`translate(${(960-zx*zs).toFixed(1)}px,${(540-zy*zs).toFixed(1)}px) scale(${zs})`;
  if(f<534) push(PL.cam,f,500,0.0009); else PL.cam.style.transform='';
  plChips.forEach((c,i)=>{ const p=approach(f,c._st,24,0.1); const dx=(1-p)*c._from; const v=vel(t=>(1-approach(t,c._st,24,0.1))*c._from,f);
    c.style.transform=`translateX(${dx.toFixed(1)}px) scaleX(${(1+Math.min(1.5,Math.abs(v)*0.012)).toFixed(3)})`; mblur(c,v*BLUR*1.4,0);
    const solid=approach(f,c._st+14,10); c.firstChild.style.opacity=c.lastChild.style.opacity=solid.toFixed(2);
    c.style.background=solid<1?`linear-gradient(90deg,${STREAK_COL[i]},rgba(255,255,255,.4))`:c._bg; });
  plDays.forEach((d,i)=>{ const st=489+i*2; d.style.visibility=f>=st?'visible':'hidden'; d.style.color=f<st+4?(i%2?'#FF8FB0':'#FFA36C'):'#151413'; });
  plDn.forEach((d,i)=>{ d.style.visibility=f>=495+i?'visible':'hidden'; });
  plCols.forEach((c,i)=>{ c.style.transformOrigin='0 0'; c.style.transform=`scaleY(${approach(f,486+i,10).toFixed(3)})`; });
  const sp=approach(f,500,8); show(plSide,f>=500); plSide.style.transform=`translateX(${((1-sp)*-300).toFixed(1)}px)`; mblur(plSide,vel(t=>(1-approach(t,500,8))*-300,f)*BLUR,0);
  plTitle.forEach((t,i)=>{ t.style.visibility=f>=504+i*2?'visible':'hidden'; });
}

/* ---------- 14 · téléphone : score de goût, rubans holographiques, « Taste applied » ---------- */
const PH=scene('sPhone',561,641,f=>shotPhone(f));
const phRib=canvas(PH.cam,960,540,'inset:0;width:1920px;height:1080px');
const phone=el(PH.cam,'phone'); const phScr=el(phone,'scr');
const phImg=canvas(phScr,192,240,'left:0;top:0;width:384px;height:480px'); const ph3=canvas(phScr,384,480,'left:0;top:0;width:384px;height:480px');
el(phScr,'glass','saasly','position:absolute;left:22px;top:26px;height:38px;line-height:38px;padding:0 16px;border-radius:19px;color:#fff;font-size:16px;font-weight:600');
el(phScr,'abs','Q3 flavor','left:24px;top:400px;font-size:40px;color:#fff;letter-spacing:-0.03em');
const phStats=el(phScr,'','', 'position:absolute;left:0;right:0;top:480px;bottom:0;background:#151413');
el(phStats,'abs m','TASTE SCORE','left:26px;top:28px;font-size:13px;letter-spacing:.1em;color:#8E877F');
const phNum=el(phStats,'abs','8.6','left:22px;top:52px;font-size:96px;color:#fff;letter-spacing:-0.05em;line-height:1');
el(phStats,'abs m','TASTE TIME','left:228px;top:28px;font-size:13px;letter-spacing:.1em;color:#8E877F');
const phTime=el(phStats,'abs','0:07:23','left:226px;top:60px;font-size:40px;color:#fff;letter-spacing:-0.03em');
el(phStats,'','Stop tasting ■','position:absolute;left:22px;right:22px;bottom:24px;height:62px;border-radius:31px;background:#FF3D5E;color:#fff;font-size:20px;line-height:62px;text-align:center');
const phTint=canvas(phScr,96,204,'inset:0;width:100%;height:100%');
const phDone=el(phScr,'','', 'position:absolute;left:0;right:0;bottom:0;height:430px;background:#151413;border-radius:30px 30px 0 0');
phDone.innerHTML=`<div style="position:absolute;left:26px;top:30px;width:44px;height:44px;border-radius:12px;background:#FF3D5E;color:#fff;font-size:26px;line-height:44px;text-align:center">✓</div>
  <div style="position:absolute;left:26px;top:92px;font-size:52px;color:#fff;letter-spacing:-0.04em;line-height:1">Taste<br><em style="font-size:60px">applied.</em></div>
  <div class="m" style="position:absolute;left:28px;top:226px;font-size:13px;color:#8E877F">arial removed · 1 accent · 47 fixes</div>
  <div style="position:absolute;left:22px;right:22px;bottom:24px;height:62px;border-radius:31px;background:#FF3D5E;color:#fff;font-size:20px;line-height:62px;text-align:center">Back to dashboard</div>`;
cue(561,'impact',{v:.55}); cue(573,'shimmer',{v:.35,end:603}); [588,603].forEach(f=>cue(f,'tick',{v:.3})); cue(606,'swish',{v:.45,peak:609,dur:8}); cue(608,'pop',{v:.5,n:84});
function shotPhone(f){ push(PH.cam,f,561,0.0008);
  const rib=f<573?approach(f,563,10):f<606?1:1-approach(f,606,24);
  iriTo(phRib,{t:T(f)*1.4,seed:8.8,zoom:0.9,hot:.25,bands:1.0}); phRib.style.opacity=(0.15+0.85*rib).toFixed(3);
  phRib.style.webkitMaskImage=phRib.style.maskImage=`linear-gradient(100deg,transparent ${(62-30*rib).toFixed(0)}%,#000 ${(92-30*rib).toFixed(0)}%)`;
  place(phone,960,lerp(560,540,approach(f,561,9)));
  iriTo(phImg,{t:T(f),seed:3.3,zoom:0.8,hot:.3,bands:.35}); if(window.T3D) T3D.shaker(ph3,{t:T(f),spin:T(f)*0.8,drop:1,zoom:0.95,lookY:-0.05,sprinkle:.6,shadow:.5});
  const sc=lerp(8.6,9.2,clamp((f-573)/30)); phNum.textContent=sc.toFixed(1); phTime.textContent='0:07:'+(23+Math.floor(clamp((f-573)/30)*2.99));
  setTint(phTint,{t:T(f),seed:2.6,zoom:1,hot:.6,bands:.6},1-approach(f,561,9));
  const dp=approach(f,606,10); phDone.style.transform=`translateY(${((1-dp)*440).toFixed(1)}px)`; mblur(phDone,0,vel(t=>(1-approach(t,606,10))*440,f)*BLUR);
}

/* ---------- 15-16 · « My clients », puis gros plan sur la barre d'outils ---------- */
const CL=scene('sClients',642,695,f=>shotClients(f)); sky(CL.cam);
const clCard=el(CL.cam,'','', 'position:absolute;left:0;top:0;width:1740px;height:1000px;border-radius:18px;overflow:hidden;box-shadow:0 50px 100px -40px rgba(40,30,30,.5)'); clCard.innerHTML=tplClients();
const clZoom=el(CL.s,'','', 'position:absolute;inset:0;display:none;background:#EEE9E4');
const clZbg=canvas(clZoom,480,120,'left:0;top:660px;width:1920px;height:420px;filter:blur(18px)');
const clBand=el(clZoom,'','', 'position:absolute;left:-40px;right:-40px;top:300px;height:360px;background:#F7F6F4;box-shadow:0 1px 0 #E6E1DB');
const clIcon=el(clBand,'','', 'position:absolute;left:630px;top:100px;width:170px;height:170px;border-radius:34px');
el(clIcon,'',SHAKER_SVG('#151413',3),'position:absolute;inset:18px');
el(clBand,'abs','∿','left:1000px;top:110px;font-size:120px;color:#151413;line-height:1');
el(clBand,'abs m','&lt;/&gt;','left:1210px;top:132px;font-size:96px;color:#151413;line-height:1');
el(clBand,'abs','Share','left:1500px;top:96px;height:170px;line-height:166px;padding:0 60px;border-radius:30px;background:#fff;box-shadow:0 0 0 3px #E6E1DB;font-size:84px');
cue(642,'impact',{v:.5}); cue(672,'swish',{v:.35,peak:673,dur:5}); cue(689,'click',{v:.95});
function shotClients(f){ const z=f>=672; show(clZoom,z); show(CL.cam,!z);
  if(!z){ push(CL.cam,f,642,0.001); placeTL(clCard,-20-(f-642)*0.6,150); iriTo(q1(clCard,'.cbg'),{t:T(f),seed:7.2,zoom:1.4,hot:.25,bands:.35});
    if(window.T3D) T3D.shaker(q1(clCard,'.cshaker'),{t:T(f),spin:T(f)*0.7,drop:1,zoom:0.9,lookY:0.05,sprinkle:.5,shadow:0});
    const cp=approach(f,666,12); cursor(lerp(980,800,cp),lerp(1120,940,cp),0,f>=666); return; }
  iriTo(clZbg,{t:T(f),seed:7.2,zoom:1.4,hot:.25,bands:.35});
  clBand.style.transform=`translateX(${(-(f-672)*0.8).toFixed(1)}px)`;
  const hov=f>=678; clIcon.style.background=hov?(f>=688?'#E2DCD5':'#ECE8E3'):'transparent';
  const cp=approach(f,672,7); cursor(lerp(900,722,cp)-(f-672)*0.8,lerp(780,520,cp),f>=688&&f<691?1:0,true);
}
