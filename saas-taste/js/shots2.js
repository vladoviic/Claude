/* ============================================================
   Plans 17 à 32
   ============================================================ */

/* ---------- 17-19 · terminal : npm rm boring --force → add motion → éditeur (numéros de la réf : scène recalée +1) ---------- */
const TE=scene('sTerm',696,815,f=>shotTerm(f),'dark');
const cR17=cueAt(1);
const ARROW=(w,h)=>`<svg width="${w}" height="${h}" viewBox="0 0 240 170"><path d="M14 85 H210 M140 20 L214 85 L140 150" fill="none" stroke="#FF3D5E" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const teGhost=el(TE.cam,'abs tt','taste','font-size:520px;color:#fff;opacity:.03;left:0;top:0');
const teBig=el(TE.cam,'abs',ARROW(240,170),'line-height:0');
const teBigCaret=el(TE.cam,'abs','', 'width:30px;height:280px;border-radius:4px');
const teLine=el(TE.cam,'abs tt'); const teBox=el(TE.cam,'tpanel','', 'border-color:#3A3633;display:none');
const tePanel=el(TE.cam,'tpanel'); const teDim1=el(tePanel,'abs m','velvetly / src / taste.ts','left:26px;top:18px;font-size:16px;color:#3E3B38');
const teDim2=el(tePanel,'abs m','ln 12 · utf-8 · typescript','right:26px;bottom:16px;left:auto;font-size:16px;color:#3E3B38');
const teSide=el(tePanel,'','', 'position:absolute;left:0;top:0;bottom:0;width:64px;border-right:1px solid #2C2C2C;display:none');
for(let k=0;k<5;k++) el(teSide,'','', `position:absolute;left:20px;top:${70+k*56}px;width:24px;height:24px;border-radius:6px;border:2px solid ${k==1?'#FF3D5E':'#3E3B38'}`);
const tePanelLine=el(TE.cam,'abs tt','', 'font-size:84px');
const CODE=[['<span class="k">export const</span> taste = {',0],['  font: <span class="s">"Inter Display"</span>,',1],['  accent: <span class="s">"#FF3D5E"</span>,   <span class="c">// one. used well.</span>',2],['  ease: <span class="s">"out"</span>,',3],
  ['  motion: { arrive: <span class="s">"fast"</span>, land: <span class="s">"soft"</span> },',4],['  arial: <span class="k">false</span>,',5],['  stockPhotos: <span class="n">0</span>,',6],['};',7],['',8],['app.use(taste);   <span class="c">// the whole trick</span>',9],['<span class="k">export default</span> velvetly;',10],['<span class="c">// before: font-family: Arial;</span>',11]];
const CODE_T=[767,767,767,767,773,784,784,788,788,792,796,799];   // arrivées par paquets (réf)
const teCode=CODE.map(([h,i])=>{ const d=el(tePanel,'cline'); d._h=`<span class="n" style="display:inline-block;width:64px">${i+1}</span>${h}`; d.innerHTML=d._h; d.style.fontSize='34px'; return d; });
const teSel=el(tePanel,'','', 'position:absolute;top:0;height:46px;border-radius:6px;background:rgba(120,150,255,.22)');
const teTok=el(tePanel,'','', 'position:absolute;top:0;height:46px;border-radius:6px;background:rgba(255,61,94,.22)');
const teBlack=el(TE.s,'','', 'position:absolute;inset:0;background:#000;opacity:0;pointer-events:none');
const TEW=[[750,'<em style="font-size:96px">taste.</em>'],[757,'mo'],[762,'moti'],[764,'motion']];
const TE_CMD='npm rm ';
let TEL={};
function termLayout(){ teLine.innerHTML=`<span style="display:inline-block;margin-right:22px">${ARROW(110,78)}</span>npm rm <span class="tsel">boring</span> <span class="tsel2">--force</span>`; TEL.w=teLine.offsetWidth; teLine.innerHTML=''; }
for(let i=0;i<TE_CMD.length;i++) if(TE_CMD[i]!==' ') cR17(707+Math.round(i*2.9),'key',{v:.4});
cR17(695,'break',{}); cR17(732,'tick',{v:.45}); cR17(739,'tick',{v:.45}); cR17(750,'enter',{v:.8}); [757,762,764].forEach(f=>cR17(f,'key',{v:.35})); cR17(766,'pop',{v:.3,n:84});
[773,784,788,792,796,799].forEach(f=>cR17(f,'key',{v:.22})); cR17(790,'swish',{v:.3,peak:791,dur:4});
const CARET_COL=[[695,'#8A9A5B'],[697,'#6B7A8F'],[699,'#9C86FF'],[703,'#FF8FB0']];
function shotTerm(F){ const f=F-1;
  teGhost.style.opacity=(0.035*(1-approach(f,695,10))).toFixed(3); placeTL(teGhost,280,180);
  const big=f<707; show(teBig,big); show(teBigCaret,big);
  if(big){ const sl=37*approach(f,695,11,0.2); place(teBig,950+sl,540); let cc='#8A9A5B'; for(const [cf,c] of CARET_COL) if(f>=cf) cc=c;
    teBigCaret.style.background=cc; teBigCaret.style.transform=`scaleY(${f>=698&&f<701?1.35:1})`; teBigCaret.style.transformOrigin='50% 50%'; placeTL(teBigCaret,1105+sl,400); }
  // la ligne se tape (1 touche / 2,9 images), immobile entre les touches ; la taille descend en 3 paliers nets (719, 732, 739)
  const lineMode=f>=707&&f<750; show(teLine,lineMode);
  if(lineMode){ const n=clamp(Math.floor((f-707)/2.9)+1,0,TE_CMD.length);
    let h=`<span style="display:inline-block;vertical-align:-2px;margin-right:22px">${ARROW(110,78)}</span>`+TE_CMD.slice(0,n);
    if(f>=732) h+=`<span class="tsel" style="display:inline-block;transform:scale(${(1.15-0.15*approach(f,732,3)).toFixed(3)})">boring</span>`; if(f>=739) h+=` <span class="tsel2" style="display:inline-block;transform:scale(${(1.15-0.15*approach(f,739,3)).toFixed(3)})">--force</span>`;
    const car=(f<739||Math.floor(f/6)%2==0); h+=`<span style="display:inline-block;width:16px;height:112px;background:#F2EEE8;vertical-align:-20px;margin-left:10px;visibility:${car?'visible':'hidden'}"></span>`;
    teLine.innerHTML=h; const S=f<719?2.3:f<732?lerp(2.3,1.51,approach(f,719,2,0.5)):f<739?lerp(1.51,1.21,approach(f,732,2,0.5)):lerp(1.21,1,approach(f,739,2,0.5));
    place(teLine,960-1.6*(f-707),540,S);
    show(teBox,f>=740); if(f>=740){ const w=TEL.w+120; Object.assign(teBox.style,{left:(960-1.6*(f-707)-w/2)+'px',top:'462px',width:w+'px',height:'156px',opacity:approach(f,740,5).toFixed(2)}); } }
  else show(teBox,false);
  const panel=f>=750; show(tePanel,panel); show(tePanelLine,panel&&f<767);
  if(panel){ // panneau fixe ; recul par palier à 790 (barre d'icônes qui apparaît), pas de poussée continue
    const st=approach(f,790,3,0.4), pw=f<767?1280:lerp(1357,1568,st), ph=f<767?300:lerp(660,720,st);
    Object.assign(tePanel.style,{left:(960-pw/2)+'px',top:(540-ph/2)+'px',width:pw+'px',height:ph+'px'});
    show(teSide,f>=790); const lx=f>=790?96:40, fs=lerp(34,26,st), lh=lerp(51,40,st);
    let w=''; for(const [wf,t] of TEW) if(f>=wf) w=t;
    tePanelLine.innerHTML=`<span style="color:${f<752?'#FF3D5E':'#F2EEE8'}">→</span> <span style="color:#FF3D5E">add</span>&nbsp;&nbsp;${w}`;
    placeTL(tePanelLine,970-tePanelLine.offsetWidth/2,540-44,f>=766?1+0.1*(1-approach(f,766,4)):1);
    // le code arrive par paquets : insertion avec sélection (773, frappe 2 car./image jusqu'à 784), sauts d'indentation (784), paquets (788, 792, 796, 799)
    let row=0; teCode.forEach((d,i)=>{ const t0=CODE_T[i], on=f>=t0&&f>=767; show(d,on); if(!on) return;
      d.style.fontSize=fs+'px'; d.style.left=(lx+(i==5||i==6?45*(1-approach(f,784,3,0.4)):0))+'px'; d.style.top=(70+row*lh)+'px'; row++;
      if(i!==4&&t0>767&&f<t0+3) d.style.clipPath=`inset(0 ${((1-(f-t0+1)/3)*100).toFixed(0)}% 0 0)`; else d.style.clipPath='';
      d.innerHTML=i==4&&f<784?`<span class="n" style="display:inline-block;width:64px">5</span>`+'  motion: { arrive: "fast", land: "soft" },'.slice(0,2+(f-773)*4):d._h; });
    show(teSel,f>=773&&f<786); if(f>=773){ Object.assign(teSel.style,{left:(lx-6)+'px',top:(70+4*lh-4)+'px',width:(f<784?260+(f-773)*30:600)+'px'}); }
    show(teTok,f>=792); if(f>=792){ const sp=approach(f,792,4); Object.assign(teTok.style,{left:(lx+64*(fs/34)+16)+'px',top:(70+5*lh-4)+'px',width:(300*sp*(fs/34))+'px'}); } }
  TE.cam.style.transform=''; teBlack.style.opacity=f>=808?'1':'0';   // coupe franche au noir, comme la réf
}

/* ---------- 20 · macro N&B en contre-jour (séquence Cycles) : le fond s'allume, puis le sujet ; recul qui accélère (réf, +1) ---------- */
const MA=scene('sMacro',816,879,f=>shotMacro(f));
const cR20=cueAt(1);
const maSeq=canvas(MA.cam,1280,720,'left:0;top:0;width:1920px;height:1080px;filter:grayscale(1) contrast(1.15)');
cR20(815,'riser',{v:.35,end:826}); cR20(864,'whoosh',{v:.6,peak:876,dur:12});
// curseur en 3 segments (réf) : entrée rapide 826-832, glisse le long du pied en ralentissant jusqu'à 868, repart à gauche
const MA_CUR=[[826,683,1011],[832,896,649],[868,1515,559],[878,1109,627]];
function maCursor(f){ if(f<826) return null; for(let k=0;k<MA_CUR.length-1;k++){ const [a,x0,y0]=MA_CUR[k],[b,x1,y1]=MA_CUR[k+1]; if(f<=b){ const t=(f-a)/(b-a), e=k==1?1-Math.pow(1-t,1.6):k==2?t*t:t; return [lerp(x0,x1,e),lerp(y0,y1,e)]; } } return [1109,627]; }
function shotMacro(F){ const f=F-1;
  seqDraw(maSeq,SEQ.macro,f-816);
  // fin : le recul rendu continue en 2D avec un flou directionnel croissant (pas de roulis)
  const wh=accel(f,872,6,2.4); MA.cam.style.transform=`scale(${(1-0.12*wh).toFixed(4)})`; MA.cam.style.filter=wh>0?`blur(${(wh*10).toFixed(1)}px)`:'';
  const c=maCursor(f); cursor(c?c[0]:0,c?c[1]:0,0,!!c&&f<878);
}

/* ---------- 21 · chat IA + page produit : l'interface ne bouge pas, tout se passe dans la vue 3D et dans le fil ---------- */
const CH=scene('sChat',880,953,f=>shotChat(f));
const chRoot=el(CH.cam,'','', 'position:absolute;inset:0'); chRoot.innerHTML=tplVChat();
const chTurn=q1(chRoot,'.pturn'), chThermal=q1(chRoot,'.pthermal'), chCol=q1(chRoot,'.spcol'), chSw=q1(chRoot,'.spsw'), chView=chTurn.parentElement;
const chTurnR=canvas(chView,1100,800,'inset:0;width:100%;height:100%;display:none'); chView.insertBefore(chTurnR,chThermal);
const chKids=[...q1(chRoot,'.chatp').children];   // 0 logo · 1 bulle · 2 réflexion · 3 réponse · 4-5 paquets · 6 approbation · 7 suggestions · 8-10 puces · 11 saisie
const chNew=el(q1(chRoot,'.chatp'),'','', 'position:absolute;inset:0;display:none'); chNew.innerHTML=`<div class="bubble" style="top:104px">Make it <em style="font-size:24px">red velvet.</em></div>
  <div class="ctext" style="top:196px">Swapped Corporate blue for red velvet. Same chair, more taste.</div>
  <div style="position:absolute;left:32px;right:32px;top:270px;height:64px;border-radius:16px;background:#fff;box-shadow:0 0 0 1px #E6E1DB"><span class="m" style="position:absolute;left:20px;top:22px;font-size:13px;color:#6d6760"><b style="color:#FF3D5E">✓</b>&nbsp; Updated 1 material · fabric_rosso</span></div>`;
const chNewK=[...chNew.children];
const CH_SUG2=['Show in room','Add a pouf','Ship it'];
const chHot=el(chRoot,'','', 'position:absolute;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:32px;box-shadow:0 0 0 3px #FF3D5E,0 0 0 10px rgba(255,61,94,.18);display:none');
const chTip=el(chRoot,'m','', 'position:absolute;height:34px;line-height:34px;padding:0 14px;border-radius:17px;background:#151413;color:#F3EFEA;font-size:13px;white-space:nowrap;display:none');
const pad2=i=>String(i).padStart(2,'0');
const TURN={blue:[],red:[],mask:[]};
for(let i=0;i<48;i++) TURN.blue[i]=preload(`img/turn/blue_${pad2(i)}.jpg`);
for(let i=38;i<72;i++) TURN.red[i]=preload(`img/turn/red_${pad2(i)}.jpg`);
for(let i=36;i<50;i++) TURN.mask[i]=preload(`img/turn/mask_${pad2(i)}.png`);
cue(880,'impact',{v:.55}); cue(881,'tick',{v:.2}); cue(883,'tick',{v:.25}); [895,901,910].forEach(f=>cue(f,'tick',{v:.2})); cue(917,'shimmer',{v:.45,end:928}); cue(917,'tick',{v:.2}); cue(922,'pop',{v:.45,n:79}); cue(918,'impact',{v:.3}); cue(940,'whoosh',{v:.6,peak:951,dur:12});
const CH_HOVER=[[895,898,'bolt','Steel bolts · ×8'],[901,907,'seat','Velvet · 380 g/m²'],[910,916,'back','Hand-tufted back']];
function chView3(f){ // caméra de la vue produit (réf) : recul + travelling flou à l'entrée, roulis, secousse au changement, anticipation, poussée finale
  const a=approach(f,880,10,0.25); let s=lerp(1.25,1,a), x=120*(1-a), y=0, r=3*(approach(f,892,4)-approach(f,898,6));
  y+=22*(approach(f,918,2,0.5)-approach(f,921,8)); const an=approach(f,936,3); s*=1-0.04*an; r-=2.4*an*(1-approach(f,940,4));
  const pu=accel(f,940,10,3); s*=1+0.8*pu; y-=150*pu; return {s,x,y,r,bx:vel(t=>120*(1-approach(t,880,10,0.25)),f), by:vel(t=>-150*accel(t,940,10,3),f)}; }
function shotChat(f){
  const i=clamp(f-880,0,71), swapped=f>=922, V=chView3(f);
  const tr=`translate(${V.x.toFixed(1)}px,${V.y.toFixed(1)}px) rotate(${V.r.toFixed(2)}deg) scale(${V.s.toFixed(4)})`;
  [chTurn,chTurnR,chThermal].forEach(c=>{ c.style.transform=tr; });
  chTurn.style.filter=Math.abs(V.bx)>1||Math.abs(V.by)>2?`blur(${Math.min(14,(Math.abs(V.bx)+Math.abs(V.by))*0.25).toFixed(1)}px)`:''; chTurnR.style.filter=chTurn.style.filter;
  seqDrawRaw(chTurn,TURN.blue[Math.min(47,i)]);
  // le nouveau tissu se résout de l'arrière vers l'avant (922-928)
  show(chTurnR,f>=922); if(f>=922){ seqDrawRaw(chTurnR,TURN.red[Math.max(38,i)]); const w=approach(f,922,6,0.3)*130; chTurnR.style.webkitMaskImage=chTurnR.style.maskImage=f<929?`linear-gradient(90deg,#000 ${(w-20).toFixed(0)}%,transparent ${w.toFixed(0)}%)`:''; }
  const th=f<917?0:f<919?(f-916)/2:f<922?1:1-clamp((f-922)/4); show(chThermal,th>0);
  if(th>0){ chThermal.style.opacity=th.toFixed(2); iriTo(chThermal,{t:T(f)*6,seed:4.7,zoom:1.2,hot:.6,bands:.8,therm:1});
    const m=TURN.mask[clamp(i,36,49)]; const t2=chThermal.getContext('2d'); t2.globalCompositeOperation='destination-in'; t2.drawImage(m,0,0,chThermal.width,chThermal.height); t2.globalCompositeOperation='source-over'; }
  chCol.textContent=swapped?'Red velvet':'Corporate blue'; chSw.style.background=swapped?VA:'#2D6CDF';
  // survol : le curseur visite le boulon, l'assise, le dossier ; une étiquette s'accroche au point (positions exportées du rendu)
  const H=TURNHOT[i]||TURNHOT[String(Math.min(47,i))]; let hv=null; for(const h of CH_HOVER) if(f>=h[0]&&f<=h[1]) hv=h;
  const P=k=>{ if(!H||!H[k]) return [1090,560]; const px=(H[k][0]-0.5)*918, py=(H[k][1]-0.5)*668, c=Math.cos(V.r*Math.PI/180), sn=Math.sin(V.r*Math.PI/180);
    return [630+459+V.x+V.s*(px*c-py*sn), 196+334+V.y+V.s*(px*sn+py*c)]; };
  show(chHot,!!hv); show(chTip,!!hv);
  if(hv){ const [hx,hy]=P(hv[2]); chHot.style.left=hx+'px'; chHot.style.top=hy+'px'; chHot.style.transform=`scale(${back(f,hv[0],4).toFixed(3)})`;
    chTip.textContent=hv[3]; chTip.style.left=(hx+44)+'px'; chTip.style.top=(hy-60)+'px'; chTip.style.opacity=approach(f,hv[0],3).toFixed(2); }
  let cxy=null; if(f>=893&&f<918){ const tg=f<899?P('bolt'):f<908?P('seat'):P('back'); const pv=f<899?[1300,900]:f<908?P('bolt'):P('seat'); const st=f<899?893:f<908?899:908; const k=approach(f,st,4,0.3); cxy=[lerp(pv[0],tg[0],k)+14,lerp(pv[1],tg[1],k)+14]; }
  cursor(cxy?cxy[0]:0,cxy?cxy[1]:0,0,!!cxy);
  // le fil : la bulle seule (880), réflexion + réponse (881), paquets + approbation teintée (883), défile de 13 px ; nouveau tour à 917
  const old=f<917, scr=-13*approach(f,881,9);
  chKids.forEach((k,j)=>{ if(j==0||j>=7) return; const t0=j==1?880:j<=3?881:883; k.style.visibility=old&&f>=t0?'visible':'hidden'; k.style.translate=`0 ${scr.toFixed(1)}px`; });
  chKids[1].style.background=mixc('#E8E1FF','#ECE8E3',approach(f,880,6)); chKids[6].style.background=mixc('#E8E1FF','#FFFFFF',approach(f,883,7));
  show(chNew,!old); if(!old){ chNewK.forEach((k,j)=>{ k.style.visibility=f>=[917,918,920][j]?'visible':'hidden'; }); }
  chKids.slice(8,11).forEach((c,j)=>{ c.textContent=f>=922?CH_SUG2[j]:['Add a sofa','Warmer light','Make it spin'][j]; });
}

