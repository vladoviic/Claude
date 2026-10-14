"""Moteur d'animation des intros / outros SFEER.

Un concept est une fonction du temps `frame(t) -> [calques]`. À partir d'elle on produit :
- la planche de storyboard (images clés + pelure d'oignon + trajectoires + courbes d'easing),
- les SVG autonomes des images clés (import Illustrator / After Effects),
- l'animatique MP4 à 25 i/s (rendu Chromium + ffmpeg).

Calques (dict) :
  {"k": "bg", "v": "gradient"|"indigo"|"orange"|"green"|...}
  {"k": "fill", "d": path, "fill": couleur, "id": "nom", "ghost": True, "pts": [(x, y), ...]}
  {"k": "video", "d": path|None, "zoom": z, "id": "nom"}      -> plaque verte (None = plein cadre)
  {"k": "raw", "svg": "..."}                                   -> SVG libre (logo, texte...)
`pts` = points suivis (centres des bulles) pour dessiner les trajectoires sur la planche.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Callable

sys.path.insert(0, os.path.dirname(__file__))
from sfeer_svg import (H, W, Board, bg, defs_gradient, f, frame_svg)  # noqa: E402

FPS = 25
GREEN = "#00B140"      # vert d'incrustation
GREEN_D = "#00953A"
GREEN_L = "#3BD16F"


# --- Easing --------------------------------------------------------------------
def bezier(x1, y1, x2, y2):
    """cubic-bezier CSS / After Effects -> fonction t -> valeur."""
    def bx(s):
        return 3 * x1 * s * (1 - s) ** 2 + 3 * x2 * s * s * (1 - s) + s ** 3

    def by(s):
        return 3 * y1 * s * (1 - s) ** 2 + 3 * y2 * s * s * (1 - s) + s ** 3

    def dbx(s):
        return 3 * x1 * (1 - s) ** 2 + 6 * (x2 - x1) * s * (1 - s) + 3 * (1 - x2) * s * s

    def fn(t):
        if t <= 0:
            return 0.0
        if t >= 1:
            return 1.0
        s = t
        for _ in range(8):
            d = dbx(s)
            if abs(d) < 1e-6:
                break
            s -= (bx(s) - t) / d
            s = min(1, max(0, s))
        lo, hi = 0.0, 1.0
        for _ in range(30):  # sécurité : dichotomie
            if abs(bx(s) - t) < 1e-5:
                break
            if bx(s) < t:
                lo = s
            else:
                hi = s
            s = (lo + hi) / 2
        return by(s)
    fn.bez = (x1, y1, x2, y2)
    return fn


def back_out(s=1.70158):
    def fn(t):
        t -= 1
        return t * t * ((s + 1) * t + s) + 1
    return fn


def back_in(s=1.70158):
    def fn(t):
        return t * t * ((s + 1) * t - s)
    return fn


def spring(freq=2.2, damp=0.38):
    """Ressort amorti normalisé (0 -> 1 avec dépassement et rebonds). freq = oscillations sur la durée."""
    w = 2 * math.pi * freq

    def fn(t):
        if t >= 1:
            return 1.0
        return 1 - math.exp(-damp * w * t) * math.cos(w * math.sqrt(max(1 - damp * damp, 1e-6)) * t)
    return fn


EASE = {
    "linear": lambda t: t,
    "in_cubic": lambda t: t ** 3,
    "out_cubic": lambda t: 1 - (1 - t) ** 3,
    "inout_cubic": lambda t: 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2,
    "in_expo": lambda t: 0 if t <= 0 else 2 ** (10 * t - 10),
    "out_expo": lambda t: 1 if t >= 1 else 1 - 2 ** (-10 * t),
    "inout_expo": bezier(0.87, 0, 0.13, 1),
    "out_back": back_out(),
    "out_back_fort": back_out(2.6),
    "in_back": back_in(),
    "emphase": bezier(0.2, 0, 0, 1),          # Material « emphasized »
    "anticipe": bezier(0.6, -0.28, 0.735, 0.045),
    "plongee": bezier(0.7, 0, 0.15, 1),       # caméra qui accélère puis traverse
    "ressort": spring(2.2, 0.38),
    "ressort_mou": spring(1.4, 0.32),
    "ressort_vif": spring(3.0, 0.28),
}


def ease(name_or_fn):
    return EASE[name_or_fn] if isinstance(name_or_fn, str) else name_or_fn


def curve_points(name_or_fn, n=24):
    fn = ease(name_or_fn)
    pts = [(i / n, fn(i / n)) for i in range(n + 1)]
    lo = min(0, min(p[1] for p in pts))
    hi = max(1, max(p[1] for p in pts))
    return [(x, (y - lo) / (hi - lo)) for x, y in pts]


# --- Pistes de clés ------------------------------------------------------------
def _mix(a, b, u):
    if isinstance(a, (tuple, list)):
        return tuple(_mix(x, y, u) for x, y in zip(a, b))
    return a + (b - a) * u


class Track:
    """Pistes de clés : Track((0, 0), (0.4, 1, "out_back"), (1.2, 3, "plongee")).

    Chaque clé = (temps_s, valeur, easing_pour_arriver_à_cette_clé). Les temps peuvent
    aussi être donnés en images : F(12) = 12 / 25 s.
    """

    def __init__(self, *keys):
        self.keys = [(k[0], k[1], k[2] if len(k) > 2 else "inout_cubic") for k in keys]

    def __call__(self, t):
        ks = self.keys
        if t <= ks[0][0]:
            return ks[0][1]
        for (t0, v0, _), (t1, v1, e) in zip(ks, ks[1:]):
            if t <= t1:
                u = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                return _mix(v0, v1, ease(e)(u))
        return ks[-1][1]


def F(n):
    """Images -> secondes."""
    return n / FPS


def lerp(a, b, u):
    return a + (b - a) * u


def clamp01(u):
    return max(0.0, min(1.0, u))


def prog(t, t0, t1, e="linear"):
    """Progression 0..1 entre t0 et t1 avec easing."""
    return ease(e)(clamp01((t - t0) / (t1 - t0))) if t1 > t0 else float(t >= t1)


def breathe(t, amp=0.06, period=1.6, phase=0.0):
    """Respiration continue (tenues jamais figées)."""
    return 1 + amp * math.sin(2 * math.pi * (t / period + phase))


# --- Plaque vidéo verte ---------------------------------------------------------
def green_plate(zoom=1.0, uid="v", label=True) -> str:
    """Plaque verte d'incrustation : hachures + mire qui grandissent avec la poussée caméra."""
    z = max(zoom, 0.05)
    o = [f'<g id="{uid}-plaque">',
         f'<rect width="{W}" height="{H}" fill="{GREEN}"/>',
         f'<g transform="translate({W / 2} {H / 2}) scale({f(z)}) translate({-W / 2} {-H / 2})">']
    step = 90
    hatch = []
    for i in range(-14, 36):
        x = i * step
        hatch.append(f"M{x} -40L{x + 1200} {H + 40}")
    o.append(f'<path d="{" ".join(hatch)}" stroke="{GREEN_D}" stroke-width="16" fill="none"/>')
    o.append(f'<rect x="{W * .1}" y="{H * .1}" width="{W * .8}" height="{H * .8}" fill="none" stroke="{GREEN_L}" stroke-width="6" stroke-dasharray="30 20"/>')
    o.append(f'<path d="M{W / 2 - 60} {H / 2}H{W / 2 + 60}M{W / 2} {H / 2 - 60}V{H / 2 + 60}" stroke="{GREEN_L}" stroke-width="8"/>')
    o.append(f'<circle cx="{W / 2}" cy="{H / 2}" r="150" fill="none" stroke="{GREEN_L}" stroke-width="6"/>')
    if label:
        o.append(f'<text x="{W / 2}" y="{H / 2 + 250}" font-family="Inter, Arial, sans-serif" font-size="64" '
                 f'font-weight="700" fill="{GREEN_L}" text-anchor="middle" letter-spacing="12">VIDÉO</text>')
    o.append("</g></g>")
    return "".join(o)


