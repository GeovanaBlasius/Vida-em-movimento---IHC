"""
src/interface/feedback_visual.py
"""

import cv2


class FeedbackVisual:

    @staticmethod
    def estilo_feedback(cor_hex):

        return f"""
            QLabel {{
                background-color: {cor_hex};
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 16px;
                padding: 16px;
            }}
        """

    @staticmethod
    def desenhar_esqueleto(
    frame,
    landmarks,
    pontos,
    largura,
    altura,
    cor,
    pescoco=None,
    cintura=None
    ):

        for idx in pontos:

            x = int(
                landmarks[idx].x * largura
            )

            y = int(
                landmarks[idx].y * altura
            )

            cv2.circle(
                frame,
                (x, y),
                12,
                cor,
                -1
            )

        for i in range(len(pontos) - 1):

            p1 = pontos[i]
            p2 = pontos[i + 1]

            x1 = int(
                landmarks[p1].x * largura
            )

            y1 = int(
                landmarks[p1].y * altura
            )

            x2 = int(
                landmarks[p2].x * largura
            )

            y2 = int(
                landmarks[p2].y * altura
            )

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                cor,
                8
            )

        if pescoco and cintura:

            x1 = int(pescoco[0] * largura)
            y1 = int(pescoco[1] * altura)

            x2 = int(cintura[0] * largura)
            y2 = int(cintura[1] * altura)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 255),
                6
            )

