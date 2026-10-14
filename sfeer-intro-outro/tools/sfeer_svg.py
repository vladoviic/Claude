"""Bibliothèque SVG SFEER : bulles de la charte, décors aplats du film, planches de storyboard.

Tout est en coordonnées d'image 1920 x 1080 (axe horizontal de la charte : y = 540).
Aucune dépendance : on assemble des chaînes SVG.

Géométrie des bulles
--------------------
La forme de la charte (pages 2.46, 3.1) = deux cercles reliés par un col concave.
On la construit comme sur la charte : chaque bord du col est un arc d'un cercle
« de col » tangent extérieurement aux deux bulles. Paramètre `h` = demi-épaisseur
du col au point le plus fin (0 = les bulles se touchent par un point, grand = gros col).
"""
from __future__ import annotations

import math
from html import escape

W, H = 1920, 1080
AXIS = 540

# --- Palette (charte 2.37) -------------------------------------------------
INDIGO = "#240852"
ORANGE = "#FF6720"
LAVENDER = "#817EFF"
WHITE = "#FFFFFF"
MID = "#5243A8"  # mélange 50/50 indigo-lavande, placé à 70 % du dégradé
# Teintes secondaires digitales (80/60/40/20 %)
ORANGE_T = {80: "#FF854D", 60: "#FFA479", 40: "#FFC2A6", 20: "#FFE1D2"}
INDIGO_T = {80: "#503975", 60: "#7C6B97", 40: "#A79CBA", 20: "#D3CEDC"}
LAV_T = {80: "#9A98FF", 60: "#B3B2FF", 40: "#CDCBFF", 20: "#E6E5FF"}

# Décors du film (monde monochrome orange, studio) : nuances d'éclairage
SET = {
    "light": "#FF8A45",
    "base": "#F2601C",
    "mid": "#DE5014",
    "dark": "#C2410E",
    "deep": "#9E330B",
    "glow": "#FFC58F",
    "sky": "#FFD9B0",
}
COSTUME = "#2C2A9E"   # bleu-violet des costumes du film
COSTUME_D = "#1E1C74"
SKIN = "#8C4A2C"
SCARF = "#F3ECE4"

FONT = "Inter, 'Loew Riyadh Air', Arial, sans-serif"
FONT_AR = "'Loew Riyadh Air Arabic', 'DejaVu Sans', sans-serif"


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


# --- Fonds -----------------------------------------------------------------
def defs_gradient(gid: str = "sfeerGrad") -> str:
    """Dégradé principal indigo -> lavande, point milieu à 70 % (charte 2.37)."""
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{INDIGO}"/>'
        f'<stop offset="0.7" stop-color="{MID}"/>'
        f'<stop offset="1" stop-color="{LAVENDER}"/></linearGradient>'
    )


def bg(kind: str = "gradient", gid: str = "sfeerGrad") -> str:
    fill = {
        "gradient": f"url(#{gid})",
        "indigo": INDIGO,
        "orange": ORANGE,
        "lavender": LAVENDER,
        "white": WHITE,
    }.get(kind, kind)
    return f'<rect id="fond" width="{W}" height="{H}" fill="{fill}"/>'


# --- Géométrie des bulles ---------------------------------------------------
def circle_d(cx: float, cy: float, r: float) -> str:
    return (
        f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 0 {f(2 * r)} 0"
        f"a{f(r)} {f(r)} 0 1 0 {f(-2 * r)} 0Z"
    )


def _neck_circle(c1, c2, h):
    """Rayon R et centre x du cercle de col tangent aux deux bulles (axe horizontal)."""
    (x1, _, r1), (x2, _, r2) = c1, c2
    d = x2 - x1
    # xn - x1 = m + k R ; tangence aux deux bulles => équation du 2nd degré en R
    k = (r1 - r2) / d
    m = d / 2 + (r1 - r2) * (r1 + r2) / (2 * d)
    a = k * k
    b = 2 * m * k + 2 * (h - r1)
    c = m * m + h * h - r1 * r1
    if abs(a) < 1e-12:
        if b == 0:
            return None
        roots = [-c / b]
    else:
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
        sq = math.sqrt(disc)
        roots = [(-b - sq) / (2 * a), (-b + sq) / (2 * a)]
    roots = sorted(R for R in roots if R > 1e-6)
    if not roots:
        return None
    R = roots[0]
    return R, x1 + m + k * R


