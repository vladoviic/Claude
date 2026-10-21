/* ============================================================
   Ouverture (54-119) : l'éclatement de sites. Onze sites inventés au niveau des Sites of the Day d'Awwwards,
   un métier, une direction artistique et une couleur dominante chacun (noms et marques inventés).
   Lecture en 1 s à 30-60 % : une idée forte par site (typo géante, objet, champ de couleur), du détail crédible autour.
   Pendant les teintes de la réf (62-69, 114-116), chaque carte passe en camaïeu de SA couleur.
   Les tailles (w, h) sont celles de la mise en page de js/shots1.js (BR, BXT) : ne pas les changer.
   ============================================================ */
const SITES=[];
function site(name,color,w,h,html){ SITES.push({name,color,w,h,html}); return SITES.length-1; }
const P='position:absolute;';
// grain de film : bruit fractal en SVG (rastérisé une fois, en mosaïque), posé en incrustation
const NOISE=`url(&quot;data:image/svg+xml,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160"><filter id="n" x="0" y="0"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="160" height="160" filter="url(#n)"/></svg>')}&quot;)`;
const grain=(o=.2,m='overlay')=>`<div style="${P}inset:0;background-image:${NOISE};background-size:160px 160px;mix-blend-mode:${m};opacity:${o}"></div>`;
const row=(items,css)=>`<div style="display:flex;${css}">${items.map(t=>`<span>${t}</span>`).join('')}</div>`;

// 0 · écurie de course : noir carbone, « 07 » ultra-condensé avec traînée de vitesse, citron électrique (esprit des sites de pilotes)
site('Korvo Racing','#D4FF3A',884,405,`<div style="${P}inset:0;background:#0A0B09;color:#EEF0E6;overflow:hidden;font-family:'ID'">
  <div style="${P}inset:0;background:radial-gradient(46% 78% at 30% 68%,rgba(212,255,58,.24),rgba(212,255,58,0) 72%),radial-gradient(36% 60% at 100% 0%,rgba(255,255,255,.07),rgba(255,255,255,0) 70%)"></div>
  <div style="${P}inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.055) 0 1px,transparent 1px 98px);-webkit-mask:linear-gradient(180deg,transparent 8%,#000 40%,#000 75%,transparent)"></div>
  <svg width="884" height="405" style="${P}left:0;top:0">
    <defs><filter id="kr0a" x="-80%" y="-10%" width="260%" height="120%"><feGaussianBlur stdDeviation="54 0"/></filter>
      <filter id="kr0b" x="-80%" y="-10%" width="260%" height="120%"><feGaussianBlur stdDeviation="14 0"/></filter>
      <linearGradient id="kr0g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3FFB8"/><stop offset=".35" stop-color="#DDFF55"/><stop offset="1" stop-color="#A9D80E"/></linearGradient>
      <linearGradient id="kr0s" x1="0" x2="1"><stop offset="0" stop-color="#D4FF3A" stop-opacity="0"/><stop offset="1" stop-color="#D4FF3A" stop-opacity=".9"/></linearGradient></defs>
    ${[[120,176,1.5],[150,232,1],[40,262,2],[96,318,1],[10,350,1.5]].map(([x,y,s])=>`<rect x="${x}" y="${y}" width="${200-x/2}" height="${s}" fill="url(#kr0s)"/>`).join('')}
    <g transform="translate(300 428) skewX(-10)" style="font:900 486px 'AV';font-stretch:62%;letter-spacing:-.035em" text-anchor="middle">
      <text x="-130" fill="#D4FF3A" opacity=".16" filter="url(#kr0a)">07</text>
      <text x="-44" fill="#D4FF3A" opacity=".38" filter="url(#kr0b)">07</text>
      <text x="0" fill="url(#kr0g)">07</text></g>
  </svg>
  <div style="${P}left:0;right:0;top:0;height:28px;background:#D4FF3A;color:#0A0B09;font:500 10.5px/28px 'JB';letter-spacing:.04em;display:flex;justify-content:space-between;padding:0 44px">
    <span>● LIVE — SUZUKA GP · FREE PRACTICE 2</span><span>ONBOARD CAM 07 · 312 KM/H · SECTOR 2 PURPLE</span><span>WATCH →</span></div>
  <div style="${P}left:44px;right:34px;top:44px;display:flex;justify-content:space-between;align-items:center">
    <span style="font:900 19px 'AV';font-stretch:125%;letter-spacing:-.01em">KORVO<span style="color:#D4FF3A">/</span>07</span>
    ${row(['Season 26','Helmet lab','Onboard','Partners','Store'],"gap:26px;font:500 12.5px 'ID';color:#C9CCC0")}
    <span style="font:600 12px 'ID';height:32px;line-height:30px;padding:0 16px;border:1px solid rgba(238,240,230,.35);border-radius:16px">Shop the kit ↗</span></div>
  <div style="${P}left:560px;top:104px;font:500 10.5px 'JB';color:#D4FF3A;letter-spacing:.06em">(DRIVER 07) — ROUND 18 / 24</div>
  <div style="${P}left:556px;top:126px;font:800 58px/.9 'AV';font-stretch:88%;letter-spacing:-.045em;color:#F4F5EE">Ninety laps.<br><span style="color:#D4FF3A">Zero lift.</span></div>
  <div style="${P}left:560px;top:250px;width:270px;font:400 13px/1.45 'ID';color:#92978B">Rookie of the year in ’25, now hunting the title in the KV-26 — seven tenths quicker through every sector.</div>
  <div style="${P}left:560px;top:312px;display:flex;gap:10px;font:600 12.5px 'ID'">
    <span style="height:36px;line-height:36px;padding:0 18px 0 14px;border-radius:18px;background:#D4FF3A;color:#0A0B09;display:flex;align-items:center;gap:9px"><i style="width:0;height:0;border-left:8px solid #0A0B09;border-top:5px solid transparent;border-bottom:5px solid transparent;display:block"></i>Watch onboard</span>
    <span style="height:36px;line-height:34px;padding:0 18px;border-radius:18px;border:1px solid rgba(238,240,230,.35)">Season 26 →</span></div>
  <div style="${P}left:560px;right:34px;bottom:0;height:44px;border-top:1px solid rgba(238,240,230,.16);display:flex;justify-content:space-between;align-items:center;font:500 10px 'JB';color:#7D8276;letter-spacing:.05em">
    <span><b style="font:800 19px 'AV';font-stretch:70%;color:#EEF0E6;letter-spacing:0">14</b> PODIUMS</span><span><b style="font:800 19px 'AV';font-stretch:70%;color:#EEF0E6;letter-spacing:0">06</b> POLES</span><span><b style="font:800 19px 'AV';font-stretch:70%;color:#D4FF3A;letter-spacing:0">P2</b> STANDINGS</span></div>
</div>`);

