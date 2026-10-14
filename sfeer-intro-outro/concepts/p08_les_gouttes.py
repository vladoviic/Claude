"""Piste 8 (croquis de la DA) : « les gouttes ».

Chaque goutte est un point gagné. Elles arrivent une à une, le long de l'axe, comme des perles qui
glissent sur un fil : la première éclot au centre, les suivantes partent des bords (coupées à leur
milieu vertical), en alternance gauche / droite. Chaque arrivée est un choc : la goutte s'écrase
contre la chaîne, rebondit et tire un col (charte 3.5). Une onde de taille parcourt la chaîne (3.6).
La dernière goutte déclenche tout : la bulle du centre avale la chaîne, garde deux petites bosses,
s'ouvre sur la vidéo et l'on plonge. L'outro rétracte la vidéo en bulle à bosses, qui expulse trois
gouttes en cascade ; elles se resserrent et deux deviennent les points du logo.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, bezier, breathe, lerp, prog, render_layers  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import AXIS, ORANGE, WHITE, W, arrow, bridge_d, f, mix_hex  # noqa: E402

CX, CY = W / 2, AXIS
TAU = 2 * math.pi
GLISSE = bezier(0.5, 0, 0.75, 0.5)      # la goutte accélère sur le fil et arrive encore vite : choc

META = {
    "id": "p08_les_gouttes",
    "num": "P8",
    "title": "Les gouttes",
    "logline": "Piste 8 de la DA. Chaque goutte est un point gagné : elles glissent sur l'axe, s'écrasent et se lient en chaîne ; "
               "la bulle du centre avale tout, s'ouvre sur la vidéo et l'on plonge. En outro, elle recrache trois gouttes.",
}


# =============================================================== géométrie (helpers locaux)
def circle_cw(cx, cy, r):
    """Cercle tracé dans le sens horaire, comme bridge_d : les unions de sous-tracés ne font pas de trous."""
    return f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_d(cx, cy, rx, ry):
    """Goutte étirée ou écrasée sur l'axe (sens horaire)."""
    return (f"M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 1 {f(cx + rx)} {f(cy)}"
            f"A{f(rx)} {f(ry)} 0 1 1 {f(cx - rx)} {f(cy)}Z")


_TOK = re.compile(r"[MLAZaz]|-?\d+(?:\.\d+)?")


