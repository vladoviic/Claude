"""Piste 9 (croquis de la DA) : « la bobine ».

Les deux points du logo filent aux bords du cadre et deviennent deux bobines, coupées à leur
milieu vertical. La bobine droite déroule une pellicule de bulles qui défile à toute vitesse
le long de l'axe, puis freine comme un rouleau de machine à sous : une bulle s'arrête pile au
centre (cran), ses cous cassent, elle s'ouvre en fenêtre verte et l'on plonge.
OUTRO : la vidéo se rétracte en bulle, la pellicule repart à l'envers et dépose deux bulles
qui deviennent les points du logo.

Correction de la DA : sa colonne verticale de points devient une bande HORIZONTALE sur l'axe
(bulles alignées verticalement interdites par la charte).
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, prog  # noqa: E402
from blocks import LG, arabic, endcard, squash, video, word  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, arrow, bridge_d, ellipse_d, f,  # noqa: E402
                       label, mix_hex, waist_h)

CX = W / 2
DOT_R = LG["dot_r"]
DGX, DDX = LG["dot_g"][0], LG["dot_d"][0]

META = {
    "id": "p09_la_bobine",
    "num": "P9",
    "title": "La bobine",
    "logline": "Piste 9 de la DA. Les points du logo deviennent deux bobines aux bords du cadre ; une pellicule de bulles "
               "défile à toute vitesse, freine, une bulle s'arrête au centre comme un rouleau de machine à sous et s'ouvre sur le film.",
}


# ================================================================= OUTILS DE FORME
_TOK = re.compile(r"[MLAaZz]|-?\d*\.?\d+")


def stretch_d(d, sx, sy, cx=CX, cy=AXIS):
    """Étire un tracé (M, L, A, a, Z) autour de (cx, cy). Un arc de cercle devient un arc d'ellipse."""
    if abs(sx - 1) < 1e-4 and abs(sy - 1) < 1e-4:
        return d
    tok = _TOK.findall(d)
    out, i, cmd = [], 0, None
    while i < len(tok):
        t = tok[i]
        if t in "MLAaZz":
            cmd = t
            out.append(t)
            i += 1
            continue
        if cmd in ("M", "L"):
            x, y = float(tok[i]), float(tok[i + 1])
            out.append(f"{f(cx + (x - cx) * sx)} {f(cy + (y - cy) * sy)}")
            i += 2
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = tok[i:i + 7]
            out.append(f"{f(float(rx) * sx)} {f(float(ry) * sy)} {rot} {la} {sw} "
                       f"{f(cx + (float(x) - cx) * sx)} {f(cy + (float(y) - cy) * sy)}")
            i += 7
        elif cmd == "a":
            rx, ry, rot, la, sw, x, y = tok[i:i + 7]
            out.append(f"{f(float(rx) * sx)} {f(float(ry) * sy)} {rot} {la} {sw} "
                       f"{f(float(x) * sx)} {f(float(y) * sy)}")
            i += 7
        else:
            i += 1
    return " ".join(out)


def circ(cx, r, cy=AXIS):
    """Cercle tracé dans le sens horaire (même sens que bridge_d : les unions restent pleines)."""
    return (f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)}Z")


def strip_d(cs, hs):
    """Pellicule : bulles (x, r) triées par x ; hs[i] = demi-épaisseur du cou entre i et i+1 (None = séparées)."""
    parts, linked = [], set()
    for i in range(len(cs) - 1):
        h = hs[i]
        if h is None or h < 0.6:
            continue
        (x1, r1), (x2, r2) = cs[i], cs[i + 1]
        c1, c2 = (x1, AXIS, r1), (x2, AXIS, r2)
        if x2 - x1 < r1 + r2:
            h = max(h, waist_h(c1, c2, 0.15))
        parts.append(bridge_d(c1, c2, min(h, 0.92 * min(r1, r2))))
        linked |= {i, i + 1}
    for i, (x, r) in enumerate(cs):
        if i not in linked:
            parts.append(circ(x, r))
    return "".join(parts)


