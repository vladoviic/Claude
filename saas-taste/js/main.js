/* ============================================================
   Rendu d'une image + initialisation + aperçu navigateur
   ============================================================ */
function renderFrame(f){
  f=Math.round(f);
  show(CUR,false); CUR.style.opacity='';
  for(const sc of SCENES){ const on=f>=sc.f0&&f<=sc.f1; show(sc.el,on); if(on) sc.render(f); }
  return f;
}
/* Recalage sur les coupes exactes de la réf (mesurées image par image) :
   [début, fin, décalage] — la scène rend f+décalage, ses cues sont avancés d'autant. */
const REMAP={sTree:[300,346,0],sDash:[347,379,1],sHero:[380,417,1],sPills:[418,465,2],sPlan:[466,558,2],sPhone:[559,641,2],
  sTerm:[695,814,1],sMacro:[815,879,1],sChat:[880,951,0],sDone:[952,1077,2],sGrid:[1078,1129,2],sReport:[1130,1174,1],
  sAlerts:[1175,1249,1],sShip:[1250,1306,1],sMont:[1307,1377,1],sOutro:[1378,1559,2]};
function applyRemap(){
  for(const sc of SCENES){ const m=REMAP[sc.id]; if(!m) continue; const [n0,n1,d]=m, o0=sc.f0, o1=sc.f1;
    for(const c of CUES){ if(c._moved||c.f<o0||c.f>o1) continue; c.f-=d; for(const k of ['peak','end']) if(k in c) c[k]-=d; c._moved=true; }
    sc.f0=n0; sc.f1=n1; const r=sc.render; sc.render=f=>r(f+d); }
  CUES.forEach(c=>delete c._moved);
}
// V23 : la dent du papier (img/tooth.png, fibres courtes, tuile de 1024) sous le contenu des fonds papier, en lumière douce (≈ 1,6/255).
// Elle est dans la caméra : elle appartient à la feuille et bouge avec elle. Les cartes et les boutons, opaques, restent lisses.
// La caméra a un transform, donc son propre contexte de fusion : un fond papier sous la dent lui donne quelque chose à éclairer.
const TOOTH_SCENES=['sW','sLogo','sPrompt','sTree','sPills','sPlan','sPhone','sGrid','sReport','sOutro'];
preload('img/tooth.png');
function addTooth(){ for(const id of TOOTH_SCENES){ const cam=$(id).querySelector(':scope>.cam'); if(!cam) continue;
  const g=document.createElement('div'); g.className='sheet'; g.style.background=getComputedStyle($(id)).backgroundColor;
  const t=document.createElement('div'); t.className='tooth'; cam.prepend(g,t); } }
async function init(){
  applyRemap(); addTooth();
  // toutes les photos (rendus Cycles) décodées avant la première image
  // toutes les images chargées (le décodage se fait à la demande, au dessin : decode() rejette quand il y en a des centaines)
  await Promise.all([...document.images,...PRELOAD].map(im=>im.complete&&im.naturalWidth?0:new Promise(r=>{ im.addEventListener('load',r,{once:true}); im.addEventListener('error',()=>{ console.error('image manquante : '+im.src); r(); },{once:true}); })));
  await Promise.all(ASYNC);
  await document.fonts.ready;
  await Promise.all(['500 52px ID','600 52px ID','400 52px ID','italic 400 60px BE','italic 500 60px BE','20px JB','500 20px JB','700 30px AR','30px AR','30px "Noto Color Emoji"','800 40px AV','700 40px SY','600 40px UB','40px AN','40px DS','italic 40px DS'].map(s=>document.fonts.load(s).catch(()=>{})));
  // mises en page qui dépendent des mesures de texte : scènes visibles le temps de mesurer
  const meas=['sPills','sTerm','sOutro','sLogo','sW'].map(id=>$(id)); meas.forEach(s=>show(s,true));
  pillsLayout(); termLayout(); outroLayout(); logoLayout(); wLayout(); prLayout();
  meas.forEach(s=>show(s,false));
  CUES.sort((a,b)=>a.f-b.f);
  window.CUES=CUES; window.TOTAL=TOTAL; window.renderFrame=renderFrame; window.READY=true;
  if(!/render/.test(location.search)) preview();
}
function preview(){
  const st=$('stage'); const fit=()=>{ const s=Math.min(innerWidth/W,(innerHeight-40)/H); st.style.transform=`scale(${s})`; }; fit(); addEventListener('resize',fit);
  const ui=$('ui'), uis=$('uis'), uif=$('uif'); ui.style.display='flex'; uis.max=TOTAL-1;
  let f=0, playing=true, t0=performance.now(), f0=0;
  const set=x=>{ f=((x%TOTAL)+TOTAL)%TOTAL; renderFrame(f); uis.value=f; uif.textContent='f'+f+' · '+(f/FPS).toFixed(2)+'s'; };
  uis.oninput=()=>{ playing=false; set(+uis.value); };
  addEventListener('keydown',e=>{ if(e.code=='Space'){ playing=!playing; t0=performance.now(); f0=f; e.preventDefault(); } if(e.code=='ArrowRight'){playing=false;set(f+1);} if(e.code=='ArrowLeft'){playing=false;set(f-1);} });
  (function loop(){ if(playing) set(f0+Math.floor((performance.now()-t0)/1000*FPS)); requestAnimationFrame(loop); })();
}
init();
