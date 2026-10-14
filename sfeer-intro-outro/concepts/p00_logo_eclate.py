"""Piste Ø (croquis de la DA) : « le logo éclaté ».

Le croquis : ·sfeer· pris dans une bulle à deux lobes ; les deux bulles s'écartent et révèlent le mot,
se multiplient en chaîne de 4 (deux extérieures + une paire chevauchante, cascade 3.5-02), puis tout
converge d'un coup en UNE bulle, qui devient la fenêtre où l'on entre.

INTRO : les points du logo gonflent en bulles orange qui mangent le mot, se percutent, rebondissent
en chaîne de 4, puis tout claque au centre : la bulle unique éclot en vidéo verte et la caméra plonge.
OUTRO : l'inverse. La vidéo est aspirée en bulle, la bulle éclate en chaîne de 4, les cols cassent et
les deux bulles extérieures rapetissent jusqu'aux points du logo pendant que le mot éclot au centre.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, prog  # noqa: E402
from blocks import LG, arabic, drift, endcard, endorse, squash, video  # noqa: E402
from sfeer_svg import (AXIS, FONT, ORANGE, WHITE, W, arrow, bridge_d, f, mix_hex,  # noqa: E402
                       waist_h)

CX = W / 2
DG = CX - LG["dot_g"][0]      # 279 px : demi-écart des points du logo
DR = LG["dot_r"]              # 10,9 px : rayon des points du logo
FS, WX, WW = LG["fs"], LG["word_x"], LG["word_w"]

META = {
    "id": "p00_logo_eclate",
    "num": "PØ",
    "title": "Le logo éclaté",
    "principe": "Les points du logo gonflent en bulles, se percutent et se rassemblent en une bulle qui ouvre la fenêtre.",
    "logline": "Piste Ø de la DA. Les points du logo gonflent en bulles qui mangent le mot, se percutent, rebondissent "
               "en chaîne de 4, puis tout claque au centre : la bulle unique éclot en vidéo et la caméra plonge.",
}


# ------------------------------------------------------------------ outils de forme
def cw_circle(cx, cy, r):
    """Cercle tracé dans le sens horaire, comme les ponts de bridge_d : l'union reste pleine (nonzero)."""
    return (f"M{f(cx - r)} {f(cy)}a{f(r)} {f(r)} 0 1 1 {f(2 * r)} 0"
            f"a{f(r)} {f(r)} 0 1 1 {f(-2 * r)} 0Z")


def neck(c1, c2, t=0.35):
    """Demi-épaisseur du col : taille de cacahuète au contact, puis col fin (0,07 r) à l'écart maximal
    mesuré sur la charte (3.3-01 : écart 1,3 r -> col 0,14 r)."""
    rmin = min(c1[2], c2[2])
    gap = abs(c2[0] - c1[0]) - c1[2] - c2[2]
    if gap <= 0:
        return waist_h(c1, c2, t)
    return rmin * (0.07 + 0.27 * math.exp(-2.2 * gap / rmin))


def contact_h(c1, c2):
    """Col qui naît au contact : rien tant que l'écart dépasse 0,3 r, puis un fil qui s'épaissit
    jusqu'à la taille de cacahuète (continu avec waist_h au contact)."""
    rmin = min(c1[2], c2[2])
    gap = abs(c2[0] - c1[0]) - c1[2] - c2[2]
    if gap <= 0:
        return waist_h(c1, c2, 0.35)
    if gap > 0.3 * rmin:
        return None
    return rmin * (0.02 + 0.32 * (1 - gap / (0.3 * rmin)) ** 1.5)