def strip_path(cs, hs, sx=1.0):
    """Pellicule étirée dans le sens de la vitesse (sx), volume conservé (sy = 1/sx), centres inchangés."""
    if abs(sx - 1) < 1e-3:
        return strip_d(cs, hs)
    pre = [(CX + (x - CX) / sx, r) for x, r in cs]
    return stretch_d(strip_d(pre, hs), sx, 1 / sx)


def vel(fn, t):
    """Vitesse en px par image."""
    return (fn(t + 0.02) - fn(t - 0.02)) / 0.04 / 25


def sx_speed(v, vmax=150):
    return 1 + 0.35 * min(1.0, abs(v) / vmax)


def visible(cs, hs, margin=140):
    """Ne garde que les bulles proches du cadre (et leurs cous)."""
    keep = [i for i, (x, r) in enumerate(cs) if -margin - r < x < W + margin + r]
    if not keep:
        return [], []
    a, b = keep[0], keep[-1]
    return cs[a:b + 1], hs[a:b]


def reel(x, r, sq=1.0, fill=ORANGE, rid="bobine", pts=True):
    return {"k": "fill", "id": rid, "fill": fill, "d": ellipse_d(x, AXIS, r * sq, r / sq),
            "pts": [(x, AXIS)] if pts else []}


R_REEL = 300          # rayon des bobines (coupées à leur milieu vertical)
RB, RS = 96, 64       # bulles de la pellicule : grande / petite (motif 3.6)
RWIN = 400            # rayon de la fenêtre au repos
LENS = 0.5            # loupe du centre : +50 % au passage (le « tic » du rouleau)


def r_of(j):
    """Motif de la pellicule : grande, petite, grande... (j = rang par rapport à la bulle gagnante)."""
    return RB if j % 2 == 0 else RS


def lens(x):
    """Une bulle grossit en passant au centre, comme la face avant d'un rouleau de machine à sous."""
    return 1 + LENS * math.exp(-((x - CX) / 240) ** 2)


def strip_layer(cs, hs, sx, lid, pts=None):
    cs = [(x, r * lens(x)) for x, r in cs]
    cs, hs = visible(cs, hs)
    if not cs:
        return []
    return [{"k": "fill", "id": lid, "fill": ORANGE, "d": strip_path(cs, hs, sx), "ghost": True, "pts": pts or []}]


# ================================================================= INTRO (4,0 s)
push_logo = Track((0, 1.0), (F(10), 1.05, "linear"))
ar_rev = Track((F(1), 1), (F(8), 0, "in_cubic"))
WORD_END = LG["word_x"] + LG["word_w"]

# point droit : contre-mouvement vers l'intérieur, tir vers le bord droit, il gonfle en arrivant (pop à l'impact)
dR_x = Track((F(2), DDX), (F(7), DDX - 18, "inout_cubic"), (F(14), W + 48, "inout_cubic"), (F(20), W, "out_back"))
dR_r = Track((F(2), DOT_R), (F(8), DOT_R * 0.7, "inout_cubic"), (F(16), R_REEL * 1.12, "inout_cubic"), (F(23), R_REEL, "ressort"))
# point gauche : il gonfle sur place et ENROULE le mot (bobine réceptrice), puis file au bord gauche
dL_x = Track((F(2), DGX), (F(7), DGX + 14, "inout_cubic"), (F(11), DGX - 50, "out_cubic"), (F(16), DGX - 50),
             (F(22), -48, "in_cubic"), (F(27), 0, "out_back"))
dL_r = Track((F(2), DOT_R), (F(7), DOT_R * 0.7, "inout_cubic"), (F(11), 118, "out_back"), (F(16), 150, "out_cubic"),
             (F(22), R_REEL * 1.12, "out_cubic"), (F(29), R_REEL, "ressort"))
# le mot glisse vers la gauche et disparaît dans le point gauche (coupé à son centre)
word_dx = Track((F(2), 0), (F(7), 18, "inout_cubic"), (F(9), 20, "linear"), (F(16), DGX - 50 - WORD_END - 20, "in_cubic"))


