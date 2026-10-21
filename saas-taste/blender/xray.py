"""Loupe X-ray de la landing : chaque image du rendu land/ redessinée en trait d'encre sur papier, seul le velours rouge garde sa couleur.
   python3 xray.py <dossier img/land> [indices…]  → x_XX.jpg dans le même dossier"""
import sys, os, glob
import numpy as np, cv2
D = sys.argv[1]
idx = [int(a) for a in sys.argv[2:]] or range(66)
PAPER = np.array([0xE4, 0xE9, 0xEE], np.float32)  # BGR de #EEE9E4
INK = np.array([0x13, 0x14, 0x15], np.float32)
for i in idx:
    src = cv2.imread(os.path.join(D, f'l_{i:02d}.jpg'))
    h, w = src.shape[:2]
    big = cv2.resize(src, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
    g = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
    g = cv2.bilateralFilter(g, 9, 40, 9)
    g = cv2.GaussianBlur(g, (0, 0), 1.6)
    e = cv2.Canny(g, 14, 38, L2gradient=True)
    # les traits courts (texture du bouclé, feuilles) sont du bruit : on ne garde que les contours d'au moins 40 px
    n, lab, st, _ = cv2.connectedComponentsWithStats(e, connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 30
    e = (keep[lab] * 255).astype(np.uint8)
    e = cv2.dilate(e, np.ones((2, 2), np.uint8))
    line = cv2.resize(e.astype(np.float32) / 255, (w, h), interpolation=cv2.INTER_AREA)
    line = np.clip(line * 1.6, 0, 1)[..., None]
    # modelé d'argile sous le papier (≈ 30 % d'écart) : les volumes et la tache de soleil se lisent même sans traits
    lum = cv2.GaussianBlur(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), (0, 0), 2).astype(np.float32)[..., None] / 255
    out = PAPER * (0.70 + 0.30 * np.clip(lum * 1.5, 0, 1))
    # le velours rouge : teinte rouge saturée, masque adouci
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV).astype(np.float32)
    H, S, V = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    red = (((H < 6) | (H > 172)) & (S > 0.5) & (V > 0.15)).astype(np.uint8)
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    # seul le fauteuil : les rayures de l'affiche et le pouf prune sont de petites taches, on les écarte
    n, lab, st, _ = cv2.connectedComponentsWithStats(red, connectivity=8)
    keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= 900
    red = keep[lab].astype(np.float32)
    red = cv2.GaussianBlur(red, (0, 0), 1.2)[..., None]
    out = out * (1 - red) + src.astype(np.float32) * red
    out = out * (1 - line) + INK * line
    cv2.imwrite(os.path.join(D, f'x_{i:02d}.jpg'), np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(i, end=' ', flush=True)
print()
