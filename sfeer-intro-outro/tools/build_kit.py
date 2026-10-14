"""Kit de bulles : états clés des comportements de motion de la charte (3.3 à 3.5).

Chaque état est exporté en SVG 1920x1080 séparé (assets/keyframes/) pour servir de
poses clés dans After Effects (import en calques de forme), plus une planche récapitulative
(assets/kit_bulles.svg). Les aires sont conservées : un point de rayon R se divise en
deux bulles de rayon R/sqrt(2), en trois bulles de rayon R/sqrt(3).

Lancer depuis sfeer-intro-outro/ :  python3 tools/build_kit.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sfeer_svg import (AXIS, ORANGE, W, Board, bg, bridge_d, chain_d, circle_d,  # noqa: E402
                       frame_svg, logo, shape, waist_h)

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
KEY = os.path.join(OUT, "keyframes")
os.makedirs(KEY, exist_ok=True)
CX = W / 2
R = 170


def _peanut(c1, c2, t=0.3):
    return bridge_d(c1, c2, waist_h(c1, c2, t))


def _peanut_chain(cs, t=0.3):
    return chain_d(cs, [waist_h(cs[i], cs[i + 1], t) for i in range(len(cs) - 1)])


def split_states():
    """3.3-01 : un point se divise en deux puis se rejoint."""
    r2 = R / math.sqrt(2)
    return [
        ("split_k1_point", circle_d(CX, AXIS, R)),
        ("split_k2_cacahuete", _peanut((CX - 0.62 * r2, AXIS, r2 * 1.06), (CX + 0.62 * r2, AXIS, r2 * 1.06))),
        ("split_k3_col", bridge_d((CX - 1.7 * r2, AXIS, r2), (CX + 1.7 * r2, AXIS, r2), r2 * 0.12)),
        ("split_k4_rupture", circle_d(CX - 2.2 * r2, AXIS, r2) + circle_d(CX + 2.2 * r2, AXIS, r2)),
    ]


def swap_states():
    """3.3-02 : deux bulles jointes de tailles différentes échangent leur taille."""
    big, small, d = 1.25 * R * 0.8, 0.5 * R * 0.8, 1.9 * R
    mid = math.sqrt((big ** 2 + small ** 2) / 2)
    return [
        ("swap_k1_grande_gauche", bridge_d((CX - d / 2, AXIS, big), (CX + d / 2, AXIS, small), 18)),
        ("swap_k2_egales", bridge_d((CX - d / 2, AXIS, mid), (CX + d / 2, AXIS, mid), 18)),
        ("swap_k3_grande_droite", bridge_d((CX - d / 2, AXIS, small), (CX + d / 2, AXIS, big), 18)),
    ]


def trio_states():
    """3.5-01 : un point se divise en trois sur l'axe horizontal."""
    r3 = R / math.sqrt(3)
    return [
        ("trio_k1_point", circle_d(CX, AXIS, R)),
        ("trio_k2_serre", _peanut_chain([(CX - 1.25 * r3, AXIS, r3 * 1.05), (CX, AXIS, r3 * 1.05), (CX + 1.25 * r3, AXIS, r3 * 1.05)])),
        ("trio_k3_chaine", chain_d([(CX - 2.6 * r3, AXIS, r3), (CX, AXIS, r3), (CX + 2.6 * r3, AXIS, r3)], [r3 * 0.16, r3 * 0.16])),
    ]


def main():
    groups = [
        ("3.3-01 · Division / réunion (aire conservée)", split_states()),
        ("3.3-02 · Échange de taille", swap_states()),
        ("3.5-01 · Division en trois", trio_states()),
    ]
    board = Board("KIT", "Kit de bulles · poses clés",
                  "États clés des comportements de motion de la charte, construits avec le col tangent "
                  "de la charte (deux cercles + arcs concaves). Un fichier SVG 1920x1080 par pose dans assets/keyframes/.")
    for name, states in groups:
        frames = []
        for fid, d in states:
            inner = bg() + shape(d, ORANGE, sid=fid)
            with open(os.path.join(KEY, f"{fid}.svg"), "w") as fh:
                fh.write(frame_svg(inner, title=fid))
            frames.append(dict(inner=inner, tc=fid.split("_", 1)[1].replace("_", " "), cap=""))
        board.section(name, frames)
    # le logo et ses points-bulles
    lg = bg() + logo(W / 2, AXIS, 2.2, anchor="c", lid="logo")
    with open(os.path.join(KEY, "logo_points_bulles.svg"), "w") as fh:
        fh.write(frame_svg(lg, title="logo : les deux points sont des cercles animables"))
    board.section("Logo · les deux points sont des bulles (gabarit)",
                  [dict(inner=lg, tc="logo-dot-g / logo-dot-d", cap="Gabarit : remplacer par le vectoriel officiel, garder les points en calques séparés.")])
    board.note("Règles de construction", [
        "Bulles toujours centrées sur l'axe horizontal (y = 540).",
        "Aire conservée à la division : r = R/√2 (deux), R/√3 (trois).",
        "Col = arcs de cercles tangents aux deux bulles ; épaisseur pilotée par un seul paramètre.",
    ])
    board.note("Usage motion", [
        "Importer chaque pose en calques de forme et interpoler le tracé (même nombre de sommets).",
        "Alternative souple : deux cercles + effet 'gooey' (flou + seuil), à éviter pour Lottie.",
    ])
    with open(os.path.join(OUT, "kit_bulles.svg"), "w") as fh:
        fh.write(board.render())
    print("kit ok")


if __name__ == "__main__":
    main()
