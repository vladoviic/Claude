/* ============================================================
   Gabarits d'écrans (HTML). Chaque gabarit se dessine dans sa taille de conception
   et se met à l'échelle de son cadre ; on interroge ses éléments par classe.
   ============================================================ */
const q1=(root,s)=>root.querySelector(s), qa=(root,s)=>[...root.querySelectorAll(s)];
const DOT='<span style="display:inline-block;width:9px;height:9px;border-radius:5px;background:var(--accent);margin-left:3px"></span>';
const SHAKER_SVG=(stroke='#151413',w=4)=>`<svg viewBox="0 0 88 88" width="100%" height="100%"><g fill="none" stroke="${stroke}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"><path d="M32 38 L56 38 L59 66 Q59 70 55 70 L33 70 Q29 70 29 66 Z"/><path d="M33 38 Q33 22 44 22 Q55 22 55 38"/></g><g fill="${stroke}"><circle cx="40" cy="29" r="1.8"/><circle cx="48" cy="29" r="1.8"/><circle cx="44" cy="33" r="1.8"/></g></svg>`;
const MARK_SVG=`<svg viewBox="0 0 96 96" width="100%" height="100%"><circle cx="48" cy="48" r="48" fill="#FF3D5E"/><path d="M36 66 L60 30" stroke="#EEE9E4" stroke-width="9" stroke-linecap="round"/></svg>`;

/* Met un gabarit de conception (dw×dh) dans un cadre noir de taille w×h */
function framed(el,html,w,h,dw=1240,dh=730,bg='var(--win)'){
  el.className='frame'; el.style.width=w+'px'; el.style.height=h+'px';
  el.innerHTML=`<div class="scr" style="background:${bg}"><div class="design" style="width:${dw}px;height:${dh}px">${html}</div></div>`;
  const d=q1(el,'.design'); const sw=(w-20)/dw, sh=(h-20)/dh; const s=Math.min(sw,sh);
  d.style.transform=`translate(${(((w-20)-dw*s)/2).toFixed(1)}px,${(((h-20)-dh*s)/2).toFixed(1)}px) scale(${s.toFixed(4)})`;
  return d;
}

/* ---------- avant : 5 écrans de SaaS fades (Arial, bleu, placeholder) ---------- */
function tplBoringStock(){ return `<div class="full" style="background:#D9DCE1">
  <svg width="180" height="144" viewBox="0 0 120 96" style="position:absolute;left:50%;top:42%;transform:translate(-50%,-50%)"><rect x="3" y="3" width="114" height="90" rx="6" fill="none" stroke="#A9AEB6" stroke-width="4"/><circle cx="84" cy="30" r="10" fill="#A9AEB6"/><path d="M8 84 L42 44 L66 70 L80 56 L112 84 Z" fill="#A9AEB6"/></svg>
  <div class="ar" style="position:absolute;left:0;right:0;top:66%;text-align:center;font-size:22px;color:#8A8F97">stock_handshake_final_v3.jpg</div></div>`; }
function tplBoringMobile(){ let rows=''; for(let i=0;i<6;i++) rows+=`<div style="position:absolute;left:20px;right:20px;top:${120+i*62}px;height:50px;border-bottom:1px solid #E3E5E9"><div style="position:absolute;left:0;top:6px;width:38px;height:38px;border-radius:19px;background:#C9CDD3"></div><div class="ar" style="position:absolute;left:52px;top:8px;font-size:17px;color:#333">User ${i+1}</div><div class="ar" style="position:absolute;left:52px;top:29px;font-size:13px;color:#999">Lorem ipsum dolor</div></div>`;
  return `<div class="full" style="background:#fff"><div style="position:absolute;left:0;right:0;top:0;height:92px;background:#2D6CDF"></div><div class="ar" style="position:absolute;left:20px;top:44px;font-size:24px;font-weight:700;color:#fff">SaaSly</div>${rows}</div>`; }
