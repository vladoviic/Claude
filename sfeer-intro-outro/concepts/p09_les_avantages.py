"""Piste 9 (croquis de la DA, précisée) : « Les avantages ».

Le point droit de ·sfeer· fait jaillir une liste d'avantages (puces + texte, lorem ipsum
pour l'instant) qui défile verticalement comme une machine à sous. Elle ralentit et s'arrête
sur une ligne : la puce de cette ligne et le point du logo se lient par un cou horizontal.
Le mot est avalé, la liste s'écarte, il reste trois bulles empilées : celle du centre grossit
et devient la fenêtre.

Écart de charte assumé par la DA : défilement et empilement verticaux (« on garde le
défilement vertical parce que le lien est horizontal »).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, FPS, Anim, Beat, Track, back_out, breathe, prog, render_layers  # noqa: E402
from blocks import LG, arabic, drift, endorse, hold_drift, logo_dots, video, word  # noqa: E402
from sfeer_svg import (AXIS, FONT, H, ORANGE, WHITE, W, arrow, bridge_d, circle_d,  # noqa: E402
                       curved_arrow, ellipse_d, f, mix_hex)

CX = W / 2

META = {
    "id": "p09_les_avantages",
    "num": "P9",
    "title": "Les avantages",
    "principe": "Le logo lance la liste des avantages : elle tourne, s'arrête, la puce se lie au logo et ouvre la fenêtre.",
    "logline": "Piste 9 de la DA. Le point de ·sfeer· fait jaillir la liste des avantages, qui défile comme une machine à sous. "
               "Elle s'arrête : la puce et le point du logo se lient, trois bulles restent, celle du centre devient la fenêtre.",
}

# --- Mise en page de la liste -------------------------------------------------
DX = -400                       # le logo est décalé à gauche pendant la liste
XD = LG["dot_d"][0] + DX        # point droit du logo (≈ 839)
XG = LG["dot_g"][0] + DX        # point gauche du logo
XB = XD + 125                   # colonne des puces (au plus près du point du logo, comme sur le croquis)
XT = XB + 30                    # début du texte
SP = 70                         # interligne
FS = 30
RB = 9                          # rayon d'une puce
R_ARC = 820                     # la liste court sur un arc (tambour de machine à sous) bombé vers la droite
FAN = 0.45                      # les lignes s'ouvrent en éventail (rotation = 45 % de l'angle sur l'arc)
PHRASES = ["Lorem ipsum dolor sit amet", "Consectetur adipiscing elit", "Sed do eiusmod tempor",
           "Ut labore et dolore magna", "Duis aute irure dolor", "Excepteur sint occaecat",
           "Cupidatat non proident", "Sunt in culpa qui officia", "Ut enim ad minim veniam",
           "Quis nostrud exercitation"]

# défilement : vitesse constante puis arrêt « machine à sous » (dépassement puis retour)
V0 = 47.0                                       # px par image (≈ 0,67 ligne par image)
N1 = 30                                         # fin de la vitesse constante (image)
K = round((V0 * N1 + V0 * 26 / 4.7) / SP)        # ligne sur laquelle on s'arrête
D = K * SP - V0 * N1
T_DEC = D * 4.7 / V0                            # durée de décélération (images) qui raccorde la vitesse
STOP = N1 + T_DEC


def phrase(i):
    return PHRASES[(i - K) % len(PHRASES)]


def scroll_in(n):
    """Décalage vertical (px) de la liste à l'image n (intro)."""
    if n <= N1:
        return V0 * n
    u = min(1.0, (n - N1) / T_DEC)
    s = 1.70158
    e = (u - 1) ** 2 * ((s + 1) * (u - 1) + s) + 1          # back out, vitesse initiale raccordée
    return V0 * N1 + D * e


def speed(fn, n):
    return abs(fn(n + 0.5) - fn(n - 0.5))


def item_pos(yl):
    """Position d'un item sur le tambour : yl = écart à l'axe le long de la liste (px).
    Renvoie (x, y, angle_deg, échelle) : l'item glisse sur un arc, s'incline en éventail et rapetisse
    en s'éloignant de l'axe (perspective du tambour)."""
    th = yl / R_ARC
    return (XB - R_ARC * (1 - math.cos(th)), AXIS + R_ARC * math.sin(th),
            math.degrees(th) * FAN, 0.55 + 0.45 * math.cos(th))


