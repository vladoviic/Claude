/* ============================================================
   Plans 1 à 16 : timings recopiés de la réf (numéros d'image de la réf, cf. SPEC.md)
   ============================================================ */
function el(parent,cls='',html='',css=''){ const d=document.createElement('div'); if(cls) d.className=cls; if(html) d.innerHTML=html; if(css) d.style.cssText=css; parent.appendChild(d); return d; }
function canvas(parent,w,h,css=''){ const c=document.createElement('canvas'); c.width=w; c.height=h; c.style.cssText='position:absolute;'+css; parent.appendChild(c); return c; }
const SCENES=[];
function scene(id,f0,f1,render,cls=''){ const s=document.createElement('div'); s.className='scene '+cls; s.id=id; $('stage').insertBefore(s,$('cursor')); const cam=el(s,'cam'); SCENES.push({id,f0,f1,render,el:s}); return {s,cam}; }
// dégradé vertical mélangé en lumière linéaire et tramé à ±1 (triangulaire) : pas de bandes sous x264
function ditherV(stops,h,seed){ const c=document.createElement('canvas'); c.width=8; c.height=h; const x=c.getContext('2d'), im=x.createImageData(8,h), R=rng(seed);
  const st=stops.map(([t,hx])=>[t,hex(hx).map(v=>Math.pow(v/255,2.2))]);
  for(let y=0;y<h;y++){ const t=y/(h-1); let k=0; while(k<st.length-2&&st[k+1][0]<t) k++; const [t0,a]=st[k], [t1,b]=st[k+1], u=clamp((t-t0)/(t1-t0));
    const lin=a.map((v,i)=>lerp(v,b[i],u)); for(let xx=0;xx<8;xx++){ const o=(y*8+xx)*4; lin.forEach((v,i)=>{ im.data[o+i]=clamp(Math.round(Math.pow(v,1/2.2)*255+(R()-R())),0,255); }); im.data[o+3]=255; } }
  x.putImageData(im,0,0); return c.toDataURL(); }
// derrière les écrans cadrés : le ciel de la fenêtre de Ship it (1251), chroma ramené à 12 au plus. Un ciel, un soleil.
const SKY_STOPS=[[0,'#ECE4DC'],[.25,'#F2E3D5'],[.45,'#F6E2D0'],[.6,'#F6E3D0'],[.75,'#E7DACC'],[.98,'#B3CAC9'],[1,'#B3CAC9']];
let SKY_URL=null;
function sky(parent){ SKY_URL=SKY_URL||ditherV(SKY_STOPS,1200,11); el(parent,'sky','',`background:url(${SKY_URL}) 0 0/100% 100%`); }
const push=(cam,f,f0,k=0.001)=>{ cam.style.transform=`scale(${(1+k*(f-f0)).toFixed(4)})`; };
const T=f=>f/FPS;

/* ---------- 1-3 · « Your SaaS is boring. » → caret rouge → « a bit » inséré ; puis l'éclatement de sites ---------- */
const W1=scene('sW',0,119,f=>shotW(f));
// la phrase vit dans l'espace écran (hors caméra) : la coupe de 62 ne change que ce qu'il y a derrière
const wWord=el(W1.s,'abs c word','', 'font-size:60px;z-index:30;text-shadow:0 0 24px rgba(238,233,228,.9)');
wWord.innerHTML='<span class="wa"></span><span class="wi" style="display:inline-block;overflow:hidden;vertical-align:bottom;white-space:pre"></span><span class="wb ar" style="color:var(--blue);font-weight:400"></span>';
const [wA,wI,wB2]=['.wa','.wi','.wb'].map(q=>wWord.querySelector(q));
// la phrase : six mots comme la réf (« How | far | can | your | apps | go? »), une fenêtre de trois mots au plus,
// qui change sur les mêmes images (17, 24, 44, 49, 55, 61, 80, 85) ; « boring. » est le bleu Arial du fondateur (le « go? » coloré de la réf)
const WST=[[17,'Your',''],[24,'Your SaaS',''],[44,'is',''],[49,'is a',''],[55,'is a bit',''],[61,'a bit ','boring.'],[80,'bit ','boring.'],[85,'','boring.'],[93,'','']];
function wLayout(){}
const wInk=inkLayer(W1.s);
const GACC='#FF3D5E', GLIL='#9C86FF', GINK='#151413', GBORN='#C9D9F6', GOR='#EE8A4C', GLV='#A98AE8';
// le fantôme : les sites à venir, très flous, à peine visibles derrière la phrase (réf 0-61)
const wGhost=el(W1.s,'','', 'position:absolute;inset:0;pointer-events:none;filter:blur(26px)');
wGhost.innerHTML=[[150,150,260,200],[420,120,200,240],[880,90,140,300],[1240,140,230,220],[180,560,240,210],[430,620,200,180],[880,600,120,280],[1240,640,220,200],[1560,300,160,160],[60,360,90,100]].map(([x,y,w,h],k)=>`<i style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:24px;display:block;background:${['#8A7F76','#6E655E','#9A8F86'][k%3]}"></i>`).join('');
W1.s.insertBefore(wGhost,W1.cam);
// les deux grands signes (réf) : « / » seul (0), « // » (7), écartés autour du mot (17), crochets (24), crochets colorés (44)
const W_BR=[0,7].map(b=>el(W1.cam,'abs c glyph','', 'font-size:72px;display:none'));
const W_BRS=[[0,['/','/'],[0,0],[GINK,GINK]],[7,['/','/'],[-14,14],[GINK,GINK]],[17,['/','/'],[-205,205],[GINK,GINK]],[24,['<','>'],[-230,230],[GINK,GINK]],[44,['<','>'],[-230,230],[GLV,GOR]],[53,null]];
// le champ de glyphes : il naît à 26 et s'épaissit comme la réf (1, 2, 4, 6, 8, 10… 26) ; il se ré-agence à chaque mot (44, 49)
const W_FB=[26,28,30,30,31,31,34,35,36,38,38,42,43,44,44,44,44,46,47,49,49,49,49,50,51,51];
const W_FL=[[26,1,330,150],[44,2,380,230],[49,3,520,350]];
const wFld=W_FB.map((b,k)=>{ const r=rng(300+k), d=el(W1.cam,'abs c glyph','', 'display:none'); d._b=b; d._spin=r()<0.45; d._ch=['/','/','<','>','*','/','\\'][(r()*7)|0];
  d._col=r()<0.16?GOR:r()<0.19?GLV:GINK; d._pale=r()<0.12; d._P={}; return d; });
// positions par phase, sur une ellipse autour du mot, jamais sur lui, jamais deux glyphes à moins de 64 px
W_FL.forEach(([,ph,rx,ry])=>{ const r=rng(410+ph*31), pts=[]; wFld.forEach(d=>{ let x,y,t=0; do{ x=(r()*2-1)*rx; y=(r()*2-1)*ry; t++; }
  while(t<800&&((Math.abs(x)<300&&Math.abs(y)<62)||x*x/(rx*rx)+y*y/(ry*ry)>1||pts.some(p=>Math.hypot(p[0]-x,p[1]-y)<64))); pts.push([x,y]); d._P[ph]=[x,y]; }); });
// glyphes épars (prompt, outro) : encre seulement
function gset(n,seed,rx,ry,keep=(x,y)=>Math.abs(x)>=70||Math.abs(y)>=46){ const r=rng(seed), a=[]; let t=0; while(a.length<n&&t++<900){ const x=(r()*2-1)*rx, y=(r()*2-1)*ry; if(!keep(x,y)) continue; if(x*x/(rx*rx)+y*y/(ry*ry)>1) continue; if(a.some(g=>Math.hypot(g[1]-x,g[2]-y)<54)) continue;
  r(); a.push([['/','/','/','<','>','*','|','\\'][(r()*8)|0],x,y,GINK]); } return a; }
// fragments du CSS ennuyeux, dans le bleu du fondateur sur 3 profondeurs ; une grille de 24 px et pas de chevauchement
const FRAGS=['font-family: Arial;','color: #2D6CDF;','box-shadow: 0 6px 10px #000;','border-radius: 4px;','/* TODO: make it pop */','<h1>Welcome back, User!</h1>','lorem ipsum dolor sit','img: stock_handshake.jpg','.btn-primary { }','font-size: 12px;','!important','z-index: 9999;','<marquee>','cursor: pointer;','text-align: center;','Get Started Today!',
  'padding: 4px;','line-height: 1;','gradient(#00f, #f0f)','"Synergy"','name: "User"','alert("Welcome!")','.card { shadow }','font-weight: bold;','Click here','onclick="go()"','#2D6CDF','Arial, sans-serif',
  'opacity: .99;','width: 100%;','{ }',':hover','display: block;','<div class="hero">','stock_photo_02.jpg','<br><br><br>','margin: 0 auto;','!!!','TODO','v1_final_FINAL','<center>','color: blue;','font: 12px Arial','<table>','spacer.gif','€9.99/mo'];
const FRBOX=[]; function fragPos(t,seed,sz){ const r=rng(seed), w=t.length*sz*0.6+40, h=sz*1.5; let x,y,k=0;
  do{ x=20+Math.round(r()*(1860-w)/12)*12; y=40+Math.round(r()*1000/12)*12; k++; }while(k<300&&((Math.abs(x+w/2-960)<w/2+260&&Math.abs(y-540)<60)||FRBOX.some(b=>x<b[2]+8&&x+w+8>b[0]&&y<b[3]+6&&y+h+6>b[1])));
  FRBOX.push([x,y,x+w,y+h]); return [x,y,r]; }
// la réf : ils naissent de 53 à 60 (24, 34, 44, 48 à l'écran), tapés en 2-4 images, sur trois profondeurs ; tout disparaît à la coupe (62)
const W_FRB=FRAGS.map((t,i)=>i<24?53:i<34?54+(i%2):i<44?56+(i%3):59+(i%2));   // 24 à 53, 34 à 55, 44 à 58, 48 à 60 (réf)
const wFr=FRAGS.map((t,i)=>{ const tier=i%10===9?2:i%7===3?1:0, sz=[26,23,21][tier]; const d=el(W1.cam,'abs frag','', `font-size:${sz}px;font-family:FM`); d._t=t; const [x,y,r]=fragPos(t,500+i,sz); d._x=x; d._y=y;
  d._st=W_FRB[i]; d._tier=tier; d.style.filter=tier===1?'blur(1px)':tier===2?'blur(2.2px)':''; d.style.opacity=[1,.62,.34][tier];
  d._col=r()<0.62?GINK:r()<0.3?'#2D6CDF':r()<0.5?GLV:GOR; d._pre=r()<0.3?(r()<0.5?'● ':'○ '):''; d._post=r()<0.25?(r()<0.5?' ●○':' ●'):''; d._hl=r()<0.12; return d; });
