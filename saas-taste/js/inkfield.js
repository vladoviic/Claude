/* ============================================================
   Champ d'encre plein cadre (WebGL, pleine résolution) pour la plongée dans le trait (V07, 219-233).
   Mode 0 : on plonge dans le trait M3 ; le bord et les fibres sont calculés en coordonnées du papier,
            avec des octaves qui suivent le zoom : du détail nouveau apparaît à chaque image.
   Mode 1 : l'encre sèche à travers les fibres, la dernière qui reste est le carré de la landing.
   ============================================================ */
const INK=(()=>{
  const c=document.createElement('canvas'); c.width=W; c.height=H;
  c.style.cssText=`position:absolute;inset:0;width:${W}px;height:${H}px;pointer-events:none;z-index:40;display:none`;
  const gl=c.getContext('webgl',{preserveDrawingBuffer:true,antialias:false,premultipliedAlpha:true,alpha:true});
  if(!gl) return null;
  const vs=`attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}`;
  const fs=`precision highp float;
  uniform vec2 R, O; uniform float Z, ZN, MODE, DRY, SIG, RR, WET; uniform vec4 RECT;
  uniform vec3 P[64]; uniform float NP;
  float h(vec2 p){ p=fract(p*vec2(.1031,.1030)); p+=dot(p,p.yx+33.33); return fract((p.x+p.y)*p.x); }
  float vn(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.-2.*f);
    return mix(mix(h(i),h(i+vec2(1,0)),u.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),u.x),u.y); }
  // fibres : bruit « en crête », étiré 4:1 selon une direction qui change d'une octave à l'autre (fibres emmêlées)
  // fibres : bruit « en crête » étiré 4:1 ; deux couches croisées par octave, directions fixes et différentes d'une octave à l'autre
  float fib(vec2 q){ float v=0., a=.5, tot=0.;
    float lz=log2(max(ZN,1.)); float k0=floor(lz), fr=fract(lz);
    for(int i=0;i<9;i++){ float k=float(i)+k0; float r=0.;
      for(int j=0;j<2;j++){ float ang=k*2.399+float(j)*1.31; mat2 m=mat2(cos(ang),-sin(ang),sin(ang),cos(ang));
        vec2 s=m*q*0.28*exp2(k); s.x*=.25; float rr=1.-abs(2.*vn(s+k*17.3+float(j)*41.7)-1.); r=max(r,pow(rr,5.)); }
      float w=a*(i==0?(1.-fr):1.)*(i==8?fr:1.);
      float per=ZN/(0.28*exp2(k)); w*=smoothstep(4.,10.,per);
      v+=w*r; tot+=w; a*=.62; }
    return v/max(tot,1e-4); }
  float tooth(vec2 q){ float v=0., a=.5, tot=0.; float lz=log2(max(ZN,1.)); float k0=floor(lz);
    for(int i=0;i<6;i++){ float k=float(i)+k0; float per=ZN/(0.5*exp2(k)); float w=a*smoothstep(4.,10.,per); v+=w*vn(q*0.5*exp2(k)+k*5.1); tot+=w; a*=.55; } return v/max(tot,1e-4); }
  float sdStroke(vec2 q){ float d=1e9;
    for(int i=0;i<63;i++){ if(float(i)>=NP-1.) break; vec3 a=P[i], b=P[i+1]; vec2 pa=q-a.xy, ba=b.xy-a.xy; float t=clamp(dot(pa,ba)/max(dot(ba,ba),1e-6),0.,1.);
      d=min(d,length(pa-ba*t)-mix(a.z,b.z,t)); } return d; }
  float sdRR(vec2 p, vec2 b, float r){ vec2 q=abs(p)-b+r; return length(max(q,0.))+min(max(q.x,q.y),0.)-r; }
  void main(){
    vec2 fc=vec2(gl_FragCoord.x, R.y-gl_FragCoord.y);
    vec2 q=O+(fc-.5*R)/Z;            // coordonnées du papier
    float px=1./Z;                    // un pixel écran en px papier
    vec2 qn=MODE<.5?q:q/10.;           // au séchage (échelle 1), le bruit est lu comme à ×10 : fibres de 4 à 60 px
    float fb=fib(qn), tt=tooth(qn);
    vec3 ink=vec3(1.,.239,.369), deep=vec3(.66,.07,.19), paper=vec3(.984,.973,.957);
    float a; vec3 col;
    if(MODE<.5){
      float sd=sdStroke(q);
      // bord : le corps du trait ondule à peine ; l'encre file le long des fibres au-delà du bord (capillarité)
      float core=1.-smoothstep(-px,px,sd-(tt-.5)*.35);
      // seules les fibres qui touchent le bord boivent l'encre, de moins en moins loin
      float reach=clamp(sd/.45,0.,1.);
      float bleed=smoothstep(.62+.3*reach,.9+.08*reach,fb)*(1.-reach);
      a=max(core,bleed*.92);
      float rim=1.-smoothstep(0.,1.4,-sd);
      col=mix(ink,deep,.18*rim+.10*smoothstep(.55,.9,1.-tt));
      col=mix(col,ink*1.04,.12*smoothstep(.6,.85,tt));
      float skip=smoothstep(.80,.93,fb)*.85*core;
      col=mix(col,paper,skip*(1.-rim*.6));
      col=mix(col,min(vec3(1.),col*1.06+.03),WET);
    } else {
      float sd=sdRR(q-RECT.xy,RECT.zw,RR);
      float bias=1.35*exp(-max(0.,sd)/SIG);
      float level=mix(1.05,-.12,DRY)+bias;
      float v=fb*.65+tt*.35;
      a=1.-smoothstep(level-.02,level+.02,v);
      float near=1.-smoothstep(0.,.08,level-v);
      col=mix(ink,deep,.45*near);
      col=mix(col,paper,smoothstep(.74,.9,fb)*.7*(1.-DRY*.5));
    }
    gl_FragColor=vec4(col*a,a);
  }`;
  function sh(t,src){const s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(s);return s;}
  const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
  const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const U={};for(const k of ['R','O','Z','ZN','MODE','DRY','SIG','RR','WET','RECT','P','NP'])U[k]=gl.getUniformLocation(pr,k);
  gl.viewport(0,0,W,H); gl.uniform2f(U.R,W,H);
  return {canvas:c,
    // pts : [[x,y,demi-largeur]…] en coordonnées papier ; o : {O:[x,y], Z, mode, dry, sig, rect:[cx,cy,hw,hh], rr, wet}
    draw(o,pts=[]){ const arr=new Float32Array(64*3); const n=Math.min(64,pts.length); for(let i=0;i<n;i++){ arr[i*3]=pts[i][0]; arr[i*3+1]=pts[i][1]; arr[i*3+2]=pts[i][2]; }
      gl.uniform3fv(U.P,arr); gl.uniform1f(U.NP,n); gl.uniform2f(U.O,o.O[0],o.O[1]); gl.uniform1f(U.Z,o.Z); gl.uniform1f(U.ZN,o.mode?10:o.Z); gl.uniform1f(U.MODE,o.mode||0);
      gl.uniform1f(U.DRY,o.dry||0); gl.uniform1f(U.SIG,o.sig||10); gl.uniform1f(U.RR,o.rr||0); gl.uniform1f(U.WET,o.wet||0); const r=o.rect||[0,0,1,1]; gl.uniform4f(U.RECT,r[0],r[1],r[2],r[3]);
      gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES,0,3); gl.finish(); }};
})();
// le contour d'un trait perfect-freehand résumé en 64 points (centre, demi-largeur) pour le shader
function inkSpine(pts,size){ const r=penResample(pts,64); return r.map(p=>[p[0],p[1],0.5*size*(0.45+0.55*p[2])]); }
