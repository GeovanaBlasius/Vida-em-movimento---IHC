"""
src/core/controle/controlador_exercicio.py
"""
from src.config import TOLERANCIAS

class ControladorExercicio:

    def __init__(self):

        self.contagem_pose = 0
        self.contagem_reps = 0

        self.fase = "BAIXO"

        self.movimento_valido = False

        self.dificuldade = "medio"

    # ======================================================
    # DIFICULDADE
    # ======================================================

    def definir_dificuldade(
        self,
        dificuldade
    ):

        dificuldade = dificuldade.lower()

        if dificuldade in TOLERANCIAS:

            self.dificuldade = dificuldade

    # ======================================================
    # CONTAGEM
    # ======================================================

    def incrementar(
        self,
        valor=1
    ):

        self.contagem_pose += valor

    def decrementar(self):

        self.contagem_pose = max(
            0,
            self.contagem_pose - 1
        )

    def resetar(self):

        self.contagem_pose = 0
        self.contagem_reps = 0

        self.fase = "BAIXO"

        self.movimento_valido = False
        
