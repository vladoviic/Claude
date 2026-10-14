# Charte SFEER — analyse image par image des keyframes motion (3.1 → 3.6)

Sources : rendus PNG 2934×1650 des pages 3.1 à 3.6 de la charte (mo-68 à mo-73).
Les 35 vignettes ont été découpées puis mesurées au pixel en Python (numpy). Chaque vignette fait 331 px de côté et représente un cadre carré.
Unités : px vignette. Pour une sortie en 1080 px de haut, multiplier par 3,263.

## Méthode

1. Découpe automatique des vignettes par projection des pixels non blancs (5 colonnes × 2 rangées par page, 331×331 px).
2. Masque orange en alpha flottant : alpha = (R − R_fond)/(254 − R_fond). Le fond est estimé colonne par colonne, puisque le dégradé est horizontal. L'aire est la somme des alphas, à précision sous-pixel.
3. Étiquetage des taches (BFS, 4-connexité), puis boîte englobante et aire de chaque tache.
4. Les cercles sont repérés aux maxima du profil vertical h(x), puis ajustés par moindres carrés (méthode de Kåsa) sur les bords sous-pixel (seuil alpha 0,5). On obtient r, cx et cy à environ 0,1 px près.
5. Le col est le minimum de h(x) entre deux centres. Le congé est mesuré de deux façons : par ajustement d'un cercle sur le bord concave, et par inversion du modèle « congé constant » (voir ci-dessous).
6. Les héros 3.1 et 3.2 sont mesurés sur la page entière. Leur résolution est 7× plus haute, ils servent donc de référence.

Fichiers : `mesures.json` (toutes les valeurs) et les planches `00` à `08`. Chaque planche montre les keyframes avec un calque de mesure (cercles ajustés en blanc, disques de congé en turquoise, barre de col), les valeurs sous chaque image, trois mini-graphes et une proposition de timing à 25 i/s.

## 1. La géométrie exacte (planche 00)

| constante | vignettes | héros 3.1 / 3.2 |
|---|---|---|
| écart des centres en pose étirée, d/r | 3,27 | 3,30 |
| rayon du congé, R/r (constant) | 0,91 (0,86–0,92) | 0,934 |
| col en pose étirée, t/D | 7,0 % | 7,4 % |
| d de rupture, 2√(r²+2rR) | 3,36 r | 3,39 r |
| marge avant rupture | 2,7 % | 2,6 % |

- Le col n'est pas un metaball flou. C'est un congé circulaire de rayon constant : une fermeture morphologique. Le modèle reproduit les 98 cols mesurés sur les vignettes (R/r médian 0,91, plage 0,86–0,92) et les 3 cols des héros (0,934). Formule : t = 2·(√((r+R)² − d²/4) − R).
- R reste constant quand les rayons s'échangent de ±40 % (3.3-02, 3.6). Il dépend du rayon moyen, pas des rayons instantanés.
- Dans After Effects : Merge Paths (Add), puis Offset Paths +R (joint arrondi), puis Offset Paths −R. Il suffit ensuite d'animer d (ou r). Le col suit tout seul.
- Toutes les poses étirées de la charte sont à 3,27–3,30 r, soit à 2,6 % de la casse. La marque vit au bord de la rupture.
- Le col s'effondre à la fin du trajet. Entre d = 2,8 r et 3,27 r (les 15 derniers % du trajet), il passe de 39 % à 7 % de D.

## 2. Comportement par comportement

### 3.3-01 split & rejoin (identique au pixel à 3.4-01) — planche 01
- Les mesures : r = 50,7 px (D = 30,6 % du cadre), constant sur les 5 KF ; d/r = 0 → 1,88 → 3,27 → 1,88 → 0 ; col 100 → 75,5 → 7,0 → 75,5 → 100 % ; aire ×1,00 → 2,05 → 2,14 → 2,05 → 1,00.
- Ce que ça implique :
  - La masse n'est pas conservée : le point se duplique.
  - La charte est un ping-pong strict (KF4 = KF2 et KF5 = KF1, différence de pixels = 0).
  - Les centres restent à y = 164,5 px sur toutes les poses : aucun mouvement vertical.
- Ce qui manque : timing, easing, anticipation, overshoot, rupture et impact.
- Proposition (39 i) :
  - anticipation 3 i (sx 0,88) ;
  - KF1 → KF3 en 9 i en ease-out cubique (KF2 vers i4, KF3 vers i9), avec stretch 1,15 au lâcher ;
  - overshoot à 3,34 r à i11, rebond sur 5 i ;
  - tension 4 i (d ±0,6 %) ;
  - retour en ease-in cubique sur 8 i (KF4 vers i26, impact à i28) ;
  - ressort d'impact sur 10 i : sx 0,86 → 1,07 → 0,96 → 1.
  - Rendu image par image : planche 07 et `07-inbetweens-proposition.mp4`.

### 3.3-02 échange de taille — planche 02
- Les mesures :
  - Les centres sont fixes (86,5 et 241,3 px ; d = 154,8 = 3,27 r̄).
  - Les rayons valent 0,60 r̄ ↔ 1,40 r̄ (±40 %), avec r1 + r2 = 94,6 px à chaque KF.
  - L'aire tombe à ×0,88 au passage où les rayons sont égaux.
  - Le col passe de 4,5 % aux extrêmes à 6,9 % au passage.
  - La silhouette garde 248 px de long et glisse de ±19 px.
- Ce que ça implique : KF2 et KF4 (rayons égaux) sont des poses de passage à mi-temps, donc l'easing est en ease-in-out. KF5 = KF1 : la séquence boucle.
- Proposition (26 i par cycle) :
  - 4 + 4 i d'un extrême à l'autre, puis un dépassement à ±45 % ramené à ±40 % en 5 i ;
  - le « receveur » prend 1 i de retard ;
  - le gros cercle (1,40 r̄) est le meilleur candidat FENÊTRE.

