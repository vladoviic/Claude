// Objets 3D du film (three.js), rendus à la demande dans un canvas hors écran puis
// copiés dans les canvas 2D de la page. Tout dépend de t : aucune horloge, aucun aléatoire libre.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

function mulberry(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const COL = { paper: 0xF3EFEA, ink: 0x2A2724, accent: 0xFF3D5E, salt: 0xFBF8F3 };

const canvas = document.createElement('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setClearColor(0x000000, 0);
const pmrem = new THREE.PMREMGenerator(renderer);
const env = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
// Studio pour le verre : softbox très lumineuses = reflets nets qui dessinent la forme
const studio = (() => {
  const sc = new THREE.Scene();
  sc.add(new THREE.Mesh(new THREE.SphereGeometry(12, 32, 16), new THREE.MeshBasicMaterial({ color: 0x6f6866, side: THREE.BackSide })));
  const panel = (w, h, x, y, z, k, c = 0xffffff) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(k), side: THREE.DoubleSide })); m.position.set(x, y, z); m.lookAt(0, 0, 0); sc.add(m); };
  panel(1.6, 9, -5.5, 0.5, 3.5, 9); panel(0.9, 9, 5.2, 0, 3, 6); panel(7, 1.6, 0, 7.5, 1, 4); panel(4, 4, 1, -2, -7, 2.5, 0xffb8cc); panel(4, 3, -6, -3, -3, 1.5, 0xffd2b0);
  return pmrem.fromScene(sc, 0.015).texture;
})();
function grainTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const r = mulberry(3);
  g.fillStyle = '#808080'; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 5000; i++) { const v = (r() * 255) | 0; g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(r() * 256, r() * 256, 2 + r() * 2, 2 + r() * 2); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 2); return t;
}

function mulberry_unused(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const lathe = (pts, seg = 96) => new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), seg);

function softShadowTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'); const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, 'rgba(40,20,20,0.55)'); grd.addColorStop(0.45, 'rgba(40,20,20,0.22)'); grd.addColorStop(1, 'rgba(40,20,20,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const SHADOW_TEX = softShadowTexture();

/* ---------------- Salière ---------------- */
const shakerScene = new THREE.Scene(); shakerScene.environment = studio;
const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-3, 5, 4); shakerScene.add(key);
const rim = new THREE.DirectionalLight(0xffd6e0, 1.2); rim.position.set(4, 2, -3); shakerScene.add(rim);
const shakerCam = new THREE.PerspectiveCamera(26, 1, 0.1, 50);

const shaker = new THREE.Group();
const glass = new THREE.MeshPhysicalMaterial({
  color: 0xffffff, roughness: 0.02, metalness: 0, transparent: true, opacity: 0.3, depthWrite: false, side: THREE.DoubleSide,
  iridescence: 1, iridescenceIOR: 1.3, iridescenceThicknessRange: [220, 820],
  clearcoat: 1, clearcoatRoughness: 0.02, envMapIntensity: 2.4,
});
// verre cannelé : 18 côtes verticales
function flute(geo, n = 18, a = 0.03) {
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), y = p.getY(i); const th = Math.atan2(z, x);
    const k = (y > -1.05 && y < 0.7) ? 1 + a * (0.5 + 0.5 * Math.cos(n * th)) : 1; p.setX(i, x * k); p.setZ(i, z * k); }
  geo.computeVertexNormals(); return geo;
}
const body = new THREE.Mesh(flute(lathe([[0, -1.1], [0.5, -1.1], [0.6, -1.075], [0.645, -1.0], [0.66, -0.6], [0.69, 0.2], [0.705, 0.66], [0.69, 0.76],
  [0.6, 0.76], [0.6, 0.66], [0.585, 0.2], [0.56, -0.6], [0.54, -0.93], [0.45, -0.97], [0, -0.97]], 144)), glass);
body.renderOrder = 2; shaker.add(body);
const GRAIN = grainTexture();
const salt = new THREE.Mesh(flute(lathe([[0, -0.965], [0.53, -0.955], [0.548, -0.6], [0.555, -0.32], [0.48, -0.25], [0.25, -0.21], [0, -0.2]], 144), 18, 0.026),
  new THREE.MeshStandardMaterial({ color: 0xF6F1EA, roughness: 0.95, bumpMap: GRAIN, bumpScale: 2.2, envMapIntensity: 0.55 }));