def waist_h(c1, c2, t: float = 0.35) -> float:
    """Demi-épaisseur de col valide pour deux bulles qui se chevauchent (pose « cacahuète »).

    Le col doit être plus épais que le point d'intersection des deux cercles :
    t=0 -> pincement maximal, t=1 -> plus de taille (gélule).
    """
    (x1, _, r1), (x2, _, r2) = c1, c2
    d = abs(x2 - x1)
    rmin = min(r1, r2)
    if d >= r1 + r2:
        return rmin * 0.12 + t * rmin * 0.5
    a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    yi = math.sqrt(max(r1 * r1 - a * a, 0))
    return yi + t * (rmin - yi) * 0.98


def bridge_d(c1, c2, h: float) -> str:
    """Contour de deux bulles reliées par le col de la charte.

    c1, c2 = (cx, cy, r) avec c1 à gauche de c2, même cy. h = demi-épaisseur du col.
    Si h >= min(r1, r2) le col disparaît (les bulles fusionnent visuellement) :
    on renvoie alors l'union des deux cercles + une capsule.
    """
    (x1, cy, r1), (x2, _, r2) = c1, c2
    if x2 < x1:
        (x1, cy, r1), (x2, _, r2) = c2, c1
        c1, c2 = c2, c1
    d = x2 - x1
    if d <= abs(r1 - r2):  # un cercle contient l'autre
        big = c1 if r1 >= r2 else c2
        return circle_d(*big)
    sol = _neck_circle((x1, cy, r1), (x2, cy, r2), h) if h < min(r1, r2) else None
    if sol is None:
        # col plein : enveloppe convexe simple (tangentes extérieures) = fusion
        ang = math.asin(max(-1, min(1, (r1 - r2) / d)))
        nx, ny = math.sin(ang), math.cos(ang)
        p1u = (x1 + r1 * nx, cy - r1 * ny)
        p2u = (x2 + r2 * nx, cy - r2 * ny)
        p2d = (x2 + r2 * nx, cy + r2 * ny)
        p1d = (x1 + r1 * nx, cy + r1 * ny)
        return (
            f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}"
            f"A{f(r2)} {f(r2)} 0 0 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 0 1 {f(p1u[0])} {f(p1u[1])}Z"
        )
    R, xn = sol
    yn = R + h
    nu = (xn, cy - yn)
    nd = (xn, cy + yn)

    def tangent(cx, r, n):
        vx, vy = n[0] - cx, n[1] - cy
        L = math.hypot(vx, vy)
        return (cx + r * vx / L, cy + r * vy / L)

    t1u, t2u = tangent(x1, r1, nu), tangent(x2, r2, nu)
    t1d, t2d = tangent(x1, r1, nd), tangent(x2, r2, nd)

    def span(cx, a, b):
        aa = math.atan2(a[1] - cy, a[0] - cx)
        bb = math.atan2(b[1] - cy, b[0] - cx)
        return (bb - aa) % (2 * math.pi)

    l2 = 1 if span(x2, t2u, t2d) > math.pi else 0
    l1 = 1 if span(x1, t1d, t1u) > math.pi else 0
    return (
        f"M{f(t1u[0])} {f(t1u[1])}"
        f"A{f(R)} {f(R)} 0 0 0 {f(t2u[0])} {f(t2u[1])}"
        f"A{f(r2)} {f(r2)} 0 {l2} 1 {f(t2d[0])} {f(t2d[1])}"
        f"A{f(R)} {f(R)} 0 0 0 {f(t1d[0])} {f(t1d[1])}"
        f"A{f(r1)} {f(r1)} 0 {l1} 1 {f(t1u[0])} {f(t1u[1])}Z"
    )


def chain_d(circles, h) -> str:
    """Chaîne de bulles (3.5) : union des ponts successifs. h scalaire ou liste."""
    hs = h if isinstance(h, (list, tuple)) else [h] * (len(circles) - 1)
    parts = []
    for i in range(len(circles) - 1):
        if hs[i] is None:  # bulles séparées
            parts.append(circle_d(*circles[i]))
            parts.append(circle_d(*circles[i + 1]))
        else:
            parts.append(bridge_d(circles[i], circles[i + 1], hs[i]))
    if len(circles) == 1:
        parts.append(circle_d(*circles[0]))
    return " ".join(parts)


def shape(d: str, fill: str = ORANGE, sid: str = "", extra: str = "") -> str:
    idattr = f' id="{sid}"' if sid else ""
    return f'<path{idattr} d="{d}" fill="{fill}" fill-rule="nonzero"{extra}/>'


