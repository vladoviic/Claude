#!/bin/sh
# Assemble out/frames/*.png + out/audio.wav → out/saas-taste.mp4
# Son normalisé à -14 LUFS (deux passes loudnorm, gain linéaire), vidéo H.264 4:2:0.
set -e
cd "$(dirname "$0")"
M=$(ffmpeg -hide_banner -i out/audio.wav -af loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -v error -i out/audio.wav -af "loudnorm=I=-14:TP=-1.0:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" -ar 48000 out/audio_master.wav
ffmpeg -y -v error -framerate 30 -i out/frames/%04d.png -i out/audio_master.wav \
  -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 256k -shortest out/saas-taste.mp4
echo "out/saas-taste.mp4"