// l'éclatement : onze sites recréés (js/sites.js), cinq en grand puis six qui rejoignent le collage
const BR=[[0,0],[1180,0],[0,587],[330,783],[1090,640]].map(([x,y],i)=>[x,y,SITES[i].w,SITES[i].h,i]);
const BCL=[[-200,-95,560,0],[210,-120,430,0],[-360,60,200,0],[-80,120,390,0],[260,95,470,0]];
const BDR=[[-50,-20],[40,-5],[-45,10],[35,40],[100,45]], BST=[84,89,90,89,91], BSW=[[110,0],[-90,1.3],[140,2.2],[-80,3.1],[120,4.4]];
const BXT=[5,6,7,8,9,10].map(i=>[i,SITES[i].w,SITES[i].h]);
const BXC=[[-440,-20,300,-3,-1,0],[-330,-180,270,4,-1,-1],[360,-10,300,-2,1,0],[-40,170,280,3,0,1],[150,-190,200,2,1,-1],[-260,150,240,-4,-1,1]];
const wCol=el(W1.cam,'abs','', 'inset:0;width:1920px;height:1080px'); let wColB=null;
const wB=BR.map(([x,y,w,h,si])=>{ const d=el(wCol,'bshot',SITES[si].html, `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0;background:${SITES[si].color}`); d._r=[x,y,w,h]; d._si=si; return d; });
const wX=BXT.map(([si,w,h])=>{ const d=el(wCol,'bshot',SITES[si].html, `left:0;top:0;width:${w}px;height:${h}px;transform-origin:0 0;background:${SITES[si].color}`); d._w=w; d._h=h; d._si=si; return d; });
const ease3=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
(()=>{ const T=st=>{ const xs=st.map(c=>hex(c)); return [0,1,2].map(j=>xs.map(c=>(c[j]/255).toFixed(3)).join(' ')); };
  const F=(id,st)=>{ const [r,g,b]=T(st); return `<filter id="${id}" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".3 .59 .11 0 0 .3 .59 .11 0 0 .3 .59 .11 0 0 0 0 0 1 0"/><feComponentTransfer><feFuncR type="table" tableValues="${r}"/><feFuncG type="table" tableValues="${g}"/><feFuncB type="table" tableValues="${b}"/></feComponentTransfer></filter>`; };
  $('fx').innerHTML+=F('thA',['#E8732F','#F28C45','#F49A5A','#F2B9A6','#DCC9EC','#BFE4F4','#EAF7FB'])+F('thB',['#D86FD8','#E27FE0','#EBA0D8','#F1C1C6','#E3D3F0','#C9E6F5','#EEF7FB'])
    +F('thIri',['#6E9BAA','#7FA9B8','#9CCFD8','#E8B9D8','#F3C9B0','#CFEFF4','#EEF9FA']); })();
function wTint(f,i){ if(f<64+i) return 'url(#thA)'; if(f<67+i) return 'url(#thB)'; if(f>=114+i*0.6&&f<118) return 'url(#thIri)'; return ''; }
// 115-120 : la pile fond dans une nacre cyan (réf 118-120), le disque bleu pâle la continue (121)
function wPink(d,f){ if(!d._pk) d._pk=el(d,'','', 'position:absolute;inset:0;z-index:99;pointer-events:none;display:none;background:linear-gradient(135deg,#C7F4F3 0%,#BFE3F6 45%,#E6D4F4 75%,#F3D3E6 100%)');
  const p=clamp((f-115)/4.5), e=p*p*(3-2*p); d._pk.style.display=e>0?'block':'none'; d._pk.style.opacity=e.toFixed(3); }
// la carte du fondateur parmi les beaux sites (juge, ronde 3) : SON dashboard v1, bleu #2D6CDF + Arial, pas de teinte ;
// elle arrive en dernier (92, quand « boring. » s'en va), au centre, le curseur « You » posé dessus ; la barre M2 la traverse et la déchirure l'emporte
const wFo=el(wCol,'bshot','', 'left:0;top:0;width:560px;height:350px;transform-origin:0 0;background:#F4F6F9;display:none;overflow:hidden;border-radius:10px');
wFo.innerHTML=`<div class="ar" style="position:absolute;inset:0;font-family:'AR'">
  <div style="position:absolute;left:0;top:0;bottom:0;width:118px;background:#2D6CDF;color:#fff"><div style="position:absolute;left:16px;top:18px;font-weight:700;font-size:17px">velvetly</div>
    ${['Dashboard','Rooms','Embeds','Settings'].map((t,i)=>`<div style="position:absolute;left:10px;right:10px;top:${58+i*30}px;height:24px;border-radius:5px;${i?'':'background:rgba(255,255,255,.18);'}font-size:11px;line-height:24px;padding-left:10px">${t}</div>`).join('')}</div>
  <div style="position:absolute;left:138px;top:20px;font-weight:700;font-size:21px;color:#333">Welcome back, User! <span style="font-family:'Noto Color Emoji'">👋</span></div>
  <div style="position:absolute;left:138px;top:48px;font-size:11px;color:#777">Here is your dashboard overview.</div>
  <div style="position:absolute;right:16px;top:18px;height:28px;line-height:28px;padding:0 14px;border-radius:5px;background:#2D6CDF;color:#fff;font-size:12px;font-weight:700;box-shadow:0 4px 8px rgba(0,0,0,.35)">Get Started</div>
  ${[['Rooms published','1,234'],['Embeds','312'],['3D views','48.2k']].map(([t,v],i)=>`<div style="position:absolute;left:${138+i*136}px;top:76px;width:124px;height:66px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.18)"><div style="position:absolute;left:10px;top:9px;font-size:10px;color:#777">${t}</div><div style="position:absolute;left:10px;top:30px;font-size:21px;font-weight:700;color:#333">${v}</div></div>`).join('')}
  <div style="position:absolute;left:138px;top:156px;width:250px;height:176px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.18)"><div style="position:absolute;left:12px;top:10px;font-size:11px;font-weight:700;color:#333">Monthly 3D Views</div>
    ${[40,52,34,60,48,70,44,74,62,84,66,90].map((h,i)=>`<i style="position:absolute;left:${16+i*19}px;bottom:16px;width:12px;height:${h*1.25}px;background:#2D6CDF;display:block"></i>`).join('')}</div>
  <div style="position:absolute;left:402px;top:156px;width:142px;height:176px;background:#D9DCE1"><svg width="56" height="45" viewBox="0 0 120 96" style="position:absolute;left:43px;top:52px"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="6"/><circle cx="84" cy="30" r="10" fill="#A9AEB6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg>
    <div style="position:absolute;left:0;right:0;top:112px;text-align:center;font-size:8.5px;color:#8A8F97">stock_handshake_final_v3.jpg</div></div></div>`;
