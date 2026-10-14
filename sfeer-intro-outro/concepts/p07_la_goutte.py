"""Piste 7 (croquis de la DA) : « La goutte ».

Un point éclot à gauche et se divise en cascade (3.5-02) ; la bulle du milieu bourgeonne en
diagonale : une molécule de 7 bulles en rangées autour de l'axe (3.6), qui palpite. La bulle
centrale aspire les autres une à une le long des cols (gorgées visibles, rythme qui accélère),
enfle, et son cou file hors cadre à droite : c'est la goutte du gabarit portrait de la charte
(sfeer_svg.drop_d, reach 0 -> 1). La vidéo éclot dans la goutte, et l'on plonge vers elle,
décentrée à gauche. L'outro : la goutte recule, la vidéo repart par le cou, le cou revient du
hors-champ et tire la goutte, qui se redivise en molécule, puis se replie en deux points.

Toutes les formes sont tracées dans le sens horaire : une union de cercles et de cols dans un seul
tracé reste pleine. Les cols en diagonale sont des cols de la charte tournés autour de leur bulle.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, back_out, breathe, ease, green_plate, lerp, prog  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, curved_arrow, drop_d,  # noqa: E402
                       f, mix_hex)

CX = W / 2

META = {
    "id": "p07_la_goutte",
    "num": "P7",
    "title": "La goutte",
    "principe": "Une molécule de bulles se vide dans une seule goutte dont le cou file hors cadre : la goutte est la fenêtre.",
    "logline": "Piste 7 de la DA. Un point se multiplie en molécule qui palpite ; la bulle du centre aspire toutes "
               "les autres, enfle en goutte dont le cou file hors cadre à droite. La vidéo éclot dedans, on plonge.",
}


# =================================================================== géométrie (sens horaire partout)
def circ(x, y, r):
    return f"M{f(x - r)} {f(y)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ell(x, y, rx, ry, ang=0.0):
    """Ellipse à volume constant, grand axe orienté selon ang (radians)."""
    c, s = math.cos(ang), math.sin(ang)
    x0, y0, x1, y1 = x - rx * c, y - rx * s, x + rx * c, y + rx * s
    deg = f(math.degrees(ang))
    return (f"M{f(x0)} {f(y0)}A{f(rx)} {f(ry)} {deg} 1 1 {f(x1)} {f(y1)}"
            f"A{f(rx)} {f(ry)} {deg} 1 1 {f(x0)} {f(y0)}Z")


def hull(x1, r1, x2, r2, y):
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, y - r1 * ny), (x2 + r2 * nx, y - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, y + r2 * ny), (x1 + r1 * nx, y + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def fillet_h(d, r1, r2):
    """Col de la charte : congé de rayon constant R = 0,91 r moyen ; rupture à 3,36 r. None = rompu."""
    rm = (r1 + r2) / 2
    rf = 0.91 * rm
    v = (rm + rf) ** 2 - d * d / 4
    if v <= rf * rf:
        return None
    return math.sqrt(v) - rf


def link(x1, r1, x2, r2, y, h):
    """Pont de la charte entre deux cercles d'une même ligne (cacahuète, col ou fusion)."""
    if x2 < x1:
        x1, r1, x2, r2 = x2, r2, x1, r1
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        return circ(x1, y, r1) if r1 >= r2 else circ(x2, y, r2)
    rmin = min(r1, r2)
    if d < r1 + r2:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        h = max(h, math.sqrt(max(r1 * r1 - a * a, 0)) + 0.5)
    if h >= 0.97 * rmin or _neck_circle((x1, y, r1), (x2, y, r2), h) is None:
        return hull(x1, r1, x2, r2, y)
    return bridge_d((x1, y, r1), (x2, y, r2), h)


_TOK = re.compile(r"[A-Za-z]|-?\d*\.?\d+")


