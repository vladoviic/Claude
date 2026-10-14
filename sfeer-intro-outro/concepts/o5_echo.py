"""Concept original O5 : « L'Écho, une voix devient un chœur ».

Une bulle orange se divise en trois (3.5-01), puis la chaîne bourgeonne jusqu'aux bords (3.5-02 en
miroir) : on obtient la rangée axiale du motif 3.6, trois bulles pleines et deux demi-bulles coupées
sur leur médiane. Chaque génération tombe sur un temps (120 bpm = 12,5 images) et sonne une octave
plus haut. La rangée s'allume en fenêtres, de gauche à droite (arpège), respire, puis une marée de
bulles qui gonflent sur place et fusionnent ouvre le plein cadre.
Outro : marée inverse, extinction de droite à gauche, rassemblement en une bulle (3.5-01 à l'envers),
puis la bulle « s'éteint en écho » (trois rebonds de plus en plus petits) jusqu'au point du logo.

Différences : p03 divise en motif ×2 (masse) ; ici une seule RANGÉE sur l'axe et un rythme musical,
et l'on entre par une fusion collective, sans zoom de cercle.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, bezier, breathe, clamp01, ease, prog  # noqa: E402
from blocks import LG, endcard, squash, video  # noqa: E402
from sfeer_svg import AXIS, H, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, f, mix_hex  # noqa: E402

CX = W / 2
BEAT = F(12.5)                         # 120 bpm
XS = (0, 480, 960, 1440, 1920)         # nœuds fixes de la rangée (3 pleines + 2 demi-bulles)
RS = (190, 210, 230, 210, 190)
TIDE = bezier(0.7, 0, 0.84, 0)         # marée : ease-in fort (spec : cubic-bezier(0.7,0,0.84,0))

META = {
    "id": "o5_echo",
    "num": "O5",
    "title": "L'Écho",
    "principe": "Une bulle se divise en rythme jusqu'aux bords, s'allume en fenêtres ; une marée les fond en plein cadre.",
    "logline": "Une bulle se divise en trois, puis en cinq jusqu'aux bords, sur le tempo. La rangée s'allume en fenêtres, "
               "de gauche à droite, puis une marée de bulles qui fusionnent ouvre le plein cadre. L'outro rassemble tout en un point.",
}


# =================================================================== géométrie (tracés horaires)
def ell(cx, rx, ry, cy=AXIS):
    return (f"M{f(cx - rx)} {f(cy)}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0"
            f"a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z")


def hull(x1, r1, x2, r2, cy=AXIS):
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, cy - r1 * ny), (x2 + r2 * nx, cy - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, cy + r2 * ny), (x1 + r1 * nx, cy + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def neck(x1, r1, x2, r2, h, cy=AXIS):
    """Col de la charte entre deux cercles de l'axe ; gère chevauchement et inclusion."""
    if h is None or r1 < 1 or r2 < 1:
        return ""
    if x2 < x1:
        x1, r1, x2, r2 = x2, r2, x1, r1
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        return ""
    rmin = min(r1, r2)
    if d < r1 + r2:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        h = max(h, yi + 0.5)
    if h >= rmin - 0.5:
        return hull(x1, r1, x2, r2, cy)
    if _neck_circle((x1, cy, r1), (x2, cy, r2), h) is None:
        # très fort chevauchement : l'union des deux cercles suffit (festons nets, pas d'enveloppe droite)
        return "" if d < r1 + r2 else hull(x1, r1, x2, r2, cy)
    return bridge_d((x1, cy, r1), (x2, cy, r2), h)


def fillet_h(x1, r1, x2, r2, k=0.9):
    """Épaisseur (demi) du col de congé constant R = k·r moyen (mesure de la charte) ; None si rompu."""
    R = k * (r1 + r2) / 2
    d = abs(x2 - x1)
    a, b = r1 + R, r2 + R
    if d < 1e-6:
        return 1e9
    xa = (a * a - b * b + d * d) / (2 * d)
    y2 = a * a - xa * xa
    if y2 <= 0:
        return None
    return math.sqrt(y2) - R


def neck_h(x1, r1, x2, r2, kh=0.22):
    """Col tenu à 22 % du petit diamètre ; tant que les bulles se chevauchent, neck() le tient
    au-dessus de l'intersection (pose cacahuète de la scission)."""
    return kh * min(r1, r2)


