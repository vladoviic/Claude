"""Concept original O1 : « Le Relais, la bulle qui donne ».

Une grande bulle orange, coupée à son milieu par le bord gauche, donne de sa matière :
une bulle naît, puis une troisième (charte 3.5-02), qui naît fenêtre sur la vidéo.
La valeur circule dans les cous (gorgées qui traversent le cou, onde qui accélère),
puis on plonge dans la fenêtre sans jamais lâcher le lien.
Outro : la vidéo est aspirée dans la bulle, la valeur repart vers la gauche, le cou casse
net, et le dernier relais écrit le logo (3.5-02 en petit : un point en fait naître un second).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, GREEN, GREEN_D, GREEN_L, Anim, Beat, Track, breathe, clamp01, lerp, prog  # noqa: E402
from blocks import LG, endcard, squash, video  # noqa: E402
from sfeer_svg import AXIS, H, ORANGE, WHITE, W, _neck_circle, arrow, bridge_d, curved_arrow, f, mix_hex  # noqa: E402

CX = W / 2

META = {
    "id": "o1_relais",
    "num": "O1",
    "title": "Le Relais",
    "logline": "Une grande bulle rognée au bord gauche donne de sa matière : une bulle naît, puis une troisième qui "
               "s'ouvre sur la vidéo. La valeur circule dans les cous, et on plonge dans la fenêtre sans lâcher le lien.",
}


# =================================================================== outils géométriques
def circle_cw(cx, r):
    """Cercle sur l'axe, tracé dans le sens horaire (même sens que bridge_d : union sans trou)."""
    return f"M{f(cx - r)} {AXIS}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z"


def ellipse_cw(cx, rx, ry):
    return f"M{f(cx - rx)} {AXIS}a{f(rx)} {f(ry)} 0 1 1 {f(2 * rx)} 0a{f(rx)} {f(ry)} 0 1 1 {f(-2 * rx)} 0Z"