def wound_word(t):
    """Mot + arabe, poussés par la caméra, découpés à droite du centre du point gauche (le mot s'enroule)."""
    s, dx = push_logo(t), word_dx(t)
    cut = CX + (dL_x(t) - CX) * s
    inner = "".join(L["svg"] for L in word(1) + arabic(ar_rev(t)))
    return {"k": "raw", "svg":
            f'<clipPath id="enroule"><rect x="{f(cut)}" y="0" width="{W}" height="1080"/></clipPath>'
            f'<g clip-path="url(#enroule)"><g transform="translate({f(CX + dx)} {AXIS}) scale({f(s)}) '
            f'translate({f(-CX)} {-AXIS})">{inner}</g></g>'}


# pellicule : la gagnante (rang 0) part loin à droite, accélère, file à 150 px/image, freine, dépasse, cran
JX0 = 3505
xJ = Track((F(17), JX0), (F(24), JX0 - 350, "in_cubic"), (F(34), JX0 - 1850, "linear"),
           (F(49), CX - 55, "out_cubic"), (F(56), CX, "ressort"))
spacing = Track((F(17), 260), (F(32), 292, "inout_cubic"), (F(49), 232, "out_cubic"), (F(56), 256, "ressort"))
neck = Track((F(17), 12), (F(34), 8, "linear"), (F(49), 22, "out_cubic"))
J_HEAD, J_TAIL = 6, 6
T_HIT = F(49)

# rupture : les cous de la gagnante s'affinent puis cassent (gauche f53, droite f55), les moitiés reculent
tension = Track((F(49), 0), (F(53), 40, "in_cubic"))
recoil_L = Track((F(53), 0), (F(62), 1250, "out_expo"))
recoil_R = Track((F(55), 0), (F(64), 1250, "out_expo"))
neck_J = Track((F(49), 22), (F(53), 1.5, "in_cubic"))
# rayon de la gagnante « avant loupe » (la loupe vaut 1,5 au centre)
rJ = Track((F(47), RB), (F(50), RB * 1.18, "out_back"), (F(53), RB * 0.9, "in_cubic"), (F(62), RWIN / (1 + LENS), "out_back"))
green_in = Track((F(53), 0), (F(57), 1, "out_expo"))

# plongée caméra (zoom radial depuis le centre)
_dive = Track((F(60), 1.0), (F(96), 3.3, "plongee"))


def dive(t):
    return _dive(t) + 0.15 * max(0.0, t - F(96))


def reel_pulse(t, xref, sp):
    """Les bobines « avalent » chaque bulle : pulsation calée sur le passage de la pellicule."""
    w = prog(t, F(19), F(26)) * (1 - prog(t, F(50), F(56)))
    return 1 + 0.04 * w * math.sin(2 * math.pi * xref / max(sp, 1))


def intro_strip(t):
    """Bulles de la pellicule (avant et après la rupture)."""
    if t < F(17):
        return []
    x0, sp = xJ(t), spacing(t)
    sxv = sx_speed(vel(xJ, t)) / squash(t, T_HIT, F(8), 0.22)
    if t < F(53):
        ten = tension(t)
        cs = [(x0 + j * sp + (-ten if j < 0 else ten if j > 0 else 0),
               (rJ(t) if j == 0 else r_of(j)) * breathe(t, 0.04, 0.5, phase=0.13 * j))
              for j in range(-J_HEAD, J_TAIL + 1)]
        hs = [neck_J(t) if j in (-1, 0) else neck(t) for j in range(-J_HEAD, J_TAIL)]
        return strip_layer(cs, hs, sxv, "pellicule", [(x0, AXIS)] if x0 < W else [])
    L = []
    ten = 40
    for side, js, rec, t_snap in (("g", range(-J_HEAD, 0), -recoil_L(t), F(53)), ("d", range(1, J_TAIL + 1), recoil_R(t), F(55))):
        if side == "d" and t < t_snap:   # le cou droit tient encore 2 images
            continue
        cs = [(x0 + j * sp + (ten if side == "d" else -ten) + rec, r_of(j)) for j in js]
        sxg = sx_speed(vel(recoil_L if side == "g" else recoil_R, t), 260)
        L += strip_layer(cs, [neck(t)] * (len(cs) - 1), sxg, f"pellicule-{side}")
    if t < F(55):
        cs = [(x0 + j * sp + (ten if j > 0 else 0), (rJ(t) if j == 0 else r_of(j))) for j in range(0, J_TAIL + 1)]
        hs = [neck_J(t)] + [neck(t)] * (J_TAIL - 1)
        L += strip_layer(cs, hs, sxv, "pellicule-d")
    return L