/* ---------- 22-24 · Order Complete (vidéo Cycles) → plein cadre → le thermique naît du fauteuil → Taste Check → grille qui casse (réf, +2) ---------- */
const DO=scene('sDone',954,1079,f=>shotDone(f));
const cR22=cueAt(2);
const doFrame=el(DO.cam); const doD=framed(doFrame,tplVDone(),1362,918,1240,830,VINK);
function doIriTitle(root){ const t=q1(root,'.vhead'), c=t.cloneNode(true); c.classList.add('vhiri'); t.after(c); return [t,c]; }
const [doTitle,doTitleI]=doIriTitle(q1(doD,'.full')), doSeq=q1(doD,'.vseq'), doPills=qa(doD,'.vpill'), doSum=q1(doD,'.full>div:last-child');
const doFull=el(DO.cam,'','', 'position:absolute;inset:0;display:none;overflow:hidden');
const doFullIn=el(doFull,'','', `position:absolute;left:0;top:0;width:1240px;height:830px;transform-origin:0 0;background:${VINK}`); doFullIn.innerHTML=q1(doD,'.full').outerHTML;
const doFSeq=q1(doFullIn,'.vseq'), doFTitle=qa(doFullIn,'.vhead');
const doTh=canvas(DO.cam,960,540,'inset:0;width:1920px;height:1080px;display:none');
// à partir de 1003 : la même photo, passée dans une table « chaleur » (le fauteuil reste rouge : pas de retour au bleu)
const doTP=el(DO.cam,'','', 'position:absolute;inset:0;overflow:hidden;display:none'); const doTPi=el(doTP,'','', 'position:absolute;left:0;top:0;width:1240px;height:830px;transform-origin:0 0;filter:url(#gmHeat)'); doTPi.innerHTML=vimg('chair_hero','inset:0;width:100%;height:100%');
const doBtn=el(DO.cam,'abs','Start Taste Check','height:74px;line-height:74px;padding:0 42px;border-radius:18px;background:#151413;color:#F3EFEA;font-size:34px');
// grille irrégulière (colonnes 80-310 px, lignes serrées en haut et en bas), blocs « glitch » qui montrent des copies décalées et zoomées
const DO_COLS=(()=>{ const w=[80,140,310,120,200,90,260,150,180,110,230,140]; const a=[]; let x=0; for(const k of w){ x+=k; if(x<1920) a.push(x); } return a; })();
const DO_ROWS=[38,66,90,110,126,260,540,820,950,966,984,1006,1034];
const doGrid=el(DO.cam,'','', 'position:absolute;inset:0;display:none');
const doLines=[...DO_COLS.map(x=>el(doGrid,'gline','', `left:${x-1}px;top:0;width:2px;height:1080px;transform-origin:50% 50%`)),...DO_ROWS.map(y=>el(doGrid,'gline','', `left:0;top:${y-1}px;width:1920px;height:2px;transform-origin:50% 50%`))];
const doDots=[]; DO_COLS.forEach((x,i)=>DO_ROWS.forEach((y,j)=>{ const sz=lerp(21,5,clamp(Math.abs(y-540)/540)); doDots.push(el(doGrid,'gdot','', `left:${x}px;top:${y}px;width:${sz}px;height:${sz}px;margin:${-sz/2}px 0 0 ${-sz/2}px;border-radius:50%;box-shadow:0 0 ${sz}px rgba(255,255,255,.9)`)); }));
const doBlocks=[0,1,2,3,4,5,6,7].map(()=>{ const b=el(doGrid,'','', 'position:absolute;width:235px;height:287px;overflow:hidden;display:none'); const im=el(b,'','', 'position:absolute;left:0;top:0;width:1240px;height:830px;transform-origin:0 0;filter:url(#gmHeat)'); im.innerHTML=vimg('chair_hero','inset:0;width:100%;height:100%'); b._im=im; return b; });
const doMaskC=document.createElement('canvas'); doMaskC.width=960; doMaskC.height=540;
cR22(952,'impact',{v:.55}); cR22(978,'whoosh',{v:.5,peak:989,dur:11}); cR22(989,'swish',{v:.4,peak:990,dur:5}); cR22(995,'shimmer',{v:.5,end:1003}); cR22(1003,'impact',{v:.45});
cR22(1020,'pop',{v:.45,n:76}); cR22(1050,'click',{v:.95}); cR22(1052,'riser',{v:.5,end:1077}); for(let k=0;k<8;k++) cR22(1058+k*2.5,'tick',{v:.16});
const fullT=s=>`translate(${(960-560*s).toFixed(1)}px,${(540-300*s).toFixed(1)}px) scale(${s.toFixed(4)})`;
function shotDone(F){ const f=F-2;
  const card=f<989; show(doFrame,card); show(doFull,f>=989&&f<1003);
  // carte : entre à 0,95 en glissant de 50 px (952-966), tient en rampant (+0,12 %/i), puis poussée qui accélère ×1,19 (978-988)
  if(card){ const en=approach(f,952,14,0.2); const s=lerp(0.95,1,en)*(1+0.0012*Math.max(0,f-966))*(1+0.19*accel(f,978,11,3));
    place(doFrame,960+50*(1-en),540,s); const fu=q1(doD,'.full'); fu.style.transformOrigin='55% 60%'; fu.style.transform=`scale(${(1+0.12*accel(f,980,9,3)).toFixed(4)})`;
    seqDraw(doSeq,SEQ.done,f-952);
    doTitleI.style.opacity=(f<966?1-approach(f,952,14):0.7*approach(f,982,6)).toFixed(3); doTitleI.style.backgroundPosition=`${((f-952)*4)%300}% 50%`;
    doPills.forEach((p,i)=>{ if(i==1) p.style.background=f<960?'#FFA6C9':f<966?'#FF9A4D':VA; });
    doSum.style.clipPath=`inset(0 0 ${((1-approach(f,956,10))*100).toFixed(1)}% 0 round 18px)`; }
  // plein cadre : zoom qui ralentit (+8,5 %), le titre s'efface en dérivant ; le thermique naît du fauteuil (995-1002)
  if(f>=989&&f<1003){ const s=1.62*(1+0.085*approach(f,989,13)); doFullIn.style.transform=fullT(s); seqDraw(doFSeq,SEQ.done,f-952);
    doFTitle.forEach(t=>{ t.style.opacity=(1-approach(f,989,6)).toFixed(3); t.style.translate=`0 ${(-40*approach(f,989,6)).toFixed(1)}px`; }); }
  const thMask=f>=995&&f<1003, thFull=f>=1003; show(doTh,thMask||thFull);
  if(thMask||thFull){ iriTo(doTh,{t:T(f)*(thFull?5:2),seed:7.4,zoom:1.15,hot:.6,bands:.8,therm:1});
    if(thMask){ const m=SEQ.doneMask[clamp(f-952,43,56)], s=1.62*(1+0.085*approach(f,989,13)), g=approach(f,995,8,0.15);
      const mc=doMaskC.getContext('2d'); mc.clearRect(0,0,960,540); mc.filter=`blur(${(4+26*g).toFixed(1)}px)`;
      const w=1240*s*0.5, h=830*s*0.5, x0=(960-560*s)*0.5, y0=(540-300*s)*0.5, k=1+1.6*g; mc.drawImage(m,x0+w*(1-k)/2,y0+h*(1-k)/2,w*k,h*k); mc.filter='none';
      const t2=doTh.getContext('2d'); t2.globalCompositeOperation='destination-in'; t2.drawImage(doMaskC,0,0); t2.globalCompositeOperation='source-over'; doTh.style.opacity='1'; }
    else { doTh.style.opacity=lerp(0.55,0.3,approach(f,1003,8)).toFixed(3); doTh.style.mixBlendMode='soft-light'; } }
  // 1003 : coupe franche sur la photo en table thermique, qui continue de glisser ; défocalisation + blanchiment dès 1067
  show(doTP,thFull); if(thFull){ doTP.style.filter=`hue-rotate(${(18*(1-approach(f,1003,7))).toFixed(1)}deg)`; const s=1.62*1.085*(1+0.006*(f-1003)), pan=f<1062?0:f<1075?(f-1062)*15:13*15+(f-1075)*40, z=f<1075?1:1-0.045*(f-1075);
    doTPi.style.transform=`translate(${(960-560*s*z+pan).toFixed(1)}px,${(540-300*s*z+pan*0.6).toFixed(1)}px) scale(${(s*z).toFixed(4)})`;
    const df=approach(f,1067,10); if(df>0) doTP.style.filter=`blur(${(20*df).toFixed(1)}px) brightness(${(1+0.6*df).toFixed(2)}) saturate(${(1-0.6*df).toFixed(2)})`; }
  // le bouton : apparaît à 0,91, texte accent 1 image, grandit de 10 % ; clic 1050 = 1 image à 0,82, brun chaud qui reste
  const bOn=f>=1020&&f<1072; show(doBtn,bOn); if(bOn){ const sc=lerp(0.91,1,approach(f,1020,14))*(f==1050?0.82/1:f==1051?0.97:1);
    place(doBtn,960,556,sc); doBtn.style.color=f==1020?'#FF3D5E':'#F3EFEA'; doBtn.style.background=f>=1050?mixc('#151413','#FF3D5E',0.35):'#151413';
    mblur(doBtn,f>=1062?vel(t=>t<1062?0:(t-1062)**1.6*3,f)*3:0,0); doBtn.style.opacity=(1-approach(f,1064,8)).toFixed(3); }
  const cp=approach(f,1031,9,0.2); cursor(lerp(1180,1004,cp),lerp(860,582,cp),f==1050?1:0,f>=1031&&f<1066);
  const gOn=f>=1052; show(doGrid,gOn); if(gOn){ const lp=approach(f,1052,7); doLines.forEach((l,i)=>{ l.style.transform=i<DO_COLS.length?`scaleY(${lp.toFixed(3)})`:`scaleX(${lp.toFixed(3)})`; });
    doDots.forEach((d,i)=>{ d.style.transform=`scale(${back(f,1058+(i%7),5).toFixed(3)})`; });
    const key=Math.floor((f-1058)/2.5);
    doBlocks.forEach((b,i)=>{ const on=f>=1058&&f<1077&&i<3+Math.min(5,f-1058); show(b,on); if(!on) return; const r=rng(4000+key*13+i);
      const bx=r()*1685, by=r()*793, dx=20+r()*40, dy=20+r()*40, z=1.5+r()*1.5; b.style.left=bx+'px'; b.style.top=by+'px';
      b._im.style.transform=`translate(${(-bx+dx).toFixed(1)}px,${(-by+dy).toFixed(1)}px) scale(${(1.62*z).toFixed(3)})`; b.style.filter=doTP.style.filter; }); }
}

