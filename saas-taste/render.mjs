// Rend index.html image par image avec Chromium (Playwright), puis assemble avec ffmpeg.
//
//   node render.mjs --stills 68,190,278,430,960   → out/stills/fXXXX.png
//   node render.mjs                               → out/frames/*.png + out/cues.json
//   node render.mjs --from 300 --to 509           → une plage seulement
//   node render.mjs --cues                       → out/cues.json seulement (pour audio.py)
//   node render.mjs --serve                      → aperçu dans le navigateur
//   options : --workers 4
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { dirname, extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); }
catch { playwright = require('/opt/node22/lib/node_modules/playwright'); }

const here = dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const out = join(here, 'out');

// Petit serveur statique : les modules ES (three.js) ne se chargent pas en file://
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.otf': 'font/otf', '.ttf': 'font/ttf', '.png': 'image/png', '.jpg': 'image/jpeg' };
const server = createServer(async (req, res) => {
  const p = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^([/\\])+/, '');
  const file = join(here, p || 'index.html');
  if (!file.startsWith(here)) { res.writeHead(403).end(); return; }
  try { const buf = await readFile(file); res.writeHead(200, { 'content-type': TYPES[extname(file)] || 'application/octet-stream' }).end(buf); }
  catch { res.writeHead(404).end(); }
});
await new Promise(r => server.listen(+arg('port', 0), '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}/`;
if (process.argv.includes('--serve')) {
  console.log(`aperçu : ${base}index.html  (espace : lecture, ← → : image par image)`);
  await new Promise(() => {});
}
const url = base + 'index.html?render';

const browser = await playwright.chromium.launch({
  args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('page error:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('console:', m.text()); });
  page.on('response', r => { if (r.status() >= 400) console.error('missing:', r.url().replace(base, '')); });
  await page.goto(url);
  await page.waitForFunction(() => window.READY === true);
  return page;
}
async function shoot(page, f, file) {
  await page.evaluate(n => window.renderFrame(n), f);
  await page.screenshot({ path: file, type: 'png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
}

const stills = arg('stills');
if (process.argv.includes('--cues')) {
  const page = await openPage();
  const { total, cues } = await page.evaluate(() => ({ total: window.TOTAL, cues: window.CUES }));
  mkdirSync(out, { recursive: true });
  writeFileSync(join(out, 'cues.json'), JSON.stringify({ fps: 30, total, cues }, null, 1));
  console.log(`out/cues.json : ${cues.length} cues`);
} else if (stills) {
  mkdirSync(join(out, 'stills'), { recursive: true });
  const page = await openPage();
  for (const f of stills.split(',').map(Number)) {
    const file = join(out, 'stills', `f${String(f).padStart(4, '0')}.png`);
    await shoot(page, f, file); console.log(file);
  }
} else {
  mkdirSync(join(out, 'frames'), { recursive: true });
  const first = await openPage();
  const { total, cues } = await first.evaluate(() => ({ total: window.TOTAL, cues: window.CUES }));
  writeFileSync(join(out, 'cues.json'), JSON.stringify({ fps: 30, total, cues }, null, 1));
  const from = +arg('from', 0), to = +arg('to', total - 1);
  const n = +arg('workers', 4);
  const pages = [first, ...await Promise.all(Array.from({ length: n - 1 }, openPage))];
  const t0 = Date.now(); let done = 0;
  await Promise.all(pages.map(async (page, w) => {
    for (let f = from + w; f <= to; f += n) {
      await shoot(page, f, join(out, 'frames', `${String(f).padStart(4, '0')}.png`));
      if (++done % 60 === 0) console.log(`${done}/${to - from + 1} images · ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
  }));
  console.log(`terminé : ${done} images en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
await browser.close();
server.close();