def scale_d(d, ox, oy, sx, sy):
    """Écrasement / étirement d'un tracé de cercles et de cols autour de (ox, oy), volume conservé par l'appelant."""
    toks = _TOK.findall(d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        tk = toks[i]
        if tk.isalpha():
            cmd = tk
            i += 1
            if cmd in "Zz":
                out.append("Z")
            continue
        if cmd in ("M", "L"):
            x, y = float(toks[i]), float(toks[i + 1])
            i += 2
            out.append(f"{cmd}{f(ox + (x - ox) * sx)} {f(oy + (y - oy) * sy)}")
        else:
            rx, ry, rot, la, sw, x, y = (float(v) for v in toks[i:i + 7])
            i += 7
            if cmd == "A":
                x, y = ox + (x - ox) * sx, oy + (y - oy) * sy
            else:
                x, y = x * sx, y * sy
            out.append(f"{cmd}{f(rx * sx)} {f(ry * sy)} {f(rot)} {int(la)} {int(sw)} {f(x)} {f(y)}")
    return "".join(out)


def link_d(c1, c2, reach=1.8, tight=0.35):
    """Deux gouttes sur l'axe : séparées, reliées par un col (fin quand on l'étire, il casse au-delà de
    reach rayons), en cacahuète si elles se chevauchent, ou fondues. reach = 0 : pas de col à distance."""
    (x1, y, r1), (x2, _, r2) = c1, c2
    if x2 < x1:
        (x1, y, r1), (x2, _, r2) = c2, c1
    d = x2 - x1
    rmin = min(r1, r2)
    if d <= abs(r1 - r2) + 0.5:
        return circle_cw(x1, y, r1) if r1 >= r2 else circle_cw(x2, y, r2)
    g = d - r1 - r2
    rg = reach * rmin
    if g >= rg:
        return circle_cw(x1, y, r1) + circle_cw(x2, y, r2)
    if g > 0:
        path = bridge_d((x1, y, r1), (x2, y, r2), rmin * (0.04 + 0.30 * (1 - g / rg)))
        return path if "L" not in path else circle_cw(x1, y, r1) + circle_cw(x2, y, r2)
    a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    yi = math.sqrt(max(r1 * r1 - a * a, 0))
    for tt in (tight, tight * 0.5, tight * 0.2, 0.04):
        path = bridge_d((x1, y, r1), (x2, y, r2), yi + tt * (rmin - yi))
        if "L" not in path:          # jamais l'enveloppe à bords droits : seulement des arcs
            return path
    return circle_cw(x1, y, r1) + circle_cw(x2, y, r2)


def linked(b1, b2, reach):
    """Vrai si deux gouttes forment une seule forme (chevauchement, ou col encore tendu)."""
    g = abs(b2[0] - b1[0]) - b1[1] - b2[1]
    return g < reach * min(b1[1], b2[1])


def shapes(bodies, links, t, free_stretch=True):
    """Assemble les gouttes : composantes liées -> un tracé (cols de la charte), gouttes libres -> ellipses
    étirées dans le sens de leur vitesse (sx·sy = 1, maximum 1,35). bodies : nom -> (x, r, vx)."""
    alive = {n: b for n, b in bodies.items() if b[1] > 0.5}
    parent = {n: n for n in alive}

    def root(n):
        while parent[n] != n:
            n = parent[n]
        return n
    edges = []
    for n1, n2, reach in links:
        if n1 in alive and n2 in alive and linked(alive[n1], alive[n2], reach):
            parent[root(n1)] = root(n2)
            edges.append((n1, n2, reach))
    comps = {}
    for n in alive:
        comps.setdefault(root(n), []).append(n)
    out = []
    for members in comps.values():
        if len(members) == 1:
            x, r, vx = alive[members[0]]
            s = min(1.35, 1 + 0.0035 * abs(vx)) if free_stretch else 1.0
            out.append((members, ellipse_d(x, CY, r * s, r / s)))
        else:
            d = "".join(link_d((alive[a][0], CY, alive[a][1]), (alive[b][0], CY, alive[b][1]), reach)
                        for a, b, reach in edges if a in members)
            out.append((members, d))
    return out


def pulse(tau, dur=F(9)):
    """Onde de taille : gonfle, revient, petit creux (ressort)."""
    u = tau / dur
    if u <= 0 or u >= 1.6:
        return 0.0
    return math.sin(math.pi * u) * math.exp(-0.8 * u)


def vel(fn, t):
    return fn(t) - fn(t - F(1))


def precise_card(card, t, t0, extra_rate=0.04):
    """Le groupe du carton est réécrit avec une échelle à 5 décimales (le moteur arrondit à 0,01, ce qui
    fait avancer la poussée par à-coups) et une poussée renforcée de +4 %/s : la tenue reste fluide."""
    out = []
    for L in card:
        if L["k"] != "group":
            out.append(L)
            continue
        sc = L["s"] * (1 + extra_rate * max(0.0, t - t0))
        out.append({"k": "raw", "svg": f'<g id="carton" transform="translate({CX} {CY}) scale({sc:.5f}) translate({-CX} {-CY})">'
                                      f'{render_layers(L["layers"], uid="ec")}</g>'})
    return out


# =============================================================== INTRO (4,0 s)
# A éclot au centre ; B arrive de la gauche, C de la droite, D de la gauche (perles sur un fil).
A_R = Track((0, 0), (F(2), 20, "out_cubic"), (F(5), 10, "in_cubic"), (F(11), 124, "out_expo"),
            (F(17), 110, "out_back"), (F(46), 110), (F(56), 272, "in_cubic"), (F(64), 250, "ressort"))
B_X = Track((F(6), 0), (F(10), 0), (F(13), -28, "out_cubic"), (F(21), 794, GLISSE), (F(29), 668, "out_back"),
            (F(40), 668), (F(44), 704, "out_cubic"), (F(47), 694, "inout_cubic"), (F(56), 688, "in_cubic"))
B_R = Track((F(6), 0), (F(10), 96, "out_back"), (F(40), 96), (F(46), 124, "out_back"), (F(47), 124),
            (F(56), 62, "in_cubic"))
C_X = Track((F(16), W), (F(20), W), (F(23), W + 28, "out_cubic"), (F(31), 1130, GLISSE), (F(39), 1260, "out_back"),
            (F(45), 1260), (F(49), 1332, "out_cubic"), (F(56), 1230, "in_cubic"))
C_R = Track((F(16), 0), (F(20), 100, "out_back"), (F(47), 100), (F(56), 56, "in_cubic"))
D_X0 = Track((F(26), 0), (F(30), 0), (F(33), -26, "out_cubic"), (F(40), 524, GLISSE))
D_R = Track((F(26), 0), (F(30), 84, "out_back"), (F(40), 84), (F(47), 0, "in_cubic"))
HITS = [(F(21), 1.5), (F(31), 2.5), (F(40), 0.5)]        # (instant, point de contact dans la chaîne D0 B1 A2 C3)
IDX = {"D": 0, "B": 1, "A": 2, "C": 3}
R_WIN = 250


def D_X(t):
    if t <= F(40):
        return D_X0(t)
    return lerp(524, B_X(t), prog(t, F(40), F(47), "inout_cubic"))


def wave(name, t):
    """Onde de taille de la charte 3.6 : chaque choc fait gonfler les voisines, 3 images plus tard par maillon."""
    m = 1.0
    for th, origin in HITS:
        steps = max(0.0, abs(IDX[name] - origin) - 0.5)
        m += 0.17 * 0.8 ** steps * pulse(t - th - F(3) * steps)
    return m


def plunge_out(t):
    """Pendant la plongée, les bosses cassent leur col et filent le long de l'axe."""
    return 700 * prog(t, F(66), F(80), "in_expo")


def intro_bodies(t):
    br = breathe(t, 0.03, 1.1)
    po = plunge_out(t)
    b = {
        "A": (CX, A_R(t) * wave("A", t) * br, 0.0),
        "B": (B_X(t) - po, B_R(t) * wave("B", t) * breathe(t, 0.04, 0.9, 0.3), vel(lambda u: B_X(u) - plunge_out(u), t)),
        "C": (C_X(t) + po, C_R(t) * wave("C", t) * breathe(t, 0.04, 1.0, 0.6), vel(lambda u: C_X(u) + plunge_out(u), t)),
        "D": (D_X(t), D_R(t) * wave("D", t), vel(D_X, t)),
    }
    return b


def intro_links(t):
    return [("D", "B", 1.8 if t >= F(40) else 0), ("B", "A", 1.8 if t >= F(21) else 0),
            ("A", "C", 1.8 if t >= F(31) else 0)]


def chain_squash(t):
    """Chaque choc écrase toute la chaîne (90 % x 111 %), l'impact final plus fort (85 % x 118 %)."""
    sx = 1.0
    for th, _ in HITS:
        sx *= squash(t, th, F(8), -0.1)
    return sx * squash(t, F(56), F(10), -0.15)


_cam = Track((F(62), 1.0), (F(66), 0.93, "in_cubic"), (F(90), 5.6, "plongee"))


def cam(t):
    return _cam(t) + drift(t, F(66), 1.0)        # la poussée ne s'arrête jamais


def cam_speed(t):
    return abs(cam(t + 0.01) - cam(t - 0.01)) / 0.02


def plate_zoom(t, k):
    """Contre-zoom plus lent de la vidéo (parallaxe), plus une poussée propre d'au moins 1 % par image."""
    return 0.8 * k ** 0.55 + 0.35 * max(0.0, t - F(70))


_iris = Track((F(56), 0.0), (F(62), 1.05, "out_expo"), (F(66), 1.0, "out_cubic"))


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    k = cam(t)
    s = min(1 + 0.02 * cam_speed(t), 1.15)
    sq = chain_squash(t)
    gx, gy = k * s, k / s
    for members, d in shapes(intro_bodies(t), intro_links(t), t):
        if "A" in members:
            if len(members) == 1 and t < F(21):
                sa = squash(t, F(11), F(8), 0.18)                   # éclosion : écrasement puis rond
                d = scale_d(d, CX, CY, sa, 1 / sa)
            else:
                d = scale_d(d, CX, CY, sq, 1 / sq)
        if k != 1.0:
            d = scale_d(d, CX, CY, gx, gy)
        name = "bulle" if "A" in members else "goutte-" + "".join(sorted(members)).lower()
        L.append({"k": "fill", "id": name, "fill": ORANGE, "d": d, "ghost": k < 3,
                  "pts": [(intro_bodies(t)[m][0], CY) for m in members if m != "A"]})
    gr = _iris(t)
    if gr > 0.01:
        rr = R_WIN * 0.87 * gr * breathe(t, 0.03, 1.1)
        L.append(video(plate_zoom(t, k), ellipse_d(CX, CY, rr * sq * gx, rr / sq * gy), ghost=rr * k < 900))
    return L


def a_arrivee(side, y=300):
    def fn(t):
        if side == "g":
            return arrow(40, y, 330, y)
        return arrow(W - 40, y, W - 330, y)
    return fn


def a_onde(t):
    return arrow(440, 290, 700, 290, w=6) + arrow(860, 290, 1060, 290, w=6) + arrow(1200, 290, 1420, 290, w=6)


def a_avale(t):
    return arrow(470, 360, 650, 360) + arrow(W - 470, 360, W - 650, 360)


def a_coins(t):
    return "".join(arrow(CX + dx * 520, CY + dy * 300, CX + dx * 860, CY + dy * 480) for dx in (-1, 1) for dy in (-1, 1))


def a_plongee(t):
    return (arrow(560, CY, 120, CY) + arrow(W - 560, CY, W - 120, CY) +
            "".join(arrow(CX + dx * 620, CY + dy * 330, CX + dx * 900, CY + dy * 490) for dx in (-1, 1) for dy in (-1, 1)))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(10), "Première goutte : elle éclot au centre. Elle se contracte 3 images (anticipation), puis jaillit avec 13 % de dépassement.", "out_expo", onion=2, onion_dt=F(2)),
    Beat(F(23), "Une goutte part du bord gauche (coupée à son milieu), recule de 28 px, file sur l'axe, s'écrase contre la première et rebondit : un col naît.", "out_back", ann=a_arrivee("g"), onion=3, onion_dt=F(3)),
    Beat(F(35), "Troisième goutte, depuis la droite : même choc. La chaîne de 3 (charte 3.5) encaisse l'impact (90 % × 111 %).", "out_back", ann=a_arrivee("d"), onion=3, onion_dt=F(3)),
    Beat(F(44), "Quatrième goutte, à gauche : elle fond dans sa voisine. Une onde de taille (+17 %) traverse la chaîne, 3 images par maillon, et tend le dernier col.", "out_cubic", ann=a_onde, onion=2, onion_dt=F(2)),
    Beat(F(53), "La bulle du centre avale la chaîne en 10 images (in_cubic) : +150 % de rayon, il ne reste que deux bosses sur l'axe.", "in_cubic", ann=a_avale, onion=2, onion_dt=F(2)),
    Beat(F(61), "Impact (85 % × 118 %, ressort) puis la vidéo perce la bulle depuis le centre en 6 images : c'est la fenêtre, et le zoom commence.", "out_expo", ann=a_coins, onion=0),
    Beat(F(75), "Plongée : zoom ×5,6 depuis le centre. Les deux bosses cassent leur col et filent le long de l'axe, hors champ.", "plongee", ann=a_plongee, onion=2, onion_dt=F(3)),
    Beat(F(96), "Plein cadre vidéo, la poussée continue (+15 %/s) : on raccorde sur un plan en mouvement.", "out_cubic", onion=0),
])