def hull_cw(c1, c2):
    """Enveloppe convexe de deux cercles (x, r), x1 < x2 : col plein, arcs corrects même si r1 != r2."""
    (x1, r1), (x2, r2) = c1, c2
    d = x2 - x1
    ang = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, AXIS - r1 * ny), (x2 + r2 * nx, AXIS - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, AXIS + r2 * ny), (x1 + r1 * nx, AXIS + r1 * ny)
    l1, l2 = (1 if ang > 0 else 0), (1 if ang < 0 else 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


def link(c1, c2, h):
    """Pont de la charte entre deux cercles (x, r) : gère le chevauchement (cacahuète) et l'inclusion."""
    (x1, r1), (x2, r2) = sorted([c1, c2])
    d = x2 - x1
    if d <= abs(r1 - r2) + 0.5:
        x, r = (x1, r1) if r1 >= r2 else (x2, r2)
        return circle_cw(x, r)
    rmin = min(r1, r2)
    if d < r1 + r2:
        a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
        yi = math.sqrt(max(r1 * r1 - a * a, 0))
        ov = clamp01((r1 + r2 - d) / max(rmin, 1))
        h = max(h, yi + (rmin - yi) * 0.35 * ov + 0.5)
    h = min(h, 0.97 * rmin)
    if _neck_circle((x1, AXIS, r1), (x2, AXIS, r2), h) is None:
        return hull_cw((x1, r1), (x2, r2))
    return bridge_d((x1, AXIS, r1), (x2, AXIS, r2), h)


def blob(bubs, necks, lid, fill=ORANGE, ghost=True, track=None):
    """Chaîne de bulles. bubs : [(x, r, sx)], sx = étirement horizontal (volume conservé : ry = r / sx).
    necks[i] : demi-épaisseur du cou entre i et i+1 (None = séparées).
    Les cous s'accrochent au cercle intérieur ; l'ellipse étirée se superpose (même sens de tracé)."""
    core = [(x, r * min(sx, 1 / sx)) for x, r, sx in bubs]
    parts, linked = [], set()
    for i, h in enumerate(necks):
        a, b = core[i], core[i + 1]
        if h is None or a[1] < 1 or b[1] < 1:
            continue
        parts.append(link(a, b, h))
        linked |= {i, i + 1}
    for i, (x, r, sx) in enumerate(bubs):
        if r < 0.5:
            continue
        if abs(sx - 1) > 1e-3:
            parts.append(ellipse_cw(x, r * sx, r / sx))
        elif i not in linked:
            parts.append(circle_cw(x, r))
    idx = range(len(bubs)) if track is None else track
    pts = [(bubs[i][0], AXIS) for i in idx if bubs[i][1] >= 0.5]
    return {"k": "fill", "id": lid, "fill": fill, "d": " ".join(parts), "pts": pts, "ghost": ghost}


# =================================================================== plaque verte et fenêtre
HATCH = " ".join(f"M{i * 90 - 1200} -1200L{i * 90 + 2400} 2280" for i in range(-40, 75))


def plate(uid, cx=CX, zoom=1.0):
    """Même plaque que blocks.video, mais centrée sur la fenêtre (cx) : identique à zoom >= 1 et cx = 960."""
    z = max(zoom, 0.05)
    return (f'<g id="{uid}-plaque"><rect x="-2400" y="-1600" width="6720" height="4280" fill="{GREEN}"/>'
            f'<g transform="translate({f(cx)} {AXIS}) scale({f(z)}) translate({f(-CX)} {-AXIS})">'
            f'<path d="{HATCH}" stroke="{GREEN_D}" stroke-width="16" fill="none"/>'
            f'<rect x="{W * .1}" y="{H * .1}" width="{W * .8}" height="{H * .8}" fill="none" stroke="{GREEN_L}" '
            f'stroke-width="6" stroke-dasharray="30 20"/>'
            f'<path d="M{W / 2 - 60} {H / 2}H{W / 2 + 60}M{W / 2} {H / 2 - 60}V{H / 2 + 60}" stroke="{GREEN_L}" stroke-width="8"/>'
            f'<circle cx="{W / 2}" cy="{H / 2}" r="150" fill="none" stroke="{GREEN_L}" stroke-width="6"/>'
            f'<text x="{W / 2}" y="{H / 2 + 250}" font-family="Inter, Arial, sans-serif" font-size="64" '
            f'font-weight="700" fill="{GREEN_L}" text-anchor="middle" letter-spacing="12">VIDÉO</text></g></g>')


def window(uid, clip_d, content, iris=None):
    """Fenêtre : contenu découpé par la bulle, et par le disque iris (x, r) qui ouvre ou ferme la vidéo."""
    s = f'<clipPath id="{uid}-c"><path d="{clip_d}"/></clipPath>'
    inner = content
    if iris is not None:
        s += f'<clipPath id="{uid}-i"><circle cx="{f(iris[0])}" cy="{AXIS}" r="{f(max(iris[1], 0.1))}"/></clipPath>'
        inner = f'<g clip-path="url(#{uid}-i)">{inner}</g>'
    return {"k": "raw", "svg": s + f'<g id="{uid}" clip-path="url(#{uid}-c)">{inner}</g>'}


# =================================================================== outils de mouvement
def pulse(t, t0, dur):
    """Bosse douce 0 -> 1 -> 0 entre t0 et t0 + dur (en s)."""
    u = (t - t0) / dur
    return math.sin(math.pi * u) ** 2 if 0 < u < 1 else 0.0


def speed(fn, t, dt=0.02):
    return (fn(t + dt) - fn(t - dt)) / (2 * dt)


def stretch(fn, t, k=7000.0, cap=1.16, v0=900.0):
    """Étirement dans le sens de la vitesse horizontale (px/s) au-delà de v0, plafonné."""
    return min(cap, 1 + max(0.0, abs(speed(fn, t)) - v0) / k)


def bead(x0, x1, h, u):
    """Gorgée : petite bulle qui traverse le cou de x0 à x1 (u de 0 à 1), plus grosse au milieu."""
    return (lerp(x0, x1, u), h * (1.25 + 1.5 * math.sin(math.pi * clamp01(u))), 1.0)


# =================================================================== INTRO (3,6 s)
# A : grande bulle coupée par le bord gauche (centre x = 0)
rA_t = Track((0, 0), (F(3), 74, "out_cubic"), (F(5), 54, "inout_cubic"),       # pointe puis recule (anticipation)
             (F(13), 330, "out_back"),                                             # éclosion, dépassement 10 %
             (F(21), 300, "inout_cubic"), (F(30), 280, "inout_cubic"),             # donne à B puis à C
             (F(46), 0, "inout_cubic"))                                            # se vide entièrement dans B
sxA_t = Track((F(9), 1.0), (F(13), 0.9, "inout_cubic"), (F(19), 1.0, "out_back"))  # inspire avant de donner

# B : naît du flanc de A, puis prend sa place au bord
xB_t = Track((F(13), 190), (F(22), 615, "out_back"),
             (F(25), 596, "out_cubic"), (F(30), 615, "out_back"),                 # recul quand C part (3 %)
             (F(32), 615), (F(46), 0, "inout_cubic"),                              # le relais : B glisse au bord
             (F(61), 0), (F(64), 0), (F(75), -700, "in_cubic"))                    # arrachée hors champ au saut
rB_t = Track((F(13), 0), (F(19), 168, "out_cubic"), (F(24), 150, "inout_cubic"),
             (F(32), 150), (F(46), 250, "inout_cubic"), (F(60), 330, "inout_cubic"),
             (F(64), 348, "inout_cubic"), (F(75), 380, "in_cubic"))
sxB_t = Track((F(20), 1.0), (F(23), 0.9, "inout_cubic"), (F(28), 1.0, "out_back"))  # inspire avant C

# C : naît de B, fenêtre ; s'approche, inspire, saute vers la caméra
xC_t = Track((F(22), 650), (F(31), 1115, "out_back"),
             (F(32), 1115), (F(46), 720, "inout_cubic"),                           # recule avec la chaîne
             (F(60), 940, "inout_cubic"), (F(64), 912, "inout_cubic"),            # approche puis inspire
             (F(70), CX, "out_cubic"))
rC_t = Track((F(22), 0), (F(29), 214, "out_cubic"), (F(33), 200, "inout_cubic"),
             (F(46), 290, "inout_cubic"), (F(60), 470, "inout_cubic"),
             (F(64), 432, "inout_cubic"),                                          # inspiration (-8 %)
             (F(76), 1900, "plongee"))                                             # le saut
irisC = Track((F(24), 0.0), (F(31), 1.0, "out_cubic"))                             # la vidéo coule depuis le cou
zC_t = Track((F(24), 0.40), (F(46), 0.50, "linear"), (F(60), 0.64, "inout_cubic"), (F(64), 0.62, "inout_cubic"),
             (F(70), 1.0, "in_cubic"), (F(90), 1.14, "out_cubic"))                 # contre-zoom plus lent
hBC_t = Track((F(26), 18), (F(46), 22), (F(60), 26), (F(64), 34), (F(74), 11, "in_cubic"))

# gorgées : deux ondes A -> B -> C, la seconde plus rapide
WAVES_IN = [  # (début, durée dans le cou A-B, début, durée dans le cou B-C) en images
    (31, 6, 35, 5),
    (39, 4, 42, 3),
    (99, 1, 51, 3),                                  # 3e gorgée : B -> C seulement, pendant l'approche
]


def intro_state(t):
    xA, rA = 0.0, rA_t(t) * (1 - 0.1 * pulse(t, F(30), F(5)) - 0.08 * pulse(t, F(38), F(4)))
    xB, rB = xB_t(t), rB_t(t)
    xC, rC = xC_t(t), rC_t(t)
    if rA > 1:
        rA *= breathe(t, 0.012, 0.9)
    # onde de taille : le receveur gonfle après le passage de la gorgée
    rB *= 1 + 0.16 * pulse(t, F(34), F(6)) + 0.18 * pulse(t, F(40), F(4))
    rB *= 1 + 0.1 * pulse(t, F(49), F(5))                                     # 3e gorgée pendant l'approche
    rC *= (1 + 0.14 * pulse(t, F(39), F(6)) + 0.18 * pulse(t, F(44), F(4)) + 0.1 * pulse(t, F(53), F(5))) \
        * breathe(t, 0.015, 1.1, 0.3)
    sxA = sxA_t(t) * squash(t, F(12), F(9), 0.1)
    sxB = stretch(xB_t, t) * sxB_t(t) * squash(t, F(21), F(9), -0.12)
    sxC = stretch(xC_t, t) * (squash(t, F(30), F(9), -0.12) if t < F(46) else 1.0)
    if t >= F(64):                                   # B arrachée : étirée dans le sens de la traction
        sxB = 1 + 0.26 * prog(t, F(64), F(72), "in_cubic")
        sxC = 1.0
    return xA, rA, sxA, xB, rB, sxB, xC, rC, sxC


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    xA, rA, sxA, xB, rB, sxB, xC, rC, sxC = intro_state(t)
    z = zC_t(t) + 0.3 * max(0.0, t - F(70))          # la poussée ne s'arrête jamais
    # plein cadre : la fenêtre couvre tout -> plaque standard (raccord invisible, zoom >= 1)
    if rC >= math.hypot(max(xC, W - xC), AXIS) + 2 and t >= F(68):
        return [video(z, ghost=False)]
    bubs = [(xA, rA, sxA), (xB, rB, sxB), (xC, rC, sxC)]
    hAB = 0.1 * min(rA, max(rB, 1)) + 12 * sum(pulse(t, F(a), F(d)) for a, d, _, _ in WAVES_IN)
    hBC = hBC_t(t)
    necks = [hAB if rA > 1 and rB > 1 else None, hBC if rB > 1 and rC > 1 else None]
    # gorgées : billes qui traversent les cous (insérées dans la chaîne)
    chain, cn, track = [bubs[0]], [], [0]
    for i in (0, 1):
        x0 = bubs[i][0] + bubs[i][1] * 0.55
        x1 = bubs[i + 1][0] - bubs[i + 1][1] * 0.55
        for a, d, b, e in WAVES_IN:
            s0, dd = (a, d) if i == 0 else (b, e)
            u = (t - F(s0)) / F(dd)
            if 0 < u < 1 and necks[i] is not None and bubs[i][1] > 30:
                chain.append(bead(x0, x1, necks[i], u))
                cn.append(necks[i])
                break
        cn.append(necks[i])
        chain.append(bubs[i + 1])
        track.append(len(chain) - 1)
    L.append(blob(chain, cn, "chaine", track=track))
    # fenêtre dans C : la vidéo coule depuis le cou puis remplit la bulle
    if rC > 1 and t >= F(24):
        u = irisC(t)
        iris = None if u >= 1 else (xC - rC + u * rC, rC * 1.03 * u)
        cd = ellipse_cw(xC, rC * sxC, rC / sxC) if abs(sxC - 1) > 1e-3 else circle_cw(xC, rC)
        L.append(window("fenetre-c", cd, plate("pc", xC, z), iris))
    return L


def a_pop(t):
    return arrow(40, AXIS, 300, AXIS) + arrow(330, AXIS - 300, 395, AXIS - 360) + arrow(330, AXIS + 300, 395, AXIS + 360)


def a_naissance_b(t):
    return arrow(330, AXIS, 640, AXIS)


def a_naissance_c(t):
    return arrow(760, AXIS, 1080, AXIS) + arrow(600, AXIS - 210, 560, AXIS - 210)


def a_gorgee(t):
    return curved_arrow(150, AXIS - 360, 420, AXIS - 470, 690, AXIS - 300) + curved_arrow(760, AXIS - 300, 860, AXIS - 420, 980, AXIS - 300)


def a_relais(t):
    return arrow(560, AXIS - 300, 260, AXIS - 300) + arrow(1100, AXIS + 340, 860, AXIS + 340)


def a_approche(t):
    return arrow(820, AXIS, 1010, AXIS) + "".join(arrow(CX + dx * 360, AXIS + dy * 250, CX + dx * 520, AXIS + dy * 400)
                                                for dx in (-1, 1) for dy in (-1, 1) if dx > 0)


def a_saut(t):
    return arrow(300, AXIS + 420, 60, AXIS + 420) + "".join(
        arrow(CX + dx * 560, AXIS + dy * 330, CX + dx * 860, AXIS + dy * 500) for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 3.6, intro, [
    Beat(F(9), "Une grande bulle orange éclot au bord gauche, coupée à son milieu : pointe, recule 2 images, puis jaillit avec 10 % de dépassement.",
         "out_back", ann=a_pop, onion=3, onion_dt=F(2)),
    Beat(F(18), "A inspire (écrasée à 90 % sur 4 images) puis donne : B jaillit de son flanc vers la droite, étirée à 115 % dans sa course.",
         "out_back", ann=a_naissance_b, onion=3, onion_dt=F(2)),
    Beat(F(28), "B fait naître C (3.5-02) et recule de 3 % : action, réaction. La vidéo coule du cou dans C et la remplit en 7 images.",
         "out_cubic", ann=a_naissance_c, onion=2, onion_dt=F(3)),
    Beat(F(37), "Le relais : une gorgée traverse chaque cou de gauche à droite et le receveur gonfle de 16 %. La 2e onde va 1,5 fois plus vite.",
         "inout_cubic", ann=a_gorgee, onion=0),
    Beat(F(45), "A se vide dans B, qui glisse au bord et se recoupe sur sa médiane. C recule de 400 px avec la chaîne : c'est l'élan.",
         "inout_cubic", ann=a_relais, onion=2, onion_dt=F(4)),
    Beat(F(58), "Approche : C file au centre et passe de 290 à 470 px de rayon, tenue par un cou fin. La vidéo dedans grossit 2 fois moins vite.",
         "inout_cubic", ann=a_approche, onion=2, onion_dt=F(4)),
    Beat(F(67), "Saut : C inspire (−4 %) puis fonce vers la caméra (courbe plongée, plein cadre en 5 images). B, encore liée, est arrachée à gauche.",
         "plongee", ann=a_saut, onion=2, onion_dt=F(2)),
    Beat(F(84), "Plein cadre vidéo : la plaque continue de pousser (100 → 116 %) en décélérant. On raccorde sur un plan en mouvement.",
         "out_cubic", onion=0),
])


# =================================================================== OUTRO (4,0 s)
T0_LOGO = F(52)                      # début du carton (mot révélé de gauche à droite, derrière le point)
DOT_R = LG["dot_r"]
XG, XD = LG["dot_g"][0], LG["dot_d"][0]

zO_t = Track((0, 1.10), (F(4), 1.17, "linear"), (F(15), 0.6, "out_cubic"), (F(30), 0.5, "linear"))
rCo_t = Track((F(4), 1160), (F(14), 470, "out_cubic"), (F(15), 470), (F(36), 110, "inout_cubic"))
xCo_t = Track((F(4), CX), (F(14), 1010, "out_cubic"), (F(15), 1010), (F(36), 640, "inout_cubic"),
              (F(46), 662, "in_cubic"), (F(55), XG, "out_back"))
rBo_t = Track((F(5), 400), (F(15), 330, "out_cubic"), (F(36), 372, "inout_cubic"))
xBo_t = Track((F(4), -620), (F(15), 0, "out_back"), (F(46), 0), (F(54), -470, "out_cubic"))
closeC = Track((F(17), 0.0), (F(28), 1.0, "in_cubic"))      # la vidéo est aspirée vers le cou
hBCo_t = Track((F(4), 10), (F(15), 22, "out_cubic"), (F(36), 20), (F(46), 2.5, "in_cubic"))
SNAP = F(46)
WAVES_OUT = [(16, 6, 19, 6), (24, 5, 27, 5), (31, 3, 33, 4)]   # (C donne, durée, B reçoit, durée)


def reveal(t):
    """Révélation du mot du carton (identique à blocks.endcard, mode gauche)."""
    return Track((T0_LOGO, 0), (T0_LOGO + F(14), 1, "emphase"))(t)


def front(t):
    """Bord droit de la partie révélée du mot (même cache que blocks.word, mode gauche)."""
    return LG["word_x"] - 4 + (LG["word_w"] + 8) * reveal(t)


def dots_state(t):
    """Les deux points du logo : C (gauche) et D, né de C, qui file juste devant la révélation du mot."""
    xC = xCo_t(t)
    rC = Track((F(46), 105), (F(51), 66, "out_cubic"), (F(57), DOT_R * 1.4, "out_cubic"), (F(62), DOT_R))(t)
    tb = T0_LOGO - F(2)
    col = mix_hex(ORANGE, WHITE, prog(t, F(47), F(57)))
    if t < tb:
        return [(xC, rC, squash(t, SNAP, F(10), 0.22))], [], col
    rD = Track((tb, 0), (tb + F(3), 52, "out_cubic"), (tb + F(14), DOT_R, "inout_cubic"))(t)

    def xD_at(s):
        rv = reveal(s)
        return min(XD, front(s) + Track((tb, 0), (tb + F(3), 52, "out_cubic"))(s) * (1 - rv) + 12 + 60 * rv)
    xD = xD_at(t)
    bre = prog(t, tb + F(14), tb + F(22))
    rC = lerp(rC, DOT_R * breathe(t, 0.2, 1.1), bre)
    rD = lerp(rD, DOT_R * breathe(t, 0.2, 1.1, 0.25), bre)
    neck = [min(rC, rD) * 0.35] if t < tb + F(4) else [None]       # le cou C-D casse net à 4 images
    xC -= 8 * pulse(t, tb + F(4), F(4))                            # recul de C à la rupture
    sxD = stretch(xD_at, t, k=5000, cap=1.3)
    return [(xC, rC, squash(t, SNAP, F(10), 0.22)), (xD, rD, sxD)], neck, col


def outro_shapes(t):
    if t < F(4):
        return [video(zO_t(t), ghost=False)]
    L = [{"k": "bg", "v": "gradient"}]
    xB, rB = xBo_t(t), rBo_t(t)
    xC, rC = xCo_t(t), rCo_t(t)
    if t < SNAP:
        rC *= 1 - 0.1 * sum(pulse(t, F(a), F(d)) for a, d, _, _ in WAVES_OUT)
        rB *= 1 + 0.08 * sum(pulse(t, F(b), F(e)) for _, _, b, e in WAVES_OUT)
        if t >= F(36):                                             # merci : échange de tailles 3.3-02
            m = pulse(t, F(36), F(10))
            rC, rB = rC * (1 + 0.36 * m), rB * (1 - 0.05 * m)
        rB *= breathe(t, 0.012, 1.0)
        h = hBCo_t(t) * (1 + 1.2 * sum(pulse(t, F(a + 1), F(d)) for a, d, _, _ in WAVES_OUT))
        chain, cn = [(xB, rB, 1.0)], []
        for a, d, _, _ in WAVES_OUT:                               # gorgées de droite à gauche
            u = (t - F(a + 1)) / F(d)
            if 0 < u < 1:
                chain.append(bead(xC - rC * 0.55, xB + rB * 0.55, h, u))
                cn.append(h)
                break
        cn.append(h)
        sxC = squash(t, F(13), F(9), -0.1) * stretch(xCo_t, t, k=7000, cap=1.12)
        chain.append((xC, rC, sxC))
        L.append(blob(chain, cn, "chaine", track=[0, len(chain) - 1]))
        u = closeC(t)
        if u < 1 and rC > 1:
            iris = (lerp(xC, xC - rC, u), rC * 1.03 * (1 - u)) if u > 0 else None
            cd = ellipse_cw(xC, rC * sxC, rC / sxC) if abs(sxC - 1) > 1e-3 else circle_cw(xC, rC)
            L.append(window("fenetre-c", cd, plate("pc", xC, zO_t(t)), iris))
        return L
    # après la rupture : B recule et sort à gauche ; restes de cou qui se rétractent
    u = prog(t, SNAP, SNAP + F(5), "out_cubic")
    if xB + rB > 0:
        nub = [(xB + rB * 0.8 + 70 * (1 - u), 14 * (1 - u) + 0.1, 1.0)] if u < 1 else []
        L.append(blob([(xB, rB * breathe(t, 0.012, 1.0), 1.0)] + nub, [8 * (1 - u) + 1] if nub else [], "bulle-b"))
    return L


def outro(t):
    L = outro_shapes(t)
    if t < SNAP:
        return L
    bubs, neck, col = dots_state(t)
    u = prog(t, SNAP, SNAP + F(5), "out_cubic")
    if u < 1:                                                      # reste de cou côté C
        bubs = [(bubs[0][0] - bubs[0][1] * 0.8 - 60 * (1 - u), 10 * (1 - u) + 0.1, 1.0)] + bubs
        neck = [6 * (1 - u) + 1] + neck
        track = list(range(1, len(bubs)))
    else:
        track = None
    pts_layer = blob(bubs, neck, "points-logo", fill=col, track=track)
    card = endcard(t, T0_LOGO, dots=False, word_mode="gauche", extra=[pts_layer])
    # poussée supplémentaire (+5 %/s) : le carton ne s'arrête jamais
    return L + [{"k": "group", "s": 1 + 0.05 * max(0.0, t - T0_LOGO), "layers": card}]


def a_aspiration(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 500, CX + dx * 620, AXIS + dy * 330) for dx in (-1, 1) for dy in (-1, 1)) \
        + arrow(40, AXIS + 360, 260, AXIS + 360)


