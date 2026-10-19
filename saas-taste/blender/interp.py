"""Complète une séquence rendue « 1 image sur 2 » : les images impaires manquantes sont interpolées
par flux optique (ffmpeg minterpolate, compensation de mouvement).  python interp.py DOSSIER PREFIXE N"""
import os, re, subprocess, sys, tempfile, shutil
d, pre, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
have = sorted(int(m.group(1)) for f in os.listdir(d) if (m := re.fullmatch(rf'{pre}_(\d+)\.jpg', f)))
evens = [i for i in range(0, N, 2) if i in have]
missing = [i for i in range(N) if i not in have]
if not missing: sys.exit(0)
tmp = tempfile.mkdtemp()
for k, i in enumerate(evens): shutil.copy(f'{d}/{pre}_{i:02d}.jpg', f'{tmp}/s_{k:03d}.jpg')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '15', '-i', f'{tmp}/s_%03d.jpg',
                '-vf', 'minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1', '-q:v', '2', f'{tmp}/o_%03d.jpg'], check=True)
outs = sorted(f for f in os.listdir(tmp) if f.startswith('o_'))
# sortie k (base 1) ↔ temps (k-1)/30 s ↔ indice d'image 2·(k-1)/2 = k-1
for i in missing:
    src = f'{tmp}/o_{i + 1:03d}.jpg'
    if os.path.exists(src): shutil.copy(src, f'{d}/{pre}_{i:02d}.jpg')
    else: shutil.copy(f'{d}/{pre}_{max(j for j in have if j < i):02d}.jpg', f'{d}/{pre}_{i:02d}.jpg')
shutil.rmtree(tmp); print(d, 'interpolées :', len(missing))
