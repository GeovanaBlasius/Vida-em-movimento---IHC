"""
src/core/video/gerenciador_video.py
"""

import logging
import cv2

log = logging.getLogger(__name__)


class GerenciadorVideo:

    def __init__(self):

        self.video = None

    # =====================================================
    # CARREGAR
    # =====================================================

    def carregar(self, caminho_video):

        log.debug("Carregando vídeo: %s", caminho_video)

        self.liberar()

        self.video = cv2.VideoCapture(str(caminho_video))

        log.debug("Vídeo aberto: %s", self.video.isOpened())

    # =====================================================
    # FRAME
    # =====================================================

    def ler_frame(self):

        if self.video is None:

            return None

        sucesso, frame = self.video.read()

        if not sucesso:

            self.video.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

            sucesso, frame = self.video.read()

            if not sucesso:

                return None

        return frame

    # =====================================================
    # STATUS
    # =====================================================

    def carregado(self):

        return (
            self.video is not None
        )

    # =====================================================
    # REINICIAR
    # =====================================================

    def reiniciar(self):

        if self.video is not None:

            self.video.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

    # =====================================================
    # LIBERAR
    # =====================================================

    def liberar(self):

        if self.video is not None:

            self.video.release()

            self.video = None