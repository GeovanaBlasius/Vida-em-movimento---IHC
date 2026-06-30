from src.config import VIDEOS_LATERAL

from .exercicio_base import ExercicioBase

class ElevacaoLateralBilateral(ExercicioBase):

    nome = "Elevação Lateral"
    bilateral = True

    def __init__(
        self,
        lado,
        dificuldade
    ):
        super().__init__(
            "BILATERAL",
            dificuldade
        )

        self.meta_angular = 85
        self.tipo = "reps"
        self.meta_reps = 10
        self.video_path = VIDEOS_LATERAL["BILATERAL"]

