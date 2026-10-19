/* ============================================================
   Plans 17 à 32
   ============================================================ */

/* ---------- 17-19 · terminal : npm uninstall boring --force → add taste → éditeur ---------- */
const TE=scene('sTerm',696,815,f=>shotTerm(f),'dark');
const teBig=el(TE.cam,'abs','<span style="color:#FF3D5E">→</span>','font-size:250px;line-height:1');
const teBigCaret=el(TE.cam,'abs','', 'width:12px;height:264px;border-radius:3px');
const teLine=el(TE.cam,'abs tt'); const teCaret=el(TE.cam,'abs','', 'width:6px;height:112px;background:#F2EEE8');
const tePanel=el(TE.cam,'tpanel'); const teDim1=el(tePanel,'abs m','saasly / src / taste.ts','left:26px;top:18px;font-size:16px;color:#3E3B38');
const teDim2=el(tePanel,'abs m','ln 12 · utf-8 · typescript','right:26px;bottom:16px;left:auto;font-size:16px;color:#3E3B38');
const tePanelLine=el(TE.cam,'abs tt','', 'font-size:84px');
const CODE=[['<span class="k">export const</span> taste = {',0],['  font: <span class="s">"Inter Display"</span>,',1],['  accent: <span class="s">"#FF3D5E"</span>,   <span class="c">// one. used well.</span>',2],['  ease: <span class="s">"out"</span>,',3],
  ['  motion: { arrive: <span class="s">"fast"</span>, land: <span class="s">"soft"</span> },',4],['  arial: <span class="k">false</span>,',5],['  stockPhotos: <span class="n">0</span>,',6],['};',7],['',8],['app.use(taste);   <span class="c">// the whole trick</span>',9]];
const teCode=CODE.map(([h,i])=>{ const d=el(tePanel,'cline'); d.innerHTML=`<span class="n" style="display:inline-block;width:56px">${i+1}</span>${h}`; d.style.left='40px'; d.style.top=(70+i*50)+'px'; return d; });
const teSel=el(tePanel,'','', 'position:absolute;left:96px;top:0;height:44px;border-radius:6px;background:rgba(255,61,94,.22)');
const teBlack=el(TE.s,'','', 'position:absolute;inset:0;background:#000;opacity:0;pointer-events:none');
const TEW=[[750,'<em style="font-size:96px">taste.</em>'],[759,'mo'],[762,'moti'],[765,'motion']];
let TEL={};
function termLayout(){ teLine.innerHTML='<span style="color:#FF3D5E">→</span> npm uninstall <span class="tsel">boring</span> <span class="tsel2">--force</span>'; TEL.w=teLine.offsetWidth; teLine.innerHTML=''; TEL.x0=960-TEL.w/2; }
for(let i=0;i<13;i++) cue(708+Math.round(i*1.6),'key',{v:.4});
cue(696,'break',{}); cue(732,'tick',{v:.45}); cue(738,'tick',{v:.45}); cue(750,'enter',{v:.8}); [759,762,765].forEach(f=>cue(f,'key',{v:.35}));
cue(768,'swish',{v:.3,peak:771,dur:8}); for(let i=0;i<10;i++) cue(772+i*3,'key',{v:.18});
function shotTerm(f){ const lf=f-696;
  const big=f<708; show(teBig,big); show(teBigCaret,big);
  if(big){ place(teBig,920,540,lerp(1.08,1,approach(f,696,6))); placeTL(teBigCaret,1100,408); teBigCaret.style.background=f<700?'#9C86FF':'#FF3D5E'; teBigCaret.style.visibility=Math.floor(f/5)%2==0?'visible':'hidden'; }
  const lineMode=f>=708&&f<750; show(teLine,lineMode); show(teCaret,lineMode);
  if(lineMode){ const cmd='npm uninstall'; const n=clamp(Math.floor((f-708)/1.6)+1,0,cmd.length);
    let h='<span style="color:#FF3D5E">→</span> '+cmd.slice(0,n); if(f>=732) h+=' <span class="tsel">boring</span>'; if(f>=738) h+=' <span class="tsel2">--force</span>';
    teLine.innerHTML=h; placeTL(teLine,TEL.x0,540-52); placeTL(teCaret,TEL.x0+teLine.offsetWidth+8,540-56); teCaret.style.visibility=(f<738||Math.floor(f/6)%2==0)?'visible':'hidden'; }
  const panel=f>=750; show(tePanel,panel); show(tePanelLine,panel&&f<768);
  if(panel){ const g=approach(f,768,10); const pw=lerp(1280,1440,g), ph=lerp(300,620,g);
    Object.assign(tePanel.style,{left:(960-pw/2)+'px',top:(540-ph/2)+'px',width:pw+'px',height:ph+'px'});
    let w=''; for(const [wf,t] of TEW) if(f>=wf) w=t;
    tePanelLine.innerHTML=`<span style="color:#8E877F">→</span> <span style="color:#FF3D5E">add</span>&nbsp;&nbsp;${w}`; placeTL(tePanelLine,960-430,540-44);
    teCode.forEach((d,i)=>{ const st=770+i*3.2; const on=f>=st; show(d,on); if(on) d.style.clipPath=`inset(0 ${((1-approach(f,st,6))*100).toFixed(0)}% 0 0)`; });
    show(teSel,f>=790); if(f>=790){ const sp=approach(f,790,6); Object.assign(teSel.style,{top:(70+5*50-6)+'px',width:(330*sp)+'px'}); } }
  const zoom=f<768?1+0.0012*lf:lerp(1+0.0012*72,1.24,approach(f,768,40)); TE.cam.style.transform=`scale(${zoom.toFixed(4)})`; TE.cam.style.transformOrigin=f<768?'960px 540px':'820px 520px';
  teBlack.style.opacity=accel(f,804,11,1.4).toFixed(3);
}

