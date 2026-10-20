"""Contrôle qualité avant le rendu final (V20). Sort en erreur si une règle du film est cassée.

  node render.mjs --qa                      → out/qa/dom.json (texte visible, curseur, bouton Envoyer)
  node render.mjs --stills 0,4,…,36,126,…   → les images que ce script lit
  python3 qa/check.py                       → rapport + out/qa/contact.png (planche des posters, à valider à l'œil)
"""
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, 'out')
RED = np.array([0xFF, 0x3D, 0x5E])
POSTERS = [126, 233, 1232, 1295, 1559]
EARLY = list(range(0, 37, 4))
fails, warns = [], []


def still(f):
    return os.path.join(OUT, 'stills', f'f{f:04d}.png')


def need_stills(frames):
    miss = [f for f in frames if not os.path.exists(still(f))]
    if miss:
        subprocess.run(['node', os.path.join(HERE, 'render.mjs'), '--stills', ','.join(map(str, miss))], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def rule(ok, msg, warn=False):
    print(('ok    ' if ok else ('WARN  ' if warn else 'FAIL  ')) + msg)
    if not ok:
        (warns if warn else fails).append(msg)


dom = json.load(open(os.path.join(OUT, 'qa', 'dom.json')))
need_stills(EARLY + POSTERS)

# 1 · les prises du stylo : tant qu'elles manquent, les traits sont des brouillons de synthèse
takes = sorted(glob.glob(os.path.join(HERE, 'pen', 'G0[1-9].json')))
rule(len(takes) == 9, f'prises du stylo : {len(takes)}/9 (sinon brouillons de synthèse)', warn=True)

# 2 · loi du rouge : pas de rouge avant le caret M1 (37)
worst = 0
for f in EARLY:
    a = np.asarray(Image.open(still(f)).convert('RGB')).astype(int)
    d = np.abs(a - RED).sum(2)
    worst = max(worst, int((d < 60).sum()))
rule(worst == 0, f'loi du rouge : aucun pixel rouge avant 37 (max {worst} px)')

# 3 · vocabulaire : velvetly est un B2B, pas une boutique ; et l'offre est un redesign, pas de la sécurité
SHOP = re.compile(r'\b(add to cart|cart|checkout|buy now|shop now|order(s|ed)? complete|free shipping)\b|€', re.I)
SEC = re.compile(r'\b(security|secure|vulnerab\w*|CVE|breach|exploit|pentest)\b', re.I)
for name, rx in (('boutique', SHOP), ('sécurité', SEC)):
    hits = sorted({(r['f'], m.group(0)) for r in dom if 'sW' not in r['scenes'] for m in rx.finditer(r['text'])})
    rule(not hits, f'vocabulaire {name} absent' + (f' : {hits[:6]}' if hits else ''))

# 4 · le 47 : chaque nombre de changements imprimé vaut 47
nums = sorted({(r['f'], int(m.group(1))) for r in dom for m in re.finditer(r'\b(\d+) (?:changes|fixes|suggestions)\b', r['text'])})
bad = [x for x in nums if x[1] != 47]
rule(not bad, f'le 47 est partout le même ({len(nums)} occurrences)' + (f' : {bad[:6]}' if bad else ''))

# 5 · parité du curseur : la main survole Envoyer au même décalage à 206 et à la fin
def offset(f):
    r = next((x for x in dom if x['f'] == f), None)
    if not r or not r['cursor'] or not r['send']:
        return None
    c, s = r['cursor']['r'], r['send']
    return (c[0] - (s[0] + s[2] / 2), c[1] - (s[1] + s[3] / 2)), r['cursor']['shape']


a, b = offset(206), offset(1559)
if a and b:
    gap = max(abs(a[0][0] - b[0][0]), abs(a[0][1] - b[0][1]))
    rule(a[1] == b[1] == 'hand' and gap <= 6, f'curseur : main sur Envoyer à 206 et 1559, écart {gap:.1f} px')
else:
    rule(False, 'curseur : main ou bouton Envoyer introuvable à 206 / 1559')

# 6 · le poster lu par une machine : 1559 réduit à 320×180 doit encore dire « taste » et « kwinndo »
im = Image.open(still(1559)).convert('L').resize((320, 180), Image.LANCZOS).resize((1280, 720), Image.LANCZOS)
tmp = os.path.join(OUT, 'qa', 'ocr.png')
im.save(tmp)
txt = subprocess.run(['tesseract', tmp, '-', '--psm', '6'], capture_output=True, text=True).stdout.lower()
rule('taste' in txt and 'kwinndo' in txt, f'OCR du poster 1559 à 320×180 : {" ".join(txt.split())[:90]!r}')

# 7 · planche des posters, à valider à l'œil avant le rendu final
ims = [Image.open(still(f)).convert('RGB').resize((640, 360), Image.LANCZOS) for f in POSTERS]
sheet = Image.new('RGB', (640 * 3 + 40, 360 * 2 + 30), (21, 20, 19))
for i, x in enumerate(ims):
    sheet.paste(x, (10 + (i % 3) * 650, 10 + (i // 3) * 370))
sheet.save(os.path.join(OUT, 'qa', 'contact.png'))
print('planche : out/qa/contact.png')

print(f'\n{len(fails)} échec(s), {len(warns)} avertissement(s)')
sys.exit(1 if fails else 0)
