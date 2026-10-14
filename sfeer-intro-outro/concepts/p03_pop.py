"""Piste 3 (croquis de la DA) : « POP ! ».

Une bulle gonfle, claque et se divise en 2, puis 4, puis 8, chaque division plus rapide que la
précédente (1 -> 2 en 10 images, 2 -> 4 en 7, 4 -> 8 en 5, puis 1 image par bulle). Les rangées du
motif 3.6 se déroulent depuis les bords comme des fermetures éclair. Le motif est aspiré vers le
centre et se tasse en une masse bosselée qui bouge encore ; elle se lisse en un grand cercle : la
fenêtre verte. On plonge. L'outro rejoue tout à l'envers et finit sur les deux points du logo.

Toutes les formes sont tracées dans le sens horaire (même sens que bridge_d) : une union de cercles
et de cols dans un seul tracé reste pleine, sans trou.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, back_out, breathe, ease, lerp, prog  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, curved_arrow, f,  # noqa: E402
                       mix_hex)

CX = W / 2

META = {
    "id": "p03_pop",
    "num": "P3",
    "title": "Pop !",
    "logline": "Piste 3 de la DA. Une bulle gonfle et claque : 1, 2, 4, 8, de plus en plus vite, puis le motif 3.6 "
               "se déroule. Tout est aspiré en une masse bosselée qui se lisse en fenêtre verte, et l'on plonge.",
}


# =================================================================== géométrie (sens horaire partout)
def circ(x, y, r):
    return f"M{f(x - r)} {f(y)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ell(x, y, rx, ry, ang=0.0):
    """Ellipse (étirement à volume constant), grand axe orienté selon ang (radians)."""
    c, s = math.cos(ang), math.sin(ang)
    x0, y0, x1, y1 = x - rx * c, y - rx * s, x + rx * c, y + rx * s
    deg = f(math.degrees(ang))
    return (f"M{f(x0)} {f(y0)}A{f(rx)} {f(ry)} {deg} 1 1 {f(x1)} {f(y1)}"
            f"A{f(rx)} {f(ry)} {deg} 1 1 {f(x0)} {f(y0)}Z")


def hull(x1, r1, x2, r2, y):
    """Enveloppe convexe de deux cercles sur une même ligne (col plein)."""
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, y - r1 * ny), (x2 + r2 * nx, y - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, y + r2 * ny), (x1 + r1 * nx, y + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def fillet_h(d, r1, r2):
    """Demi-épaisseur du col de la charte : congé de rayon constant R = 0,91 r moyen (analyse 3.3).
    Rupture à d = 3,36 r. None = rompu."""
    rm = (r1 + r2) / 2
    rf = 0.91 * rm
    v = (rm + rf) ** 2 - d * d / 4
    if v <= rf * rf:
        return None
    return math.sqrt(v) - rf


def link(x1, r1, x2, r2, y, h):
    """Pont de la charte entre deux cercles d'une même rangée (cacahuète, col ou fusion)."""
    if x2 < x1:
        x1, r1, x2, r2 = x2, r2, x1, r1
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        return circ(x1, y, r1) if r1 >= r2 else circ(x2, y, r2)
    rmin = min(r1, r2)
    if d < r1 + r2:                                        # cercles qui se chevauchent : taille valide
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        h = max(h, math.sqrt(max(r1 * r1 - a * a, 0)) + 0.5)
    if h >= 0.97 * rmin or _neck_circle((x1, y, r1), (x2, y, r2), h) is None:
        return hull(x1, r1, x2, r2, y)
    return bridge_d((x1, y, r1), (x2, y, r2), h)


def blob(rows):
    """rows : rangées de bulles (x, y, r, sx, ang). Cols de la charte entre voisines d'une rangée,
    calculés sur le cercle intérieur ; l'ellipse étirée se superpose (même sens de tracé)."""
    parts = []
    for row in rows:
        row = sorted((b for b in row if b[2] > 0.5), key=lambda b: b[0])
        for a, b in zip(row, row[1:]):
            ra, rb = a[2] * min(a[3], 1 / a[3]), b[2] * min(b[3], 1 / b[3])
            h = fillet_h(abs(b[0] - a[0]), ra, rb)
            if h is not None:
                parts.append(link(a[0], ra, b[0], rb, a[1], h))
        for x, y, r, sx, ang in row:
            parts.append(ell(x, y, r * sx, r / sx, ang) if abs(sx - 1) > 2e-3 else circ(x, y, r))
    return " ".join(parts)