function tplBoringReport(){ return `<div class="full" style="background:#fff">
  <div class="ar" style="position:absolute;left:28px;top:22px;font-size:24px;font-weight:700;color:#333">Q3 Synergy Report</div>
  <svg width="220" height="220" viewBox="0 0 32 32" style="position:absolute;left:34px;top:74px"><circle r="16" cx="16" cy="16" fill="#2D6CDF"/><path d="M16 16 L16 0 A16 16 0 0 1 31.2 11 Z" fill="#F4B400"/><path d="M16 16 L31.2 11 A16 16 0 0 1 22 30.8 Z" fill="#DB4437"/><path d="M16 16 L22 30.8 A16 16 0 0 1 3 26 Z" fill="#0F9D58"/></svg>
  ${[0,1,2,3].map(i=>`<div class="ar" style="position:absolute;left:300px;top:${90+i*44}px;font-size:18px;color:#555">■ Synergy metric ${i+1}<span style="position:absolute;left:260px">${[23,41,12,24][i]}%</span></div>`).join('')}</div>`; }
function tplBoringLanding(){ return `<div class="full" style="background:#fff">
  <div style="position:absolute;left:0;right:0;top:0;height:70px;border-bottom:1px solid #E3E5E9"></div><div class="ar" style="position:absolute;left:30px;top:20px;font-size:26px;font-weight:700;color:#2D6CDF">SaaSly</div>
  <div class="ar" style="position:absolute;left:520px;top:26px;font-size:17px;color:#555">Features&nbsp;&nbsp;&nbsp;&nbsp;Pricing&nbsp;&nbsp;&nbsp;&nbsp;About&nbsp;&nbsp;&nbsp;&nbsp;Contact</div>
  <div class="ar" style="position:absolute;left:60px;top:130px;font-size:52px;font-weight:700;color:#222;line-height:1.15">The #1 Platform<br>for Synergy.</div>
  <div class="ar" style="position:absolute;left:62px;top:282px;font-size:20px;color:#777">Leverage best-in-class solutions to empower your workflow.</div>
  <div class="ar" style="position:absolute;left:60px;top:336px;height:58px;padding:0 30px;border-radius:4px;background:#2D6CDF;color:#fff;font-size:20px;font-weight:700;line-height:58px;box-shadow:0 6px 10px rgba(0,0,0,.4)">Get Started Today!</div>
  <div style="position:absolute;right:50px;top:110px;width:330px;height:280px;background:#D9DCE1"></div><div class="ar" style="position:absolute;right:120px;top:240px;font-size:16px;color:#8A8F97">hero_image.png</div></div>`; }

/* ---------- landing générée (héros 3D) ---------- */
function tplLanding(){ return `<div class="full" style="background:#F3EFEA">
  <div class="ln-nav" style="left:52px;font-family:'ID';font-weight:600;font-size:30px;color:var(--ink);letter-spacing:-0.035em;top:30px">saasly${DOT}</div>
  <div class="ln-nav" style="left:430px">(01) product&nbsp;&nbsp;&nbsp;(02) pricing&nbsp;&nbsp;&nbsp;(03) changelog</div>
  <div class="ln-nav" style="left:1050px;top:24px;height:48px;line-height:48px;padding:0 22px;border-radius:24px;background:var(--ink);color:#F3EFEA;font-family:'ID';font-size:18px;font-weight:500">Get saasly</div>
  <div class="lh lh1"><span>Dashboards</span></div>
  <canvas class="lshaker" width="600" height="660" style="position:absolute;left:680px;top:40px;width:600px;height:660px"></canvas>
  <div class="lh lh2"><span>with&nbsp;</span><em>taste.</em></div>
  <div class="m" style="position:absolute;left:56px;top:648px;font-size:15px;color:var(--grey)">Same SaaS. Now people actually want to open it.</div>
  <div style="position:absolute;left:1000px;top:632px;height:60px;padding:0 28px;border-radius:30px;background:var(--ink);color:#F3EFEA;font-size:21px;line-height:60px">Start free →</div></div>`; }

