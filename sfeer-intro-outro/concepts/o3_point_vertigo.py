"""Concept original « Le Point : du logo au vertige ».

Le point du logo (première image de 3.4-02) se divise en une grande bulle orange et une petite
bulle (3.4-01). L'orange se retire par le cou : la petite bulle s'allume en fenêtre. Elles échangent
leur taille (3.3-02) en TRAVELLING COMPENSÉ façon Vertigo, en deux temps : la fenêtre grandit ×4
pendant que l'image dedans recule (la plaque dézoome de 156 à 76 %, centrée sur la fenêtre).
L'image s'est tendue comme un élastique : au saut, elle repart en avant (fronde) pendant que la
fenêtre jaillit hors cadre et éjecte le point.
L'outro joue le vertige inversé, l'orange remord la fenêtre depuis le cou, puis la paire claque en
un point blanc qui redevient le logo.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, back_out, bezier, breathe, prog  # noqa: E402
from blocks import LG, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, arrow, bridge_d, ellipse_d, f,  # noqa: E402
                       label, waist_h)

CX = W / 2
DOT_R = LG["dot_r"]
HALF = (LG["dot_d"][0] - LG["dot_g"][0]) / 2      # demi-écart des points du logo
BACK6 = back_out(1.25)                             # dépassement ≈ 6 %
STROKE = bezier(0.3, 0.1, 0.25, 1.12)              # vertige : départ franc, arrivée encore en mouvement
CLAP = bezier(0.4, 0.1, 0.9, 0.5)                  # claquement : accélère sans départ mort
OUT_Q = bezier(0.5, 1, 0.89, 1)                    # out_quad : arrivée douce (anticipations, retours)
JUMP = bezier(0.6, 0, 0.15, 1)                     # traversée mesurée (réf. Coinbase) : plein cadre vers 40 %
HALF_DIAG = math.hypot(W / 2, AXIS)                # rayon qui couvre le cadre depuis le centre

META = {
    "id": "o3_point_vertigo",
    "num": "O3",
    "title": "Le Point, du logo au vertige",
    "principe": "Le point du logo se divise en bulle et fenêtre ; leur échange de tailles fait reculer l'image, puis la propulse.",
    "logline": "Le point du logo se divise en une bulle orange et une fenêtre. Elles échangent leur taille en travelling compensé "
               "façon Vertigo : la fenêtre avance, l'image recule comme un élastique, puis repart en avant au saut.",
}


# ================================================================= OUTILS DE FORME
def circ(cx, r, cy=AXIS):
    """Cercle tracé dans le sens horaire (même sens que bridge_d)."""
    return (f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)}Z")


def pair_d(c1, c2, h):
    """Deux bulles (x, r) sur l'axe reliées par le cou de la charte ; fusion propre si elles se chevauchent."""
    (x1, r1), (x2, r2) = c1, c2
    if r1 < 0.5 and r2 < 0.5:
        return ""
    if r2 < 0.5:
        return circ(x1, r1)
    if r1 < 0.5:
        return circ(x2, r2)
    if x2 < x1:
        (x1, r1), (x2, r2) = (x2, r2), (x1, r1)
    a, b = (x1, AXIS, r1), (x2, AXIS, r2)
    if x2 - x1 <= abs(r1 - r2):
        return circ(*((x1, r1) if r1 >= r2 else (x2, r2)))
    if h is None:
        return circ(x1, r1) + circ(x2, r2)
    if x2 - x1 < r1 + r2:
        h = max(h, waist_h(a, b, 0.2))
    return bridge_d(a, b, min(h, 0.95 * min(r1, r2)))


def crescent_d(cx, r, bx, br, sx=1.0):
    """Morsure : la partie du cercle (cx, r) que ne couvre pas le cercle (bx, br), bx <= cx (la morsure
    vient de la gauche, du cou). sx : déformation horizontale (volume conservé) autour de cx."""
    d = cx - bx
    if r < 0.5 or d + r <= br:
        return ""
    if d >= r + br:
        return ellipse_d(cx, AXIS, r * sx, r / sx)
    a = (d * d + br * br - r * r) / (2 * d)            # abscisse des intersections, depuis bx
    yi = math.sqrt(max(br * br - a * a, 0.0))
    xi = bx + a

    def m(x, y):
        return f"{f(cx + (x - cx) * sx)} {f(AXIS + (y - AXIS) / sx)}"
    big_w = 1 if xi < cx else 0                         # arc de la fenêtre, côté droit
    big_b = 1 if xi < bx else 0                         # arc de la morsure, côté droit
    return (f"M{m(xi, AXIS - yi)}A{f(r * sx)} {f(r / sx)} 0 {big_w} 1 {m(xi, AXIS + yi)}"
            f"A{f(br * sx)} {f(br / sx)} 0 {big_b} 0 {m(xi, AXIS - yi)}Z")


