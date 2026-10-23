/* ============================================================
   L'après de velvetly : une vraie refonte, pas un recoloriage.
   App sombre, photo plein cadre du salon en tête, titre géant « Morning, Léa. », chiffres en grand,
   liste des pièces avec vignettes (la réf passe à une UI sombre et photographique à 642).
   Le morph est un « élément partagé » : chaque bloc de la v1 vole vers son bloc de la v2
   (boîte qui change de taille et de rayon, contenu qui suit), né lilas, sec à l'ivoire.
   Espace de travail : 1360 × H (800 par défaut), le même que buildDash.
   ============================================================ */
const D2_IV='#F3EFEA', D2_MOD='#1E1C1B';
// positions finales de la v2
const D2_R={flood:[0,0,1360,800],hero:[0,0,1360,470],title:[120,246,820,130],sub:[126,394,700,26],btn:[1166,26,154,48],nav:[400,30,520,40],
  kpi0:[120,500,280,270],kpi1:[420,500,280,270],kpi2:[720,500,280,270],list:[1020,500,300,270]};
// positions de la v1 (buildDash, mêmes coordonnées)
const D2_A1={flood:[0,0,260,800],hero:[980,350,340,410],title:[300,40,560,74],sub:[302,112,420,30],btn:[1150,52,170,46],
  kpi0:[300,170,320,150],kpi1:[650,170,320,150],kpi2:[1000,170,320,150],list:[300,350,650,410]};
