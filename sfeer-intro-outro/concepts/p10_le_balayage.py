"""Piste 10 (croquis de la DA) : « le balayage ».

Des points arrivent de la gauche en grossissant et se fondent en une bulle, qui tremble. Une bulle
géante entre par le bord gauche, coupée à son milieu (2.48). Son bord se bombe en pic vers la petite
bulle, qui en tend un aussi : les deux pics se rejoignent en un long cou tendu qui traverse le cadre.
La vidéo coule dans la géante, puis dans le cou. Claquement : la petite bulle est aspirée et la
géante balaie tout le cadre de gauche à droite, front étiré et bord concave du cou à droite.
Outro : le vert se retire vers le bord droit en laissant une bulle collée par un cou ; le cou casse,
la bulle libérée rebondit au centre, se divise en deux points : le logo.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, clamp01, lerp, prog  # noqa: E402
from blocks import LG, drift, endcard, squash, video  # noqa: E402
from sfeer_svg import AXIS, H, ORANGE, W, WHITE, _neck_circle, arrow, bridge_d, curved_arrow, f, mix_hex  # noqa: E402

CX = W / 2

META = {
    "id": "p10_le_balayage",
    "num": "P10",
    "title": "Le balayage",
    "logline": "Piste 10 de la DA. Des points se fondent en une bulle qui tremble ; une géante entre par le bord, la relie "
               "par un long cou tendu, puis claque et balaie tout le cadre en emportant la vidéo.",
}


# =================================================================== géométrie (tracés horaires)
def circle_cw(x, r):
    r = max(r, 0.01)
    return f"M{f(x - r)} {AXIS}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_cw(x, rx, ry):
    return f"M{f(x - rx)} {AXIS}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z"


def hull_cw(x1, r1, x2, r2):
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, AXIS - r1 * ny), (x2 + r2 * nx, AXIS - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, AXIS + r2 * ny), (x1 + r1 * nx, AXIS + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def link(x1, r1, x2, r2, h):
    """Col de la charte entre deux cercles de l'axe ; gère cacahuète et inclusion."""
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


def neck(x1, r1, x2, r2, h):
    """Géométrie du col (x1 < x2) : cercle de col (Rn, xn, yn) et points de tangence haut (t1, t2)."""
    sol = _neck_circle((x1, AXIS, r1), (x2, AXIS, r2), h)
    if sol is None:
        return None
    Rn, xn = sol
    yn = Rn + h

    def tang(cx, r):
        vx, vy = xn - cx, -yn
        L = math.hypot(vx, vy)
        return cx + r * vx / L, AXIS + r * vy / L

    return Rn, xn, yn, tang(x1, r1), tang(x2, r2)


def neck_ht(nk, x):
    Rn, xn, yn = nk[0], nk[1], nk[2]
    return yn - math.sqrt(max(Rn * Rn - (x - xn) ** 2, 0.0))


def flood_neck(nk, xf):
    """Partie du col remplie jusqu'à xf (front plat), depuis la bulle de gauche."""
    Rn, (t1x, t1y) = nk[0], nk[3]
    hf = neck_ht(nk, xf)
    return (f"M{f(t1x)} {f(t1y)}A{f(Rn)} {f(Rn)} 0 0 0 {f(xf)} {f(AXIS - hf)}"
            f"L{f(xf)} {f(AXIS + hf)}A{f(Rn)} {f(Rn)} 0 0 0 {f(t1x)} {f(2 * AXIS - t1y)}Z")


def tendril_left(nk, x_tip, nose):
    """Le col réel, révélé depuis la bulle de gauche jusqu'à x_tip, avec un nez arrondi (pic)."""
    Rn, (t1x, t1y) = nk[0], nk[3]
    if x_tip <= t1x + 0.5:
        return ""
    hf = neck_ht(nk, x_tip)
    return (f"M{f(t1x)} {f(t1y)}A{f(Rn)} {f(Rn)} 0 0 0 {f(x_tip)} {f(AXIS - hf)}"
            f"A{f(max(nose, 0.5))} {f(hf)} 0 0 1 {f(x_tip)} {f(AXIS + hf)}"
            f"A{f(Rn)} {f(Rn)} 0 0 0 {f(t1x)} {f(2 * AXIS - t1y)}Z")


