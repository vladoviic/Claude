"""Piste 6 (croquis de la DA) : « le logo replié ».

Le croquis : ·sfeer· entouré de flèches qui tournent (le mot se replie), puis les deux points se
rejoignent en haltère, puis un seul point. C'est la charte 3.4 jouée à rebours. Développé ici : ce point
devient la fenêtre.

INTRO : le mot s'élargit de 4 %, puis se referme comme une fermeture éclair : les deux points en sont les
curseurs et foncent l'un vers l'autre. Contact, col, fusion. Le point fait un pop blanc -> orange, inspire,
puis gonfle en s'étirant à l'horizontale. Une petite bulle-fenêtre naît de lui et ils échangent leurs tailles
(3.3-02) : le col casse, la fenêtre se recentre et la caméra plonge dedans.
OUTRO : le même geste à l'endroit. La vidéo est aspirée en bulle, une bulle orange naît d'elle, elles
échangent leurs tailles, la fenêtre est avalée, la bulle se contracte en point blanc, se divise (3.4-01)
et le mot se rouvre entre les deux points, qui en sont les curseurs (3.4-02).
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import EASE, F, Anim, Beat, Track, breathe, prog, spring  # noqa: E402
from blocks import LG, arabic, drift, endcard, endorse, squash, video  # noqa: E402
from sfeer_svg import (AXIS, FONT, ORANGE, WHITE, W, arrow, bridge_d, f, mix_hex,  # noqa: E402
                       waist_h)

# ressort doux : dépassement 12 % puis un petit rebond (les ressorts du moteur dépassent de 27 à 40 %)
EASE.setdefault("ressort_doux", spring(1.6, 0.55))

CX = W / 2
DG = CX - LG["dot_g"][0]      # 279 px : demi-écart des points du logo
DR = LG["dot_r"]              # 10,9 px : rayon des points du logo
FS, WX, WW = LG["fs"], LG["word_x"], LG["word_w"]
GAP = 0.32 * FS               # 41 px entre un point et le mot
D_CLOSED = GAP + DR           # 51,8 px : demi-écart des points quand le mot est fermé (·e· de 3.4-02)
R_RUN = 24                    # rayon des points lancés : ils prennent de la masse en fonçant
R_ONE = R_RUN * math.sqrt(2)  # 34 px : un point qui a avalé l'autre (même surface)

META = {
    "id": "p06_logo_replie",
    "num": "P6",
    "title": "Le logo replié",
    "logline": "Piste 6 de la DA. Le mot se referme comme une fermeture éclair dont les points sont les curseurs ; "
               "les points fusionnent, virent à l'orange, gonflent et échangent leur taille avec la fenêtre où l'on plonge.",
}


# ------------------------------------------------------------------ outils de forme
def cw_circle(cx, cy, r):
    """Cercle tracé dans le sens horaire, comme les ponts de bridge_d : l'union reste pleine (nonzero)."""
    return (f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0"
            f"a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z")


def neck(c1, c2, t=0.35):
    """Col de la charte : taille de cacahuète au contact, 0,07 r à l'écart maximal (mesuré sur 3.3-01)."""
    rmin = min(c1[2], c2[2])
    gap = abs(c2[0] - c1[0]) - c1[2] - c2[2]
    if gap <= 0:
        return waist_h(c1, c2, t)
    return rmin * (0.07 + 0.27 * math.exp(-2.2 * gap / rmin))


def contact_h(c1, c2):
    """Col qui naît au contact de deux points qui s'approchent (rien tant que l'écart dépasse 0,3 r)."""
    rmin = min(c1[2], c2[2])
    gap = abs(c2[0] - c1[0]) - c1[2] - c2[2]
    if gap <= 0:
        return waist_h(c1, c2, 0.35)
    if gap > 0.3 * rmin:
        return None
    return rmin * (0.02 + 0.32 * (1 - gap / (0.3 * rmin)) ** 1.5)


def split_h(c1, c2):
    """Division 3.4-01 : col qui s'étire et s'affine, puis rupture nette au-delà d'un écart de 1,4 r."""
    rmin = min(c1[2], c2[2])
    gap = abs(c2[0] - c1[0]) - c1[2] - c2[2]
    if gap > 1.4 * rmin:
        return None
    return neck(c1, c2)


