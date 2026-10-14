// Rend des séquences d'images SVG (0000.svg, 0001.svg...) en PNG, dans le même dossier.
// Usage : node tools/render_seq.mjs <largeur> <dossier> [<dossier> ...]
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const globalRoot = execSync('npm root -g').toString().trim();
const { chromium } = createRequire(globalRoot + '/')('playwright');

const [width, ...dirs] = process.argv.slice(2);
const w = Number(width) || 960;
const h = Math.round(w * 9 / 16);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: w, height: h } });
for (const dir of dirs) {
  const files = readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
  for (const f of files) {
    const svg = readFileSync(join(dir, f), 'utf8');
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden}body>svg{display:block;width:${w}px;height:${h}px}</style>${svg}`);
    await page.screenshot({ path: join(dir, f.replace(/\.svg$/, '.png')) });
  }
}
await browser.close();