def tendril_right(nk, x_tip, nose):
    """Même chose depuis la bulle de droite, vers la gauche."""
    Rn, (t2x, t2y) = nk[0], nk[4]
    if x_tip >= t2x - 0.5:
        return ""
    hf = neck_ht(nk, x_tip)
    return (f"M{f(t2x)} {f(2 * AXIS - t2y)}A{f(Rn)} {f(Rn)} 0 0 0 {f(x_tip)} {f(AXIS + hf)}"
            f"A{f(max(nose, 0.5))} {f(hf)} 0 0 1 {f(x_tip)} {f(AXIS - hf)}"
            f"A{f(Rn)} {f(Rn)} 0 0 0 {f(t2x)} {f(t2y)}Z")


def lens(xm, rm, e, rho):
    """Intersection de la bulle (xm, rm) et d'un iris de rayon rho centré en e (sur l'axe, e < xm)."""
    D = xm - e
    if rho >= D + rm:
        return circle_cw(xm, rm)
    if rho <= max(rm - D, 0.5):
        return circle_cw(e, max(rho, 0.01))
    a = (rho * rho - rm * rm + D * D) / (2 * D)
    yi = math.sqrt(max(rho * rho - a * a, 0.0))
    xi = e + a
    large_iris = 1 if a < 0 else 0          # arc de l'iris côté droit
    large_main = 1 if xi > xm else 0        # arc de la bulle côté gauche
    return (f"M{f(xi)} {f(AXIS - yi)}A{f(rho)} {f(rho)} 0 {large_iris} 1 {f(xi)} {f(AXIS + yi)}"
            f"A{f(rm)} {f(rm)} 0 {large_main} 1 {f(xi)} {f(AXIS - yi)}Z")


def half_front(cx, R, rx, side="right"):
    """Géante : un demi-cercle, et un demi-ellipse étiré (rx) du côté du mouvement."""
    if side == "right":
        return (f"M{f(cx)} {f(AXIS - R)}A{f(rx)} {f(R)} 0 0 1 {f(cx)} {f(AXIS + R)}"
                f"A{f(R)} {f(R)} 0 0 1 {f(cx)} {f(AXIS - R)}Z")
    return (f"M{f(cx)} {f(AXIS - R)}A{f(R)} {f(R)} 0 0 1 {f(cx)} {f(AXIS + R)}"
            f"A{f(rx)} {f(R)} 0 0 1 {f(cx)} {f(AXIS - R)}Z")


def speed(fn, t, dt=0.02):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def stretch(v, k=14000, cap=0.32):
    return 1 + min(cap, abs(v) / k)


def lim(sx):
    return max(1 / 1.35, min(1.35, sx))


def covered(cx, R):
    """Le disque (cx, R) couvre-t-il tout le cadre ?"""
    return R >= math.hypot(max(cx, W - cx), AXIS) + 3


# =================================================================== INTRO (4,0 s)
XS = 1240                                    # la petite bulle, à droite du centre : le cou traversera le cadre
R_END = [80, 46, 42, 38]                     # rayons d'arrivée : meneuse + 3 suiveurs (rampe de taille)
X0 = [150 - 165 * i for i in range(4)]
DOTS = [Track((0, X0[i]), (F(16 + 4 * i), XS, "emphase")) for i in range(4)]
RM = math.sqrt(sum(r * r for r in R_END))   # ≈ 108 px quand tout est fondu
H0 = 24                                      # demi-épaisseur du cou tendu


def dot_r(i, x):
    """Les points grossissent en avançant (rampe de taille)."""
    p = clamp01((x - X0[i]) / (XS - X0[i]))
    return 10 + (R_END[i] - 10) * p ** 1.3


def _impacts():
    """Instant où chaque suiveur touche la meneuse (pour l'écrasement)."""
    out = []
    for i in range(1, 4):
        hit = F(20)
        for n in range(0, 60):
            x = DOTS[i](n / 25)
            if XS - x <= 70 + dot_r(i, x) * 0.2:
                hit = n / 25
                break
        out.append(hit)
    return out