/* ---------- 20 · macro N&B de la salière ---------- */
const MA=scene('sMacro',816,879,f=>shotMacro(f));
const maBg=el(MA.cam,'full','', 'background:radial-gradient(80% 90% at 60% 40%,#E4E1DD,#8F8C89)');
const ma3=canvas(MA.cam,1440,810,'inset:0;width:1920px;height:1080px');
const maBlack=el(MA.s,'','', 'position:absolute;inset:0;background:#000;pointer-events:none');
cue(816,'riser',{v:.35,end:830}); cue(874,'whoosh',{v:.8,peak:878,dur:8});
function shotMacro(f){
  const zoom=f<864?lerp(3.1,3.3,(f-816)/48):f<874?lerp(3.3,1.9,approach(f,864,10)):1.9;
  const whip=accel(f,874,6,2); MA.cam.style.transform=`scale(${(1-0.45*whip).toFixed(4)}) rotate(${(-whip*8).toFixed(2)}deg)`;
  MA.cam.style.filter=`grayscale(1) contrast(1.35)${whip>0?` blur(${(whip*18).toFixed(1)}px)`:''}`;
  if(window.T3D) T3D.shaker(ma3,{t:T(f),spin:0.4+T(f)*0.25+whip*3,tilt:0.08,drop:1,zoom,lookY:0.95,camY:1.1,camX:0.9,sprinkle:0,shadow:0.4});
  maBlack.style.opacity=(1-approach(f,816,14)).toFixed(3);
  const cp=clamp((f-828)/33); cursor(lerp(420,1160,cp),lerp(900,640,cp)+Math.sin(f*0.2)*6,0,f>=826&&f<874);
}

/* ---------- 21 · chat IA + page produit, la salière tourne et change de bouchon ---------- */
const CH=scene('sChat',880,953,f=>shotChat(f));
const chRoot=el(CH.cam,'','', 'position:absolute;inset:0'); chRoot.innerHTML=tplChat();
const chShaker=q1(chRoot,'.pshaker'), chThermal=q1(chRoot,'.pthermal');
cue(880,'impact',{v:.55}); cue(918,'shimmer',{v:.45,end:928}); cue(922,'pop',{v:.45,n:79});
function shotChat(f){ push(CH.cam,f,880,0.0005);
  const swapped=f>=922; const zoom=f<927?1.0:lerp(1.0,1.18,approach(f,927,20));
  if(window.T3D) T3D.shaker(chShaker,{t:T(f),spin:0.3+(f-880)*0.045,drop:1,zoom,lookY:0.0,sprinkle:0,shadow:1,cap:swapped?0x151413:0xFF3D5E});
  const th=f<918?0:f<921?(f-918)/3:f<924?1:1-(f-924)/3; show(chThermal,th>0); if(th>0){ chThermal.style.opacity=th.toFixed(2); iriTo(chThermal,{t:T(f),seed:4.7,zoom:1.2,hot:.6,bands:.8,therm:1}); }
  q1(chRoot,'.srow:nth-child(4) b').textContent=swapped?'#151413':'#FF3D5E';
}

