/* ============================================================
   velvetly : la boutique de mobilier « avec du goût » montrée dans tous les écrans
   (l'équivalent de trailride dans la réf). Les photos sont des rendus Cycles (img/).
   Même grammaire que la réf : UI sombre, photo plein cadre, titres blancs géants,
   petites données denses en mono, un seul accent.
   ============================================================ */
const VA='#FF3D5E', VINK='#121110', VG='#8E877F';
const IMG=n=>`img/${n}.jpg`;
// tracé du plan reporté sur la vue plongeante (coordonnées dans room_top recadrée 2080×1170)
const HERO_ROUTE='M1000 980 C1010 860 1160 820 1240 760 S1360 690 1350 660', HERO_DOT=[1350,660];
const vimg=(n,css,pos='50% 50%')=>`<img class="vi" src="${IMG(n)}" style="${css};object-position:${pos}">`;
const VLOGO=(c='#F3EFEA',s=22)=>`<span style="font-family:'ID';font-weight:600;font-size:${s}px;letter-spacing:-0.035em;color:${c};white-space:nowrap"><span style="display:inline-block;width:${(s*0.62).toFixed(1)}px;height:${(s*0.62).toFixed(1)}px;border-radius:${(s*0.2).toFixed(1)}px;background:${VA};margin-right:${(s*0.32).toFixed(1)}px"></span>velvetly</span>`;
const CHAIR_SVG=(c='#151413',w=4)=>`<svg viewBox="0 0 88 88" width="100%" height="100%"><g fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"><path d="M26 22 Q26 16 32 16 H56 Q62 16 62 22 V42 H26 Z"/><path d="M20 46 Q20 42 26 42 H62 Q68 42 68 46 V54 Q68 58 62 58 H26 Q20 58 20 54 Z"/><path d="M28 58 L24 72 M60 58 L64 72"/></g></svg>`;
// pictogramme de la marque velvetly dans les titres géants (le ✿ de la réf)
const VMARK=(s)=>`<span style="display:inline-block;width:${s}px;height:${s}px;border-radius:${(s*0.26).toFixed(1)}px;background:${VA};vertical-align:${(s*0.02).toFixed(1)}px;position:relative"><span style="position:absolute;inset:14%;display:block;line-height:0;font-size:0">${CHAIR_SVG('#fff',4.5)}</span></span>`;

/* ---------- landing : salon plein cadre + « Sit with ▢ taste. » + tuiles ---------- */
const CATS=[['chair','Lounge Chairs','24 pieces'],['sofa','Sofas','18 pieces'],['pouf','Poufs','31 pieces'],['lamp','Lighting','42 pieces'],['plant','Living Things','12 pieces']];
function tplVLanding(){ return `<div class="full" style="background:${VINK};overflow:hidden">
  ${vimg('room_eye','left:0;top:0;width:1240px;height:560px','50% 58%')}
  <div class="full" style="height:560px;background:linear-gradient(180deg,rgba(18,17,16,.35) 0%,rgba(18,17,16,0) 22%,rgba(18,17,16,0) 55%,rgba(18,17,16,.92) 100%)"></div>
  <div class="vpill" style="left:22px;top:20px;background:rgba(18,17,16,.55)">${VLOGO('#F3EFEA',17)}<span style="margin-left:16px;color:#8E877F">≡</span></div>
  <div class="vpill" style="right:150px;top:20px;background:${VA};color:#fff">New in</div>
  <div class="vpill" style="right:22px;top:20px;background:rgba(18,17,16,.55);color:#F3EFEA">Search pieces</div>
  <div class="vhead lnh" style="left:-18px;top:338px;font-size:204px">Sit with ${VMARK(150)} <em style="font-size:226px">taste.</em></div>
  <div class="m" style="position:absolute;left:24px;top:548px;font-size:12px;color:#F3EFEA">▪ Best sellers</div>
  <div class="m" style="position:absolute;left:330px;top:548px;font-size:11px;color:${VG}">Pieces under €900, delivered in 3 days</div>
  ${CATS.map(([k,t,n],i)=>`<div class="vtile" style="left:${12+i*244}px;top:572px;width:${i==3?250:236}px">${vimg('tile_'+k,'inset:0;width:100%;height:100%','50% 62%')}<div class="vtl">${t}</div><div class="m vtn">${n}</div></div>`).join('')}
  </div>`; }

