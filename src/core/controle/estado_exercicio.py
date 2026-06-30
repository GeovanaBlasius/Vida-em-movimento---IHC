class EstadoExercicio:

    SEQUENCIA = [
        ("Inclinação Lateral",  "ESQUERDO"),
        ("Inclinação Lateral",  "DIREITO"),
        ("Elevação Frontal",    "ESQUERDO"),
        ("Elevação Frontal",    "DIREITO"),
        ("Elevação Lateral",    "BILATERAL"),
    ]

    def __init__(self):
        self.resetar()

    def resetar(self):
        self.etapa_atual = 0
        self.concluido = False

    @property
    def lado_atual(self):
        if self.etapa_atual < len(self.SEQUENCIA):
            return self.SEQUENCIA[self.etapa_atual][1]
        return None

    def proxima_etapa(self):
        self.etapa_atual += 1
        if self.etapa_atual >= len(self.SEQUENCIA):
            self.concluido = True

    def etapa_atual_info(self):
        if self.etapa_atual < len(self.SEQUENCIA):
            return self.SEQUENCIA[self.etapa_atual]
        return (None, None)