def list_layers(n, s, v, reveal=1.0, text=1.0, rows=None, xb=XB, keep=None, ry_scale=None, uid="l"):
    """Puces + lignes de texte. v = vitesse (px/image) : au-dessus de 14, le texte devient des barres
    (comme les traits du croquis) et les puces s'étirent verticalement (volume conservé)."""
    L = []
    st = min(1.35, 1 + v / 110)
    half = 600 * reveal
    clip = f'<clipPath id="{uid}c"><rect x="0" y="{f(AXIS - half)}" width="{W}" height="{f(2 * half)}"/></clipPath>'
    bul, txt = [], []
    for i in (rows if rows is not None else range(-8, K + 9)):
        yl = i * SP - s
        if abs(yl) > R_ARC * 1.0:
            continue
        if keep is not None and i in keep:
            continue
        x, y, ang, sc = item_pos(yl)
        x += xb - XB
        r = RB * (ry_scale(i) if ry_scale else 1)
        g = f'translate({f(x)} {f(y)}) rotate({f(ang)}) scale({f(sc)})'
        bul.append(f'<path transform="{g}" d="{ellipse_d(0, 0, r / st, r * st)}" fill="{ORANGE}"/>')
        if text > 0:
            tw = len(phrase(i)) * FS * 0.5
            dx = XT - XB
            if v > 10:
                txt.append(f'<rect transform="{g}" x="{dx}" y="-5" width="{f(tw * text)}" height="10" rx="5" fill="{WHITE}" opacity="0.85"/>')
            else:
                txt.append(f'<g transform="{g}"><clipPath id="{uid}t{i}"><rect x="{dx - 4}" y="{f(-FS)}" width="{f((tw + 30) * text)}" height="{f(FS * 1.6)}"/></clipPath>'
                           f'<text clip-path="url(#{uid}t{i})" x="{dx}" y="{f(FS * 0.34)}" font-family="{FONT}" '
                           f'font-size="{FS}" fill="{WHITE}">{phrase(i)}</text></g>')
    L.append({"k": "raw", "svg": clip + f'<g clip-path="url(#{uid}c)">{"".join(txt)}{"".join(bul)}</g>'})
    return L


def logo_left(t, swallow=0.0, uid="lg"):
    """Logo complet décalé à gauche ; swallow 0..1 = le mot est avalé vers son point droit."""
    inner = render_layers(word(1) + arabic(1), uid=uid)
    x0 = LG["word_x"] - 30
    x1 = LG["dot_d"][0]
    cut = x0 + (x1 - x0) * swallow
    svg = (f'<clipPath id="{uid}sw"><rect x="{f(cut)}" y="300" width="{f(x1 - cut + 40)}" height="420"/></clipPath>'
           f'<g clip-path="url(#{uid}sw)">{inner}</g>')
    return {"k": "group", "dx": DX, "layers": [{"k": "raw", "svg": svg}]}


# ----------------------------------------------------------------- INTRO (4,4 s)
LINK0, LINK1 = math.ceil(STOP), math.ceil(STOP) + 5         # langue puis contact
rd = Track((F(LINK0 - 3), LG["dot_r"]), (F(LINK0), LG["dot_r"] * 1.7, "out_back"),
           (F(LINK1), LG["dot_r"] * 1.4, "in_cubic"), (F(LINK1 + 8), 34, "out_back"))
rb = Track((F(LINK1 - 1), RB), (F(LINK1 + 9), 58, "out_back_fort"))
neck = Track((F(LINK1), 5), (F(LINK1 + 8), 14, "out_cubic"))
merge = Track((F(72), 0.0), (F(81), 1.0, "in_expo"))               # le point du logo est absorbé
center_x = Track((F(76), XB), (F(88), CX, "emphase"))
trio = Track((F(72), 0.0), (F(86), 1.0, "out_back"))
grow = Track((F(86), 1.0), (F(89), 0.9, "in_cubic"), (F(98), 3.6, "out_back"))   # anticipation puis gonfle
green = Track((F(88), 0.0), (F(96), 1.0, "out_expo"))
plunge = Track((F(97), 1.0), (F(110), 3.4, "plongee"))


