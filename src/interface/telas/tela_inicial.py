from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

from src.config import IMG_AVISO
from src.interface.tema import Tema


class TelaInicial(QWidget):

    def __init__(self, callback_iniciar):
        super().__init__()

        self.callback_iniciar = callback_iniciar

        self.setStyleSheet(
            Tema.obter_estilo("fundo_app")
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        titulo = QLabel("VIDA EM MOVIMENTO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(
            Tema.obter_estilo("titulo")
        )

        layout.addWidget(titulo)

        subtitulo = QLabel(
            "Exercícios de alongamento assistidos por IA"
        )

        subtitulo.setAlignment(Qt.AlignCenter)

        subtitulo.setStyleSheet(
            Tema.obter_estilo("subtitulo")
        )

        layout.addWidget(subtitulo)

        imagem = QLabel()

        if IMG_AVISO.exists():

            pixmap = QPixmap(str(IMG_AVISO))

            imagem.setPixmap(
                pixmap.scaled(
                    700,
                    700,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        imagem.setAlignment(Qt.AlignCenter)

        layout.addWidget(imagem)

        botao = QPushButton("INICIAR")

        botao.setMinimumHeight(60)

        botao.setStyleSheet(
            Tema.obter_estilo(
                "botao_principal"
            )
        )

        botao.clicked.connect(
            self.callback_iniciar
        )

        layout.addWidget(botao)

        self.setLayout(layout)