T_HIT = _impacts()

R_G = Track((F(24), 0), (F(28), 84, "out_cubic"), (F(31), 60, "inout_cubic"),     # pointe, recule (anticipation)
            (F(38), 515, "out_expo"), (F(45), 470, "ressort"),                      # éclosion, dépasse de 10 %
            (F(49), 470), (F(62), 548, "in_cubic"))                                 # gonfle : tension
vib = Track((F(22), 0.0), (F(28), 2.5, "out_cubic"), (F(49), 3.0), (F(62), 5.0, "in_cubic"), (F(66), 0.0))
p_g = Track((F(38), 0.0), (F(49), 1.0, "inout_cubic"))                              # pic de la géante
p_s = Track((F(42), 0.0), (F(49), 1.0, "in_cubic"))                                 # pic de la petite (4 i. après)
egg = Track((F(42), 0.0), (F(60), 1.0, "inout_cubic"))                              # la petite s'étire vers la géante
h_t = Track((F(49), H0), (F(62), 9, "in_cubic"))                                    # le cou se tend et s'affine
xs_off = Track((F(49), 0.0), (F(58), -20, "inout_cubic"), (F(61), 14, "out_cubic"),  # attirée, puis recul
               (F(66), -240, "in_cubic"), (F(71), -330, "out_cubic"))               # aspiration
fl_g = Track((F(51), 0.0), (F(55), 1.0, "out_expo"))                                # la vidéo s'ouvre dans la géante
fl_n = Track((F(55), 0.0), (F(59), 1.0, "out_cubic"))                                # ... coule dans le cou
fl_s = Track((F(58.5), 0.0), (F(62), 1.0, "out_cubic"))                             # ... remplit la petite
# balayage : position du front (bord droit de la géante). Recul, accélération, puis freinage hors champ
FRONT = Track((F(62), 548), (F(63.5), 524, "out_cubic"), (F(67), 860, "in_cubic"), (F(81), 2400, "out_cubic"))
zv_in = Track((F(51), 0.7), (F(62), 0.76, "linear"), (F(70), 0.98, "in_cubic"), (F(100), 1.12, "out_cubic"))


def sweep(t):
    """Centre et rayon de la géante pendant le balayage : le bord gauche du cadre reste couvert."""
    fr = FRONT(t)
    cx = (fr * fr - 548 ** 2) / (2 * fr)
    return cx, fr - cx


def small(t):
    """Petite bulle : position (tremblement), étirement."""
    x = XS + xs_off(t) + vib(t) * math.sin(2 * math.pi * 11 * t)
    sx = 1 + 0.14 * egg(t)
    for th in T_HIT:
        sx *= squash(t, th, F(7), 0.12)
    sx *= stretch(speed(xs_off, t), 12000, 0.3)
    return x, lim(sx)


