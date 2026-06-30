"""
src/core/analisador.py
Classe unificada de análise de postura
"""

import mediapipe as mp
import numpy as np


class Analisador:

    def __init__(self, model_path):

        self.options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=model_path
            ),
            running_mode=mp.tasks.vision.RunningMode.VIDEO
        )

        self.detector = (
            mp.tasks.vision.PoseLandmarker.create_from_options(
                self.options
            )
        )

    # ==========================================================
    # DETECÇÃO
    # ==========================================================

    def detectar_pose(self, frame_rgb, tempo):

        mp_img = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        return self.detector.detect_for_video(
            mp_img,
            tempo
        )

    def detectar(self, frame_rgb, tempo):

        return self.detectar_pose(
            frame_rgb,
            tempo
        )

    # ==========================================================
    # ÂNGULOS
    # ==========================================================
    def calcular_elevacao_braco(
        self,
        ombro,
        quadril,
        pulso
    ):

        return self.calcular_angulo_3_pontos(
            quadril,
            ombro,
            pulso
        )

    def calcular_angulo_3_pontos(self, a, b, c):

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        cos = np.dot(ba, bc) / (
            np.linalg.norm(ba) *
            np.linalg.norm(bc)
        )

        cos = np.clip(cos, -1.0, 1.0)

        return np.degrees(
            np.arccos(cos)
        )
    
    def extrair_bracos_bilateral(
        self,
        landmarks
    ):

        ombro_esq = [
            landmarks[12].x,
            landmarks[12].y
        ]

        cotovelo_esq = [
            landmarks[14].x,
            landmarks[14].y
        ]

        pulso_esq = [
            landmarks[16].x,
            landmarks[16].y
        ]

        ombro_dir = [
            landmarks[11].x,
            landmarks[11].y
        ]

        cotovelo_dir = [
            landmarks[13].x,
            landmarks[13].y
        ]

        pulso_dir = [
            landmarks[15].x,
            landmarks[15].y
        ]

        return (
            ombro_esq,
            cotovelo_esq,
            pulso_esq,
            ombro_dir,
            cotovelo_dir,
            pulso_dir
        )
    
    def calcular_angulo(
        self,
        pescoco,
        cintura
    ):
        dx = cintura[0] - pescoco[0]
        return abs(dx * 250)

    # ==========================================================
    # EXTRAÇÃO DE PONTOS
    # ==========================================================

    def extrair_dados_pose(
        self,
        landmarks,
        lado
    ):

        nariz = [
            landmarks[0].x,
            landmarks[0].y
        ]

        pescoco = [
            (
                landmarks[11].x +
                landmarks[12].x
            ) / 2,
            (
                landmarks[11].y +
                landmarks[12].y
            ) / 2
        ]

        cintura = [
            (
                landmarks[23].x +
                landmarks[24].x
            ) / 2,
            (
                landmarks[23].y +
                landmarks[24].y
            ) / 2
        ]

        if lado == "ESQUERDO":

            pulso = [
                landmarks[16].x,
                landmarks[16].y
            ]

            pontos_braco = [
                12,
                14,
                16
            ]

        elif lado == "DIREITO":

            pulso = [
                landmarks[15].x,
                landmarks[15].y
            ]

            pontos_braco = [
                11,
                13,
                15
            ]

        elif lado == "BILATERAL":

            pulso = [
                (
                    landmarks[15].x +
                    landmarks[16].x
                ) / 2,
                (
                    landmarks[15].y +
                    landmarks[16].y
                ) / 2
            ]

            pontos_braco = [
                11, 13, 15,
                12, 14, 16
            ]
            
        return (
            nariz,
            pescoco,
            cintura,
            pulso,
            pontos_braco
        )

    def extrair_pontos(
        self,
        landmarks,
        lado
    ):

        return self.extrair_dados_pose(
            landmarks,
            lado
        )

    # ==========================================================
    # VALIDAÇÕES
    # ==========================================================

    def extrair_quadril(self, landmarks, lado):

        if lado == "ESQUERDO":

            return [
                landmarks[24].x,
                landmarks[24].y
            ]

        elif lado == "DIREITO":

            return [
                landmarks[23].x,
                landmarks[23].y
            ]

        return [
            (
                landmarks[23].x +
                landmarks[24].x
            ) / 2,

            (
                landmarks[23].y +
                landmarks[24].y
            ) / 2
        ]
    
    def calcular_inclinacao_lateral(
        self,
        pescoco,
        cintura,
        lado
    ):
        dx = cintura[0] - pescoco[0]

        if lado == "ESQUERDO":
            return -dx * 250

        elif lado == "DIREITO":
            return -dx * 250

        return abs(dx * 250)

    def extrair_ombro(self, landmarks, lado):

        if lado == "ESQUERDO":

            return [
                landmarks[12].x,
                landmarks[12].y
            ]

        elif lado == "DIREITO":

            return [
                landmarks[11].x,
                landmarks[11].y
            ]

        return [
            (
                landmarks[11].x +
                landmarks[12].x
            ) / 2,

            (
                landmarks[11].y +
                landmarks[12].y
            ) / 2
        ]
    
    def validar_posicionamento(self, landmarks):
        """
        Verifica se o usuário está posicionado corretamente na câmera.
        Isso é independente do movimento do braço.
        """
        if landmarks is None:
            return False
        
        # Pontos principais para verificar se o corpo está visível
        pontos_principais = [0, 11, 12, 23, 24]  # nariz, ombros, quadris
        
        for idx in pontos_principais:
            if idx >= len(landmarks):
                return False
            # Verifica se o ponto está dentro da tela (5% a 95%)
            if not (0.05 < landmarks[idx].x < 0.95 and 0.05 < landmarks[idx].y < 0.95):
                return False
        
        return True
    
    def validar_braco(
        self,
        pulso,
        nariz
    ):

        if pulso is None:
            return False

        
        return pulso[1] < nariz[1]

    # ==========================================================
    # FECHAR
    # ==========================================================

    def fechar(self):

        self.detector.close()