def row_d(bubs, hs):
    """bubs = [(x, rx, ry)], hs = cols entre voisines (None = séparées) : union horaire."""
    parts = [ell(x, rx, ry) for x, rx, ry in bubs if rx > 0.5 and ry > 0.5]
    for i, h in enumerate(hs):
        (x1, rx1, ry1), (x2, rx2, ry2) = bubs[i], bubs[i + 1]
        parts.append(neck(x1, min(rx1, ry1), x2, min(rx2, ry2), h))
    return " ".join(p for p in parts if p)


def bump(t, t0, dur):
    u = (t - t0) / dur
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def ghost_layer(d, lid, pts=None):
    """Calque invisible : sert seulement à la pelure d'oignon et aux trajectoires de la planche."""
    return {"k": "fill", "id": lid, "d": d, "fill": "none", "ghost": True, "pts": pts or []}


def covers_frame(circles):
    """Vrai si l'union des cercles (x, r) de l'axe couvre tout le cadre (bords haut et bas testés)."""
    for xx in range(0, W + 1, 40):
        if not any((xx - x) ** 2 + AXIS ** 2 <= r * r for x, r in circles):
            return False
    return True


# =================================================================== INTRO (3,2 s)
# temps 1 (f0) : 1 -> 3 ; temps 2 (f12,5) : 3 -> 5 ; temps 3 (f25) : écho en fenêtres ;
# temps 4 (f37,5) : la rangée respire ; temps 5 (f50) : marée, plein cadre à f57
pop_c = Track((0, 206), (F(3), 258, "out_cubic"), (F(9), 230, "out_back"))
bud_l = Track((0, 80), (F(9), 480, "out_back"))
bud_r = Track((F(2), 80), (F(11), 480, "out_back"))                  # 2 images de retard
bud_rl = Track((0, 140), (F(9), 210, "out_cubic"))
bud_rr = Track((F(2), 140), (F(11), 210, "out_cubic"))
edge_l = Track((F(12), 0), (F(20), 1, "out_back"))                    # 2e génération, plus rapide
edge_r = Track((F(14), 0), (F(22), 1, "out_back"))
LIGHT_T = [F(25 + 2 * i) for i in range(5)]                          # arpège de gauche à droite
T_BREATHE = F(37)
anticip = Track((F(43), 0), (F(47), 1, "out_cubic"))
TIDE_T = (F(51), F(49), F(47), F(50), F(52))                          # centre d'abord, puis les côtés
TIDE_DUR = F(9)
TIDE_R = 650


def plate_zoom_in(t):
    """Plaque : 125 % à l'allumage, contre-zoom pendant la marée, puis rampe continue vers 100 %."""
    z = Track((F(24), 1.26), (F(47), 1.2, "linear"), (F(60), 1.12, "out_cubic"), (F(80), 1.0, "linear"))(t)
    return z


def intro_row(t):
    """Rangée à l'instant t : [(x, r, sx)] pour les 5 nœuds (r = 0 : pas encore née)."""
    live = breathe(t, 0.02, 0.5)                                      # pulsation d'un temps
    xl, xr = CX - bud_l(t), CX + bud_r(t)
    # recul des latérales quand la 2e génération part d'elles (action / réaction)
    xl += 14 * bump(t, F(12), F(8))
    xr -= 14 * bump(t, F(14), F(8))
    el, er = edge_l(t), edge_r(t)
    x0 = xl - (xl - 0) * el if el > 0 else xl
    x4 = xr + (W - xr) * er if er > 0 else xr
    r0 = (110 + 80 * min(el, 1.0)) if t >= F(12) else 0.0
    r4 = (110 + 80 * min(er, 1.0)) if t >= F(14) else 0.0
    rows = [
        [x0, r0, squash(t, F(20), F(8), -0.16)],
        [xl, bud_rl(t), squash(t, F(8), F(8), 0.12)],
        [CX, pop_c(t), squash(t, 0, F(8), -0.1)],
        [xr, bud_rr(t), squash(t, F(10), F(8), 0.12)],
        [x4, r4, squash(t, F(22), F(8), -0.16)],
    ]
    # la rangée respire : grandes et petites échangent leur taille en vague (3.6), 2 images d'écart
    b = prog(t, F(36), F(40)) * (1 - prog(t, F(44), F(48)))
    for i, row in enumerate(rows):
        sgn = 1 if i in (1, 3) else -1
        wave = 1 + b * 0.1 * sgn * math.sin(2 * math.pi * (t - T_BREATHE - i * F(2)) / F(12))
        pop = 1 + 0.1 * bump(t, LIGHT_T[i] - F(1), F(5))
        row[1] *= live * wave * pop * (1 - 0.06 * anticip(t))
        # marée : chaque bulle gonfle sur place jusqu'à fusionner
        u = clamp01((t - TIDE_T[i]) / TIDE_DUR)
        if u > 0:
            row[1] = row[1] + (TIDE_R - row[1]) * TIDE(u)
    return rows


