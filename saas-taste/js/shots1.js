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
// tables de couleurs : la teinte suit les clairs et les ombres de l'image (réf 62-69, 114-116, 232)
(()=>{ const tab=cs=>{ const c=cs.map(h=>[1,3,5].map(k=>parseInt(h.slice(k,k+2),16)/255)); return [0,1,2].map(j=>c.map(x=>x[j].toFixed(3)).join(' ')); };
  const gm=(id,cs)=>{ const [r,g,b]=tab(cs); return `<filter id="${id}" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".3 .59 .11 0 0 .3 .59 .11 0 0 .3 .59 .11 0 0 0 0 0 1 0"/><feComponentTransfer><feFuncR type="table" tableValues="${r}"/><feFuncG type="table" tableValues="${g}"/><feFuncB type="table" tableValues="${b}"/></feComponentTransfer></filter>`; };
  $('fx').innerHTML+=gm('gmTherm',['#20205E','#3070D0','#5CC8E8','#FFE59A','#FF8A4D','#FF6B6B','#FFC9A3'])+gm('gmHeat',['#2A0718','#8E1B3C','#FF5A5A','#FFB070','#BFE6F2','#E6F7FF','#FFFFFF'])+gm('gmPastel',['#7E6BE0','#B9A8FF','#FFA6C9','#FFC7A1','#FFF1E6','#FFFAF6']); })();
const GM=k=>k===1?'url(#gmTherm)':k===2?'url(#gmPastel)':'';
function setTint(c,o,a){ if(a<=0.003){ c.style.display='none'; return; } c.style.display='block'; c.style.opacity=a.toFixed(3); iriTo(c,o); }

/* ---------- 1-3 · « Your SaaS is a bit boring. » + glyphes, code, écrans fades, collage ---------- */
const W1=scene('sW',0,119,f=>shotW(f));
const wWord=el(W1.cam,'abs c word');
const WORDS=[[18,'Your'],[24,'Your SaaS'],[45,'is'],[51,'is a'],[55,'is a bit'],[61,'a bit <span style="color:var(--accent)">boring.</span>'],[80,'bit <span style="color:var(--accent)">boring.</span>'],[85,'boring'],[88,'<span style="color:var(--accent)">boring</span>'],[91,'<span style="color:#FFA6C9">boring</span>'],[94,'']];
const GACC='#FF3D5E', GLIL='#9C86FF', GINK='#151413';
function gset(n,seed,rx,ry){ const r=rng(seed), a=[]; let t=0; while(a.length<n&&t++<600){ const x=(r()*2-1)*rx, y=(r()*2-1)*ry; if(Math.abs(x)<70&&Math.abs(y)<46) continue; if(x*x/(rx*rx)+y*y/(ry*ry)>1) continue; if(a.some(g=>Math.hypot(g[1]-x,g[2]-y)<54)) continue;
  const q=r(); a.push([['/','/','/','<','>','*','|','\\'][(r()*8)|0],x,y,q<.14?GACC:q<.26?GLIL:GINK]); } return a; }
// Les glyphes s'accumulent jusqu'à 53 (comme dans la réf) ; les deux premiers s'écartent pour laisser place aux mots.
const GLY=[{ch:[[0,'/'],[24,'<']],pos:[[0,0,0],[8,-18,0],[13,-124,0],[19,-232,0],[45,-190,0]],col:GINK,born:0,big:1},
           {ch:[[8,'/'],[24,'>']],pos:[[8,18,0],[13,124,0],[19,232,0],[45,190,0]],col:GINK,born:8,big:1}];
(()=>{ const r=rng(7), ex=[]; [27,30,30,33,36,36,36,39,42,45,45,45,45,47,49,51,51,51,52,52].forEach(b=>{ let x,y,t=0;
  do{ x=(r()*2-1)*505; y=(r()*2-1)*330; t++; }while(t<500&&((Math.abs(x)<240&&Math.abs(y)<62)||x*x/(505*505)+y*y/(330*330)>1||ex.some(e=>Math.hypot(e[0]-x,e[1]-y)<74)));
  ex.push([x,y]); const q=r(); GLY.push({ch:[[b,['/','/','/','<','>','*','|','\\'][(r()*8)|0]]],pos:[[b,x,y]],col:q<.15?GACC:q<.28?GLIL:GINK,born:b}); }); })();