def rot_path(d, ox, oy, ang):
    """Tourne un tracé (M, L, A, a, Z) autour de (ox, oy). Les arcs de cercle restent des arcs de cercle."""
    c, s = math.cos(ang), math.sin(ang)
    deg = math.degrees(ang)
    toks, out, i, cmd = _TOK.findall(d), [], 0, None
    while i < len(toks):
        tk = toks[i]
        if tk.isalpha():
            cmd = tk
            out.append(tk)
            i += 1
            continue
        if cmd in ("M", "L"):
            x, y = float(toks[i]) - ox, float(toks[i + 1]) - oy
            out.append(f"{f(ox + x * c - y * s)} {f(oy + x * s + y * c)}")
            i += 2
        elif cmd in ("A", "a"):
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            x, y = float(x), float(y)
            if cmd == "A":
                x, y = x - ox, y - oy
                X, Y = ox + x * c - y * s, oy + x * s + y * c
            else:
                X, Y = x * c - y * s, x * s + y * c
            out.append(f"{rx} {ry} {f(float(rot) + deg)} {la} {sw} {f(X)} {f(Y)}")
            i += 7
        else:
            i += 1
    return " ".join(out)


def link_any(x1, y1, r1, x2, y2, r2, h):
    """Col de la charte entre deux bulles quelconques (rangée ou diagonale de la molécule)."""
    d, ang = math.hypot(x2 - x1, y2 - y1), math.atan2(y2 - y1, x2 - x1)
    if abs(ang) < 1e-6:
        return link(x1, r1, x2, r2, y1, h)
    return rot_path(link(x1, r1, x1 + d, r2, y1, h), x1, y1, ang)


def blob(bubs, necks, extra=()):
    """bubs : {nom: (x, y, r, sx, ang)} ; necks : [(a, b, h)] avec h = None -> col de la charte.
    Les cols s'accrochent au cercle intérieur, l'ellipse étirée se superpose (même sens de tracé)."""
    parts = []
    for a, b, h in necks:
        if a not in bubs or b not in bubs:
            continue
        xa, ya, ra, sxa, _ = bubs[a]
        xb, yb, rb, sxb, _ = bubs[b]
        ca, cb = ra * min(sxa, 1 / sxa), rb * min(sxb, 1 / sxb)
        if ca < 1 or cb < 1:
            continue
        hh = fillet_h(math.hypot(xb - xa, yb - ya), ca, cb) if h is None else h
        if hh is not None:
            parts.append(link_any(xa, ya, ca, xb, yb, cb, hh))
    for x, y, r, sx, ang in list(bubs.values()) + list(extra):
        if r >= 0.5:
            parts.append(ell(x, y, r * sx, r / sx, ang) if abs(sx - 1) > 2e-3 else circ(x, y, r))
    return " ".join(parts)


def vel2(fn, t, dt=0.008):
    (ax, ay), (bx, by) = fn(t - dt), fn(t + dt)
    return math.hypot(bx - ax, by - ay) / (2 * dt), math.atan2(by - ay, bx - ax)


def vstretch(v, k=9000.0, cap=1.28):
    return min(cap, 1 + abs(v) / k)


def window(clip_d, iris, zoom, uid="fenetre"):
    """Fenêtre : plaque verte découpée par la goutte ET par le disque iris (cx, r) qui s'ouvre."""
    s = f'<clipPath id="{uid}-c"><path d="{clip_d}"/></clipPath>'
    inner = green_plate(zoom, uid=uid)
    if iris is not None:
        s += f'<clipPath id="{uid}-i"><circle cx="{f(iris[0])}" cy="{AXIS}" r="{f(max(iris[1], 0.1))}"/></clipPath>'
        inner = f'<g clip-path="url(#{uid}-i)">{inner}</g>'
    return {"k": "raw", "svg": s + f'<g id="{uid}" clip-path="url(#{uid}-c)">{inner}</g>'}


BK = back_out(0.9)        # dépassement 3 %
BK1 = back_out(0.4)       # dépassement 1 % : le col de la cascade tient
BK6 = back_out(1.7)       # dépassement 10 %

# =================================================================== la molécule (rangées autour de l'axe, 3.6)
R0, PX, PY = 85, 280, 233                 # axe à 3,3 r (pose de la charte), diagonales à 3,2 r
XA = 720                                                   # la future goutte, décentrée à gauche
POS = {"L": (XA - PX, AXIS), "A": (XA, AXIS), "R": (XA + PX, AXIS),
       "UL": (XA - PX / 2, AXIS - PY), "UR": (XA + PX / 2, AXIS - PY),
       "DL": (XA - PX / 2, AXIS + PY), "DR": (XA + PX / 2, AXIS + PY)}
NECKS = [("L", "A", None), ("A", "R", None), ("A", "UL", None), ("A", "UR", None), ("A", "DL", None),
         ("A", "DR", None)]                                # rayons depuis le centre : chaque col garde r1 + r2 constant