def intro(t):
    n = t * FPS
    L = [{"k": "bg", "v": "gradient"}]
    s = scroll_in(n)
    v = speed(scroll_in, n)
    # 1) liste + logo
    if n < 86:
        swallow = prog(t, F(66), F(78), "in_expo")
        if swallow < 1:
            L.append(logo_left(t, swallow))
        if n < 72:
            gx = LG["dot_g"][0] + DX
            L += [{"k": "fill", "id": "logo-point-g", "fill": WHITE, "ghost": False,
                   "d": circle_d(gx, AXIS, LG["dot_r"] * breathe(t, 0.2, 1.1))}]
        elif n < 78:
            # le point gauche file le long de l'axe et rejoint le lien
            u = prog(t, F(72), F(78), "in_expo")
            gx = XG + (XD - XG) * u
            L.append({"k": "fill", "id": "logo-point-g", "fill": mix_hex(WHITE, ORANGE, u), "ghost": False,
                      "d": ellipse_d(gx, AXIS, LG["dot_r"] * (1 + u * 0.6), LG["dot_r"] / (1 + u * 0.6)), "pts": [(gx, AXIS)]})
        if n < LINK0 - 3:
            L.append({"k": "fill", "id": "logo-point-d", "fill": WHITE, "ghost": False,
                      "d": circle_d(XD, AXIS, LG["dot_r"] * breathe(t, 0.2, 1.1, 0.25))})
        reveal = prog(t, 0, F(10), "out_expo")
        retract = 1 - prog(t, F(64), F(74), "in_cubic")
        spread = prog(t, F(70), F(84), "in_expo")
        keep = {K - 1, K, K + 1} if n >= LINK1 else ({K} if n >= LINK0 - 3 else set())
        if spread < 1:
            # les autres lignes s'écartent vers le haut et le bas en accélérant
            L += list_layers(n, s + 0, v, reveal, retract, keep=keep, uid="li") if spread == 0 else \
                list_layers(n, s, 0, 1, retract, rows=[i for i in range(K - 8, K + 9) if i not in keep and i < K], uid="lh") + \
                [{"k": "group", "dy": -900 * spread, "layers": []}]
            if spread > 0:
                L += [{"k": "group", "dy": -1100 * spread, "layers": list_layers(n, s, 0, 1, retract, rows=[i for i in range(K - 8, K) if i not in keep], uid="lu")},
                      {"k": "group", "dy": 1100 * spread, "layers": list_layers(n, s, 0, 1, retract, rows=[i for i in range(K + 1, K + 9) if i not in keep], uid="ld")}]
                L = [x for x in L if not (x.get("k") == "group" and not x.get("layers"))]
                L = [x for x in L if x.get("k") != "raw" or "lhc" not in x.get("svg", "")]
        # voisines K-1 / K+1 : elles deviennent les bulles du haut et du bas
        if n >= LINK1:
            for j, sign in ((K - 1, -1), (K + 1, 1)):
                x0, y0, _, _ = item_pos(j * SP - s)
                u = trio(t)
                y = y0 + (AXIS + sign * (430 if sign < 0 else 470) - y0) * u
                x = x0 + (center_x(t) - x0) * u
                r = RB + (82 - RB) * u
                if retract > 0:
                    L += list_layers(n, s, 0, 1, retract, rows=[j], uid=f"v{j}")
                    L = [x2 for x2 in L if not (x2.get("k") == "raw" and f'id="v{j}c"' in x2.get("svg", "") and False)]
                L.append({"k": "fill", "id": f"trio-{'hb'[sign > 0]}", "fill": ORANGE, "d": circle_d(x, y, r), "pts": [(x, y)]})
        # 2) la puce sélectionnée et le lien avec le point du logo
        yK = AXIS + K * SP - s
        if n < LINK0 - 3:
            if retract > 0:
                pass  # la ligne K est dessinée avec la liste
        xb = center_x(t)
        rbb = rb(t) * (breathe(t, 0.05, 0.5) if n > LINK1 + 9 else 1)
        if n >= LINK0 - 3:
            if retract > 0:
                rk = 1 - prog(t, F(LINK1 - 3), F(LINK1 + 5), "in_cubic")
                if rk > 0:
                    L += list_layers(n, s, 0, 1, rk, rows=[K], uid="lk", ry_scale=lambda i: 0)
        if LINK0 - 3 <= n < LINK1:
            # langue : le point du logo s'étire vers la puce
            u = prog(t, F(LINK0), F(LINK1), "in_expo")
            tip = XD + (XB - XD) * u
            dcol = mix_hex(WHITE, ORANGE, u)
            L.append({"k": "fill", "id": "puce", "fill": ORANGE, "d": circle_d(XB, yK, RB)})
            if u > 0.02:
                L.append({"k": "fill", "id": "langue", "fill": dcol, "d": bridge_d((XD, AXIS, rd(t)), (tip, AXIS, 6), 3), "pts": [(tip, AXIS)]})
            else:
                L.append({"k": "fill", "id": "logo-point-d", "fill": dcol, "d": circle_d(XD, AXIS, rd(t))})
        elif n >= LINK1:
            m = merge(t)
            xd = XD + (xb - XD) * m
            r_d = rd(t) * (1 - 0.6 * m)
            sq = 1 + 0.25 * math.exp(-4 * prog(t, F(81), F(89))) * math.cos(3 * math.pi * prog(t, F(81), F(89))) if n >= 81 else 1
            if m < 0.98 and xb - xd > rbb * 0.6:
                d = bridge_d((xd, AXIS, r_d), (xb, AXIS, rbb), neck(t) * (1 - m) + 2)
            else:
                d = ellipse_d(xb, AXIS, rbb * sq, rbb / sq)
            L.append({"k": "fill", "id": "lien", "fill": ORANGE, "d": d, "pts": [(xd, AXIS)]})
    # 3) trio vertical -> la bulle du centre devient la fenêtre
    if n >= 86:
        g = grow(t)
        rc = 62 * g * (1 + 0.04 * math.sin(2 * math.pi * t * 3)) if n < 97 else 62 * 3.6
        k = plunge(t)
        rc = rc * (k if n >= 97 else 1)
        absorb = prog(t, F(88), F(97), "in_expo")
        for sign in (-1, 1):
            y = AXIS + sign * (430 if sign < 0 else 470) * (1 - absorb)
            if absorb < 0.999:
                L.append({"k": "fill", "id": f"trio-{'hb'[sign > 0]}", "fill": ORANGE, "d": circle_d(CX, y, 82 * (1 - 0.4 * absorb)), "pts": [(CX, y)]})
        L.append({"k": "fill", "id": "bulle-centre", "fill": ORANGE, "d": circle_d(CX, AXIS, rc)})
        gr = green(t)
        if gr > 0:
            L.append(video(0.7 * k ** 0.6 + drift(t, F(97), 0.3), circle_d(CX, AXIS, rc * gr), ghost=gr < 1))
    return L