/* ---------- Build your Room : panneau sombre + plan d'archi + tracé ---------- */
function tplVRoom(){ const chk=(t,on)=>`<div class="vchk"><span style="${on?`background:${VA};border-color:${VA}`:''}">${on?'✓':''}</span>${t}</div>`;
  return `<div class="full" style="background:#F2EDE6">
  <svg class="vplan" viewBox="0 0 940 730" width="940" height="730" style="position:absolute;left:300px;top:0">
    <defs><pattern id="vgrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0 H0 V40" fill="none" stroke="#E4DCD2" stroke-width="1"/></pattern></defs>
    <rect width="940" height="730" fill="url(#vgrid)"/>
    <g fill="none" stroke="#3A3633" stroke-linecap="square">
      <path class="pw" pathLength="1" d="M150 110 H800 V640 H560 M470 640 H150 V470 M150 300 V110" stroke-width="10"/>
      <path class="pw" pathLength="1" d="M150 300 V470" stroke-width="3" stroke="#8E877F"/><path class="pw" pathLength="1" d="M143 300 V470 M157 300 V470" stroke-width="1.5" stroke="#8E877F"/>
      <path class="pw" pathLength="1" d="M560 640 A90 90 0 0 0 470 550" stroke-width="2" stroke="#8E877F" stroke-dasharray="6 6"/>
    </g>
    <g class="pf" fill="rgba(255,255,255,.55)" stroke="#3A3633" stroke-width="2.5">
      <path d="M300 170 Q300 150 330 150 H640 Q672 150 672 180 V215 Q672 235 640 232 Q560 226 470 240 Q380 256 330 250 Q300 246 300 222 Z"/>
      <rect x="250" y="285" width="470" height="300" rx="10" fill="none" stroke-dasharray="10 8" stroke="#B3ABA4"/>
      <circle cx="455" cy="410" r="44"/><circle cx="455" cy="410" r="12" fill="none"/>
      <g transform="rotate(-38 692 406)"><rect x="640" y="360" width="104" height="92" rx="22" fill="rgba(255,61,94,.16)" stroke="${VA}"/></g>
      <circle cx="232" cy="178" r="40"/><circle cx="232" cy="178" r="20" fill="none" stroke-dasharray="4 5"/>
      <circle cx="210" cy="250" r="34" fill="none"/>
    </g>
    <path class="vroute" pathLength="1" d="M515 600 C520 520 600 520 640 470 S700 420 690 404" fill="none" stroke="${VA}" stroke-width="6" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>
    <g class="m" font-size="13" fill="#8E877F"><text x="440" y="96">5.20 m</text><text x="812" y="380">4.60 m</text><text x="164" y="392" transform="rotate(-90 164 392)">window · SW</text><text x="270" y="140">sofa 2.19</text><text x="700" y="490">lounge chair</text></g>
  </svg>
  <div class="vdot" style="left:990px;top:404px"></div>
  <div style="position:absolute;right:20px;bottom:18px;width:64px;height:30px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #E4DCD2" class="m"><span style="position:absolute;left:14px;top:5px;font-size:15px;color:#6d6760">–&nbsp;&nbsp;+</span></div>
  <div style="position:absolute;left:0;top:0;width:300px;height:730px;background:${VINK};color:#F3EFEA">
    <div style="position:absolute;left:0;top:0;width:44px;height:730px;border-right:1px solid rgba(255,255,255,.07)">${[0,1,2,3,4,5].map(i=>`<div style="position:absolute;left:13px;top:${22+i*40}px;width:18px;height:18px;border-radius:5px;${i==1?`background:${VA}`:'border:1.5px solid rgba(243,239,234,.3)'}"></div>`).join('')}</div>
    <div class="vside">
      <div style="font-size:18px;letter-spacing:-0.02em">Build your Room</div><div class="m" style="font-size:10px;color:${VG};margin-top:3px">Customise your space</div>
      <div class="vlab" style="margin-top:22px">ROOM</div>
      ${[['Living room',1],['Bedroom',0],['Studio',0],['Home office',0],['Add a room',0]].map(([t,on])=>`<div class="vrow fi">${on?`<b style="background:${VA}"></b>`:'<b></b>'}${t}</div>`).join('')}
      <div class="vlab" style="margin-top:16px">SIZE<span style="float:right;color:#F3EFEA">24 m²</span></div>
      <div style="position:relative;height:4px;border-radius:2px;background:rgba(255,255,255,.12);margin-top:10px"><div style="position:absolute;left:0;top:0;width:62%;height:4px;border-radius:2px;background:${VA}"></div><div style="position:absolute;left:60%;top:-5px;width:14px;height:14px;border-radius:7px;background:#fff"></div></div>
      <div class="vlab" style="margin-top:20px">STYLE</div>
      <div class="vgrid2 fi">${chk('Warm minimal',1)}${chk('Japandi',0)}${chk('70s revival',1)}${chk('Mid-century',0)}${chk('Velvet',1)}${chk('Bouclé',0)}</div>
      <div class="vlab" style="margin-top:16px">LIGHT</div>
      <div class="vgrid2 fi">${chk('South-west',1)}${chk('North',0)}</div>
    </div>
    <div class="vbtn" style="left:58px;right:16px;bottom:16px">Build Room<span></span></div>
  </div></div>`; }