# =============================================================== OUTRO (4,0 s)
_ok = Track((0, 7.0), (F(3), 7.5, "linear"), (F(18), 1.0, "out_expo"))
_close = Track((F(20), 1.0), (F(23), 1.07, "out_cubic"), (F(29), 0.0, "in_cubic"))
M_R = Track((0, 250), (F(29), 250), (F(34), 232, "in_cubic"), (F(37), 205, "out_cubic"), (F(41), 178, "out_cubic"),
            (F(48), 165, "out_cubic"), (F(55), 130, "inout_cubic"), (F(59), 150, "out_cubic"), (F(66), 0, "in_back"))
E1_X = Track((F(34), CX + 232 - 80), (F(46), 1530, "out_cubic"), (F(49), 1552, "out_cubic"), (F(57), CX + 50, "in_expo"))
E1_R = Track((F(34), 80), (F(42), 80), (F(46), 70, "out_cubic"), (F(57), 60, "linear"), (F(60), 0, "in_cubic"))
E2_X = Track((F(38), CX - 205 + 76), (F(50), 390, "out_cubic"), (F(52), 366, "out_cubic"), (F(63), LG["dot_g"][0], "out_back"))
E3_X0 = Track((F(42), 1450), (F(52), 1790, "out_cubic"), (F(54), 1814, "out_cubic"), (F(64), LG["dot_d"][0], "out_back"))
BUMP_IN = Track((F(4), 700), (F(19), 0, "out_expo"))       # les bosses reviennent le long de l'axe
T_EXP = (F(34), F(38), F(42))