def intro(t):
    L = [{"k": "bg", "v": "gradient"}]
    k = dive(t)
    # -- logo : mot + arabe, poussée lente, puis le mot est happé vers la gauche
    if t < F(17):
        L.append(wound_word(t))
    # -- pellicule
    L += intro_strip(t)
    # -- gagnante seule, puis fenêtre verte
    if t >= F(53):
        r = rJ(t) * (1 + LENS) * k
        sq = 1 / squash(t, F(62), F(8), 0.08)
        g = green_in(t)
        if g < 1 and t >= F(55):
            L.append({"k": "fill", "id": "gagnante", "fill": ORANGE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
        if g > 0:
            rg = r * g
            z = 0.72 * k ** 0.55 + 0.32 * max(0.0, t - F(53))
            if rg > 1110:
                L.append(video(z, None, ghost=False))
            else:
                L.append(video(z, ellipse_d(CX, AXIS, rg * sq, rg / sq), ghost=rg < 1000))
    # -- bobines (par-dessus : la pellicule en sort et y rentre)
    pul = reel_pulse(t, xJ(t), spacing(t))
    for i, (side, xt, rt, t_hit, t_col) in enumerate((("g", dL_x, dL_r, F(22), F(8)), ("d", dR_x, dR_r, F(14), F(8)))):
        x, r = xt(t), rt(t)
        if t < F(10):                    # les points suivent la poussée du logo et respirent
            x = CX + (x - CX) * push_logo(t)
            r *= breathe(t, 0.2, 1.1, phase=0.25 * i) if t < F(5) else 1
        x = CX + (x - CX) * k
        r *= k * (pul if side == "d" else 2 - pul)
        if side == "g":                  # la bobine gauche tourne en enroulant le mot
            r *= 1 + 0.05 * math.sin(2 * math.pi * (t - F(9)) * 6) * prog(t, F(9), F(11)) * (1 - prog(t, F(15), F(17)))
        sq = 1 / squash(t, t_hit, F(8), 0.18) / squash(t, T_HIT + (F(2) if side == "d" else 0), F(8), 0.07)
        col = mix_hex(WHITE, ORANGE, prog(t, t_col, t_col + F(3)))
        if x + r > -5 and x - r < W + 5:
            L.append(reel(x, r, sq, col, rid=f"bobine-{side}", pts=t > F(6)))
    return L


# ----------------------------------------------------------------- annotations
def a_tir(t):
    return arrow(DDX + 160, 330, W - 120, 330) + arrow(1240, 700, 760, 700, dash=True) + label(700, 780, "le mot s'enroule", 52)


def a_deroule(t):
    return arrow(1500, 330, 900, 330) + label(760, 280, "la pellicule sort de la bobine droite", 52)


def speed_lines(t, n=6, x0=420, sens=1):
    out = []
    for i in range(n):
        y = AXIS - 210 + i * 84
        if abs(y - AXIS) < 60:
            continue
        x1 = x0 + (i * 137) % 300
        out.append(f'<line class="annot" x1="{x1}" y1="{y}" x2="{x1 + 560}" y2="{y}" stroke="#FFFFFF" '
                   f'stroke-width="7" stroke-dasharray="46 20" opacity="0.85" stroke-linecap="round"/>')
    return "".join(out)


def a_vitesse(t):
    return speed_lines(t) + arrow(1260, 250, 660, 250) + label(660, 210, "150 px / image", 56)


def a_cran(t):
    return arrow(CX - 120, 330, CX + 10, 330) + label(CX - 380, 280, "dépasse de 55 px, revient", 52)


def a_rupture(t):
    return arrow(640, 320, 330, 320) + arrow(1280, 320, 1590, 320)


def a_plongee(t):
    return "".join(arrow(CX + dx * 560, AXIS + dy * 300, CX + dx * 900, AXIS + dy * 490)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(6), "Logo vivant. Anticipation : les deux points se contractent de 30 % et reculent de 14 à 18 px vers le centre ; l'arabe se replie.", "inout_cubic", onion=2),
    Beat(F(12), "Le point droit file au bord. Le gauche gonfle ×11 et commence à enrouler le mot, qui glisse vers lui en accélérant.", "in_cubic", ann=a_tir, onion=2, onion_dt=F(2)),
    Beat(F(16), "Le point droit éclate en bobine à l'impact (écrasement 82 %). Le mot est entièrement enroulé dans la bobine gauche.", "inout_cubic", onion=2, onion_dt=F(2)),
    Beat(F(24), "La bobine gauche claque au bord (dépassement 48 px). La bobine droite déroule une pellicule de bulles vers la gauche.", "in_cubic", ann=a_deroule, onion=0),
    Beat(F(33), "Pleine vitesse : 150 px par image, bulles étirées à 135 % × 74 %. Chaque bulle grossit de 50 % en passant au centre.", "linear", ann=a_vitesse, onion=0),
    Beat(F(51), "Cran : la grande bulle dépasse le centre de 55 px, revient sur un ressort et gonfle de 18 %. Écrasement 82 %, les bobines tressautent.", "ressort", ann=a_cran, onion=1, onion_dt=F(3)),
    Beat(F(56), "Rupture : les cous cassent (gauche f53, droite f55), les moitiés reculent dans les bobines. Iris vert en 4 images.", "out_expo", ann=a_rupture, onion=2, onion_dt=F(2)),
    Beat(F(74), "Plongée : la fenêtre a gonflé ×2,8 (+10 %), la caméra zoome depuis le centre ; la plaque verte zoome plus lentement.", "plongee", ann=a_plongee, onion=2, onion_dt=F(3)),
])


