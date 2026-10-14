"""Concept original O4 : « La Jonction, on entre par le lien ».

Deux bulles égales, jointes par le col de la charte (forme héros 3.1), s'ouvrent chacune sur
la vidéo : deux plaques, deux regards (décadrés et zoomés en sens contraires). La caméra plonge
vers leur cou et les bulles se rejoignent pendant la plongée (3.3-01) : les deux regards
s'alignent comme dans un télémètre de mise au point et la jonction devient le plein cadre.
Outro : le cadre se pince en deux bulles, la scission rejoue 3.3-01, puis la paire se
contracte et éclate en deux points : ceux du logo.

Différence avec la piste 5 (p05) : ici les fenêtres sont les bulles elles-mêmes, formes
positives au centre du cadre, et c'est leur RÉUNION qui ouvre le plein cadre.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, GREEN, GREEN_D, GREEN_L, Anim, Beat, Track, bezier, breathe, clamp01, lerp, prog  # noqa: E402
from blocks import LG, endcard, squash, video  # noqa: E402
from sfeer_svg import AXIS, H, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, curved_arrow, f, mix_hex  # noqa: E402

CX = W / 2

META = {
    "id": "o4_jonction",
    "num": "O4",
    "title": "La Jonction",
    "principe": "Deux bulles jointes sont deux fenêtres ; leur réunion ouvre le plein cadre, leur scission referme sur le logo.",
    "logline": "Deux bulles jointes s'ouvrent sur deux regards de la vidéo. La caméra plonge vers leur cou : les bulles "
               "se rejoignent, les deux regards s'alignent, et la jonction devient le plein cadre.",
}


# =================================================================== outils géométriques
def circle_cw(cx, r):
    """Cercle sur l'axe, tracé dans le sens horaire (même sens que bridge_d : union sans trou)."""
    return f"M{f(cx - r)} {AXIS}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_cw(cx, rx, ry):
    return f"M{f(cx - rx)} {AXIS}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z"