def link(c1, c2, h="auto"):
    """Deux bulles reliées par le col de la charte (h=None : séparées)."""
    (x1, _, r1), (x2, _, r2) = c1, c2
    if r1 < 0.5 and r2 < 0.5:
        return ""
    if r1 < 0.5 or r2 < 0.5:
        return cw_circle(*(c1 if r1 >= r2 else c2))
    if abs(x2 - x1) <= abs(r1 - r2) + 0.01:
        return cw_circle(*(c1 if r1 >= r2 else c2))
    if h == "auto":
        h = neck(c1, c2)
    if h is None:
        return cw_circle(*c1) + cw_circle(*c2)
    d = bridge_d(c1, c2, h)
    return hull_d(c1, c2) if "L" in d else d       # col plein : enveloppe juste même à rayons inégaux


def hull_d(c1, c2):
    """Enveloppe convexe de deux bulles (col plein). Les grands arcs sont choisis selon les rayons :
    le repli de bridge_d les suppose égaux et casse la forme quand une bulle avale l'autre."""
    if c2[0] < c1[0]:
        c1, c2 = c2, c1
    (x1, cy, r1), (x2, _, r2) = c1, c2
    d = x2 - x1
    ang = math.asin(max(-1, min(1, (r1 - r2) / d)))
    nx, ny = math.sin(ang), math.cos(ang)
    p1u, p2u = (x1 + r1 * nx, cy - r1 * ny), (x2 + r2 * nx, cy - r2 * ny)
    p2d, p1d = (x2 + r2 * nx, cy + r2 * ny), (x1 + r1 * nx, cy + r1 * ny)
    l1, l2 = (1, 0) if r1 > r2 else (0, 1) if r2 > r1 else (0, 0)
    return (f"M{f(p1u[0])} {f(p1u[1])}L{f(p2u[0])} {f(p2u[1])}A{f(r2)} {f(r2)} 0 {l2} 1 {f(p2d[0])} {f(p2d[1])}"
            f"L{f(p1d[0])} {f(p1d[1])}A{f(r1)} {f(r1)} 0 {l1} 1 {f(p1u[0])} {f(p1u[1])}Z")


_TOK = re.compile(r"[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)")
_ARITY = {"M": 2, "L": 2, "A": 7, "a": 7}


def stretch(d, sx, sy=None, cx=CX, cy=AXIS):
    """Étirement / écrasement d'un tracé autour de (cx, cy), volume conservé (sy = 1/sx)."""
    sy = 1 / sx if sy is None else sy
    if abs(sx - 1) < 1e-4 and abs(sy - 1) < 1e-4:
        return d
    out, buf, cmd = [], [], None
    for tk in _TOK.findall(d):
        if tk.isalpha():
            cmd = tk
            out.append(tk)
            continue
        buf.append(float(tk))
        if len(buf) < _ARITY.get(cmd, 2):
            continue
        if cmd in ("M", "L"):
            x, y = buf
            out.append(f"{f(cx + (x - cx) * sx)} {f(cy + (y - cy) * sy)}")
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = buf
            out.append(f"{f(rx * sx)} {f(ry * sy)} 0 {int(la)} {int(sw)} {f(cx + (x - cx) * sx)} {f(cy + (y - cy) * sy)}")
        elif cmd == "a":
            rx, ry, rot, la, sw, x, y = buf
            out.append(f"{f(rx * sx)} {f(ry * sy)} 0 {int(la)} {int(sw)} {f(x * sx)} {f(y * sy)}")
        buf = []
    return " ".join(out)


def word_cut(xa, xb, s=1.0, uid="mot"):
    """Mot « sfeer » (mêmes position et typo que blocks.word) caché hors de [xa, xb] : un cache, jamais
    une déformation du logo."""
    if xb - xa < 2:
        return []
    tr = f"translate({f(CX)} {AXIS}) scale({f(s)}) translate({f(-CX)} {-AXIS})"
    return [{"k": "raw", "svg":
             f'<clipPath id="{uid}"><rect x="{f(xa)}" y="{f(AXIS - FS * 1.2)}" width="{f(xb - xa)}" height="{f(FS * 1.8)}"/></clipPath>'
             f'<g clip-path="url(#{uid})"><text transform="{tr}" x="{f(WX)}" y="{f(AXIS + FS * 0.26)}" '
             f'font-family="{FONT}" font-size="{f(FS)}" letter-spacing="{f(FS * 0.16)}" fill="{WHITE}" '
             f'textLength="{f(WW)}" lengthAdjust="spacingAndGlyphs">sfeer</text></g>'}]