[17,24,44,49,55,61].forEach((f,i)=>cue(f,'pluck',{n:[64,67,69,71,72,74][i],v:.3})); cue(0,'tick',{v:.3}); cue(7,'tick',{v:.4}); [80,85].forEach(f=>cue(f,'tick',{v:.25})); 
[26,30,31,36,38,43].forEach(f=>cue(f,'tick',{v:.14})); cue(53,'shimmer',{v:.3,end:61}); cue(104,'riser',{v:.4,end:119}); cue(62,'swish',{v:.45,peak:64,dur:6}); cue(89,'whoosh',{v:.4,peak:99,dur:14}); [64,66,67,70].forEach(f=>cue(f,'tick',{v:.2})); cue(96,'swish',{v:.45,peak:97,dur:4}); cue(104,'shimmer',{v:.5,end:112}); cue(113,'whoosh',{v:.55,peak:120,dur:8}); cue(114,'reel',{v:.35,end:127});
function wState(f){ let st=['','']; for(const [wf,a,b] of WST) if(f>=wf) st=[a,b]; return st; }
function shotW(f){ push(W1.cam,f,0,0.0009);
  // la phrase : centrée, à l'écran, elle change d'un coup sur l'image (comme la réf) ; « boring. » passe au lilas et s'efface (89-92)
  const [ta,tb]=wState(f); show(wWord,!!(ta||tb)); wA.textContent=ta; wB2.textContent=tb; wI.textContent=''; wI.style.width='0px';
  if(ta||tb) place(wWord,960,540,1/(1+0.0009*f));
  wB2.style.color=f>=89?mixc('#2D6CDF','#B79AF0',clamp((f-88)/2)):''; wWord.style.opacity=f>=89?(1-clamp((f-89)/3.5)).toFixed(3):'';
  inkClear(wInk);
  // le fantôme des sites à venir : présent dès 0, il se lève un peu avec le code, disparaît à la coupe
  show(wGhost,f<62); wGhost.style.opacity=(0.055+0.05*clamp((f-50)/10)).toFixed(3);
  // les deux grands signes
  let br=null; for(const b of W_BRS) if(f>=b[0]) br=b;
  W_BR.forEach((d,k)=>{ const on=br&&br[1]&&f>=[0,7][k]; show(d,!!on); if(!on) return; d.textContent=br[1][k]; d.style.color=br[3][k]; place(d,960+br[2][k],540); });
  // le champ : chaque glyphe naît pâle et prend sa couleur en 3 images ; un sur deux tourne (/ | \ -) toutes les 2 images
  const ph=f>=49?3:f>=44?2:1;
  wFld.forEach((d,k)=>{ const on=f>=d._b&&f<53; show(d,on); if(!on) return; const [x,y]=d._P[ph];
    d.textContent=d._spin?['/','|','\\','-'][(Math.floor(f/2)+k)%4]:d._ch; d.style.color=mixc('#E9E2F4',d._col,clamp((f-d._b+1)/3)); d.style.opacity=d._pale?'.45':''; place(d,960+x,540+y); });
  // le code du fondateur (53-61) : tapé, avec puces et surlignages ; il ne survit pas à la coupe
  wFr.forEach((d,i)=>{ const on=f>=d._st&&f<62; show(d,on); if(!on) return; const n=Math.max(2,Math.ceil((f-d._st+1)*d._t.length/3));
    const t=d._t.slice(0,n), hl=d._hl&&n>=d._t.length?`<span style="background:${d._col===GINK?GOR:d._col};color:transparent;margin-left:6px">▆▆▆</span>`:'';
    d.innerHTML=`${d._pre}${t.replace(/&/g,'&amp;').replace(/</g,'&lt;')}${n>=d._t.length?d._post:''}${hl}`; d.style.color=d._col; placeTL(d,d._x,d._y); });
  // collage : accélère progressivement à partir de 89 (comme la réf) ; à 113 il se déchire le long du trait M2
  // la pile est rebattue toutes les 2 images après le serrage ; teinte carte par carte à partir de 114, flou 6 → 24 px sur 117-120
  const shuf=f<97?0:Math.floor((f-97)/2)+1, bl=f>=117?` blur(${lerp(6,24,clamp((f-117)/3)).toFixed(1)}px)`:'';
  // entrée : quatre sites à 62, le cinquième à 64 ; chaque teinte sèche à son tour (carte i à 70 + i)
  wB.forEach((d,i)=>{ if(f<(i==4?64:i==2?60:62)){ show(d,false); return; } show(d,true); const [x,y0,w,h]=d._r, [cx,cy,cw]=BCL[i].map(v=>v*W_PK), y=y0+(i==2?[90,40][f-60]||0:0);
    const pc=wSnap(f), dr=approach(f,62,27,0.08);
    // le collage ne tient jamais : toutes les 3 images (le battement de la réf), chaque carte saute de cadrage (zoom et recentrage
    // de son contenu), bouge de quelques pixels et passe devant ou derrière ; ça s'arrête au serrage (96)
    const bt=f<96?Math.floor((f-62)/3):-1, rb=rng(620+bt*17+i*5), jx=bt>=0?(rb()-0.5)*28:0, jy=bt>=0?(rb()-0.5)*20:0, js=bt>=0?1+(rb()-0.5)*0.04:1;
    if(d.firstElementChild){ const zc=bt>=0?1+0.08*((bt+i)%3):1; d.firstElementChild.style.transformOrigin=`${(20+rb()*60).toFixed(0)}% ${(20+rb()*60).toFixed(0)}%`; d.firstElementChild.style.transform=zc>1?`scale(${zc.toFixed(3)})`:''; }
    const s0=(1+0.0012*(f-62))*js, X=lerp(x+w/2+BDR[i][0]*dr+jx,960+cx,pc), Y=lerp(y+h/2+BDR[i][1]*dr+jy,540+cy,pc), S=lerp(s0,cw/w,pc);
    d.style.zIndex=(shuf?((i*3+shuf)%5):bt>=0?((i+bt*2)%5):i)+2;   // +2 : au-dessus du mot « boring. » (z 1)
    mblur(d,f>=96&&f<98?vel(t=>lerp(x+w/2,960+cx,wSnap(t)),f)*BLUR*0.6:0,f>=96&&f<98?vel(t=>lerp(y+h/2,540+cy,wSnap(t)),f)*BLUR*0.6:0);
    d.style.transform=`translate(${(X-w*S/2).toFixed(1)}px,${(Y-h*S/2).toFixed(1)}px) scale(${S.toFixed(4)})`;
    d.style.boxShadow=pc>0?`0 ${(20*pc).toFixed(0)}px ${(50*pc).toFixed(0)}px -20px rgba(40,30,30,${(.35*pc).toFixed(2)})`:''; d.style.borderRadius=(10*pc)+'px';
    d.style.filter=(wTint(f,i)+bl).trim(); wPink(d,f); });
  // les six autres naissent DANS la pile (97-98) : 40 px de décalage qui se résorbe, ×0,92 → 1, fondu de 2 images, un peu désaturés
  wX.forEach((d,i)=>{ const st=97+(i%2); if(f<st){ show(d,false); return; } show(d,true); const [cx,cy,cw]=BXC[i].slice(0,3).map(v=>v*W_PK), [,,,rot,ox,oy]=BXC[i]; const p=clamp((f-st+1)/2);
    const X=960+cx+ox*40*(1-p), Y=540+cy+oy*40*(1-p), S=cw/d._w*lerp(0.92,1,p); d.style.zIndex=10+((i+shuf)%6); d.style.opacity=p.toFixed(3);
    d.style.transform=`translate(${(X-d._w*S/2).toFixed(1)}px,${(Y-d._h*S/2).toFixed(1)}px) rotate(${rot}deg) scale(${S.toFixed(4)})`; d.style.borderRadius='10px'; d.style.boxShadow='0 20px 50px -20px rgba(40,30,30,.35)';
    mblur(d,0,0); d.style.filter=((f>=114+i*0.5&&f<118?'url(#thIri)':'')+bl).trim(); wPink(d,f); });   // les beaux sites gardent leur couleur : le contraste avec la carte bleue
  // la carte du fondateur : monte du bas à 88, se pose au centre, sur le dessus ; le curseur « You » se pose sur « Get Started » (il ne clique pas)
  const foOn=f>=96; show(wFo,foOn);
  if(foOn){ // elle tombe sur la pile en même temps que le serrage (70 % à 96, posée à 97), au centre, au-dessus de tout
    const foY=t=>t<96?840:t<97?lerp(840,548,0.3*(t-95)):548;   // comme les autres : à peine engagée à 96, posée à 97
    const S=((f<97?1.04:1)+0.02*clamp((f-100)/12))*W_PK, X=960, Y=foY(f);
    wFo.style.zIndex=40; wFo.style.transform=`translate(${(X-280*S).toFixed(1)}px,${(Y-175*S).toFixed(1)}px) scale(${S.toFixed(4)})`;
    wFo.style.boxShadow='0 30px 60px -24px rgba(40,30,30,.45)'; mblur(wFo,0,f<98?vel(foY,f)*BLUR*0.5:0);
    wFo.style.filter=bl.trim(); wPink(wFo,f);
    const cp=clamp((twos(f,97)-97)/7), tg=wMap([X+238*S,Y-175*S+40*S],f); if(f>=97&&f<113) cursor(lerp(1330,tg[0],cp),lerp(820,tg[1],cp),0,true,1,cp>=1?'hand':'arrow'); }
  wFoMorph(f);
  gather(f);
}
// l'après de la carte du fondateur : la même refonte que chez les clients (js/dash2.js), à l'échelle de la carte (560 / 1360)
const WFO_K=560/1360, wFoIn=el(wFo,'','', `position:absolute;left:0;top:0;width:1360px;height:850px;transform:scale(${WFO_K});transform-origin:0 0;pointer-events:none`);
const wFoD2=buildDash2(wFoIn,850), wFoA=[...wFo.firstElementChild.children];
// les blocs de la v1 de la carte, en coordonnées de la v2
const WFO_A=Object.fromEntries(Object.entries({flood:[0,0,118,350],title:[138,20,250,26],sub:[138,48,200,14],btn:[444,18,100,28],kpi0:[138,76,124,66],kpi1:[274,76,124,66],kpi2:[410,76,124,66],list:[138,156,250,176],hero:[402,156,142,176]}).map(([k,r])=>[k,r.map(v=>v/WFO_K)]));
const WFO_AEL={flood:wFoA[0],title:wFoA[1],sub:wFoA[2],btn:wFoA[3],kpi0:wFoA[4],kpi1:wFoA[5],kpi2:wFoA[6],list:wFoA[7],hero:wFoA[8]};
function wFoMorph(f){ dash2Morph(wFoD2,f,104,WFO_A,WFO_AEL,WFO_K); }
// le regroupement (réf, largeurs mesurées image par image) : toute la pile se contracte vers le centre en accélérant,
// ×0,28 de 113 à 120 (−27 %/image à la fin), avec un flou qui monte ; le disque du logo prend la suite au même rythme (121)
const W_Z=[1,.85,.80,.74,.64,.55,.40,.284], wZ=f=>f<=113?1:f>=120?W_Z[7]:lerp(W_Z[Math.floor(f-113)],W_Z[Math.floor(f-113)+1],(f-113)%1);
// le serrage : 12 % du chemin à 95 (les cartes rampent), 30 % à 96, posé à 97 (le temps fort)
function wSnap(f){ return f<89?0:f<95?0.12*Math.pow((f-89)/6,1.6):f<96?lerp(0.12,0.3,f-95):f<97?lerp(0.3,1,f-96):1; }   // réf : à 96 les cartes ont à peine bougé, à 97 la pile est faite
// la caméra de la pile : après le serrage elle continue de se resserrer (−1,4 %/image) en dérivant, puis la contraction finale
const W_PK=1.35, wAmk=f=>f<113?1:lerp(1,1/W_PK,clamp((f-113)/7));
function wCam(f){ const n=clamp(f,97,113)-97; return {z:Math.pow(0.986,n)*wZ(f)*wAmk(f),dx:4*n,dy:-3*n}; }
function wMap(p,f){ const m=wCam(f); return [960+(p[0]-960+m.dx)*m.z,540+(p[1]-540+m.dy)*m.z]; }
function gather(f){ if(f<97){ wCol.style.transform=''; return; } const m=wCam(f); wCol.style.transformOrigin='960px 540px';
  wCol.style.transform=`scale(${m.z.toFixed(4)}) translate(${m.dx.toFixed(1)}px,${m.dy.toFixed(1)}px)`; }
// le disque du logo naît à la taille de la pile contractée
const LG_IN=232;

/* ---------- 4 · le trait devient la marque : disque rouge derrière la barre, fantôme du geste, puis « vladan » ---------- */
const L1=scene('sLogo',120,173,f=>shotLogo(f));
const lgGhost=inkLayer(L1.s,{ground:'dark'}); lgGhost.style.mixBlendMode='multiply';
const lgBlob=el(L1.cam,'abs','', 'overflow:hidden;border-radius:50%'); const lgG3=el(lgBlob,'full','', 'background:#FF3D5E');
const lgSlash=el(lgBlob,'full','<svg viewBox="0 0 96 96" width="100%" height="100%"><path d="M36 66 L60 30" stroke="#EEE9E4" stroke-width="9" stroke-linecap="round"/></svg>');
const lgInk=inkLayer(L1.s);
const lgWord=el(L1.cam,'abs','vladan','font-size:84px;font-weight:600;letter-spacing:-0.04em;line-height:1');
let LGW=330; function logoLayout(){ show(lgWord,true); LGW=lgWord.offsetWidth; show(lgWord,false); }
cue(120,'drop',{}); cue(132,'boom',{v:.95}); cue(139,'shimmer',{v:.45,end:147});
function shotLogo(f){ push(L1.cam,f,140,0.0007); const G=f+1;   // G : numéro d'image du film (la scène est décalée d'une image)
  // diamètres de la réf, image par image (243 → 128), puis la marque à 81 à 139 ; le disque glisse à gauche 136-138, le mot arrive entier à 139
  const LS=[243,201,199,196,177,167,159,151,150,149,141,138,133,128,128,128,128,128], S=G>=139?81:LS[clamp(G-121,0,17)]*(1+0.0004*Math.max(0,G-134));
  const ww=LGW, gap=24, tot=81+gap+ww, x=G>=139?960-tot/2+40.5:960-[0,0,0,11,21,42][clamp(G-133,0,5)];
  show(lgBlob,S>0.5); Object.assign(lgBlob.style,{width:S+'px',height:S+'px'}); lgBlob.style.transform=`translate(${(x-S/2).toFixed(1)}px,${(540-S/2).toFixed(1)}px)`;
  inkClear(lgInk);
  { const p=morphT(G,131,3); lgSlash.style.opacity=p.toFixed(3); lgSlash.style.filter=p>0&&p<0.99?`blur(${(3*(1-p)).toFixed(1)}px)`:''; }   // la barre se pose à 132 (les rayures du soleil de la réf)
  // né bleu pâle (le bleu du fondateur qui fond), il passe par le lilas, le rose, le corail et sèche au rouge de la marque (réf 121-134)
  { const C=['#9CCFF8','#B6C6F8','#C9C4F7','#EFC8F3','#FFC2D6','#FFBDC1','#FFAFA8','#FF9C98','#FF8686','#FF6E77','#FF566A','#FF4762','#FF3D5E'], k=clamp(G-121,0,12), c0=C[k], c1=C[Math.min(12,k+1)];
    lgG3.style.background=`linear-gradient(170deg,${c1} 0%,${c0} 70%)`; }
  // le geste d'origine, fantôme graphite à 7 % : main libre → marque nette
  // le fantôme gris de la barre se lisait comme une trace sale : retiré (le calque reste vide)
  inkClear(lgGhost);
  show(lgWord,G>=139); if(G>=139){ placeTL(lgWord,x+40.5+gap,540-42,1+0.07*approach(G,139,16)); lgWord.style.webkitMaskImage=lgWord.style.maskImage='';
    lgWord.innerHTML=`<span style="color:${mixc('#E6A6D8','#151413',clamp((G-139)/3))}">vl</span>adan`; }
  L1.cam.style.translate=`0 ${(-12*accel(f,167,6,2)).toFixed(1)}px`;
}

/* ---------- 5-6 · le brief du fondateur : il survole « Envoyer » sans cliquer ; le stylo biffe « Arial, », la caméra plonge dans l'encre ---------- */
const P1=scene('sPrompt',174,227,f=>shotPrompt(f));
// une revue de design, pas un chat : le site v1 du fondateur en mode commentaire, Léa épingle son brief dessus
const prSite=el(P1.cam,'','', 'position:absolute;left:250px;top:86px;width:1400px;height:880px;border-radius:18px;overflow:hidden;background:#F7F4F0;box-shadow:0 50px 100px -40px rgba(40,30,30,.45)');
prSite.innerHTML=`<div style="position:absolute;left:0;right:0;top:0;height:60px;background:#ECE8E3;box-shadow:0 1px 0 #DDD6CE">
  ${[0,1,2].map(i=>`<span style="position:absolute;left:${22+i*22}px;top:24px;width:12px;height:12px;border-radius:6px;background:#CFC8C0"></span>`).join('')}
  <div class="m" style="position:absolute;left:420px;top:14px;width:560px;height:32px;border-radius:9px;background:#F7F4F0;font-size:14px;line-height:32px;text-align:center;color:#5C5650;white-space:nowrap">velvetly.app · room planner for furniture brands</div>
  <div class="m" style="position:absolute;right:16px;top:12px;height:36px;line-height:36px;padding:0 14px;border-radius:9px;background:#151413;color:#F3EFEA;font-size:14px">● Comment mode</div></div>
  <div class="prD" style="position:absolute;left:20px;top:70px;width:1360px;height:800px;transform-origin:0 0"></div>
  <div style="position:absolute;inset:60px 0 0 0;background:rgba(238,233,228,.66)"></div>`;
