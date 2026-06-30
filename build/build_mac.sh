#!/bin/bash
# build_mac.sh - Build do executavel para Mac

set -e
cd "$(dirname "$0")/.."

echo "============================================"
echo "  Vida em Movimento - Build para Mac"
echo "============================================"
echo ""

echo "[1/3] Instalando dependencias..."
pip3 install "opencv-python>=4.13.0" "mediapipe==0.10.14" "numpy>=2.4.0" "PySide6==6.11.1" --quiet
pip3 install pyinstaller --quiet

echo "[2/3] Gerando executavel..."
pyinstaller VidaEmMovimento.spec --noconfirm

echo "[3/3] Compactando..."
rm -f VidaEmMovimento-Mac.zip
cd dist && zip -r ../VidaEmMovimento-Mac.zip VidaEmMovimento/ && cd ..

echo ""
echo "============================================"
echo "  PRONTO!"
echo "  App:  dist/VidaEmMovimento/VidaEmMovimento.app"
echo "  ZIP:  VidaEmMovimento-Mac.zip"
echo "============================================"