def a_defile(t):
    return arrow(1880, 820, 1880, 260) + arrow(1830, 820, 1830, 360)


def a_lien(t):
    return arrow(XD + 20, AXIS - 90, XB - 30, AXIS - 90)


def a_trio(t):
    return arrow(CX + 170, AXIS - 60, CX + 170, AXIS - 320) + arrow(CX + 170, AXIS + 60, CX + 170, AXIS + 320)


def a_plonge(t):
    return "".join(arrow(CX + dx * 480, AXIS + dy * 270, CX + dx * 880, AXIS + dy * 490) for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.4, intro, [
    Beat(F(4), "Les avantages jaillissent du point droit du logo : la liste s'ouvre depuis l'axe (10 images) et défile déjà.", "out_expo", onion=0),
    Beat(F(20), "Tambour de machine à sous : la liste tourne sur son arc (0,7 ligne par image), le texte n'est plus que des traits en éventail.", "linear", ann=a_defile, onion=0),
    Beat(F(46), "Freinage : la liste ralentit, le texte redevient lisible, une ligne dépasse l'axe de 10 % puis revient se caler.", "out_back", onion=2, onion_dt=F(4)),
    Beat(F(LINK0 + 3), "Le point du logo gonfle et tire une langue horizontale vers la puce arrêtée sur l'axe.", "in_expo", ann=a_lien),
    Beat(F(LINK1 + 6), "Contact : le point et la puce se lient (haltère o—O), le texte se rétracte dans les puces.", "out_back_fort"),
    Beat(F(80), "Le mot est avalé par son point, la liste s'écarte vers le haut et le bas, les voisines deviennent deux bulles.", "in_expo", ann=a_trio),
    Beat(F(92), "Trois bulles empilées ; celle du centre vibre, rétrécit (anticipation) puis gonfle et avale les deux autres.", "out_back"),
    Beat(F(104), "La vidéo éclot dans la bulle, plongée en zoom diagonal, la poussée ne s'arrête jamais.", "plongee", ann=a_plonge),
])