q1(prSite,'.prD').style.filter='blur(2.5px)';
const prDash=buildDash(q1(prSite,'.prD'));
// le repère du commentaire, planté sur la photo de poignée de main
const prPin=el(P1.cam,'','', 'position:absolute;left:1494px;top:536px;width:46px;height:46px;border-radius:23px 23px 23px 4px;background:#2D6CDF;color:#fff;font:700 21px/46px AR;text-align:center;box-shadow:0 0 0 3px #fff,0 8px 18px rgba(0,0,0,.25)'); prPin.textContent='L';
const prTh=canvas(P1.s,1920,1080,'left:0;top:0;width:1920px;height:1080px;display:none'); P1.s.insertBefore(prTh,P1.cam);
const prBox=el(P1.cam,'pbox','', 'left:450px;top:396px');
const prCode=el(P1.s,'','', 'position:absolute;inset:0;display:none;pointer-events:none;z-index:31');
function prHeat(f){ const g=clamp((f-214)/13);
  // la landing posée comme à 228 (cachée), sa carte thermique développée depuis un aplat : à 227 c'est l'image exacte de 228
  const was=LA.s.style.display; LA.s.style.display='block'; shotLand(228);
  landThermal(LA.s,laFrame,laSeq,laMark,prTh,{flat:lerp(0.85,LA_FLAT[0],g*g*(3-2*g)),t:f}); LA.s.style.display=was; show(laTh,false); show(laCode,false);
  prTh.style.filter=g<1?`blur(${(16*(1-g)).toFixed(1)}px)`:''; }
el(prBox,'','', 'position:absolute;left:36px;top:30px;width:44px;height:44px;border-radius:22px;background:#2D6CDF;color:#fff;font:700 20px/44px AR;text-align:center').textContent='L';
el(prBox,'','Léa <span class="m" style="font-size:15px;color:#8E877F;margin-left:10px">velvetly · founder · now</span>','position:absolute;left:94px;top:38px;font-size:23px;color:#151413');
const prText=el(prBox,'ptext ar'); const prSend=el(prBox,'psend','<svg viewBox="0 0 72 72" width="72" height="72"><path d="M36 50 V22 M24 33 L36 21 L48 33" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>');
el(prBox,'picon m','@&nbsp;&nbsp;☺&nbsp;&nbsp;⧉','left:40px;bottom:30px;font-size:22px;color:#A39C94;letter-spacing:.02em');
// Léa a déjà mentionné Vladan : la mention « @vladan » s'envolera dans le champ TO de l'e-mail, à la fin
el(prBox,'pmodel pmention','@vladan','right:124px;bottom:34px');
const prInk=inkLayer(P1.cam);   // l'encre vit dans la caméra : elle colle au texte
const PROMPT='Make my SaaS less boring. It’s blue, it’s Arial, and there’s a stock handshake.';
// frappe au rythme de la réf (≈ 1 caractère/image) : 58 caractères à 174, « handshake. » après 5 images de honte (le fondateur efface un caractère et le retape)
const PR_INC=[1,1,1,1,0,1,1,1,0,1,1,1,0, 0,0,-1,0,1, 2,1,2,1,2,2];
const PR_N=(()=>{ const a=[58]; for(const k of PR_INC) a.push(a[a.length-1]+k); return a; })();
for(let i=0;i<PR_INC.length;i++) if(PR_INC[i]) cue(175+i,'key',{v:.2+Math.abs(PR_INC[i])*0.08});
// autour de la carte (443-1476 × 371-675, marge 40 px), jamais sur son texte
const prGly=gset(12,33,860,430,(x,y)=>!(Math.abs(x)<560&&y>-215&&y<170)).map(g=>{ const d=el(P1.cam,'abs c glyph'); d._g=g; return d; });
cue(207,'shimmer',{v:.55,end:215}); cue(212,'rub',{v:.7,peak:226,dur:16}); cue(220,'impact',{v:.35});
let PR_ARIAL=[0,0,0,0], PR_XH=15.6; const PR_BOXH=330;
function prLayout(){ show(P1.s,true); prText.innerHTML=prSeg(PROMPT.length); const sp=prText.querySelector('.ari'), r=sp.getBoundingClientRect(), st=P1.s.getBoundingClientRect(), k=st.width/W;
  PR_ARIAL=[(r.left-st.left)/k,(r.top-st.top)/k,(r.right-st.left)/k,(r.bottom-st.top)/k];
  sp.innerHTML='<span style="font-family:ID;font-weight:500">Inter Display,</span>'; PR_AW=[(r.right-r.left)/k,sp.firstChild.getBoundingClientRect().width/k]; show(P1.s,false); }
let PR_AW=[80,190];
// le brief en segments : « blue » dans le bleu du fondateur, « Arial, » repérable pour le trait
function prSeg(n){ const t=PROMPT.slice(0,n); const iB=PROMPT.indexOf('blue'), iA=PROMPT.indexOf('Arial,');
  const seg=(a,b,cls)=>{ const x=t.slice(a,Math.min(b,n)); return x?(cls?`<span class="${cls}">${x}</span>`:x):''; };
  return seg(0,iB)+seg(iB,iB+4,'blu')+seg(iB+4,iA)+seg(iA,iA+6,'ari')+seg(iA+6,PROMPT.length); }
// la caméra : poussée lente, puis plongée exponentielle ×2,4/image dans le trait (219-227), l'origine glisse sur le centre du trait
// la plongée : ×2,4 par image (220-224), puis elle freine en entrant dans le rouge (×2,2, ×1,8, ×1,45 : le rouge couvre le cadre à 227) au lieu de s'arrêter net
function prCam(f){ const base=1+0.0008*(f-174), ty=-23*approach(f,174,20);
  const C=[(PR_ARIAL[0]+PR_ARIAL[2])/2,(PR_ARIAL[1]+PR_ARIAL[3])/2];
  let k=base, t=[960-960*base,540-540*base+ty];
  if(f>212){ const p=ease3(clamp((f-212)/15)), Z=1+0.55*p; k=base*Z; const sc=[t[0]+C[0]*base,t[1]+C[1]*base], m=0.35*p;
    const Cs=[lerp(sc[0],960,m),lerp(sc[1],540,m)]; t=[Cs[0]-C[0]*k,Cs[1]-C[1]*k]; }
  return {k,t}; }
function shotPrompt(f){
  updateDash(prDash,()=>0,f);   // le site tel qu'il est : la v1 du fondateur
  const {k,t}=prCam(f); P1.cam.style.transformOrigin='0 0'; P1.cam.style.translate=''; P1.cam.style.transform=`translate(${t[0].toFixed(2)}px,${t[1].toFixed(2)}px) scale(${k.toFixed(5)})`;
  const n=Math.min(PROMPT.length,PR_N[clamp(f-174,0,PR_N.length-1)]); const done=n>=PROMPT.length;
  // caret plein pendant la frappe (et la pause), puis clignotement 8 images allumé / 8 éteint
  const blink=!done||Math.floor(f/8)%2==0;
  prText.innerHTML=prSeg(n)+(blink&&f<207?'<span class="pcaret"></span>':'');
  // le curseur du fondateur : linéaire, sur deux images, jusqu'au bouton ; il devient une main et reste en survol. Pas de clic.
  // la main survole Envoyer sans rien presser : le bouton ne change pas (sinon on lit un envoi, et la fin dit qu'il n'est jamais parti)
  const hov=f>=204;
  const cp=1-Math.pow(1-clamp((f-199)/5),2);   // ease-out image par image (la réf ne bouge pas sur deux images)
  const sx=450+1020-30-36, sy=396+PR_BOXH-26-36;   // centre du bouton (en bas à droite, comme dans un fil de commentaires)
  const px=lerp(1290,sx-4,cp), py=lerp(640,sy+4,cp), scr=[t[0]+px*k,t[1]+py*k];
  cursor(scr[0],scr[1],0,f>=199,f>219?Math.min(k,60):1,hov?'hand':'arrow');
  prGly.forEach((d,i)=>{ const st=204+i; const on=f>=st&&f<224; show(d,on); if(!on) return; const g=d._g; const drift=1+(f-st)*0.012;
    d.textContent=i%2?['/','|','\\','-'][(Math.floor(f/2)+i)%4]:g[0]; d.style.color=mixc(GBORN,GINK,approach(f,st,6)); place(d,960+g[1]*drift,546+g[2]*drift,back(f,st,4)); });
  // M3 : le trait biffe « Arial, » (207-212) ; au-delà de ×3, le champ d'encre plein cadre prend le relais
  const C3=[(PR_ARIAL[0]+PR_ARIAL[2])/2,(PR_ARIAL[1]+PR_ARIAL[3])/2], ho=clamp((f-213)/6); show(prTh,ho>0&&!!THERMAL); if(ho>0&&THERMAL){ prHeat(f); prTh.style.opacity=ho.toFixed(3); } { const sh=q1(P1.cam,'.sheet'), to=q1(P1.cam,'.tooth'); if(sh) sh.style.opacity=(1-ho).toFixed(3); if(to) to.style.opacity=(0.62*(1-ho)).toFixed(3); }   // la feuille et sa dent (main.js) s'effacent sur la chaleur : sans feuille, la dent en soft-light griserait l'image   // le trait en coordonnées écran
  prBox.style.opacity=(1-0.88*clamp((f-223)/4)).toFixed(3); prSite.style.opacity=(1-clamp((f-213)/6)).toFixed(3);
  const co=clamp((f-221)/4); show(prCode,co>0); if(co>0){ if(!prCode.firstChild) prCode.innerHTML=laCode.innerHTML; prCode.style.opacity=(0.42*co).toFixed(3); prCode.style.transform=`translateY(${(-(f-221)*4).toFixed(1)}px)`; }
  inkClear(prInk);
  if(f>=207){ const a=q1(prText,'.ari'); if(a){ const p=morphT(f,207,7);
    a.innerHTML='<span style="visibility:hidden">Arial,</span><span>Arial,</span><span style="font-family:ID;font-weight:500">Inter Display,</span>';
    Object.assign(a.style,{display:'inline-block',position:'relative',whiteSpace:'nowrap',width:lerp(PR_AW[0],PR_AW[1],p).toFixed(1)+'px'});
    const [,o,nn]=a.children; o.style.cssText='position:absolute;left:0;top:0'; Object.assign(nn.style,{position:'absolute',left:'0',top:'0'});
    morphOut(o,p,5); morphIn(nn,p,5,0.96); nn.style.color=morphInk(f,207,7,10); } }
}