def window(d: str, content: str, wid: str, ring: str | None = None, ring_w: float = 0) -> str:
    """Fenêtre-bulle : le contenu (décor du film) est découpé par la forme d."""
    out = [f'<clipPath id="{wid}"><path d="{d}"/></clipPath>']
    out.append(f'<g id="{wid}-film" clip-path="url(#{wid})">{content}</g>')
    if ring:
        out.append(f'<path d="{d}" fill="none" stroke="{ring}" stroke-width="{f(ring_w)}"/>')
    return "".join(out)


def scaled(content: str, s: float, cx: float = W / 2, cy: float = H / 2, dx: float = 0, dy: float = 0) -> str:
    """Zoom d'un décor autour de (cx, cy) : simule l'approche caméra."""
    return (
        f'<g transform="translate({f(cx + dx)} {f(cy + dy)}) scale({f(s)}) '
        f'translate({f(-cx)} {f(-cy)})">{content}</g>'
    )


# --- Logo (gabarit) ---------------------------------------------------------
def logo(x: float, y: float, size: float = 1.0, color: str = WHITE, arabic: bool = True,
         anchor: str = "bl", dots: bool = True, letters: str = "sfeer", lid: str = "logo") -> str:
    """Gabarit du logo bilingue ·sfeer· / سفير (à remplacer par le vectoriel officiel).

    size=1 -> wordmark ~ 260 px de large. anchor 'bl' : (x, y) = coin bas-gauche du bloc,
    'c' : centre du mot latin. Les deux points sont de vrais cercles (ids logo-dot-g/d)
    pour pouvoir les animer comme des bulles.
    """
    fs = 64 * size
    word_w = {"sfeer": 0.82, "e": 0.18}.get(letters, 0.82) * fs * len(letters) / 5 * (5 if letters == "sfeer" else 1)
    if letters == "sfeer":
        word_w = 3.55 * fs
    elif letters == "e":
        word_w = 0.62 * fs
    dot_r = 0.085 * fs
    gap = 0.32 * fs
    total = word_w + 2 * (gap + dot_r * 2) if dots else word_w
    block_h = fs * (1.55 if arabic else 0.75)
    if anchor == "bl":
        x0, base = x, y - (block_h - fs * 0.72)
    else:  # centre du mot latin
        x0, base = x - total / 2, y + fs * 0.26
    cy_dot = base - fs * 0.26
    out = [f'<g id="{lid}" font-family="{FONT}">']
    xd = x0
    if dots:
        out.append(f'<circle id="{lid}-dot-g" cx="{f(xd + dot_r)}" cy="{f(cy_dot)}" r="{f(dot_r)}" fill="{color}"/>')
        xd += 2 * dot_r + gap
    out.append(
        f'<text x="{f(xd)}" y="{f(base)}" font-size="{f(fs)}" font-weight="400" '
        f'letter-spacing="{f(fs * 0.16)}" fill="{color}" textLength="{f(word_w)}" '
        f'lengthAdjust="spacingAndGlyphs">{letters}</text>'
    )
    if dots:
        xr = xd + word_w + gap
        out.append(f'<circle id="{lid}-dot-d" cx="{f(xr + dot_r)}" cy="{f(cy_dot)}" r="{f(dot_r)}" fill="{color}"/>')
    if arabic:
        out.append(
            f'<text x="{f(xd + 0.12 * fs)}" y="{f(base + fs * 0.92)}" font-family="{FONT_AR}" '
            f'font-size="{f(fs * 0.86)}" fill="{color}" textLength="{f(word_w * 0.56)}" '
            f'lengthAdjust="spacing">سفيـــــر</text>'
        )
    out.append("</g>")
    return "".join(out)


def endorsement(x: float, y: float, size: float = 1.0, color: str = WHITE, anchor: str = "end") -> str:
    fs = 26 * size
    return (
        f'<text id="endorsement" x="{f(x)}" y="{f(y)}" font-family="{FONT}" font-size="{f(fs)}" '
        f'fill="{color}" text-anchor="{anchor}">Powered by '
        f'<tspan font-weight="500" letter-spacing="{f(fs * 0.04)}">RIYADH AIR</tspan></text>'
    )


def lockup_end(color: str = WHITE, margin: float = 120, size: float = 1.0) -> str:
    """Logo en bas à gauche + endossement opposé en bas à droite (charte 2.12 / 2.47)."""
    return logo(margin, H - margin, size, color) + endorsement(W - margin, H - margin - 10 * size, size, color)


