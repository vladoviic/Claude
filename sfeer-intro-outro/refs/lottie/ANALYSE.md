# Références Lottie (After Effects) analysées image par image

Clé : `lottie`. Objectif : tirer du motion pro (exporté d'After Effects en Lottie) des mesures exploitables pour les bumpers INTRO/OUTRO SFEER : bulles orange #FF6720 sur dégradé indigo #240852 vers lavande #817EFF, axe horizontal, une bulle devient FENÊTRE (vert chroma) et la caméra passe à travers. Consigne de la DA : « super motion, rien de statique ».

## Méthode

1. **Sources** : uniquement des paquets npm (`npm pack` dans un dossier de travail ; pinterest, vimeo, behance, dribbble et les autres sites de ce type sont bloqués). J'ai scanné 35 paquets pour trouver des JSON Lottie (clés `v`, `fr`, `layers`), y compris ceux qui sont intégrés dans du JS (react-useanimations v3, extrait dans un contexte `vm` isolé). Au total, environ 140 animations trouvées, 70 candidates passées en revue (planches d'aperçu), **8 références retenues** (10 animations).
2. **Rendu** : lottie-web **5.13.0** (npm), moteur `svg`, Chromium headless (Playwright), `anim.goToAndStop(frame, true)`. Les images fractionnaires sont interpolées par lottie-web, ce qui permet de rééchantillonner **exactement à 25 ips** des sources à 24, 30 ou 60 ips.
3. **Planches** : chaque vignette porte `#n` = numéro d'image **à 25 ips**, `src fX` = image source, plus une mesure.
4. **Mesures** :
   - **Courbes** : extraites du JSON. Les tangentes `o`/`i` de chaque clé donnent `cubic-bezier(o.x, o.y, i.x, i.y)`. Pour AE : influence de sortie = o.x × 100, influence d'entrée = (1 − i.x) × 100. Je calcule aussi le pic de vitesse (multiple de la vitesse moyenne) et le dépassement éventuel.
   - **Mouvement réel** : second rendu haute résolution à la cadence native (400 à 513 px), puis mesure au pixel (composantes connexes : centre, diamètre équivalent, L/H, surface couverte) et boîtes englobantes DOM des calques.

## Fichiers

| Fichier | Contenu |
|---|---|
| `0X_*_planche.png` | Planches-contact numérotées à 25 ips, avec annotations (moins de 2400 px de large) |
| `courbes/0X_*_courbes.png` | Courbes valeur et vitesse (graduations = images à 25 ips) |
| `keyframes/0X_*.txt` | Toutes les clés animées : durée en images src et @25, cubic-bezier, influence AE, pic de vitesse, dépassement |
| `mesures/*.csv` | Mesures image par image (pixel ou analytique) |
| `videos/*.mp4` | Aperçus rééchantillonnés à 25 ips (H.264) |

## Sources et licences (lues dans package.json)

| # | Animation | Paquet npm (version) | Licence |
|---|---|---|---|
| 01 | `test/animations/bacon.json` (flaque liquide) | lottie-web 5.13.0 | MIT |
| 02 | `cisco-ai-assistant/hello_32px.json` | @momentum-design/animations 0.4.3 | MIT (LICENSE.md, Momentum Design ; champ absent du package.json) |
| 03 | `cisco-ai-assistant/responding_32px_{start,loop,end}.json` | @momentum-design/animations 0.4.3 | MIT (idem) |
| 04 | `giftingZoom.json` | @coinbase/cds-lottie-files 3.3.4 | **non déclarée** dans package.json (dépôt coinbase/cds) : étude seulement, ne pas redistribuer |
| 05 | `tradeStatus.json` | @coinbase/cds-lottie-files 3.3.4 | non déclarée (idem) |
| 06 | `loading3` | react-useanimations 3.1.1 | MIT |
| 07a | `activityIndicator.json` | @coinbase/cds-lottie-files 3.3.4 | non déclarée (idem) |
| 07b | `moreHorizontal` | react-useanimations 3.1.1 | MIT |
| 07c | `src/loader.json` | react-native-animated-loader 1.0.0 | MIT |
| 08 | `webex_logo_loop.json` | @momentum-design/animations 0.4.3 | MIT |

Candidates écartées : useAnimations (icônes à trait), Mural brand-wordmark (rubans de logo), lottie-web starfish/monster/navidad, Coinbase nux/earnComplete, réactions Webex, etc. Elles sont moins proches du langage « bulles ».

---

## 01 · Bacon (lottie-web) : flaque liquide plein cadre, transition « wipe » organique

