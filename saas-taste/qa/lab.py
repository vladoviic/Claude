"""Mesures de labo sur le film exporté (méthode Motion Lab de Florence, @flxrnc). Sort en erreur si un seuil casse.

  python3 qa/lab.py [film.mp4]              → rapport ; out/qa/lab.json (courbes par image)

  flashs        paires de variations opposées de luminance relative ≥ 0,1 (image la plus sombre < 0,8)
                sur ≥ 25 % du cadre (WCAG 2.3.1, approx.) ; seuil : ≤ 3 par fenêtre d'une seconde
  tronçons      morts (rien ne change visiblement ≥ 4 s) : erreur ; vides (pas de bords ≥ 0,3 s) : à lire
  bleu-violet   images dont ≥ 40 % des pixels sont saturés entre 200° et 290° ; seuil : < 30 % du film
  coupes        chaque coupe porte un bruitage (début ou crête) à ±3 images (out/cues.json) ; à lire seulement :
                le rebattage du collage coupe toutes les 3 images sans bruitage, et c'est voulu
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, 'out')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, 'saas-taste_master444.mp4')
W, H, FPS = 192, 108, 30
fails, warns = [], []

raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-vf', f'scale={W}:{H}:flags=area', '-f', 'rawvideo',
                      '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32) / 255
n = len(F)
Y = np.where(F <= 0.04045, F / 12.92, ((F + 0.055) / 1.055) ** 2.4) @ np.array([0.2126, 0.7152, 0.0722])

# flashs
d = Y[1:] - Y[:-1]
big = (np.abs(d) >= 0.1) & (np.minimum(Y[1:], Y[:-1]) < 0.8)
area = big.mean(axis=(1, 2))
sign = np.sign((d * big).sum(axis=(1, 2)))
ev = [(i + 1, sign[i]) for i in range(n - 1) if area[i] >= 0.25]
flashes = [b[0] for a, b in zip(ev, ev[1:]) if a[1] != b[1] and b[0] - a[0] <= FPS]
worst, at = max(((sum(1 for x in flashes if f <= x < f + FPS), f) for f in range(n)), default=(0, 0))
(fails if worst > 3 else []).append(f'{worst} flashs dans la seconde qui commence à {at} (max 3)')
print(f'{"ÉCHEC" if worst > 3 else "ok   "} flashs : {len(flashes)} en tout, pire seconde {worst} (image {at})')

# tronçons morts et vides
diff = np.abs(F[1:] - F[:-1]).mean(axis=(1, 2, 3))
edge = np.abs(np.diff(Y, axis=2)).mean(axis=(1, 2)) + np.abs(np.diff(Y, axis=1)).mean(axis=(1, 2))


def runs(mask, length):
    out, r = [], 0
    for i, m in enumerate(mask):
        r = r + 1 if m else 0
        if r == length:
            out.append(i - length + 1)
    return out


dead = runs(diff < 0.0015, 4 * FPS)
blank = [f for f in runs(edge < 0.0025, 9) if FPS < f < n - FPS]
if dead:
    fails.append(f'tronçons morts ≥ 4 s à {dead}')
if blank:
    warns.append(f'tronçons sans bords ≥ 0,3 s à {blank} (à lire : un noir voulu, une icône seule)')
print(f'{"ÉCHEC" if dead else "ok   "} tronçons morts ≥ 4 s : {dead or "aucun"}')
print(f'{"avert" if blank else "ok   "} tronçons vides ≥ 0,3 s : {blank or "aucun"}')

# bleu-violet
mx, mn = F.max(-1), F.min(-1)
sat = (mx - mn) / (mx + 1e-6)
r, g, b = F[..., 0], F[..., 1], F[..., 2]
hue = np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) % 360
bp = (((hue > 200) & (hue < 290) & (sat > 0.25)).mean(axis=(1, 2)) > 0.4).mean()
(fails if bp >= 0.3 else []).append(f'{bp:.0%} d’images bleu-violet')
print(f'{"ÉCHEC" if bp >= 0.3 else "ok   "} images bleu-violet : {bp:.1%}')

# coupes et bruitages
cuts = [i + 1 for i in range(n - 1) if diff[i] > 0.08 and diff[i] > 3 * np.median(diff[max(0, i - 6):i + 6])]
try:
    cues = sorted({t for c in json.load(open(os.path.join(OUT, 'cues.json')))['cues'] for t in (c['f'], c.get('peak', c['f']))})
    bare = [c for c in cuts if not any(abs(q - c) <= 3 for q in cues)]
    if bare:
        warns.append(f'coupes sans bruitage à ±3 images : {bare}')
    print(f'{"avert" if bare else "ok   "} coupes : {len(cuts)}, sans bruitage : {bare or "aucune"}')
except FileNotFoundError:
    print('       coupes : out/cues.json absent (lancer node render.mjs)')

os.makedirs(os.path.join(OUT, 'qa'), exist_ok=True)
json.dump({'flashes': flashes, 'cuts': cuts, 'dead': dead, 'blank': blank, 'blue_purple': float(bp),
           'energy': [round(float(x), 4) for x in diff], 'meanY': [round(float(x), 3) for x in Y.mean(axis=(1, 2))]},
          open(os.path.join(OUT, 'qa', 'lab.json'), 'w'))
for w in warns:
    print('avertissement :', w)
for e in fails:
    print('ÉCHEC :', e)
print(f'\n{len(fails)} échec(s), {len(warns)} avertissement(s)')
sys.exit(1 if fails else 0)
