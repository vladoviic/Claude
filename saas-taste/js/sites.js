/* ============================================================
   Ouverture (54-119) : l'éclatement de sites. Onze sites recréés dans l'esprit des Sites of the Day
   d'Awwwards (mises en page de référence, noms inventés), chacun bâti sur sa couleur dominante.
   Pendant les teintes de la réf (62-69, 114-116), chaque carte passe en camaïeu de SA couleur.
   ============================================================ */
const SITES=[];
function site(name,color,w,h,html){ SITES.push({name,color,w,h,html}); return SITES.length-1; }
const sNav=(items,c,f='ID',sz=13)=>`<div style="display:flex;gap:${sz*1.6}px;font:500 ${sz}px ${f};color:${c}">${items.map(t=>`<span>${t}</span>`).join('')}</div>`;

// 0 · pilote automobile : lime électrique sur noir, casque, chiffres géants (esprit des sites de pilotes F1)
site('KOVA','#D4FF3F',884,405,`<div style="position:absolute;inset:0;background:#0E0F0C;color:#D4FF3F;overflow:hidden">
  <div style="position:absolute;left:28px;top:22px;right:28px;display:flex;justify-content:space-between;align-items:center">
    <span style="font:800 22px 'AV';font-stretch:125%;letter-spacing:-.02em">KOVA</span>${sNav(['Calendar','Helmets','Store','On track'],'#D4FF3F','ID',12)}
    <span style="font:600 11px 'JB';border:1px solid #D4FF3F;border-radius:20px;padding:6px 12px">NEXT · MONACO 24.05</span></div>
  <div style="position:absolute;left:22px;bottom:-34px;font:900 300px/0.8 'AV';font-stretch:62%;letter-spacing:-.04em;color:#D4FF3F">07</div>
  <svg viewBox="0 0 400 360" style="position:absolute;left:214px;top:70px;width:400px;height:360px;filter:drop-shadow(0 30px 40px #000)">
    <defs><radialGradient id="kvS" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="#FAFFE0"/><stop offset=".18" stop-color="#E4FF7A"/><stop offset=".45" stop-color="#C6F02A"/><stop offset=".8" stop-color="#5E7A0C"/><stop offset="1" stop-color="#1C2605"/></radialGradient>
      <linearGradient id="kvV" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A4256"/><stop offset=".35" stop-color="#0D1018"/><stop offset=".6" stop-color="#1E2A3F"/><stop offset="1" stop-color="#05070B"/></linearGradient>
      <linearGradient id="kvH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
    <path d="M58 236 C38 120 122 26 232 28 C334 30 386 112 372 206 C364 258 330 302 278 316 L122 322 C86 320 64 284 58 236 Z" fill="url(#kvS)"/>
    <path d="M90 118 C150 52 260 40 340 84" fill="none" stroke="#F4FFD0" stroke-width="14" stroke-linecap="round" opacity=".9"/>
    <path d="M78 150 C140 82 262 70 352 116" fill="none" stroke="#0E0F0C" stroke-width="6" stroke-linecap="round" opacity=".8"/>
    <path d="M150 152 C196 122 300 118 364 150 L358 208 C302 220 214 224 152 208 C134 192 134 168 150 152 Z" fill="url(#kvV)" stroke="#0E0F0C" stroke-width="5"/>
    <path d="M168 160 C214 138 290 136 346 156" fill="none" stroke="url(#kvH)" stroke-width="7" stroke-linecap="round"/>
    <path d="M122 322 L278 316 C292 300 300 282 296 262 L130 268 C120 284 118 304 122 322 Z" fill="#0E0F0C" opacity=".85"/>
    <circle cx="104" cy="226" r="26" fill="#0E0F0C"/><text x="104" y="235" text-anchor="middle" font-family="AV" font-weight="900" font-stretch="70%" font-size="26" fill="#D4FF3F">07</text>
  </svg>
  <div style="position:absolute;right:28px;top:110px;width:250px;font:500 15px/1.35 'ID';color:#D4FF3F">Fast is a feeling. <span style="opacity:.55">Season 26 starts on the street where it all began.</span></div>
  <div style="position:absolute;right:28px;bottom:26px;display:flex;gap:28px;font:700 46px/1 'AV';font-stretch:75%"><span>P1<small style="font:500 11px 'JB';display:block;opacity:.6">MIAMI</small></span><span>P3<small style="font:500 11px 'JB';display:block;opacity:.6">IMOLA</small></span><span>P2<small style="font:500 11px 'JB';display:block;opacity:.6">BAKU</small></span></div>
</div>`);

