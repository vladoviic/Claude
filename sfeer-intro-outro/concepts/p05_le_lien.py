"""Piste 5 (croquis de la DA) : « utiliser le lien comme fenêtre ».

Deux bulles du fond SFEER, coupées à leur milieu vertical par les bords du cadre, pincent
l'espace orange entre elles : ce col, le lien, devient la fenêtre sur la vidéo.
La caméra pousse en diagonale (zoom depuis le centre) et non verticalement (correction DA).

Trois couches empilées : le monde SFEER (dégradé), le lien (orange), la vidéo (vert).
Les bulles sont des trous qui montrent le dégradé.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from motion import F, Anim, Beat, Track, breathe, prog  # noqa: E402
from blocks import GRAD, LG, drift, endcard, video  # noqa: E402
from sfeer_svg import (AXIS, ORANGE, WHITE, W, arrow, bridge_d, circle_d, ellipse_d,  # noqa: E402
                       mix_hex, waist_h)

CX = W / 2

META = {
    "id": "p05_le_lien",
    "num": "P5",
    "title": "Le lien",
    "logline": "Piste 5 de la DA. Un point orange explose et inonde le cadre ; deux bulles du dégradé le mordent "
               "depuis les bords et le pincent en sablier : ce lien devient la fenêtre, la caméra plonge en diagonale.",
}


# ----------------------------------------------------------------- INTRO (4,0 s)
dot_r = Track((0, 0), (F(3), 22, "out_cubic"), (F(12), 96, "out_back_fort"),
              (F(20), 78, "in_cubic"),                       # inspiration (anticipation)
              (F(38), 1250, "out_expo"))                     # explosion radiale = diagonale
hole_l = Track((F(24), 0), (F(38), 600, "out_back"), (F(52), 690, "in_cubic"),
               (F(60), 640, "out_back_fort"))                # recul quand la vidéo éclate
hole_r = Track((F(26), 0), (F(40), 600, "out_back"), (F(53), 690, "in_cubic"),
               (F(61), 640, "out_back_fort"))                # 2 images de retard : asymétrie
green_r = Track((F(52), 0), (F(64), 1150, "out_expo"))
_push = Track((F(58), 1.0), (F(90), 3.6, "plongee"))


def push(t):
    return _push(t) + drift(t, F(58))          # la poussée ne s'arrête jamais (raccord en mouvement)


def push_speed(t):
    return (push(t + 0.01) - push(t - 0.01)) / 0.02


def holes(t, rl, rr, k=1.0):
    """Bulles-trous sur les bords, éloignées et grossies par la poussée caméra k (zoom centré)."""
    s = min(1.0 + 0.035 * push_speed(t), 1.3)            # étirement dans le sens du mouvement
    out = []
    for side, r in (("g", rl), ("d", rr)):
        if r <= 1:
            continue
        cx = CX - CX * k if side == "g" else CX + CX * k
        out.append({"k": "fill", "id": f"bulle-{side}", "fill": GRAD,
                    "d": ellipse_d(cx, AXIS, r * k * s, r * k / math.sqrt(s)), "pts": [(cx, AXIS)]})
    return out


def intro(t):
    k = push(t)
    L = [{"k": "bg", "v": "gradient"}]
    r = dot_r(t)
    if r > 0.5:
        # écrasement à l'atterrissage du pop, puis rond
        sq = 1 + 0.18 * math.sin(math.pi * prog(t, F(9), F(16)))
        L.append({"k": "fill", "id": "point", "fill": ORANGE, "ghost": r < 900,
                  "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
    if green_r(t) > 1:
        L.append(video(0.8 * k ** 0.55, circle_d(CX, AXIS, green_r(t)), ghost=green_r(t) < 1100))
    L += holes(t, hole_l(t), hole_r(t), k)
    return L


def a_explosion(t):
    return "".join(arrow(CX + dx * 170, AXIS + dy * 120, CX + dx * 560, AXIS + dy * 400)
                   for dx in (-1, 1) for dy in (-1, 1))


def a_morsure(t):
    return arrow(60, AXIS, 330, AXIS) + arrow(W - 60, AXIS, W - 330, AXIS)


def a_poussee(t):
    return "".join(arrow(CX + dx * 520, AXIS + dy * 290, CX + dx * 900, AXIS + dy * 500)
                   for dx in (-1, 1) for dy in (-1, 1))


INTRO = Anim("INTRO", 4.0, intro, [
    Beat(F(7), "Un point orange éclot au centre, sur l'axe : pop avec dépassement (+15 %) et léger écrasement à l'arrivée.", "out_back_fort"),
    Beat(F(18), "Anticipation : le point « inspire » et rétrécit de 20 % pendant 8 images avant d'exploser.", "in_cubic"),
    Beat(F(28), "Explosion radiale : l'orange envahit le cadre en 18 images, dans toutes les directions (diagonales).", "out_expo", ann=a_explosion),
    Beat(F(36), "Deux bulles du dégradé mordent l'orange depuis les bords, coupées à leur milieu vertical. La droite suit avec 2 images de retard.", "out_back", ann=a_morsure),
    Beat(F(50), "Tension : les bulles gonflent et serrent le lien orange en sablier. Le col se resserre, ça va céder.", "in_cubic"),
    Beat(F(57), "La vidéo éclate au cœur du lien (point vert qui grandit) ; les bulles reculent sous le choc (action secondaire).", "out_expo"),
    Beat(F(74), "Plongée : zoom depuis le centre, les bulles filent en diagonale vers les coins et s'étirent avec la vitesse.", "plongee", ann=a_poussee),
    Beat(F(96), "Plein cadre vidéo, la poussée continue en décélérant : on raccorde sur un plan en mouvement, jamais figé.", "out_cubic"),
])


# ----------------------------------------------------------------- OUTRO (4,0 s)
pull = Track((0, 1.25), (F(14), 1.0, "out_cubic"), (F(44), 0.9, "linear"))
hx_l = Track((F(6), -980), (F(26), 0, "out_back"))
hx_r = Track((F(9), W + 980), (F(29), W, "out_back"))
squeeze_l = Track((F(26), 640), (F(52), 790, "in_cubic"))     # les bulles serrent le lien : tension
squeeze_r = Track((F(28), 640), (F(54), 790, "in_cubic"))
orange_in = Track((F(28), 0), (F(40), 1110, "out_expo"), (F(58), 70, "anticipe"))   # 1110 = coin du cadre
split = Track((F(64), 0.0), (F(76), 1.0, "out_cubic"))
travel = Track((F(72), 0.0), (F(86), 1.0, "emphase"))


def outro(t):
    L = []
    swap = t >= F(40)                                     # bascule invisible vert -> dégradé
    L.append({"k": "bg", "v": "gradient"} if swap else video(pull(t), ghost=False))
    ro = orange_in(t)
    if ro > 1 and t < F(58):
        L.append({"k": "fill", "id": "lien", "fill": ORANGE, "ghost": ro < 1100,
                  "d": circle_d(CX, AXIS, ro), "pts": []})
    if t < F(58):
        # les bulles restent posées : sur le dégradé elles deviennent invisibles d'elles-mêmes
        for side, tr, sq in (("g", hx_l, squeeze_l), ("d", hx_r, squeeze_r)):
            x = tr(t)
            L.append({"k": "fill", "id": f"bulle-{side}", "fill": GRAD, "d": circle_d(x, AXIS, sq(t)),
                      "pts": [(x, AXIS)], "ghost": not swap})
    if t >= F(58):
        u, v = split(t), travel(t)
        # le point se divise (cacahuète -> col -> rupture) puis les deux bulles rejoignent les points du logo
        gx, dx = LG["dot_g"][0], LG["dot_d"][0]
        spread = 70 * u + (CX - gx - 70) * v
        r = (80 / math.sqrt(2)) * (1 - v) + LG["dot_r"] * breathe(t, 0.2, 1.1) * v
        if t < F(66):
            # impact : écrasement 130 % x 77 % qui revient au rond sur un ressort amorti
            u = prog(t, F(58), F(66))
            sq = 1 + 0.3 * math.exp(-4 * u) * math.cos(3 * math.pi * u)
            r = 70 + 10 * prog(t, F(58), F(62), "out_back_fort")
            L.append({"k": "fill", "id": "point", "fill": ORANGE, "d": ellipse_d(CX, AXIS, r * sq, r / sq)})
        else:
            col = mix_hex(ORANGE, WHITE, prog(t, F(76), F(84)))
            c1, c2 = (CX - spread, AXIS, r), (CX + spread, AXIS, r)
            if u < 0.55:
                d = bridge_d(c1, c2, waist_h(c1, c2, 0.4 * (1 - u)))
            elif u < 0.8:
                d = bridge_d(c1, c2, r * 0.22 * (0.8 - u) / 0.25 + 1)
            else:
                d = circle_d(*c1) + circle_d(*c2)
            L.append({"k": "fill", "id": "points-logo", "fill": col, "d": d,
                      "pts": [(CX - spread, AXIS), (CX + spread, AXIS)]})
    return L


def outro_full(t):
    """Outro = formes du lien + carton logo (les points amenés par l'animation suivent la poussée)."""
    L = outro(t)
    dots = [x for x in L if x.get("id") == "points-logo"]
    rest = [x for x in L if x.get("id") != "points-logo"]
    return rest + endcard(t, F(76), dots=False, extra=dots)


def a_entree(t):
    return arrow(40, 300, 260, 300) + arrow(W - 40, 300, W - 260, 300)


def a_aspiration(t):
    return "".join(arrow(CX + dx * 820, AXIS + dy * 440, CX + dx * 360, AXIS + dy * 200)
                   for dx in (-1, 1) for dy in (-1, 1))


OUTRO = Anim("OUTRO", 4.0, outro_full, [
    Beat(F(8), "Fin du plan : la caméra recule (dézoom 125 % -> 100 %), le mouvement du film se prolonge.", "out_cubic"),
    Beat(F(20), "Les deux bulles du dégradé rentrent par les bords et dépassent de 6 % avant de se caler : la vidéo est pincée en lien.", "out_back", ann=a_entree),
    Beat(F(33), "Le lien redevient orange : éclosion depuis le centre en 12 images, la vidéo disparaît derrière.", "out_expo"),
    Beat(F(54), "Aspiration : les bulles serrent le lien (tension), puis l'orange se rétracte vers le centre en accélérant.", "anticipe", ann=a_aspiration),
    Beat(F(60), "Impact : le point arrive écrasé (130 % x 77 %) puis revient au rond sur un ressort amorti (2 oscillations).", "ressort_vif"),
    Beat(F(71), "Charte 3.4-02 : le point se divise. Cacahuète, col qui s'affine, rupture nette.", "out_cubic"),
    Beat(F(82), "Les deux bulles filent vers les positions des points du logo en virant au blanc ; « sfeer » s'ouvre depuis le centre (14 images).", "emphase"),
    Beat(F(98), "Tenue vivante : points qui respirent (±20 %), poussée lente de 7,5 %/s ; l'arabe s'est révélé de droite à gauche, l'endossement est posé en bas.", "emphase"),
])

NOTES = [
    ("Pourquoi ça marche", [
        "C'est ton idée telle quelle : le col entre deux bulles, l'espace qui relie, devient la fenêtre. C'est le sens de SFEER (« a new world of connections ») dit par la forme.",
        "Même grammaire que l'affiche 4.4 de la charte, où le portrait est posé dans l'orange entre deux bulles lavande.",
        "Fonctionne avec n'importe quelle vidéo : le lien est un cache, rien ne dépend du contenu.",
    ]),
    ("Charte et corrections", [
        "Correction de ton croquis : l'orange ne monte plus depuis le bas (vertical interdit), il explose depuis le centre, et la poussée finale se fait en zoom diagonal.",
        "Bulles sur l'axe horizontal, coupées à leur milieu vertical par les bords (règle 2.48).",
        "Bulles = trous qui montrent le dégradé : à la fin, le monde SFEER réapparaît sans fondu.",
    ]),
    ("Mouvement", [
        "Aucune image fixe : pop, inspiration, explosion, morsure, tension, éclosion, plongée.",
        "Asymétrie : 2 à 3 images d'écart entre gauche et droite pour casser la symétrie de la charte.",
        "AE : calques de forme, cache alpha inversé pour les bulles, zoom via un nul parent. Compatible Lottie.",
    ]),
]
