"""Piste 2 (croquis de la DA) : « le champ de points ».

Le cadre se remplit de petits points orange : les points de fidélité SFEER. Ils éclosent, grossissent,
certains se lient en cacahuètes, puis un tourbillon les aspire tous au centre. Ils forment une seule
bulle, qui devient la fenêtre sur la vidéo, et l'on plonge dedans.
L'outro fait le chemin inverse : la fenêtre recule et se referme en bulle, la bulle éclate en points,
deux points reviennent au centre, se divisent (3.4-02) et deviennent les points du logo.
"""
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, clamp01, ease, lerp, prog, render_layers  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import (AXIS, H, ORANGE, WHITE, W, arrow, bridge_d, curved_arrow, f,  # noqa: E402
                       mix_hex)

CX, CY = W / 2, AXIS
TAU = 2 * math.pi

META = {
    "id": "p02_champ_de_points",
    "num": "P2",
    "title": "Le champ de points",
    "principe": "Un champ de points de fidélité est aspiré en une seule bulle : la fenêtre se gagne point par point.",
    "logline": "Piste 2 de la DA. Des centaines de points SFEER éclosent et respirent ; un tourbillon les aspire au centre "
               "en une seule bulle, qui claque, s'ouvre sur la vidéo et nous avale. En outro, elle éclate en points.",
}


# =============================================================== géométrie (helpers locaux)
def circle_cw(cx, cy, r):
    """Cercle tracé dans le sens horaire, comme bridge_d : les unions de sous-tracés ne font pas de trous."""
    return f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_rot(cx, cy, rx, ry, ang):
    """Point étiré dans le sens de sa vitesse (ang en radians), volume conservé par l'appelant."""
    c, s = math.cos(ang), math.sin(ang)
    x1, y1, x2, y2 = cx - rx * c, cy - rx * s, cx + rx * c, cy + rx * s
    deg = math.degrees(ang)
    return (f"M{f(x1)} {f(y1)}A{f(rx)} {f(ry)} {f(deg)} 1 1 {f(x2)} {f(y2)}"
            f"A{f(rx)} {f(ry)} {f(deg)} 1 1 {f(x1)} {f(y1)}Z")


_TOK = re.compile(r"[MLAZaz]|-?\d+(?:\.\d+)?")


def xform_d(d, fp, fv, arc):
    """Transforme un tracé M/L/A/a/Z : fp(x, y) pour les points absolus, fv pour les vecteurs relatifs."""
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
            x, y = fp(float(toks[i]), float(toks[i + 1]))
            i += 2
            out.append(f"{cmd}{f(x)} {f(y)}")
        else:  # A / a
            rx, ry, rot, la, sw, x, y = (float(v) for v in toks[i:i + 7])
            i += 7
            rx, ry, rot = arc(rx, ry, rot)
            x, y = fp(x, y) if cmd == "A" else fv(x, y)
            out.append(f"{cmd}{f(rx)} {f(ry)} {f(rot)} {int(la)} {int(sw)} {f(x)} {f(y)}")
    return "".join(out)


def rot_d(d, ox, oy, ang):
    """Rotation d'un tracé autour de (ox, oy) : un col de la charte orienté vers le centre."""
    c, s = math.cos(ang), math.sin(ang)
    return xform_d(d, lambda x, y: (ox + (x - ox) * c - (y - oy) * s, oy + (x - ox) * s + (y - oy) * c),
                   lambda x, y: (x * c - y * s, x * s + y * c),
                   lambda rx, ry, rot: (rx, ry, rot + math.degrees(ang)))


def link_d(c1, c2, reach=1.2, tight=0.35):
    """Deux bulles sur une même ligne : séparées, reliées par un col (qui s'épaissit en approchant),
    en cacahuète si elles se chevauchent, ou fondues. reach = portée du col en rayons du petit point."""
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
        h = rmin * (0.04 + 0.30 * (1 - g / rg))
    else:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        for tt in (tight, tight * 0.5, tight * 0.2, 0.04):
            path = bridge_d((x1, y, r1), (x2, y, r2), yi + tt * (rmin - yi))
            if "L" not in path:        # pas d'enveloppe à bords droits : seulement des arcs
                return path
        return circle_cw(x1, y, r1) + circle_cw(x2, y, r2)
    path = bridge_d((x1, y, r1), (x2, y, r2), h)
    return path if "L" not in path else circle_cw(x1, y, r1) + circle_cw(x2, y, r2)


