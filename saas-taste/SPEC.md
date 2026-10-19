# SPEC — « Your SaaS is boring. Lemme give it taste. »

Film promo de 34,5 s pour Vladan (vladan@kwinndo.fr), construit en code selon la méthode
du PDF « How to Motionmaxx with Opus 5.5 » : référence → étude image par image → brief →
règles visuelles → plans → stills → motion → son → critique → rendu final.

## 1. Étude de la référence (`ref.mp4`, 736×414, 30 i/s, 50,47 s, 1514 images)

Mesures faites en code (`ffmpeg` → PNG, différence d'images, boîtes englobantes, pixels) :

| Mesure | Valeur relevée |
|---|---|
| Fond papier | `rgb(238,233,228)` = `#EEE9E4` (médiane sur 9 images, constante) |
| Fond scènes sombres | `rgb(29,29,29)` = `#1D1D1D` |
| Texte courant | ≈ 4,6 % de la hauteur (≈ 50 px en 1080p), centré, grotesque fine |
| Pills | hauteur ≈ 9 % de l'image (≈ 96 px en 1080p), contour encre ≈ 4 px, texte ≈ 52 px |
| Arrivée en décalé | icône f420 → « Connect to » f424-430 → « Calendar » f434 : **8 images** entre éléments |
| Glissements | regroupement des pills f446→f460 : **14 images**, arrivée rapide, fin douce |
| Tenue du logo | x 297→291 sur 28 images : push-in lent ≈ 0,07 %/image, jamais figé |
| Typo de fin | le texte se tape mot par mot dans une pill (≈ 6 images/mot), puis la pill disparaît (f1488) et le texte reste 1 s |
| Coupes (pics de différence) | 2,07 · 9,33 · 11,57 · 12,67 · 13,93 · 17,73 · 21,40 · 22,40 · 23,17 · 29,33 · 31,73 · 33,43 · 37,67 · 39,17 · 41,67 · 43,57 · 44,17 · 44,97 s |
| Son | intro calme (−22 dB RMS) 0-4 s, drop sur le logo à 4 s, break calme sur la scène sombre (22-28 s), retour à 28 s, tempo ≈ 136 BPM |

Grammaire visuelle observée :
1. Ouverture : glyphes de code (`/ < > * |`) éparpillés autour d'un mot centré qui change à chaque temps (« How far » → « can » → « your apps » → « go? »). Quelques glyphes en couleur d'accent.
2. Fragments d'UI et de code qui envahissent le cadre autour du texte.
3. Pills à contour fin, entrée en décalé, clic au curseur, sortie en traînée floue horizontale (couleur d'accent).
4. Champs irisés (pêche, rose, lilas, cyan) qui servent de transition et de fond.
5. Scène sombre : frappe d'une commande (`→ git push origin`) avec sélection surlignée, puis le 2ᵉ mot change à chaque temps.
6. Bouton noir sur dégradé de ciel, curseur, clic → montage d'écrans qui claquent sur le temps.
7. Fragments qui convergent en un point → logo → pill tapée → texte seul.

## 2. Brief

| Garder | Changer | Interdit |
|---|---|---|
| Rythme (un changement par temps), décalés de 8 images, arrivée rapide / fin douce | Marque : Vladan, accent unique rose-rouge `#FF3D5E` | Dégradés au hasard |
| Fond papier `#EEE9E4`, fond sombre `#1D1D1D` | Typo : Inter Display + Instrument Serif italique pour le mot « taste » | Tout qui apparaît en fondu |
| Glyphes de code, pills à contour, curseur, champs irisés, frappe | Texte : la blague du SaaS ennuyeux, en anglais | Lueur sur le texte |
| Bouton sur ciel, montage d'écrans, convergence → logo → pill de fin | Écrans : un faux SaaS volontairement fade (« Saasly ») puis sa version avec du goût | Bursts de particules |
| Flou de mouvement directionnel, coupe sur le temps | Musique : 120 BPM synthétisée en code, bruitages calés à l'image | Deux choses qui se battent pour l'attention |

## 3. Règles visuelles (une seule fois, ici ; `index.html` → `TOKENS`)

- 1920×1080, 30 i/s, **120 BPM → 1 temps = 15 images, 1 mesure = 60 images**. Toute coupe tombe sur un temps ou 2 images avant.
- Couleurs : papier `#EEE9E4`, encre `#151413`, gris `#8E877F`, sombre `#1D1D1D`, accent `#FF3D5E`. Irisé : pêche `#FFC7A1`, rose `#FFA6C9`, lilas `#C7B8FF`, cyan `#A9E7F2`, beurre `#FFF0B5`.
- Typo : Inter Display 500 (mots, UI), Instrument Serif italique (le mot *taste* et ses échos), JetBrains Mono (glyphes, code, annotations). Liberation Sans (clone d'Arial) **uniquement** pour le SaaS ennuyeux.
- Texte courant 52 px ; pills 96 px de haut, contour 4 px.
- Mouvement : décroissance exponentielle (≈ 12 % de la distance restante par image) × (1−t)², donc départ rapide et vitesse nulle à l'arrivée. Jamais de vitesse constante, jamais d'arrêt sec. Mouvements ≥ 0,3 s (9 images), grands mouvements 15-22 images.
- Rien ne fige : push-in caméra ≈ 0,1-0,2 %/image pendant les tenues.
- Groupes décalés de 2 à 8 images. Un texte reste immobile ≥ 8 images avant de bouger.
- Flou de mouvement dans l'axe du déplacement (SVG `feGaussianBlur` anisotrope), nul à l'arrêt, jamais à travers une coupe.
- Un seul point focal par image.
- Chaque image est une fonction pure du temps (`renderFrame(f)`), aucune minuterie, aléatoire seedé.

## 4. Liste des plans

| # | Images | Temps | Contenu | Son |
|---|---|---|---|---|
| 1 | 0-89 | 0-3 s | Papier. Glyphes éparpillés, un mot par temps : « Your » · « SaaS » · « is » · … puis **« boring. »** en Arial gris (f60). « (no offense) » en mono à f76. | Plucks discrets sur les temps, tick par glyphe ; **tout s'arrête** sur « boring. » + bruit sourd |
| 2 | 90-209 | 3-7 s | L'audit : le SaaS fade (gris, Arial, bleu `#2D6CDF`, ombre portée, poignée de main stock). Annotations en stylo rouge qui tombent toutes les 8 images (« Arial. Bold choice. », « #2D6CDF, like every SaaS ever », « drop shadow from 2009 »…), compteur « 47 boring issues ». | Tic-tac de pendule (musique d'ascenseur), tick par annotation |
| 3 | 210-299 | 7-10 s | « Lemme » · « give it » · pill [*taste*] en décalés de 8 images. Curseur, clic f262, la pill passe à l'accent et part en traînée floue (f270-285), champ irisé. | Riser, clic f262, whoosh qui culmine f278 |
| 4 | 300-509 | 10-17 s | Le curseur saisit un slider « *taste* 0 % » et le pousse : le SaaS se transforme composant par composant (typo, fond, sidebar, KPI, graphe, salutation, bouton, visuel). 100 % à f420. Il pousse encore : 140 %, le cadre sature d'irisé, « ok, too much. » → retour sec à 100 %. | **Drop** f300. Une note montante par composant transformé. Montée filtrée, puis rembobinage sec au retour |
| 5 | 510-629 | 17-21 s | Sombre. Frappe « → npm uninstall boring », « boring » surligné, entrée. Puis « → install » + mot qui change à chaque temps : *taste*, rhythm, motion, typography, restraint. Log fantôme derrière. | Break : nappes seules + frappe clavier |
| 6 | 630-689 | 21-23 s | Ciel pastel, bouton noir « Ship it », curseur, clic f660. | Clic f660, riser |
| 7 | 690-854 | 23-28,5 s | Montage de 5 écrans, 1 s chacun (2 temps), qui claquent sur f690 · f720 · f750 · f780 · f810 : dashboard · landing héros 3D (la salière saupoudre, les lettres de *taste.* tombent comme des grains) · palette ⌘K (« remove Arial » → meilleure suggestion « Add *taste* » ⏎) · pricing Bland / Tasteful / Chef (l'interrupteur passe à *tasteful*, Bland se fait rayer) · mobile Liquid Glass (notification en verre, anneau 92 %). Envol vers la caméra à f840. | Drop + impact par écran, frappe, Entrée, clic, stylo, whoosh f850 |
| 8 | 855-914 | 28,5-30,5 s | Les glyphes convergent en un point accent → marque (cercle + « / ») + « vladan ». | **Impact le plus fort** à f871 |
| 9 | 915-1034 | 30,5-34,5 s | Pill tapée mot par mot : « Let's give yours taste. » puis l'e-mail **vladan@kwinndo.fr**, la pill disparaît, texte seul jusqu'à la fin. | Accord final qui résonne (f960) |

## 5. Direction de l'« après » : plat → tactile

L'avant est le SaaS générique : Arial, bleu `#2D6CDF`, ombres portées, icônes plates au trait,
photo stock en placeholder. L'après ne se contente pas d'être « propre » : il devient **tactile**.

| Référence | Ce qu'on en prend (principe, jamais la marque) |
|---|---|
| Linear, Vercel | Retenue : monochrome, la couleur seulement quand elle veut dire quelque chose → un seul accent, réservé à la valeur clé (dernière barre, +18 %, le bouchon). |
| Stripe, Mercury | Une donnée héros d'abord (« $128.4k » en 62 px), le reste en mono discret. |
| Airbnb, été 2025 (icônes 3D animées) | La sidebar passe d'icônes plates à des **icônes 3D en argile** (tuiles, barres, buste, bouton rotatif) qui bougent doucement. |
| Apple Liquid Glass / Moonlitt (Apple Design Award 2026, Interaction) | Le verre comme matière : la **salière en verre cannelé irisé** (three.js) dans la carte « Q3 tastes *delicious.* » et en héros de la landing, où elle saupoudre. |
| Family (Benji Taylor) | Continuité par le mouvement : le bouton « Ship it » devient l'écran, l'irisé sort de la carte et y retourne. |
| Raycast, Linear (palette de commandes) | Écran ⌘K en verre sombre : la blague « Best match: Add *taste* » quand on tape « remove Arial ». |
| Vercel, Attio (pricing) | Trois formules très typographiques, une seule mise en avant (la noire), l'accent réservé au badge et au rayé. |
| Awwwards, Site of the Year 2025 | Landing éditoriale : titre à 214 px, l'objet 3D passe devant la typo. |

La salière fait le lien avec le jeu de mots (*taste* = goût) : icône 2D au plan 3, objet 3D dans l'après.
Réseau de l'environnement de fabrication : seuls npm et GitHub étaient joignables (pas de banque
d'images ou de vidéos), donc toute la 3D est modélisée en code (`three3d.js`).

## 6. Stills à valider avant le rendu complet

1. Ouverture (f68 : « boring. ») · 2. Composition principale (f190 : l'audit) · 3. Produit (f430 : SaaS à 100 %) · 4. Transition la plus rapide (f278 : traînée) · 5. Carte de fin (f1005).