# --- Personnages aplats ----------------------------------------------------
def figure(x, feet, h, pose="stand", robe=COSTUME, scarf=SCARF, hijab=False, glasses=False,
           flip=False, fid="") -> str:
    """Silhouette aplat (robe longue, tête, coiffe). x = centre, feet = y des pieds."""
    s = h / 100.0
    t = f"translate({f(x)} {f(feet)}) scale({f(-s if flip else s)} {f(s)})"
    head_y = -88
    parts = []
    if pose == "sit":
        parts.append(f'<path d="M-15 -70 Q-18 -40 -16 -28 L30 -28 L34 -4 L22 -4 L18 -16 L-22 -16 Q-30 -40 -18 -72Z" fill="{robe}"/>')
        parts.append(f'<path d="M-14 -72 Q0 -78 14 -72 L14 -40 L-14 -40Z" fill="{robe}"/>')
        head_y = -82
    elif pose == "walk":
        parts.append(f'<path d="M-12 -74 Q0 -80 12 -74 L20 -4 L6 0 L0 -20 L-8 0 L-24 -4Z" fill="{robe}"/>')
        parts.append(f'<path d="M-12 -70 L-22 -38 L-17 -36 L-6 -62Z" fill="{COSTUME_D}"/>')
    else:
        parts.append(f'<path d="M-12 -74 Q0 -80 12 -74 L18 0 L-18 0Z" fill="{robe}"/>')
        parts.append(f'<path d="M-12 -70 L-16 -36 L-11 -36 L-7 -62Z" fill="{COSTUME_D}"/>')
    if hijab:
        parts.append(f'<path d="M-9 {head_y + 2} Q-10 {head_y - 13} 0 {head_y - 13} Q10 {head_y - 13} 9 {head_y + 2} L12 {head_y + 16} L-12 {head_y + 16}Z" fill="{robe}"/>')
        parts.append(f'<ellipse cx="1.5" cy="{head_y + 1}" rx="5" ry="6.5" fill="{SKIN}"/>')
    else:
        parts.append(f'<circle cx="0" cy="{head_y}" r="7.5" fill="{SKIN}"/>')
        if scarf:
            parts.append(f'<path d="M-9 {head_y - 2} Q0 {head_y - 14} 9 {head_y - 2} L13 {head_y + 14} L4 {head_y + 4} L-4 {head_y + 4} L-13 {head_y + 14}Z" fill="{scarf}"/>')
            parts.append(f'<rect x="-8.5" y="{head_y - 6}" width="17" height="2.6" rx="1.3" fill="{COSTUME_D}"/>')
    if glasses:
        parts.append(f'<rect x="-6" y="{head_y - 2}" width="13" height="4" rx="1" fill="{WHITE}"/>')
    idattr = f' id="{fid}"' if fid else ""
    return f'<g{idattr} transform="{t}">{"".join(parts)}</g>'


# --- Décors aplats des séquences du film ------------------------------------
def scene_cabin() -> str:
    """Séq. 01 : cabine d'avion abstraite, hublots ovales, homme assis face caméra."""
    S = SET
    o = ['<g id="decor-s01-cabine">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["base"]}"/>')
    o.append(f'<path d="M0 0H1920L1260 330H660Z" fill="{S["mid"]}"/>')
    for i, (a, b) in enumerate([(560, 620), (900, 1020), (1300, 1360)]):
        o.append(f'<path d="M{a} 0H{b}L{660 + (b - 0) * 0.31:.0f} 330H{660 + a * 0.31:.0f}Z" fill="{S["glow"]}" opacity="0.85"/>')
    o.append(f'<path d="M0 1080H1920L1260 760H660Z" fill="{S["dark"]}"/>')
    o.append(f'<path d="M0 0L660 330V760L0 1080Z" fill="{S["light"]}"/>')
    o.append(f'<path d="M1920 0L1260 330V760L1920 1080Z" fill="{S["mid"]}"/>')
    o.append(f'<rect x="660" y="330" width="600" height="430" fill="{S["base"]}"/>')
    o.append(f'<circle cx="960" cy="545" r="190" fill="none" stroke="{S["mid"]}" stroke-width="10"/>')
    for x, sk in [(300, -12), (1620, 12)]:
        o.append(f'<g transform="translate({x} 500) skewY({sk})"><ellipse rx="78" ry="118" fill="{S["deep"]}"/>'
                 f'<ellipse rx="62" ry="100" fill="{S["sky"]}"/><ellipse rx="62" ry="40" cy="45" fill="{S["glow"]}"/></g>')
    o.append(f'<path d="M150 1080L420 860H560L520 1080Z" fill="{S["mid"]}"/>')
    o.append(f'<path d="M1770 1080L1500 860H1360L1400 1080Z" fill="{S["deep"]}"/>')
    # fauteuil bleu + passager
    o.append(f'<path d="M830 880 Q825 660 960 650 Q1095 660 1090 880Z" fill="#4A44C4"/>')
    o.append(f'<rect x="780" y="780" width="360" height="110" rx="40" fill="#4A44C4"/>')
    o.append(figure(960, 905, 420, pose="sit", fid="passager"))
    o.append(f'<ellipse cx="960" cy="905" rx="230" ry="26" fill="{S["deep"]}" opacity="0.5"/>')
    o.append("</g>")
    return "".join(o)