def wander(ph, per, t, amp=1.0):
    """Dérive brownienne lente (somme de sinus déphasés) : un point n'est jamais immobile."""
    a, b = per
    dx = 9 * math.sin(TAU * (t / a + ph[1])) + 4 * math.sin(TAU * (t / (a * 0.53) + ph[2]))
    dy = 7 * math.sin(TAU * (t / b + ph[3])) + 3 * math.sin(TAU * (t / (b * 0.61) + ph[0]))
    return dx * amp, dy * amp


def stretch_dot(p_now, p_prev, r, k=0.011, smax=1.35):
    """Ellipse étirée dans le sens de la vitesse (px par image), sx·sy = 1."""
    vx, vy = p_now[0] - p_prev[0], p_now[1] - p_prev[1]
    v = math.hypot(vx, vy)
    if v < 0.6:
        return circle_cw(p_now[0], p_now[1], r)
    s = min(smax, 1 + k * v)
    return ellipse_rot(p_now[0], p_now[1], r * s, r / s, math.atan2(vy, vx))


# =============================================================== le champ (déterministe)
def _make_field(seed=7, cols=18, rows=10, jit=0.38):
    rnd = random.Random(seed)
    grid = {}
    for j in range(rows):
        for i in range(cols):
            x = (i + 0.5 + rnd.uniform(-jit, jit)) * W / cols
            y = (j + 0.5 + rnd.uniform(-jit, jit)) * H / rows
            if math.hypot(x - CX, y - CY) < 110:
                continue
            grid[(i, j)] = dict(x=x, y=y, r0=rnd.uniform(5, 9), g=rnd.uniform(1.7, 2.6),
                                ph=[rnd.random() for _ in range(4)],
                                per=(rnd.uniform(1.1, 2.3), rnd.uniform(1.1, 2.3)),
                                bp=rnd.uniform(0.9, 1.4), jit=rnd.random())
    rmax = max(math.hypot(D["x"] - CX, D["y"] - CY) for D in grid.values())
    for D in grid.values():
        D["tp"] = F(11) * math.hypot(D["x"] - CX, D["y"] - CY) / rmax + F(1.5) * D["jit"]
    used, bodies = set(), []
    for j in range(rows):
        for i in range(cols):
            if (i, j) in used or (i, j) not in grid:
                continue
            a, b = grid[(i, j)], grid.get((i + 1, j))
            if b is not None and (i + 1, j) not in used and rnd.random() < 0.24:
                used |= {(i, j), (i + 1, j)}
                bodies.append(dict(m=[a, b], tm=F(10) + F(5) * rnd.random(),
                                   bx=(a["x"] + b["x"]) / 2, by=(a["y"] + b["y"]) / 2))
            else:
                used.add((i, j))
                bodies.append(dict(m=[a], bx=a["x"], by=a["y"]))
    for n, B in enumerate(bodies):
        B["n"] = n
        dx, dy = B["bx"] - CX, B["by"] - CY
        B["rho"], B["th"] = math.hypot(dx, dy), math.atan2(dy, dx)
    rb = max(B["rho"] for B in bodies)
    for B in bodies:
        q = B["rho"] / rb
        jj = B["m"][0]["jit"]
        B["s"] = F(31) + F(4) * q + F(1.5) * jj           # les plus proches partent d'abord
        B["dur"] = F(10) + F(4) * q
    return bodies


BODIES = _make_field()
TRACKED = {B["n"] for B in BODIES if B["n"] % 23 == 5}   # trajectoires montrées sur la planche


def xwave(t):
    """Vague de taille (charte 3.6) qui balaie le champ de gauche à droite."""
    return lerp(-300, W + 300, prog(t, F(9), F(30), "inout_cubic"))