# ================================================================= OUTRO (4,0 s)
pull = Track((0, 3.6), (F(3), 3.35, "linear"), (F(16), 0.965, "out_expo"), (F(22), 1.0, "ressort_mou"))
win_r = Track((F(7), RWIN), (F(19), RB * (1 + LENS), "anticipe"))
orange_in = Track((F(16), 0), (F(20), 1, "out_cubic"))
grp_L = Track((F(20), -1150), (F(28), 0, "out_back"))
grp_R = Track((F(22), 1150), (F(30), 0, "out_back"))
neck_join = Track((F(26), 0), (F(31), 18, "out_back"))

# défilement inverse : contre-mouvement, accélération, 125 px/image
xr = Track((F(31), CX), (F(35), CX - 40, "out_cubic"), (F(41), CX + 210, "in_cubic"), (F(49), CX + 1210, "linear"),
           (F(60), CX + 2585, "linear"))
sp_out = Track((F(31), 256), (F(43), 280, "inout_cubic"), (F(49), 270))
suck = Track((F(49), 0), (F(56), 900, "in_cubic"))          # le reste de la pellicule est aspiré à droite
T_SNAP = F(49)
_c0 = xr(T_SNAP) - 4.5 * sp_out(T_SNAP)
_hd0 = sp_out(T_SNAP) / 2
# la paire de queue (rangs -5 et -4) se détache d'un coup sec, freine, puis se divise vers les points du logo
pair_c = Track((T_SNAP, _c0), (T_SNAP + F(4), _c0 + 40, "out_cubic"), (T_SNAP + F(10), CX, "ressort"))
pair_hd = Track((T_SNAP, _hd0), (F(51), _hd0 * 0.86, "out_cubic"), (F(54), _hd0 * 1.35, "in_cubic"),
                (F(60), (DDX - DGX) / 2, "out_back"))
pair_h = Track((T_SNAP, 18), (F(51), 24), (F(54), 1.5, "in_cubic"))
exit_L = Track((F(45), 0), (F(48), 24, "out_cubic"), (F(54), -360, "in_cubic"))
exit_R = Track((F(50), 0), (F(53), -24, "out_cubic"), (F(58), 360, "in_cubic"))
T_LOGO = F(56)