/* ---------- 25 · collage sur grille : la caméra recule et se pose (dérive bas-droite), tuiles vivantes, révélations jusqu'à 1116 (réf, +2) ---------- */
const GR=scene('sGrid',1080,1130,f=>shotGrid(f));
const cR25=cueAt(2);
const grIn=el(GR.cam,'','', 'position:absolute;left:0;top:0;width:2200px;height:1080px');
const grIri=[[2,4,1,1,1080],[7,0,1,1,1081],[3,7,1,1,1082],[16,5,1,1,1083],[1,8,1,1,1084],[8,7,1,1,1085],[17,2,1,1,1086],[5,6,1,1,1087],[8,1,6,6,1083]].map(([i,j,w,h,st],k)=>{ const c=canvas(grIn,120,80,`left:${i*120}px;top:${j*120}px;width:${w*120}px;height:${h*120}px;display:none`); c._st=st; c._k=k; return c; });
const grMacroTile=el(grIn,'','', 'position:absolute;left:960px;top:120px;width:720px;height:720px;display:none;filter:grayscale(1) contrast(1.25) brightness(1.05);overflow:hidden');
const grMacro=canvas(grMacroTile,720,720,'inset:0;width:100%;height:100%');
const grThumb2=el(grIn,'gcard','', 'left:1680px;top:600px;width:240px;height:240px;display:none;filter:grayscale(1) contrast(1.2)'); const grMacro2=canvas(grThumb2,240,240,'inset:0;width:100%;height:100%');
const GR_CH=[[0,120,220,60,1084,''],[600,486,230,56,1089,''],[1960,860,260,56,1095,'<span style="color:#FF3D5E">●</span>&nbsp; arial: 0'],[240,990,220,56,1092,'<span style="color:#FF3D5E">●</span>&nbsp; taste'],[1960,240,240,56,1098,'Low stock'],[720,240,140,56,1100,'1 accent'],[360,860,330,56,1104,'Living room · 24 m²'],[1700,120,300,56,1100,'Matching fabrics…']];
const grChips=GR_CH.map(([x,y,w,h,st,t])=>{ const d=el(grIn,'m',t,`position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:17px;line-height:${h}px;padding-left:22px;display:none;white-space:nowrap;overflow:hidden`); d._st=st; d._t=d.innerHTML; d._plain=d.textContent; return d; });
const grStat=el(grIn,'gcard','', 'left:240px;top:120px;width:360px;height:240px;display:none');
el(grStat,'abs m','SIGNUPS SINCE TASTE','left:24px;top:22px;font-size:12px;letter-spacing:.1em;color:#8E877F'); const grNum=el(grStat,'abs','+14%','left:20px;top:52px;font-size:96px;letter-spacing:-0.05em;line-height:1');
const grSpark=el(grStat,'','<svg width="310" height="70" viewBox="0 0 310 70"><path class="sp" fill="none" stroke="#FF3D5E" stroke-width="4" stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400"/></svg>','position:absolute;left:24px;top:156px'); const grSp=q1(grSpark,'.sp');
const grLine=el(grIn,'gcard','', 'left:0;top:360px;width:240px;height:240px;background:#151413;display:none');
el(grLine,'','<svg width="240" height="240" viewBox="0 0 240 240"><path class="lp" d="M20 190 L60 150 L90 165 L130 110 L165 120 L200 60 L225 40" fill="none" stroke="#FF3D5E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="320" stroke-dashoffset="320"/></svg>','position:absolute;inset:0');
const grPrice=el(grIn,'abs','<span class="m" style="font-size:14px;color:#8E877F">from</span> €890 <span style="display:inline-block;width:36px;height:36px;border-radius:18px;background:#151413;vertical-align:-8px;margin-left:8px"></span>','left:380px;top:510px;font-size:30px;display:none');
const grRight=el(grIn,'abs','', 'left:850px;top:870px;font-size:56px;letter-spacing:-0.03em;display:none'); el(grIn,'abs m','RETURNS %','left:852px;top:846px;font-size:13px;color:#8E877F');
const grCode=el(grIn,'gcard','', 'left:1680px;top:360px;width:240px;height:240px;background:#151413;display:none');
const GR_CODE=['taste.apply()','  .font("Inter")','  .accent(1)','  .ship()']; const grCodeL=GR_CODE.map((t,i)=>el(grCode,'abs m','',`left:18px;top:${24+i*30}px;font-size:15px;color:${i?'#BFB9B2':'#FF8FA3'}`));
const grBars=el(grIn,'gcard','', 'left:600px;top:600px;width:240px;height:240px;display:none'); const grBarE=[0,1,2,3,4].map(i=>el(grBars,'','', `position:absolute;left:${28+i*40}px;bottom:30px;width:24px;height:0;border-radius:6px 6px 2px 2px;background:${i==4?'#FF3D5E':'#151413'}`));
const grThumb=el(grIn,'gcard','', 'left:360px;top:0;width:120px;height:120px;background:#C9C3BD;display:none');
const grLines=[]; for(let i=0;i<=18;i++) grLines.push(el(grIn,'gline','', `left:${i*120-1}px;top:0;width:2px;height:1080px`));
// lignes horizontales qui se resserrent vers le bas (grille bombée), gros points aux croisements
[120,240,360,480,600,720,840,930,990,1030,1056].forEach(y=>grLines.push(el(grIn,'gline','', `left:0;top:${y-1}px;width:2200px;height:2px`)));
for(const y of [120,240,360,480,600,720,840,930,990,1030]) for(let i=0;i<=18;i++){ const sz=y<200||y>900?18:10; el(grIn,'gdot','', `left:${i*120}px;top:${y}px;width:${sz}px;height:${sz}px;margin:${-sz/2}px 0 0 ${-sz/2}px;border-radius:50%`); }
cR25(1078,'drop2',{}); cR25(1078,'impact',{v:.6}); [1084,1089,1092,1095,1098,1100,1104].forEach(f=>cR25(f,'tick',{v:.3})); for(let k=0;k<9;k++) cR25(1093+k*2.6,'tick',{v:.14});
function typed(d,f,st,cps=0.5){ const n=Math.floor((f-st)*cps)+1; return d._plain.slice(0,Math.max(0,n)); }
function shotGrid(F){ const f=F-2;
  const z1=lerp(1.25,1,approach(f,1078,14,0.2)), z2=lerp(1.03,1,approach(f,1100,14)); GR.cam.style.transform=`scale(${(z1*(f>=1100?z2:1.03)).toFixed(4)})`;
  const X=-313*(1-approach(f,1086,40,0.11)), Y=-300*(1-approach(f,1077,12,0.2));
  grIn.style.transform=`translate(${X.toFixed(1)}px,${Y.toFixed(1)}px)`;
  mblur(grIn,vel(t=>-313*(1-approach(t,1086,40,0.11)),f)*BLUR*0.6,vel(t=>-300*(1-approach(t,1077,12,0.2)),f)*BLUR*0.6);
  // tuiles irisées qui bouillonnent ; les petites s'éteignent d'ici 1094, la grande se fond à 50 % dans la macro à 1087
  grIri.forEach(c=>{ const on=f>=c._st&&(c._k<8?f<1094:f<1089); show(c,on); if(!on) return; iriTo(c,{t:T(f)*14,seed:3+c._k,zoom:1.3,hot:.5,bands:.5,therm:.5});
    c.style.opacity=(c._k<8?1-approach(f,1090,4):f>=1087?0.5:1).toFixed(3); });
  show(grMacroTile,f>=1087); if(f>=1087) seqDraw(grMacro,SEQ.macro,6+(f-1087)*0.9,0.56,0.46);
  show(grThumb2,f>=1100); if(f>=1100) seqDraw(grMacro2,SEQ.macro,30+(f-1100)*1.2,0.5,0.5,1.4);
  grChips.forEach(d=>{ const on=f>=d._st; show(d,on); if(!on) return; d.style.transform=`translateX(${((1-approach(f,d._st,6))*-60).toFixed(1)}px)`;
    if(d._plain) d.textContent=typed(d,f,d._st); if(d._plain&&d._t.includes('●')&&f>=d._st+d._plain.length*2) d.innerHTML=d._t; });
  show(grStat,f>=1093); grNum.textContent='+'+Math.round(lerp(14,45,1-Math.pow(1-clamp((f-1093)/23),1.4)))+'%'; show(grThumb,f>=1093);
  grSp.setAttribute('d','M0 60 '+[...Array(32)].map((_,k)=>{ const x=k*10, y=60-56*(x/310)**1.3+(f>1110?4*Math.sin(0.35*f+x/40):0); return `L${x} ${y.toFixed(1)}`; }).join(' '));
  grSp.setAttribute('stroke-dashoffset',(400*(1-approach(f,1100,10))).toFixed(1));
  show(grLine,f>=1096); q1(grLine,'.lp').setAttribute('stroke-dashoffset',(320*(1-approach(f,1099,12))).toFixed(1));
  show(grPrice,f>=1101); show(grRight,f>=1094); grRight.textContent=lerp(6.5,2.8,clamp((f-1094)/16)).toFixed(1);
  show(grCode,f>=1104); grCodeL.forEach((d,i)=>{ const st=1104+i*3; d.textContent=f>=st?GR_CODE[i].slice(0,(f-st+1)*5):''; });
  show(grBars,f>=1098); grBarE.forEach((b,i)=>{ b.style.height=(lerp(0,[60,90,70,120,170][i],approach(f,1098+i*1.5,6))).toFixed(1)+'px'; });
}