# ----------------------------------------------------------------- OUTRO (4,4 s)
o_win = Track((F(4), 3.6), (F(20), 1.0, "emphase"))                  # le plein cadre se referme en bulle
o_pull = Track((0, 1.25), (F(20), 1.0, "out_cubic"))
o_orange = Track((F(22), 0.0), (F(32), 1.0, "out_expo"))             # la bulle redevient orange
o_trio = Track((F(22), 0.0), (F(34), 1.0, "out_back"))               # les bulles du haut et du bas sortent
o_shrink = Track((F(34), 0.0), (F(44), 1.0, "in_cubic"))             # trio -> puces, la liste repousse
o_bloom = Track((F(40), 0.0), (F(50), 1.0, "out_expo"))
# défilement vers le bas : accélère (in_cubic), puis freine avec un léger dépassement et se cale sur K
_rest = Track((F(42), 14 * SP), (F(56), 9 * SP, "in_cubic"), (F(84), 0, back_out(0.8)))


def scroll_out(n):
    return K * SP + _rest(n / FPS)


o_link = Track((F(84), 0.0), (F(90), 1.0, "in_expo"))                 # la puce se lie au point du logo
o_gather = Track((F(86), 0.0), (F(94), 1.0, "in_expo"))               # la liste part, il reste le logo
o_center = Track((F(93), DX), (F(106), 0, "emphase"))                  # le logo glisse au centre
o_word = Track((F(56), 0.0), (F(70), 1.0, "emphase"))
o_ar = Track((F(62), 0.0), (F(74), 1.0, "emphase"))
o_endo = Track((F(98), 0.0), (F(108), 1.0, "emphase"))


def outro(t):
    n = t * FPS
    L = []
    if n < 20:
        L.append(video(o_pull(t), ghost=False))
        r = 620 * o_win(t)
        L.insert(0, {"k": "bg", "v": "gradient"})
        L[-1] = video(o_pull(t), circle_d(CX, AXIS, r), ghost=r < 1500)
        return L
    L.append({"k": "bg", "v": "gradient"})
    if n < 44:
        rc = 620 * (1 - 0.35 * o_trio(t)) * (1 - 0.8 * o_shrink(t))
        u = o_trio(t) * (1 - o_shrink(t))
        for sign in (-1, 1):
            y = AXIS + sign * 440 * o_trio(t)
            xa, ya, _, _ = item_pos(sign * SP)
            y = y + (ya - y) * o_shrink(t)
            r = 82 * u + RB * o_shrink(t)
            if o_trio(t) > 0.02:
                L.append({"k": "fill", "id": f"trio-{'hb'[sign > 0]}", "fill": ORANGE, "d": circle_d(CX + (xa - CX) * o_shrink(t), y, max(r, 2)), "pts": [(CX, y)]})
        x = CX + (XB - CX) * o_shrink(t)
        L.append({"k": "fill", "id": "bulle-centre", "fill": ORANGE, "d": circle_d(x, AXIS, max(rc, RB))})
        if o_orange(t) < 1:
            L.append(video(1.0 + drift(t, F(20), 0.4), circle_d(x, AXIS, max(rc, RB) * (1 - o_orange(t))), ghost=False))
        return L
    # la liste repousse depuis les puces, défile vers le bas puis s'arrête
    s = scroll_out(n)
    v = speed(scroll_out, n)
    gather = o_gather(t)
    bloom = o_bloom(t)
    if gather < 1:
        rows_up = [i for i in range(K - 9, K + 9) if i < K]
        rows_dn = [i for i in range(K - 9, K + 9) if i > K]
        L += [{"k": "group", "dy": -1100 * gather, "layers": list_layers(n, s, v, bloom, bloom * (1 - gather), rows=rows_up, uid="ou")},
              {"k": "group", "dy": 1100 * gather, "layers": list_layers(n, s, v, bloom, bloom * (1 - gather), rows=rows_dn, uid="od")}]
        if o_link(t) == 0:
            L += list_layers(n, s, v, bloom, bloom, rows=[K], uid="ok")
    # logo à gauche, qui glisse ensuite au centre
    dx = o_center(t)
    logo_l = word(o_word(t)) + arabic(o_ar(t))
    lk = o_link(t)
    yK = AXIS + K * SP - s
    dots = logo_dots(t)
    if lk > 0:
        # la puce K (sur l'axe) se lie au point droit du logo puis s'y fond
        xd = LG["dot_d"][0] + dx
        xb = XB + (xd - XB) * o_gather(t)
        rb_ = RB * (1 - 0.3 * o_gather(t))
        if xb - xd > 6:
            d = bridge_d((xd, AXIS, LG["dot_r"] * (1 + lk * 0.4)), (xb, AXIS, rb_), 3 + 3 * lk)
            L.append({"k": "fill", "id": "lien", "fill": mix_hex(ORANGE, WHITE, o_gather(t)), "d": d, "pts": [(xb, AXIS)]})
        rk = 1 - prog(t, F(84), F(90), "in_cubic")
        if rk > 0:
            L += list_layers(n, s, 0, 1, rk, rows=[K], uid="okt", ry_scale=lambda i: 0)
    drift_s = hold_drift(t, F(104))
    L.append({"k": "group", "s": drift_s, "layers": [{"k": "group", "dx": dx, "layers": logo_l + dots}]})
    L += endorse(o_endo(t))
    return L


