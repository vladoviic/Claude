# API de `sfeer_svg.py`

Toutes les coordonnées sont celles d'une image 1920 × 1080. L'axe horizontal de la charte est `AXIS = 540`.
Les fonctions renvoient des chaînes SVG que l'on concatène.

## Couleurs
`INDIGO #240852`, `ORANGE #FF6720`, `LAVENDER #817EFF`, `WHITE`, `MID` (milieu du dégradé),
teintes `ORANGE_T[80|60|40|20]`, `INDIGO_T[...]`, `LAV_T[...]`.
Le dictionnaire `SET` regroupe les nuances des décors orange du film (`light`, `base`, `mid`, `dark`, `deep`, `glow`, `sky`).
`COSTUME` donne le bleu-violet des costumes.

## Fonds
- `bg("gradient" | "indigo" | "orange" | "lavender" | "white")` : rectangle plein cadre. Le dégradé principal (`url(#sfeerGrad)`) est déclaré automatiquement par `frame_svg` et `Board`.

## Bulles (forme de la charte : deux cercles et un col concave tangent)
- `circle_d(cx, cy, r)` : tracé d'un cercle.
- `bridge_d((cx1, cy, r1), (cx2, cy, r2), h)` : deux bulles reliées par un col. `h` est la demi-épaisseur du col au plus fin. Un petit `h` donne un col fin, sur le point de rompre.
- `waist_h(c1, c2, t)` : calcule le `h` valide quand les deux cercles se chevauchent (pose « cacahuète »). `t = 0` donne la taille la plus marquée, `t = 1` une gélule.
- `chain_d([c1, c2, c3...], h | [h1, h2...])` : chaîne de bulles. Avec `h = None` pour un maillon, les bulles sont séparées.
- `drop_d(cx, cy, r, side="right" | "left", h=None, reach=0..1)` : grande bulle dont le col part hors cadre, comme le gabarit portrait de la charte.
- `edge_bubbles(r, fill=INDIGO, spread=0)` : deux bulles coupées à leur milieu vertical par les bords gauche et droit. L'espace entre elles est le « lien ». `spread` les repousse hors champ.
- `dots_field(pull=0..1, grow=1, fill=ORANGE, seed=..)` : champ de points (piste 2). `pull` les attire vers le centre.
- `shape(d, fill=ORANGE, sid="calque")` : remplit un tracé. `sid` devient l'id du calque, réutilisé dans After Effects.

## Fenêtre sur le film
- `film("s01" | "s02" | "s03" | "s05" | "s07" | "s12" | "s13", zoom=1.0, dx=0, dy=0)` : décor aplat d'une séquence du film, avec un zoom caméra autour du centre.
  - `s01` cabine
  - `s02` rue, couple
  - `s03` plongée sur la ville
  - `s05` cinéma
  - `s07` réservoir (fond violet, ouverture orange)
  - `s12` sphères
  - `s13` plateforme
- `window(d, contenu, "id-unique", ring=None, ring_w=0)` : découpe le contenu par le tracé `d`. Les ids doivent être uniques dans une image.
- `scaled(contenu, s, cx, cy, dx, dy)` : zoom générique.

## Logo et endossement (gabarits, à remplacer par les vectoriels officiels)
- `logo(x, y, size=1, color=WHITE, arabic=True, anchor="bl" | "c", dots=True, letters="sfeer" | "e", lid="logo")`. Les deux points sont des cercles (`{lid}-dot-g` et `{lid}-dot-d`). Avec `size = 1`, le mot latin mesure environ 230 px.
- `endorsement(x, y, size=1, color=WHITE, anchor="end" | "middle")` : « Powered by RIYADH AIR ».
- `lockup_end(color, margin=120, size=1)` : logo en bas à gauche et endossement opposé, en bas à droite.

## Personnages et accessoires
- `figure(x, pieds_y, hauteur, pose="stand" | "walk" | "sit", hijab=False, glasses=False, flip=False)`.
- `hand(x, y, s=1)` : main aplat, index levé. `(x, y)` correspond au bout de l'index.

## Annotations de storyboard (blanches par défaut, `color=` pour changer)
- `arrow(x1, y1, x2, y2, dash=False)`
- `curved_arrow(x1, y1, cx, cy, x2, y2)`
- `ghost(d)` : contour pointillé de l'état précédent
- `zoom_brackets(cx, cy, w, h)` : cadre caméra
- `label(x, y, "texte", size)`
- `axis_line()` : rappel de l'axe horizontal

## Sorties
- `frame_svg(inner, defs="", title="")` : image 1920 × 1080 autonome, à importer dans Illustrator ou After Effects.
- `Board(num, titre, logline, cols=4, thumb_w=600)`, puis :
  - `.section("INTRO · 4,0 s", [dict(inner=..., tc="0,0 – 0,6 s", cap="légende"), ...])`
  - `.note("Titre", ["ligne", ...])`
  - `.render()`, qui renvoie la planche complète en SVG.

## Rendu PNG (contrôle)
`node tools/render_png.mjs png/ storyboards/xx.svg --width=1600`