/* ---------- 22-24 · « Taste Complete », zoom, thermique, Taste Check, grille qui casse ---------- */
const DO=scene('sDone',954,1079,f=>shotDone(f));
const doFrame=el(DO.cam); const doD=framed(doFrame,`<div class="full" style="background:#EDE6DF"><canvas class="dbg" width="310" height="183" style="position:absolute;inset:0;width:100%;height:100%"></canvas><canvas class="d3" width="1240" height="730" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
  <div style="position:absolute;left:56px;top:48px;font-size:128px;color:#fff;letter-spacing:-0.05em;line-height:1;text-shadow:0 2px 30px rgba(80,30,40,.15)">Taste <span style="display:inline-block;width:70px;height:70px;vertical-align:8px">${MARK_SVG}</span> Complete</div>
  <div style="position:absolute;right:40px;bottom:40px;width:300px;height:150px;border-radius:18px;background:rgba(21,20,19,.82);color:#F3EFEA"><div class="m" style="position:absolute;left:20px;top:18px;font-size:12px;color:#8E877F">ORDER SUMMARY</div><div style="position:absolute;left:20px;top:44px;font-size:20px">1× taste, extra salt</div><div style="position:absolute;left:20px;right:20px;bottom:16px;height:44px;border-radius:22px;background:#FF3D5E;font-size:17px;line-height:44px;text-align:center">Track order</div></div></div>`,1362,918,1240,830);
const doFull=el(DO.cam,'','', 'position:absolute;inset:0;display:none;overflow:hidden');
const doFullIn=el(doFull,'','', 'position:absolute;left:0;top:0;width:1240px;height:830px;transform-origin:0 0;background:#EDE6DF'); doFullIn.innerHTML=q1(doD,'.full').outerHTML;
const doTh=canvas(DO.cam,960,540,'inset:0;width:1920px;height:1080px;display:none');
const doBtn=el(DO.cam,'abs','Start Taste Check','height:56px;line-height:56px;padding:0 30px;border-radius:14px;background:#151413;color:#F3EFEA;font-size:26px');
const doGrid=el(DO.cam,'','', 'position:absolute;inset:0'); const doLow=document.createElement('canvas'); doLow.width=16; doLow.height=9;
const doCells=[]; for(let j=0;j<9;j++) for(let i=0;i<16;i++){ const c=el(doGrid,'','', `position:absolute;left:${i*120}px;top:${j*120}px;width:120px;height:120px;display:none`); const r=rng(900+j*16+i); c._r1=1056+r()*14; c._r2=1066+r()*13; c._i=i; c._j=j; doCells.push(c); }
const doLines=[]; for(let i=1;i<16;i++) doLines.push(el(doGrid,'gline','', `left:${i*120-1}px;top:0;width:2px;height:1080px;transform-origin:50% 50%`)); for(let j=1;j<9;j++) doLines.push(el(doGrid,'gline','', `left:0;top:${j*120-1}px;width:1920px;height:2px;transform-origin:50% 50%`));
const doDots=[]; for(let j=1;j<9;j++) for(let i=1;i<16;i++) doDots.push(el(doGrid,'gdot','', `left:${i*120}px;top:${j*120}px`));
cue(954,'impact',{v:.55}); cue(990,'swish',{v:.4,peak:991,dur:5}); cue(999,'shimmer',{v:.5,end:1010}); cue(1005,'hush',{}); cue(1020,'pop',{v:.45,n:76}); cue(1049,'click',{v:.95}); cue(1053,'riser',{v:.5,end:1079});
function render3dDone(cvs,f){ if(window.T3D) T3D.shaker(cvs,{t:T(f),spin:T(f)*0.4+1,tilt:-0.35,drop:1,zoom:1.15,lookY:0.4,camX:-1.2,camY:2.4,sprinkle:1,shadow:.8}); }
function shotDone(f){
  const card=f<990; show(doFrame,card); show(doFull,f>=990&&f<1006);
  if(card){ place(doFrame,960,540,lerp(0.92,1.0,approach(f,954,35))); q1(doD,'.full').style.transform=`scale(${(1+0.0018*(f-954)).toFixed(4)})`; q1(doD,'.full').style.transformOrigin='55% 70%';
    iriTo(q1(doD,'.dbg'),{t:T(f),seed:1.9,zoom:1.0,hot:.25,bands:.4}); render3dDone(q1(doD,'.d3'),f); }
  if(f>=990&&f<1006){ const s=2.3+0.004*(f-990); doFullIn.style.transform=`translate(${(960-700*s).toFixed(1)}px,${(540-420*s).toFixed(1)}px) scale(${s.toFixed(3)})`;
    iriTo(q1(doFullIn,'.dbg'),{t:T(f),seed:1.9,zoom:1.0,hot:.25,bands:.4}); render3dDone(q1(doFullIn,'.d3'),f); }
  const th=f>=999; show(doTh,th); if(th){ iriTo(doTh,{t:T(f)*0.7,seed:7.4,zoom:1.15,hot:.6,bands:.8,therm:1}); const rr=approach(f,999,7)*2400;
    doTh.style.webkitMaskImage=doTh.style.maskImage=f<1006?`radial-gradient(circle at 960px 560px,#000 ${Math.max(0,rr-280).toFixed(0)}px,transparent ${rr.toFixed(0)}px)`:''; }
  const bOn=f>=1020&&f<1068; show(doBtn,bOn); if(bOn){ const bl=accel(f,1060,8,1.6); place(doBtn,960,556,1+bl*0.08); doBtn.style.filter=bl>0?`blur(${(bl*16).toFixed(1)}px)`:'';
    doBtn.style.color=f<1023?'#FF3D5E':'#F3EFEA'; doBtn.style.background=f>=1049?'#FF3D5E':'#151413'; doBtn.style.transform+=` scale(${f>=1049&&f<1052?0.95:1})`; }
  const cp=approach(f,1029,17); cursor(lerp(1260,990,cp),lerp(1010,574,cp),f>=1049&&f<1052?1:0,f>=1029&&f<1066);
  // la grille casse le thermique en blocs, puis les blocs redeviennent papier
  const gOn=f>=1053; show(doGrid,gOn); if(gOn){ const lp=approach(f,1053,7); doLines.forEach((l,i)=>{ l.style.transform=i<15?`scaleY(${lp.toFixed(3)})`:`scaleX(${lp.toFixed(3)})`; });
    doDots.forEach((d,i)=>{ d.style.transform=`scale(${back(f,1062+(i%7),5).toFixed(3)})`; });
    const g=doLow.getContext('2d'); g.imageSmoothingEnabled=true; g.drawImage(doTh,0,0,16,9); const px=g.getImageData(0,0,16,9).data;
    doCells.forEach(c=>{ const on=f>=c._r1; show(c,on); if(!on) return; const k=(c._j*16+c._i)*4; c.style.background=f>=c._r2?'#EEE9E4':`rgb(${px[k]},${px[k+1]},${px[k+2]})`; }); }
}

