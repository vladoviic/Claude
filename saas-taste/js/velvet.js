/* ============================================================
   velvetly : la boutique de mobilier « avec du goût » montrée dans tous les écrans
   (l'équivalent de trailride dans la réf). Les photos sont des rendus Cycles (img/).
   Même grammaire que la réf : UI sombre, photo plein cadre, titres blancs géants,
   petites données denses en mono, un seul accent.
   ============================================================ */
const VA='#FF3D5E', VINK='#121110', VG='#8E877F';
const IMG=n=>`img/${n}.jpg`;
// séquences Cycles animées (img/<dossier>/, une image par image du film)
const SEQ={land:seqLoad('land','l',66), aerial:seqLoad('aerial','a',39), macro:seqLoad('macro','m',64), done:seqLoad('done','d',57),
  doneMask:seqLoad('done','mask',57,'png',43), phone:seqLoad('phone','p',80)};
let AERIAL=[], TURNHOT={};
ASYNC.push(fetch('img/aerial/proj.json').then(r=>r.json()).then(j=>AERIAL=j).catch(()=>console.error('proj.json manquant')), fetch('img/turn/hot.json').then(r=>r.json()).then(j=>TURNHOT=j).catch(()=>console.error('hot.json manquant')));
const vimg=(n,css,pos='50% 50%')=>`<img class="vi" src="${IMG(n)}" style="${css};object-position:${pos}">`;
const VLOGO=(c='#F3EFEA',s=22)=>`<span style="font-family:'ID';font-weight:600;font-size:${s}px;letter-spacing:-0.035em;color:${c};white-space:nowrap"><span style="display:inline-block;width:${(s*0.62).toFixed(1)}px;height:${(s*0.62).toFixed(1)}px;border-radius:${(s*0.2).toFixed(1)}px;background:${VA};margin-right:${(s*0.32).toFixed(1)}px"></span>velvetly</span>`;
const CHAIR_SVG=(c='#151413',w=4)=>`<svg viewBox="0 0 88 88" width="100%" height="100%"><g fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"><path d="M26 22 Q26 16 32 16 H56 Q62 16 62 22 V42 H26 Z"/><path d="M20 46 Q20 42 26 42 H62 Q68 42 68 46 V54 Q68 58 62 58 H26 Q20 58 20 54 Z"/><path d="M28 58 L24 72 M60 58 L64 72"/></g></svg>`;
// pictogramme de la marque velvetly dans les titres géants (le ✿ de la réf)
const VMARK=(s)=>`<span class="vmk" style="display:inline-block;width:${s}px;height:${s}px;border-radius:${(s*0.26).toFixed(1)}px;background:${VA};vertical-align:${(s*0.02).toFixed(1)}px;position:relative"><span style="position:absolute;inset:14%;display:block;line-height:0;font-size:0">${CHAIR_SVG('#fff',4.5)}</span></span>`;