Planche `01_bacon_flaque_planche.png` · courbes `courbes/01_bacon_courbes.png` · CSV `mesures/01_bacon_couverture.csv`

Lecture image par image (@25) :

- **#01 à #06** : le personnage lance une goutte (accroche). La goutte occupe 2 % du cadre puis 9 % à l'éclaboussure (#06).
- **#07 à #13 : INONDATION**, de **24 % à 93 %** du cadre en **7 images @25** (8 images src). La première image arrive déjà à 24 % : pas de fondu ni d'ouverture progressive, on « coupe » sur une forme déjà grosse. La vitesse est d'environ **+12 à +15 points de surface par image @25**. Les clés de tracé sont espacées de 3, 2 puis 3 images src en interpolation quasi linéaire (0.167/0.833), donc une avancée constante et brutale.
- **#14 à #44** : la flaque est pleine, mais l'intérieur vit (beurre et bacon animés). La forme continue à dériver (clé 8 vers 49 en `cubic-bezier(0.167,0.167,0.667,1)`).
- **#44 à #50 : anticipation**. La flaque **gonfle de +3,5 %** (93 → 97 %) juste avant de se retirer.
- **#50 à #66 : VIDANGE** en **16 à 17 images @25**, environ −6 à −7 points par image : **deux fois plus lente que l'entrée**. Le bord supérieur ondule avec une amplitude d'environ **11 % de la hauteur** et révèle progressivement la scène dessous (le personnage réapparaît à #61).

Technique :

- Chaque nappe n'a que **4 sommets bézier** : une forme liquide crédible n'a pas besoin de plus.
- **Deux calques de jaune** (clair et foncé) partagent les clés d'entrée. Ils **divergent en sortie** : le clair passe par une clé intermédiaire (src 49 → 62 → 78), le foncé va directement de 49 à 78. Le décalage crée une lèvre bicolore, donc de l'épaisseur, sans aucun dégradé.

## 02 · Cisco AI « HELLO » : naissance d'un anneau et de son satellite

Planche `02_cisco_hello_planche.png` · `keyframes/02_cisco_hello.txt`

- **#01 à #13 (0,5 s)** : trois propriétés animées **simultanément** sur la même durée :
  - échelle 0 → 98 % : `cubic-bezier(0.57,0.555,0.5,1)`, départ instantané ;
  - rotation −90° → 0 : `(0.66,0,0.34,1)` ;
  - tracé (trim) 0 → 100 % : `(0.76,0,0.24,1)`, soit **76 % d'influence** des deux côtés.
- Résultat mesuré : échelle 27 % mais arc 5 % à #04 ; échelle 62 % et arc 42 % à #07 ; arc 86 % à #09. Le trait reste un « point » longtemps puis **se referme en 2 images @25**. Aucune paire d'images n'est identique.
- **Satellite** : il naît à l'image src 24, sa taille suit 5 clés non uniformes (0 → 60,5 → 76,9 → 83 → 98 %) et il fait **une orbite complète en 1 s** (`0.66,0,0.34,1`). Le mouvement secondaire continue après la pose de l'anneau.

## 03 · Cisco AI « RESPONDING » : anneau, puis 2 disques sur l'axe horizontal, puis anneau

Planche `03_cisco_responding_planche.png` · courbes `courbes/03_cisco_responding_courbes.png` · CSV `mesures/03_cisco_responding.csv`

C'est la référence la plus proche des bulles SFEER.

- **Start, #01 à #13 (0,5 s)**, sur la même courbe `cubic-bezier(0.66,0,0.34,1)` (influence 66/66) :
  - l'anneau tourne de 180° ;
  - son **épaisseur de trait passe de 5,5 à 21** : l'anneau devient un disque plein sans changer de forme ;
  - son échelle passe de 200 à 69 %.
  - Le satellite glisse sur l'axe horizontal et sa taille passe de 200 à 100 %.
  - Un null d'échelle fait une **respiration 100 → 90 → 100 %** (6,7 puis 5,8 images @25).
- **Séparation nette à l'image src 21, soit l'image 9 @25 (0,35 s)**.
- **Boucle, #14 à #38 (1 s)** :
  - les **centres sont fixes** (entraxe 46 % du cadre) ;
  - les deux disques **respirent en opposition** : diamètre gauche 24 → 44 → 24 %, diamètre droit 45 → 23 → 45 % du cadre ;
  - **la somme des diamètres reste quasi constante (64 à 69 %, moyenne 67 %)** : l'un se nourrit de l'autre ;
  - l'écart bord à bord reste entre 11,6 et 14,1 % ;
  - courbe `cubic-bezier(0.48,0.04,0.52,0.96)` (quasi sinus), **12,5 images @25 par demi-cycle**.