def speed(track, t, dt=0.02):
    return abs(track(t + dt) - track(t - dt)) / (2 * dt)


def dot(x, r, s, cx=None):
    """Point étiré dans le sens de sa vitesse (s = étirement horizontal, volume conservé)."""
    return stretch(cw_circle(x, AXIS, r), s, cx=x if cx is None else cx)


# =================================================================== INTRO (4,0 s)
g_i = Track((0, 1.0), (F(8), 1.04, "out_cubic"))                   # le mot s'élargit de 4 % (anticipation)
arab_i = Track((0, 1), (F(9), 0, "in_cubic"))
endo_i = Track((F(2), 1), (F(11), 0, "in_cubic"))
# Fermeture éclair : demi-écart des points. Ils suivent l'élargissement, reculent (contre-mouvement de la
# courbe « anticipe ») puis foncent ; la droite part 2 images après et arrive en même temps : contact, fusion.
T_HIT = F(17)
D_G = Track((0, DG), (F(4), DG * 1.035, "out_cubic"), (T_HIT, R_RUN * 1.02, "anticipe"), (F(22), 0, "inout_cubic"))
D_D = Track((0, DG), (F(6), DG * 1.04, "out_cubic"), (T_HIT, R_RUN * 1.02, "anticipe"), (F(22), 0, "inout_cubic"))
R_PAIR = Track((F(7), DR), (T_HIT, R_RUN, "in_cubic"), (F(22), R_ONE, "out_cubic"))
# Point unique : pop de couleur, inspiration, gonflement élastique.
R_ONE_T = Track((F(22), R_ONE), (F(25), 62, "out_back"), (F(29), 44, "in_cubic"), (F(43), 235, "ressort_doux"))
# Naissance de la bulle-fenêtre et échange de tailles (3.3-02)
X_OR = Track((F(40), CX), (F(48), 790, "out_cubic"), (F(59), 600, "inout_cubic"), (F(62), 566, "out_cubic"))
R_OR = Track((F(43), 235), (F(48), 226), (F(59), 92, "inout_cubic"))
X_GR = Track((F(41), CX + 150), (F(49), 1250, "out_back"), (F(59), 1010, "inout_cubic"), (F(62), 1034, "out_cubic"),
             (F(69), CX, "out_cubic"))
R_GR = Track((F(41), 0), (F(49), 100, "out_back"), (F(59), 265, "inout_cubic"))
SNAP_I = F(59)
_dive = Track((F(60), 1.0), (F(95), 4.5, "plongee"))


