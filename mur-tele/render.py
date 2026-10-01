#!/usr/bin/env python3
"""
MUR TÉLÉ — mur de CRT 9:16, bichromie rouge, boucle parfaite de 30 s.

Chaque écran joue une timeline de segments (média ou scène procédurale).
Les timelines « s'enroulent » sur 30 s : la frame 900 == la frame 0, donc la
vidéo boucle sans couture sur Reels / TikTok / Shorts.

Usage rapide :
    python render.py                          # démo procédurale -> out/mur_tele.mp4
    python render.py --sources sources        # avec tes images / vidéos
    python render.py --plan plan.json         # rejouer / retoucher un plan exact
    python render.py --stills 2,9,17,26       # planches PNG pour valider vite

Voir README.md pour le détail.
"""
import argparse
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- format ----
W, H = 1080, 1920          # 9:16
FPS = 30
DUR = 30.0                 # durée de la boucle (s)
NF = int(FPS * DUR)
PAD = 140                  # marge du « monde » autour du cadre (pour la dérive caméra)

# ------------------------------------------------------- direction artistique
# Gradient map luminance -> RGB. Tout passe par là : c'est ce qui unifie
# des sources hétérogènes (smartphone, presse, archives) dans la même teinte.
# Valeurs relevées sur l'image de référence : noirs bruns, rouge écran
# (210,48,25) quasi uniforme, hautes lumières rose très pâle.
PALETTE = [
    (0.00, (24, 12, 10)),
    (0.14, (44, 16, 13)),
    (0.34, (118, 28, 16)),
    (0.50, (176, 32, 16)),
    (0.62, (214, 38, 18)),
    (0.70, (244, 44, 22)),
    (0.80, (242, 108, 86)),
    (0.90, (248, 190, 178)),
    (1.00, (253, 243, 240)),
]
BG_COLOR = (20, 10, 8)
BLANK_L = 0.62             # luminance d'un écran allumé sans signal (-> 210,48,25)

SLOGANS = [
    ["BLOQUONS", "TOUT"],
    ["LYCÉE", "BLOQUÉ"],
    ["PAS DE", "JUSTICE", "PAS DE", "PAIX"],
    ["ON LÂCHE", "RIEN"],
    ["LA RUE", "EST À", "NOUS"],
    ["QUI NOUS", "PROTÈGE ?"],
]
CHYRONS = [
    "BLOCUS DANS LES LYCÉES — LA MOBILISATION S'ÉTEND",
    "MANIFESTATION — FACE-À-FACE AVEC LES FORCES DE L'ORDRE",
    "INTERPELLATIONS EN MARGE DU CORTÈGE",
]
TICKER = ("EN DIRECT  •  BLOCUS  •  CORTÈGE  •  GAZ LACRYMOGÈNE  •  "
          "INTERPELLATIONS  •  RASSEMBLEMENT  •  ")

FONT_BOLD = ["fonts/display.ttf", "fonts/display.otf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT_MONO = ["fonts/mono.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"]

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
VID_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}


# ================================================================ helpers ====
def find_font(cands):
    for c in cands:
        p = Path(c) if Path(c).is_absolute() else ROOT / c
        if p.exists():
            return str(p)
    raise SystemExit("Aucune police trouvée")


@lru_cache(None)
def font(kind, size):
    return ImageFont.truetype(find_font(FONT_BOLD if kind == "bold" else FONT_MONO), size)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def build_lut():
    xs = np.linspace(0, 1, 256)
    pos = [p for p, _ in PALETTE]
    lut = np.zeros((256, 3), np.float32)
    for c in range(3):
        lut[:, c] = np.interp(xs, pos, [col[c] for _, col in PALETTE])
    return lut


def make_field(n, beta, seed):
    """Bruit fractal 1/f^beta, tuilable par construction (FFT)."""
    rng = np.random.default_rng(seed)
    fy = np.fft.fftfreq(n)[:, None]
    fx = np.fft.rfftfreq(n)[None, :]
    k = np.sqrt(fx * fx + fy * fy)
    k[0, 0] = 1.0
    spec = (rng.standard_normal(k.shape) + 1j * rng.standard_normal(k.shape)) / k ** beta
    spec[0, 0] = 0
    f = np.fft.irfft2(spec, s=(n, n)).astype(np.float32)
    lo, hi = np.percentile(f, [1, 99])
    return np.clip((f - lo) / (hi - lo), 0, 1)


def sample(field, w, h, x0=0.0, y0=0.0, scale=1.0):
    """Fenêtre w×h (bilinéaire, enroulée) dans un champ de bruit tuilable.
    scale peut être un tuple (sx, sy) pour un échantillonnage anisotrope."""
    n = field.shape[0]
    sx, sy = scale if isinstance(scale, tuple) else (scale, scale)
    xs = np.arange(w, dtype=np.float32) * sx + x0
    ys = np.arange(h, dtype=np.float32) * sy + y0
    x0i = np.floor(xs).astype(np.int64)
    y0i = np.floor(ys).astype(np.int64)
    fx = (xs - x0i)[None, :]
    fy = (ys - y0i)[:, None]
    xa, xb = x0i % n, (x0i + 1) % n
    ya, yb = (y0i % n)[:, None], ((y0i + 1) % n)[:, None]
    top = field[ya, xa] * (1 - fx) + field[ya, xb] * fx
    bot = field[yb, xa] * (1 - fx) + field[yb, xb] * fx
    return top * (1 - fy) + bot * fy


@lru_cache(None)
def uv(w, h):
    """Coordonnées normalisées [-1,1] centrées."""
    u = (np.arange(w, dtype=np.float32) + 0.5) / w * 2 - 1
    v = (np.arange(h, dtype=np.float32) + 0.5) / h * 2 - 1
    return np.broadcast_to(u[None, :], (h, w)), np.broadcast_to(v[:, None], (h, w))


def window(layer, w, h, dx, dy, m):
    """Recadre un calque dessiné avec une marge m (évite les bords enroulés)."""
    dx = int(np.clip(round(dx), -m, m))
    dy = int(np.clip(round(dy), -m, m))
    return layer[m + dy:m + dy + h, m + dx:m + dx + w]


def to_l(img):
    return np.asarray(img, dtype=np.float32) / 255.0


def seg_rng(seg, *extra):
    return np.random.default_rng([seg["seed"], *[int(e) & 0x7FFFFFFF for e in extra]])


# ============================================================== contexte ====
class Ctx:
    def __init__(self, sources=None):
        self.lut = build_lut()
        self.cloud = make_field(512, 1.55, 11)
        self.cloud2 = make_field(512, 1.35, 23)
        self.fine = make_field(512, 0.95, 37)
        self.cache = {}
        self.sources = sources

    def memo(self, key, fn):
        if key not in self.cache:
            self.cache[key] = fn()
        return self.cache[key]


