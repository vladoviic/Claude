# YOUR SAAS IS BORING : film promo de 52 s, 100 % code

« Your SaaS is boring. Lemme give it taste. » Un film 1920×1080, 30 i/s, 52 s, pour donner envie de
travailler avec Vladan (vladan@kwinndo.fr). C'est une **reconstruction plan par plan** de la vidéo de
référence, selon la méthode du PDF *How to Motionmaxx with Opus 5.5* : on garde le découpage, le timing,
la caméra et les transitions de la réf (mesurés image par image, voir `SPEC.md`) ; on change la marque,
les couleurs, les textes et les écrans.

- **L'histoire** : « Your SaaS is a bit *boring.* » → logo → on demande « Make my SaaS less boring » →
  la landing générée, les fichiers (`NoMoreArial.tsx`, `Taste.tsx`), le dashboard, la salière 3D,
  « Lemme give it *taste* », le planning, le téléphone, `npm uninstall boring --force`, la page produit,
  le Taste Check, les stats, « 47 boring issues → Apply taste », Ship it, montage, logo, e-mail.
- **La 3D** : salière en verre cannelé irisé et icônes tactiles en three.js (`three3d.js`).
- **Le son** : synthétisé en code (`audio.py`), 135 BPM sur la grille de la réf, chaque bruitage calé
  sur l'image de son action, master à −14 LUFS.

## Lancer

```bash
npm install                      # three.js
pip install numpy scipy          # + ffmpeg et Chromium/Playwright sur la machine

node render.mjs --serve          # aperçu dans le navigateur (espace : lecture, ← → : image)
node render.mjs --stills 70,440,735,1110,1500   # stills de contrôle → out/stills/
node render.mjs                  # 1560 images → out/frames/ + out/cues.json (≈ 12 min, 4 workers)
python3 audio.py                 # → out/audio.wav
sh build.sh                      # → out/saas-taste.mp4 (H.264, son à −14 LUFS)
```

## Où changer quoi

| Quoi | Où |
|---|---|
| Couleurs, typo | `style.css`, bloc `TOKENS` ; l'accent `#FF3D5E` est aussi dans le shader (`js/engine.js`) et `three3d.js` |
| Un plan | `js/shots1.js` (plans 1-16) et `js/shots2.js` (17-32) : un `scene(id, image début, image fin, rendu)` par plan, timings de la réf en commentaire |
| Textes | dans chaque plan (`WORDS`, `PROMPT`, `TREE`, terminal, `OUW` pour la fin) et dans les gabarits `js/screens.js` |
| Les écrans | `js/screens.js` (landing, palette ⌘K, pricing, planning, clients, chat produit, écrans fades) et `js/dash.js` (dashboard) |
| La 3D | `three3d.js` : salière (`shakerRender`) et icônes (`iconRender`) |
| La musique | `audio.py` : grille 135 BPM, sections, niveaux |

Chaque image est une fonction pure du numéro d'image (`renderFrame(f)`) : pas de minuterie, aléatoire
seedé, donc n'importe quelle image se re-rend seule et le rendu est reproductible.

Polices incluses (licence OFL, voir `fonts/LICENCES.md`) : Inter Display, Instrument Serif,
JetBrains Mono, Liberation Sans (clone d'Arial, réservé aux écrans fades).
