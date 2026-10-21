/* ============================================================
   Le dashboard « Saasly » : un seul composant, deux goûts.
   comp[c] ∈ [0,1] pour 8 composants : 0 typo, 1 fond, 2 sidebar, 3 salutation,
   4 KPI, 5 graphe, 6 bouton, 7 visuel.
   ============================================================ */
const HB=[120,150,100,170,140,190,130,200,160,215,175,230];
const HT=[84,104,98,128,150,138,168,192,184,222,246,274];
const KSPARK=[[.1,.18,.15,.3,.28,.42,.5,.47,.62,.7,.86,1],[.2,.15,.28,.25,.38,.34,.45,.52,.5,.63,.72,.8],[.05,.1,.12,.2,.26,.3,.42,.55,.6,.74,.9,1]];
function sw(c,i,x,y,h,a,b,extra=''){ return `<div class="sw" data-c="${c}" data-i="${i}" style="left:${x}px;top:${y}px;height:${h}px;${extra}"><span class="a" style="line-height:${h}px">${a}</span><span class="b" style="line-height:${h}px">${b}</span></div>`; }
function buildDash(root){
  // la même app velvetly, deux goûts : v1 (le fondateur : Arial, bleu, ombres noires) et v2 (après le stylo). Mêmes valeurs, même géométrie.
  const items=[['Dashboard','Overview'],['Rooms','Rooms'],['Embeds','Embeds'],['Settings','Settings']];
  const kpis=[['Rooms published','ROOMS','1,234','1,234','+18%'],['Embeds','EMBEDS','312','312','+9%'],['3D views','3D VIEWS','48.2k','48.2k','+31%']];
  let h=`<div class="d-win"></div><div class="d-clip">
    <div class="d-side"></div><div class="d-act"></div>`;
  h+=sw(2,0,36,34,56,`<span class="ar" style="font-weight:700;font-size:27px;color:#fff">velvetly</span>`,`<span style="display:inline-block;width:22px;height:22px;border-radius:6px;background:var(--accent);margin-right:10px;vertical-align:-2px"></span><span style="font-weight:600;font-size:31px;color:#F3EFEA;letter-spacing:-0.035em">velvetly</span>`);
  const FLAT=['<path d="M4 11 L12 4 L20 11 V20 H4 Z"/><path d="M10 20 V14 H14 V20"/>','<path d="M5 20 V12 M12 20 V6 M19 20 V9"/>','<circle cx="9" cy="8" r="3.2"/><path d="M3 20 C3 15 15 15 15 20"/><path d="M16 5.5 A3 3 0 0 1 16 11.5 M18 14.5 C20.5 15.5 21 17.5 21 20"/>','<circle cx="12" cy="12" r="3.2"/><path d="M12 3 V6 M12 18 V21 M3 12 H6 M18 12 H21 M5.6 5.6 L7.8 7.8 M16.2 16.2 L18.4 18.4 M5.6 18.4 L7.8 16.2 M16.2 7.8 L18.4 5.6"/>'];
  items.forEach((it,i)=>{ h+=`<svg class="ico-a" width="24" height="24" viewBox="0 0 24 24" style="position:absolute;left:38px;top:${138+i*52}px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transform-origin:50% 50%">${FLAT[i]}</svg><canvas class="ico-b" width="96" height="96" style="position:absolute;left:28px;top:${128+i*52}px;width:44px;height:44px;transform-origin:50% 50%"></canvas>`; });
  items.forEach((it,i)=>{ h+=sw(0,i,78,128+i*52,44,`<span class="ar" style="font-size:16px;color:#fff;${i==0?'font-weight:700':''}">${it[0]}</span>`,`<span style="font-size:19px;color:${i==0?'#F3EFEA':'rgba(243,239,234,.5)'}">${it[1]}</span>`); });
  h+=sw(3,0,300,40,74,`<span class="ar" style="font-weight:700;font-size:33px;color:#333">Welcome back, <span class="usr">User! 👋</span></span>`,`<span class="greet" style="font-size:52px;letter-spacing:-0.035em">Morning, <em style="font-size:50px">Léa.</em></span>`);
  h+=sw(3,1,302,112,30,`<span class="ar" style="font-size:16px;color:#777">Here is your dashboard overview.</span>`,`<span class="m" style="font-size:16px;color:#8E877F">velvetly · Studio plan · 14/20 seats</span>`);
  h+=`<div class="d-box" id="BTN" style="top:50px"><div class="sw" data-c="6" data-i="0" style="left:0;top:0;width:100%;height:100%"><span class="a ar" style="width:100%;text-align:center;font-weight:700;font-size:17px;color:#fff">Get Started</span><span class="b" style="width:100%;text-align:center;font-size:20px;color:#F3EFEA">New report →</span></div></div>`;
  kpis.forEach((k,i)=>{
    h+=`<div class="d-box kpi" style="left:${300+i*350}px;top:170px;width:320px;height:150px">`;
    h+=sw(0,4+i,24,16,26,`<span class="ar" style="font-size:15px;color:#888">${k[0]}</span>`,`<span class="m" style="font-size:13px;letter-spacing:.08em;color:#8E877F">${k[1]}</span>`);
    h+=sw(4,i,22,52,80,`<span class="ar" style="font-weight:700;font-size:31px;color:#333">${k[2]}</span>`,`<span style="font-size:62px;letter-spacing:-0.045em">${k[3]}</span>`);
    h+=`<div class="chip kchip" style="right:20px;top:18px;border:1.5px solid rgba(21,20,19,.25);line-height:25px;color:var(--ink)">${k[4]}</div>`;
    // v2 : une sparkline à l'encre, finie par un point (le KPI se lit comme une donnée, pas comme une carte)
    const sp=KSPARK[i].map((v,j)=>`${(j*120/(KSPARK[i].length-1)).toFixed(1)},${(26-v*24).toFixed(1)}`);
    h+=`<svg class="kspk" width="124" height="30" viewBox="-2 -2 124 30" style="position:absolute;left:176px;top:104px;overflow:visible;opacity:0"><polyline points="${sp.join(' ')}" fill="none" stroke="#151413" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${sp[sp.length-1].split(',')[0]}" cy="${sp[sp.length-1].split(',')[1]}" r="3" fill="#151413"/></svg></div>`;
  });
  h+=`<div class="d-box" id="CH" style="left:300px;top:350px;width:650px;height:410px">`;
  h+=sw(5,0,28,20,36,`<span class="ar" style="font-weight:700;font-size:18px;color:#333">Monthly 3D Views</span>`,`<span style="font-size:25px;letter-spacing:-0.02em">3D views <span class="m" style="font-size:15px;color:#8E877F;letter-spacing:0">· 12 mo</span></span>`);
  // la ligne « 0 » est la base des barres (372) : même ennuyeux, le graphique est juste
  [0,1,2,3,4].forEach(i=>{ h+=`<div class="grid" style="left:62px;top:${124+i*62}px;width:560px"></div><div class="glab gl" style="left:24px;top:${117+i*62}px">${['20k','15k','10k','5k','0'][i]}</div>`; });   // une ligne 20k : la barre de décembre (≈19k) reste sous l'échelle
  h+=`<div id="BARS" style="position:absolute;left:0;top:0;width:650px;height:372px">`;
  for(let i=0;i<12;i++) h+=`<div class="d-bar"></div>`;
  h+=`</div><div class="chip" id="TIP" style="background:var(--ink);color:#F3EFEA">48.2k</div>`;
  'JFMAMJJASOND'.split('').forEach((m,i)=>{ h+=sw(0,8+i,0,380,18,`<span class="ar" style="font-size:12px;color:#9AA0A8">${m}</span>`,`<span class="m" style="font-size:12px;color:#8E877F">${m}</span>`,'').replace('class="sw"',`class="sw mlab" data-k="${i}"`); });
  h+=`</div>`;
  h+=`<div class="d-box" id="IMG" style="left:980px;top:350px;width:340px;height:410px;overflow:hidden">
      <img class="IMGC" src="img/chair_hero.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%">
      <div class="PH1" style="position:absolute;inset:0;background:#D9DCE1"><svg class="ph-ico" width="120" height="96" viewBox="0 0 120 96" style="left:110px;top:120px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="4"/><circle cx="84" cy="30" r="10" fill="#A9AEB6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg>
      <div class="ar" style="position:absolute;left:0;right:0;top:250px;text-align:center;font-size:14px;color:#8A8F97">stock_handshake_final_v3.jpg</div></div>
      <canvas class="IMG3" width="400" height="482" style="position:absolute;left:0;top:0;width:340px;height:410px"></canvas>
      <div class="IMGT" style="position:absolute;left:28px;bottom:26px;font-size:38px;line-height:1.02;letter-spacing:-0.03em;color:#F3EFEA">Room 04<br><em style="font-size:40px">is live.</em></div>
    </div>`;
  h+=`</div>`;
  root.innerHTML=h;
  const q=s=>root.querySelector(s), qa=s=>[...root.querySelectorAll(s)];
  return {root,win:q('.d-win'),side:q('.d-side'),act:q('.d-act'),icoA:qa('.ico-a'),icoB:qa('.ico-b'),img3:q('.IMG3'),sws:qa('.sw'),btn:q('#BTN'),kpis:qa('.kpi'),kchips:qa('.kchip'),kspk:qa('.kspk'),
    ch:q('#CH'),grids:qa('.grid'),glabs:qa('.gl'),bars:qa('.d-bar'),tip:q('#TIP'),img:q('#IMG'),imgc:q('.IMGC'),ph1:q('.PH1'),imgt:q('.IMGT'),mlabs:qa('.mlab'),usr:q('.usr'),greet:q('.greet')};
}
const SH_B=[0,8,18,0,0,0,0,0.28], SH_T=[0,50,90,-40,60,30,20,0.30];
function shadow(t){ const s=mixa(SH_B,SH_T,t); return `${s[0]}px ${s[1].toFixed(1)}px ${s[2].toFixed(1)}px ${s[3].toFixed(1)}px rgba(${s[4]|0},${s[5]|0},${s[6]|0},${s[7].toFixed(3)})`; }
// comp(c,i) -> progression du composant c pour l'élément d'indice i
// le morph : bleu → lilac → encre (le bleu ne se mélange jamais directement à l'encre)
function morphMix(a,b,p){ return p<0.5?mixc(a,MORPH.fill,p*2):mixc(MORPH.fill,b,(p-0.5)*2); }
function updateDash(D,comp,f){
  const c=k=>comp(k,0);
  // swaps
  for(const el of D.sws){ const k=+el.dataset.c, i=+el.dataset.i; const p=comp(k,i);
    const a=el.children[0], b=el.children[1];
    a.style.transform=`translateY(${(-p*100).toFixed(2)}%)`; b.style.transform=`translateY(${((1-p)*100).toFixed(2)}%)`;
  }
  // fond / fenêtre
  const c1=c(1);
  D.win.style.background=mixc('#F4F5F7','#F7F4F0',c1);
  const rad=lerp(6,20,c1);   // 20 px (30 faisait bulle) D.win.style.borderRadius=D.root.querySelector('.d-clip').style.borderRadius=rad+'px';
  D.win.style.boxShadow=shadow(c1)+`, 0 0 0 ${lerp(1,0,c1).toFixed(2)}px #C9CDD3`;
  // sidebar
  const c2=c(2);
  D.side.style.background=morphMix('#2D6CDF','#151413',c2);
  D.act.style.background=rgba(mixa([255,255,255,.18],[243,239,234,.07],c2)); D.act.style.borderRadius=lerp(4,14,c2)+'px';
  const KINDS=['overview','reports','customers','settings'];
  D.icoA.forEach((el,i)=>{ const p=comp(2,i); el.style.transform=`scale(${(1-p).toFixed(3)})`; el.style.display=p>=1?'none':'block'; });
  D.icoB.forEach((el,i)=>{ const p=comp(2,i); const pop=p<=0?0:back(p*10,0,10,1.7); el.style.display=pop>0.001?'block':'none'; });
  // bouton
  const c6=c(6); const bw=lerp(170,214,c6), bh=lerp(46,58,c6);
  Object.assign(D.btn.style,{left:(1320-bw)+'px',width:bw+'px',height:bh+'px',top:lerp(52,48,c6)+'px',borderRadius:lerp(4,29,c6)+'px',background:morphMix('#2D6CDF','#151413',c6),
    boxShadow:`0 ${lerp(6,0,c6)}px ${lerp(10,0,c6)}px rgba(0,0,0,${lerp(.45,0,c6).toFixed(3)}), inset 0 ${lerp(-3,0,c6)}px 0 rgba(0,0,0,${lerp(.25,0,c6).toFixed(3)})`});
  for(const sp of D.btn.querySelectorAll('.sw>span')) sp.style.lineHeight=bh+'px';
  // KPI
  // v2 : grille ouverte (le fond de la fenêtre, un filet d'encre en haut), plus de carte
  D.kpis.forEach((k,i)=>{ const p=comp(4,i);
    Object.assign(k.style,{background:mixc('#FFFFFF','#F7F4F0',p),borderRadius:lerp(4,0,p)+'px',boxShadow:`0 2px 4px rgba(0,0,0,${lerp(.12,0,p).toFixed(3)}), 0 0 0 ${lerp(1,0,p).toFixed(2)}px #D5D8DE, inset 0 ${p.toFixed(2)}px 0 rgba(21,20,19,${(.14*p).toFixed(3)})`});
    D.kchips[i].style.transform=`scale(${back(p*12,2,10).toFixed(3)})`; D.kspk[i].style.opacity=clamp(p*1.4-0.4).toFixed(3); });
  // graphe
  const c5=c(5);
  Object.assign(D.ch.style,{background:mixc('#FFFFFF','#F7F4F0',c5),borderRadius:lerp(4,0,c5)+'px',boxShadow:`0 2px 4px rgba(0,0,0,${lerp(.12,0,c5).toFixed(3)}), 0 0 0 ${lerp(1,0,c5).toFixed(2)}px #D5D8DE, inset 0 ${c5.toFixed(2)}px 0 rgba(21,20,19,${(.14*c5).toFixed(3)})`});
  D.grids.forEach((g,i)=>{ const p=comp(5,i); g.style.transform=`scaleX(${(1-p).toFixed(3)})`; });
  D.glabs.forEach((g,i)=>{ const p=comp(5,i); g.style.transform=`translateX(${(-p*60).toFixed(1)}px)`; g.style.clipPath=`inset(0 ${(p*100).toFixed(1)}% 0 0)`; });
  let maxX=0,maxH=0;
  D.bars.forEach((b,i)=>{ const p=comp(5,i+1); const w=lerp(30,36,p), gap=lerp(16.5,12,p);
    const x=lerp(66,58,p)+i*(w+gap); const hh=lerp(HB[i],HT[i],p);
    const col=morphMix('#2D6CDF','#151413',p);
    Object.assign(b.style,{left:x+'px',width:w+'px',height:hh+'px',background:col,borderRadius:`${lerp(2,6,p)}px ${lerp(2,6,p)}px 0 0`});
    if(i==11){maxX=x+w/2;maxH=hh;}
    D.mlabs[i].style.left=(x+w/2-4)+'px';
  });
  const tp=comp(5,14); D.tip.style.left=(maxX-52)+'px'; D.tip.style.top=(372-maxH-44)+'px'; D.tip.style.transform=`scale(${back(tp*12,0,10).toFixed(3)})`; D.tip.style.transformOrigin='50% 100%';
  // visuel
  const c7=c(7);
  Object.assign(D.img.style,{background:mixc('#D9DCE1','#ECE6DF',c7),borderRadius:lerp(4,20,c7)+'px',boxShadow:`0 0 0 ${lerp(1,0,c7).toFixed(2)}px #C4C8CF`});
  show(D.img3,false);
  const tt=comp(7,1); D.imgt.style.transform=`translateY(${((1-tt)*40).toFixed(1)}px)`; D.imgt.style.clipPath=`inset(-20px -20px ${((1-tt)*100).toFixed(1)}% -20px)`;
}

