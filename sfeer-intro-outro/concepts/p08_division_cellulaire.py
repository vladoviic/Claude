"""Piste 8 (reprise demandée par la DA) : « Division cellulaire ».

1 cellule -> 3 -> 11 -> 26, chaque division sur un temps, avec une signature sonore courte et
entêtante (trois « pops » montants do-mi-sol, façon clic de console). Puis tout se regroupe en une
seule bulle (aspiration + impact) qui devient la fenêtre sur la suite. L'outro rejoue le motif à
l'envers (26 -> 11 -> 3 -> 1, sol-mi-do) et finit sur le logo.

Disposition : rangées horizontales centrées sur l'axe (motif 3.6), en losange 1 / 3 / 3-5-3 / 8-10-8.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, prog  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, arrow, bridge_d, circle_d, ellipse_d, f,  # noqa: E402
                       mix_hex)

CX = W / 2

META = {
    "id": "p08_division_cellulaire",
    "ae_intro": "SFEER_INTRO_01_DIVISION_16x9",
    "ae_outro": "SFEER_OUTRO_01_DIVISION_16x9",
    "ae_folder": "SFEER · 01 DIVISION",
    "num": "P8",
    "title": "Division cellulaire",
    "principe": "Une cellule se divise sur un rythme (1, 3, 11, 26) puis tout se regroupe en une bulle qui ouvre la fenêtre.",
    "logline": "Piste 8 reprise par la DA. La bulle se divise comme une cellule, en trois temps qui sonnent do-mi-sol. "
               "Tout le motif est aspiré en une seule bulle, impact, clic : la fenêtre s'ouvre sur la suite.",
}


# --- Géométrie des générations ---------------------------------------------
def rows(counts, r, dx_k=3.1, dy_k=2.7):
    """Rangées horizontales centrées sur l'axe, décalées en damier (motif 3.6)."""
    out = []
    n = len(counts)
    for j, c in enumerate(counts):
        y = AXIS + (j - (n - 1) / 2) * dy_k * r
        for i in range(c):
            out.append((CX + (i - (c - 1) / 2) * dx_k * r, y, r))
    return out


GEN = [rows([1], 112), rows([3], 78), rows([3, 5, 3], 48), rows([8, 10, 8], 33)]


def parents_of(children, parents):
    """Chaque enfant naît de la cellule-mère la plus proche."""
    return [min(range(len(parents)), key=lambda k: math.dist(c[:2], parents[k][:2])) for c in children]


PARENT = [None] + [parents_of(GEN[g], GEN[g - 1]) for g in range(1, len(GEN))]


def home_child(g):
    """Pour chaque mère, l'enfant le plus proche reste sur place (les autres bourgeonnent de lui)."""
    homes = {}
    for ci, pi in enumerate(PARENT[g]):
        p = GEN[g - 1][pi]
        if pi not in homes or math.dist(GEN[g][ci][:2], p[:2]) < math.dist(GEN[g][homes[pi]][:2], p[:2]):
            homes[pi] = ci
    return homes


HOME = [None] + [home_child(g) for g in range(1, len(GEN))]


# --- Cou orienté (bridge_d est horizontal : on le fait tourner) ----------------
_TOK = re.compile(r"[MLAZaz]|-?\d+(?:\.\d+)?")


def rotate_path(d, cx, cy, ang):
    toks = _TOK.findall(d)
    ca, sa = math.cos(ang), math.sin(ang)

    def rot(x, y):
        x, y = x - cx, y - cy
        return cx + x * ca - y * sa, cy + x * sa + y * ca
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MLAZ":
            cmd = t
            out.append(t)
            i += 1
            continue
        if cmd in ("M", "L"):
            x, y = rot(float(toks[i]), float(toks[i + 1]))
            out.append(f"{f(x)} {f(y)}")
            i += 2
        elif cmd == "A":
            rx, ry, xr, la, sw = toks[i:i + 5]
            x, y = rot(float(toks[i + 5]), float(toks[i + 6]))
            out.append(f"{rx} {ry} {xr} {la} {sw} {f(x)} {f(y)}")
            i += 7
        else:
            i += 1
    return "".join(o if o in "MLAZ" else o + " " for o in out).replace(" Z", "Z")


