"""Concept original « Le Point : du logo au vertige ».

Le logo se replie en un point (3.3-01 / 3.4-02 à rebours). Le point se divise en une grande bulle
orange et une petite fenêtre (3.4-01). Elles échangent leur taille (3.3-02) en TRAVELLING COMPENSÉ
façon Vertigo : la fenêtre grandit pendant que l'image dedans recule (la plaque dézoome, centrée
sur la fenêtre). Puis la fenêtre jaillit hors cadre et le point, toujours attaché, nous pousse
dans le film. L'outro rejoue le geste à l'envers jusqu'au logo.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, back_in, back_out, bezier, breathe, prog  # noqa: E402
from blocks import LG, arabic, endcard, squash, video, word  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, arrow, bridge_d, ellipse_d, f,  # noqa: E402
                       label, mix_hex, waist_h)

CX = W / 2
DOT_R = LG["dot_r"]
HALF = (LG["dot_d"][0] - LG["dot_g"][0]) / 2      # demi-écart des points du logo
R_ONE = DOT_R * math.sqrt(2)                       # point unique : même surface que les deux points
BACK6 = back_out(1.25)                             # dépassement ≈ 6 %
SWAP = bezier(0.65, 0, 0.35, 1)                    # échange de tailles (charte 3.3-02)
JUMP = bezier(0.7, 0, 0.84, 0)                     # saut : accélération pure
BACK_IN4 = back_in(1.0)                            # anticipation ≈ 4 %

META = {
    "id": "o3_point_vertigo",
    "num": "O3",
    "title": "Le Point, du logo au vertige",
    "logline": "Le point du logo se divise en une bulle orange et une petite fenêtre. Elles échangent leur taille en travelling "
               "compensé façon Vertigo : la fenêtre avance, l'image recule. Puis le point nous pousse dans le film.",
}


# ================================================================= OUTILS DE FORME
_TOK = re.compile(r"[MLAaZz]|-?\d*\.?\d+")


def stretch_d(d, sx, sy, cx=CX, cy=AXIS):
    """Étire un tracé (M, L, A, a, Z) autour de (cx, cy). Un arc de cercle devient un arc d'ellipse."""
    if abs(sx - 1) < 1e-4 and abs(sy - 1) < 1e-4:
        return d
    tok = _TOK.findall(d)
    out, i, cmd = [], 0, None
    while i < len(tok):
        t = tok[i]
        if t in "MLAaZz":
            cmd = t
            out.append(t)
            i += 1
            continue
        if cmd in ("M", "L"):
            x, y = float(tok[i]), float(tok[i + 1])
            out.append(f"{f(cx + (x - cx) * sx)} {f(cy + (y - cy) * sy)}")
            i += 2
        elif cmd in ("A", "a"):
            rx, ry, rot, la, sw, x, y = tok[i:i + 7]
            if cmd == "A":
                x, y = f(cx + (float(x) - cx) * sx), f(cy + (float(y) - cy) * sy)
            else:
                x, y = f(float(x) * sx), f(float(y) * sy)
            out.append(f"{f(float(rx) * sx)} {f(float(ry) * sy)} {rot} {la} {sw} {x} {y}")
            i += 7
        else:
            i += 1
    return " ".join(out)


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
        return circ(*(c1 if r1 >= r2 else c2))
    if h is None:
        return circ(x1, r1) + circ(x2, r2)
    if x2 - x1 < r1 + r2:
        h = max(h, waist_h(a, b, 0.2))
    return bridge_d(a, b, min(h, 0.95 * min(r1, r2)))


def squashed(d, sx):
    """Écrasement / étirement horizontal d'un groupe de bulles, centres conservés (tracé en espace « pré-étiré »)."""
    return d if abs(sx - 1) < 1e-3 else stretch_d(d, sx, 1 / sx)


def pre(x, sx):
    return CX + (x - CX) / sx


def vel(fn, t):
    return (fn(t + 0.02) - fn(t - 0.02)) / 0.04 / 25


def window_layers(xw, rw, sx, zoom, gid="fenetre"):
    """Fenêtre verte : la plaque est zoomée autour du CENTRE de la fenêtre (travelling compensé)."""
    if rw < 0.5:
        return []
    if rw * min(sx, 1 / sx) > 1110:
        return [video(zoom, None, ghost=False)]
    d = ellipse_d(CX, AXIS, rw * sx, rw / sx)
    return [{"k": "group", "s": 1, "dx": xw - CX, "layers": [video(zoom, d, vid=gid, ghost=False)]},
            {"k": "fill", "id": f"{gid}-repere", "fill": "none", "d": ellipse_d(xw, AXIS, rw * sx, rw / sx),
             "pts": [(xw, AXIS)], "ghost": rw < 1000}]