def r_dot(D, t):
    pop = prog(t, D["tp"], D["tp"] + F(6), "out_back_fort")
    grow = lerp(1, D["g"], prog(t, F(8), F(26), "out_cubic"))
    wave = 1 + 0.5 * math.exp(-((D["x"] - xwave(t)) / 170) ** 2)
    inhale = 1 - 0.18 * prog(t, F(27), F(33), "out_cubic")
    return D["r0"] * pop * grow * wave * inhale * breathe(t, 0.1, D["bp"], D["ph"][0])


def dil(t):
    """Anticipation : le champ « inspire » vers l'extérieur (+7 %) avant l'aspiration."""
    return 1 + 0.07 * prog(t, F(27), F(33), "out_cubic")


SWIRL = 0.55       # rotation du tourbillon (rad) pendant l'aspiration


def body_pos(B, t):
    """Centre du corps (point seul ou paire) : dérive, inspiration, puis spirale vers le centre."""
    u = prog(t, B["s"], B["s"] + B["dur"])
    pr = ease("in_expo")(u)
    rho = B["rho"] * dil(t) * (1 - pr)
    th = B["th"] + SWIRL * ease("in_cubic")(u)
    wx, wy = wander(B["m"][0]["ph"], B["m"][0]["per"], t, 1 - u)
    return CX + rho * math.cos(th) + wx, CY + rho * math.sin(th) + wy, rho, th, u


def body_r(B, t):
    return math.sqrt(sum(r_dot(D, t) ** 2 for D in B["m"]))


R_FULL = 290
_AREA = {B["n"]: body_r(B, F(31)) ** 2 for B in BODIES}
_AREA_TOT = sum(_AREA.values())


def core_r(t):
    """Rayon de la bulle centrale : graine qui respire, puis somme des points absorbés, puis impact."""
    seed = 30 * prog(t, 0, F(6), "out_back_fort") * lerp(1, 1.45, prog(t, F(8), F(26), "out_cubic"))
    seed *= breathe(t, 0.08, 0.9)
    tot = 0.0
    for B in BODIES:
        u = prog(t, B["s"], B["s"] + B["dur"])
        tot += _AREA[B["n"]] * clamp01((u - 0.93) / 0.07)
    r = max(seed, R_FULL * math.sqrt(tot / _AREA_TOT))
    if t > F(49):                                    # impact : dépassement amorti
        tau = t - F(49)
        r *= 1 + 0.2 * math.exp(-7 * tau) * math.sin(TAU * 3 * tau)
    return r * breathe(t, 0.025, 1.3, 0.1)


def field_layers(t, core):
    """Points du champ : seuls, en cacahuètes, puis aspirés avec un col vers la bulle centrale."""
    L = []
    for B in BODIES:
        x, y, rho, th, u = body_pos(B, t)
        pts = [(x, y)] if B["n"] in TRACKED else []
        if len(B["m"]) == 2 and t < F(32):
            a, b = B["m"]
            ra, rb = r_dot(a, t), r_dot(b, t)
            if ra + rb < 1:
                continue
            m = prog(t, B["tm"], B["tm"] + F(8), "inout_cubic")
            fz = prog(t, F(27), F(32), "in_cubic")
            rf = math.sqrt(ra * ra + rb * rb)
            ra, rb = lerp(ra, rf, fz), lerp(rb, rf, fz)
            dl = dil(t)
            cxp, cyp = CX + (B["bx"] - CX) * dl, CY + (B["by"] - CY) * dl
            half0 = (b["x"] - a["x"]) / 2 * dl
            sep = lerp(half0, 0.4 * (ra + rb), m) * (1 - fz)
            # avant la liaison, chaque point garde sa propre dérive ; liés, ils dérivent ensemble
            ws = wander(a["ph"], a["per"], t)
            wa, wb = wander(a["ph"], a["per"], t), wander(b["ph"], b["per"], t)
            wa = (lerp(wa[0], ws[0], m), lerp(wa[1], ws[1], m))
            wb = (lerp(wb[0], ws[0], m), lerp(wb[1], ws[1], m))
            yc = 1 - clamp01(m * 2.2)
            ya = cyp + (a["y"] - B["by"]) * dl * yc + wa[1]
            yb = cyp + (b["y"] - B["by"]) * dl * yc + wb[1]
            if yc > 0:
                d = circle_cw(cxp - sep + wa[0], ya, ra) + circle_cw(cxp + sep + wb[0], yb, rb)
            else:
                d = link_d((cxp - sep + wa[0], ya, ra), (cxp + sep + wb[0], ya, rb), reach=1.4)
            pts = [(cxp, cyp)] if B["n"] in TRACKED else []
            L.append({"k": "fill", "id": f"point-{B['n']}", "fill": ORANGE, "d": d, "ghost": False, "pts": pts})
            continue
        r = body_r(B, t)
        if r < 0.5:
            continue
        if rho + r <= core - 2:            # absorbé
            continue
        g = rho - core - r
        if t > F(30) and g < 1.3 * r:
            # col de la charte entre le point et la bulle centrale, orienté vers le centre
            d = rot_d(link_d((CX, CY, core), (CX + rho, CY, r), reach=1.3), CX, CY, th)
        else:
            x0, y0, *_ = body_pos(B, t - F(1))
            d = stretch_dot((x, y), (x0, y0), r)
        L.append({"k": "fill", "id": f"point-{B['n']}", "fill": ORANGE, "d": d, "ghost": False, "pts": pts})
    return L


