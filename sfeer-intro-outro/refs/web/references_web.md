# Références web : motion des bulles SFEER (intro / outro 3 à 5 s)

Clé : `web`. Rédigé le 14/10/2026. Cadence de référence : **25 i/s (1 image = 40 ms)**.

> **Je n'ai visionné AUCUNE image de ces références.** Vimeo, YouTube, Behance, Dribbble, Pinterest, Giphy et LottieFiles sont bloqués ici, comme presque tous les sites éditoriaux. Chaque fiche s'appuie donc :
> - soit sur le **texte des résultats de recherche** (articles, études de cas, presse). C'est marqué `[texte]`. Les citations sont des paraphrases de ces résultats. Je n'ai pas lu les pages elles-mêmes.
> - soit sur une **source primaire que j'ai pu lire en entier**, marquée `[primaire lue]` : code et jetons publiés sur npm (`@material/web` 2.5.0, `@carbon/motion` 11.54.0, `@fluentui/tokens`, `@shopify/polaris-tokens` 9.4.2, `@mui/material` 9.5.0, `@ibm/motion` 0.3.1, `paper` 0.12.18), fichiers sources AndroidX / AOSP / Material Components lus sur raw.githubusercontent.com, documentation Apple (JSON developer.apple.com) et transcriptions des sessions WWDC18 803 et WWDC23 10158.
>
> La rubrique « À regarder image par image » de chaque fiche dit **ce que la DA doit mettre en pause et mesurer** quand elle aura la vidéo. Ce ne sont pas des observations de ma part.
> Les seuls chiffres « mesurés » de ce dossier sont **calculés** à partir des specs publiées (courbes, ressorts, algorithme de Sato). Ils sont reproduits dans les deux planches PNG et dans `specs_25ips.json`.

Fichiers du dossier :
- `references_web.md` (ce document)
- `specs_espacement_25ips.png` : tableau d'espacement image par image de 7 courbes publiées, pour un mouvement de 15 images
- `sato_cou_planche.png` : amincissement du cou metaball (algorithme de Sato / Paper.js) en 12 états mesurés
- `specs_25ips.json`, `sato_cou_mesures.json` : les données chiffrées

---

## 0. Ce qu'on retient : 12 règles chiffrées pour SFEER

