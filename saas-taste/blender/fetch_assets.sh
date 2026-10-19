#!/bin/sh
# Télécharge les modèles glTF (Khronos glTF-Sample-Assets) dans ../assets/khr (non versionnés).
set -e
cd "$(dirname "$0")/.." && mkdir -p assets/khr
B=https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models
for m in SheenChair GlamVelvetSofa SpecularSilkPouf GlassVaseFlowers DiffuseTransmissionTeacup DiffuseTransmissionPlant IridescenceLamp; do
  [ -f assets/khr/$m.glb ] || curl -sfL -o assets/khr/$m.glb $B/$m/glTF-Binary/$m.glb
done
echo "assets/khr prêt"