def a_retour(t):
    return curved_arrow(1060, AXIS - 420, 760, AXIS - 520, 420, AXIS - 380)


def a_fermeture(t):
    return arrow(940, AXIS - 260, 700, AXIS - 260)


def a_merci(t):
    return "".join(arrow(640 + dx * 120, AXIS + dy * 120, 640 + dx * 200, AXIS + dy * 200) for dx in (-1, 1) for dy in (-1, 1) if dx > 0) \
        + arrow(420, AXIS - 300, 360, AXIS - 360)


def a_rupture(t):
    return arrow(330, AXIS - 200, 120, AXIS - 200) + arrow(560, AXIS - 120, 700, AXIS - 120)


def a_ecrit(t):
    return arrow(780, AXIS - 120, 1180, AXIS - 120)


OUTRO = Anim("OUTRO", 4.0, outro, [
    Beat(F(7), "Aspiration : la vidéo plein cadre est avalée par la bulle C (rayon 1160 → 470 px en 10 images). B rentre par la gauche, déjà liée.",
         "out_cubic", ann=a_aspiration, onion=2, onion_dt=F(2)),
    Beat(F(19), "La valeur repart vers la gauche : 3 gorgées de C vers B, chacune plus rapide (6, 5 puis 3 images). C fond de 470 à 110 px.",
         "inout_cubic", ann=a_retour, onion=0),
    Beat(F(25), "La vidéo est aspirée par le cou : le disque vert glisse vers la gauche et se ferme en 11 images, en accélérant.",
         "in_cubic", ann=a_fermeture, onion=0),
    Beat(F(41), "Merci (3.3-02) : C regonfle de 36 % et B cède 5 %, puis tout revient. Le cou s'affine jusqu'à 5 px : tension.",
         "inout_cubic", ann=a_merci, onion=2, onion_dt=F(3)),
    Beat(F(48), "Rupture nette : le cou casse. B recule et sort à gauche en 8 images, C rebondit vers la droite et s'écrase à 122 %.",
         "out_back", ann=a_rupture, onion=2, onion_dt=F(2)),
    Beat(F(53), "C blanchit et fait naître D (3.5-02 en petit) : le cou casse à la 4e image, D file vers la droite, étirée à 130 %.",
         "emphase", ann=a_ecrit, onion=2, onion_dt=F(1)),
    Beat(F(59), "D écrit le mot en filant devant lui : « sfeer » se révèle de gauche à droite en 14 images, l'arabe suit de droite à gauche.",
         "emphase", onion=2, onion_dt=F(2)),
    Beat(F(92), "Tenue vivante : les deux points respirent (±20 %), poussée lente de 7,5 %/s ; « Powered by RIYADH AIR » est posé en bas.",
         "emphase", onion=0),
])

