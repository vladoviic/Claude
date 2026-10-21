/* ============================================================
   Plans 17 à 32
   ============================================================ */

/* ---------- 17-19 · terminal : npm rm boring --force → add motion → éditeur (numéros de la réf : scène recalée +1) ---------- */
const TE=scene('sTerm',696,815,f=>shotTerm(f),'dark');
const cR17=cueAt(1);
const ARROW=(w,h)=>`<svg width="${w}" height="${h}" viewBox="0 0 240 170"><path d="M14 85 H210 M140 20 L214 85 L140 150" fill="none" stroke="#F3EFEA" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
const teGhost=el(TE.cam,'abs','<em>taste.</em>','font-size:520px;color:#fff;opacity:.03;left:0;top:0;line-height:1');
const teBig=el(TE.cam,'abs',ARROW(240,170),'line-height:0');
const teBigCaret=el(TE.cam,'abs','', 'width:30px;height:280px;border-radius:4px');
const teLine=el(TE.cam,'abs tt'); const teBox=el(TE.cam,'tpanel','', 'border-color:#3A3633;display:none');
const tePanel=el(TE.cam,'tpanel'); const teDim1=el(tePanel,'abs','<span style="color:#CFC8BF">taste.ts</span>&nbsp;&nbsp;velvetly / src','left:26px;top:20px;font-family:FM;font-size:15px;color:#5A544E');
const teDim2=el(tePanel,'abs','ln 6 · utf-8 · typescript','right:26px;bottom:16px;left:auto;font-family:FM;font-size:14px;color:#4A4541');
const teSide=el(tePanel,'','', 'position:absolute;left:0;top:0;bottom:0;width:64px;border-right:1px solid #2C2C2C;display:none');
for(let k=0;k<5;k++) el(teSide,'','', `position:absolute;left:20px;top:${70+k*56}px;width:24px;height:24px;border-radius:6px;border:2px solid ${k==1?'#F3EFEA':'#3E3B38'}`);
const tePanelLine=el(TE.cam,'abs tt','', 'font-size:84px');
// coloration à l'encre : mots-clés papier, chaînes en italique, commentaires et « taste » en Besley (la loi : Besley Italic = le goût)
const CODE=[['<span class="k">export const</span> <span class="t">taste</span> = {',0],['  font: <span class="s">"Inter Display"</span>,',1],['  accent: <span class="sq"></span><span class="s">"#FF3D5E"</span>,  <span class="c">// one. used well.</span>',2],['  ease: <span class="s">"out"</span>,',3],
  ['  motion: { arrive: <span class="s">"fast"</span>, land: <span class="s">"soft"</span> },',4],['  arial<span class="colon"><svg viewBox="0 0 60 100"><circle cx="30" cy="47.75" r="6.25"/><circle cx="30" cy="93.75" r="6.25"/></svg></span> <span class="k">false</span>,',5],['  stockPhotos: <span class="n">0</span>,',6],['};',7],['',8],['app.use(<span class="t">taste</span>);  <span class="c">// the whole trick</span>',9],['<span class="k">export default</span> velvetly;',10],['<span class="c">// before: font-family: Arial;</span>',11]];
const GUT=i=>`<span class="n" style="display:inline-block;width:64px">${i+1}</span>`;
// les n premiers caractères visibles d'une ligne colorée (les balises passent telles quelles)
function sliceHTML(h,n){ let o='',k=0; for(let i=0;i<h.length;i++){ if(h[i]=='<'){ const j=h.indexOf('>',i); o+=h.slice(i,j+1); i=j; continue; } if(k>=n) continue; o+=h[i]; k++; } return o; }
const CODE_T=[767,767,767,767,773,784,784,788,788,792,796,799];   // arrivées par paquets (réf)
const teCode=CODE.map(([h,i])=>{ const d=el(tePanel,'cline'); d._h=GUT(i)+h; d.innerHTML=d._h; return d; });
const teSel=el(tePanel,'','', 'position:absolute;top:0;height:40px;border-radius:6px;background:rgba(243,239,234,.13)');
const teTok=el(tePanel,'','', 'position:absolute;top:0;height:40px;border-radius:6px;background:rgba(243,239,234,.12)');
/* l'aperçu en direct : le site du fondateur (bleu, Arial, poignée de main) se recharge à chaque ligne de code.
   font (769) : les polices basculent ; accent (771) : le bleu passe à l'encre, un seul rouge apparaît ;
   motion (784) : les blocs ré-arrivent vite et se posent doucement ; arial: false (786) : le dernier Arial tombe ;
   stockPhotos: 0 (788) : la photo de stock tombe à son tour, le fauteuil était dessous */
const TP_BLUE='#2D6CDF', TP_INK='#151413';
const tpPair=(css,a,b)=>`<div class="tpp" style="${css}"><span class="a">${a}</span><span class="b">${b}</span></div>`;
const tePrev=el(tePanel,'','', 'position:absolute;left:0;top:0;width:600px;height:640px;border-radius:14px;overflow:hidden;background:#1C1B1A;box-shadow:0 0 0 1px #2C2C2C;transform-origin:0 0;display:none');
tePrev.innerHTML=`<div style="position:absolute;left:18px;top:0;height:40px;line-height:40px;font-family:FM;font-size:13px;color:#6E6862">localhost:5173<span style="color:#45403C"> / velvetly</span></div>
  <div style="position:absolute;right:18px;top:0;height:40px;line-height:40px;font-family:FM;font-size:13px;color:#6E6862"><span class="tpDot" style="display:inline-block;width:8px;height:8px;border-radius:4px;background:#4A4542;margin-right:8px;vertical-align:1px"></span>live</div>
  <div class="tpBar" style="position:absolute;left:0;top:38px;height:2px;width:0;background:#F3EFEA"></div>
  <div class="tpPage" style="position:absolute;left:0;top:40px;width:600px;height:600px;overflow:hidden;background:#fff">
    ${tpPair('left:24px;top:20px;width:220px;height:32px','<span class="ar" style="font-weight:700;font-size:22px;line-height:32px">velvetly</span>',
      `<span style="font-family:ID;font-weight:600;font-size:22px;line-height:32px;letter-spacing:-0.035em"><span class="tpMk" style="display:inline-block;width:0;height:13.6px;border-radius:4.4px;background:${VA};vertical-align:0"></span>velvetly</span>`)}
    ${tpPair('right:24px;top:24px;width:330px;height:24px','<span class="ar" style="font-size:13px;line-height:24px;word-spacing:14px">Home Products About Contact</span>','<span style="font-family:ID;font-size:13px;line-height:24px;word-spacing:16px">Product Customers Pricing</span>')}
    ${tpPair('left:24px;top:86px;width:560px;height:172px','<span class="ar" style="font-weight:700;font-size:40px;line-height:1.12;color:#1F2A44">Furniture Planning<br>Software For Your<br>Business</span>',
      `<span style="font-family:ID;font-weight:500;font-size:78px;line-height:.98;letter-spacing:-0.055em">Plan with<br>${VMARK(58)} <em style="font-size:76px">taste.</em></span>`)}
    ${tpPair('left:24px;top:272px;width:560px;height:24px','<span class="ar" style="font-size:15px;line-height:24px;color:#6B7280">The #1 solution for all your furniture needs!</span>','<span style="font-family:FM;font-size:12.5px;line-height:24px;color:#8E877F">Room planner · 3D hero · AR · one line of JS</span>')}
    <div class="tpBtn" style="position:absolute;left:24px;top:312px;height:46px">${tpPair('left:0;top:0;width:100%;height:100%','<span class="ar" style="display:block;width:100%;text-align:center;font-weight:700;font-size:15px;line-height:46px;color:#fff">Get Started Today!</span>','<span style="display:block;width:100%;text-align:center;font-family:ID;font-weight:500;font-size:15px;line-height:46px;color:#F3EFEA">Book a demo →</span>')}</div>
    <div class="tpImg" style="position:absolute;left:24px;top:384px;width:552px;height:178px;overflow:hidden"><img src="img/chair_hero.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 58%"></div>
    <div class="tpPh" style="position:absolute;left:24px;top:384px;width:552px;height:178px;background:#D9DCE1;transform-origin:30% 100%"><svg width="70" height="56" viewBox="0 0 120 96" style="position:absolute;left:241px;top:44px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="5"/><circle cx="84" cy="30" r="10" fill="#A9AEB6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg><div class="ar" style="position:absolute;left:0;right:0;top:112px;text-align:center;font-size:12px;color:#8A8F97">stock_handshake_final_v3.jpg</div></div>
    <div class="tpFoot ar" style="position:absolute;left:24px;top:574px;font-size:11px;color:#9AA0A8;white-space:pre">${[...'© 2024 velvetly Inc. All rights reserved.'].map(c=>`<span style="display:inline-block">${c==' '?'&nbsp;':c}</span>`).join('')}</div>
  </div>`;
const TP={pairs:qa(tePrev,'.tpp'),page:q1(tePrev,'.tpPage'),mk:q1(tePrev,'.tpMk'),vmk:q1(tePrev,'.vmk'),btn:q1(tePrev,'.tpBtn'),img:q1(tePrev,'.tpImg'),ph:q1(tePrev,'.tpPh'),
  foot:qa(q1(tePrev,'.tpFoot'),'span'),dot:q1(tePrev,'.tpDot'),bar:q1(tePrev,'.tpBar')};
const TP_RELOAD=[769,771,784,786,788];
function tePrevUpdate(f){
  const pF=k=>vl(f,769+k*0.7,4), pA=vl(f,771,4), pop=pA*(1+0.28*Math.sin(Math.PI*pA));
  // les polices glissent (même geste que les composants du dashboard), le haut part en haut, le bas arrive par le bas
  TP.pairs.forEach((d,k)=>{ const p=pF(k), H=d.offsetHeight; d.children[0].style.transform=`translateY(${(-p*H).toFixed(1)}px)`; d.children[1].style.transform=`translateY(${((1-p)*H).toFixed(1)}px)`; });
  const [lo,nav,hd]=TP.pairs; lo.children[0].style.color=TP_BLUE; lo.children[1].style.color=mixc(TP_BLUE,TP_INK,pA);
  nav.children[0].style.color='#5A6270'; nav.children[1].style.color=mixc('#5A6270',TP_INK,pA); hd.children[1].style.color=mixc('#1F2A44',TP_INK,pA);
  TP.mk.style.width=(13.6*pA).toFixed(2)+'px'; TP.mk.style.marginRight=(7*pA).toFixed(2)+'px'; TP.vmk.style.transform=`scale(${pop.toFixed(3)})`;
  TP.page.style.background=mixc('#FFFFFF','#EEE9E4',pA);
  Object.assign(TP.btn.style,{width:lerp(212,178,pA)+'px',borderRadius:lerp(4,23,pA)+'px',background:mixc(TP_BLUE,TP_INK,pA),
    boxShadow:`0 ${lerp(6,0,pA).toFixed(1)}px ${lerp(10,0,pA).toFixed(1)}px rgba(0,0,0,${lerp(.45,0,pA).toFixed(3)})`});
  TP.img.style.borderRadius=lerp(4,14,pA)+'px'; TP.ph.style.borderRadius=TP.img.style.borderRadius;
  // motion : le titre, la ligne, le bouton et l'image ré-arrivent (arrive: fast, land: soft)
  [hd,TP.pairs[3],TP.btn].forEach((d,k)=>{ if(f<784){ d.style.translate=''; d.style.opacity=''; return; } const v=vl(f,784+k*1.5,7); d.style.translate=`0 ${(28*(1-v)).toFixed(1)}px`; d.style.opacity=v.toFixed(3); });
  // arial: false : les lettres du dernier Arial tombent, une à une
  TP.foot.forEach((c,i)=>{ const k=clamp((f-786-i*0.22)/4); c.style.transform=`translateY(${(30*k*k).toFixed(1)}px)`; c.style.opacity=(1-k).toFixed(2); });
  // stockPhotos: 0 : la photo de stock bascule et tombe hors de la page
  const g=accel(f,788,8,2); TP.ph.style.transform=`translateY(${(560*g).toFixed(1)}px) rotate(${(11*g).toFixed(2)}deg)`;
  // chaque rechargement : la pastille « live » s'allume, un filet de progression court sous la barre
  let lit=0, bar=0; for(const r of TP_RELOAD){ if(f>=r&&f<r+5) lit=Math.max(lit,1-(f-r)/5); if(f>=r&&f<r+3) bar=clamp((f-r+1)/3); }
  TP.dot.style.background=mixc('#4A4542','#F3EFEA',lit); TP.bar.style.width=(600*bar).toFixed(0)+'px';
}
const teBlack=el(TE.s,'','', 'position:absolute;inset:0;background:#000;opacity:0;pointer-events:none');
// le raccord : les deux points du « : » de « arial: false » deviennent les deux boulons de la macro (positions du rendu, image 0)
const MA_BOLT=[[1044,522],[1044,780]];
const teDots=MA_BOLT.map(()=>el(TE.s,'','', 'position:absolute;width:70px;height:70px;margin:-35px 0 0 -35px;border-radius:50%;background:#F3EFEA;display:none'));
const TEW=[[750,'<em style="font-size:96px">taste.</em>'],[757,'mo'],[762,'moti'],[764,'motion']];
const TE_CMD='npm rm ';
let TEL={};
function termLayout(){ teLine.innerHTML=`<span style="display:inline-block;margin-right:22px">${ARROW(110,78)}</span>npm rm <span class="tsel">boring</span> <span class="tsel2">--force</span>`; TEL.w=teLine.offsetWidth; teLine.innerHTML=''; }
for(let i=0;i<TE_CMD.length;i++) if(TE_CMD[i]!==' ') cR17(707+Math.round(i*2.9),'key',{v:.4});
cR17(695,'break',{}); cR17(732,'tick',{v:.45}); cR17(739,'tick',{v:.45}); cR17(750,'enter',{v:.8}); [757,762,764].forEach(f=>cR17(f,'key',{v:.35})); cR17(766,'pop',{v:.3,n:84});
[773,784,788,792,796,799].forEach(f=>cR17(f,'key',{v:.22})); cR17(790,'swish',{v:.3,peak:791,dur:4});
const CARET_COL=[[695,'#F3EFEA']];   // caret plein, couleur papier
function shotTerm(F){ const f=F-1;
  teGhost.style.opacity=(0.035*(1-approach(f,695,10))).toFixed(3); placeTL(teGhost,280,180);
  const big=f<707; show(teBig,big); show(teBigCaret,big);
  if(big){ const sl=37*approach(f,695,11,0.2); place(teBig,950+sl,540); let cc='#8A9A5B'; for(const [cf,c] of CARET_COL) if(f>=cf) cc=c;
    teBigCaret.style.background=cc; teBigCaret.style.transform=`scaleY(${f>=698&&f<701?1.35:1})`; teBigCaret.style.transformOrigin='50% 50%'; placeTL(teBigCaret,1105+sl,400); }
  // la ligne se tape (1 touche / 2,9 images), immobile entre les touches ; la taille descend en 3 paliers nets (719, 732, 739)
  const lineMode=f>=707&&f<750; show(teLine,lineMode);
  if(lineMode){ const n=clamp(Math.floor((f-707)/2.9)+1,0,TE_CMD.length);
    let h=`<span style="display:inline-block;vertical-align:-2px;margin-right:22px">${ARROW(110,78)}</span>`+TE_CMD.slice(0,n);
    // à l'Entrée (747-750), les lettres de « boring » tombent de 40 px, en linéaire, une image d'écart
    if(f>=732) h+=`<span class="tsel" style="display:inline-block;transform:scale(${(1.15-0.15*approach(f,732,3)).toFixed(3)})">${[...'boring'].map((c,i)=>{ const k=clamp((f-747-i*0.5)/3); return `<span style="display:inline-block;transform:translateY(${(40*k).toFixed(1)}px);opacity:${(1-k).toFixed(2)}">${c}</span>`; }).join('')}</span>`; if(f>=739) h+=` <span class="tsel2" style="display:inline-block;transform:scale(${(1.15-0.15*approach(f,739,3)).toFixed(3)})">--force</span>`;
    const car=(f<739||Math.floor(f/16)%2==0); h+=`<span style="display:inline-block;width:56px;height:104px;background:#F2EEE8;vertical-align:-18px;margin-left:10px;visibility:${car?'visible':'hidden'}"></span>`;
    teLine.innerHTML=h; const S=f<719?2.3:f<732?lerp(2.3,1.51,approach(f,719,2,0.5)):f<739?lerp(1.51,1.21,approach(f,732,2,0.5)):lerp(1.21,1,approach(f,739,2,0.5));
    place(teLine,960-1.6*(f-707),540,S);
    show(teBox,f>=740); if(f>=740){ const w=TEL.w+120; Object.assign(teBox.style,{left:(960-1.6*(f-707)-w/2)+'px',top:'462px',width:w+'px',height:'156px',opacity:approach(f,740,5).toFixed(2)}); } }
  else show(teBox,false);
  const panel=f>=750; show(tePanel,panel); show(tePanelLine,panel&&f<767);
  show(tePrev,panel&&f>=767);
  if(panel){ // panneau fixe ; recul par palier à 790 (barre d'icônes qui apparaît), pas de poussée continue
    const st=approach(f,790,3,0.4), pw=f<767?1280:lerp(1500,1640,st), ph=f<767?300:lerp(680,740,st);
    Object.assign(tePanel.style,{left:(960-pw/2)+'px',top:(540-ph/2)+'px',width:pw+'px',height:ph+'px'});
    show(teSide,f>=790); const lx=lerp(40,96,st), fs=lerp(28,25,st), lh=lerp(44,39,st);
    // l'aperçu occupe la droite du panneau, à pleine hauteur
    if(f>=767){ const ps=(ph-44)/640; tePrev.style.transform=`translate(${(pw-24-600*ps).toFixed(1)}px,22px) scale(${ps.toFixed(4)})`; tePrevUpdate(f); }
    let w=''; for(const [wf,t] of TEW) if(f>=wf) w=t;
    // une seule espace après « add » (plus de trou laissé par l'italique effacé) ; le caret clignote toutes les 8 images
    tePanelLine.innerHTML=`<span style="color:#F2EEE8">→</span> <span style="color:#F2EEE8">add</span> ${w.replace(/^(&nbsp;|\s)+/,'')}<span style="display:inline-block;width:3px;height:1em;background:#F2EEE8;vertical-align:-0.15em;margin-left:4px;visibility:${Math.floor(f/8)%2?'hidden':'visible'}"></span>`;
    TE.cam.style.transform=f<767?`scale(${(1+0.03*(0.5-0.5*Math.cos(Math.PI*clamp((f-750)/17)))).toFixed(4)})`:'';
    placeTL(tePanelLine,970-tePanelLine.offsetWidth/2,540-44,f>=766?1+0.1*(1-approach(f,766,4)):1);
    // le code arrive par paquets : insertion avec sélection (773, frappe 2 car./image jusqu'à 784), sauts d'indentation (784), paquets (788, 792, 796, 799)
    let row=0; teCode.forEach((d,i)=>{ const t0=CODE_T[i], on=f>=t0&&f>=767; show(d,on); if(!on) return;
      d.style.fontSize=fs+'px'; d.style.lineHeight=lh+'px'; d.style.left=(lx+(i==5||i==6?45*(1-approach(f,784,3,0.4)):0))+'px'; d.style.top=(66+row*lh)+'px'; row++;
      if(i!==4&&t0>767&&f<t0+3) d.style.clipPath=`inset(0 ${((1-(f-t0+1)/3)*100).toFixed(0)}% 0 0)`; else d.style.clipPath='';
      d.innerHTML=i==4&&f<784?GUT(4)+sliceHTML(CODE[4][0],2+(f-773)*4):d._h; });
    const cw=fs*0.6;
    show(teSel,f>=773&&f<786); if(f>=773){ Object.assign(teSel.style,{left:(lx+58)+'px',top:(66+4*lh-3)+'px',height:(lh-2)+'px',width:(f<784?cw*(2+(f-773)*4)+12:cw*44+12)+'px'}); }
    show(teTok,f>=792); if(f>=792){ const sp=approach(f,792,4); Object.assign(teTok.style,{left:(lx+58)+'px',top:(66+5*lh-3)+'px',height:(lh-2)+'px',width:((cw*15+12)*sp)+'px'}); } }
  // 790-806 : poussée qui accélère dans le « : » ; tout le reste s'éteint au noir ; 808-815 : il ne reste que les deux points
  const col=q1(tePanel,'.colon'); let z=1;
  if(f>=792&&col){ const r=col.getBoundingClientRect(), st=TE.s.getBoundingClientRect(), kk=st.width/W;
    // centre du « : » dans la caméra au repos (la caméra n'est pas encore transformée à cette image)
    // les deux points sont ronds (dessinés, pas la glyphe carrée de Fragment Mono) ; le zoom final pose leur écartement sur celui des boulons
    TE.cam.style.transform=''; const [d0,d1]=qa(col,'circle').map(e=>e.getBoundingClientRect()); const cx=((d0.left+d0.right)/2-st.left)/kk, cy=((d0.top+d1.bottom)/2-st.top)/kk;
    const zEnd=(MA_BOLT[1][1]-MA_BOLT[0][1])/((d1.top-d0.top)/kk);
    // poussée en S (792-812) : elle accélère puis freine sur les boulons (≈ ×1,26/image au plus fort), au lieu de couper à ×1,5/image
    const tz=clamp((f-792)/20), a=tz*tz*(3-2*tz); z=Math.exp(Math.log(zEnd)*a); const tx=lerp(cx,MA_BOLT[0][0],a), ty=lerp(cy,(MA_BOLT[0][1]+MA_BOLT[1][1])/2,a);
    TE.cam.style.transformOrigin='0 0'; TE.cam.style.transform=`translate(${(tx-cx*z).toFixed(1)}px,${(ty-cy*z).toFixed(1)}px) scale(${z.toFixed(4)})`;
    const fade=clamp((f-794)/12); tePanel.style.borderColor=`rgba(44,44,44,${(1-fade).toFixed(2)})`;
    teCode.forEach(d=>{ d.style.color=fade>0?mixc('#BFB9B2','#000000',fade):''; qa(d,'span').forEach(sp=>{ if(!sp.classList.contains('colon')) sp.style.opacity=(1-fade).toFixed(2); }); });
    [teDim1,teDim2,teSide,teSel,teTok,tePrev].forEach(e=>e.style.opacity=(1-fade).toFixed(2)); col.style.color='#F3EFEA';
    // à partir de 803 le noir monte ; les deux points passent au-dessus (calque teDots), exactement là où la caméra les a menés
    const dots=f>=803; col.style.visibility=dots?'hidden':''; qa(col,'circle').forEach((c,k)=>{ const r=c.getBoundingClientRect(), d=(r.right-r.left)/kk;
      Object.assign(teDots[k].style,{left:((r.left+r.right)/2-st.left)/kk+'px',top:((r.top+r.bottom)/2-st.top)/kk+'px',width:d+'px',height:d+'px',margin:`${-d/2}px 0 0 ${-d/2}px`}); }); }
  else { if(col) col.style.visibility=''; TE.cam.style.transform=''; TE.cam.style.transformOrigin=''; teCode.forEach(d=>{ d.style.color=''; qa(d,'span').forEach(sp=>sp.style.opacity=''); }); [teDim1,teDim2,teSide,teSel,teTok,tePrev].forEach(e=>e.style.opacity=''); tePanel.style.borderColor=''; }
  teBlack.style.opacity=clamp((f-802)/6).toFixed(3);
  teDots.forEach(d=>show(d,f>=803));
}

/* ---------- 20 · macro N&B en contre-jour (séquence Cycles) : le fond s'allume, puis le sujet ; recul qui accélère (réf, +1) ---------- */
const MA=scene('sMacro',816,879,f=>shotMacro(f));
const cR20=cueAt(1);
const maSeq=canvas(MA.cam,1280,720,'left:0;top:0;width:1920px;height:1080px;filter:grayscale(1) brightness(.6) contrast(1.35)');
const maDots=MA_BOLT.map(()=>el(MA.s,'','', 'position:absolute;width:70px;height:70px;margin:-35px 0 0 -35px;border-radius:50%;background:#F3EFEA;mix-blend-mode:screen'));
cR20(815,'riser',{v:.35,end:826}); cR20(864,'whoosh',{v:.6,peak:876,dur:12});
// curseur en 3 segments (réf) : entrée rapide 826-832, glisse le long du pied en ralentissant jusqu'à 868, repart à gauche
const MA_CUR=[[826,683,1011],[832,896,649],[868,1515,559],[878,1109,627]];
function maCursor(f){ if(f<826) return null; for(let k=0;k<MA_CUR.length-1;k++){ const [a,x0,y0]=MA_CUR[k],[b,x1,y1]=MA_CUR[k+1]; if(f<=b){ const t=(f-a)/(b-a), e=k==1?1-Math.pow(1-t,1.6):k==2?t*t:t; return [lerp(x0,x1,e),lerp(y0,y1,e)]; } } return [1109,627]; }
function shotMacro(F){ const f=F-1;
  seqDraw(maSeq,SEQ.macro,f-816); maSeq.style.opacity=vl(f,815,4).toFixed(3);   // la macro monte du noir (réf 815-818), sous les deux points
  // fin : le recul rendu continue en 2D avec un flou directionnel croissant (pas de roulis)
  // −5, −8, −12 %/image en plus du rendu, jusqu'à la coupe
  const wh=accel(f,872,7.6,3); MA.cam.style.transform=`scale(${(1-0.35*wh).toFixed(4)})`; MA.cam.style.filter=wh>0?`blur(${(wh*10).toFixed(1)}px)`:'';
  // les deux points du « : » fondent dans les deux boulons quand la macro s'allume (816-822)
  const m=vl(f,816,6); maDots.forEach((d,i)=>{ show(d,m<1); d.style.left=MA_BOLT[i][0]+'px'; d.style.top=MA_BOLT[i][1]+'px'; d.style.opacity=(1-m).toFixed(3); d.style.transform=`scale(${(1-0.4*m).toFixed(3)})`; });
  cursor(0,0,0,false);
}

/* ---------- 21 · chat IA + page produit : l'interface ne bouge pas, tout se passe dans la vue 3D et dans le fil ---------- */
const CH=scene('sChat',880,953,f=>shotChat(f));
const chRoot=el(CH.cam,'','', 'position:absolute;inset:0'); chRoot.innerHTML=tplVChat();
const chTurn=q1(chRoot,'.pturn'), chView=chTurn.parentElement, chFab=q1(chRoot,'.sfab'), chFix=q1(chRoot,'.cfix'), chThumbs=qa(chRoot,'.cthumb'), chApprove=q1(chRoot,'.capprove'), chThink=q1(chRoot,'.cthink');
const chTurnR=canvas(chView,1100,800,'inset:0;width:100%;height:100%;display:none');
const chPin=el(CH.s,'m','1','position:absolute;width:40px;height:40px;border-radius:20px 20px 20px 4px;color:#fff;font-size:18px;line-height:40px;text-align:center;box-shadow:0 0 0 3px #fff,0 8px 18px rgba(0,0,0,.25);display:none;z-index:6;transform-origin:4px 36px');
const chKids=[...q1(chRoot,'.chatp').children];   // 0 logo · 1 bulle · 2 réflexion · 3 réponse · 4-5 paquets · 6 approbation · 7 correction · 8 suggestions…
const chHot=el(chRoot,'','', 'position:absolute;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:32px;box-shadow:0 0 0 3px #F3EFEA,0 0 0 4px rgba(21,20,19,.35),0 6px 18px rgba(0,0,0,.25);display:none');
const chTip=el(chRoot,'m','', 'position:absolute;height:34px;line-height:34px;padding:0 14px;border-radius:17px;background:#151413;color:#F3EFEA;font-size:13px;white-space:nowrap;display:none');
const chInk=inkLayer(CH.s,{ground:'dark'});   // sur le tissu, l'encre est opaque (pas de multiply : rouge sur bleu resterait violet)
const pad2=i=>String(i).padStart(2,'0');
const TURN={blue:[],red:[]};
for(let i=0;i<48;i++) TURN.blue[i]=preload(`img/turn/blue_${pad2(i)}.jpg`);
for(let i=38;i<72;i++) TURN.red[i]=preload(`img/turn/red_${pad2(i)}.jpg`);
cue(880,'impact',{v:.55}); cue(881,'tick',{v:.2}); cue(883,'tick',{v:.25}); [895,901,910].forEach(f=>cue(f,'tick',{v:.2})); cue(918,'brush',{v:.7,end:928}); cue(926,'pluck',{v:.45,n:79}); cue(946,'beep',{v:.5}); cue(940,'whoosh',{v:.6,peak:951,dur:12});
const CH_HOVER=[[895,898,'bolt','Steel bolts · ×8'],[901,907,'seat','Velvet · 380 g/m²'],[910,916,'back','Hand-tufted back']];
function chView3(f){ // caméra de la vue produit (réf) : recul + travelling flou à l'entrée, roulis, secousse au coup de pinceau, anticipation, poussée finale
  const a=approach(f,880,10,0.25); let s=lerp(1.25,1,a), x=120*(1-a), y=0, r=3*(approach(f,892,4)-approach(f,898,6));
  y+=22*(approach(f,924,2,0.5)-approach(f,927,8)); const an=approach(f,936,3); s*=1-0.04*an; r-=2.4*an*(1-approach(f,940,4));
  s*=1+0.06*(0.5-0.5*Math.cos(Math.PI*clamp((f-890)/46)));   // lente poussée dans la vue 3D seulement : les panneaux et le texte ne bougent pas
  const pu=accel(f,940,11.5,3); s*=1+0.35*pu; y-=65*pu;   // n'arrive pas à 1 avant la coupe (952) : pas d'image figée
  // la vue doit toujours couvrir son cadre (630,196)-(1548,862) : échelle minimale pour que les 4 coins restent dans l'image tournée
  { const c=Math.cos(r*Math.PI/180), sn=Math.sin(r*Math.PI/180); let need=1;
    for(const [cx,cy] of [[-459,-334],[459,-334],[-459,334],[459,334]]){ const dx=cx-x, dy=cy-y, u=dx*c+dy*sn, v=-dx*sn+dy*c; need=Math.max(need,Math.abs(u)/459,Math.abs(v)/334); }
    s=Math.max(s,need*1.01); }
  return {s,x,y,r,bx:vel(t=>120*(1-approach(t,880,10,0.25)),f), by:vel(t=>-65*accel(t,940,11.5,3),f)}; }
// le plateau entre lancé (≈ 6°/image, comme la réf) et ralentit jusqu'à 1,3°/image à 895, tourne ainsi jusqu'à 931
// (l'indice 38 du velours rouge est atteint à 918, au coup de pinceau), puis se pose de trois quarts
const CH_TAU=9.32, CH_I895=3*CH_TAU*(1-Math.exp(-15/CH_TAU)), CH_I931=CH_I895+0.7*36;
function chIdx(f){ if(f<=880) return 0; if(f<=895) return 3*CH_TAU*(1-Math.exp(-(f-880)/CH_TAU)); if(f<=931) return CH_I895+0.7*(f-895);
  const t=clamp((f-931)/15); return CH_I931+10*(1-(1-t)*(1-t)); }
// M7 : le grand coup de feutre traverse l'assise ; l'encre boit dans le velours (926-932) en suivant le poil (luminance du rendu)
const M7=()=>penPlace('G07',[862,492,1290,540]);
const CH_MASK=document.createElement('canvas'); CH_MASK.width=275; CH_MASK.height=200;
// le velours bleu (teinte 200-225°, saturation > 0,35), à basse résolution, adouci par l'agrandissement
const CH_BLUE=document.createElement('canvas'); CH_BLUE.width=275; CH_BLUE.height=200; let CH_BLUE_SRC=null;
function chBlueKey(src){ if(src===CH_BLUE_SRC) return; CH_BLUE_SRC=src; const x=CH_BLUE.getContext('2d'); x.clearRect(0,0,275,200); x.drawImage(src,0,0,275,200);
  const im=x.getImageData(0,0,275,200), d=im.data;
  for(let o=0;o<d.length;o+=4){ const r=d[o]/255, g=d[o+1]/255, b=d[o+2]/255, mx=Math.max(r,g,b), mn=Math.min(r,g,b), sat=mx>0?(mx-mn)/mx:0;
    let h=0; if(mx===b&&mx>mn) h=240+60*(r-g)/(mx-mn); else if(mx===g&&mx>mn) h=120+60*(b-r)/(mx-mn);
    const k=clamp((sat-0.3)/0.12)*clamp(1-Math.abs(h-212)/30); d[o]=d[o+1]=d[o+2]=255; d[o+3]=Math.round(255*k); }
  x.putImageData(im,0,0); }
function chToView(p,V){ // écran → pixels du canvas de la vue (inverse de la transformation CSS)
  const cx=630+459, cy=196+334; let x=p[0]-cx-V.x, y=p[1]-cy-V.y; const c=Math.cos(-V.r*Math.PI/180), s=Math.sin(-V.r*Math.PI/180);
  const xr=(x*c-y*s)/V.s, yr=(x*s+y*c)/V.s; return [(xr+459)*1100/918,(yr+334)*800/668]; }
// le front couvre le dossier dès 930
// le pinceau révèle le velours rouge le long de son passage (918-924, ~26 px de demi-largeur), puis l'encre boit le tissu (924-930) ;
// le front est déplacé par un bruit à deux octaves (±14 px) et son bord est serré (~6 px) : pas de ligne droite, pas de halo violet
function chNoise(x,y){ const h=(a,b)=>{ const s=Math.sin(a*127.1+b*311.7)*43758.5453; return s-Math.floor(s); };
  const vn=(x,y)=>{ const i=Math.floor(x), j=Math.floor(y), u=x-i, v=y-j, uu=u*u*(3-2*u), vv=v*v*(3-2*v); return lerp(lerp(h(i,j),h(i+1,j),uu),lerp(h(i,j+1),h(i+1,j+1),uu),vv); };
  return 0.65*vn(x/22,y/22)+0.35*vn(x/9+7.3,y/9+1.9)-0.5; }
function chSoak(f,V,red){ const tt=clamp((f-924)/6), R=lerp(26,330,0.5-0.5*Math.cos(Math.PI*tt))*1100/918; const k=CH_MASK.width/1100;
  const all=penResample(M7().flat(),40), prog=clamp((f-917)/6); const pts=all.slice(0,Math.max(2,Math.ceil(all.length*prog))).map(p=>chToView(p,V));
  const x=CH_MASK.getContext('2d'); const im=x.createImageData(CH_MASK.width,CH_MASK.height);
  // luminance du velours rouge, lue une fois à basse résolution pour moduler le front
  const L=document.createElement('canvas'); L.width=CH_MASK.width; L.height=CH_MASK.height; const lx=L.getContext('2d'); lx.drawImage(red,0,0,L.width,L.height); const ld=lx.getImageData(0,0,L.width,L.height).data;
  for(let j=0;j<CH_MASK.height;j++) for(let i=0;i<CH_MASK.width;i++){ const px=i/k, py=j/k; let d=1e9;
    for(let n=0;n<pts.length-1;n++){ const a=pts[n], b=pts[n+1]; const bx=b[0]-a[0], by=b[1]-a[1]; const t=clamp(((px-a[0])*bx+(py-a[1])*by)/Math.max(1e-6,bx*bx+by*by)); d=Math.min(d,Math.hypot(px-a[0]-bx*t,py-a[1]-by*t)); }
    const o=(j*CH_MASK.width+i)*4, lum=(ld[o]*.3+ld[o+1]*.59+ld[o+2]*.11)/255; const r=R*(1+0.35*(lum-0.35));
    const dn=d+14*1100/918*2*chNoise(px,py), e=clamp((r-dn)/(6*1100/918)), a=e*e*(3-2*e); im.data[o]=im.data[o+1]=im.data[o+2]=255; im.data[o+3]=Math.round(255*a); }
  x.putImageData(im,0,0); }
function shotChat(f){
  const ii=chIdx(f), i=Math.round(ii), V=chView3(f);
  const tr=`translate(${V.x.toFixed(1)}px,${V.y.toFixed(1)}px) rotate(${V.r.toFixed(2)}deg) scale(${V.s.toFixed(4)})`;
  [chTurn,chTurnR].forEach(c=>{ c.style.transform=tr; });
  chTurn.style.filter=Math.abs(V.bx)>1||Math.abs(V.by)>2?`blur(${Math.min(14,(Math.abs(V.bx)+Math.abs(V.by))*0.25).toFixed(1)}px)`:''; chTurnR.style.filter=chTurn.style.filter;
  seqDrawRaw(chTurn,TURN.blue[Math.min(47,i)]);
  // le coup de pinceau (918-924), puis le velours apparaît là où l'encre a bu, jusqu'à recouvrir tout le fauteuil (932)
  const ix=inkClear(chInk);
  // le pinceau teint le velours (fusion « couleur » : la teinte du stylo, le modelé du tissu), bord adouci : pas un autocollant
  // (le trait n'est plus une teinte posée : il révèle le rendu du velours rouge, voir chSoak)
  const redOn=f>=918; show(chTurnR,redOn);
  if(redOn){ const red=TURN.red[clamp(i,38,71)]; const c=chTurnR.getContext('2d'); c.clearRect(0,0,1100,800); c.drawImage(red,0,0,1100,800);
    if(f<931){ chSoak(f,V,red); c.globalCompositeOperation='destination-in'; c.imageSmoothingEnabled=true; c.drawImage(CH_MASK,0,0,1100,800); c.globalCompositeOperation='source-over'; } }
  // le fil défile de 13 px (881-890) : appliqué avant toute lecture de position (sinon les traits rouges se calent sur l'état d'avant)
  const scr=-13*approach(f,881,9);
  chKids.forEach((k,j)=>{ if(j==0||j>=7) return; const t0=j==1?880:j<=3?881:883; k.style.visibility=f>=t0?'visible':'hidden'; k.style.translate=`0 ${scr.toFixed(1)}px`; });
  chFab.textContent=f>=926?'velvet':'polyester';
  // le journal de l'agent se tape une ligne toutes les 12 images (892, 904, 916) ; la troisième se résout en « ✓ … velvet » à 926
  qa(chRoot,'.clog').forEach(l=>{ const t0=+l.dataset.t; l.textContent=f<t0?'':l.dataset.s.slice(0,Math.ceil((f-t0+1)*2.5)); });
  chKids[7].style.visibility=f>=916?'visible':'hidden'; chKids[7].style.color=f>=926?'#151413':'#7A736C';
  // la carte d'approbation se résout quand le changement arrive (926) : les deux lignes barrées, « ✓ applied by v vladan »
  const done=f>=926; qa(chRoot,'.crm').forEach((e,k)=>{ e.style.textDecoration=''; e.style.color=f>=926+k*2?'#8E877F':'#151413';
    // le stylo barre chaque ligne en rouge (924-926, 926-928) : c'est lui qui applique le changement, pas le fondateur
    if(f>=924+k*2){ const b=e.getBoundingClientRect(), st=CH.s.getBoundingClientRect(), kk=st.width/W; const L=(b.left-st.left)/kk, R=(b.right-st.left)/kk, Y=((b.top+b.bottom)/2-st.top)/kk;
      penDraw(ix,penPlace('G03',[L-6,Y-2,R+10,Y+2],{mode:'stretch'}),f,924+k*2,{size:3.2,ground:'dark'}); } });
  const ca=q1(chRoot,'.chapp'); ca.innerHTML=done?'✓ applied by <span style="display:inline-block;width:20px;height:20px;border-radius:10px;background:#FF3D5E;color:#fff;font-size:12px;line-height:20px;text-align:center;margin:0 4px">v</span>vladan':'Resolve';
  if(ca._b===undefined){ ca._b=ca.style.background; ca._c=ca.style.color; ca._p=ca.style.paddingLeft; }   // garder les couleurs d'origine (les remettre à '' les effacerait)
  ca.style.background=done?'transparent':ca._b; ca.style.color=done?'#151413':ca._c; ca.style.paddingLeft=done?'0':ca._p; show(q1(chRoot,'.crej'),!done);
  chKids[7].textContent=f>=926?'✓ changed · fabric polyester → velvet':'↻ fabric · polyester → …'.slice(0,Math.ceil((f-915)*2.5));
  // la vignette reste bleue tant que le front ne l'a pas atteinte
  chThumbs.forEach(t=>t.style.filter=f<930?'hue-rotate(-145deg) saturate(1.2)':'');
  show(q1(chRoot,'.cres'),f>=926); q1(chRoot,'.cres').style.opacity=vl(f,926,4).toFixed(3);   // le fil se résout quand le velours a bu
  // survol : le curseur du fondateur visite le boulon, l'assise, le dossier ; puis il approuve (946)
  const H=TURNHOT[i]||TURNHOT[String(Math.min(47,i))]; let hv=null; for(const h of CH_HOVER) if(f>=h[0]&&f<=h[1]) hv=h;
  const P=k=>{ if(!H||!H[k]) return [1090,560]; const px=(H[k][0]-0.5)*918, py=(H[k][1]-0.5)*668, c=Math.cos(V.r*Math.PI/180), sn=Math.sin(V.r*Math.PI/180);
    return [630+459+V.x+V.s*(px*c-py*sn), 196+334+V.y+V.s*(px*sn+py*c)]; };
  // le repère du commentaire n° 1 suit l'assise du fauteuil qui tourne ; il passe en ✓ (encre) quand le fil est résolu
  { const on=f>=881&&f<938; show(chPin,on); if(on){ const [px,py]=P('seat'); const ok=f>=926; chPin.style.left=(px-14)+'px'; chPin.style.top=(py-58)+'px';
      chPin.style.background=ok?'#151413':'#2D6CDF'; chPin.textContent=ok?'✓':'1'; chPin.style.transform=`scale(${(f<884?back(f,881,4):1).toFixed(3)})`; chPin.style.opacity=(1-clamp((f-932)/6)).toFixed(2); } }
  show(chHot,!!hv); show(chTip,!!hv);
  if(hv){ const [hx,hy]=P(hv[2]); chHot.style.left=hx+'px'; chHot.style.top=hy+'px'; chHot.style.transform=`scale(${back(f,hv[0],4).toFixed(3)})`;
    chTip.textContent=hv[3]; chTip.style.left=(hx+44)+'px'; chTip.style.top=(hy-60)+'px'; chTip.style.opacity=approach(f,hv[0],3).toFixed(2); }
  let cxy=null; const tf=twos(f,893);
  if(tf>=893&&tf<918){ const tg=tf<899?P('bolt'):tf<908?P('seat'):P('back'); const pv=tf<899?[1300,900]:tf<908?P('bolt'):P('seat'); const st=tf<899?893:tf<908?899:908; const k=clamp((tf-st)/4); cxy=[lerp(pv[0],tg[0],k)+14,lerp(pv[1],tg[1],k)+14]; }
  if(tf>=934){ const k=clamp((tf-934)/10); cxy=[lerp(1400,1730,k),lerp(860,1010,k)]; }
  chApprove.style.background=f>=946&&f<948?'#DDD6CE':'#F3EFEA';
  cursor(cxy?cxy[0]:0,cxy?cxy[1]:0,f>=946&&f<948?1:0,!!cxy,1,f>=942?'hand':'arrow');
  // le fil : la bulle seule (880), réflexion + réponse (881), paquets + approbation (883), défile de 13 px
}

/* ---------- 22-24 · Order Complete (vidéo Cycles) → plein cadre → le thermique naît du fauteuil → Taste Check → grille qui casse (réf, +2) ---------- */
const DO=scene('sDone',954,1079,f=>shotDone(f));
const cR22=cueAt(2);
const doFrame=el(DO.cam); const doD=framed(doFrame,tplVDone(),1362,918,1240,830,VINK);
const doTitle=q1(doD,'.vhead'), doSeq=q1(doD,'.vseq'), doPills=qa(doD,'.vpill'), doSum=q1(doD,'.full>div:last-child');
const doFull=el(DO.cam,'','', 'position:absolute;inset:0;display:none;overflow:hidden');
const doFullIn=el(doFull,'','', `position:absolute;left:0;top:0;width:1240px;height:830px;transform-origin:0 0;background:${VINK}`); doFullIn.innerHTML=q1(doD,'.full').outerHTML;
const doFSeq=q1(doFullIn,'.vseq'), doFTitle=qa(doFullIn,'.vhead');

// 989-1079 : la page d'accueil de velvetly, claire, et sa carte de chaleur imprimée à l'encre (cinq paliers, courbes de niveau)
const doTP=el(DO.cam,'','', 'position:absolute;inset:0;overflow:hidden;display:none;background:#EEE9E4');
const doTPi=el(doTP,'','', 'position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:960px 540px');
doTPi.innerHTML=`<img src="img/turn/red_60.jpg" style="position:absolute;left:0;top:59px;width:1920px;height:1021px;object-fit:cover;object-position:50% 58%">
  <div class="dchr" style="position:absolute;left:0;right:0;top:0;height:58px;background:#E4DFDA;box-shadow:0 1px 0 rgba(21,20,19,.12)">${[0,1,2].map(i=>`<span style="position:absolute;left:${24+i*23}px;top:22px;width:13px;height:13px;border-radius:50%;background:rgba(21,20,19,.15)"></span>`).join('')}
  <div class="m dchr" style="position:absolute;left:120px;top:12px;width:560px;height:34px;border-radius:9px;background:#F3EFEA;font-size:16px;line-height:34px;padding-left:16px;color:rgba(21,20,19,.7)">velvetly.app / <b style="font-weight:500;color:#151413">home</b></div></div>
  <div class="dghost" style="position:absolute;left:150px;top:150px;width:420px;height:280px;background:#D9DCE1"><svg width="120" height="96" viewBox="0 0 120 96" style="position:absolute;left:150px;top:80px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="4"/><circle cx="84" cy="30" r="10" fill="#A9AEB6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg><div class="ar" style="position:absolute;left:0;right:0;top:204px;text-align:center;font-size:16px;color:#8A8F97">stock_handshake_final_v3.jpg</div></div>`;
