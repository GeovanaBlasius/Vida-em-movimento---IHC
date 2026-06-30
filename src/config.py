"""
src/config.py
Configurações globais do projeto Vida em Movimento
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s [%(name)s] %(message)s"
)

# ===================================
# CAMINHOS
# ===================================

# Suporte ao modo frozen (executável gerado pelo PyInstaller)
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
ASSETS_DIR = BASE_DIR / "assets"

MODEL_PATH = BASE_DIR / "pose_landmarker_full.task"
IMG_AVISO = ASSETS_DIR / "Aviso.png"

VIDEOS_INCLINACAO = {
    "ESQUERDO": ASSETS_DIR / "exercicios" / "exercicio1.1.mp4",
    "DIREITO": ASSETS_DIR / "exercicios" / "exercicio01.mp4"
}

VIDEOS_FRONTAL = {
    "ESQUERDO": ASSETS_DIR / "exercicios" / "frontal_esquerdo.mp4",
    "DIREITO": ASSETS_DIR / "exercicios" / "frontal_direito.mp4"
}

VIDEOS_LATERAL = {
    "BILATERAL": ASSETS_DIR / "exercicios" / "elevacao_lateral.mp4"
}

# ===================================
# CONFIGURAÇÕES DE EXERCÍCIO
# ===================================

META_ANGULAR = {
    "ESQUERDO": 25,
    "DIREITO": -25
}

TOLERANCIAS = {
    "facil": 19,
    "medio": 16,
    "dificil": 12
}

META_FRAMES = {
    "facil": 180,
    "medio": 240,
    "dificil": 280
}

ETAPAS = ["ESQUERDO", "DIREITO"]

# ===================================
# CONFIGURAÇÕES DE VÍDEO
# ===================================

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 33

# ===================================
# CORES (BGR para OpenCV)
# ===================================

CORES = {
    "VERDE": (0, 220, 0),
    "VERMELHO": (0, 0, 255),
    "AMARELO": (0, 255, 255),
    "AZUL": (255, 0, 0),
    "BRANCO": (255, 255, 255),
    "PRETO": (0, 0, 0),
    "CINZA": (128, 128, 128)
}

# ===================================
# CONFIANÇA MEDIAPIPE
# ===================================

MIN_DETECTION_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

# ===================================
# MENSAGENS
# ===================================

MENSAGENS = {
    # Validação de posição
    "REALIZE_MOVIMENTO": "Realize o movimento",
    "ESTIQUE_BRACO": "Estique mais o braço",
    "INCLINE_MAIS": "Incline mais o corpo",
    "MUITO_BEM": "Muito bem! Continue assim",

    # Fases de repetição — feedback graduado para consciência corporal
    "LEVANTE_BRACO":      "Levante o braço",
    "CONTINUE_SUBINDO":   "Continue subindo...",
    "QUASE_LA":           "Quase lá! Suba mais",
    "BRACO_LEVANTADO":    "Ótimo! Agora abaixe",
    "ABAIXE_BRACO":       "Abaixe o braço",
    "MANTENHA_POSICAO":   "Mantenha a posição",
    # Correção de forma (reps)
    "ESTIQUE_COTOVELO":   "Estique o braço — mantenha-o reto",
    # Bilateral específico (reps)
    "LEVANTE_MAIS_ESQ":   "Suba mais: braço ESQUERDO",
    "LEVANTE_MAIS_DIR":   "Suba mais: braço DIREITO",
    # Inclinação Lateral — hierarquia de posição do braço
    "LEVANTE_COTOVELO":   "Levante o cotovelo acima do ombro",
    "LEVANTE_MAO_CABECA": "Levante a mão acima da cabeça",
    "ABAIXE_UM_POUCO":    "Abaixe um pouco o braço",

    # Transições
    "TROCANDO_LADO": "ÓTIMO! TROCANDO LADO...",
    "EXERCICIO_CONCLUIDO": "EXERCÍCIO CONCLUÍDO!"
}