def scene_street(walkers: int = 2) -> str:
    """Séq. 02/08/09 : rue de blocs orange en contre-plongée, couple qui marche."""
    S = SET
    o = ['<g id="decor-s02-rue">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["sky"]}"/>')
    o.append(f'<rect y="560" width="{W}" height="520" fill="{S["mid"]}"/>')
    blocks = [
        (0, 0, 330, 1080, S["dark"]), (300, 120, 220, 600, S["base"]), (500, 260, 150, 380, S["light"]),
        (640, 360, 90, 240, S["mid"]), (1590, 0, 330, 1080, S["deep"]), (1400, 100, 220, 620, S["mid"]),
        (1270, 250, 150, 400, S["base"]), (1190, 350, 90, 260, S["light"]),
    ]
    for x, y, w, h, c in blocks:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
    o.append(f'<path d="M760 600H1160L1500 1080H420Z" fill="{S["base"]}"/>')
    o.append(f'<path d="M760 600H1160L1250 680H670Z" fill="{S["glow"]}" opacity="0.6"/>')
    if walkers >= 1:
        o.append(figure(880, 960, 330, pose="walk", hijab=True, fid="marcheuse"))
    if walkers >= 2:
        o.append(figure(1060, 975, 350, pose="walk", fid="marcheur"))
        for bx in (1095, 1110):
            o.append(f'<rect x="{bx}" y="880" width="30" height="40" fill="{S["glow"]}"/>')
    o.append("</g>")
    return "".join(o)


def scene_cinema() -> str:
    """Séq. 05 : cinéma, deux femmes en lunettes 3D, pop-corn figé (bullet time)."""
    S = SET
    o = ['<g id="decor-s05-cinema">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["mid"]}"/>')
    for i, r in enumerate([760, 600, 440]):
        c = [S["base"], S["light"], S["glow"]][i]
        o.append(f'<path d="M{960 - r} 1080V{560}A{r} {r} 0 0 1 {960 + r} 560V1080Z" fill="{c}"/>')
    o.append(f'<path d="M{960 - 300} 1080V600A300 300 0 0 1 {960 + 300} 600V1080Z" fill="{S["mid"]}"/>')
    o.append(figure(880, 1080, 560, hijab=True, glasses=True, fid="spectatrice-1"))
    o.append(figure(1040, 1080, 545, glasses=True, scarf=None, fid="spectatrice-2"))
    o.append(f'<circle cx="1040" cy="595" r="40" fill="{COSTUME_D}"/>')
    import random
    rnd = random.Random(5)
    for _ in range(26):
        x, y, r = rnd.uniform(80, 1840), rnd.uniform(60, 1000), rnd.uniform(10, 34)
        if 760 < x < 1160 and y > 500:
            continue
        o.append(f'<g transform="translate({f(x)} {f(y)})"><circle r="{f(r)}" fill="#FFF3DF"/>'
                 f'<circle cx="{f(r * .6)}" cy="{f(-r * .4)}" r="{f(r * .7)}" fill="#FFE7C2"/>'
                 f'<circle cx="{f(-r * .5)}" cy="{f(r * .5)}" r="{f(r * .55)}" fill="#FFF8EC"/></g>')
    o.append("</g>")
    return "".join(o)


def scene_spheres() -> str:
    """Séq. 12 : femme qui empile des sphères (chaque sphère = un point gagné)."""
    S = SET
    o = ['<g id="decor-s12-spheres">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["sky"]}"/>')
    o.append(f'<rect y="700" width="{W}" height="380" fill="{S["base"]}"/>')
    o.append(f'<path d="M100 700V260A140 140 0 0 1 380 260V700Z" fill="{S["mid"]}"/>')
    o.append(f'<path d="M180 700V320A60 60 0 0 1 300 320V700Z" fill="{S["sky"]}"/>')
    o.append(f'<rect x="1500" y="300" width="260" height="400" fill="{S["dark"]}"/>')

    def sphere(cx, cy, r):
        return (f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{S["base"]}"/>'
                f'<path d="M{f(cx + r * .2)} {f(cy - r * .98)}A{f(r)} {f(r)} 0 0 1 {f(cx + r * .2)} {f(cy + r * .98)}'
                f'A{f(r * 1.1)} {f(r * 1.1)} 0 0 0 {f(cx + r * .2)} {f(cy - r * .98)}Z" fill="{S["dark"]}"/>'
                f'<circle cx="{f(cx - r * .35)}" cy="{f(cy - r * .35)}" r="{f(r * .22)}" fill="{S["light"]}"/>')
    y = 900
    for r in (150, 110, 85, 64):
        o.append(sphere(1120, y - r, r))
        y -= 2 * r - 6
    o.append(sphere(330, 860, 120))
    o.append(sphere(1650, 960, 90))
    o.append(figure(860, 900, 420, pose="walk", hijab=True, flip=True, fid="empileuse"))
    o.append(f'<ellipse cx="1120" cy="905" rx="190" ry="20" fill="{S["deep"]}" opacity="0.4"/>')
    o.append("</g>")
    return "".join(o)