# ======================================================== scènes : dessin ====
def draw_crowd(w, h, seed, depth, m):
    """Silhouettes de foule (têtes, épaules, poings levés, capuches)."""
    S = 2
    W2, H2 = (w + 2 * m) * S, (h + 2 * m) * S
    im = Image.new("L", (W2, H2), 0)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed * 7 + depth)
    base = H2 * (0.60 if depth == 0 else 0.80)
    n = 16 if depth == 0 else 7
    sc = (0.075 if depth == 0 else 0.15) * H2
    xs = np.sort(rng.uniform(-0.05, 1.05, n))
    for x in xs * W2:
        s = sc * rng.uniform(0.8, 1.2)
        y = base + rng.uniform(-0.05, 0.05) * H2
        hr = s * 0.5
        d.ellipse([x - hr * 0.82, y - hr, x + hr * 0.82, y + hr * 1.05], fill=255)
        d.rounded_rectangle([x - s * 1.25, y + hr * 0.85, x + s * 1.25, H2 + 10],
                            radius=int(s * 0.75), fill=255)
        r = rng.random()
        if r < 0.28:  # poing levé
            sgn = rng.choice([-1, 1])
            ax = x + sgn * s * 0.95
            top = y - s * rng.uniform(1.3, 2.1)
            tx = ax + rng.uniform(-0.25, 0.25) * s
            d.line([ax, y + hr * 1.2, tx, top], fill=255, width=max(2, int(s * 0.36)))
            d.ellipse([tx - s * 0.27, top - s * 0.32, tx + s * 0.27, top + s * 0.18], fill=255)
        elif r < 0.45:  # capuche
            d.ellipse([x - hr * 1.05, y - hr * 1.15, x + hr * 1.05, y + hr * 0.9], fill=255)
        elif r < 0.58:  # casquette
            d.rectangle([x - hr * 0.8, y - hr * 0.62, x + hr * 1.5, y - hr * 0.35], fill=255)
    return to_l(im.resize((w + 2 * m, h + 2 * m), Image.LANCZOS))


def draw_placards(w, h, seed, m):
    """Pancartes éclairées de face (valeur, alpha)."""
    S = 2
    W2, H2 = (w + 2 * m) * S, (h + 2 * m) * S
    a = Image.new("L", (W2, H2), 0)
    v = Image.new("L", (W2, H2), 0)
    da, dv = ImageDraw.Draw(a), ImageDraw.Draw(v)
    rng = np.random.default_rng(seed * 13)
    words = ["NON", "STOP", "49.3", "BLOCUS", "!!", "RÉSISTE", "STOP"]
    f = font("bold", int(H2 * 0.05))
    for _ in range(rng.integers(2, 4)):
        cx = rng.uniform(0.1, 0.9) * W2
        top = rng.uniform(0.28, 0.42) * H2
        pw, ph = rng.uniform(0.16, 0.26) * W2, rng.uniform(0.09, 0.13) * H2
        tilt = rng.uniform(-0.04, 0.04) * pw
        da.line([cx, top + ph, cx + tilt, H2 * 0.62], fill=255, width=int(H2 * 0.008))
        box = [cx - pw / 2, top, cx + pw / 2, top + ph]
        da.rectangle(box, fill=255)
        dv.rectangle(box, fill=int(rng.uniform(150, 215)))
        word = words[rng.integers(len(words))]
        dv.text((cx, top + ph / 2), word, font=f, fill=20, anchor="mm")
    sz = (w + 2 * m, h + 2 * m)
    return to_l(v.resize(sz, Image.LANCZOS)), to_l(a.resize(sz, Image.LANCZOS))


def draw_riot_line(w, h, seed, m):
    """Ligne de CRS : casques, visières, boucliers. Renvoie (alpha, reflets)."""
    S = 2
    W2, H2 = (w + 2 * m) * S, (h + 2 * m) * S
    a = Image.new("L", (W2, H2), 0)
    g = Image.new("L", (W2, H2), 0)
    da, dg = ImageDraw.Draw(a), ImageDraw.Draw(g)
    rng = np.random.default_rng(seed * 17)
    for row, (by, s, n) in enumerate([(0.70, 0.085, 9), (0.95, 0.14, 6)]):
        by *= H2
        s *= H2
        xs = (np.arange(n) + 0.5 + rng.uniform(-0.15, 0.15, n)) / n * W2
        for x in xs:
            hy = by - s * 2.15
            da.rounded_rectangle([x - s * 0.95, hy + s * 0.5, x + s * 0.95, H2 + 10],
                                 radius=int(s * 0.5), fill=255)        # épaules
            da.ellipse([x - s * 0.55, hy - s * 0.55, x + s * 0.55, hy + s * 0.6], fill=255)  # casque
            da.rectangle([x - s * 0.62, hy - s * 0.05, x + s * 0.62, hy + s * 0.08], fill=255)
            dg.rectangle([x - s * 0.45, hy + s * 0.02, x + s * 0.45, hy + s * 0.09],
                         fill=150 if row else 110)                      # reflet visière
            sx = x + rng.uniform(-0.1, 0.1) * s
            da.rounded_rectangle([sx - s * 0.7, by - s * 1.5, sx + s * 0.7, by + s * 0.9],
                                 radius=int(s * 0.18), fill=255)       # bouclier
            dg.rounded_rectangle([sx - s * 0.7, by - s * 1.5, sx + s * 0.7, by + s * 0.9],
                                 radius=int(s * 0.18), outline=95 if row else 70,
                                 width=max(2, int(s * 0.06)))
            dg.rectangle([sx - s * 0.35, by - s * 1.2, sx + s * 0.35, by - s * 0.95],
                         fill=55 if row else 40)                        # hublot
    sz = (w + 2 * m, h + 2 * m)
    return to_l(a.resize(sz, Image.LANCZOS)), to_l(g.resize(sz, Image.LANCZOS))


def draw_branches(w, h, seed, roots, depth=8, length=0.22, spread=0.55, width=3.0):
    """Arborescence (fissures / branches / veines). Renvoie une carte de
    « distance à la racine » : pixel visible si dist < révélation."""
    S = 2
    im = Image.new("F", (w * S, h * S), 1e9)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed * 29)

    def grow(x, y, ang, ln, wd, dist, k):
        if k == 0 or ln < 2:
            return
        steps = 4
        for _ in range(steps):
            ang += rng.normal(0, 0.18)
            nx = x + math.cos(ang) * ln / steps
            ny = y + math.sin(ang) * ln / steps
            dist += ln / steps
            d.line([x, y, nx, ny], fill=float(dist), width=max(1, int(wd)))
            x, y = nx, ny
        nb = 2 if rng.random() < 0.75 else 3
        for i in range(nb):
            na = ang + rng.uniform(-spread, spread) + (i - (nb - 1) / 2) * spread * 0.6
            grow(x, y, na, ln * rng.uniform(0.6, 0.82), wd * 0.72, dist, k - 1)

    for rx, ry, ang in roots:
        grow(rx * w * S, ry * h * S, ang, length * h * S, width * S, 0.0, depth)
    arr = np.asarray(im.resize((w, h), Image.NEAREST), dtype=np.float32) / S
    return arr


def text_block(lines, w, h, target_w=0.86, squash=0.74, gap=0.06):
    """Typo affiche : lignes justifiées en largeur, condensées."""
    rows = []
    for line in lines:
        f = font("bold", 220)
        bb = f.getbbox(line)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        im = Image.new("L", (tw + 20, th + 20), 0)
        ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), line, font=f, fill=255)
        rows.append(im.crop(im.getbbox()))
    tw = int(w * target_w)
    scaled = []
    for r in rows:
        k = tw / r.width
        scaled.append(r.resize((tw, max(1, int(r.height * k / squash)))))
    total = sum(r.height for r in scaled) + gap * h * (len(scaled) - 1)
    if total > h * 0.84:  # trop haut : on réduit tout
        k = h * 0.84 / total
        scaled = [r.resize((max(1, int(r.width * k)), max(1, int(r.height * k)))) for r in scaled]
        total *= k
    out = Image.new("L", (w, h), 0)
    y = (h - total) / 2
    for r in scaled:
        out.paste(r, (int((w - r.width) / 2), int(y)))
        y += r.height + gap * h * (total / (sum(r.height for r in scaled) + gap * h * (len(scaled) - 1)))
    return to_l(out)


