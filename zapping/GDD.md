# ZAPPING : document de game design

> Arcade en un écran. Tu es le dernier signal d'un mur de téléviseurs rouges.
> Tu rallumes les écrans en passant dessus ; la neige (l'écran sans signal) te traque.
> Une partie dure 1 à 3 minutes. On rejoue tout de suite.

Prototype jouable : `prototype/index.html` (ouvre-le dans Safari ou Chrome sur ton Mac).
Les chiffres de la section « Réglages » sont les mêmes dans le prototype et dans la version Unreal.

---

## 1. Pourquoi ce jeu

| Choix | Justification |
|---|---|
| **Univers Mur Télé** | On réutilise la DA déjà validée chez marble.studio (bichromie rouge, CRT, l'œil). Le jeu devient une extension de l'univers, pas un projet à part. Cohérence de marque, zéro coût de recherche graphique. |
| **Un seul écran fixe** | Lisible en capture 9:16 (Reels, TikTok, Shorts). Chaque partie est un clip partageable sans montage. |
| **Grille 9 × 14** | Proche du 9:16. Le cadrage du jeu est le cadrage du réseau social. |
| **Parties courtes + record** | Boucle « encore une ». Le record est le moteur de rétention et de partage (« bats mon score »). |
| **Pas de personnage humain** | Le héros est un œil : aucun travail d'animation de personnage, ce qui garde le projet faisable à deux sur un MacBook Air. |
| **Tout émissif, pas d'éclairage réaliste** | Les écrans éclairent la scène. On coupe Lumen et Nanite, ce qui garde le jeu fluide sur une puce M sans ventilateur. |

**Cible** : 16-30 ans, joueurs mobiles et réseaux sociaux, sensibles à l'esthétique analogique (VHS, CRT, glitch).
**Promesse marketing** : « Garde le signal. » Un jeu qui se regarde autant qu'il se joue.

## 2. Boucle de jeu

1. Le signal (un œil) se déplace d'un écran à la fois (flèches, ZQSD, glisser sur mobile).
2. Chaque écran traversé s'allume en rouge : **+1 point**. Il s'éteint au bout de 9 s.
3. Un **œil** apparaît sur un écran au hasard : **+25 points**, mais une nouvelle neige apparaît.
4. La **neige** avance d'un écran à intervalle régulier, à 70 % vers toi, à 30 % au hasard (pour qu'on puisse l'esquiver). Elle éteint les écrans qu'elle traverse.
5. **Zap** (Espace, ou toucher) : saut de 3 écrans dans la dernière direction. Recharge 4 s.
6. Toucher la neige = fin. Le jeu accélère (la neige va plus vite, une neige de plus toutes les 20 s).

Tension centrale : prendre l'œil rapporte gros mais rend le mur plus dangereux.

## 3. Réglages (source de vérité)

| Paramètre | Valeur |
|---|---|
| Grille | 9 colonnes × 14 rangées |
| Durée d'un écran allumé | 9 s |
| Points écran / œil | 1 / 25 |
| Neiges au départ | 1, puis +1 toutes les 20 s, +1 par œil |
| Pas de la neige | 0,62 s, × 0,985 à chaque pas, minimum 0,24 s |
| Répit au départ | 1,5 s |
| Zap | 3 écrans, recharge 4 s |

## 4. Direction artistique

- **Palette** (reprise du générateur Mur Télé) : écran allumé ≈ 210/48/25, noirs bruns ≈ 30/14/12, coque ≈ 58/26/20, signal ≈ 255/122/77.
- **Écran** : dalle légèrement bombée aux coins carrés, lignes de balayage, reflet en haut à gauche, tirets « sans signal ».
- **Neige** : bruit animé teinté rouge, avec une barre de défilement verticale.
- **Caméra** : orthographique, face au mur. Lecture graphique et plate, comme une planche de manga. Pas de perspective qui déformerait la grille.
- **Post-process** : bloom fort, aberration chromatique légère, grain, vignette. Pas d'auto-exposition, pour garder un rouge constant.
- **Typo** : titre très gras (Dela Gothic One, qui vient du japonais : clin d'œil manga), interface en monospace.

## 5. Plan de construction dans Unreal (avec Claude via MCP)

Chaque étape est un prompt à envoyer à Claude Code une fois l'éditeur ouvert et connecté (voir README).
Sauvegarde (Cmd+S, « Save All ») avant et après chaque étape.

**Étape 1 : la dalle**
> Crée le matériau `M_Ecran` dans `/Game/Zapping/Materials` : émissif, paramètres scalaires `Allume` (0-1) et `Neige` (0-1), couleur éteinte 58/22/17, allumée 210/48/25, lignes de balayage via un sinus sur l'UV vertical, bruit animé quand `Neige` vaut 1. Puis une instance `MI_Ecran`.

**Étape 2 : le téléviseur**
> Crée `BP_Ecran` : une coque (cube aplati brun) et une dalle (plan) avec un Dynamic Material Instance de `MI_Ecran`. Fonctions `Allumer()`, `Neiger()`, et un Tick qui fait redescendre `Allume` en 9 s.

**Étape 3 : le mur**
> Crée la map `/Game/Zapping/Maps/L_Mur` vide. Crée `BP_Mur` qui génère 9 × 14 `BP_Ecran` en grille et garde un tableau d'état. Place une caméra orthographique cadrée sur le mur en 9:16, et un Post Process Volume (bloom, grain, vignette, aberration chromatique, exposition fixe).

**Étape 4 : le signal**
> Crée les Input Actions `IA_Bouger` (Vector2D) et `IA_Sauter`, un Input Mapping Context avec flèches, ZQSD et Espace. Crée le pawn `BP_Signal` qui se déplace d'une case à la fois sur la grille de `BP_Mur` avec une petite interpolation, et allume l'écran d'arrivée.

**Étape 5 : neige, œil, règles**
> Crée `BP_Neige` (avance toutes les 0,62 s, 70 % vers le joueur) et `BP_Oeil` (+25, fait apparaître une neige). Crée `BP_ZappingMode` (GameMode) qui gère le score, l'accélération, le zap et la fin de partie, avec les réglages de GDD.md section 3.

**Étape 6 : interface**
> Crée `WBP_Regie` (score, record, jauge de zap) et `WBP_Carton` (accueil et fin de partie). Sauvegarde le record avec un SaveGame `SG_Record`.

**Étape 7 : le son, puis l'export Mac**
> Ajoute un bruit blanc pour la neige, un « clic » de zapping par déplacement. Puis vérifie les réglages d'export Mac (Apple Silicon).

## 6. Budget performance (MacBook Air)

- 126 téléviseurs = 252 meshes très simples. Si besoin, passer en Instanced Static Mesh.
- Lumen, Nanite et Virtual Shadow Maps désactivés dans `Config/DefaultEngine.ini`.
- Pas de lumière dynamique : l'émissif + le bloom suffisent.
- Objectif : 60 i/s en jeu, éditeur en qualité « Moyenne » (Settings > Engine Scalability).

## 7. Idées pour la suite (à décider ensemble)

- Écrans « hero » qui diffusent tes planches de manga ou des médias de `mur-tele/sources/`.
- Mode 30 s « clip » pensé pour l'enregistrement d'écran.
- Classement partagé.