/* ---------- 7 · la landing velvetly (vidéo Cycles), recul qui ralentit, accélération dans la coupe, « › Taste Files » ---------- */
const LA=scene('sLand',228,299,f=>shotLand(f)); sky(LA.cam);
const laFrame=el(LA.cam); const laD=framed(laFrame,tplVLanding(),1440,900,1240,730,VINK);
const laLabel=el(LA.cam,'abs','<span style="font-family:JB;margin-right:22px">›</span>Taste Files','font-size:84px;font-weight:400;color:#3A3633;letter-spacing:-0.01em');
const laSeq=q1(laD,'.vseq'), laXr=q1(laD,'.vxr'), laPills=qa(laD,'.vpill'), laIx=qa(laD,'.vix');
const PH_COL=['#3A3633','#4A4542','#2E2B28'];   // squelettes de chargement (gris), pas de couleurs
// l'icône du carré se dessine 234-238
qa(laD,'.vmk svg path').forEach(p=>{ p.setAttribute('pathLength','1'); p.style.strokeDasharray='1'; });
const laMark=q1(laD,'.vmk');
cue(234,'impact',{v:.5}); cue(244,'tick',{v:.25}); cue(256,'tick',{v:.25}); cue(259,'swish',{v:.25,peak:262,dur:6}); cue(276,'whoosh',{v:.5,peak:281,dur:6}); cue(281,'tick',{v:.45}); cue(294,'shimmer',{v:.35,end:300});
// la loupe X-ray : elle s'ouvre sur la lampe et le pouf (246, rayon 0 → 110 en 6 images), longe le canapé et finit sur le fauteuil,
// qui seul garde son velours
function laLensAt(f){ const t=ease3(clamp((f-246)/42)); return [lerp(420,1095,t),lerp(330,330,t)]; }
// 228-235 : l'aplat d'encre se développe en image thermique de la landing (le rouge du stylo est le 0,70 de la palette),
// qui recule en accélérant comme la carte thermique de la réf, puis refroidit vers la photo ; le carré de la marque reste chaud le dernier
const laTh=document.createElement('canvas'); laTh.width=1920; laTh.height=1080; laTh.style.cssText='position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:30;display:none;pointer-events:none'; LA.s.appendChild(laTh);
const LA_FLAT=[.25,.1,0,0];
// l'image thermique d'une landing à l'écran (sa carte, sa photo, sa bande papier, sa marque chaude), dans le canvas dest
function landThermal(stage,frame,seq,mark,dest,o){ const st=stage.getBoundingClientRect(), k=st.width/W, R=e=>{ const r=e.getBoundingClientRect(); return [(r.left-st.left)/k/2,(r.top-st.top)/k/2,(r.right-r.left)/k/2,(r.bottom-r.top)/k/2]; };
  const x=THERMAL.srcCtx; x.fillStyle='#2A2624'; x.fillRect(0,0,960,540);
  const fr=R(frame), ph=R(seq); x.fillStyle='#151413'; x.fillRect(...fr); x.drawImage(seq,...ph); x.fillStyle='#EEE9E4'; x.fillRect(ph[0],ph[1]+ph[3],ph[2],ph[3]*170/560);
  const m=R(mark); THERMAL.draw(null,Object.assign({spots:[[(m[0]+m[2]/2)/960,(m[1]+m[3]/2)/540,0.045,0.5]],wimg:1,lo:0.12,hi:0.9,gam:1.1,blur:5},o));
  dest.getContext('2d').drawImage(THERMAL.canvas,0,0,1920,1080); }
// réf 222-235 : du code flotte sur l'image thermique ; ici les lignes de taste.ts, à l'encre en valeur moyenne (contexte, pas héros)
const LA_CODE=[[118,92,'export const taste = {'],[1396,70,'taste.font'],[262,318,'font: "Inter Display",'],[150,574,'=> ●'],[1482,430,'accent: "#FF3D5E",'],
  [1170,712,'ease: "out",'],[300,912,'arial: false,'],[1352,968,'stockPhotos: 0 }']];
const laCode=el(LA.s,'','', 'position:absolute;inset:0;display:none;pointer-events:none;z-index:31');
laCode.innerHTML=LA_CODE.map(([x,y,t])=>`<div class="m" style="position:absolute;left:${x}px;top:${y}px;font-size:22px;color:#151413;white-space:pre">${t}</div>`).join('');
function laThermal(f){ const on=THERMAL&&f>=228&&f<236; show(laTh,on); show(laCode,false); if(!on) return;
  show(laCode,true); laCode.style.opacity=(0.42*(1-clamp((f-231)/4))).toFixed(3); laCode.style.transform=`translateY(${(-(f-221)*4).toFixed(1)}px)`;
  landThermal(LA.s,laFrame,laSeq,laMark,laTh,{flat:LA_FLAT[Math.min(f-228,3)],t:f});
  // 232-235 : la chaleur sèche par un balayage dans le sens du trait (gauche → droite, bord doux de 30 %), pas un voile
  const w=f<232?-40:lerp(-30,110,(f-231.5)/4); laTh.style.webkitMaskImage=laTh.style.maskImage=f<232?'':`linear-gradient(100deg,transparent ${w.toFixed(1)}%,#000 ${(w+30).toFixed(1)}%)`; }
function shotLand(f){
  const fl=Math.max(f,234);
  // réf : recul qui ralentit (235-273), accélération dans la coupe (274-280), puis petit écran qui se pose (281+)
  let sc,x=960,y=540;
  // la landing apparaît déjà en mouvement : recul dès 231, pendant le fondu (≈ −3,5 %/image, comme la réf), au lieu de tenir jusqu'à 235
  // 228-230 : la carte thermique recule (−6,5 %/image) ; puis la landing continue de reculer en ralentissant
  if(f<231) sc=[1.5,1.42,1.36][clamp(f-228,0,2)]; else if(f<274) sc=lerp(1.3,0.94,approach(f,231,43,0.09));
  else if(f<281){ const a=accel(f,274,6.6,2.6); sc=lerp(0.94,0.80,a); x=960+40*a; }   // sortie à la vitesse de la réf (−3 / −4,3 %/image), nette
  else { const p=approach(f,281,14,0.25); sc=lerp(0.683,0.632,p); x=1588-720*sc+lerp(16,0,p); y=548; }
  const gone=f>=294?approach(f,294,5):0;
  if(!laD._iri) laD._iri=el(laD,'','', 'position:absolute;inset:0;z-index:60;pointer-events:none;mix-blend-mode:screen;display:none;background:linear-gradient(115deg,#CDB9F2 0%,#BFE7F3 34%,#FFC9A8 68%,#F3B9D0 100%)');
  { const ir=vl(f,293,4); laD._iri.style.display=ir>0?'block':'none'; laD._iri.style.opacity=(0.75*ir).toFixed(3); }
  place(laFrame,x,y,sc); laFrame.style.filter=gone>0?`blur(${(8*gone).toFixed(1)}px) brightness(${(1+0.2*gone).toFixed(2)})`:''; laFrame.style.opacity=(1-0.85*clamp((f-297)/3)).toFixed(3);
  mblur(LA.cam,f>=276&&f<281?0.5*vel(t=>40*accel(t,274,6.6,2.6),f):0,0);
  seqDraw(laSeq,SEQ.land,fl-234);
  // Ken Burns dans la carte ; le titre ne glisse plus (il tient exactement entre les marges, à cheval sur le bord de la photo)
  const kb=0.5-0.5*Math.cos(Math.PI*clamp((f-238)/52)), ktr=`translateX(${(-40*kb).toFixed(1)}px) scale(${(1+0.08*kb).toFixed(4)})`; laSeq.style.transformOrigin='50% 55%'; laSeq.style.transform=ktr;
  if(f>=246){ seqDraw(laXr,SEQ.landX,fl-234); const [lx,ly]=laLensAt(f); landLens(laD,110*vl(f,246,6),lx,ly,ktr); } else landLens(laD,0,700,300,ktr);
  qa(laD,'.vmk svg path').forEach(p=>p.style.strokeDashoffset=(1-vl(f,234,4)).toFixed(3));
  if(INK&&INK.canvas.parentNode===LA.s) show(INK.canvas,false);
  laThermal(f);
  // boutons d'abord en blocs de couleur qui changent toutes les 4 images, puis le logo (244) et les boutons (256)
  // (les couleurs d'origine sont gardées : remettre style.color à '' effaçait le texte clair de « Book a demo »)
  laPills.forEach((pl,i)=>{ const ready=f>=(i==0?244:256); if(pl._c===undefined){ pl._c=pl.style.color; pl._b=pl.style.background; }
    pl.style.color=ready?pl._c:'transparent'; pl.style.background=ready?pl._b:PH_COL[(Math.floor((fl-234)/4)+i)%3];
    pl.querySelectorAll('span').forEach(sp=>sp.style.visibility=ready?'visible':'hidden'); });
  q1(laD,'.vstat').style.visibility=f>=242?'visible':'hidden';
  // l'index monte derrière un masque, une colonne toutes les 2 images (248-258)
  laIx.forEach((c,i)=>{ const p=vl(f,248+2*i,6); c.style.clipPath=`inset(0 0 ${((1-p)*100).toFixed(1)}% 0)`; c.style.translate=`0 ${(14*(1-p)).toFixed(1)}px`; });
  show(laLabel,f>=281); if(f>=281) placeTL(laLabel,150,300-10*approach(f,281,12));
}

/* ---------- 8 · l'arborescence « Taste Files » : défilement par paliers, couleurs qui passent cyan → lilas → pêche → gris ---------- */
const TR=scene('sTree',300,347,f=>shotTree(f));
const TREE=[[300,'▾ Taste Files',150,0,'title'],[305,'Brand.ts',380,1,'file'],[308,'Typography.ts',380,2,'file'],[312,'Components',380,3,'dir'],
  [317,'NoMoreArial.tsx',610,4,'file'],[320,'OneAccent.tsx',610,5,'file'],[322,'EaseOut.tsx',610,6,'file'],[329,'Taste.tsx',610,7,'last']];
// chaque nom arrive en faisant ce qu'il dit : NoMoreArial change de police lettre à lettre, OneAccent sèche à l'encre,
// EaseOut arrive sur la courbe vladan (+ son tracé) ; les autres se posent à l'encre
const glyphs=t=>[...t].map(c=>`<span class="g">${c}</span>`).join('');
// une vraie icône de document (coin plié, masque CSS à la couleur du nom ; un SVG en ligne dupliquait l'arbre dans Chromium) ;
// les carrés vides se lisaient comme des glyphes manquants
const TR_DOC=`<span class="fi"></span>`;
// la hiérarchie de la réf : chaque nom naît en couleur (bleu pâle → rose) et sèche à l'encre ; dès que le suivant arrive,
// il passe au gris : l'œil suit toujours le dernier
function trColor(i,f){ const d=trEls[i], a=f-d._f, nf=i+1<TREE.length?TREE[i+1][0]:1e9, m=(p,q,t)=>p.map((v,k)=>lerp(v,q[k],t));
  const c=a<2?m(hex('#9CC9F5'),hex('#F2A7C3'),clamp(a/2)):m(hex('#F2A7C3'),hex('#151413'),clamp((a-2)/4)), o=m(c,hex('#B8B0A8'),clamp((f-nf)/6));
  return `rgb(${o.map(Math.round).join(',')})`; }
const trEls=TREE.map(([f0,t,x,row,kind])=>{ const d=el(TR.cam,'titem'); d._k=kind; d._x=x; d._row=row; d._f=f0; d._t=t;
  d.innerHTML=kind==='title'?`<span style="font-family:JB;margin-right:16px">▾</span>Taste Files`:kind==='dir'?`<span class="chev" style="font-family:JB;display:inline-block;margin-right:16px">›</span>${t}`
    :kind==='last'?`${TR_DOC}<em style="font-size:72px">Taste</em>.tsx`:`${TR_DOC}${/NoMoreArial|EaseOut/.test(t)?glyphs(t):t}`;
  Object.assign(d.style,{fontSize:kind==='title'?'84px':'72px',color:'#151413'}); if(kind==='title') d.style.color='#3A3633'; return d; });