def vel(fn, t, dt=0.008):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def vstretch(v, k=9000.0, cap=1.28):
    """Étirement dans le sens de la vitesse (px/s), volume conservé, plafonné à 1,28."""
    return min(cap, 1 + abs(v) / k)


def first_snap(fn_d, fn_r, t0, t1):
    """Instant où le col casse (écart > 3,36 r) : pour placer l'écrasement de recul."""
    n = int((t1 - t0) * 400)
    for i in range(n + 1):
        t = t0 + i / 400
        if fillet_h(fn_d(t), fn_r(t), fn_r(t)) is None:
            return t
    return t1


# =================================================================== grille du motif 3.6
R8, PX, PY = 75, 240, 183                 # rayon du motif, pas horizontal (3,2 r), pas vertical (2,44 r)
X8 = [120 + PX * i for i in range(8)]     # rangées paires (axe, ±2)
XA = [PX * i for i in range(9)]           # rangées impaires : bulles des bords coupées à leur milieu
X4 = [240, 720, 1200, 1680]
X2 = [480, 1440]
R1, R2, R4 = 190, 150, 108
BK = back_out(0.9)                         # dépassement 3 % (le col ne casse pas)
BK6 = back_out(1.7)                        # dépassement 10 %


def row_y(j):
    return AXIS + j * PY


def wave36(t, i, j, x, t_on, amp=0.3):
    """Charte 3.6 : les tailles ondulent (gros + petit = constant), vague de gauche à droite."""
    a = amp * prog(t, t_on, t_on + F(8), "out_cubic")
    return 1 + a * (-1) ** (i + j) * math.sin(2 * math.pi * 2.2 * (t - x / W * F(14)))


# =================================================================== INTRO (4,0 s)
r_pop = Track((0, 0), (F(5), R1, "out_back_fort"), (F(10), R1 * 1.1, "in_cubic"))   # pop puis gonfle de 10 %
sx_ant = Track((F(7), 1.0), (F(10), 0.84, "in_cubic"), (F(13), 1.0, "out_cubic"))   # se tasse avant de claquer
D1 = Track((F(10), 0), (F(14), 245, "inout_cubic"), (F(20), 480, BK6))              # 1 -> 2 : col tendu 4 i., rupture, recul
r12 = Track((F(10), R1 * 1.1), (F(14), R2 * 1.04, "out_cubic"), (F(16), R2, "out_cubic"))
T2 = [F(20), F(22)]                                                                  # 2 -> 4 : 7 images, 2 i. d'écart
D2 = [Track((t0, 0), (t0 + F(3), 172, "inout_cubic"), (t0 + F(7), 240, BK6)) for t0 in T2]
r24 = [Track((t0 - F(3), R2), (t0, R2 * 0.95, "in_cubic"), (t0 + F(4), R4, "out_cubic")) for t0 in T2]
T3 = [F(29), F(27), F(28), F(30)]                                                    # 4 -> 8 : 5 images, du centre vers les bords
D3 = [Track((t0, 0), (t0 + F(5), 120, BK)) for t0 in T3]
r48 = [Track((t0, R4), (t0 + F(3), R8, "out_cubic")) for t0 in T3]
SNAP1 = first_snap(lambda t: 2 * D1(t), r12, F(10), F(20))
SNAP2 = [first_snap(lambda t, k=k: 2 * D2[k](t), r24[k], T2[k], T2[k] + F(7)) for k in range(2)]

# rangées 3.6 qui se déroulent depuis les bords (1 image par bulle) : (j, type, sens, départ)
ZIP = [(+1, "A", +1, F(31)), (-1, "A", -1, F(33)), (-2, "B", +1, F(35)), (+2, "B", -1, F(36))]
BREATH_ON = F(34)