SIGN = {"A": 1, "L": -1, "R": -1, "UL": -1, "UR": -1, "DL": -1, "DR": -1}   # le centre gonfle quand les autres dégonflent


def palp(t, name, x, t_on, amp=0.28, t_off=None):
    """Charte 3.6 : la molécule palpite (gros + petit = constant), légère vague de gauche à droite.
    Tout le monde s'arrête ensemble (t_off) pour que les cols tiennent."""
    a = amp * prog(t, t_on, t_on + F(6), "out_cubic")
    if t_off is not None:
        a *= 1 - prog(t, t_off, t_off + F(4), "inout_cubic")
    return 1 + a * SIGN[name] * math.sin(2 * math.pi * 2.2 * (t - x / W * F(3)))


def dir_to(a, b):
    return math.atan2(b[1] - a[1], b[0] - a[0])


# =================================================================== INTRO (4,0 s)
rL_pop = Track((0, 0), (F(5), R0, "out_back_fort"))
xL = Track((F(5), POS["L"][0]), (F(8), POS["L"][0] - 9, "out_cubic"), (F(13), POS["L"][0], "out_back"))  # ancre qui recule
sxL = Track((F(5), 1.0), (F(8), 0.86, "in_cubic"), (F(11), 1.0, "out_cubic"))       # se tasse avant de se diviser
xA_birth = Track((F(8), POS["L"][0]), (F(15), XA, BK1))                             # 3.5-02 : A naît de L
xR_birth = Track((F(12), XA), (F(18), XA + PX, BK1))                                 # puis R naît de A (4 i. de chevauchement)
BUDS = {"UR": F(18), "DL": F(20), "UL": F(21), "DR": F(23)}                        # bourgeons en diagonale, décalés
PALP_ON = F(24)
PALP_OFF = F(33)
GULP = {"L": (F(36), F(5)), "UL": (F(40), F(4)), "DL": (F(43), F(4)), "UR": (F(45), F(3)), "DR": (F(47), F(3))}
GAIN = {"L": 50, "UL": 34, "DL": 29, "UR": 25, "DR": 22}                           # A grossit à chaque gorgée
FLING = Track((F(50), 0.0), (F(56), 0.55, "in_cubic"), (F(59), 1.0, "out_cubic"))  # le cou file hors cadre (rampe)
rA_end = Track((F(50), 0), (F(58), 75, "out_back"))
iris_in = Track((F(54), 0), (F(63), 1500, "out_expo"))
_cam = Track((F(59), 1.0), (F(63), 0.92, "inout_cubic"), (F(80), 4.8, "plongee"))   # inspire, puis plonge
DROP_R, DROP_X2, DROP_R2, DROP_H = 320, 2500, 272, 51.2                              # = drop_d(720, 540, 320, reach=1)


def cam(t):
    return _cam(t) + drift(t, F(80), 0.5)


def rA_of(t):
    r = R0
    for k, (tg, dur) in GULP.items():
        r += GAIN[k] * ease("out_back")(prog(t, tg + dur - F(1), tg + dur + F(3)))
    return r + rA_end(t)


def a_squash(t):
    """A s'étire dans la direction de la dernière gorgée, puis revient sur un ressort."""
    best = None
    for k, (tg, dur) in GULP.items():
        if t >= tg + dur:
            best = (tg + dur, dir_to(POS["A"], POS[k]))
    if best is None:
        return 1.0, 0.0
    return squash(t, best[0], F(8), 0.18), best[1]


