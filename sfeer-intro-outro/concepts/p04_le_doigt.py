"""Piste 4 (croquis de la DA) : « le doigt ».

Un doigt appuie sur une bulle (tap), glisse vers la droite et en tire une seconde par un cou
élastique : c'est elle qui devient la fenêtre. Elle est décentrée (x = 1250, « pas forcément au
centre ») ; la caméra pousse dessus, centrée sur elle, puis la recentre pendant la plongée.
Outro : la vidéo se rétracte dans une bulle à droite, le doigt revient, une pichenette la renvoie
vers la bulle de gauche (cou qui se reforme, fusion), tap final : onde du dégradé, deux points, logo.

Monde orange du film, bulles lavande (charte 2.46 : orange sur dégradé « ou l'inverse »),
main indigo à manchette bleu costume : sur l'orange, la main se lit sans contour.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, clamp01, lerp, prog  # noqa: E402
from blocks import GRAD, LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, COSTUME, INDIGO, LAVENDER, W, WHITE, _neck_circle, arrow, bridge_d,  # noqa: E402
                       curved_arrow, f, mix_hex, zoom_brackets)

CX = W / 2

META = {
    "id": "p04_le_doigt",
    "num": "P4",
    "title": "Le doigt",
    "principe": "Un doigt touche une bulle et en tire une autre : la bulle tirée devient la fenêtre, comme dans une app.",
    "logline": "Piste 4 de la DA. Un doigt appuie sur une bulle, glisse et en tire une seconde par un cou élastique : "
               "elle claque, gonfle et devient la fenêtre, décentrée ; la caméra plonge dedans.",
}


# =================================================================== géométrie (tracés horaires)
def circle_cw(x, r):
    r = max(r, 0.01)
    return f"M{f(x - r)} {AXIS}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_cw(x, rx, ry):
    return f"M{f(x - rx)} {AXIS}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z"


def hull_cw(x1, r1, x2, r2):
    """Enveloppe convexe de deux cercles (x1 < x2) : col plein."""
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, AXIS - r1 * ny), (x2 + r2 * nx, AXIS - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, AXIS + r2 * ny), (x1 + r1 * nx, AXIS + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def link(x1, r1, x2, r2, h):
    """Col de la charte entre deux cercles de l'axe ; gère cacahuète (chevauchement) et inclusion."""
    (x1, r1), (x2, r2) = sorted([(x1, r1), (x2, r2)])
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        return circle_cw(x1, r1) if r1 >= r2 else circle_cw(x2, r2)
    rmin = min(r1, r2)
    if d < r1 + r2:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        h = max(h, yi + 0.3 * (rmin - yi))
    if h >= 0.97 * rmin or _neck_circle((x1, AXIS, r1), (x2, AXIS, r2), h) is None:
        return hull_cw(x1, r1, x2, r2)
    return bridge_d((x1, AXIS, r1), (x2, AXIS, r2), h)


def pair_d(xa, ra, sxa, xb, rb, sxb, h):
    """Bulle A + bulle B reliées par le col (h None : séparées). Étirements sx, volume conservé."""
    parts = [ellipse_cw(xa, ra * sxa, ra / sxa)]
    if rb > 0.5:
        if h is not None:
            parts.append(link(xa, ra * min(sxa, 1 / sxa), xb, rb * min(sxb, 1 / sxb), h))
        parts.append(ellipse_cw(xb, rb * sxb, rb / sxb))
    return " ".join(parts)


def speed(fn, t, dt=0.02):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def stretch(v, k=14000, cap=0.32):
    """Étirement dans le sens de la vitesse (px/s), plafonné : sx ≤ 1,32."""
    return 1 + min(cap, abs(v) / k)


def lim(sx):
    return max(1 / 1.35, min(1.35, sx))