FILLET = 0.93          # rayon du congé du cou / rayon moyen des bulles (mesuré sur la charte, héros 3.1)


def charte_h(c1, c2):
    """Demi-épaisseur du cou pour un congé de rayon constant R = 0,93 r (construction de la charte).
    None si les bulles sont trop loin : le cou a cassé (≈ 3,36 r pour deux bulles égales)."""
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    d = math.dist((x1, y1), (x2, y2))
    if d < 1e-6:
        return None
    R = FILLET * (r1 + r2) / 2
    a = (d * d + (r1 + R) ** 2 - (r2 + R) ** 2) / (2 * d)
    y2_ = (r1 + R) ** 2 - a * a
    if y2_ <= 0:
        return None
    h = math.sqrt(y2_) - R
    return h if h > 0.5 else None


def neck(c1, c2, h=None):
    """Deux cellules reliées par le cou de la charte, dans n'importe quelle direction.
    Renvoie None si le cou a cassé."""
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    dist = math.dist((x1, y1), (x2, y2))
    if dist < 1:
        return circle_d(x1, y1, max(r1, r2))
    h = charte_h(c1, c2) if h is None else h
    if h is None:
        return None
    ang = math.atan2(y2 - y1, x2 - x1)
    d = bridge_d((x1, y1, r1), (x1 + dist, y1, r2), h)
    if "a" in d or "L" in d:                    # cas dégénérés : simple union de cercles
        return circle_d(x1, y1, r1) + circle_d(x2, y2, r2)
    return rotate_path(d, x1, y1, ang)


def division(g, u, wob=1.0):
    """Génération g-1 -> g à l'avancement u (0..1, peut dépasser 1 avec out_back).
    Les enfants bourgeonnent de l'enfant « maison » : cou de la charte qui s'affine, puis casse net."""
    L = []
    homes = HOME[g]
    pos = []
    for ci, c in enumerate(GEN[g]):
        p = GEN[g - 1][PARENT[g][ci]]
        x = p[0] + (c[0] - p[0]) * u
        y = p[1] + (c[1] - p[1]) * u
        r = p[2] + (c[2] - p[2]) * min(1.0, u)
        pos.append((x, y, r * wob))
    for ci, c in enumerate(pos):
        h = homes[PARENT[g][ci]]
        if ci != h:
            d = neck(pos[h], c)
            if d:
                L.append({"k": "fill", "fill": ORANGE, "d": d, "ghost": False})
        L.append({"k": "fill", "id": f"c{g}-{ci}", "fill": ORANGE, "d": circle_d(*c), "pts": [c[:2]], "ghost": ci < 12})
    return L


def cells(gen, wob=1.0, wave_t=None):
    """Génération posée ; wave_t : onde de taille qui traverse le motif de gauche à droite (3.6)."""
    L = []
    for ci, (x, y, r) in enumerate(GEN[gen]):
        k = 1.0
        if wave_t is not None:
            k = 1 + 0.16 * math.sin(2 * math.pi * (wave_t * 2.2 - (x - CX) / 900))
        L.append({"k": "fill", "id": f"c{gen}-{ci}", "fill": ORANGE, "d": circle_d(x, y, r * k * wob), "ghost": False})
    return L