/* ---------- 25 · collage sur grille : stats marketing ---------- */
const GR=scene('sGrid',1080,1130,f=>shotGrid(f));
const grIn=el(GR.cam,'','', 'position:absolute;left:0;top:0;width:2200px;height:1080px');
const grIri=[[2,4,1,1,1080],[9,1,1,1,1081],[3,7,1,1,1082],[13,5,1,1,1083],[6,1,4,3,1083]].map(([i,j,w,h,st],k)=>{ const c=canvas(grIn,120,80,`left:${i*120}px;top:${j*120}px;width:${w*120}px;height:${h*120}px;display:none`); c._st=st; c._k=k; return c; });
const grMacro=canvas(grIn,600,480,'left:1080px;top:120px;width:600px;height:480px;display:none;filter:grayscale(1) contrast(1.4)');
const grChips=[[0,120,220,60,1086,''],[600,486,230,56,1089,''],[1720,860,260,56,1095,'<span style="color:#FF3D5E">●</span>&nbsp; arial: 0']].map(([x,y,w,h,st,t])=>{ const d=el(grIn,'m',t,`position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:17px;line-height:${h}px;padding-left:22px;display:none`); d._st=st; return d; });
const grStat=el(grIn,'gcard','', 'left:240px;top:120px;width:360px;height:240px;display:none');
el(grStat,'abs m','SIGNUPS SINCE TASTE','left:24px;top:22px;font-size:12px;letter-spacing:.1em;color:#8E877F'); const grNum=el(grStat,'abs','+15%','left:20px;top:52px;font-size:96px;letter-spacing:-0.05em;line-height:1');
const grSpark=el(grStat,'','<svg width="310" height="70" viewBox="0 0 310 70"><path d="M0 60 C40 58 60 50 90 46 S150 30 190 26 S260 10 310 4" fill="none" stroke="#FF3D5E" stroke-width="4" stroke-linecap="round"/></svg>','position:absolute;left:24px;top:156px');
const grLine=el(grIn,'gcard','', 'left:0;top:360px;width:240px;height:240px;background:#151413;display:none');
el(grLine,'','<svg width="240" height="240" viewBox="0 0 240 240"><path class="lp" d="M20 190 L60 150 L90 165 L130 110 L165 120 L200 60 L225 40" fill="none" stroke="#FF3D5E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="320" stroke-dashoffset="320"/></svg>','position:absolute;inset:0');
const grPrice=el(grIn,'abs','<span class="m" style="font-size:14px;color:#8E877F">from</span> $49 <span style="display:inline-block;width:36px;height:36px;border-radius:18px;background:#151413;vertical-align:-8px;margin-left:8px"></span>','left:380px;top:510px;font-size:30px;display:none');
const grRight=el(grIn,'abs','', 'left:1820px;top:150px;font-size:44px;letter-spacing:-0.03em;display:none'); el(grIn,'abs m','BOUNCE %','left:1822px;top:120px;font-size:12px;color:#8E877F');
const grThumb=el(grIn,'gcard','', 'left:360px;top:0;width:120px;height:120px;background:#C9C3BD;display:none');
const grLines=[]; for(let i=0;i<=18;i++) grLines.push(el(grIn,'gline','', `left:${i*120-1}px;top:0;width:2px;height:1080px`)); for(let j=1;j<9;j++) grLines.push(el(grIn,'gline','', `left:0;top:${j*120-1}px;width:2200px;height:2px`));
for(let j=1;j<9;j++) for(let i=0;i<=18;i++) el(grIn,'gdot','', `left:${i*120}px;top:${j*120}px`);
cue(1080,'drop2',{}); cue(1080,'impact',{v:.6}); [1086,1089,1095,1101].forEach(f=>cue(f,'tick',{v:.4})); for(let k=0;k<7;k++) cue(1095+k*3,'tick',{v:.18});
function shotGrid(f){ GR.cam.style.transform=`scale(${(1+0.0008*(f-1080)).toFixed(4)})`; grIn.style.transform=`translateX(${(-(f-1080)*1.6).toFixed(1)}px)`;
  grIri.forEach(c=>{ const on=f>=c._st&&(c._k<4||f<1089); show(c,on); if(on) iriTo(c,{t:T(f),seed:3+c._k,zoom:1.3,hot:.5,bands:.5}); });
  show(grMacro,f>=1089); if(f>=1089&&window.T3D) T3D.shaker(grMacro,{t:T(f),spin:0.6+T(f)*0.3,tilt:0.08,drop:1,zoom:3.0,lookY:0.95,camY:1.1,camX:0.9,shadow:.3});
  grChips.forEach(d=>{ show(d,f>=d._st); if(f>=d._st) d.style.transform=`translateX(${((1-approach(f,d._st,6))*-60).toFixed(1)}px)`; });
  show(grStat,f>=1095); grNum.textContent='+'+Math.round(lerp(15,45,clamp((f-1095)/21)))+'%'; show(grThumb,f>=1095);
  show(grLine,f>=1098); q1(grLine,'.lp').setAttribute('stroke-dashoffset',(320*(1-approach(f,1101,12))).toFixed(1));
  show(grPrice,f>=1101); show(grRight,f>=1098); grRight.textContent=lerp(5.9,2.8,clamp((f-1098)/18)).toFixed(1);
}