const wGly=GLY.map(g=>el(W1.cam,'abs c glyph','',g.big?'font-size:64px':''));
function gpos(g,f){ let i=0; for(let k=0;k<g.pos.length;k++) if(f>=g.pos[k][0]) i=k; const c=g.pos[i], p=i?g.pos[i-1]:c, t=approach(f,c[0],5); return [lerp(p[1],c[1],t),lerp(p[2],c[2],t)]; }
function gch(g,f){ let c=g.ch[0][1]; for(const k of g.ch) if(f>=k[0]) c=k[1]; return c; }
const FRAGS=['font-family: Arial;','color: #2D6CDF;','box-shadow: 0 6px 10px #000;','border-radius: 4px;','/* TODO: make it pop */','<h1>Welcome back, User!</h1>','lorem ipsum dolor sit','img: stock_handshake.jpg','.btn-primary { }','font-size: 12px;','!important','z-index: 9999;','● ○','●','○ ●','<marquee>','cursor: pointer;','text-align: center;','#2D6CDF','Get Started Today!'];
function fragPos(t,seed){ const r=rng(seed), w=t.length*20.4; let x,y,k=0; do{ x=30+r()*(1860-w); y=80+r()*900; k++; }while(k<300&&Math.abs(x+w/2-960)<w/2+250&&Math.abs(y-540)<80); return [x,y,r]; }
const wFr=FRAGS.map((t,i)=>{ const d=el(W1.cam,'abs frag'); d._t=t; const [x,y,r]=fragPos(t,500+i); d._x=x; d._y=y; d._d=(r()*6)|0; d._c=r()<.38?GACC:r()<.7?GINK:'#9A928A'; d._ty=i%2; return d; });
// deuxième couche plus dense et plus pâle (réf 59)
const wFr2=FRAGS.map((t,i)=>{ const d=el(W1.cam,'abs frag',t,'font-size:22px;opacity:.16'); const [x,y]=fragPos(t,900+i); d._x=x; d._y=y; return d; });
const wHeat=canvas(W1.cam,240,180,'left:40px;top:720px;width:330px;height:250px;border-radius:6px;display:none');
const BR=[[0,0,884,405,'dash'],[1180,0,740,480,tplBoringStock()],[0,587,320,493,tplBoringMobile()],[330,783,550,297,tplBoringReport()],[1090,640,830,440,tplBoringLanding()]];
const BCL=[[-200,-95,560,0],[210,-120,430,0],[-360,60,200,0],[-80,120,390,0],[260,95,470,0]];
const BDR=[[-50,-20],[40,-5],[-45,10],[35,40],[100,45]], BST=[84,89,90,89,91], BSW=[[110,0],[-90,1.3],[140,2.2],[-80,3.1],[120,4.4]];
// 5 écrans de plus entrent dans le collage (la réf en empile une dizaine)
const BXT=[[tplBoringLogin(),420,300],[tplBoringTable(),420,300],[tplBoringEmail(),440,300],[tplBoringReport(),480,280],[tplBoringMobile(),240,380],[tplBoringStock(),420,300]];
const BXC=[[40,-30,300,-3,-1,-1],[-330,-180,270,4,-1,-1],[360,-10,300,-2,1,0],[-40,170,280,3,0,1],[150,-190,200,2,1,-1],[-260,150,240,-4,-1,1]];
const wB=BR.map(([x,y,w,h,html],i)=>{ const d=el(W1.cam,'bshot','', `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0`);
  if(html==='dash'){ const dd=el(d,'','', 'position:absolute;left:0;top:0;width:1360px;height:800px;transform-origin:0 0;transform:scale(0.65)'); d._D=buildDash(dd); } else d.innerHTML=html;
  d._tint=canvas(d,160,100,'inset:0;width:100%;height:100%;mix-blend-mode:hard-light;display:none'); d._r=[x,y,w,h]; return d; });