def scene_platform() -> str:
    """Séq. 13 : grande plateforme circulaire, la communauté se rassemble."""
    S = SET
    o = ['<g id="decor-s13-plateforme">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["sky"]}"/>')
    o.append(f'<rect y="520" width="{W}" height="560" fill="{S["base"]}"/>')
    o.append(f'<rect x="120" y="140" width="420" height="380" fill="{S["mid"]}"/>')
    o.append(f'<circle cx="330" cy="320" r="110" fill="{S["sky"]}"/>')
    for i in range(5):
        o.append(f'<rect x="{1320 + i * 90}" y="180" width="46" height="340" fill="{S["dark"]}"/>')
    o.append(f'<rect x="1300" y="160" width="460" height="40" fill="{S["dark"]}"/>')
    o.append(f'<ellipse cx="960" cy="760" rx="560" ry="150" fill="{S["dark"]}"/>')
    o.append(f'<ellipse cx="960" cy="730" rx="560" ry="150" fill="{S["light"]}"/>')
    o.append(f'<circle cx="1560" cy="610" r="90" fill="{S["mid"]}"/>')
    import random
    rnd = random.Random(13)
    pts = [(rnd.uniform(520, 1400), rnd.uniform(640, 820)) for _ in range(14)]
    for x, y in sorted(pts, key=lambda p: p[1]):
        o.append(figure(x, y, rnd.uniform(130, 170), pose=rnd.choice(["stand", "walk"]),
                        hijab=rnd.random() < .4, flip=rnd.random() < .5))
    o.append("</g>")
    return "".join(o)


def scene_tank() -> str:
    """Séq. 07 : vue depuis l'intérieur du réservoir, espace violet, ouverture orange ronde."""
    o = ['<g id="decor-s07-reservoir">']
    o.append(f'<rect width="{W}" height="{H}" fill="{INDIGO}"/>')
    o.append(f'<circle cx="960" cy="540" r="330" fill="{SET["base"]}"/>')
    o.append(f'<circle cx="960" cy="540" r="330" fill="none" stroke="{MID}" stroke-width="26"/>')
    o.append(f'<path d="M700 760 Q960 640 1220 700" stroke="{SET["dark"]}" stroke-width="40" fill="none"/>')
    o.append(figure(960, 830, 420, fid="pompiste"))
    o.append("</g>")
    return "".join(o)


def scene_city_top() -> str:
    """Séq. 03/04 : plongée verticale sur la ville orange (blocs et ombres)."""
    S = SET
    o = ['<g id="decor-s03-ville">']
    o.append(f'<rect width="{W}" height="{H}" fill="{S["mid"]}"/>')
    o.append('<g transform="rotate(-32 960 540)">')
    for i in range(-6, 14):
        for j in range(-6, 10):
            x, y = i * 190, j * 170
            o.append(f'<rect x="{x + 40}" y="{y + 40}" width="130" height="110" fill="{S["deep"]}"/>')
            o.append(f'<rect x="{x + 20}" y="{y + 20}" width="130" height="110" fill="{S["light"] if (i + j) % 3 else S["base"]}"/>')
    o.append("</g>")
    o.append(f'<circle cx="960" cy="540" r="90" fill="{S["glow"]}"/>')
    o.append(figure(960, 560, 60, hijab=True, fid="voyageuse"))
    o.append("</g>")
    return "".join(o)


SCENES = {
    "s01": scene_cabin,
    "s02": scene_street,
    "s03": scene_city_top,
    "s05": scene_cinema,
    "s07": scene_tank,
    "s12": scene_spheres,
    "s13": scene_platform,
}


# --- Annotations de storyboard ---------------------------------------------
ANNOT = "#FFFFFF"