const trEase=el(TR.cam,'abs','', 'display:flex;align-items:center;gap:18px'); 
trEase.innerHTML=`<svg width="120" height="44" viewBox="0 0 120 44"><path d="M2 42 ${Array.from({length:41},(_,i)=>`L${(2+i*2.9).toFixed(1)} ${(42-40*vladan(i/40)).toFixed(1)}`).join(' ')}" fill="none" stroke="#151413" stroke-width="1.75" stroke-linecap="round"/></svg><span class="m" style="font-size:22px;color:#151413">ease: vladan</span>`;
const trLines=[[360,1,3],[590,4,7]]   // le guide descend jusqu'à Taste.tsx, frère d'EaseOut au même pas de 100 px
.map(([x,a,b])=>{ const l=el(TR.cam,'tline'); l._x=x; l._a=a; l._b=b; return l; });
TREE.forEach(([f0],i)=>cue(f0,i==TREE.length-1?'pluck':'tick',{v:i==TREE.length-1?.5:.3,n:79}));
const TR_STEPS=[[305,232],[312,219],[317,175],[322,149],[329,107]];
// paliers en entrée-sortie douce (la réf monte en 2-4 images, approach() partait à vitesse maximale)
function trY(f){ let y=313; for(const [s,t] of TR_STEPS) y=lerp(y,t,ease3(clamp((f-s)/(s==329?9:6)))); return y; }
function shotTree(f){
  // pas de push continu : on tient, puis recul + léger roulis avant la coupe (340-346)
  // le recul de la landing se prolonge à travers la coupe (−1 %, −0,5 %/image), puis on tient
  const pb=accel(f,339,7,2.2), inh=1.015-0.015*approach(f,300,6,0.3); TR.cam.style.transform=`scale(${(inh*(1-0.025*pb)).toFixed(4)}) rotate(${(1.2*pb).toFixed(3)}deg)`;
  const ty=trY(f), LH=100;
  trEls.forEach(d=>{ const on=f>=d._f; show(d,on); if(!on) return;
    placeTL(d,d._x,ty+d._row*LH+(d._row?14:0));
    const a=f-d._f;
    if(/NoMoreArial/.test(d._t)) qa(d,'.g').forEach((g,i)=>{ g.style.fontFamily=a>=4+i?'ID':'AR'; });
    if(d._k!=='title') d.style.color=trColor(trEls.indexOf(d),f);
    if(/EaseOut/.test(d._t)) qa(d,'.g').forEach((g,i)=>{ const dx=[18,10,5,2,1,0][Math.min(5,Math.max(0,a-i))]; g.style.display='inline-block'; g.style.transform=`translateX(${dx}px)`; g.style.opacity=a>=i?1:0; });
    if(d._k==='dir'){ const ch=q1(d,'.chev'); ch.style.transform=`rotate(${(90*approach(f,317,4)).toFixed(1)}deg)`; } });
  const eo=trEls[6]; show(trEase,f>=325); if(f>=325){ placeTL(trEase,eo._x+eo.offsetWidth+40,ty+6*LH+14+14); trEase.style.opacity=vl(f,325,4).toFixed(3); }
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
  DA.cam.style.transform=`scale(${(1+0.046*accel(f,374,5,3.2)).toFixed(4)})`;   // finit sur la dernière image du plan (pas d'image figée avant la coupe)
}

/* ---------- 10 · le salon en vol plongeant (séquence Cycles) : tracé, point et plan au sol accrochés à l'image ---------- */
const cR10=cueAt(1);
const HE=scene('sHero',381,419,f=>shotHero(f));
const heSeq=canvas(HE.cam,1280,720,'left:0;top:0;width:1920px;height:1080px;filter:brightness(1.14) contrast(1.04)');
const heSvg=el(HE.cam,'',`<svg width="1920" height="1080" viewBox="0 0 1920 1080"><g class="hplan" fill="none" stroke="#F3EFEA" stroke-width="1.5"></g><g class="htick" stroke="#F3EFEA" stroke-width="1.5" fill="none"></g>
  <path class="hers" fill="none" stroke="rgba(21,20,19,.35)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" style="filter:blur(8px)"/><path class="her" fill="none" stroke="#151413" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle class="hp1" r="14" fill="none" stroke="#F3EFEA" stroke-width="2"/><circle class="hp2" r="14" fill="none" stroke="#F3EFEA" stroke-width="2"/>
  <text class="hlab" font-family="JB" font-size="15" fill="#F3EFEA">83 × 57 cm</text></svg>`,'position:absolute;left:0;top:0');
const hePlan=q1(heSvg,'.hplan'), heRoute=q1(heSvg,'.her'), heRouteS=q1(heSvg,'.hers'), heTick=q1(heSvg,'.htick'), heLab=q1(heSvg,'.hlab'), heP=[q1(heSvg,'.hp1'),q1(heSvg,'.hp2')];
const HE_SH=['rug','sofa','pouf','table','plant','chair'];
const heShapes=HE_SH.map(()=>{ const p=document.createElementNS('http://www.w3.org/2000/svg','path'); hePlan.appendChild(p); return p; });
el(HE.cam,'','', 'position:absolute;left:-100px;right:-100px;top:-60px;height:390px;backdrop-filter:blur(12px);-webkit-mask-image:linear-gradient(#000 40%,transparent);mask-image:linear-gradient(#000 40%,transparent)');
el(HE.cam,'','', 'position:absolute;left:-100px;right:-100px;bottom:-60px;height:330px;backdrop-filter:blur(12px);-webkit-mask-image:linear-gradient(transparent,#000 60%);mask-image:linear-gradient(transparent,#000 60%)');
const heDot=el(HE.cam,'vdot','', 'width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:15px;box-shadow:0 0 0 7px #fff,0 6px 18px rgba(0,0,0,.3)');
cR10(380,'impact',{v:.6}); cR10(384,'shimmer',{v:.3,end:400});
const pth=pts=>'M'+pts.map(([x,y])=>`${(x*1920).toFixed(1)} ${(y*1080).toFixed(1)}`).join(' L');
function shotHero(F){ const f=F-1, i=clamp(f-380,0,38);
  // la réf pousse en entrant (+1,6 %, +3,3 %/image), même sens que la poussée du plan d'avant ; puis une caméra 2D par-dessus le vol
  // du drone (−5 px, +0,6 %/image) : le rendu seul volait 2,5× moins vite que la réf
  HE.cam.style.transform=`translateX(${(-5*(f-380)).toFixed(1)}px) scale(${((1+0.08*approach(f,380,6,0.3))*(1+0.006*(f-380))).toFixed(4)})`;
  seqDraw(heSeq,SEQ.aerial,i);
  const P=AERIAL[seqIdx(SEQ.aerial,i)]; if(!P) return;
  heRoute.setAttribute('d',pth(P.route)); heRouteS.setAttribute('d',pth(P.route));
  let tk='';
  HE_SH.forEach((k,j)=>{ heShapes[j].setAttribute('d',pth(P[k])+' Z'); const o=vl(f,383+j*2,6); heShapes[j].style.opacity=(k==='chair'?0:o).toFixed(3);
    // équerres de 10 px aux coins de la boîte englobante
    if(o>0.5){ const xs=P[k].map(p=>p[0]*1920), ys=P[k].map(p=>p[1]*1080); const a=Math.min(...xs), b=Math.max(...xs), d=Math.max(...ys), c=Math.min(...ys)-(k==='chair'?0.26*(d-Math.min(...ys)):0);
      tk+=`M${a} ${c+10}V${c}H${a+10} M${b-10} ${c}H${b}V${c+10} M${b} ${d-10}V${d}H${b-10} M${a+10} ${d}H${a}V${d-10} `;
      if(k==='chair'){ heLab.setAttribute('x',(b+12).toFixed(0)); heLab.setAttribute('y',(c+16).toFixed(0)); } } });
  heTick.innerHTML=`<path d="${tk}"/>`; heLab.style.opacity=vl(f,394,5).toFixed(3);
  const d=P.route[P.route.length-1]; heDot.style.left=(d[0]*1920)+'px'; heDot.style.top=(d[1]*1080)+'px';
  heP.forEach((c,j)=>{ const ph=((f-381)/14+j*0.5)%1; c.setAttribute('cx',d[0]*1920); c.setAttribute('cy',d[1]*1080); c.setAttribute('r',(14+20*ph).toFixed(1)); c.style.opacity=((1-ph)*0.8).toFixed(3); });
}

/* ---------- 11 · pills « Lemme give it · fauteuil · taste » : couleurs à l'arrivée, resserrage décalé, fonte sur place ---------- */
const cR11=cueAt(2);
const PI=scene('sPills',420,467,f=>shotPills(f));
const piL=el(PI.cam,'pill','Lemme give it'), piR=el(PI.cam,'pill acc','<em>taste</em>'), piI=el(PI.cam,'picn','');
// la fonte : une traînée horizontale (queue transparente, corps orangé, tête rose-lilas), floutée dans le sens du mouvement,
// qui devient la première barre du planning (réf 460-466 : un trait de vitesse, pas une tache ronde)
const piMelt=el(PI.cam,'','', 'position:absolute;left:0;top:480px;height:120px;border-radius:60px;background:linear-gradient(90deg,rgba(255,154,77,0) 0%,rgba(255,154,77,.9) 38%,#FF9A8A 70%,#D9C2F5 100%);display:none');
// ce que vend Vladan, dans la fente de l'icône : marque (Aa), interface (panneaux), mouvement ; puis la fente se remplit d'encre avec la barre de la marque
const PI_ICO=[c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>`,
  c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`,
  c=>`<svg viewBox="0 0 24 24" width="44" height="44" fill="none" stroke="${c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h3l3-8 6 16 3-8h3"/></svg>`,
  c=>`<svg viewBox="0 0 96 96" width="60" height="60"><path d="M36 66 L60 30" stroke="${c}" stroke-width="9" stroke-linecap="round"/></svg>`];
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
  const ic=(f>=427)+(f>=436)+(f>=446); piI.innerHTML=`<div style="position:absolute;inset:0;display:grid;place-items:center">${PI_ICO[ic](filled?'#EEE9E4':'#151413')}</div>`;
  // l'icône est déjà là à 418 (pas d'image vide après la coupe) ; les mots naissent orangés et sèchent à l'encre en 6 images
  place(piI,xi,540,back(f,416.5,4)); piI.style.borderColor='#151413';
  show(piL,f>=424); piL.style.opacity=approach(f,424,3).toFixed(3); place(piL,xl,540); piL.style.color=piL.style.borderColor=mixc('#FF9A4D','#151413',clamp((f-424)/6));
  show(piR,f>=430); place(piR,xr,540,back(f,430,6)); piR.style.color=mixc('#FF9A4D','#151413',clamp((f-430)/6));
  [[piL,xl-L.wl/2],[piI,xi-45],[piR,xr-L.wr/2]].forEach(([e,left])=>{ const k=front-left; e.style.webkitMaskImage=e.style.maskImage=melt?`linear-gradient(90deg,transparent ${k.toFixed(0)}px,#000 ${(k+60).toFixed(0)}px)`:''; });
  show(piMelt,melt); if(melt){ piMelt.style.left=x0+'px'; piMelt.style.width=Math.max(146,front-x0+40)+'px'; mblur(piMelt,22,3); }
}