const wX=BXT.map(([html,w,h],i)=>{ const d=el(W1.cam,'bshot',html, `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0`); d._w=w; d._h=h; d._tint=canvas(d,160,100,'inset:0;width:100%;height:100%;mix-blend-mode:hard-light;display:none'); return d; });
const ease3=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const wToast=el(wB[4],'ar','', 'position:absolute;right:24px;bottom:24px;height:46px;padding:0 18px;background:#333;color:#fff;font-size:17px;line-height:46px;border-radius:4px;display:none');
function swapB(d,i,f){
  if(i==2){ const hd=d.querySelector('.full>div'); if(hd) hd.style.background=f>=70?'#1F3A8A':'#2D6CDF'; }
  if(i==1){ const sv=d.querySelector('svg'); if(sv) sv.style.opacity=f>=67&&f<70?0:1; const lb=d.querySelector('.ar'); if(lb) lb.textContent=f>=67&&f<70?'Loading…':'stock_handshake_final_v3.jpg'; }
  if(i==0&&d._D){ d._D.side.style.background=f>=66?'#4B5BD6':'#2D6CDF'; }
  if(i==4){ show(wToast,f>=91); if(f>=91) wToast.textContent='Saved!'.slice(0,Math.min(6,(f-90)*2)); }
}
cue(8,'tick',{v:.4}); [18,24,45,51,55,61].forEach((f,i)=>cue(f,'pluck',{n:[64,67,69,71,72,76][i],v:.3}));
[27,30,36,42,49].forEach(f=>cue(f,'tick',{v:.25})); cue(53,'shimmer',{v:.35,end:61}); cue(104,'riser',{v:.4,end:119}); cue(62,'swish',{v:.45,peak:64,dur:6}); cue(89,'whoosh',{v:.4,peak:99,dur:14}); [64,66,67,70].forEach(f=>cue(f,'tick',{v:.2})); cue(96,'swish',{v:.45,peak:97,dur:4}); [104,108,113].forEach(f=>cue(f,'tick',{v:.22}));
function shotW(f){ push(W1.cam,f,0,0.0009);
  let w=''; for(const [wf,t] of WORDS) if(f>=wf) w=t; show(wWord,!!w); if(w){ wWord.innerHTML=w; place(wWord,960,540); }
  const grow=f<45?1:f<51?1.2:1.45;
  GLY.forEach((g,i)=>{ const d=wGly[i]; const on=f>=g.born&&f<53; show(d,on); if(!on) return; let [x,y]=gpos(g,f);
    if(!g.big){ const r=rng(90+i*7+(f>=51?2:f>=45?1:0)); x=x*grow+(f>=45?(r()-0.5)*40:0); y=y*grow+(f>=45?(r()-0.5)*30:0); }
    const rot=i>=2&&i%2==1&&gch(g,f)!=='*'; d.textContent=rot?['/','|','\\','-'][(Math.floor(f/2)+i)%4]:gch(g,f);
    const warm=approach(f,g.born,4), cool=g.col===GACC?approach(f,g.born+5,4):0;
    d.style.color=mixc(mixc('#EEE9E4',g.col===GINK?'#FFB59A':g.col,warm),g.col===GACC?GINK:g.col,g.col===GINK?warm:cool);
    place(d,960+x,540+y,g.born===0?1:back(f,g.born-1,4)); });
  wFr.forEach((d,i)=>{ const st=53+d._d; const on=f>=st&&f<(i<5?64:62); show(d,on); if(!on) return;
    d.textContent=d._ty?d._t.slice(0,Math.max(3,(f-st+1)*2)):d._t; d.style.color=mixc('#FFC9D6',d._c,approach(f,st,4)); placeTL(d,d._x+(f-53)*0.6,d._y,back(f,st-1,4)); });
  wFr2.forEach(d=>{ const on=f>=59&&f<62; show(d,on); if(on) placeTL(d,d._x-(f-59)*1.5,d._y); });
  if(f>=58&&f<62){ show(wHeat,true); iriTo(wHeat,{t:T(f),seed:4.4,zoom:1.4,hot:.7,bands:.6,therm:1}); } else show(wHeat,false);
  // collage : accélère progressivement à partir de 89 (comme la réf), puis tout rétrécit en un blob irisé
  const g=1-0.72*accel(f,113,8,2.0);
  const tintK=(f,i)=>{ const k=f-i; return k<62?0:k<65?1:k<70?2:(f>=114&&f<117)?2:0; };
  const sway=f<98?0:Math.sin(2*Math.PI*(f-98)/13.33);
  wB.forEach((d,i)=>{ if(f<62){ show(d,false); return; } show(d,true); const [x,y,w,h]=d._r, [cx,cy,cw]=BCL[i];
    const pc=ease3(clamp((f-BST[i])/18)), dr=approach(f,62,27,0.08);
    const s0=1+0.0012*(f-62), X=lerp(x+w/2+BDR[i][0]*dr,960+cx+BSW[i][0]*Math.sin(2*Math.PI*(f-98)/13.33+BSW[i][1])*(f>=98?1:0),pc), Y=lerp(y+h/2+BDR[i][1]*dr,540+cy,pc), S=lerp(s0,cw/w,pc);
    const Xg=960+(X-960)*g, Yg=540+(Y-540)*g, Sg=S*g; d.style.zIndex=f<104?i:f<108?(5-i):f<113?((i*3)%5):i;
    mblur(d,f>=84&&f<100?vel(t=>lerp(x+w/2,960+cx,ease3(clamp((t-BST[i])/18))),f)*BLUR*0.6:0,0);
    d.style.transform=`translate(${(Xg-w*Sg/2).toFixed(1)}px,${(Yg-h*Sg/2).toFixed(1)}px) scale(${Sg.toFixed(4)})`;
    d.style.boxShadow=pc>0?`0 ${(20*pc).toFixed(0)}px ${(50*pc).toFixed(0)}px -20px rgba(40,30,30,${(.35*pc).toFixed(2)})`:''; d.style.borderRadius=(10*pc)+'px';
    show(d._tint,false); const bl=f>=116?` blur(${(accel(f,116,5,1.6)*18).toFixed(1)}px)`:''; d.style.filter=(GM(tintK(f,i))+bl).trim()||'';
    if(d._D) updateDash(d._D,()=>0,f); swapB(d,i,f); });
  wX.forEach((d,i)=>{ const st=96+(i%2); if(f<st){ show(d,false); return; } show(d,true); const [cx,cy,cw,rot,ox,oy]=BXC[i]; const p=approach(f,st,10);
    const sx=(i%2?-1:1)*90*sway; const X=lerp(960+ox*1400+cx,960+cx+sx,p), Y=lerp(540+oy*900+cy,540+cy,p), S=cw/d._w; const Xg=960+(X-960)*g, Yg=540+(Y-540)*g, Sg=S*g; d.style.zIndex=10+((i+(f>=104)+(f>=108)*2)%6);
    d.style.transform=`translate(${(Xg-d._w*Sg/2).toFixed(1)}px,${(Yg-d._h*Sg/2).toFixed(1)}px) rotate(${rot}deg) scale(${Sg.toFixed(4)})`; d.style.borderRadius='10px'; d.style.boxShadow='0 20px 50px -20px rgba(40,30,30,.35)';
    mblur(d,vel(t=>lerp(960+ox*1400+cx,960+cx,approach(t,st,12)),f)*BLUR,vel(t=>lerp(540+oy*900+cy,540+cy,approach(t,st,12)),f)*BLUR);
    show(d._tint,false); const bl=f>=116?` blur(${(accel(f,116,5,1.6)*18).toFixed(1)}px)`:''; d.style.filter=((f>=114&&f<117?GM(2):'')+bl).trim(); });
}

/* ---------- 4 · blob → cercle → marque → « vladan » ---------- */
const L1=scene('sLogo',120,173,f=>shotLogo(f));
const lgBlob=el(L1.cam,'abs','', 'overflow:hidden'); const lgIri=canvas(lgBlob,200,200,'inset:0;width:100%;height:100%');
const lgG1=el(lgBlob,'full','', 'background:linear-gradient(135deg,#C7B8FF,#A9E7F2)'), lgG2=el(lgBlob,'full','', 'background:linear-gradient(135deg,#FFA6C9,#FFC7A1)'), lgG3=el(lgBlob,'full','', 'background:#FF3D5E');
const lgSlash=el(lgBlob,'full','<svg viewBox="0 0 96 96" width="100%" height="100%"><path d="M36 66 L60 30" stroke="#EEE9E4" stroke-width="9" stroke-linecap="round"/></svg>');
const lgWord=el(L1.cam,'abs','vladan','font-size:84px;font-weight:600;letter-spacing:-0.04em;line-height:1');
// le mot sort de la marque en 2-3 images, bord adouci et irisé (comme la réf)
let LGW=330; function logoLayout(){ show(lgWord,true); LGW=lgWord.offsetWidth; show(lgWord,false); }
function revealWord(d,f,f0){ const p=approach(f,f0,3), e=lerp(-15,118,p);
  d.style.webkitMaskImage=d.style.maskImage=p<1?`linear-gradient(90deg,#000 ${(e-14).toFixed(1)}%,transparent ${(e+14).toFixed(1)}%)`:'';
  const tint=p<1; d.style.background=tint?`linear-gradient(90deg,#151413 ${(e-30).toFixed(0)}%,#FFA6C9 ${(e-8).toFixed(0)}%,#A9E7F2 ${(e+6).toFixed(0)}%)`:'';
  d.style.webkitBackgroundClip=d.style.backgroundClip=tint?'text':''; d.style.color=tint?'transparent':''; }
