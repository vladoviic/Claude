# YOUR SAAS IS BORING : film promo de 52 s, 100 % code

« Your SaaS is boring. Lemme give it taste. » Un film 1920×1080, 30 i/s, 52 s, pour donner envie de
travailler avec Vladan (vladan@kwinndo.fr). C'est une **reconstruction plan par plan** de la vidéo de
référence, selon la méthode du PDF *How to Motionmaxx with Opus 5.5* : on garde le découpage, le timing,
la caméra et les transitions de la réf (mesurés image par image, voir `SPEC.md`) ; on change la marque,
les couleurs, les textes et les écrans.

- **L'histoire** : « Your SaaS is a bit *boring.* » → logo → « Make my furniture store less boring » →
  **velvetly**, la boutique de mobilier générée (l'équivalent de trailride dans la réf) : landing
  « Sit with *taste.* », fichiers (`NoMoreArial.tsx`, `Taste.tsx`), Build your Room, le salon vu d'en haut,
  « Lemme give it *taste* », Delivery & Install Status, le téléphone AR, My Orders,
  `npm uninstall boring --force`, la macro du fauteuil, le chat qui passe le velours du bleu au rouge,
  Order Complete, le Taste Check, les stats, « 47 boring issues → Apply taste », Ship it, montage, logo, e-mail.
- **Les images** : rendus photoréalistes Blender Cycles (`blender/`, sortie dans `img/`) à partir de
  modèles libres Khronos/Wayfair, crédits dans `img/CREDITS.md`. Studio à lumière de fenêtre pour le
  produit, vrai soleil par une fenêtre d'atelier pour le salon.
- **Le son** : synthétisé en code (`audio.py`), 135 BPM sur la grille de la réf, chaque bruitage calé
  sur l'image de son action, master à −14 LUFS.

## Lancer

```bash
pip install numpy scipy bpy      # + ffmpeg et Chromium/Playwright sur la machine
npm run images                   # (optionnel, plusieurs heures CPU) re-rend img/ avec Blender Cycles
                                 # séquences : python3 blender/prod.py final aerial,macro_seq,done_seq,land_seq,turn2,phone_seq
                                 # puis python3 blender/interp.py img/<dossier> <préfixe> <n> pour les images impaires

node render.mjs --serve          # aperçu dans le navigateur (espace : lecture, ← → : image)
node render.mjs --stills 70,440,735,1110,1500   # stills de contrôle → out/stills/
node render.mjs                  # 1560 images → out/frames/ + out/cues.json (≈ 12 min, 4 workers)
python3 audio.py                 # → out/audio.wav
sh build.sh                      # → out/saas-taste.mp4 (H.264, son à −14 LUFS)
```

## Où changer quoi

| Quoi | Où |
|---|---|
| Couleurs, typo | `style.css`, bloc `TOKENS` ; l'accent `#FF3D5E` est aussi dans le shader (`js/engine.js`) et `js/velvet.js` |
| Un plan | `js/shots1.js` (plans 1-16) et `js/shots2.js` (17-32) : un `scene(id, image début, image fin, rendu)` par plan, timings de la réf en commentaire |
| Textes | dans chaque plan (`WORDS`, `PROMPT`, `TREE`, terminal, `OUW` pour la fin) et dans les gabarits `js/screens.js` |
| Les écrans velvetly | `js/velvet.js` (landing, Build your Room, planning, My Orders, chat + page produit, Order Complete, profil) |
| Les écrans fades | `js/screens.js` et `js/dash.js` (le dashboard « avant ») |
| Les photos 3D | `blender/prod.py` : un `j_…` par image (cadrage, lumière, teinte du velours), `blender/room.py` : le salon |
| La musique | `audio.py` : grille 135 BPM, sections, niveaux |

Chaque image est une fonction pure du numéro d'image (`renderFrame(f)`) : pas de minuterie, aléatoire
seedé, donc n'importe quelle image se re-rend seule et le rendu est reproductible.

Polices incluses (licence OFL, voir `fonts/LICENCES.md`) : Inter Display, Instrument Serif,
JetBrains Mono, Liberation Sans (clone d'Arial, réservé aux écrans fades).
