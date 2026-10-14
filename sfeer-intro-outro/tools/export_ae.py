"""Export d'un concept vers After Effects : écrit un script ExtendScript (.jsx) qui construit
les compositions, les calques nommés et toutes les clés d'animation dans le projet ouvert.

Usage (depuis sfeer-intro-outro/) :
  python3 -I tools/export_ae.py concepts/p07_la_goutte.py [--fps 50]
Dans After Effects : Fichier > Scripts > Exécuter le fichier de script… > after-effects/<id>.jsx

Ce qui est créé dans le projet (dossier « SFEER · <titre> ») :
- <NOM>_INTRO et <NOM>_OUTRO (1920x1080), avec un repère de composition à chaque temps fort ;
- <NOM>_MONTAGE : intro, 2 s de vidéo, outro, bout à bout ;
- VIDÉO · placeholder : précompo verte à remplacer par le film (Alt-glisser sur le calque).
Calques : fond dégradé (Dégradé = effet Ramp), formes orange (calques de forme, un tracé par
sous-forme), cache de la fenêtre (cache alpha de la vidéo), points et textes du logo.
Les tracés sont clés image par image (géométrie exacte de l'animatique) ; l'interpolation passe
en « maintien » seulement quand le nombre de sommets change.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import load  # noqa: E402

W, H, CX, CY = 1920, 1080, 960, 540

# --- Tracés SVG -> sommets de Bézier (format Shape d'After Effects) ------------------
_TOK = re.compile(r"[MmLlHhVvAaZz]|-?\d*\.?\d+(?:e-?\d+)?")


def _arc_to_beziers(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """Arc SVG (paramétrage aux extrémités) -> liste de cubiques [(c1, c2, p2)]."""
    if rx == 0 or ry == 0:
        return [((x1, y1), (x2, y2), (x2, y2))]
    rx, ry = abs(rx), abs(ry)
    cp, sp = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1p ** 2) / rx ** 2 + (y1p ** 2) / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if fa == fs:
        co = -co
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2) - 1e-9)))
    d = dt / n
    k = 4 / 3 * math.tan(d / 4)
    out = []

    def pt(t):
        x, y = rx * math.cos(t), ry * math.sin(t)
        return cx + cp * x - sp * y, cy + sp * x + cp * y

    def dv(t):
        x, y = -rx * math.sin(t), ry * math.cos(t)
        return cp * x - sp * y, sp * x + cp * y
    for i in range(n):
        a0, a1 = t1 + i * d, t1 + (i + 1) * d
        p0, p1 = pt(a0), pt(a1)
        d0, d1 = dv(a0), dv(a1)
        out.append(((p0[0] + k * d0[0], p0[1] + k * d0[1]), (p1[0] - k * d1[0], p1[1] - k * d1[1]), p1))
    return out


def svg_path_to_shapes(d, tf=None):
    """d -> liste de sous-tracés fermés {v, i, o} (sommets absolus, tangentes relatives)."""
    toks = _TOK.findall(d)
    shapes, cur, pos, start, cmd, i = [], None, (0.0, 0.0), (0.0, 0.0), None, 0

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    def new(p):
        return {"v": [p], "i": [(0.0, 0.0)], "o": [(0.0, 0.0)]}

    def line(p):
        cur["v"].append(p)
        cur["i"].append((0.0, 0.0))
        cur["o"].append((0.0, 0.0))

    def close():
        if cur and len(cur["v"]) > 1:
            a, b = cur["v"][0], cur["v"][-1]
            if abs(a[0] - b[0]) < 1e-3 and abs(a[1] - b[1]) < 1e-3:   # dernier = premier : fusion
                cur["i"][0] = cur["i"][-1]
                cur["v"].pop(); cur["i"].pop(); cur["o"].pop()
            shapes.append(cur)

    while i < len(toks):
        t = toks[i]
        if re.match(r"[A-Za-z]", t):
            cmd = t
            i += 1
            if cmd in "Zz":
                close()
                cur = None
                pos = start
                continue
        else:
            if cmd is None:
                break
            if cmd == "M":
                cmd = "L"
            elif cmd == "m":
                cmd = "l"
        if cmd in "Mm":
            x, y = num(), num()
            if cmd == "m":
                x, y = pos[0] + x, pos[1] + y
            if cur:
                close()
            pos = start = (x, y)
            cur = new(pos)
        elif cmd in "Ll":
            x, y = num(), num()
            if cmd == "l":
                x, y = pos[0] + x, pos[1] + y
            pos = (x, y)
            line(pos)
        elif cmd in "Hh":
            x = num()
            pos = (x if cmd == "H" else pos[0] + x, pos[1])
            line(pos)
        elif cmd in "Vv":
            y = num()
            pos = (pos[0], y if cmd == "V" else pos[1] + y)
            line(pos)
        elif cmd in "Aa":
            rx, ry, phi, fa, fs, x, y = num(), num(), num(), num(), num(), num(), num()
            if cmd == "a":
                x, y = pos[0] + x, pos[1] + y
            for c1, c2, p2 in _arc_to_beziers(pos[0], pos[1], rx, ry, phi, int(fa), int(fs), x, y):
                cur["o"][-1] = (c1[0] - cur["v"][-1][0], c1[1] - cur["v"][-1][1])
                cur["v"].append(p2)
                cur["i"].append((c2[0] - p2[0], c2[1] - p2[1]))
                cur["o"].append((0.0, 0.0))
            pos = (x, y)
        else:
            i += 1
    if cur:
        close()
    if tf:
        shapes = [transform_shape(s, tf) for s in shapes]
    return shapes


def transform_shape(s, tf):
    """tf = (s, tx, ty, rot_deg) : rotation puis échelle puis translation."""
    sc, tx, ty, rot = tf
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def P(p):
        return (tx + sc * (c * p[0] - sn * p[1]), ty + sc * (sn * p[0] + c * p[1]))

    def V(p):
        return (sc * (c * p[0] - sn * p[1]), sc * (sn * p[0] + c * p[1]))
    return {"v": [P(p) for p in s["v"]], "i": [V(p) for p in s["i"]], "o": [V(p) for p in s["o"]]}


def circle_shape(cx, cy, r):
    return svg_path_to_shapes(f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z")[0]


def rect_shape(x, y, w, h):
    return {"v": [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], "i": [(0, 0)] * 4, "o": [(0, 0)] * 4}


def hexrgb(h):
    h = h.lstrip("#")
    return [round(int(h[k:k + 2], 16) / 255, 4) for k in (0, 2, 4)]


# --- Lecture d'une image du moteur -> état par piste ------------------------------
SCALE_RE = re.compile(r"scale\(([-\d.]+)\)")


def frame_state(layers):
    """Pistes : fills par id, fenêtre (cache + zoom), textes (cache rect), échelle du carton."""
    st = {"fills": {}, "win": None, "zoom": None, "texts": {}, "card": 1.0}

    def add_fill(L, sc=1.0):
        d = L.get("d")
        if not d or L.get("fill") in (None, "none"):
            return
        tf = (sc, CX - sc * CX, CY - sc * CY, 0) if sc != 1.0 else None
        key = L.get("id") or "forme"
        prev = st["fills"].get(key)
        shapes = svg_path_to_shapes(d, tf)
        if prev:
            prev["shapes"] += shapes
        else:
            st["fills"][key] = {"shapes": shapes, "color": L["fill"]}

    def raw(svg, sc=1.0):
        m = re.search(r'<clipPath id="fenetre-c"><path d="([^"]+)"', svg)
        if m:
            win = svg_path_to_shapes(m.group(1))
            ci = re.search(r'<clipPath id="fenetre-i"><circle cx="([-\d.]+)" cy="([-\d.]+)" r="([-\d.]+)"', svg)
            iris = circle_shape(*map(float, ci.groups())) if ci else circle_shape(CX, CY, 6000)
            z = SCALE_RE.search(svg)
            st["win"] = (win, iris)
            st["zoom"] = float(z.group(1)) if z else 1.0
            return
        for key in ("mot", "ar", "endo"):
            m = re.search(rf'<clipPath id="{key}"><rect x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', svg)
            if m:
                st["texts"][key] = [float(v) for v in m.groups()]
                return
        for pm in re.finditer(r'<path(?: transform="translate\(([-\d.]+) ([-\d.]+)\) rotate\(([-\d.]+)\)")? d="([^"]+)" fill="(#[0-9A-Fa-f]{6})"', svg):
            tx, ty, rot, d, col = pm.groups()
            tf = (1.0, float(tx), float(ty), float(rot)) if tx else None
            shapes = svg_path_to_shapes(d, tf)
            prev = st["fills"].get("forme")
            if prev:
                prev["shapes"] += shapes
            else:
                st["fills"]["forme"] = {"shapes": shapes, "color": col}

    for L in layers:
        k = L["k"]
        if k == "fill":
            add_fill(L)
        elif k == "video":
            if L.get("d"):
                st["win"] = (svg_path_to_shapes(L["d"]), circle_shape(CX, CY, 6000))
            else:
                st["win"] = ([rect_shape(-50, -50, W + 100, H + 100)], circle_shape(CX, CY, 6000))
            st["zoom"] = L.get("zoom", 1.0)
        elif k == "raw":
            raw(L["svg"])
        elif k == "group":
            sc = L.get("s", 1.0)
            st["card"] = sc
            for x in L["layers"]:
                if x["k"] == "fill":
                    add_fill(x, sc)
                elif x["k"] == "raw":
                    raw(x["svg"], sc)
    return st


# --- Assemblage des données d'une animation ---------------------------------------
NAMES = {
    "molecule": "Molécule · bulles orange",
    "goutte": "Goutte · bulle orange",
    "points-logo": "Logo · points",
    "forme": "Formes · orange",
}


def r1(v):
    return round(v, 1)


def pack_shape(s):
    return [[[r1(x), r1(y)] for x, y in s["v"]], [[r1(x), r1(y)] for x, y in s["i"]], [[r1(x), r1(y)] for x, y in s["o"]]]


def anim_data(anim, fps):
    n = int(round(anim.duration * fps))
    states = [frame_state(anim.frame(i / fps)) for i in range(n)]
    ids = []
    for s in states:
        for k in s["fills"]:
            if k not in ids:
                ids.append(k)
    fills = []
    for k in ids:
        slots = max(len(s["fills"][k]["shapes"]) if k in s["fills"] else 0 for s in states)
        frames = []
        for s in states:
            f = s["fills"].get(k)
            frames.append(None if not f else {"p": [pack_shape(x) for x in f["shapes"]], "c": hexrgb(f["color"])})
        fills.append({"name": NAMES.get(k, k), "slots": slots, "frames": frames})
    win_slots = max(len(s["win"][0]) if s["win"] else 0 for s in states)
    win = []
    for s in states:
        if s["win"]:
            win.append({"p": [pack_shape(x) for x in s["win"][0]], "iris": pack_shape(s["win"][1]), "z": round(s["zoom"] * 100, 2)})
        else:
            win.append(None)
    texts = {}
    for key in ("mot", "ar", "endo"):
        if any(key in s["texts"] for s in states):
            texts[key] = [[r1(v) for v in s["texts"][key]] if key in s["texts"] else None for s in states]
    card = [round(s["card"] * 100, 3) for s in states]
    beats = [{"t": round(b.t, 3), "c": b.cap} for b in anim.beats]
    return {"name": anim.name, "dur": anim.duration, "n": n, "fills": fills, "winSlots": win_slots,
            "win": win, "texts": texts, "card": card, "beats": beats}


JSX = r"""// SFEER · %(title)s — construit les compositions dans le projet After Effects ouvert.
// Généré par tools/export_ae.py (marble.studio). Fichier > Scripts > Exécuter le fichier de script…
// Compatible After Effects CC 2018 et plus récent. Aucune extension tierce requise.
(function () {
var DATA = %(data)s;
var FPS = %(fps)s;
var PREFIX = "%(prefix)s";
var IND = [36/255, 8/255, 82/255], LAV = [129/255, 126/255, 255/255], GREEN = [0, 177/255, 64/255], WHITE = [1, 1, 1];

function mkShape(p) {
    var s = new Shape();
    s.vertices = p[0]; s.inTangents = p[1]; s.outTangents = p[2]; s.closed = true;
    return s;
}
function emptyShape(x, y) { return mkShape([[[x, y]], [[0, 0]], [[0, 0]]]); }
function setKeys(prop, times, values) { if (times.length) { prop.setValuesAtTimes(times, values); } }
function holdAll(prop) {
    for (var k = 1; k <= prop.numKeys; k++) {
        prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
    }
}
// Clés de tracé : une clé par image ; maintien quand le nombre de sommets change.
function pathKeys(prop, frames, fx, fallback) {
    var times = [], vals = [], counts = [];
    for (var i = 0; i < frames.length; i++) {
        var p = fx(frames[i]);
        times.push(i / FPS);
        if (p) { vals.push(mkShape(p)); counts.push(p[0].length); }
        else { vals.push(emptyShape(fallback[0], fallback[1])); counts.push(1); }
    }
    setKeys(prop, times, vals);
    for (var k = 1; k < counts.length; k++) {
        if (counts[k] !== counts[k - 1]) {
            prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
        }
    }
}
// Clés « en escalier » : seulement aux changements, en maintien (opacité, couleur, cache texte).
function stepKeys(prop, values) {
    var times = [], vals = [], last = null;
    for (var i = 0; i < values.length; i++) {
        var v = values[i], key = v.toString();
        if (key !== last) { times.push(i / FPS); vals.push(v); last = key; }
    }
    setKeys(prop, times, vals);
    holdAll(prop);
}
function smoothKeys(prop, values) {
    var times = [], vals = [];
    for (var i = 0; i < values.length; i++) { times.push(i / FPS); vals.push(values[i]); }
    setKeys(prop, times, vals);
}
function zeroTransform(layer) {
    layer.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([0, 0]);
    layer.property("ADBE Transform Group").property("ADBE Position").setValue([0, 0]);
}

// Calque de forme : un groupe, N tracés (un par sous-forme), un remplissage.
function shapeLayer(comp, name, slots, frames, label) {
    var layer = comp.layers.addShape();
    layer.name = name;
    layer.label = label;
    zeroTransform(layer);
    var grp = layer.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
    grp.name = name;
    for (var s = 0; s < slots; s++) {
        grp.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Group").name = "Tracé " + (s + 1);
    }
    grp.property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill").name = "Remplissage";
    var vg = layer.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group");
    for (var t = 0; t < slots; t++) {
        (function (idx) {
            pathKeys(vg.property(idx + 1).property("ADBE Vector Shape"), frames,
                function (f) { return f && f.p[idx] ? f.p[idx] : null; }, [960, 540]);
        })(t);
    }
    var fill = vg.property("Remplissage").property("ADBE Vector Fill Color");
    var cols = [], ops = [], lastCol = [1, 0.4, 0.125];
    for (var i = 0; i < frames.length; i++) {
        if (frames[i]) { lastCol = frames[i].c; }
        cols.push(lastCol);
        ops.push(frames[i] ? 100 : 0);
    }
    stepKeys(fill, cols);
    stepKeys(layer.property("ADBE Transform Group").property("ADBE Opacity"), ops);
    return layer;
}

function background(comp) {
    var bg = comp.layers.addSolid(IND, "Fond · dégradé SFEER (indigo → lavande)", 1920, 1080, 1, comp.duration);
    var ramp = bg.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    ramp.name = "Dégradé de la charte";
    ramp.property("ADBE Ramp-0001").setValue([0, 540]);
    ramp.property("ADBE Ramp-0002").setValue(IND);
    ramp.property("ADBE Ramp-0003").setValue([1920, 540]);
    ramp.property("ADBE Ramp-0004").setValue(LAV);
    ramp.property("ADBE Ramp-0005").setValue(1);
    bg.locked = true;
    bg.label = 0;
    return bg;
}

function videoPlaceholder(folder) {
    var c = app.project.items.addComp("VIDÉO · placeholder (remplacer par le film)", 1920, 1080, 1, 30, FPS);
    c.parentFolder = folder;
    c.bgColor = GREEN;
    var s = c.layers.addSolid(GREEN, "Vert d'incrustation · remplacer", 1920, 1080, 1, 30);
    var t = c.layers.addText("VIDÉO");
    var tp = t.property("ADBE Text Properties").property("ADBE Text Document");
    var td = tp.value;
    td.fontSize = 72; td.fillColor = [0.23, 0.82, 0.44]; td.applyFill = true; td.applyStroke = false;
    td.justification = ParagraphJustification.CENTER_JUSTIFY; td.tracking = 200;
    tp.setValue(td);
    t.property("ADBE Transform Group").property("ADBE Position").setValue([960, 565]);
    t.name = "Repère · VIDÉO";
    return c;
}

function windowLayers(comp, d, placeholder) {
    var vid = comp.layers.add(placeholder);
    vid.name = "VIDÉO · film dans la fenêtre";
    vid.label = 9;
    var zs = [], ops = [], lastZ = 100;
    for (var i = 0; i < d.n; i++) {
        if (d.win[i]) { lastZ = d.win[i].z; }
        zs.push([lastZ, lastZ]);
        ops.push(d.win[i] ? 100 : 0);
    }
    smoothKeys(vid.property("ADBE Transform Group").property("ADBE Scale"), zs);
    stepKeys(vid.property("ADBE Transform Group").property("ADBE Opacity"), ops);

    var m = comp.layers.addShape();
    m.name = "Cache · fenêtre (goutte ∩ iris)";
    m.label = 2;
    zeroTransform(m);
    var root = m.property("ADBE Root Vectors Group");
    var g1 = root.addProperty("ADBE Vector Group"); g1.name = "Forme de la fenêtre";
    for (var s = 0; s < d.winSlots; s++) {
        g1.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Group").name = "Tracé " + (s + 1);
    }
    g1.property("ADBE Vectors Group").addProperty("ADBE Vector Filter - Merge").name = "Union";
    var g2 = m.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group"); g2.name = "Iris d'ouverture";
    g2.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Group").name = "Iris";
    var mg = m.property("ADBE Root Vectors Group").addProperty("ADBE Vector Filter - Merge"); mg.name = "Intersection";
    m.property("ADBE Root Vectors Group").addProperty("ADBE Vector Graphic - Fill").name = "Remplissage";
    root = m.property("ADBE Root Vectors Group");
    root.property("Intersection").property("ADBE Vector Merge Type").setValue(4);
    root.property("Forme de la fenêtre").property("ADBE Vectors Group").property("Union").property("ADBE Vector Merge Type").setValue(2);
    root.property("Remplissage").property("ADBE Vector Fill Color").setValue(WHITE);
    var vg = root.property("Forme de la fenêtre").property("ADBE Vectors Group");
    for (var t = 0; t < d.winSlots; t++) {
        (function (idx) {
            pathKeys(vg.property(idx + 1).property("ADBE Vector Shape"), d.win,
                function (f) { return f && f.p[idx] ? f.p[idx] : null; }, [960, 540]);
        })(t);
    }
    pathKeys(root.property("Iris d'ouverture").property("ADBE Vectors Group").property(1).property("ADBE Vector Shape"),
        d.win, function (f) { return f ? f.iris : null; }, [960, 540]);
    m.moveBefore(vid);
    if (typeof vid.setTrackMatte === "function") { vid.setTrackMatte(m, TrackMatteType.ALPHA); }
    else { vid.trackMatteType = TrackMatteType.ALPHA; }
    m.enabled = false;
    return vid;
}

// Textes du logo (gabarit Inter : remplacer par le vectoriel officiel), révélés par un masque.
function textLayer(comp, parent, txt, size, track, x, y, rects, name) {
    var t = comp.layers.addText(txt);
    t.name = name;
    t.label = 1;
    var tp = t.property("ADBE Text Properties").property("ADBE Text Document");
    var td = tp.value;
    td.fontSize = size; td.fillColor = WHITE; td.applyFill = true; td.applyStroke = false;
    td.justification = ParagraphJustification.CENTER_JUSTIFY; td.tracking = track;
    try { td.font = "Inter-Regular"; } catch (e) {}
    tp.setValue(td);
    if (parent) { t.parent = parent; t.property("ADBE Transform Group").property("ADBE Position").setValue([x - 960, y - 540]); }
    else { t.property("ADBE Transform Group").property("ADBE Position").setValue([x, y]); }
    var mask = t.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    mask.name = "Révélation";
    var shapes = [], ops = [];
    for (var i = 0; i < rects.length; i++) {
        var r = rects[i];
        if (r) {
            var x0 = r[0] - x, y0 = r[1] - y;
            shapes.push(mkShape([[[x0, y0], [x0 + r[2], y0], [x0 + r[2], y0 + r[3]], [x0, y0 + r[3]]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]]));
        } else {
            shapes.push(mkShape([[[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]]]));
        }
        ops.push(r ? 100 : 0);
    }
    var times = [];
    for (var j = 0; j < shapes.length; j++) { times.push(j / FPS); }
    setKeys(t.property("ADBE Mask Parade").property(1).property("ADBE Mask Shape"), times, shapes);
    stepKeys(t.property("ADBE Transform Group").property("ADBE Opacity"), ops);
    return t;
}

function buildComp(d, folder, placeholder) {
    var comp = app.project.items.addComp(PREFIX + "_" + d.name, 1920, 1080, 1, d.dur, FPS);
    comp.parentFolder = folder;
    comp.bgColor = IND;
    background(comp);
    // formes (dessous -> dessus dans l'ordre du moteur)
    var made = [];
    for (var f = 0; f < d.fills.length; f++) {
        if (d.fills[f].name.indexOf("Logo") === 0) { continue; }
        made.push(shapeLayer(comp, d.fills[f].name, d.fills[f].slots, d.fills[f].frames, 11));
    }
    var hasWin = false;
    for (var w = 0; w < d.win.length; w++) { if (d.win[w]) { hasWin = true; break; } }
    if (hasWin) { windowLayers(comp, d, placeholder); }
    // carton logo
    var hasText = false;
    for (var k in d.texts) { if (d.texts.hasOwnProperty(k)) { hasText = true; } }
    var nul = null;
    if (hasText) {
        nul = comp.layers.addNull();
        nul.name = "Carton · poussée lente (échelle)";
        nul.property("ADBE Transform Group").property("ADBE Anchor Point").setValue([0, 0]);
        nul.property("ADBE Transform Group").property("ADBE Position").setValue([960, 540]);
        var sc = [];
        for (var i = 0; i < d.card.length; i++) { sc.push([d.card[i], d.card[i]]); }
        smoothKeys(nul.property("ADBE Transform Group").property("ADBE Scale"), sc);
        if (d.texts.endo) { textLayer(comp, null, "Powered by RIYADH AIR", 37.7, 40, 960, 982, d.texts.endo, "Logo · Powered by RIYADH AIR"); }
        if (d.texts.ar) { textLayer(comp, nul, "سفيـــــر", 110, 0, 875.4, 691, d.texts.ar, "Logo · سفير (arabe)"); }
        if (d.texts.mot) { textLayer(comp, nul, "sfeer", 128, 160, 960, 573.3, d.texts.mot, "Logo · sfeer"); }
    }
    for (var p = 0; p < d.fills.length; p++) {
        if (d.fills[p].name.indexOf("Logo") === 0) {
            var pl = shapeLayer(comp, d.fills[p].name, d.fills[p].slots, d.fills[p].frames, 1);
            pl.moveToBeginning();
        }
    }
    for (var b = 0; b < d.beats.length; b++) {
        comp.markerProperty.setValueAtTime(d.beats[b].t, new MarkerValue(d.beats[b].c));
    }
    return comp;
}

app.beginUndoGroup("SFEER · " + PREFIX);
if (!app.project) { app.newProject(); }
var folder = app.project.items.addFolder("SFEER · %(title)s");
var sub = app.project.items.addFolder("Précompos"); sub.parentFolder = folder;
var placeholder = videoPlaceholder(sub);
var intro = buildComp(DATA[0], folder, placeholder);
var outro = buildComp(DATA[1], folder, placeholder);
var gap = 2;
var montage = app.project.items.addComp(PREFIX + "_MONTAGE (intro + film + outro)", 1920, 1080, 1, intro.duration + gap + outro.duration, FPS);
montage.parentFolder = folder;
var lo = montage.layers.add(outro); lo.startTime = intro.duration + gap; lo.name = "OUTRO";
var lv = montage.layers.add(placeholder); lv.startTime = intro.duration; lv.outPoint = intro.duration + gap; lv.name = "FILM · placeholder";
var li = montage.layers.add(intro); li.startTime = 0; li.name = "INTRO";
intro.openInViewer();
app.endUndoGroup();
alert("SFEER · %(title)s\n\nCréé dans le dossier « SFEER · %(title)s » :\n• " + intro.name + "\n• " + outro.name + "\n• " + montage.name + "\n\nRemplace la précompo « VIDÉO · placeholder » par le film (Alt-glisser).");
})();
"""


def main(argv):
    path = [a for a in argv if a.endswith(".py")][0]
    fps = int(argv[argv.index("--fps") + 1]) if "--fps" in argv else 50
    mod = load(path)
    m = mod.META
    prefix = "SFEER_" + re.sub(r"[^A-Za-z0-9]+", "_", m["title"].replace("é", "e").replace("è", "e")).strip("_")
    data = [anim_data(mod.INTRO, fps), anim_data(mod.OUTRO, fps)]
    js = JSX % {"data": json.dumps(data, ensure_ascii=False, separators=(",", ":")), "fps": fps,
                "prefix": prefix, "title": m["title"]}
    out_dir = os.path.join(os.path.dirname(HERE), "after-effects")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{m['id']}.jsx")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("﻿" + js)            # BOM : ExtendScript lit l'UTF-8 (accents, arabe)
    print(out, f"{os.path.getsize(out) / 1e6:.1f} Mo")


if __name__ == "__main__":
    main(sys.argv[1:])