/* ---------- palette ⌘K ---------- */
function tplPalette(){ return `<div class="full" style="background:#121110">
  <canvas class="kbg" width="620" height="365" style="position:absolute;inset:0;width:100%;height:100%;opacity:.55"></canvas>
  <div style="position:absolute;inset:0;background:radial-gradient(60% 70% at 50% 45%,rgba(18,17,16,.15),rgba(18,17,16,.85))"></div>
  <div class="kpanel">
    <div class="kin"><span class="kchip">⌘K</span><span class="ktext">remove Arial</span><span class="kchip" style="position:absolute;right:26px;top:26px">esc</span></div>
    <div class="klab" style="top:104px">BEST MATCH</div>
    <div class="krow ksel" style="top:128px;background:rgba(255,61,94,.5)"><span class="ktile" style="background:var(--accent)">+</span><span>Add <em style="font-size:34px">taste</em></span><span class="kkeys"><span class="kchip">⌘</span><span class="kchip" style="background:#FF3D5E;color:#fff">⏎</span></span></div>
    <div class="klab" style="top:210px">SUGGESTIONS</div>
    <div class="krow" style="top:234px"><span class="ktile">Aa</span>Remove Arial<span class="kcat">Typography</span></div>
    <div class="krow" style="top:292px"><span class="ktile">#</span>Replace #2D6CDF<span class="kcat">Color</span></div>
    <div class="krow" style="top:350px"><span class="ktile">▢</span>Delete drop shadows (2009)<span class="kcat">Effects</span></div>
    <div class="krow" style="top:408px"><span class="ktile">@</span>Rename “User” to a human<span class="kcat">Copy</span></div>
  </div>
  <div style="position:absolute;left:50%;top:624px;transform:translateX(-50%);height:52px;padding:0 24px;border-radius:26px;background:var(--accent);color:#fff;font-size:19px;line-height:52px;white-space:nowrap">✓&nbsp; Taste added to 47 screens</div></div>`; }

/* ---------- pricing ---------- */
function tplPricing(){ const strike=t=>`<span style="background:linear-gradient(var(--accent),var(--accent)) 0 52%/100% 2px no-repeat;color:#A39C94">${t}</span>`;
  return `<div class="full" style="background:#F3EFEA">
  <div style="position:absolute;left:60px;top:46px;font-size:66px;letter-spacing:-0.04em;line-height:1">Pick your <em style="font-size:78px;color:var(--accent)">flavor.</em></div>
  <div class="m" style="position:absolute;left:62px;top:132px;font-size:15px;color:var(--grey)">prices in taste, billed monthly</div>
  <div class="m" style="position:absolute;left:868px;top:76px;font-size:16px;color:var(--grey)">bland</div>
  <div style="position:absolute;left:934px;top:68px;width:68px;height:36px;border-radius:18px;background:var(--accent)"><div style="position:absolute;left:36px;top:4px;width:28px;height:28px;border-radius:14px;background:#fff"></div></div>
  <div class="m" style="position:absolute;left:1016px;top:76px;font-size:16px">tasteful</div>
  <div class="pcol" style="left:60px;background:#E4DED7"><div class="pname">Bland</div><div class="pprice">$0<span class="m pper">/forever</span></div>
    ${['– Arial','– #2D6CDF','– Stock handshakes','– Lorem ipsum'].map((t,i)=>`<div class="pfeat" style="top:${230+i*40}px">${strike(t)}</div>`).join('')}
    <div class="pbtn" style="border:2px solid rgba(21,20,19,.2);color:#9A938B">Meh</div></div>
  <div class="pcol" style="left:440px;background:var(--ink);color:#F3EFEA;transform:scale(1.035)"><div class="chip" style="right:26px;top:28px;background:var(--accent);color:#fff">most picked</div>
    <div class="pname">Tasteful</div><div class="pprice">$49<span class="m pper" style="color:#8E877F">/mo</span></div>
    ${['Real typography','One accent. Used well.','Motion that lands','3D that means it'].map((t,i)=>`<div class="pfeat" style="top:${230+i*40}px"><b>●</b> ${t}</div>`).join('')}
    <div class="pbtn" style="background:#F3EFEA;color:var(--ink)">Get taste →</div></div>
  <div class="pcol" style="left:820px;background:#ECE6DF;box-shadow:inset 0 0 0 2px rgba(21,20,19,.08)"><div class="pname">Chef</div><div class="pprice" style="font-size:62px;top:102px">Let’s talk</div>
    ${['→ Brand from scratch','→ Motion system','→ A launch film like this one'].map((t,i)=>`<div class="pfeat" style="top:${230+i*40}px">${t}</div>`).join('')}
    <div class="pbtn" style="border:2px solid var(--ink)">Book a tasting →</div></div></div>`; }