def E3_X(t):
    """La troisième goutte naît dans la première (cascade 3.5-02), puis suit sa propre course."""
    return E3_X0(t) + (E1_X(t) + 18 - 1450) * (1 - prog(t, F(42), F(48), "inout_cubic"))


def recoil(t, ti, amp):
    """Recul (action / réaction) : le corps part à l'opposé de la goutte expulsée puis revient sur un ressort."""
    tau = t - ti
    if tau <= 0:
        return 0.0
    return amp * (1 - math.exp(-tau / 0.03)) * math.exp(-tau / 0.2) * math.cos(TAU * tau / 0.6)


def dot_r(t, t0, t1, r0):
    r = lerp(r0, LG["dot_r"], prog(t, t0, t1, "inout_cubic"))
    return r * (1 + (breathe(t, 0.2, 1.1) - 1) * prog(t, t1 - F(4), t1 + F(6)))


def outro_bodies(t):
    mx = CX - recoil(t, T_EXP[0], 40) + recoil(t, T_EXP[1], 40)
    b = {"M": (mx, M_R(t) * breathe(t, 0.025, 1.2), 0.0)}
    if t < F(34):
        bi = BUMP_IN(t)
        absorb = prog(t, F(29), F(34), "in_cubic")              # charge : les bosses rentrent
        rb_l, rb_r = 62 * (1 - absorb), 56 * (1 - absorb)
        b["BL"] = (CX - (R_WIN + 20) * (1 - 0.6 * absorb) - bi, rb_l * breathe(t, 0.05, 0.9), -vel(BUMP_IN, t))
        b["BR"] = (CX + (R_WIN + 18) * (1 - 0.6 * absorb) + bi, rb_r * breathe(t, 0.05, 1.0, 0.4), vel(BUMP_IN, t))
    if t >= F(34):
        x1 = E1_X(t) - recoil(t, T_EXP[2], 30)
        b["E1"] = (x1, E1_R(t) * breathe(t, 0.04, 0.9), vel(E1_X, t))
    if t >= F(38):
        b["E2"] = (E2_X(t), dot_r(t, F(50), F(63), 76), vel(E2_X, t))
    if t >= F(42):
        b["E3"] = (E3_X(t), dot_r(t, F(52), F(64), 62) * prog(t, F(42), F(43), "out_cubic") ** 0.3, vel(E3_X, t))
    return b


