"""
src/core/camera/gerenciador_camera.py
"""

import cv2


class GerenciadorCamera:

    def __init__(self, largura, altura, indice_camera=0):
        self._largura = largura
        self._altura = altura
        self._indice = indice_camera
        self.cap = None

    # =====================================================
    # ABRIR
    # =====================================================

    def abrir(self):
        if self.esta_aberta():
            return

        self.cap = cv2.VideoCapture(self._indice)

        if not self.cap.isOpened():
            raise RuntimeError("ERRO: câmera não encontrada")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._largura)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._altura)

    # =====================================================
    # LEITURA
    # =====================================================

    def ler_frame(self):
        if not self.esta_aberta():
            return None

        sucesso, frame = self.cap.read()

        if not sucesso:
            return None

        return cv2.flip(frame, 1)

    # =====================================================
    # STATUS
    # =====================================================

    def esta_aberta(self):
        return self.cap is not None and self.cap.isOpened()

    # =====================================================
    # LIBERAR
    # =====================================================

    def liberar(self):
        if self.esta_aberta():
            self.cap.release()
        self.cap = None