def link(c1, c2, h="auto"):
    """Deux bulles reliées par le col de la charte (h=None : séparées)."""
    (x1, _, r1), (x2, _, r2) = c1, c2
    if r1 < 0.5 and r2 < 0.5:
        return ""
    if r1 < 0.5 or r2 < 0.5:
        return cw_circle(*(c1 if r1 >= r2 else c2))
    if abs(x2 - x1) <= abs(r1 - r2) + 0.01:
        return cw_circle(*(c1 if r1 >= r2 else c2))
    if h is None:
        return cw_circle(*c1) + cw_circle(*c2)
    if h == "auto":
        h = neck(c1, c2)
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
    """Étirement / écrasement d'un tracé autour de (cx, cy), volume conservé (sy = 1/sx).
    Les arcs de cercle deviennent des arcs d'ellipse : exact pour une échelle alignée sur les axes."""
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
    """Mot « sfeer » (mêmes position et typo que blocks.word) caché hors de [xa, xb] :
    les bulles le mangent, il n'est jamais posé sur une forme."""
    if xb - xa < 2:
        return []
    tr = f"translate({f(CX)} {AXIS}) scale({f(s)}) translate({f(-CX)} {-AXIS})"
    return [{"k": "raw", "svg":
             f'<clipPath id="{uid}"><rect x="{f(xa)}" y="{f(AXIS - FS * 1.2)}" width="{f(xb - xa)}" height="{f(FS * 1.8)}"/></clipPath>'
             f'<g clip-path="url(#{uid})"><text transform="{tr}" x="{f(WX)}" y="{f(AXIS + FS * 0.26)}" '
             f'font-family="{FONT}" font-size="{f(FS)}" letter-spacing="{f(FS * 0.16)}" fill="{WHITE}" '
             f'textLength="{f(WW)}" lengthAdjust="spacingAndGlyphs">sfeer</text></g>'}]


def chain4(dol, dor, rol, ror, dil, dir_, ril, rir):
    """Chaîne de 4 sur l'axe : extérieure G, paire centrale G/D, extérieure D (demi-écarts depuis le centre).
    La paire centrale ne se relie qu'au contact (col qui naît), les extérieures par le col de la charte."""
    og, ig = (CX - dol, AXIS, rol), (CX - dil, AXIS, ril)
    id_, od = (CX + dir_, AXIS, rir), (CX + dor, AXIS, ror)
    hc = contact_h(ig, id_) if abs(id_[0] - ig[0]) > abs(ril - rir) + 0.01 else "auto"
    return " ".join(p for p in (link(og, ig), link(ig, id_, hc), link(id_, od)) if p)


# =================================================================== INTRO (4,0 s)
push_logo = Track((0, 1.0), (F(24), 1.035, "out_cubic"))            # poussée lente sur le logo
endo_i = Track((0, 1), (F(9), 0, "in_cubic"))
arab_i = Track((F(1), 1), (F(11), 0, "in_cubic"))

# Bulles extérieures (= points du logo qui gonflent). Demi-écart D depuis le centre, rayon r.
DO_I = Track((0, DG), (F(4), DG), (F(10), DG + 12, "out_cubic"),      # anticipation : recul de 12 px
             (F(18), 245, "out_cubic"), (F(23), 200, "linear"),        # poussée continue sur le mot
             (F(28), 95, "in_cubic"),                                   # charge l'une vers l'autre
             (F(42), 560, "out_back"),                                  # rebond : éjection (cascade 3.5-02)
             (F(47), 600, "in_cubic"),                                  # tension : les cols s'affinent
             (F(57), 0, "anticipe"))                                    # convergence violente
RO_I = Track((0, DR), (F(4), DR * 1.1, "out_cubic"), (F(10), DR * 0.6, "in_cubic"),
             (F(22), 175, "out_back"), (F(28), 168),
             (F(42), 150, "out_cubic"), (F(47), 146), (F(57), 270, "in_cubic"))
# Paire centrale : née des deux lobes de la cacahuète après le choc.
DI_I = Track((F(28), 95), (F(36), 110, "out_cubic"), (F(47), 112), (F(57), 0, "in_cubic"))
RI_I = Track((F(28), 168), (F(36), 135, "out_cubic"), (F(47), 132), (F(57), 270, "in_cubic"))

GREEN_I = Track((F(58), 0.0), (F(65), 1.0, "out_expo"))               # éclosion de la vidéo
_dive = Track((F(59), 1.0), (F(95), 4.6, "plongee"))
R_WIN = 270
DELAY = F(2)                                                            # la droite suit avec 2 images