def sat_state(t, k):
    """Bulle satellite : naissance, palpitation, gorgée (gonfle, file le long du col, s'étire)."""
    x0, y0 = POS[k]
    if k in BUDS:
        tb = BUDS[k]
        if t < tb:
            return None
        u = BK6(prog(t, tb, tb + F(5)))
        x, y = lerp(XA, x0, u), lerp(AXIS, y0, u)
        r = R0 * lerp(0.55, 1, prog(t, tb, tb + F(4), "out_cubic"))
        sp, ang = vel2(lambda tt: (lerp(XA, x0, BK6(prog(tt, tb, tb + F(5)))), lerp(AXIS, y0, BK6(prog(tt, tb, tb + F(5))))), t)
        sx = vstretch(sp)
    elif k == "L":
        x, y, r, sx, ang = xL(t), AXIS, rL_pop(t), sxL(t) if t > F(5) else squash(t, F(4), F(8), 0.12), 0.0
    if k in GULP:
        r *= palp(t, k, x0, PALP_ON, t_off=PALP_OFF)
        tg, dur = GULP[k]
        if t >= tg + dur:
            return None
        if tg - F(2) <= t < tg:
            r *= 1 + 0.1 * prog(t, tg - F(2), tg, "out_cubic")              # gonfle avant d'être bue
        if t >= tg:
            fn = lambda tt: (lerp(x0, XA, ease("emphase")(prog(tt, tg, tg + dur))), lerp(y0, AXIS, ease("emphase")(prog(tt, tg, tg + dur))))  # noqa: E731
            x, y = fn(t)
            u = prog(t, tg, tg + dur)
            r = R0 * palp(tg, k, x0, PALP_ON, t_off=PALP_OFF) * 1.1 * (1 - 0.5 * u)
            sp, ang = vel2(fn, t)
            sx = vstretch(sp, 7000, 1.25)
    return (x, y, r, sx, ang if sx > 1.002 else 0.0)


def beads(t):
    """Gorgées : une perle de matière traverse le col vers A juste avant chaque aspiration."""
    out = []
    for k, (tg, dur) in GULP.items():
        u = prog(t, tg - F(4), tg)
        if 0 < u < 1:
            (x0, y0), (x1, y1) = POS[k], POS["A"]
            e = ease("in_cubic")(u)
            out.append((lerp(x0, x1, 0.25 + 0.6 * e), lerp(y0, y1, 0.25 + 0.6 * e), R0 * 0.42 * math.sin(math.pi * u) + 6, 1.0, 0.0))
    return out


def tail_state(t, rA):
    """R : naît de A, reste accrochée pendant que A enfle, puis file hors cadre (la queue de la goutte)."""
    if t < F(12):
        return None
    x_rest = XA + rA + PX - R0 if t >= F(36) else xR_birth(t)
    r = R0 * palp(t, "R", XA + PX, PALP_ON, t_off=PALP_OFF)
    u = FLING(t)
    x = lerp(x_rest if u <= 0 else XA + rA_of(F(50)) + PX - R0, DROP_X2, u)
    return (x, AXIS, lerp(r, DROP_R2, u ** 2), 1.0, 0.0), u


def drop_path(t):
    """La goutte : A + col vers R. Après la rampe, c'est exactement drop_d(720, 540, 320, reach=1)."""
    rA = rA_of(t)
    if FLING(t) >= 1:
        return drop_d(XA, AXIS, DROP_R, "right", reach=1.0), rA
    (xr, yr, rr, _, _), u = tail_state(t, rA)
    xa = XA - 22 * math.sin(math.pi * prog(t, F(50), F(58)))         # recul de A quand la queue part (action-réaction)
    h0 = min(0.9 * rr, 0.9 * R0)
    d = link(xa, rA, xr, rr, AXIS, lerp(h0, DROP_H, u))
    sq, sang = a_squash(t)
    if abs(sq - 1) > 2e-3:                                             # impact de la dernière gorgée
        d += " " + ell(xa, AXIS, rA * sq, rA / sq, sang)
    return d, rA


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(50):
        rA = rA_of(t)
        bubs = {}
        if t < F(8):
            bubs["L"] = sat_state(t, "L")
        else:
            l = sat_state(t, "L")
            if l:
                bubs["L"] = l
            fnA = lambda tt: (xA_birth(tt), AXIS)                        # noqa: E731
            sp, _ = vel2(fnA, t)
            sq, sang = a_squash(t)
            ra = rA * palp(t, "A", XA, PALP_ON, t_off=PALP_OFF)
            bubs["A"] = (xA_birth(t), AXIS, ra, vstretch(sp) if t < F(16) else sq, 0.0 if t < F(16) else sang)
            ts = tail_state(t, rA)
            if ts:
                bubs["R"] = ts[0]
            for k in BUDS:
                s = sat_state(t, k)
                if s:
                    bubs[k] = s
        d = blob(bubs, NECKS, beads(t))
        pts = [(b[0], b[1]) for k, b in bubs.items() if k not in ("A", "R") and (t < F(30) or t >= GULP[k][0] - F(1))]
        L.append({"k": "fill", "id": "molecule", "fill": ORANGE, "d": d, "pts": pts, "ghost": t < F(34) or t > F(48)})
        return L
    k = cam(t)
    dp, rA = drop_path(t)
    if FLING(t) >= 1 and abs(k - 1) > 5e-4:                              # plongée : zoom centré sur la goutte
        dp = bridge_d((XA, AXIS, DROP_R * k), (XA + (DROP_X2 - XA) * k, AXIS, DROP_R2 * k), DROP_H * k)
    if FLING(t) >= 1:                                                     # la queue a claqué : la goutte vibre
        sq = squash(t, F(58), F(14), 0.09)
        dp += " " + ell(XA, AXIS, DROP_R * k * sq, DROP_R * k / sq)
    zoom = 0.75 * k ** 0.5 + drift(t, F(56), 0.2)
    ri = iris_in(t)
    if k < 4.3:
        sq, sang = a_squash(t)
        L.append({"k": "fill", "id": "goutte", "fill": ORANGE, "d": dp, "pts": [], "ghost": k > 1.2 or FLING(t) < 1})
        if ri > 1:
            L.append(window(dp, (XA, ri * k) if ri < 1500 else None, zoom))
    else:
        L.append(video(zoom, ghost=False))
    return L