/* ---------- 26 · BrandReport → Apply taste ---------- */
const RE=scene('sReport',1131,1175,f=>shotReport(f));
const reBg=canvas(RE.cam,960,540,'inset:0;width:1920px;height:1080px'); el(RE.cam,'full','', 'background:rgba(246,241,236,.42)');
const reCard=el(RE.cam,'rcard'); reCard.innerHTML=`<div style="position:absolute;left:36px;top:30px;font-size:38px;letter-spacing:-0.02em">BrandReport <span class="m" style="font-size:16px;color:#8E877F;margin-left:10px">● public</span></div>
  <div style="position:absolute;left:36px;top:92px;font-size:24px;color:#8E877F;font-weight:400"><span style="color:#FF3D5E">⊘</span>&nbsp; 47 boring issues found</div>
  <div style="position:absolute;left:24px;right:24px;bottom:28px;height:100px;border-radius:16px;background:#F4F1ED"><span class="m" style="position:absolute;left:24px;top:40px;font-size:17px;color:#6d6760">arial · #2D6CDF · drop shadows · stock photos</span></div>`;
const reBtn=el(reCard,'abs','Apply taste','left:auto;right:44px;top:206px;height:62px;line-height:62px;padding:0 28px;border-radius:12px;background:#151413;color:#F3EFEA;font-size:24px');
cue(1131,'impact',{v:.5}); cue(1161,'click',{v:1}); cue(1163,'pop',{v:.5,n:84});
function shotReport(f){ push(RE.cam,f,1131,0.0008); iriTo(reBg,{t:T(f),seed:9.4,zoom:0.7,hot:.22,bands:.15});
  const p=approach(f,1131,4); place(reCard,960,545,lerp(0.97,1,p)); reCard.style.opacity=lerp(0.35,1,p).toFixed(3);
  const pr=f>=1161&&f<1164; reBtn.style.background=f>=1161?'#FF3D5E':'#151413'; reBtn.style.transform=`scale(${pr?0.94:1})`;
  const cp=approach(f,1146,12); cursor(lerp(1400,1290,cp),lerp(1040,785,cp),pr?1:0,f>=1146);
}

