/* ============================================================
   Caméra thermique (WebGL) : la luminance floutée d'une source + des points chauds (l'attention, l'encre)
   passent par une palette thermique à isothermes. Deux palettes :
     clair : papier-lilas (froid) → rose → rouge du stylo → corail → blanc chaud (le plus chaud) ;
     sombre : presque noir → prune → bordeaux → braise, pour les fonds de nuit.
   Le rouge du stylo est à 0,70 : un champ « aplati » à 0,70 est exactement l'encre rouge, ce qui permet
   de développer une image thermique à partir d'un aplat d'encre (FLAT 1 → 0).
   ============================================================ */
const THERMAL=(()=>{
  const c=document.createElement('canvas'); c.width=960; c.height=540;
  const gl=c.getContext('webgl',{preserveDrawingBuffer:true,antialias:false,premultipliedAlpha:false,alpha:false});
  if(!gl) return null;
  const vs=`attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}`;
  const fs=`precision highp float;
  uniform sampler2D T; uniform vec2 R; uniform vec4 SP[8]; uniform float NS, BIAS, WIMG, BANDS, TIME, DARK, BLUR, FLAT, GAM, LO, HI, INV;
  float hash(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
  float vnoise(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
    return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y); }
  vec3 ramp(float h, vec3 a, vec3 b, vec3 c, vec3 d, vec3 e, vec3 f, vec3 g){
    if(h<.22) return mix(a,b,h/.22); if(h<.42) return mix(b,c,(h-.22)/.20); if(h<.58) return mix(c,d,(h-.42)/.16);
    if(h<.70) return mix(d,e,(h-.58)/.12); if(h<.84) return mix(e,f,(h-.70)/.14); return mix(f,g,(h-.84)/.16); }
  vec3 pal(float h){
    vec3 l=ramp(h,vec3(.933,.918,.961),vec3(.843,.820,.941),vec3(.953,.725,.816),vec3(1.,.490,.576),vec3(1.,.239,.369),vec3(1.,.498,.384),vec3(1.,.886,.651));
    vec3 d=ramp(h,vec3(.055,.051,.071),vec3(.137,.098,.227),vec3(.290,.118,.275),vec3(.478,.133,.251),vec3(.722,.263,.247),vec3(.80,.42,.30),vec3(.898,.604,.361));
    return mix(l,d,DARK); }
  void main(){
    vec2 uv=gl_FragCoord.xy/R; uv.y=1.-uv.y;
    float L=0., ws=0.;
    for(int i=-2;i<=2;i++) for(int j=-2;j<=2;j++){ vec2 o=vec2(float(i),float(j))*BLUR/R; float w=exp(-float(i*i+j*j)/4.);
      L+=w*dot(texture2D(T,uv+o).rgb,vec3(.299,.587,.114)); ws+=w; }
    L=L/ws; L=mix(L,1.-L,INV);   // INV : le sujet sombre devient le chaud (le velours sur un fond clair)
    L=pow(clamp((L-LO)/(HI-LO),0.,1.),GAM);   // niveaux : la scène occupe toute la palette, du froid au blanc chaud
    float h=WIMG*L;
    for(int k=0;k<8;k++){ if(float(k)>=NS) break; vec4 s=SP[k]; vec2 d=(uv-s.xy)*vec2(R.x/R.y,1.); h+=s.w*exp(-dot(d,d)/(s.z*s.z)); }
    // le chatoiement de l'air chaud : un bruit lent, qui dérive
    h+=.06*(vnoise(uv*vec2(5.,3.)+vec2(TIME*.03,-TIME*.02))-.5);
    h=clamp(mix(h+BIAS,.70,FLAT),0.,1.);
    // isothermes : des aplats doux avec un filet à chaque palier, comme une vraie caméra
    float q=h*BANDS, fq=fract(q); float hb=(floor(q)+smoothstep(.25,.75,fq))/BANDS; h=mix(h,hb,.6*(1.-FLAT));
    float edge=1.-smoothstep(0.,.07,min(fq,1.-fq));
    vec3 col=pal(h); col*=1.-.06*edge*(1.-FLAT);
    col+=(hash(gl_FragCoord.xy+fract(TIME*.37)*91.)-.5)*.03;
    gl_FragColor=vec4(col,1.);
  }`;
  function sh(t,src){const s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(s);return s;}
  const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
  const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const U={};for(const k of ['T','R','SP','NS','BIAS','WIMG','BANDS','TIME','DARK','BLUR','FLAT','GAM','LO','HI','INV'])U[k]=gl.getUniformLocation(pr,k);
  const tex=gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,tex);
  for(const [k,v] of [[gl.TEXTURE_MIN_FILTER,gl.LINEAR],[gl.TEXTURE_MAG_FILTER,gl.LINEAR],[gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE],[gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D,k,v);
  gl.viewport(0,0,c.width,c.height); gl.uniform2f(U.R,c.width,c.height); gl.uniform1i(U.T,0);
  // la source est retaillée à la résolution du rendu (la caméra thermique est douce par nature)
  const src2=document.createElement('canvas'); src2.width=c.width; src2.height=c.height; const sx=src2.getContext('2d');
  // un champ sans image : des taches chaudes qui dérivent (fonds du rapport et des alertes), flouté ensuite en CSS
  const blank=document.createElement('canvas'); blank.width=8; blank.height=8;
  return {canvas:c, src:src2, srcCtx:sx, blank,
    // o : {spots:[[u,v,rayon,poids]…] (u,v en 0-1), bias, wimg, bands, t, dark, blur (px), flat, gam, lo/hi (niveaux de la source)} ; src : canvas/image, ou null pour le canvas src
    draw(src,o={}){ if(src) { sx.clearRect(0,0,c.width,c.height); sx.drawImage(src,0,0,c.width,c.height); }
      gl.bindTexture(gl.TEXTURE_2D,tex); gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,src2);
      const sp=new Float32Array(32), S=(o.spots||[]).slice(0,8); S.forEach((s,i)=>sp.set(s,i*4));
      gl.uniform4fv(U.SP,sp); gl.uniform1f(U.NS,S.length); gl.uniform1f(U.BIAS,o.bias||0); gl.uniform1f(U.WIMG,o.wimg??0.8); gl.uniform1f(U.BANDS,o.bands||9);
      gl.uniform1f(U.TIME,o.t||0); gl.uniform1f(U.DARK,o.dark||0); gl.uniform1f(U.BLUR,o.blur??6); gl.uniform1f(U.FLAT,o.flat||0); gl.uniform1f(U.GAM,o.gam||1); gl.uniform1f(U.LO,o.lo??0); gl.uniform1f(U.HI,o.hi??1); gl.uniform1f(U.INV,o.inv||0);
      gl.drawArrays(gl.TRIANGLES,0,3); gl.finish(); return c; }};
})();