cue(120,'drop',{}); cue(132,'boom',{v:.95}); cue(139,'shimmer',{v:.45,end:147});
function shotLogo(f){ push(L1.cam,f,140,0.0007);
  const S=f<123?lerp(330,210,approach(f,120,3)):f<126?lerp(210,170,approach(f,123,3)):f<132?lerp(170,132,approach(f,126,6)):f<137?132:lerp(132,81,approach(f,137,4));
  const ww=LGW, gap=24, tot=81+gap+ww, slide=approach(f,137,4);
  const x=lerp(960,960-tot/2+40.5,slide);
  Object.assign(lgBlob.style,{width:S+'px',height:S+'px',borderRadius:(f<123?28:50)+'%',filter:f<123?`blur(${lerp(22,6,approach(f,120,3)).toFixed(1)}px)`:f<128?`blur(${lerp(4,0,(f-123)/5).toFixed(1)}px)`:''});
  lgBlob.style.transform=`translate(${(x-S/2).toFixed(1)}px,${(540-S/2).toFixed(1)}px)`;
  if(f<124) iriTo(lgIri,{t:T(f),seed:2.2,zoom:1.6,hot:.3,bands:.4});
  lgG1.style.opacity=clamp((f-121)/2)*(1-clamp((f-125)/2)); lgG2.style.opacity=clamp((f-124)/2)*(1-clamp((f-130)/2)); lgG3.style.opacity=clamp((f-129)/3);
  lgSlash.style.opacity=f>=132?1:0; lgSlash.style.transform=`scale(${back(f,131,5).toFixed(3)})`;
  show(lgWord,f>=139); if(f>=139){ placeTL(lgWord,x+40.5+gap,540-42,1+0.07*approach(f,139,16)); revealWord(lgWord,f,139); if(f>=142) lgWord.innerHTML=f<150?'<span style="color:#FFA6C9">v</span>ladan':'vladan'; }
  L1.cam.style.translate=`0 ${(-12*accel(f,167,6,2)).toFixed(1)}px`;
}

/* ---------- 5-6 · le prompt, l'envoi, l'irisé qui avale tout ---------- */
const P1=scene('sPrompt',174,233,f=>shotPrompt(f));
const prIri=canvas(P1.cam,960,540,'inset:0;width:1920px;height:1080px;display:none');
const prBox=el(P1.cam,'pbox','', 'left:450px;top:396px');
const prText=el(prBox,'ptext'); const prSend=el(prBox,'psend','<svg viewBox="0 0 72 72" width="72" height="72"><path d="M36 50 V22 M24 33 L36 21 L48 33" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>');
el(prBox,'picon','+','left:40px;bottom:26px'); el(prBox,'picon','◉','right:36px;bottom:28px;font-size:26px');
const PROMPT='Make my furniture store less boring. It’s blue, it’s Arial, and there’s a stock handshake.';
const prGly=gset(12,33,640,250).map(g=>{ const d=el(P1.cam,'abs c glyph'); d._g=g; return d; });
const prGhost=['const taste = {','font: "Inter Display",','arial: false','accent: "#FF3D5E"','ease: "out"'].map((t,i)=>{ const d=el(P1.cam,'abs m',t,`font-size:30px;color:rgba(255,255,255,.75)`); d._x=[180,1300,420,1180,760][i]; d._y=[120,150,860,820,980][i]; return d; });
// frappe irrégulière (0-3 caractères par image, comme la réf) ; clic à 207-208 ; l'irisé envahit tout 215-218, bascule thermique à 222
const PR_INC=[3,2,2,0,2,1,3,0,1,2,1,1,2,0,1,3,2,1,0,2,3,1];
const PR_N=(()=>{ const a=[46]; for(const k of PR_INC) a.push(a[a.length-1]+k); return a; })();
for(let i=0;i<PR_INC.length;i++) if(PR_INC[i]) cue(174+i,'key',{v:.2+PR_INC[i]*0.08});
cue(207,'click',{v:1}); cue(208,'shimmer',{v:.5,end:216}); cue(212,'whoosh',{v:.7,peak:226,dur:20}); cue(222,'swish',{v:.45,peak:224,dur:5});
const prGhostImg=el(P1.cam,'','', 'position:absolute;inset:0;display:none;mix-blend-mode:soft-light'); prGhostImg.innerHTML=vimg('room_eye','inset:0;width:100%;height:100%;filter:blur(12px)');
const prGlow=el(prSend,'','', 'position:absolute;inset:0;border-radius:18px;background:radial-gradient(circle at 50% 30%,#FF8A3D,#7A2A10 60%,#151413);opacity:0');
function shotPrompt(f){ push(P1.cam,f,174,0.0008); P1.cam.style.translate=`0 ${(-23*approach(f,174,20)).toFixed(1)}px`;
  const n=Math.min(PROMPT.length,PR_N[clamp(f-174,0,PR_N.length-1)]); const done=n>=PROMPT.length;
  prText.innerHTML=PROMPT.slice(0,n)+((!done||Math.floor(f/7)%2==0)&&f<210?'<span class="pcaret"></span>':'');
  const pr=f>=207&&f<209; prSend.style.transform=`scale(${pr?0.94:1})`; prGlow.style.opacity=f<207?0:(1-approach(f,208,6)).toFixed(3);
  const cp=approach(f,193,5); cursor(lerp(1404+75,1404,cp),lerp(470+85,470,cp),pr?1:0,f>=193&&f<214);
  prGly.forEach((d,i)=>{ const st=204+i; const on=f>=st&&f<224; show(d,on); if(!on) return; const g=d._g; const drift=1+(f-st)*0.012;
    d.textContent=i%2?['/','|','\\','-'][(Math.floor(f/2)+i)%4]:g[0]; d.style.color=f>=216?'#fff':mixc('#EEE9E4',g[3]===GINK?'#FF9A6A':g[3],approach(f,st,4)); place(d,960+g[1]*drift,546+g[2]*drift,back(f,st,4)); });
  // l'irisé part du bouton et envahit le fond, puis avale le champ
  // l'irisé (rapide, ×8) gagne tout le cadre 215-218, bascule en thermique en 2 images à 222, chauffe jusqu'à 231, filé horizontal 229-231
  if(f>=214){ show(prIri,true); const hot=f<226?lerp(.35,.45,approach(f,215,6)):lerp(.45,.9,approach(f,226,5));
    iriTo(prIri,{t:T(f)*8,seed:3.1,zoom:1.2,hot,bands:lerp(.4,.85,approach(f,218,8)),therm:f<222?0:clamp((f-221)/2)});
    prIri.style.opacity=clamp((f-214)/4).toFixed(3); prIri.style.webkitMaskImage=prIri.style.maskImage=''; mblur(prIri,f>=229?40:0,0); } else show(prIri,false);
  show(prGhostImg,f>=216); if(f>=216){ prGhostImg.style.opacity=(0.45*approach(f,216,6)).toFixed(3); prGhostImg.style.transform=`scale(${(1+0.08*clamp((f-216)/17)).toFixed(4)})`; }
  const dz=approach(f,222,5); prBox.style.opacity=(1-dz).toFixed(3); prBox.style.filter=dz>0?`blur(${(dz*14).toFixed(1)}px)`:''; prBox.style.transform=`scale(${(1+dz*0.04).toFixed(4)})`;
  prGhost.forEach((d,i)=>{ const on=f>=222; show(d,on); if(on){ placeTL(d,d._x-(f-222)*2,d._y); d.style.opacity=(0.8*approach(f,222+i,5)).toFixed(2); } });
}