# --- Rendu d'une image -------------------------------------------------------------
def render_layers(layers, uid="i") -> str:
    out = []
    n = 0
    for L in layers:
        k = L["k"]
        n += 1
        if k == "bg":
            v = L["v"]
            out.append(green_plate(L.get("zoom", 1.0), uid=f"{uid}{n}") if v == "green" else bg(v))
        elif k == "fill":
            idattr = f' id="{L["id"]}"' if L.get("id") else ""
            op = f' opacity="{f(L["opacity"])}"' if "opacity" in L else ""
            out.append(f'<path{idattr} d="{L["d"]}" fill="{L.get("fill", "#FF6720")}"{op}/>')
        elif k == "video":
            plate = green_plate(L.get("zoom", 1.0), uid=f"{uid}{n}", label=L.get("label", True))
            if L.get("d"):
                cid = f'{L.get("id", "fenetre")}-{uid}{n}'
                out.append(f'<clipPath id="{cid}"><path d="{L["d"]}"/></clipPath>'
                           f'<g id="{L.get("id", "fenetre")}" clip-path="url(#{cid})">{plate}</g>')
            else:
                out.append(plate)
        elif k == "raw":
            out.append(L["svg"])
        elif k == "group":
            # groupe transformé (caméra locale) : {"k": "group", "s": échelle, "cx", "cy", "dx", "dy", "layers": [...]}
            cx, cy = L.get("cx", W / 2), L.get("cy", H / 2)
            tr = (f'translate({f(cx + L.get("dx", 0))} {f(cy + L.get("dy", 0))}) scale({f(L.get("s", 1))}) '
                  f'translate({f(-cx)} {f(-cy)})')
            out.append(f'<g transform="{tr}">{render_layers(L["layers"], uid=f"{uid}g{n}")}</g>')
    return "".join(out)


