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
                       mix_hex, waist_h)

CX = W / 2

META = {
    "id": "p08_division_cellulaire",
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


def neck(c1, c2, h):
    """Deux cellules reliées par un cou, dans n'importe quelle direction."""
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    dist = math.dist((x1, y1), (x2, y2))
    if dist < 1:
        return circle_d(x1, y1, max(r1, r2))
    ang = math.atan2(y2 - y1, x2 - x1)
    d = bridge_d((x1, y1, r1), (x1 + dist, y1, r2), h)
    if "a" in d or "L" in d:                    # cas dégénérés : simple union de cercles
        return circle_d(x1, y1, r1) + circle_d(x2, y2, r2)
    return rotate_path(d, x1, y1, ang)


def division(g, u, wob=1.0):
    """Génération g-1 -> g à l'avancement u (0..1, peut dépasser 1 avec out_back).
    Les enfants bourgeonnent de l'enfant « maison » ; le cou s'affine puis casse à u ≈ 0,8."""
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
        if ci != h and u < 0.95:
            hc = pos[h]
            rr = min(c[2], hc[2])
            dd = math.dist(c[:2], hc[:2]) / rr
            if dd < 0.05:
                thick = None
            elif dd < 1.95:                                  # encore collées : taille de cacahuète
                thick = waist_h((0, 0, hc[2]), (dd * rr, 0, c[2]), 0.25)
            else:                                          # le cou s'affine jusqu'à la rupture (≈ 3,3 r)
                thick = max(2.0, rr * (0.42 - 0.40 * (dd - 1.95) / 1.35))
            if thick is not None and dd < 3.3:
                L.append({"k": "fill", "fill": ORANGE, "d": neck(hc, c, thick), "ghost": False})
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


# ----------------------------------------------------------------- INTRO (4,4 s)
pop = Track((0, 46), (F(7), 112, "out_back_fort"))
d1 = Track((F(12), 0.0), (F(24), 1.0, "out_back"))     # 1 -> 3   ♪ do
d2 = Track((F(28), 0.0), (F(40), 1.0, "out_back"))     # 3 -> 11  ♪ mi
d3 = Track((F(44), 0.0), (F(54), 1.0, "out_back"))     # 11 -> 26 ♪ sol (plus rapide)
g_in = Track((F(66), 0.0), (F(78), 1.0, "in_expo"))     # aspiration
win = Track((F(84), 0.0), (F(94), 1.0, "out_expo"))     # la fenêtre s'ouvre ♪ clic
plunge = Track((F(94), 1.0), (F(110), 3.6, "plongee"))


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
    elif t < F(66):
        if t < F(54):
            L += division(3, d3(t))
        else:
            L += cells(3, wave_t=t - F(54))                       # le motif ondule : tension
    elif t < F(80):
        L += gather(g_in(t))
    else:
        k = plunge(t) + drift(t, F(94), 0.4)
        sq = squash(t, F(78), F(10), 0.28)
        r = 150 * (1 + 1.4 * win(t)) * (k if t >= F(94) else 1)
        L.append({"k": "fill", "id": "cellule-unique", "fill": ORANGE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
        if win(t) > 0:
            L.append(video(0.7 * k ** 0.6, ellipse_d(CX, AXIS, r * sq * win(t) * 0.97, r / sq * win(t) * 0.97), ghost=win(t) < 1))
    return L


def a_div(t):
    return arrow(CX - 150, AXIS - 230, CX - 330, AXIS - 230) + arrow(CX + 150, AXIS - 230, CX + 330, AXIS - 230)


def a_gather(t):
    return "".join(arrow(CX + dx * 720, AXIS + dy * 330, CX + dx * 300, AXIS + dy * 140) for dx in (-1, 1) for dy in (-1, 1))


def a_plunge(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 290, CX + dx * 880, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.4, intro, [
    Beat(F(4), "Accroche dès l'image 0 : la cellule surgit au centre avec dépassement (+15 %).", "out_back_fort", onion=0),
    Beat(F(10), "Anticipation : la cellule s'étire de 16 % sur l'axe juste avant de se diviser.", "in_cubic"),
    Beat(F(14), "♪ do. 1 → 3 : deux cellules bourgeonnent de part et d'autre, le cou s'affine et casse net.", "out_back", ann=a_div),
    Beat(F(30), "♪ mi. 3 → 11 : chaque cellule se divise en rangées autour de l'axe (3 / 5 / 3).", "out_back"),
    Beat(F(45), "♪ sol, plus rapide. 11 → 26 : le motif 8 / 10 / 8 se forme en 10 images.", "out_back"),
    Beat(F(60), "Le motif ondule de gauche à droite (±16 %, motif 3.6) : la tension monte.", "linear", onion=0),
    Beat(F(74), "Regroupement : tout est aspiré vers le centre en accélérant, étiré vers le cœur, et fusionne en une bulle.", "in_expo", ann=a_gather),
    Beat(F(100), "♪ clic. Impact écrasé puis la bulle s'ouvre sur la vidéo et l'on plonge en zoom diagonal.", "plongee", ann=a_plunge),
])


# ----------------------------------------------------------------- OUTRO (4,0 s)
o_close = Track((F(2), 3.4), (F(16), 1.0, "emphase"))
o_pull = Track((0, 1.25), (F(16), 1.0, "out_cubic"))
o_orange = Track((F(16), 0.0), (F(24), 1.0, "out_expo"))
o_burst = Track((F(24), 0.0), (F(34), 1.0, "out_back"))        # 1 -> 26 d'un coup  ♪ sol
o_m1 = Track((F(38), 1.0), (F(46), 0.0, "in_cubic"))           # 26 -> 11 ♪ mi
o_m2 = Track((F(48), 1.0), (F(55), 0.0, "in_cubic"))           # 11 -> 3
o_m3 = Track((F(57), 1.0), (F(63), 0.0, "in_cubic"))           # 3 -> 1   ♪ do
o_split = Track((F(66), 0.0), (F(78), 1.0, "emphase"))         # 1 -> 2 points du logo ♪ clic
LOGO_T0 = F(72)


def outro(t):
    if t < F(16):
        r = 560 * o_close(t)
        return [{"k": "bg", "v": "gradient"}, video(o_pull(t), circle_d(CX, AXIS, r), ghost=r < 1400)]
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(24):
        r = 560 + (112 - 560) * prog(t, F(16), F(24), "in_expo")
        L.append({"k": "fill", "id": "cellule", "fill": ORANGE, "d": circle_d(CX, AXIS, r)})
        if o_orange(t) < 1:
            L.append(video(1.0, circle_d(CX, AXIS, r * (1 - o_orange(t))), ghost=False))
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
    Beat(F(8), "Fin du plan : la vidéo se referme en une bulle centrée (zoom arrière 125 % -> 100 %).", "emphase"),
    Beat(F(20), "La bulle redevient orange et se contracte en cellule (aspiration in expo).", "in_expo"),
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