// 1 · festival de création : bleu électrique, grotesque blanche géante, bandeau défilant
site('Driftweek','#0039FF',740,480,`<div style="position:absolute;inset:0;background:#0039FF;color:#fff;overflow:hidden">
  <div style="position:absolute;left:26px;top:20px;right:26px;display:flex;justify-content:space-between;font:500 12px 'JB'"><span>DRIFTWEEK ®</span><span>LISBON — 02/06 → 07/06/26</span><span>(TICKETS)</span></div>
  <div style="position:absolute;left:20px;top:64px;font:800 156px/0.84 'AV';font-stretch:100%;letter-spacing:-.06em">Drift<br>week<span style="font:400 italic 156px 'DS';letter-spacing:-.03em">26</span></div>
  <div style="position:absolute;right:26px;top:84px;width:200px;font:500 14px/1.35 'ID'">Six days of talks, raves and badly parked bikes. 140 speakers. One river.</div>
  <div style="position:absolute;right:30px;top:210px;width:150px;height:150px;border-radius:50%;border:1.5px solid #fff;display:grid;place-items:center;font:600 13px 'JB';text-align:center">GET<br>TICKETS<br>→</div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:54px;background:#fff;color:#0039FF;font:800 30px/54px 'AV';font-stretch:120%;white-space:nowrap;letter-spacing:-.02em">✺ TALKS ✺ WORKSHOPS ✺ NIGHT RIDES ✺ TALKS ✺ WORKSHOPS ✺</div>
</div>`);

// 2 · application mobile : un petit monde en 3D à travers lequel on envoie une lettre (esprit portfolio WebGL)
site('Courier','#8FC8FF',320,493,`<div style="position:absolute;inset:0;background:linear-gradient(180deg,#BFE1FF 0,#8FC8FF 60%,#6FAEF2);color:#0B2A52;overflow:hidden">
  <div style="position:absolute;left:18px;top:16px;right:18px;display:flex;justify-content:space-between;font:700 15px 'SY'"><span>courier</span><span style="font:500 11px 'JB'">☰</span></div>
  <div style="position:absolute;left:40px;top:96px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFFDF5 0,#FFE3A8 12%,#9BD67F 30%,#4FA35E 55%,#245C49 80%,#163A3A);box-shadow:0 40px 60px -30px rgba(11,42,82,.6)">
    <div style="position:absolute;left:110px;top:-18px;width:12px;height:40px;background:#FF8A3D;border-radius:3px"></div><div style="position:absolute;left:122px;top:-18px;width:26px;height:16px;background:#fff;border-radius:2px"></div>
    <div style="position:absolute;left:150px;top:70px;width:34px;height:28px;background:#fff;border-radius:3px;transform:rotate(12deg)"></div></div>
  <div style="position:absolute;left:18px;right:18px;top:336px;font:700 31px/0.95 'SY';letter-spacing:-.03em">A tiny world,<br>one letter<br>at a time.</div>
  <div style="position:absolute;left:18px;bottom:18px;height:42px;padding:0 18px;border-radius:21px;background:#0B2A52;color:#fff;font:600 13px/42px 'ID'">Send a letter ✉</div>
</div>`);

// 3 · studio de marque : jaune, typo noire massive, pastilles autocollantes
site('Sunday®','#FDCD34',550,297,`<div style="position:absolute;inset:0;background:#FDCD34;color:#111;overflow:hidden">
  <div style="position:absolute;left:20px;top:16px;right:20px;display:flex;justify-content:space-between;font:600 12px 'ID'"><span style="font:700 16px 'SY'">Sunday®</span><span>Work · Studio · Say hi</span></div>
  <div style="position:absolute;left:18px;top:48px;font:700 52px/0.92 'SY';letter-spacing:-.045em">We make<br>brands people<br><span style="font:italic 400 56px 'DS';letter-spacing:-.02em">miss.</span></div>
  <div style="position:absolute;right:30px;bottom:26px;width:110px;height:110px;border-radius:50%;background:#111;color:#FDCD34;display:grid;place-items:center;font:700 13px/1.1 'SY';text-align:center;transform:rotate(-12deg)">OPEN FOR<br>SUMMER ’26</div>
  <div style="position:absolute;left:20px;bottom:22px;display:flex;gap:8px">${['Branding','Packaging','Motion'].map(t=>`<span style="font:600 12px 'ID';border:1.5px solid #111;border-radius:20px;padding:6px 12px">${t}</span>`).join('')}</div>
</div>`);

