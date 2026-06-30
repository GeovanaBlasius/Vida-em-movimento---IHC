@echo off
cd /d "%~dp0.."

echo ============================================
echo   Vida em Movimento - Build do Executavel
echo ============================================
echo.

echo [1/3] Instalando dependencias...
pip install "opencv-python>=4.13.0" "mediapipe==0.10.14" "numpy>=2.4.0" "PySide6==6.11.1" --quiet
pip install pyinstaller --quiet

echo [2/3] Gerando executavel...
pyinstaller VidaEmMovimento.spec --noconfirm
if errorlevel 1 (
    echo.
    echo [ERRO] Build falhou. Veja as mensagens acima.
    pause
    exit /b 1
)

echo [3/3] Gerando instalador...
if not exist instaladores mkdir instaladores

set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"

if not exist %ISCC% (
    echo.
    echo [AVISO] Inno Setup nao encontrado.
    echo   Baixe em: https://jrsoftware.org/isdl.php
    echo   Depois rode o build.bat novamente.
    echo.
    echo   Por enquanto o executavel esta em:
    echo   dist\VidaEmMovimento\VidaEmMovimento.exe
    pause
    exit /b 0
)

%ISCC% setup.iss
if errorlevel 1 (
    echo [ERRO] Falha ao gerar instalador.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   PRONTO!
echo   Instalador: instaladores\VidaEmMovimento-Setup-Windows.exe
echo ============================================
pause