// 1 · festival : coucher de soleil magenta → orange, soleil qui se lève derrière les dunes, « Solstice » en serif italique géante
site('Solstice','#F0457B',740,480,`<div style="${P}inset:0;background:linear-gradient(180deg,#1E0527 0%,#470B44 24%,#9E1A62 46%,#F0457B 63%,#FF7A45 80%,#FFB25E 100%);color:#FFF1E4;overflow:hidden;font-family:'ID'">
  <div style="${P}left:330px;top:150px;width:330px;height:330px;border-radius:50%;background:radial-gradient(circle at 50% 42%,#FFFBE8 0,#FFE9A6 22%,#FFC05A 52%,#FF8A45 80%,#FF5F5F 100%);box-shadow:0 0 90px 24px rgba(255,170,90,.6),0 0 240px 90px rgba(240,69,123,.45)"></div>
  <svg width="740" height="480" viewBox="0 0 740 480" style="${P}left:0;top:0" preserveAspectRatio="none">
    <defs><linearGradient id="so1a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E1B4D"/><stop offset="1" stop-color="#3A0A2C"/></linearGradient>
      <linearGradient id="so1b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4B0C36"/><stop offset="1" stop-color="#1A0420"/></linearGradient></defs>
    <path d="M0 372 C120 340 200 352 300 366 C400 380 470 330 580 336 C650 340 700 352 740 346 L740 480 L0 480 Z" fill="url(#so1a)"/>
    <path d="M0 412 C90 390 190 384 300 404 C420 426 520 392 620 398 C680 402 720 410 740 408 L740 480 L0 480 Z" fill="url(#so1b)"/>
  </svg>
  ${grain(.32)}
  <div style="${P}left:0;right:0;top:0;height:26px;border-bottom:1px solid rgba(255,241,228,.18);font:500 10px/26px 'JB';letter-spacing:.06em;color:rgba(255,241,228,.8);display:flex;justify-content:space-between;padding:0 26px"><span>PHASE 2 TICKETS — 82% SOLD</span><span>CAMPING ADD-ON NOW OPEN</span><span>EN / ES</span></div>
  <div style="${P}left:26px;right:56px;top:40px;display:flex;justify-content:space-between;align-items:center">
    <span style="font:800 16px 'SY';letter-spacing:-.01em;display:flex;align-items:center;gap:8px"><i style="width:14px;height:14px;border-radius:50%;background:#FFD27A;display:block;box-shadow:0 0 12px #FFD27A"></i>solstice</span>
    ${row(['Line-up','Tickets','Camping','Journal','Info'],"gap:24px;font:500 12.5px 'ID'")}
    <span style="font:600 12px 'ID';height:32px;line-height:32px;padding:0 16px;border-radius:16px;background:#FFF1E4;color:#470B44">Tickets from €189 →</span></div>
  <div style="${P}left:28px;top:96px;font:500 11px 'JB';letter-spacing:.08em;color:rgba(255,241,228,.85)">(A FESTIVAL FOR THE LONGEST DAY)</div>
  <div style="${P}left:16px;top:104px;font:italic 400 214px/1 'DS';letter-spacing:-.045em;white-space:nowrap">Solstice<span style="font:800 30px 'AV';font-stretch:125%;letter-spacing:-.02em;vertical-align:top;position:relative;top:44px;margin-left:6px">’26</span></div>
  <div style="${P}left:30px;top:320px;display:flex;gap:26px;align-items:baseline">
    <span style="font:800 22px 'AV';font-stretch:125%;letter-spacing:-.02em">19—22.06</span><span style="font:400 13px/1.35 'ID';color:rgba(255,241,228,.85)">Tarifa, Andalucía<br>4 days · 3 stages · 1 very long sunset</span></div>
  <div style="${P}left:30px;right:56px;top:398px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px">
    ${[['FRI 19.06','Moss Temple','Aya Korin · Halo Halo'],['SAT 20.06','Dune Machine','Velvet Antenna · Oru'],['SUN 21.06','Soft Riot','Noor &amp; the Tide · Parallax']].map(([d,a,b])=>`<div style="border-top:1px solid rgba(255,241,228,.3);padding-top:8px"><div style="font:500 9.5px 'JB';letter-spacing:.08em;opacity:.7">${d}</div><div style="font:800 19px/1.1 'AV';font-stretch:80%;letter-spacing:-.01em;text-transform:uppercase;margin-top:4px">${a}</div><div style="font:500 11.5px 'ID';opacity:.8;margin-top:2px">${b}</div></div>`).join('')}</div>
</div>`);