/* ---------- landing : salon plein cadre + « Sit with ▢ taste. » + tuiles ---------- */
const CATS=[['chair','Lounge Chairs','24 pieces'],['sofa','Sofas','18 pieces'],['pouf','Poufs','31 pieces'],['lamp','Lighting','42 pieces'],['plant','Living Things','12 pieces']];
// la landing de velvetly v2 : un SaaS de configurateur 3D pour marques de mobilier (pas une boutique)
const FEATS=[['sofa','Room planner','drag, drop, done'],['chair','3D hero','360° in the browser'],['lamp','AR preview','see it in their room'],['pouf','Fabric swap','212 fabrics'],['plant','Embed','1 line of JS']];
function tplVLanding(){ return `<div class="full" style="background:${VINK};overflow:hidden">
  ${vimg('room_eye','left:0;top:0;width:1240px;height:560px','50% 58%')}<canvas class="vseq" width="1240" height="560" style="position:absolute;left:0;top:0;width:1240px;height:560px"></canvas>
  <div class="full" style="height:560px;background:linear-gradient(180deg,rgba(18,17,16,.35) 0%,rgba(18,17,16,0) 22%,rgba(18,17,16,0) 55%,rgba(18,17,16,.92) 100%)"></div>
  <div class="vpill" style="left:22px;top:20px;background:rgba(18,17,16,.55)">${VLOGO('#F3EFEA',17)}<span style="margin-left:10px;color:#8E877F">▾ for brands</span></div>
  <div style="position:absolute;left:470px;top:20px;height:34px;line-height:34px;font-size:14px;color:#F3EFEA;display:flex;gap:26px"><span>Product</span><span>Customers</span><span>Pricing</span></div>
  <div class="vpill" style="right:150px;top:20px;background:#151413;color:#F3EFEA;box-shadow:inset 0 0 0 1px rgba(243,239,234,.25)">Book a demo</div>
  <div class="vpill" style="right:22px;top:20px;background:rgba(18,17,16,.55);color:#F3EFEA">Sign in</div>
  <div class="vhead lnh big" style="left:-18px;top:352px;font-size:185px">Plan with ${VMARK(136)} <em style="font-size:180px">taste.</em></div>
  <div class="m" style="position:absolute;left:24px;top:548px;font-size:12px;color:#F3EFEA">▪ Used by 140 furniture brands¹</div>
  <div class="m" style="position:absolute;left:330px;top:548px;font-size:11px;color:${VG}">Room planner · 3D hero · AR · one line of JS</div>
  ${FEATS.map(([k,t,n],i)=>`<div class="vtile" style="left:${12+i*244}px;top:572px;width:${i==3?250:236}px">${vimg('tile_'+k,'inset:0;width:100%;height:100%','50% 62%')}<div style="position:absolute;left:0;right:0;top:0;height:84px;background:linear-gradient(rgba(21,20,19,.74) 0,rgba(21,20,19,.72) 50px,rgba(21,20,19,0) 84px)"></div><div class="vtl">${t}</div><div class="m vtn">${n}</div></div>`).join('')}
  </div>`; }