# --------------------------------------------------------------- annotations intro
def a_cascade(t):
    return arrow(POS["L"][0] + 60, 380, XA + 40, 380) + arrow(POS["L"][0] - 40, 700, POS["L"][0] - 110, 700)


def a_buds(t):
    return "".join(arrow(XA + dx * 70, AXIS + dy * 110, XA + dx * 200, AXIS + dy * 300) for dx in (-1, 1) for dy in (-1, 1))


def a_gulp(t):
    return "".join(arrow(POS[k][0] + (POS[k][0] - XA) * 0.6, POS[k][1] + (POS[k][1] - AXIS) * 0.6,
                         POS[k][0] + (XA - POS[k][0]) * 0.1, POS[k][1] + (AXIS - POS[k][1]) * 0.1)
                   for k in ("L", "UL", "DL"))


def a_gulp2(t):
    return "".join(arrow(POS[k][0] + (POS[k][0] - XA) * 0.9, POS[k][1] + (POS[k][1] - AXIS) * 0.9,
                         POS[k][0] + (POS[k][0] - XA) * 0.35, POS[k][1] + (POS[k][1] - AXIS) * 0.35)
                   for k in ("UR", "DR"))


def a_fling(t):
    return arrow(1300, 300, 1860, 300) + arrow(1300, 780, 1860, 780)


def a_plonge(t):
    return "".join(arrow(XA + dx * 420, AXIS + dy * 300, XA + dx * (700 if dx < 0 else 1100), AXIS + dy * 500)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(11), "Un point éclot à gauche (+20 %), recule de 9 px et se divise : cascade 3.5-02, la 2e bulle file vers la droite.", "out_back", ann=a_cascade, onion=2),
    Beat(F(17), "La 3e bulle naît de la 2e, 4 images après : rangée de 3 reliée par les cols de la charte (écart 3,3 r).", "out_back", onion=2),
    Beat(F(22), "La bulle du milieu bourgeonne en diagonale : 4 bulles jaillissent (+10 %), 1 à 2 images d'écart entre elles.", "out_back", ann=a_buds, onion=1),
    Beat(F(32), "La molécule palpite (charte 3.6) : le centre gonfle quand les 6 autres dégonflent (± 28 %), les cols tiennent.", "inout_cubic", onion=0),
    Beat(F(38), "Aspiration : une perle traverse le col, la bulle gonfle (+10 %), puis file dans le cou et s'étire vers le centre.", "in_cubic", ann=a_gulp, onion=1),
    Beat(F(46), "Gorgées de plus en plus rapides (5, 4, 4, 3, 3 images) ; la bulle centrale passe de 85 à 245 px.", "in_cubic", ann=a_gulp2, onion=0),
    Beat(F(55), "Le cou file hors cadre à droite en 9 images (accélère, puis freine hors champ) : la goutte de la charte. La vidéo éclot dedans.", "in_cubic", ann=a_fling, onion=2, onion_dt=F(1)),
    Beat(F(68), "La goutte vibre, inspire (-8 %), puis plongée : zoom x4,8 centré sur elle, décentrée à gauche ; la plaque zoome 2 fois moins vite.", "plongee", ann=a_plonge, onion=2),
])


