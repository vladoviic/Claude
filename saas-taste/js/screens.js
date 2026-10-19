/* ============================================================
   Gabarits d'écrans (HTML). Chaque gabarit se dessine dans sa taille de conception
   et se met à l'échelle de son cadre ; on interroge ses éléments par classe.
   ============================================================ */
const q1=(root,s)=>root.querySelector(s), qa=(root,s)=>[...root.querySelectorAll(s)];
const DOT='<span style="display:inline-block;width:9px;height:9px;border-radius:5px;background:var(--accent);margin-left:3px"></span>';
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