| # | Règle | Chiffre à 25 i/s | Source |
|---|---|---|---|
| R1 | **Jamais immobile : une couche de fond qui bouge toujours, plus des événements ponctuels.** Chez Google, les points sont « un état du logo en mouvement perpétuel ». Le loader M3 Expressive change de forme toutes les 650 ms et tourne en continu. | Événement toutes les **16 images** (650 ms). Rotation de fond de **≈ 3,1° par image** (360° en 4 666 ms, linéaire). | design.google 2015 `[texte]` ; `LoadingIndicator.kt` `[primaire lue]` |
| R2 | **Entrée « emphasized » : on part vite, longue traîne.** Courbe M3 emphasized : 50 % du trajet à 18 % du temps, 90 % à 38 %. | Sur 15 images : 64 % à l'image 3, 91 % à l'image 6, puis 9 images pour les derniers 9 %. | jetons M3 `[primaire lue]` + calcul |
| R3 | **Sortie « accelerate » : presque rien, puis tout d'un coup.** Courbe emphasized-accelerate (0.3, 0, 0.8, 0.15) : 15 % du trajet à mi-temps, 50 % à 81 % du temps. | Sur 10 images, la bulle part vraiment dans les **2 dernières images**. | idem |
| R4 | **Budget de dépassement (overshoot) : 3 à 10 % maximum.** Back de Penner s=1.70158 : **10,0 %**, pic à 58 % de la durée. Ressort M3 expressive fast (ζ 0,6) : **9,5 %**. Apple bouncy : **4,6 %**. Apple conseille 100 % d'amortissement par défaut et 80 % (≈ 1,5 %) seulement quand le geste a de l'élan. | Pic de dépassement : image 3-4 (M3 fast), image 9 (Apple bouncy à 0,5 s), image 9 sur 15 (Penner). | calculs sur specs `[primaire lue]` ; WWDC18 803 `[primaire lue]` |
| R5 | **La déformation ne dépasse pas, l'échelle si.** Le loader M3E plafonne volontairement la progression de la déformation (pas de rebond de forme) et simule le rebond par un changement d'échelle du dessin. | Progression du cou / de la déformation bornée à [0,1]. Rebond porté par l'échelle (≈ +5 à +10 %). | `LoadingIndicator.kt`, commentaire du code `[primaire lue]` |
| R6 | **Écrasement publié : -15 % puis +5 %.** Keyframes `bounce` de Polaris : échelle 1 → **0,85** (à 75 % du temps) → **1,05** (à 82,5 %) → 1 (à 85 %). Tout le rebond tient dans les 20 derniers pour cent de la durée. | Sur 25 images : écrasement aux images 16 à 19, rebond aux images 19 à 21, stable à 21. | `@shopify/polaris-tokens` `[primaire lue]` |
| R7 | **Volume constant : étirement le long de l'axe en déplacement, contraction à l'arrêt.** Les particules Gemini « s'étirent en voyageant, se contractent en se posant ». L'icône iPhone X « s'étire élastiquement » pour devenir l'app. | Garder sx × sy = 1. L'étirement suit la vitesse et revient à 1 en 2 à 4 images après l'arrêt (proposition à valider). | Art&Graft `[texte]` ; WWDC18 `[primaire lue]` ; Disney 12 principes `[texte]` |
| R8 | **Smear = 1 à 2 images d'intervalle allongé** (ou des « multiples » le long de la trajectoire). Apple : trop de changement entre deux images voisines produit du **stroboscope**, et 25 i/s y est plus sensible que 60 i/s. | 1 image de smear dès qu'une bulle avance de plus d'environ 1 diamètre par image (seuil à valider en test). | Wikipedia Smear frame, Bloop `[texte]` ; WWDC18 `[primaire lue]` |
| R9 | **Le cou de Sato s'amincit de façon linéaire puis plafonne : il ne casse jamais tout seul.** Pour une petite bulle de 0,6 r : cou = 69 % du diamètre de la petite bulle au contact, 49 % à d = 1,3 Σr, 28 % à 1,6 Σr, **7,5 % à 1,9 Σr**, puis un palier à 7 %. Dans la démo, la membrane disparaît d'un coup à maxDistance (≈ 2 Σr). Le point le plus fin est **décalé vers la petite bulle** (à 58 à 65 % de l'entraxe). | La **rupture (snap) se place à d ≈ 1,9 Σr**, sur 1 image. Ensuite, les deux moitiés du cou rentrent dans leur bulle en 3 à 5 images avec un ressort ζ ≈ 0,6 (≈ 9 % de dépassement). | Paper.js `MetaBalls.html` `[primaire lue]` + mesure |
| R10 | **Bulle → fenêtre plein cadre (container transform).** À l'entrée : la vidéo apparaît en fondu sur 0-25 % de la progression, le masque de forme (bulle vers rectangle) se fait sur 0-75 %, l'échelle sur 0-100 %. Voile (scrim) noir à 32 %. | Transition de 20 images : vidéo visible aux images 0-5, contour devenu rectangle à l'image 15, zoom jusqu'à l'image 20. | MDC Android `Motion.md` `[primaire lue]` |
| R11 | **La durée croît moins vite que la distance.** MUI : 100 px → 239 ms (6 images), 1 080 px → 451 ms (11 images), 1 920 px → 552 ms (14 images). IBM expressive plafonne vers 333 ms. M3 : « la durée augmente avec l'aire ou la distance parcourue ». | Traversée horizontale de 1 920 px ≈ **14 images** en base UI. Pour un moment fort de bumper : × 1,5 à 2, soit 20 à 28 images. | `@mui/material`, `@ibm/motion` `[primaire lue]` |
| R12 | **Sortie plus courte que l'entrée (≈ 85 %)** : MD2 entrée 225 ms / sortie 195 ms ; container transform 300 / 250 ms. **Décalage (offset & delay)** : les éléments partagent la même courbe et sont décalés dans le temps. Les points Google suivent « des arcs géométriques et un jeu standard de courbes vives ». | Entrée 15 images → sortie 12-13 images. Décalage entre bulles de 2 à 4 images. | MUI `[primaire lue]` ; UX in Motion, design.google `[texte]` |

---

## 1. Les 20 fiches de références

Légende du statut : `[texte]` = connu par le texte des résultats de recherche ; `[primaire lue]` = source primaire lue en entier. **Aucune vidéo n'a été vue.**

### A. Logos à points, bulles et cercles

#### 1. Google : « Evolving the Google Identity » (2015) et les points d'état (écoute, réflexion, réponse)
- **Auteurs** : Google Design et Creative Lab. Jonathan Jarvis, directeur de création du Creative Lab, est interviewé par Motionographer. Jonathan Lee (Material Design) et Alex Cook sont cités comme co-auteurs selon It's Nice That. Note de divulgation technique Kuscher & Martin (2017).
- **URL** : https://design.google/library/evolving-google-identity/ · https://motionographer.com/2015/11/09/interview-motion-design-and-the-google-identity/ · https://www.designboom.com/design/new-google-logo-09-01-2015/ · https://www.fastcompany.com/3050613/googles-new-logo-is-its-biggest-update-in-16-years · https://www.tdcommons.org/dpubs_series/375 · https://www.protopie.io/blog/voice-and-cross-device-prototyping
- **Ce qu'on sait** `[texte]` : les 4 points sont une forme distillée du logotype, utilisée pour « les moments interactifs, d'assistance et de transition ». C'est « un état du logo dynamique et en mouvement perpétuel ». Le mouvement repose sur « des trajectoires et un timing constants : arcs géométriques, jeu standard de courbes d'accélération vives ». Une gamme d'expressions a été créée : écoute, réflexion, réponse, incompréhension, confirmation. En recherche vocale, les points deviennent un égaliseur qui réagit au ton et à la hauteur de la voix. Ils réapparaissent et **tournent** pendant le traitement, puis se retransforment en « Google ». Au repos (idle), ils montent et descendent lentement. En écoute, ils **s'alignent à l'horizontale** et réagissent au son.
- **À regarder image par image** :
  1. Le passage du mot « Google » aux 4 points. Les lettres rétrécissent-elles en points, ou les points sortent-ils des lettres ? Combien d'images dure la transformation ?
  2. Pendant la rotation de « réflexion », les points gardent-ils un espacement constant, ou se rapprochent-ils dans les virages (overlap) ? Mesurer l'angle par image.
  3. Le rebond d'écoute : hauteur maximale d'un point en % de son diamètre, et décalage en images entre les points 1, 2, 3 et 4.
  4. Le retour points → « G » : y a-t-il une image d'étirement (smear) avant de devenir le G ?
- **Règle SFEER** : on définit un **vocabulaire d'états** pour les bulles (repos qui flotte → regroupement → déformation → ouverture de fenêtre). Tous les déplacements suivent des **arcs** (pas de lignes droites), avec la même courbe pour tous et un décalage de 2 à 4 images d'une bulle à l'autre. Les bulles **s'alignent sur l'horizontale** au moment clé, comme les points d'écoute de Google : c'est l'axe SFEER.

#### 2. Gemini : système de particules d'Art&Graft et dégradés de Google Design
- **Auteurs** : Art&Graft (Gulya Voronova, senior motion designer) pour Google DeepMind ; Google Design (« Illustrating the Gemini App ») ; Porto Rocha (identité Spark).
- **URL** : https://abduzeedo.com/art-graft-gemini-identity-system · https://design.google/library/gemini-ai-visual-design · https://www.portorocha.com/gemini
- **Ce qu'on sait** `[texte]` : identité pilotée par le mouvement, faite de particules (points et pilules) qui bougent « comme un banc de poissons ». Elles dérivent doucement à l'état ambiant et forment des figures précises quand l'utilisateur interagit. Elles **s'étirent en voyageant et se contractent en se posant**. Dégradé à 4 couleurs. Chez Google Design, les dégradés ont **un bord avant net et une queue diffuse**, pour donner une direction et de l'énergie.
- **À regarder image par image** : le rapport longueur / largeur maximal d'une pilule en plein vol ; le nombre d'images entre l'arrêt d'une particule et le retour à sa forme ronde ; le passage de l'état ambiant à la figure (les particules partent-elles toutes en même temps ou en vague ?).
- **Règle SFEER** : étirement proportionnel à la vitesse, le long de l'axe horizontal, puis contraction à l'arrêt (R7). Le dégradé indigo → lavande peut **suivre le mouvement** : bord avant net côté direction, bord arrière diffus. Le fond n'est ainsi jamais figé.

#### 3. Mastercard : refonte Pentagram (2016)
- **Auteurs** : Pentagram (Michael Bierut, Luke Hayman).
- **URL** : https://www.pentagram.com/work/mastercard/story · https://www.creativereview.co.uk/new-mastercard-logo-pentagram/ · https://www.itsnicethat.com/news/mastercard-brand-mark-refresh-by-pentagram-150716
- **Ce qu'on sait** `[texte]` : deux cercles qui se chevauchent. La zone commune est un **orange additif**, plus lumineux. Système de cercles répétés, animation prévue dans le système. Aucune spec de timing n'est publiée.
- **À regarder image par image** : dans les films de marque, le moment où les deux cercles se croisent. La zone commune apparaît-elle d'un coup ou progressivement ? Les cercles ralentissent-ils au moment du recouvrement ?
- **Règle SFEER** : quand deux bulles se croisent, la **zone d'intersection est un événement** (changement de couleur, éclair), pas un simple chevauchement passif.

#### 4. Oi : logo qui réagit à la voix (2016)
- **Auteurs** : Wolff Olins (identité) ; onformative (logiciel génératif ; Cedric Kiefer, Mark Tiedemann).
- **URL** : https://onformative.com/work/oi/ · https://www.designweek.co.uk/issues/4-april-10-april/oi-wolff-olins-designs-telecoms-logo-which-reacts-to-the-human-voice/ · https://www.dezeen.com/?p=883036
- **Ce qu'on sait** `[texte]` : le logo est une **bulle de dialogue** devenue un « blob » vivant. Le volume sonore fait varier la taille, la hauteur fait varier la couleur et la forme. Les voix calmes donnent du bleu calme, les voix fortes donnent du fluo agité.
- **À regarder image par image** : l'amplitude de la déformation sur une attaque sonore (combien d'images pour gonfler, combien pour revenir) ; le contour reste-t-il lisse ou présente-t-il des pointes ?
- **Règle SFEER** : **synchroniser les pics de déformation sur les attaques du logo sonore** de Riyadh Air (identité sonore Sonicbrand). La bulle gonfle sur le temps fort et revient avec un ressort.