# =================================================================== la main (accessoire, aplat)
_INDEX = "M-34 250L-34 34C-34 15 -19 0 0 0C19 0 34 15 34 34L34 250Z"
_NAIL = "M-19 64L-19 30C-19 19 -11 12 0 12C11 12 19 19 19 30L19 64Z"
_PALM = ("M-40 170Q-44 140 -10 140L120 150Q170 156 172 200L176 330Q180 430 90 470L-20 480"
         "Q-110 470 -120 380L-128 260Q-130 220 -96 214Q-60 210 -52 240Z")
_CREASE = ("M30 227Q100 219 150 233L150 240Q100 226 30 234Z M30 297Q100 289 156 303L156 310Q100 296 30 304Z "
           "M34 367Q96 359 150 371L150 378Q96 366 34 374Z")
_CUFF = "M-110 460L160 440L196 820L-96 840Z"
_HAND = [("index", _INDEX, INDIGO), ("paume", _PALM, INDIGO), ("plis", _CREASE, mix_hex(INDIGO, LAVENDER, 0.42)),
         ("ongle", _NAIL, mix_hex(INDIGO, LAVENDER, 0.3)), ("manche", _CUFF, COSTUME)]


def _xf(d, x, y, s):
    """Tracé absolu (M L Q C Z) déplacé en (x, y) et mis à l'échelle s autour du bout de l'index."""
    out, n = [], 0
    for tk in re.findall(r"[A-Za-z]|-?\d*\.?\d+", d):
        if tk.isalpha():
            out.append(tk)
            n = 0
        else:
            out.append(f((x if n % 2 == 0 else y) + float(tk) * s))
            n += 1
    return " ".join(out)


HS = 1.4                              # échelle de la main : le doigt fait 1/3 de la bulle, comme sur le croquis


def hand(x, y, s=1.0, ghost=False):
    """Main en aplat, index tendu vers le haut ; (x, y) = bout de l'index. Formes pleines, sans contour."""
    s *= HS
    return [{"k": "fill", "id": f"main-{key}", "fill": col, "d": _xf(d, x, y, s),
             "ghost": ghost and key == "index", "pts": [(x, y)] if key == "index" else []}
            for key, d, col in _HAND]


# =================================================================== INTRO (4,0 s)
XA, XB, TIP = 600, 1250, 592          # bulle tapée, fenêtre décentrée, bout du doigt (sous le centre de A)
DG = (-0.6, 0.8)                      # direction bas-gauche : la main entre ↗ et sort ↙ (diagonale)

rA = Track((0, 0), (F(5), 168, "out_cubic"), (F(10), 150, "inout_cubic"),       # pop avec dépassement
           (F(24), 150), (F(33), 136, "out_cubic"),                              # la masse part dans B
           (F(44), 142, "inout_cubic"), (F(53), 86, "out_back"))                 # échange de taille (3.3-02)
xA = Track((F(23), XA), (F(35), XA + 40, "inout_cubic"), (F(41), XA + 44, "linear"),
           (F(54), XA, "ressort"))                                               # relâché : A revient en ressort
xB = Track((F(23), XA + 10), (F(27), XA + 92, "out_cubic"),                      # le bord se bombe
           (F(33), XB + 62, "inout_expo"),                                       # fouet : 560 px en 6 images
           (F(43), XB, "ressort"))                                               # dépasse de 62 px, revient
rB = Track((F(23), 0), (F(27), 64, "out_cubic"), (F(33), 98, "out_cubic"), (F(43), 108, "inout_cubic"),
           (F(45), 100, "inout_cubic"),                                          # inspire avant de gonfler
           (F(54), 270, "out_back"))                                             # gonfle : +9 % puis 270
hF = Track((F(23), 0.9), (F(27), 0.55, "out_cubic"), (F(33), 0.07, "in_cubic"),  # le cou s'affine (7 %)
           (F(43), 0.2, "out_cubic"), (F(54), 0.3, "inout_cubic"))
