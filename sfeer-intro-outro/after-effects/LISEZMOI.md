# La goutte dans After Effects

## Lancer
1. Ouvre ton projet After Effects (2018 ou plus récent).
2. Va dans **Fichier › Scripts › Exécuter le fichier de script…** et choisis `p07_la_goutte.jsx`.
3. Si After Effects demande l'accès aux fichiers, active **Préférences › Scripts et expressions › Autoriser les scripts à écrire des fichiers…**. Ce script n'écrit rien sur le disque, mais certaines versions demandent quand même l'autorisation.

Tout est créé en une seule étape d'annulation (Ctrl/Cmd + Z pour tout retirer).

## Ce que le script crée

Dossier **SFEER · La goutte** :

| Élément | Contenu |
|---|---|
| `SFEER_La_goutte_INTRO` | 4 s, 1920 × 1080, 50 i/s |
| `SFEER_La_goutte_OUTRO` | 4 s, 1920 × 1080, 50 i/s |
| `SFEER_La_goutte_MONTAGE (intro + film + outro)` | intro, 2 s de film, outro, bout à bout |
| Précompos › `VIDÉO · placeholder (remplacer par le film)` | plaque verte |

Calques, de haut en bas :

| Calque | Rôle |
|---|---|
| Logo · points | Points du logo (formes) |
| Logo · sfeer / Logo · سفير (arabe) / Logo · Powered by RIYADH AIR | Textes, révélés par un masque « Révélation » animé |
| Carton · poussée lente (échelle) | Nul parent des textes : la lente poussée du carton |
| Cache · fenêtre (goutte ∩ iris) | Cache alpha de la vidéo : la goutte intersectée avec l'iris d'ouverture (Fusion des tracés › Intersection) |
| VIDÉO · film dans la fenêtre | La précompo verte, avec l'échelle clée (contre-zoom de la plaque) |
| Goutte · bulle orange / Molécule · bulles orange | Calques de forme, un tracé par sous-forme |
| Fond · dégradé SFEER | Solide + effet Dégradé, indigo → lavande (verrouillé) |

Chaque temps fort du storyboard est posé en **repère de composition**, avec sa légende.

## À savoir
- **Clés image par image.** Les tracés sont clés à chaque image (50 i/s), avec la géométrie exacte de l'animatique. L'interpolation passe en « maintien » seulement quand le nombre de sommets d'un tracé change. Pour retoucher le timing, déplace des groupes de clés ou utilise le remappage temporel sur la compo.
- **Mettre le film.** Sélectionne le calque « VIDÉO · film dans la fenêtre », puis Alt-glisse (Option sur Mac) ton métrage depuis le panneau Projet. Ou remplace le contenu de la précompo placeholder : toutes les compos se mettent à jour.
- **Logo.** C'est un gabarit en Inter. Remplace les textes par le vectoriel officiel ·sfeer· / سفير en gardant les masques « Révélation ». Typo de marque : Loew Riyadh Air.
- **Dégradé.** L'effet Dégradé ne gère que deux couleurs. La charte met le milieu du dégradé à 70 % : pour être exact, remplace le fond par un calque de forme en dégradé à 3 arrêts (indigo, #5243A8 à 70 %, lavande).
- **Passer en 25 i/s.** Paramètres de composition › 25 i/s. Les clés restent à leur temps.