// 4 · hôtel de luxe : sable, serif, grande photo, barre de réservation
site('Maison Dune','#D4C6B9',830,440,`<div style="position:absolute;inset:0;background:#D4C6B9;color:#2B241E;overflow:hidden">
  <div style="position:absolute;left:30px;top:22px;right:30px;display:flex;justify-content:space-between;align-items:center;font:500 12px 'ID';letter-spacing:.08em"><span>ROOMS</span><span style="font:400 26px 'DS';letter-spacing:.02em">Maison Dune</span><span>RESERVE</span></div>
  <img src="img/room_eye.jpg" style="position:absolute;left:30px;top:74px;width:480px;height:320px;object-fit:cover;border-radius:2px">
  <div style="position:absolute;left:536px;top:84px;width:280px;font:400 40px/1 'DS';letter-spacing:-.02em;white-space:nowrap">Slow mornings<br><span style="font-style:italic">by the dunes.</span></div>
  <div style="position:absolute;left:540px;top:196px;width:250px;font:400 13px/1.45 'ID';color:#5A4F45">Twelve rooms, one garden, no televisions. Breakfast until noon, always.</div>
  <div style="position:absolute;left:540px;top:338px;width:260px;height:46px;border:1px solid #2B241E;display:flex;justify-content:space-between;align-items:center;padding:0 14px;box-sizing:border-box;font:500 11px 'ID'"><span>14—18 Jun · 2 guests</span><span>Book →</span></div>
</div>`);

// 5 · studio créatif : violet profond, orbe néon, grille
site('Volta.studio™','#6E2BD9',420,300,`<div style="position:absolute;inset:0;background:#1A0B3B;color:#E9DCFF;overflow:hidden">
  <div style="position:absolute;inset:0;background-image:linear-gradient(#ffffff10 1px,transparent 1px),linear-gradient(90deg,#ffffff10 1px,transparent 1px);background-size:35px 35px"></div>
  <div style="position:absolute;left:150px;top:40px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#FFFFFF 0,#E2C8FF 10%,#A46BFF 30%,#6E2BD9 55%,#2A0F66 80%);filter:blur(.5px);box-shadow:0 0 90px 10px #6E2BD9aa"></div>
  <div style="position:absolute;left:16px;top:14px;font:600 13px 'UB'">Volta.studio™</div>
  <div style="position:absolute;left:16px;bottom:16px;font:500 40px/0.92 'UB';letter-spacing:-.05em;color:#fff">Digital<br>experiences<br>with gravity.</div>
  <div style="position:absolute;right:14px;top:14px;font:500 10px 'JB'">(SHOWREEL 26)</div>
</div>`);

// 6 · agence d'architecture : sauge, serif fin, photo, filets
site('Atelier Mur','#B8C2A9',420,300,`<div style="position:absolute;inset:0;background:#B8C2A9;color:#1F2419;overflow:hidden">
  <div style="position:absolute;left:16px;top:14px;right:16px;display:flex;justify-content:space-between;font:500 11px 'ID';letter-spacing:.06em"><span>ATELIER MUR</span><span>PROJECTS (24)</span></div>
  <div style="position:absolute;left:16px;right:16px;top:38px;height:1px;background:#1F2419"></div>
  <img src="img/room_top.jpg" style="position:absolute;left:206px;top:54px;width:198px;height:230px;object-fit:cover">
  <div style="position:absolute;left:16px;top:58px;width:180px;font:400 38px/1 'DS';letter-spacing:-.02em">Rooms that hold the light.</div>
  <div style="position:absolute;left:16px;bottom:16px;font:500 10px/1.5 'JB'">N° 014 — CASA PINHAL<br>LISBON · 2026</div>
</div>`);

// 7 · sommet fintech : bleu nuit, chiffres énormes
site('Payline Summit','#0A1AA8',440,300,`<div style="position:absolute;inset:0;background:#06107A;color:#fff;overflow:hidden">
  <div style="position:absolute;left:16px;top:14px;right:16px;display:flex;justify-content:space-between;font:600 12px 'ID'"><span>payline</span><span style="font:500 10px 'JB';opacity:.7">SUMMIT · BLR</span></div>
  <div style="position:absolute;left:12px;top:30px;font:900 170px/0.85 'AV';font-stretch:75%;letter-spacing:-.05em;color:#fff">S26</div>
  <div style="position:absolute;left:16px;bottom:18px;width:220px;font:500 14px/1.3 'ID'">Money moves faster than meetings. 2 days, 60 founders.</div>
  <div style="position:absolute;right:16px;bottom:18px;width:120px;height:44px;border-radius:22px;background:#9CF2FF;color:#06107A;font:700 13px/44px 'ID';text-align:center">Register</div>
  <div style="position:absolute;right:16px;top:52px;width:150px;height:150px;border-radius:24px;background:linear-gradient(135deg,#2A3BFF,#9CF2FF);transform:rotate(14deg)"></div>
</div>`);