/* ---------- Delivery & Install Status (plein cadre, mêmes classes que l'ancien planning) ---------- */
const PLAN_X0=330, PLAN_COL=212;
const PLAN_CHIPS=[
  ['Emma Laurent','Marais','#FF3D5E','#fff',0,2,372],['Hugo Martin','Lyon','#FFD9B8',null,1,3,462],['Inès Moreau','Bordeaux','#D8CCF4',null,3,2,552],
  ['Noah Petit','Saint-Germain','#BFE6F2',null,2,2,642],['Léa Bernard','Marais','#E9DFA8',null,4,2,372],['Jules Roux','Lyon','#F6C9D3',null,5,2,462],
  ['Chloé Fournier','Nantes','#FF3D5E','#fff',6,1,552],['Sacha Girard','Lille','#151413','#F3EFEA',6,1,732],['Manon Dubois','Marais','#CFE3C9',null,0,2,822],['Louis Faure','Bordeaux','#BFE6F2',null,4,2,822]];
function tplPlan(){ const days=[19,20,21,22,23,24,25], dn=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  const sl=(t,i,n,on)=>`<div class="sitem" style="top:${i}px;${on?'color:#F3EFEA':''}"><span style="display:inline-block;width:14px;height:14px;border-radius:4px;border:1.5px solid ${on?VA:'rgba(243,239,234,.35)'};${on?`background:${VA};`:''}margin-right:14px;vertical-align:-1px"></span>${t}${n?`<span class="m" style="position:absolute;right:-150px;font-size:12px;color:rgba(243,239,234,.35)">${n}</span>`:''}</div>`;
  let h=`<div class="plan"><div class="side"><div style="position:absolute;left:30px;top:34px">${VLOGO('#F3EFEA',24)}</div>
    <div class="m" style="position:absolute;left:30px;right:24px;top:90px;height:36px;border-radius:9px;background:rgba(255,255,255,.07);font-size:13px;line-height:36px;padding-left:14px;color:rgba(243,239,234,.4)">Search…</div>
    <div class="vlab" style="position:absolute;left:30px;top:150px">SHOWROOMS</div>
    ${['Marais','Saint-Germain','Lyon Confluence','Bordeaux','Nantes'].map((t,i)=>sl(t,180+i*36,0,i==0)).join('')}
    <div class="vlab" style="position:absolute;left:30px;top:378px">PRODUCTS</div>
    ${[['Lounge chairs','12'],['Sofas','8'],['Poufs','14'],['Lighting','9'],['Living things','6']].map(([t,n],i)=>sl(t,408+i*36,n,0)).join('')}
    <div class="vlab" style="position:absolute;left:30px;top:606px">PAGES</div>
    ${['Performance','Team','Customers'].map((t,i)=>sl(t,636+i*36,0,0)).join('')}
    <div style="position:absolute;left:30px;bottom:30px;font-size:15px;color:rgba(243,239,234,.55)">Sofia Lambert<div class="m" style="font-size:11px;color:rgba(243,239,234,.3)">ops · velvetly</div></div></div>
    <div class="ptitle" style="position:absolute;left:${PLAN_X0}px;top:50px;font-size:48px;letter-spacing:-0.03em;color:#3A3633">Delivery &amp; Install Status</div>
    <div class="m psub" style="position:absolute;left:${PLAN_X0+2}px;top:112px;font-size:15px;color:${VG}">Track and plan home deliveries</div>
    <div class="m plx" style="position:absolute;left:${PLAN_X0+2}px;top:150px;font-size:13px;color:${VA}">October 2026</div>
    <div class="m plx" style="position:absolute;left:1520px;top:146px;height:28px;line-height:28px;padding:0 14px;border-radius:14px;background:${VINK};color:#fff;font-size:12px">Today</div>
    <div class="plx" style="position:absolute;left:1830px;top:50px;width:1px;height:1030px;background:#E4DDD5"></div>`;
  days.forEach((d,i)=>{ const x=PLAN_X0+i*PLAN_COL; h+=`<div class="day" style="left:${x}px;top:182px;${i>=5?'color:#C9A7F0':''}">${d}</div><div class="dname" style="left:${x+86}px;top:222px">${dn[i]}</div><div class="col" style="left:${x-14}px"></div>`; });
  PLAN_CHIPS.forEach(([t,pl,bg,fg,c,span,y],i)=>{ h+=`<div class="pchip" data-i="${i}" style="left:${PLAN_X0+c*PLAN_COL-6}px;top:${y}px;width:${span*PLAN_COL-20}px;background:${bg};color:${fg||'#151413'}"><b>› ${t}<span style="font-weight:400;opacity:.7;margin-left:14px">${pl}</span></b><i>${dn[c]} ${days[c]} – ${dn[Math.min(6,c+span-1)]} ${days[Math.min(6,c+span-1)]}&nbsp;&nbsp;# VL-${2041+i*37}</i></div>`; });
  h+=`<div class="plx"><div class="m" style="position:absolute;left:1842px;top:56px;font-size:11px;color:${VG};white-space:normal;width:70px;line-height:1.5">QUICK ACTIONS</div>
    ${['New delivery','Reschedule','Assign crew'].map((t,i)=>`<div class="m" style="position:absolute;left:1842px;top:${96+i*40}px;width:70px;height:30px;border-radius:8px;box-shadow:0 0 0 1px #E4DDD5;font-size:10px;line-height:30px;padding-left:8px;overflow:hidden">${t}</div>`).join('')}
    <div class="m" style="position:absolute;left:1842px;top:236px;font-size:11px;color:${VG}">IN STOCK</div>
    ${['chair','sofa','pouf','lamp'].map((k,i)=>`<div style="position:absolute;left:1842px;top:${266+i*92}px;width:70px;height:80px;border-radius:10px;overflow:hidden">${vimg('tile_'+k,'inset:0;width:100%;height:100%','50% 60%')}</div>`).join('')}</div>`;
  return h+'</div>'; }

