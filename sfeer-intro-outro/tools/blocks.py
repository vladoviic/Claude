"""Blocs réutilisables pour tous les concepts : carton logo animé, plaque vidéo, bulles-trous.

Chaque bloc renvoie une liste de calques (voir motion.py). Les temps sont en secondes.
"""
import math

from motion import F, Track, breathe, prog
from sfeer_svg import (AXIS, FONT, FONT_AR, W, WHITE, circle_d, endorsement, f, logo_geometry,
                       mix_hex)

CX = W / 2
GRAD = "url(#sfeerGradU)"     # remplir une bulle avec le dégradé du fond (bulle-trou)
LOGO_SIZE = 2.0
LG = logo_geometry(LOGO_SIZE)


def video(zoom=1.0, d=None, vid="fenetre", ghost=True, label=True):
    """Plaque verte (vidéo à venir). d=None : plein cadre ; sinon découpée par le tracé d."""
    return {"k": "video", "zoom": zoom, "d": d, "id": vid, "ghost": ghost, "label": label}


def word(reveal: float, size: float = LOGO_SIZE, color: str = WHITE, uid: str = "mot", mode: str = "centre"):
    """Mot latin « sfeer » révélé par un cache. mode 'centre' (s'ouvre depuis le centre),
    'gauche' (de gauche à droite). reveal 0..1 ; 1 = entier. Sans les points (dessinés à part)."""
    if reveal <= 0:
        return []
    g = logo_geometry(size)
    x, w = g["word_x"], g["word_w"]
    if mode == "centre":
        half = w / 2 * reveal + 4
        rx, rw = CX - half, 2 * half
    else:
        rx, rw = x - 4, (w + 8) * reveal
    return [{"k": "raw", "svg":
             f'<clipPath id="{uid}"><rect x="{f(rx)}" y="{f(AXIS - g["fs"])}" width="{f(rw)}" height="{f(g["fs"] * 1.4)}"/></clipPath>'
             f'<text clip-path="url(#{uid})" x="{f(x)}" y="{f(AXIS + g["fs"] * 0.26)}" font-family="{FONT}" '
             f'font-size="{f(g["fs"])}" letter-spacing="{f(g["fs"] * 0.16)}" fill="{color}" '
             f'textLength="{f(w)}" lengthAdjust="spacingAndGlyphs">sfeer</text>'}]


def arabic(reveal: float, size: float = LOGO_SIZE, color: str = WHITE, uid: str = "ar"):
    """« سفير » sous le mot latin, révélé de droite à gauche (sens de lecture arabe)."""
    if reveal <= 0:
        return []
    g = logo_geometry(size)
    xr = g["word_x"] + g["word_w"] * 0.62
    wa = g["word_w"] * 0.58
    return [{"k": "raw", "svg":
             f'<clipPath id="{uid}"><rect x="{f(xr - wa * reveal)}" y="{f(AXIS + g["fs"] * 0.3)}" width="{f(wa * reveal)}" height="{f(g["fs"] * 1.2)}"/></clipPath>'
             f'<text clip-path="url(#{uid})" x="{f(g["word_x"] + g["fs"] * 0.12)}" y="{f(AXIS + g["fs"] * 1.18)}" '
             f'font-family="{FONT_AR}" font-size="{f(g["fs"] * 0.86)}" fill="{color}" '
             f'textLength="{f(g["word_w"] * 0.56)}" lengthAdjust="spacing">سفيـــــر</text>'}]


def endorse(reveal: float, color: str = WHITE, uid: str = "endo", y: float = 982, size: float = 1.45):
    """« Powered by RIYADH AIR » centré en bas, révélé depuis le centre (jamais accolé au logo)."""
    if reveal <= 0:
        return []
    return [{"k": "raw", "svg":
             f'<clipPath id="{uid}"><rect x="{f(CX - 330 * reveal)}" y="{f(y - 52)}" width="{f(660 * reveal)}" height="70"/></clipPath>'
             f'<g clip-path="url(#{uid})">{endorsement(CX, y, size, color, "middle")}</g>'}]


def logo_dots(t, alive=True, color=WHITE, scale=1.0, spread=1.0):
    """Les deux points du logo à leur place, qui respirent (tenue jamais figée).
    spread < 1 les rapproche du centre (mot replié)."""
    out = []
    for i, key in enumerate(("dot_g", "dot_d")):
        x, y = LG[key]
        x = CX + (x - CX) * spread
        r = LG["dot_r"] * scale * (breathe(t, 0.2, 1.1, phase=0.25 * i) if alive else 1)
        out.append({"k": "fill", "id": f"logo-point-{'gd'[i]}", "fill": color, "d": circle_d(x, y, r), "ghost": False})
    return out


def endcard(t, t0, dots=True, word_mode="centre", extra=None):
    """Carton final standard (charte 3.4-02), à partir de t0 :
    mot qui s'ouvre (14 images, emphase), arabe de droite à gauche (+6 i.), endossement (+10 i.),
    points qui respirent, poussée lente continue. dots=False si le concept amène lui-même les
    points à leur place : passer alors ses calques dans `extra` pour qu'ils suivent la poussée."""
    if t < t0:
        return list(extra or [])
    L = list(extra or [])
    L += word(Track((t0, 0), (t0 + F(14), 1, "emphase"))(t), mode=word_mode)
    L += arabic(Track((t0 + F(6), 0), (t0 + F(18), 1, "emphase"))(t))
    if dots:
        L += logo_dots(t)
    out = [{"k": "group", "s": hold_drift(t, t0), "layers": L}]
    out += endorse(Track((t0 + F(10), 0), (t0 + F(20), 1, "emphase"))(t))
    return out


def hold_drift(t, t0, rate=0.075):
    """Poussée lente et continue sur le carton (≈ 7,5 %/s) : la tenue n'est jamais figée."""
    return 1 + rate * max(0.0, t - t0)


def drift(t, t0, rate=0.5):
    """Dérive linéaire à ajouter à une poussée caméra pour qu'elle ne s'arrête jamais."""
    return rate * max(0.0, t - t0)


def logo_full(t, alive=True):
    """Logo complet posé (début d'intro qui part du logo), points vivants."""
    return word(1) + arabic(1) + logo_dots(t, alive)


def dot_to_logo(t, t0, t1, start, r0, col0="#FF6720"):
    """Une bulle (start=(x, y), rayon r0) qui file vers... rien : utilitaire de trajectoire.
    Renvoie (x, y, r, couleur) à l'instant t pour aller vers le point gauche du logo."""
    u = prog(t, t0, t1, "emphase")
    x = start[0] + (LG["dot_g"][0] - start[0]) * u
    y = start[1] + (LG["dot_g"][1] - start[1]) * u
    r = r0 + (LG["dot_r"] - r0) * u
    return x, y, r, mix_hex(col0, WHITE, prog(t, t0 + (t1 - t0) * 0.4, t1))


def squash(t, t_hit, dur=F(8), amp=0.3):
    """Écrasement à l'impact puis retour au rond sur ressort amorti -> facteur sx (sy = 1/sx)."""
    u = prog(t, t_hit, t_hit + dur)
    if t < t_hit:
        return 1.0
    return 1 + amp * math.exp(-4 * u) * math.cos(3 * math.pi * u)