def hull_cw(c1, c2):
    """Enveloppe convexe de deux cercles (x, r), x1 < x2 : col plein, arcs corrects même si r1 != r2."""
    (x1, r1), (x2, r2) = c1, c2
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, AXIS - r1 * ny), (x2 + r2 * nx, AXIS - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, AXIS + r2 * ny), (x1 + r1 * nx, AXIS + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def link(c1, c2, h):
    """Col de la charte entre deux cercles (x, r) : gère le chevauchement (cacahuète) et l'inclusion."""
    (x1, r1), (x2, r2) = sorted([c1, c2])
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        x, r = (x1, r1) if r1 >= r2 else (x2, r2)
        return circle_cw(x, r)
    rmin = min(r1, r2)
    if d < r1 + r2:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        ov = clamp01((r1 + r2 - d) / max(rmin, 1))
        h = max(h, yi + (rmin - yi) * 0.3 * ov + 0.5)
    h = min(h, 0.97 * rmin)
    if _neck_circle((x1, AXIS, r1), (x2, AXIS, r2), h) is None:
        return hull_cw((x1, r1), (x2, r2))
    return bridge_d((x1, AXIS, r1), (x2, AXIS, r2), h)


def pair_d(xg, xd, r, sx, h, rd=None):
    """Paire de bulles jointes (h = None : séparées), étirées de sx (volume conservé).
    r : rayon de la bulle gauche ; rd : rayon de la droite (par défaut égal)."""
    rd = r if rd is None else rd
    k = min(sx, 1 / sx)
    if h == "charte":                                                    # col calculé par le modèle de la charte
        h = charte_h(xg, r, xd, rd)
        h = None if not h or h < 0.5 else h
    parts = []
    if h is not None and r > 1 and rd > 1:
        parts.append(link((xg, r * k), (xd, rd * k), h))
    for x, rr in ((xg, r), (xd, rd)):
        if abs(sx - 1) > 1e-3:
            parts.append(ellipse_cw(x, rr * sx, rr / sx))
        elif h is None:
            parts.append(circle_cw(x, rr))
    return " ".join(parts)


def bubble_d(x, r, sx):
    return ellipse_cw(x, r * sx, r / sx) if abs(sx - 1) > 1e-3 else circle_cw(x, r)


# =================================================================== plaques vertes et fenêtres
HATCH = " ".join(f"M{i * 90 - 1200} -1200L{i * 90 + 2400} 2280" for i in range(-40, 75))


def plate(uid, cx=CX, zoom=1.0):
    """Même plaque que blocks.video, recadrée horizontalement (cx) : identique à blocks.video quand
    cx = 960 et zoom >= 1. Pas de rotation : la vidéo ne glisse que le long de l'axe."""
    z = max(zoom, 0.05)
    return (f'<g id="{uid}-plaque"><rect x="-2400" y="-1600" width="6720" height="4280" fill="{GREEN}"/>'
            f'<g transform="translate({f(cx)} {AXIS}) scale({f(z)}) translate({f(-CX)} {-AXIS})">'
            f'<path d="{HATCH}" stroke="{GREEN_D}" stroke-width="16" fill="none"/>'
            f'<rect x="{W * .1}" y="{H * .1}" width="{W * .8}" height="{H * .8}" fill="none" stroke="{GREEN_L}" '
            f'stroke-width="6" stroke-dasharray="30 20"/>'
            f'<path d="M{W / 2 - 60} {H / 2}H{W / 2 + 60}M{W / 2} {H / 2 - 60}V{H / 2 + 60}" stroke="{GREEN_L}" stroke-width="8"/>'
            f'<circle cx="{W / 2}" cy="{H / 2}" r="150" fill="none" stroke="{GREEN_L}" stroke-width="6"/>'
            f'<text x="{W / 2}" y="{H / 2 + 250}" font-family="Inter, Arial, sans-serif" font-size="64" '
            f'font-weight="700" fill="{GREEN_L}" text-anchor="middle" letter-spacing="12">VIDÉO</text></g></g>')


def window(uid, clip_d, content, iris=None, band=None):
    """Fenêtre : contenu découpé par la bulle, par le disque iris (x, r) qui ouvre ou ferme la vidéo,
    et par une bande verticale (x0, x1) : chaque bulle garde sa moitié, couture au milieu du cou."""
    s = f'<clipPath id="{uid}-c"><path d="{clip_d}"/></clipPath>'
    inner = content
    if iris is not None:
        s += f'<clipPath id="{uid}-i"><circle cx="{f(iris[0])}" cy="{AXIS}" r="{f(max(iris[1], 0.1))}"/></clipPath>'
        inner = f'<g clip-path="url(#{uid}-i)">{inner}</g>'
    if band is not None:
        s += (f'<clipPath id="{uid}-b"><rect x="{f(band[0])}" y="-20" width="{f(band[1] - band[0])}" '
              f'height="{H + 40}"/></clipPath>')
        inner = f'<g clip-path="url(#{uid}-b)">{inner}</g>'
    return {"k": "raw", "svg": s + f'<g id="{uid}" clip-path="url(#{uid}-c)">{inner}</g>'}


# =================================================================== outils de mouvement
def pulse(t, t0, dur):
    """Bosse douce 0 -> 1 -> 0 entre t0 et t0 + dur (en s)."""
    u = (t - t0) / dur
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def speed(fn, t, dt=0.02):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def covered(e, r):
    """La paire (centres à 960 ± e, rayon r) couvre-t-elle tout le cadre ?"""
    pts = [(0, 0), (0, H), (W, 0), (W, H), (CX, 0), (CX, H)]
    return all(min(math.hypot(x - (CX - e), y - AXIS), math.hypot(x - (CX + e), y - AXIS)) <= r - 2 for x, y in pts)


SPLIT = bezier(0.1, 0.85, 0.3, 1.0)          # départ explosif de la scission (45 % du trajet en 1 image)
R0 = 230                                     # rayon des jumelles
DP = 3.27                                    # pose signature (3.1, 3.3) : écart des centres = 3,27 r
E0 = DP * R0 / 2                             # demi-écart de la pose signature
KF = 0.91                                    # rayon du congé du col = 0,91 r moyen (mesuré sur la charte)


def charte_h(x1, r1, x2, r2):
    """Demi-épaisseur du col, modèle mesuré de la charte : congé circulaire de rayon constant
    (0,91 r moyen) tangent aux deux bulles. Donne 100 % -> 75 % -> 7 % du diamètre pour d = 0 -> 1,88 r -> 3,27 r,
    et rompt à 3,36 r. None : un seul cercle ; 0 : col rompu."""
    d = abs(x2 - x1)
    if d < 1:
        return None
    rf = KF * (r1 + r2) / 2
    a, b = r1 + rf, r2 + rf
    xn = (a * a - b * b + d * d) / (2 * d)
    y2 = a * a - xn * xn
    return max(0.0, math.sqrt(y2) - rf) if y2 > 0 else 0.0


# =================================================================== INTRO (3,2 s)
R_in = Track((0, 70), (F(6), R0, "out_back_fort"),                      # surgit dès l'image 0, dépassement
             (F(24), R0), (F(45), 290, "inout_cubic"),                   # approche : la paire grossit
             (F(49), 280, "inout_cubic"),                                # inspire
             (F(61), 1500, "plongee"))                                   # plongée
D_in = Track((F(10), 0), (F(19), DP * 1.022, SPLIT), (F(24), DP, "inout_cubic"),   # scission (écart / r), dépasse 2 %
             (F(45), DP), (F(49), 3.34, "inout_cubic"),                  # tension : le col file vers la rupture
             (F(59), 0, "in_cubic"))                                     # réunion en claquement


E_slam = Track((F(49), 3.34 * 140), (F(58), 0, "in_cubic"))              # réunion en claquement (écart à l'écran)


def E_in(t):
    return D_in(t) * R_in(t) / 2 if t < F(49) else E_slam(t)
sq_in = Track((F(6), 1.0), (F(8), 0.86, "out_cubic"), (F(10), 0.86), (F(11), 1.0, "out_cubic"))   # anticipation X 0,86
# plaques : deux regards qui tournent et zooment en sens contraires, puis s'alignent
zfull = Track((F(49), 0.56), (F(59), 1.0, "in_cubic"), (F(80), 1.16, "out_cubic"))
zG_own = Track((F(14), 0.34), (F(49), 0.58, "out_cubic"))
zD_own = Track((F(17), 0.84), (F(49), 0.54, "out_cubic"))
offG_own = Track((F(14), -190.0), (F(49), -40.0, "out_cubic"))         # cadrages décalés : chacun regarde
offD_own = Track((F(17), 210.0), (F(49), 46.0, "out_cubic"))           # un côté du même monde
# deux regards : échange de tailles 3.3-02 (r1 + r2 constant), gauche puis droite, avec dépassement
EX = Track((F(22), 0.0), (F(27), 0.30, "out_back"), (F(30), 0.27, "inout_cubic"),
           (F(36), -0.30, "out_back"), (F(39), -0.27, "inout_cubic"), (F(46), 0.0, "inout_cubic"))
focus = Track((F(49), 0.0), (F(56), 1.0, "inout_cubic"))                 # mise au point : les regards s'alignent
openG = Track((F(14), 0.0), (F(21), 1.0, "out_cubic"))
openD = Track((F(17), 0.0), (F(24), 1.0, "out_cubic"))                  # 3 images de retard sur G


def intro(t):
    R = R_in(t)
    # deux regards (3.3-02) : la gauche gonfle, la droite cède 1 image après, puis la bascule
    ag, ad = EX(t), -EX(t - F(1))
    if t < F(49):
        R *= breathe(t, 0.012, 1.3, 0.2)                                  # la pose respire
        E = D_in(t) * R * (2 + ag + ad) / 4                               # écart = 3,27 x rayon moyen réel
    else:
        E = E_in(t)
    k = focus(t)                                                          # convergence des deux regards
    z = zfull(t) + 0.3 * max(0.0, t - F(59))
    if t >= F(59) or (k >= 0.999 and covered(E, R)):
        return [video(z, ghost=False)]                                    # plein cadre : une seule plaque
    L = [{"k": "bg", "v": "gradient"}]
    if R < 0.5:
        return L
    # étirement : anticipation (X 0,86) puis traînée dans le sens de la scission, écrasement à l'arrivée
    v = abs(speed(E_in, t)) if F(10) <= t <= F(25) else 0.0
    sx = sq_in(t) * min(1.15, 1 + v / 9000) * squash(t, F(19), F(9), -0.1) * squash(t, F(6), F(6), 0.08)
    h = "charte" if t >= F(10) else None
    xg, xd = CX - E, CX + E
    if E < 1:                                                              # un seul point
        L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": bubble_d(CX, R, sx), "pts": [(CX, AXIS)]})
        return L
    rg, rd = R * (1 + ag), R * (1 + ad)
    L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": pair_d(xg, xd, rg, sx, h, rd),
              "pts": [(xg, AXIS), (xd, AXIS)]})
    if t >= F(14):
        zg = lerp(zG_own(t) * (1 + 0.5 * ag), zfull(t), k)                # chaque vidéo zoome avec sa bulle
        zd = lerp(zD_own(t) * (1 + 0.5 * ad), zfull(t), k)
        uG, uD = openG(t), openD(t)
        irisG = None if uG >= 1 else (xg + rg - uG * rg, rg * 1.03 * uG)    # la vidéo coule depuis le cou
        irisD = None if uD >= 1 else (xd - rd + uD * rd, rd * 1.03 * uD)
        # à partir de la tension, toute la paire est fenêtre : la jonction s'ouvre sur la vidéo
        cg = pair_d(xg, xd, rg, sx, "charte", rd) if t >= F(49) else bubble_d(xg, rg, sx)
        cd = pair_d(xg, xd, rg, sx, "charte", rd) if t >= F(49) else bubble_d(xd, rd, sx)
        if uG > 0:
            L.append(window("fen-g", cg, plate("pg", xg + offG_own(t) * (1 - k), zg), irisG, (-50, CX)))
        if uD > 0:
            L.append(window("fen-d", cd, plate("pd", xd + offD_own(t) * (1 - k), zd), irisD, (CX, W + 50)))
    return L