// 8 · baskets / sport : vert, typo détourée géante, produit
site('FIELD/ONE','#42C82A',480,280,`<div style="position:absolute;inset:0;background:#42C82A;color:#0B1A08;overflow:hidden">
  <div style="position:absolute;left:-6px;top:30px;font:400 190px/0.8 'AN';color:transparent;-webkit-text-stroke:2px #0B1A08;letter-spacing:-.01em">FIELD</div>
  <svg viewBox="0 0 300 140" style="position:absolute;left:150px;top:78px;width:300px;height:140px;transform:rotate(-10deg);filter:drop-shadow(0 26px 18px #0B1A0870)">
    <path d="M14 104 C40 104 70 70 96 52 L132 34 C150 26 170 30 180 44 C200 70 240 76 276 84 C292 88 296 104 290 114 Z" fill="#F4F4EE"/>
    <path d="M10 112 L292 112 C294 124 286 132 272 132 L24 132 C12 132 6 124 10 112 Z" fill="#0B1A08"/>
    <path d="M60 96 C110 70 170 70 240 92" fill="none" stroke="#42C82A" stroke-width="12" stroke-linecap="round"/>
    <path d="M100 56 L150 86 M118 46 L168 80 M136 38 L184 72" stroke="#0B1A08" stroke-width="5" stroke-linecap="round"/>
    <path d="M176 44 C186 30 200 26 214 32" fill="none" stroke="#0B1A08" stroke-width="6" stroke-linecap="round"/>
  </svg>
  <div style="position:absolute;left:16px;top:12px;font:400 20px 'AN'">FIELD/ONE</div>
  <div style="position:absolute;right:16px;bottom:14px;font:700 12px 'ID'">Run 01 — €180 →</div>
</div>`);

// 9 · audio (mobile) : orange brûlé, enceinte ronde
site('Kiln Audio','#FF6B1A',240,380,`<div style="position:absolute;inset:0;background:#FF6B1A;color:#1E0D02;overflow:hidden">
  <div style="position:absolute;left:14px;top:12px;font:700 15px 'UB'">kiln</div>
  <div style="position:absolute;left:40px;top:60px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle,#1E0D02 0 22%,#3A1A06 23% 46%,#1E0D02 47% 49%,#FF8B45 50% 100%);box-shadow:0 24px 40px -20px #1E0D02"></div>
  <div style="position:absolute;left:14px;top:244px;font:600 30px/0.95 'UB';letter-spacing:-.05em">Warm<br>sound.</div>
  <div style="position:absolute;left:14px;bottom:14px;right:14px;display:flex;justify-content:space-between;font:500 11px 'JB'"><span>K-1 · €390</span><span>ADD +</span></div>
</div>`);

// 10 · labo de création WebGL : noir, sphère de particules lumineuses
site('Lumen Lab','#E9E6DD',420,300,`<div style="position:absolute;inset:0;background:#0B0B0E;color:#E9E6DD;overflow:hidden">
  <div style="position:absolute;left:120px;top:30px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 50% 50%,transparent 0 40%,#E9E6DD33 41% 41.5%,transparent 42% 55%,#E9E6DD22 56% 56.5%,transparent 57%),repeating-conic-gradient(from 0deg,#E9E6DD66 0 1deg,transparent 1deg 7deg);-webkit-mask:radial-gradient(circle,#000 0 60%,transparent 70%);mask:radial-gradient(circle,#000 0 60%,transparent 70%)"></div>
  <div style="position:absolute;left:196px;top:106px;width:88px;height:88px;border-radius:50%;background:radial-gradient(circle,#fff,#E9E6DD 30%,transparent 70%);filter:blur(4px)"></div>
  <div style="position:absolute;left:16px;top:14px;font:500 12px 'JB'">LUMEN LAB / R&D</div>
  <div style="position:absolute;left:16px;bottom:16px;font:400 italic 40px/0.95 'DS'">Light, but<br>make it think.</div>
  <div style="position:absolute;right:16px;bottom:18px;font:500 10px 'JB';text-align:right">FIG. 03<br>PARTICLES 120K</div>
</div>`);

/* camaïeu de la couleur dominante : ombres → couleur → clair, appliqué par luminance (comme les teintes de la réf) */
(()=>{ const sh=(h,k)=>{ const c=hex(h); return c.map(v=>v*k); }, li=(h,k)=>{ const c=hex(h); return c.map(v=>v+(255-v)*k); };
  const tab=cs=>[0,1,2].map(j=>cs.map(c=>(c[j]/255).toFixed(3)).join(' '));
  $('fx').innerHTML+=SITES.map((s,i)=>{ const [r,g,b]=tab([sh(s.color,.12),sh(s.color,.55),hex(s.color),li(s.color,.55),li(s.color,.9)]);
    return `<filter id="duo${i}" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".3 .59 .11 0 0 .3 .59 .11 0 0 .3 .59 .11 0 0 0 0 0 1 0"/><feComponentTransfer><feFuncR type="table" tableValues="${r}"/><feFuncG type="table" tableValues="${g}"/><feFuncB type="table" tableValues="${b}"/></feComponentTransfer></filter>`; }).join(''); })();
const DUO=i=>`url(#duo${i})`;