/* ---------- My Orders dans l'espace de travail (navigateur) ---------- */
const ORDERS=[['chair','Lounge Chair','October 12th, 2026','Red velvet','83 × 57 cm','€890'],['sofa','Kidney Sofa','September 3rd, 2026','Oat velvet','219 × 102 cm','€2,450'],['pouf','Shot Silk Pouf','August 21st, 2026','Plum silk','61 × 61 cm','€340'],['lamp','Glass Lamp','July 9th, 2026','Iridescent','Ø 30 cm','€260']];
function tplVOrders(){ return `<div class="full" style="background:#141312">
  <div class="bar"><span style="position:absolute;left:24px;top:22px">workspace</span><span class="tbtn" style="left:130px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">Preview</span>
    <span style="position:absolute;left:250px;top:20px;letter-spacing:12px;color:#A49D96">○ □ ○</span>
    <span style="position:absolute;right:300px;top:20px;letter-spacing:14px;color:#6d6760">◎ ∿ ‹/›</span>
    <span class="tbtn" style="right:130px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">Share</span><span class="tbtn" style="right:24px;background:var(--ink);color:#fff">Publish</span></div>
  <div style="position:absolute;left:0;right:0;top:64px;height:330px;overflow:hidden">${vimg('chair_hero','inset:0;width:100%;height:100%','50% 42%')}
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,18,.1) 30%,rgba(20,19,18,.82))"></div>
    <div style="position:absolute;left:36px;top:132px;font-size:96px;color:#fff;letter-spacing:-0.045em;line-height:1">My Orders</div>
    <div class="m" style="position:absolute;left:40px;top:240px;font-size:16px;color:rgba(255,255,255,.75)">Your home, so far</div>
    <div style="position:absolute;right:36px;top:24px;display:flex;gap:8px">${[0,1,2].map(()=>`<span style="width:30px;height:30px;border-radius:15px;background:rgba(18,17,16,.6);box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)"></span>`).join('')}</div>
    <div class="m" style="position:absolute;left:36px;right:36px;top:280px;height:40px;border-radius:10px;background:rgba(18,17,16,.62);font-size:13px;line-height:40px;padding-left:16px;color:rgba(243,239,234,.5)">⌕&nbsp; Search by product&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;◷&nbsp; Search by date</div></div>
  <div class="m" style="position:absolute;left:36px;right:36px;top:412px;height:40px;font-size:13px;color:#8E877F"><span style="position:absolute;left:0">PRODUCT</span><span style="position:absolute;left:520px"><b style="color:${VA}">▪</b> FABRIC</span><span style="position:absolute;left:820px"><b style="color:${VA}">▪</b> SIZE</span><span style="position:absolute;left:1080px"><b style="color:${VA}">▪</b> PRICE</span><span style="position:absolute;right:60px"><b style="color:${VA}">▪</b> STATUS</span></div>
  ${ORDERS.map((r,i)=>`<div class="trow" style="top:${452+i*104}px;height:104px">
    <div style="position:absolute;left:0;top:14px;width:76px;height:76px;border-radius:10px;overflow:hidden">${vimg('tile_'+r[0],'inset:0;width:100%;height:100%','50% 62%')}</div>
    <span class="tcell" style="left:96px;top:20px;line-height:1;font-size:24px">${r[1]}</span><span class="tcell m" style="left:96px;top:56px;line-height:1;font-size:13px;color:#8E877F">${r[2]}</span>
    <span class="tcell m" style="left:520px;line-height:104px;font-size:16px;color:#C9C2BA">${r[3]}</span><span class="tcell m" style="left:820px;line-height:104px;font-size:16px;color:#C9C2BA">${r[4]}</span><span class="tcell m" style="left:1080px;line-height:104px;font-size:16px;color:#C9C2BA">${r[5]}</span>
    <span class="tcell" style="right:60px;line-height:104px"><span class="tchip">● ${i==0?'On its way':'Delivered'}</span></span><span class="tcell" style="right:0;line-height:104px;color:#6d6760">›</span></div>`).join('')}</div>`; }