/* ---------- 26 · BrandReport → Apply taste : fond qui file, poussée qui ralentit, la carte se pose, la ligne se tape (réf, +1) ---------- */
const RE=scene('sReport',1131,1175,f=>shotReport(f));
const cR26=cueAt(1);
const reBg=canvas(RE.cam,960,540,'inset:0;width:1920px;height:1080px'); el(RE.cam,'full','', 'background:linear-gradient(180deg,rgba(246,241,236,.25) 0%,rgba(246,241,236,.85) 28%,rgba(246,241,236,.85) 62%,rgba(246,241,236,.25) 100%)');
const reGrid=el(RE.cam,'full',''); for(let i=1;i<16;i++) el(reGrid,'gline','', `left:${i*120-1}px;top:0;width:2px;height:1080px`); for(let j=1;j<9;j++) el(reGrid,'gline','', `left:0;top:${j*120-1}px;width:1920px;height:2px`);
const reCard=el(RE.cam,'rcard'); reCard.innerHTML=`<div style="position:absolute;left:36px;top:30px;font-size:38px;letter-spacing:-0.02em">BrandReport <span class="m rpub" style="font-size:16px;color:#8E877F;margin-left:10px">● public</span></div>
  <div style="position:absolute;left:36px;top:92px;font-size:24px;color:#8E877F;font-weight:400"><span style="color:#FF3D5E">⊘</span>&nbsp; 47 boring issues found</div>
  <div style="position:absolute;left:24px;right:24px;bottom:28px;height:100px;border-radius:16px;background:#F4F1ED"><span class="m rrow" style="position:absolute;left:24px;top:40px;font-size:17px;color:#6d6760"></span></div>`;
