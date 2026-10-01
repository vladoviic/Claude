# MUR TÉLÉ : mur de CRT, bichromie rouge, 9:16, boucle de 30 s

Générateur vidéo inspiré de la référence « mur de téléviseurs rouges » (l'œil au
centre, des écrans allumés sans signal, la silhouette, les branches).
Il produit un **MP4 1080×1920, 30 i/s, 30 s qui boucle sans couture** (la frame 900
retombe exactement sur la frame 0), prêt pour Reels / TikTok / Shorts.

- Sans médias, la démo reprend la composition de la référence : œil au centre,
  silhouette au-dessus, branches en dessous, macro d'iris dans les téléviseurs
  clairs, écrans allumés sans signal avec tirets, zapping ponctuel, et un « écho »
  de l'œil sur 5 écrans vers 18 s. Couleurs, interstices et façades sont calibrés
  sur les pixels de la réf. (écran vide ≈ 210/48/25, noirs bruns ≈ 30/14/12).
- Les scènes dessinées « manif », « crs », « feu », « slogan » existent toujours
  (clé `kind` du plan) mais ne sont plus dans la démo : elles font illustration.
  Pour s'approcher de la réf., il faut des photos ou des vidéos réelles.
- Dépose tes vrais médias dans `sources/` et relance : ils remplacent les scènes
  procédurales et passent automatiquement dans la même teinte rouge.

## Lancer

```bash
pip install numpy pillow        # + ffmpeg installé sur la machine
python render.py                # démo, ou utilise sources/ s'il contient des fichiers
python render.py --stills 2,9,17,26   # 4 PNG pour valider en quelques secondes
python render.py --seed 12      # autre tirage de la timeline
python render.py --plan out/plan_utilise.json   # rejouer / retoucher un plan précis
```

Le rendu complet prend environ 5 à 8 min sur 4 cœurs.

## Mettre tes images / vidéos

```
sources/
  hero/        -> écran central (le « héros », comme l'œil de la réf.), joués à la suite
  *.mp4 *.mov *.webm *.jpg *.png ...  -> répartis sur les autres écrans
```

- Vidéos : les 12 premières secondes sont lues en boucle et recadrées en « cover »
  sur l'écran. Les niveaux sont normalisés automatiquement avant la mise en teinte.
- Photos : Ken Burns lent (zoom de 14 % et dérive).
- Le reste du mur garde des écrans vides, de la neige, la mire et des slogans pour
  conserver le rythme de la référence, où environ la moitié des écrans ne montrent
  rien.

## Retoucher la timeline (direction artistique)

Chaque rendu écrit `out/plan_utilise.json` : 15 écrans × une liste de segments.

```json
{"row": 2, "col": 1, "timeline": [
  {"kind": "media", "src": "sources/hero/nahel_marche.mp4", "start": 0, "dur": 12, "seed": 1},
  {"kind": "oeil", "start": 12, "dur": 18, "seed": 4}
]}
```

| clé | rôle |
|---|---|
| `kind` | `media`, `blank`, `static`, `bars`, `slogan`, `manif`, `crs`, `feu`, `silhouette`, `fissures`, `oeil` |
| `start` / `dur` | en secondes. Un segment peut chevaucher la fin (ex. start 27, dur 6), c'est ce qui rend la boucle invisible |
| `src`, `offset` | fichier média et point d'entrée dans la vidéo |
| `osd` | `true` : incrustation caméra de surveillance (REC, CAM 03, timecode) |
| `chyron` | `true` ou un texte : bandeau « EN DIRECT » avec titre et ticker défilant |
| `text` | pour `slogan` : liste de lignes, ex. `["ON LÂCHE", "RIEN"]` |
| `contrast` | pour `media` : dureté de la courbe (1,25 par défaut) |

Grille : 5 rangées × 3 colonnes (`row` 0-4, `col` 0-2). Les colonnes de gauche et de
droite sont coupées par le cadre, comme sur la référence. Les moniteurs beiges sont
en (0,0), (2,2) et (4,1). L'écran héros est en (2,1).

Les réglages globaux sont en tête de `render.py` : `PALETTE` (gradient map de la
bichromie), `SLOGANS`, `CHYRONS`, `TICKER`, durée et fps. Pour une typo display
(Druk, Anton, etc.), dépose `fonts/display.ttf`.

## Où trouver les images (légalement)

L'environnement où ce mur a été généré n'avait pas accès aux sites de médias.
La démo est donc procédurale. Pistes, par ordre de sécurité juridique :

1. **Wikimedia Commons** (licences CC, crédit obligatoire, parfois partage à
   l'identique) : catégorie [Bloquons tout](https://commons.wikimedia.org/wiki/Category:Bloquons_tout)
   (mouvement de sept. à oct. 2025). Recherches utiles sur Commons : « gilets jaunes »,
   « réforme des retraites 2023 », « manifestation Paris 2023 », « lycée blocus ».
   Filtrer sur le type « vidéo » pour avoir des .webm.
2. **Banques libres** (Pexels / Pixabay) : de la foule, des fumigènes et des
   gyrophares génériques, pratiques comme fonds d'écran.
3. **Journalistes et collectifs indépendants** qui filment les cortèges et les
   blocus : demander l'autorisation, souvent accordée contre crédit. C'est la
   meilleure source pour les blocus lycéens récents.
4. **Agences** (AFP, Getty, SOPA Images) : sous licence payante. Les images de presse
   ou de JT reprises sans licence = contrefaçon, même recolorées.

Contexte récent : blocages de lycées en Île-de-France en 2026, avec une trentaine
d'interpellations ([Sud Radio / AFP](https://www.sudradio.fr/societe/blocus-de-lycees-franciliens-la-mobilisation-samplifie-le-ministre-denonce-une-instrumentalisation-politique)),
une journée à 75 lycées bloqués ([Hespress](https://fr.hespress.com/441738-journee-de-mobilisation-75-blocages-complets-ou-partiels-de-lycees.html)),
et le mouvement [Bloquons tout](https://en.wikipedia.org/wiki/Bloquons_tout) du 10 septembre 2025.

## À vérifier avant de publier

- **Mineurs** : les blocus lycéens filment surtout des moins de 18 ans. Floute ou
  pixelise les visages identifiables. La bichromie et la trame ne suffisent pas à
  anonymiser.
- **Vérification** : de vieilles vidéos d'émeutes (ou d'autres pays) circulent
  régulièrement comme « récentes » (voir les fact-checks de
  [Logically](https://logicallyfacts.com/en/fact-check/false-old-videos-from-2023-riots-in-paris-shared-as-arson-amid-2024-olympics)
  ou [Alt News](https://www.altnews.in/france-riots-unrelated-old-photos-ai-images-flood-social-mainstream-media/)).
  Garde la source et la date de chaque plan.
- **Violences policières** : la diffusion d'images de policiers en intervention est
  légale en France. Un floutage ne s'impose que pour certaines unités spécifiques.
  En revanche, identifier une victime ou une personne interpellée engage le droit
  à l'image et la présomption d'innocence.
- **Usage marque** : sur un contenu promotionnel (manga, studio), le reproche de
  « récupération » arrive vite. Un carton de contexte ou de crédits en fin de boucle,
  ou une légende sourcée, protège la crédibilité du projet.