/* ---------- chat IA + page produit (plateau tournant Cycles) + Order Details ---------- */
function tplVChat(){ return `<div class="full" style="background:#F3EFEA">
  <div class="chatp"><div style="position:absolute;left:32px;top:30px">${VLOGO('#151413',22)}<span class="m" style="font-size:13px;color:${VG};margin-left:12px">studio</span></div>
    <div class="bubble" style="top:104px">Add a 3D hero. Make it <em style="font-size:24px">velvet.</em></div>
    <div class="m" style="position:absolute;left:32px;top:196px;font-size:13px;color:#A39C94">Thought for 4s ›</div>
    <div class="ctext" style="top:228px">Swapped the stock handshake for a real-time 3D lounge chair. Velvet, soft window light, one accent.</div>
    <div class="citem" style="top:326px">▾ Installed 2 packages</div><div class="citem" style="top:356px;color:#A39C94">&nbsp;&nbsp;three · velvet-shader</div>
    <div style="position:absolute;left:32px;right:32px;top:398px;height:150px;border-radius:16px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">
      <div style="position:absolute;left:20px;top:18px;font-size:17px">Approval Required</div><div class="m" style="position:absolute;left:20px;top:44px;font-size:12px;color:${VG}">These files will be removed forever</div>
      <div class="m" style="position:absolute;left:20px;top:72px;font-size:13px;color:#E5484D">– stock_handshake_final_v3.jpg</div><div class="m" style="position:absolute;left:20px;top:94px;font-size:13px;color:#E5484D">– font-family: Arial;</div>
      <div class="m chapp" style="position:absolute;left:20px;bottom:-56px;height:38px;line-height:38px;padding:0 18px;border-radius:19px;background:var(--ink);color:#fff;font-size:14px">Approve</div>
      <div class="m" style="position:absolute;left:130px;bottom:-56px;height:38px;line-height:36px;padding:0 18px;border-radius:19px;border:1px solid #D9D2CA;color:#6d6760;font-size:14px">Reject</div></div>
    <div class="m" style="position:absolute;left:32px;top:860px;font-size:13px;color:${VG}">▪ SUGGESTIONS</div>
    ${['Add a sofa','Warmer light','Make it spin'].map((t,i)=>`<div class="m" style="position:absolute;left:${32+i*180}px;top:890px;height:38px;line-height:36px;padding:0 14px;border-radius:19px;border:1px solid #D9D2CA;font-size:14px;color:#5f5952">${t}</div>`).join('')}
    <div style="position:absolute;left:24px;right:24px;bottom:28px;height:84px;border-radius:20px;background:#fff;box-shadow:0 0 0 1px #E6E1DB"><span style="position:absolute;left:22px;top:28px;font-size:19px;color:#A39C94;font-weight:400">What would you like to change?</span><span style="position:absolute;right:16px;top:16px;width:52px;height:52px;border-radius:14px;background:var(--ink)"></span></div></div>
  <div style="position:absolute;left:640px;top:34px">${VLOGO('#151413',22)}</div>
  <div style="position:absolute;left:640px;top:92px;font-size:46px;letter-spacing:-0.035em">Lounge Chair</div>
  <div class="m" style="position:absolute;left:643px;top:152px;font-size:15px;color:${VG}">Built for sitting well</div>
  <div style="position:absolute;left:630px;top:196px;width:918px;height:668px;border-radius:24px;overflow:hidden;background:#E6DED4"><canvas class="pturn" width="1100" height="800" style="position:absolute;inset:0;width:100%;height:100%"></canvas><canvas class="pthermal" width="459" height="334" style="position:absolute;inset:0;width:100%;height:100%;display:none"></canvas></div>
  <div style="position:absolute;left:630px;top:884px;display:flex;gap:12px">${['chair','sofa','pouf','lamp'].map((k,i)=>`<div style="width:112px;height:112px;border-radius:16px;overflow:hidden;${i==0?`box-shadow:0 0 0 3px ${VA}`:''}">${vimg('tile_'+k,'position:relative;width:100%;height:100%','50% 62%')}</div>`).join('')}</div>
  <div class="spec"><div class="m" style="position:absolute;left:32px;top:36px;font-size:12px;color:#8E877F">ORDER DETAILS</div>
    <div style="position:absolute;left:32px;top:70px;width:84px;height:84px;border-radius:12px;overflow:hidden">${vimg('tile_chair','inset:0;width:100%;height:100%','50% 62%')}</div>
    <div style="position:absolute;left:132px;top:78px;font-size:24px;letter-spacing:-0.02em">Lounge Chair</div><div class="m spcol" style="position:absolute;left:132px;top:114px;font-size:13px;color:#8E877F">Corporate blue</div>
    ${[['fabric','velvet'],['colour','<i class="spsw"></i>'],['size','83 × 57 cm'],['delivery','3 days'],['assembly','none needed'],['arial','0']].map((r,i)=>`<div class="srow" style="top:${190+i*62}px">${r[0]}<b>${r[1]}</b></div>`).join('')}
    <div class="m" style="position:absolute;left:32px;top:600px;font-size:12px;color:#8E877F">TOTAL</div><div style="position:absolute;left:32px;top:622px;font-size:54px;letter-spacing:-0.04em">€890</div>
    <div style="position:absolute;left:32px;right:32px;bottom:36px;height:64px;border-radius:32px;background:var(--accent);color:#fff;font-size:21px;line-height:64px;text-align:center">Add to cart →</div></div></div>`; }