#### 5. Patreon : refonte « motion-first » (2023)
- **Auteurs** : Wolff Olins (stratégie), David McLeod (3D), Active Theory (digital et motion), Dinamo (typographie).
- **URL** : https://news.patreon.com/articles/patreon-redesigned · https://wolffolins.com/work/patreon · https://www.itsnicethat.com/news/patreon-rebrand-graphic-design-121023
- **Ce qu'on sait** `[texte]` : un « P » 3D abstrait qui se déforme selon son environnement. Le logo « n'a pas de forme canonique exacte ; c'est un objet dynamique en mouvement constant ».
- **À regarder image par image** : la vitesse de déformation au repos. Est-elle perceptible à chaque image ou seulement sur une seconde ? Quels points du contour bougent en premier ?
- **Règle SFEER** : même « à l'arrêt », la bulle **respire** (variation lente, de l'ordre de ±1 à 2 % d'échelle sur 1 à 2 s). La forme de référence n'apparaît qu'aux images clés.

#### 6. Spotify Music + Talk (2022) et NN North Sea Jazz (2022-2023) : Studio Dumbar/DEPT
- **Auteur** : Studio Dumbar/DEPT®.
- **URL** : https://studiodumbar.com/work/spotify-music-talk · https://awards.europeandesign.org/winner/256485 · https://studiodumbar.com/work/north-sea-jazz · https://www.itsnicethat.com/news/studio-dumbar-north-sea-jazz-festival-identity-graphic-design-241022
- **Ce qu'on sait** `[texte]` : pour Music + Talk, les formes qui contiennent le texte **s'étirent et se contractent** pour exprimer la pulsation du son, et cela crée une famille de formes. Argent aux European Design Awards 2022, catégorie Motion Logo. Pour North Sea Jazz, la typographie « se tord, fléchit et se transforme comme une onde sonore ». D&AD Wood Pencil 2023.
- **À regarder image par image** : le rapport d'étirement maximal d'une capsule ; le **rythme** (combien d'images entre deux pulsations) ; l'étirement est-il symétrique ou part-il d'un bord ?
- **Règle SFEER** : la capsule (deux bulles plus un cou) est une **forme élastique sur l'axe horizontal**. Elle peut pulser en étirement / contraction au tempo de la musique, à volume constant.

#### 7. *Dr. No* (1962) : générique de Maurice Binder (points colorés)
- **Auteur** : Maurice Binder.
- **URL** : https://www.artofthetitle.com/feature/james-bond-50-years-of-main-title-design/ · https://www.watchthetitles.com/?p=682 · https://en.wikipedia.org/wiki/Maurice_Binder
- **Ce qu'on sait** `[texte]` : générique fait de points colorés, de carrés et de silhouettes. Les points changent de couleur et de position et forment des motifs **au tempo rapide de la musique**. Binder ne lisse pas les transitions : si la musique repart, ses titres repartent.
- **À regarder image par image** : combien d'images un point reste dans une couleur ; les points apparaissent-ils par « pop » (0 → 100 % en 1 image) ou par croissance ; le synchronisme avec les temps de la musique.
- **Règle SFEER** : des **apparitions sèches sur le temps** (pop en 1 à 2 images, avec un dépassement de +10 % à l'image suivante) donnent l'énergie « super motion ». Le lissage n'est pas obligatoire partout.

### B. Liquide, metaball, effet « gooey »

#### 8. SATO Hiroyuki / Paper.js « Meta Balls » : la géométrie du cou entre deux cercles
- **Auteurs** : SATO Hiroyuki (script Scriptographer / Illustrator d'origine), porté dans les exemples de Paper.js.
- **URL** : paperjs.org/examples/meta-balls (lien cité dans les résultats) · code lu : paquet npm `paper@0.12.18`, fichier `examples/Paperjs.org/MetaBalls.html` `[primaire lue]`
- **Ce qu'on sait** `[primaire lue]` : la membrane est posée sur les deux cercles à des angles calculés par `acos((r1-r2)/d)`, avec un facteur d'écartement `v = 0.5` et un taux de poignée `handle_len_rate = 2.4`. La poignée est bornée à `v·rate = 1,2 r`. Au-delà de `maxDistance` (300 px dans la démo, soit 2 Σr pour 100 + 50, ou 3 Σr pour 50 + 50), la membrane **n'est plus dessinée du tout**.
- **Mesures** (planche `sato_cou_planche.png`, calcul par rastérisation) :

  | d / (r1+r2) | 0,85 | 1,00 | 1,15 | 1,30 | 1,45 | 1,60 | 1,75 | 1,90 | ≥ 2,0 |
  |---|---|---|---|---|---|---|---|---|---|
  | cou, % du diamètre de la petite bulle (r2 = 0,6 r1) | 91 | 69 | 59 | 49 | 39 | 28 | 18 | **7,5** | 7 (palier) |
  | cou, % du diamètre (r1 = r2) | 74 | 55 | 47 | 40 | 32 | 24 | 16 | **7,5** | 7 (palier) |
  | point le plus fin (0 = grande bulle, 1 = petite), r2 = 0,6 r1 | 0,74 | 0,65 | 0,64 | 0,62 | 0,60 | 0,59 | 0,59 | 0,58 | 0,56 |

- **À regarder image par image** (dans la démo interactive, ou dans les marques qui utilisent ce script) : la disparition **sèche** du pont à maxDistance (1 image) ; le cou reste plat et fin sur une longue distance avant de disparaître (« spaghetti »).
- **Règle SFEER** : sur la forme publiée, le cou maigrit de 5 à 7 points (en % du diamètre de la petite bulle) par 0,1 Σr d'écartement, entre 1,0 et 1,9 Σr. Au-delà, il ne fait que s'allonger. **La rupture doit donc être une décision d'animation**, à d ≈ 1,9 Σr, en 1 image. Elle est suivie d'un retour des deux moignons en 3 à 5 images avec dépassement (R9). Pour garder l'aspect « concave » de la charte, il ne faut jamais montrer le palier plat. Il faut aussi tenir compte du fait que le cou casse **plus près de la petite bulle**.

#### 9. Varun Vachhar : « Metaballs » (SVG, une seule forme)
- **Auteur** : Varun Vachhar.
- **URL** : https://varun.ca/metaballs
- **Ce qu'on sait** `[texte]` : il reconstruit la méthode de Sato en SVG pour obtenir **tout le blob en un seul tracé**. Les tangentes extérieures communes donnent la largeur maximale du connecteur. L'écartement est `acos((r1 - r2)/d)` multiplié par `v`. Le cas des cercles sans chevauchement est traité séparément.
- **À regarder image par image** : les démos de l'article. Comparer la forme du cou quand `v` varie à distance constante.
- **Règle SFEER** : pour un rendu vectoriel net (nécessaire en flat 2D), on garde **un seul tracé** (deux cercles plus deux béziers). On évite le flou + seuil, qui arrondit les bords et fait « baver » les couleurs (voir fiche 10). **Animer `v` vers 0 juste avant la rupture** donne un pincement propre.

#### 10. Lucas Bebber / Codrops : « Creative Gooey Effects » (2015)
- **Auteur** : Lucas Bebber (Codrops) ; reprises par CSS-Tricks et Visual Cinnamon (Nadieh Bremer).
- **URL** : https://tympanus.net/codrops/2015/03/10/creative-gooey-effects/ · https://css-tricks.com/?p=195076 · https://www.visualcinnamon.com/2015/05/gooey-effect/
- **Ce qu'on sait** `[texte]` : flou, puis `feColorMatrix` qui pousse le contraste du canal alpha (les formes fusionnent), puis `feComposite atop` qui redessine l'original. Il faut un fond transparent et c'est coûteux sur de grandes surfaces. Le compositing final préserve les tailles mais rend la fusion de couleurs différentes moins belle.
- **À regarder image par image** : les démos de menus qui explosent. Le pont se forme-t-il **avant** le contact (attraction à distance) ? Combien d'images dure la goutte qui se détache ?
- **Règle SFEER** : l'effet gooey **anticipe** le contact. Le pont apparaît quand l'écart est encore d'environ 0,2 à 0,5 rayon (à mesurer), ce qui donne une anticipation gratuite de 2 à 3 images avant la fusion.

### C. Fenêtres, portails, iris : entrer dans la vidéo

#### 11. James Bond, la séquence du canon (*Dr. No*, 1962 et suivants)
- **Auteurs** : Maurice Binder, assisté de Trevor Bond (caméra sténopé à travers un vrai canon).
- **URL** : https://en.wikipedia.org/wiki/Gun_barrel_sequence · https://www.artofthetitle.com/feature/james-bond-50-years-of-main-title-design/ · https://faroutmagazine.co.uk/james-bond-gun-barrel-sequence-story/
- **Ce qu'on sait** `[texte]` : des **points blancs clignotent et traversent l'écran sur une ligne horizontale** (Binder a utilisé des étiquettes autocollantes de prix), puis un point devient le canon. À la fin, le canon se fond en un point blanc qui soit enchaîne sur le générique, soit rétrécit et disparaît (en sautant en bas à droite), soit passe du blanc à une **découpe circulaire de la première scène qui s'agrandit** jusqu'au plein cadre.
- **À regarder image par image** (c'est la référence n°1 pour la piste « fenêtre ») :
  1. Le nombre d'images entre deux points sur la ligne horizontale (cadence), et leur espacement en % de la largeur.
  2. L'image où le point s'arrête et « devient » le canon : y a-t-il un écrasement ?
  3. **L'ouverture finale** : nombre d'images entre le petit cercle et le plein cadre. L'iris est-il linéaire, accéléré ou freiné ? Le contour est-il net ?
  4. La version CGI (après le milieu des années 1990) comparée à la version pratique : différences de flou de bord.
- **Règle SFEER** : la structure exacte de notre intro existe déjà. **Points sur l'axe horizontal → un point devient cercle → le cercle est une fenêtre sur le film → ouverture plein cadre.** On la reprend en flat, avec les bulles orange et le cou.

#### 12. L'iris (iris in / out) : Looney Tunes, le volet en forme
- **Sources** : Wikipedia « Wipe (transition) » ; histoire de la fin des Looney Tunes.
- **URL** : https://en.wikipedia.org/wiki/Wipe_(transition) · https://cartoonresearch.com/index.php/cartoons-about-cartoons-part-14/ · https://developer.android.com/reference/android/view/ViewAnimationUtils.html
- **Ce qu'on sait** `[texte]` : l'iris est un volet en cercle qui grandit ou rétrécit. Les Looney Tunes et Merrie Melodies l'utilisent pour signifier la fin, parfois comme gag de dernière image. Android propose le même geste en natif avec `createCircularReveal`, qui anime un **cercle de découpe** d'un rayon de départ à un rayon d'arrivée et découpe aussi les ombres.
- **À regarder image par image** : dans un iris-out de cartoon, le cercle s'arrête-t-il un temps sur un détail (le personnage qui sort la tête) avant de se fermer ? Combien d'images dure ce temps d'arrêt ?
- **Règle SFEER (outro)** : l'outro peut être un **iris-out en bulle**. Le film se referme dans une bulle, la bulle **marque un arrêt de 6 à 10 images** sur le centre d'intérêt, puis se ferme d'un coup (courbe accelerate, R3), et le cou ramène la bulle au logo.

#### 13. Material « container transform » (MDC Android, M3)
- **Auteur** : Google Material Design / Material Components.
- **URL** (telle que trouvée) : https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md?ref=androidweekly.io · https://material.io/design/motion/the-motion-system.html `[primaire lue : Motion.md via raw.githubusercontent]`
- **Ce qu'on sait** `[primaire lue]` : le conteneur de départ (une carte, une ligne, un **FAB rond**) change de taille et de forme pour devenir l'écran d'arrivée, et le contenu est échangé pendant la transformation. Valeurs par défaut :
  - entrée : fondu du contenu sur **0,00-0,25** de la progression ; masque de forme sur **0,00-0,75** ; échelle et masque d'échelle sur **0,00-1,00** ;
  - entrée avec arc : fondu 0,10-0,40 ; forme 0,10-0,90 ;
  - retour : fondu 0,60-0,90 ; forme 0,30-0,90 ;
  - voile `#52000000` (noir à 32 %) ; durée d'entrée 300 ms (`motionDurationLong1`), de sortie 250 ms ; trajectoire linéaire ou en arc.
- **À regarder image par image** (GIF de la doc, vitesse normale et ralenti) : le **FAB rond qui devient une page**. À quelle image le cercle cesse-t-il d'être un cercle ? Le contenu apparaît-il avant que la forme soit rectangulaire ?
- **Règle SFEER** : c'est le modèle exact de « la bulle devient la fenêtre ». Sur 20 images : la vidéo (fond vert) **apparaît dès les images 0 à 5, à l'intérieur de la bulle encore ronde** ; la bulle s'élargit en rectangle aux images 0 à 15 ; le zoom continue jusqu'à 20. La trajectoire en arc donne plus de vie.

#### 14. Apple, WWDC18 « Designing Fluid Interfaces » (session 803)
- **Auteurs** : Chan, Marcos et Nathan (équipe Human Interface d'Apple ; prénoms donnés dans la transcription).
- **URL** : https://developer.apple.com/videos/play/wwdc2018/803/ `[primaire lue : transcription]`
- **Ce qu'on sait** `[primaire lue]` :
  - « Au lancement d'une app, l'icône **s'étire élastiquement** vers le bas pour devenir l'app, et s'étire vers le haut dans l'autre sens à la fermeture » : c'est le *motion stretching*, qui ajoute de l'information entre les images.
  - Trop de différence entre deux images voisines provoque un **stroboscope** : à 30 i/s, il faut aller moins vite qu'à 60 i/s. Remèdes : flou de mouvement ou étirement.
  - On commence à **100 % d'amortissement** (pas de dépassement). On réserve **80 %** aux gestes qui ont de l'élan (exemple : balayer Now Playing).
  - Les photos ont moins de « masse » que les apps : la masse est un choix sémantique.
- **À regarder image par image** : l'ouverture d'app sur iPhone X et suivants filmée au ralenti. Rapport hauteur / largeur de l'icône à l'image la plus étirée, et nombre d'images entre l'icône et le plein écran.
- **Règle SFEER** : la bulle qui devient fenêtre **s'étire dans le sens du zoom** pendant le mouvement, puis se détend. À 25 i/s, le risque de stroboscope est plus grand qu'à 60 : on compense par l'étirement ou le smear (R8).

#### 15. Le raccord graphique (match cut) par la forme
- **Exemples** : *2001* (l'os devient un vaisseau), *Lawrence d'Arabie* (l'allumette devient le soleil, monteuse Anne V. Coates).
- **URL** : https://www.studiobinder.com/blog/match-cuts-creative-transitions-examples/
- **Ce qu'on sait** `[texte]` : la forme et la position à l'écran sont conservées au moment de la coupe.
- **À regarder image par image** : les images juste avant et juste après la coupe. La forme est-elle exactement superposée (même centre, même taille) ?
- **Règle SFEER** : pour un plan réel (fond vert), le **cercle de la bulle doit tomber sur un objet rond** du plan suivant (hublot, soleil, roue, tasse vue de dessus). On coupe sur l'image où les deux cercles coïncident.

### D. Craft : principes, smear, ressorts

#### 16. Les 12 principes de Disney et Lasseter (1987)
- **Auteurs** : Frank Thomas et Ollie Johnston, *The Illusion of Life* (1981) ; John Lasseter, « Principles of Traditional Animation Applied to 3D Computer Animation », SIGGRAPH 1987, *Computer Graphics* 21(4), p. 35-44.
- **URL** : https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation · https://www.evl.uic.edu/aej/527/papers/lasseter.pdf · https://education.siggraph.org/static/HyperGraph/animation/character_animation/principles/prin_trad_anim.htm
- **Ce qu'on sait** `[texte]` : écrasement et étirement (squash & stretch) à **volume constant** ; le timing traduit la masse ; Lasseter adapte les principes après *Luxo Jr.*
- **À regarder image par image** : dans *Luxo Jr.* (1986), la petite lampe qui saute sur la balle. Compter les images d'anticipation (accroupissement) par rapport à la durée du saut.
- **Règle SFEER** : chaque grand geste suit **anticipation → action → follow-through**. L'anticipation se fait dans le sens opposé, à environ 10-20 % de l'amplitude (proposition, à mesurer sur *Luxo*).

#### 17. Smear frames : Bloop Animation, *The Dover Boys* (1942), *Spider-Verse*
- **Auteurs** : Bloop Animation (article) ; Chuck Jones (*The Dover Boys*, Warner 1942) ; Sony Pictures Animation (*Spider-Verse*).
- **URL** : https://www.bloopanimation.com/the-art-of-smear-frames/ · https://Www.Wikipedia.org/wiki/Smear_frame · https://theses.fh-hagenberg.at/index.php/system/files/pdf/Lendenfeld18.pdf
- **Ce qu'on sait** `[texte]` : le smear relie deux poses « en aussi peu d'images que possible, souvent une seule ». *The Dover Boys* en compte **plus de trois douzaines**. Wikipedia distingue l'**intervalle allongé (1 à 2 images)** et les **multiples** (copies non déformées le long de la trajectoire). *Spider-Verse* remplace le flou de mouvement CGI par des smears et des multiples. Le terme vient de *The Animator's Survival Kit* de Richard Williams.
- **À regarder image par image** : dans *The Dover Boys*, les sorties de champ éclair. Combien d'images entre la pose A, le smear et la pose B ? Le smear garde-t-il la couleur pleine ou s'éclaircit-il ?
- **Règle SFEER** : en flat, le smear d'une bulle est une **capsule orange pleine** (un cercle étiré le long de l'axe) ou 2 à 3 **multiples** décroissants. On le place sur **1 image**, au plus 2, pendant le déplacement le plus rapide.

#### 18. School of Motion : follow-through, squash & stretch dans After Effects
- **Auteur** : School of Motion (Joey Korenman, Animation Bootcamp).
- **URL** : https://schoolofmotion.com/blog/animation-tricks-follow-through-after-effects · https://schoolofmotion.com/blog/how-to-squash-and-stretch-animations-more-efficiently · https://schoolofmotion.com/blog/automatic-follow-through-after-effects
- **Ce qu'on sait** `[texte]` : follow-through sans découper l'illustration ; un **creux d'anticipation** avant une rotation ; décaler les clés pour créer du dépassement ; une expression qui copie le mouvement principal **quelques images plus tard** pour un follow-through automatique ; une balle qui rebondit avec écrasement, étirement, anticipation et exagération.
- **À regarder image par image** : dans le tutoriel de la balle, les **images de contact** (écrasement maximal) et l'image juste après (étirement). Mesurer largeur / hauteur.
- **Règle SFEER** : les éléments secondaires (2e et 3e bulle, cou) **copient la bulle maîtresse avec 2 à 4 images de retard**. On peut le faire par expression, comme dans le tutoriel.

#### 19. « Creating Usability with Motion: The UX in Motion Manifesto » (2017)
- **Auteur** : Issara Willenskomer.
- **URL** : https://uxmag.com/articles/creating-usability-with-motion-the-ux-in-motion-manifesto · https://ixd.prattsi.org/2017/04/creating-usability-with-motion-the-ux-in-motion-manifest/
- **Ce qu'on sait** `[texte]` : 12 principes (easing, offset & delay, parenting, transformation, value change, **masking**, overlay, cloning, obscuration, parallax, dimensionality, dolly & zoom). Il distingue l'**état** masqué de l'**acte** de masquer : quand l'objet est en train d'être masqué, il y a mouvement.
- **À regarder image par image** : les GIF de démonstration du *masking* et du *dolly & zoom*. Le masque bouge-t-il en même temps que le contenu, ou le contenu reste-t-il fixe pendant que le masque s'ouvre ?
- **Règle SFEER** : la bulle-fenêtre est un **acte de masquage**. Le masque (la bulle) et le contenu (la vidéo) doivent bouger **à des vitesses différentes** : la vidéo zoome plus lentement que la bulle (parallaxe d'environ 0,6 à 0,8, à tester). C'est ce qui donne la sensation de « passer à travers ».

#### 20. Apple, WWDC23 « Animate with springs » (session 10158) et la doc `Spring`
- **Auteur** : Apple (présentée par « Jacob », équipe SwiftUI).
- **URL** : https://developer.apple.com/videos/play/wwdc2023/10158/?time=1080 · https://wwdcnotes.com/notes/wwdc23/10158 · https://developer.apple.com/documentation/swiftui/spring.md `[primaire lue : transcription et JSON de la doc]`
- **Ce qu'on sait** `[primaire lue]` :
  - Un ressort se règle avec 2 paramètres, **durée (perceptuelle) et rebond (bounce)**. Rebond 0 = critique (« smooth ») ; rebond > 0 = dépassement ; rebond < 0 = suramorti (aplati).
  - `Spring(duration: 0.5, bounce: 0.3)` donne masse 1, raideur 157,9, amortissement 17,6. Autrement dit : raideur = (2π/D)² et ζ = 1 − bounce.
  - Préréglages : `.smooth`, `.snappy` et `.bouncy` durent 0,5 s par défaut, avec un rebond de base de **0 / 0,15 / 0,3**. `.spring()` = response 0,5 et dampingFraction 0,825. `interactiveSpring` = 0,15 / 0,86.
  - On vise la **continuité de position et de vitesse** : pas de saut de vitesse au départ ni à l'arrivée.
- **À regarder image par image** : les courbes affichées dans la session vers 18:00-21:14 (*snappy*, rebond 0,15 puis 0,3).
- **Règle SFEER** : voir le tableau des ressorts au §2.3. Les bulles qui arrivent utilisent un ressort type « bouncy » ; la fenêtre plein cadre utilise « smooth » (le film ne rebondit pas).

---

## 2. Specs numériques publiées (vérifiées sur la source primaire)

### 2.1 Courbes d'accélération (easing) : où en est-on à 10 %, 50 % et 90 % ?
t10 / t50 / t90 = fraction du temps écoulé quand le mouvement atteint 10 % / 50 % / 90 % du trajet (calcul sur la courbe exacte).

| Courbe | Valeur publiée | t10 | t50 | t90 | Source |
|---|---|---|---|---|---|
| M3 **emphasized** | `path: M 0,0 C 0.05,0 0.133333,0.06 0.166666,0.4 C 0.208333,0.82 0.25,1 1,1` | 0,10 | **0,18** | **0,38** | MDC `Motion.md` ; AOSP `fast_out_extra_slow_in.xml` (API 28) |
| M3 standard (= « emphasized » en CSS web) | `cubic-bezier(0.2, 0, 0, 1)` | 0,08 | 0,20 | 0,54 | `@material/web` 2.5.0 `md-sys-motion` |
| M3 emphasized decelerate | `cubic-bezier(0.05, 0.7, 0.1, 1)` | 0,01 | 0,06 | 0,36 | idem |
| M3 emphasized accelerate | `cubic-bezier(0.3, 0, 0.8, 0.15)` | 0,41 | 0,81 | 0,97 | idem |
| M3 standard decelerate / accelerate | `(0, 0, 0, 1)` / `(0.3, 0, 1, 1)` | | | | idem |
| M2 / MUI easeInOut · easeOut · easeIn · sharp | `(0.4,0,0.2,1)` · `(0,0,0.2,1)` · `(0.4,0,1,1)` · `(0.4,0,0.6,1)` | 0,18 | 0,35 | 0,63 | `@mui/material` 9.5.0 |
| Carbon productive standard / entrance / exit | `(0.2,0,0.38,0.9)` / `(0,0,0.38,0.9)` / `(0.2,0,1,0.9)` | 0,13 | 0,37 | 0,74 | `@carbon/motion` 11.54.0 |
| Carbon **expressive** standard / entrance / exit | `(0.4,0.14,0.3,1)` / `(0,0,0.3,1)` / `(0.4,0.14,1,1)` | 0,15 | 0,36 | 0,65 | idem |
| Fluent easyEaseMax · easyEase | `(0.8,0,0.2,1)` · `(0.33,0,0.67,1)` | 0,33 | 0,50 | 0,67 | `@fluentui/tokens` |
| Fluent decelerateMax / Mid / Min | `(0.1,0.9,0.2,1)` / `(0,0,0,1)` / `(0.33,0,0.1,1)` | | | | idem |
| Fluent accelerateMax / Mid / Min | `(0.9,0.1,1,0.2)` / `(1,0,1,1)` / `(0.8,0,0.78,1)` | | | | idem |
| Polaris ease / ease-out / ease-in-out | `(0.25,0.1,0.25,1)` / `(0.19,0.91,0.38,1)` / `(0.42,0,0.58,1)` | | | | `@shopify/polaris-tokens` 9.4.2 |
| Penner easeOutBack | `1+(s+1)(t−1)³+s(t−1)²`, s = 1.70158 | | | | jQuery Easing 1.3, Phaser |

Quand une ligne regroupe plusieurs courbes, t10 / t50 / t90 sont ceux de la **première** courbe de la ligne (MUI easeInOut, Carbon standard, Fluent easyEaseMax).

Pour la lecture image par image, la planche `specs_espacement_25ips.png` donne la position de 7 courbes à chaque image d'un mouvement de 15 images :
- **M3 emphasized** : 0 · 3,8 · 19,3 · **63,6** · 80,0 · 87,1 · 91,2 · 94,0 · 95,9 · 97,3 · 98,3 · 99,0 · 99,5 · 99,8 · 99,9 · 100 %. Le saut principal a lieu entre les images 2 et 3 : c'est **là que se place un smear**.
- **Carbon expressive** : 50 % à l'image 6, 90 % à l'image 10. Plus « symétrique », plus calme.
- **Fluent easyEaseMax** : 50 % à l'image 8, avec un très fort ralenti au début et à la fin. Bon pour un mouvement de caméra « passer à travers ».

### 2.2 Durées (tokens), converties en images à 25 i/s

| Système | Tokens (ms → images) |
|---|---|
| **M3** (`@material/web`, MDC Android) | short1-4 : 50 / 100 / 150 / 200 ms → 1,25 / 2,5 / 3,75 / 5 im · medium1-4 : 250 / 300 / 350 / 400 → 6,25 / 7,5 / 8,75 / 10 · long1-4 : 450 / 500 / 550 / 600 → 11,25 / 12,5 / 13,75 / 15 · extra-long1-4 : 700 / 800 / 900 / 1000 → 17,5 / 20 / 22,5 / 25. La doc précise : « la durée doit augmenter avec l'aire ou la distance parcourue ». |
| **M2 / MUI** | shortest 150 (3,75 im) · shorter 200 (5) · short 250 (6,25) · **standard 300 (7,5)** · complex 375 (9,4) · **entrée 225 (5,6)** · **sortie 195 (4,9)**. Durée automatique selon la hauteur : `(4 + 15·(h/36)^0,25 + (h/36)/5)·10` ms → 100 px = 239 ms (6 im), 600 px = 376 (9,4), 1 080 px = 451 (11,3), 1 920 px = 552 (13,8). |
| **IBM Carbon** | fast-01 70 (1,75 im) · fast-02 110 (2,75) · moderate-01 150 (3,75) · moderate-02 240 (6) · slow-01 400 (10) · slow-02 700 (17,5), réservé aux « grandes transitions héroïques ». |
| **IBM motion v7** (2018) | durée de déplacement en mode expressif = `max(min(0,1·d+112, 142), d/(3d+1200·sf)·1000)` ms. Pour d = 1 920 px : 276 ms. Mode productif : 159 ms. Plus c'est loin, plus on va vite, pour une perception constante. |
| **Fluent 2** | ultraFast 50 · faster 100 · fast 150 · normal 200 · gentle 250 · slow 300 · slower 400 · ultraSlow 500 ms (1,25 à 12,5 im). |
| **Polaris** | 0 à 500 ms par pas de 50 ms, plus 5 000 ms. Keyframes `bounce` : échelle 1 → 0,85 (75 %) → 1,05 (82,5 %) → 1 (85 %). |
| **Apple** | Préréglages de ressort 0,5 s (12,5 im). `interactiveSpring` 0,15 s. Le HIG Motion ne donne **aucun chiffre** : « bref et précis », « laisser l'utilisateur interrompre », 30-60 i/s pour les jeux. |

À retenir : ces durées sont faites **pour l'interface**. Pour un bumper de 3 à 5 s (75 à 125 images), on garde le **profil** des courbes et les **ratios** (entrée / sortie ≈ 1 / 0,85 ; durée sous-linéaire avec la distance), et on monte les gestes héroïques à 15-25 images.

### 2.3 Ressorts publiés, convertis en images (masse 1, réponse à un échelon)

| Ressort | ζ (amortissement) | raideur k | dépassement | pic à | 90 % atteint à | entrée dans ±2 % | Source |
|---|---|---|---|---|---|---|---|
| M3 standard spatial fast / default / slow | 0,9 | 1400 / 700 / 300 | 0,15 % | 4,8 / 6,8 / 10,4 im | 2,3 / 3,2 / 4,9 im | 3,1 / 4,4 / 6,8 im | `StandardMotionTokens.kt`, `md-sys-motion` |
| **M3 expressive spatial fast** | **0,6** | 800 | **9,5 %** | **3,5 im** | 2,1 im | 5,3 im | `ExpressiveMotionTokens.kt` |
| M3 expressive spatial default | 0,8 | 380 | 1,5 % | 6,7 im | 3,8 im | 4,8 im | idem |
| M3 expressive spatial slow | 0,8 | 200 | 1,5 % | 9,3 im | 5,3 im | 6,6 im | idem |
| M3 effects (opacité, couleur) fast / default / slow | 1,0 | 3800 / 1600 / 800 | 0 | – | – / 2,4 / – | – / 3,6 / – | idem |
| **M3E LoadingIndicator** (déformation) | 0,6 | 200 | 9,5 % (progression bornée, rebond porté par l'échelle) | 6,9 im | 4,2 im | 10,5 im | `LoadingIndicator.kt` : changement de forme toutes les 650 ms, +90° par changement, 360° / 4 666 ms en continu |
| Apple `.smooth` (0,5 s) | 1,0 | 157,9 | 0 | – | 7,7 im | 11,6 im | doc Apple `Spring` |
| Apple `.snappy` (0,5 s, rebond 0,15) | 0,85 | 157,9 | 0,6 % | 11,9 im | 6,3 im | 8,3 im | idem |
| **Apple `.bouncy`** (0,5 s, rebond 0,3) | 0,7 | 157,9 | **4,6 %** | 8,8 im | 5,2 im | 11,9 im | idem |
| Apple `.spring()` par défaut | 0,825 | 157,9 | 1,0 % | 11,1 im | 6,1 im | 7,9 im | idem |
| Apple `interactiveSpring` | 0,86 | 1754,6 | 0,5 % | 3,7 im | 1,9 im | 2,6 im | idem |
| Apple « fluide », 80 % d'amortissement (réponse supposée 0,5 s) | 0,8 | 157,9 | 1,5 % | 10,4 im | 5,9 im | 7,5 im | WWDC18 803 |

**Penner, easeOutBack** (vérifié par calcul) : s = 1,70158 → **10,0 %** de dépassement, pic à 58 % de la durée. Pour un dépassement visé : **3 % → s = 0,90** ; **5 % → 1,17** ; **8 % → 1,50** ; 10 % → 1,70 ; **15 % → 2,16** ; 20 % → 2,59. Repère : ζ 0,6 ≈ 9,5 % ; ζ 0,7 ≈ 4,6 % ; ζ 0,8 ≈ 1,5 % ; ζ 0,9 ≈ 0,15 %.

### 2.4 Container transform converti pour une transition bulle → fenêtre de 20 images

| Canal | Progression (entrée) | Images (sur 20) |
|---|---|---|
| Fondu du contenu (vidéo / fond vert) | 0,00 → 0,25 | 0 → 5 |
| Masque de forme (bulle → rectangle) | 0,00 → 0,75 | 0 → 15 |
| Échelle / masque d'échelle | 0,00 → 1,00 | 0 → 20 |
| Variante avec arc : fondu / forme | 0,10 → 0,40 / 0,10 → 0,90 | 2 → 8 / 2 → 18 |
| Retour (outro) : fondu / forme | 0,60 → 0,90 / 0,30 → 0,90 | 12 → 18 / 6 → 18 |
| Voile (scrim) | noir à 32 % (`#52000000`) | à remplacer par l'indigo #240852 à environ 30 % |

---

## 3. Références secondaires ou écartées (et pourquoi)

| Référence | URL | Statut |
|---|---|---|
| Meta, logo en boucle (2021), « pensé pour vivre en mouvement et en 3D » | https://www.meta.com/design-at-meta/blog/designing-our-new-company-brand-meta/ · https://www.itsnicethat.com/news/creative-x-facebook-meta-branding-graphic-design-081121 | `[texte]` Pertinent pour le principe « motion first », moins pour les bulles. |
| Instagram, refonte 2022 : dégradé « éclairé de l'intérieur » (Rose Pilkington) | https://www.meta.com/design-at-meta/blog/behind-instagrams-brand-evolution-movement-inclusivity-and-a-new-purpose/ · https://www.creativeboom.com/news/instagram-reveals-its-first-brand-refresh-in-10-years-with-a-new-wordmark-and-three-typefaces/ | `[texte]` Utile pour un **dégradé vivant**. Aucune animation de glyphe documentée. |
| Deliveroo : **la refonte est de DesignStudio (2016), pas de Koto** | https://www.creativereview.co.uk/deliveroorebrand/ · https://www.dezeen.com/?p=967416 | `[texte]` Aucune spec motion trouvée. Faible pertinence. |
| Airbnb, Bélo (DesignStudio, 2014), film de lancement | https://www.dezeen.com/2014/07/16/airbnb-rebrand-designstudio-logo-belo/amp/ · https://www.creativereview.co.uk/the-airbnb-rebrand-10-years-on/ | `[texte]` Animation non décrite. |
| Revolut (refonte 2024 autour de la 3D et du motion) | https://medium.com/@arushidesigns01/revoluts-brand-evolution-a-look-at-the-old-vs-new-design-a576b57d8c3e | `[texte]` Sources de seconde main seulement. |
| Nickelodeon, « Splat » (Roger, 2023) : splat construit sur une grille circulaire | https://motionographer.com/quickie/nickelodeon-global-rebrand-2023-roger/ · https://www.designweek.co.uk/issues/10-july-14-july/nickelodeon-rebrand-roger-splat/ | `[texte]` Liquide « cartoon ». Animation non décrite. |
| Spotify Wrapped 2023 (Vucko), blog ingénierie | https://engineering.atspotify.com/2024/1/exploring-the-animation-landscape-of-2023-wrapped | `[texte]` Formes déformées. À voir si accessible. |
| British Airways « Windows » (Uncommon, 2024) : le hublot comme cadre | https://musebyclios.com/advertising/window-seats-british-airways-vibrant-ooh-is-poetry-in-motion/ · https://www.creativereview.co.uk/british-airways-reflections-uncommon-advertising/ | `[texte]` Affichage avec mouvement subtil. Pas de transition de hublot vers le film. **Je n'ai trouvé aucun film de compagnie aérienne documenté avec une transition « à travers le hublot ».** |
| Contexte Riyadh Air / Sfeer : FutureBrand (écosystème de marque, dont les sous-marques fidélité et cargo), PriestmanGoode (logo, livrée), Sonicbrand (identité sonore). Sfeer signifie « ambassadeur », mot rapproché de « sphere » par au moins une source de presse. | https://futurebrand.com/our-work/riyadh-air · https://www.designweek.co.uk/futurebrand-develops-new-brand-ecosystem-for-riyadh-air/ · https://www.priestmangoode.com/project/riyadh-air/ · https://www.adsoftheworld.com/campaigns/new-branding · https://onemileatatime.com/news/riyadh-air-loyalty-program/ | `[texte]` Le jeu sur « sphere » justifie la bulle, mais c'est à confirmer avec le client. Aucun film de lancement documenté. |

---

## 4. Protocole pour l'analyse image par image (une fois les vidéos récupérées)

1. Ramener la vidéo à 25 i/s et faire une planche numérotée :
   `ffmpeg -i ref.mp4 -vf "fps=25,scale=300:-1,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{frame_num}':x=8:y=8:fontcolor=white:box=1:boxcolor=black@0.6,tile=8x4" planche_%02d.png` (testé ici : 32 images numérotées par planche)
2. Sur chaque événement, noter : **image de départ, image du pic (dépassement ou écrasement), image de stabilisation**. Mesurer largeur / hauteur de la bulle à l'image du pic (ratio d'étirement) et le dépassement en % de la distance parcourue.
3. Pour une fusion ou séparation : **image du premier pont, image de cou minimal, image de rupture**, puis nombre d'images avant que les moignons disparaissent. Comparer avec le tableau Sato (§1, fiche 8).
4. Pour une fenêtre ou un iris : image où le contenu devient visible, image où le contour cesse d'être rond, image du plein cadre. Comparer avec le §2.4.
5. Reporter les mesures dans `specs_25ips.json` pour qu'elles puissent être reprises directement dans les animatiques.

---

## 5. Limites

- **Aucune image de référence n'a été vue.** Les sites vidéo et la plupart des sites éditoriaux sont bloqués : seuls npm, raw.githubusercontent.com et developer.apple.com ont répondu. Toutes les descriptions `[texte]` sont des paraphrases de résultats de recherche. Je n'ai pas lu les articles et des détails peuvent y manquer ou être déformés.
- Les règles marquées « proposition » (seuil de smear, parallaxe 0,6-0,8, anticipation de 10-20 %, respiration de ±1-2 %) **ne sont pas publiées**. Ce sont des points de départ à valider en animatique.
- Les durées publiées sont des durées d'interface (50-1 000 ms). Les transposer en bumper demande un facteur ×1,5-2 sur les gestes héroïques. Les profils de courbes et les dépassements, eux, se transposent tels quels.
- Le tableau de Sato mesure **l'algorithme publié**, pas la charte SFEER. La forme exacte du cou de la charte (`refs/charte/00-construction-bulle.png`) peut avoir d'autres paramètres `v` et `handle_len_rate`.
- La valeur de réponse 0,5 s du ressort « 80 % » d'Apple est une **hypothèse** : WWDC18 ne donne que l'amortissement.