# ================================================================= INTRO (4,0 s)
T_MERGE = F(11)
word_rev = Track((F(2), 1), (F(10), 0, "in_cubic"))
ar_rev = Track((0, 1), (F(6), 0, "in_cubic"))
dots_dx = Track((F(1), HALF), (F(4), HALF + 12, "out_cubic"), (T_MERGE, 0, "in_cubic"))
one_r = Track((T_MERGE, R_ONE), (F(13), 21, "out_back"), (F(15), 13, "inout_cubic"))

# division (3.4-01), anticipation, échange de tailles (3.3-02) en travelling compensé, visée, recul, saut
T_SPLIT, T_SWAP0, T_SWAP1, T_AIM, T_REC, T_JUMP = F(15), F(26), F(49), F(56), F(59), F(67)
xW = Track((T_SPLIT, CX), (F(23), 1210, BACK6), (T_SWAP0, 1236, "out_cubic"),
           (T_SWAP1, 1050, SWAP), (T_AIM, CX, "inout_cubic"))
rW = Track((T_SPLIT + F(1), 0), (F(23), 110, BACK6), (T_SWAP0, 102, "out_cubic"),
           (T_SWAP1, 345, SWAP), (T_AIM, 420, "inout_cubic"),
           (T_REC, 402, "in_cubic"), (T_JUMP, 1120, JUMP))
rO = Track((T_SPLIT, 13), (F(22), 300, BACK6), (T_SWAP0, 306, "out_cubic"),
           (T_SWAP1, 104, SWAP), (T_AIM, 140, "inout_cubic"),
           (T_REC, 132, "in_cubic"), (T_JUMP, 260, JUMP))
gap = Track((T_SPLIT, -13), (F(22), 20, "out_cubic"), (T_SWAP1, 20), (T_AIM, 25, "linear"))
# plaque dans la fenêtre : 162 % -> 100 % pendant que la fenêtre grandit (l'image recule), puis poussée
_zoom = Track((T_SPLIT, 1.66), (T_SWAP0, 1.62, "linear"), (T_SWAP1, 1.0, SWAP), (T_REC, 1.04, "linear"),
              (T_JUMP, 1.15, JUMP), (F(80), 1.27, "out_cubic"))


def alive(t, t0, t1, phase=0.0):
    """Respiration douce des deux bulles pendant les tenues (jamais figées)."""
    w = prog(t, t0, t0 + F(3)) * (1 - prog(t, t1 - F(3), t1))
    return 1 + 0.03 * w * math.sin(2 * math.pi * (t / 0.72 + phase))


def zoom_in(t):
    return _zoom(t) + 0.3 * max(0.0, t - T_JUMP)


def xO(t):
    """Le point reste collé à la fenêtre : son centre se déduit du bord gauche de la fenêtre."""
    return xW(t) - rW(t) - gap(t) - rO(t)


def pair_sx(t, part="intro"):
    """Écrasement de la paire aux impacts (fin de division, fin d'échange)."""
    if part == "intro":
        return 1 / squash(t, F(22), F(8), 0.1) / squash(t, T_SWAP1, F(8), 0.05)
    return 1 / squash(t, T_BACK, F(8), 0.12) / squash(t, T_U1, F(8), 0.05)