gI = Track((F(46), 0), (F(55), 1, "out_expo"))                                   # la vidéo s'ouvre dans B

# la main : entrée ↗, recul de 22 px (anticipation), appui, glissé de 96 px, sortie ↙ (transitoire 7 i.)
hd = Track((F(1), 980), (F(10), -18, "out_expo"), (F(14), 0, "inout_cubic"),
           (F(19), 22, "out_cubic"), (F(22), 0, "in_expo"),
           (F(41), 0), (F(48), 1150, "in_expo"))
hs = Track((F(1), 1.0), (F(14), 1.0), (F(19), 1.04, "out_cubic"), (F(22), 0.94, "in_expo"),
           (F(40), 0.94), (F(42), 1.05, "out_cubic"), (F(48), 1.0))
drag = Track((F(23), 0), (F(35), 96, "inout_cubic"), (F(41), 104, "linear"))

# caméra : inspire (-5 %), puis plongée centrée sur la fenêtre qui se recentre (1250 -> 960)
kc = Track((F(54), 1.0), (F(58), 0.95, "out_cubic"), (F(98), 4.7, "plongee"))
zv_in = Track((F(45), 0.78), (F(58), 0.86, "linear"), (F(100), 1.14, "plongee"))


def cam_k(t):
    return kc(t) + drift(t, F(98), 1.2)


def recentre(t):
    return prog(t, F(58), F(98), "plongee")


def intro(t):
    k = cam_k(t)
    S = lerp(XB, CX, recentre(t))

    def X(x):
        return S + (x - XB) * k

    zv = zv_in(t) + drift(t, F(45), 0.25)                                   # la plaque ne s'arrête jamais
    xa, xb = xA(t), xB(t)
    ra = rA(t) * breathe(t, 0.018, 0.9)
    rb = rB(t) * breathe(t, 0.022, 0.8, 0.3)
    Xa, Xb, Ra, Rb = X(xa), X(xb), ra * k, rb * k
    if Rb >= math.hypot(max(Xb, W - Xb), AXIS) + 4:                           # plein cadre : une seule plaque
        return [video(zv, ghost=False)]
    L = [{"k": "bg", "v": "orange"}]
    if ra < 0.5:
        return L
    # A : écrasement au pop, à l'appui (128 %), traînée du glissé, recul au relâché, étirement de plongée
    vA = speed(lambda u: S + (xA(u) - XB) * cam_k(u), t)
    sxa = lim(squash(t, F(5), F(14), 0.16) * squash(t, F(22), F(10), 0.28) * stretch(vA, 16000, 0.3))
    # B : fouet (étirement 1,32 max), ressort, écrasement quand elle gonfle
    sxb = lim(stretch(speed(xB, t), 15000, 0.33) * squash(t, F(54), F(8), 0.1))
    h = hF(t) * min(ra, rb) * k if rb > 0.5 else None
    L.append({"k": "fill", "id": "bulles", "fill": LAVENDER, "d": pair_d(Xa, Ra, sxa, Xb, Rb, sxb, h),
              "pts": [(Xa, AXIS), (Xb, AXIS)] if rb > 0.5 else [(Xa, AXIS)]})
    g = gI(t)
    if g > 0:                                                                 # iris vert depuis le centre de B
        dv = circle_cw(Xb, Rb * min(sxb, 1 / sxb) * g) if g < 0.999 else ellipse_cw(Xb, Rb * sxb, Rb / sxb)
        L.append(video(zv, dv, ghost=g < 0.999))
    d = hd(t)
    if d < 1100:
        L += hand(XA + drag(t) + DG[0] * d, TIP + DG[1] * d, hs(t), ghost=True)
    return L


def a_entree(t):
    return arrow(120, 1010, 330, 730)


def a_recul(t):
    return arrow(XA - 190, TIP + 200, XA - 260, TIP + 295)


def a_appui(t):
    return arrow(XA - 200, AXIS - 230, XA - 330, AXIS - 230) + arrow(XA + 200, AXIS - 230, XA + 330, AXIS - 230)