def intro(t):
    zv = zv_in(t) + drift(t, F(51), 0.22) + 0.05 * math.exp(-6 * max(0.0, t - F(68))) * math.sin(
        2 * math.pi * 2.4 * max(0.0, t - F(68)))                                   # la plaque encaisse l'impact
    if t >= F(62):
        cx, R = sweep(t)
        if covered(cx, R):
            return [video(zv, ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    xs, sxs = small(t)
    if t < F(29):
        # --- les points : file sur l'axe, rampe de taille, fusion dans la meneuse
        parts, pts = [], []
        rl = dot_r(0, DOTS[0](t))
        absorbed = 0.0
        for i in range(1, 4):
            x = DOTS[i](t)
            r = dot_r(i, x)
            absorbed += clamp01(1 - (DOTS[0](t) - x) / (rl + r)) * r * r
        rm = math.sqrt(rl * rl + absorbed) * breathe(t, 0.02, 0.5)
        x0 = DOTS[0](t) + (xs - XS)
        sx0 = lim(sxs * stretch(speed(DOTS[0], t), 16000, 0.3))
        parts.append(ellipse_cw(x0, rm * sx0, rm / sx0))
        pts.append((x0, AXIS))
        for i in range(1, 4):
            x = DOTS[i](t)
            r = dot_r(i, x)
            if x < -r or x0 - x <= rm - r:
                continue
            sxi = lim(stretch(speed(DOTS[i], t), 16000, 0.3))
            d = x0 - x
            near = clamp01((1.7 * (rm + r) - d) / (0.7 * (rm + r)))
            if near > 0:
                parts.append(link(x, r / sxi, x0, rm / sx0, min(r, rm) * (0.06 + 0.4 * near)))
            parts.append(ellipse_cw(x, r * sxi, r / sxi))
            pts.append((x, AXIS))
        L.append({"k": "fill", "id": "points", "fill": ORANGE, "d": " ".join(parts), "pts": pts})
        if R_G(t) > 0.5:
            L.append({"k": "fill", "id": "geante", "fill": ORANGE, "d": circle_cw(0, R_G(t))})
        return L
    rs = RM * breathe(t, 0.02, 0.5)
    rsk = rs / sxs                                                              # cercle intérieur (pour le col)
    small_d = ellipse_cw(xs, rs * sxs, rs / sxs)
    if t < F(62):
        # --- géante coupée par le bord gauche ; le vrai col se révèle depuis chaque bulle (pics)
        R = R_G(t) * breathe(t, 0.012, 1.1)
        parts = [circle_cw(0, R), small_d]
        connected = p_g(t) >= 1 and p_s(t) >= 1
        h = h_t(t) if connected else H0
        nk = neck(0, R, xs, rsk, h) if R > 120 else None
        if nk and not connected:
            xn = nk[1]
            pg, ps = p_g(t), p_s(t)
            if pg > 0:
                xt = lerp(nk[3][0], xn, pg)
                parts.append(tendril_left(nk, xt, neck_ht(nk, xt) * 0.6 * min(1.0, 3 * pg)))
            if ps > 0:
                xt = lerp(nk[4][0], xn, ps)
                parts.append(tendril_right(nk, xt, neck_ht(nk, xt) * 0.6 * min(1.0, 3 * ps)))
        elif connected:
            parts.append(link(0, R, xs, rsk, h))
        L.append({"k": "fill", "id": "geante-et-bulle", "fill": ORANGE, "d": " ".join(p for p in parts if p),
                  "pts": [(xs, AXIS)]})
        # --- la vidéo coule : iris dans la géante, front plat dans le cou, iris dans la petite bulle
        if t >= F(51) and connected and nk:
            vparts = [circle_cw(0, R * fl_g(t))]
            if fl_n(t) > 0:
                vparts.append(flood_neck(nk, lerp(nk[3][0], nk[4][0], fl_n(t))))
            if fl_s(t) > 0:
                if fl_s(t) >= 1:
                    vparts.append(small_d)
                else:
                    e = nk[4][0] - 2
                    vparts.append(lens(xs, rsk, e, fl_s(t) * (xs - e + rsk)))
            L.append(video(zv, " ".join(vparts), ghost=False))
        return L
    # --- CLAQUEMENT : la géante (déjà vidéo) balaie le cadre ; la petite bulle est aspirée
    cx, R = sweep(t)
    sxf = 1 + min(0.3, abs(speed(FRONT, t)) / 22000)
    parts = [half_front(cx, R, R * sxf)]
    if xs - cx > R - rsk + 1:                                                   # pas encore avalée
        parts.append(link(cx, R, xs, rsk, h_t(t)))
        parts.append(small_d)
    L.append(video(zv, " ".join(parts), ghost=True))
    L[-1]["pts"] = [(xs, AXIS)]
    return L


def a_file(t):
    return arrow(60, AXIS - 200, 560, AXIS - 200)


def a_fusion(t):
    return arrow(XS - 520, AXIS - 200, XS - 260, AXIS - 200)


def a_tremble(t):
    return arrow(40, AXIS - 300, 220, AXIS - 300) + arrow(XS - 200, AXIS - 200, XS - 160, AXIS - 200) \
        + arrow(XS + 200, AXIS - 200, XS + 160, AXIS - 200)


def a_pic(t):
    return arrow(520, AXIS - 120, 700, AXIS - 120)


def a_cou(t):
    return arrow(720, AXIS - 120, 820, AXIS - 120) + arrow(XS - 260, AXIS - 120, XS - 360, AXIS - 120)


def a_tension(t):
    return arrow(400, AXIS - 440, 580, AXIS - 440) + arrow(300, AXIS + 330, 900, AXIS + 330) \
        + arrow(XS - 160, AXIS - 200, XS - 270, AXIS - 200)


def a_balayage(t):
    return arrow(120, AXIS - 440, 1500, AXIS - 440) + arrow(1560, AXIS + 330, 1260, AXIS + 330)


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(7), "Quatre points filent sur l'axe depuis la gauche, 4 images d'écart, et grossissent en arrivant (rayon ×4 à ×8). Freinage en emphase.",
         "emphase", ann=a_file, onion=2, onion_dt=F(2)),
    Beat(F(21), "Les points se fondent un à un dans la meneuse : le cou se reforme, cacahuète, écrasement de 12 % à chaque impact.",
         "out_cubic", ann=a_fusion, onion=2, onion_dt=F(2)),
    Beat(F(31), "La bulle tremble (±3 px, 11 fois par seconde). La géante pointe au bord gauche : 84 px, puis recul à 60 px (anticipation).",
         "inout_cubic", ann=a_tremble, onion=3, onion_dt=F(1)),
    Beat(F(42), "La géante éclot, coupée à son milieu par le bord (2.48) : 515 px puis ressort à 470. Son bord se bombe en pic vers la bulle.",
         "out_expo", ann=a_pic, onion=2, onion_dt=F(2)),
    Beat(F(47), "La petite tend son pic à son tour (4 images plus tard) et s'étire vers la géante. Les deux pics vont se toucher au milieu.",
         "in_cubic", ann=a_cou, onion=2, onion_dt=F(2)),
    Beat(F(58), "Cou tendu, affiné de 48 à 18 px ; la géante gonfle de 16 %. La vidéo s'ouvre dans la géante (4 i.) puis coule dans le cou.",
         "in_cubic", ann=a_tension, onion=0),
    Beat(F(67), "Claquement : la bulle est aspirée ←, la géante recule de 26 px puis balaie le cadre → : accélère 3,5 images, freine 14. Front étiré à 130 %.",
         "in_cubic", ann=a_balayage, onion=2, onion_dt=F(1)),
    Beat(F(92), "Plein cadre vidéo : la plaque encaisse l'impact (+5 %, amorti) et continue de pousser. Raccord en mouvement.",
         "out_cubic", onion=0),
])