// 2 · parfum (mobile) : flacon de verre ambré sur socle de travertin, pêche poudrée, la marque en serif italique géante derrière l'objet
// (la carte est rognée à gauche pendant l'éclatement : l'objet et le texte sont décalés vers la droite)
site('Sève Parfums','#F2C3A5',320,493,`<div style="${P}inset:0;background:radial-gradient(120% 70% at 64% 34%,#FCE4D3 0,#F3BF9F 50%,#DE9673 100%);color:#3A1C12;overflow:hidden;font-family:'ID'">
  <div style="${P}left:16px;right:16px;top:16px;display:flex;justify-content:space-between;align-items:center;font:500 11px 'ID'">
    <span style="display:flex;flex-direction:column;gap:4px"><i style="width:18px;height:1.5px;background:#3A1C12;display:block"></i><i style="width:12px;height:1.5px;background:#3A1C12;display:block"></i></span>
    <span style="font:400 19px 'DS';letter-spacing:.24em;margin-left:14px">SÈVE</span><span>Bag (0)</span></div>
  <div style="${P}left:0;width:372px;top:58px;text-align:center;font:italic 400 142px/1 'DS';letter-spacing:-.05em;color:#E2936F;white-space:nowrap">Sève</div>
  <div style="${P}left:82px;top:350px;width:220px;height:42px;background:linear-gradient(90deg,#C9AD94,#EDE0D1 30%,#F6EDE3 45%,#DAC4AE 75%,#BB9C83);border-radius:0 0 110px 110px / 0 0 20px 20px"></div>
  <div style="${P}left:82px;top:322px;width:220px;height:56px;border-radius:50%;background:radial-gradient(closest-side,#FAF2E9,#EBDBCB 70%,#DCC5B0);box-shadow:inset 0 1px 0 rgba(255,255,255,.8)"></div>
  <div style="${P}left:198px;top:334px;width:110px;height:28px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,140,50,.75),rgba(255,140,50,0))"></div>
  <div style="${P}left:118px;top:338px;width:150px;height:22px;border-radius:50%;background:radial-gradient(closest-side,rgba(80,30,10,.5),rgba(80,30,10,0));filter:blur(2px)"></div>
  <div style="${P}left:158px;top:88px;width:68px;height:80px;border-radius:7px 7px 3px 3px;background:linear-gradient(90deg,#0B0806 0,#2E241F 16%,#8E7E74 27%,#2A201B 38%,#0D0907 64%,#3E322C 86%,#120D0A);box-shadow:0 8px 10px -6px rgba(0,0,0,.5)"></div>
  <div style="${P}left:168px;top:166px;width:48px;height:12px;background:linear-gradient(90deg,#6E4E1C,#F0D28A 34%,#FFF1C6 44%,#B6893A 64%,#553A12)"></div>
  <div style="${P}left:116px;top:176px;width:152px;height:170px;border-radius:24px;background:linear-gradient(180deg,rgba(255,240,228,.55),rgba(250,205,175,.35));box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.65),inset 0 -14px 22px rgba(140,50,10,.25),0 26px 30px -20px rgba(90,30,10,.6)">
    <div style="${P}left:13px;right:13px;top:34px;bottom:13px;border-radius:13px;background:linear-gradient(180deg,#FFC27E 0,#F49144 40%,#D2632A 78%,#A9441B 100%);box-shadow:inset 0 2px 0 rgba(255,236,200,.9)"></div>
    <div style="${P}left:13px;right:13px;bottom:13px;height:20px;border-radius:0 0 13px 13px;background:linear-gradient(180deg,rgba(255,220,170,0),rgba(255,220,170,.5))"></div>
    <div style="${P}inset:0;border-radius:24px;background:linear-gradient(90deg,rgba(255,255,255,.62) 0,rgba(255,255,255,.12) 7%,rgba(255,255,255,0) 22%,rgba(255,255,255,0) 66%,rgba(255,255,255,.22) 84%,rgba(255,255,255,.7) 93%,rgba(255,255,255,.12) 100%)"></div>
    <div style="${P}left:40px;top:72px;width:72px;height:46px;background:#FBF4EC;box-shadow:0 1px 2px rgba(80,30,10,.25);text-align:center;color:#3A1C12"><div style="font:400 13px/1 'DS';letter-spacing:.2em;margin-top:9px;margin-left:2px">SÈVE</div><div style="font:500 6px 'JB';letter-spacing:.12em;margin-top:6px">N°4 · EAU DE PARFUM</div></div></div>
  ${grain(.14)}
  <div style="${P}left:20px;right:18px;top:404px;display:flex;justify-content:space-between;font:500 9.5px 'JB';letter-spacing:.06em;color:#7A4A36"><span>04 / 07</span><span>EAU DE PARFUM · 50 ML · €148</span></div>
  <div style="${P}right:18px;top:426px;text-align:right;font:400 23px/1.02 'DS';letter-spacing:-.01em;white-space:nowrap">Fig leaf, wet stone<br><i>&amp; a little smoke.</i></div>
  <div style="${P}left:20px;top:432px;width:42px;height:42px;border-radius:50%;background:#3A1C12;color:#FBEFE6;font:400 18px/42px 'ID';text-align:center">+</div>
</div>`);