def outro_shapes(t):
    L = []
    k = pull(t)
    # -- vidéo : plein cadre puis aspirée dans la bulle
    if t < F(22):
        r = win_r(t) * k
        z = 0.72 * k ** 0.55
        if r > 1110:
            L.append(video(z, None, ghost=False))
        else:
            sq = 1 / squash(t, F(19), F(7), 0.18)
            L.append({"k": "bg", "v": "gradient"})
            L.append(video(z, ellipse_d(CX, AXIS, r * sq, r / sq), ghost=r < 1000))
            o = orange_in(t)
            if o > 0:
                L.append({"k": "fill", "id": "gagnante", "fill": ORANGE, "d": ellipse_d(CX, AXIS, r * o * sq, r * o / sq)})
    else:
        L.append({"k": "bg", "v": "gradient"})
    if t < F(20):
        return L
    # -- pellicule
    sp, x0 = sp_out(t), xr(t)
    if t < F(31):
        for side, js, g in (("g", range(-5, 0), grp_L), ("d", range(1, 9), grp_R)):
            cs = [(x0 + j * sp + g(t), r_of(j)) for j in js]
            L += strip_layer(cs, [18] * (len(cs) - 1), sx_speed(vel(g, t), 300), f"pellicule-{side}")
        hj = neck_join(t)
        if hj > 0.6:
            cs = [(x0 - sp + grp_L(t), RS), (x0, RB), (x0 + sp + grp_R(t), RS)]
            L += strip_layer(cs, [hj, hj], 1.0, "pellicule-c")
        elif t >= F(22):
            L += strip_layer([(x0, RB)], [], 1 / squash(t, F(19), F(7), 0.18), "gagnante")
    elif t < T_SNAP:
        cs = [(x0 + j * sp, r_of(j)) for j in range(-5, 12)]
        L += strip_layer(cs, [18] * (len(cs) - 1), sx_speed(vel(xr, t), 125), "pellicule", [(x0 - 5 * sp, AXIS)])
    else:
        cs = [(x0 + j * sp + suck(t), r_of(j)) for j in range(-3, 12)]
        L += strip_layer(cs, [18] * (len(cs) - 1), sx_speed(vel(xr, t) + vel(suck, t), 160), "pellicule")
    return L


def pair_layers(t):
    """Les deux bulles de queue qui deviennent les points du logo."""
    if t < T_SNAP:
        return []
    c, hd = pair_c(t), pair_hd(t)
    u = prog(t, F(52), F(60), "inout_cubic")
    ra0, rb0 = RS * lens(_c0 - _hd0), RB * lens(_c0 + _hd0)
    ra, rb = ra0 + (DOT_R - ra0) * u, rb0 + (DOT_R - rb0) * u
    col = mix_hex(ORANGE, WHITE, prog(t, F(54), F(59)))
    if t < F(54):
        sxv = sx_speed(vel(pair_c, t), 125) / squash(t, T_SNAP, F(6), 0.18)
        d = strip_path([(c - hd, ra), (c + hd, rb)], [pair_h(t)], sxv)
        return [{"k": "fill", "id": "points-logo", "fill": col, "d": d, "pts": [(c - hd, AXIS), (c + hd, AXIS)]}]
    out = []
    for i, (x, r) in enumerate(((c - hd, ra), (c + hd, rb))):
        if t > F(60):
            r = DOT_R * breathe(t, 0.2, 1.1, phase=0.25 * i)
        out.append({"k": "fill", "id": f"logo-point-{'gd'[i]}", "fill": col, "d": circ(x, r), "pts": [(x, AXIS)]})
    return out


def outro_reels(t):
    out = []
    for side, kk, ex in (("g", pull(t), exit_L), ("d", pull(max(0.0, t - F(2))), exit_R)):
        x = (CX - CX * kk if side == "g" else CX + CX * kk) + ex(t)
        sq = 1 / squash(t, F(16) + (F(2) if side == "d" else 0), F(8), 0.12)
        gulp = 1.0
        if side == "d":
            gulp = 1 + 0.07 * math.sin(math.pi * prog(t, F(49), F(54)))
            w = prog(t, F(37), F(42)) * (1 - prog(t, F(48), F(50)))
            gulp *= 1 + 0.04 * w * math.sin(2 * math.pi * xr(t) / sp_out(t))
        r = R_REEL * kk * gulp
        if x + r > -5 and x - r < W + 5:
            out.append(reel(x, r, sq, rid=f"bobine-{side}"))
    return out