# =================================================================== OUTRO (4,0 s)
o_cam = Track((0, 4.8), (F(14), 1.0, "emphase"))
o_zoom = Track((0, 1.4), (F(14), 1.0, "out_expo"), (F(22), 0.9, "out_cubic"))
o_iris = Track((F(10), 0.0), (F(21), 1.0, "emphase"))            # la vidéo repart par le cou
o_neck = Track((F(16), 1.0), (F(28), 0.0, "out_cubic"))            # le cou revient du hors-champ (élastique)
o_xA = Track((F(19), XA), (F(30), CX, "out_back"))                  # la goutte est tirée (3 i. de retard)
o_rA = Track((F(16), DROP_R), (F(30), 200, "inout_cubic"), (F(34), 186, "in_cubic"), (F(41), R0, "out_cubic"))
O_HIT = F(28)
OPOS = {k: (x - XA + CX, y) for k, (x, y) in POS.items()}         # la molécule se reforme autour du centre
BURST = {"L": F(34), "UR": F(35), "DL": F(36), "UL": F(37), "DR": F(38)}
O_PALP = F(40)
FOLD = {"UL": ("L", F(50), F(4)), "DR": ("R", F(51), F(4)), "DL": ("L", F(52), F(3)), "UR": ("R", F(53), F(3))}
DRAIN = Track((F(55), 1.0), (F(60), 0.0, "out_cubic"))              # A se vide dans L et R
T_DOTS = F(60)
LOGO_T0 = F(62)


def o_side(t, k):
    """L ou R : grossit à chaque gorgée et quand A se vide, puis file vers un point du logo."""
    gain = sum(18 * ease("out_back")(prog(t, t0 + d - F(1), t0 + d + F(3))) for s, (to, t0, d) in FOLD.items() if to == k)
    gain += 16 * (1 - DRAIN(t))
    x0 = OPOS[k][0]
    r = (R0 + gain) * palp(t, k, x0, O_PALP, 0.24, F(46))
    return x0, r


def outro_bubs(t):
    """Molécule de l'outro (après l'impact) : A, R, puis L et les bourgeons qui jaillissent."""
    xa = o_xA(t)
    bubs = {}
    sx_hit = squash(t, O_HIT, F(8), 0.2)
    sx_ant = 1 - 0.12 * math.sin(math.pi * prog(t, F(30), F(34)))
    ra = o_rA(t) * palp(t, "A", CX, O_PALP, 0.24, F(46)) * DRAIN(t)
    bubs["A"] = (xa, AXIS, ra, sx_hit * sx_ant, 0.0)
    for k in ("L", "R"):
        if k == "L" and t < BURST["L"]:
            continue
        x, r = o_side(t, k)
        if k == "L":
            u = BK1(prog(t, BURST["L"], BURST["L"] + F(5)))
            x = lerp(xa, x, u)
            r *= lerp(0.6, 1, prog(t, BURST["L"], BURST["L"] + F(4), "out_cubic"))
        bubs[k] = (x, AXIS, r, sx_hit if k == "R" else 1.0, 0.0)
    for k in ("UL", "UR", "DL", "DR"):
        tb = BURST[k]
        if t < tb:
            continue
        x0, y0 = OPOS[k]
        to, tg, dur = FOLD[k]
        if t >= tg + dur:
            continue
        fn = lambda tt, x0=x0, y0=y0, tb=tb: (lerp(xa, x0, BK6(prog(tt, tb, tb + F(5)))), lerp(AXIS, y0, BK6(prog(tt, tb, tb + F(5)))))  # noqa: E731
        x, y = fn(t)
        r = R0 * lerp(0.6, 1, prog(t, tb, tb + F(4), "out_cubic")) * palp(t, k, x0, O_PALP, 0.24, F(46))
        sp, ang = vel2(fn, t)
        if t >= tg:                                                    # repli : bu par L ou R, en diagonale
            tx, ty = OPOS[to]
            fg = lambda tt, x0=x0, y0=y0, tx=tx, ty=ty, tg=tg, dur=dur: (lerp(x0, tx, ease("emphase")(prog(tt, tg, tg + dur))), lerp(y0, ty, ease("emphase")(prog(tt, tg, tg + dur))))  # noqa: E731
            x, y = fg(t)
            r = R0 * (1.08 - 0.55 * prog(t, tg, tg + dur))
            sp, ang = vel2(fg, t)
        sx = vstretch(sp, 6000, 1.35)
        bubs[k] = (x, y, r, sx, ang if sx > 1.002 else 0.0)
    return bubs