def dive(t):
    return _dive(t) + drift(t, F(60), 0.9)


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    g = g_i(t)
    # -- logo : la fermeture éclair (le cache suit les points à 41 px, l'écart du logo)
    if t < F(18):
        dl, dr = D_G(t), D_D(t)
        rp = R_PAIR(t)
        xa = CX - dl + rp + GAP * g
        xb = CX + dr - rp - GAP * g
        L += word_cut(xa, xb, s=g)
        L.append({"k": "group", "s": g, "layers": arabic(arab_i(t))})
        L += endorse(endo_i(t))
    if t < F(22):
        dl, dr = D_G(t), D_D(t)
        rp = R_PAIR(t)
        if t < T_HIT:
            bl, br = breathe(t, 0.18, 1.1), breathe(t, 0.18, 1.1, 0.25)
            sl = min(1 + speed(D_G, t) / 2200, 1.35)
            sr = min(1 + speed(D_D, t) / 2200, 1.35)
            d = dot(CX - dl, rp * bl, sl) + " " + dot(CX + dr, rp * br, sr)
        else:
            c1, c2 = (CX - dl, AXIS, rp), (CX + dr, AXIS, rp)
            d = stretch(link(c1, c2, contact_h(c1, c2)), squash(t, T_HIT, F(9), 0.3))
        L.append({"k": "fill", "id": "points", "fill": WHITE, "d": d, "pts": [(CX - dl, AXIS), (CX + dr, AXIS)]})
        return L

    # -- point unique : pop blanc -> orange, inspiration, gonflement avec étirement horizontal
    col = mix_hex(WHITE, ORANGE, prog(t, F(22), F(25)))
    if t < F(41):
        r = R_ONE_T(t)
        v = (R_ONE_T(t + 0.02) - R_ONE_T(t - 0.02)) / 0.04            # vitesse de croissance (px/s)
        s = 1 + max(-0.12, min(0.3, v / 4000))                          # rebond élastique : s'étire puis se resserre
        s *= squash(t, T_HIT, F(9), 0.3)
        L.append({"k": "fill", "id": "bulle", "fill": col, "d": stretch(cw_circle(CX, AXIS, r), s), "pts": []})
        return L

    # -- la fenêtre naît de la bulle, échange de tailles, rupture, plongée
    k = dive(t)
    xo, ro = X_OR(t), R_OR(t) if t > F(43) else R_ONE_T(t)
    xg, rg = X_GR(t), R_GR(t)
    ro *= breathe(t, 0.03, 0.7)
    sp = min(1 + 0.035 * max((dive(t + 0.01) - dive(t - 0.01)) / 0.02, 0), 1.28)
    co, cg = (xo, AXIS, ro), (xg, AXIS, rg)
    if t < SNAP_I:
        thin = 1 - 0.75 * prog(t, SNAP_I - F(4), SNAP_I, "in_cubic")
        h = neck(co, cg) * thin if abs(xg - xo) > abs(ro - rg) + 1 else "auto"
        d = link(co, cg, h)
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": d, "pts": [(xo, AXIS)]})
    else:
        xo_k = CX + (xo - CX) * k
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": stretch(cw_circle(xo_k, AXIS, ro * k), sp, cx=xo_k),
                  "pts": [(xo_k, AXIS)], "ghost": ro * k < 600})
    if rg > 0.5:
        xg_k = CX + (xg - CX) * k
        rk = (rg + 1.5) * k
        z = 0.7 * k ** 0.55 * (1 + 0.3 * max(0.0, t - F(78)))
        L.append(video(z, stretch(cw_circle(xg_k, AXIS, rk), sp, cx=xg_k), ghost=rk < 900))
    return L


def a_zip(t):
    return arrow(560, 330, 760, 330) + arrow(W - 560, 330, W - 760, 330)


def a_pop(t):
    return "".join(arrow(CX + dx * 90, AXIS + dy * 80, CX + dx * 230, AXIS + dy * 190)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_grow(t):
    return arrow(CX - 300, AXIS, CX - 470, AXIS) + arrow(CX + 300, AXIS, CX + 470, AXIS)


def a_bud(t):
    return arrow(1330, 320, 1530, 320) + arrow(760, 220, 600, 220)


def a_swap(t):
    return (arrow(420, AXIS, 520, AXIS) + arrow(780, AXIS, 680, AXIS)            # l'orange rétrécit
            + arrow(1110, 210, 1260, 160) + arrow(1110, 870, 1260, 920))          # la fenêtre grandit


def a_dive(t):
    return "".join(arrow(CX + dx * 560, AXIS + dy * 300, CX + dx * 900, AXIS + dy * 490)
                   for dx in (-1, 1) for dy in (-1, 1)) + arrow(420, AXIS, 120, AXIS)


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(5), "Anticipation : le mot s'élargit de 4 % ; les points reculent de 27 px ; l'arabe et l'endossement se referment.", "out_cubic", onion=2),
    Beat(F(15), "Fermeture éclair : les points foncent l'un vers l'autre (11 images, la droite part 2 images après) et le mot se ferme derrière eux.", "anticipe", ann=a_zip),
    Beat(F(19), "Contact : les points ont doublé de taille en fonçant. Haltère horizontale, le col s'épaissit, fusion en 5 images, écrasement à 130 %.", "out_cubic", onion=2, onion_dt=F(1)),
    Beat(F(25), "Pop : le point vire du blanc à l'orange et gonfle de 80 % en 3 images, puis inspire (-30 %) avant de grandir.", "out_back", ann=a_pop, onion=2, onion_dt=F(2)),
    Beat(F(32), "La bulle gonfle de 44 à 235 px sur un ressort (dépassement 12 %) en s'étirant de 30 % à l'horizontale.", "ressort_doux", ann=a_grow, onion=2),
    Beat(F(47), "Une bulle-fenêtre naît de son flanc droit (dépassement 10 %) ; la bulle orange glisse à gauche pour lui faire place.", "out_back", ann=a_bud),
    Beat(F(55), "Échange de tailles (3.3-02) : la fenêtre passe de 100 à 265 px, l'orange de 226 à 92 px. Le col s'affine.", "inout_cubic", ann=a_swap, onion=2),
    Beat(F(70), "Le col casse, la fenêtre se recentre et la caméra plonge (zoom x4,5) ; le point orange file hors champ à gauche.", "plongee", ann=a_dive, onion=2),
])


