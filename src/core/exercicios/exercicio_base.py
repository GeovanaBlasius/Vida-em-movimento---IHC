from src.config import (
    TOLERANCIAS,
    META_FRAMES
)

class ExercicioBase:

    nome = ""
    bilateral = False

    def __init__(
        self,
        lado,
        dificuldade
    ):

        self.lado = lado

        self.tolerancia = TOLERANCIAS[
            dificuldade.lower()
        ]

        self.meta_frames = META_FRAMES[
            dificuldade.lower()
        ]

        self.meta_angular = 0
        self.video_path = ""
        self.tipo = "frames"   # ← adiciona
        self.meta_reps = 10   