/* ---------- Build your Room : panneau sombre + plan d'archi + tracé ---------- */
function tplVRoom(){ const chk=(t,on)=>`<div class="vchk"><span style="${on?'background:#F3EFEA;border-color:#F3EFEA;color:#151413':''}">${on?'✓':''}</span>${t}</div>`;
  const tick=(x,y)=>`<path d="M${x-5} ${y+5} L${x+5} ${y-5}" stroke="#3A3633" stroke-width="1.4"/>`;
  // plan d'architecte : murs pochés hachurés, porte et son débattement, fenêtre en trois traits, cotes à tirets 45°, nord, échelle
  return `<div class="full" style="background:#F2EDE6">
  <svg class="vplan" viewBox="0 0 940 730" width="940" height="730" style="position:absolute;left:300px;top:0">
    <defs><pattern id="vgrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0 H0 V40" fill="none" stroke="#E8E1D8" stroke-width="1"/></pattern>
      <pattern id="vhatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#F2EDE6"/><path d="M0 0 V7" stroke="#3A3633" stroke-width="1.6"/></pattern></defs>
    <rect width="940" height="730" fill="url(#vgrid)"/>
    <g fill="none" stroke-linecap="butt">
      <path class="pw" pathLength="1" d="M150 110 H800 V640 H560 M470 640 H150 V470 M150 300 V110" stroke="#3A3633" stroke-width="20"/>
      <path class="pw" pathLength="1" d="M150 110 H800 V640 H560 M470 640 H150 V470 M150 300 V110" stroke="url(#vhatch)" stroke-width="16"/>
      <path class="pw" pathLength="1" d="M142 300 V470 M150 300 V470 M158 300 V470" stroke="#3A3633" stroke-width="1.4"/>
      <path class="pw" pathLength="1" d="M560 640 V550" stroke="#3A3633" stroke-width="3"/>
      <path class="pw" pathLength="1" d="M470 640 A90 90 0 0 1 560 550" stroke="#8E877F" stroke-width="1.4" stroke-dasharray="5 5"/>
    </g>
    <g class="m" font-size="14" fill="#3A3633">
      <path d="M150 74 H800 M150 64 V84 M800 64 V84" stroke="#3A3633" stroke-width="1"/>${tick(150,74)}${tick(800,74)}<rect x="440" y="64" width="70" height="20" fill="#F2EDE6"/><text x="446" y="79">5.20 m</text>
      <path d="M840 110 V640 M830 110 H850 M830 640 H850" stroke="#3A3633" stroke-width="1"/>${tick(840,110)}${tick(840,640)}<rect x="830" y="350" width="20" height="70" fill="#F2EDE6"/><text x="0" y="0" transform="translate(846 420) rotate(-90)">4.60 m</text>
    </g>
    <g class="pf" fill="rgba(255,255,255,.6)" stroke="#3A3633" stroke-width="2">
      <path d="M296 196 C292 160 330 146 380 150 L600 150 C640 150 676 162 676 196 C676 226 650 236 620 232 C560 224 520 230 470 244 C420 258 360 262 330 252 C306 244 298 222 296 196 Z"/>
      <path d="M300 186 C330 170 380 166 420 168 L600 166 C630 166 660 174 670 190" fill="none" stroke-width="1.4"/>
      <path d="M440 168 C444 196 448 222 452 248 M560 166 C562 190 566 212 570 228" fill="none" stroke-width="1.4"/>
      <rect x="250" y="285" width="470" height="300" rx="6" fill="none" stroke-dasharray="10 8" stroke="#B3ABA4"/>
      <g><circle cx="455" cy="410" r="44"/>${Array.from({length:12},(_,i)=>{ const a=i/12*Math.PI*2; return `<path d="M${(455+10*Math.cos(a)).toFixed(1)} ${(410+10*Math.sin(a)).toFixed(1)} L${(455+44*Math.cos(a)).toFixed(1)} ${(410+44*Math.sin(a)).toFixed(1)}" stroke-width="1.2"/>`; }).join('')}<circle cx="455" cy="410" r="10"/></g>
      <g transform="rotate(-38 692 406)"><rect x="644" y="366" width="96" height="84" rx="18"/><path d="M646 386 C660 352 724 352 738 386" fill="none" stroke-width="5" stroke-linecap="round"/>${[[652,448],[732,448],[652,372],[732,372]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="3.5" fill="#3A3633"/>`).join('')}</g>
      <g><circle cx="232" cy="178" r="40"/>${[0,1,2,3,4].map(i=>{ const a=i/5*Math.PI*2-1; return `<path d="M232 178 Q${(232+30*Math.cos(a+.3)).toFixed(1)} ${(178+30*Math.sin(a+.3)).toFixed(1)} ${(232+38*Math.cos(a)).toFixed(1)} ${(178+38*Math.sin(a)).toFixed(1)}" fill="none" stroke-width="1.3"/>`; }).join('')}</g>
      <g><circle cx="214" cy="560" r="30" fill="none"/><path d="M196 560 H232 M214 542 V578" stroke-width="1.2"/></g>
    </g>
    <path class="vroute" pathLength="1" d="M515 600 C520 520 600 520 640 470 S700 420 690 404" fill="none" stroke="#151413" stroke-width="5" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>
    <g class="m" font-size="13" fill="#5C5650"><text x="300" y="138">kidney sofa · 2.19 m</text><text x="700" y="496">lounge chair · 0.83 m</text><text x="404" y="482">pouf · Ø 0.61 m</text><text x="128" y="400" transform="rotate(-90 128 400)">window · SW</text></g>
    <g transform="translate(880 120)" font-family="JB" font-size="12" fill="#3A3633"><circle r="16" fill="none" stroke="#3A3633" stroke-width="1.2"/><path d="M0 -12 L5 6 L0 2 L-5 6 Z" fill="#3A3633"/><text x="-4" y="-22">N</text></g>
    <g transform="translate(170 690)" font-family="JB" font-size="11" fill="#3A3633"><rect width="125" height="6" fill="#3A3633"/><rect x="125" width="125" height="6" fill="none" stroke="#3A3633" stroke-width="1"/><text y="22">0</text><text x="121" y="22">1</text><text x="244" y="22">2 m</text></g>
  </svg>
  <div class="vdot" style="left:990px;top:404px"></div>
  <div class="m" style="position:absolute;left:316px;top:20px;height:32px;line-height:32px;padding:0 12px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #E4DCD2;font-size:14px;color:#3A3633">Embed &lt;/&gt;</div>
  <div style="position:absolute;right:20px;bottom:18px;width:64px;height:30px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #E4DCD2" class="m"><span style="position:absolute;left:14px;top:5px;font-size:15px;color:#6d6760">–&nbsp;&nbsp;+</span></div>
  <div style="position:absolute;left:0;top:0;width:300px;height:730px;background:${VINK};color:#F3EFEA">
    <div style="position:absolute;left:0;top:0;width:44px;height:730px;border-right:1px solid rgba(255,255,255,.07)">${[0,1,2,3,4,5].map(i=>`<div style="position:absolute;left:13px;top:${22+i*40}px;width:18px;height:18px;border-radius:5px;${i==1?'background:#F3EFEA':'border:1.5px solid rgba(243,239,234,.3)'}"></div>`).join('')}</div>
    <div class="vside">
      <div class="m" style="font-size:11px;color:${VG}">velvetly ▾</div>
      <div style="font-size:18px;letter-spacing:-0.02em;margin-top:6px">Build your Room</div><div class="m" style="font-size:10px;color:${VG};margin-top:3px">Room 04 · draft</div>
      <div class="vlab" style="margin-top:22px">ROOM</div>
      ${[['Living room',1],['Bedroom',0],['Studio',0],['Home office',0],['Add a room',0]].map(([t,on])=>`<div class="vrow fi">${on?'<b style="background:#F3EFEA;border-color:#F3EFEA"></b>':'<b></b>'}${t}</div>`).join('')}
      <div class="vlab" style="margin-top:16px">SIZE<span style="float:right;color:#F3EFEA">24 m²</span></div>
      <div style="position:relative;height:4px;border-radius:2px;background:rgba(255,255,255,.12);margin-top:10px"><div style="position:absolute;left:0;top:0;width:62%;height:4px;border-radius:2px;background:#F3EFEA"></div><div style="position:absolute;left:60%;top:-5px;width:14px;height:14px;border-radius:7px;background:#fff"></div></div>
      <div class="vlab" style="margin-top:20px">STYLE</div>
      <div class="vgrid2 fi">${chk('Warm minimal',1)}${chk('Japandi',0)}${chk('70s revival',1)}${chk('Mid-century',0)}${chk('Velvet',1)}${chk('Bouclé',0)}</div>
      <div class="vlab" style="margin-top:16px">FIT CHECK</div>
      <div style="font-size:30px;letter-spacing:-0.03em;margin-top:4px">98<span style="font-size:16px;color:${VG}"> %</span></div>
    </div>
    <div class="vbtn" style="left:58px;right:16px;bottom:16px">Publish room<span></span></div>
  </div></div>`; }

/* ---------- Taste Sprint : le plan du fondateur (Ship lundi), cinq jours, le week-end est off ---------- */
const PLAN_X0=330, PLAN_COL=212;
// [libellé, livrable, colonne, durée, y, voix du fondateur]
const PLAN_CHIPS=[['Ship','v1 → prod',0,1,462,1],['Type system','Typography.ts',1,1,642,0],['Colour & tokens','OneAccent.tsx',2,1,372,0],['Motion pass','EaseOut.tsx',3,1,732,0],
  ['Taste Check','audit · 47 items',4,1,552,0],['Kickoff','brief.md',0,1,732,0],['Hand-off','Figma + code',4,1,822,0]];
function tplPlan(){ const days=[19,20,21,22,23,24,25], dn=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const sl=(t,i,on)=>`<div class="sitem" style="top:${i}px;${on?'color:#F3EFEA':''}"><span style="display:inline-block;width:14px;height:14px;border-radius:4px;border:1.5px solid ${on?'#F3EFEA':'rgba(243,239,234,.35)'};${on?'background:#F3EFEA;':''}margin-right:14px;vertical-align:-1px"></span>${t}</div>`;
  let h=`<div class="plan"><div class="side"><div style="position:absolute;left:30px;top:34px;font-size:26px;font-weight:600;letter-spacing:-0.04em;color:#F3EFEA"><span style="display:inline-block;width:24px;height:24px;border-radius:12px;background:#F3EFEA;vertical-align:-3px;margin-right:10px"></span>vladan</div>
    <div class="vlab" style="position:absolute;left:30px;top:120px">PILLARS</div>
    ${['Brand','UI','Motion'].map((t,i)=>sl(t,150+i*36,i==0)).join('')}
    <div class="vlab" style="position:absolute;left:30px;top:280px">SCREENS</div>
    ${['Landing','Planner','Dashboard','Mobile','Emails'].map((t,i)=>sl(t,310+i*36,0)).join('')}
    <div class="vlab" style="position:absolute;left:30px;top:520px">QUICK ACTIONS</div>
    ${['Add screen','Move','Ask Vladan'].map((t,i)=>`<div style="position:absolute;left:30px;top:${552+i*48}px;font-size:22px;color:rgba(243,239,234,.75)">${t}</div>`).join('')}
    <div style="position:absolute;left:30px;bottom:30px;font-size:17px;color:rgba(243,239,234,.6)">Vladan<div class="m" style="font-size:12px;color:rgba(243,239,234,.35)">art director</div></div></div>
    <div class="ptitle" style="position:absolute;left:${PLAN_X0}px;top:50px;font-size:48px;letter-spacing:-0.03em;color:#3A3633">Taste Sprint</div>
    <div class="m psub" style="position:absolute;left:${PLAN_X0+2}px;top:112px;font-size:15px;color:${VG}">velvetly.app · 5 days · # TASTE-041</div>
    <div class="m plx" style="position:absolute;left:${PLAN_X0+2}px;top:150px;font-size:13px;color:#151413">October 2026</div>
    <div class="m plx" style="position:absolute;left:${PLAN_X0+PLAN_COL+60}px;top:146px;height:28px;line-height:28px;padding:0 14px;border-radius:14px;background:${VINK};color:#fff;font-size:12px">Today</div>
    <div class="plx" style="position:absolute;left:1830px;top:50px;width:1px;height:1030px;background:#E4DDD5"></div>`;
  days.forEach((d,i)=>{ const x=PLAN_X0+i*PLAN_COL; h+=`<div class="day" style="left:${x}px;top:182px;${i>=5?'color:#B3ABA4':''}">${d}</div><div class="dname" style="left:${x+86}px;top:222px">${dn[i]}${i>=5?' <span style="font-size:22px;color:#B3ABA4">off</span>':''}</div><div class="col" style="left:${x-14}px"></div>`; });
  PLAN_CHIPS.forEach(([t,dl,c,span,y,fd],i)=>{ h+=`<div class="pchip${fd?' fd':''}" data-i="${i}" style="left:${PLAN_X0+c*PLAN_COL-6}px;top:${y}px;width:${span*PLAN_COL-20}px"><b>${t}</b><i>${dl}</i></div>`; });
  h+=`<div class="plx"><div class="m" style="position:absolute;left:1842px;top:56px;font-size:11px;color:${VG};white-space:normal;width:70px;line-height:1.5">SCREENS</div>
    ${['chair','sofa','pouf','lamp'].map((k,i)=>`<div style="position:absolute;left:1842px;top:${96+i*92}px;width:70px;height:80px;border-radius:10px;overflow:hidden">${vimg('tile_'+k,'inset:0;width:100%;height:100%','50% 60%')}</div>`).join('')}</div>`;
  return h+'</div>'; }

// « Thought for N years » : l'année de début de Vladan (page « Prises au stylo ») ; sinon « a while »
let VL_YEARS=null;
function tplVChat(){ return `<div class="full" style="background:#F3EFEA">
  <div class="chatp"><div style="position:absolute;left:32px;top:30px;display:flex;align-items:center;gap:12px">${VLOGO('#151413',22)}<span style="font-size:20px">Comments</span><span class="m" style="font-size:13px;color:${VG}">2 open · Lounge Chair</span></div>
    <div class="cthr" style="position:absolute;left:24px;right:24px;top:96px;height:132px;border-radius:16px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">
      <div style="position:absolute;left:18px;top:16px;display:flex;align-items:center;gap:10px"><span style="display:inline-block;width:34px;height:34px;border-radius:17px;background:#2D6CDF;color:#fff;font:700 15px/34px AR;text-align:center;vertical-align:middle">L</span><span style="font-size:17px">Léa</span><span class="m" style="font-size:12px;color:${VG}">2 min</span></div>
      <span class="m" style="position:absolute;right:16px;top:20px;width:26px;height:26px;border-radius:13px 13px 13px 3px;background:#2D6CDF;color:#fff;font-size:13px;line-height:26px;text-align:center">1</span>
      <div class="ar" style="position:absolute;left:18px;top:64px;font-size:25px;color:#151413">Add a 3D hero. Less blue, please.</div></div>
    <div class="m cthink" style="position:absolute;left:32px;top:242px;font-size:14px;color:#8E877F">pinned on the seat · hero</div>
    <div class="cres" style="position:absolute;left:24px;right:24px;top:270px;height:62px;border-radius:14px;background:#F8F5F1;box-shadow:0 0 0 1px #E6E1DB;display:flex;align-items:center;gap:10px;padding-left:16px;font-size:16px"><span style="display:inline-block;width:26px;height:26px;border-radius:13px;background:#FF3D5E;color:#fff;font:700 11px/26px AR;text-align:center;vertical-align:middle">v</span><b style="font-weight:500">vladan</b><span class="m" style="font-size:14px;color:#5C5650">✓ resolved · velvet, one accent</span></div>
    <div class="m" style="position:absolute;left:32px;top:352px;font-size:13px;color:${VG}"><span style="display:inline-block;width:24px;height:24px;border-radius:12px;background:#2D6CDF;color:#fff;font:700 10px/24px AR;text-align:center;vertical-align:middle">L</span>&nbsp; Léa · 1 min</div>
    <div class="m" style="position:absolute;left:32px;top:378px;font-size:13px;color:${VG}"> </div>
    <div style="position:absolute;left:24px;right:24px;top:398px;height:150px;border-radius:16px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">
      <div class="ar" style="position:absolute;left:20px;top:18px;font-size:18px">Remove these for good:</div><div class="m" style="position:absolute;left:20px;top:44px;font-size:12px;color:${VG}">velvetly.app · whole site</div>
      <div class="m crm" style="position:absolute;left:20px;top:70px;font-size:22px;color:#151413">– font-family: Arial;</div><div class="m crm" style="position:absolute;left:20px;top:102px;font-size:22px;color:#151413">– #2D6CDF</div>
      <div class="m chapp" style="position:absolute;left:20px;bottom:-56px;white-space:nowrap;height:38px;line-height:38px;padding:0 18px;border-radius:19px;background:var(--ink);color:#fff;font-size:14px">Resolve</div>
      <div class="m crej" style="position:absolute;left:130px;bottom:-56px;height:38px;line-height:36px;padding:0 18px;border-radius:19px;border:1px solid #D9D2CA;color:#6d6760;font-size:14px">Reply</div></div>
    <div class="m cfix" style="position:absolute;left:32px;top:666px;font-size:16px;color:#151413;visibility:hidden">✓ fabric · polyester → velvet</div>
    <div style="position:absolute;left:24px;right:24px;bottom:28px;height:84px;border-radius:20px;background:#fff;box-shadow:0 0 0 1px #E6E1DB"><span style="position:absolute;left:22px;top:28px;font-size:19px;color:#A39C94;font-weight:400">Reply…</span><span class="m" style="position:absolute;right:86px;top:28px;font-size:20px;color:#A39C94">@</span><span style="position:absolute;right:16px;top:16px;width:52px;height:52px;border-radius:26px;background:var(--ink)"></span></div></div>
  <div style="position:absolute;left:640px;top:34px">${VLOGO('#151413',22)}</div>
  <div style="position:absolute;left:640px;top:92px;font-size:46px;letter-spacing:-0.035em">Lounge Chair</div>
  <div class="m" style="position:absolute;left:643px;top:152px;font-size:15px;color:${VG}">Built for sitting well</div>
  <div style="position:absolute;left:630px;top:196px;width:918px;height:668px;border-radius:24px;overflow:hidden;background:#E6DED4"><canvas class="pturn" width="1100" height="800" style="position:absolute;inset:0;width:100%;height:100%"></canvas></div>
  <div style="position:absolute;left:630px;top:884px;display:flex;gap:12px">${['chair','sofa','pouf','lamp'].map((k,i)=>`<div class="${i==0?'cthumb':''}" style="width:112px;height:112px;border-radius:16px;overflow:hidden;${i==0?'box-shadow:0 0 0 2px #151413':''}">${vimg('tile_'+k,'position:relative;width:100%;height:100%','50% 62%')}</div>`).join('')}</div>
  <div class="spec"><div class="m" style="position:absolute;left:32px;top:36px;font-size:12px;color:#8E877F">HERO SPEC</div>
    <div style="position:absolute;left:32px;top:70px;width:84px;height:84px;border-radius:12px;overflow:hidden" class="cthumb">${vimg('tile_chair','inset:0;width:100%;height:100%','50% 62%')}</div>
    <div style="position:absolute;left:132px;top:78px;font-size:24px;letter-spacing:-0.02em">Lounge Chair</div><div class="m spcol" style="position:absolute;left:132px;top:114px;font-size:13px;color:#8E877F">hero · 3D</div>
    <div class="srow" style="top:190px;font-size:26px;height:80px;line-height:80px">fabric<b class="sfab">polyester</b></div>
    ${[['size','83 × 57 cm'],['motion','autorotate'],['arial','0']].map((r,i)=>`<div class="srow" style="top:${290+i*62}px">${r[0]}<b>${r[1]}</b></div>`).join('')}
    <div class="m" style="position:absolute;left:32px;top:520px;font-size:12px;color:#8E877F">SIGN-OFF</div><div style="position:absolute;left:32px;top:546px;font-size:22px;color:#F3EFEA">Léa · founder</div>
    <div class="capprove" style="position:absolute;left:32px;right:32px;bottom:36px;height:64px;border-radius:32px;background:#F3EFEA;color:#151413;font-size:21px;line-height:64px;text-align:center">Approve hero →</div></div></div>`; }

/* ---------- Order Complete (photo plein cadre, titre géant, résumé) ---------- */
function tplVDone(){ return `<div class="full" style="background:${VINK};overflow:hidden">${vimg('chair_hero','inset:0;width:100%;height:100%','50% 50%')}<canvas class="vseq" width="1240" height="830" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
  <div class="full" style="background:linear-gradient(180deg,rgba(18,17,16,.28),rgba(18,17,16,0) 35%)"></div>
  <div class="vpill" style="left:22px;top:20px;background:rgba(18,17,16,.55)">${VLOGO('#F3EFEA',17)}<span style="margin-left:10px;color:#8E877F">▾ for brands</span></div>
  <div class="vpill" style="right:150px;top:20px;background:#151413;color:#F3EFEA;box-shadow:inset 0 0 0 1px rgba(243,239,234,.25)">Book a demo</div><div class="vpill" style="right:22px;top:20px;background:rgba(18,17,16,.55);color:#F3EFEA">Pricing</div>
  <div class="vhead" style="left:20px;top:58px;font-size:168px">Hero ${VMARK(124)} Approved</div>
  <div style="position:absolute;right:28px;bottom:28px;width:360px;height:188px;border-radius:18px;background:rgba(18,17,16,.84);color:#F3EFEA"><div class="m" style="position:absolute;left:20px;top:18px;font-size:22px;color:#8E877F">SIGNED OFF</div>
    <div style="position:absolute;left:20px;top:52px;font-size:28px;letter-spacing:-0.02em">“finally.” — Léa, founder</div><div class="m" style="position:absolute;left:20px;top:94px;font-size:15px;color:#8E877F">Tue 20 Oct · 10:42 · ships Fri 23</div>
    <div style="position:absolute;left:20px;right:20px;bottom:16px;height:44px;border-radius:22px;background:#F3EFEA;color:#151413;font-size:17px;line-height:44px;text-align:center">View live ↗</div></div></div>`; }

/* ---------- montage après « Ship it » : le seul résultat du film, la table v1 re-composée, la marque sur un vrai objet ---------- */
function tplVInsights(){ const sp=[8,10,9,13,12,16,18,17,22,26,31,36,45]; const pts=sp.map((v,i)=>`${(40+i*74).toFixed(0)},${(250-v*4.4).toFixed(0)}`);
  return `<div class="full" style="background:${VINK};color:#F3EFEA;overflow:hidden">
  <div style="position:absolute;left:34px;top:26px">${VLOGO('#F3EFEA',20)}</div><div class="m" style="position:absolute;left:34px;top:70px;font-size:15px;color:${VG}">velvetly · Studio plan · 14/20 seats</div>
  <div class="m" style="position:absolute;left:34px;top:150px;font-size:22px;color:${VG}">demo requests</div>
  <div class="mst" style="position:absolute;left:24px;top:176px;font-size:200px;letter-spacing:-0.05em;line-height:1;font-variant-numeric:tabular-nums">+14%<sup style="font-size:60px;vertical-align:110px">¹</sup></div>
  <svg width="1000" height="270" viewBox="0 0 1000 270" style="position:absolute;left:200px;top:420px"><polyline points="${pts.join(' ')}" fill="none" stroke="#F3EFEA" stroke-width="3" stroke-linejoin="round"/><circle cx="${40+12*74}" cy="${250-45*4.4}" r="9" fill="#FF3D5E"/></svg>
  <div style="position:absolute;right:40px;top:150px;width:330px;display:grid;gap:26px">
    <div><div class="m" style="font-size:15px;color:${VG}">TIME TO FIRST ROOM</div><div class="mst2" style="font-size:64px;letter-spacing:-0.04em">0:52</div></div>
    <div><div class="m" style="font-size:15px;color:${VG}">ARIAL</div><div style="font-size:64px;letter-spacing:-0.04em">0</div></div></div>
  <div class="m" style="position:absolute;left:34px;bottom:26px;font-size:22px;color:#8E877F">¹ velvetly is fictional. The taste isn't.</div></div>`; }
