"""Contrôle « rien de statique », sans rendu vidéo.

Usage (depuis sfeer-intro-outro/) : python3 -I tools/check_motion.py <id_concept>

Calcule le SVG de chaque image (25 i/s) directement depuis concepts/<id>.py et compare
les images consécutives : une suite d'au moins 3 images identiques est signalée comme figée.
Aucune image n'est rendue (pas de Chromium, pas de ffmpeg).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motion  # noqa: E402
from build import load  # noqa: E402

RUN = 3


def check_anim(anim):
    prev, start, runs = None, None, []
    n = anim.n_frames
    for i in range(n + 1):
        cur = motion.render_layers(anim.frame(i / motion.FPS), uid="c") if i < n else None
        if cur is not None and cur == prev:
            start = i - 1 if start is None else start
        else:
            if start is not None and i - start >= RUN:
                runs.append((start, i - 1))
            start = None
        prev = cur
    return n, runs


def main(cid):
    mod = load(os.path.join(motion.ROOT, "concepts", f"{cid}.py"))
    ok = True
    for anim in (mod.INTRO, mod.OUTRO):
        n, runs = check_anim(anim)
        if runs:
            ok = False
            print(f"FIGÉ   {anim.name.lower()} : " + ", ".join(f"f{a:03d}-f{b:03d}" for a, b in runs))
        else:
            print(f"OK     {anim.name.lower()} : aucune suite de {RUN} images identiques ({n} images)")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) else 1)
