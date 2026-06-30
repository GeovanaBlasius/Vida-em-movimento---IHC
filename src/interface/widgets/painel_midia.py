"""
src/interface/widgets/painel_midia.py
Widget base compartilhado por PainelCamera e PainelVideo.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from src.interface.tema import Tema


class PainelMidia(QLabel):

    def __init__(self, largura_minima: int, altura_minima: int):
        super().__init__()

        self.setMinimumSize(largura_minima, altura_minima)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(Tema.obter_estilo("midia"))
        self.setAlignment(Qt.AlignCenter)

    def atualizar_frame(self, frame_rgb):
        imagem = QImage(
            frame_rgb.data,
            frame_rgb.shape[1],
            frame_rgb.shape[0],
            frame_rgb.strides[0],
            QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(imagem)
        self.setPixmap(
            pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