# aspiration : le motif se tasse vers le centre (zoom radial), les bulles grossissent et fusionnent
s_in = Track((F(45), 1.0), (F(49), 1.04, "out_cubic"), (F(58), 0.0, "in_cubic"))   # grille -> masse
rm_in = Track((F(56), 270), (F(68), 60, "out_cubic"))                                # la masse se tasse dans le cercle
g_in = Track((F(49), 1.0), (F(58), 1.32, "in_cubic"), (F(68), 0.55, "inout_cubic"))
core = Track((F(51), 0), (F(58), 240, "out_cubic"), (F(66), 345, "out_back"))
iris = Track((F(54), 0), (F(59), 205, "out_expo"), (F(66), 347, "out_back"))
inhale = Track((F(63), 1.0), (F(67), 0.94, "inout_cubic"))
_cam = Track((F(66), 1.0), (F(88), 3.7, "plongee"))


def cam(t):
    return _cam(t) + drift(t, F(78), 0.5)


def axis_row(t):
    """La rangée de l'axe : 1 -> 2 -> 4 -> 8, chaque division plus rapide."""
    if t < F(10):
        r = r_pop(t)
        if F(6) < t:                                        # la tension vibre (4 px)
            r += 4 * prog(t, F(6), F(10)) * math.sin(2 * math.pi * 16 * t)
        sx = sx_ant(t) if t > F(7) else squash(t, F(4), F(8), 0.12)
        return [(CX, AXIS, r, sx, 0.0)]
    out = []
    for h, sgn in enumerate((-1, 1)):
        xh = CX + sgn * D1(t)
        sx_h = sx_ant(t) * vstretch(vel(D1, t)) * (squash(t, SNAP1, F(8), 0.16) if t >= SNAP1 else 1)
        if t < T2[h]:
            if T2[h] - F(3) < t:                            # anticipation de la division suivante
                sx_h *= 1 - 0.1 * prog(t, T2[h] - F(3), T2[h], "in_cubic")
            out.append((xh, AXIS, r12(t) if t < F(16) else r24[h](t), sx_h, 0.0))
            continue
        for c, sc in enumerate((-1, 1)):
            idx = 2 * h + c
            xc = X2[h] + sc * D2[h](t)
            sx_c = vstretch(vel(D2[h], t)) * (squash(t, SNAP2[h], F(8), 0.16) if t >= SNAP2[h] else 1)
            if t < T3[idx]:
                if T3[idx] - F(2) < t:
                    sx_c *= 1 - 0.08 * prog(t, T3[idx] - F(2), T3[idx], "in_cubic")
                out.append((xc, AXIS, r24[h](t) if t < T2[h] + F(4) else r48[idx](t), sx_c, 0.0))
                continue
            for sg in (-1, 1):
                xg = xc + sg * D3[idx](t)
                out.append((xg, AXIS, r48[idx](t), vstretch(vel(D3[idx], t)), 0.0))
    return out


def zip_row(t, j, typ, dirn, t0):
    """Rangée qui se déroule depuis un bord (cascade 3.5-02 accélérée : 1 image par bulle)."""
    xs = XA if typ == "A" else X8
    order = xs if dirn > 0 else xs[::-1]
    y = row_y(j)
    out = []
    for k, xk in enumerate(order):
        tb = t0 + k * F(1)
        if t < tb:
            break
        if k == 0 and typ == "A":                          # pop au bord, coupée à son milieu
            x_of = lambda tt, xk=xk: xk                     # noqa: E731
            r = R8 * ease("out_back_fort")(prog(t, tb, tb + F(4)))
        else:
            x0 = order[k - 1] if k > 0 else xk - dirn * PX
            x_of = lambda tt, x0=x0, xk=xk, tb=tb: lerp(x0, xk, BK(prog(tt, tb, tb + F(4))))  # noqa: E731
            r = R8 * (lerp(0.55, 1, prog(t, tb, tb + F(3), "out_cubic")) if k > 0 else 1)
        i = xs.index(xk)
        out.append((x_of(t), y, r * wave36(t, i, j, xk, max(tb + F(4), BREATH_ON)), vstretch(vel(x_of, t)), 0.0))
    return out


def pattern(t):
    """Toutes les rangées, avant l'aspiration."""
    ax = axis_row(t)
    if t >= F(32):                                         # la rangée de l'axe respire aussi
        ax = [(x, y, r * wave36(t, i, 0, x, BREATH_ON), sx, a) for i, (x, y, r, sx, a) in enumerate(ax)]
    rows = [ax]
    for j, typ, dirn, t0 in ZIP:
        if t >= t0:
            rows.append(zip_row(t, j, typ, dirn, t0))
    return rows


