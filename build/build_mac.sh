#!/bin/bash
# build_mac.sh - Build do instalador para Mac (.dmg)

set -e
cd "$(dirname "$0")/.."

echo "============================================"
echo "  Vida em Movimento - Build para Mac"
echo "============================================"
echo ""

echo "[1/3] Instalando dependencias..."
pip3 install "opencv-python>=4.13.0" "mediapipe==0.10.14" "numpy>=2.4.0" "PySide6==6.11.1" --quiet
pip3 install pyinstaller --quiet

echo "[2/3] Gerando .app com PyInstaller..."
pyinstaller VidaEmMovimento.spec --noconfirm

echo "[3/3] Criando instalador .dmg..."
mkdir -p instaladores

APP_PATH="dist/VidaEmMovimento/VidaEmMovimento.app"
DMG_PATH="instaladores/VidaEmMovimento-Mac.dmg"

rm -f "$DMG_PATH"

hdiutil create \
  -volname "Vida em Movimento" \
  -srcfolder "$APP_PATH" \
  -ov \
  -format UDZO \
  "$DMG_PATH"

echo ""
echo "============================================"
echo "  PRONTO!"
echo "  App:       $APP_PATH"
echo "  Instalador: $DMG_PATH"
echo "============================================"
echo ""
echo "Para distribuir: compartilhe o arquivo .dmg"
echo "A pessoa abre o .dmg e arrasta o app para Applications."
