"""
src/interface/widgets/painel_video.py
"""

from src.interface.widgets.painel_midia import PainelMidia


class PainelVideo(PainelMidia):

    def __init__(self):
        super().__init__(largura_minima=320, altura_minima=520)
