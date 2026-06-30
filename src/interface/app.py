from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget
)

from PySide6.QtCore import (
    QPropertyAnimation
)

from PySide6.QtWidgets import (
    QGraphicsOpacityEffect
)

from src.interface.telas.tela_inicial import TelaInicial
from src.interface.telas.tela_dificuldade import TelaDificuldade
from src.interface.telas.tela_exercicio import TelaExercicio
from src.interface.telas.tela_final import TelaFinal

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()

        self.tela_inicial = TelaInicial(
            self.abrir_dificuldade
        )

        self.tela_dificuldade = TelaDificuldade(
            self.iniciar_exercicio,
            self.voltar_inicio
        )

        self.tela_exercicio = TelaExercicio(
            self.voltar_inicio,
            self.abrir_final,
            self.voltar
        )

        self.tela_final = TelaFinal(
            self.voltar_inicio
        )

        self.stack.addWidget(
            self.tela_inicial
        )

        self.stack.addWidget(
            self.tela_dificuldade
        )

        self.stack.addWidget(
            self.tela_exercicio
        )

        self.stack.addWidget(
            self.tela_final
        )

        layout = QVBoxLayout()

        layout.addWidget(
            self.stack
        )

        self.setLayout(layout)

    def abrir_dificuldade(self):
        self.trocar_tela(
            self.tela_dificuldade
        )

    def iniciar_exercicio(self, dificuldade):
        iniciou = self.tela_exercicio.iniciar(dificuldade)

        if iniciou:
            self.trocar_tela(self.tela_exercicio)

    def abrir_final(self):
        self.trocar_tela(
            self.tela_final
        )

    def voltar(self):

        atual = self.stack.currentWidget()

        if atual == self.tela_exercicio:

            self.trocar_tela(
                self.tela_dificuldade
            )

        elif atual == self.tela_dificuldade:

            self.trocar_tela(
                self.tela_inicial
            )

    def voltar_inicio(self):
        self.trocar_tela(
            self.tela_inicial
        )

    def trocar_tela(
        self,
        widget_destino
    ):

        atual = self.stack.currentWidget()

        efeito = QGraphicsOpacityEffect(
            atual
        )

        atual.setGraphicsEffect(
            efeito
        )

        anim = QPropertyAnimation(
            efeito,
            b"opacity"
        )

        anim.setDuration(200)

        anim.setStartValue(1)
        anim.setEndValue(0)

        def depois_saida():

            self.stack.setCurrentWidget(
                widget_destino
            )

            efeito_novo = (
                QGraphicsOpacityEffect(
                    widget_destino
                )
            )

            widget_destino.setGraphicsEffect(
                efeito_novo
            )

            anim2 = QPropertyAnimation(
                efeito_novo,
                b"opacity"
            )

            anim2.setDuration(200)

            anim2.setStartValue(0)

            anim2.setEndValue(1)

            anim2.start()

            widget_destino._anim = anim2

        anim.finished.connect(
            depois_saida
        )

        anim.start()

        atual._anim = anim