def outro_full(t):
    L = outro_shapes(t) + outro_reels(t)
    return L + endcard(t, T_LOGO, dots=False, extra=pair_layers(t))


def a_aspire(t):
    return "".join(arrow(CX + dx * 900, AXIS + dy * 480, CX + dx * 560, AXIS + dy * 300)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_retour(t):
    return arrow(60, 300, 330, 300) + arrow(W - 60, 300, W - 330, 300)


def a_rejoint(t):
    return arrow(360, 360, 640, 360) + arrow(W - 360, 360, W - 640, 360)


def a_inverse(t):
    return speed_lines(t, x0=600) + arrow(660, 250, 1260, 250) + label(560, 210, "sens inverse · 125 px / image", 56)


def a_depose(t):
    return arrow(1300, 330, 1640, 330) + label(1300, 280, "aspirée", 52)


def a_division(t):
    return arrow(830, 380, 640, 380) + arrow(1090, 380, 1280, 380)


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(6), "Aspiration : la vidéo plein cadre se rétracte en bulle (zoom radial 335 % → 100 % en 13 images), la plaque recule aussi.", "out_expo", ann=a_aspire, onion=2, onion_dt=F(2)),
    Beat(F(15), "Les bobines reviennent aux bords et dépassent de 3,5 % avant de se caler sur leur milieu (la droite 2 images après).", "ressort_mou", ann=a_retour, onion=2, onion_dt=F(2)),
    Beat(F(21), "La fenêtre inspire (+6 %) puis se contracte ×2,8 ; un iris orange referme la vidéo en 4 images, avec écrasement.", "anticipe", onion=2, onion_dt=F(2)),
    Beat(F(27), "Les deux moitiés de pellicule ressortent des bobines (décalage 2 images) et se ressoudent à la bulle centrale.", "out_back", ann=a_rejoint, onion=0),
    Beat(F(45), "Défilement inverse : recul de 40 px, puis la pellicule file à droite à 125 px par image ; chaque bulle grossit au centre.", "in_cubic", ann=a_inverse, onion=0),
    Beat(F(51), "Coup sec : la queue de la pellicule se détache et freine (écrasement) ; le reste est aspiré dans la bobine droite (+7 %).", "out_cubic", ann=a_depose, onion=2, onion_dt=F(2)),
    Beat(F(56), "Les deux dernières bulles se séparent : le cou s'affine et casse, elles virent au blanc et filent vers les points du logo.", "out_back", ann=a_division, onion=2, onion_dt=F(2)),
    Beat(F(90), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; « sfeer » s'est ouvert, l'arabe écrit de droite à gauche.", "emphase", onion=0),
])


NOTES = [
    ("Pourquoi ça marche", [
        "Une image simple : deux bobines et une pellicule. Le cinéma est dit par la forme, avant même la vidéo.",
        "Le cran de machine à sous crée l'attente puis la récompense : une bulle est tirée au sort et devient l'histoire.",
        "Les points du logo deviennent les bobines, et l'outro les rend au logo : la boucle est fermée.",
    ]),
    ("Charte et corrections", [
        "Ta colonne verticale de points devient une bande horizontale sur l'axe y = 540 : la charte interdit les bulles alignées à la verticale.",
        "Tes 3 cercles empilés deviennent le cran horizontal ; ton haltère devient le cou qui casse. Les bobines sont coupées à leur milieu (2.48).",
        "Écarts à valider : le mot s'enroule dans le point gauche (7 images) ; un anneau orange entoure l'iris vert pendant 3 images.",
    ]),
    ("Mouvement", [
        "Rampe complète : accélération in_cubic, 150 px par image, freinage out_cubic, dépassement de 55 px et ressort.",
        "Étirement jusqu'à 135 % × 74 % avec la vitesse, écrasement 82 % à l'arrêt ; décalages de 2 à 3 images entre gauche et droite.",
        "AE : pellicule = calques de forme sur un nul qui défile ; les bobines sont des masques. Natif en Lottie.",
    ]),
]