NOTES = [
    ("Pourquoi ça marche", [
        "SFEER, c'est se donner des points : la bulle qui donne et la gorgée qui traverse le cou montrent l'échange, sans un mot.",
        "La fenêtre naît d'un lien et on y entre sans le lâcher : B tient encore C quand la vidéo prend tout le cadre.",
        "Le logo naît du dernier relais : un point en fait naître un second, qui écrit le mot. Marche avec n'importe quelle vidéo.",
    ]),
    ("Charte et corrections", [
        "Chaîne 3.5-02 depuis la gauche, échange de tailles 3.3-02, porte-image avec cou hors champ (2.50). Centres toujours sur y = 540.",
        "A puis B coupées pile sur leur médiane au bord gauche (2.48). Écarts à valider : B dépasse sa médiane 8 images au saut et à la sortie.",
        "Cous de la charte (épaisseur 5 à 10 % du diamètre) ; carton 3.4-02 centré, l'arabe se révèle de droite à gauche.",
    ]),
    ("Mouvement", [
        "Chaque naissance : inspiration (écrasement 90 %), jaillissement étiré (115 %), dépassement 10 %, rebond amorti.",
        "Onde qui accélère : gorgées de 6, 5, 4 puis 3 images. Rupture nette en outro avec recul des deux moitiés.",
        "Plongée en courbe plongée, plaque en contre-zoom 2 fois plus lent ; plein cadre et carton poussent sans arrêt.",
    ]),
]