# --- Animation ---------------------------------------------------------------------
@dataclass
class Beat:
    t: float                      # instant montré (s)
    cap: str                      # légende (FR, <= 150 caractères)
    ease: str | None = None       # courbe dominante du mouvement en cours
    ann: Callable[[float], str] | str | None = None   # annotations SVG (flèches...)
    onion: int = 3                # nombre de poses fantômes
    onion_dt: float = F(3)        # écart entre poses fantômes


@dataclass
class Anim:
    name: str                     # "INTRO" / "OUTRO"
    duration: float
    frame: Callable[[float], list]
    beats: list = field(default_factory=list)

    @property
    def n_frames(self):
        return int(round(self.duration * FPS))


def ghosts(anim: Anim, t: float, n=3, dt=F(3), color="#FFFFFF") -> str:
    """Pelure d'oignon : contours pointillés des formes aux instants précédents + trajectoires."""
    out = []
    for i in range(n, 0, -1):
        tt = t - i * dt
        if tt < 0:
            continue
        op = 0.25 + 0.5 * (n - i + 1) / (n + 1)
        for L in anim.frame(tt):
            if L["k"] in ("fill", "video") and L.get("d") and L.get("ghost", True):
                out.append(f'<path d="{L["d"]}" fill="none" stroke="{color}" stroke-width="5" '
                           f'stroke-dasharray="14 12" opacity="{f(op)}"/>')
    # trajectoires des points suivis
    trails = {}
    for i in range(0, 9):
        tt = t - i * dt / 1.5
        if tt < 0:
            break
        for L in anim.frame(tt):
            for j, p in enumerate(L.get("pts", []) or []):
                trails.setdefault((L.get("id", ""), j), []).append(p)
    for pts in trails.values():
        if len(pts) > 1 and math.dist(pts[0], pts[-1]) > 12:
            d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
            out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 16" opacity="0.9"/>')
            out.append(f'<circle cx="{f(pts[0][0])}" cy="{f(pts[0][1])}" r="9" fill="{color}"/>')
    return f'<g class="pelure">{"".join(out)}</g>'