// 3 · fonderie typographique : lie-de-vin, « Ag » géant avec ses lignes de métrique, réglages d'axes variables
site('Basalt Type','#5E0F1B',550,297,`<div style="${P}inset:0;background:#5E0F1B;color:#FFC9CF;overflow:hidden;font-family:'ID'">
  <div style="${P}inset:0;background:radial-gradient(70% 90% at 25% 70%,#7A1626,rgba(122,22,38,0) 70%)"></div>
  <div style="${P}left:18px;right:18px;top:14px;display:flex;justify-content:space-between;align-items:center">
    <span style="font:800 16px 'AV';font-stretch:112%;letter-spacing:-.02em">Basalt<sup style="font:500 8px 'JB';letter-spacing:.06em;margin-left:3px;vertical-align:6px">TYPE</sup></span>
    ${row(['Typefaces','In use','Trials','Licensing','Cart (2)'],"gap:18px;font:500 11px 'ID'")}</div>
  <div style="${P}left:18px;right:18px;top:40px;height:1px;background:rgba(255,201,207,.25)"></div>
  <svg width="340" height="297" style="${P}left:0;top:0">
    ${[[66,'CAP 710'],[111,'X 528'],[200,'BASE 0'],[238,'DESC −210']].map(([y,t])=>`<line x1="18" x2="332" y1="${y}" y2="${y}" stroke="#FFC9CF" stroke-opacity=".35" stroke-dasharray="2 3"/><text x="332" y="${y-4}" text-anchor="end" style="font:500 7.5px 'JB';letter-spacing:.06em" fill="#FFC9CF" fill-opacity=".7">${t}</text>`).join('')}
    <text x="12" y="200" style="font:800 190px 'AV';font-stretch:72%;letter-spacing:-.04em" fill="#FFC9CF">Ag</text>
  </svg>
  <div style="${P}left:356px;top:54px;width:176px">
    <div style="font:600 19px/1 'ID';letter-spacing:-.02em;color:#FFE4E7">Basalt Grotesk</div>
    <div style="font:500 9px 'JB';letter-spacing:.05em;margin-top:6px;opacity:.7">VARIABLE · 2 AXES · 72 STYLES</div>
    ${[['Weight',800,.86],['Width',72,.15]].map(([k,v,p])=>`<div style="margin-top:14px;display:flex;justify-content:space-between;font:500 10px 'ID'"><span>${k}</span><span style="font-family:'JB'">${v}</span></div><div style="position:relative;height:2px;background:rgba(255,201,207,.25);margin-top:7px"><div style="position:absolute;left:0;top:0;height:2px;width:${p*100}%;background:#FFC9CF"></div><div style="position:absolute;left:calc(${p*100}% - 6px);top:-5px;width:12px;height:12px;border-radius:50%;background:#FFC9CF"></div></div>`).join('')}
    <div style="display:flex;gap:6px;margin-top:16px">${['a','g','&amp;','R','3'].map((g,i)=>`<span style="width:30px;height:30px;border:1px solid rgba(255,201,207,.35);border-radius:4px;display:grid;place-items:center;font:${[300,500,800,900,600][i]} 17px 'AV';font-stretch:${[62,90,72,112,125][i]}%">${g}</span>`).join('')}</div>
    <div style="display:flex;gap:6px;margin-top:16px;font:600 10.5px 'ID'"><span style="height:30px;line-height:30px;padding:0 12px;border-radius:15px;background:#FFC9CF;color:#5E0F1B;white-space:nowrap">Buy family · €480</span><span style="height:30px;line-height:28px;padding:0 12px;border-radius:15px;border:1px solid rgba(255,201,207,.45);white-space:nowrap">Trial ↓</span></div></div>
  <div style="${P}left:18px;right:18px;top:262px;height:1px;background:rgba(255,201,207,.25)"></div>
  <div style="${P}left:18px;top:270px;display:flex;gap:16px;align-items:baseline;white-space:nowrap;font-size:17px;font-family:'AV';letter-spacing:-.02em">${[[100,62,'Thin'],[300,75,'Light'],[400,87,'Book'],[600,100,'Medium'],[800,112,'Bold'],[900,125,'Black']].map(([w,s,t])=>`<span style="font-weight:${w};font-stretch:${s}%">${t}</span>`).join('')}</div>
</div>`);

