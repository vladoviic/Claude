"""Visuel d'ambiance « façon Cosmos » avec les bulles SFEER (aucun texte).

Formes de la charte dispersées autour d'un centre dégagé, légèrement inclinées, avec de la
profondeur (les lointaines plus petites et plus pâles). Certaines sont des fenêtres (vert = vidéo),
les autres orange. Une paire-fenêtre au centre. Deux fonds : clair (comme la réf.) et dégradé.

Lancer depuis sfeer-intro-outro/ : python3 -I tools/cosmos.py
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfeer_svg import (AXIS, H, INDIGO_T, LAV_T, ORANGE, ORANGE_T, W, bridge_d, chain_d, circle_d,  # noqa: E402
                       defs_gradient, f, waist_h)

GREEN, GREEN_D, GREEN_L = "#00B140", "#00953A", "#7FD9A0"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "visuels")


def shape_d(kind, r):
    """Formes de la charte centrées sur (0, 0)."""
    if kind == "rond":
        return circle_d(0, 0, r)
    if kind == "paire":
        return bridge_d((-1.63 * r, 0, r), (1.63 * r, 0, r), r * 0.12)
    if kind == "grande-petite":
        return bridge_d((-0.9 * r, 0, r), (1.45 * r, 0, r * 0.55), r * 0.08)
    if kind == "trio":
        rr = r * 0.72
        return chain_d([(-3.2 * rr, 0, rr), (0, 0, rr), (3.2 * rr, 0, rr)], rr * 0.12)
    c1, c2 = (-0.62 * r, 0, r), (0.62 * r, 0, r)                      # cacahuète
    return bridge_d(c1, c2, waist_h(c1, c2, 0.3))


def extent(kind, r):
    return {"rond": r, "paire": 2.7 * r, "grande-petite": 2.1 * r, "trio": 3.0 * r, "cacahuete": 1.7 * r}[kind]


def build(theme):
    rnd = random.Random(7)
    items = []
    tries = 0
    while len(items) < 46 and tries < 6000:
        tries += 1
        x, y = rnd.uniform(-60, W + 60), rnd.uniform(-60, H + 60)
        # centre dégagé (comme la zone du titre de la réf.)
        if ((x - W / 2) / 560) ** 2 + ((y - AXIS) / 300) ** 2 < 1:
            continue
        depth = rnd.random()                      # 0 = loin, 1 = près
        r = 18 + 46 * depth ** 1.3
        kind = rnd.choices(["rond", "paire", "grande-petite", "trio", "cacahuete"], [4, 3, 2, 1.5, 1.5])[0]
        e = extent(kind, r)
        if any(math.dist((x, y), (o["x"], o["y"])) < (e + o["e"]) * 0.9 + 14 for o in items):
            continue
        items.append({"x": x, "y": y, "r": r, "e": e, "kind": kind, "depth": depth,
                      "ang": rnd.uniform(-28, 28), "video": rnd.random() < 0.42})
    items.sort(key=lambda o: o["depth"])
    if theme == "clair":
        bg = '<rect width="1920" height="1080" fill="#F6F4F8"/>'
        far_o, far_v = ORANGE_T[40], GREEN_L
    else:
        bg = '<rect width="1920" height="1080" fill="url(#sfeerGrad)"/>'
        far_o, far_v = ORANGE_T[60], "#5BC983"
    defs = [defs_gradient(),
            f'<pattern id="vid" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="34" height="34" fill="{GREEN}"/><rect width="12" height="34" fill="{GREEN_D}"/></pattern>',
            f'<pattern id="vidloin" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="34" height="34" fill="{far_v}"/><rect width="12" height="34" fill="{GREEN}" opacity="0.35"/></pattern>']
    body = [bg]
    for o in items:
        far = o["depth"] < 0.35
        fill = ("url(#vidloin)" if far else "url(#vid)") if o["video"] else (far_o if far else ORANGE)
        body.append(f'<path transform="translate({f(o["x"])} {f(o["y"])}) rotate({f(o["ang"])})" '
                    f'd="{shape_d(o["kind"], o["r"])}" fill="{fill}"/>')
    # la paire-fenêtre héros au centre, sur l'axe
    body.append(f'<path d="{bridge_d((W / 2 - 250, AXIS, 165), (W / 2 + 250, AXIS, 165), 26)}" fill="url(#vid)"/>')
    body.append(f'<circle cx="{W / 2 + 470}" cy="{AXIS}" r="44" fill="{ORANGE}"/>')
    body.append(f'<circle cx="{W / 2 - 470}" cy="{AXIS}" r="26" fill="{ORANGE}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>')
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"cosmos_{theme}.svg")
    with open(path, "w") as fh:
        fh.write(svg)
    return path


if __name__ == "__main__":
    for th in ("clair", "degrade"):
        print(build(th))
