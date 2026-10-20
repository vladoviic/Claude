"""Planches de jugement : une image toutes les 10 (3 par seconde), 4 × 4 par planche, numéro d'image incrusté.

  python3 qa/sheets.py   → out/qa/sheet_01.png …
"""
import glob
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frames = sorted(glob.glob(os.path.join(HERE, 'out', 'frames', '*.png')))
pick = frames[::10]
CW, CH, COLS, ROWS = 480, 270, 4, 4
for k in range(0, len(pick), COLS * ROWS):
    sheet = Image.new('RGB', (COLS * (CW + 8) + 8, ROWS * (CH + 8) + 8), (21, 20, 19))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(pick[k:k + COLS * ROWS]):
        x, y = 8 + (i % COLS) * (CW + 8), 8 + (i // COLS) * (CH + 8)
        sheet.paste(Image.open(p).convert('RGB').resize((CW, CH), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + 52, y + 18], fill=(21, 20, 19))
        d.text((x + 4, y + 3), os.path.basename(p)[:-4], fill=(255, 255, 255))
    out = os.path.join(HERE, 'out', 'qa', f'sheet_{k // (COLS * ROWS) + 1:02d}.png')
    sheet.save(out)
    print(out)