def dive(t):
    return _dive(t) + drift(t, F(59), 0.9)           # la poussée ne s'arrête jamais


def dive_speed(t):
    return (dive(t + 0.01) - dive(t - 0.01)) / 0.02


def intro_shapes(t):
    """État des bulles : demi-écarts et rayons (gauche, droite décalée de 2 images)."""
    tl, tr = t, t - DELAY
    g = push_logo(t)
    st = {}
    for side, tt in (("g", tl), ("d", tr)):
        do, ro = DO_I(tt), RO_I(tt)
        if tt < F(28):
            do *= 1 + (g - 1) * (1 - prog(tt, F(10), F(20)))     # les points suivent la poussée du logo
            di, ri = do, ro
        else:
            di, ri = DI_I(tt), RI_I(tt)
            # tenue : la paire centrale échange ses tailles (3.3-02), comme le motif 3.6
            sw = math.sin(math.pi * prog(tt, F(34), F(52), "inout_cubic"))
            ri *= 1 + (0.16 if side == "g" else -0.16) * sw
        st[side] = (do, ro, di, ri)
    return st


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    g = push_logo(t)
    st = intro_shapes(t)
    (dol, rol, dil, ril), (dor, ror, dir_, rir) = st["g"], st["d"]

    # -- logo : le mot est mangé par les bords intérieurs des bulles, l'arabe et l'endossement se referment
    if t < F(32):
        xa, xb = CX - dol + rol + 2, CX + dor - ror - 2
        L += word_cut(xa, xb, s=g)
        L.append({"k": "group", "s": g, "layers": arabic(arab_i(t))})
        L += endorse(endo_i(t))

    if t < F(57):
        if rol < 40 and ror < 40:
            # les deux points, blancs puis orange : pop de couleur au début du gonflement
            col = mix_hex(WHITE, ORANGE, prog(t, F(9), F(13)))
            d = cw_circle(CX - dol, AXIS, rol * breathe(t, 0.15, 1.1)) + cw_circle(CX + dor, AXIS, ror * breathe(t, 0.15, 1.1, 0.25))
            L.append({"k": "fill", "id": "points", "fill": col, "d": d,
                      "pts": [(CX - dol, AXIS), (CX + dor, AXIS)]})
        else:
            col = mix_hex(WHITE, ORANGE, prog(t, F(9), F(13)))
            d = chain4(dol, dor, rol, ror, dil, dir_, ril, rir)
            sx = 1 / squash(t, F(29), F(9), 0.2)                     # choc de la cacahuète : écrasement
            d = stretch(d, sx)
            pts = [(CX - dol, AXIS), (CX + dor, AXIS)]
            if t > F(28):
                pts += [(CX - dil, AXIS), (CX + dir_, AXIS)]
            L.append({"k": "fill", "id": "chaine", "fill": col, "d": d, "pts": pts})
        return L

    # -- une seule bulle : impact (130 % x 77 %) puis ressort, la vidéo éclot dedans, la caméra plonge
    k = dive(t)
    sq = squash(t, F(57), F(10), 0.3)
    sp = min(1 + 0.035 * max(dive_speed(t), 0), 1.28)            # étirement horizontal avec la vitesse
    sx = sq * sp
    R = R_WIN * breathe(t, 0.025, 0.7) * k
    gu = GREEN_I(t)
    if gu < 1:
        L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": stretch(cw_circle(CX, AXIS, R), sx)})
    if gu > 0.01:
        rg = R * gu
        z = 0.72 * k ** 0.55 * (1 + 0.3 * max(0.0, t - F(76)))      # contre-zoom plus lent, qui ne s'arrête pas
        L.append(video(z, stretch(cw_circle(CX, AXIS, rg), sx), ghost=rg < 900))
    return L


def a_pop(t):
    return arrow(470, 300, 700, 300) + arrow(W - 470, 300, W - 700, 300)