/* ---------- 27 · alertes rouges → cercles → convergence → la marque ---------- */
const AL=scene('sAlerts',1176,1250,f=>shotAlerts(f),'dark');
const alBg=canvas(AL.cam,960,540,'inset:0;width:1920px;height:1080px;opacity:.16');
const AL_TRI='<svg viewBox="0 0 42 42" width="42" height="42"><path d="M21 5 L38 36 H4 Z" fill="none" stroke="#E5484D" stroke-width="3" stroke-linejoin="round"/></svg>';
const AL_EXC='<svg viewBox="0 0 42 42" width="42" height="42"><circle cx="21" cy="21" r="16" fill="none" stroke="#E5484D" stroke-width="3"/><path d="M21 12 V23 M21 29 V30" stroke="#E5484D" stroke-width="3" stroke-linecap="round"/></svg>';
const AL_OK='<svg viewBox="0 0 42 42" width="42" height="42"><circle cx="21" cy="21" r="15" fill="none" stroke="#F3EFEA" stroke-width="3"/></svg>';
const alIcons=[]; for(let j=0;j<6;j++) for(let i=0;i<15;i++){ const x=204+i*108, y=366+j*108; el(AL.cam,'gdot','', `left:${x}px;top:${y}px;width:4px;height:4px;margin:-2px 0 0 -2px;background:#4A4643`);
  const dx=(x-960)/760, dy=(y-636)/330; if(dx*dx+dy*dy>1) continue; const r=rng(1200+j*15+i); if(r()<0.18) continue;
  const d=el(AL.cam,'alert'); d._x=x; d._y=y; d._a=1176+r()*9; d._b=1188+(i/14)*26+r()*6; d._kind=r()<.6?0:1; alIcons.push(d); }
const alMark=el(AL.cam,'abs','', 'width:96px;height:96px'); alMark.innerHTML=MARK_SVG;
const alFade=el(AL.s,'','', 'position:absolute;left:0;right:0;bottom:0;height:500px;background:linear-gradient(transparent,#BFD7E0);opacity:0');
cue(1176,'hush',{}); for(let k=0;k<5;k++) cue(1188+k*7,'tick',{v:.25}); cue(1224,'reverse',{v:.6,end:1233}); cue(1233,'boom',{v:.8});
function shotAlerts(f){ push(AL.cam,f,1176,0.0007); iriTo(alBg,{t:T(f),seed:5.9,zoom:0.8,hot:.4,bands:.3});
  const cv=approach(f,1224,8,0.18);
  alIcons.forEach(d=>{ const on=f>=d._a&&f<1232; show(d,on); if(!on) return; const ok=f>=d._b; d.innerHTML=ok?AL_OK:(d._kind?AL_EXC:AL_TRI);
    const x=lerp(d._x,960+(d._x-960)*0.12,cv), y=lerp(d._y,540+(d._y-636)*0.12,cv); d.style.left=x+'px'; d.style.top=y+'px';
    d.style.transform=`scale(${(back(f,d._a,5)*lerp(1,0.5,cv)).toFixed(3)})`; });
  show(alMark,f>=1231); if(f>=1231) place(alMark,960,540,back(f,1231,7,1.6));
  alFade.style.opacity=approach(f,1243,7).toFixed(3);
}

/* ---------- 28 · ciel, « Ship it » ---------- */
const SH=scene('sShip',1251,1307,f=>shotShip(f)); sky(SH.cam);
const shTeal=el(SH.cam,'full','', 'background:linear-gradient(180deg,#6FA6BC 0%,#B9D3DC 30%,rgba(238,233,228,0) 60%)');
const shBtn=el(SH.cam,'bbtn','Ship it');
cue(1251,'impact',{v:.5}); cue(1293,'click',{v:1}); cue(1296,'riser',{v:.55,end:1308});
function shotShip(f){ push(SH.cam,f,1251,0.0009); shTeal.style.opacity=(1-approach(f,1251,8)).toFixed(3);
  const pr=f>=1293&&f<1297; place(shBtn,960,540,pr?0.95:1); shBtn.style.background=f>=1293?'#3A3330':'#151413';
  const cp=approach(f,1272,10); cursor(lerp(1200,990,cp),lerp(1130,566,cp),pr?1:0,f>=1272);
}