def a_eclosion(t):
    return "".join(arrow(CX + dx * 190, AXIS + dy * 150, CX + dx * 300, AXIS + dy * 240) for dx in (-1, 1) for dy in (-1, 1))


def a_scission(t):
    return arrow(CX - 120, AXIS - 300, CX - 420, AXIS - 300) + arrow(CX + 120, AXIS - 300, CX + 420, AXIS - 300)


def radial(cx, r, out=True, side=0):
    """Deux flèches diagonales autour d'une bulle (côté extérieur si side = -1 ou 1) : gonfle ou dégonfle."""
    dxs = (side,) if side else (-1, 1)
    o = []
    for dx in dxs:
        for dy in (-1, 1):
            a, b = (0.78, 1.12) if out else (1.18, 0.86)
            o.append(arrow(cx + dx * r * a * 0.7, AXIS + dy * r * a * 0.7, cx + dx * r * b * 0.7, AXIS + dy * r * b * 0.7))
    return "".join(o)


def a_regards(t):
    return radial(585, 300, True, -1) + radial(1335, 165, False, 1)


def a_bascule(t):
    return radial(500, 210, False, -1) + radial(1420, 360, True, 1)


def a_tension(t):
    return arrow(CX - 200, AXIS - 380, CX - 330, AXIS - 380) + arrow(CX + 200, AXIS - 380, CX + 330, AXIS - 380)