def mass_pos(x, y, s, rm):
    """Entre la grille (s = 1) et la masse (s = 0) : la grille est projetée sur un disque de rayon rm
    (carré -> disque), donc chaque bulle file le long de son rayon, en diagonale."""
    u, v = (x - CX) / 1000, (y - AXIS) / 400
    mx = CX + rm * u * math.sqrt(max(0.0, 1 - v * v / 2))
    my = AXIS + rm * v * math.sqrt(max(0.0, 1 - u * u / 2))
    return lerp(mx, x, s), lerp(my, y, s)


def squeeze(rows, t, s_fn, rm_fn, g, wob_amp):
    """Aspiration / explosion : position mélangée grille <-> masse, étirement le long de la vitesse."""
    out, n = [], 0
    dt = 0.008
    for row in rows:
        nr = []
        for x, y, r, sx, ang in row:
            n += 1
            px, py = mass_pos(x, y, s_fn(t), rm_fn(t))
            ax, ay = mass_pos(x, y, s_fn(t - dt), rm_fn(t - dt))
            bx, by = mass_pos(x, y, s_fn(t + dt), rm_fn(t + dt))
            sp = math.hypot(bx - ax, by - ay) / (2 * dt)
            if sp > 300:
                sx, ang = vstretch(sp, 7000), math.atan2(by - ay, bx - ax)
            wob = 1 + wob_amp * math.sin(2 * math.pi * (2.6 * t + 0.37 * n))
            nr.append((px, py, r * g * wob, sx, ang))
        out.append(nr)
    return out


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    rows = pattern(min(t, F(49)))
    if t > F(49):                                          # le motif ne bouge plus que par l'aspiration
        rows = [[(x, y, r * wave36(t, 0, 0, 0, 0, 0) * (1 + 0.1 * math.sin(2 * math.pi * 2.2 * t + x / 300)), sx, a)
                 for x, y, r, sx, a in row] for row in rows]
    if t > F(45):
        rows = squeeze(rows, t, s_in, rm_in, g_in(t), 0.12 * prog(t, F(52), F(56)))
    cam_k = cam(t)
    rg = iris(t) * inhale(t) * breathe(t, 0.012, 0.9) * cam_k
    d = blob(rows)
    rc = core(t)
    if rc > 1:
        d += " " + circ(CX, AXIS, min(rc * breathe(t, 0.02, 0.7), rg - 2 if rg > 300 else 1e9))
    covered = t > F(68)                                    # toutes les bosses sont rentrées
    if not covered:
        tracked = [(x, y) for row in rows[:1] for x, y, *_ in row[::2]] if t < F(30) else \
                  [(x, y) for row in rows[1:3] for x, y, *_ in (row[:1] + row[-1:])] if t > F(47) else []
        L.append({"k": "fill", "id": "bulles", "fill": ORANGE, "d": d, "pts": tracked, "ghost": t < F(30)})
    if rg > 1:
        if rg > 1180:
            L.append(video(0.7 * cam_k ** 0.5 + drift(t, F(54), 0.25), ghost=False))
        else:
            L.append(video(0.7 * cam_k ** 0.5 + drift(t, F(54), 0.25), circ(CX, AXIS, rg), vid="fenetre", ghost=t > F(70)))
    return L