// 4 · agence d'architecture : colonne béton clair + photo en bichromie (la fenêtre et ses ombres portées), titre fin mêlé d'italique
// (la carte est rognée à droite et en bas pendant l'éclatement : le texte est dans la colonne de gauche, la fenêtre juste à côté)
site('Ombra Architects','#CBC3B5',830,440,`<div style="${P}inset:0;background:#D8D1C4;color:#1B1916;overflow:hidden;font-family:'ID'">
  <div style="${P}left:340px;top:0;right:0;bottom:0;overflow:hidden;background:#26231F">
    <img src="img/room_top.jpg" style="${P}left:-14px;top:-96px;width:1380px;height:776px;object-fit:cover;filter:grayscale(1) contrast(1.32) brightness(1.03)">
    <div style="${P}inset:0;background:#2B2621;mix-blend-mode:lighten"></div>
    <div style="${P}inset:0;background:#EEE4D3;mix-blend-mode:multiply"></div>
    <div style="${P}inset:0;background:linear-gradient(180deg,rgba(20,18,15,.45),rgba(20,18,15,0) 20%,rgba(20,18,15,0) 70%,rgba(20,18,15,.6))"></div>
    ${grain(.2)}
    <div style="${P}left:24px;bottom:22px;font:500 10px/1.6 'JB';letter-spacing:.05em;color:rgba(250,246,239,.9)">CASA SOMBRA — COMPORTA<br>RESIDENTIAL · 240 M² · 2025</div>
    <div style="${P}right:26px;bottom:24px;display:flex;align-items:center;gap:12px;font:500 10px 'JB';color:rgba(250,246,239,.9)"><span>03</span><span style="width:110px;height:1px;background:rgba(250,246,239,.3);position:relative"><i style="position:absolute;left:0;top:0;width:28%;height:1px;background:#FAF6EF;display:block"></i></span><span>12</span></div>
    <div style="${P}right:26px;top:24px;display:flex;gap:24px;font:500 12px 'ID';color:#FAF6EF">${['Projects <sup style="font-size:8px">31</sup>','Studio','Research','Contact'].map(t=>`<span>${t}</span>`).join('')}<span style="font:500 10.5px 'JB';margin-left:8px">EN / PT</span></div></div>
  ${grain(.12,'multiply')}
  <div style="${P}left:30px;top:24px;font:600 14px 'AV';font-stretch:125%;letter-spacing:.34em">OMBRA</div>
  <div style="${P}left:30px;top:52px;font:500 9.5px 'JB';letter-spacing:.06em;color:#6E665B">ARCHITECTS — PORTO, SINCE 2011</div>
  <div style="${P}left:26px;top:104px;font:300 47px/.94 'AV';font-stretch:100%;letter-spacing:-.055em;white-space:nowrap">We draw with<br>light first,<br>then build<br><span style="font:italic 400 49px 'DS';letter-spacing:-.035em">around it.</span></div>
  <div style="${P}left:30px;top:304px;width:270px;font:400 12px/1.5 'ID';color:#4F483F">Houses, schools and one very quiet chapel — 31 buildings drawn around the sun’s path.</div>
  <div style="${P}left:30px;top:366px;display:flex;gap:8px;font:600 11.5px 'ID'"><span style="height:34px;line-height:34px;padding:0 16px;border-radius:17px;background:#1B1916;color:#EFEAE1">View projects</span><span style="height:34px;line-height:32px;padding:0 16px;border-radius:17px;border:1px solid rgba(27,25,22,.4)">Studio reel ▸</span></div>
</div>`);