### 3.4-02 point → ·e· → ·sfeer· → arabe — planche 03
- Les mesures :
  - Point blanc de D = 14,6 px (4,4 %). Après le split, écart de 32,3 px (2,2 D), sans col visible.
  - Les points rétrécissent à D = 5,5 px (×0,37) quand le « e » apparaît (23 px de haut).
  - L'écart passe ensuite de 41,6 à 172,2 px : les points chevauchent les bords du mot (176 px = 53 % de la largeur).
  - Les points remontent de 3 px : c'est le seul mouvement vertical de toute la charte.
  - L'arabe arrive en dernier, calé à gauche sous le « s ».
  - Le fond de cette page est un dégradé diagonal.
- Ce que ça implique : les points SONT la ponctuation du logo. Toute chaîne peut se résorber en 1 point, puis en ·sfeer· : c'est l'outro.
- Proposition (42 i) :
  - pop d'entrée 0 → 115 → 100 % en 6 i ;
  - split en ease-out expo sur 5 i ;
  - rétrécissement des points synchronisé avec le scale-in du « e » (6 i) ;
  - ouverture du mot en 8 i en ease-out expo, avec +4 % de dépassement ;
  - wipe de l'arabe de droite à gauche sur 8 i, à +4 i de décalage ;
  - respiration des points ±5 % sur l'image de fin.

### 3.5-01 split triple — planche 04
- Les mesures : r = 33,8 px, exactement 2/3 du rayon du duo. Les ratios sont les mêmes que pour le duo (1,88 r puis 3,27 r). Le cercle central reste fixe, l'envergure finale couvre 87 % de la largeur (marges de 6 %).
- Proposition (38 i) : même timing que le duo. En plus :
  - pincement du centre (sx 0,92) sur 3 i ;
  - satellites décalés de 1 i ;
  - en intro, ruptures décalées de 2 i pour un rythme « pop-pop ».

### 3.5-02 cascade — planche 05
- Les mesures :
  - Le point de gauche est une ancre (bord à x = 20 px).
  - KF2 : d = 2,43 r (74 % du trajet).
  - KF3 : d = 3,25 r.
  - KF4 : le 3e point naît à 2,04 r alors que la première paire est déjà posée. Les deux splits sont séquentiels.
  - Positions finales identiques à 3.5-01 KF3.
- Proposition : chevaucher les deux splits. Le 2e démarre quand la 1re paire atteint 74 %, soit 4 i de décalage : 16 i au total au lieu de 24. En plus :
  - recul de l'ancre de 3 % de D ;
  - pour l'outro, la même séquence en miroir, de droite à gauche.

### 3.6 pattern — planche 06
- Les mesures :
  - Grille fixe de 4 × 5 points : pas de 79,6 px (3,28 r0) en X et 60,7 px en Y ; D0 = 48,5 px (14,6 %).
  - Les rangées alternent en damier. Aucun centre ne bouge.
  - D gros + D petit = 2 D0 à chaque KF.
  - Amplitude du point (r1, c1) : 0 → −39,8 → +22,0 → −10,1 → −39,8 %.
- Ce que ça implique : KF2 → KF3 → KF4 est un ressort amorti mesuré, avec ×0,50 par demi-oscillation (ζ ≈ 0,21). KF5 = KF2 relance le mouvement. L'overshoot fait donc déjà partie de la charte.
- Proposition :
  - demi-période de 5 i (2,5 Hz) ; en expression AE : amp·sin(2π·2,5·t)/exp(3,5·t) ;
  - relance tous les 20–25 i ;
  - vague en décalant chaque colonne de 2 i, de gauche à droite.

## 3. Ce que la charte impose, et ce qui est compatible

Ce que la charte impose :
- Un seul axe horizontal. Pas de rotation, de flou, de fondu ni de mouvement vertical (sauf 3 px dans le logo).
- La géométrie : congé R ≈ 0,91–0,93 r et pose étirée à 3,27–3,30 r.
- Les poses symétriques (sauf la cascade) et le ping-pong.
- La règle d'échange r1 + r2 = constante, avec une amplitude de ±40 %.
- Des tailles quantifiées : D = 30,6 % (duo), 20,4 % (trio), 14,6 % (pattern), 4,4 → 1,65 % (points du logo).

Ce qui n'y figure pas mais reste compatible :
- anticipation ;
- overshoot sur d, plafonné à +2,7 % pour ne pas casser ;
- rupture volontaire en ease-in ;
- gouttelette satellite de D ≈ 0,3 r ;
- squash & stretch sur l'axe X (sx·sy = 1, stretch ≤ 1,15, squash ≥ 0,86) ;
- décalages de 1 à 2 i ;
- smear si un cercle parcourt plus de 0,5 D en une image ;
- iris vert dans un cercle (la fenêtre) puis zoom exponentiel 12^(x²) en 8 i (planche 08).

## Limites
- La charte ne donne aucune durée. Tous les timings ci-dessus sont des propositions, pas des mesures.
- L'aire mesurée inclut une légère erreur de bord. Les valeurs ×2,05 ou ×0,88 sont fiables à ±0,5 %.
- R/r vaut 0,91 sur les vignettes et 0,934 sur les héros. L'écart vient sans doute de l'échelle de rendu des vignettes (col de 7 px mesuré à ±0,3 px). Les valeurs des héros, plus résolus, font référence.
- 3.4-02 est blanc sur un dégradé diagonal. Les mesures y sont faites sur les taches blanches, sans modèle de col.