# --------------------------------------------------------------- annotations intro
def a_pop(t):
    return "".join(arrow(CX + dx * 250, AXIS + dy * 200, CX + dx * 420, AXIS + dy * 330)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_split1(t):
    return arrow(CX - 120, 250, CX - 470, 250) + arrow(CX + 120, 250, CX + 470, 250)


def a_split8(t):
    return "".join(arrow(x - 40 * s, 360, x + 70 * s, 360) for x in X4 for s in (-1, 1))


def a_zip(t):
    return (arrow(80, row_y(1) + 120, 760, row_y(1) + 120) + arrow(W - 80, row_y(-1) - 120, W - 760, row_y(-1) - 120))


def a_aspire(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 470, CX + dx * 480, AXIS + dy * 280)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_plonge(t):
    return "".join(arrow(CX + dx * 480, AXIS + dy * 270, CX + dx * 880, AXIS + dy * 490)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(9), "Pop : la bulle éclot (+20 % puis retour), gonfle de 10 % en vibrant, puis se tasse à 84 % de large : elle va claquer.", "in_cubic", ann=a_pop),
    Beat(F(13), "Clac ! 1 -> 2 en 10 images : 4 images de col qui s'affine, rupture nette au centre, puis recul étiré à 130 %.", "inout_cubic", ann=a_split1, onion=2),
    Beat(F(22), "2 -> 4 en 7 images, la droite 2 images après la gauche : chaque division est plus rapide que la précédente.", "out_back", onion=2),
    Beat(F(30), "4 -> 8 en 5 images, du centre vers les bords. Les voisines se touchent et se relient : la rangée devient le motif 3.6.", "out_back", ann=a_split8, onion=1),
    Beat(F(40), "Les rangées du motif se déroulent depuis les bords, 1 image par bulle, en sens alternés. Les tailles ondulent (± 30 %).", "out_back", ann=a_zip, onion=0),
    Beat(F(54), "Aspiration en 9 images : chaque bulle file le long de son rayon vers le centre (diagonales), s'étire et fusionne.", "in_cubic", ann=a_aspire, onion=1),
    Beat(F(58), "Masse bosselée qui bout (± 12 %) ; la vidéo éclot en son cœur en 5 images et avale les bosses : reste un cercle propre.", "out_expo", onion=0),
    Beat(F(76), "Le cercle inspire (-6 %), puis plongée : zoom x3,7 depuis le centre ; la plaque verte zoome 2 fois moins vite.", "plongee", ann=a_plonge, onion=2),
])


# =================================================================== OUTRO (4,0 s)
w_close = Track((0, 1250), (F(12), 345, "emphase"))                  # la fenêtre recule
p_zoom = Track((0, 1.3), (F(12), 1.0, "out_cubic"), (F(22), 0.9, "linear"))
o_iris = Track((F(11), 345), (F(21), 0, "in_cubic"))                 # la vidéo se referme dans la masse
o_core = Track((F(10), 0), (F(11), 343), (F(22), 240, "inout_cubic"), (F(27), 215, "in_cubic"), (F(33), 0, "out_cubic"))
o_s = Track((F(27), 0.0), (F(39), 1.0, back_out(1.4)))                         # masse -> grille (explosion)
o_rm = Track((F(10), 60), (F(22), 270, "out_cubic"), (F(27), 228, "in_cubic"))  # bosses qui sortent, puis inspire
o_g = Track((F(10), 0.55), (F(22), 1.32, "out_cubic"), (F(39), 1.0, "out_cubic"))
O_BREATH = F(34)
# repli : chaque rangée se referme vers un bord comme une fermeture éclair (front qui accélère)
FOLD = {+1: (+1, F(50)), -1: (-1, F(51)), +2: (-1, F(52)), -2: (+1, F(53))}   # j : (sens de sortie, départ)
# rangée de l'axe : 8 -> 4 -> 2 -> points du logo
M84 = [F(55), F(54), F(54), F(55)]                                   # paires du centre d'abord (+1 image)
M42 = [F(60), F(61)]
T_DOTS = F(65)
LOGO_T0 = F(66)


def front_x(t, j):
    """Position du front de la fermeture : part du bord opposé et file vers la sortie (in_cubic)."""
    sens, t0 = FOLD[j]
    xs = XA if j % 2 else X8
    a, b = (xs[0] - 10, W + 200) if sens > 0 else (xs[-1] + 10, -200)
    return lerp(a, b, ease("in_cubic")(prog(t, t0, t0 + F(11))))


def fold_row(t, j):
    xs = XA if j % 2 else X8
    y = row_y(j)
    sens, t0 = FOLD[j]
    rows_b = []
    for i, x in enumerate(xs):
        rows_b.append((x, y, R8 * wave36(t, i, j, x, O_BREATH, 0.32), 1.0, 0.0))
    if t < t0:
        return rows_b
    fx = front_x(t, j)
    v = vel(lambda tt: front_x(tt, j), t)
    ahead = [b for b in rows_b if (b[0] - fx) * sens > 0]
    eaten = len(rows_b) - len(ahead)
    rf = R8 * min(1.35, 1 + 0.1 * eaten) * (1 - prog(t, t0 + F(8), t0 + F(11), "in_cubic"))
    return ahead + [(fx, y, rf, vstretch(v, 12000), 0.0)]