def vel(fn, t):
    """Vitesse en px par image."""
    return (fn(t + 0.02) - fn(t - 0.02)) / 0.04 / 25


def covers(xw, rw):
    return rw >= math.hypot(max(xw, W - xw), AXIS) + 2


def window_layers(xw, rw, sw, zoom, e=1.0, gid="fenetre"):
    """Fenêtre verte : plaque zoomée autour du CENTRE de la fenêtre (travelling compensé).
    e < 1 : l'orange mord la fenêtre depuis le cou (gauche) ; e = 0 : fenêtre éteinte."""
    if rw < 0.5 or e <= 0:
        return []
    if e >= 1 and covers(xw, rw * min(sw, 1 / sw)):
        return [video(zoom, None, ghost=False)]
    if e >= 1:
        d = ellipse_d(CX, AXIS, rw * sw, rw / sw)
    else:
        d = crescent_d(CX, rw, CX - 0.15 * rw - 2 * rw * e, 1.15 * rw, sw)
        if not d:
            return []
    return [{"k": "group", "s": 1, "dx": xw - CX, "layers": [video(zoom, d, vid=gid, ghost=False)]},
            {"k": "fill", "id": f"{gid}-repere", "fill": "none", "d": ellipse_d(xw, AXIS, rw * sw, rw / sw),
             "pts": [(xw, AXIS)], "ghost": rw < 1000}]


def pair_layers(xo, ro, so, xw, rw, sw, h, zoom, e=1.0, col=ORANGE):
    """Point + cou + fenêtre. so / sw : déformation horizontale propre à chaque bulle (étirement,
    écrasement). Le cou s'accroche aux cercles intérieurs ; les ellipses déformées les recouvrent."""
    ko, kw = min(so, 1 / so), min(sw, 1 / sw)
    L = [{"k": "fill", "id": "point-fenetre", "fill": col, "d": pair_d((xo, ro * ko), (xw, rw * kw), h),
          "pts": [(xo, AXIS)], "ghost": abs(so - 1) < 0.02}]
    if abs(so - 1) > 0.01 and xo + ro * so > -5:
        L.append({"k": "fill", "id": "point-deforme", "fill": col, "d": ellipse_d(xo, AXIS, ro * so, ro / so)})
    if abs(sw - 1) > 0.01 and rw > 0.5:
        L.append({"k": "fill", "id": "fenetre-deformee", "fill": col, "d": ellipse_d(xw, AXIS, rw * sw, rw / sw), "ghost": False})
    L += window_layers(xw, rw, sw, zoom, e)
    return L


# ================================================================= INTRO (3,2 s)
# accroche : le point blanc surgit, inspire (comprimé à l'horizontale), vire à l'orange, explose
pt_r = Track((0, 15), (F(2), 26, "out_back"), (F(4), 12, "in_cubic"))
split_s = Track((F(4), 0.82), (F(5), 1.18, "linear"), (F(8), 1.0, "out_cubic"))
# 3.4-01 : division ; tension ; vertige en deux temps ; recul ; saut (la fenêtre éjecte le point)
xW = Track((F(6), CX), (F(12), 1215, BACK6), (F(14), 1215), (F(17), 1236, OUT_Q),
           (F(31), 1056, STROKE), (F(34), 1060, OUT_Q), (F(43), CX, STROKE))
rW = Track((F(6), 0), (F(12), 110, BACK6), (F(14), 110), (F(17), 104, OUT_Q),
           (F(31), 345, STROKE), (F(34), 330, OUT_Q), (F(43), 445, STROKE),
           (F(49), 398, OUT_Q), (F(62), 3400, JUMP))