# ============================================================ scènes ========
def sc_blank(c, seg, lt, w, h):
    """Écran allumé sans signal : aplat lumineux + tirets parasites (cf. réf.)."""
    def build():
        rng = np.random.default_rng(seg["seed"])
        u, v = uv(w, h)
        base = BLANK_L + 0.012 * (1 - u * u - v * v) + rng.uniform(-0.02, 0.025)
        l = np.array(base, np.float32)
        # lignes fantômes (rémanence) : rectangles à peine visibles, cf. réf.
        for _ in range(rng.integers(3, 8)):
            if rng.random() < 0.6:
                y = int(rng.uniform(0.1, 0.9) * h)
                x0, x1 = sorted((rng.uniform(0, 1, 2) * w).astype(int))
                l[y:y + 2, x0:x1] -= rng.uniform(0.012, 0.03)
            else:
                x = int(rng.uniform(0.1, 0.9) * w)
                y0, y1 = sorted((rng.uniform(0, 1, 2) * h).astype(int))
                l[y0:y1, x:x + 2] -= rng.uniform(0.012, 0.03)
        # tirets noirs francs
        dashes = []
        for _ in range(rng.choice([0, 1, 2, 2, 3])):
            y = int(rng.uniform(0.12, 0.88) * h)
            th = max(3, int(h * rng.uniform(0.012, 0.02)))
            x0 = int(rng.uniform(-0.1, 0.6) * w)
            ln = int(rng.uniform(0.12, 0.5) * w)
            dashes.append((y, th, max(0, x0), max(0, x0 + ln)))
        return l, dashes

    l0, dashes = c.memo(("blank", seg["seed"], w, h), build)
    l = l0 + 0.012 * (sample(c.cloud, w, h, seg["seed"] % 400 + lt * 6, lt * 9, 0.5) - 0.5)
    rng = seg_rng(seg, int(lt * 7))
    for y, th, x0, x1 in dashes:
        dy = int(rng.integers(-1, 2)) if rng.random() < 0.15 else 0
        l[y + dy:y + dy + th, x0:x1] = 0.04
    return l