def axis_fold(t):
    """8 -> 4 -> 2 : les paires fusionnent (cacahuète, impact écrasé), de plus en plus gros."""
    out = []
    for h in range(2):
        if t >= M42[h]:
            u = prog(t, M42[h], M42[h] + F(4), "in_cubic")
            for c in range(2):
                idx = 2 * h + c
                x = lerp(X4[idx], X2[h], u)
                r = lerp(R4, R2, prog(t, M42[h] + F(2), M42[h] + F(6), "out_back"))
                sx = squash(t, M42[h] + F(4), F(8), 0.2) if u >= 1 else vstretch(vel(lambda tt, i=idx: lerp(X4[i], X2[h], prog(tt, M42[h], M42[h] + F(4), "in_cubic")), t))
                out.append((x, AXIS, r, sx, 0.0))
            continue
        for c in range(2):
            idx = 2 * h + c
            if t < M84[idx]:
                for s in range(2):
                    i = 2 * idx + s
                    out.append((X8[i], AXIS, R8 * wave36(t, i, 0, X8[i], O_BREATH, 0.32), 1.0, 0.0))
                continue
            u = prog(t, M84[idx], M84[idx] + F(4), "in_cubic")
            for s in range(2):
                i = 2 * idx + s
                x = lerp(X8[i], X4[idx], u)
                r = lerp(R8, R4, prog(t, M84[idx] + F(2), M84[idx] + F(5), "out_back"))
                sx = squash(t, M84[idx] + F(4), F(8), 0.2) if u >= 1 else 1 + 0.18 * u
                out.append((x, AXIS, r, sx, 0.0))
    return out


def dots_state(t):
    """Les deux dernières bulles filent vers les points du logo en rétrécissant (150 -> 11 px) et virent au blanc."""
    u = prog(t, T_DOTS, T_DOTS + F(8), "emphase")
    out = []
    for h, key in enumerate(("dot_g", "dot_d")):
        x = lerp(X2[h], LG[key][0], u)
        r = lerp(R2, LG["dot_r"], u) * (breathe(t, 0.2, 1.1, 0.25 * h) if u >= 1 else 1)
        sx = squash(t, T_DOTS + F(8), F(8), 0.25) if u >= 1 else 1 + 0.25 * math.sin(math.pi * u)
        out.append((x, AXIS, r, sx, 0.0))
    return out, mix_hex(ORANGE, WHITE, prog(t, T_DOTS + F(2), T_DOTS + F(7)))


def outro(t):
    L = []
    rw = w_close(t) * breathe(t, 0.01, 0.8)
    if t < F(11):
        L.append({"k": "bg", "v": "gradient"})
        if rw > 1180:
            L.append(video(p_zoom(t), ghost=False))
        else:
            L.append(video(p_zoom(t), circ(CX, AXIS, rw), ghost=True))
        return L
    L.append({"k": "bg", "v": "gradient"})
    if t < F(50):
        rows = [[(x, AXIS + j * PY, R8 * wave36(t, i, j, x, O_BREATH, 0.32), 1.0, 0.0)
                 for i, x in enumerate(XA if j % 2 else X8)] for j in (0, 1, -1, 2, -2)]
    else:
        rows = [axis_fold(t)] + [fold_row(t, j) for j in (1, -1, 2, -2) if t < FOLD[j][1] + F(11)]
    if t < F(40):
        rows = squeeze(rows, t, o_s, o_rm, o_g(t), 0.12 * (1 - prog(t, F(27), F(34))))
    d = blob(rows)
    rc = o_core(t)
    if rc > 1:
        d += " " + circ(CX, AXIS, rc * breathe(t, 0.02, 0.7))
    pts = [(x, y) for row in rows[1:3] for x, y, *_ in (row[:1] + row[-1:])] if t < F(44) else [(x, y) for x, y, *_ in rows[0]]
    L.append({"k": "fill", "id": "bulles", "fill": ORANGE, "d": d, "pts": pts if t < F(44) or t > F(53) else [],
              "ghost": t < F(24)})
    ri = o_iris(t)
    if ri > 1:
        L.append(video(p_zoom(t), circ(CX, AXIS, ri * breathe(t, 0.01, 0.8)), ghost=True))
    return L


def outro_dots(t):
    if t < T_DOTS:
        return []
    bubs, col = dots_state(t)
    return [{"k": "fill", "id": "points-logo", "fill": col, "d": blob([bubs]), "pts": [(b[0], b[1]) for b in bubs]}]


