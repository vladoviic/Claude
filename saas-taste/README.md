# YOUR SAAS IS BORING : film promo de 33 s, 100 % code

« Your SaaS is boring. Lemme give it taste. » Un film 1920×1080, 30 i/s, 33 s, pour donner envie
de travailler avec Vladan (vladan@kwinndo.fr). Construit selon la méthode du PDF
*How to Motionmaxx with Opus 5.5* : la référence a été étudiée image par image (`SPEC.md`),
puis rebâtie plan par plan avec nos propres textes, couleurs et écrans.

- **Le gag** : un SaaS fade (« Saasly ») se fait auditer au stylo rouge, puis un curseur pousse
  un slider *taste* de 0 à 100 % : le dashboard se transforme composant par composant. Il pousse
  jusqu'à 140 %, tout déborde en irisé, « ok, *too much.* », retour sec à 100 %.
- **L'avant/après** : plat et générique → tactile (icônes 3D en argile, salière en verre irisé en
  three.js). Les références et ce qu'on en tire sont dans `SPEC.md` § 5.
- **Le son** : synthétisé en code (`audio.py`), 120 BPM, chaque bruitage calé sur l'image de son
  action via `out/cues.json`, master à −14 LUFS.

## Lancer

```bash
npm install                      # three.js
pip install numpy scipy          # + ffmpeg et Chromium/Playwright sur la machine

node render.mjs --serve          # aperçu dans le navigateur (espace : lecture, ← → : image)
node render.mjs --stills 68,190,278,430,960   # 5 stills de contrôle → out/stills/
node render.mjs                  # 990 images → out/frames/ + out/cues.json (≈ 10 min, 4 workers)
python3 audio.py                 # → out/audio.wav
sh build.sh                      # → out/saas-taste.mp4 (H.264, son à −14 LUFS)
```

## Où changer quoi

| Quoi | Où |
|---|---|
| Couleurs, typo | `index.html`, bloc `TOKENS` (`:root`) ; l'accent `#FF3D5E` est aussi dans le shader et `three3d.js` (`COL`) |
| Textes | `index.html` : `S1WORDS`, `ANN` (annotations de l'audit), `S5W` (mots du terminal), `S9W` + `#s9mail` (fin) |
| Timing | chaque scène est une fonction `sN(f)` ; les cues son sont déclarés à côté (`cue(f, ...)`) |
| Le dashboard | `buildDash()` / `updateDash()` : un seul composant, 8 « composants de goût » de 0 à 1 |
| La 3D | `three3d.js` : salière (`shakerRender`) et icônes (`iconRender`) |
| La musique | `audio.py` : progression `PROG`, sections, niveaux (`PAD`, gains des bus) |

Chaque image est une fonction pure du numéro d'image (`renderFrame(f)`) : pas de minuterie, aléatoire
seedé, donc n'importe quelle image se re-rend seule et le rendu est reproductible.

Polices incluses (licence OFL) : Inter Display, Instrument Serif, JetBrains Mono, Liberation Sans
(clone d'Arial, réservé au SaaS ennuyeux).