- **End, #39 à #50** : exactement le start à l'envers (mêmes durées et mêmes courbes).

## 04 · Coinbase giftingZoom : la caméra traverse le trou du logo (= la bulle-fenêtre)

Planche `04_coinbase_zoom_planche.png` · courbes `courbes/04_coinbase_zoom_courbes.png`

- Une seule clé d'échelle : **100 → 2576 % (×25,8) en 30 images à 60 ips, soit 12,5 images @25 (0,5 s)**. Courbe `cubic-bezier(0.6,0,0.15,1)` : influence de sortie 60 %, d'entrée **85 %**, pic de vitesse ×3,8 la moyenne.
- Image par image : le logo fait 16 % de la largeur du cadre à #01, 29 % à #03, 52 % à #04 et 76 % à #05. Il **dépasse la largeur à 32 % de la durée** (src 9,5, image 4,0 @25) et la hauteur à 37 % (src 11,1, image 4,6). À **43 %** (src 13, image 5,4), le **trou couvre tout le cadre** : on est dedans.
- **Vitesse perçue** (dérivée de ln(échelle)) : pic de **0,75 par image @25, soit ×2,1 par image**, juste au moment de la traversée. Les 57 % restants sont une longue décélération à l'intérieur du nouveau monde.
- Le contenu vu à travers le trou (la carte) passe de 100 à 0 % d'opacité sur **la même courbe** (src 3 → 27).

## 05 · Coinbase tradeStatus : fusion de points, anticipation, chute, éclosion, pop élastique

Planche `05_coinbase_dots_merge_planche.png` · courbes `courbes/05_coinbase_dots_merge_courbes.png` · CSV `mesures/05_coinbase_tradeStatus_pixels.csv`