/* ---------- 7 · la landing velvetly (vidéo Cycles), recul qui ralentit, accélération dans la coupe, « › Taste Files » ---------- */
const LA=scene('sLand',234,299,f=>shotLand(f)); sky(LA.cam);
const laFrame=el(LA.cam); const laD=framed(laFrame,tplVLanding(),1440,900,1240,730,VINK);
const laTint=canvas(laFrame,240,150,'inset:0;width:100%;height:100%;border-radius:18px;mix-blend-mode:hard-light;display:none');
const laLabel=el(LA.cam,'abs','<span style="font-family:JB;margin-right:22px">›</span>Taste Files','font-size:84px;font-weight:400;color:#3A3633;letter-spacing:-0.01em');
const laSeq=q1(laD,'.vseq'), laPills=qa(laD,'.vpill'), laTiles=qa(laD,'.vtile');
const laShop=el(q1(laD,'.full'),'m','Shop','position:absolute;top:688px;height:22px;line-height:22px;padding:0 10px;border-radius:6px;background:#FF3D5E;color:#fff;font-size:11px');
const PH_COL=['#FF9A4D','#FFA6C9','#B9A8FF'];
cue(234,'impact',{v:.5}); cue(244,'tick',{v:.25}); cue(256,'tick',{v:.25}); cue(259,'swish',{v:.25,peak:262,dur:6}); cue(276,'whoosh',{v:.5,peak:281,dur:6}); cue(281,'tick',{v:.45}); cue(294,'shimmer',{v:.35,end:300});
function laLayout(f){ // accordéon des tuiles (réf 259-270) : la tuile large passe à sa voisine
  const p=approach(f,259,11); const W=[236,lerp(236,330,p),236,lerp(250,156,p),236]; let x=12;
  laTiles.forEach((t,i)=>{ t.style.left=x+'px'; t.style.width=W[i]+'px'; x+=W[i]+8; });
  laShop.style.left=lerp(12+3*244+150-60,12+244+330-70,p).toFixed(1)+'px'; }
function shotLand(f){
  // réf : recul qui ralentit (235-273), accélération dans la coupe (274-280), puis petit écran qui se pose (281+)
  let sc,x=960,y=540;
  if(f<235) sc=1.08; else if(f<274) sc=lerp(1.08,0.915,approach(f,235,38,0.09));
  else if(f<281){ const a=accel(f,274,6.5,2.6); sc=lerp(0.915,0.823,a); x=960+40*a; }
  else { const p=approach(f,281,14,0.25); sc=lerp(0.683,0.632,p); x=1588-720*sc+lerp(16,0,p); y=548; }
  const gone=f>=294?approach(f,294,5):0;
  place(laFrame,x,y,sc); laFrame.style.filter=gone>0?`url(#gmPastel) blur(${(10*gone).toFixed(1)}px) brightness(${(1+0.35*gone).toFixed(2)})`:''; laFrame.style.opacity=(1-0.85*clamp((f-297)/3)).toFixed(3);
  mblur(LA.cam,f>=276&&f<281?vel(t=>40*accel(t,274,6.5,2.6),f):0,0);
  seqDraw(laSeq,SEQ.land,f-234);
  q1(laD,'.lnh').style.transform=`translateX(${(-290*approach(f,235,36,0.10)).toFixed(1)}px)`;
  // boutons d'abord en blocs de couleur qui changent toutes les 4 images, puis le logo (244) et les boutons (256)
  laPills.forEach((pl,i)=>{ const ready=f>=(i==0?244:256); pl.style.color=ready?'':'transparent'; pl.style.background=ready?'':PH_COL[(Math.floor((f-234)/4)+i)%3];
    if(i==0) pl.style.background=ready?'rgba(18,17,16,.55)':pl.style.background; if(i==1&&ready) pl.style.background='#FF3D5E'; if(i==2&&ready) pl.style.background='rgba(18,17,16,.55)';
    pl.querySelectorAll('span').forEach(sp=>sp.style.visibility=ready?'visible':'hidden'); });
  q1(laD,'.full>.m').style.visibility=f>=242?'visible':'hidden';
  laLayout(f);
  setTint(laTint,{t:T(f)*4,seed:5.2,zoom:1.2,hot:.6,bands:.6,therm:1},1-approach(f,234,6));
  show(laLabel,f>=281); if(f>=281) placeTL(laLabel,150,300-10*approach(f,281,12));
}