def sc_static(c, seg, lt, w, h):
    frames = c.memo(("static", w, h), lambda: [
        np.repeat(np.random.default_rng(i).random((h, (w + 1) // 2), dtype=np.float32),
                  2, axis=1)[:, :w] * 0.8 + 0.12 for i in range(8)])
    l = frames[int(lt * FPS) % 8].copy()
    y = (np.arange(h) / h)[:, None]
    l *= 0.8 + 0.3 * smoothstep(0.0, 0.12, np.abs(((y - lt * 0.7) % 1.0) - 0.5))
    return l


def sc_bars(c, seg, lt, w, h):
    def build():
        lv = np.array([0.96, 0.84, 0.72, 0.6, 0.47, 0.34, 0.2], np.float32)
        col = (np.arange(w) * 7 // w)
        l = np.repeat(lv[col][None, :], h, 0)
        l[int(h * 0.72):int(h * 0.8)] = lv[::-1][col]
        l[int(h * 0.8):] = np.where((np.arange(w) // (w // 6)) % 2 == 0, 0.08, 0.5)[None, :]
        im = Image.fromarray((l * 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        f = font("mono", int(h * 0.075))
        d.rectangle([w * 0.18, h * 0.38, w * 0.82, h * 0.52], fill=15)
        d.text((w / 2, h * 0.45), "PAS DE SIGNAL", font=f, fill=235, anchor="mm")
        return to_l(im)
    l = c.memo(("bars", w, h), build)
    return l * (0.97 + 0.03 * math.sin(lt * 40))


def sc_slogan(c, seg, lt, w, h):
    rng0 = np.random.default_rng(seg["seed"])
    lines = seg.get("text") or SLOGANS[seg["seed"] % len(SLOGANS)]
    inv = bool(rng0.integers(2))
    txt = c.memo(("slogan", tuple(lines), w, h), lambda: text_block(lines, w, h))
    if inv:
        l = 0.08 + 0.85 * txt
    else:
        l = 0.80 - 0.74 * txt
    l = l + 0.05 * (sample(c.cloud, w, h, lt * 5, lt * 3, 0.7) - 0.5)
    rng = seg_rng(seg, int(lt * 12))
    if rng.random() < 0.18:  # glitch de ligne
        y0 = int(rng.uniform(0, 0.9) * h)
        y1 = min(h, y0 + int(rng.uniform(0.03, 0.15) * h))
        l[y0:y1] = np.roll(l[y0:y1], int(rng.uniform(-0.12, 0.12) * w), axis=1)
    return l


def sc_manif(c, seg, lt, w, h):
    s = seg["seed"]
    m = 24
    back = c.memo(("crowd", s, 0, w, h), lambda: draw_crowd(w, h, s, 0, m))
    front = c.memo(("crowd", s, 1, w, h), lambda: draw_crowd(w, h, s, 1, m))
    pv, pa = c.memo(("plac", s, w, h), lambda: draw_placards(w, h, s, m))
    u, v = uv(w, h)
    rng = np.random.default_rng(s)
    lx = rng.uniform(-0.5, 0.5)
    sm = sample(c.cloud, w, h, s * 37 + lt * 10, s * 11 + lt * 26, 0.55)
    sm2 = sample(c.cloud2, w, h, s * 5 - lt * 6, lt * 14, 0.33)
    light = 0.45 + 0.55 * np.exp(-((u - lx) ** 2 + (v + 0.35) ** 2) / 0.7)
    l = np.clip(light * (0.35 + 0.95 * sm * sm2 * 1.5), 0, 1)
    sway = 3 * math.sin(lt * 1.3 + s)
    a = window(back, w, h, sway, 1.5 * math.sin(lt * 4.1), m)
    l = l * (1 - a) + 0.11 * a
    a = window(pa, w, h, sway * 1.4, 2.5 * math.sin(lt * 3.3 + 1), m)
    val = window(pv, w, h, sway * 1.4, 2.5 * math.sin(lt * 3.3 + 1), m)
    l = l * (1 - a) + val * a
    a = window(front, w, h, -sway * 1.8, 3 * abs(math.sin(lt * 2.6 + s)), m)
    l = l * (1 - a) + 0.015 * a
    fog = sample(c.cloud, w, h, 200 - lt * 18, 90 + lt * 9, 0.45)
    return l * (1 - 0.22 * fog) + 0.22 * fog * 0.75


def sc_riot(c, seg, lt, w, h):
    s = seg["seed"]
    m = 16
    alpha, glint = c.memo(("riot", s, w, h), lambda: draw_riot_line(w, h, s, m))
    rng = np.random.default_rng(s)
    flashes = c.memo(("flash", s), lambda: np.cumsum(rng.uniform(1.2, 3.2, 20)) - 0.6)
    dt = lt - flashes
    fl = float(np.sum(np.where(dt >= 0, np.exp(-np.clip(dt, 0, None) * 4.5), 0)))
    fl = min(fl, 1.3)
    fx = math.sin(s * 3.1) * 0.5
    u, v = uv(w, h)
    sm = sample(c.cloud, w, h, s * 19 + lt * 14, s * 7 + lt * 20, 0.5)
    rad = np.exp(-((u - fx) ** 2 + (v + 0.15) ** 2) / 0.5)
    l = np.clip(0.18 + 0.42 * sm + fl * 0.75 * rad * (0.6 + 0.6 * sm), 0, 1)
    dx = 1.2 * math.sin(lt * 0.9)
    a = window(alpha, w, h, dx, 0, m)
    g = window(glint, w, h, dx, 0, m)
    l = l * (1 - a) + a * (0.03 + g * (0.35 + 0.65 * min(fl, 1)))
    gas = np.clip(sample(c.cloud2, w, h, 300 + lt * 22, 100 + lt * 16, 0.4) * 1.6 - 0.55, 0, 1)
    gas *= smoothstep(-0.2, 1.0, v) * min(1.0, 0.25 + lt / 6)
    return l * (1 - 0.6 * gas) + gas * 0.6 * (0.55 + 0.35 * min(fl, 1))


def sc_fire(c, seg, lt, w, h):
    s = seg["seed"]
    m = 12

    def car():
        S = 2
        im = Image.new("L", ((w + 2 * m) * S, (h + 2 * m) * S), 0)
        d = ImageDraw.Draw(im)
        W2, H2 = im.size
        gy = H2 * 0.93
        d.rounded_rectangle([W2 * 0.14, gy - H2 * 0.13, W2 * 0.86, gy - H2 * 0.03], radius=12, fill=255)
        d.polygon([(W2 * 0.3, gy - H2 * 0.12), (W2 * 0.38, gy - H2 * 0.21),
                   (W2 * 0.64, gy - H2 * 0.21), (W2 * 0.74, gy - H2 * 0.12)], fill=255)
        for wx in (0.28, 0.72):
            d.ellipse([W2 * wx - H2 * 0.05, gy - H2 * 0.08, W2 * wx + H2 * 0.05, gy + H2 * 0.02], fill=255)
        d.rectangle([0, gy, W2, H2], fill=255)
        # silhouette debout à gauche
        px, ps = W2 * 0.1, H2 * 0.075
        d.ellipse([px - ps * 0.45, gy - ps * 5.0, px + ps * 0.45, gy - ps * 4.0], fill=255)
        d.rounded_rectangle([px - ps * 0.85, gy - ps * 4.1, px + ps * 0.85, gy - ps * 1.6],
                            radius=int(ps * 0.4), fill=255)
        d.rectangle([px - ps * 0.6, gy - ps * 1.8, px + ps * 0.6, gy], fill=255)
        return to_l(im.resize((w + 2 * m, h + 2 * m), Image.LANCZOS))

    sil = c.memo(("car", w, h), car)
    u, v = uv(w, h)
    n1 = sample(c.cloud2, w, h, s * 41 + 6 * math.sin(lt * 2), lt * 190, (0.9, 0.55))
    n2 = sample(c.cloud, w, h, s * 3, lt * 110, (0.5, 0.3))
    yy = (v + 1) / 2
    env = np.exp(-((u - 0.05) ** 2) / 0.45)
    shape = (0.5 * n1 + 0.8 * n2) * yy ** 1.1 * 1.6 * env
    f = np.clip((shape - 0.36) * 2.4, 0, 1) ** 1.3
    smoke = 0.10 + 0.20 * sample(c.cloud2, w, h, s * 9 + lt * 6, lt * 40, 0.5) * (1 - yy)
    glow = float(np.mean(f)) * 1.6
    l = np.maximum(smoke + glow * 0.25 * yy, f)
    a = window(sil, w, h, 0, 0, m)
    return l * (1 - a) + 0.02 * a


def sc_silhouette(c, seg, lt, w, h):
    """Tête et épaules à contre-jour sur aplat rouge, cheveux longs en bataille
    (comme l'écran au-dessus de l'œil dans la réf.)."""
    s = seg["seed"]
    m = 20

    def build():
        S = 2
        W2, H2 = (w + 2 * m) * S, (h + 2 * m) * S
        im = Image.new("L", (W2, H2), 0)
        d = ImageDraw.Draw(im)
        rng = np.random.default_rng(s * 31)
        cx, cy, r = W2 * 0.53, H2 * 0.40, H2 * 0.16
        d.ellipse([cx - r * 0.82, cy - r, cx + r * 0.82, cy + r * 1.02], fill=255)
        d.polygon([(cx - r * 0.42, cy + r * 0.7), (cx + r * 0.42, cy + r * 0.7),
                   (cx + r * 0.6, cy + r * 1.6), (cx - r * 0.6, cy + r * 1.6)], fill=255)
        d.ellipse([cx - r * 3.3, cy + r * 1.35, cx + r * 3.3, cy + r * 6.5], fill=255)  # épaules
        for _ in range(900):  # mèches : marches aléatoires depuis le crâne
            ang = rng.uniform(math.pi * 0.85, math.pi * 2.15)
            x = cx + math.cos(ang) * r * 0.78
            y = cy + math.sin(ang) * r * 0.95
            dirx, diry = math.cos(ang), math.sin(ang)
            side = max(0.0, math.cos(ang) ** 2)
            wd = max(1, int(r * rng.uniform(0.015, 0.04)))
            pts = [(x, y)]
            for _ in range(int(rng.integers(4, 9 + int(8 * side)))):
                diry += 0.18 + 0.25 * side           # gravité, plus forte sur les côtés
                dirx += rng.normal(0, 0.25)
                nrm = math.hypot(dirx, diry)
                step = r * rng.uniform(0.07, 0.14)
                x += dirx / nrm * step
                y += diry / nrm * step
                pts.append((x, y))
            d.line(pts, fill=255, width=wd, joint="curve")
        return to_l(im.resize((w + 2 * m, h + 2 * m), Image.LANCZOS))

    sil = c.memo(("sil", s, w, h), build)
    u, v = uv(w, h)
    l = 0.70 + 0.015 * (1 - u * u - v * v) + 0.02 * (sample(c.cloud, w, h, lt * 8, s, 0.5) - 0.5)
    a = window(sil, w, h, 4 * math.sin(lt * 0.6 + s), 1.5 * math.sin(lt * 0.45), m)
    return l * (1 - a) + 0.03 * a


def sc_cracks(c, seg, lt, w, h):
    """Branches / fissures qui poussent (cf. écran du bas de la réf.)."""
    s = seg["seed"]

    def build():
        rng = np.random.default_rng(s)
        roots = [(rng.uniform(0.3, 0.7), 1.02, -math.pi / 2 + rng.uniform(-0.3, 0.3)),
                 (-0.02, rng.uniform(0.4, 0.7), rng.uniform(-0.4, 0.2)),
                 (1.02, rng.uniform(0.3, 0.6), math.pi + rng.uniform(-0.2, 0.4))]
        return draw_branches(w, h, s, roots, depth=6, length=0.24, spread=0.55, width=4.0)

    dist = c.memo(("cracks", s, w, h), build)
    reveal = lt * h * 0.45
    vis = smoothstep(reveal, reveal - 6, dist)
    bg = 0.02 + 0.05 * sample(c.cloud, w, h, s * 13, lt * 4, 0.6)
    fl = 0.97 + 0.03 * math.sin(lt * 23) * math.sin(lt * 7)
    return bg * (1 - vis) + 0.64 * fl * vis


def sc_eye(c, seg, lt, w, h):
    """Œil en très gros plan, traité « photo » haute clé comme la réf. :
    peau claire striée, iris sombre marbré, cils, reflet de fenêtre.
    seg["zoom"] > 1 : macro sur l'iris (ex. 3)."""
    s = seg["seed"]
    zoom = seg.get("zoom", 1.0)
    u, v = uv(w, h)

    rng = np.random.default_rng(s)
    sacc_t = c.memo(("sacc_t", s), lambda: np.cumsum(rng.uniform(0.9, 2.6, 40)))
    sacc_p = c.memo(("sacc_p", s), lambda: np.random.default_rng(s + 1).uniform(-1, 1, (41, 2)))
    k = int(np.searchsorted(sacc_t, lt))
    t0 = sacc_t[k - 1] if k > 0 else 0.0
    e = smoothstep(0.0, 0.08, lt - t0)
    gx, gy = sacc_p[k] * e + sacc_p[max(k - 1, 0)] * (1 - e) if k > 0 else sacc_p[0]
    blinks = c.memo(("blink", s), lambda: np.cumsum(np.random.default_rng(s + 2).uniform(3.0, 6.5, 20)))
    bd = np.min(np.abs(lt - blinks))
    open_ = 1 - (1 - smoothstep(0.0, 0.14, bd)) * 0.97 if zoom < 1.5 else 1.0

    icx, icy = gx * 0.22 + 0.08, gy * 0.05 - 0.01
    X = u / zoom * 1.0 + (icx if zoom > 1 else 0.0)
    Y = v * h / w / zoom + (icy if zoom > 1 else 0.0)

    L = 1.25
    xx = np.clip(1 - (X / L) ** 2, 0, None)
    yu = -0.50 * open_ * xx ** 0.7 + 0.03
    yl = 0.28 * open_ * xx ** 0.9 + 0.03
    inside = smoothstep(-0.008, 0.008, Y - yu) * smoothstep(-0.008, 0.008, yl - Y)

    R = 0.46
    dx, dy = X - icx, Y - icy
    rr = np.sqrt(dx * dx + dy * dy) / R
    th = np.arctan2(dy, dx)
    n = c.fine.shape[0]
    ta = ((th / (2 * np.pi)) + 0.5)
    fib = c.fine[((rr * 60).astype(np.int64) % n), (ta * n * 3).astype(np.int64) % n]
    mot = c.cloud[((rr * 90).astype(np.int64) % n), (ta * n * 2).astype(np.int64) % n]
    pupil = 0.34 + 0.03 * math.sin(lt * 0.8 + s)
    iris = 0.06 + 0.34 * smoothstep(0.35, 0.85, mot) + 0.16 * smoothstep(0.45, 0.8, fib) * smoothstep(1.0, 0.45, rr)
    iris += 0.12 * np.exp(-((rr - pupil - 0.12) ** 2) / 0.006)     # collerette
    iris *= 1 - 0.7 * smoothstep(0.82, 1.0, rr)                     # limbe sombre
    pm = smoothstep(pupil + 0.015, pupil - 0.015, rr)
    iris = iris * (1 - pm) + 0.025 * pm

    veins = c.memo(("veins", s, w, h, zoom), lambda: draw_branches(
        w, h, s + 5, [(0.0, 0.5, 0.0), (0.0, 0.42, -0.3), (1.0, 0.55, math.pi),
                      (1.0, 0.45, math.pi + 0.3)], depth=5, length=0.15, spread=0.7, width=1.4))
    vein = (veins < 1e8).astype(np.float32) * 0.22
    sclera = 0.95 - 0.12 * X ** 2 - vein
    sclera -= 0.38 * smoothstep(yu + 0.16, yu, Y)                    # ombre de paupière
    ib = smoothstep(1.0, 0.985, rr)
    eye = iris * ib + sclera * (1 - ib)

    hx, hy = icx - R * 0.15, icy - R * 0.42                           # reflet fenêtre
    hl = smoothstep(0.075, 0.06, np.abs(X - hx)) * smoothstep(0.042, 0.03, np.abs(Y - hy))
    eye = np.maximum(eye, hl * (rr < 1))

    # peau : claire, striée de lignes fines (cf. réf.)
    ox = s % 300
    bend = (0.10 * xx * h)                                           # rides qui suivent l'œil
    nf = c.fine.shape[0]
    iy = ((np.arange(h)[:, None] + bend) * (2.4 / zoom) + 40).astype(np.int64) % nf
    ix = ((np.arange(w)[None, :]) * (0.22 / zoom) + ox).astype(np.int64) % nf
    st1 = c.fine[iy, np.broadcast_to(ix, iy.shape)]
    st2 = sample(c.fine, w, h, ox + 90, 140, (2.2 / zoom, 2.2 / zoom))
    lines = smoothstep(0.60, 0.74, st1) * 0.75 + smoothstep(0.66, 0.8, st2) * 0.3
    skin = 0.90 - 0.32 * lines - 0.10 * sample(c.cloud2, w, h, ox, 7, 0.6 / zoom)
    crease = yu - 0.12 - 0.05 * xx
    skin -= 0.32 * np.exp(-((Y - crease) ** 2) / 0.0009) * (xx > 0.02)
    skin -= 0.18 * np.exp(-((Y - yl - 0.07) ** 2) / 0.0015) * (xx > 0.02)
    # cils : peigne de traits sombres au-dessus de la paupière supérieure
    comb = smoothstep(0.55, 0.7, sample(c.fine, w, h, ox * 3, 0, (4.5 / zoom, 0.05 / zoom)))
    band = smoothstep(yu - 0.08 * (0.3 + xx), yu, Y) * (Y < yu + 0.004) * (xx > 0.01)
    lash = np.clip(comb * band + np.exp(-((Y - yu) ** 2) / 0.0007) * (xx > 0.0), 0, 1)
    skin = skin * (1 - 0.88 * lash)
    lowlash = np.exp(-((Y - yl) ** 2) / 0.0002) * (xx > 0.05) * 0.5
    out = skin * (1 - inside) + eye * inside
    out -= lowlash * 0.5
    wet = np.exp(-((Y - yl + 0.008) ** 2) / 0.00006) * (xx > 0.1) * 0.25
    return np.clip(out + wet * inside, 0, 1)


# ------------------------------------------------------------- médias -------
def load_video(path, w, h, max_s=12.0):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-t", str(max_s), "-vf",
           f"fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},format=gray",
           "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    if n == 0:
        raise RuntimeError(f"vidéo illisible : {path}")
    arr = np.frombuffer(raw[:n * w * h], np.uint8).reshape(n, h, w)
    lo, hi = np.percentile(arr[::max(1, n // 12)], [2, 98])
    lut = np.clip((np.arange(256) - lo) / max(1, hi - lo), 0, 1)
    return (lut[arr] * 255).astype(np.uint8)


def load_image(path, w, h, over=1.22):
    im = Image.open(path).convert("L")
    k = max(w * over / im.width, h * over / im.height)
    im = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    lo, hi = np.percentile(a, [2, 98])
    a = np.clip((a - lo) / max(1, hi - lo), 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8))


def sc_media(c, seg, lt, w, h):
    p = Path(seg["src"])
    if p.suffix.lower() in VID_EXT:
        fr = c.memo(("vid", str(p), w, h), lambda: load_video(p, w, h, seg.get("max_s", 12)))
        i = (int(lt * FPS) + int(seg.get("offset", 0) * FPS)) % len(fr)
        l = fr[i].astype(np.float32) / 255
    else:
        im = c.memo(("img", str(p), w, h), lambda: load_image(p, w, h))
        rng = np.random.default_rng(seg["seed"])
        prog = lt / max(seg["dur"], 0.1)
        z = 1.0 + 0.14 * prog                          # Ken Burns lent
        cw, ch = im.width / z / 1.0, im.height / z / 1.0
        cw, ch = min(cw, im.width), min(ch, im.height)
        dirx, diry = rng.uniform(-1, 1, 2)
        cx = im.width / 2 + dirx * (im.width - cw) / 2 * prog
        cy = im.height / 2 + diry * (im.height - ch) / 2 * prog
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        l = to_l(im.resize((w, h), Image.BILINEAR, box=box))
    g = seg.get("contrast", 1.25)                      # courbe « graphique »
    return np.clip((l - 0.5) * g + 0.5, 0, 1)


SCENES = {
    "blank": sc_blank, "static": sc_static, "bars": sc_bars, "slogan": sc_slogan,
    "manif": sc_manif, "crs": sc_riot, "feu": sc_fire, "silhouette": sc_silhouette,
    "fissures": sc_cracks, "oeil": sc_eye, "media": sc_media,
}


# ---------------------------------------------------------- overlays --------
def overlay_osd(l, seg, lt, w, h):
    im = Image.fromarray((np.clip(l, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    f = font("mono", max(12, int(h * 0.058)))
    pad = int(w * 0.06)
    if (lt % 1.0) < 0.6:
        d.ellipse([pad, pad + 4, pad + h * 0.04, pad + 4 + h * 0.04], fill=245, outline=10, width=2)
    d.text((pad + h * 0.06, pad), "REC", font=f, fill=245, stroke_width=2, stroke_fill=10)
    d.text((w - pad, pad), f"CAM {seg['seed'] % 9 + 1:02d}", font=f, fill=245, anchor="ra", stroke_width=2, stroke_fill=10)
    secs = 17 * 3600 + 42 * 60 + int(seg["seed"] % 50) + lt
    tc = f"{int(secs // 3600):02d}:{int(secs // 60 % 60):02d}:{int(secs % 60):02d}:{int(lt * FPS) % FPS:02d}"
    d.text((pad, h - pad), tc, font=f, fill=245, anchor="ld", stroke_width=2, stroke_fill=10)
    return to_l(im)


def overlay_chyron(c, l, seg, lt, w, h):
    head = seg.get("chyron") if isinstance(seg.get("chyron"), str) else CHYRONS[seg["seed"] % len(CHYRONS)]

    def build():
        lay = Image.new("L", (w, h), 0)
        a = Image.new("L", (w, h), 0)
        d, da = ImageDraw.Draw(lay), ImageDraw.Draw(a)
        f1 = font("bold", int(h * 0.06))
        bw = f1.getlength("● EN DIRECT") + w * 0.06
        box = [w * 0.05, h * 0.07, w * 0.05 + bw, h * 0.07 + h * 0.09]
        d.rectangle(box, fill=235)
        da.rectangle(box, fill=255)
        d.text((box[0] + w * 0.03, (box[1] + box[3]) / 2), "● EN DIRECT", font=f1, fill=15, anchor="lm")
        f2 = font("bold", int(h * 0.055))
        band = [0, h * 0.70, w, h * 0.84]
        d.rectangle(band, fill=228)
        da.rectangle(band, fill=255)
        words, lines, cur = head.split(), [], ""
        for wd in words:
            if f2.getlength((cur + " " + wd).strip()) < w * 0.9:
                cur = (cur + " " + wd).strip()
            else:
                lines.append(cur)
                cur = wd
        lines.append(cur)
        txt = "\n".join(lines[:2])
        d.multiline_text((w * 0.05, (band[1] + band[3]) / 2), txt, font=f2, fill=15,
                         anchor="lm", spacing=2)
        f3 = font("bold", int(h * 0.045))
        tk = TICKER * 3
        tw = int(f3.getlength(TICKER))
        strip = Image.new("L", (tw * 3, int(h * 0.08)), 20)
        ImageDraw.Draw(strip).text((0, strip.height / 2), tk, font=f3, fill=230, anchor="lm")
        return to_l(lay), to_l(a), to_l(strip), tw

    lay, a, strip, tw = c.memo(("chyron", head, w, h), build)
    l = l * (1 - a) + lay * a
    off = int(lt * w * 0.28) % tw
    y0 = int(h * 0.84)
    sh = min(strip.shape[0], h - y0)
    l[y0:y0 + sh] = strip[:sh, off:off + w]
    return l


# ============================================================ l'écran ========
def superellipse(w, h, n=5.0, aa=1.4, bulge=0.0):
    """Masque de tube cathodique : rectangle arrondi dont les côtés bombent
    légèrement vers l'extérieur (bulge), comme les écrans de la référence."""
    u, v = uv(w, h)
    ue = u * (1 + bulge) / (1 + bulge * (1 - v * v))
    ve = v * (1 + bulge) / (1 + bulge * (1 - u * u))
    r = (np.abs(ue) ** n + np.abs(ve) ** n) ** (1 / n)
    d = (1 - r) * min(w, h) / 2
    return np.clip(d / aa + 0.5, 0, 1).astype(np.float32), r


class Screen:
    def __init__(self, idx, cx, cy, w, h, style, hero, timeline):
        self.idx, self.style, self.hero, self.timeline = idx, style, hero, timeline
        if style == "crt":
            self.gw, self.gh = w, h
            self.gx, self.gy = int(cx - w / 2), int(cy - h / 2)
            self.mask, r = superellipse(w, h, 9.0, 1.2, bulge=0.035)
        else:  # téléviseur à façade claire : dalle plus petite, cadre blanc
            self.gw, self.gh = int(w * 0.74), int(h * 0.50)
            self.gx, self.gy = int(cx - self.gw / 2 - w * 0.03), int(cy - self.gh / 2 + h * 0.03)
            self.mask, r = superellipse(self.gw, self.gh, 14.0, 1.0, bulge=0.01)
        self.cx, self.cy, self.w, self.h = cx, cy, w, h
        gw, gh = self.gw, self.gh
        u, v = uv(gw, gh)
        # ombrage très léger : la réf. est presque plate jusqu'au bord du verre
        vig = 1 - 0.07 * smoothstep(0.7, 1.0, r) - 0.22 * smoothstep(0.965, 1.0, r)
        scan = np.where((np.arange(gh) % 3) == 0, 0.975, 1.0).astype(np.float32)[:, None]
        self.shade = (vig * scan).astype(np.float32)
        self.sheen = (0.012 * np.exp(-((u + 0.3) ** 2 + (v + 0.6) ** 2) / 0.5)).astype(np.float32)
        k = 0.93 + 0.07 * (u * u + v * v)              # bombé du tube
        self.my = np.clip(((v * k + 1) / 2 * gh), 0, gh - 1).astype(np.int64)
        self.mx = np.clip(((u * k + 1) / 2 * gw), 0, gw - 1).astype(np.int64)
        rng = np.random.default_rng(idx * 101 + 7)
        self.fl_phase = rng.uniform(0, 6.28)
        self.hum_phase = rng.uniform(0, 1)
        self.gain = rng.uniform(0.96, 1.03)

    def draw_casing(self, canvas):
        """Les CRT n'ont pas de boîtier visible (fondus dans le noir, cf. réf.).
        Les téléviseurs clairs ont une façade gris rosé bombée + cadre blanc."""
        if self.style == "crt":
            return
        ox, oy = PAD, PAD
        cw, ch = self.w, self.h
        m, r = superellipse(cw, ch, 5.0, 1.2, bulge=0.05)
        u, v = uv(cw, ch)
        light = 1.0 + 0.10 * (-v) - 0.06 * np.abs(u) + 0.05 * np.exp(-((u + 0.3) ** 2 + (v + 0.4) ** 2) / 0.3)
        col = np.array([100, 52, 45], np.float32) * light[..., None]
        col *= (1 - 0.18 * smoothstep(0.9, 1.0, r))[..., None]
        self._paint(canvas, int(self.cx - cw / 2) + ox, int(self.cy - ch / 2) + oy, col, m)
        fw = max(6, int(ch * 0.035))                    # cadre blanc
        fm, _ = superellipse(self.gw + 2 * fw, self.gh + 2 * fw, 16.0, 1.0)
        self._paint(canvas, self.gx - fw + ox, self.gy - fw + oy,
                    np.full(fm.shape + (3,), 1, np.float32) * np.array([188, 160, 154], np.float32), fm)
        dk = max(3, fw // 2)                            # filet sombre
        dm, _ = superellipse(self.gw + 2 * dk, self.gh + 2 * dk, 16.0, 1.0)
        self._paint(canvas, self.gx - dk + ox, self.gy - dk + oy,
                    np.full(dm.shape + (3,), 1, np.float32) * np.array([30, 14, 12], np.float32), dm)

    @staticmethod
    def _paint(canvas, x0, y0, col, m):
        h, w = m.shape
        Hc, Wc = canvas.shape[:2]
        xa, ya = max(0, x0), max(0, y0)
        xb, yb = min(Wc, x0 + w), min(Hc, y0 + h)
        if xa >= xb or ya >= yb:
            return
        sub = canvas[ya:yb, xa:xb].astype(np.float32)
        mm = m[ya - y0:yb - y0, xa - x0:xb - x0, None]
        cc = col[ya - y0:yb - y0, xa - x0:xb - x0]
        canvas[ya:yb, xa:xb] = np.clip(sub * (1 - mm) + cc * mm, 0, 255).astype(np.uint8)

    def segment_at(self, t):
        for seg in self.timeline:
            lt = (t - seg["start"]) % DUR
            if lt < seg["dur"]:
                return seg, lt
        return self.timeline[-1], 0.0

    def render(self, c, t, f, canvas):
        seg, lt = self.segment_at(t)
        gw, gh = self.gw, self.gh
        try:
            l = SCENES[seg["kind"]](c, seg, lt + seg.get("t0", 0.0), gw, gh)
        except Exception as e:  # un média cassé ne doit pas tuer le rendu
            print(f"[warn] écran {self.idx} {seg.get('src', seg['kind'])}: {e}", file=sys.stderr)
            seg["kind"] = "static"
            l = sc_static(c, seg, lt, gw, gh)
        l = np.array(l, np.float32, copy=True)
        if seg.get("osd"):
            l = overlay_osd(l, seg, lt, gw, gh)
        if seg.get("chyron"):
            l = overlay_chyron(c, l, seg, lt, gw, gh)

        # changement de chaîne : neige + roulement d'image
        TR = 0.28
        if lt < TR and seg["kind"] != "static":
            k = smoothstep(0.0, TR, lt)
            st = sc_static(c, seg, lt, gw, gh)
            l = np.roll(l, int((1 - k) * gh * 0.35), axis=0)
            l = l * k + st * (1 - k)

        rng = np.random.default_rng([f, self.idx])
        if rng.random() < 0.012:  # déchirure horizontale ponctuelle
            y0 = int(rng.uniform(0, 0.85) * gh)
            y1 = min(gh, y0 + int(rng.uniform(0.04, 0.2) * gh))
            l[y0:y1] = np.roll(l[y0:y1], int(rng.uniform(-0.2, 0.2) * gw), axis=1)

        y = np.arange(gh, dtype=np.float32) / gh
        hum = 1 + 0.07 * np.exp(-(((y - t / 6.0 - self.hum_phase) % 1.0 - 0.5) ** 2) / 0.01)
        l = l * hum[:, None]
        l = l[self.my, self.mx]                          # bombé

        flick = self.gain * (0.965 + 0.025 * math.sin(2 * math.pi * 8 * t + self.fl_phase)
                             + 0.02 * rng.random())
        idx = np.clip(l * 255, 0, 255).astype(np.uint8)
        rgb = c.lut[idx] * (self.shade * flick)[..., None]
        rgb += (self.sheen * 255)[..., None] * np.array([1.0, 0.82, 0.78], np.float32)
        self._paint(canvas, self.gx + PAD, self.gy + PAD, rgb, self.mask)


# ======================================================== mise en page =======
# Proportions relevées sur la réf. (écran ~4:3, interstice ~11 % de la largeur,
# colonne centrale légèrement décalée à droite, bords gauche/droit coupés).
ROWS = [140, 535, 930, 1325, 1720]
COLS = [110, 600, 1090]
SW, SH = 435, 340
MONITORS = {(1, 0), (4, 1)}  # téléviseurs à façade claire
HERO = (2, 1)


def layout():
    rng = np.random.default_rng(3)
    cells = []
    for ri, cy in enumerate(ROWS):
        for ci, cx in enumerate(COLS):
            style = "mon" if (ri, ci) in MONITORS else "crt"
            hero = (ri, ci) == HERO
            jx, jy = (0, 0) if hero else rng.integers(-3, 4, 2)
            jw, jh = (0, 0) if hero else rng.integers(-12, 9, 2)
            cells.append(dict(row=ri, col=ci, cx=int(cx + jx), cy=int(cy + jy),
                              w=int(SW + jw), h=int(SH + jh), style=style, hero=hero))
    return cells


def scan_sources(src):
    if not src:
        return [], []
    src = Path(src)
    files = sorted(p for p in src.rglob("*") if p.suffix.lower() in IMG_EXT | VID_EXT)
    hero = [p for p in files if "hero" in p.parts]
    rest = [p for p in files if p not in hero]
    return [str(p) for p in hero], [str(p) for p in rest]


def ref_plan(seed):
    """Démo sans médias : reprend la composition de la référence
    (œil au centre, silhouette au-dessus, branches en dessous, iris en macro
    dans le téléviseur clair, le reste en écrans allumés sans signal) et l'anime :
    zapping ponctuel, tirets qui changent, et un « écho » de l'œil sur
    plusieurs écrans vers 18 s."""
    rng = np.random.default_rng(seed)
    fixed = {
        (2, 1): [dict(kind="oeil", start=0.0, dur=DUR, seed=4)],
        (1, 1): [dict(kind="silhouette", start=0.0, dur=DUR, seed=2)],
        (1, 0): [dict(kind="oeil", zoom=3.2, start=0.0, dur=DUR, seed=9)],
        (4, 1): [dict(kind="oeil", zoom=2.2, start=0.0, dur=DUR, seed=21)],
        (3, 1): [dict(kind="fissures", start=3.0, dur=24.5, seed=5),
                 dict(kind="static", start=27.5, dur=0.5, seed=6),
                 dict(kind="blank", start=28.0, dur=5.0, seed=7)],
    }
    echo = {(2, 0), (2, 2), (1, 2), (3, 0), (3, 2)}
    ECHO_T, ECHO_D = 18.0, 1.4
    plan = []
    for cell in layout():
        key = (cell["row"], cell["col"])
        if key in fixed:
            segs = fixed[key]
        else:
            segs, t = [], float(rng.uniform(0, 4))
            stop = t + DUR
            while t < stop - 1e-6:
                end = t + float(rng.uniform(4.5, 10.0))
                if end > stop - 1.2:
                    end = stop
                segs.append(dict(kind="blank", start=round(t % DUR, 3), dur=round(end - t, 3),
                                 seed=int(rng.integers(1e6))))
                t = end
                if t < stop - 1e-6:   # zapping bref
                    z = float(rng.uniform(0.12, 0.35))
                    segs.append(dict(kind="static", start=round(t % DUR, 3), dur=round(z, 3),
                                     seed=int(rng.integers(1e6))))
                    t += z
            if key in echo:  # l'écho de l'œil prend le dessus sur la timeline
                segs.insert(0, dict(kind="oeil", start=ECHO_T, dur=ECHO_D, seed=4, t0=ECHO_T))
        plan.append(dict(row=cell["row"], col=cell["col"], timeline=segs))
    return plan


def auto_plan(seed, sources):
    hero_media, media = scan_sources(sources)
    rng = np.random.default_rng(seed)
    if media or hero_media:
        pool = {"media": 0.46, "blank": 0.28, "slogan": 0.09, "static": 0.05,
                "bars": 0.04, "fissures": 0.04, "silhouette": 0.04}
    else:
        pool = {"blank": 0.32, "manif": 0.14, "crs": 0.13, "feu": 0.09, "slogan": 0.1,
                "silhouette": 0.07, "fissures": 0.06, "static": 0.04, "bars": 0.03, "oeil": 0.02}
    kinds, wts = list(pool), np.array(list(pool.values()))
    wts = wts / wts.sum()
    media_cycle = list(media or hero_media)
    rng.shuffle(media_cycle)
    mi = 0
    plan = []
    for cell in layout():
        segs = []
        if cell["hero"]:
            hm = hero_media or []
            if hm:
                n = len(hm)
                d = DUR / n
                for i, p in enumerate(hm):
                    segs.append(dict(kind="media", src=p, start=round(i * d, 3), dur=round(d, 3),
                                     seed=int(rng.integers(1e6))))
            else:
                segs.append(dict(kind="oeil", start=0.0, dur=DUR, seed=int(rng.integers(1e6))))
        else:
            off = float(rng.uniform(0, DUR))
            total, last = 0.0, None
            while total < DUR - 1e-6:
                d = float(rng.uniform(2.6, 7.5))
                if DUR - total - d < 2.0:
                    d = DUR - total
                k = last
                while k == last:
                    k = str(rng.choice(kinds, p=wts))
                seg = dict(kind=k, start=round((off + total) % DUR, 3), dur=round(d, 3),
                           seed=int(rng.integers(1e6)))
                if k == "media":
                    seg["src"] = media_cycle[mi % len(media_cycle)]
                    seg["offset"] = round(float(rng.uniform(0, 4)), 2)
                    mi += 1
                if k in ("manif", "crs", "feu", "media") and rng.random() < 0.3:
                    seg["osd"] = True
                elif k in ("manif", "crs", "media") and rng.random() < 0.1:
                    seg["chyron"] = True
                segs.append(seg)
                total += d
                last = k
        plan.append(dict(row=cell["row"], col=cell["col"], timeline=segs))
    return plan


# =============================================================== rendu =======
def build_screens(plan):
    cells = {(c["row"], c["col"]): c for c in layout()}
    out = []
    for i, p in enumerate(plan):
        c = cells[(p["row"], p["col"])]
        out.append(Screen(i, c["cx"], c["cy"], c["w"], c["h"], c["style"], c["hero"], p["timeline"]))
    return out


def background(screens):
    Hc, Wc = H + 2 * PAD, W + 2 * PAD
    rng = np.random.default_rng(1)
    bg = np.empty((Hc, Wc, 3), np.uint8)
    bg[:] = BG_COLOR
    bg = np.clip(bg + rng.integers(0, 3, (Hc, Wc, 1)), 0, 255).astype(np.uint8)
    for s in screens:
        s.draw_casing(bg)
    return bg


def camera(canvas, t):
    """Lente poussée / dérive, périodique sur la boucle."""
    ph = 2 * math.pi * t / DUR
    z = 1.035 + 0.025 * (0.5 - 0.5 * math.cos(ph))
    dx = 14 * math.sin(ph)
    dy = 18 * math.sin(2 * ph + 0.6)
    cx, cy = PAD + W / 2 + dx, PAD + H / 2 + dy
    hw, hh = W / 2 / z, H / 2 / z
    im = Image.fromarray(canvas)
    return im.resize((W, H), Image.BICUBIC, box=(cx - hw, cy - hh, cx + hw, cy + hh))


# Look « photo de vrais écrans » : halo rouge large + glow serré, image
# légèrement douce, vignettage discret, grain fin.
FILTER = ("[0:v]format=gbrp,split=3[a][b][c];"
          "[b]scale=270:480,gblur=sigma=14,scale=1080:1920[g1];"
          "[c]scale=540:960,gblur=sigma=5,scale=1080:1920[g2];"
          "[a][g2]blend=all_mode=screen:all_opacity=0.26[a2];"
          "[a2][g1]blend=all_mode=screen:all_opacity=0.30,"
          "gblur=sigma=1.3,vignette=angle=0.45,format=yuv420p,noise=c0s=7:c0f=t[v]")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "out" / "mur_tele.mp4"))
    ap.add_argument("--sources", default=None, help="dossier d'images / vidéos (sous-dossier hero/ = écran central)")
    ap.add_argument("--plan", default=None, help="plan JSON à rejouer (sinon généré)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--stills", default=None, help="ex. 2,9,17 : exporte des PNG au lieu de la vidéo")
    ap.add_argument("--frames", default=None, help="ex. 0:120 : ne rendre qu'une plage (test)")
    ap.add_argument("--crf", type=int, default=20)
    args = ap.parse_args()

    if args.sources is None and (ROOT / "sources").exists() and any(
            p.suffix.lower() in IMG_EXT | VID_EXT for p in (ROOT / "sources").rglob("*")):
        args.sources = str(ROOT / "sources")

    if args.plan:
        plan = json.loads(Path(args.plan).read_text())
    else:
        plan = auto_plan(args.seed, args.sources) if args.sources else ref_plan(args.seed)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    (out.parent / "plan_utilise.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))

    ctx = Ctx(args.sources)
    screens = build_screens(plan)
    bg = background(screens)

    def frame(fi):
        t = fi / FPS
        canvas = bg.copy()
        for s in screens:
            s.render(ctx, t, fi, canvas)
        return camera(canvas, t)

    if args.stills:
        for ts in args.stills.split(","):
            fi = int(float(ts) * FPS)
            p = out.parent / f"still_{float(ts):05.1f}s.png"
            fx = FILTER.replace(",format=yuv420p", ",format=yuv444p")  # même look que la vidéo
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-i", "-", "-filter_complex", fx, "-map", "[v]",
                            "-frames:v", "1", str(p)], input=frame(fi).tobytes(), check=True)
            print("->", p)
        return

    a, b = 0, NF
    if args.frames:
        a, b = (int(x) for x in args.frames.split(":"))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-filter_complex", FILTER, "-map", "[v]",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf), "-profile:v", "high",
           "-maxrate", "16M", "-bufsize", "32M", "-r", str(FPS), "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(a, b):
        proc.stdin.write(frame(fi).tobytes())
        if fi % 60 == 0:
            print(f"frame {fi}/{b}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("->", out)


if __name__ == "__main__":
    main()