def gather(u, gen=3, r_end=150):
    """Regroupement : tout le motif est aspiré vers le centre et fusionne en une bulle."""
    L = []
    for ci, (x, y, r) in enumerate(GEN[gen]):
        xx, yy = x + (CX - x) * u, y + (AXIS - y) * u
        rr = r + (r_end * 0.62 - r) * u
        st = 1 + 0.3 * math.sin(math.pi * u)            # étirées vers le centre
        ang = math.degrees(math.atan2(AXIS - y, CX - x))
        L.append({"k": "raw", "svg": f'<path transform="translate({f(xx)} {f(yy)}) rotate({f(ang)})" '
                                     f'd="{ellipse_d(0, 0, rr * st, rr / st)}" fill="{ORANGE}"/>'})
    if u > 0.55:
        L.append({"k": "fill", "id": "cellule-unique", "fill": ORANGE, "d": circle_d(CX, AXIS, r_end * prog(u, 0.55, 1.0, "out_cubic"))})
    return L


# --- Composition finale : la fenêtre au centre, des chaînes de cellules remplissent le cadre ---
WIN_R = 330
STEP = 183            # 3,27 r pour r = 56 : la pose étirée de la charte
FINAL = [
    # axe : demi-bulles coupées au milieu par les bords, bulles moyennes reliées à la fenêtre
    [(0, AXIS, 150), (395, AXIS, 100)],
    [(1525, AXIS, 100), (1920, AXIS, 150)],
    # rangées haute et basse en damier (motif 3.6), chaînes de 2 et 3
    [(120, 106, 56), (120 + STEP, 106, 56)],
    [(640, 106, 56), (640 + STEP, 106, 56), (640 + 2 * STEP, 106, 56)],
    [(1530, 106, 56), (1530 + STEP, 106, 56)],
    [(214, 974, 56), (214 + STEP, 974, 56)],
    [(914, 974, 56), (914 + STEP, 974, 56), (914 + 2 * STEP, 974, 56)],
    [(1617, 974, 56), (1617 + STEP, 974, 56)],
]
LINK_TO_WIN = []                         # la fenêtre reste libre : pas de cou épais vers elle
TARGETS = [b for ch in FINAL for b in ch]


def final_layer(u, t, k=1.0, uid="fin", wob_t=None):
    """Les chaînes jaillissent de la bulle centrale vers leur place (u 0..1, dépassement possible),
    décalées par distance au centre. k : poussée caméra (zoom centré). Cous de la charte."""
    L = []
    pos_ch = []
    for ci, ch in enumerate(FINAL):
        row = []
        for bi, (x, y, r) in enumerate(ch):
            dist = math.dist((x, y), (CX, AXIS))
            lag = 0.22 * dist / 1100                       # les plus loin partent un peu après
            uu = max(0.0, (u - lag) / (1 - lag)) if u < 1 else u
            e = uu
            xx, yy = CX + (x - CX) * e, AXIS + (y - AXIS) * e
            rr = r * min(1.0, 0.35 + 0.65 * uu)
            if wob_t is not None:                          # onde qui court de gauche à droite (3.6)
                rr *= 1 + 0.07 * math.sin(2 * math.pi * (wob_t * 1.4 - x / 1200))
            xx, yy, rr = CX + (xx - CX) * k, AXIS + (yy - AXIS) * k, rr * k
            row.append((xx, yy, rr))
        pos_ch.append(row)
    for row in pos_ch:
        for a, b in zip(row, row[1:]):
            d = neck(a, b)
            if d:
                L.append({"k": "fill", "fill": ORANGE, "d": d, "ghost": False})
        for c in row:
            L.append({"k": "fill", "id": uid, "fill": ORANGE, "d": circle_d(*c), "ghost": False})
    return L, pos_ch