/* ---------- 8 · l'arborescence « Taste Files » : défilement par paliers, couleurs qui passent cyan → lilas → pêche → gris ---------- */
const TR=scene('sTree',300,347,f=>shotTree(f));
const TREE=[[300,'▾ Taste Files',150,0,'title'],[305,'Brand.ts',380,1,'file'],[308,'Typography.ts',380,2,'file'],[312,'Components',380,3,'dir'],
  [317,'NoMoreArial.tsx',610,4,'file'],[320,'OneAccent.tsx',610,5,'file'],[322,'EaseOut.tsx',610,6,'file'],[329,'Taste.tsx',840,7,'last']];
const trEls=TREE.map(([f0,t,x,row,kind])=>{ const d=el(TR.cam,'titem'); d._k=kind; d._x=x; d._row=row; d._f=f0;
  d.innerHTML=kind==='title'?`<span style="font-family:JB;margin-right:16px">▾</span>Taste Files`:kind==='dir'?`<span class="chev" style="font-family:JB;display:inline-block;margin-right:16px">›</span>${t}`:`<span class="fi"></span>${t}`;
  Object.assign(d.style,{fontSize:kind==='title'?'84px':kind==='last'?'84px':'72px'}); if(kind==='title') d.style.color='#3A3633'; if(kind==='last') d.style.color='#151413'; return d; });
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
    if(d._k!=='title'&&d._k!=='last'){ const a=f-d._f; d.style.color=a<4?'#7FD3E6':a<9?'#B9A8FF':a<14?'#FFC7A1':mixc('#FFC7A1','#958D86',clamp((a-14)/4)); }
    if(d._k==='dir'){ const ch=q1(d,'.chev'); ch.style.transform=`rotate(${(90*approach(f,317,4)).toFixed(1)}deg)`; } });
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
const heSvg=el(HE.cam,'',`<svg width="1920" height="1080" viewBox="0 0 1920 1080"><g class="hplan" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="2"></g><path class="her" fill="none" stroke="#FF3D5E" stroke-width="11" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 4px 10px rgba(80,20,30,.35))"/></svg>`,'position:absolute;left:0;top:0');
const hePlan=q1(heSvg,'.hplan'), heRoute=q1(heSvg,'.her');
const HE_SH=['rug','sofa','pouf','table','plant','chair'];
const heShapes=HE_SH.map((k,i)=>{ const p=document.createElementNS('http://www.w3.org/2000/svg','path'); p.setAttribute('fill',['rgba(199,184,255,.18)','rgba(255,166,201,.16)','rgba(169,231,242,.18)','rgba(255,199,161,.18)','rgba(169,231,242,.16)','rgba(255,61,94,.14)'][i]); hePlan.appendChild(p); return p; });
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
  heRoute.setAttribute('d',pth(P.route)); heRoute.style.opacity=1;
  HE_SH.forEach((k,j)=>{ heShapes[j].setAttribute('d',pth(P[k])+' Z'); heShapes[j].style.opacity=approach(f,383+j*2,8).toFixed(3); });
  const d=P.route[P.route.length-1]; heDot.style.left=(d[0]*1920)+'px'; heDot.style.top=(d[1]*1080)+'px';
}

/* ---------- 11 · pills « Lemme give it · fauteuil · taste » : couleurs à l'arrivée, resserrage décalé, fonte sur place ---------- */
const cR11=cueAt(2);
const PI=scene('sPills',420,467,f=>shotPills(f));
const piL=el(PI.cam,'pill','Lemme give it'), piR=el(PI.cam,'pill acc','<em>taste</em>'), piI=el(PI.cam,'picn',`<div style="position:absolute;inset:8px">${CHAIR_SVG('#151413',4)}</div>`);
const piMelt=el(PI.cam,'','', 'position:absolute;left:0;top:467px;height:146px;border-radius:73px;background:linear-gradient(90deg,#FFA6C9,#FF9A4D 55%,#FFF0B5);filter:blur(14px);display:none');
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
  piI.innerHTML=`<div style="position:absolute;inset:8px">${CHAIR_SVG(filled?'#EEE9E4':mixc('#B9A8FF','#151413',clamp((f-418)/11)),4)}</div>`;
  place(piI,xi,540,back(f,418,4)); piI.style.borderColor=mixc('#A9E7F2','#151413',clamp((f-418)/11));
  show(piL,f>=424); piL.style.opacity=approach(f,424,3).toFixed(3); place(piL,xl,540); const cl=arrive(f,424,'#FFF0B5'); piL.style.color=cl; piL.style.borderColor=cl;
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
const PL_BARS=[[466,467,'#FFA6C9'],[466,180,'#FF9A4D'],[470,720,'#FFF0B5'],[472,300,'#B9A8FF'],[474,610,'#A9E7F2'],[474,850,'#FFC7A1'],[474,120,'#FF3D5E']].map(([st,y,c],i)=>{ const d=el(PL.cam,'','', `position:absolute;top:${y}px;height:${138+(i%3)*4}px;border-radius:70px;background:${c};filter:blur(14px);display:none`); const r=rng(810+i); d._st=st; d._x=i==0?600:80+r()*900; d._g=25+r()*65; d._c=100+r()*70; return d; });
plChips.forEach((c,i)=>{ c._bg=c.style.background; c._st=504+i*1.3; });
for(let k=0;k<7;k++) cR12(494+k*2.4,'tick',{v:.2}); PL_BARS.forEach(b=>cR12(b._st,'swish',{v:.18,peak:b._st+3,dur:6}));
cR12(532,'impact',{v:.45}); cR12(541,'swish',{v:.35,peak:542,dur:5}); cR12(550,'swish',{v:.35,peak:551,dur:5}); cR12(555,'whoosh',{v:.4,peak:559,dur:5});
function shotPlan(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // zooms 532-558 : UNE poussée qui ralentit à travers les 3 coupes ; la puce grandit à la fin (raccord téléphone)
  let zs=1, zx=960, zy=540; if(f>=532){ const Z=[[532,800,470],[541,1280,560],[550,960,770]]; let z=Z[0]; for(const q of Z) if(f>=q[0]) z=q;
    zs=2.15*(1+0.032*approach(f,532,27,0.09)); zx=z[1]; zy=z[2]; }
  plRoot.style.transform=`translate(${(960-zx*zs).toFixed(1)}px,${(540-zy*zs).toFixed(1)}px) scale(${zs})`;
  // caméra : recul qui ralentit (499-516), puis parfaitement immobile jusqu'à la coupe
  PL.cam.style.transform=f<532?`scale(${(1.04-0.04*approach(f,499,17,0.1)).toFixed(4)})`:'';
  plRoot.firstChild.style.background=mixc('#EEE9E4','#F6F2EE',approach(f,490,16));
  PL_BARS.forEach(b=>{ const a=f-b._st; const on=a>=0&&a<14&&f<532; show(b,on); if(!on) return; const grow=Math.min(a,5)*b._g, tail=Math.max(0,a-5)*b._c;
    b.style.left=(b._x+tail)+'px'; b.style.width=Math.max(10,180+grow-tail)+'px'; b.style.opacity=(1-clamp((a-8)/6)).toFixed(3); });
  plChips.forEach((c,i)=>{ const blob=f>=486+(i%6)*1.4, sharp=approach(f,c._st,3,0.3);
    c.style.visibility=blob?'visible':'hidden'; c.style.transform=f>=555&&i==3?`scaleY(${(1+0.4*accel(f,555,4,2)).toFixed(3)})`:''; if(i==3) c.style.transformOrigin='50% 0';
    c.style.filter=sharp<1?`blur(${(14*(1-sharp)).toFixed(1)}px)`:''; c.firstChild.style.opacity=c.lastChild.style.opacity=sharp.toFixed(2); c.style.background=c._bg; });
  plDays.forEach((d,i)=>{ const st=494+i*2.4; d.style.visibility=f>=st?'visible':'hidden'; d.style.color=f<st+4?mixc('#FFA6C9','#151413',clamp((f-st)/4)):(i>=5?'#C9A7F0':'#151413'); });
  plDn.forEach((d,i)=>{ d.style.visibility=f>=497+i*2.4?'visible':'hidden'; });
  plCols.forEach((c,i)=>{ c.style.transformOrigin='0 0'; c.style.transform=`scaleY(${approach(f,488+i,10).toFixed(3)})`; });
  show(plSide,f>=498); plSide.style.background=mixc('#FFC9D6','#121110',approach(f,498,14));
  [...plSide.children].forEach(e=>{ e.style.opacity=approach(f,505,6).toFixed(2); });
  plTitle.forEach((t,i)=>{ t.style.visibility=f>=506+i*2?'visible':'hidden'; if(i==0) t.style.color=mixc('#B9A8FF','#3A3633',approach(f,506,10)); });
  plX.forEach((t,i)=>{ t.style.visibility=f>=508+i?'visible':'hidden'; });
}