def a_plongee(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 300, CX + dx * 860, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1)) \
        + arrow(CX - 520, AXIS, CX - 120, AXIS) + arrow(CX + 520, AXIS, CX + 120, AXIS)


INTRO = Anim("INTRO", 3.2, intro, [
    Beat(F(8), "Dès l'image 0, un point orange surgit au centre (×3 en 6 images, +16 %), puis s'écrase à 86 % en largeur : il prend son élan.",
         "out_back_fort", ann=a_eclosion, onion=3, onion_dt=F(2)),
    Beat(F(12), "Scission explosive (3.3-01) : 45 % du trajet en 1 image, bulles étirées à 115 %. Le col suit la charte et s'affine à 7 % du diamètre.",
         "emphase", ann=a_scission, onion=2, onion_dt=F(1)),
    Beat(F(18), "La vidéo coule depuis le col dans chaque bulle, la droite 3 images après la gauche. La paire dépasse de 2 % puis revient.",
         "out_cubic", onion=0),
    Beat(F(27), "Regard gauche (3.3-02) : la bulle gauche gonfle de 30 %, la droite cède autant 1 image après. Chaque vidéo zoome avec sa bulle.",
         "out_back", ann=a_regards, onion=2, onion_dt=F(2)),
    Beat(F(38), "Bascule en 6 images : la droite prend le dessus (+36 % au pic). En même temps la caméra s'approche, la paire grossit de 26 %.",
         "out_back", ann=a_bascule, onion=2, onion_dt=F(2)),
    Beat(F(48), "Tension : les bulles s'écartent jusqu'au bord de la rupture (3,34 r), le col n'est plus qu'un fil. Elles inspirent (−3 %).",
         "inout_cubic", ann=a_tension, onion=2, onion_dt=F(2)),
    Beat(F(52), "Réunion en claquement pendant la plongée : la paire fonce vers la caméra, le col devient fenêtre et ses creux sortent du cadre.",
         "plongee", ann=a_plongee, onion=2, onion_dt=F(1)),
    Beat(F(55), "Mise au point : plein cadre, les deux vidéos glissent le long de l'axe et se superposent en 2 images. La plaque pousse toujours.",
         "inout_cubic", onion=0),
])