def a_fouet(t):
    return arrow(XA + 260, AXIS - 260, XB + 120, AXIS - 260) + arrow(XA + 40, TIP + 330, XA + 140, TIP + 330)


def a_relache(t):
    return curved_arrow(XB + 120, AXIS - 210, XB + 70, AXIS - 300, XB - 10, AXIS - 210) \
        + arrow(XA - 120, TIP + 360, XA - 330, TIP + 640)


def a_gonfle(t):
    return "".join(arrow(XB + dx * 200, AXIS + dy * 200, XB + dx * 300, AXIS + dy * 300)
                   for dx in (-1, 1) for dy in (-1, 1)) + arrow(XA - 230, AXIS, XA - 120, AXIS)


def a_plongee(t):
    k = cam_k(t)
    S = lerp(XB, CX, recentre(t))
    return zoom_brackets(S, AXIS, 1500, 860) + arrow(S - 200, AXIS + 330, S - 520, AXIS + 330) \
        + "".join(arrow(S + dx * 420, AXIS + dy * 250, S + dx * 640, AXIS + dy * 380) for dx in (-1, 1) for dy in (-1, 1)) \
        if k > 0 else ""


def a_croquis(t):
    return zoom_brackets(XB, AXIS, 900, 700)


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(6), "Une bulle lavande éclot en 5 images (+12 %) et s'écrase à l'arrivée ; la main entre en diagonale ↗ et dépasse de 18 px.",
         "out_expo", ann=a_entree, onion=2, onion_dt=F(2)),
    Beat(F(19), "Anticipation : le doigt recule de 22 px ↙ et grossit de 4 % (il se lève de l'écran) pendant 5 images, avant d'appuyer.",
         "out_cubic", ann=a_recul, onion=2, onion_dt=F(2)),
    Beat(F(22), "Tap : appui en 3 images (main à 94 %), la bulle s'écrase à 128 % × 78 % puis revient au rond sur un ressort amorti.",
         "ressort_vif", ann=a_appui, onion=2, onion_dt=F(1)),
    Beat(F(31), "Le doigt glisse de 96 px → ; une 2e bulle claque hors de la 1re : 560 px en 6 images, étirée à 132 %, cou affiné à 7 %.",
         "inout_expo", ann=a_fouet, onion=3, onion_dt=F(1)),
    Beat(F(42), "Relâché : la bulle tirée dépasse de 62 px et revient en ressort ; le doigt part ↙ en 7 images (transitoire d'accessoire).",
         "ressort", ann=a_relache, onion=3, onion_dt=F(2)),
    Beat(F(50), "Échange de taille (3.3-02) : la fenêtre gonfle 108 → 270 px (+9 %), la 1re rétrécit à 86 px ; la vidéo s'ouvre en iris.",
         "out_back", ann=a_gonfle, onion=2, onion_dt=F(2)),
    Beat(F(72), "Plongée : zoom ×4,7 centré sur la fenêtre, qui glisse de x = 1250 à 960 ; la 1re bulle file à gauche le long de l'axe.",
         "plongee", ann=a_plongee, onion=2, onion_dt=F(2)),
    Beat(F(97), "Plein cadre vidéo : la poussée continue (+1,2/s) et la plaque contre-zoome plus lentement. Raccord en mouvement.",
         "out_cubic", onion=0),
])


# =================================================================== OUTRO (4,0 s)
XA2, XB2, TIP2 = 780, 1420, 572
DG2 = (0.6, 0.8)                     # la main revient ↖ depuis le bas-droit, ressort ↘
TIPX2 = 1674                         # bout du doigt contre le bord droit de la fenêtre
T_LOGO = F(57)
RM = 172                             # bulle fusionnée