def lit(i, t):
    """Allumage en fenêtre : iris vert depuis le centre, 4 images, au sommet du pop."""
    return ease("out_expo")(clamp01((t - LIGHT_T[i] - F(1)) / F(4)))


def intro(t):
    rows = intro_row(t)
    circles = [(x, r) for x, r, _ in rows if r > 0.5]
    if t > F(47) and covers_frame(circles):
        return [video(plate_zoom_in(t), ghost=False)]
    bubs = [(x, r * sx, r / sx) for x, r, sx in rows]
    hs = []
    for i in range(4):
        (x1, r1, _), (x2, r2, _) = rows[i], rows[i + 1]
        hs.append(neck_h(x1, r1, x2, r2) if r1 > 1 and r2 > 1 else None)
    L = [{"k": "bg", "v": "gradient"}]
    us = [lit(i, t) for i in range(5)]
    # orange : ce qui n'est pas encore fenêtre
    o_parts = [ell(x, rx, ry) for (x, rx, ry), u in zip(bubs, us) if u < 0.999 and rx > 0.5]
    for i, h in enumerate(hs):
        if h is not None and min(us[i], us[i + 1]) < 0.999:
            (x1, rx1, ry1), (x2, rx2, ry2) = bubs[i], bubs[i + 1]
            o_parts.append(neck(x1, min(rx1, ry1), x2, min(rx2, ry2), h))
    o_d = " ".join(p for p in o_parts if p)
    if o_d:
        L.append({"k": "fill", "id": "rangee", "fill": ORANGE, "d": o_d, "ghost": t < F(24),
                  "pts": [(x, AXIS) for x, _, _ in rows]})
    # vidéo : iris allumés + cols entre deux fenêtres
    v_parts = []
    for (x, rx, ry), u in zip(bubs, us):
        if u > 0.002:
            v_parts.append(ell(x, rx * u, ry * u))
    for i, h in enumerate(hs):
        g = clamp01((min(us[i], us[i + 1]) - 0.9) / 0.1)
        if h is not None and g > 0:
            (x1, rx1, ry1), (x2, rx2, ry2) = bubs[i], bubs[i + 1]
            v_parts.append(neck(x1, min(rx1, ry1), x2, min(rx2, ry2), max(h * g, 1)))
    if v_parts:
        v_d = " ".join(p for p in v_parts if p)
        L.append(video(plate_zoom_in(t), d=v_d, ghost=False))
        if t >= F(24):
            L.append(ghost_layer(row_d(bubs, hs), "fenetres", [(x, AXIS) for x, _, _ in rows]))
    return L


# ---- annotations intro
def a_scission(t):
    return arrow(CX - 260, AXIS - 330, CX - 520, AXIS - 330) + arrow(CX + 260, AXIS - 330, CX + 520, AXIS - 330)


def a_bords(t):
    return arrow(380, AXIS - 300, 60, AXIS - 300) + arrow(W - 380, AXIS - 300, W - 60, AXIS - 300)


def a_arpege(t):
    return arrow(60, AXIS - 330, 1860, AXIS - 330, dash=True)


def a_vague(t):
    return arrow(200, AXIS + 330, 1720, AXIS + 330, dash=True)


def a_maree(t):
    return "".join(arrow(x, AXIS + s * 330, x, AXIS + s * 500) for x in (480, 960, 1440) for s in (-1, 1))


