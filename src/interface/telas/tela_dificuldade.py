from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

from PySide6.QtWidgets import QSizePolicy
from src.interface.tema import Tema


class TelaDificuldade(QWidget):

    def __init__(
        self,
        callback_dificuldade,
        callback_voltar
    ):
        super().__init__()

        self.callback_dificuldade = callback_dificuldade
        self.callback_voltar = callback_voltar

        self.setStyleSheet(
            Tema.obter_estilo("fundo_app")
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.setContentsMargins(
            Tema.MARGEM_LATERAL_DIFICULDADE,
            Tema.MARGEM_SUPERIOR_DIFICULDADE,
            Tema.MARGEM_LATERAL_DIFICULDADE,
            Tema.MARGEM_INFERIOR_DIFICULDADE
        )

        layout.setSpacing(Tema.ESPACAMENTO_BOTOES_DIFICULDADE)

        titulo = QLabel(
            "Escolha o nível do exercício"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setStyleSheet(
            Tema.obter_estilo("titulo")
        )

        layout.addWidget(titulo)

        subtitulo = QLabel(
            "Toque em uma opção para continuar"
        )

        subtitulo.setAlignment(Qt.AlignCenter)

        subtitulo.setStyleSheet(
            Tema.obter_estilo("subtitulo")
        )

        layout.addWidget(subtitulo)

        def criar_botao(
            texto,
            tipo,
            nivel
        ):
            botao = QPushButton(texto)

            botao.setMinimumHeight(
                Tema.BOTAO_DIFICULDADE_ALTURA
            )

            botao.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Fixed
            )
            
            botao.setStyleSheet(
                Tema.obter_estilo_dificuldade(
                    tipo
                )
            )

            botao.clicked.connect(
                lambda _, n=nivel:
                self.callback_dificuldade(n)
            )

            return botao

        layout.addWidget(
            criar_botao(
                "🟢 FÁCIL\n Movimentos leves",
                "facil",
                "FACIL"
            )
        )

        layout.addWidget(
            criar_botao(
                "🟡 MÉDIO\n Movimentos moderados",
                "medio",
                "MEDIO"
            )
        )

        layout.addWidget(
            criar_botao(
                "🔴 DIFÍCIL\n Movimentos mais intensos",
                "dificil",
                "DIFICIL"
            )
        )

        # =====================================================
        # BOTÃO VOLTAR - EXPANDIDO
        # =====================================================
        
        voltar = QPushButton(
            "← VOLTAR AO INÍCIO" 
        )

        voltar.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        
        voltar.setMinimumHeight(55)
        voltar.setStyleSheet(
            Tema.obter_estilo("botao_voltar") +
            "QPushButton{font-size:18px; padding:12px 20px;}"
        )

        voltar.clicked.connect(
            self.callback_voltar
        )

        layout.addWidget(voltar)

        self.setLayout(layout)