k2 = Track((0, 5.6), (F(3), 5.8, "out_cubic"), (F(15), 0.96, "inout_expo"), (F(21), 1.0, "ressort"))
zv_out = Track((0, 1.2), (F(3), 1.25, "linear"), (F(18), 1.02, "out_cubic"), (F(38), 0.86, "linear"))
rB2 = Track((0, 200), (F(29), 200), (F(38), 140, "inout_cubic"))
xB2 = Track((F(29), XB2), (F(35), 1110, "out_cubic"), (F(40), 1010, "in_cubic"))   # pichenette, puis attraction
flick = Track((F(27.5), 1.0), (F(28.7), 0.74, "out_cubic"), (F(30), 1.0, "out_cubic"))  # B écrasée par le doigt
xA2 = Track((F(33), XA2), (F(40), 850, "in_cubic"))                                    # A tend vers B
g2 = Track((F(29), 1.0), (F(37), 0.0, "in_expo"))                                      # la vidéo s'aspire dans B
merge = Track((F(40), 0.0), (F(45), 1.0, "out_cubic"))
XM0 = (850 * 100 ** 2 + 1010 * 140 ** 2) / (100 ** 2 + 140 ** 2)                       # centre de masse au contact
xM = Track((F(40), XM0), (F(48), CX, "ressort"))
rM = Track((F(40), RM), (F(48), RM), (F(53), 82, "in_back"))                           # le tap la comprime
ripple = Track((F(48), 0), (F(60), 1180, "out_cubic"))                                 # onde du dégradé
split = Track((F(52), 0.0), (F(57), 1.0, "out_cubic"))
travel = Track((F(56), 0.0), (F(66), 1.0, "emphase"))

hd2 = Track((F(9), 980), (F(19), -16, "out_expo"), (F(22), 0, "inout_cubic"),
            (F(25), 24, "out_cubic"), (F(27), 0, "in_expo"),
            (F(44), 0), (F(46), 20, "out_cubic"), (F(48), 0, "in_expo"),
            (F(50), 0), (F(56), 1150, "in_expo"))
hx2 = Track((F(25), 0), (F(26), 10, "out_cubic"), (F(29), -200, "in_expo"), (F(44), CX - TIPX2, "out_cubic"))
hs2 = Track((F(9), 1.0), (F(22), 1.0), (F(25), 1.04, "out_cubic"), (F(27), 1.0, "in_expo"),
            (F(44), 1.0), (F(46), 1.04, "out_cubic"), (F(48), 0.94, "in_expo"), (F(50), 0.94),
            (F(52), 1.03, "out_cubic"))


def S2(t):
    return lerp(CX, XB2, prog(t, F(3), F(15), "inout_expo"))


