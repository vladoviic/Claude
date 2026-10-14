"""Concept original O4 : « La Jonction, on entre par le lien ».

Deux bulles égales, jointes par le col de la charte (forme héros 3.1), s'ouvrent chacune sur
la vidéo : deux plaques, deux regards (inclinés et zoomés en sens contraires). La caméra plonge
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


def plate(uid, cx=CX, zoom=1.0, rot=0.0):
    """Même plaque que blocks.video, centrée sur sa bulle et inclinée (rot, en degrés) :
    identique à blocks.video quand cx = 960, rot = 0 et zoom >= 1."""
    z = max(zoom, 0.05)
    return (f'<g id="{uid}-plaque"><rect x="-2400" y="-1600" width="6720" height="4280" fill="{GREEN}"/>'
            f'<g transform="translate({f(cx)} {AXIS}) rotate({f(rot)}) scale({f(z)}) translate({f(-CX)} {-AXIS})">'
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
E0 = 3.27 * R0 / 2                           # demi-écart de la pose signature 3.3-01 (d = 3,27 r)


# =================================================================== INTRO (3,6 s)
R_in = Track((0, 0), (F(7), R0, "out_back_fort"),                       # éclosion avec dépassement
             (F(24), R0), (F(36), R0 * 1.06, "linear"),                  # visée : poussée lente
             (F(46), 292, "inout_cubic"),                                # approche : la paire grossit
             (F(49), 280, "inout_cubic"),                                # inspire
             (F(61), 1500, "plongee"))                                   # plongée
E_in = Track((F(10), 0), (F(19), E0 * 1.022, SPLIT), (F(24), E0, "inout_cubic"),   # scission, dépasse 2 %, revient
             (F(36), E0 * 1.06, "linear"), (F(46), 318, "inout_cubic"),  # les bulles se rapprochent
             (F(49), 336, "inout_cubic"),                                # inspire : elles s'écartent (tension)
             (F(59), 0, "in_cubic"))                                     # réunion en claquement
H_in = Track((F(10), 160), (F(19), 16, "out_cubic"), (F(34), 17), (F(46), 60, "inout_cubic"),
             (F(49), 24, "inout_cubic"), (F(56), 120, "in_cubic"))
sq_in = Track((F(6), 1.0), (F(8), 0.86, "out_cubic"), (F(10), 0.86), (F(11), 1.0, "out_cubic"))   # anticipation X 0,86
# plaques : deux regards qui tournent et zooment en sens contraires, puis s'alignent
zfull = Track((F(49), 0.56), (F(59), 1.0, "in_cubic"), (F(80), 1.16, "out_cubic"))
zG_own = Track((F(14), 0.34), (F(49), 0.58, "out_cubic"))
zD_own = Track((F(17), 0.84), (F(49), 0.54, "out_cubic"))
rotG_own = Track((F(14), -24.0), (F(49), -5.0, "out_cubic"))
rotD_own = Track((F(17), 22.0), (F(49), 4.0, "out_cubic"))
swing = Track((F(22), 0.0), (F(27), 1.0, "inout_cubic"), (F(38), 1.0), (F(46), 0.0, "inout_cubic"))
openG = Track((F(14), 0.0), (F(21), 1.0, "out_cubic"))
openD = Track((F(17), 0.0), (F(24), 1.0, "out_cubic"))                  # 3 images de retard sur G


def intro(t):
    E, R = E_in(t), R_in(t)
    if t < F(49):
        E *= breathe(t, 0.006, F(8))                                      # la pose respire (±0,6 %)
        R *= breathe(t, 0.012, 1.3, 0.2)
    k = clamp01(1 - E / 336) if t >= F(49) else 0.0                       # convergence des deux regards
    z = zfull(t) + 0.3 * max(0.0, t - F(59))
    if t >= F(59) or (k >= 0.999 and covered(E, R)):
        return [video(z, ghost=False)]                                    # plein cadre : une seule plaque
    L = [{"k": "bg", "v": "gradient"}]
    if R < 0.5:
        return L
    # étirement : anticipation (X 0,86) puis traînée dans le sens de la scission, écrasement à l'arrivée
    v = abs(speed(E_in, t)) if F(10) <= t <= F(25) else 0.0
    sx = sq_in(t) * min(1.16, 1 + v / 9000) * squash(t, F(19), F(9), -0.1) * squash(t, F(6), F(6), 0.08)
    h = H_in(t) if t >= F(10) else None
    xg, xd = CX - E, CX + E
    if E < 1:                                                              # un seul point
        L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": bubble_d(CX, R, sx), "pts": [(CX, AXIS)]})
        return L
    # les deux regards respirent en alternance (±7 %, 3.3-02 en douceur) : la pose n'est jamais figée
    a = 0.07 * swing(t) * math.sin(2 * math.pi * (t - F(22)) / 0.84)
    rg, rd = R * (1 + a), R * (1 - a)
    L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": pair_d(xg, xd, rg, sx, h, rd),
              "pts": [(xg, AXIS), (xd, AXIS)]})
    if t >= F(14):
        zg = lerp(zG_own(t), zfull(t), k)
        zd = lerp(zD_own(t), zfull(t), k)
        uG, uD = openG(t), openD(t)
        irisG = None if uG >= 1 else (xg + rg - uG * rg, rg * 1.03 * uG)    # la vidéo coule depuis le cou
        irisD = None if uD >= 1 else (xd - rd + uD * rd, rd * 1.03 * uD)
        if uG > 0:
            L.append(window("fen-g", bubble_d(xg, rg, sx), plate("pg", xg, zg, rotG_own(t) * (1 - k)), irisG, (-50, CX)))
        if uD > 0:
            L.append(window("fen-d", bubble_d(xd, rd, sx), plate("pd", xd, zd, rotD_own(t) * (1 - k)), irisD, (CX, W + 50)))
    return L


def a_eclosion(t):
    return "".join(arrow(CX + dx * 190, AXIS + dy * 150, CX + dx * 300, AXIS + dy * 240) for dx in (-1, 1) for dy in (-1, 1))


def a_scission(t):
    return arrow(CX - 120, AXIS - 300, CX - 420, AXIS - 300) + arrow(CX + 120, AXIS - 300, CX + 420, AXIS - 300)


def a_regards(t):
    return curved_arrow(CX - 470, AXIS - 300, CX - 370, AXIS - 330, CX - 270, AXIS - 280) \
        + curved_arrow(CX + 470, AXIS - 300, CX + 370, AXIS - 330, CX + 270, AXIS - 280)


def a_approche(t):
    return arrow(CX - 620, AXIS - 360, CX - 420, AXIS - 360) + arrow(CX + 620, AXIS - 360, CX + 420, AXIS - 360)


def a_tension(t):
    return arrow(CX - 200, AXIS - 380, CX - 330, AXIS - 380) + arrow(CX + 200, AXIS - 380, CX + 330, AXIS - 380)


def a_plongee(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 300, CX + dx * 860, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1)) \
        + arrow(CX - 520, AXIS, CX - 120, AXIS) + arrow(CX + 520, AXIS, CX + 120, AXIS)


INTRO = Anim("INTRO", 3.2, intro, [
    Beat(F(5), "Un point orange éclot au centre en 7 images, avec 16 % de dépassement, puis s'écrase à 86 % en largeur : il prend son élan.",
         "out_back_fort", ann=a_eclosion, onion=2, onion_dt=F(2)),
    Beat(F(13), "Scission explosive (3.3-01) : 45 % du trajet en une image, chaque bulle étirée à 116 %. Le col s'affine jusqu'à 7 % du diamètre.",
         "emphase", ann=a_scission, onion=3, onion_dt=F(1)),
    Beat(F(19), "La vidéo coule depuis le col dans chaque bulle, la droite 3 images après la gauche. La paire dépasse de 2 % puis revient.",
         "out_cubic", onion=2, onion_dt=F(2)),
    Beat(F(31), "Deux regards : les plaques tournent en sens contraires (−24° → −5°, +22° → +4°), les bulles respirent en alternance (±7 %).",
         "out_cubic", ann=a_regards, onion=0),
    Beat(F(44), "Approche : la paire grossit de 27 % et les bulles se rapprochent. Le col s'élargit comme une porte qui s'entrouvre.",
         "inout_cubic", ann=a_approche, onion=2, onion_dt=F(3)),
    Beat(F(49), "Tension : les bulles s'écartent de 18 px et le col se pince sur 3 images, juste avant de céder. C'est l'inspiration.",
         "inout_cubic", ann=a_tension, onion=2, onion_dt=F(2)),
    Beat(F(54), "Plongée et réunion : la paire fonce vers la caméra et se rejoint en claquant. Les creux du col sortent par le haut et le bas.",
         "plongee", ann=a_plongee, onion=2, onion_dt=F(2)),
    Beat(F(57), "Mise au point : plein cadre, les deux regards glissent et tournent jusqu'à se superposer. La couture disparaît en 2 images.",
         "in_cubic", onion=0),
])


# =================================================================== OUTRO (4,0 s)
T0_LOGO = F(43)
DOT_R = LG["dot_r"]
XG, XD = LG["dot_g"][0], LG["dot_d"][0]
E_DOT = XD - CX                                                          # 279 px : demi-écart des points du logo

z_out = Track((0, 1.10), (F(3), 1.16, "linear"), (F(14), 0.58, "out_cubic"), (F(30), 0.5, "linear"))
R_out = Track((F(3), 1500), (F(14), 300, "out_cubic"), (F(24), R0, "inout_cubic"),
              (F(31), R0), (F(37), 214, "inout_cubic"),                  # inspire avant l'éclatement
              (F(39), 214), (F(47), DOT_R * 1.5, "out_cubic"), (F(52), DOT_R, "inout_cubic"))
E_out = Track((F(3), 0), (F(14), 330, "out_cubic"), (F(20), E0 * 1.022, "out_cubic"), (F(24), E0, "inout_cubic"),
              (F(31), E0), (F(37), 236, "inout_cubic"),                  # la paire se resserre (cacahuète)
              (F(39), 262, "in_cubic"),                                  # le col s'étire et se pince
              (F(45), E_DOT * 1.14, "out_expo"), (F(51), E_DOT, "out_back"))   # éclatement, recul, retour
H_out = Track((F(3), 140), (F(14), 40, "out_cubic"), (F(22), 16, "out_cubic"), (F(31), 17),
              (F(37), 90, "inout_cubic"), (F(39), 4, "in_cubic"))
SNAP = F(39)
closeG = Track((F(20), 0.0), (F(28), 1.0, "in_cubic"))
closeD = Track((F(23), 0.0), (F(31), 1.0, "in_cubic"))                   # 3 images de retard
kdiv = Track((F(3), 0.0), (F(16), 1.0, "out_cubic"))                      # les deux regards se séparent
zG_o = Track((F(3), 1.16), (F(16), 0.52, "out_cubic"), (F(31), 0.6, "linear"))
zD_o = Track((F(3), 1.16), (F(16), 0.66, "out_cubic"), (F(31), 0.56, "linear"))


def outro(t):
    if t < F(4):
        return [video(z_out(t), ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    E, R = E_out(t), R_out(t)
    k = kdiv(t)
    xg, xd = CX - E, CX + E
    sx = squash(t, F(14), F(10), -0.12) if t < SNAP else squash(t, SNAP, F(10), -0.2)
    if t < SNAP:
        R *= breathe(t, 0.01, 1.2)
        L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": pair_d(xg, xd, R, sx, H_out(t)),
                  "pts": [(xg, AXIS), (xd, AXIS)]})
        uG, uD = closeG(t), closeD(t)
        if uG < 1:
            L.append(window("fen-g", bubble_d(xg, R, sx), plate("pg", xg, zG_o(t), -12 * k),
                            (xg, R * 1.03 * (1 - uG)) if uG > 0 else None, (-50, CX)))
        if uD < 1:
            L.append(window("fen-d", bubble_d(xd, R, sx), plate("pd", xd, zD_o(t), 11 * k),
                            (xd, R * 1.03 * (1 - uD)) if uD > 0 else None, (CX, W + 50)))
        return L
    # rupture : le col casse, les deux moitiés reculent et deviennent les points du logo
    col = mix_hex(ORANGE, WHITE, prog(t, SNAP, F(47)))
    bre = prog(t, F(52), F(58))
    rg = lerp(R, DOT_R * breathe(t, 0.2, 1.1), bre)
    rd = lerp(R, DOT_R * breathe(t, 0.2, 1.1, 0.25), bre)
    u = prog(t, SNAP, SNAP + F(5), "out_cubic")
    parts = [bubble_d(xg, rg, sx), bubble_d(xd, rd, sx)]
    if u < 1:                                                             # restes du col qui se rétractent
        nub = 0.32 * R * (1 - u)
        parts += [link((xg, rg), (xg + rg + nub, 0.15 * R * (1 - u) + 0.5), 0.06 * R * (1 - u) + 0.5),
                  link((xd - rd - nub, 0.15 * R * (1 - u) + 0.5), (xd, rd), 0.06 * R * (1 - u) + 0.5)]
    dots = {"k": "fill", "id": "points-logo", "fill": col, "d": " ".join(parts), "pts": [(xg, AXIS), (xd, AXIS)]}
    card = endcard(t, T0_LOGO, dots=False, word_mode="centre", extra=[dots])
    return L + [{"k": "group", "s": 1 + 0.05 * max(0.0, t - T0_LOGO), "layers": card}]


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
    return arrow(CX - 120, AXIS - 120, CX - 230, AXIS - 120) + arrow(CX + 120, AXIS - 120, CX + 230, AXIS - 120)


OUTRO = Anim("OUTRO", 3.6, outro, [
    Beat(F(7), "Le cadre se pince : deux creux entrent par le haut et le bas au centre et dessinent deux bulles jointes, en 11 images.",
         "out_cubic", ann=a_pincement, onion=2, onion_dt=F(2)),
    Beat(F(15), "Scission (3.3-01) : les bulles s'écartent et rétrécissent. Les deux regards se séparent : chaque plaque tourne de 12° et dézoome.",
         "out_cubic", ann=a_scission_o, onion=2, onion_dt=F(2)),
    Beat(F(25), "La vidéo se ferme en orange de l'extérieur vers le centre, la droite 3 images après la gauche.",
         "in_cubic", ann=a_fermeture, onion=0),
    Beat(F(36), "Inspiration : la paire se resserre de 280 px en 6 images et le col gonfle jusqu'à 180 px d'épaisseur, en cacahuète.",
         "inout_cubic", ann=a_resserre, onion=2, onion_dt=F(3)),
    Beat(F(40), "Rupture nette : le col s'étire, se pince et casse en 2 images. Les deux moitiés reculent, écrasées à 80 % puis rebondissent.",
         "out_expo", ann=a_eclate, onion=2, onion_dt=F(1)),
    Beat(F(45), "Les bulles rétrécissent 14 fois en blanchissant et se posent sur les points du logo après 14 % de dépassement.",
         "out_back", onion=2, onion_dt=F(2)),
    Beat(F(51), "« sfeer » s'ouvre depuis le centre entre les deux points (14 images), l'arabe se révèle de droite à gauche.",
         "emphase", onion=0),
    Beat(F(84), "Tenue vivante : les points respirent (±20 %), poussée lente de 12,5 %/s ; « Powered by RIYADH AIR » est posé en bas.",
         "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "« A new world of connections » au pied de la lettre : on n'entre pas par un trou, on entre par la jonction de deux bulles.",
        "Deux bulles, deux regards, puis un seul plan : la réunion fonctionne comme la mise au point d'un télémètre.",
        "L'outro rejoue la scission et la paire devient les deux points du logo. Marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Forme héros 3.1 (deux bulles égales, col de 7 % du diamètre, écart 3,27 r), comportement 3.3-01 réparti entre intro et outro.",
        "Fenêtres = bulles pleines au centre, jamais l'espace entre deux demi-bulles de bord (différence nette avec la piste 5).",
        "Centres toujours sur y = 540. Écart à valider : 3 images de couture verticale en plein cadre pendant la mise au point.",
    ]),
    ("Mouvement", [
        "Éclosion avec dépassement, anticipation X 0,86, scission explosive, rebond ; tension avant la plongée.",
        "Décalage de 3 images entre gauche et droite à l'ouverture et à la fermeture ; plaques en rotations opposées.",
        "Plongée en courbe plongée, plaques en contre-zoom 2 fois plus lent ; plein cadre et carton poussent sans arrêt.",
    ]),
]