/* ---------- 29-30 · montage : palette · pricing · dashboard · landing, puis thermique ---------- */
const MO=scene('sMont',1308,1379,f=>shotMont(f)); sky(MO.cam);
const moP=el(MO.cam); const moPD=framed(moP,tplPalette(),1368,912,1240,730,'#121110');
const moR=el(MO.cam); framed(moR,tplPricing(),1368,912,1240,730,'#F3EFEA');
const moDa=el(MO.cam); moDa.className='frame'; Object.assign(moDa.style,{width:'1368px',height:'912px'}); const moDs=el(moDa,'scr'); moDs.style.background='#F7F4F0';
const moDd=el(moDs,'','', 'position:absolute;left:0;top:0;width:1360px;height:800px;transform-origin:0 0'); const MOD=buildDash(moDd); moDd.style.transform=`translate(0px,${((892-800*1348/1360)/2).toFixed(1)}px) scale(${(1348/1360).toFixed(4)})`;
const moL=el(MO.cam); const moLD=framed(moL,tplLanding(),1368,912,1240,730,'#F3EFEA');
const moTint=canvas(moL,240,160,'inset:0;width:100%;height:100%;border-radius:18px;mix-blend-mode:hard-light;display:none');
const MOS=[[moP,1308],[moR,1326],[moDa,1338],[moL,1350]];
cue(1308,'impact',{v:.7}); cue(1326,'impact',{v:.6}); cue(1338,'impact',{v:.6}); cue(1350,'impact',{v:.7}); cue(1374,'shimmer',{v:.45,end:1380});
function shotMont(f){ let cur=MOS[0]; for(const m of MOS) if(f>=m[1]) cur=m;
  MOS.forEach(m=>show(m[0],m===cur)); place(cur[0],960,540,1+0.0016*(f-cur[1]));
  if(cur[0]===moP) iriTo(q1(moPD,'.kbg'),{t:T(f),seed:5.5,zoom:1.0,hot:.35,bands:.3});
  if(cur[0]===moDa){ updateDash(MOD,()=>1,f); iriTo(MOD.imgc,{t:T(f),seed:2.1,zoom:1.2,hot:.2,bands:.35}); }
  if(cur[0]===moL&&window.T3D) T3D.shaker(q1(moLD,'.lshaker'),{t:T(f),spin:T(f)*0.6+2.0,tilt:-0.62+0.14*Math.sin(T(f)*19),drop:1,zoom:0.92,lookY:0.15,sprinkle:1,shadow:0,camX:0.2});
  setTint(moTint,{t:T(f),seed:5.2,zoom:1.2,hot:.6,bands:.7,therm:1},approach(f,1373,4));
}