- **FUSION, #07 à #13** :
  - 3 points de diamètre 32 px, entraxe **2,5 diamètres**, convergent en 8 images src (6,7 @25) ;
  - courbe `cubic-bezier(0.037,0.757,0.477,0.938)` : **52 % du trajet parcouru dès la première image**, puis arrivée amortie ;
  - les points se soudent en **gélule L/H 2,42**, qui redevient ronde en 6 images src (5 @25), avec un L/H de **2,0 / 1,58 / 1,33 / 1,19 / 1,03 / 1,0** (chaque image retire environ 35 à 45 % de l'excès).
- **ANTICIPATION** : pendant la fusion, le point **monte de 0,7 diamètre** (13 images src) et marque un petit temps en haut.
- **CHUTE** : le point descend en accélérant (`cubic-bezier(0.66,0,0.985,0.268)` : influence de sortie 66 %, influence d'entrée de seulement **1,5 %** avec une pente raide, donc une vitesse finale de ×49 la moyenne).
- **IMPACT** : en 1 image, le point est **remplacé** par le disque final à 12 %, posé 3,6 diamètres plus bas, avec 1 image de tassement (L/H 1,28). Le grand saut passe parce que la vitesse était déjà très élevée.
- **ÉCLOSION** : le point d'ancrage est sur le **bord inférieur** (anchor [0,64]), donc le disque pousse vers le haut, comme une bulle qui sort du sol. Il atteint **56 % du diamètre final en 2 images src**, 95 % en 10, avec une surcourse de +1 %. La surcourse est portée par la poignée `o.y = 1.48` au lieu d'une clé supplémentaire.
- **POP JAUNE, #64 à #90** : diamètre 18 → 100 % (6 images src) → **120 %** (9) → **93,6 %** (5) → 100 % (12), soit **5 / 7,5 / 4 / 10 images @25**. Le rebond suivant fait environ 1/3 de l'amplitude précédente (+20 %, puis −6,4 %). Mouvement secondaire : la position Y **monte pendant la croissance et descend pendant la surcourse** (contre-phase, environ 0,1 diamètre).
- **Signature Coinbase** : l'arrivée en `i=(0.12,1)`, soit **88 % d'influence d'entrée** (28 clés). 86 poignées sur 521 sortent de [0,1] : les dépassements sont dessinés dans les tangentes, pas avec des clés en plus.

## 06 · useAnimations « loading3 » : un point qui s'étire en gélule (début et fin de trim décalés en courbe)

Planche `06_loading3_planche.png` · courbes `courbes/06_loading3_courbes.png` · CSV `mesures/06_loading3.csv`

- C'est un seul trait à bouts ronds. Sur chaque trajet de 12 images (12,5 @25, 0,5 s, 3 diamètres de course), le **début et la fin du trim** ont **les mêmes clés** mais des courbes opposées :
  - **tête** : `cubic-bezier(0.3,0,0.3,1)` (part vite, arrive doucement) ;
  - **queue** : `cubic-bezier(0.7,0,0.7,1)` (part tard, rattrape d'un coup).
- Longueur mesurée (#01 à #13) : 1,03 / 1,11 / 1,31 / 1,68 / 2,07 / 2,35 / **2,47** / 2,43 / 2,22 / 1,88 / 1,48 / 1,19 / 1,05 diamètre. L'étirement est **symétrique, maximal à mi-course (×2,48)**, sans aucune clé d'échelle.
- C'est exactement la mécanique d'un **col qui s'allonge, s'amincit puis claque** quand la queue rattrape la tête.

## 07 · Labo de points : décalage, courbes différentielles, relais

Planche `07_points_labo_planche.png` · courbes `courbes/07_points_labo_courbes.png`

- **07a, activityIndicator (Coinbase)** : 3 points sur la même orbite avec **les mêmes clés (0 → 360° en 61 images src, 2 s) et aucun décalage temporel**. Seule l'influence de sortie change : 16,7 %, 50,6 % et 69,9 % (même entrée à 16,7 %). Ils partent groupés, **s'étalent jusqu'à 64,5°** à mi-cycle et se regroupent exactement sur la clé : un accordéon organique.
- **07b, moreHorizontal** : vague de 3 points (diamètre 4 u, entraxe 1,75 diamètre) :
  - saut de 0,75 diamètre ;
  - montée en 6 images src `(0,0,0.58,1)` : décollage sec ;
  - descente en 6 images `(0.42,0,1,1)` : gravité ;
  - **décalage de 4 images src (3,3 @25), soit 2/3 de la montée**.

  Contre-exemple pour SFEER : **13 images @25 totalement immobiles** sur 33 (40 % du cycle).
- **07c, loader en anneaux** : disques concentriques qui rétrécissent de 100 à 0 % en 20 images (Easy Ease 33 %), en relais toutes les 5 images src (4,2 @25). Chaque couche part au quart de la précédente : 75 % de recouvrement, le centre ne s'arrête jamais.

## 08 · Webex logo loop : logo-ruban en tapis roulant

Planche `08_webex_logo_loop_planche.png` · `keyframes/08_webex_logo_loop.txt`

- Le logo garde sa silhouette pendant 5 s, mais rien ne s'arrête :
  - un long trait sinusoïdal est **translaté horizontalement à vitesse constante** (interpolation linéaire 0.167/0.833, 172 px en 150 images à 60 ips) ;
  - une **fenêtre de trim de 18 %** glisse dessus (41 → 56 → 72 %) ;
  - 3 mattes rectangulaires se relaient toutes les 150 images (période 2,5 s).
- C'est le modèle du **« hold vivant »** : le plan de pause d'un logo, sans ease, donc sans arrêt.

---

## Règles de mouvement SFEER (à 25 ips)

1. **Entrée de flaque ou de fenêtre plein cadre en 6 à 7 images**. La première image montre déjà environ 20 à 25 % du cadre (pas d'ouverture progressive), puis environ +12 à 15 points de surface par image. **Sortie 2× plus lente (15 à 17 images)**, avec un bord ondulé d'amplitude environ 10 % de la hauteur qui révèle la scène dessous. (01)
2. **Juste avant de se retirer, la masse gonfle de 3 à 4 % pendant 5 à 7 images** (anticipation). (01)
3. **Formes liquides en 4 sommets bézier, doublées par une nappe teinte** (orange foncé sous #FF6720) qui partage les clés d'entrée et **diverge de 2 à 4 images en sortie** : de l'épaisseur sans dégradé. (01)
4. **Deux bulles sur l'axe horizontal = vases communicants** : centres fixes, **somme des diamètres constante (±4 %)**, respiration en opposition en `cubic-bezier(0.48,0.04,0.52,0.96)`, **12 à 13 images par demi-cycle**. Écart bord à bord minimal ≥ 0,17 × la somme des diamètres. (03)
5. **Ne jamais animer une seule propriété** : une entrée combine échelle, rotation et tracé sur les mêmes 12 à 13 images, avec des influences différentes (55 / 66 / 76 %). Un point devient arc, puis anneau, puis disque (épaisseur de trait 5,5 → 21 = anneau vers disque plein). (02, 03)
6. **Traversée de la bulle-fenêtre en 12 à 13 images**, une seule clé d'échelle **×25** en `cubic-bezier(0.6,0,0.15,1)`. Le bord de la bulle sort du cadre entre 32 et 37 % de la durée, le vert remplit 100 % du cadre à environ 43 %. À ce moment l'échelle **double à chaque image**, puis il reste environ 7 images de décélération dans le vert. Ce qui est autour de la bulle se fond **sur la même courbe**. (04)
7. **Fusion de bulles** : convergence en environ 7 images en `cubic-bezier(0.04,0.76,0.48,0.94)` (plus de 50 % du trajet dès l'image 1). La forme fusionnée **s'étire à L/H 2,4**, puis revient au rond en **5 images** en retirant environ 40 % de l'excès par image (2,0 → 1,6 → 1,3 → 1,2 → 1,0). (05)
8. **Col et étirement** : pour qu'une bulle file sur l'axe, animer le **bord avant** en `cubic-bezier(0.3,0,0.3,1)` et le **bord arrière** en `cubic-bezier(0.7,0,0.7,1)` sur les mêmes clés. L'allongement est maximal à mi-course (×2,5 le diamètre pour 3 diamètres parcourus en 12,5 images), puis l'arrière **claque** sur l'avant. Le col s'amincit pendant que l'arrière traîne. (06)
9. **Pop élastique de bulle** : 0 → 100 % en 5 images, **120 %** à +7,5 images, **94 %** à +4 images, 100 % à +10 images. Chaque rebond fait environ 1/3 du précédent. Le centre **monte pendant la croissance et redescend pendant la surcourse** (contre-phase, environ 0,1 diamètre). Mettre le dépassement **dans la poignée** (`o.y > 1`) plutôt que dans une clé supplémentaire. (05)
10. **Anticipation et impact** : montée de 0,5 à 0,7 diamètre en environ 11 images, chute accélérée en environ 12 images (`cubic-bezier(0.66,0,0.985,0.27)` : influence d'entrée 1,5 %, vitesse finale environ ×50 la moyenne). À l'impact, **substituer la nouvelle forme en 1 image** (tassement L/H 1,3), puis éclosion **depuis un ancrage au sol** : 56 % de la taille en 2 images et 95 % en 8. (05)
11. **Groupe organique sans décalage** : mêmes clés pour toutes les bulles, influences de sortie étagées (17 / 51 / 70 %). Elles s'écartent puis se regroupent pile sur la clé. Si on décale dans le temps, le faire de **2/3 de la durée du geste** (3 images pour un geste de 5) ou d'**1/4 de la durée** pour un relais (4 images sur 17). (07)
12. **Arrivées signature** : `i = (0.12, 1)`, soit 88 % d'influence d'entrée, pour des atterrissages longs et soyeux. Départs `(0.66, 0)` ou `(0.6, 0)` pour les gestes majeurs. **Bannir l'Easy Ease par défaut (33 %)**, qui est mou. (02 à 05)
13. **Aucun maintien mort** : pendant un plan « posé » (logo final de l'outro), garder un mouvement **linéaire perpétuel** sur l'axe horizontal (dérive du dégradé, ruban ou bulles qui coulent) à vitesse constante, sur une période de 2 à 3 s. Le contre-exemple 07b est immobile 40 % du temps. (08, 07b)

## Limites

- Les sources sont des icônes et des loaders (32 à 480 px) ou des transitions courtes, pas des bumpers TV complets. Les règles sont des **ratios** à transposer à l'échelle 1920×1080.
- Aucune Lottie npm trouvée ne montre un vrai **métaball avec col concave** entre deux cercles. Les analogues les plus proches sont la gélule de fusion (05), l'étirement par trim (06) et les deux disques Cisco (03), qui se recouvrent sans col. Le col SFEER reste à construire, par exemple avec la règle 8 pour l'amincissement et la règle 7 pour le retour au rond.
- Précision des mesures au pixel : ±1 px sur des rendus de 400 à 513 px, soit ±0,2 à 0,5 % du cadre. Les boîtes DOM ignorent l'épaisseur de trait ; les diamètres de 03 et 05 viennent donc des pixels.
- Le rééchantillonnage des sources à 60 ips vers 25 ips passe par l'interpolation de lottie-web (images fractionnaires). Les durées « @25 » sont exactes, les vignettes tombent entre deux images source.
- Les fichiers Coinbase n'ont **pas de licence déclarée** dans package.json : ils servent à l'étude, ne pas les réutiliser tels quels.