def o_beads(t):
    """Quand A se vide : deux perles filent dans les cols vers L et R."""
    u = prog(t, F(54), F(59))
    if not 0 < u < 1:
        return []
    out = []
    for k in ("L", "R"):
        x1 = OPOS[k][0]
        out.append((lerp(CX, x1, 0.2 + 0.7 * ease("out_cubic")(u)), AXIS, R0 * 0.33 * math.sin(math.pi * u) + 6, 1.0, 0.0))
    return out


def dots_state(t):
    u = prog(t, T_DOTS, T_DOTS + F(8), "emphase")
    out = {}
    for k, key in (("L", "dot_g"), ("R", "dot_d")):
        x0, r0 = o_side(T_DOTS, k)
        x = lerp(x0, LG[key][0], u)
        r = lerp(r0, LG["dot_r"], u) * (breathe(t, 0.2, 1.1, 0.25 * (k == "R")) if u >= 1 else 1)
        sx = squash(t, T_DOTS + F(8), F(8), 0.25) if u >= 1 else 1 + 0.15 * math.sin(math.pi * u)
        out[k] = (x, AXIS, r, sx, 0.0)
    return out, mix_hex(ORANGE, WHITE, prog(t, T_DOTS + F(2), T_DOTS + F(7)))


def outro_drop(t):
    """La goutte de l'outro : zoom arrière, puis le cou revient et tire la goutte (étirée par la vitesse)."""
    k, u = o_cam(t), o_neck(t)
    if u >= 1:
        dp = bridge_d((XA, AXIS, DROP_R * k), (XA + (DROP_X2 - XA) * k, AXIS, DROP_R2 * k), DROP_H * k)
        return dp, [(XA, AXIS)]
    xa, ra = o_xA(t), o_rA(t)
    xr = lerp(xa + PX, DROP_X2, u)
    rr = lerp(R0, DROP_R2, u ** 2)
    sp, _ = vel2(lambda tt: (o_xA(tt), AXIS), t)
    sxa = vstretch(sp, 5000, 1.25)
    d = link(xa, ra / sxa ** 0.5, xr, rr, AXIS, lerp(0.9 * R0, DROP_H, u)) + " " + ell(xa, AXIS, ra * sxa, ra / sxa)
    return d, [(xa, AXIS), (xr, AXIS)]


def fold_necks(t):
    """Repli : le col vers le centre casse net (rupture), un col se forme vers la bulle de l'axe qui boit."""
    out = []
    for a, b, h in NECKS:
        k = b if a == "A" else None
        if k in FOLD and t >= FOLD[k][1] - F(1):
            continue
        out.append((a, b, h))
    return out + [(k, to, None) for k, (to, tg, _) in FOLD.items() if t >= tg - F(1)]


def outro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < O_HIT:
        zoom = o_zoom(t)
        if o_cam(t) > 4.3:
            L.append(video(zoom, ghost=False))
            return L
        dp, pts = outro_drop(t)
        L.append({"k": "fill", "id": "goutte", "fill": ORANGE, "d": dp, "pts": pts, "ghost": True})
        v = o_iris(t)
        if v < 1:
            iris = None if v <= 0 else (lerp(XA, 2700, v), lerp(1500, 120, v))
            L.append(window(dp, iris, zoom))
        return L
    bubs = outro_bubs(t)
    if t >= T_DOTS:
        bubs.pop("L", None)
        bubs.pop("R", None)
    d = blob(bubs, fold_necks(t), o_beads(t))
    pts = [(b[0], b[1]) for kk, b in bubs.items() if kk != "A"]
    if d.strip():
        L.append({"k": "fill", "id": "molecule", "fill": ORANGE, "d": d, "pts": pts, "ghost": t < F(44) or t > F(49)})
    return L


def outro_dots(t):
    if t < T_DOTS:
        return []
    bubs, col = dots_state(t)
    return [{"k": "fill", "id": "points-logo", "fill": col, "d": blob(bubs, []), "pts": [(b[0], b[1]) for b in bubs.values()]}]