rO = Track((F(4), 12), (F(10), 300, BACK6), (F(14), 300), (F(17), 308, OUT_Q),
           (F(31), 116, STROKE), (F(34), 114, OUT_Q), (F(43), 148, STROKE),
           (F(49), 156, OUT_Q), (F(62), 280, JUMP))
gap = Track((F(4), -12), (F(10), 20, "out_cubic"), (F(14), 20), (F(17), 44, OUT_Q), (F(22), 22, "inout_cubic"),
            (F(31), 22), (F(34), 34, OUT_Q), (F(39), 25, "inout_cubic"), (F(43), 25),
            (F(49), 14, OUT_Q), (F(54), 70, "out_cubic"))
# demi-épaisseur du cou : 27,5 (55 px) ; il s'affine à chaque tension, s'épaissit au recul
neck = Track((F(10), 27.5), (F(14), 27.5), (F(17), 11, OUT_Q), (F(22), 27.5, "inout_cubic"), (F(31), 27.5),
             (F(34), 16, OUT_Q), (F(39), 25, "inout_cubic"), (F(43), 25), (F(49), 32, OUT_Q),
             (F(54), 10, "out_cubic"))
# plaque dans la fenêtre : elle recule pendant que la fenêtre avance (vertige), puis la fronde la relâche
zin = Track((F(6), 1.6), (F(17), 1.56, "linear"), (F(31), 1.0, STROKE), (F(34), 0.98, "linear"), (F(43), 0.8, STROKE),
            (F(49), 0.76, "linear"), (F(57), 1.25, "out_expo"), (F(80), 1.34, "out_cubic"))
T_JUMP = F(49)


def zoom_in(t):
    return zin(t) + 0.12 * max(0.0, t - F(57))       # la poussée ne s'arrête jamais (raccord en mouvement)


def xO(t):
    """Le point reste collé à la fenêtre : son centre se déduit du bord gauche de la fenêtre."""
    return xW(t) - rW(t) - gap(t) - rO(t)


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(4):
        # le point blanc du logo surgit (+73 %) puis inspire, comprimé à l'horizontale : il va se diviser
        r, sx = pt_r(t), 1 - 0.18 * prog(t, F(2), F(4), "in_cubic")
        L.append({"k": "fill", "id": "point", "fill": WHITE, "d": ellipse_d(CX, AXIS, r * sx, r / sx)})
        return L
    xw, rw, ro, xo = xW(t), rW(t), rO(t), xO(t)
    if t < F(10):
        so = split_s(t)                                            # éclatement vers la gauche
    else:
        so = 1 + min(0.22, abs(vel(xO, t)) / 260) if t > F(18) else 1.0   # étirement dans le sens de la vitesse
        so /= squash(t, F(10), F(6), 0.14) * squash(t, F(31), F(6), 0.08) * squash(t, F(43), F(6), 0.08)
    sw = 1 / (squash(t, F(12), F(6), 0.2) * squash(t, F(31), F(6), 0.05))
    e = prog(t, F(12), F(16), "out_cubic")                         # la fenêtre s'allume de droite à gauche
    L += pair_layers(xo, ro, so, xw, rw, sw, neck(t), zoom_in(t), e)
    return L


# ----------------------------------------------------------------- annotations
def vertigo_ann(xw, rw, out_lbl, in_lbl, inverse=False):
    out = []
    for a in (-2.4, -0.75, 0.75, 2.4):
        ca, sa = math.cos(a), math.sin(a)
        p_out = ((xw + 0.94 * rw * ca, AXIS + 0.94 * rw * sa), (xw + 1.24 * rw * ca, AXIS + 1.24 * rw * sa))
        p_in = ((xw + 0.66 * rw * ca, AXIS + 0.66 * rw * sa), (xw + 0.36 * rw * ca, AXIS + 0.36 * rw * sa))
        if inverse:
            p_out, p_in = (p_out[1], p_out[0]), (p_in[1], p_in[0])
        out.append(arrow(*p_out[0], *p_out[1], head=30))
        out.append(arrow(*p_in[0], *p_in[1], head=24, w=6, dash=True))
    out.append(label(xw, AXIS - rw * 1.24 - 26, out_lbl, 54, anchor="middle"))
    out.append(label(xw, AXIS + rw * 1.24 + 66, in_lbl, 54, anchor="middle"))
    return "".join(out)