// 5 · banque en ligne (goût) : vert forêt, carte en métal brossé inclinée, serif éditoriale
site('Halden','#123D2E',420,300,`<div style="${P}inset:0;background:radial-gradient(90% 80% at 75% 40%,#1C5A43,#123D2E 55%,#0B2a20);color:#EAF1E8;overflow:hidden;font-family:'ID'">
  <div style="${P}left:16px;right:16px;top:14px;display:flex;justify-content:space-between;align-items:center;font:500 11px 'ID'"><span style="font:400 18px 'DS';letter-spacing:-.01em">Halden</span>${row(['Save','Invest','Business'],'gap:14px;opacity:.8')}<span style="height:24px;line-height:24px;padding:0 10px;border-radius:12px;background:#EAF1E8;color:#123D2E;font-weight:600">Open account</span></div>
  <div style="${P}left:16px;top:66px;font:400 42px/.95 'DS';letter-spacing:-.025em">Money,<br><i>quietly.</i></div>
  <div style="${P}left:16px;top:170px;width:150px;font:400 11.5px/1.45 'ID';opacity:.75">No noise, no confetti. Just a very good rate.</div>
  <div style="${P}left:16px;bottom:16px"><div style="font:800 40px/1 'AV';font-stretch:68%;letter-spacing:-.02em;color:#C8F0B4">4.10%</div><div style="font:500 9px 'JB';letter-spacing:.06em;opacity:.7;margin-top:4px">AER · INSTANT ACCESS</div></div>
  <div style="${P}left:192px;top:78px;width:210px;height:132px;border-radius:12px;transform:perspective(600px) rotateY(-18deg) rotateX(10deg) rotateZ(-8deg);background:linear-gradient(118deg,#B9CBBE 0,#E7F0E9 22%,#93AE9D 46%,#DDE8E0 64%,#7E9A89 100%);box-shadow:0 30px 40px -16px rgba(0,0,0,.55),inset 0 0 0 1px rgba(255,255,255,.45);color:#123D2E">
    <div style="${P}inset:0;border-radius:12px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.08) 0 1px,transparent 1px 3px)"></div>
    <div style="${P}left:16px;top:14px;font:400 16px 'DS'">Halden</div>
    <div style="${P}left:16px;top:48px;width:30px;height:22px;border-radius:4px;background:linear-gradient(135deg,#E9D08C,#B48C3E 60%,#F3E2B0)"></div>
    <div style="${P}left:16px;bottom:14px;font:500 10px 'JB';letter-spacing:.12em">•••• 0417</div><div style="${P}right:14px;bottom:12px;font:500 8px 'JB';letter-spacing:.08em">METAL</div></div>
  ${grain(.16)}
</div>`);

// 6 · céramiste : terre cuite, photo de la jarre dans une arche, serif chaude
site('Terra Cruda','#C4643F',420,300,`<div style="${P}inset:0;background:#C4643F;color:#FBEDE1;overflow:hidden;font-family:'ID'">
  <div style="${P}inset:0;background:radial-gradient(80% 90% at 20% 20%,#D27650,rgba(210,118,80,0) 70%)"></div>
  ${grain(.24)}
  <div style="${P}left:16px;right:16px;top:14px;display:flex;justify-content:space-between;font:500 10.5px 'ID'"><span style="font:600 11px 'ID';letter-spacing:.18em">TERRA CRUDA</span>${row(['Shop','Studio','Workshops','Cart 1'],'gap:14px')}</div>
  <div style="${P}right:18px;top:40px;width:164px;height:236px;border-radius:82px 82px 4px 4px;overflow:hidden;background:#2A2522;box-shadow:0 20px 30px -18px rgba(60,20,5,.6)">
    <img src="img/tile_plant.jpg" style="${P}left:-74px;top:-150px;width:312px;height:416px;object-fit:cover;filter:saturate(.9) contrast(1.05)"></div>
  <div style="${P}left:16px;top:50px;font:400 37px/.95 'DS';letter-spacing:-.02em">Thrown slow,<br>fired<br><i>slower.</i></div>
  <div style="${P}left:16px;top:188px;width:200px;font:400 11px/1.45 'ID';opacity:.85">Red Alentejo clay, wood-fired twice a year. Every jar is a little lopsided, on purpose.</div>
  <div style="${P}left:16px;bottom:16px;height:28px;line-height:28px;padding:0 12px;border-radius:14px;background:#FBEDE1;color:#7A3018;font:600 10.5px 'ID'">Shop the kiln →</div>
  <div style="${P}right:18px;bottom:8px;width:164px;display:flex;justify-content:space-between;font:500 8.5px 'JB';letter-spacing:.05em;opacity:.9"><span>VASO N°12</span><span>€86</span></div>
</div>`);

// 7 · magazine culturel : violet, titre de une en serif géante, grille d'articles avec images génératives
site('Parallax Magazine','#7D4CF2',440,300,`<div style="${P}inset:0;background:#7D4CF2;color:#140A2B;overflow:hidden;font-family:'ID'">
  <div style="${P}left:14px;right:14px;top:10px;display:flex;justify-content:space-between;font:500 9px 'JB';letter-spacing:.06em"><span>N°12 — THE SLOW ISSUE</span><span>AUTUMN 2026</span><span>SUBSCRIBE →</span></div>
  <div style="${P}left:6px;top:12px;font:400 121px/1 'DS';letter-spacing:-.055em;color:#F3EEFF;white-space:nowrap">Parallax</div>
  <div style="${P}left:14px;right:14px;top:128px;height:1px;background:#140A2B"></div>
  <div style="${P}left:14px;top:138px;width:200px;height:146px;border-radius:3px;overflow:hidden;background:radial-gradient(60% 70% at 62% 40%,#FFD08A,#FF7A3C 40%,#B3205A 75%,#3A0E3E)">
    <div style="${P}left:54px;top:30px;width:92px;height:92px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#4A3A5E,#120A1E 60%,#000);box-shadow:24px 30px 40px rgba(40,0,30,.5)"></div>${grain(.35)}</div>
  ${[['ESSAY','The last analog darkroom in Porto'],['DESIGN','Why every chair wants to be a sculpture'],['INTERVIEW','A typographer who only draws in pencil']].map(([k,t],i)=>`<div style="${P}left:228px;right:14px;top:${138+i*50}px;height:44px;border-bottom:1px solid rgba(20,10,43,.35)"><div style="font:500 8px 'JB';letter-spacing:.08em">0${i+1} · ${k}</div><div style="font:400 14px/1 'DS';margin-top:3px;letter-spacing:-.01em">${t}</div></div>`).join('')}
</div>`);