const doHeatC=canvas(doTPi,1920,1021,'left:0;top:59px;width:1920px;height:1021px');
const doDotsC=canvas(doTPi,1920,1080,'left:0;top:0;width:1920px;height:1080px');
const doHud=el(doTPi,'','', 'position:absolute;right:28px;top:84px;display:flex;gap:8px');
doHud.innerHTML=['HEATMAP · CLICKS','1,204 sessions · since hero v2'].map(t=>`<span class="m" style="font-size:15px;font-weight:500;letter-spacing:.04em;background:rgba(243,239,234,.9);box-shadow:0 0 0 1px rgba(21,20,19,.12);border-radius:8px;padding:8px 12px">${t}</span>`).join('');
const doLeg=el(doTPi,'m','', 'position:absolute;left:28px;bottom:28px;display:flex;align-items:center;font-size:13px;color:rgba(21,20,19,.7)');
doLeg.innerHTML=`<span style="margin-right:10px">low</span>${[5,9,14,20,28].map(a=>`<i style="display:block;width:34px;height:10px;background:rgba(21,20,19,${a/100})"></i>`).join('')}<span style="margin-left:10px">high</span>`;
const doRing=el(doTPi,'','', 'position:absolute;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;box-shadow:0 0 0 2px #151413');
const doRingL=el(doTPi,'m','hero · 61% of clicks','position:absolute;font-size:22px;color:#151413;background:rgba(243,239,234,.9);padding:4px 10px;border-radius:6px');
const DO_SEAT=[990,520], DO_BACK=[900,300], DO_GHOST=[360,290];
// le champ de chaleur : six gaussiennes, posterisé en cinq paliers d'encre, calculé une fois
const DO_HSRC=[[DO_BACK[0],DO_BACK[1]-59,170,1.0],[DO_SEAT[0],DO_SEAT[1]-59,210,0.85],[1260,560,140,0.35],[960,556-59,120,0.7],[300,40,90,0.3],[1720,40,80,0.28]];
const DO_LVL=(()=>{ const L=new Uint8Array(1920*1021), th=[0.10,0.24,0.42,0.62,0.82];
  for(let y=0;y<1021;y++) for(let x=0;x<1920;x++){ let v=0; for(const s of DO_HSRC){ const dx=x-s[0], dy=y-s[1]; v+=s[3]*Math.exp(-(dx*dx+dy*dy)/(2*s[2]*s[2])); } let k=0; for(let i=0;i<5;i++) if(v>th[i]) k=i+1; L[y*1920+x]=k; } return L; })();