def outro_links(t):
    return [("BL", "M", 1.8), ("M", "BR", 1.8), ("M", "E1", 1.8), ("E2", "M", 1.8 if t < F(46) else 0),
            ("E1", "E3", 1.8 if t < F(50) else 0)]


def outro_squash(t):
    sx = squash(t, F(18), F(9), 0.15) * squash(t, F(29), F(8), -0.06)
    if F(29) <= t < F(34):
        sx *= 1 - 0.08 * prog(t, F(29), F(34), "in_cubic")       # charge : la bulle se comprime
    elif t >= F(34):
        sx *= squash(t, F(34), F(10), -0.08)                       # et se détend à la première expulsion
    return sx


def outro(t):
    L = [{"k": "bg", "v": "gradient"}]
    k = _ok(t)
    s = min(1 + 0.02 * abs(_ok(t + 0.01) - _ok(t - 0.01)) / 0.02, 1.15)
    sq = outro_squash(t)
    bodies = outro_bodies(t)
    logo = []
    for members, d in shapes(bodies, outro_links(t), t):
        if "M" in members:
            d = scale_d(d, bodies["M"][0], CY, sq, 1 / sq)
        if k != 1.0:
            d = scale_d(d, CX, CY, k * s, k / s)
        if members in (["E2"], ["E3"]):
            col = mix_hex(ORANGE, WHITE, prog(t, F(54), F(63)))
            logo.append({"k": "fill", "id": f"point-logo-{'g' if members == ['E2'] else 'd'}", "fill": col, "d": d,
                         "pts": [(bodies[members[0]][0], CY)]})
            continue
        name = "bulle" if "M" in members else "goutte-" + "".join(sorted(members)).lower()
        L.append({"k": "fill", "id": name, "fill": ORANGE, "d": d, "ghost": k < 3,
                  "pts": [(bodies[m][0], CY) for m in members if m != "M"]})
    gr = _close(t) if t >= F(20) else 1.0
    if gr > 0.01 and t < F(30):
        rr = R_WIN * 0.87 * gr * breathe(t, 0.025, 1.2)
        L.append(video(0.8 * k ** 0.55, ellipse_d(CX, CY, rr * sq * k * s, rr / sq * k / s), ghost=rr * k < 900))
    return L, logo


