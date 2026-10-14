# Grammaire « super motion » SFEER (intro / outro, 25 i/s)

Cette grammaire synthétise trois études image par image :

- **charte** : `refs/charte/analyse.md`, 35 poses clés de la charte mesurées au pixel ;
- **lottie** : `refs/lottie/ANALYSE.md`, 8 animations After Effects professionnelles décortiquées image par image ;
- **web** : `refs/web/references_web.md`, jetons de mouvement publiés par Material, IBM, Apple, Fluent et Shopify.

L'étude « moteurs metaball » n'a pas abouti (session d'agent interrompue). La géométrie mesurée sur la charte la remplace.

## Les règles

| # | Règle | Chiffres | Source |
|---|---|---|---|
| 1 | **La forme : congé constant, pas de flou.** Le col est un arc de rayon fixe R ≈ 0,93 r tangent aux deux bulles. En AE : Merge Paths (Add), Offset +R (joint rond), puis Offset −R. On n'anime que l'écart et les rayons. | col t = 2·(√((r+R)² − d²/4) − R) | charte |
| 2 | **La pose étirée vit au bord de la rupture.** Repos étiré à d = 3,3 r, avec un col de 7 % du diamètre. Le dépassement est permis jusqu'à 3,34 r. Au-delà, le col casse : c'est un choix, et il se met en scène. | rupture à 3,36 r | charte |
| 3 | **Le point se duplique, il ne se divise pas.** Le rayon reste constant à la division 3.3-01. On ne réduit pas les cercles pour « conserver le volume ». | aire ×2 | charte |
| 4 | **L'easing se choisit pour le col, pas pour la trajectoire.** Ease-out sur l'écart : départ explosif, le col s'étire sous les yeux. Ease-in : le col tient puis casse en 1 à 2 images (snap). | 10 images, out ou in cubique | charte |
| 5 | **Le ressort est dans la charte.** Le motif 3.6 rebondit avec un amortissement ζ ≈ 0,2, et chaque demi-oscillation vaut la moitié de la précédente. À utiliser pour tout atterrissage. | demi-période 5 images (2,5 Hz) | charte |
| 6 | **L'échange de tailles se fait à somme des rayons constante.** Amplitude ±40 %, centres immobiles, ease-in-out, et le receveur part avec 1 image de retard. | cycle de 26 images | charte, lottie 03 |
| 7 | **Accroche dès l'image 0.** La première image montre déjà quelque chose : 20 à 25 % du cadre, ou un point qui surgit. Jamais d'écran vide ni de fondu d'ouverture. | événement fort avant f006 | lottie 01, demande de la DA |
| 8 | **Anticipation avant chaque geste majeur.** La masse gonfle de 3 à 4 % ou recule avant de partir. | 3 à 7 images | lottie 01 et 05, charte |
| 9 | **Pop élastique.** 0 → 100 % en 5 images, 120 % à +7 images, 94 % à +4 images, puis 100 %. Chaque rebond vaut environ ⅓ du précédent. | 15 à 17 images au total | lottie 05 |
| 10 | **Fusion.** Convergence rapide (plus de 50 % du trajet dès la 1re image), puis la forme fusionnée s'étire (L/H jusqu'à 2,4) et revient au rond en 5 images. | `cubic-bezier(0.04,0.76,0.48,0.94)` | lottie 05 |
| 11 | **Une bulle qui file s'étire.** Le bord avant part en (0.3,0,0.3,1) et le bord arrière en (0.7,0,0.7,1). L'arrière claque sur l'avant. Étirement plafonné à ×1,35, volume conservé. | sx·sy = 1 | lottie 06 |
| 12 | **Traverser la fenêtre.** Une seule clé d'échelle en (0.6,0,0.15,1). Le vert remplit le cadre vers 43 % du temps, puis environ 7 images de décélération. La plaque vidéo zoome 2 fois moins vite (parallaxe). | 12 à 13 images | lottie 04 |
| 13 | **Décalages.** Pour un groupe, décaler de ⅔ de la durée du geste (3 images pour un geste de 5), ou de ¼ pour un relais. Entre gauche et droite : 2 à 4 images. | 2 à 4 images | lottie 07 |
| 14 | **Atterrissage signature et bannissement de l'Easy Ease.** Arrivées longues et soyeuses, avec une influence d'entrée de 88 %. L'Easy Ease par défaut (33 %) est mou. | arrivée `(0.12, 1)` | lottie, web M3 |
| 15 | **Sortie « accelerate ».** Presque rien, puis tout d'un coup : 15 % du trajet à mi-temps. Pour les aspirations. | `cubic-bezier(0.3,0,0.8,0.15)` | web M3 |
| 16 | **Aucun maintien mort.** Le carton logo garde toujours un mouvement : points qui respirent (±20 %), poussée lente (7,5 %/s), dérive linéaire. Contrôle automatique : aucune suite de 3 images identiques. | `tools/check_motion.py` | lottie 08, demande de la DA |

## Courbes nommées (moteur `tools/motion.py`)

| Nom | cubic-bezier | Usage |
|---|---|---|
| `emphase` | (0.2, 0, 0, 1) | apparitions, logo, recadrages |
| `plongee` | (0.7, 0, 0.15, 1) | traversée de la fenêtre |
| `anticipe` | (0.6, −0.28, 0.735, 0.045) | aspiration avec recul |
| `inout_expo` | (0.87, 0, 0.13, 1) | quart de tour, échanges rapides |
| `out_back` / `out_back_fort` | dépassement 10 % / 26 % | pop, naissances |
| `ressort`, `ressort_vif` | ζ 0,38 / 0,28 | atterrissages, impacts |

## Gabarit de temps (intro 4 s, outro 4 s)

**Intro**

| Images | Temps |
|---|---|
| f000–f006 | accroche |
| f006–f030 | mécanique de bulles (division, lien, échange) |
| f030–f060 | tension, puis moment fort |
| f060–f080 | la fenêtre s'ouvre |
| f080–f100 | plongée, puis raccord en mouvement |

**Outro**

| Images | Temps |
|---|---|
| f000–f016 | la vidéo se referme en bulle |
| f016–f060 | mécanique inverse, avec une variation |
| f060–f075 | arrivée sur les points du logo |
| f075–f100 | carton vivant |