shaker.add(salt);
const capMat = new THREE.MeshPhysicalMaterial({ color: COL.accent, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 0.55 });
const capProfile = [[0.001, 1.2], [0.3, 1.18], [0.52, 1.11], [0.66, 1.0], [0.72, 0.88], [0.735, 0.78], [0.73, 0.72], [0.7, 0.7], [0.62, 0.7]];
shaker.add(new THREE.Mesh(lathe(capProfile), capMat));
const ring = new THREE.Mesh(new THREE.TorusGeometry(0.715, 0.03, 16, 96), new THREE.MeshStandardMaterial({ color: 0xf2ece6, metalness: 1, roughness: 0.16, envMapIntensity: 0.8 }));
ring.rotation.x = Math.PI / 2; ring.position.y = 0.71; shaker.add(ring);
function capY(r) { for (let i = 0; i < capProfile.length - 1; i++) { const [r0, y0] = capProfile[i], [r1, y1] = capProfile[i + 1]; if (r >= r0 && r <= r1) return y0 + (y1 - y0) * (r - r0) / (r1 - r0); } return 1.2; }
const holeMat = new THREE.MeshBasicMaterial({ color: 0x3a1018 });
const HOLES = [[0, 0], ...Array.from({ length: 6 }, (_, i) => [0.3, i / 6 * Math.PI * 2])];
for (const [r, a] of HOLES) {
  const h = new THREE.Mesh(new THREE.CircleGeometry(0.058, 20), holeMat);
  const x = Math.cos(a) * r, z = Math.sin(a) * r, y = capY(r) + 0.004;
  h.position.set(x, y, z); h.lookAt(x * 2.2, y + 0.8, z * 2.2); shaker.add(h);
}
const shakerPivot = new THREE.Group(); shakerPivot.add(shaker); shakerScene.add(shakerPivot);
const shadow = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 3.2), new THREE.MeshBasicMaterial({ map: SHADOW_TEX, transparent: true, depthWrite: false }));
shadow.rotation.x = -Math.PI / 2; shadow.position.y = -1.12; shakerScene.add(shadow);

// grains de sel : petites facettes qui tombent des trous quand la salière penche
const GR = 70; const grainGeo = new THREE.BoxGeometry(0.05, 0.05, 0.05);
const grains = new THREE.InstancedMesh(grainGeo, new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4, envMapIntensity: 1.0 }), GR);
shakerScene.add(grains);
const GRS = (() => { const r = mulberry(7); return Array.from({ length: GR }, () => ({ t0: r(), vx: (r() - 0.5) * 0.5, vz: (r() - 0.5) * 0.5, spin: r() * 6, hole: (r() * HOLES.length) | 0 })); })();
const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpE = new THREE.Euler(), tmpV = new THREE.Vector3(), tmpS = new THREE.Vector3();

function sizeTo(w, h, cam) {
  if (canvas.width !== w || canvas.height !== h) renderer.setSize(w, h, false);
  cam.aspect = w / h; cam.updateProjectionMatrix();
}
function blit(target, clear = true) {
  const ctx = target.getContext('2d'); if (clear) ctx.clearRect(0, 0, target.width, target.height);
  ctx.drawImage(canvas, 0, 0, target.width, target.height);
}

/**
 * o : { t (s), spin (rad), tilt (rad, penche vers la droite), drop (0→1, chute d'entrée),
 *       zoom, lookY, sprinkle (0→1), shadow (0→1), camX }
 */
function shakerRender(target, o = {}) {
  const t = o.t || 0;
  sizeTo(target.width, target.height, shakerCam);
  const z = o.zoom ?? 1;
  shakerCam.position.set(o.camX ?? 0, 1.5, 7.4 / z); shakerCam.lookAt(0, o.lookY ?? 0.05, 0);
  const drop = o.drop ?? 1;
  shaker.rotation.set(0, o.spin ?? t * 0.6, 0);
  shakerPivot.rotation.set(0, 0, -(o.tilt || 0));
  shakerPivot.position.set(0, (1 - drop) * 4.2, 0);
  shadow.material.opacity = (o.shadow ?? 1) * (0.25 + 0.75 * drop);
  shadow.scale.setScalar(0.8 + 0.4 * drop);
  // grains
  const sp = o.sprinkle || 0; let k = 0;
  shakerPivot.updateMatrixWorld(true);
  for (const g of GRS) {
    const life = 1.1; const age = ((t * 0.9 + g.t0 * life) % life);
    if (sp <= 0.01 || g.t0 > sp) { tmpM.makeScale(0, 0, 0); grains.setMatrixAt(k++, tmpM); continue; }
    const [hr, ha] = HOLES[g.hole];
    tmpV.set(Math.cos(ha) * hr, capY(hr) + 0.02, Math.sin(ha) * hr).applyMatrix4(shaker.matrixWorld);
    const dir = new THREE.Vector3(0, 1, 0).applyQuaternion(shakerPivot.quaternion);
    tmpV.addScaledVector(dir, 0.6 * age).add(new THREE.Vector3(g.vx * age, -4.2 * age * age, g.vz * age));
    tmpE.set(g.spin * age, g.spin * 0.7 * age, 0); tmpQ.setFromEuler(tmpE); tmpS.setScalar(1);
    tmpM.compose(tmpV, tmpQ, tmpS); grains.setMatrixAt(k++, tmpM);
  }
  grains.instanceMatrix.needsUpdate = true;
  renderer.render(shakerScene, shakerCam);
  blit(target, o.clear !== false);
}

