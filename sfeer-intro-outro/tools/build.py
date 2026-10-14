"""Construit planche + images clés + animatiques pour un ou plusieurs concepts.

Usage (depuis sfeer-intro-outro/) :
  python3 tools/build.py concepts/p05_le_lien.py [autres.py ...] [--no-animatic] [--png]
"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motion  # noqa: E402


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    files = [a for a in argv if a.endswith(".py")]
    animatic = "--no-animatic" not in argv
    png = "--png" in argv
    for p in files:
        mod = load(p)
        outs = motion.build(mod, animatic=animatic)
        for o in outs:
            print(o)
        if png:
            subprocess.run(["node", os.path.join(HERE, "render_png.mjs"), os.path.join(motion.ROOT, "png"), outs[0], "--width=1800"], check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