/* ---------- 12-13 · barres floues → « Delivery & Install Status » → une seule poussée sur les 3 recadrages ---------- */
const cR12=cueAt(2);
const PL=scene('sPlan',468,560,f=>shotPlan(f));
const plRoot=el(PL.cam,'','', 'position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0'); plRoot.innerHTML=tplPlan();
const plMinor=qa(plRoot,'.pminor'), plChips=qa(plRoot,'.pchip'), plDays=qa(plRoot,'.day'), plDn=qa(plRoot,'.dname'), plCols=qa(plRoot,'.col'), plSide=q1(plRoot,'.side'), plTitle=[q1(plRoot,'.ptitle'),q1(plRoot,'.psub')], plX=qa(plRoot,'.plx');
// vague 1 : grosses barres floues (≈140 px), qui poussent vers la droite puis se rattrapent et s'éteignent (réf 466-480)
// barres floues nées dans des teintes du bleu du fondateur, qui sèchent en teintes d'encre (488-500)
const PL_BLUE=['#FFC9A8','#F3B9D0','#FFB27A','#D9C2F5','#FF9A8A','#E6C3B2'], PL_INK=[.06,.10,.16,.08,.12,.10];
// dix barres, deux toutes les deux images ; elles naissent dans le rose-orangé de la coulée des pilules et bleuissent (466-476)
const PL_BARS=Array.from({length:12},(_,i)=>[466+2*Math.floor(i/2),(()=>{ const r=rng(900+i); return 130+r()*820; })()]).map(([st,y],i)=>{ const c=PL_BLUE[i%6]; const r=rng(810+i), hh=70+r()*60; const d=el(PL.cam,'','', `position:absolute;top:${y}px;height:${hh.toFixed(0)}px;border-radius:${(hh/2).toFixed(0)}px;display:none`); d._st=st; d._i=i; d._x=i==0?600:60+r()*1100; d._g=30+r()*70; d._c=100+r()*70; return d; });
plChips.forEach((c,i)=>{ c._st=496+i*1.3; c._x0=parseFloat(c.style.left); c._y0=parseFloat(c.style.top); });
const plInk=inkLayer(plRoot);
// M4 : le S d'inversion relie « Ship » (lundi) et « Taste Check » (vendredi) ; chacun part sur un lobe du S (523-529)
const PL_SHIP=plChips[0], PL_TC=plChips[4];
cR12(515,'glide',{v:.5,end:523}); cR12(523,'tick',{v:.3});
for(let k=0;k<7;k++) cR12(494+k*2.4,'tick',{v:.2}); PL_BARS.forEach(b=>cR12(b._st,'swish',{v:.18,peak:b._st+3,dur:6}));
cR12(532,'impact',{v:.45}); cR12(541,'swish',{v:.35,peak:542,dur:5}); cR12(550,'swish',{v:.35,peak:551,dur:5}); cR12(555,'whoosh',{v:.4,peak:559,dur:5});
const m3=(p,q,t)=>p.map((v,k)=>lerp(v,q[k],t));
function shotPlan(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // zooms 532-558 : UNE poussée qui ralentit à travers les 3 coupes ; la puce grandit à la fin (raccord téléphone)
  let zs=1, zx=960, zy=540; if(f>=532){ const Z=[[532,760,470],[541,1280,560],[550,960,770]]; let z=Z[0]; for(const q of Z) if(f>=q[0]) z=q;
    zs=2.15*(1+0.032*approach(f,532,27,0.09)); zx=z[1]; zy=z[2]; }
  plRoot.style.transform=`translate(${(960-zx*zs).toFixed(1)}px,${(540-zy*zs).toFixed(1)}px) scale(${zs})`;
  // caméra : recul qui ralentit (499-516), puis parfaitement immobile jusqu'à la coupe
  plChips.forEach(c=>c.classList.remove('phero')); if(f>=532){ const sb=PL.s.getBoundingClientRect(), kk=sb.width/W; let best=null, bd=1e9;
    plChips.forEach(c=>{ const r=c.getBoundingClientRect(), d=Math.hypot((r.left+r.width/2-sb.left)/kk-960,(r.top+r.height/2-sb.top)/kk-540); if(d<bd){ bd=d; best=c; } }); if(best) best.classList.add('phero'); }
  PL.cam.style.transform=f<532?`scale(${(1.04-0.04*approach(f,499,17,0.1)).toFixed(4)})`:'';
  plRoot.firstChild.style.background=mixc('#EEE9E4','#F6F2EE',approach(f,490,16));
  // elles vivent 26 images (fondu à partir de 16) et dérivent ensemble de 10 px/image : l'écran n'est jamais vide avant le calendrier
  PL_BARS.forEach(b=>{ const a=f-b._st; const on=a>=0&&a<26&&f<532; show(b,on); if(!on) return; const grow=Math.min(a,5)*b._g, j=b._i%6;
    // une traînée : queue transparente, corps, tête plus claire ; née rose-orangé, bleuit, puis sèche à l'encre ; flou de vitesse horizontal
    const dr=vladan(clamp((f-488)/12)), cb=hex(PL_BLUE[j]), c0=m3(m3(hex('#FF9A8A'),hex('#C9A6F2'),(b._i%3)/2),cb,clamp((f-466)/10)), c=m3(c0,[21,20,19],dr), al=lerp(1,PL_INK[j]*4,dr);
    const C=(k,a)=>`rgba(${k.map(Math.round).join(',')},${a.toFixed(3)})`;
    b.style.background=`linear-gradient(90deg,${C(c,0)} 0%,${C(c,al*0.85)} 45%,${C(m3(c,[255,255,255],0.35),al)} 100%)`;
    b.style.left=(b._x+10*(f-466))+'px'; b.style.width=(180+grow)+'px'; b.style.opacity=(1-clamp((a-16)/10)).toFixed(3); mblur(b,34,7); });
  plChips.forEach((c,i)=>{ const blob=f>=486+(i%6)*1.4, sharp=approach(f,c._st,3,0.3);
    c.style.visibility=blob?'visible':'hidden'; c.style.transform=f>=555&&i==3?`scaleY(${(1+0.4*accel(f,555,4,2)).toFixed(3)})`:''; if(i==3) c.style.transformOrigin='50% 0';
    c.style.filter=sharp<1?`blur(${(14*(1-sharp)).toFixed(1)}px) saturate(${(1+2.2*(1-sharp)).toFixed(2)})`:''; [...c.children].forEach(e=>e.style.opacity=sharp.toFixed(2)); });
  // les tâches secondaires arrivent après les principales, déjà en retrait
  plMinor.forEach((c,i)=>{ const p=approach(f,508+i*1.5,6,0.25); c.style.opacity=p.toFixed(3); c.style.visibility=p>0?'visible':'hidden'; });
  // l'inversion : « Taste Check » prend le lobe du haut vers lundi, « Ship » le lobe du bas vers vendredi ; l'encre de chaque lobe se rétracte derrière sa puce
  const sw=vl(f,515,8); const sx=PL_TC._x0-PL_SHIP._x0, sy=PL_TC._y0-PL_SHIP._y0;
  [[PL_TC,-1,-140],[PL_SHIP,1,140]].forEach(([c,dir,bow])=>{ const u=sw; const dx=-dir*sx*u*-1, dy=dir*sy*u*-1;
    const ox=dir>0?sx*u:-sx*u, oy=(dir>0?sy:-sy)*u+bow*Math.sin(Math.PI*u)*(dir>0?1:-1)*0.5; c.style.translate=`${ox.toFixed(1)}px ${oy.toFixed(1)}px`; c.style.zIndex=u>0?5:''; });
  PL_SHIP.classList.toggle('fd',f<515);   // une fois corrigée, « Ship » n'est plus au fondateur : plus de contour
  inkClear(plInk);
  // le morph : pendant l'échange, les deux tâches sont lilas, puis elles sèchent vers leur teinte (523-533)
  [[PL_TC,4],[PL_SHIP,0]].forEach(([c,i])=>{ if(f<515||f>=534||c.classList.contains('phero')){ c.style.background=''; return; } c.style.background=mixc(MORPH.fill,PLAN_TINT[i][0],clamp((f-521)/12)); });
  // le week-end sèche directement vers son gris (il ne passe plus par l'encre avant de sauter au gris)
  plDays.forEach((d,i)=>{ const st=494+i*2.4, fin=i>=5?'#B3ABA4':'#151413'; d.style.visibility=f>=st?'visible':'hidden'; d.style.color=f<st+4?mixc('#C6D8F7',fin,clamp((f-st)/4)):fin; });
  plDn.forEach((d,i)=>{ d.style.visibility=f>=497+i*2.4?'visible':'hidden'; });
  plCols.forEach((c,i)=>{ c.style.transformOrigin='0 0'; c.style.transform=`scaleY(${approach(f,488+i,10).toFixed(3)})`; });
  show(plSide,f>=496); plSide.style.background=mixc('#E4DED7','#151413',approach(f,496,14,0.15));   // la barre latérale monte du papier à l'encre
  [...plSide.children].forEach(e=>{ e.style.opacity=approach(f,505,6).toFixed(2); });
  plTitle.forEach((t,i)=>{ t.style.visibility=f>=506+i*2?'visible':'hidden'; if(i==0) t.style.color=mixc('#C5C0BB','#3A3633',approach(f,506,10)); });
  plX.forEach((t,i)=>{ t.style.visibility=f>=508+i?'visible':'hidden'; });
}

/* ---------- 14 · téléphone : se déplie en hauteur, écran irisé balayé par le bas, vidéo en grue, rubans plein cadre ---------- */
const cR14=cueAt(2);
const PH=scene('sPhone',561,641,f=>shotPhone(f));
// le téléphone : anneau de métal, île, boutons, reflet du verre qui glisse, ombre de contact ; l'app velvetly AR démarre comme une caméra
// les rubans de soie nacrée passent derrière le téléphone (575-627), clairs et peu saturés : le fond reste en retrait
const phRib=canvas(PH.cam,960,540,'left:0;top:0;width:1920px;height:1080px;display:none');
const phShadow=el(PH.cam,'','', 'position:absolute;left:820px;top:952px;width:280px;height:18px;border-radius:50%;background:radial-gradient(closest-side,rgba(40,30,30,.45),rgba(40,30,30,0))');
const phone=el(PH.cam,'phone'); el(phone,'ring'); [[-6,210,60],[-6,290,60],[408,250,96]].forEach(([x,y,h])=>el(phone,'pbtn','', `left:${x}px;top:${y}px;height:${h}px`));
const phScr=el(phone,'scr');
const phSeq=canvas(phScr,612,1260,'left:0;top:0;width:384px;height:816px');
el(phScr,'','', 'position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 48%,rgba(10,9,8,.86) 78%)');
// l'écran naît holographique et sèche vers l'image de la caméra (réf 559-571)
const phHolo=el(phScr,'','', 'position:absolute;inset:0;background:linear-gradient(150deg,#BFE6F4 0%,#E6CBF3 34%,#FFD6BC 62%,#C9F0E4 100%);pointer-events:none');
el(phScr,'island');
el(phScr,'glass',`${VMARK(18)}<span style="margin-left:8px">velvetly AR</span>`,'position:absolute;left:22px;top:58px;height:38px;line-height:38px;padding:0 14px;border-radius:12px;color:#fff;font-size:15px;display:flex;align-items:center');
el(phScr,'abs','Living room','left:24px;top:108px;font-size:46px;color:#fff;letter-spacing:-0.04em');
const phStats=[el(phScr,'abs m','▪ ROOM FIT','left:26px;top:478px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)')];
const phNum=el(phScr,'abs','92%','left:22px;top:498px;font-size:104px;color:#fff;letter-spacing:-0.05em;line-height:1');
phStats.push(phNum, el(phScr,'abs m','▪ TIME TO FIRST ROOM','left:26px;top:612px;font-size:12px;letter-spacing:.08em;color:rgba(255,255,255,.7)'));
const phTime=el(phScr,'abs','2:59','left:22px;top:632px;font-size:58px;color:#fff;letter-spacing:-0.04em;line-height:1');
phStats.push(phTime, el(phScr,'abs m','chair 0.83 m · sofa 2.19 m','left:26px;top:700px;font-size:12px;color:rgba(255,255,255,.55)'));
el(phScr,'','Share this room →','position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#151413;box-shadow:inset 0 0 0 1px rgba(243,239,234,.2);color:#F3EFEA;font-size:20px;line-height:62px;padding-left:22px');
const phSheen=el(phScr,'','', 'position:absolute;left:-120px;top:-40px;width:160px;height:900px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.10),rgba(255,255,255,0));transform:rotate(18deg)');
const phDone=el(phScr,'','', 'position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,rgba(18,17,16,0),#121110 26%)');
phDone.innerHTML=`<div style="position:absolute;left:24px;top:96px;width:44px;height:44px;border-radius:12px;background:#F3EFEA;color:#151413;font-size:26px;line-height:44px;text-align:center">✓</div>
  <div style="position:absolute;left:24px;top:156px;font-size:54px;color:#fff;letter-spacing:-0.045em;line-height:.98">Fits<br>perfectly</div>
  <div class="m" style="position:absolute;left:26px;top:280px;font-size:12px;color:#8E877F">sofa 2.19 m · chair 0.83 m · 24 m²</div>
  <div style="position:absolute;left:18px;right:18px;bottom:22px;height:62px;border-radius:16px;background:#F3EFEA;color:#151413;font-size:20px;line-height:62px;text-align:center">Share this room →</div>`;