def a_eclat(t):
    return arrow(CX - 60, 290, CX - 420, 290) + arrow(CX + 60, 290, CX + 300, 290)


def a_allumage(t):
    xw, rw = xW(t), rW(t)
    return arrow(xw + rw + 40, AXIS - rw - 50, xw - rw - 40, AXIS - rw - 50, head=26, w=6) + \
        label(xw, AXIS - rw - 90, "la fenêtre s'allume", 50, anchor="middle")


def a_tension(t):
    xo, ro, xw, rw = xO(t), rO(t), xW(t), rW(t)
    return arrow(xo + ro * 0.2, AXIS - ro - 50, xo - ro * 0.6, AXIS - ro - 50, head=26, w=6) + \
        arrow(xw - rw * 0.2, AXIS - rw - 70, xw + rw * 1.4, AXIS - rw - 70, head=26, w=6)


def a_vertigo(t):
    return vertigo_ann(xW(t), rW(t), "la fenêtre avance", "l'image recule")


def a_fronde(t):
    xw, rw = xW(t), rW(t)
    return (arrow(xw - rw * 1.02, AXIS - rw * 0.2, xw - rw * 0.86, AXIS - rw * 0.2, head=22, w=6)
            + arrow(xw + rw * 1.02, AXIS - rw * 0.2, xw + rw * 0.86, AXIS - rw * 0.2, head=22, w=6)
            + label(xw, AXIS - rw - 40, "recul de 5 % : la fronde se tend", 50, anchor="middle"))


def a_saut(t):
    return ("".join(arrow(CX + dx * 560, AXIS + dy * 300, CX + dx * 900, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1))
            + arrow(300, AXIS, 40, AXIS))


INTRO = Anim("INTRO", 3.2, intro, [
    Beat(F(5), "Accroche : le point blanc du logo surgit (+73 %), inspire 2 images, vire à l'orange et éclate à gauche, ×15 en une image (3.4-01).", "out_back", ann=a_eclat, onion=2, onion_dt=F(2)),
    Beat(F(13), "Une petite bulle naît du flanc droit, 2 images après, et s'écrase à l'arrivée (80 %). L'orange se retire par le cou : la fenêtre s'allume.", "out_cubic", ann=a_allumage, onion=1, onion_dt=F(3)),
    Beat(F(17), "Anticipation en 3 images : la paire se tend (écart 20 → 44 px), le cou s'affine de 60 %, la fenêtre recule de 5 %.", "out_cubic", ann=a_tension, onion=0),
    Beat(F(23), "Vertige, 1er temps (3.3-02) : la fenêtre passe de 104 à 345 px pendant que la plaque dézoome de 156 à 100 %. Le point fond à 116 px.", "inout_cubic", ann=a_vertigo, onion=2, onion_dt=F(4)),
    Beat(F(40), "2e temps, après une tension de 3 images : la fenêtre se recentre et dépasse à 445 px ; l'image recule encore, jusqu'à 80 %.", "emphase", ann=a_vertigo, onion=2, onion_dt=F(4)),
    Beat(F(50), "Recul : la fenêtre se rétracte de 10 % (445 → 398 px), le cou s'épaissit, l'image est à 76 %. La fronde est tendue.", "out_cubic", ann=a_fronde, onion=1, onion_dt=F(3)),
    Beat(F(53), "Saut en 13 images (0.6, 0, 0.15, 1) : la plaque bondit à 125 %, la fenêtre couvre le cadre en 5 images, le point est éjecté à gauche.", "plongee", ann=a_saut, onion=2, onion_dt=F(1)),
    Beat(F(70), "Plein cadre : la poussée continue en décélérant (125 → 134 %, puis dérive) ; on raccorde sur un plan en mouvement.", "out_cubic", onion=0),
])


# ================================================================= OUTRO (3,4 s)
SLAM = F(3)
orW = Track((0, 1500), (F(7), 440, "out_expo"), (F(23), 104, STROKE), (F(26), 110, OUT_Q),
            (F(29), 96, OUT_Q), (F(35), 0, CLAP))
oxW = Track((F(7), CX), (F(23), 1215, STROKE), (F(26), 1220, OUT_Q), (F(29), 1242, OUT_Q),
            (F(35), CX, CLAP))