// 8 · marque de running : orange signal, « 42.195 » géant penché, tracé de parcours
site('Second Wind','#FF5A1F',480,280,`<div style="${P}inset:0;background:#FF5A1F;color:#140B06;overflow:hidden;font-family:'ID'">
  <div style="${P}inset:0;background:radial-gradient(70% 90% at 80% 20%,#FF8A4A,rgba(255,138,74,0) 70%)"></div>
  <svg width="480" height="280" style="${P}left:0;top:0"><path d="M-10 214 C50 170 96 112 170 118 C240 124 236 176 300 170 C360 164 362 108 420 112 C450 114 470 128 500 120" fill="none" stroke="#FFE7D6" stroke-width="2.5" stroke-dasharray="1 6" stroke-linecap="round"/><circle cx="420" cy="112" r="5" fill="#140B06"/><circle cx="420" cy="112" r="11" fill="none" stroke="#140B06" stroke-width="1.5"/></svg>
  <div style="${P}left:274px;top:101px;height:22px;line-height:22px;padding:0 9px;border-radius:11px;background:#140B06;color:#FFE7D6;font:500 9.5px 'JB';letter-spacing:.04em">KM 42 · 4’12”/KM</div>
  <div style="${P}left:16px;right:16px;top:14px;display:flex;justify-content:space-between;align-items:center;font:500 11px 'ID'"><span style="font:900 13px 'AV';font-stretch:125%;letter-spacing:-.01em">SECOND WIND®</span>${row(['Shoes','Apparel','Run club','Journal'],'gap:16px')}<span>Bag 0</span></div>
  <div style="${P}left:16px;top:44px;font:600 17px/1.1 'ID';letter-spacing:-.02em;width:200px">Built for the last<br>195 metres.</div>
  <div style="${P}right:16px;top:46px;text-align:right;font:500 9px/1.5 'JB';letter-spacing:.05em">TEMPO 3 — €165<br>NEW · 7 COLOURS</div>
  <div style="${P}left:12px;bottom:-28px;font:900 198px/1 'AV';font-stretch:62%;letter-spacing:-.045em;transform:skewX(-10deg);transform-origin:0 100%;white-space:nowrap">42.195<span style="font:800 26px 'AV';font-stretch:100%;letter-spacing:-.02em;margin-left:6px">km</span></div>
  ${grain(.2)}
</div>`);

// 9 · boisson (mobile) : canette rose « Sprizzo » sur pistache, rondelles d'orange sanguine en conic-gradient
site('Sprizzo','#C9DE9A',240,380,`<div style="${P}inset:0;background:radial-gradient(100% 70% at 50% 38%,#E4F0C2,#C9DE9A 60%,#AFC97C);color:#1F3410;overflow:hidden;font-family:'ID'">
  <div style="${P}left:14px;right:14px;top:12px;display:flex;justify-content:space-between;align-items:center;font:600 10px 'ID'"><span style="font:900 14px 'UB';letter-spacing:-.04em">sprizzo</span><span>Shop · ☰</span></div>
  ${[[22,96,46,30],[170,70,38,-20],[176,236,30,50]].map(([x,y,s,r])=>`<div style="${P}left:${x}px;top:${y}px;width:${s}px;height:${s}px;border-radius:50%;background:#FFE6C9;padding:3px;transform:rotate(${r}deg);box-shadow:0 8px 12px -6px rgba(31,52,16,.4)"><div style="width:100%;height:100%;border-radius:50%;background:repeating-conic-gradient(#D7263D 0 26deg,#FFD3B0 26deg 30deg)"></div></div>`).join('')}
  <div style="${P}left:72px;top:48px;width:96px;height:200px;transform:rotate(-8deg)">
    <div style="${P}left:0;top:10px;width:96px;height:184px;border-radius:12px/9px;background:linear-gradient(90deg,#9E0F3E 0,#E2306A 14%,#FF8CB2 27%,#FF4F86 40%,#E2306A 70%,#A1123F 100%);box-shadow:0 30px 30px -18px rgba(31,52,16,.6)">
      <div style="${P}left:0;right:0;top:0;height:14px;border-radius:12px/9px;background:linear-gradient(90deg,#9B9B9B,#F2F2F2 30%,#BDBDBD 55%,#7A7A7A)"></div>
      <div style="${P}left:0;right:0;bottom:0;height:10px;border-radius:12px/7px;background:linear-gradient(90deg,#8A8A8A,#E6E6E6 30%,#A8A8A8 60%,#6E6E6E)"></div>
      <div style="${P}left:50%;top:94px;transform:translate(-50%,-50%) rotate(-90deg);font:900 28px/1 'UB';letter-spacing:-.05em;color:#FFF0E4;white-space:nowrap">sprizzo</div>
      </div>
    <div style="${P}left:6px;top:0;width:84px;height:18px;border-radius:50%;background:radial-gradient(closest-side,#FAFAFA,#C8C8C8 70%,#9A9A9A)"></div></div>
  <div style="${P}left:14px;top:268px;font:800 21px/.98 'SY';letter-spacing:-.04em;white-space:nowrap">Aperitivo,<br>minus the<br>hangover.</div>
  <div style="${P}left:14px;right:14px;bottom:12px;display:flex;justify-content:space-between;align-items:center;font:600 10px 'ID'"><span style="height:26px;line-height:26px;padding:0 11px;border-radius:13px;background:#1F3410;color:#E4F0C2">12-pack · €29</span><span style="font:500 9px 'JB'">0% ABV</span></div>
</div>`);