pop = Track((0, 46), (F(7), 112, "out_back_fort"))
d1 = Track((F(12), 0.0), (F(24), 1.0, "out_back"))     # 1 -> 3   ♪ do
d2 = Track((F(28), 0.0), (F(40), 1.0, "out_back"))     # 3 -> 11  ♪ mi
d3 = Track((F(44), 0.0), (F(54), 1.0, "out_back"))     # 11 -> 26 ♪ sol (plus rapide)
g_in = Track((F(64), 0.0), (F(76), 1.0, "in_expo"))     # tout se regroupe en une seule bulle
expel = Track((F(79), 0.0), (F(93), 1.0, "out_back"))   # la bulle ré-éjecte les chaînes vers les bords
grow = Track((F(76), 150), (F(79), 136, "in_cubic"), (F(93), WIN_R, "out_back"))
win = Track((F(82), 0.0), (F(94), 1.0, "emphase"))      # la fenêtre s'ouvre dans la bulle ♪ clic


def push(t):
    return 1 + 0.004 * max(0.0, t * 25 - 90) + 0.0 * t   # poussée lente continue sur la tenue


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(12):
        sx = 1 + 0.16 * prog(t, F(7), F(12), "in_cubic")          # anticipation : s'étire avant de se diviser
        r = pop(t)
        L.append({"k": "fill", "id": "cellule", "fill": ORANGE, "d": ellipse_d(CX, AXIS, r * sx, r / sx)})
    elif t < F(28):
        L += division(1, d1(t), breathe(t, 0.04, 0.5) if t > F(24) else 1)
    elif t < F(44):
        L += division(2, d2(t), breathe(t, 0.05, 0.4) if t > F(40) else 1)
    elif t < F(64):
        if t < F(54):
            L += division(3, d3(t))
        else:
            L += cells(3, wave_t=t - F(54))                       # le motif ondule : tension
    elif t < F(78):
        L += gather(g_in(t))
    else:
        k = push(t)
        sq = squash(t, F(76), F(10), 0.28)
        rw = grow(t) * k
        u = expel(t)
        if u > 0:
            fl, pos_ch = final_layer(u, t, k, wob_t=t - F(93) if t > F(93) else None)
            # cous qui relient la fenêtre aux bulles moyennes de l'axe
            for ci, bi in LINK_TO_WIN:
                d = neck((CX, AXIS, rw), pos_ch[ci][bi])
                if d:
                    L.append({"k": "fill", "fill": ORANGE, "d": d, "ghost": False})
            L += fl
        L.append({"k": "fill", "id": "cellule-unique", "fill": ORANGE, "d": ellipse_d(CX, AXIS, rw * sq, rw / sq)})
        if win(t) > 0.03:
            rv = rw * win(t) * 0.94
            L.append(video(0.9 + 0.1 * k, ellipse_d(CX, AXIS, rv * sq, rv / sq), ghost=win(t) < 1))
    return L


def a_div(t):
    return arrow(CX - 150, AXIS - 230, CX - 330, AXIS - 230) + arrow(CX + 150, AXIS - 230, CX + 330, AXIS - 230)


def a_gather(t):
    return "".join(arrow(CX + dx * 720, AXIS + dy * 330, CX + dx * 300, AXIS + dy * 140) for dx in (-1, 1) for dy in (-1, 1))


def a_expel(t):
    return (arrow(CX - 360, AXIS - 60, CX - 560, AXIS - 60) + arrow(CX + 360, AXIS - 60, CX + 560, AXIS - 60) +
            arrow(CX - 200, AXIS - 300, CX - 420, AXIS - 400) + arrow(CX + 200, AXIS + 300, CX + 420, AXIS + 400))