def arrow(x1, y1, x2, y2, color=ANNOT, w=8, head=28, dash=False) -> str:
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1 = x2 - head * math.cos(ang - 0.45)
    hy1 = y2 - head * math.sin(ang - 0.45)
    hx2 = x2 - head * math.cos(ang + 0.45)
    hy2 = y2 - head * math.sin(ang + 0.45)
    da = ' stroke-dasharray="18 14"' if dash else ""
    return (
        f'<g class="annot"><line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{color}" '
        f'stroke-width="{w}" stroke-linecap="round"{da}/>'
        f'<path d="M{f(x2)} {f(y2)}L{f(hx1)} {f(hy1)}L{f(hx2)} {f(hy2)}Z" fill="{color}"/></g>'
    )


def curved_arrow(x1, y1, cx, cy, x2, y2, color=ANNOT, w=8, head=28) -> str:
    ang = math.atan2(y2 - cy, x2 - cx)
    hx1 = x2 - head * math.cos(ang - 0.45)
    hy1 = y2 - head * math.sin(ang - 0.45)
    hx2 = x2 - head * math.cos(ang + 0.45)
    hy2 = y2 - head * math.sin(ang + 0.45)
    return (
        f'<g class="annot"><path d="M{f(x1)} {f(y1)}Q{f(cx)} {f(cy)} {f(x2)} {f(y2)}" fill="none" '
        f'stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
        f'<path d="M{f(x2)} {f(y2)}L{f(hx1)} {f(hy1)}L{f(hx2)} {f(hy2)}Z" fill="{color}"/></g>'
    )


def ghost(d: str, color=ANNOT, w=5) -> str:
    """Contour pointillé : état précédent / suivant d'une forme."""
    return f'<path class="annot" d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-dasharray="16 14" opacity="0.8"/>'


def zoom_brackets(cx, cy, w, h, color=ANNOT, L=60, sw=8) -> str:
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    p = []
    for (x, y, dx, dy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        p.append(f"M{f(x + dx * L)} {f(y)}H{f(x)}V{f(y + dy * L)}")
    return f'<path class="annot" d="{" ".join(p)}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def label(x, y, txt, size=34, color=ANNOT, anchor="start", weight=500) -> str:
    return (f'<text class="annot" x="{f(x)}" y="{f(y)}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(txt)}</text>')


def axis_line(color=ANNOT) -> str:
    """Axe horizontal de la charte (repère de mise en page)."""
    return f'<line class="annot" x1="0" y1="{AXIS}" x2="{W}" y2="{AXIS}" stroke="{color}" stroke-width="3" stroke-dasharray="22 16" opacity="0.55"/>'


# --- Images et planches -----------------------------------------------------
def frame_svg(inner: str, defs: str = "", title: str = "") -> str:
    """Image 1920x1080 autonome (importable dans Illustrator / After Effects)."""
    t = f"<title>{escape(title)}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
        f"{t}<defs>{defs_gradient()}{defs}</defs>{inner}</svg>"
    )