// 10 · galerie d'art : mur blanc, toile en champs de couleur sous la lumière, cartel
site('Hall Nine','#E9E3D8',420,300,`<div style="${P}inset:0;background:linear-gradient(180deg,#F6F3EE,#E9E3D8 70%,#D9D1C3);color:#161412;overflow:hidden;font-family:'ID'">
  <div style="${P}inset:0;background:radial-gradient(34% 75% at 29% 0%,rgba(255,252,246,.95),rgba(255,252,246,0) 72%)"></div>
  <div style="${P}left:16px;right:16px;top:14px;display:flex;justify-content:space-between;font:500 10.5px 'ID'"><span style="font:700 12px 'ID';letter-spacing:-.01em">Hall Nine</span>${row(['Exhibitions','Visit','Shop'],'gap:14px')}<span>Tickets</span></div>
  <div style="${P}left:38px;top:48px;width:168px;height:206px;background:#6A1424;overflow:hidden;box-shadow:0 24px 28px -16px rgba(40,20,10,.55),0 2px 3px rgba(40,20,10,.25)">
    <div style="${P}left:14px;right:14px;top:16px;height:92px;background:linear-gradient(180deg,#F06A33,#E2502A 60%,#D8482A);border-radius:4px;box-shadow:0 0 6px 3px #E2502A"></div>
    <div style="${P}left:16px;right:16px;top:118px;height:6px;background:#B32A2A;border-radius:3px;box-shadow:0 0 5px 2px #B32A2A;opacity:.85"></div>
    <div style="${P}left:14px;right:14px;top:132px;height:58px;background:#2B0A16;border-radius:4px;box-shadow:0 0 6px 3px #2B0A16"></div>
    <div style="${P}inset:0;background:linear-gradient(180deg,rgba(255,240,220,.16),rgba(255,240,220,0) 45%,rgba(0,0,0,.18))"></div>${grain(.3)}</div>
  <div style="${P}left:236px;top:58px;font:500 9px 'JB';letter-spacing:.08em;color:#6B635A">NOW ON VIEW — HALL 2</div>
  <div style="${P}left:236px;top:74px;font:600 30px/.95 'ID';letter-spacing:-.045em">Mira Olsen</div>
  <div style="${P}left:236px;top:104px;font:italic 400 30px/1 'DS';letter-spacing:-.02em">Weight of Air</div>
  <div style="${P}left:236px;top:150px;width:160px;font:400 11px/1.45 'ID';color:#4A443E">Twelve paintings about the hour before a storm.</div>
  <div style="${P}left:236px;top:202px;font:500 10px/1.6 'JB';color:#161412">12.09 — 30.11.26<br>FREE ENTRY</div>
  <div style="${P}left:236px;bottom:16px;font:600 11px 'ID';border-bottom:1px solid #161412;padding-bottom:2px">Plan your visit →</div>
  <div style="${P}left:38px;bottom:16px;font:500 8.5px 'JB';color:#6B635A">UNTITLED (RUST), 2026 · OIL ON LINEN</div>
</div>`);

/* camaïeu de la couleur dominante : ombres → couleur → clair, appliqué par luminance (comme les teintes de la réf) */
(()=>{ const sh=(h,k)=>{ const c=hex(h); return c.map(v=>v*k); }, li=(h,k)=>{ const c=hex(h); return c.map(v=>v+(255-v)*k); };
  const tab=cs=>[0,1,2].map(j=>cs.map(c=>(c[j]/255).toFixed(3)).join(' '));
  $('fx').innerHTML+=SITES.map((s,i)=>{ const [r,g,b]=tab([sh(s.color,.12),sh(s.color,.55),hex(s.color),li(s.color,.55),li(s.color,.9)]);
    return `<filter id="duo${i}" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".3 .59 .11 0 0 .3 .59 .11 0 0 .3 .59 .11 0 0 0 0 0 1 0"/><feComponentTransfer><feFuncR type="table" tableValues="${r}"/><feFuncG type="table" tableValues="${g}"/><feFuncB type="table" tableValues="${b}"/></feComponentTransfer></filter>`; }).join(''); })();
const DUO=i=>`url(#duo${i})`;