const reRow=q1(reCard,'.rrow'), rePub=q1(reCard,'.rpub'), RE_ROW='arial · #2D6CDF · drop shadows · stock photos';
const reGlass=el(reCard,'','', 'position:absolute;inset:0;border-radius:22px;background:rgba(169,231,242,.55);pointer-events:none');
const reBtn=el(reCard,'abs','Apply taste','left:auto;right:44px;top:206px;height:62px;line-height:62px;padding:0 28px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:24px');
cR26(1130,'impact',{v:.5}); cR26(1161,'click',{v:1}); cR26(1162,'pop',{v:.5,n:84}); for(let k=0;k<4;k++) cR26(1134+k*2,'key',{v:.15});
function shotReport(F){ const f=F-1;
  RE.cam.style.transform=`scale(${(1+0.08*approach(f,1131,36,0.09)).toFixed(4)})`;
  const sp=f<1166?11:11+(f-1166)*3.5; iriTo(reBg,{t:T(1130)+(f-1130)/FPS*sp,seed:9.4,zoom:0.7,hot:.05,bands:.9},[240,0,480,540]);
  reGrid.style.opacity=(1-approach(f,1130,6)).toFixed(3);
  const p=approach(f,1130,6); place(reCard,960,545); reCard.style.opacity=lerp(0.3,1,p).toFixed(3); reGlass.style.opacity=(1-p).toFixed(3);
  rePub.style.visibility=f>=1134?'visible':'hidden'; reRow.textContent=RE_ROW.slice(0,Math.max(0,Math.floor((f-1131)*4.2)));
  // clic 1161→1162 : encre teintée vers l'accent, 0,955 une image, revient en 3 images
  const pr=f==1162?0.955:f>1162?lerp(0.97,1,approach(f,1162,3)):1; reBtn.style.transform=`scale(${pr.toFixed(4)})`; reBtn.style.background=f>=1162?mixc('#151413','#FF3D5E',0.25):'#151413';
  const cin=approach(f,1145,3); cursor(1262+18*(1-cin),630+18*(1-cin),f==1162?1:0,f>=1145); CUR.style.opacity=cin.toFixed(2);
}

