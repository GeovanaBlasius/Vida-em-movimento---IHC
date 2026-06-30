from .exercicio_base import ExercicioBase
from src.config import META_ANGULAR, VIDEOS_INCLINACAO

class InclinacaoLateral(ExercicioBase):

    nome = "Inclinação Lateral"

    def __init__(
        self,
        lado,
        dificuldade
    ):
        super().__init__(
            lado,
            dificuldade
        )

        self.meta_angular = META_ANGULAR[lado]
        self.video_path = VIDEOS_INCLINACAO[lado]

