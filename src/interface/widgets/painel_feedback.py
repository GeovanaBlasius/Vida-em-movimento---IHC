"""
src/interface/widgets/painel_feedback.py
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

from src.interface.tema import Tema


class PainelFeedback(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel("Posicione-se na câmera")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(64)
        self.label.setStyleSheet(Tema.obter_estilo("feedback"))

        self.barra = QProgressBar()
        self.barra.setRange(0, 100)
        self.barra.setValue(0)
        self.barra.setTextVisible(True)
        self.barra.setFormat("0s / 0s")
        self.barra.setMinimumHeight(48)
        self.barra.setStyleSheet(Tema.obter_estilo("barra_progresso_feedback"))

        layout.addWidget(self.label)
        layout.addWidget(self.barra)

        self.setLayout(layout)

    def atualizar(self, mensagem, cor_bgr):
        self.label.setText(mensagem)

        b, g, r = cor_bgr
        cor_hex = "#{:02X}{:02X}{:02X}".format(r, g, b)

        self.label.setStyleSheet(Tema.estilo_feedback_com_cor(cor_hex))
        self.barra.setStyleSheet(Tema.estilo_barra_feedback_com_cor(cor_hex))

    def atualizar_progresso(self, valor, formato):
        self.barra.setValue(valor)
        self.barra.setFormat(formato)

    def resetar_progresso(self, formato="0s / 0s"):
        self.barra.setValue(0)
        self.barra.setFormat(formato)