# =============================================================== INTRO (4,0 s)
_cam = Track((F(57), 1.0), (F(61), 0.92, "in_cubic"), (F(88), 6.0, "plongee"))


def cam(t):
    return _cam(t) + drift(t, F(61), 1.0)       # la poussée ne s'arrête jamais


def plate_zoom(t, k):
    """Contre-zoom plus lent de la vidéo (parallaxe), plus une poussée propre d'au moins 1 % par image."""
    return 0.8 * k ** 0.55 + 0.35 * max(0.0, t - F(66))


def cam_speed(t):
    return abs(cam(t + 0.01) - cam(t - 0.01)) / 0.02


_iris = Track((F(51), 0.0), (F(58), 1.05, "out_expo"), (F(62), 1.0, "out_cubic"))

# éclaboussures de l'impact : angle (rad, jamais vertical), distance, rayon
SPLASH = [(0.32, 230, 27), (0.95, 170, 20), (2.25, 210, 24), (2.78, 260, 30),
          (3.55, 190, 21), (4.05, 240, 26), (5.35, 200, 22), (5.95, 250, 29)]


def splash_pos(a, dd, t, k):
    u = prog(t, F(49), F(58), "out_expo")
    rho = (R_FULL + 10 + dd * u) * k ** 1.7          # plus près de la caméra que la bulle : parallaxe
    wx = 6 * math.sin(TAU * (t / 1.3 + a))
    return CX + rho * math.cos(a) + wx, CY + rho * math.sin(a) * 0.92


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    k = cam(t)
    core = core_r(t)
    if t < F(52):
        L += field_layers(t, core)
    sx = squash(t, F(49), F(10), 0.24)
    s = min(1 + 0.015 * cam_speed(t), 1.1)              # étirement horizontal pendant la plongée
    if core > 0.5:
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "ghost": core * k < 900,
                  "d": ellipse_rot(CX, CY, core * sx * k * s, core / sx * k / s, 0)})
    gr = _iris(t)
    if gr > 0.01:
        rr = core * 0.87 * gr * k
        L.append(video(plate_zoom(t, k), ellipse_rot(CX, CY, rr * sx * s, rr / sx / s, 0), ghost=rr < 900))
    if t >= F(49):
        for n, (a, dd, r) in enumerate(SPLASH):
            p = splash_pos(a, dd, t, k)
            p0 = splash_pos(a, dd, t - F(1), cam(t - F(1)))
            rr = r * prog(t, F(49), F(53), "out_back") * k ** 1.3 * breathe(t, 0.1, 0.8, a)
            if rr > 0.5 and -300 < p[0] < W + 300 and -300 < p[1] < H + 300:
                L.append({"k": "fill", "id": f"goutte-{n}", "fill": ORANGE, "ghost": False,
                          "d": stretch_dot(p, p0, rr, k=0.006), "pts": [p]})
    return L