// l'ordre de la vague (images après le départ) et la durée de chaque bloc
const D2_T={flood:[0,8],hero:[1,9],title:[2,7],sub:[3,6],btn:[3,6],nav:[4,6],kpi0:[4,7],kpi1:[5,7],kpi2:[6,7],list:[6,7]};
const D2_SPARK=[[.1,.18,.15,.3,.28,.42,.5,.47,.62,.7,.86,1],[.2,.15,.28,.25,.38,.34,.45,.52,.5,.63,.72,.8],[.05,.1,.12,.2,.26,.3,.42,.55,.6,.74,.9,1]];
// ressort amorti à 0,8 (dépassement ≈ 1,5 %), posé en fin de durée
function d2Spring(t){ if(t<=0) return 0; if(t>=1) return 1; const z=6, w=4.5; return 1-Math.exp(-z*t)*(Math.cos(w*t)+(z/w)*Math.sin(w*t)); }
let D2_N=0;
function buildDash2(root,H=800){ const u='d2'+(D2_N++);   // identifiants de dégradé propres à chaque instance (sinon la courbe pointe vers une copie cachée)
  const box=(k,css,inner='')=>`<div class="d2 d2-${k}" data-k="${k}" style="position:absolute;${css}"><div class="d2c" style="position:absolute;left:0;top:0;transform-origin:0 0">${inner}</div></div>`;
  const kpis=[['ROOMS LIVE','1,234','+18%'],['EMBEDS','312','+9%'],['3D VIEWS','48.2k','+31%']];
  const spark=(v,i)=>{ const p=v.map((y,j)=>[j*232/(v.length-1),52-y*44]); const d=p.map(([x,y],j)=>(j?'L':'M')+x.toFixed(1)+' '+y.toFixed(1)).join(' ');
    return `<svg width="232" height="56" viewBox="0 0 232 56" style="position:absolute;left:24px;top:192px;overflow:visible"><defs><linearGradient id="${u}g${i}" x1="0" x2="1"><stop offset="0" stop-color="#CDB9F2"/><stop offset="1" stop-color="#FFC9A8"/></linearGradient>
      <linearGradient id="${u}a${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CDB9F2" stop-opacity=".22"/><stop offset="1" stop-color="#CDB9F2" stop-opacity="0"/></linearGradient></defs>
      <path d="${d} L232 56 L0 56 Z" fill="url(#${u}a${i})"/><path d="${d}" fill="none" stroke="url(#${u}g${i})" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="${p[p.length-1][0]}" cy="${p[p.length-1][1]}" r="4.5" fill="#FFC9A8"/></svg>`; };
  let h=box('flood',`left:0;top:0;width:260px;height:${H}px;border-radius:20px;background:#151413`);
  h+=box('hero','left:0;top:0;width:1360px;height:470px;border-radius:20px 20px 0 0;overflow:hidden',
    `<img src="img/room_eye.jpg" class="d2img" style="position:absolute;left:0;top:-140px;width:1360px;height:765px;object-fit:cover">
     <div style="position:absolute;left:0;top:0;width:1360px;height:470px;background:linear-gradient(90deg,rgba(21,20,19,.82) 0%,rgba(21,20,19,.45) 42%,rgba(21,20,19,0) 68%),linear-gradient(180deg,rgba(21,20,19,.35) 0%,rgba(21,20,19,0) 22%,rgba(21,20,19,0) 62%,#151413 100%)"></div>
     <div class="d2hot" style="position:absolute;left:1112px;top:262px;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:22px;box-shadow:0 0 0 2px ${D2_IV},0 0 0 10px rgba(243,239,234,.18)"></div>
     <div class="d2tag" style="position:absolute;right:270px;top:180px;height:34px;padding:0 14px;border-radius:17px;background:rgba(21,20,19,.55);backdrop-filter:blur(8px);font:400 13px/34px 'JB';color:${D2_IV};white-space:nowrap">Lounge Chair · velvet · 61%</div>`);
  h+=box('nav','left:400px;top:30px;width:520px;height:40px',['Overview','Rooms','Embeds','Settings'].map((t,i)=>`<span style="position:absolute;left:${[0,124,226,330][i]}px;top:0;height:40px;padding:0 18px;border-radius:20px;font:500 15px/40px 'ID';white-space:nowrap;${i?`background:rgba(243,239,234,.12);color:${D2_IV}`:`background:${D2_IV};color:#151413`}">${t}</span>`).join('')+
    `<span style="position:absolute;left:-280px;top:4px;font:600 26px/32px 'ID';letter-spacing:-.03em;color:${D2_IV};white-space:nowrap"><span style="display:inline-block;width:14px;height:14px;border-radius:7px;background:#FF3D5E;margin-right:10px;vertical-align:2px"></span>velvetly</span>`);
  h+=box('btn','left:1166px;top:26px;width:154px;height:48px;border-radius:24px;background:'+D2_IV,`<span style="position:absolute;left:0;top:0;width:154px;height:48px;text-align:center;font:500 17px/48px 'ID';color:#151413;white-space:nowrap">New report →</span>`);
  h+=box('title','left:120px;top:246px;width:820px;height:130px',`<span class="d2t" style="position:absolute;left:0;top:0;font:500 124px/1 'ID';letter-spacing:-.05em;color:${D2_IV};white-space:nowrap">Morning, <em style="font-family:'BE';font-weight:400;letter-spacing:-.02em">Léa.</em></span>`);
  h+=box('sub','left:126px;top:394px;width:700px;height:26px',`<span class="d2t" style="position:absolute;left:0;top:0;font:400 16px/26px 'JB';color:rgba(243,239,234,.72);white-space:nowrap">Room 04 is live · 1,204 people sat in it today</span>`);
  kpis.forEach(([l,v,d],i)=>{ h+=box('kpi'+i,`left:${120+i*300}px;top:500px;width:280px;height:270px;border-radius:18px;background:${D2_MOD}`,
    `<span style="position:absolute;left:24px;top:24px;font:400 12px 'JB';letter-spacing:.1em;color:#8E877F;white-space:nowrap">${l}</span>
     <span style="position:absolute;left:186px;top:18px;width:70px;height:26px;text-align:center;border-radius:13px;box-shadow:inset 0 0 0 1px rgba(243,239,234,.22);font:500 12px/26px 'JB';color:${D2_IV}">${d}</span>
     <span class="d2t" style="position:absolute;left:20px;top:64px;font:500 88px/1 'ID';letter-spacing:-.055em;color:${D2_IV};white-space:nowrap">${v}</span>${spark(D2_SPARK[i],i)}`); });
  h+=box('list',`left:1020px;top:500px;width:300px;height:270px;border-radius:18px;background:${D2_MOD}`,
    `<span style="position:absolute;left:24px;top:22px;font:500 18px 'ID';color:${D2_IV};white-space:nowrap">Top rooms <span style="font:400 12px 'JB';color:#8E877F;margin-left:6px">today</span></span>`+
    [['tile_chair','Lounge Chair','61% of clicks'],['tile_sofa','Kidney Sofa','22% of clicks'],['tile_pouf','Velvet Pouf','9% of clicks']].map(([im,n,s],i)=>
      `<div style="position:absolute;left:24px;top:${64+i*66}px;width:252px;height:54px"><img src="img/${im}.jpg" style="position:absolute;left:0;top:0;width:54px;height:54px;border-radius:12px;object-fit:cover">
        <span style="position:absolute;left:70px;top:6px;font:500 16px 'ID';color:${D2_IV};white-space:nowrap">${n}</span><span style="position:absolute;left:70px;top:30px;font:400 12px 'JB';color:#8E877F;white-space:nowrap">${s}</span>
        <span style="position:absolute;right:0;top:15px;font:500 13px 'JB';color:${D2_IV}">${['↑ 18','↑ 6','↑ 2'][i]}</span></div>`).join(''));
  const w=document.createElement('div'); w.className='dash2'; w.style.cssText=`position:absolute;left:0;top:0;width:1360px;height:${H}px;pointer-events:none`; w.innerHTML=h; root.appendChild(w);
  const els={}; w.querySelectorAll('.d2').forEach(e=>{ els[e.dataset.k]=e; e._c=e.firstElementChild; });
  return {w,els,H,img:w.querySelector('.d2img'),hot:w.querySelector('.d2hot'),tag:w.querySelector('.d2tag')};
}
// f : image courante ; f0 : départ de la vague ; A : rectangles de la v1 (coordonnées de la v2), Ael : éléments de la v1 à faire partir,
// ak : taille d'une unité de la v2 dans l'espace des éléments de la v1 (1 si même espace)
function dash2Morph(D,f,f0,A=D2_A1,Ael={},ak=1){
  const any=f>=f0; D.w.style.display=any?'block':'none';
  for(const k in D.els){ const e=D.els[k], [t0,dur]=D2_T[k], t=clamp((f-f0-t0)/dur), s=d2Spring(t), R=k==='flood'?[0,0,1360,D.H]:D2_R[k], a=A[k];
    const r=a?[lerp(a[0],R[0],s),lerp(a[1],R[1],s),lerp(a[2],R[2],s),lerp(a[3],R[3],s)]:R;
    Object.assign(e.style,{left:r[0].toFixed(1)+'px',top:r[1].toFixed(1)+'px',width:Math.max(1,r[2]).toFixed(1)+'px',height:Math.max(1,r[3]).toFixed(1)+'px'});
    // le contenu suit sa boîte, à l'échelle de sa hauteur (jamais déformé)
    const cs=a?clamp(lerp(a[3]/R[3],1,s),0.2,1.6):1; e._c.style.transform=`scale(${cs.toFixed(4)})`;
    const born=clamp((f-f0-t0-dur*0.55)/10);
    if(k==='flood'){ e.style.background=t<=0?'#2D6CDF':t<0.15?mixc('#2D6CDF',MORPH.fill,t/0.15):mixc(MORPH.fill,'#151413',clamp((t-0.15)/0.25)); e.style.borderRadius=lerp(0,20,s).toFixed(1)+'px'; e.style.opacity=t>0?'1':'0'; continue; }
    if(k==='hero'){ e.style.opacity=t>0?'1':'0'; e.style.borderRadius=`${lerp(4,20,s).toFixed(1)}px ${lerp(4,20,s).toFixed(1)}px ${lerp(4,0,s).toFixed(1)}px ${lerp(4,0,s).toFixed(1)}px`;
      e.style.filter=t>0&&t<1?`blur(${(5*(1-t)).toFixed(1)}px)`:''; continue; }
    if(k==='btn'){ e.style.background=t<0.2?mixc('#2D6CDF',MORPH.fill,t/0.2):mixc(MORPH.fill,D2_IV,clamp((t-0.2)/0.3)); e.style.borderRadius=lerp(4,24,s).toFixed(1)+'px'; }
    if(k.startsWith('kpi')||k==='list') e.style.background=t<0.12?mixc('#FFFFFF',MORPH.fill,t/0.12):mixc(MORPH.fill,D2_MOD,clamp((t-0.12)/0.25));
    // le contenu se pose : flou 6 → 0, né lilas, sèche à l'ivoire
    const ci=clamp((t-0.25)/0.6); e._c.style.opacity=ci.toFixed(3); e._c.style.filter=ci>0.01&&ci<0.99?`blur(${(6*(1-ci)).toFixed(1)}px)`:'';
    if(k!=='btn'&&k!=='nav') e._c.querySelectorAll('.d2t').forEach(x=>x.style.color=mixc(MORPH.fill,D2_IV,born));
    e.style.opacity=t>0?'1':'0'; if(k==='nav') e.style.translate=`0 ${(10*(1-s)).toFixed(1)}px`; }
  // la v1 part vers la place de son bloc v2 en se troublant
  for(const k in Ael){ const el=Ael[k]; if(!el) continue; const [t0,dur]=D2_T[k], t=clamp((f-f0-t0)/dur), a=A[k], R=k==='flood'?[0,0,1360,D.H]:D2_R[k];
    if(t<=0){ el.style.opacity=''; el.style.filter=''; el.style.translate=''; el.style.scale=''; continue; }
    const s=d2Spring(t), dx=(R[0]-a[0])*s*ak, dy=(R[1]-a[1])*s*ak, sc=lerp(1,R[3]/a[3],s*0.6);
    el.style.translate=`${dx.toFixed(1)}px ${dy.toFixed(1)}px`; el.style.scale=sc.toFixed(4); el.style.transformOrigin='0 0';
    el.style.opacity=(1-clamp(t/0.5)).toFixed(3); el.style.filter=`blur(${(6*clamp(t/0.5)).toFixed(1)}px)`; }
  // la photo respire (2 %), le repère pulse doucement
  if(any){ const kb=clamp((f-f0)/24); D.img.style.transform=`scale(${(1.06-0.06*kb).toFixed(4)})`; D.img.style.transformOrigin='70% 50%';
    const hp=clamp((f-f0-8)/5); D.hot.style.opacity=hp.toFixed(3); D.tag.style.opacity=hp.toFixed(3); D.tag.style.translate=`${(12*(1-hp)).toFixed(1)}px 0`; }
}