/* ---------- 27 · alertes : apparition radiale, bascule au hasard, contraction tardive et rapide, la marque sans rebond (réf, +1) ---------- */
const AL=scene('sAlerts',1176,1250,f=>shotAlerts(f),'dark');
const cR27=cueAt(1);
const alBg=canvas(AL.cam,960,540,'inset:0;width:1920px;height:1080px');
const AL_I=[`<svg viewBox="0 0 42 42" width="42" height="42"><path d="M21 5 L38 36 H4 Z" fill="#E5484D"/><path d="M21 16 V26 M21 30 V31" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/></svg>`,
  `<svg viewBox="0 0 42 42" width="42" height="42"><path d="M21 5 L38 36 H4 Z" fill="none" stroke="#C175A1" stroke-width="3" stroke-linejoin="round"/></svg>`,
  `<svg viewBox="0 0 42 42" width="42" height="42"><path d="M21 4 L35 9 V20 Q35 31 21 38 Q7 31 7 20 V9 Z" fill="none" stroke="#FF9A4D" stroke-width="3"/><path d="M21 14 V23 M21 27 V28" stroke="#FF9A4D" stroke-width="3" stroke-linecap="round"/></svg>`];
const AL_OK='<svg viewBox="0 0 42 42" width="42" height="42"><circle cx="21" cy="21" r="13" fill="#FF3D5E"/><path d="M17 27 L25 15" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/></svg>';
const alIcons=[]; let alMax=0; for(let j=0;j<6;j++) for(let i=0;i<15;i++){ const x=204+i*108, y=271+j*108; el(AL.cam,'gdot','', `left:${x}px;top:${y}px;width:4px;height:4px;margin:-2px 0 0 -2px;background:#4A4643`);
  const dx=(x-960)/760, dy=(y-541)/330; if(dx*dx+dy*dy>1) continue; const r=rng(1200+j*15+i); if(r()<0.18) continue;
  const d=el(AL.cam,'alert'); d._x=x; d._y=y; d._dist=Math.hypot(x-960,y-541); alMax=Math.max(alMax,d._dist); d._kind=(r()*3)|0; d._b=1187+25*Math.pow(r(),2.2); alIcons.push(d); }