def a_pop(t):
    return "".join(arrow(CX + math.cos(a) * 150, CY + math.sin(a) * 150, CX + math.cos(a) * 330, CY + math.sin(a) * 330, w=6)
                   for a in (0.5, 2.64, 3.64, 5.78))


def a_vague(t):
    x = xwave(t)
    return arrow(x - 260, 90, x + 160, 90) + arrow(x - 260, H - 90, x + 160, H - 90)


def a_inspire(t):
    return "".join(arrow(CX + dx * 360, CY + dy * 210, CX + dx * 470, CY + dy * 275, w=6)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_spirale(t):
    o = []
    for a in (0.6, 2.2, 3.75, 5.3):
        r1, r2 = 820, 330
        x1, y1 = CX + r1 * math.cos(a), CY + r1 * math.sin(a) * 0.62
        x2, y2 = CX + r2 * math.cos(a + 0.6), CY + r2 * math.sin(a + 0.6) * 0.62
        cx, cy = CX + 640 * math.cos(a + 0.45), CY + 640 * math.sin(a + 0.45) * 0.62
        o.append(curved_arrow(x1, y1, cx, cy, x2, y2))
    return "".join(o)


def a_eclat(t):
    return "".join(arrow(CX + math.cos(a) * 420, CY + math.sin(a) * 400, CX + math.cos(a) * 640, CY + math.sin(a) * 560, w=6)
                   for a, _, _ in SPLASH[::2])


def a_plongee(t):
    return "".join(arrow(CX + dx * 520, CY + dy * 290, CX + dx * 900, CY + dy * 500)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(7), "Les points éclosent en onde depuis le centre (11 images, du centre aux coins), chacun avec un dépassement de 15 %.", "out_back_fort", ann=a_pop, onion=0),
    Beat(F(22), "Une vague de taille balaie le champ de gauche à droite (+50 %) ; des voisins se lient en cacahuètes horizontales (8 images).", "inout_cubic", ann=a_vague, onion=0),
    Beat(F(31), "Anticipation : le champ inspire vers l'extérieur (+7 %), les points rétrécissent de 18 % et les cacahuètes se ferment.", "out_cubic", ann=a_inspire, onion=0),
    Beat(F(43), "Aspiration en spirale (32°) avec rampe in_expo : les proches partent d'abord, les points s'étirent jusqu'à 135 % et font un col en touchant.", "in_expo", ann=a_spirale, onion=1, onion_dt=F(2)),
    Beat(F(50), "Impact au centre : la bulle claque à 124 % × 81 % et dépasse de 11 % ; 8 gouttes éclaboussent en diagonale.", "ressort_vif", ann=a_eclat, onion=2, onion_dt=F(1)),
    Beat(F(56), "La vidéo perce la bulle depuis le centre en 7 images : il reste un anneau orange de 13 %. C'est la fenêtre.", "out_expo", onion=2, onion_dt=F(2)),
    Beat(F(72), "Plongée : zoom ×6 depuis le centre ; les gouttes passent devant la caméra (parallaxe ×1,7) et sortent en diagonale.", "plongee", ann=a_plongee, onion=2, onion_dt=F(3)),
    Beat(F(96), "Plein cadre vidéo, la poussée continue (+15 %/s) : on raccorde sur un plan en mouvement.", "out_cubic", onion=0),
])


# =============================================================== OUTRO (4,0 s)
_ok = Track((0, 7.0), (F(3), 7.5, "linear"), (F(18), 1.0, "out_expo"))


def ok(t):
    return _ok(t)


def ok_speed(t):
    return abs(ok(t + 0.01) - ok(t - 0.01)) / 0.02


_close = Track((F(19), 1.0), (F(22), 1.07, "out_cubic"), (F(28), 0.0, "in_cubic"))
R_BURST = 250