cR14(559,'impact',{v:.55}); cR14(566,'shimmer',{v:.35,end:578}); [588,603].forEach(f=>cR14(f,'tick',{v:.3})); cR14(606,'swish',{v:.45,peak:609,dur:8}); cR14(608,'pop',{v:.5,n:84});
function shotPhone(F){ const f=F-2;   // numéros de la réf (REMAP +2)
  // dépli en hauteur (478 → 861 px), puis la caméra s'approche (×0,9 → ×1,28, décélération) en tournant de 4° : le téléphone vit
  // entrée de la réf : ×1,4 en 7 images (+20 → +3 %/image, ease-out), puis lente approche ; sortie : il se lève et recule en accélérant (637-641)
  const pt=clamp((f-559)/82), pin=1-Math.pow(1-clamp((f-559)/7),2), ex=accel(f,636,5.5,2.4);
  const ps=(f<566?lerp(0.9,1.0,pin):lerp(1.0,1.16,1-Math.pow(1-clamp((f-566)/75),2)))*(1-0.05*ex), ry=lerp(-2.5,1.5,pt);   // 1,16 : ~60 px de marge, le téléphone ne touche jamais le cadre
  // tenu à la main : ±6 px, ±0,5° de roulis, ~0,3 Hz (deux fréquences, déterministe)
  const hx=10*Math.sin(f*0.063+1.1)*0.75+2.5*Math.sin(f*0.17), hy=8*Math.sin(f*0.051+2.3)*0.8+2*Math.sin(f*0.21+0.4)-22*ex, hr=0.8*Math.sin(f*0.058+0.7);
  phone.style.transform=`translate(${(960+hx).toFixed(2)}px,${(540+hy).toFixed(2)}px) translate(-50%,-50%) rotate(${hr.toFixed(3)}deg) perspective(2400px) rotateY(${ry.toFixed(2)}deg) scale(${ps.toFixed(4)}) scaleY(${lerp(0.555,1,pin).toFixed(4)})`;
  phShadow.style.transform=`translate(${(hx*0.6).toFixed(1)}px,${(430*(ps-1)).toFixed(1)}px) scale(${ps.toFixed(3)},1)`;
  seqDraw(phSeq,SEQ.phone,f-559); phSeq.style.transform=`scale(${(1.14*(1+0.06*clamp((f-606)/35))).toFixed(4)}) translateX(${lerp(-24,40,pt).toFixed(1)}px)`;
  // démarrage d'une caméra AR : la mise au point cherche (22 → 0 → 4 → 0 px) et l'exposition se pose (+0,6 IL → 0), en 6 images
  const b=f<561?22:f<563?lerp(22,0,(f-561)/2):f<565?lerp(0,4,(f-563)/2):f<567?lerp(4,0,(f-565)/2):0, ev=0.6*(1-vl(f,561,6));
  phSeq.style.filter=(b>0.05?`blur(${b.toFixed(1)}px) `:'')+(ev>0.01?`brightness(${Math.pow(2,ev).toFixed(3)})`:'');
  phHolo.style.opacity=(1-vl(f,562,9)).toFixed(3); phHolo.style.backgroundPosition=`${(f-559)*6}px 0`;
  { const ro=Math.min(vl(f,573,8),1-vl(f,620,8)); show(phRib,ro>0&&!!RIB); if(ro>0&&RIB){ phRib.getContext('2d').clearRect(0,0,960,540); phRib.getContext('2d').drawImage(RIB.draw(f*0.9),0,0); phRib.style.opacity=ro.toFixed(3); } }
  phNum.textContent=Math.round(lerp(92,98,clamp((f-573)/30)))+'%';
  // se pose sur 0:42 (comme la carte de 1318) avant « Fits perfectly »
  const secs=Math.round(lerp(179,42,vladan(clamp((f-580)/21)))); phTime.textContent=`${Math.floor(secs/60)}:${String(secs%60).padStart(2,'0')}`;
  phSheen.style.translate=`${(140*clamp((f-559)/80)).toFixed(1)}px 0`;
  const dp=approach(f,606,10); phDone.style.transform=`translateY(${((1-dp)*440).toFixed(1)}px)`;
  phStats.forEach(e=>e.style.opacity=(1-clamp((f-604)/6)).toFixed(2));   // pas de « ROOM FIT » fantôme derrière le panneau
}

/* ---------- 15-16 · l'avant/après : la v1 exacte du fondateur, deux marques au stylo, puis la v2 en une vague ; gros plan de la barre d'outils ---------- */
const CL=scene('sClients',642,694,f=>shotClients(f)); sky(CL.cam);
const LU={branch:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/><path d="M6 9v6M18 9a9 9 0 0 1-9 9"/>',activity:'<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
  terminal:'<path d="M4 17l6-6-6-6M12 19h8"/>',code:'<path d="M10 9l-3 3 3 3M14 15l3-3-3-3"/><rect x="3" y="3" width="18" height="18" rx="2"/>'};
const lu=(k,sz,c='#151413',w=2)=>`<svg viewBox="0 0 24 24" width="${sz}" height="${sz}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round">${LU[k]}</svg>`;
const clCard=el(CL.cam,'','', 'position:absolute;left:0;top:0;width:1400px;height:880px;border-radius:18px;overflow:hidden;background:#F7F4F0;box-shadow:0 50px 100px -40px rgba(40,30,30,.5)');
clCard.innerHTML=`<div style="position:absolute;left:0;right:0;top:0;height:60px;background:#ECE8E3;box-shadow:0 1px 0 #DDD6CE">
  ${[0,1,2].map(i=>`<span style="position:absolute;left:${22+i*22}px;top:24px;width:12px;height:12px;border-radius:6px;background:#CFC8C0"></span>`).join('')}
  <div class="m" style="position:absolute;left:520px;top:14px;width:360px;height:32px;border-radius:9px;background:#F7F4F0;font-size:14px;line-height:32px;text-align:center;color:#5C5650">velvetly.app/overview</div>
  <div style="position:absolute;right:120px;top:16px;display:flex;gap:26px">${['branch','activity','terminal','code'].map(k=>lu(k,26)).join('')}</div>
  <div style="position:absolute;right:16px;top:12px;height:36px;line-height:36px;padding:0 16px;border-radius:9px;background:#fff;box-shadow:0 0 0 1px #DDD6CE;font-size:15px">Share</div></div>
  <div class="clD" style="position:absolute;left:20px;top:70px;width:1360px;height:800px;transform-origin:0 0"></div>`;
const clDash=buildDash(q1(clCard,'.clD'));
// l'après : une refonte complète (js/dash2.js), chaque bloc de la v1 vole vers son bloc de la v2
const clD2=buildDash2(q1(clCard,'.clD')), clSw=(c,i)=>clDash.sws.find(e=>e.dataset.c==c&&e.dataset.i==i);
const CL_AEL={flood:clDash.side,hero:clDash.img,title:clSw(3,0),sub:clSw(3,1),btn:clDash.btn,kpi0:clDash.kpis[0],kpi1:clDash.kpis[1],kpi2:clDash.kpis[2],list:clDash.ch};
CL.cam.style.transformOrigin='1602px 109px';   // la barre d'outils : la poussée finale va vers elle
const clInk=inkLayer(CL.s);
function clRect(e){ const r=e.getBoundingClientRect(), st=CL.s.getBoundingClientRect(), k=st.width/W; return [(r.left-st.left)/k,(r.top-st.top)/k,(r.right-st.left)/k,(r.bottom-st.top)/k]; }
const clZoom=el(CL.s,'','', 'position:absolute;inset:0;display:none;background:#F6F2EE');
const clBelow=el(clZoom,'','', 'position:absolute;left:0;top:0;width:1400px;height:880px;transform-origin:0 0;filter:blur(7px);opacity:.45');
const clBand=el(clZoom,'','', 'position:absolute;left:-40px;right:-200px;top:300px;height:360px;background:#ECE8E3;box-shadow:0 1px 0 #DDD6CE;transform-origin:50% 50%');
const CL_IC=[['branch',560],['activity',830],['terminal',1100],['code',1370]];
const clIcons=CL_IC.map(([k,x])=>{ const d=el(clBand,'','', `position:absolute;left:${x}px;top:95px;width:170px;height:170px;border-radius:34px`); el(d,'',lu(k,120,'#151413',1.6),'position:absolute;inset:25px'); return d; });
el(clBand,'abs','Share','left:1640px;top:96px;height:170px;line-height:166px;padding:0 60px;border-radius:30px;background:#fff;box-shadow:0 0 0 3px #DDD6CE;font-size:84px');
cue(642,'impact',{v:.5}); cue(648,'shimmer',{v:.5,end:660}); cue(668,'whoosh',{v:.45,peak:671,dur:4}); cue(676,'tick',{v:.25}); cue(690,'click',{v:.95}); cue(687,'whoosh',{v:.4,peak:694,dur:7});
function shotClients(f){ const z=f>=672; show(clZoom,z); show(CL.cam,!z);
  if(!z){ const y=70+40*(1-approach(f,642,4,0.3)); clCard.style.transformOrigin='0 0'; placeTL(clCard,-90,y,1.3);   // déborde à gauche et en bas ; le titre de la v2 reste entier
    CL.cam.style.transform=`scale(${((1+0.035*clamp((f-642)/26))*(1+0.058*accel(f,668,4,3))).toFixed(4)})`;   // lente poussée vers la barre d'outils pendant l'avant/après
    updateDash(clDash,()=>0,f); dash2Morph(clD2,f,648,D2_A1,CL_AEL);
    inkClear(clInk);
    cursor(0,0,0,false); return; }
  // la poussée continue à travers la coupe et ralentit (672-680), on tient (680-686), puis panoramique qui accélère vers la gauche (687-694)
  const zp=approach(f,672,8,0.25), pan=-60*accel(f,686,8,2.8);
  clBand.style.transform=`translate(${(pan-26*zp).toFixed(1)}px,${(16*zp).toFixed(1)}px) scale(${(1.3*(1+0.045*zp)).toFixed(4)})`; clBand.style.transformOrigin='2300px 180px';
  // copie figée dans l'état v2 (toute la vague passée) : l'image reste une fonction de f, quel que soit l'ordre de rendu
  if(!clBelow.firstChild){ updateDash(clDash,()=>0,671); dash2Morph(clD2,671,648,D2_A1,CL_AEL); const c=clCard.cloneNode(true); c.style.transform=''; c.style.boxShadow='none'; clBelow.appendChild(c); }
  clBelow.style.transform=`translate(${(-2866+pan-26*zp).toFixed(1)}px,${(384+16*zp).toFixed(1)}px) scale(3.2)`;
  mblur(clBand,f>=689?vel(t=>-60*accel(t,686,8,2.8),f)*BLUR:0,0);
  const hov=f>=680; clIcons[2].style.background=hov?(f>=688&&f<691?'#DDD6CE':'#E4DFD9'):'transparent';
  // le curseur du fondateur clique le terminal (690) : c'est lui qui ouvre le terminal du plan suivant
  const cf=f, cp=clamp((cf-672)/10), ib=clIcons[2].getBoundingClientRect(), zb=CL.s.getBoundingClientRect(), kz=zb.width/W;
  cursor(lerp(760,(ib.left+ib.width*0.6-zb.left)/kz,cp),lerp(820,(ib.top+ib.height*0.62-zb.top)/kz,cp),f>=688&&f<691?1:0,true,3);
}