alIcons.forEach(d=>{ d._a=1174+13*d._dist/alMax; });
const AL_SLOTS=[]; [3,5,3,2].forEach((n,row)=>{ for(let k=0;k<n;k++) AL_SLOTS.push([960+(k-(n-1)/2)*85,540+(row-1.5)*85]); });
alIcons.map(d=>[d._dist,d]).sort((a,b)=>a[0]-b[0]).forEach(([,d],k)=>{ d._rank=k; d._slot=AL_SLOTS[k]||null; });
const alMark=el(AL.cam,'abs','', 'width:150px;height:150px'); alMark.innerHTML=MARK_SVG;
const alFade=el(AL.s,'','', 'position:absolute;left:0;right:0;bottom:0;height:430px;background:linear-gradient(transparent,#3C3C3C);opacity:0');
cR27(1175,'hush',{}); for(let k=0;k<5;k++) cR27(1188+k*5,'tick',{v:.25}); cR27(1226,'reverse',{v:.6,end:1232}); cR27(1232,'boom',{v:.8});
function shotAlerts(F){ const f=F-1; push(AL.cam,f,1175,0.0007);
  iriTo(alBg,{t:f<1188?T(f)*6:T(1188)*6+(f-1188)/FPS*1.2,seed:5.9,zoom:0.8,hot:.4,bands:.3}); alBg.style.opacity=lerp(1,0.05,approach(f,1175,12)).toFixed(3); alBg.style.filter='brightness(.32) saturate(1.5)';
  const cv=approach(f,1226,5,0.25), n=alIcons.length;
  alIcons.forEach(d=>{ const cull=f>=1226&&d._rank>=Math.round(lerp(n,13,clamp((f-1226)/4))); const on=f>=d._a&&f<1232&&!cull; show(d,on); if(!on) return;
    d.innerHTML=f>=d._b?AL_OK:AL_I[d._kind];
    const k=lerp(1,0.73,cv), px=960+(d._x-960)*k, py=541+(d._y-541)*k, tg=d._slot?[lerp(px,d._slot[0],clamp((f-1228)/3)),lerp(py,d._slot[1],clamp((f-1228)/3))]:[px,py];
    d.style.left=tg[0]+'px'; d.style.top=tg[1]+'px'; d.style.transform=`scale(${back(f,d._a,4).toFixed(3)})`; });
  show(alMark,f>=1232); if(f>=1232) place(alMark,960,540,lerp(1.04,1,approach(f,1232,6)));
  alFade.style.opacity=approach(f,1243,7).toFixed(3);
}

/* ---------- 28 · ciel qui bascule (le bouton reste fixe), « Ship it » (réf, +1) ---------- */
const SH=scene('sShip',1251,1307,f=>shotShip(f));
const cR28=cueAt(1);
const shSky=el(SH.cam,'','', 'position:absolute;left:-60px;right:-60px;top:-60px;height:2100px;background:linear-gradient(180deg,#6FA6BC 0%,#B9D3DC 9%,#F1E6DC 26%,#F3E2D5 42%,#EFD9D0 50%,#DCE2E2 58%,#C6DCE4 72%,#B3D1DE 100%)');
el(shSky,'haze','', 'top:1240px;height:120px;background:rgba(255,236,226,.55)');
const shBtn=el(SH.s,'bbtn','Ship it'); shBtn.style.zIndex=5;
cR28(1250,'impact',{v:.5}); cR28(1295,'click',{v:1}); cR28(1298,'riser',{v:.55,end:1306});
function shotShip(F){ const f=F-1;
  shSky.style.transform=`translateY(${(-900*approach(f,1250,36,0.11)).toFixed(1)}px)`;
  const pr=f==1295; place(shBtn,960,540,pr?0.94:1); shBtn.style.background=f>=1295?mixc(mixc('#151413','#FF3D5E',0.3),'#151413',approach(f,1295,6)):'#151413';
  const cin=clamp((f-1270)/2), cp=approach(f,1270,10,0.2); cursor(lerp(1185,1007,cp),lerp(705,605,cp),pr?1:0,f>=1270); CUR.style.opacity=cin.toFixed(2);
}

/* ---------- 29-30 · montage (ordre de la réf) : profil · planning · Build your Room · landing ; chaque sous-plan a sa propre caméra (réf, +1) ---------- */
const MO=scene('sMont',1308,1378,f=>shotMont(f)); sky(MO.cam);
const cR29=cueAt(1);
const moP=el(MO.cam); const moPD=framed(moP,tplVProfile(),1368,912,1240,730,VINK);
const moR=el(MO.cam); framed(moR,tplPlan(),1368,912,1920,1080,'#F6F2EE');
const moDa=el(MO.cam); framed(moDa,tplVRoom(),1368,912,1240,730,'#F2EDE6'); qa(moDa,'.vroute').forEach(p=>p.setAttribute('stroke-dashoffset','0'));
const moL=el(MO.cam); const moLD=framed(moL,tplVLanding(),1368,912,1240,730,VINK);
const moTint=canvas(moL,240,160,'inset:0;width:100%;height:100%;border-radius:18px;mix-blend-mode:soft-light;display:none');
const moPSeq=q1(moPD,'.vseq'), moLSeq=q1(moLD,'.vseq'), moLh=q1(moLD,'.lnh'), moLT=qa(moLD,'.vtile');
const moRows=qa(moPD,'.full>div:nth-last-child(3)>div'), moStats=qa(moPD,'.full>div[style*="height:92px"] > div:first-child');
const MOS=[[moP,1307],[moR,1325],[moDa,1336],[moL,1349]];
cR29(1307,'impact',{v:.7}); cR29(1325,'impact',{v:.6}); cR29(1336,'impact',{v:.6}); cR29(1349,'impact',{v:.7}); [1312,1314,1315].forEach(f=>cR29(f,'tick',{v:.2})); cR29(1372,'shimmer',{v:.45,end:1378});
const MO_ST=[['12',13,1312],['€8,940','€9,830',1314],['3',4,1315]];
function shotMont(F){ const f=F-1; let cur=MOS[0]; for(const m of MOS) if(f>=m[1]) cur=m;
  MOS.forEach(m=>show(m[0],m===cur)); const a=f-cur[1];
  let sc=1; if(cur[0]===moP) sc=1+0.035*approach(f,1307,18,0.12); else if(cur[0]===moR) sc=1+0.0007*a; else if(cur[0]===moDa) sc=1+0.0004*a; else sc=1-0.03*accel(f,1366,10,2);
  place(cur[0],960,540,sc);
  if(cur[0]===moP){ seqDraw(moPSeq,SEQ.land,20+a*1.2,0.5,0.62);
    moRows.forEach((r,i)=>{ const p=approach(f,1307+i,4,0.3); r.style.translate=`0 ${((1-p)*80).toFixed(1)}px`; r.style.opacity=p.toFixed(2); r.style.color=f<1307+i+3?'#FF3D5E':''; });
    moStats.forEach((s,i)=>{ const [v0,v1,t]=MO_ST[i]; s.textContent=f>=t?String(v1):String(v0); }); }
  if(cur[0]===moL){ seqDraw(moLSeq,SEQ.land,a*1.0,0.5,0.58); moLh.style.transform=`translateX(${(-2.3*a).toFixed(1)}px)`;
    moLT.forEach((t,i)=>{ const p=approach(f,1350+i,8,0.2); t.style.translate=`0 ${((1-p)*24).toFixed(1)}px`; }); }
  setTint(moTint,{t:T(f)*3,seed:5.2,zoom:1.2,hot:.2,bands:.7},0.6*approach(f,1374,3));
}