def tc(t):
    n = int(round(t * FPS))
    return f"f{n:03d} · {t:.2f} s".replace(".", ",")


def beat_frames(anim: Anim):
    frames = []
    for b in anim.beats:
        inner = render_layers(anim.frame(b.t), uid=f"b{int(b.t * 1000)}")
        if b.onion:
            inner += ghosts(anim, b.t, b.onion, b.onion_dt)
        if b.ann:
            inner += b.ann(b.t) if callable(b.ann) else b.ann
        fr = dict(inner=inner, tc=tc(b.t), cap=b.cap)
        if b.ease:
            fr["curve"] = curve_points(b.ease)
            fr["curve_name"] = b.ease
        frames.append(fr)
    return frames


# --- Sorties ---------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def build(concept, out_root=ROOT, animatic=False, width=960):
    """concept : module avec META (dict), INTRO, OUTRO (Anim), NOTES (liste de (titre, [lignes]))."""
    m = concept.META
    cid = m["id"]
    board = Board(m.get("num", cid.upper()), m["title"], m["logline"], cols=m.get("cols", 4))
    for anim in (concept.INTRO, concept.OUTRO):
        board.section(f"{anim.name} · {anim.duration:.1f} s · {anim.n_frames} images à 25 i/s".replace(".", ","), beat_frames(anim))
    for head, lines in getattr(concept, "NOTES", []):
        board.note(head, lines)
    sb_dir = os.path.join(out_root, "storyboards")
    os.makedirs(sb_dir, exist_ok=True)
    sb_path = os.path.join(sb_dir, f"{cid}.svg")
    with open(sb_path, "w") as fh:
        fh.write(board.render())
    # images clés autonomes (sans annotations) pour After Effects / Illustrator
    kf_dir = os.path.join(out_root, "frames", cid)
    if os.path.isdir(kf_dir):
        shutil.rmtree(kf_dir)
    os.makedirs(kf_dir)
    for anim in (concept.INTRO, concept.OUTRO):
        for i, b in enumerate(anim.beats, 1):
            n = int(round(b.t * FPS))
            with open(os.path.join(kf_dir, f"{anim.name.lower()}_{i:02d}_f{n:03d}.svg"), "w") as fh:
                fh.write(frame_svg(render_layers(anim.frame(b.t), uid="k"), title=f"{m['title']} · {anim.name} · {tc(b.t)}"))
    outs = [sb_path]
    if animatic:
        outs += render_animatic(concept, out_root, width)
    return outs


def render_animatic(concept, out_root=ROOT, width=960):
    """Rend chaque image (25 i/s) puis assemble intro, outro et une version enchaînée en MP4."""
    cid = concept.META["id"]
    tmp = os.path.join("/tmp/claude-0/animatics", cid)
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    seqs = []
    for anim in (concept.INTRO, concept.OUTRO):
        d = os.path.join(tmp, anim.name.lower())
        os.makedirs(d)
        for i in range(anim.n_frames):
            t = i / FPS
            with open(os.path.join(d, f"{i:04d}.svg"), "w") as fh:
                fh.write(frame_svg(render_layers(anim.frame(t), uid="a")))
        seqs.append((anim.name.lower(), d))
    subprocess.run(["node", os.path.join(HERE, "render_seq.mjs"), str(width)] + [d for _, d in seqs], check=True)
    out_dir = os.path.join(out_root, "animatiques")
    os.makedirs(out_dir, exist_ok=True)
    outs = []
    for name, d in seqs:
        mp4 = os.path.join(out_dir, f"{cid}_{name}.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(d, "%04d.png"),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", mp4], check=True)
        outs.append(mp4)
    return outs