# =================================================================== OUTRO (4,0 s)
XB0, RB = 700, 128                           # la bulle laissée par le vert
T_SNAP = F(27)
T_LOGO = F(54)

CXO = Track((0, CX), (F(2), CX - 30, "out_cubic"),                                  # recul (anticipation)
            (F(5), 1080, "in_cubic"), (F(15), W, "out_cubic"),                       # le vert se retire →
            (F(19), W), (F(27), 2010, "in_cubic"),                                   # il tire sur le cou
            (F(33), 2640, "in_expo"))                                                # libéré, il sort à droite
R_settle = Track((F(15), 548), (F(23), 470, "ressort"))
xb_o = Track((F(15), XB0), (F(27), XB0 + 90, "in_cubic"),                           # la bulle est tirée →
             (F(31), XB0 - 50, "out_cubic"),                                         # rupture : recul ←
             (F(43), CX, "out_back"))                                                # rebond jusqu'au centre
pull = Track((F(17), 0.0), (F(27), 1.0, "in_cubic"))
h_o = Track((F(6), 0.7), (F(17), 0.22, "out_cubic"), (F(27), 0.035, "in_cubic"))
stub = Track((T_SNAP, 1.0), (T_SNAP + F(5), 0.0, "out_cubic"))                     # restes du cou qui se rétractent
pinch = Track((F(45), 1.0), (F(48), 0.88, "out_cubic"), (F(49), 1.0, "out_cubic"))  # anticipation de la division
split = Track((F(48), 0.0), (F(54), 1.0, "out_cubic"))
travel = Track((F(53), 0.0), (F(63), 1.0, "emphase"))
zv_out = Track((0, 1.16), (F(2), 1.19, "linear"), (F(17), 0.9, "out_cubic"), (F(33), 0.8, "linear"))