# =================================================================== OUTRO (4,0 s)
o_zoom = Track((0, 1.3), (F(14), 1.0, "out_cubic"))
R_W = Track((0, 1180), (F(11), 250, "in_cubic"), (F(16), 265, "out_back"), (F(21), 265),
            (F(34), 95, "inout_cubic"), (F(40), 0, "in_cubic"))
X_W = Track((0, CX), (F(5), CX), (F(18), 1010, "out_cubic"), (F(21), 1010), (F(34), 1204, "inout_cubic"),
            (F(40), 935, "in_cubic"))
X_O = Track((F(12), 770), (F(20), 600, "out_back"), (F(22), 600), (F(34), 830, "inout_cubic"), (F(42), CX, "out_cubic"))
R_O = Track((F(12), 0), (F(20), 92, "out_back"), (F(22), 92), (F(34), 230, "inout_cubic"),
            (F(48), R_ONE, "anticipe"))                  # prend son élan (+8 %) puis s'effondre en point
HIT_O = F(48)
D_SPLIT = Track((F(51), 0), (F(55), 34, "out_cubic"), (F(59), D_CLOSED, "out_back"))   # col, rupture, recul
R_SPLIT = Track((F(51), R_ONE), (F(54), R_RUN, "out_cubic"), (F(59), DR, "inout_cubic"))
T0_LOGO = F(59)
REV = Track((T0_LOGO, 0), (T0_LOGO + F(14), 1, "emphase"))   # même piste que le mot de blocks.endcard


def outro(t):
    L = []
    z = o_zoom(t) - 0.3 * max(0.0, t - F(14))
    if R_W(t) > 1150:
        L.append(video(z, ghost=False))
        return L
    L.append({"k": "bg", "v": "gradient"})
    if t < HIT_O:
        xw, rw = X_W(t), R_W(t) * (breathe(t, 0.02, 0.8) if F(16) < t < F(34) else 1)
        xo, ro = X_O(t), R_O(t)
        sx = squash(t, F(11), F(8), 0.15)
        if ro > 0.5:
            ro_b = ro * (breathe(t, 0.03, 0.7, 0.3) if t < F(34) else 1)
            co, cw = (xo, AXIS, ro_b), (xw, AXIS, max(rw, 0.6))
            d = link(co, cw)
            if t > F(40):
                # aspiration : la bulle se contracte en point, étirée en hauteur par la vitesse
                v = speed(R_O, t)
                d = stretch(cw_circle(xo, AXIS, ro), 1 / min(1 + v / 9000, 1.3), cx=xo)
            L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": stretch(d, sx, cx=xw) if t < F(20) else d,
                      "pts": [(xo, AXIS)]})
        if rw > 0.5:
            L.append(video(z, stretch(cw_circle(xw, AXIS, rw + 1.5), sx, cx=xw), ghost=rw < 1100))
        return L

    # impact du point, blanc ; division 3.4-01 ; le mot s'ouvre entre les points (curseurs de la fermeture)
    col = mix_hex(ORANGE, WHITE, prog(t, F(47), F(52)))
    if t < F(51):
        r = R_ONE * (1 + 0.12 * math.sin(math.pi * prog(t, HIT_O, F(51))))   # rebond du point à l'impact
        d = stretch(cw_circle(CX, AXIS, r), squash(t, HIT_O, F(8), 0.3))
        L.append({"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": []})
        return L
    ds, rs = D_SPLIT(t), R_SPLIT(t)
    if t >= T0_LOGO:
        ds = D_CLOSED + (DG - D_CLOSED) * REV(t)
    w = prog(t, T0_LOGO, T0_LOGO + F(12))                     # la respiration s'installe en douceur
    bl, br = 1 + (breathe(t, 0.2, 1.1) - 1) * w, 1 + (breathe(t, 0.2, 1.1, 0.25) - 1) * w
    c1, c2 = (CX - ds, AXIS, rs * bl), (CX + ds, AXIS, rs * br)
    h = split_h(c1, c2) if ds > 0.5 else "auto"
    d = link(c1, c2, h) if h is not None else cw_circle(*c1) + " " + cw_circle(*c2)
    L.append({"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": [(CX - ds, AXIS), (CX + ds, AXIS)]})
    return L