orO = Track((0, 270), (F(7), 152, "out_expo"), (F(23), 306, STROKE), (F(26), 300, OUT_Q),
            (F(29), 292, OUT_Q), (F(35), 16, CLAP))
ogap = Track((0, 25), (F(23), 20), (F(26), 20), (F(29), 60, OUT_Q), (F(35), -16, CLAP))
oneck = Track((0, 25), (F(23), 27.5), (F(26), 27.5), (F(29), 8, OUT_Q), (F(35), 30, CLAP))
# la plaque recule avec la fenêtre, puis rezoome pendant que la fenêtre rétrécit (vertige inversé)
_ozoom = Track((0, 1.34), (F(7), 0.93, "out_expo"), (F(23), 1.6, STROKE), (F(35), 1.72, "linear"))
dot_r = Track((F(35), 16), (F(37), 22, "out_back"), (F(40), 13, "in_cubic"))
split_dx = Track((F(40), 0), (F(42), 16, "out_cubic"), (F(48), HALF, BACK6))
T_LOGO = F(42)


def slam(t):
    """Le point percute la fenêtre : dépassement vers la droite (30 px) puis rebond amorti."""
    u = prog(t, SLAM, SLAM + F(10))
    return 0.0 if t < SLAM else 50 * math.exp(-3 * u) * math.sin(2.5 * math.pi * u)


def oxO(t):
    return oxW(t) - orW(t) - ogap(t) - orO(t) + slam(t)


