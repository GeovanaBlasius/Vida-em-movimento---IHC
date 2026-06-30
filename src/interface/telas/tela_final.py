from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

from src.interface.tema import Tema


class TelaFinal(QWidget):

    def __init__(self, callback_inicio):
        super().__init__()

        self.callback_inicio = callback_inicio

        self.setStyleSheet(Tema.obter_estilo("fundo_app"))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(120, 60, 120, 60)
        layout.setSpacing(0)

        # =====================================================
        # BADGE TOPO
        # =====================================================

        badge = QLabel("⭐  SESSÃO CONCLUÍDA  ⭐")
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet("""
            QLabel {
                background-color: #00D084;
                color: #0F172A;
                font-size: 22px;
                font-weight: bold;
                font-family: Arial;
                padding: 14px 40px;
                border-radius: 16px 16px 0 0;
            }
        """)

        layout.addWidget(badge)

        # =====================================================
        # PAINEL CENTRAL
        # =====================================================

        painel = QWidget()
        painel.setStyleSheet("""
            QWidget {
                background-color: #22263A;
                border-radius: 0 0 20px 20px;
            }
        """)

        painel_layout = QVBoxLayout(painel)
        painel_layout.setAlignment(Qt.AlignCenter)
        painel_layout.setContentsMargins(60, 50, 60, 50)
        painel_layout.setSpacing(20)

        titulo = QLabel("PARABÉNS!")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet(Tema.obter_estilo("titulo"))
        painel_layout.addWidget(titulo)

        subtitulo = QLabel("Você completou todos os exercícios")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet(Tema.obter_estilo("subtitulo"))
        painel_layout.addWidget(subtitulo)

        mensagem = QLabel("Continue se cuidando!")
        mensagem.setAlignment(Qt.AlignCenter)
        mensagem.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: Arial;
                color: #76AED4;
                background: transparent;
                border: none;
            }
        """)
        painel_layout.addWidget(mensagem)

        painel_layout.addSpacing(20)

        botao = QPushButton("VOLTAR AO INÍCIO")
        botao.setMinimumHeight(60)
        botao.setStyleSheet(Tema.obter_estilo("botao_principal"))
        botao.clicked.connect(self.callback_inicio)
        painel_layout.addWidget(botao)

        layout.addWidget(painel)
        self.setLayout(layout)