/* ---------- 14 · téléphone : se déplie en hauteur, écran irisé balayé par le bas, vidéo en grue, rubans plein cadre ---------- */
const cR14=cueAt(2);
const PH=scene('sPhone',561,641,f=>shotPhone(f));
const phRib=canvas(PH.cam,960,540,'inset:0;width:1920px;height:1080px');
const phone=el(PH.cam,'phone'); const phScr=el(phone,'scr');
const phSeq=canvas(phScr,612,1260,'left:0;top:0;width:384px;height:816px');
el(phScr,'','', 'position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 48%,rgba(10,9,8,.86) 78%)');
el(phScr,'glass',VLOGO('#fff',15),'position:absolute;left:22px;top:30px;height:38px;line-height:38px;padding:0 14px;border-radius:12px');
el(phScr,'glass','','position:absolute;right:22px;top:30px;width:38px;height:38px;border-radius:12px');
el(phScr,'abs','Living room','left:24px;top:84px;font-size:46px;color:#fff;letter-spacing:-0.04em');
el(phScr,'abs m','▪ ROOM FIT','left:26px;top:478px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)');
const phNum=el(phScr,'abs','92%','left:22px;top:498px;font-size:104px;color:#fff;letter-spacing:-0.05em;line-height:1');
el(phScr,'abs m','▪ ARRIVES IN','left:26px;top:612px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)');
const phTime=el(phScr,'abs','2:59:58','left:22px;top:632px;font-size:58px;color:#fff;letter-spacing:-0.04em;line-height:1');
el(phScr,'','Place in room<span style="position:absolute;right:8px;top:8px;width:46px;height:46px;border-radius:12px;background:#151413"></span>','position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#FF3D5E;color:#fff;font-size:20px;line-height:62px;padding-left:22px');
const phTint=canvas(phScr,96,204,'inset:0;width:100%;height:100%');
const phDone=el(phScr,'','', 'position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,rgba(18,17,16,0),#121110 26%)');
phDone.innerHTML=`<div style="position:absolute;left:24px;top:96px;width:44px;height:44px;border-radius:12px;background:#FF3D5E;color:#fff;font-size:26px;line-height:44px;text-align:center">✓</div>
  <div style="position:absolute;left:24px;top:156px;font-size:54px;color:#fff;letter-spacing:-0.045em;line-height:.98">Fits<br>perfectly</div>
  <div class="m" style="position:absolute;left:26px;top:280px;font-size:12px;color:#8E877F">sofa 2.19 m · chair 0.83 m · 24 m²</div>
  <div style="position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#FF3D5E;color:#fff;font-size:20px;line-height:62px;text-align:center">Back to shop</div>`;