/* ---------- planning « Taste plan » (plein cadre) ---------- */
const PLAN_X0=330, PLAN_COL=226;
const PLAN_CHIPS=[
  ['Kill Arial','#FF3D5E','#fff',0,2,370],['Brand sprint','#FFC7A1',null,1,3,460],['Type system','#C7B8FF',null,3,2,550],
  ['One accent','#A9E7F2',null,2,2,640],['Motion pass','#FFF0B5',null,4,2,370],['3D hero','#FFA6C9',null,5,2,460],
  ['Launch film','#FF3D5E','#fff',6,1,550],['Ship it','#151413','#F3EFEA',6,1,730],['Rename “User”','#E4DED7',null,0,2,820],['No stock photos','#A9E7F2',null,4,2,820]];
function tplPlan(){ const days=[22,23,24,25,26,27,28], dn=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
  let h=`<div class="plan"><div class="side"><div style="position:absolute;left:36px;top:40px;font-size:30px;font-weight:600;color:#F3EFEA;letter-spacing:-0.035em">saasly${DOT}</div>
    ${['Overview','Taste plan','Clients','Reports','Settings'].map((t,i)=>`<div class="sitem" style="top:${130+i*48}px;${i==1?'color:#F3EFEA':''}">${t}</div>`).join('')}</div>
    <div class="ptitle" style="position:absolute;left:${PLAN_X0}px;top:56px;font-size:46px;letter-spacing:-0.03em">Taste plan</div>
    <div class="m" style="position:absolute;left:${PLAN_X0+2}px;top:116px;font-size:16px;color:var(--grey)">brand · ui · motion — for saasly</div>`;
  days.forEach((d,i)=>{ const x=PLAN_X0+i*PLAN_COL; h+=`<div class="day" style="left:${x}px;top:180px">${d}</div><div class="dname" style="left:${x+4}px;top:258px">${dn[i]}</div><div class="col" style="left:${x-14}px"></div>`; });
  PLAN_CHIPS.forEach(([t,bg,fg,c,span,y],i)=>{ h+=`<div class="pchip" data-i="${i}" style="left:${PLAN_X0+c*PLAN_COL-6}px;top:${y}px;width:${span*PLAN_COL-20}px;background:${bg};color:${fg||'#151413'}"><b>${t}</b><i>${dn[c]} ${days[c]} – ${dn[Math.min(6,c+span-1)]} ${days[Math.min(6,c+span-1)]} · #TS-${2840+i*17}</i></div>`; });
  return h+'</div>'; }

