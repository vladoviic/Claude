# SPEC v3 — reconstruction plan par plan de la référence

« Your SaaS is boring. Lemme give it taste. » Film promo pour Vladan (vladan@kwinndo.fr).
Méthode du PDF *How to Motionmaxx with Opus 5.5* appliquée à la lettre : **on garde** le découpage,
le timing, la caméra, les positions, le flou et les transitions de la réf ; **on change** la marque,
les couleurs, les textes et les écrans. Les numéros d'image sont ceux de la réf (30 i/s, base 0).

**Une seule déviation** : la tenue finale passe de 0,8 s à 2,3 s pour laisser lire l'e-mail
(1560 images = 52 s au lieu de 1514).

## Mesures de la réf (736×414 → converties en 1920×1080)

| Mesure | Valeur |
|---|---|
| Fond | papier `#EEE9E4`, sombre `#1D1D1D`, ciel pêche → bleu pâle |
| Tempo | 135 BPM, premier temps à 0,33 s (image 10), 1 temps = 13,33 images |
| Texte courant / logo | 50 px / marque 78 px + mot 64 px |
| Pills | 78 px de haut, texte 42 px, contour 3 px ; décalé de 6 images entre éléments |
| Écrans | 1440 px de large dans un cadre noir de 12 px, rayon 18 |
| Terminal | texte ~110 px, frappe ≈ 1 car. / 2-3 images |
| Énergie du son | calme 0-4 s · drop au logo (4 s) · fort 4-20 s · break 22-28 s (terminal, macro) · retour 28-34 s · creux 34-36 s (check) · fort 36-46 s · fin calme |

## Plans

| # | Images réf | Réf | Nous |
|---|---|---|---|
| 1 | 0-53 | `/`, `//`, « How » → « How far » → « can » → « can your », glyphes qui s'ajoutent | mêmes glyphes, « Your » → « Your SaaS » → « is » → « is a » |
| 2 | 54-92 | « can your apps » + fragments de code ; « your apps **go?** » + 5 images autour, teintées irisé 9 images puis normales ; les mots partent un par un | « is a bit » + CSS ringard (`font-family: Arial;`…) ; « a bit **boring.** » + 5 écrans de SaaS fades |
| 3 | 93-119 | les images convergent en collage au centre, rétrécissent, passent en irisé | idem avec nos écrans fades |
| 4 | 120-173 | blob irisé → cercle lilas/cyan → rose/pêche → icône → mot « Base 44 » (141), tenue | → marque (cercle + « / ») → « vladan » |
| 5 | 174-207 | champ de prompt, frappe ~1,8 car./image, curseur, clic sur Envoyer (206) | « Make my SaaS less boring. It's blue, it's Arial, and there's a stock handshake. » |
| 6 | 207-233 | glyphes autour du champ, le fond devient irisé, le champ se dissout dans le thermique | idem |
| 7 | 234-299 | landing générée dans un cadre, recul caméra, puis petite à droite + « › Code Files » (282) | landing « Dashboards with *taste.* » + salière 3D ; « › Taste Files » |
| 8 | 300-347 | l'arborescence se déplie (un élément toutes les 3-6 images), dernier élément en noir | `Brand.ts`, `Typography.ts`, `Components` › `NoMoreArial.tsx`, `OneAccent.tsx`, `EaseOut.tsx`, **`Taste.tsx`** |
| 9 | 348-380 | app « Build your Route » qui se remplit | dashboard Saasly soigné qui se remplit |
| 10 | 381-419 | photo plein cadre, push-in lent | salière 3D plein cadre qui saupoudre |
| 11 | 420-467 | icône (420) · « Connect to » (426) · « Calendar » (432) · icône noire (444) · resserrage (447-459) · traînée (462) | « Lemme give it » · salière · « *taste* » |
| 12 | 468-533 | barres colorées floues → grille de calendrier → UI complète | barres → planning « Taste plan » |
| 13 | 534-560 | zoom sur les puces du calendrier, 3 panoramiques coupés (534, 543, 552) | zoom sur « Kill Arial », « Type system », « Motion pass »… |
| 14 | 561-641 | téléphone : écran irisé → contenu, rubans holographiques, compteurs ; « Ride Complete » (606) | téléphone : score de goût 8.6 → 9.2 ; « Taste applied » |
| 15 | 642-671 | dashboard « My Rides » dans un navigateur, curseur | « My clients : before → after » |
| 16 | 672-695 | gros plan de la barre d'outils, curseur sur la 1re icône, clic (690) | 1re icône = salière |
| 17 | 696-749 | sombre : « → \| », frappe « git push », « origin » (732) et « main » (738) surlignés | « npm uninstall », « boring » et « --force » surlignés |
| 18 | 750-767 | « → push main » → « .cain » → « .collap » dans un cadre | « → add *taste* » → « mo » → « motion » |
| 19 | 768-815 | éditeur de code qui se tape, push-in, passage au noir | `export const taste = { … arial: false }` |
| 20 | 816-879 | macro N&B (pièce de vélo) qui s'allume, curseur, recul, filé | macro N&B 3D du bouchon de la salière |
| 21 | 880-953 | chat IA + page produit, vélo 3D qui tourne, changement de modèle (918-927) | « Add a 3D hero. Make it salty. » + salière qui tourne, bouchon qui change |
| 22 | 954-989 | carte « Order Complete », zoom | « Taste Complete » |
| 23 | 990-1052 | plein cadre, le thermique s'étend, bouton « Start Security Check », clic (1050) | « Start Taste Check » |
| 24 | 1053-1079 | grille blanche, le thermique se casse en blocs | idem |
| 25 | 1080-1130 | collage sur grille : irisé, macro N&B, stats +15 % → +45 % | stats marketing : +45 % inscriptions, rebond 5.9 → 2.8 |
| 26 | 1131-1175 | fond irisé pastel, carte « DamageReport », clic « Apply Fixes » (1161) | « BrandReport · 47 boring issues » → « Apply taste » |
| 27 | 1176-1250 | sombre : ⚠ rouges → cercles verts → convergence → bouclier (1233) | ⚠ rouges → cercles → convergence → notre marque |
| 28 | 1251-1307 | ciel, bouton « Publish », curseur, clic (1293) | « Ship it » |
| 29 | 1308-1373 | montage : 1308 · 1326 · 1338 · 1350 | palette ⌘K · pricing · dashboard · landing |
| 30 | 1374-1391 | la landing passe en thermique → fragments de code → glyphes qui convergent | idem |
| 31 | 1392-1445 | cercle → icône → « Base 44 » | → « vladan » |
| 32 | 1446-1514 | pill tapée « Build » · « Build it » · « Build it your way », flash, la pill disparaît | « Give » · « Give it » · « Give it *taste.* » ; puis **vladan@kwinndo.fr** jusqu'à 52 s |

## Règles visuelles (une seule fois, ici)

- Accent unique `#FF3D5E` (remplace l'orange de la réf), encre `#151413`, papier `#EEE9E4`.
- Inter Display (texte, UI), Instrument Serif italique (*taste* et ses échos), JetBrains Mono (code, glyphes).
- Arrivée rapide, fin douce : exponentielle × (1−t)², vitesse nulle à l'arrivée. Flou de mouvement
  dans l'axe du déplacement, jamais à travers une coupe. Push-in lent pendant les tenues.
- Chaque image est une fonction pure du temps ; aléatoire seedé.