/* ---------------- Icônes tactiles ---------------- */
const iconScene = new THREE.Scene(); iconScene.environment = env;
const ik = new THREE.DirectionalLight(0xffffff, 2.0); ik.position.set(-2.5, 4, 5); iconScene.add(ik);
const iconCam = new THREE.PerspectiveCamera(20, 1, 0.1, 50); iconCam.position.set(0, 0, 8.5); iconCam.lookAt(0, 0, 0);
const clay = c => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.42, clearcoat: 0.5, clearcoatRoughness: 0.25, envMapIntensity: 0.9 });
const M = { paper: clay(COL.paper), accent: clay(COL.accent), ink: clay(0x4A4542) };
const ICONS = {};
{ // overview : 2×2 tuiles
  const g = new THREE.Group();
  [[-1, 1, 'paper'], [1, 1, 'accent'], [-1, -1, 'paper'], [1, -1, 'paper']].forEach(([x, y, m]) => {
    const b = new THREE.Mesh(new RoundedBoxGeometry(0.88, 0.88, 0.42, 4, 0.16), M[m]); b.position.set(x * 0.5, y * 0.5, 0); g.add(b); });
  ICONS.overview = g;
}
{ // reports : trois barres
  const g = new THREE.Group();
  [[0.75, 'paper'], [1.2, 'paper'], [1.75, 'accent']].forEach(([h, m], i) => {
    const b = new THREE.Mesh(new RoundedBoxGeometry(0.56, h, 0.56, 4, 0.14), M[m]); b.position.set((i - 1) * 0.68, -0.85 + h / 2, 0); g.add(b); });
  ICONS.reports = g;
}
{ // customers : tête + buste
  const g = new THREE.Group();
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.42, 48, 32), M.paper); head.position.y = 0.5; g.add(head);
  const bust = new THREE.Mesh(new THREE.CapsuleGeometry(0.62, 0.3, 12, 32), M.accent); bust.position.y = -0.62; bust.scale.set(1, 0.72, 0.8); g.add(bust);
  ICONS.customers = g;
}
{ // settings : bouton rotatif
  const g = new THREE.Group();
  const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.86, 0.46, 64), M.paper); knob.rotation.x = Math.PI / 2; g.add(knob);
  for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2; const r = new THREE.Mesh(new RoundedBoxGeometry(0.13, 0.13, 0.5, 2, 0.05), M.paper); r.position.set(Math.cos(a) * 0.86, Math.sin(a) * 0.86, 0); r.rotation.z = a; g.add(r); }
  const dot = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.1, 24), M.accent); dot.rotation.x = Math.PI / 2; dot.position.set(0, 0.48, 0.25); g.add(dot);
  ICONS.settings = g;
}
for (const g of Object.values(ICONS)) { g.visible = false; iconScene.add(g); }

/** kind : overview | reports | customers | settings ; pop 0→1 (apparition), t (s) */
function iconRender(target, kind, t = 0, pop = 1, i = 0) {
  sizeTo(target.width, target.height, iconCam);
  for (const [k, g] of Object.entries(ICONS)) g.visible = k === kind;
  const g = ICONS[kind];
  g.scale.setScalar(Math.max(0.0001, pop));
  g.rotation.set(0.42 + Math.sin(t * 1.4 + i) * 0.06, -0.5 + Math.sin(t * 1.1 + i * 2) * 0.12 + (1 - pop) * 1.4, 0);
  if (kind === 'settings') g.rotation.z = Math.sin(t * 0.9) * 0.35;
  renderer.render(iconScene, iconCam);
  blit(target);
}

window.T3D = { shaker: shakerRender, icon: iconRender };
window.dispatchEvent(new Event('t3d-ready'));