/* ---------- 31-32 · fragments → glyphes → marque → « vladan » → pill → e-mail (réf, scène recalée +2) ---------- */
const OU=scene('sOutro',1380,1559,f=>shotOutro(f));
const cR31=cueAt(2);
const ouFr=FRAGS.map((t,i)=>{ const d=el(OU.cam,'abs frag'); d.textContent=t; const r=rng(700+i); let x,y; do{ x=60+r()*1660; y=110+r()*860; }while(Math.abs(x+120-960)<380&&Math.abs(y-540)<90); d._x=x; d._y=y; d.style.color=r()<.4?GACC:GINK; return d; });
const ouGl=gset(16,77,420,190).map(g=>{ const d=el(OU.cam,'abs c glyph'); d._g=g; d.textContent=g[0]; d.style.color=g[3]; return d; });
const ouDot=el(OU.cam,'abs','', 'border-radius:50%');
const ouMark=el(OU.cam,'abs','', 'width:81px;height:81px'); ouMark.innerHTML=MARK_SVG;
const ouWord=el(OU.cam,'abs','vladan','font-size:84px;font-weight:600;letter-spacing:-0.04em;line-height:1');
// pill en SVG : contour dont la couleur balaie de droite à gauche puis qui se dé-trace
const ouPill=el(OU.cam,'abs',`<svg width="100%" height="100%" style="overflow:visible"><defs><linearGradient id="ouG" gradientUnits="objectBoundingBox" x1="0" x2="1"><stop offset="0" stop-color="#151413"/><stop offset="0.25" stop-color="#151413"/><stop offset="0.45" stop-color="#FF9A4D"/><stop offset="0.6" stop-color="#FFA6C9"/><stop offset="0.75" stop-color="#B9A8FF"/><stop offset="1" stop-color="#B9A8FF"/></linearGradient></defs><rect x="1.75" y="1.75" rx="41.5" pathLength="1" fill="none" stroke="#151413" stroke-width="3.5"/></svg>`,'height:86px;overflow:visible');
const ouRect=q1(ouPill,'rect'), ouGrad=q1(ouPill,'linearGradient');
const OUW=[[1448,'Give'],[1453,'it'],[1467,'<em style="font-size:58px;color:#FF3D5E">taste.</em>']];
const ouWords=OUW.map(([f,h])=>el(OU.cam,'abs',h,'font-size:48px;line-height:1'));
const ouMail=el(OU.cam,'abs','vladan<span style="color:#FF3D5E">@</span>kwinndo.fr','font-size:44px;letter-spacing:-0.02em;line-height:1');
const ouSub=el(OU.cam,'abs m','brand · UI · motion for SaaS','font-size:18px;color:#8E877F');
let OUL={};
function outroLayout(){ OUL.ws=ouWords.map(e=>e.offsetWidth); OUL.ww=ouWord.offsetWidth; OUL.mw=ouMail.offsetWidth; OUL.sw=ouSub.offsetWidth; }
cR31(1378,'shimmer',{v:.35,end:1386}); cR31(1385,'reverse',{v:.6,end:1393}); cR31(1393,'boom',{v:1.15}); cR31(1408,'shimmer',{v:.4,end:1416});
OUW.forEach(([f],i)=>cR31(f,i==2?'pluck':'tick',{n:84,v:i==2?.55:.4})); cR31(1439,'swish',{v:.3,peak:1446,dur:7}); cR31(1481,'shimmer',{v:.3,end:1489}); cR31(1492,'final',{}); cR31(1492,'swish',{v:.3,peak:1495,dur:8});
const DOT_C=['#B9A8FF','#FFA6C9','#FFC7A1','#FF3D5E'];
function shotOutro(F){ const f=F-2; push(OU.cam,f,1378,0.0008);
  // code dense (1378-1380), puis une couche clairsemée (1381-1384)
  ouFr.forEach((d,i)=>{ const on=f<1381||(f<1385&&i%2==0); show(d,on); if(on){ placeTL(d,d._x+(d._x<960?1:-1)*(f-1378)*6,d._y); d.style.opacity=f<1381?'1':'0.45'; } });
  // anneau de glyphes net (1385-1386) qui se contracte et passe au pastel (1387-1391), sans flou
  const k=lerp(1,0.7,approach(f,1387,6)); ouGl.forEach((d,i)=>{ const on=f>=1385&&f<1392; show(d,on); if(!on) return; const g=d._g; place(d,960+g[1]*k,540+g[2]*k);
    d.style.color=f>=1389?['#FFA6C9','#B9A8FF','#A9E7F2','#FFC7A1'][i%4]:g[3]; });
  // le point change de couleur à chaque image : lilas, rose, pêche, accent ; la marque à 1398
  const dOn=f>=1390&&f<1398; show(ouDot,dOn); if(dOn){ const S=f<1394?lerp(90,120,(f-1390)/4):lerp(120,81,approach(f,1394,4)); Object.assign(ouDot.style,{width:S+'px',height:S+'px',background:DOT_C[Math.min(3,f-1390)],filter:f<1392?'blur(4px)':''}); place(ouDot,960,540); }
  const tot=81+24+OUL.ww; const slide=approach(f,1404,4); const logoOn=f>=1398&&f<1448;
  show(ouMark,logoOn); show(ouWord,logoOn&&f>=1408);
  if(logoOn){ // le mot pose (+12 px, ×1,035), son dégradé chaud sèche jusqu'à l'encre ; anticipation de sortie 1439-1446 ; dissolution depuis la marque 1445-1447
    const an=accel(f,1439,8,2), ex=-40*an, es=1-0.04*an, st=approach(f,1408,9);
    const mx=lerp(960,960-tot/2+40.5,slide)+ex; place(ouMark,mx,540,(f<1400?lerp(0.9,1,(f-1398)/2):1)*es);
    if(f>=1408){ placeTL(ouWord,mx+40.5+24+12*st,540-42,es*(1+0.035*st)); const dry=approach(f,1408,16);
      ouWord.style.background=dry<1?`linear-gradient(90deg,${mixc('#FF9A4D','#151413',dry)},${mixc('#7A2A10','#151413',dry)})`:''; ouWord.style.webkitBackgroundClip=ouWord.style.backgroundClip=dry<1?'text':''; ouWord.style.color=dry<1?'transparent':'';
      const ds=clamp((f-1445)/3); ouWord.style.webkitMaskImage=ouWord.style.maskImage=ds>0?`linear-gradient(90deg,transparent ${(ds*100-10).toFixed(0)}%,#000 ${(ds*100+10).toFixed(0)}%)`:''; ouMark.style.opacity=(1-ds).toFixed(2); } }
  // la pill naît avec son premier mot ; après chaque mot le groupe se recentre avec une traîne et une petite pulsation
  let k2=-1; OUW.forEach(([wf],i)=>{ if(f>=wf) k2=i; }); const sp=12, pad=30;
  const TW=OUW.map((_,i)=>OUL.ws.slice(0,i+1).reduce((a,b)=>a+b+sp,0)-sp);
  let tw=TW[0]; for(let i=1;i<OUW.length;i++) tw=lerp(tw,TW[i],approach(f,OUW[i][0],9,0.5));
  const pulse=k2>=0?1+0.02*(1-approach(f,OUW[k2][0],8)):1, pw=(tw+2*pad)*pulse;
  const pOn=f>=1448&&f<1490; show(ouPill,pOn); if(pOn){ Object.assign(ouPill.style,{width:pw+'px',left:(960-pw/2)+'px',top:(540-43*pulse)+'px',height:(86*pulse)+'px'});
    ouRect.setAttribute('width',Math.max(0,pw-3.5)); ouRect.setAttribute('height',86*pulse-3.5);
    const sw=clamp((f-1481)/6); ouRect.setAttribute('stroke',sw>0?'url(#ouG)':'#151413'); ouGrad.setAttribute('x1',(1-1.2*sw).toFixed(3)); ouGrad.setAttribute('x2',(2-1.2*sw).toFixed(3));
    ouRect.setAttribute('stroke-dasharray','1'); ouRect.setAttribute('stroke-dashoffset',(-clamp((f-1486)/3)).toFixed(3)); }
  let cx=960-tw/2*pulse; ouWords.forEach((d,i)=>{ show(d,i<=k2&&f<1490); if(i>k2) return; placeTL(d,cx,540-26-(i==2?6:0),pulse); cx+=(OUL.ws[i]+sp)*pulse;
    d.style.color=i==0?mixc('#FF3D5E','#151413',approach(f,1448,12)):''; });
  show(ouMail,f>=1492); if(f>=1492){ const p=approach(f,1492,9); placeTL(ouMail,960-OUL.mw/2,630+(1-p)*40); ouMail.style.clipPath=`inset(-10px -10px ${((1-p)*100).toFixed(0)}% -10px)`; mblur(ouMail,0,vel(t=>(1-approach(t,1492,9))*40,f)*BLUR); }
  show(ouSub,f>=1504); if(f>=1504){ const p=approach(f,1504,9); placeTL(ouSub,960-OUL.sw/2,704+(1-p)*20); ouSub.style.clipPath=`inset(-10px -10px ${((1-p)*100).toFixed(0)}% -10px)`; }
}