/* ---------- Order Complete (photo plein cadre, titre géant, résumé) ---------- */
function tplVDone(){ return `<div class="full" style="background:${VINK};overflow:hidden">${vimg('chair_hero','inset:0;width:100%;height:100%','50% 50%')}
  <div class="full" style="background:linear-gradient(180deg,rgba(18,17,16,.28),rgba(18,17,16,0) 35%)"></div>
  <div class="vpill" style="left:22px;top:20px;background:rgba(18,17,16,.55)">${VLOGO('#F3EFEA',17)}<span style="margin-left:16px;color:#8E877F">≡</span></div>
  <div class="vpill" style="right:150px;top:20px;background:${VA};color:#fff">New in</div><div class="vpill" style="right:22px;top:20px;background:rgba(18,17,16,.55);color:#F3EFEA">Search pieces</div>
  <div class="vhead" style="left:20px;top:58px;font-size:168px">Order ${VMARK(124)} Complete</div>
  <div style="position:absolute;right:28px;bottom:28px;width:330px;height:168px;border-radius:18px;background:rgba(18,17,16,.84);color:#F3EFEA"><div class="m" style="position:absolute;left:20px;top:18px;font-size:12px;color:#8E877F">ORDER SUMMARY</div>
    <div style="position:absolute;left:20px;top:44px;font-size:19px">1× Lounge Chair, red velvet</div><div class="m" style="position:absolute;left:20px;top:74px;font-size:13px;color:#8E877F">arrives Thu 22 Oct · €890</div>
    <div style="position:absolute;left:20px;right:20px;bottom:16px;height:44px;border-radius:22px;background:${VA};font-size:17px;line-height:44px;text-align:center">Track order</div></div></div>`; }