INTRO = Anim("INTRO", 4.4, intro, [
    Beat(F(4), "Accroche dès l'image 0 : la cellule surgit au centre avec dépassement (+15 %).", "out_back_fort", onion=0),
    Beat(F(10), "Anticipation : la cellule s'étire de 16 % sur l'axe juste avant de se diviser.", "in_cubic"),
    Beat(F(14), "♪ do. 1 → 3 : deux cellules bourgeonnent de part et d'autre, le cou s'affine et casse net.", "out_back", ann=a_div),
    Beat(F(30), "♪ mi. 3 → 11 : chaque cellule se divise en rangées autour de l'axe (3 / 5 / 3).", "out_back"),
    Beat(F(45), "♪ sol, plus rapide. 11 → 26 : le motif 8 / 10 / 8 se forme en 10 images.", "out_back"),
    Beat(F(72), "Regroupement : tout est aspiré vers le centre en accélérant, étiré vers le cœur, et fusionne en une bulle.", "in_expo", ann=a_gather),
    Beat(F(86), "Impact, puis la bulle ré-éjecte des chaînes vers les bords (dépassement 10 %) et s'ouvre sur la vidéo. ♪ clic", "out_back", ann=a_expel),
    Beat(F(109), "Dernière image : fenêtre au centre, chaînes reliées par les cous de la charte jusqu'aux bords ; onde et poussée lente.", "emphase", onion=0),
])


# ----------------------------------------------------------------- OUTRO (4,0 s)
o_close = Track((0, 3.4), (F(14), 1.0, "emphase"))             # le plein cadre se referme sur la composition
o_in = Track((0, 0.0), (F(14), 1.0, "out_expo"))                 # les chaînes reviennent depuis le hors-champ
o_suck = Track((F(14), 0.0), (F(24), 1.0, "anticipe"))          # tout est aspiré dans la fenêtre
o_orange = Track((F(16), 0.0), (F(24), 1.0, "out_expo"))
o_burst = Track((F(24), 0.0), (F(34), 1.0, "out_back"))        # 1 -> 26 d'un coup  ♪ sol
o_m1 = Track((F(38), 1.0), (F(46), 0.0, "in_cubic"))           # 26 -> 11 ♪ mi
o_m2 = Track((F(48), 1.0), (F(55), 0.0, "in_cubic"))           # 11 -> 3
o_m3 = Track((F(57), 1.0), (F(63), 0.0, "in_cubic"))           # 3 -> 1   ♪ do
o_split = Track((F(66), 0.0), (F(78), 1.0, "emphase"))         # 1 -> 2 points du logo ♪ clic
LOGO_T0 = F(72)


def outro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(24):
        su = o_suck(t)
        k = 1 + 1.6 * (1 - o_in(t))                               # zoom arrière : les chaînes rentrent par les bords
        rw = (WIN_R * o_close(t) if t < F(14) else WIN_R + (112 - WIN_R) * su)
        fl, pos_ch = final_layer(1 - su, t, k, uid="fin")
        for ci, bi in LINK_TO_WIN:
            d = neck((CX, AXIS, rw), pos_ch[ci][bi])
            if d:
                L.append({"k": "fill", "fill": ORANGE, "d": d, "ghost": False})
        L += fl
        L.append({"k": "fill", "id": "cellule", "fill": ORANGE, "d": circle_d(CX, AXIS, rw)})
        if o_orange(t) < 0.97:
            L.append(video(1.0 + 0.25 * (1 - o_in(t)), circle_d(CX, AXIS, rw * 0.94 * (1 - o_orange(t))) if rw < 1300 else None, ghost=False))
        return L
    elif t < F(36):
        # la cellule éclate directement en 26 (le motif réapparaît)
        u = o_burst(t)
        for ci, (x, y, r) in enumerate(GEN[3]):
            xx, yy = CX + (x - CX) * u, AXIS + (y - AXIS) * u
            L.append({"k": "fill", "id": f"c3-{ci}", "fill": ORANGE, "d": circle_d(xx, yy, r * (0.4 + 0.6 * min(u, 1.2))), "ghost": ci < 10})
    elif t < F(47):
        L += division(3, o_m1(t)) if t >= F(38) else cells(3, wave_t=t - F(36))
    elif t < F(56):
        L += division(2, o_m2(t)) if t >= F(48) else cells(2)
    elif t < F(64):
        L += division(1, o_m3(t)) if t >= F(57) else cells(1)
    if t >= F(64):
        u = o_split(t)
        sq = squash(t, F(63), F(8), 0.25)
        gx, dx = LG["dot_g"][0], LG["dot_d"][0]
        if u <= 0:
            L.append({"k": "fill", "id": "cellule", "fill": ORANGE, "d": ellipse_d(CX, AXIS, 112 * sq, 112 / sq)})
        else:
            r = 112 / math.sqrt(2) * (1 - u) + LG["dot_r"] * u * breathe(t, 0.2, 1.1)
            spread = 60 * min(1, u * 3) + (CX - gx - 60) * u
            col = mix_hex(ORANGE, WHITE, prog(t, F(70), F(78)))
            c1, c2 = (CX - spread, AXIS, r), (CX + spread, AXIS, r)
            d = bridge_d(c1, c2, r * 0.3 * max(0.0, 1 - u * 4)) if u < 0.25 else circle_d(*c1) + circle_d(*c2)
            dots = [{"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": [c1[:2], c2[:2]]}]
            L += endcard(t, LOGO_T0, dots=False, extra=dots) if t >= LOGO_T0 else dots
    return L