def a_charge(t):
    return arrow(330, AXIS, 600, AXIS) + arrow(W - 330, AXIS, W - 600, AXIS)


def a_cascade(t):
    return arrow(820, 300, 520, 300) + arrow(1100, 300, 1400, 300)


def a_converge(t):
    return (arrow(140, 300, 560, 400) + arrow(W - 140, 300, W - 560, 400)
            + arrow(140, 780, 560, 680) + arrow(W - 140, 780, W - 560, 680))


def a_dive(t):
    return "".join(arrow(CX + dx * 560, AXIS + dy * 300, CX + dx * 900, AXIS + dy * 490)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(6), "Logo vivant : l'endossement et l'arabe se referment en 10 images ; les points inspirent (-40 %) et reculent de 12 px.", "in_cubic", onion=2),
    Beat(F(17), "Pop : les points virent à l'orange et gonflent x16 en 12 images (dépassement +10 %). Ils mangent le mot par les bords.", "out_back", ann=a_pop),
    Beat(F(26), "Charge : après une poussée continue (9 px/image), les bulles foncent l'une vers l'autre en 5 images (in_cubic). La droite a 2 images de retard.", "in_cubic", ann=a_charge),
    Beat(F(31), "Choc : la cacahuète s'écrase à 82 % de largeur, le mot a disparu. Le rebond va renvoyer les bulles vers les bords.", "ressort_vif", onion=2),
    Beat(F(39), "Cascade 3.5-02 : chaque lobe éjecte une bulle vers l'extérieur (dépassement 10 %). Chaîne de 4, paire chevauchante au centre.", "out_back", ann=a_cascade),
    Beat(F(53), "Tension puis convergence : les cols s'affinent, les bulles reculent de 40 px puis foncent toutes au centre en 10 images.", "anticipe", ann=a_converge),
    Beat(F(61), "Impact : une seule bulle, écrasée à 130 % x 77 %, revient au rond sur ressort. La vidéo verte éclot en son centre (7 images).", "ressort_vif", onion=2),
    Beat(F(71), "Plongée : zoom x4,6 depuis le centre, la bulle s'étire jusqu'à 28 % avec la vitesse ; la plaque verte zoome 2 fois moins vite.", "plongee", ann=a_dive, onion=2),
])


# =================================================================== OUTRO (4,0 s)
o_zoom = Track((0, 1.3), (F(14), 1.0, "out_cubic"))
o_win = Track((0, 1180), (F(13), 232, "in_cubic"), (F(19), 270, "out_back"))   # aspiration en bulle
o_iris = Track((F(17), 1.0), (F(25), 0.0, "in_cubic"))                          # la vidéo se referme
SNAP_O = F(52)
DO_O = Track((F(31), 0), (F(43), 560, "out_back"), (SNAP_O, 600, "in_cubic"),
             (SNAP_O + F(3), 632, "out_cubic"),                                  # recul après rupture (D_BACK)
             (F(67), DG, "emphase"))                                             # vers les points du logo
RO_O = Track((F(25), 270), (F(31), 230, "inout_cubic"), (F(43), 150, "out_cubic"), (SNAP_O, 142),
             (SNAP_O + F(3), 140))
D_BACK = 632                                                                     # demi-écart au recul


def ro_outro(t, tt):
    """Après le recul, le rayon suit le trajet : la bulle rapetisse à mesure qu'elle approche du point
    du logo (son bord intérieur reste toujours hors du mot qui éclot)."""
    if tt < SNAP_O + F(3):
        return RO_O(tt)
    u = max(0.0, (DO_O(tt) - DG) / (D_BACK - DG))
    return DR + (140 - DR) * u ** 1.15
DI_O = Track((F(31), 0), (F(43), 110, "out_back"), (SNAP_O, 114), (SNAP_O + F(3), 78, "out_cubic"),
             (F(56), 30, "in_cubic"))
RI_O = Track((F(25), 270), (F(31), 230, "inout_cubic"), (F(43), 135, "out_cubic"), (SNAP_O, 132),
             (F(56), 0, "in_back"))