# =================================================================== OUTRO (3,6 s)
T0_LOGO = F(41)
DOT_R = LG["dot_r"]
XG, XD = LG["dot_g"][0], LG["dot_d"][0]
E_DOT = XD - CX                                                          # 279 px : demi-écart des points du logo

z_out = Track((0, 1.12), (F(1), 1.15, "out_cubic"), (F(12), 0.58, "out_cubic"), (F(28), 0.5, "linear"))
R_out = Track((F(1), 1150), (F(12), 300, "out_cubic"), (F(22), R0, "inout_cubic"),
              (F(29), R0), (F(35), 205, "inout_cubic"),                  # inspire avant l'éclatement
              (F(37), 170, "in_cubic"),                                  # s'étire jusqu'à la rupture
              (F(45), DOT_R * 1.5, "out_cubic"), (F(50), DOT_R, "inout_cubic"))
D_out = Track((F(1), 0), (F(12), 2.3, "out_cubic"), (F(18), DP * 1.022, "out_cubic"), (F(22), DP, "inout_cubic"),
              (F(29), DP), (F(35), 2.0, "inout_cubic"),                  # la paire se resserre (cacahuète)
              (F(37), 3.42, "in_cubic"))                                 # le col file et casse (3,36 r)
SNAP = F(37)
E_post = Track((SNAP, 3.42 * 170 / 2), (F(41), E_DOT * 1.14, "out_expo"), (F(47), E_DOT, "out_back"))   # recul, retour


def E_out(t):
    return D_out(t) * R_out(t) / 2 if t < SNAP else E_post(t)

closeG = Track((F(18), 0.0), (F(26), 1.0, "in_cubic"))
closeD = Track((F(21), 0.0), (F(29), 1.0, "in_cubic"))                   # 3 images de retard
kdiv = Track((F(1), 0.0), (F(14), 1.0, "out_cubic"))                      # les deux regards se séparent
zG_o = Track((F(1), 1.15), (F(14), 0.52, "out_cubic"), (F(29), 0.6, "linear"))
zD_o = Track((F(1), 1.15), (F(14), 0.66, "out_cubic"), (F(29), 0.56, "linear"))
# gouttelette du col : elle reste au centre, blanchit, puis devient le point de départ du mot
drop_r = Track((SNAP, 0), (SNAP + F(1), 34, "out_cubic"), (T0_LOGO, 24, "inout_cubic"), (T0_LOGO + F(2), 0, "in_cubic"))