/* ---------- « My clients » dans un navigateur ---------- */
function tplClients(){ const rows=[['Saasly','Arial · #2D6CDF','Inter · one accent'],['Bluedesk','stock handshakes','3D hero'],['Synergyo','lorem ipsum','real copy'],['Dashify','drop shadows (2009)','motion that lands']];
  return `<div class="full" style="background:#141312">
  <div class="bar"><span style="position:absolute;left:24px;top:22px">workspace</span><span class="tbtn" style="left:130px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">Preview</span>
    <span style="position:absolute;left:250px;top:20px;letter-spacing:12px;color:#A49D96">○ □ ○</span>
    <span style="position:absolute;right:300px;top:20px;letter-spacing:14px;color:#6d6760">◎ ∿ ‹/›</span>
    <span class="tbtn" style="right:130px;background:#fff;box-shadow:0 0 0 1px #E6E1DB">Share</span><span class="tbtn" style="right:24px;background:var(--ink);color:#fff">Publish</span></div>
  <div style="position:absolute;left:0;right:0;top:64px;height:330px;overflow:hidden"><canvas class="cbg" width="580" height="110" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,18,0) 40%,rgba(20,19,18,.75))"></div>
    <div style="position:absolute;left:36px;top:150px;font-size:84px;color:#fff;letter-spacing:-0.045em">My clients</div>
    <div class="m" style="position:absolute;left:40px;top:250px;font-size:17px;color:rgba(255,255,255,.75)">before → after, so far</div>
    <canvas class="cshaker" width="300" height="330" style="position:absolute;right:120px;top:0;width:300px;height:330px"></canvas></div>
  <div class="m" style="position:absolute;left:36px;right:36px;top:412px;height:40px;font-size:14px;color:#8E877F"><span style="position:absolute;left:0">CLIENT</span><span style="position:absolute;left:470px">BEFORE</span><span style="position:absolute;left:900px">AFTER</span><span style="position:absolute;right:20px">STATUS</span></div>
  ${rows.map((r,i)=>`<div class="trow" style="top:${452+i*84}px"><span class="tcell" style="left:0;font-size:24px">${r[0]}</span><span class="tcell m" style="left:470px;color:#8E877F;font-size:17px;text-decoration:line-through">${r[1]}</span><span class="tcell" style="left:900px">${r[2]}</span><span class="tcell" style="right:20px"><span class="tchip">● tasteful</span></span></div>`).join('')}</div>`; }

/* ---------- chat IA + page produit ---------- */
function tplChat(){ return `<div class="full" style="background:#F3EFEA">
  <div class="chatp"><div style="position:absolute;left:32px;top:30px;font-size:22px;font-weight:600;letter-spacing:-0.03em">saasly${DOT}<span class="m" style="font-weight:400;font-size:14px;color:var(--grey);margin-left:12px">taste chat</span></div>
    <div class="bubble" style="top:110px">Add a 3D hero. Make it <em style="font-size:24px">salty.</em></div>
    <div class="ctext" style="top:220px">Added a fluted glass shaker with a #FF3D5E cap. Removed 1 stock handshake. Kept one accent, used well.</div>
    <div class="citem" style="top:350px">✓ installed three.js</div><div class="citem" style="top:384px">✓ removed handshake.jpg</div><div class="citem" style="top:418px">✓ approved by Vladan</div>
    <div class="m" style="position:absolute;left:32px;top:480px;height:40px;line-height:40px;padding:0 18px;border-radius:20px;background:var(--ink);color:#fff;font-size:14px">Approve</div>
    <div class="m" style="position:absolute;left:32px;top:860px;font-size:13px;color:var(--grey)">SUGGESTIONS</div>
    ${['More salt','Dark mode','Make it spin'].map((t,i)=>`<div class="m" style="position:absolute;left:${32+i*180}px;top:890px;height:38px;line-height:36px;padding:0 14px;border-radius:19px;border:1px solid #D9D2CA;font-size:14px;color:#5f5952">${t}</div>`).join('')}
    <div style="position:absolute;left:24px;right:24px;bottom:28px;height:84px;border-radius:20px;background:#fff;box-shadow:0 0 0 1px #E6E1DB"><span style="position:absolute;left:22px;top:28px;font-size:19px;color:#A39C94;font-weight:400">What would you like to change?</span><span style="position:absolute;right:16px;top:16px;width:52px;height:52px;border-radius:14px;background:var(--ink)"></span></div></div>
  <div style="position:absolute;left:640px;top:36px;font-size:22px;font-weight:600;letter-spacing:-0.03em">saasly${DOT}</div>
  <div style="position:absolute;left:640px;top:96px;font-size:44px;letter-spacing:-0.03em">Taste Shaker</div>
  <div class="m" style="position:absolute;left:643px;top:154px;font-size:16px;color:var(--grey)">built for flavor</div>
  <div style="position:absolute;left:630px;top:200px;width:918px;height:760px;border-radius:24px;overflow:hidden;background:radial-gradient(70% 70% at 50% 60%,#FBF8F4,#E9E2DA)"><canvas class="pshaker" width="918" height="760" style="position:absolute;inset:0;width:100%;height:100%"></canvas><canvas class="pthermal" width="459" height="380" style="position:absolute;inset:0;width:100%;height:100%;display:none"></canvas></div>
  <div class="spec"><div style="position:absolute;left:32px;top:36px;font-size:26px">Taste Shaker</div><div class="m" style="position:absolute;left:32px;top:74px;font-size:14px;color:#8E877F">SPEC</div>
    ${[['glass','fluted'],['cap','#FF3D5E'],['salt','100%'],['arial','0'],['stock photos','0'],['accent','one']].map((r,i)=>`<div class="srow" style="top:${130+i*64}px">${r[0]}<b>${r[1]}</b></div>`).join('')}
    <div style="position:absolute;left:32px;right:32px;bottom:36px;height:64px;border-radius:32px;background:var(--accent);color:#fff;font-size:21px;line-height:64px;text-align:center">Add to taste →</div></div></div>`; }