/* ---------- 31-32 · fragments → glyphes → marque → « vladan » → pill → e-mail ---------- */
const OU=scene('sOutro',1380,1559,f=>shotOutro(f));
const ouFr=FRAGS.map((t,i)=>{ const d=el(OU.cam,'abs frag'); d.textContent=t; const r=rng(700+i); let x,y; do{ x=60+r()*1660; y=110+r()*860; }while(Math.abs(x+120-960)<380&&Math.abs(y-540)<90); d._x=x; d._y=y; d.style.color=r()<.4?GACC:GINK; return d; });
const ouGl=gset(16,77,420,190).map(g=>{ const d=el(OU.cam,'abs c glyph'); d._g=g; d.textContent=g[0]; d.style.color=g[3]; return d; });
const ouDot=el(OU.cam,'abs','', 'border-radius:50%');
const ouMark=el(OU.cam,'abs','', 'width:78px;height:78px'); ouMark.innerHTML=MARK_SVG;
const ouWord=el(OU.cam,'abs','vladan','font-size:64px;font-weight:600;letter-spacing:-0.04em;line-height:1');
const ouPill=el(OU.cam,'abs','', 'height:86px;border:3.5px solid #151413;border-radius:43px');
const OUW=[[1449,'Give'],[1455,'it'],[1470,'<em style="font-size:58px;color:#FF3D5E">taste.</em>']];
const ouWords=OUW.map(([f,h])=>el(OU.cam,'abs',h,'font-size:48px;line-height:1'));
const ouMail=el(OU.cam,'abs','vladan<span style="color:#FF3D5E">@</span>kwinndo.fr','font-size:44px;letter-spacing:-0.02em;line-height:1');
const ouSub=el(OU.cam,'abs m','brand · UI · motion for SaaS','font-size:18px;color:#8E877F');
let OUL={};
function outroLayout(){ OUL.ws=ouWords.map(e=>e.offsetWidth); OUL.ww=ouWord.offsetWidth; OUL.mw=ouMail.offsetWidth; OUL.sw=ouSub.offsetWidth; }
cue(1380,'shimmer',{v:.35,end:1390}); cue(1386,'reverse',{v:.6,end:1395}); cue(1395,'boom',{v:1.15}); cue(1410,'shimmer',{v:.4,end:1418});
OUW.forEach(([f],i)=>cue(f,i==2?'pluck':'tick',{n:84,v:i==2?.55:.4})); cue(1446,'swish',{v:.3,peak:1447,dur:4}); cue(1485,'tick',{v:.35}); cue(1494,'final',{}); cue(1494,'swish',{v:.3,peak:1497,dur:8});
function shotOutro(f){ push(OU.cam,f,1380,0.0008);
  ouFr.forEach(d=>{ const on=f<1386; show(d,on); if(on) placeTL(d,d._x+(d._x<960?1:-1)*(f-1380)*6,d._y); });
  const cg=approach(f,1386,8,0.14); ouGl.forEach((d,i)=>{ const on=f>=1386&&f<1393; show(d,on); if(!on) return; const g=d._g; place(d,960+g[1]*(1-cg),540+g[2]*(1-cg),lerp(1,0.4,cg)); mblur(d,Math.abs(g[1])*0.06*(1-cg),Math.abs(g[2])*0.06*(1-cg)); });
  const dOn=f>=1392&&f<1398; show(ouDot,dOn); if(dOn){ const S=f<1395?60:70; Object.assign(ouDot.style,{width:S+'px',height:S+'px',background:f<1395?'radial-gradient(#FFC7A1,#FFA6C9)':'#FF3D5E',filter:f<1395?'blur(6px)':''}); place(ouDot,960,540); }
  const tot=78+22+OUL.ww; const slide=approach(f,1407,8); const logoOn=f>=1398&&f<1449;
  show(ouMark,logoOn); show(ouWord,logoOn&&f>=1410);
  if(logoOn){ const mx=lerp(960,960-tot/2+39,slide); const exit=clamp((f-1446)/3); place(ouMark,mx,540,back(f,1398,6)); placeTL(ouWord,mx+39+22-(1-approach(f,1410,8))*40,540-34);
    ouWord.style.clipPath=`inset(-20px ${((1-approach(f,1410,8))*100).toFixed(1)}% -20px ${(exit*100).toFixed(0)}%)`; ouMark.style.clipPath=`inset(0 0 0 ${(exit*100).toFixed(0)}%)`; }
  // pill tapée mot par mot, flash, la pill disparaît, l'e-mail arrive
  let k=-1; OUW.forEach(([wf],i)=>{ if(f>=wf) k=i; }); const sp=12, pad=30;
  let tw=0; for(let i=0;i<=k;i++){ const prev=i?OUL.ws.slice(0,i).reduce((a,b)=>a+b+sp,0)-sp:0; const cur=OUL.ws.slice(0,i+1).reduce((a,b)=>a+b+sp,0)-sp; tw=lerp(prev,cur,approach(f,OUW[i][0],6)); }
  const pOn=f>=1449&&f<1488; show(ouPill,pOn); if(pOn){ const pw=tw+2*pad; Object.assign(ouPill.style,{width:pw+'px',left:(960-pw/2)+'px',top:'497px',borderColor:(f<1455||(f>=1485&&f<1488))?'#FF3D5E':'#151413'}); }
  let cx=960-tw/2; ouWords.forEach((d,i)=>{ show(d,i<=k); if(i>k) return; placeTL(d,cx,540-26-(i==2?6:0)); cx+=OUL.ws[i]+sp; d.style.color=(f<1455&&i==0)?'#FF3D5E':''; });
  show(ouMail,f>=1494); if(f>=1494){ const p=approach(f,1494,9); placeTL(ouMail,960-OUL.mw/2,630+(1-p)*40); ouMail.style.clipPath=`inset(-10px -10px ${((1-p)*100).toFixed(0)}% -10px)`; mblur(ouMail,0,vel(t=>(1-approach(t,1494,9))*40,f)*BLUR); }
  show(ouSub,f>=1506); if(f>=1506){ const p=approach(f,1506,9); placeTL(ouSub,960-OUL.sw/2,704+(1-p)*20); ouSub.style.clipPath=`inset(-10px -10px ${((1-p)*100).toFixed(0)}% -10px)`; }
}