def outro(t):
    if t < F(1):                                   # 1 image de poussée (anticipation), puis pincement
        return [video(z_out(t), ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    R = R_out(t)
    if t < SNAP:
        R *= breathe(t, 0.01, 1.2)
    E = D_out(t) * R / 2 if t < SNAP else E_out(t)                       # écart = 3,27 x rayon réel
    k = kdiv(t)
    xg, xd = CX - E, CX + E
    sx = squash(t, F(12), F(10), -0.08) if t < SNAP else squash(t, SNAP, F(10), -0.14)
    if t < SNAP:
        L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": pair_d(xg, xd, R, sx, "charte"),
                  "pts": [(xg, AXIS), (xd, AXIS)]})
        uG, uD = closeG(t), closeD(t)
        if uG < 1:
            L.append(window("fen-g", bubble_d(xg, R, sx), plate("pg", xg - 150 * k, zG_o(t)),
                            (xg, R * 1.03 * (1 - uG)) if uG > 0 else None, (-50, CX)))
        if uD < 1:
            L.append(window("fen-d", bubble_d(xd, R, sx), plate("pd", xd + 170 * k, zD_o(t)),
                            (xd, R * 1.03 * (1 - uD)) if uD > 0 else None, (CX, W + 50)))
        return L
    # rupture : le col casse, les deux moitiés reculent et deviennent les points du logo
    col = mix_hex(ORANGE, WHITE, prog(t, SNAP, F(47)))
    bre = prog(t, F(52), F(58))
    rg = lerp(R, DOT_R * breathe(t, 0.2, 1.1), bre)
    rd = lerp(R, DOT_R * breathe(t, 0.2, 1.1, 0.25), bre)
    u = prog(t, SNAP, SNAP + F(5), "out_cubic")
    parts = [bubble_d(xg, rg, sx), bubble_d(xd, rd, sx)]
    rdrop = drop_r(t)
    if rdrop > 0.5:                                                       # gouttelette : la graine du mot
        parts.append(circle_cw(CX, rdrop))
    if u < 1:                                                             # restes du col qui se rétractent
        nub, kc = 0.32 * R * (1 - u), min(sx, 1 / sx)                    # accroché au cercle intérieur de l'ellipse
        parts += [link((xg, rg * kc), (xg + rg * sx + nub, 0.15 * R * (1 - u) + 0.5), 0.06 * R * (1 - u) + 0.5),
                  link((xd - rd * sx - nub, 0.15 * R * (1 - u) + 0.5), (xd, rd * kc), 0.06 * R * (1 - u) + 0.5)]
    dots = {"k": "fill", "id": "points-logo", "fill": col, "d": " ".join(parts), "pts": [(xg, AXIS), (xd, AXIS)]}
    card = endcard(t, T0_LOGO, dots=False, word_mode="centre", extra=[dots])
    # poussée supplémentaire (+5 %/s) sur le logo seul : l'endossement reste calé en bas
    logo = [x for x in card if x["k"] != "raw"]
    endo = [x for x in card if x["k"] == "raw"]
    return L + [{"k": "group", "s": 1 + 0.05 * max(0.0, t - T0_LOGO), "layers": logo}] + endo


def a_pincement(t):
    return arrow(CX - 90, AXIS, CX - 330, AXIS) + arrow(CX + 90, AXIS, CX + 330, AXIS) \
        + "".join(arrow(CX + dx * 860, AXIS + dy * 470, CX + dx * 600, AXIS + dy * 330) for dx in (-1, 1) for dy in (-1, 1))


def a_scission_o(t):
    return arrow(CX - 120, AXIS - 300, CX - 360, AXIS - 300) + arrow(CX + 120, AXIS - 300, CX + 360, AXIS - 300)