/* écrans fades supplémentaires pour le collage */
function tplBoringLogin(){ return `<div class="full" style="background:#F4F5F7"><div class="ar" style="position:absolute;left:0;right:0;top:40px;text-align:center;font-size:26px;font-weight:700;color:#2D6CDF">SaaSly</div>
  <div style="position:absolute;left:60px;right:60px;top:100px;height:44px;border:1px solid #C9CDD3;background:#fff"></div><div class="ar" style="position:absolute;left:72px;top:112px;font-size:16px;color:#999">Email</div>
  <div style="position:absolute;left:60px;right:60px;top:160px;height:44px;border:1px solid #C9CDD3;background:#fff"></div><div class="ar" style="position:absolute;left:72px;top:172px;font-size:16px;color:#999">Password</div>
  <div class="ar" style="position:absolute;left:60px;right:60px;top:224px;height:46px;background:#2D6CDF;color:#fff;font-size:18px;font-weight:700;line-height:46px;text-align:center;box-shadow:0 4px 8px rgba(0,0,0,.35)">LOGIN</div></div>`; }
function tplBoringTable(){ return `<div class="full" style="background:#fff">${['ID','Name','Status','Date'].map((h,i)=>`<div class="ar" style="position:absolute;left:${20+i*95}px;top:20px;font-size:15px;font-weight:700;color:#333">${h}</div>`).join('')}
  ${[0,1,2,3,4,5].map(j=>`<div style="position:absolute;left:14px;right:14px;top:${50+j*40}px;height:40px;background:${j%2?'#fff':'#F2F4F7'}"></div>`+['#'+(1023+j),'User '+(j+1),'Active','01/0'+(j+1)].map((t,i)=>`<div class="ar" style="position:absolute;left:${20+i*95}px;top:${62+j*40}px;font-size:14px;color:${i==2?'#2D6CDF':'#555'}">${t}</div>`).join('')).join('')}</div>`; }
function tplBoringEmail(){ return `<div class="full" style="background:#fff"><div style="position:absolute;left:0;right:0;top:0;height:54px;background:#2D6CDF"></div><div class="ar" style="position:absolute;left:20px;top:16px;font-size:20px;font-weight:700;color:#fff">SaaSly Newsletter</div>
  <div class="ar" style="position:absolute;left:24px;top:80px;font-size:20px;color:#333">Dear User,</div><div class="ar" style="position:absolute;left:24px;top:116px;right:24px;font-size:15px;color:#777;line-height:1.5;white-space:normal">We are excited to announce our new synergy-driven features. Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
  <div class="ar" style="position:absolute;left:24px;top:220px;height:40px;padding:0 20px;background:#2D6CDF;color:#fff;font-size:15px;font-weight:700;line-height:40px">Click Here!</div></div>`; }