def outro_full(t):
    L, logo = outro(t)
    return L + precise_card(endcard(t, F(66), dots=False, extra=logo), t, F(66))


def a_retour(t):
    return (arrow(CX + 860, CY + 470, CX + 560, CY + 300) + arrow(CX - 860, CY - 470, CX - 560, CY - 300) +
            arrow(CX + 860, CY - 470, CX + 560, CY - 300) + arrow(CX - 860, CY + 470, CX - 560, CY + 300) +
            arrow(80, 380, 380, 380, w=6) + arrow(W - 80, 380, W - 380, 380, w=6))


def a_ferme(t):
    return arrow(CX - 420, CY - 300, CX - 230, CY - 160, w=6) + arrow(CX + 420, CY - 300, CX + 230, CY - 160, w=6)


def a_charge(t):
    return arrow(CX - 470, CY, CX - 300, CY, w=6) + arrow(CX + 470, CY, CX + 300, CY, w=6)


def a_expulse(t):
    return arrow(1290, 380, 1560, 380)


def a_cascade(t):
    return arrow(620, 380, 380, 380) + arrow(1600, 380, 1800, 380)


def a_resserre(t):
    return arrow(330, 400, 560, 400) + arrow(1830, 400, 1360, 400) + arrow(1560, 640, 1150, 640, dash=True)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(8), "La vidéo se rétracte d'un coup (zoom ×7,5 -> ×1 en 15 images) ; les deux bosses reviennent le long de l'axe et se raccrochent.", "out_expo", ann=a_retour, onion=2, onion_dt=F(2)),
    Beat(F(25), "La vidéo se referme vers le centre en 6 images (après +7 % d'anticipation) : il reste une bulle orange à bosses.", "in_cubic", ann=a_ferme, onion=2, onion_dt=F(2)),
    Beat(F(32), "Charge : les bosses rentrent et la bulle se comprime à 92 % en largeur pendant 5 images, puis se détend en expulsant.", "in_cubic", ann=a_charge, onion=2, onion_dt=F(2)),
    Beat(F(37), "Première expulsion, à droite : la goutte bourgeonne, étire son col puis casse net ; la bulle recule de 40 px (action-réaction).", "out_cubic", ann=a_expulse, onion=2, onion_dt=F(2)),
    Beat(F(46), "Cascade (charte 3.5-02) : une goutte part à gauche 4 images plus tard, une troisième naît de la première et file à droite.", "out_cubic", ann=a_cascade, onion=2, onion_dt=F(3)),
    Beat(F(57), "Les gouttes se resserrent : recul de 24 px puis glissement vers le centre ; celles des bords rétrécissent et virent au blanc.", "out_back", ann=a_resserre, onion=2, onion_dt=F(3)),
    Beat(F(65), "La bulle du centre avale la goutte de droite, gonfle, puis s'éteint (in_back) : « sfeer » s'ouvre à sa place.", "in_back", onion=0),
    Beat(F(94), "Les deux gouttes sont les points du logo et respirent (±20 %) ; arabe de droite à gauche ; poussée continue de 11,5 %/s.", "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "C'est ton croquis : chaque goutte est un point gagné, on les compte à l'oreille et à l'œil (4 chocs), sans chiffre ni compteur.",
        "La chaîne de la charte (3.5) se construit sous nos yeux, puis devient la fenêtre : la récompense est faite de nos points.",
        "La fenêtre est un cache rond : elle marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Correction : les gouttes ne tombent plus d'en haut (vertical interdit). Elles glissent sur l'axe depuis les bords, en alternance gauche / droite.",
        "Variante à valider : une chute ultra-courte (6 images) pour la 4e goutte, plus « goutte », mais c'est un écart à la charte.",
        "Gouttes orange sur le dégradé (et non rose / violet) ; elles entrent coupées à leur milieu vertical par le bord (règle 2.48).",
    ]),
    ("Mouvement", [
        "Chaque arrivée : recul de 28 px, glissement qui accélère, choc, rebond avec col, onde de taille dans la chaîne (3 images par maillon).",
        "Asymétrie : les gouttes n'ont ni la même taille ni le même écart ; la droite se tend quand la gauche frappe.",
        "AE : un calque de forme par goutte sur l'axe, cols en tracé animé ; la fenêtre est un cache alpha sur la vidéo.",
    ]),
]