def outro(t):
    k, S = k2(t), S2(t)

    def X(x):
        return S + (x - XB2) * k

    zv = zv_out(t) - drift(t, F(38), 0.2)
    rb = rB2(t) * breathe(t, 0.02, 0.8)
    Xb, Rb = X(xB2(t)), rb * k
    if t < F(24) and Rb >= math.hypot(max(Xb, W - Xb), AXIS) + 4:
        return [video(zv, ghost=False)]
    rp = ripple(t)
    L = [{"k": "bg", "v": "gradient" if rp >= 1105 else "orange"}]
    if 0.5 < rp < 1105:                                                     # le tap ouvre le monde SFEER
        L.append({"k": "fill", "id": "onde", "fill": GRAD, "d": circle_cw(CX, rp), "pts": []})
    m = merge(t)
    if t < F(40):
        xa = X(xA2(t))
        ra = 100 * k * breathe(t, 0.025, 0.9, 0.5)
        # B : écrasée à l'impact du doigt, puis étirée par la vitesse ; A s'étire vers B (attraction)
        sxb = lim(squash(t, F(15), F(9), 0.14) * flick(t) * stretch(speed(xB2, t), 12000))
        sxa = lim(squash(t, F(17), F(9), 0.12) * (1 + 0.16 * prog(t, F(35), F(40), "in_cubic")))
        d = Xb - xa
        near = clamp01((1.3 * (ra + Rb) - d) / (0.3 * (ra + Rb)))           # le cou se reforme à l'approche
        h = min(ra, Rb) * (0.06 + 0.5 * near) if near > 0 else None
        L.append({"k": "fill", "id": "bulles", "fill": LAVENDER, "d": pair_d(xa, ra, sxa, Xb, Rb, sxb, h),
                  "pts": [(xa, AXIS), (Xb, AXIS)]})
        g = g2(t)
        if g > 0.001:
            dv = ellipse_cw(Xb, Rb * sxb, Rb / sxb) if g >= 0.999 else circle_cw(Xb, Rb * min(sxb, 1 / sxb) * g)
            L.append(video(zv, dv, ghost=False))
    elif t < F(52):
        # fusion : les deux centres se rejoignent (cacahuète -> rond), impact écrasé 130 %
        xm = xM(t)
        xa, xb = lerp(850, xm, m), lerp(1010, xm, m)
        ra, rb_ = lerp(100, rM(t), m), lerp(140, rM(t), m)
        sx = lim(squash(t, F(40), F(10), 0.3) * squash(t, F(48), F(8), 0.24))
        if m < 0.999:
            dd = pair_d(xa, ra, 1.0, xb, rb_, 1.0, 0.5 * min(ra, rb_))
        else:
            dd = ellipse_cw(xm, rM(t) * sx, rM(t) / sx)
        L.append({"k": "fill", "id": "bulles", "fill": LAVENDER, "d": dd, "pts": [(xm, AXIS)]})
    else:
        # charte 3.4-01 : la bulle se divise (cacahuète, col, rupture), les moitiés filent vers les points du logo
        u, v = split(t), travel(t)
        r2 = rM(t) / math.sqrt(2)
        gx = LG["dot_g"][0]
        e_snap = 1.7 * r2
        spread = e_snap * u + (CX - gx - e_snap) * v
        r = lerp(r2, LG["dot_r"] * breathe(t, 0.2, 1.1), v)
        c1, c2 = CX - spread, CX + spread
        sx = lim(squash(t, F(56.5), F(8), -0.16))                            # recul des moitiés après la rupture
        if u < 0.55:
            dd = link(c1, r, c2, r, 0.5 * r * (1 - u))
        elif u < 0.88:
            dd = link(c1, r, c2, r, r * 0.2 * (0.88 - u) / 0.33 + 0.8)
        else:
            dd = ellipse_cw(c1, r * sx, r / sx) + " " + ellipse_cw(c2, r * sx, r / sx)
        col = mix_hex(LAVENDER, WHITE, prog(t, F(57), F(65)))
        L.append({"k": "fill", "id": "points-logo", "fill": col, "d": dd, "pts": [(c1, AXIS), (c2, AXIS)]})
    d = hd2(t)
    if d < 1100:
        L += hand(TIPX2 + hx2(t) + DG2[0] * d, TIP2 + DG2[1] * d, hs2(t), ghost=True)
    return L


def outro_full(t):
    """Outro + carton logo (les points amenés par l'animation suivent la poussée du carton)."""
    L = outro(t)
    dots = [x for x in L if x.get("id") == "points-logo"]
    rest = [x for x in L if x.get("id") != "points-logo"]
    return rest + endcard(t, T_LOGO, dots=False, extra=dots)


