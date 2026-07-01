from src.config import VIDEOS_FRONTAL

from .exercicio_base import ExercicioBase

class ElevacaoFrontalUnilateral(ExercicioBase):

    nome = "Elevação Frontal"

    def __init__(
        self,
        lado,
        dificuldade
    ):
        super().__init__(
            lado,
            dificuldade
        )

        self.meta_angular = 85
        self.tipo = "reps"
        self.meta_reps = 10
        self.video_path = VIDEOS_FRONTAL[lado]