cR14(559,'impact',{v:.55}); cR14(566,'shimmer',{v:.35,end:578}); [588,603].forEach(f=>cR14(f,'tick',{v:.3})); cR14(606,'swish',{v:.45,peak:609,dur:8}); cR14(608,'pop',{v:.5,n:84});
function shotPhone(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // rubans holographiques qui balaient tout le cadre de droite à gauche (≈90 px/image), éteints vers 635
  const fr=2300-(f-566)*90; iriTo(phRib,{t:T(f)*6,seed:8.8,zoom:0.9,hot:.25,bands:1.0}); phRib.style.opacity=(f<566?0:(1-approach(f,612,23))).toFixed(3);
  phRib.style.webkitMaskImage=phRib.style.maskImage=`linear-gradient(100deg,transparent ${(fr-900).toFixed(0)}px,#000 ${(fr-500).toFixed(0)}px,#000 ${(fr-100).toFixed(0)}px,transparent ${(fr+300).toFixed(0)}px)`;
  // dépli en hauteur seulement (478 → 861 px), largeur fixe ; pas de poussée ensuite
  place(phone,960,540,1,0,1); phone.style.transform+=` scaleY(${lerp(0.555,1,approach(f,559,13,0.25)).toFixed(4)})`;
  seqDraw(phSeq,SEQ.phone,f-559);
  phNum.textContent=Math.round(lerp(92,98,clamp((f-573)/30)))+'%';
  phTime.textContent=`2:59:${String(58-Math.floor(Math.max(0,f-559)/30)).padStart(2,'0')}`;
  // écran irisé, puis balayage du bas vers le haut (566-576)
  const wp=approach(f,566,10,0.15)*120; show(phTint,f<577); if(f<577){ iriTo(phTint,{t:T(f)*5,seed:2.6,zoom:1,hot:.6,bands:.6,therm:1});
    phTint.style.webkitMaskImage=phTint.style.maskImage=f<566?'':`linear-gradient(0deg,transparent ${(wp-12).toFixed(1)}%,#000 ${wp.toFixed(1)}%)`; }
  const dp=approach(f,606,10); phDone.style.transform=`translateY(${((1-dp)*440).toFixed(1)}px)`;
}

/* ---------- 15-16 · « My Orders » : le cadre se pose en remontant, vidéo dans le bandeau, poussée qui accélère vers la barre d'outils ---------- */
const CL=scene('sClients',642,694,f=>shotClients(f)); sky(CL.cam);
const clCard=el(CL.cam,'','', 'position:absolute;left:0;top:0;width:1740px;height:1000px;border-radius:18px;overflow:hidden;box-shadow:0 50px 100px -40px rgba(40,30,30,.5)'); clCard.innerHTML=tplVOrders();
const clSeq=q1(clCard,'.vseq'), clRows=qa(clCard,'.trow');
CL.cam.style.transformOrigin='1330px 162px';
const clZoom=el(CL.s,'','', 'position:absolute;inset:0;display:none;background:#EEE9E4');
const clZbg=canvas(clZoom,480,120,'left:0;top:660px;width:1920px;height:420px;filter:blur(18px)');
const clBand=el(clZoom,'','', 'position:absolute;left:-40px;right:-200px;top:300px;height:360px;background:#F7F6F4;box-shadow:0 1px 0 #E6E1DB;transform-origin:50% 50%');
const clIcon=el(clBand,'','', 'position:absolute;left:630px;top:100px;width:170px;height:170px;border-radius:34px');
el(clIcon,'','<svg viewBox="0 0 48 48" width="100%" height="100%"><g fill="none" stroke="#151413" stroke-width="3" stroke-linecap="round"><circle cx="14" cy="10" r="5"/><circle cx="14" cy="38" r="5"/><circle cx="34" cy="18" r="5"/><path d="M14 15 V33 M34 23 Q34 30 22 31 Q16 32 14 33"/></g></svg>','position:absolute;inset:26px');
el(clBand,'abs','∿','left:1000px;top:110px;font-size:120px;color:#151413;line-height:1');
el(clBand,'abs m','&lt;/&gt;','left:1210px;top:132px;font-size:96px;color:#151413;line-height:1');
el(clBand,'abs','Share','left:1500px;top:96px;height:170px;line-height:166px;padding:0 60px;border-radius:30px;background:#fff;box-shadow:0 0 0 3px #E6E1DB;font-size:84px');
cue(642,'impact',{v:.5}); cue(665,'whoosh',{v:.45,peak:671,dur:7}); cue(676,'tick',{v:.25}); cue(689,'click',{v:.95}); cue(687,'whoosh',{v:.4,peak:694,dur:7});
function shotClients(f){ const z=f>=672; show(clZoom,z); show(CL.cam,!z);
  if(!z){ // le contenu remonte en ralentissant (≈45 px, 642-660), immobile 662-664, puis poussée qui accélère (665-670) vers la barre d'outils
    const y=140+45*(1-approach(f,642,18,0.2)); placeTL(clCard,-10,y,1.0);
    CL.cam.style.transform=`scale(${(1+0.058*accel(f,665,6,3)).toFixed(4)})`;
    seqDraw(clSeq,SEQ.done,8+(f-642)*1.3,0.5,0.42);
    clRows.forEach((r,i)=>{ const p=approach(f,643+i*2,6,0.3); r.style.opacity=p.toFixed(2); r.style.translate=`0 ${((1-p)*30).toFixed(1)}px`; });
    const cp=approach(f,667,5,0.3); cursor(lerp(1180,1290,cp),lerp(520,190,cp),0,f>=667); return; }
  iriTo(clZbg,{t:T(f)*3,seed:7.2,zoom:1.4,hot:.25,bands:.35});
  // la poussée continue à travers la coupe et ralentit (672-680), on tient (680-686), puis panoramique qui accélère vers la gauche (687-694)
  const zp=approach(f,672,8,0.25), pan=-60*accel(f,686,8,2.8);
  clBand.style.transform=`translate(${(pan-(f-672)*0.3).toFixed(1)}px,${(30*(1-zp)).toFixed(1)}px) scale(${(1.06-0.06*zp).toFixed(4)})`;
  mblur(clBand,f>=689?vel(t=>-60*accel(t,686,8,2.8),f)*BLUR:0,0);
  const hov=f>=676; clIcon.style.background=hov?(f>=688&&f<691?'#E2DCD5':'#ECE8E3'):'transparent';
  const cp=approach(f,672,6,0.3); cursor(lerp(930,722,cp)+pan,lerp(800,520,cp),f>=688&&f<691?1:0,true,3);
}