def outro_core(t):
    r = R_FULL * lerp(1, R_BURST / R_FULL, prog(t, F(28), F(33), "in_cubic"))
    r *= 1 + 0.03 * math.sin(TAU * t / 0.16) * prog(t, F(28), F(33))     # la bulle tremble : elle se charge
    return r * breathe(t, 0.02, 1.2)


def _make_burst(seed=11, cols=20, rows=11, jit=0.42):
    rnd = random.Random(seed)
    out = []
    for j in range(rows):
        for i in range(cols):
            x = (i + 0.5 + rnd.uniform(-jit, jit)) * W / cols
            y = (j + 0.5 + rnd.uniform(-jit, jit)) * H / rows
            out.append(dict(x=x, y=y, rb=rnd.uniform(14, 24), ph=[rnd.random() for _ in range(4)],
                            per=(rnd.uniform(1.1, 2.3), rnd.uniform(1.1, 2.3)), jit=rnd.random(),
                            bp=rnd.uniform(0.8, 1.3)))
    # les deux points qui deviendront les points du logo : près de l'axe, à gauche et à droite
    out = [D for D in out if math.hypot(D["x"] - 520, D["y"] - 500) > 90 and math.hypot(D["x"] - 1420, D["y"] - 575) > 90]
    out.append(dict(x=520, y=500, rb=30, ph=[0.1, 0.3, 0.6, 0.8], per=(1.6, 1.9), jit=0.2, bp=1.0, special="g"))
    out.append(dict(x=1420, y=575, rb=30, ph=[0.7, 0.2, 0.4, 0.9], per=(1.8, 1.5), jit=0.5, bp=1.1, special="d"))
    rmax = max(math.hypot(D["x"] - CX, D["y"] - CY) for D in out)
    for D in out:
        dx, dy = D["x"] - CX, D["y"] - CY
        D["rho"], D["th"] = math.hypot(dx, dy), math.atan2(dy, dx)
        q = D["rho"] / rmax
        D["rho0"] = q * (R_BURST - D["rb"])
        D["ts"] = F(33) + F(2) * (1 - q)
        D["te"] = F(45) + F(4) * D["jit"]
    return out


BURST = _make_burst()


def burst_pos(D, t):
    u = prog(t, D["ts"], D["ts"] + F(16))
    rho = lerp(D["rho0"], D["rho"], ease("out_back")(u))
    th = D["th"] + 0.3 * (ease("out_expo")(u) - 1)            # légère spirale inverse de l'intro
    ue = 0.0
    if "special" not in D:
        ue = prog(t, D["te"], D["te"] + F(13))
        rho += 1500 * ease("in_expo")(ue)                        # sortie du cadre en accélérant
        th += 0.25 * ease("in_cubic")(ue)
    wx, wy = wander(D["ph"], D["per"], t, prog(t, D["ts"] + F(6), D["ts"] + F(20)))
    return CX + rho * math.cos(th) + wx, CY + rho * math.sin(th) + wy


def ring_wave(t, rho):
    """Onde de taille radiale après l'éclatement (charte 3.6 en anneau)."""
    rw = lerp(150, 1300, prog(t, F(35), F(52), "out_cubic"))
    return 1 + 0.4 * math.exp(-((rho - rw) / 160) ** 2)


def burst_r(D, t):
    u = prog(t, D["ts"], D["ts"] + F(16))
    return D["rb"] * lerp(1.0, 0.75, u) * ring_wave(t, D["rho"]) * breathe(t, 0.1, D["bp"], D["ph"][0])


# les deux points du logo : retour au centre, choc, fusion, division (3.4-02), atterrissage
_ret = {s: Track((F(44), 0.0), (F(47), -0.06, "out_cubic"), (F(56), 1.0, "in_expo")) for s in "gd"}
_rety = Track((F(44), 0.0), (F(52), 1.0, "inout_cubic"))
_spread = Track((F(59), 0.0), (F(63), 53, "inout_cubic"), (F(71), 302, "emphase"), (F(77), CX - LG["dot_g"][0], "out_cubic"))
T_SNAP = F(63.3)