INTRO = Anim("INTRO", 3.2, intro, [
    Beat(F(3), "Image 0, temps 1 : la bulle claque (+12 %) et se divise en trois (3.5-01) ; le bourgeon droit part 2 images après le gauche.",
         "out_back", ann=a_scission, onion=0),
    Beat(F(7), "Les bourgeons dépassent de 10 % puis reviennent ; le col passe de cacahuète à 22 % du diamètre. 1re note.",
         "out_back", onion=1, onion_dt=F(3)),
    Beat(F(16), "Temps 2, une octave plus haut : chaque latérale lance un bourgeon vers le bord (8 images) et recule de 14 px.",
         "out_back", ann=a_bords, onion=2, onion_dt=F(2)),
    Beat(F(23), "Rangée axiale du motif 3.6 : 3 bulles et 2 demi-bulles coupées pile à x = 0 et 1920, écrasées à l'impact (84 %).",
         "ressort", onion=0),
    Beat(F(30), "Temps 3, l'écho : de gauche à droite, chaque bulle fait un pop de 10 % et s'allume en fenêtre (iris de 4 images, 2 d'écart).",
         "out_expo", ann=a_arpege, onion=0),
    Beat(F(41), "Temps 4 : la rangée respire, grandes et petites échangent leur taille (±10 %) en vague, 2 images d'écart.",
         "inout_cubic", ann=a_vague, onion=2, onion_dt=F(3)),
    Beat(F(57), "Temps 5, la marée : contraction de 6 %, puis les bulles gonflent sur place (centre d'abord) et fusionnent en 9 images.",
         "in_expo", ann=a_maree, onion=2, onion_dt=F(2)),
    Beat(F(70), "Plein cadre à f61 : les festons quittent le cadre en haut et en bas ; la plaque glisse de 112 à 100 % sans s'arrêter.",
         "out_cubic", onion=0),
])


# =================================================================== OUTRO (4,0 s)
O_TIDE_T = (F(0), F(2), F(4), F(3), F(1))                 # les bords d'abord, puis vers le centre
O_DARK_T = [F(8 + 2 * (4 - i)) for i in range(5)]        # extinction de droite à gauche
# rassemblement : demi-bulles dans les latérales, puis latérales dans le centre (3.5-01 à l'envers)
g_edge_l = Track((F(19), 0), (F(21), -0.04, "out_cubic"), (F(27), 1, "in_cubic"))
g_edge_r = Track((F(21), 0), (F(23), -0.04, "out_cubic"), (F(29), 1, "in_cubic"))
g_lat_l = Track((F(31), 0), (F(33), -0.04, "out_cubic"), (F(38), 1, "in_cubic"))
g_lat_r = Track((F(33), 0), (F(35), -0.04, "out_cubic"), (F(40), 1, "in_cubic"))
# l'écho s'éteint : trois rebonds de plus en plus petits jusqu'au point du logo
ECHO_STEPS = ((F(42), 300, 200), (F(47), 200, 124), (F(52), 124, LG["dot_r"] * 2.0))
T_DOT = F(56)
split = Track((F(56), 0.0), (F(61), 1.0, "out_cubic"))
travel = Track((F(58), 0.0), (F(67), 1.0, "emphase"))
T_LOGO = F(59)


def o_plate(t):
    return 1.0 + 0.12 * prog(t, 0, F(22), "out_cubic") + 0.08 * t


def dark(i, t):
    return ease("out_expo")(clamp01((t - O_DARK_T[i] - F(1)) / F(4)))