def outro_full(t):
    L = outro(t)
    if t >= T_DOTS:                                        # les deux dernières bulles sortent du calque commun
        for lay in L:
            if lay.get("id") == "bulles":
                rows = [axis_fold(t)] + [fold_row(t, j) for j in (1, -1, 2, -2) if t < FOLD[j][1] + F(11)]
                rows[0] = []
                lay["d"] = blob(rows)
        L = [x for x in L if not (x.get("id") == "bulles" and not x["d"].strip())]
    return L + (endcard(t, LOGO_T0, dots=False, extra=outro_dots(t)) if t >= LOGO_T0 else outro_dots(t))


# --------------------------------------------------------------- annotations outro
def a_recule(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 500, CX + dx * 560, AXIS + dy * 320)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_inspire(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 330, CX + dx * 360, AXIS + dy * 230)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_explose(t):
    return "".join(arrow(CX + dx * 380, AXIS + dy * 230, CX + dx * 720, AXIS + dy * 440)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_fold(t):
    return (arrow(700, row_y(1) + 110, 1500, row_y(1) + 110) + arrow(W - 700, row_y(-1) - 110, 420, row_y(-1) - 110))


def a_merge(t):
    return "".join(arrow(x - 150 * s, 380, x - 40 * s, 380) for x in X2 for s in (-1, 1))


def a_dots(t):
    return arrow(380, 420, 640, 520) + arrow(W - 380, 420, W - 640, 520)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(6), "La fenêtre recule : le plein cadre se rétracte en cercle en 12 images (emphase), le dégradé revient par les 4 coins.", "emphase", ann=a_recule, onion=2),
    Beat(F(18), "Des bosses orange poussent autour du cercle, puis la vidéo se referme au centre : il reste une masse bosselée.", "in_cubic", onion=0),
    Beat(F(26), "La masse bout (chaque bosse pulse ± 12 %), puis inspire : -15 % en 5 images. Ça va sauter.", "in_cubic", ann=a_inspire, onion=0),
    Beat(F(30), "Explosion : le motif 3.6 jaillit en 12 images le long des rayons, bulles étirées dans le sens de la vitesse, +7 % puis retour.", "out_back", ann=a_explose, onion=1),
    Beat(F(46), "Le motif respire : les tailles ondulent de ± 32 %, en vague de gauche à droite (charte 3.6). Rien n'est tenu.", "inout_cubic", onion=0),
    Beat(F(56), "Repli : chaque rangée se referme vers un bord comme une fermeture éclair qui accélère ; sur l'axe, 8 -> 4.", "in_cubic", ann=a_fold, onion=0),
    Beat(F(66), "4 -> 2, puis les deux bulles filent vers les points du logo en rétrécissant (150 -> 11 px) et virent au blanc.", "emphase", ann=a_dots, onion=2),
    Beat(F(94), "Carton 3.4-02 : « sfeer » s'ouvre depuis le centre, l'arabe de droite à gauche ; points qui respirent, poussée de 7,5 %/s.", "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "C'est ton croquis dans l'ordre : pop, haltère, motif, masse noire, cercle. La masse devient orange, la couleur de la charte.",
        "1 -> 2 -> 4 -> 8 de plus en plus vite : on sent la multiplication des points, sans chiffre ni compteur.",
        "La fenêtre est un simple cercle : elle marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "L'haltère était vertical sur ton croquis : il est couché sur l'axe, et toutes les divisions se font en horizontal.",
        "Le motif garde les rangées horizontales du 3.6 ; les rangées naissent en glissant le long de leur ligne, jamais du haut ou du bas.",
        "Aspiration et explosion en zoom radial depuis le centre (diagonales). Masse et cercle restent orange et vert, sans contour.",
    ]),
    ("Mouvement", [
        "Rampe : 10, 7, 5 images par division, puis 1 image par bulle. Chaque claquement = col qui casse, recul étiré, écrasement.",
        "Wow intro : le claquement du pop, puis l'aspiration. Wow outro : l'explosion du motif hors de la masse.",
        "Jamais figé : vibration, vague 3.6, masse qui bout, plaque qui zoome, carton qui pousse. 2 images d'écart entre paires.",
    ]),
]