def logo_pair(t):
    """Calques des deux points spéciaux. Renvoie [] tant qu'ils sont dans le champ."""
    if t < F(44):
        return []
    S = [D for D in BURST if "special" in D]
    col = mix_hex(ORANGE, WHITE, prog(t, F(62), F(70)))
    if t < F(56):
        out = []
        for D in S:
            fx, fy = burst_pos(D, F(44))
            sgn = -1 if D["special"] == "g" else 1
            u = _ret[D["special"]](t)
            tx = CX + sgn * 34
            x = fx + (tx - fx) * u
            y = fy + (AXIS - fy) * _rety(t)
            r = lerp(burst_r(D, t), 34, prog(t, F(44), F(54)))
            x0 = fx + (tx - fx) * _ret[D["special"]](t - F(1))
            y0 = fy + (AXIS - fy) * _rety(t - F(1))
            out.append({"k": "fill", "id": f"point-logo-{D['special']}", "fill": col,
                        "d": stretch_dot((x, y), (x0, y0), r), "pts": [(x, y)]})
        return out
    if t < F(59):
        # choc puis fusion : la paire devient un seul point, qui oscille (75 % x 133 %)
        u = prog(t, F(56), F(58.5), "out_cubic")
        r = lerp(34, 48, u)
        sep = 34 * (1 - u)
        if sep > 1.5:
            d = link_d((CX - sep, CY, r), (CX + sep, CY, r), reach=1.0)
        else:
            sx = squash(t, F(58.5), F(9), -0.25)
            d = ellipse_rot(CX, CY, r * sx, r / sx, 0)
        return [{"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": [(CX, CY)]}]
    s = _spread(t)
    r = lerp(34, LG["dot_r"], prog(t, F(63), F(75), "inout_cubic"))
    r *= 1 + (breathe(t, 0.2, 1.1) - 1) * prog(t, F(70), F(80))
    if t < F(60):
        r = lerp(48, 34, prog(t, F(59), F(60)))
    c1, c2 = (CX - s, CY, r), (CX + s, CY, r)
    if 2 * s - 2 * r < 1.2 * r:
        d = link_d(c1, c2, reach=1.2)
    else:
        sx = squash(t, T_SNAP, F(8), 0.22)            # recul des deux moitiés après la rupture
        d = ellipse_rot(CX - s, CY, r * sx, r / sx, 0) + ellipse_rot(CX + s, CY, r * sx, r / sx, 0)
    return [{"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": [(CX - s, CY), (CX + s, CY)]}]


def outro(t):
    L = [{"k": "bg", "v": "gradient"}]
    if t < F(33.5):
        k = ok(t)
        s = min(1 + 0.015 * ok_speed(t), 1.1)
        core = outro_core(t)
        sx = squash(t, F(18), F(9), 0.16) * squash(t, F(28), F(8), -0.1)
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "ghost": core * k < 900,
                  "d": ellipse_rot(CX, CY, core * k * s * sx, core * k / s / sx, 0)})
        gr = _close(t) if t >= F(19) else 1.0
        if gr > 0.01:
            rr = core * 0.87 * gr * k
            L.append(video(0.8 * k ** 0.55, ellipse_rot(CX, CY, rr * s * sx, rr / s / sx, 0), ghost=rr < 900))
    if t >= F(33):
        for n, D in enumerate(BURST):
            if "special" in D and t >= F(44):
                continue
            x, y = burst_pos(D, t)
            if not (-80 < x < W + 80 and -80 < y < H + 80):
                continue
            x0, y0 = burst_pos(D, t - F(1))
            r = burst_r(D, t)
            L.append({"k": "fill", "id": f"eclat-{n}", "fill": ORANGE, "ghost": False,
                      "d": stretch_dot((x, y), (x0, y0), r),
                      "pts": [(x, y)] if n % 17 == 3 or "special" in D else []})
    return L


def outro_full(t):
    """Outro = formes + carton logo ; les points du logo amenés par l'animation suivent la poussée."""
    return outro(t) + precise_card(endcard(t, F(66), dots=False, extra=logo_pair(t)), t, F(66))


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


