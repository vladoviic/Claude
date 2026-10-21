/* ============================================================
   Rubans de soie nacrée (WebGL) derrière le téléphone (réf 575-627 : rubans irisés plein cadre).
   Trois bandes sinueuses qui dérivent ; chaque bande a un reflet nacré (couleur de couche mince pâle :
   lilas, pêche, menthe) qui tourne avec le pli du tissu. Valeurs claires et peu saturées : le fond reste en retrait.
   ============================================================ */
const RIB=(()=>{
  const c=document.createElement('canvas'); c.width=960; c.height=540;
  const gl=c.getContext('webgl',{preserveDrawingBuffer:true,antialias:false,premultipliedAlpha:false,alpha:true});
  if(!gl) return null;
  const vs=`attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}`;
  const fs=`precision highp float;
  uniform vec2 R; uniform float T;
  // nacre : un cycle lilas → pêche → rose → cyan pâle (pas de vert), comme les rubans de la réf
  vec3 film(float h){ h=fract(h)*4.; vec3 a=vec3(.851,.800,.961), b=vec3(1.,.824,.722), c=vec3(.965,.788,.867), d=vec3(.769,.914,.953);
    if(h<1.) return mix(a,b,smoothstep(0.,1.,h)); if(h<2.) return mix(b,c,smoothstep(1.,2.,h)); if(h<3.) return mix(c,d,smoothstep(2.,3.,h)); return mix(d,a,smoothstep(3.,4.,h)); }
  void main(){
    vec2 uv=gl_FragCoord.xy/R; uv.y=1.-uv.y; float x=uv.x*R.x/R.y;
    vec3 col=vec3(0.); float A=0.;
    for(int k=0;k<2;k++){ float fk=float(k);
      float y0=.36+.30*fk, fr=1.0+.3*fk, ph=fk*2.1, sp=.045+.012*fk;
      float yc=y0+.11*sin(x*fr+T*sp+ph)+.05*sin(x*fr*2.3-T*sp*.7+ph*1.7);
      float dy=.11*fr*cos(x*fr+T*sp+ph)+.05*fr*2.3*cos(x*fr*2.3-T*sp*.7+ph*1.7);   // pente de la ligne centrale
      float w=.13+.06*sin(x*.9+fk*1.3+T*.02);                                       // largeur qui respire : le ruban vrille
      float d=(uv.y-yc)/w, a=1.-smoothstep(.75,1.,abs(d));
      float twist=d*.35+dy*.45+x*.12+T*.004;
      vec3 c=film(twist+fk*.21); c=mix(c,vec3(1.),.35*pow(1.-abs(d),4.));           // reflet sur le pli
      c*=1.-.06*abs(d);                                                             // le bord tourne vers l'ombre
      // composition prémultipliée : pas de liseré gris au bord des rubans
      float ak=a*.92; col+=c*ak*(1.-A); A+=ak*(1.-A);
    }
    gl_FragColor=vec4(A>0.?col/A:col,A);
  }`;
  function sh(t,src){const s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(s);return s;}
  const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
  const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const U={R:gl.getUniformLocation(pr,'R'),T:gl.getUniformLocation(pr,'T')};
  gl.viewport(0,0,c.width,c.height); gl.uniform2f(U.R,c.width,c.height);
  return {canvas:c, draw(t){ gl.uniform1f(U.T,t); gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES,0,3); gl.finish(); return c; }};
})();