def outro_row(t):
    live = breathe(t, 0.02, 0.5)
    rows = []
    for i in range(5):
        u = ease("out_expo")(clamp01((t - O_TIDE_T[i]) / F(8)))
        r = TIDE_R + (RS[i] - TIDE_R) * u
        r *= live * (1 + 0.1 * bump(t, O_DARK_T[i] - F(1), F(5)))
        rows.append([float(XS[i]), r, 1.0])
    # rassemblement
    ge_l, ge_r, gl_l, gl_r = g_edge_l(t), g_edge_r(t), g_lat_l(t), g_lat_r(t)
    rows[0][0] = 0 + (rows[1][0] - 0) * ge_l
    rows[0][1] *= 1 - clamp01(ge_l) ** 1.6
    rows[4][0] = W - (W - rows[3][0]) * ge_r
    rows[4][1] *= 1 - clamp01(ge_r) ** 1.6
    rows[1][1] = rows[1][1] * (1 + 0.09 * prog(t, F(25), F(29))) * (1 + 0.08 * bump(t, F(26), F(6)))
    rows[3][1] = rows[3][1] * (1 + 0.09 * prog(t, F(27), F(31))) * (1 + 0.08 * bump(t, F(28), F(6)))
    rows[1][2] = squash(t, F(27), F(8), 0.18)
    rows[3][2] = squash(t, F(29), F(8), 0.18)
    rows[1][0] = 480 + (CX - 480) * gl_l
    rows[1][1] *= 1 - clamp01(gl_l) ** 1.6
    rows[3][0] = 1440 - (1440 - CX) * gl_r
    rows[3][1] *= 1 - clamp01(gl_r) ** 1.6
    rows[0][0] = min(rows[0][0], rows[1][0]) if ge_l >= 1 else rows[0][0]
    rows[4][0] = max(rows[4][0], rows[3][0]) if ge_r >= 1 else rows[4][0]
    rc = rows[2][1] * (1 + 0.3 * prog(t, F(36), F(40), "out_back"))       # 230 -> 300 : le centre absorbe
    rows[2][2] = squash(t, F(38), F(8), 0.1) * squash(t, F(40), F(8), 0.2)
    # écho qui s'éteint : inspiration de 4 %, chute, pop à l'atterrissage
    for t0, ra, rb in ECHO_STEPS:
        if t >= t0:
            u = clamp01((t - t0) / F(4))
            rc = ra + (rb - ra) * ease("in_back")(u)
            rows[2][2] = squash(t, t0 + F(4), F(6), 0.16 if rb > 30 else 0.3)
    rows[2][1] = rc
    return rows


def outro_shapes(t):
    rows = outro_row(t)
    circles = [(x, r) for x, r, _ in rows if r > 0.5]
    if t < F(4) and covers_frame(circles):
        return [video(o_plate(t), ghost=False)]
    bubs = [(x, r * sx, r / sx) for x, r, sx in rows]
    hs = []
    for i in range(4):
        (x1, r1, _), (x2, r2, _) = rows[i], rows[i + 1]
        hs.append(neck_h(x1, r1, x2, r2) if r1 > 1 and r2 > 1 else None)
    L = [{"k": "bg", "v": "gradient"}]
    ds = [dark(i, t) for i in range(5)]
    if min(ds) < 0.999:
        L.append(video(o_plate(t), d=row_d(bubs, hs), ghost=False))
        L.append(ghost_layer(row_d(bubs, hs), "fenetres", [(x, AXIS) for x, _, _ in rows]))
        o_parts = [ell(x, rx * u, ry * u) for (x, rx, ry), u in zip(bubs, ds) if u > 0.002]
        for i, h in enumerate(hs):
            g = clamp01((min(ds[i], ds[i + 1]) - 0.9) / 0.1)
            if h is not None and g > 0:
                (x1, rx1, ry1), (x2, rx2, ry2) = bubs[i], bubs[i + 1]
                o_parts.append(neck(x1, min(rx1, ry1), x2, min(rx2, ry2), max(h * g, 1)))
        if o_parts:
            L.append({"k": "fill", "id": "extinction", "fill": ORANGE, "d": " ".join(p for p in o_parts if p),
                      "ghost": False})
        return L
    if t < T_DOT:
        col = mix_hex(ORANGE, WHITE, prog(t, T_DOT - F(1.5), T_DOT))
        L.append({"k": "fill", "id": "rangee", "fill": col, "d": row_d(bubs, hs),
                  "pts": [(x, AXIS) for x, r, _ in rows if r > 1]})
    return L


def dots_layer(t):
    """Le point blanc se divise en deux (cacahuète, col, rupture) et file vers les points du logo."""
    if t < T_DOT:
        return []
    u, v = split(t), travel(t)
    gx = LG["dot_g"][0]
    spread = 30 * u + (CX - gx - 30) * v
    r0 = LG["dot_r"] * 2.0 / math.sqrt(2)
    r = r0 * (1 - v) + LG["dot_r"] * breathe(t, 0.2, 1.1) * v
    x1, x2 = CX - spread, CX + spread
    if u < 0.6:
        d = row_d([(x1, r, r), (x2, r, r)], [r * 0.6 * (1 - u / 0.6) + 0.2 * r])
    else:
        d = ell(x1, r, r) + ell(x2, r, r)
    return [{"k": "fill", "id": "points-logo", "fill": WHITE, "d": d, "pts": [(x1, AXIS), (x2, AXIS)]}]