def outro_full(t):
    """Outro + carton logo : les points amenés par l'animation suivent la poussée du carton."""
    L = outro(t)
    dots = [x for x in L if x.get("id") == "points-logo"]
    rest = [x for x in L if x.get("id") != "points-logo"]
    return rest + endcard(t, T0_LOGO, dots=False, extra=dots)


def a_aspire(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 500, CX + dx * 520, AXIS + dy * 290)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_bud_o(t):
    return arrow(720, 230, 520, 230) + arrow(1150, 230, 1300, 230)


def a_swap_o(t):
    return arrow(560, 250, 680, 330) + arrow(1360, 330, 1300, 380)


def a_swallow(t):
    return arrow(1260, 300, 1060, 300)


def a_contract(t):
    return "".join(arrow(CX + dx * 360, AXIS + dy * 330, CX + dx * 180, AXIS + dy * 170)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_split(t):
    return arrow(CX - 60, 440, CX - 200, 440) + arrow(CX + 60, 440, CX + 200, 440)


def a_unzip(t):
    return arrow(CX - 120, 380, CX - 330, 380) + arrow(CX + 120, 380, CX + 330, 380)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(7), "La caméra recule (130 % -> 100 %) et la vidéo est aspirée en bulle de 265 px, qui glisse à droite ; le dégradé entre par les coins.", "in_cubic", ann=a_aspire, onion=2),
    Beat(F(17), "Une bulle orange naît du flanc gauche de la fenêtre (dépassement 10 %) : c'est la paire de la charte 3.3-02.", "out_back", ann=a_bud_o),
    Beat(F(28), "Échange de tailles : l'orange passe de 92 à 230 px, la fenêtre de 265 à 95 px. Le col reste tendu entre elles.", "inout_cubic", ann=a_swap_o),
    Beat(F(37), "La fenêtre est avalée par la bulle orange (6 images) ; la bulle se recentre et gonfle encore de 8 % : elle prend son élan.", "anticipe", ann=a_swallow, onion=2),
    Beat(F(46), "Aspiration : la bulle s'effondre en point de 248 à 34 px en accélérant (8 images), étirée en hauteur par la vitesse.", "anticipe", ann=a_contract, onion=2),
    Beat(F(54), "Impact : le point blanchit, s'écrase à 130 % puis se divise (3.4-01) : col qui s'affine, rupture, recul de 10 %.", "out_back", ann=a_split, onion=2, onion_dt=F(2)),
    Beat(F(63), "Les points sont les curseurs : ils s'écartent et « sfeer » s'ouvre entre eux depuis le centre (14 images).", "emphase", ann=a_unzip, onion=2, onion_dt=F(2)),
    Beat(F(94), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; arabe révélé de droite à gauche, endossement en bas.", "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "C'est l'animation du logo de la charte (3.4) jouée à rebours : le logo se range dans un point, et ce point ouvre le film.",
        "Les points du logo sont les curseurs d'une fermeture éclair : le mot se ferme et se rouvre derrière eux, sans être déformé.",
        "L'outro rejoue le même geste à l'endroit : intro et outro se répondent et se bouclent.",
    ]),
    ("Charte et corrections", [
        "Ton croquis dessine l'haltère en diagonale : elle est corrigée à l'horizontale, centres sur y = 540.",
        "Tes flèches qui tournent autour du mot deviennent une fermeture horizontale : pas de rotation ni de mouvement vertical (règle de l'axe).",
        "Échange de tailles 3.3-02 en rapport 2,9 : 1 maximum (92 / 265 px). Le passage blanc -> orange du point est un écart à valider.",
    ]),
    ("Mouvement", [
        "Rampes franches : recul puis accélération pour la fermeture et l'aspiration, ressort doux (+12 %) pour le gonflement.",
        "Étirement dans le sens de la vitesse, volume conservé : points jusqu'à 135 % en course, bulle 130 % en croissance.",
        "Points décalés de 2 images au départ. AE : un calque de forme par bulle, cache alpha pour la fenêtre, zoom via un nul parent.",
    ]),
]