OUTRO = Anim("OUTRO", 4.0, outro, [
    Beat(F(7), "Fin du plan : la vidéo se referme dans la fenêtre, les chaînes rentrent par les bords (zoom arrière).", "emphase"),
    Beat(F(19), "Tout est aspiré dans la fenêtre, qui redevient orange et se contracte en cellule.", "anticipe"),
    Beat(F(30), "♪ sol. Éclatement : la cellule repart d'un coup en 26 (8 / 10 / 8) avec dépassement.", "out_back"),
    Beat(F(44), "♪ mi. Les cellules fusionnent deux à deux : 26 → 11, les cous se reforment.", "in_cubic"),
    Beat(F(52), "11 → 3, plus vite : les rangées du haut et du bas rejoignent l'axe.", "in_cubic"),
    Beat(F(61), "♪ do. 3 → 1 : impact écrasé au centre, retour au rond sur un ressort.", "in_cubic"),
    Beat(F(70), "♪ clic. La cellule se divise en deux (charte 3.4-02) qui filent vers les points du logo en blanchissant.", "emphase"),
    Beat(F(96), "Carton : « sfeer » s'ouvre entre les points, arabe et endossement ; tenue vivante.", "emphase"),
])

NOTES = [
    ("Pourquoi ça marche", [
        "La division cellulaire dit la croissance : chaque membre en fait naître d'autres, la communauté se multiplie (1, 3, 11, 26).",
        "Le regroupement final montre l'inverse : tous ensemble, une seule bulle, et c'est elle qui ouvre le film.",
        "Principe réutilisable : seuls les nombres de cellules et la vidéo changent d'un projet à l'autre.",
    ]),
    ("Signature sonore", [
        "Trois « pops » courts et montants calés sur les divisions : do, mi, sol (triade majeure, 40 ms chacun, timbre boisé et sec).",
        "Aspiration courte qui descend en hauteur au regroupement, puis un « clic » sec à l'ouverture de la fenêtre, comme l'emboîtement d'une manette.",
        "Outro : le même motif à l'envers (sol, mi, do) puis le clic sur le logo. Le motif tient en 1,8 s et se retient dès la 2e écoute.",
    ]),
    ("Charte et mouvement", [
        "Rangées horizontales centrées sur l'axe (motif 3.6), cous de la charte qui s'affinent et cassent à chaque division.",
        "Rythme qui accélère : 12, 12 puis 10 images par division, avec dépassement et ressort à chaque pose.",
        "Écart à valider : cous obliques entre rangées pendant les divisions (transitoires de moins de 10 images).",
    ]),
]


def AE_TRACK(layer_id):
    """Regroupement des calques pour After Effects : toutes les cellules dans un seul calque de forme."""
    return "Logo · points" if layer_id == "points-logo" else "Cellules · orange"
