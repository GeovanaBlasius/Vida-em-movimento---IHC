"""
src/core/controle/validador_exercicio.py
"""

import logging

from src.config import MENSAGENS

log = logging.getLogger(__name__)


class ValidadorExercicio:

    @staticmethod
    def validar_tronco(angulo_tronco, meta_angular, tolerancia):
        diferenca = abs(float(angulo_tronco) - float(meta_angular))
        log.debug(
            "TRONCO angulo=%.2f meta=%s dif=%.2f tol=%s",
            angulo_tronco, meta_angular, diferenca, tolerancia
        )
        return diferenca <= tolerancia

    @staticmethod
    def validar_movimento(mao_ok, braco_ok, tronco_ok):
        if not mao_ok:
            return {
                "mensagem": MENSAGENS["REALIZE_MOVIMENTO"],
                "cor": (0, 0, 255),
                "valido": False,
                "incremento": 0
            }

        if not braco_ok:
            return {
                "mensagem": MENSAGENS["ESTIQUE_BRACO"],
                "cor": (0, 0, 255),
                "valido": False,
                "incremento": 0
            }

        if not tronco_ok:
            return {
                "mensagem": MENSAGENS["INCLINE_MAIS"],
                "cor": (0, 0, 255),
                "valido": False,
                "incremento": 0
            }

        return {
            "mensagem": MENSAGENS["MUITO_BEM"],
            "cor": (0, 255, 0),
            "valido": True,
            "incremento": 3
        }