def a_recul(t):
    return "".join(arrow(CX + dx * 900, CY + dy * 500, CX + dx * 560, CY + dy * 310)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_ferme(t):
    return arrow(CX - 470, CY, CX - 290, CY, w=6) + arrow(CX + 470, CY, CX + 290, CY, w=6)


def a_charge(t):
    return "".join(arrow(CX + math.cos(a) * 420, CY + math.sin(a) * 380, CX + math.cos(a) * 300, CY + math.sin(a) * 270, w=6)
                   for a in (0.6, 2.54, 3.74, 5.68))


def a_burst(t):
    return "".join(arrow(CX + math.cos(a) * 300, CY + math.sin(a) * 260, CX + math.cos(a) * 620, CY + math.sin(a) * 470, w=6)
                   for a in (0.35, 1.1, 2.05, 2.8, 3.5, 4.3, 5.2, 5.95))


def a_sortie(t):
    return (arrow(560, 520, 820, 540, w=6) + arrow(1380, 565, 1110, 540, w=6) +
            "".join(arrow(CX + dx * 640, CY + dy * 330, CX + dx * 900, CY + dy * 480, dash=True)
                    for dx in (-1, 1) for dy in (-1, 1)))


def a_division(t):
    return arrow(CX - 60, CY - 120, CX - 230, CY - 120, w=6) + arrow(CX + 60, CY - 120, CX + 230, CY - 120, w=6)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(8), "La fenêtre recule d'un coup : zoom ×7,5 -> ×1 en 15 images (out_expo). Les coins du dégradé réapparaissent.", "out_expo", ann=a_recul, onion=2, onion_dt=F(2)),
    Beat(F(24), "La vidéo se referme vers le centre en 6 images, après s'être ouverte de 7 % (anticipation). La bulle redevient orange.", "in_cubic", ann=a_ferme, onion=2, onion_dt=F(2)),
    Beat(F(31), "Charge : la bulle se contracte de 14 % en 5 images et tremble (±3 %, 6 fois par seconde) avant d'éclater.", "in_cubic", ann=a_charge, onion=0),
    Beat(F(36), "Éclatement : la bulle se brise en 220 points projetés en spirale inverse, étirés à 135 % dans le sens de la vitesse.", "out_back", ann=a_burst, onion=2, onion_dt=F(1)),
    Beat(F(46), "Les points dépassent leur place de 10 %, freinent et dérivent ; une onde de taille (+40 %) court du centre vers les bords.", "out_back", onion=0),
    Beat(F(53), "Deux points reculent puis filent vers le centre et rejoignent l'axe ; tous les autres sortent du cadre en accélérant.", "in_expo", ann=a_sortie, onion=0),
    Beat(F(61), "Choc au centre, fusion (75 % × 133 %), puis division (3.4-02) : cacahuète, col qui s'affine, rupture nette en 4 images.", "inout_cubic", ann=a_division, onion=0),
    Beat(F(94), "Les deux points ont viré au blanc et ouvert « sfeer » ; arabe de droite à gauche ; poussée continue de 11,5 %/s, points qui respirent (±20 %).", "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "C'est ton croquis : chaque point est un point de fidélité. On les voit naître, se lier, puis tous se réunir en une seule bulle : la fenêtre se gagne.",
        "Les points sont aspirés : on comprend sans texte que la récompense vient de leur somme.",
        "La fenêtre est un cache rond : elle marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Tes cases vides sont développées : impact, ouverture de la fenêtre, plongée. L'outro rejoue le croquis à l'envers.",
        "Écart à valider : le champ de points couvre tout le cadre, hors de l'axe. C'est un transitoire de 2 s, et toutes les cacahuètes sont horizontales.",
        "L'aspiration et l'éclatement sont radiaux depuis le centre (diagonales, pas de vertical). La spirale (32°) est un écart léger à valider.",
    ]),
    ("Mouvement", [
        "Rien de figé : dérive brownienne de ±9 px, respiration, vague de taille, zoom continu de la vidéo.",
        "Chaque action a son contre-mouvement : inspiration avant l'aspiration, recul avant le retour des deux points.",
        "AE : un calque de forme par point, positions en expressions (bruit + spirale), cols dessinés en tracé animé.",
    ]),
]