T0_LOGO = F(57)


def outro(t):
    L = []
    if t < F(25):
        # la vidéo plein cadre recule puis est aspirée dans une bulle (le dégradé apparaît par les coins)
        L.append({"k": "bg", "v": "gradient"})
        z = o_zoom(t) - 0.3 * max(0.0, t - F(14))
        sx = squash(t, F(13), F(8), 0.18)
        r = o_win(t) * (breathe(t, 0.02, 0.8) if t > F(19) else 1)
        if t > F(15):
            L.append({"k": "fill", "id": "bulle", "fill": ORANGE, "d": stretch(cw_circle(CX, AXIS, r), sx)})
        rg = r * o_iris(t)
        if rg > 1:
            L.append(video(z, stretch(cw_circle(CX, AXIS, rg), sx), ghost=rg < 1100))
        return L

    L.append({"k": "bg", "v": "gradient"})
    tl, tr = t, t - DELAY
    sides = {}
    for side, tt in (("g", tl), ("d", tr)):
        if tt < F(31):
            r = RO_O(max(tt, F(25)))
            sides[side] = (0.0, r, 0.0, r)
        else:
            ti = t if t >= SNAP_O else tt          # après la rupture, la paire centrale se replie d'un bloc
            ri = RI_O(ti)
            if ti < SNAP_O:                        # tenue : la paire échange ses tailles (3.3-02)
                ri *= 1 + (0.15 if side == "g" else -0.15) * math.sin(math.pi * prog(t, F(41), SNAP_O, "inout_cubic"))
            sides[side] = (DO_O(tt), ro_outro(t, tt), DI_O(ti), ri)
    (dol, rol, dil, ril), (dor, ror, dir_, rir) = sides["g"], sides["d"]

    snapped = t >= SNAP_O
    if not snapped:
        # cols qui s'affinent jusqu'à la rupture
        thin = 1 - 0.75 * prog(t, SNAP_O - F(5), SNAP_O, "in_cubic")
        og, ig = (CX - dol, AXIS, rol), (CX - dil, AXIS, ril)
        id_, od = (CX + dir_, AXIS, rir), (CX + dor, AXIS, ror)
        hl = neck(og, ig) * thin if dol > dil + 1 else "auto"
        hr = neck(id_, od) * thin if dor > dir_ + 1 else "auto"
        hc = waist_h(ig, id_, 0.35) if dil + dir_ > 0.5 else "auto"
        d = " ".join(p for p in (link(og, ig, hl), link(ig, id_, hc), link(id_, od, hr)) if p)
        sx = squash(t, F(25), F(8), 0.12) * (1 / (1 + 0.08 * math.sin(math.pi * prog(t, F(25), F(31)))))
        L.append({"k": "fill", "id": "chaine", "fill": ORANGE, "d": stretch(d, sx),
                  "pts": [(CX - dol, AXIS), (CX + dor, AXIS)] if t > F(31) else []})
        return L

    # rupture : la paire centrale se replie au centre et disparaît ; les extérieures filent vers les points du logo
    if ril > 0.5 or rir > 0.5:
        ig, id_ = (CX - dil, AXIS, max(ril, 0.6)), (CX + dir_, AXIS, max(rir, 0.6))
        d = link(ig, id_, waist_h(ig, id_, 0.5) if dil + dir_ > abs(ril - rir) + 0.01 else "auto")
        L.append({"k": "fill", "id": "paire", "fill": ORANGE, "d": d})
    col = mix_hex(ORANGE, WHITE, prog(t, F(57), F(66)))
    bl = breathe(t, 0.2, 1.1) if t > F(67) else 1
    br = breathe(t, 0.2, 1.1, 0.25) if t > F(67) else 1
    # étirement horizontal des points pendant le trajet (vitesse)
    v = abs(DO_O(t + 0.02) - DO_O(t - 0.02)) / 0.04
    s = min(1 + v / 2500, 1.3)
    dots = f"{stretch(cw_circle(CX - dol, AXIS, rol * bl), s, cx=CX - dol)} {stretch(cw_circle(CX + dor, AXIS, ror * br), s, cx=CX + dor)}"
    L.append({"k": "fill", "id": "points-logo", "fill": col, "d": dots,
              "pts": [(CX - dol, AXIS), (CX + dor, AXIS)]})
    return L