def wrap(text: str, max_chars: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + (1 if cur else 0) > max_chars:
            lines.append(cur)
            cur = wd
        else:
            cur = f"{cur} {wd}" if cur else wd
    if cur:
        lines.append(cur)
    return lines


class Board:
    """Planche de storyboard : en-tête, sections (intro/outro), vignettes 16:9 + légendes."""

    def __init__(self, num: str, title: str, logline: str, cols: int = 4, thumb_w: int = 600):
        self.num, self.title, self.logline = num, title, logline
        self.cols, self.tw = cols, thumb_w
        self.th = thumb_w * 9 / 16
        self.sections: list[tuple[str, list]] = []
        self.notes: list[tuple[str, list[str]]] = []

    def section(self, name: str, frames: list):
        """frames : liste de dict(inner=svg 1920x1080, tc='0.0–0.6 s', cap='légende', defs='')"""
        self.sections.append((name, frames))

    def note(self, heading: str, lines: list[str]):
        self.notes.append((heading, lines))

    def render(self) -> str:
        pad, gap = 70, 34
        cap_lines = 4
        cap_h = 34 * cap_lines + 70
        width = pad * 2 + self.cols * self.tw + (self.cols - 1) * gap
        y = 0
        body = []
        # en-tête
        head_h = 260
        body.append(f'<rect width="{width}" height="{head_h}" fill="url(#sfeerGrad)"/>')
        body.append(f'<text x="{pad}" y="92" font-family="{FONT}" font-size="30" fill="{ORANGE}" font-weight="600" letter-spacing="3">SFEER · INTRO / OUTRO · CONCEPT {escape(self.num)}</text>')
        body.append(f'<text x="{pad}" y="160" font-family="{FONT}" font-size="64" fill="{WHITE}" font-weight="700">{escape(self.title)}</text>')
        for i, ln in enumerate(wrap(self.logline, 150)[:2]):
            body.append(f'<text x="{pad}" y="{208 + i * 36}" font-family="{FONT}" font-size="28" fill="{WHITE}" opacity="0.92">{escape(ln)}</text>')
        y = head_h + 50
        uid = 0
        for name, frames in self.sections:
            body.append(f'<text x="{pad}" y="{y + 40}" font-family="{FONT}" font-size="40" font-weight="700" fill="{INDIGO}">{escape(name)}</text>')
            body.append(f'<line x1="{pad}" y1="{y + 62}" x2="{width - pad}" y2="{y + 62}" stroke="{INDIGO}" stroke-width="2" opacity="0.25"/>')
            y += 90
            for k, fr in enumerate(frames):
                c, r = k % self.cols, k // self.cols
                x0 = pad + c * (self.tw + gap)
                y0 = y + r * (self.th + cap_h + gap)
                uid += 1
                inner = fr["inner"].replace('id="', f'id="f{uid}-').replace("url(#", f"url(#f{uid}-").replace("url(#f%d-sfeerGrad)" % uid, "url(#sfeerGrad)")
                defs = fr.get("defs", "").replace('id="', f'id="f{uid}-').replace("url(#", f"url(#f{uid}-")
                body.append(
                    f'<svg x="{f(x0)}" y="{f(y0)}" width="{f(self.tw)}" height="{f(self.th)}" viewBox="0 0 {W} {H}" overflow="hidden">'
                    f"<defs>{defs}</defs>{inner}</svg>"
                )
                body.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(self.tw)}" height="{f(self.th)}" fill="none" stroke="{INDIGO}" stroke-width="2"/>')
                body.append(f'<circle cx="{f(x0 + 30)}" cy="{f(y0 + 30)}" r="20" fill="{ORANGE}"/>')
                body.append(f'<text x="{f(x0 + 30)}" y="{f(y0 + 38)}" font-family="{FONT}" font-size="22" font-weight="700" fill="{INDIGO}" text-anchor="middle">{k + 1}</text>')
                body.append(f'<text x="{f(x0)}" y="{f(y0 + self.th + 38)}" font-family="{FONT}" font-size="24" font-weight="700" fill="{ORANGE}">{escape(fr.get("tc", ""))}</text>')
                for li, ln in enumerate(wrap(fr.get("cap", ""), int(self.tw / 13.2))[:cap_lines]):
                    body.append(f'<text x="{f(x0)}" y="{f(y0 + self.th + 74 + li * 32)}" font-family="{FONT}" font-size="23" fill="{INDIGO}">{escape(ln)}</text>')
            rows = math.ceil(len(frames) / self.cols)
            y += rows * (self.th + cap_h + gap) + 30
        # notes
        if self.notes:
            ncols = min(3, len(self.notes))
            colw = (width - 2 * pad - (ncols - 1) * 50) / ncols
            max_h = 0
            for i, (hd, lines) in enumerate(self.notes):
                x0 = pad + (i % ncols) * (colw + 50)
                yy = y + 40 + (i // ncols) * 0
                body.append(f'<text x="{f(x0)}" y="{f(yy)}" font-family="{FONT}" font-size="30" font-weight="700" fill="{ORANGE}">{escape(hd)}</text>')
                yy += 46
                for ln in lines:
                    wl = wrap(ln, int(colw / 12.6))
                    for j, piece in enumerate(wl):
                        prefix = "• " if j == 0 else "  "
                        body.append(f'<text x="{f(x0)}" y="{f(yy)}" font-family="{FONT}" font-size="23" fill="{INDIGO}" xml:space="preserve">{escape(prefix + piece)}</text>')
                        yy += 32
                    yy += 8
                max_h = max(max_h, yy - y)
            y += max_h + 30
        y += 40
        body.append(f'<text x="{pad}" y="{y - 14}" font-family="{FONT}" font-size="20" fill="{INDIGO}" opacity="0.6">Storyboard marble.studio · gabarit logo, typo Inter en remplacement de Loew Riyadh Air · décors du film simplifiés en aplats</text>')
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(width)} {f(y)}" width="{f(width)}" height="{f(y)}">'
            f'<defs>{defs_gradient()}</defs><rect width="100%" height="100%" fill="{WHITE}"/>{"".join(body)}</svg>'
        )