/* ---------- profil client (montage, comme « Jessica Martinez ») ---------- */
function tplVProfile(){ return `<div class="full" style="background:${VINK};color:#F3EFEA;overflow:hidden">
  <div style="position:absolute;left:0;top:0;width:52px;height:730px;border-right:1px solid rgba(255,255,255,.07)">${[0,1,2,3,4,5,6].map(i=>`<div style="position:absolute;left:17px;top:${24+i*44}px;width:18px;height:18px;border-radius:5px;${i==2?`background:${VA}`:'border:1.5px solid rgba(243,239,234,.3)'}"></div>`).join('')}</div>
  <div style="position:absolute;left:52px;right:0;top:0;height:300px;overflow:hidden">${vimg('room_eye','inset:0;width:100%;height:100%','50% 62%')}<div class="full" style="background:linear-gradient(180deg,rgba(18,17,16,.15),rgba(18,17,16,.9))"></div></div>
  <div class="m" style="position:absolute;left:80px;top:24px;font-size:12px;color:rgba(243,239,234,.75)">Dashboard&nbsp;&nbsp;&nbsp;Rooms&nbsp;&nbsp;&nbsp;<b style="color:#fff">Customers</b></div>
  <div style="position:absolute;left:80px;top:198px;width:64px;height:64px;border-radius:16px;background:${VA};font-size:26px;line-height:64px;text-align:center;color:#fff">EL</div>
  <div style="position:absolute;left:162px;top:196px;font-size:58px;letter-spacing:-0.04em;line-height:1">Emma Laurent</div><div class="m" style="position:absolute;left:166px;top:256px;font-size:13px;color:${VG}">@emma_lives_here · Marais</div>
  <div class="m" style="position:absolute;left:80px;top:318px;font-size:12px;color:${VG}">Pieces&nbsp;&nbsp;&nbsp;&nbsp;Rooms&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#F3EFEA">Orders</b>&nbsp;&nbsp;&nbsp;&nbsp;Wishlist</div>
  ${[['12','pieces'],['€8,940','spent'],['3','rooms styled']].map(([n,t],i)=>`<div style="position:absolute;left:80px;top:${360+i*108}px;width:250px;height:92px;border-radius:14px;background:rgba(255,255,255,.05)"><div style="position:absolute;left:18px;top:14px;font-size:40px;letter-spacing:-0.04em">${n}</div><div class="m" style="position:absolute;left:20px;top:64px;font-size:12px;color:${VG}">${t}</div><span style="position:absolute;right:16px;top:30px;width:30px;height:30px;border-radius:8px;background:${i==0?VA:'rgba(255,255,255,.1)'}"></span></div>`).join('')}
  <div style="position:absolute;left:356px;top:356px;width:560px;height:350px;border-radius:14px;background:rgba(255,255,255,.04)"><div class="m" style="position:absolute;left:18px;top:16px;font-size:12px;color:${VG}">RECENT ORDERS</div>
    ${ORDERS.map((r,i)=>`<div style="position:absolute;left:18px;right:18px;top:${46+i*74}px;height:64px"><div style="position:absolute;left:0;top:0;width:64px;height:64px;border-radius:10px;overflow:hidden">${vimg('tile_'+r[0],'inset:0;width:100%;height:100%','50% 62%')}</div><div style="position:absolute;left:80px;top:10px;font-size:18px">${r[1]}</div><div class="m" style="position:absolute;left:80px;top:38px;font-size:11px;color:${VG}">${r[2]}</div><div class="m" style="position:absolute;right:0;top:22px;font-size:14px;color:#C9C2BA">${r[5]}</div></div>`).join('')}</div>
  <div style="position:absolute;left:940px;top:356px;width:280px;height:170px;border-radius:14px;background:rgba(255,255,255,.04)"><div class="m" style="position:absolute;left:18px;top:16px;font-size:12px;color:${VG}">QUOTE OF THE DAY</div><div style="position:absolute;left:18px;top:46px;right:18px;font-size:21px;line-height:1.25;white-space:normal">“Life is too short for <em style="font-size:24px">boring</em> chairs.”</div></div>
  <div style="position:absolute;left:940px;top:540px;width:280px;height:166px;border-radius:14px;background:rgba(255,255,255,.04)"><div class="m" style="position:absolute;left:18px;top:16px;font-size:12px;color:${VG}">STYLE MATCH</div><div style="position:absolute;left:18px;top:40px;font-size:62px;letter-spacing:-0.05em">98<span style="font-size:28px">%</span></div><div style="position:absolute;left:18px;right:18px;bottom:22px;height:6px;border-radius:3px;background:rgba(255,255,255,.1)"><div style="width:98%;height:6px;border-radius:3px;background:${VA}"></div></div></div></div>`; }
