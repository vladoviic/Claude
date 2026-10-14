"""Contrôle « rien de statique » d'une animatique + planches-contact.

Usage (depuis sfeer-intro-outro/) : python3 -I tools/check_motion.py <id_concept>

Pour chaque paire d'images consécutives, mesure la part de pixels qui changent de plus de
6 niveaux (sur 255). Une image est « figée » si moins de 0,02 % des pixels bougent
(soit environ 100 pixels en 960 x 540). Toute suite de 3 images figées ou plus est signalée.
Écrit aussi /tmp/claude-0/contact/<id>_<intro|outro>.png (une image sur deux, numérotée).
"""
import os
import subprocess
import sys

import numpy as np

W, H = 480, 270
SEUIL_NIVEAU = 6
SEUIL_PART = 0.0002
RUN = 3


def frames(mp4):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", mp4, "-vf", f"scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)


def check(mp4):
    fr = frames(mp4)
    parts = [(np.abs(fr[i + 1] - fr[i]) > SEUIL_NIVEAU).mean() for i in range(len(fr) - 1)]
    runs, start = [], None
    for i, p in enumerate(parts + [1.0]):
        if p < SEUIL_PART:
            start = i if start is None else start
        else:
            if start is not None and i - start >= RUN:
                runs.append((start, i))
            start = None
    return len(fr), parts, runs


def main(cid):
    os.makedirs("/tmp/claude-0/contact", exist_ok=True)
    ok = True
    for part in ("intro", "outro"):
        mp4 = f"animatiques/{cid}_{part}.mp4"
        if not os.path.exists(mp4):
            print("MANQUANT", mp4)
            ok = False
            continue
        n, parts, runs = check(mp4)
        if runs:
            ok = False
            txt = ", ".join(f"f{a:03d}-f{b:03d}" for a, b in runs)
            print(f"FIGÉ   {part} : {txt}")
        else:
            print(f"OK     {part} : aucune suite de {RUN} images figées ({n} images, mouvement min {min(parts) * 100:.3f} % des pixels)")
        rows = (n // 2 + 9) // 10
        out = f"/tmp/claude-0/contact/{cid}_{part}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf",
                        f"select='not(mod(n\\,2))',scale=288:-1,drawtext=text='f%{{eif\\:n*2\\:d}}':x=6:y=6:"
                        f"fontcolor=white:fontsize=16:box=1:boxcolor=black@0.55,tile=10x{rows}",
                        "-frames:v", "1", out], check=True)
        print(f"       planche-contact : {out}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) else 1)