def outro_full(t):
    """Outro + carton logo : les points amenés par l'animation suivent la poussée du carton."""
    L = outro(t)
    dots = [x for x in L if x.get("id") == "points-logo"]
    rest = [x for x in L if x.get("id") != "points-logo"]
    return rest + endcard(t, T0_LOGO, dots=False, extra=dots)


def a_aspire(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 500, CX + dx * 480, AXIS + dy * 270)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_eclate(t):
    return arrow(760, 260, 360, 260) + arrow(1160, 260, 1560, 260)


def a_rupture(t):
    return arrow(380, 300, 220, 300) + arrow(W - 380, 300, W - 220, 300) + arrow(830, 780, 920, 780) + arrow(1090, 780, 1000, 780)


def a_retour(t):
    return arrow(330, 300, 600, 300) + arrow(W - 330, 300, W - 600, 300)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(8), "Fin du plan : la caméra recule (130 % -> 100 %) et la vidéo est aspirée dans une bulle ; le dégradé entre par les 4 coins.", "in_cubic", ann=a_aspire),
    Beat(F(21), "La bulle arrive écrasée (118 %) et rebondit ; la vidéo se referme en iris vers le centre en 8 images : il reste une bulle orange.", "in_cubic", onion=2),
    Beat(F(29), "Anticipation : la bulle inspire, -15 % de rayon en 6 images, comprimée en largeur. Elle charge avant d'éclater.", "inout_cubic", onion=2),
    Beat(F(37), "Éclatement en chaîne de 4 : les bulles extérieures jaillissent vers les bords (dépassement 10 %), la droite 2 images après.", "out_back", ann=a_eclate),
    Beat(F(51), "Tension : les cols s'étirent et s'affinent jusqu'à 3 px, les bulles tirent encore de 40 px vers l'extérieur.", "in_cubic"),
    Beat(F(55), "Rupture nette : les cols cassent, les bulles extérieures reculent de 30 px, la paire centrale se replie au centre.", "out_cubic", ann=a_rupture),
    Beat(F(62), "Les bulles extérieures rapetissent jusqu'aux points du logo en virant au blanc ; « sfeer » éclot au centre, là où la paire a disparu.", "emphase", ann=a_retour, onion=2, onion_dt=F(2)),
    Beat(F(94), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; arabe révélé de droite à gauche, endossement en bas.", "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Le logo est la bulle : ses deux points deviennent les bulles de la charte, puis redeviennent le logo à la sortie.",
        "Le mot n'est jamais déformé : il est mangé par les bulles, puis éclot au centre, comme sur la charte 3.4-02.",
        "Fonctionne avec n'importe quelle vidéo : la bulle finale est un simple cache rond qui grandit.",
    ]),
    ("Charte et corrections", [
        "Ton croquis montre le logo dans une bulle à deux lobes : ici le mot n'est jamais posé sur une forme. Il est caché pile au bord des bulles (règle logo).",
        "Convergence : tes flèches courbes passent par le haut. Ici tout converge le long de l'axe, puis la plongée se fait en zoom depuis le centre.",
        "Chaîne de 4 de la cascade 3.5-02 : tous les centres sur y = 540, cols mesurés sur la charte (0,14 r à l'écart maximal), rayons ≥ 130 px.",
    ]),
    ("Mouvement", [
        "Chaque geste a son contre-mouvement : les points reculent avant de gonfler, la bulle inspire avant d'éclater.",
        "Deux claquements : le choc de la cacahuète, puis la convergence ; écrasement 130 % x 77 % et ressort à chaque impact.",
        "Gauche et droite décalées de 2 images. AE : un calque de forme par état, chaîne pilotée par 4 nuls sur l'axe.",
    ]),
]