def a_referme(t):
    return "".join(arrow(CX + dx * 880, AXIS + dy * 480, CX + dx * 520, AXIS + dy * 300) for dx in (-1, 1) for dy in (-1, 1))


def a_defile_bas(t):
    return arrow(1880, 260, 1880, 820) + arrow(1830, 360, 1830, 820)


def a_glisse(t):
    return arrow(560, 820, 900, 820)


OUTRO = Anim("OUTRO", 4.4, outro, [
    Beat(F(10), "Fin du plan : la vidéo se referme en une grande bulle centrée (zoom arrière 125 % -> 100 %).", "emphase", ann=a_referme),
    Beat(F(28), "La bulle redevient orange depuis le centre ; deux bulles jaillissent en haut et en bas (le trio revient).", "out_back"),
    Beat(F(42), "Le trio rétrécit en puces et se range dans la colonne ; le logo commence à s'ouvrir à gauche.", "in_cubic"),
    Beat(F(56), "La liste repousse depuis les puces et part vers le bas en accélérant (traits de vitesse, puces étirées).", "in_cubic", ann=a_defile_bas, onion=0),
    Beat(F(76), "Freinage machine à sous : la liste ralentit, le texte redevient lisible, léger dépassement puis retour sur l'axe.", "out_back", onion=2, onion_dt=F(4)),
    Beat(F(87), "La puce arrêtée sur l'axe se lie au point droit du logo par un cou horizontal.", "in_expo"),
    Beat(F(97), "La liste est sortie ; la puce s'est fondue dans le point du logo, qui glisse vers le centre (13 images).", "emphase", ann=a_glisse),
    Beat(F(108), "Carton : logo centré, arabe révélé, endossement en bas ; points qui respirent et poussée lente continue.", "emphase"),
])

NOTES = [
    ("Pourquoi ça marche", [
        "Le logo parle : ses points « contiennent » les avantages SFEER. La liste est un vrai support de message, remplaçable à chaque film.",
        "La machine à sous dit la promesse sans un mot : on tire, ça s'arrête sur un avantage, et cet avantage nous ouvre le film.",
        "Lien horizontal entre le point du logo et la puce : la mécanique de la charte (3.3) au moment clé.",
    ]),
    ("Charte et corrections", [
        "Écart assumé par la DA : défilement et trio verticaux. Le lien, lui, reste horizontal et sur l'axe. À faire valider par la marque.",
        "Texte en lorem ipsum, à remplacer par les vrais avantages (ex. partenaires, points, paiement) en Loew Riyadh Air.",
        "Le logo n'est jamais recouvert : la liste reste à sa droite, puis il est avalé par son propre point.",
    ]),
    ("Mouvement", [
        "La liste court sur un arc (rayon 820 px) : lignes en éventail, items qui rapetissent vers le haut et le bas, comme un tambour.",
        "Vitesse raccordée : 47 px/image puis freinage « back out » qui part à la même vitesse ; au-delà de 10 px/image, le texte devient des traits.",
        "Asymétrie : la liste du haut et celle du bas partent avec la même accélération mais le trio se recale en 2 temps.",
    ]),
]
