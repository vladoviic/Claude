#!/usr/bin/env bash
# ZAPPING - vérifie ton Mac, active l'auto-démarrage du serveur MCP,
# puis ouvre le projet dans Unreal Editor.
# Usage :  bash preparer-mac.sh            (vérifie + ouvre)
#          bash preparer-mac.sh --verifier (vérifie seulement)
# Compatible avec le bash 3.2 livré avec macOS.

set -u
cd "$(dirname "$0")" || exit 1
PROJET="$PWD/Zapping.uproject"
UE_VERSION="5.8"
UE_RACINE="${UE_RACINE:-/Users/Shared/Epic Games/UE_${UE_VERSION}}"
UE_APP="$UE_RACINE/Engine/Binaries/Mac/UnrealEditor.app"
ok()    { printf '  \033[32mOK\033[0m   %s\n' "$1"; }
alerte(){ printf '  \033[33m!!\033[0m   %s\n' "$1"; }
erreur(){ printf '  \033[31mKO\033[0m   %s\n' "$1"; BLOQUANT=1; }
BLOQUANT=0

echo "ZAPPING : vérification du Mac"

if [ "$(uname -s)" != "Darwin" ]; then
  erreur "Ce script est fait pour macOS."
  exit 1
fi

if [ "$(uname -m)" = "arm64" ]; then ok "Puce Apple Silicon"
else alerte "Mac Intel : Unreal 5 tournera, mais lentement."; fi

RAM_GO=$(( $(sysctl -n hw.memsize) / 1073741824 ))
if [ "$RAM_GO" -ge 16 ]; then ok "Mémoire : ${RAM_GO} Go"
else alerte "Mémoire : ${RAM_GO} Go. Ça passe pour ZAPPING, mais ferme les autres apps (Chrome, Photoshop)."; fi

LIBRE_GO=$(df -g "$HOME" | awk 'NR==2 {print $4}')
if [ "$LIBRE_GO" -ge 80 ]; then ok "Disque libre : ${LIBRE_GO} Go"
else erreur "Disque libre : ${LIBRE_GO} Go. Il en faut environ 80 (moteur + cache des shaders)."; fi

if [ -d "$UE_APP" ]; then ok "Unreal Engine ${UE_VERSION} trouvé"
else
  erreur "Unreal Engine ${UE_VERSION} introuvable dans : $UE_RACINE"
  echo "         Installe-le avec l'Epic Games Launcher (onglet Unreal Engine > Bibliothèque)."
  echo "         Installé ailleurs ? Relance avec : UE_RACINE=\"/chemin/UE_${UE_VERSION}\" bash preparer-mac.sh"
fi

if xcode-select -p >/dev/null 2>&1; then ok "Outils Xcode présents"
else alerte "Xcode absent : pas grave pour jouer dans l'éditeur, nécessaire pour exporter une app .app."; fi

if command -v claude >/dev/null 2>&1; then ok "Claude Code installé"
else alerte "Claude Code absent : voir https://code.claude.com pour l'installer."; fi

# Copie per-user du réglage d'auto-démarrage (en plus de Config/DefaultEditorPerProjectUserSettings.ini)
INI_DIR="$PWD/Saved/Config/MacEditor"
INI="$INI_DIR/EditorPerProjectUserSettings.ini"
mkdir -p "$INI_DIR"
if ! grep -q "bAutoStartServer" "$INI" 2>/dev/null; then
  {
    echo ""
    echo "[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]"
    echo "bAutoStartServer=True"
  } >> "$INI"
fi
ok "Serveur MCP réglé pour démarrer avec l'éditeur (port 8000)"

if [ "$BLOQUANT" -ne 0 ]; then
  echo ""
  echo "Corrige les points KO puis relance le script."
  exit 1
fi

if [ "${1:-}" = "--verifier" ]; then
  echo ""
  echo "Tout est prêt. Lance sans --verifier pour ouvrir le projet."
  exit 0
fi

echo ""
echo "Ouverture de ZAPPING dans Unreal Editor..."
echo "La première ouverture compile les shaders : compte 10 à 30 min sur un MacBook Air."
open -a "$UE_APP" --args "$PROJET"
echo ""
echo "Quand l'éditeur est ouvert, dans un Terminal :"
echo "  cd \"$PWD\" && claude"