const DO_A=[0,13,23,36,51,71];
function doHeatDraw(kmax){ const g=doHeatC.getContext('2d'), im=g.createImageData(1920,1021), d=im.data;
  for(let p=0;p<1920*1021;p++){ const k=Math.min(DO_LVL[p],kmax); if(!k) continue; const o=p*4; d[o]=21; d[o+1]=20; d[o+2]=19; d[o+3]=DO_A[k];
    const r=p+1, dn=p+1920; if((r<1920*1021&&Math.min(DO_LVL[r],kmax)!==k)||(dn<1920*1021&&Math.min(DO_LVL[dn],kmax)!==k)) d[o+3]=77; }
  g.putImageData(im,0,0); }
let doHeatK=-1;
// 36 points de session : posés sur le fantôme de la photo de stock, ils migrent vers le fauteuil (1011-1040)
const DO_DOTS=(()=>{ const r=rng(77), g=()=>{ const u=Math.max(1e-6,r()), v=r(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }; return Array.from({length:36},(_,i)=>{ const to=i<20?DO_SEAT:DO_BACK;
  return [DO_GHOST[0]+g()*60,DO_GHOST[1]+g()*45,to[0]+g()*45,to[1]+g()*35]; }); })();
const doBtn=el(DO.cam,'abs','Start Taste Check','height:72px;line-height:72px;padding:0 32px;border-radius:14px;background:#151413;color:#F3EFEA;font-size:30px;font-weight:500;box-shadow:0 18px 40px -18px rgba(21,20,19,.66)');
// grille irrégulière (colonnes 80-310 px, lignes serrées en haut et en bas), blocs « glitch » qui montrent des copies décalées et zoomées
const DO_COLS=(()=>{ const w=[80,140,310,120,200,90,260,150,180,110,230,140]; const a=[]; let x=0; for(const k of w){ x+=k; if(x<1920) a.push(x); } return a; })();
const DO_ROWS=[38,66,90,110,126,260,540,820,950,966,984,1006,1034];
const doGrid=el(DO.cam,'','', 'position:absolute;inset:0;display:none');
const doLines=[...DO_COLS.map(x=>el(doGrid,'gline','', `left:${x-1}px;top:0;width:2px;height:1080px;transform-origin:50% 50%`)),...DO_ROWS.map(y=>el(doGrid,'gline','', `left:0;top:${y-1}px;width:1920px;height:2px;transform-origin:50% 50%`))];
const doDots=[]; DO_COLS.forEach((x,i)=>DO_ROWS.forEach((y,j)=>{ const sz=lerp(21,5,clamp(Math.abs(y-540)/540)); doDots.push(el(doGrid,'gdot','', `left:${x}px;top:${y}px;width:${sz}px;height:${sz}px;margin:${-sz/2}px 0 0 ${-sz/2}px;border-radius:50%;box-shadow:none`)); }));
const doBlocks=[0,1,2,3,4,5,6,7].map(()=>{ const b=el(doGrid,'','', 'position:absolute;width:235px;height:287px;overflow:hidden;display:none'); const im=el(b,'','', 'position:absolute;left:0;top:0;width:1920px;height:1021px;transform-origin:0 0'); im.innerHTML='<img src="img/turn/red_60.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 58%">'; b._im=im; return b; });
const doMaskC=document.createElement('canvas'); doMaskC.width=960; doMaskC.height=540;
cR22(952,'impact',{v:.55}); cR22(978,'whoosh',{v:.5,peak:989,dur:11}); cR22(989,'swish',{v:.4,peak:990,dur:5}); cR22(995,'shimmer',{v:.5,end:1003}); cR22(1003,'impact',{v:.45});
cR22(1020,'pop',{v:.45,n:76}); cR22(1050,'click',{v:.95}); cR22(1052,'riser',{v:.5,end:1077}); for(let k=0;k<8;k++) cR22(1058+k*2.5,'tick',{v:.16});
const fullT=s=>`translate(${(960-560*s).toFixed(1)}px,${(540-300*s).toFixed(1)}px) scale(${s.toFixed(4)})`;
function shotDone(F){ const f=F-2;
  const card=f<989; show(doFrame,card); show(doFull,f>=989&&f<1003);
  // carte : entre à 0,95 en glissant de 50 px (952-966), tient en rampant (+0,12 %/i), puis poussée qui accélère ×1,19 (978-988)
  if(card){ const en=approach(f,952,14,0.2); const s=lerp(0.95,1,en)*(1+0.003*Math.max(0,f-966))*(1+0.19*accel(f,978,11,3));
    place(doFrame,960+50*(1-en),540,s); const fu=q1(doD,'.full'); fu.style.transformOrigin='55% 60%'; fu.style.transform=`scale(${(1+0.12*accel(f,980,9,3)).toFixed(4)})`;
    seqDraw(doSeq,SEQ.done,f-952);
    doSum.style.clipPath=`inset(0 0 ${((1-approach(f,956,10))*100).toFixed(1)}% 0 round 18px)`; }
  // 989-1079 : la page claire et sa chaleur à l'encre
  const hp=f>=989; show(doTP,hp); show(doFull,false);
  // sortie : plus de glissement qui accélère vers une coupe sèche ; une dérive lente et un fondu par le flou (1068-1077) que la grille reprend
  if(hp){ const z=1+0.0026*(f-989), pan=f<1062?0:(f-1062)*6, zz=1;
    doTPi.style.transform=`translate(${pan.toFixed(1)}px,${(pan*0.6).toFixed(1)}px) scale(${(z*zz).toFixed(4)})`;
    // les étiquettes restent fixes à l'écran pendant la poussée (sinon le cadre coupe « 1,204 sessions » et la légende)
    if(f<1062){ const Z=z*zz; Object.assign(doHud.style,{right:(1920-(960+(1892-960)/Z)).toFixed(1)+'px',top:(540+(84-540)/Z).toFixed(1)+'px',transform:`scale(${(1/Z).toFixed(4)})`,transformOrigin:'100% 0'});
      Object.assign(doLeg.style,{left:(960+(28-960)/Z).toFixed(1)+'px',bottom:(1080-(540+(1052-540)/Z)).toFixed(1)+'px',transform:`scale(${(1/Z).toFixed(4)})`,transformOrigin:'0 100%'}); }
    qa(doTPi,'.dchr').forEach(e=>e.style.translate=`0 ${(-30*clamp((f-1018)/12)).toFixed(1)}px`);   // la barre d'adresse sort du cadre en entier, pas de liseré
    const k=f<1002?0:Math.min(5,1+Math.floor((f-1002)/3.6)); if(k!==doHeatK){ doHeatDraw(k); doHeatK=k; }
    q1(doTPi,'.dghost').style.opacity=(0.22*(1-clamp((f-1005)/6))).toFixed(3);
    const g=doDotsC.getContext('2d'); g.clearRect(0,0,1920,1080);
    DO_DOTS.forEach(([x0,y0,x1,y1],i)=>{ const t=vl(f,1011+i*0.6,8); const x=lerp(x0,x1,t), y=lerp(y0,y1,t);
      g.beginPath(); g.arc(x,y,4.5,0,7); g.fillStyle='rgba(21,20,19,.72)'; g.fill(); g.lineWidth=2; g.strokeStyle='rgba(243,239,234,.9)'; g.stroke(); });
    const rg=vl(f,1024,6); show(doRing,f>=1024); show(doRingL,f>=1024); doRing.style.left=DO_SEAT[0]+'px'; doRing.style.top=DO_SEAT[1]+'px'; doRing.style.transform=`scale(${rg.toFixed(3)})`;
    doRingL.style.left=(DO_SEAT[0]+46)+'px'; doRingL.style.top=(DO_SEAT[1]-58)+'px'; doRingL.style.opacity=rg.toFixed(3);
    [doHud,doLeg].forEach(e=>e.style.opacity=f<1052?'1':'0');
    const df=vl(f,1068,9); doTP.style.filter=df>0?`blur(${(20*df).toFixed(1)}px) brightness(${(1+0.3*df).toFixed(2)}) saturate(${(1-0.6*df).toFixed(2)})`:''; }
  // le bouton : apparaît à 0,91, texte accent 1 image, grandit de 10 % ; clic 1050 = 1 image à 0,82, brun chaud qui reste
  const bOn=f>=1020&&f<1072; show(doBtn,bOn); if(bOn){ const sc=lerp(0.91,1,approach(f,1020,14))*(f==1050?0.82/1:f==1051?0.97:1);
    place(doBtn,960,556,sc); doBtn.style.color='#F3EFEA'; doBtn.style.background=f>=1050&&f<1052?'#2E2B28':'#151413';
    mblur(doBtn,f>=1062?vel(t=>t<1062?0:(t-1062)**1.6*3,f)*3:0,0); doBtn.style.opacity=(1-approach(f,1064,8)).toFixed(3); }
  const cf=twos(f,1040), cp=clamp((cf-1040)/8); cursor(lerp(1180,1030,cp),lerp(880,590,cp),f==1050?1:0,f>=1040&&f<1066,1,cp>=1?'hand':'arrow');
  const gOn=f>=1052; show(doGrid,gOn); if(gOn){ const lp=approach(f,1052,7); doLines.forEach((l,i)=>{ l.style.transform=i<DO_COLS.length?`scaleY(${lp.toFixed(3)})`:`scaleX(${lp.toFixed(3)})`; });
    doDots.forEach((d,i)=>{ d.style.transform=`scale(${back(f,1058+(i%7),5).toFixed(3)})`; });
    const key=Math.floor((f-1058)/2.5);
    doBlocks.forEach((b,i)=>{ const on=f>=1058&&f<1077&&i<3+Math.min(5,f-1058); show(b,on); if(!on) return; const r=rng(4000+key*13+i);
      const bx=r()*1685, by=r()*793, dx=20+r()*40, dy=20+r()*40, z=1.5+r()*1.5; b.style.left=bx+'px'; b.style.top=by+'px';
      b._im.style.transform=`translate(${(-bx*z+dx).toFixed(1)}px,${(-by*z+dy+59).toFixed(1)}px) scale(${z.toFixed(3)})`; b.style.filter=doTP.style.filter; }); }
}

/* ---------- 25 · Taste Check : le scan TROUVE (cinq écrans v1 jamais touchés : login, tables, e-mails, rapports, mobile) — 47 problèmes ---------- */
const GR=scene('sGrid',1080,1130,f=>shotGrid(f));
const cR25=cueAt(2);
const BORING=[['font-family: Arial',19],['#2D6CDF',11],['drop shadow',6],['stock photo',4],['“Synergy”',3],['users named “User”',3],['stock_handshake_final_v3.jpg',1]];
const grIn=el(GR.cam,'','', 'position:absolute;left:0;top:0;width:2200px;height:1080px');
const grLines=[]; for(let i=0;i<=18;i++) grLines.push(el(grIn,'gline','', `left:${i*120-1}px;top:0;width:2px;height:1080px`));
[120,240,360,480,600,720,840,930,990].forEach(y=>grLines.push(el(grIn,'gline','', `left:0;top:${y-1}px;width:2200px;height:2px`)));
for(const y of [120,240,360,480,600,720,840,930,990]) for(let i=0;i<=18;i++){ const sz=y<200||y>900?14:8; el(grIn,'gdot','', `left:${i*120}px;top:${y}px;width:${sz}px;height:${sz}px;margin:${-sz/2}px 0 0 ${-sz/2}px;border-radius:50%`); }
// cartes posées sur la grille, avec des repères de coupe aux coins
const crop=c=>{ ['0 0','100% 0','0 100%','100% 100%'].forEach((pos,k)=>el(c,'','', `position:absolute;${k%2?'right':'left'}:-10px;${k>1?'bottom':'top'}:-10px;width:18px;height:18px;border-${k>1?'bottom':'top'}:1.5px solid rgba(21,20,19,.35);border-${k%2?'right':'left'}:1.5px solid rgba(21,20,19,.35)`)); c.style.overflow='visible'; return c; };
const grMacroTile=crop(el(grIn,'gcard','', 'left:960px;top:120px;width:720px;height:720px;display:none;filter:grayscale(1) brightness(.62) contrast(1.35)'));
const grMacro=canvas(grMacroTile,720,720,'inset:0;width:100%;height:100%');
const grThumb2=crop(el(grIn,'gcard','', 'left:1680px;top:600px;width:240px;height:240px;display:none;filter:grayscale(1) brightness(.62) contrast(1.3)')); const grMacro2=canvas(grThumb2,240,240,'inset:0;width:100%;height:100%');
const grStat=crop(el(grIn,'gcard','', 'left:240px;top:120px;width:480px;height:240px;display:none'));
el(grStat,'abs m','BORING ISSUES FOUND','left:24px;top:22px;font-size:15px;letter-spacing:.1em;color:#8E877F'); const grNum=el(grStat,'abs ar','0','left:20px;top:58px;font-size:120px;color:#2D6CDF;line-height:1');
const grChips=BORING.map(([t,n],i)=>{ const d=el(grIn,'m','',`position:absolute;height:52px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:24px;line-height:52px;padding:0 20px;display:none;white-space:nowrap`); d._t=`${t} ×${n}`; d._st=1084+i*3; return d; });
const GR_CHP=[[0,58],[600,486],[1700,126],[240,996],[1940,250],[740,250],[360,866]];
const grBars=crop(el(grIn,'gcard','', 'left:600px;top:600px;width:240px;height:240px;display:none')); const grBarE=BORING.map((b,i)=>el(grBars,'','', `position:absolute;left:${22+i*30}px;bottom:30px;width:22px;height:0;border-radius:2px;background:#2D6CDF`));
const grCode=crop(el(grIn,'gcard','', 'left:1680px;top:360px;width:240px;height:240px;background:#151413;display:none'));
const GR_CODE=['check("velvetly.app")','  .screens(5)','  .found(47)']; const grCodeL=GR_CODE.map((t,i)=>el(grCode,'abs m','',`left:16px;top:${30+i*34}px;font-size:16px;color:#F3EFEA`));
const grList=crop(el(grIn,'gcard','', 'left:0;top:360px;width:240px;height:240px;display:none')); const GR_LIST=['login','tables','emails','reports','mobile'];
const grListL=GR_LIST.map((t,i)=>el(grList,'abs m','',`left:18px;top:${24+i*40}px;font-size:22px;color:#151413`));
const grThumb=crop(el(grIn,'gcard','', 'left:360px;top:0;width:120px;height:120px;background:#D9DCE1;display:none')); grThumb.innerHTML+=`<svg width="60" height="48" viewBox="0 0 120 96" style="position:absolute;left:30px;top:36px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg>`;
cR25(1078,'drop2',{}); cR25(1078,'impact',{v:.6}); [1084,1087,1090,1093,1096,1099,1102].forEach(f=>cR25(f,'tick',{v:.3})); for(let k=0;k<9;k++) cR25(1093+k*2.6,'tick',{v:.14});
function shotGrid(F){ const f=F-2;
  // entrée : la grille sort du même flou clair que la page de chaleur (fondu enchaîné 1078-1082), sans recul ni glissement hérités
  const z2=lerp(1.03,1,approach(f,1100,14)); GR.cam.style.transform=`scale(${(f>=1100?z2:1.03).toFixed(4)})`;
  const dz=1-vl(f,1077,5); GR.cam.style.filter=dz>0.01?`blur(${(20*dz).toFixed(1)}px) brightness(${(1+0.3*dz).toFixed(2)}) saturate(${(1-0.6*dz).toFixed(2)})`:'';
  const X=-313*(1-approach(f,1086,40,0.11)), Y=0;
  grIn.style.transform=`translate(${X.toFixed(1)}px,${Y.toFixed(1)}px)`;
  mblur(grIn,vel(t=>-313*(1-approach(t,1086,40,0.11)),f)*BLUR*0.6,0);
  // la macro se révèle en 2 images
  show(grMacroTile,f>=1086); grMacroTile.style.opacity=clamp((f-1085)/2).toFixed(2); if(f>=1086) seqDraw(grMacro,SEQ.macro,6+(f-1087)*0.9,0.56,0.46);
  show(grThumb2,f>=1100); if(f>=1100) seqDraw(grMacro2,SEQ.macro,30+(f-1100)*1.2,0.5,0.5,1.4);
  grChips.forEach((d,i)=>{ const on=f>=d._st; show(d,on); if(!on) return; placeTL(d,GR_CHP[i][0],GR_CHP[i][1]); d.style.translate=`${((1-approach(f,d._st,6))*-60).toFixed(1)}px 0`;
    d.textContent=d._t.slice(0,Math.max(1,Math.floor((f-d._st+1)*2.2))); });
  show(grStat,f>=1093); grNum.textContent=Math.round(47*(1-Math.pow(1-clamp((f-1093)/23),1.4))); show(grThumb,f>=1093);
  show(grBars,f>=1098); grBarE.forEach((b,i)=>{ b.style.height=(lerp(0,BORING[i][1]*9,approach(f,1098+i*1.2,6))).toFixed(1)+'px'; });
  show(grCode,f>=1104); grCodeL.forEach((d,i)=>{ const st=1104+i*3; d.textContent=f>=st?GR_CODE[i].slice(0,(f-st+1)*5):''; });
  show(grList,f>=1096); grListL.forEach((d,i)=>{ const st=1096+i*2; d.textContent=f>=st?`✓ ${GR_LIST[i]}`:''; });
}

/* ---------- 26 · le rapport SUGGÈRE : « vladan suggested 47 changes » ; le fondateur clique « Accept all » ---------- */
const RE=scene('sReport',1131,1175,f=>shotReport(f));
const cR26=cueAt(1);
const reCard=el(RE.cam,'rcard','', 'width:960px;height:420px'); reCard.innerHTML=`<div style="position:absolute;left:40px;top:34px;font-size:38px;letter-spacing:-0.02em">BrandReport <span class="m" style="font-size:16px;color:#F3EFEA;background:#151413;border-radius:8px;padding:4px 10px;margin-left:12px;vertical-align:6px">● velvetly.app</span></div>
  <div style="position:absolute;left:40px;top:96px;display:flex;align-items:baseline;gap:16px"><span class="ar r47" style="font-size:96px;color:#2D6CDF;line-height:1">47</span><span style="font-size:30px">boring issues</span></div>
  <div style="position:absolute;left:40px;top:200px;font-size:20px;color:#5C5650;display:flex;align-items:center;gap:10px"><span style="display:inline-block;width:26px;height:26px;border-radius:13px;background:#FF3D5E;color:#fff;font-size:15px;line-height:26px;text-align:center">v</span>vladan suggested 47 changes</div>
  <div style="position:absolute;left:40px;top:248px;width:560px">
    <div class="ar" style="font-size:24px;line-height:36px;color:#333">font-family: Arial ×19</div>
    <div class="m" style="font-size:24px;line-height:36px;color:#2D6CDF">#2D6CDF ×11</div>
    <div class="m" style="font-size:24px;line-height:36px;color:#151413">users named “User” ×3</div>
    <div class="m" style="font-size:24px;line-height:36px;color:#8E877F">+14 more</div></div>
  <div class="rbars" style="position:absolute;left:620px;top:44px;width:300px">${BORING.map(([t,n])=>`<div style="height:34px;position:relative"><span class="m" style="position:absolute;left:0;top:2px;font-size:13px;color:#5C5650;white-space:nowrap">${t.length>18?t.slice(0,17)+'…':t}</span><span class="m" style="position:absolute;right:0;top:2px;font-size:13px;color:#151413">${n}</span><i style="position:absolute;left:0;top:22px;height:3px;width:${(n/19*300).toFixed(0)}px;background:#151413;transform-origin:0 0;display:block"></i></div>`).join('')}</div>
  <div class="rprog" style="position:absolute;left:40px;bottom:0;height:2px;width:0;background:#151413"></div>`;
const reNum=q1(reCard,'.r47'), reRows=[...q1(reCard,'div[style*="top:248px"]').children], reBars=[...q1(reCard,'.rbars').children];
const reBtn=el(reCard,'abs','Accept all','left:auto;right:44px;top:316px;height:64px;line-height:64px;padding:0 30px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:26px');
const reProg=q1(reCard,'.rprog');
cR26(1130,'impact',{v:.5}); cR26(1161,'click',{v:1}); cR26(1162,'pop',{v:.5,n:84});
function shotReport(F){ const f=F-1;
  RE.cam.style.transform=`scale(${(1+0.0025*(f-1131)).toFixed(4)})`;   // poussée à vitesse constante jusqu'à la coupe (l'ease-out figeait les 4 dernières images)
  // la carte monte (40 px, 10 images), le 47 se compte, les lignes et les barres par catégorie arrivent une à une
  const p=approach(f,1130,6); place(reCard,960,545+40*(1-vl(f,1131,10))); reCard.style.opacity=lerp(0.3,1,p).toFixed(3);
  reNum.textContent='47';   // pas de compte à partir de 0 : dans ce film, 0 veut dire « réglé »
  reRows.forEach((r,i)=>{ const a=vl(f,1137+i*3,4); r.style.opacity=a.toFixed(2); r.style.transform=`translateY(${(8*(1-a)).toFixed(1)}px)`; });
  reBars.forEach((r,i)=>{ const a=vl(f,1139+i*2,5); r.style.opacity=Math.min(1,a*2).toFixed(2); r.lastChild.style.transform=`scaleX(${a.toFixed(3)})`; });
  // le clic du fondateur (1161) : « Applying… 0/47 », une ligne d'encre de 2 px qui atteint 6 % à 1175
  const pr=f==1162?0.955:f>1162?lerp(0.97,1,approach(f,1162,3)):1; reBtn.style.transform=`scale(${pr.toFixed(4)})`; reBtn.textContent=f>=1162?'Applying… 0/47':'Accept all';
  reProg.style.width=(f>=1162?880*0.06*clamp((f-1162)/13):0).toFixed(1)+'px';
  // la cible est lue sur le bouton lui-même (il suit la poussée) : au bout du bouton, le libellé reste lisible
  const bb=reBtn.getBoundingClientRect(), sb=RE.s.getBoundingClientRect(), kb=sb.width/W, tx=(bb.right-sb.left)/kb-18, ty=(bb.bottom-sb.top)/kb-14;
  const cf=twos(f,1145), cp=clamp((cf-1145)/10); cursor(lerp(tx+58,tx,cp),lerp(ty+142,ty,cp),f==1161?1:0,f>=1145,1,cp>=1?'hand':'arrow');
}

/* ---------- 27 · les 47 tuiles ennuyeuses barrées d'un seul trait, puis le trait tiré comme un fil dans la fente de la marque ---------- */
const AL=scene('sAlerts',1176,1250,f=>shotAlerts(f),'dark'); AL.s.style.background='#151413';
const cR27=cueAt(1);
// 47 spécimens, rangés par catégorie : la rature les traverse rangée par rangée
const AL_KIND=[]; BORING.forEach(([t,n],k)=>{ for(let i=0;i<n;i++) AL_KIND.push(k); });
const AL_SPEC=[k=>`<div class="ar" style="position:absolute;inset:0;background:#fff;color:#333;font-size:34px;line-height:72px;text-align:center">Aa</div>`,
  k=>`<div style="position:absolute;inset:0;background:#2D6CDF;border-radius:4px"></div>`,
  k=>`<div style="position:absolute;left:12px;top:10px;right:12px;bottom:18px;background:#fff;box-shadow:0 6px 10px rgba(0,0,0,.5)"></div>`,
  k=>`<div style="position:absolute;inset:0;background:#D9DCE1"><svg width="40" height="32" viewBox="0 0 120 96" style="position:absolute;left:16px;top:20px"><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg></div>`,
  k=>`<div class="ar" style="position:absolute;inset:0;background:#fff;color:#2D6CDF;font-size:15px;font-weight:700;line-height:72px;text-align:center">Synergy</div>`,
  k=>`<div style="position:absolute;inset:0;background:#fff"><span style="position:absolute;left:24px;top:12px;width:24px;height:24px;border-radius:12px;background:#C9CDD3"></span><span class="ar" style="position:absolute;left:0;right:0;top:42px;text-align:center;font-size:13px;color:#777">User</span></div>`,
  k=>`<div style="position:absolute;inset:0;background:#D9DCE1"><svg width="40" height="32" viewBox="0 0 120 96" style="position:absolute;left:16px;top:14px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="7"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg><span class="ar" style="position:absolute;left:3px;right:3px;top:50px;font-size:7px;color:#8A8F97;text-align:center;white-space:nowrap;overflow:hidden">handshake_v3.jpg</span></div>`];
const alTiles=AL_KIND.map((k,n)=>{ const r=Math.floor(n/8), c=n%8; const d=el(AL.cam,'','', `position:absolute;width:72px;height:72px;margin:-36px 0 0 -36px;border-radius:10px;overflow:hidden;display:none`);
  d.innerHTML=AL_SPEC[k](k); d._x=610+c*100; d._y=290+r*100; d._d=Math.hypot(d._x-960,d._y-540); d._k=k; return d; });
const alMaxD=Math.max(...alTiles.map(t=>t._d));
const alCount=el(AL.s,'','', 'position:absolute;left:0;top:0;display:none');
alCount.innerHTML=`<div class="alnum ar" style="font-size:96px;line-height:1;color:#2D6CDF;font-variant-numeric:tabular-nums">47</div><div class="m" style="font-size:24px;color:rgba(243,239,234,.55);margin-top:8px">boring issues left</div>`;
const alNum=q1(alCount,'.alnum');
const alInk=inkLayer(AL.s,{ground:'dark'}); alInk.style.zIndex='3';
const alMark=el(AL.cam,'abs','', 'width:150px;height:150px'); alMark.innerHTML=MARK_SVG;
const alDisc=el(AL.s,'','', 'position:absolute;left:885px;top:465px;width:150px;height:150px;border-radius:50%;background:#FF3D5E;transform:scale(0);z-index:2');
const alFade=el(AL.s,'','', 'position:absolute;left:0;right:0;bottom:0;height:430px;background:linear-gradient(transparent,#3C3C3C);opacity:0');
const alBtn=el(AL.cam,'abs','', 'display:none;overflow:hidden'); const alBtnBar=el(alBtn,'','', 'position:absolute;left:50%;top:50%;width:14px;height:58px;margin:-29px 0 0 -7px;border-radius:7px;background:#EEE9E4;transform-origin:50% 50%');
// M8 : un seul trait, gribouillis sur les six rangées, pause sur la poignée de main, boucle « dele »
const M8=()=>penPlace('G08',[574,254,1346,826]);
const AL_A=[941.25,568.1], AL_B=[979,512];
// le chemin du fil : le trait lui-même, puis de son extrémité jusqu'à la fente (A → B) ; tirer = faire glisser le trait le long de ce chemin
let AL_PATH=null; function alPath(){ if(AL_PATH) return AL_PATH; const st=penResample(M8().flat(),260); const end=st[st.length-1];
  // le fil quitte l'extrémité du trait dans sa direction et arrive dans la fente aligné sur elle (courbe de Bézier) : jamais d'angle vif
  const pre=st[st.length-6], tx=end[0]-pre[0], ty=end[1]-pre[1], tl=Math.hypot(tx,ty)||1, ux=(AL_B[0]-AL_A[0])/Math.hypot(AL_B[0]-AL_A[0],AL_B[1]-AL_A[1]), uy=(AL_B[1]-AL_A[1])/Math.hypot(AL_B[0]-AL_A[0],AL_B[1]-AL_A[1]);
  const c1=[end[0]+tx/tl*220,end[1]+ty/tl*220], c2=[AL_A[0]-ux*260,AL_A[1]-uy*260];
  const lead=[]; for(let i=1;i<=40;i++){ const t=i/40, m=1-t; lead.push([m*m*m*end[0]+3*m*m*t*c1[0]+3*m*t*t*c2[0]+t*t*t*AL_A[0], m*m*m*end[1]+3*m*m*t*c1[1]+3*m*t*t*c2[1]+t*t*t*AL_A[1], lerp(end[2],.6,t), end[3]]); }
  const slot=[]; for(let i=1;i<=8;i++){ const t=i/8; slot.push([lerp(AL_A[0],AL_B[0],t),lerp(AL_A[1],AL_B[1],t),0.6,end[3]]); }
  const P=[...st,...lead,...slot], A=penArc(P); AL_PATH={P,A,Ls:penArc(st).pop(),L:A[A.length-1],AB:Math.hypot(AL_B[0]-AL_A[0],AL_B[1]-AL_A[1])}; return AL_PATH; }
// à quel moment (ms de la prise) le trait passe sur chaque tuile
let AL_CROSS=null; function alCross(){ if(AL_CROSS) return AL_CROSS; const st=M8().flat(); AL_CROSS=alTiles.map(t=>{ for(const p of st) if(Math.abs(p[0]-t._x)<52&&Math.abs(p[1]-t._y)<56) return p[3]; return 1e9; }); return AL_CROSS; }
cR27(1175,'hush',{}); cR27(1186,'scribble',{v:.7,end:1208}); cR27(1210,'reel',{v:.6,end:1228}); cR27(1232,'boom',{v:.8});
function shotAlerts(F){ const f=F-1; push(AL.cam,f,1175,0.0005);
  const ms=(f-1186)*PEN.ms, cross=alCross();
  // le champ est déjà allumé à 1175 (le centre), le reste se remplit jusqu'à 1184 ; à la fin la grille se resserre dans la marque
  // (facteurs de la réf : ×0,87, ×0,73, ×0,73, ×0,73, ×0,71, ×0,52 sur 1226-1231) au lieu de s'éteindre
  const zc=alZ(f);
  alTiles.forEach((t,n)=>{ const a=1175+9*Math.max(0,(t._d/alMaxD-0.3)/0.7); const on=f>=a&&f<1232&&!(n===46&&f>=1213); show(t,on); if(!on) return;
    const sIn=a<=1175?1:clamp((twos(f,Math.floor(a))-a)/3); t.style.left=(960+(t._x-960)*zc)+'px'; t.style.top=(540+(t._y-540)*zc)+'px';
    // les tuiles tiennent pendant que le fil passe : il ne pend jamais seul sur le noir
    const cf=1186+cross[n]/PEN.ms, k=clamp((f-cf)/3), fade=clamp((f-1229)/3), bz=8*(1-zc);
    t.style.transform=`scale(${(sIn*zc*(n===46?1-clamp((f-1210)/3):1)).toFixed(3)})`; t.style.filter=((k>0?`grayscale(${k.toFixed(2)}) `:'')+(bz>0.3?`blur(${bz.toFixed(1)}px)`:'')).trim(); t.style.opacity=((1-0.68*k)*(1-fade)).toFixed(3); });
  // le compteur part du « 47 » du rapport et descend d'une unité par tuile barrée ; à 0, il passe à l'encre fixée
  // pendant le fil (1210-1228), les tuiles qui restent partent avec lui : le compteur finit sur 0 à 1228 et y tient
  let left=47-cross.filter(c=>c<=ms).length; if(f>=1210){ const l0=47-cross.filter(c=>c<=(1210-1186)*PEN.ms).length, t=clamp((f-1210)/18); left=Math.round(lerp(l0,0,t*t*(3-2*t))); }
  show(alCount,f>=1175&&f<1232); const mv=vl(f,1176,8); placeTL(alCount,lerp(800,120,mv),lerp(450,860,mv));
  alNum.textContent=Math.max(0,left); if(left<=0&&f>=1210){ alNum.style.color='#F3EFEA'; alNum.style.fontFamily='ID'; } else { alNum.style.color='#2D6CDF'; alNum.style.fontFamily=''; }
  const ix=inkClear(alInk);
  if(f>=1186&&f<1210) penDraw(ix,M8(),f,1186,{size:13.5,ground:'dark'});
  // 1210-1227 : on tire le fil ; il glisse le long de son propre chemin et entre dans la fente, la queue se défait rangée par rangée
  if(f>=1210&&f<1232){ const T=alPath(); const t=clamp((f-1210)/17), d=(T.L-T.AB)*(t*t*(3-2*t));
    const vis=penSlice(T.P,d/T.L,Math.min(1,(d+T.Ls)/T.L)); const disc=clamp((f-1228)/4), paper=disc>0.6;
    penDraw(ix,[vis.map(p=>[p[0],p[1],p[2],0])],1e6,0,{size:lerp(13.5,14,clamp((f-1224)/3)),uniform:clamp((f-1224)/3),ground:'dark',color:paper?'#EEE9E4':null,wetFrames:0});
    alDisc.style.transform=`scale(${vladan(disc).toFixed(3)})`; }
  else alDisc.style.transform='scale(0)';
  show(alMark,f>=1232&&f<1243); if(f>=1232){ place(alMark,960,540,lerp(1.04,1,approach(f,1232,6))); }
  // 1243-1250 : le disque devient le bouton (228×90, rayon 14, encre) ; la barre se redresse et rétrécit jusqu'au caret : le rouge est dépensé
  const mo=f>=1243?1-Math.pow(1-clamp((f-1243)/7),3):0; show(alBtn,f>=1243);
  if(f>=1243){ Object.assign(alBtn.style,{width:lerp(150,228,mo)+'px',height:lerp(150,90,mo)+'px',borderRadius:lerp(75,14,mo)+'px',background:mixc('#FF3D5E','#151413',mo)});
    place(alBtn,960,540); alBtnBar.style.transform=`rotate(${lerp(33.7,0,mo).toFixed(1)}deg) scale(${lerp(1,0.5,mo).toFixed(3)},${lerp(1,0.55,mo).toFixed(3)})`; alBtnBar.style.width=lerp(9*1.5625,3,mo)+'px'; }
  alFade.style.opacity=approach(f,1243,7).toFixed(3);
  // sortie : petite poussée qui accélère dans la coupe (réf +0,2 → +2 %/image), pas d'image figée
  AL.cam.style.scale=(1+0.04*accel(f,1243,7,2.2)).toFixed(4);
}
const AL_Z=[1,.87,.635,.464,.338,.240,.125];
function alZ(f){ if(f<=1225) return 1; if(f>=1231) return AL_Z[6]; const i=Math.floor(f-1225); return lerp(AL_Z[i],AL_Z[i+1],f-1225-i); }

/* ---------- 28 · la fenêtre de la pièce : le ciel glisse sous le bouton déjà en place, « Ship it » se tape ; le fondateur clique (1295) ---------- */
const SH=scene('sShip',1251,1307,f=>shotShip(f));
const cR28=cueAt(1);
// ciel : les arrêts de la réf mélangés en lumière linéaire, tramés à ±1 (pas de bandes), sur 2310 px de haut
const shSkyC=(()=>{ const c=document.createElement('canvas'); c.width=8; c.height=2310; const x=c.getContext('2d'), im=x.createImageData(8,2310), R=rng(5);
  const st=[[0,'#ECE4DC'],[.25,'#F2E3D5'],[.45,'#F7E2CF'],[.6,'#F9E2CC'],[.75,'#E7DACC'],[.98,'#B3CAC9'],[1,'#B3CAC9']].map(([t,h])=>[t,hex(h).map(v=>Math.pow(v/255,2.2))]);
  for(let y=0;y<2310;y++){ const t=y/2309; let k=0; while(k<st.length-2&&st[k+1][0]<t) k++; const [t0,a]=st[k], [t1,b]=st[k+1], u=clamp((t-t0)/(t1-t0));
    const lin=a.map((v,i)=>lerp(v,b[i],u)); for(let xx=0;xx<8;xx++){ const o=(y*8+xx)*4; lin.forEach((v,i)=>{ im.data[o+i]=clamp(Math.round(Math.pow(v,1/2.2)*255+(R()-R())),0,255); }); im.data[o+3]=255; } }
  x.putImageData(im,0,0); return c; })();
const shSky=el(SH.cam,'','', 'position:absolute;left:-60px;top:-60px;width:2040px;height:2310px');
const shSkyI=document.createElement('img'); shSkyI.src=shSkyC.toDataURL(); shSkyI.style.cssText='position:absolute;inset:0;width:100%;height:100%'; shSky.appendChild(shSkyI);
// la fenêtre d'acier noir vue à 262 : meneaux à x=640/1280, traverse à y=360 ; le dossier du fauteuil rouge entre dans le coin bas-droit (10 %)
const shWin=el(SH.cam,'','', 'position:absolute;inset:0;pointer-events:none');
shWin.innerHTML=`<div style="position:absolute;left:0;top:0;right:0;height:26px;background:#151413"></div><div style="position:absolute;left:0;bottom:0;right:0;height:26px;background:#151413"></div>
  <div style="position:absolute;left:0;top:0;bottom:0;width:26px;background:#151413"></div><div style="position:absolute;right:0;top:0;bottom:0;width:26px;background:#151413"></div>
  <div style="position:absolute;left:631px;top:0;bottom:0;width:18px;background:#151413;box-shadow:inset 1px 0 0 #1E1C1B"></div><div style="position:absolute;left:1271px;top:0;bottom:0;width:18px;background:#151413;box-shadow:inset 1px 0 0 #1E1C1B"></div>
  <div style="position:absolute;left:0;right:0;top:351px;height:18px;background:#151413;box-shadow:inset 0 1px 0 #1E1C1B"></div>
  <div style="position:absolute;left:-60px;right:-60px;top:1080px;height:900px;background:linear-gradient(180deg,#8E7F73 0,#7B6D63 220px,#665a52 900px)"></div>
  <div style="position:absolute;left:-60px;right:-60px;top:1080px;height:16px;background:#B7A799;box-shadow:0 1px 0 #CDBFB1 inset,0 10px 24px rgba(40,30,25,.35)"></div>`;
// le fauteuil détouré (img/ship_chair.png, tiré de red_60), à contre-jour devant le mur ; il monte avec la pièce quand la caméra descend
const shChair=el(SH.cam,'','', 'position:absolute;left:1520px;top:1168px;width:665px;height:602px');
shChair.innerHTML='<img src="img/ship_chair.png" style="width:100%;height:100%;filter:brightness(.6) contrast(1.08) saturate(.95) ">';
// l'ombre du fauteuil sur le sol (sous le cadre, à contre-jour, elle vient vers nous)
const shChairSh=el(SH.cam,'','', 'position:absolute;left:1500px;top:1500px;width:720px;height:140px;border-radius:50%;background:radial-gradient(closest-side,rgba(21,20,19,.35),rgba(21,20,19,0));filter:blur(14px)');
// le soleil entre en biais par la fenêtre : un rayon chaud très léger sur le mur et le fauteuil
const shShaft=el(SH.cam,'','', 'position:absolute;left:-200px;top:-200px;width:2320px;height:1280px;pointer-events:none;mix-blend-mode:screen;background:linear-gradient(118deg,transparent 34%,rgba(255,240,224,1) 43%,rgba(255,240,224,1) 50%,transparent 59%)');
// la tache de soleil au sol, dans le prolongement du rayon : parallélogramme à −28°, + ~18 niveaux (screen), bord flou
SH.cam.insertBefore(shShaft,shWin);   // le rayon passe sous le cadre : les montants restent mats
// les montants (x 632 et 1287) projettent leur ombre dans la tache : c'est le soleil à travers CETTE fenêtre
const shPatch=el(SH.cam,'','', `position:absolute;left:480px;top:1100px;width:960px;height:720px;pointer-events:none;mix-blend-mode:screen;filter:blur(10px);transform-origin:50% 0;background:rgba(255,236,214,.24);${['-webkit-mask','mask'].map(k=>`${k}-image:linear-gradient(90deg,#000 0 139px,transparent 139px 165px,#000 165px 794px,transparent 794px 820px,#000 820px),linear-gradient(180deg,#000 0 330px,transparent 330px 352px,#000 352px 620px,transparent 720px);`).join('')}-webkit-mask-composite:source-in;mask-composite:intersect`);   // ombres des montants (x 632, 1287) et de la traverse haute
// dehors : une silhouette d'arbre très floue (4 % d'encre) qui glisse contre la poussée (parallaxe)
const shTree=el(SH.cam,'','', 'position:absolute;left:1180px;top:240px;width:760px;height:900px;pointer-events:none;filter:blur(30px);background:radial-gradient(38% 30% at 45% 40%,rgba(21,20,19,.05),transparent),radial-gradient(30% 26% at 70% 55%,rgba(21,20,19,.045),transparent),radial-gradient(8% 40% at 52% 90%,rgba(21,20,19,.04),transparent)');
SH.cam.insertBefore(shTree,shWin);
// les vitres : plus fraîches en haut, plus chaudes en bas (elles suivent la fenêtre)
const shPane=el(SH.cam,'','', 'position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none;opacity:.5;background:linear-gradient(#F3EAE3,#F7E3D0)'); SH.cam.insertBefore(shPane,shTree);
const shBtn=el(SH.s,'bbtn',''); shBtn.style.zIndex=5; shBtn.style.width='228px'; shBtn.style.padding='0'; shBtn.style.textAlign='center'; shBtn.style.borderRadius='14px';
const shRing=el(SH.s,'','', 'position:absolute;left:960px;top:540px;width:0;height:0;border-radius:50%;box-shadow:0 0 0 1px #151413;z-index:4');
cR28(1250,'impact',{v:.5}); cR28(1293,'beep',{v:.6}); cR28(1298,'riser',{v:.55,end:1306});
function shotShip(F){ const f=F-1; SH.cam.style.transform=`scale(${(1+0.03*clamp((f-1250)/56)).toFixed(4)})`;   // poussée de 3 %
  const y=-900*approach(f,1250,36,0.11);
  // le rayon (≈ +14 niveaux sur les vitres) glisse de 60 px pendant le plan ; il ne descend pas sur le mur
  shShaft.style.opacity='0.5'; shShaft.style.transform=`translateX(${(60*clamp((f-1250)/56)).toFixed(1)}px)`; shShaft.style.clipPath=`inset(0 0 ${Math.max(0,1280-(200+1080+y*0.35)).toFixed(0)}px 0)`;
   shSky.style.transform=`translateY(${y.toFixed(1)}px)`; shWin.style.transform=`translateY(${(y*0.35+0).toFixed(1)}px)`; shChair.style.transform=`translateY(${(y*0.42).toFixed(1)}px)`; shChairSh.style.transform=`translateY(${(y*0.42).toFixed(1)}px)`;
  shPatch.style.transform=`translate(${(60*clamp((f-1250)/56)).toFixed(1)}px,${(y*0.42).toFixed(1)}px) skewX(-28deg)`;
  // la tache commence sous le rail bas de la fenêtre (jamais par-dessus) ; l'arbre dehors suit le ciel, en retard
  shPatch.style.clipPath=`inset(${Math.max(0,(1080+y*0.35)-(1100+y*0.42)+2).toFixed(0)}px 0 0 0)`;
  shPane.style.transform=`translateY(${(y*0.35).toFixed(1)}px)`; shTree.style.transform=`translate(${(-10*clamp((f-1250)/56)).toFixed(1)}px,${(y*0.6).toFixed(1)}px)`;
  const n=clamp(f-1250,0,7); shBtn.innerHTML='Ship it'.slice(0,n)+(f<1262||Math.floor(f/8)%2?'<span style="display:inline-block;width:3px;height:40px;background:#F3EFEA;vertical-align:-6px;margin-left:3px"></span>':'');
  // le clic tombe à 1293, comme dans la réf
  const pr=f>=1293&&f<1295; place(shBtn,960,540,pr?0.94:1); shBtn.style.background='#151413';
  const rg=clamp((f-1293)/10); show(shRing,f>=1293&&f<1304); const R=120*rg; Object.assign(shRing.style,{width:2*R+'px',height:2*R+'px',left:(960-R)+'px',top:(540-R)+'px',opacity:(1-rg).toFixed(2)});
  const cf=twos(f,1270), cp=clamp((cf-1270)/10); cursor(lerp(1185,1030,cp),lerp(705,580,cp),pr?1:0,f>=1270,1,cp>=1?'hand':'arrow');
}

/* ---------- 29-30 · montage après le Ship : le seul résultat, la table v1 re-composée, la marque sur un objet, la landing (coupes de la réf) ---------- */
const MO=scene('sMont',1308,1378,f=>shotMont(f)); sky(MO.cam);
const cR29=cueAt(1);
const moP=el(MO.cam); const moPD=framed(moP,tplVInsights(),1368,912,1240,730,VINK);
// le planning après le stylo : « Ship » a pris la place de « Taste Check » (ven. 23), contour encre
const moR=el(MO.cam); const moRD=framed(moR,tplPlan(),1368,912,1620,1080,'#F6F2EE');   // recadré en largeur : pas de bande au-dessus de la barre latérale
(()=>{ const c=qa(moRD,'.pchip'), a=c[0], b=c[4], [al,at]=[a.style.left,a.style.top]; a.style.left=b.style.left; a.style.top=b.style.top; b.style.left=al; b.style.top=at; a.classList.remove('fd'); })();
// le rapport, une fois appliqué : 0 problème ennuyeux, les barres se vident
const tplReport0=()=>`<div class="full" style="background:#F7F4F0;color:#151413">
  <div style="position:absolute;left:72px;top:64px;font-size:44px;letter-spacing:-0.02em">BrandReport <span class="m" style="font-size:18px;color:#F3EFEA;background:#151413;border-radius:8px;padding:5px 12px;margin-left:14px;vertical-align:8px">● velvetly.app</span></div>
  <div style="position:absolute;left:64px;top:150px;display:flex;align-items:baseline;gap:22px"><span style="font-size:300px;line-height:.9;letter-spacing:-0.05em">0</span><span style="font-size:44px;letter-spacing:-0.02em">boring issues</span></div>
  <div class="m" style="position:absolute;left:74px;top:470px;font-size:22px;color:#5C5650">✓ 47 / 47 applied · Tue 20 Oct · ships Fri 23</div>
  <div class="mbars" style="position:absolute;left:760px;top:150px;width:400px">${BORING.map(([t,n])=>`<div style="height:46px;position:relative"><span class="m" style="position:absolute;left:0;top:2px;font-size:16px;color:#8E877F;text-decoration:line-through;text-decoration-color:#151413;white-space:nowrap">${t.length>22?t.slice(0,21)+'…':t}</span><span class="m" style="position:absolute;right:0;top:2px;font-size:16px;color:#151413">0</span><i style="position:absolute;left:0;top:28px;height:3px;width:${(n/19*400).toFixed(0)}px;background:#151413;transform-origin:0 0;display:block"></i></div>`).join('')}</div>
  <div style="position:absolute;right:80px;bottom:70px;height:64px;line-height:64px;padding:0 30px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:26px">Ship it</div></div>`;
const moDa=el(MO.cam); const moDaD=framed(moDa,tplReport0(),1368,912,1240,730,'#F7F4F0'); const moBars=[...q1(moDaD,'.mbars').children];
const moL=el(MO.cam); const moLD=framed(moL,tplVLanding(),1368,912,1240,730,VINK);
const moLSeq=q1(moLD,'.vseq'), moLXr=q1(moLD,'.vxr'), moLh=qa(moLD,'.lnh'), moLT=qa(moLD,'.vix'), moStat=q1(moPD,'.mst'), moStat2=q1(moPD,'.mst2');
const MOS=[[moP,1307],[moR,1325],[moDa,1336],[moL,1349]];
cR29(1307,'impact',{v:.7}); cR29(1325,'impact',{v:.6}); cR29(1336,'impact',{v:.6}); cR29(1349,'impact',{v:.7}); [1312,1314,1315].forEach(f=>cR29(f,'tick',{v:.2})); cR29(1372,'shimmer',{v:.45,end:1378});
// les fragments corrigés reviennent à la place exacte de leurs jumeaux ennuyeux (5, lisibles, 30 px), à cheval sur la fin du montage
const OU_FIX=[[4,'/* done. it sits. */'],[10,'/* nothing is !important */'],[13,'cursor: you;'],[5,'<h1>Morning, Léa.</h1>'],[12,'ease: vladan;']];
const moFix=OU_FIX.map(([i,t])=>{ const d=el(MO.s,'abs frag','','font-size:30px;z-index:20;display:none'); d.textContent=t; d._i=i; return d; });
// les fragments ne figent plus puis ne sautent plus : ils se rassemblent vers le centre en accélérant (1379-1390), jusqu'au point
function fixFrags(list,f,f0){ const G=1-0.92*accel(f,1379,11,2.2); list.forEach(d=>{ const on=f>=f0&&f<1390; show(d,on); if(!on) return; const src=wFr[d._i];
  placeTL(d,960+(src._x-960)*G,540+(src._y-540)*G,G); d.style.color=mixc('#FFC2CD','#151413',clamp((f-f0)/6)); d.style.opacity=(1-clamp((f-1387)/3)).toFixed(2); }); }
function shotMont(F){ const f=F-1; let cur=MOS[0]; for(const m of MOS) if(f>=m[1]) cur=m;
  MOS.forEach(m=>show(m[0],m===cur)); const a=f-cur[1];
  let sc=1; if(cur[0]===moP) sc=1+0.035*approach(f,1307,18,0.12); else if(cur[0]===moR) sc=1+0.0007*a; else if(cur[0]===moDa) sc=1+0.0016*a; else sc=1-0.03*accel(f,1366,12,2);
  place(cur[0],960,540,sc);
  // les chiffres se comptent (1308-1316) au lieu de sauter de +14 % à +45 % en une image ; même format que le téléphone
  if(cur[0]===moP){ const c=ease3(clamp((f-1308)/8)); moStat.firstChild.textContent='+'+Math.round(lerp(14,45,c))+'%'; moStat2.textContent='0:'+Math.round(lerp(52,42,c)); }
  if(cur[0]===moDa) moBars.forEach((r,i)=>{ r.lastChild.style.transform=`scaleX(${(1-vl(f,1336+i*0.4,3)).toFixed(3)})`; });   // toutes à 0 dès 1342
  // panoramique au rythme de la réf (≈ 5 px/image : le cadre dérive, le titre glisse un peu moins, sans être rogné) ; 1374-1377 : la vague de chaleur passe sur la landing (25, 60, 100 %) avant les fragments
  // la reprise : la même landing, loupe déjà ouverte sur le fauteuil
  if(cur[0]===moL){ seqDraw(moLSeq,SEQ.land,a*1.0,0.5,0.58); seqDraw(moLXr,SEQ.landX,a*1.0,0.5,0.58); landLens(moLD,110,lerp(1040,1095,a/29),330,'');
    place(cur[0],960-3*a,540,sc); moLh.forEach(h=>h.style.transform=`translateX(${(-0.8*a).toFixed(1)}px)`);
    const hk=[0,.25,.6,1,1][clamp(f-1373,0,4)]; cur[0].style.filter=hk>0?`sepia(${hk}) saturate(${(1+3*hk).toFixed(2)}) hue-rotate(${(-28*hk).toFixed(1)}deg) contrast(${(1+0.25*hk).toFixed(2)}) brightness(${(1+0.18*hk).toFixed(2)})`:'';
    moLT.forEach((t,i)=>{ const p=approach(f,1350+i,8,0.2); t.style.translate=`0 ${((1-p)*24).toFixed(1)}px`; }); }
  fixFrags(moFix,f,1366);
}

/* ---------- 31-32 · fragments corrigés → anneau → marque → « vladan » + « Made in code. Marked up by hand. » → la carte de fin : le brief était un e-mail à Vladan ---------- */
const OU=scene('sOutro',1380,1559,f=>shotOutro(f));
const cR31=cueAt(2);
const ouFix=OU_FIX.map(([i,t])=>{ const d=el(OU.s,'abs frag','','font-size:30px;z-index:20;display:none'); d.textContent=t; d._i=i; return d; });   // textContent : « <h1> » reste du code
const ouGl=gset(16,77,420,190).map(g=>{ const d=el(OU.cam,'abs c glyph'); d._g=g; d.textContent=g[0]; d.style.color=GINK; return d; });
const ouDot=el(OU.cam,'abs','', 'border-radius:50%');
const ouMark=el(OU.cam,'abs','', 'width:81px;height:81px'); ouMark.innerHTML=MARK_SVG;
const ouWord=el(OU.cam,'abs','vladan','font-size:84px;font-weight:600;letter-spacing:-0.04em;line-height:1');
const ouLine=el(OU.cam,'abs m','Made in code. Marked up by hand.','font-size:26px;color:#6E6862');
// la pill où le fondateur tape (en Arial) « Give it taste. »
const ouPill=el(OU.cam,'abs',`<svg width="100%" height="100%" style="overflow:visible"><rect x="1.75" y="1.75" rx="41.5" pathLength="1" fill="none" stroke="#151413" stroke-width="3.5"/></svg>`,'height:86px;overflow:visible');
const ouRect=q1(ouPill,'rect');
const OUW=[[1448,'Give'],[1453,'it'],[1467,'taste.']];
const ouWords=OUW.map(([f,h])=>el(OU.cam,'abs ar',h,'font-size:48px;line-height:1;color:#151413;transform-origin:0 0'));
// « taste. » en Besley, pour le fondu lettre à lettre de la fin
const ouTasteB=el(OU.cam,'abs','<em class="big" style="font-weight:400">taste.</em>','line-height:1;display:none;transform-origin:0 0');
// la carte : le même champ que le brief (174), devenu un e-mail
const OU_CH=470; // hauteur de la carte : l'en-tête TO / RE (226) + le brief + la citation, sans toucher le « + »
const ouCard=el(OU.cam,'','', `position:absolute;left:144px;top:440px;width:1500px;height:${OU_CH}px;border-radius:28px;background:#F8F6F3;box-shadow:0 30px 60px -30px rgba(60,40,40,.25);display:none;overflow:hidden`);
ouCard.innerHTML=`<div class="oto" style="position:absolute;left:44px;top:0;right:44px;height:0;overflow:hidden">
    <div class="m" style="position:absolute;left:0;top:58px;font-size:20px;letter-spacing:.08em;color:#8E877F">TO</div><div class="otoa" style="position:absolute;left:150px;top:16px;font-size:92px;letter-spacing:-0.012em;line-height:1"></div>
    <div style="position:absolute;left:0;right:0;top:126px;height:1px;background:#E2DBD3"></div>
    <div class="m" style="position:absolute;left:0;top:157px;font-size:20px;letter-spacing:.08em;color:#8E877F">SUBJECT</div><div style="position:absolute;left:150px;top:148px;font-size:30px;color:#5C5650">Re: Your SaaS is a bit boring.</div>
    <div style="position:absolute;left:0;right:0;top:206px;height:1px;background:#E2DBD3"></div></div>
  <div class="obody" style="position:absolute;left:44px;top:44px;right:200px">
    <div class="ar obrief" style="font-size:28px;line-height:1.45;color:#6E6862"></div>
    <div style="margin-top:14px;padding-left:14px;border-left:2px solid #D6CFC7;font-size:24px;color:#8E877F">Brand, UI and motion for SaaS.</div></div>
  <div style="position:absolute;left:40px;bottom:30px;width:48px;height:48px;border-radius:24px;box-shadow:inset 0 0 0 1.5px #CFC8C0;color:#8E877F;font-size:30px;line-height:46px;text-align:center">+</div>
  <div class="omodel" style="position:absolute;right:124px;bottom:34px;font:500 24px 'ID';color:#151413;background:#ECE6DF;border-radius:10px;padding:6px 12px;display:flex;align-items:center;overflow:hidden;white-space:nowrap"><span class="omc">@</span><span class="omw">vladan</span></div>
  <div class="osend" style="position:absolute;right:30px;bottom:24px;width:72px;height:72px;border-radius:36px;background:#151413"><svg viewBox="0 0 72 72" width="72" height="72"><path d="M36 50 V22 M24 33 L36 21 L48 33" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>`;
const ouTo=q1(ouCard,'.oto'), ouToA=q1(ouCard,'.otoa'), ouBody=q1(ouCard,'.obody'), ouBrief=q1(ouCard,'.obrief'), ouModel=q1(ouCard,'.omodel'), ouMW=q1(ouCard,'.omw'), ouMC=q1(ouCard,'.omc'), ouSend=q1(ouCard,'.osend');
ouBrief.innerHTML=prSeg(PROMPT.length);
const ouFly=el(OU.cam,'abs','vladan','font:500 26px ID;color:#151413;line-height:1;display:none;transform-origin:0 0');
const ouInk=inkLayer(OU.cam);
let OUL={};
function outroLayout(){ OUL.ws=ouWords.map(e=>e.offsetWidth); OUL.ww=ouWord.offsetWidth; OUL.lw=ouLine.offsetWidth;
  show(ouTasteB,true); OUL.tb=ouTasteB.offsetWidth; show(ouTasteB,false); }
cR31(1378,'shimmer',{v:.35,end:1386}); cR31(1385,'reverse',{v:.6,end:1393}); cR31(1393,'boom',{v:1.15}); cR31(1408,'shimmer',{v:.4,end:1416});
OUW.forEach(([f],i)=>cR31(f,'key',{v:.4})); cR31(1439,'swish',{v:.3,peak:1446,dur:7}); cR31(1492,'final',{}); cR31(1524,'tick',{v:.25}); cR31(1508,'scratch',{v:.8,end:1516});
// la ligne « Give it taste. » : dans la pill (48 px), puis titre de 200 px aligné à x=144, ligne de base ≈ 300
function ouLineGeom(f){ const sp=12, pad=30; const TW=OUW.map((_,i)=>OUL.ws.slice(0,i+1).reduce((a,b)=>a+b+sp,0)-sp); let tw=TW[0]; for(let i=1;i<OUW.length;i++) tw=lerp(tw,TW[i],approach(f,OUW[i][0],9,0.5));
  const h=vl(f,1489,10); const S=lerp(1,200/48,h); const x0=lerp(960-tw/2,144,h), y0=lerp(540-26,120,h); return {tw,S,x0,y0,sp,pad,h}; }
function shotOutro(F){ const f=F-2; push(OU.cam,f,1378,f<1489?0.0008:0);
  const OS=f>=1520?1+0.015*(1-Math.pow(1-clamp((f-1520)/39),2)):1; if(f>=1520) OU.cam.style.transform=`scale(${OS.toFixed(4)})`;   // l'affiche respire : 1,5 % de poussée, pas un arrêt sur image
  fixFrags(ouFix,f,1366);
  // anneau de glyphes à l'encre (1385-1391), le point à l'encre puis rouge à l'arrivée de la marque (1398)
  const k=lerp(1,0.7,approach(f,1387,6)); ouGl.forEach((d,i)=>{ const on=f>=1385&&f<1392; show(d,on); if(!on) return; const g=d._g; place(d,960+g[1]*k,540+g[2]*k); });
  const dOn=f>=1390&&f<1398; show(ouDot,dOn); if(dOn){ const S=f<1394?lerp(90,120,(f-1390)/4):lerp(120,81,approach(f,1394,4)); Object.assign(ouDot.style,{width:S+'px',height:S+'px',background:f<1396?mixc('#CDB9F2','#FF8FA3',clamp((f-1390)/6)):'#FF3D5E'}); place(ouDot,960,540); }
  const tot=81+24+OUL.ww; const slide=approach(f,1404,4); const logoOn=f>=1398&&f<1448;
  show(ouMark,logoOn); show(ouWord,logoOn&&f>=1408); show(ouLine,logoOn&&f>=1408);
  if(logoOn){ const an=accel(f,1439,8,2), ex=-40*an, es=1-0.04*an, st=approach(f,1408,9);
    const mx=lerp(960,960-tot/2+40.5,slide)+ex; place(ouMark,mx,540,(f<1400?lerp(0.9,1,(f-1398)/2):1)*es);
    if(f>=1408){ placeTL(ouWord,mx+40.5+24+12*st,540-42,es*(1+0.035*st)); ouWord.style.color=mixc('#FFC2CD','#151413',approach(f,1408,8));
      const ds=clamp((f-1445)/3); [ouWord,ouLine].forEach(e=>e.style.webkitMaskImage=e.style.maskImage=ds>0?`linear-gradient(90deg,transparent ${(ds*100-10).toFixed(0)}%,#000 ${(ds*100+10).toFixed(0)}%)`:''); ouMark.style.opacity=(1-ds).toFixed(2);
      placeTL(ouLine,960-OUL.lw/2,540+42+64-26); ouLine.style.opacity=vl(f,1408,6).toFixed(3); } }
  // la pill : le fondateur tape « Give it taste. » en Arial ; elle se dé-trace (1486-1489) et la ligne devient le titre
  const G=ouLineGeom(f); let k2=-1; OUW.forEach(([wf],i)=>{ if(f>=wf) k2=i; });
  const pw=G.tw+2*G.pad; const pOn=f>=1448&&f<1490; show(ouPill,pOn); if(pOn){ Object.assign(ouPill.style,{width:pw+'px',left:(960-pw/2)+'px',top:'497px'});
    ouRect.setAttribute('width',Math.max(0,pw-3.5)); ouRect.setAttribute('height',86-3.5); ouRect.setAttribute('stroke-dasharray','1'); ouRect.setAttribute('stroke-dashoffset',(-clamp((f-1486)/3)).toFixed(3)); }
  let cx=G.x0; const morph=f>=1515;
  ouWords.forEach((d,i)=>{ show(d,i<=k2); if(i>k2) return; placeTL(d,cx,G.y0,G.S); cx+=(OUL.ws[i]+G.sp)*G.S;
    if(i==2){ // « taste. » passe de l'Arial du fondateur au Besley, lettre à lettre (1515-1520)
      const n=morph?clamp(f-1514,0,6):0; d.innerHTML=[...'taste.'].map((c,j)=>`<span style="opacity:${j<n?0:1}">${c}</span>`).join(''); } });
  show(ouTasteB,morph); if(morph){ const x=G.x0+(OUL.ws[0]+OUL.ws[1]+2*G.sp)*G.S, n=clamp(f-1514,0,6); ouTasteB.firstChild.style.fontSize=(48*G.S*1.07*0.97)+'px';
    ouTasteB.firstChild.innerHTML=[...'taste.'].map((c,j)=>`<span style="opacity:${j<n?1:0}">${c}</span>`).join(''); placeTL(ouTasteB,x,G.y0-0.18*48*G.S); }
  // la carte (1492-1498), l'en-tête TO / SUBJECT (1496-1500), « vladan » sort du sélecteur de modèle et vole dans TO (1499-1505), « @kwinndo.fr » se tape (1505-1510)
  // puis le soulignement (1508-1516), l'italique (1515-1520), la main sur Envoyer (1524) et l'affiche tient jusqu'à la fin
  const cOn=f>=1492; show(ouCard,cOn);
  if(cOn){ const r=vl(f,1492,6); ouCard.style.translate=`0 ${(18*(1-r)).toFixed(1)}px`; ouCard.style.opacity=r.toFixed(3);
    const hh=226*vl(f,1496,4); ouTo.style.height=hh+'px'; ouBody.style.top=(44+hh*(212/226))+'px';
    const fl=clamp((f-1499)/6), fe=vladan(fl); ouMC.style.opacity=(1-clamp((f-1499)/2)).toFixed(2); ouMW.style.visibility=f>=1499?'hidden':'visible'; { const q=clamp((f-1499)/3); ouModel.style.width=f>=1499?lerp(84,0,q)+'px':''; ouModel.style.padding=f>=1499?`6px ${lerp(12,0,q).toFixed(1)}px`:''; ouModel.style.opacity=f>=1499?(1-q).toFixed(2):''; }
    const cr=ouCard.getBoundingClientRect(), st=OU.s.getBoundingClientRect(), kk=st.width/W;
    show(ouFly,f>=1499&&f<1505); if(f>=1499&&f<1505){ const sx=144+1500-130-110, sy=440+OU_CH-38-26, tx=144+44+150, ty=440+16+5; const cx=1480, cy=430, m=1-fe; const x=m*m*sx+2*m*fe*cx+fe*fe*tx, y=m*m*sy+2*m*fe*cy+fe*fe*ty;   // remonte le bord droit puis file dans TO : jamais au-dessus du texte
      placeTL(ouFly,x,y,lerp(1,92/26,fe)); }
    ouToA.textContent=f<1505?'':'vladan'+'@kwinndo.fr'.slice(0,Math.floor((f-1505+1)*2));
    // le trait M3 séché, toujours sur « Arial, »
    const ix=inkClear(ouInk); const sp=q1(ouBrief,'.ari'); if(sp&&r>0.5){ const b=sp.getBoundingClientRect(); const cx_=v=>960+(v-960)/OS, cy_=v=>540+(v-540)/OS; const rr=[cx_((b.left-st.left)/kk),cy_((b.top-st.top)/kk),cx_((b.right-st.left)/kk),cy_((b.bottom-st.top)/kk)];   // écran → caméra (la poussée finale)
      penDraw(ix,penPlace('G03',[rr[0]-6,rr[3]-28*0.52*0.5-9,rr[2]+10,0]),1e6,0,{size:3.4,alpha:r}); }
    // M9 : le stylo souligne « taste. » (1508-1516) ; le soulignement dépasse quand l'italique, plus étroit, prend sa place
    if(f>=1508){ const x=G.x0+(OUL.ws[0]+OUL.ws[1]+2*G.sp)*G.S, w=OUL.ws[2]*G.S; penDraw(ix,penPlace('G09',[x-4,G.y0+48*G.S*0.98,x+w+8,0]),f,1508,{size:13}); } }
  // le fondateur revient (linéaire, sur deux images) ; à 1524 la main survole Envoyer, au même décalage qu'à 206. Il ne clique jamais : le bouton ne change pas.
  // la cible est lue sur le bouton lui-même (il suit la poussée) ; à 1542 la main hésite (6 px vers Envoyer, puis revient) ; anneau de survol, jamais pressé
  const cf=twos(f,1516), cp=clamp((cf-1516)/8); let sx2=144+1500-30-36, sy2=440+OU_CH-24-36;
  if(f>=1492){ const b=ouSend.getBoundingClientRect(), st=OU.s.getBoundingClientRect(), kk=st.width/W; sx2=((b.left+b.right)/2-st.left)/kk; sy2=((b.top+b.bottom)/2-st.top)/kk; }
  const hz=f>=1542&&f<1550?Math.sin(Math.PI*(f-1542)/8)*6:0;
  cursor(lerp(1760,sx2-4,cp)-hz*0.7,lerp(1010,sy2+4,cp)-hz*0.7,0,f>=1516,1,f>=1524?'hand':'arrow');
  ouSend.style.boxShadow=f>=1524?`0 0 0 ${(4*vl(f,1524,4)).toFixed(1)}px rgba(21,20,19,.3)`:'';
}