def a_fermeture(t):
    return "".join(arrow(CX + sx * E0 + dx * 330, AXIS + dy * 330, CX + sx * E0 + dx * 190, AXIS + dy * 190)
                   for sx in (-1, 1) for dx in (-1, 1) for dy in (-1, 1) if dx == sx)


def a_resserre(t):
    return arrow(CX - 560, AXIS - 300, CX - 360, AXIS - 300) + arrow(CX + 560, AXIS - 300, CX + 360, AXIS - 300)


def a_eclate(t):
    return arrow(CX - 90, AXIS - 240, CX - 260, AXIS - 240) + arrow(CX + 90, AXIS - 240, CX + 260, AXIS - 240)


def a_graine(t):
    return arrow(CX, AXIS - 200, CX, AXIS - 70) + arrow(CX - 60, AXIS + 120, CX - 220, AXIS + 120) \
        + arrow(CX + 60, AXIS + 120, CX + 220, AXIS + 120)


OUTRO = Anim("OUTRO", 3.6, outro, [
    Beat(F(5), "Le cadre se pince dès l'image 1 : deux creux orange entrent par le haut et le bas au centre et dessinent deux bulles jointes.",
         "out_cubic", ann=a_pincement, onion=2, onion_dt=F(2)),
    Beat(F(16), "Scission (3.3-01) : les bulles s'écartent jusqu'à 3,27 r avec 2 % de dépassement ; les deux vidéos glissent de 160 px vers l'extérieur.",
         "out_cubic", ann=a_scission_o, onion=2, onion_dt=F(2)),
    Beat(F(23), "La vidéo se ferme en orange, de l'extérieur vers le centre de chaque bulle, la droite 3 images après la gauche.",
         "in_cubic", ann=a_fermeture, onion=0),
    Beat(F(34), "Inspiration : la paire se resserre en cacahuète (écart 3,27 r → 2 r en 6 images) et le col s'épaissit.",
         "inout_cubic", ann=a_resserre, onion=2, onion_dt=F(2)),
    Beat(F(37), "Rupture nette : en 2 images le col file jusqu'à 3,4 r et casse. Les moitiés reculent, écrasées à 86 % ; une gouttelette reste au centre.",
         "in_cubic", ann=a_eclate, onion=2, onion_dt=F(1)),
    Beat(F(40), "Trois points : les moitiés rétrécissent 16 fois en blanchissant ; au centre, la gouttelette blanchit aussi.",
         "out_expo", ann=a_graine, onion=2, onion_dt=F(1)),
    Beat(F(44), "La gouttelette devient le mot : « sfeer » s'ouvre depuis elle (14 images) et les points se posent après 14 % de dépassement.",
         "emphase", onion=0),
    Beat(F(84), "Tenue vivante : les points respirent (±20 %), le logo pousse de 12,5 %/s ; « Powered by RIYADH AIR » reste calé en bas.",
         "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "« A new world of connections » au pied de la lettre : on n'entre pas par un trou, on entre par la jonction de deux bulles.",
        "Deux bulles, deux regards qui se répondent, puis un seul plan : la réunion fonctionne comme une mise au point.",
        "L'outro rejoue la scission : la gouttelette du col devient le mot, les deux moitiés ses points. Marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Forme héros 3.1 : col calculé comme la charte (congé de 0,91 r, pose à 3,27 r, rupture à 3,36 r) ; 3.3-01 et 3.3-02 tels quels.",
        "Fenêtres = bulles pleines au centre, jamais l'espace entre deux demi-bulles de bord (différence nette avec la piste 5).",
        "Écart à valider : couture verticale entre les deux vidéos, 2 images en plein cadre (mise au point) et 3 au début de l'outro.",
    ]),
    ("Mouvement", [
        "Pop dès l'image 0, élan X 0,86, scission explosive, échange de tailles ±30 %, tension au bord de la rupture, claquement.",
        "Décalages : la droite suit à 1 image dans l'échange, à 3 images à l'ouverture et à la fermeture de la vidéo.",
        "Plongée en courbe plongée, vidéos en contre-zoom 2 fois plus lent ; plein cadre et carton poussent sans arrêt.",
    ]),
]
