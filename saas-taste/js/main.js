/* ============================================================
   Rendu d'une image + initialisation + aperçu navigateur
   ============================================================ */
function renderFrame(f){
  f=Math.round(f);
  show($('iriFull'),false); show(CUR,false);
  for(const sc of SCENES){ const on=f>=sc.f0&&f<=sc.f1; show(sc.el,on); if(on) sc.render(f); }
  return f;
}
async function init(){
  await Promise.race([new Promise(r=>window.T3D?r():addEventListener('t3d-ready',r)),new Promise(r=>setTimeout(r,8000))]);
  if(!window.T3D) console.error('3D indisponible');
  await document.fonts.ready;
  await Promise.all(['500 52px ID','600 52px ID','400 52px ID','italic 60px IS','20px JB','500 20px JB','700 30px AR','30px AR','30px "Noto Color Emoji"'].map(s=>document.fonts.load(s).catch(()=>{})));
  // mises en page qui dépendent des mesures de texte : scènes visibles le temps de mesurer
  const meas=['sPills','sTerm','sOutro','sLogo'].map(id=>$(id)); meas.forEach(s=>show(s,true));
  pillsLayout(); termLayout(); outroLayout();
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