def outro(t):
    return outro_shapes(t) + endcard(t, T_LOGO, dots=False, extra=dots_layer(t))


# ---- annotations outro
def a_reflux(t):
    return "".join(arrow(x, AXIS + s * 520, x, AXIS + s * 330) for x in (240, 720, 1200, 1680) for s in (-1, 1))


def a_extinction(t):
    return arrow(1860, AXIS - 330, 60, AXIS - 330, dash=True)


def a_rassemble1(t):
    return arrow(40, AXIS + 300, 330, AXIS + 300) + arrow(W - 40, AXIS + 300, W - 330, AXIS + 300)


def a_rassemble2(t):
    return arrow(380, AXIS + 330, 760, AXIS + 330) + arrow(W - 380, AXIS + 330, W - 760, AXIS + 330)


def a_echo(t):
    return "".join(arrow(CX + dx * 360, AXIS + dy * 300, CX + dx * 170, AXIS + dy * 140)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_logo(t):
    return (arrow(CX - 120, AXIS - 120, LG["dot_g"][0] + 10, AXIS - 120)
            + arrow(CX + 120, AXIS - 120, LG["dot_d"][0] - 10, AXIS - 120))


OUTRO = Anim("OUTRO", 4.0, outro, [
    Beat(F(3), "Image 0 : marée inverse. Les rayons retombent de 650 à 190-230 px en 8 images, les bords d'abord ; les festons reviennent.",
         "out_expo", ann=a_reflux, onion=0),
    Beat(F(13), "L'écho s'éteint de droite à gauche : pop de 10 %, puis un disque orange referme chaque fenêtre (4 images, 2 d'écart).",
         "out_expo", ann=a_extinction, onion=0),
    Beat(F(25), "Rassemblement, octave plus bas : les demi-bulles glissent dans leurs voisines (6 images), la droite 2 images après.",
         "in_cubic", ann=a_rassemble1, onion=2, onion_dt=F(2)),
    Beat(F(36), "Puis les latérales glissent dans le centre (3.5-01 à l'envers) ; le centre absorbe leur masse, de 230 à 300 px.",
         "in_cubic", ann=a_rassemble2, onion=2, onion_dt=F(2)),
    Beat(F(41), "Impact : la latérale droite arrive 2 images après la gauche ; la bulle s'écrase à 120 % puis revient au rond sur ressort.",
         "ressort", onion=0),
    Beat(F(50), "L'écho s'éteint : trois rebonds de plus en plus petits, un par demi-temps (300, 200, 124 px), chacun avec un pop.",
         "in_back", ann=a_echo, onion=3, onion_dt=F(3)),
    Beat(F(63), "Le dernier rebond donne un point blanc qui se divise (3.4-01) ; les deux points filent vers le logo, « sfeer » s'ouvre.",
         "emphase", ann=a_logo, onion=0),
    Beat(F(90), "Tenue vivante : points qui respirent (±20 %), arabe révélé de droite à gauche, endossement en bas, poussée de 7,5 %/s.",
         "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Un geste en appelle d'autres : une voix devient un chœur, puis le chœur ouvre le film. C'est la communauté Sfeer.",
        "La forme suit le tempo (120 bpm) : chaque scission tombe sur un temps et monte d'une octave, un audio-logo propre à Sfeer.",
        "Un seul tracé, une seule plaque : la rangée est un cache, elle marche avec n'importe quel film.",
    ]),
    ("Charte et corrections", [
        "Seule la rangée axiale du motif 3.6 : aucune rangée hors axe, aucune bulle à l'aplomb d'une autre.",
        "Demi-bulles coupées pile à x = 0 et 1920 ; centres fixes sur y = 540, même pendant la marée (elle ne fait que gonfler).",
        "Écart à valider : les festons de la marée sortent du cadre en 5 images. Logo seul sur le dégradé, via le carton standard.",
    ]),
    ("Mouvement", [
        "Accroche : la bulle claque à l'image 0 ; bourgeons décalés de 2 images ; impacts écrasés puis ressort.",
        "Arpège : fenêtres allumées de gauche à droite, éteintes de droite à gauche, 2 images d'écart ; marée en ease-in fort.",
        "Outro : rassemblement en deux temps, puis l'écho s'éteint en trois rebonds jusqu'au point du logo.",
    ]),
]