def logo_fold(t):
    """Le logo se replie : le mot se referme au centre, les deux points se précipitent et fusionnent."""
    L = []
    if t < F(10):
        L += word(word_rev(t)) + arabic(ar_rev(t))
    if t < T_MERGE:
        dx = dots_dx(t)
        r = DOT_R * (breathe(t, 0.2, 1.1) if t < F(2) else 1)
        rm = DOT_R + (R_ONE - DOT_R) * prog(t, F(9), T_MERGE)
        r = rm if t > F(9) else r
        h = None if 2 * dx - 2 * r > 26 else max(1.2, r * 0.5 * (1 - (2 * dx - 2 * r) / 26))
        L.append({"k": "fill", "id": "points-logo", "fill": WHITE, "d": pair_d((CX - dx, r), (CX + dx, r), h),
                  "pts": [(CX - dx, AXIS), (CX + dx, AXIS)]})
    elif t < T_SPLIT:
        sq = 1 / squash(t, T_MERGE, F(6), 0.3)
        r = one_r(t)
        L.append({"k": "fill", "id": "point", "fill": WHITE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
    return L


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    L += logo_fold(t)
    if t < T_SPLIT:
        return L
    xw, rw, ro, xo = xW(t), rW(t), rO(t), xO(t)
    rw *= alive(t, F(22), T_REC, 0.5)
    ro *= alive(t, F(22), T_REC)
    sx = pair_sx(t)
    # le point est projeté à gauche pendant le saut : étirement dans le sens de la vitesse
    so = 1 + min(0.3, abs(vel(xO, t)) / 160) if t > T_REC else 1.0
    col = mix_hex(WHITE, ORANGE, prog(t, T_SPLIT, T_SPLIT + F(2)))
    h = 27.5 + 2.5 * prog(t, T_SWAP0, T_SWAP1) - 2.5 * prog(t, T_SWAP1, T_AIM)
    # point projeté : le cou s'accroche à un cercle intérieur (r / so), l'ellipse étirée le recouvre
    d = squashed(pair_d((pre(xo, sx), ro / so), (pre(xw, sx), rw), h), sx)
    L.append({"k": "fill", "id": "point-fenetre", "fill": col, "d": d, "pts": [(xo, AXIS)], "ghost": so < 1.01})
    if so > 1.01:
        L.append({"k": "fill", "id": "point-etire", "fill": col, "d": ellipse_d(xo, AXIS, ro * so, ro / so)})
    g = prog(t, T_SPLIT + F(2), T_SPLIT + F(6), "out_cubic")
    L += window_layers(xw, rw * g, sx, zoom_in(t))
    return L


# ----------------------------------------------------------------- annotations
def vertigo_ann(xw, rw, inward_label="l'image recule", outward_label="la fenêtre avance", inverse=False):
    out = []
    for a in (-2.4, -0.75, 0.75, 2.4):
        ca, sa = math.cos(a), math.sin(a)
        p_out = ((xw + 0.92 * rw * ca, AXIS + 0.92 * rw * sa), (xw + 1.22 * rw * ca, AXIS + 1.22 * rw * sa))
        p_in = ((xw + 0.62 * rw * ca, AXIS + 0.62 * rw * sa), (xw + 0.34 * rw * ca, AXIS + 0.34 * rw * sa))
        if inverse:
            p_out = (p_out[1], p_out[0])
            p_in = (p_in[1], p_in[0])
        out.append(arrow(*p_out[0], *p_out[1], head=30))
        out.append(arrow(*p_in[0], *p_in[1], head=24, w=6, dash=True))
    out.append(label(xw, AXIS - rw * 1.22 - 24, outward_label, 52, anchor="middle"))
    out.append(label(xw, AXIS + rw * 1.22 + 64, inward_label, 52, anchor="middle"))
    return "".join(out)


def a_repli(t):
    return arrow(330, 400, 720, 400) + arrow(1590, 400, 1200, 400) + label(CX, 330, "le mot se referme, les points foncent", 54, anchor="middle")


def a_division(t):
    return arrow(CX - 120, 300, CX - 420, 300) + arrow(CX + 120, 300, CX + 330, 300)


def a_vertigo(t):
    return vertigo_ann(xW(t), rW(t))


def a_saut(t):
    return ("".join(arrow(CX + dx * 560, AXIS + dy * 300, CX + dx * 900, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1))
            + arrow(260, AXIS, 40, AXIS))


INTRO = Anim("INTRO", 3.6, intro, [
    Beat(F(6), "Le logo se replie : « sfeer » se referme au centre en 8 images ; les points reculent de 12 px puis foncent l'un vers l'autre.", "in_cubic", ann=a_repli, onion=2, onion_dt=F(2)),
    Beat(F(12), "Ils fusionnent (charte 3.3-01) en un seul point blanc, écrasé à 77 % au choc, qui rebondit puis se contracte : il va se diviser.", "out_back", onion=0),
    Beat(F(18), "Division (3.4-01) : une bulle orange ×23 part à gauche, une petite fenêtre naît à droite. La vidéo s'y allume en 4 images.", "out_back", ann=a_division, onion=2, onion_dt=F(2)),
    Beat(F(25), "Contre-mouvement : la paire recule de 26 px vers la droite, la fenêtre rétrécit de 7 %. Rapport des tailles 3:1.", "out_cubic", onion=1, onion_dt=F(3)),
    Beat(F(39), "Travelling compensé (3.3-02) : la fenêtre grandit ×3,4 pendant que la plaque dézoome de 160 à 100 %. Vertige.", "inout_cubic", ann=a_vertigo, onion=2, onion_dt=F(4)),
    Beat(F(55), "Visée : la fenêtre se recentre (r 420) ; le point, poussé à gauche, la retient par un cou de 50 px.", "out_cubic", onion=2, onion_dt=F(3)),
    Beat(F(64), "Saut en 8 images : la fenêtre jaillit ×2,8 hors cadre, le point est projeté à gauche, étiré à 130 %, coupé sur sa médiane.", "in_expo", ann=a_saut, onion=2, onion_dt=F(2)),
    Beat(F(80), "Plein cadre : la poussée continue dans le plan (115 → 127 %, puis dérive) ; on raccorde en mouvement.", "out_cubic", onion=0),
])


# ================================================================= OUTRO (4,0 s)
T_BACK, T_U0, T_U1, T_J0, T_J1, T_DOT, T_LOGO = F(11), F(13), F(29), F(31), F(40), F(44), F(46)
oxW = Track((T_BACK, CX), (T_U0, 946, "out_cubic"), (T_U1, 1222, SWAP), (T_J0, 1210, "out_cubic"),
            (T_J1, CX, BACK_IN4))
orW = Track((F(2), 1150), (T_BACK, 420, "out_expo"), (T_U0, 436, "out_cubic"), (T_U1, 104, SWAP),
            (T_J0, 110, "out_cubic"), (T_J1, 0, BACK_IN4))
orO = Track((F(2), 260), (T_BACK, 140, "out_expo"), (T_U0, 130, "out_cubic"), (T_U1, 318, SWAP),
            (T_J0, 300, "out_cubic"), (T_J1, R_ONE, BACK_IN4))
ogap = Track((T_BACK, 25), (T_U1, 20, "linear"), (T_J0, 20), (T_J1, -R_ONE, BACK_IN4))
_ozoom = Track((0, 1.26), (F(2), 1.22, "linear"), (T_BACK, 1.04, "out_expo"), (T_U1, 1.6, SWAP), (T_J0, 1.66, "linear"))
orange_close = Track((F(25), 0), (F(29), 1, "out_cubic"))
dot_r = Track((T_J1, R_ONE), (F(42), 20, "out_back"), (T_DOT, 14, "inout_cubic"))
split_dx = Track((T_DOT, 0), (F(46), 16, "out_cubic"), (F(52), HALF, BACK6))


def oxO(t):
    return oxW(t) - orW(t) - ogap(t) - orO(t)


def outro_shapes(t):
    L = []
    rw = orW(t)
    if rw > 1110:
        L.append(video(_ozoom(t), None, ghost=False))
        return L
    L.append({"k": "bg", "v": "gradient"})
    if t < T_J1:
        xw, ro, xo = oxW(t), orO(t), oxO(t)
        sx = pair_sx(t, "outro")
        so = 1 + min(0.3, abs(vel(oxO, t)) / 160) if t < T_BACK else 1.0
        col = mix_hex(ORANGE, WHITE, prog(t, T_J1 - F(2), T_J1))
        d = squashed(pair_d((pre(xo, sx), ro / so), (pre(xw, sx), rw), 27.5), sx)
        L.append({"k": "fill", "id": "point-fenetre", "fill": col, "d": d, "pts": [(xo, AXIS), (xw, AXIS)], "ghost": so < 1.01})
        if so > 1.01 and xo + ro * so > 0:
            L.append({"k": "fill", "id": "point-etire", "fill": col, "d": ellipse_d(xo, AXIS, ro * so, ro / so)})
        o = orange_close(t)
        if o < 1:
            L += window_layers(xw, rw, sx, _ozoom(t))
            if o > 0:   # iris orange qui referme la fenêtre (forme, pas de fondu)
                L.append({"k": "fill", "id": "iris", "fill": ORANGE, "d": ellipse_d(xw, AXIS, rw * o * sx, rw * o / sx), "ghost": False})
    elif t < T_DOT:
        sq = 1 / squash(t, T_J1, F(6), 0.3)
        r = dot_r(t)
        L.append({"k": "fill", "id": "point", "fill": WHITE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
    return L


def logo_points(t):
    """3.4-02 : le point se divise ; les deux points filent à leur place et respirent."""
    if t < T_DOT:
        return []
    dx = split_dx(t)
    u = prog(t, T_DOT, F(49))
    r = 14 + (DOT_R - 14) * u
    if t > F(52):
        out = []
        for i, s in enumerate((-1, 1)):
            rr = DOT_R * breathe(t, 0.2, 1.1, phase=0.25 * i)
            out.append({"k": "fill", "id": f"logo-point-{'gd'[i]}", "fill": WHITE, "d": circ(CX + s * dx, rr)})
        return out
    h = None if 2 * dx - 2 * r > 18 else max(1.0, r * 0.45 * (1 - (2 * dx - 2 * r) / 18))
    return [{"k": "fill", "id": "points-logo", "fill": WHITE, "d": pair_d((CX - dx, r), (CX + dx, r), h),
             "pts": [(CX - dx, AXIS), (CX + dx, AXIS)]}]


def outro_full(t):
    return outro_shapes(t) + endcard(t, T_LOGO, dots=False, extra=logo_points(t))


def a_aspire(t):
    return ("".join(arrow(CX + dx * 900, AXIS + dy * 480, CX + dx * 560, AXIS + dy * 300) for dx in (-1, 1) for dy in (-1, 1))
            + arrow(40, AXIS + 330, 300, AXIS + 330))


def a_vertigo_inv(t):
    return vertigo_ann(oxW(t), orW(t), "l'image avance", "la fenêtre recule", inverse=True)


def a_fusion(t):
    return arrow(380, 330, 760, 330) + arrow(1560, 330, 1180, 330)


def a_logo(t):
    return arrow(CX - 40, 400, CX - 230, 400) + arrow(CX + 40, 400, CX + 230, 400)


OUTRO = Anim("OUTRO", 3.6, outro_full, [
    Beat(F(6), "Le plan recule dans la fenêtre (r 1150 → 420, out_expo) ; le point rentre par la gauche, déjà attaché, étiré à 130 %.", "out_expo", ann=a_aspire, onion=2, onion_dt=F(2)),
    Beat(F(12), "Impact : le point s'écrase à 84 % ; la fenêtre inspire (+3 %) et glisse de 12 px à gauche avant l'échange.", "out_cubic", onion=2, onion_dt=F(2)),
    Beat(F(21), "Travelling compensé inversé : la fenêtre rétrécit ×4 pendant que la plaque rezoome de 104 à 160 % ; le point regrossit.", "inout_cubic", ann=a_vertigo_inv, onion=2, onion_dt=F(4)),
    Beat(F(28), "Un iris orange referme la vidéo en 5 images : on retrouve la paire de la charte 3.4-01, rapport 3:1.", "out_cubic", onion=0),
    Beat(F(37), "Réunion et contraction en même temps (anticipation 4 %) : jamais de grand disque seul au centre.", "in_back", ann=a_fusion, onion=2, onion_dt=F(2)),
    Beat(F(41), "Il ne reste qu'un point blanc : écrasé à 77 % à l'impact, il rebondit (×1,3) puis se contracte.", "out_back", onion=0),
    Beat(F(49), "3.4-02 : le point se divise, le cou casse, les points filent à leur place (dépassement 6 %) ; « sfeer » s'ouvre au centre.", "out_back", ann=a_logo, onion=2, onion_dt=F(2)),
    Beat(F(82), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; l'arabe s'est écrit de droite à gauche.", "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Pour un programme de fidélité, le point du logo est littéralement un point : il se dépense et devient une expérience.",
        "L'échange de tailles de la charte, joué en travelling compensé : la figure la plus célèbre du cinéma, avec deux bulles plates.",
        "Le dispositif naît du logo et y revient : l'outro finit sur la première image de l'intro, la boucle est parfaite.",
    ]),
    ("Charte et corrections", [
        "Comportements cités tels quels : 3.3-01 (réunion), 3.4-01 (division), 3.3-02 (échange de tailles), 3.4-02 (logo).",
        "Rapport des tailles ≤ 3:1, le point ne descend jamais sous r 104 ; tout reste sur l'axe y = 540, sortie du point à gauche.",
        "Pas de fondu : un iris orange referme la vidéo. Écart à valider : la bascule blanc ↔ orange du point (2 images).",
    ]),
    ("Mouvement", [
        "Le vertige : la fenêtre ×3,4 pendant que la plaque, centrée sur elle, dézoome de 160 à 100 % (et l'inverse en outro).",
        "Anticipations de 3 à 4 images avant chaque geste, dépassements de 6 %, écrasements aux impacts ; saut en 8 images in_expo.",
        "AE : deux cercles et un cou, nombre de sommets constant ; plaque parentée au centre de la fenêtre. Natif en Lottie.",
    ]),
]