def outro_shapes(t):
    rw, xw = orW(t), oxW(t)
    if covers(xw, rw):
        return [video(_ozoom(t), None, ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(35):
        ro, xo = orO(t), oxO(t)
        so = 1 + min(0.25, abs(vel(oxO, t)) / 260) if t < SLAM + F(1) else 1.0
        so /= squash(t, SLAM + F(1), F(8), 0.16) * squash(t, F(23), F(6), 0.08)
        sw = 1 / squash(t, F(7), F(6), 0.06)
        e = 1 - prog(t, F(21), F(26), "inout_cubic")                  # l'orange avale la fenêtre depuis le cou
        L += pair_layers(xo, ro, so, xw, rw, sw, oneck(t), _ozoom(t), e)
    elif t < F(40):
        sq = 1 / squash(t, F(35), F(6), 0.3)                           # impact : écrasé à 77 %
        r = dot_r(t)
        L.append({"k": "fill", "id": "point", "fill": WHITE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
    return L


def logo_points(t):
    """3.4-02 : le point se divise, le cou casse, les points filent à leur place et respirent."""
    if t < F(40):
        return []
    dx = split_dx(t)
    r = 13 + (DOT_R - 13) * prog(t, F(40), F(43))
    if t > F(48):
        return [{"k": "fill", "id": f"logo-point-{'gd'[i]}", "fill": WHITE,
                 "d": circ(CX + s * dx, DOT_R * breathe(t, 0.2, 1.1, phase=0.25 * i))}
                for i, s in enumerate((-1, 1))]
    h = None if 2 * dx - 2 * r > 18 else max(1.0, r * 0.45 * (1 - (2 * dx - 2 * r) / 18))
    return [{"k": "fill", "id": "points-logo", "fill": WHITE, "d": pair_d((CX - dx, r), (CX + dx, r), h),
             "pts": [(CX - dx, AXIS), (CX + dx, AXIS)]}]


def outro_full(t):
    return outro_shapes(t) + endcard(t, T_LOGO, dots=False, extra=logo_points(t))


def a_retour(t):
    return ("".join(arrow(CX + dx * 900, AXIS + dy * 480, CX + dx * 600, AXIS + dy * 320) for dx in (-1, 1) for dy in (-1, 1))
            + arrow(30, AXIS + 330, 300, AXIS + 330))


def a_choc(t):
    xo, ro = oxO(t), orO(t)
    return arrow(xo - ro - 260, AXIS, xo - ro - 50, AXIS) + label(xo, AXIS - ro - 50, "+30 px, rebond", 50, anchor="middle")


def a_vertigo_inv(t):
    return vertigo_ann(oxW(t), orW(t), "la fenêtre recule", "l'image avance", inverse=True)


def a_morsure(t):
    xw, rw = oxW(t), orW(t)
    return arrow(xw - rw - 120, AXIS - rw - 60, xw + rw + 40, AXIS - rw - 60, head=26, w=6) + \
        label(xw, AXIS - rw - 100, "l'orange rentre par le cou", 50, anchor="middle")


def a_tension_o(t):
    xo, ro, xw, rw = oxO(t), orO(t), oxW(t), orW(t)
    return arrow(xo, AXIS - ro - 50, xo - ro * 0.7, AXIS - ro - 50, head=26, w=6) + \
        arrow(xw - rw * 0.3, AXIS - rw - 70, xw + rw * 1.6, AXIS - rw - 70, head=26, w=6)


def a_claque(t):
    return arrow(300, 330, 760, 330) + arrow(1620, 330, 1160, 330)


def a_logo(t):
    return arrow(CX - 40, 400, CX - 230, 400) + arrow(CX + 40, 400, CX + 230, 400)


OUTRO = Anim("OUTRO", 3.2, outro_full, [
    Beat(F(2), "Le plan recule dès l'image 0 : la fenêtre se referme (r 1500 → 700 en 2 images) ; le point rentre par la gauche, coupé sur sa médiane.", "out_expo", ann=a_retour, onion=1, onion_dt=F(1)),
    Beat(F(5), "Le point percute la fenêtre : il dépasse de 30 px, s'écrase à 86 % puis rebondit. La plaque recule de 134 à 92 %.", "out_expo", ann=a_choc, onion=2, onion_dt=F(1)),
    Beat(F(18), "Vertige inversé (3.3-02), d'un seul geste : la fenêtre rétrécit ×4 pendant que la plaque rezoome de 92 à 160 % ; le point regrossit.", "inout_cubic", ann=a_vertigo_inv, onion=2, onion_dt=F(4)),
    Beat(F(27), "Morsure : l'orange rentre par le cou et avale la fenêtre de gauche à droite en 5 images. Pas de fondu.", "inout_cubic", ann=a_morsure, onion=0),
    Beat(F(31), "Anticipation en 3 images : la paire se tend, l'écart passe de 20 à 60 px, le cou s'affine à 16 px, la petite bulle recule.", "out_cubic", ann=a_tension_o, onion=1, onion_dt=F(2)),
    Beat(F(36), "Claquement : les deux bulles convergent et se contractent ensemble en 6 images, sans jamais laisser un grand disque seul.", "in_cubic", ann=a_claque, onion=2, onion_dt=F(1)),
    Beat(F(47), "Impact en point blanc (écrasé à 77 %), puis 3.4-02 : le cou casse, les points filent à leur place (+6 %), « sfeer » s'ouvre.", "out_back", ann=a_logo, onion=2, onion_dt=F(2)),
    Beat(F(76), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; l'arabe s'est écrit de droite à gauche.", "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Le point du logo devient la fenêtre : pour un programme de fidélité, le point se dépense et s'ouvre sur une expérience.",
        "Le vertige d'Hitchcock (le cadre avance, l'image recule) transforme l'échange de tailles 3.3-02 en geste de cinéma.",
        "L'image recule comme un élastique qu'on tend ; au saut elle repart en avant : la fronde donne son élan à la plongée.",
    ]),
    ("Charte et corrections", [
        "Comportements cités : 3.4-01 (division), 3.3-02 (échange de tailles), 3.4-02 (logo). Tout reste sur l'axe y = 540.",
        "Rapport des tailles ≤ 3:1 en tenue, le point ne descend jamais sous 114 px. Le logo arrive seul, sur le dégradé.",
        "Pas de fondu ni d'anneau : la fenêtre s'allume et s'éteint par une morsure le long de l'axe. À valider : point blanc → orange en 1 image.",
    ]),
    ("Mouvement", [
        "Une anticipation avant chaque geste (inspiration, paire qui se tend, recul de 10 %), dépassements de 6 %, écrasement à chaque arrivée.",
        "Vertige en deux temps à l'intro, d'un seul geste à l'outro. Saut en 13 images : le vert couvre le cadre à 40 % de la durée.",
        "AE : deux cercles et un cou, plaque parentée au centre de la fenêtre, morsure = masque circulaire soustrait. Natif en Lottie.",
    ]),
]
