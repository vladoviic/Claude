# Brief dirigé (méthode Motion Lab)

Format et règles chiffrées adaptés de l'article de Florence (@flxrnc), « Opus 5.5 Motion Lab: Make Claude
Animate Like a Studio » (https://x.com/flxrnc/status/2105311836190978392), via ses deux portages libres
(MIT) : `plgonzalezrx8/motion-lab-grok-bot` et `Adamkyl69/motionmaker`. Le découpage plan par plan est
dans `SPEC.md` ; ce fichier fixe les chiffres que chaque plan doit tenir.

**GOAL.** Un fondateur de SaaS regarde 52 s et écrit à vladan@kwinndo.fr. Message unique :
*« Ton SaaS est fade, je lui donne du goût. »*

**OUTPUT.** 1920×1080, 30 i/s, 1560 images, H.264 4:2:0 (master 4:4:4), son AAC.
Chaque image est une fonction pure de son numéro.

**TIME.** Coupes et caméra de la réf, image pour image (`SPEC.md`).
- La réf coupe sur l'image, pas sur la grille : sur 80-190 BPM, aucune grille ne colle mieux que le hasard.
- Chaque coupe porte donc son bruitage (règle vérifiée par `qa/lab.py`).
- Musique : 135 BPM, premier temps à l'image 10. Chaque temps est calculé (`10 + n·13,33`), jamais additionné.

**LOOK.** Loi des couleurs :
- bleu `#2D6CDF` + Arial : le fondateur, l'ennuyeux (sur fond sombre, sa teinte claire `#6C9BF2`) ;
- rouge `#FF3D5E` : uniquement là où l'encre du stylo a coulé ;
- encre `#151413` sur papier `#EEE9E4` : le système ;
- Besley italique : le goût.

Hiérarchie des valeurs :
- un seul élément fort par image ;
- le contexte en valeurs moyennes ;
- ce qui est réglé vieillit vers le gris ;
- ce qui naît en couleur sèche à l'encre.

**MOTION.** Les chiffres viennent de `numbers.md` (Motion Lab).

| Rôle | Courbe | Durée |
|---|---|---|
| Entrée | ease-out-expo `0.16,1,0.3,1` (premium : quint `0.22,1,0.36,1`) | 600-900 ms héros, 200-500 ms UI |
| Déplacement, caméra | ease-in-out-quart `0.76,0,0.24,1` | — |
| Sortie | ease-in-expo `0.7,0,0.84,0` | 40-50 % plus courte que l'entrée |
| Ressort | amortissement 0,7-0,85 | la position peut rebondir, jamais l'opacité ni la couleur |

- Un seul mouvement héros par plan. Les secondaires vont 50-70 % aussi loin, avec 100-200 ms de retard. L'ambiant reste sous 5 %.
- Texte : 0,3 s par mot + 0,5 s. Il ne bouge pas pendant qu'on le lit ; une poussée de 2 % garde l'image vivante.

**SHOTS.** Voir `SPEC.md` ; chaque plan a un seul rôle (accroche, montée, résolution, fin).

**BANNED.**
- dégradés violet-bleu ;
- lueur, glow, bloom ;
- particules décoratives ;
- tout qui apparaît en fondu en même temps ;
- fondu + glissement vers le haut partout ;
- tout centré ;
- texte qui bouge pendant la lecture ;
- turntables gratuites ;
- fonds spatiaux sombres ;
- aplat rouge plein cadre qui n'est pas de l'encre.

**QA.**
- `qa/check.py` : texte, OCR du poster, curseurs.
- `qa/lab.py` sur le film exporté, avec ces seuils :

| Mesure | Seuil |
|---|---|
| Flashs (WCAG 2.3.1, approx.) | ≤ 3 par seconde |
| Tronçon mort | aucun ≥ 4 s |
| Tronçon vide | à lire, la réf en a aussi |
| Images bleu-violet | < 30 % |
| Coupe | un bruitage à ±1 image |

- Son :
  - −14 LUFS, crête vraie ≤ −1 dBTP mesurée sur le MP4 décodé ;
  - chaque bruitage tombe une image après son image (`LAG = 1` dans `audio.py`) : la lumière arrive avant le son.
- Boucle de labo :
  - stills → planches réf/nous → notes avec numéro d'image ;
  - une ou deux corrections par ronde ;
  - au plus 5 notes appliquées par ronde.