def giant_R_o(t):
    cx = CXO(t)
    if t < F(15):
        return math.hypot(max(W - cx, 0.0), 548)
    return R_settle(t) * breathe(t, 0.012, 1.0)


def outro(t):
    zv = zv_out(t)
    cx, R = CXO(t), giant_R_o(t)
    if t < F(7) and cx + R >= W and covered(cx, R):
        return [video(zv, ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    xb = xb_o(t)
    rb = RB * breathe(t, 0.02, 0.9)
    if t < F(45):
        # étirement : tirée vers la droite (œuf), recul écrasé à la rupture, traînée, impact au centre
        sx = (1 + 0.18 * pull(t)) if t < T_SNAP else 1.0
        sx *= squash(t, T_SNAP, F(8), -0.2) * squash(t, F(40), F(9), 0.24)
        sx *= stretch(speed(xb_o, t), 13000, 0.3) if t >= T_SNAP else 1.0
        sx = lim(sx)
        rbk = rb * min(sx, 1 / sx)
        parts = [ellipse_cw(xb, rb * sx, rb / sx)]
        if t < T_SNAP:
            parts.append(link(xb, rbk, cx, R, h_o(t) * rbk))
        else:
            u = stub(t)
            if u > 0:                                                           # les deux moitiés du cou reculent
                nk = neck(xb_o(T_SNAP), RB, CXO(T_SNAP), giant_R_o(T_SNAP), 0.035 * RB)
                xn = nk[1] if nk else (xb + cx) / 2
                rp = 4 + 10 * u
                xp = lerp(xb + rbk - rp - 4, xn - 40 + (xb - xb_o(T_SNAP)), u)
                parts += [link(xb, rbk, xp, rp, 0.5 * rp), circle_cw(xp, rp)]
                xq = lerp(cx - R + rp + 4, xn + 40 + (cx - CXO(T_SNAP)), u)
                parts += [link(xq, rp, cx, R, 0.5 * rp), circle_cw(xq, rp)]
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": " ".join(parts), "pts": [(xb, AXIS)]})
        if cx - R < W:                                                          # la vidéo (géante) par-dessus
            vl = speed(lambda u: CXO(u) - giant_R_o(u), t)
            sxl = 1 + min(0.28, abs(vl) / 22000) if t < F(17) else 1.0
            L.append(video(zv, half_front(cx, R, R * sxl, side="left"), ghost=t < F(17)))
        return L
    # charte 3.4-01 : pincement, division, rupture ; les moitiés deviennent les points du logo
    u, v = split(t), travel(t)
    r2 = RB / math.sqrt(2)
    gx = LG["dot_g"][0]
    e_snap = 1.7 * r2
    spread = e_snap * u + (CX - gx - e_snap) * v
    r = lerp(r2 if u > 0 else rb, LG["dot_r"] * breathe(t, 0.2, 1.1), v)
    c1, c2 = CX - spread, CX + spread
    if u <= 0:
        sx = pinch(t)
        dd = ellipse_cw(CX, rb * sx, rb / sx)
    elif u < 0.55:
        dd = link(c1, r, c2, r, 0.5 * r * (1 - u))
    elif u < 0.88:
        dd = link(c1, r, c2, r, r * 0.2 * (0.88 - u) / 0.33 + 0.8)
    else:
        sx = lim(squash(t, F(53), F(8), -0.16))
        dd = ellipse_cw(c1, r * sx, r / sx) + " " + ellipse_cw(c2, r * sx, r / sx)
    col = mix_hex(ORANGE, WHITE, prog(t, F(53), F(61)))
    L.append({"k": "fill", "id": "points-logo", "fill": col, "d": dd, "pts": [(c1, AXIS), (c2, AXIS)]})
    return L


def outro_full(t):
    L = outro(t)
    dots = [x for x in L if x.get("id") == "points-logo"]
    rest = [x for x in L if x.get("id") != "points-logo"]
    return rest + endcard(t, T_LOGO, dots=False, extra=dots)


def a_retrait(t):
    return arrow(200, AXIS - 420, 1000, AXIS - 420)


def a_laisse(t):
    return arrow(1150, AXIS - 330, 1600, AXIS - 330) + arrow(XB0 - 330, AXIS, XB0 - 180, AXIS)


def a_tire(t):
    return arrow(XB0 - 100, AXIS - 220, XB0 + 30, AXIS - 220) + arrow(1700, AXIS - 300, 1860, AXIS - 300)


def a_rupture(t):
    return arrow(1080, AXIS - 120, 960, AXIS - 120) + arrow(1260, AXIS - 120, 1380, AXIS - 120)


def a_sortie(t):
    return arrow(XB0 - 40, AXIS - 220, XB0 - 160, AXIS - 220) + arrow(1600, AXIS - 300, 1880, AXIS - 300)


def a_rebond(t):
    return curved_arrow(640, AXIS - 200, 800, AXIS - 320, 900, AXIS - 200)


def a_division(t):
    return arrow(CX - 230, AXIS - 200, CX - 360, AXIS - 200) + arrow(CX + 230, AXIS - 200, CX + 360, AXIS - 200)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(6), "Plein cadre ; la masse recule de 30 px (anticipation) puis se retire vers la droite en 13 images, bord arrière étiré.",
         "inout_expo", ann=a_retrait, onion=2, onion_dt=F(2)),
    Beat(F(10), "En partant, le vert découvre le dégradé et laisse une bulle orange collée à lui : cacahuète, puis cou qui s'allonge.",
         "inout_expo", ann=a_laisse, onion=2, onion_dt=F(2)),
    Beat(F(23), "La géante se cale à x = 1920, coupée en son milieu (548 -> 470 px en ressort), puis tire : la bulle suit de 90 px, en œuf.",
         "in_cubic", ann=a_tire, onion=2, onion_dt=F(2)),
    Beat(F(28), "Rupture nette : le cou, affiné à 3,5 %, casse. Les deux restes se rétractent en 5 images, la bulle recule écrasée à 80 %.",
         "out_cubic", ann=a_rupture, onion=2, onion_dt=F(1)),
    Beat(F(32), "La géante, libérée, sort à droite en 6 images (in_expo) en emportant la vidéo ; la bulle repart vers le centre.",
         "in_expo", ann=a_sortie, onion=2, onion_dt=F(2)),
    Beat(F(40), "Rebond au centre : dépassement de 30 px (out_back) et écrasement de 124 % à l'arrivée, puis respiration.",
         "out_back", ann=a_rebond, onion=2, onion_dt=F(2)),
    Beat(F(51), "Charte 3.4-01 : pincement à 88 % (3 images), puis division ; le col s'affine et casse à 3,4 r, les moitiés reculent.",
         "out_cubic", ann=a_division, onion=2, onion_dt=F(1)),
    Beat(F(90), "Les moitiés sont devenues les points du logo ; « sfeer » s'est ouvert, l'arabe aussi. Tenue vivante, poussée lente.",
         "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "Un vrai coup de théâtre : tout se tend lentement (points, tremblement, cou), puis tout claque en une demi-seconde.",
        "La vidéo arrive par la forme : elle coule dans la géante puis dans le cou, et c'est la masse qui l'apporte.",
        "L'outro rejoue le geste à l'envers et finit sur les deux points du logo. Marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "La géante est coupée à son milieu par le bord gauche (2.48), puis par le bord droit dans l'outro. Tous les centres sur l'axe.",
        "Ajouts au croquis : la petite bulle tend aussi son pic (les deux se rejoignent), et la vidéo coule dans le cou avant le claquement.",
        "Écarts à valider : la géante dépasse la hauteur du cadre pendant le balayage, et son milieu (8 images) quand elle tire dans l'outro.",
    ]),
    ("Mouvement", [
        "Rampe de taille et de vitesse sur les points, tremblement, anticipation de la géante (84 -> 60 px), recul avant le claquement.",
        "Balayage : 3,5 images d'accélération puis 14 de freinage, front étiré à 130 % ; la plaque encaisse l'impact puis pousse toujours.",
        "Outro : retrait, tension, rupture nette avec recul des deux moitiés, rebond, division 3.4-01, carton vivant.",
    ]),
]
