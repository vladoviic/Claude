// Rend des SVG en PNG avec le Chromium préinstallé (contrôle visuel des planches).
// Usage : node tools/render_png.mjs <sortie_dir> <fichier.svg> [...] [--width=1600]
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync, mkdirSync } from 'node:fs';
import { basename, resolve } from 'node:path';

// Playwright est installé globalement : on le charge depuis la racine npm globale.
const globalRoot = execSync('npm root -g').toString().trim();
const { chromium } = createRequire(globalRoot + '/')('playwright');

const args = process.argv.slice(2);
const widthArg = args.find(a => a.startsWith('--width='));
const maxW = widthArg ? Number(widthArg.split('=')[1]) : 1600;
const [outDir, ...files] = args.filter(a => !a.startsWith('--'));
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();
for (const file of files) {
  const svg = readFileSync(file, 'utf8');
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const [w, h] = m ? [Number(m[1]), Number(m[2])] : [1920, 1080];
  const scale = Math.min(1, maxW / w);
  await page.setViewportSize({ width: Math.round(w * scale), height: Math.round(h * scale) });
  const html = `<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}body>svg{display:block;width:${w * scale}px;height:${h * scale}px}</style>${svg}`;
  await page.setContent(html, { waitUntil: 'load' });
  const out = resolve(outDir, basename(file).replace(/\.svg$/, '.png'));
  await page.screenshot({ path: out, fullPage: true });
  console.log(out);
}
await browser.close();
