"""Concept original O2 : « Le Mur Sfeer, le réseau s'ouvre pour toi ».

On découvre la vidéo à travers le motif officiel de bulles jointes (2.46 / 3.6) : un mur en dégradé,
percé de 3 rangées de trous qui respirent en vague. La caméra avance et, comme devant un vrai écran
ajouré, plus on s'approche, moins on voit de trous : le motif se simplifie (19 trous, puis une rangée
de 5, puis une chaîne de 3) et on traverse la chaîne d'un seul mouvement.
Outro : la chaîne revient de hors champ, se remplit d'orange en vague, ses cols cèdent, les deux
bulles latérales se rangent aux bords (2.48) et la bulle centrale s'aspire en point : le logo.

Différences : p03 (pop / masse) et p07 (molécule) sont des formes positives ; ici c'est un mur-écran
percé, la vidéo est DERRIÈRE, vue à travers les trous. Une seule plaque, un seul cache.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, clamp01, ease, prog  # noqa: E402
from blocks import LG, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, f,  # noqa: E402
                       mix_hex)

CX = W / 2
DIAG = math.hypot(W / 2, AXIS)          # 1101,5 : rayon qui couvre les quatre coins

META = {
    "id": "o2_mur",
    "num": "O2",
    "title": "Le Mur Sfeer",
    "principe": "Le motif de bulles est un mur percé : on avance, il se simplifie en chaîne de 3, on la traverse.",
    "logline": "On découvre la vidéo à travers le motif de bulles jointes, percé dans le dégradé. La caméra avance : "
               "19 trous, puis 5, puis 3, et l'on traverse la chaîne. En sortie, la chaîne devient orange et libère le logo.",
}


# =================================================================== géométrie (tracés horaires)
def ell(cx, rx, ry, cy=AXIS):
    """Bulle (cercle ou ellipse d'écrasement), tracée dans le sens horaire comme bridge_d."""
    return (f"M{f(cx - rx)} {f(cy)}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0"
            f"a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z")


def hull(x1, r1, x2, r2, cy=AXIS):
    """Enveloppe convexe de deux cercles (col plein), sens horaire, arcs justes si r1 != r2."""
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, cy - r1 * ny), (x2 + r2 * nx, cy - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, cy + r2 * ny), (x1 + r1 * nx, cy + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def neck(x1, r1, x2, r2, h, cy=AXIS):
    """Col de la charte entre deux cercles d'un même axe ; gère chevauchement et inclusion."""
    if h is None or r1 < 1 or r2 < 1:
        return ""
    if x2 < x1:
        x1, r1, x2, r2 = x2, r2, x1, r1
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        return ""                                   # une bulle avale l'autre : l'ellipse suffit
    rmin = min(r1, r2)
    if d < r1 + r2:                                 # cacahuète : le col ne descend pas sous l'intersection
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        h = max(h, yi + 0.5)
    if h >= rmin - 0.5:
        return hull(x1, r1, x2, r2, cy)
    if _neck_circle((x1, cy, r1), (x2, cy, r2), h) is None:
        # très fort chevauchement : l'union des deux cercles suffit (festons nets, pas d'enveloppe droite)
        return "" if d < r1 + r2 else hull(x1, r1, x2, r2, cy)
    return bridge_d((x1, cy, r1), (x2, cy, r2), h)


def blob(bubs, hs, cy=AXIS):
    """Rangée de bulles [(x, rx, ry)] reliées par des cols hs[i] (None = séparées) : union horaire."""
    parts = [ell(x, rx, ry, cy) for x, rx, ry in bubs if rx > 0.5 and ry > 0.5]
    for i, h in enumerate(hs):
        (x1, rx1, ry1), (x2, rx2, ry2) = bubs[i], bubs[i + 1]
        parts.append(neck(x1, min(rx1, ry1), x2, min(rx2, ry2), h, cy))
    return " ".join(p for p in parts if p)


def bump(t, t0, dur):
    """Bosse 0 -> 1 -> 0 (sinus²) entre t0 et t0 + dur."""
    u = (t - t0) / dur
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def vel(fn, t, dt=0.01):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def ghost_layer(d, lid, pts=None):
    """Calque invisible qui ne sert qu'à la pelure d'oignon et aux trajectoires de la planche."""
    return {"k": "fill", "id": lid, "d": d, "fill": "none", "ghost": True, "pts": pts or []}


# =================================================================== INTRO (3,2 s)
R0 = 120                                   # rayon des trous du mur (unités du mur, avant caméra)
ROW_X = {                                  # rangée de l'axe : 5 trous + 2 demi-trous de bord ;
    0: [160, 480, 800, 1120, 1440, 1760],  # rangées hors axe décalées d'une demi-colonne :
    1: [0, 320, 640, 960, 1280, 1600, 1920],   # aucun trou à l'aplomb d'un trou de l'axe
    2: [160, 480, 800, 1120, 1440, 1760],
}
ROW_Y = {0: 200, 1: AXIS, 2: 880}
T_WAVE = F(16)                             # période de la vague 3.6

# Caméra en trois poussées, chacune précédée d'un recul (anticipation) et finie par un dépassement :
# palier 1 (×1,5 : les trous x = 320 / 1600 tombent pile sur les bords), palier 2 (×2 : chaîne de 3),
# puis la plongée.
cam = Track((0, 1.0), (F(15), 1.06, "linear"),
            (F(18), 1.03, "out_cubic"), (F(26), 1.5, "out_back"), (F(31), 1.5),
            (F(33), 1.47, "out_cubic"), (F(41), 2.0, "out_back"),
            (F(53), 2.12, "inout_cubic"), (F(57), 2.0, "out_cubic"),
            (F(68), 9.0, "plongee"))
T_FULL_EST = F(64)
wave_amp = Track((0, 0.06), (F(5), 0.26, "out_cubic"), (F(26), 0.26), (F(33), 0.12, "inout_cubic"),
                 (F(41), 0.0, "inout_cubic"))
center_k = Track((F(33), 1.0), (F(41), 1.15, "out_back"))        # 3.5-01 : le centre prend le dessus
neck_k = Track((F(17), 0.2), (F(26), 0.22), (F(41), 0.24), (F(53), 0.46, "inout_cubic"),
               (F(57), 0.16, "out_cubic"))                        # les cols s'épaississent, puis se tendent
IMPULSE = {2: F(42), 3: F(45), 4: F(48)}                           # onde qui traverse la chaîne, G -> D


def plate_zoom(t):
    """Plaque verte : zoom bien plus lent que le mur (parallaxe), qui ne s'arrête jamais."""
    return 1 + 0.04 * (cam(t) - 1) + 0.04 * t + 0.12 * max(0.0, t - T_FULL_EST)


def open_k(row, x, t):
    """Perçage : chaque trou s'ouvre avec 10 % de dépassement, du centre vers les bords."""
    ring = abs(x - CX) / 320 + (1.0 if row != 1 else 0.0)
    u = clamp01((t - F(-2 + 1.0 * ring)) / F(6))
    return ease("out_back")(u) if u > 0 else 0.0


def close_k(row, x, t):
    """Rangées hors axe : inspiration (in_back, +10 %) puis fermeture sur place, des bords vers le centre."""
    if row == 1:
        return 1.0
    t0 = F(9 + 0.8 * (2.5 - abs(x - CX) / 320) + (1 if row == 2 else 0))
    return 1 - ease("in_back")(clamp01((t - t0) / F(6)))


def wave(row, i, t):
    """Vague 3.6 : grands et petits trous en damier, onde qui court de gauche à droite.
    Profil « pose à pose » : on tient les extrêmes, l'échange est vif."""
    ph = 2 * math.pi * (t - i * F(2)) / T_WAVE + math.pi * (i % 2) + math.pi * (row % 2)
    s = math.sin(ph)
    return 1 + wave_amp(t) * math.copysign(abs(s) ** 0.6, s)


def pop(t, t0, amp=0.12):
    """Impulsion : +amp en 2 images, puis retour sur ressort avec un petit creux."""
    if t <= t0:
        return 0.0
    if t < t0 + F(2):
        return amp * ease("out_cubic")((t - t0) / F(2))
    u = (t - t0 - F(2)) / F(8)
    return amp * math.exp(-3.5 * u) * math.cos(2.5 * math.pi * u) if u < 1 else 0.0


def smear(X, rr, t):
    """Étirement horizontal d'un trou selon sa vitesse à l'écran (zoom radial), volume conservé."""
    S = cam(t)
    v = abs(X - CX) * abs(vel(cam, t)) / S / 25          # px par image
    return 1 + 0.35 * min(1.0, v / max(2 * rr, 1.0))


def wall_state(t):
    """Rangées du mur en coordonnées image : {row: [(x, rx, ry, y), ...]} (x croissants)."""
    S = cam(t)
    rows = {}
    for ri in (0, 1, 2):
        bubs = []
        for ci, x0 in enumerate(ROW_X[ri]):
            r = R0 * open_k(ri, x0, t) * close_k(ri, x0, t) * wave(ri, ci, t)
            if ri == 1:
                if ci in (1, 5):                          # demi-trous du palier 1 : se ferment en sortant
                    r *= 1 - 0.6 * prog(t, F(33), F(40), "in_cubic")
                if ci == 3:
                    r *= center_k(t)
                if ci in IMPULSE:
                    r *= 1 + pop(t, IMPULSE[ci])
            X = CX + (x0 - CX) * S
            Y = AXIS + (ROW_Y[ri] - AXIS) * S
            rr = max(r, 0.0) * S
            sx = smear(X, rr, t) if ri == 1 else 1.0
            bubs.append((X, rr * sx, rr / sx, Y))
        rows[ri] = bubs
    return rows


def row_path(bubs, t, offaxis=False):
    """Une rangée : les trous s'ouvrent séparés, puis les cols les relient ; rupture nette à la fermeture."""
    k = neck_k(t)
    rref = R0 * cam(t)
    hs = []
    for (x1, rx1, ry1, _), (x2, rx2, ry2, _) in zip(bubs, bubs[1:]):
        rmin = min(rx1, ry1, rx2, ry2)
        joined = rmin > 0.45 * rref if (offaxis or t < F(12)) else rmin > 6
        hs.append(k * rmin if joined else None)
    vis = [(x, rx, ry) for x, rx, ry, _ in bubs]
    return blob(vis, hs, cy=bubs[0][3])


def intro(t):
    rows = wall_state(t)
    center = rows[1][3]
    if min(center[1], center[2]) >= DIAG:              # la fenêtre couvre le cadre : cache retiré
        return [video(plate_zoom(t), ghost=False)]
    mid = [b for b in rows[1] if b[0] + b[1] > -40 and b[0] - b[1] < W + 40]
    d_mid = row_path(mid, t)
    d_off = " ".join(row_path(rows[ri], t, offaxis=True) for ri in (0, 2)
                     if any(b[1] > 0.5 for b in rows[ri]))
    L = [{"k": "bg", "v": "gradient"},
         video(plate_zoom(t), d=(d_mid + " " + d_off).strip(), ghost=False)]
    L.append(ghost_layer(d_mid, "rangee-axe", [(b[0], AXIS) for b in mid if 0 < b[0] < W]))
    if d_off:
        L.append(ghost_layer(d_off, "rangees-hors-axe"))
    return L


# ---- annotations intro
def a_percage(t):
    return (arrow(CX + 170, AXIS, CX + 560, AXIS) + arrow(CX - 170, AXIS, CX - 560, AXIS)
            + arrow(CX + 120, AXIS - 120, CX + 420, AXIS - 300) + arrow(CX - 120, AXIS + 120, CX - 420, AXIS + 300))


def a_vague(t):
    return arrow(140, 40, 1780, 40, dash=True)


def a_ferme(t):
    return "".join(arrow(CX + dx * 640, AXIS + dy * 470, CX + dx * 420, AXIS + dy * 330)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_palier1(t):
    return (arrow(560, AXIS - 300, 140, AXIS - 300) + arrow(W - 560, AXIS - 300, W - 140, AXIS - 300)
            + arrow(560, AXIS + 300, 140, AXIS + 300) + arrow(W - 560, AXIS + 300, W - 140, AXIS + 300))


def a_palier2(t):
    return arrow(300, AXIS - 330, 40, AXIS - 330) + arrow(W - 300, AXIS - 330, W - 40, AXIS - 330)


def a_onde(t):
    return arrow(260, AXIS - 360, 1660, AXIS - 360, dash=True)


def a_recul(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 470, CX + dx * 720, AXIS + dy * 370)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_plongee(t):
    return "".join(arrow(CX + dx * 330, AXIS + dy * 180, CX + dx * 760, AXIS + dy * 420)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 3.2, intro, [
    Beat(F(2), "Image 0 : le mur se perce. 19 trous éclosent du centre vers les bords, 1 image d'écart par anneau, dépassement de 10 %.",
         "out_back", ann=a_percage, onion=0),
    Beat(F(8), "Vague 3.6 : en damier, les trous grandissent ou rétrécissent de 26 %, l'onde court de gauche à droite (2 images par colonne).",
         "inout_cubic", ann=a_vague, onion=0),
    Beat(F(13), "Rangées hors axe : elles gonflent de 10 %, leurs cols cèdent, elles se ferment sur place, des bords vers le centre.",
         "in_back", ann=a_ferme, onion=1, onion_dt=F(3)),
    Beat(F(21), "Poussée 1, après un recul de 3 % : mur ×1 → ×1,5 en 8 images. Les trous s'étirent avec la vitesse (jusqu'à 35 %).",
         "out_back", ann=a_palier1, onion=2, onion_dt=F(2)),
    Beat(F(36), "Poussée 2 : ×1,5 → ×2. Les demi-trous des bords sortent en se fermant, le centre prend 15 % : chaîne de 3 fenêtres.",
         "out_back", ann=a_palier2, onion=2, onion_dt=F(2)),
    Beat(F(48), "Approche : une onde traverse la chaîne de gauche à droite (+12 %, 3 images d'écart), les cols doublent d'épaisseur.",
         "inout_cubic", ann=a_onde, onion=2, onion_dt=F(3)),
    Beat(F(56), "Anticipation : la chaîne recule de 6 % en 4 images et ses cols se tendent (épaisseur ÷3) avant la plongée.",
         "out_cubic", ann=a_recul, onion=2, onion_dt=F(2)),
    Beat(F(62), "Plongée « plongee » ×2 → ×9 : les fenêtres latérales filent aux bords, étirées ; plein cadre à f64, la plaque zoome encore.",
         "plongee", ann=a_plongee, onion=2, onion_dt=F(1)),
])


# =================================================================== OUTRO (4,0 s)
APPROACH = ((330, 240), (960, 360), (1590, 240))      # format de la traversée
CARD = ((620, 150), (960, 170), (1300, 150))          # format carton
o_cam = Track((0, 3.4), (F(13), 1.0, "out_expo"))
o_fmt = Track((F(5), 0), (F(20), 1, "inout_cubic"))
# remplissage orange en vague, de gauche à droite (2 images d'écart)
FILL_T = (F(14), F(16), F(18))
T_FILL_END = F(28)
# tension, rupture des cols (gauche puis droite, 3 images d'écart), recul vers les bords
pull_l = Track((F(27), 0), (F(30), -12, "out_cubic"), (F(34), 64, "in_cubic"))
pull_r = Track((F(30), 0), (F(33), -12, "out_cubic"), (F(37), 64, "in_cubic"))
T_SNAP_L, T_SNAP_R = F(34), F(37)
fly_l = Track((T_SNAP_L, 0), (F(44), 1, "out_back"))
fly_r = Track((T_SNAP_R, 0), (F(47), 1, "out_back"))
EDGE_R = 230
# aspiration du centre en point blanc, puis scission en points du logo (3.4-01 -> 3.4-02)
T_DOT = F(49)
c_r = Track((F(38), 170), (F(42), 184, "out_cubic"), (T_DOT, LG["dot_r"] * 2.0, "in_expo"))
split = Track((F(50), 0.0), (F(55), 1.0, "out_cubic"))
travel = Track((F(52), 0.0), (F(61), 1.0, "emphase"))
T_LOGO = F(54)


def o_plate(t):
    return 1.0 + 0.12 * prog(t, 0, F(30), "out_cubic") + 0.1 * t


def chain_now(t):
    """(x, r) des trois bulles, caméra comprise."""
    u, S = o_fmt(t), o_cam(t)
    out = []
    for (xa, ra), (xc, rc) in zip(APPROACH, CARD):
        x = xa + (xc - xa) * u
        r = (ra + (rc - ra) * u) * card_breath(len(out), t)
        out.append((CX + (x - CX) * S, r * S))
    return out


def fill_u(i, t):
    return ease("out_cubic")(clamp01((t - FILL_T[i]) / F(7)))


def card_breath(i, t):
    """Chaîne orange vivante : la bulle centrale gonfle quand les côtés se creusent (3.5-01)."""
    a = 0.035 * prog(t, F(12), F(20)) * math.sin(2 * math.pi * (t - F(12)) / 0.64 - (0.6 if i == 0 else 1.2 if i == 2 else 0))
    return 1 + (a if i == 1 else -a)


def edge_x(side, t):
    """Bulle latérale après la rupture : file vers le bord et s'y coupe pile sur sa médiane."""
    if side == "g":
        x0 = CARD[0][0] - pull_l(T_SNAP_L)
        return x0 + (0 - x0) * fly_l(t)
    x0 = CARD[2][0] + pull_r(T_SNAP_R)
    return x0 + (W - x0) * fly_r(t)


def edge_r(side, t):
    fl = fly_l(t) if side == "g" else fly_r(t)
    base = 150 + (EDGE_R - 150) * clamp01(fl)
    # tenue vivante : les deux demi-bulles échangent leur taille (3.3-02), en opposition
    live = prog(t, F(46), F(58))
    return base * (1 + live * 0.08 * math.sin(2 * math.pi * (t - F(46)) / 1.4 + (0 if side == "g" else math.pi)))


def outro_shapes(t):
    L = []
    if t < T_FILL_END:
        ch = chain_now(t)
        hs = [0.24 * min(ch[0][1], ch[1][1]), 0.24 * min(ch[1][1], ch[2][1])]
        d_win = blob([(x, r, r) for x, r in ch], hs)
        if ch[1][1] >= DIAG:
            L.append(video(o_plate(t), ghost=False))
        else:
            L.append({"k": "bg", "v": "gradient"})
            L.append(video(o_plate(t), d=d_win, ghost=False))
            L.append(ghost_layer(d_win, "chaine", [(x, AXIS) for x, _ in ch]))
        # disques orange qui balaient chaque fenêtre de gauche à droite (tangents à son bord gauche)
        parts, us = [], []
        for i, (x, r) in enumerate(ch):
            u = fill_u(i, t)
            us.append(u)
            if u > 0.002:
                rho = r * u + 3 * u ** 4          # +3 px à la fin : l'orange recouvre le bord de la fenêtre
                parts.append(ell(x - r + rho, rho, rho))
        for i in range(2):
            if min(us[i], us[i + 1]) > 0.85:
                g = clamp01((min(us[i], us[i + 1]) - 0.85) / 0.15)
                (x1, r1), (x2, r2) = ch[i], ch[i + 1]
                parts.append(neck(x1, r1 + 3, x2, r2 + 3, max(g * (hs[i] + 3), 1)))
        if parts:
            L.append({"k": "fill", "id": "remplissage", "fill": ORANGE, "d": " ".join(parts), "ghost": False})
        return L

    L.append({"k": "bg", "v": "gradient"})
    # chaîne orange au format carton, puis tension et rupture des cols
    xc = CX
    rc = c_r(t) if t >= F(38) else 170 * card_breath(1, t)
    sq = squash(t, T_SNAP_L, F(8), 0.16) * squash(t, T_SNAP_R, F(8), -0.12) * squash(t, T_DOT, F(8), 0.3)
    col = mix_hex(ORANGE, WHITE, prog(t, T_DOT - F(2), T_DOT))
    side_d, pts = [], []
    for side in ("g", "d"):
        snapped = t >= (T_SNAP_L if side == "g" else T_SNAP_R)
        if not snapped:
            pull = pull_l(t) if side == "g" else pull_r(t)
            x = CARD[0][0] - pull if side == "g" else CARD[2][0] + pull
            r = 150 * card_breath(0 if side == "g" else 2, t)
            h = 0.24 * 150 * max(0.0, 1 - max(pull, 0) / 52) ** 1.2
            cb = (xc, rc * sq, rc / sq)
            pair = [(x, r, r), cb] if side == "g" else [cb, (x, r, r)]
            side_d.append(blob(pair, [h if h > 3 else None]))
        else:
            x, r = edge_x(side, t), edge_r(side, t)
            sx = squash(t, F(44) if side == "g" else F(47), F(8), 0.14)
            side_d.append(ell(x, r * sx, r / sx))
        pts.append((x, AXIS))
    L.append({"k": "fill", "id": "bulles-bord", "fill": ORANGE, "d": " ".join(side_d), "pts": pts})
    if t < F(50):
        L.append({"k": "fill", "id": "centre", "fill": col, "d": ell(xc, rc * sq, rc / sq), "ghost": t > F(37)})
    return L


def dots_layer(t):
    """Le point blanc se divise en deux (cacahuète, col, rupture) et file vers les points du logo."""
    if t < F(50):
        return []
    u, v = split(t), travel(t)
    gx = LG["dot_g"][0]
    spread = 30 * u + (CX - gx - 30) * v
    r0 = LG["dot_r"] * 2.0 / math.sqrt(2)
    r = r0 * (1 - v) + LG["dot_r"] * breathe(t, 0.2, 1.1) * v
    x1, x2 = CX - spread, CX + spread
    if u < 0.6:
        d = blob([(x1, r, r), (x2, r, r)], [r * 0.6 * (1 - u / 0.6) + 0.2 * r])
    else:
        d = ell(x1, r, r) + ell(x2, r, r)
    return [{"k": "fill", "id": "points-logo", "fill": WHITE, "d": d, "pts": [(x1, AXIS), (x2, AXIS)]}]


def outro(t):
    return outro_shapes(t) + endcard(t, T_LOGO, dots=False, extra=dots_layer(t))


# ---- annotations outro
def a_retour(t):
    return (arrow(40, AXIS + 330, 300, AXIS + 330) + arrow(W - 40, AXIS + 330, W - 300, AXIS + 330)
            + "".join(arrow(CX + dx * 900, AXIS + dy * 500, CX + dx * 650, AXIS + dy * 360)
                      for dx in (-1, 1) for dy in (-1, 1)))


def a_balayage(t):
    return arrow(420, AXIS - 230, 1500, AXIS - 230, dash=True)


def a_tension(t):
    return arrow(520, AXIS - 210, 380, AXIS - 210) + arrow(W - 520, AXIS - 210, W - 380, AXIS - 210)


def a_rupture(t):
    return arrow(420, AXIS + 220, 130, AXIS + 220) + arrow(W - 420, AXIS + 220, W - 130, AXIS + 220)


def a_aspire(t):
    return "".join(arrow(CX + dx * 330, AXIS + dy * 250, CX + dx * 90, AXIS + dy * 70)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_logo(t):
    return (arrow(CX - 120, AXIS - 120, LG["dot_g"][0] + 10, AXIS - 120)
            + arrow(CX + 120, AXIS - 120, LG["dot_d"][0] - 10, AXIS - 120))


OUTRO = Anim("OUTRO", 4.0, outro, [
    Beat(F(3), "Image 0 en mouvement : la caméra recule (×3,4 → ×1 en 13 images), la chaîne rentre par les bords ; la plaque, elle, zoome.",
         "out_expo", ann=a_retour, onion=2, onion_dt=F(1)),
    Beat(F(12), "La chaîne se resserre au format carton : 3 fenêtres sur l'axe, centre 170 px, côtés 150 px, cols de 72 px.",
         "inout_cubic", onion=2, onion_dt=F(3)),
    Beat(F(19), "Balayage orange de gauche à droite : chaque fenêtre se remplit en 7 images, 2 images d'écart ; les cols suivent.",
         "out_cubic", ann=a_balayage, onion=0),
    Beat(F(33), "Tension : les bulles latérales reculent de 12 px (anticipation) puis tirent vers les bords ; le col gauche s'affine.",
         "in_cubic", ann=a_tension, onion=2, onion_dt=F(2)),
    Beat(F(39), "Rupture nette, gauche puis droite (3 images d'écart) : les deux moitiés filent aux bords et se coupent sur leur médiane.",
         "out_back", ann=a_rupture, onion=2, onion_dt=F(2)),
    Beat(F(47), "Aspiration : le centre gonfle de 8 % puis s'effondre en point blanc (in_expo, 7 images) et s'écrase à l'impact.",
         "in_expo", ann=a_aspire, onion=2, onion_dt=F(2)),
    Beat(F(58), "Le point se divise (3.4-01) : cacahuète, col, rupture ; les deux points filent vers le logo, « sfeer » s'ouvre.",
         "emphase", ann=a_logo, onion=0),
    Beat(F(86), "Tenue vivante : demi-bulles des bords qui échangent leur taille (±8 %), points qui respirent, poussée de 7,5 %/s.",
         "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Plus on s'approche d'un écran ajouré, moins on voit de trous : la forme se simplifie, rien ne s'ouvre comme un store.",
        "Chaque étape est une figure de la charte : motif 2.46 / 3.6, chaîne de 3 (3.5-01), demi-bulles de bord (2.48), logo (3.4).",
        "Une seule plaque derrière un seul cache : ça marche avec n'importe quel film, sans point d'ancrage à trouver.",
    ]),
    ("Charte et corrections", [
        "Écart à valider : rangées hors axe visibles 18 images (tenue de 8), décalées d'une demi-colonne : aucun trou à l'aplomb d'un trou de l'axe.",
        "Trous centrés sur y = 540 ; demi-trous de bord coupés pile à x = 0 et 1920 ; on traverse la chaîne entière, jamais un cercle seul.",
        "Logo seul, au centre, via le carton standard : les bulles orange se rangent aux bords et ne le touchent jamais.",
    ]),
    ("Mouvement", [
        "Accroche : perçage en cascade dès l'image 0 ; vague 3.6 décalée de 2 images par colonne ; fusions décalées de 3 images.",
        "Recul de 4 % avant la plongée (anticipation) ; plongée en « plongee » ; plaque 30 fois plus lente que le mur (parallaxe).",
        "Outro : cols qui cèdent en deux temps, recul aux bords sur ressort, aspiration du centre en point blanc, puis logo.",
    ]),
]