def outro_full(t):
    L = outro(t)
    return L + (endcard(t, LOGO_T0, dots=False, extra=outro_dots(t)) if t >= LOGO_T0 else outro_dots(t))


# --------------------------------------------------------------- annotations outro
def a_recule(t):
    return "".join(arrow(XA + dx * 900, AXIS + dy * 500, XA + dx * 560, AXIS + dy * 330)
                   for dx in (-1, 1) for dy in (-1, 1) if XA + dx * 900 > -50)


def a_vidange(t):
    return arrow(900, 160, 1700, 160) + arrow(900, 920, 1700, 920)


def a_tire(t):
    return arrow(1880, 300, 1300, 300) + arrow(700, 300, 960, 300)


def a_burst(t):
    return "".join(arrow(CX + dx * 70, AXIS + dy * 110, CX + dx * 200, AXIS + dy * 300) for dx in (-1, 1) for dy in (-1, 1)) + \
        arrow(CX - 120, AXIS - 140, CX - 300, AXIS - 140)


def a_fold(t):
    return "".join(arrow(OPOS[k][0] + (OPOS[k][0] - OPOS[to][0]) * 0.4, OPOS[k][1] + (OPOS[k][1] - AXIS) * 0.45,
                         OPOS[to][0] + (OPOS[k][0] - OPOS[to][0]) * 0.35, AXIS + (OPOS[k][1] - AXIS) * 0.35)
                   for k, (to, _, _) in FOLD.items())


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(6), "La goutte recule : zoom arrière x4,8 -> x1 en 14 images, centré sur elle ; le dégradé revient d'abord à gauche.", "emphase", ann=a_recule, onion=2),
    Beat(F(15), "La vidéo repart par le cou : le disque vert glisse vers la droite et sort du cadre en 11 images.", "in_cubic", ann=a_vidange, onion=0),
    Beat(F(24), "Le cou revient du hors-champ comme un élastique et tire la goutte vers le centre, 3 images après : elle s'étire.", "in_cubic", ann=a_tire, onion=2),
    Beat(F(31), "Impact : la goutte s'écrase (120 % de large), revient sur un ressort, puis inspire (-12 %).", "ressort_vif", onion=1),
    Beat(F(38), "Elle se redivise : 5 bulles jaillissent, 1 image d'écart entre chacune, 4 en diagonale et 1 sur l'axe.", "out_back", ann=a_burst, onion=1),
    Beat(F(47), "La molécule palpite (± 24 %, charte 3.6) ; elle est tenue en rangées autour de l'axe.", "inout_cubic", onion=0),
    Beat(F(54), "Repli : les bulles du haut et du bas sont bues en diagonale par les bulles de l'axe ; le centre se vide dans les deux.", "in_cubic", ann=a_fold, onion=0),
    Beat(F(92), "Les deux bulles deviennent les points du logo (137 -> 11 px, au blanc) ; « sfeer » s'ouvre, l'arabe suit, tenue vivante.", "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "C'est ton croquis : point, haltère, molécule, grappe, puis une bulle qui enfle en goutte avec la vidéo dedans.",
        "On voit la matière circuler : chaque gorgée traverse le col avant que la bulle soit bue. Tout converge vers une seule fenêtre.",
        "La fenêtre est la goutte du gabarit portrait : un simple cache, il marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Le cou partait vers le coin haut-droit sur ton croquis : il sort horizontalement du cadre sur l'axe, comme le gabarit 2.47.",
        "La molécule n'est plus en vrac : 3 rangées horizontales autour de l'axe (3.6), reliées par des cols de la charte.",
        "À valider : les 4 cols en diagonale de la molécule (la charte 2.46 en montre). Le zoom reste centré sur la goutte, sans glissement vertical.",
    ]),
    ("Mouvement", [
        "Rampe : gorgées de 5, 4, 4, 3, 3 images, puis le cou file en 9 images (accélère, freine hors champ). Recul de 22 px.",
        "Wow intro : le cou qui file hors cadre, puis la plongée. Wow outro : l'élastique qui ramène la goutte, puis l'éclatement.",
        "Jamais figé : palpitation 3.6, perles dans les cols, plaque qui zoome, carton qui pousse. 1 à 2 images d'écart partout.",
    ]),
]