def a_retrait(t):
    return "".join(arrow(CX + dx * 860, AXIS + dy * 480, CX + dx * 560, AXIS + dy * 320)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_arme(t):
    return arrow(1880, 1050, 1790, 930) + arrow(TIPX2 + 70, TIP2 + 330, TIPX2 + 130, TIP2 + 410)


def a_pichenette(t):
    return arrow(1600, AXIS - 290, 1100, AXIS - 290) + arrow(TIPX2 - 120, TIP2 + 400, TIPX2 - 300, TIP2 + 400)


def a_fusion(t):
    return arrow(640, AXIS - 260, 760, AXIS - 260) + arrow(1240, AXIS - 260, 1120, AXIS - 260)


def a_tap(t):
    return arrow(CX + 200, TIP2 + 330, CX + 150, TIP2 + 260)


def a_onde(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 330, CX + dx * 720, AXIS + dy * 460)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_division(t):
    return arrow(CX - 200, AXIS - 200, CX - 330, AXIS - 200) + arrow(CX + 200, AXIS - 200, CX + 330, AXIS - 200)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(8), "Plein cadre, la plaque pousse de 3 % (anticipation) puis la vidéo est aspirée dans une bulle à droite (x = 1420) en 13 images.",
         "inout_expo", ann=a_retrait, onion=2, onion_dt=F(2)),
    Beat(F(25), "La bulle s'est posée en ressort, la lavande est entrée par la gauche. La main revient ↖, puis le doigt recule de 24 px ↘ pour armer.",
         "out_expo", ann=a_arme, onion=2, onion_dt=F(2)),
    Beat(F(31), "Pichenette : le doigt frappe ←, la bulle s'écrase à 74 % puis part étirée à 130 % ; la vidéo s'aspire en iris (8 images).",
         "in_expo", ann=a_pichenette, onion=2, onion_dt=F(1)),
    Beat(F(40), "Le cou se reforme à l'approche, la bulle de gauche s'étire de 16 % vers elle ; fusion en cacahuète, impact écrasé 130 %.",
         "in_cubic", ann=a_fusion, onion=2, onion_dt=F(2)),
    Beat(F(47), "Le doigt a suivi la bulle sous elle (700 px ←) : recul de 20 px, puis tap en 2 images, main à 94 %.",
         "in_expo", ann=a_tap, onion=2, onion_dt=F(2)),
    Beat(F(51), "L'onde du tap ouvre le dégradé depuis le centre (12 images). La bulle se comprime à 48 % ; la main sort ↘ en 6 images.",
         "out_cubic", ann=a_onde, onion=2, onion_dt=F(1)),
    Beat(F(54), "Charte 3.4-01 : la bulle se divise, le col casse net, les deux moitiés reculent (écrasées à 84 %) et filent vers les points.",
         "out_cubic", ann=a_division, onion=2, onion_dt=F(1)),
    Beat(F(92), "Points du logo en place, « sfeer » ouvert depuis le centre, arabe de droite à gauche. Tenue vivante, poussée lente.",
         "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "Le geste le plus familier : toucher, glisser. La fenêtre s'ouvre comme une app, en écho à la séquence 08 (paiement sans contact).",
        "La bulle tirée reste liée à la première par le cou : la grande et la petite bulle de la charte (2.46), construites par la main.",
        "Fenêtre décentrée comme sur ton croquis : la caméra la recentre en plongeant. Marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Fond orange et bulles lavande (2.46 : « ou l'inverse ») : la main indigo, couleur des costumes du film, s'y lit sans contour.",
        "Ajouts au croquis : le doigt glisse de 96 px avant de lâcher, et la fenêtre gonfle par échange de taille (3.3-02). Bulles sur l'axe.",
        "Écart à valider : la main entre et sort en diagonale (↗ ↙), sortie en 7 images. C'est un accessoire, jamais posé sur le logo.",
    ]),
    ("Mouvement", [
        "Rien de fixe : pop, recul du doigt, tap écrasé, fouet de 6 images, ressort, échange de taille, plongée qui ne s'arrête pas.",
        "Le cou s'affine à 7 % au bout du fouet : la marque vit au bord de la rupture. L'outro casse pour de vrai, en deux points.",
        "AE : main en calques de forme sous un nul, bulles en Merge Paths + Offset (congé), caméra = nul centré sur la fenêtre.",
    ]),
]
