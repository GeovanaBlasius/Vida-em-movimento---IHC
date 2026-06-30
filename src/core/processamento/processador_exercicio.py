"""
src/core/processamento/processador_exercicio.py
"""

import logging

from src.config import MENSAGENS
from src.core.controle.validador_exercicio import ValidadorExercicio

log = logging.getLogger(__name__)


class ProcessadorExercicio:

    # Ângulo do ombro (quadril→ombro→pulso) quando o braço está horizontal ≈ 90°.
    # 80° dá tolerância de 10° abaixo do horizontal — meta pedagógica das elevações.
    _ANGULO_CIMA  = 80
    _ANGULO_BAIXO = 40

    # Limiar abaixo do qual o braço é considerado em repouso.
    # Qualquer ângulo < _ANGULO_REPOUSO exibe "Levante o braço".
    # Manter _ANGULO_REPOUSO > _ANGULO_BAIXO garante que após contar a rep
    # (em _ANGULO_BAIXO = 40°) o braço ainda esteja na zona de repouso,
    # evitando "Continue subindo" enquanto o braço ainda está descendo.
    _ANGULO_REPOUSO = 50

    # Ângulo mínimo no cotovelo para braço considerado reto (180° = totalmente estendido).
    _COTOVELO_MIN = 140

    # Diferença máxima tolerada entre os dois braços no bilateral.
    _BILATERAL_DELTA = 20

    # Ângulo máximo seguro para elevação do braço.
    # Acima de 110° aumenta a compressão subacromial — risco de impingement,
    # especialmente em idosos com manguito rotador fragilizado.
    _ANGULO_MAX = 110

    def processar(self, exercicio, controlador, angulo_tronco, angulo_braco, mao_ok,
                  angulo_cotovelo=180, angulo_esq=None, angulo_dir=None,
                  cotovelo_ok=True):

        if exercicio.tipo == "reps":
            return self._processar_reps(
                controlador, angulo_braco,
                angulo_cotovelo, angulo_esq, angulo_dir
            )

        # ── Inclinação Lateral (tipo "frames") ───────────────────────────────
        # Hierarquia pedagógica: o idoso aprende a posição correta passo a passo.
        # Só valida a inclinação do tronco depois que o braço estiver posicionado.
        tronco_ok = ValidadorExercicio.validar_tronco(
            angulo_tronco,
            exercicio.meta_angular,
            exercicio.tolerancia
        )

        log.debug("FRAMES cotovelo_ok=%s mao_ok=%s tronco_ok=%s angulo=%.1f°",
                  cotovelo_ok, mao_ok, tronco_ok, angulo_tronco)

        if not cotovelo_ok:
            # Passo 1: cotovelo deve estar acima do ombro
            controlador.decrementar()
            return {"mensagem": MENSAGENS["LEVANTE_COTOVELO"],
                    "cor": (0, 0, 255), "valido": False, "incremento": 0}

        if not mao_ok:
            # Passo 2: mão/pulso deve estar acima da cabeça
            controlador.decrementar()
            return {"mensagem": MENSAGENS["LEVANTE_MAO_CABECA"],
                    "cor": (0, 0, 255), "valido": False, "incremento": 0}

        if not tronco_ok:
            # Passo 3: inclinar o tronco até a amplitude correta
            controlador.decrementar()
            return {"mensagem": MENSAGENS["INCLINE_MAIS"],
                    "cor": (0, 0, 255), "valido": False, "incremento": 0}

        # Todos os critérios atendidos — posição correta
        controlador.incrementar()
        return {"mensagem": MENSAGENS["MANTENHA_POSICAO"],
                "cor": (0, 255, 0), "valido": True, "incremento": 3}

    def _processar_reps(self, controlador, angulo_braco,
                        angulo_cotovelo=180, angulo_esq=None, angulo_dir=None):
        """
        Feedback graduado para exercícios de repetição.

        Zonas de ângulo (fase BAIXO):
          < 50°  → repouso / ainda descendo  → "Levante o braço"
          50–79° → subindo                   → "Continue subindo" / "Quase lá"
          ≥ 80°  → posição alvo              → transição CIMA

        O limiar de repouso (50°) é propositalmente maior que o limiar de contagem
        (40°): assim, quando o braço termina de descer e transita CIMA→BAIXO a ~40°,
        a zona de repouso ainda está ativa — o idoso nunca vê "Continue subindo"
        enquanto o braço ainda está descendo.
        """
        feedback = {"mensagem": "", "cor": (255, 255, 255), "valido": False, "incremento": 0}

        if controlador.fase == "BAIXO":

            if angulo_braco >= self._ANGULO_CIMA:
                # Braço chegou ao horizontal — posição alvo atingida
                controlador.fase = "CIMA"
                controlador.movimento_valido = True
                feedback["mensagem"] = MENSAGENS["BRACO_LEVANTADO"]
                feedback["cor"] = (0, 220, 0)
                log.debug("→ CIMA (%.1f°)", angulo_braco)

            elif angulo_cotovelo < self._COTOVELO_MIN and angulo_braco >= self._ANGULO_REPOUSO:
                # Braço claramente em movimento mas cotovelo dobrado — corrigir forma
                feedback["mensagem"] = MENSAGENS["ESTIQUE_COTOVELO"]
                feedback["cor"] = (0, 100, 255)

            elif angulo_esq is not None and angulo_dir is not None:
                # Bilateral: verificar assimetria entre os braços
                delta = angulo_esq - angulo_dir
                if delta < -self._BILATERAL_DELTA:
                    feedback["mensagem"] = MENSAGENS["LEVANTE_MAIS_ESQ"]
                    feedback["cor"] = (0, 165, 255)
                elif delta > self._BILATERAL_DELTA:
                    feedback["mensagem"] = MENSAGENS["LEVANTE_MAIS_DIR"]
                    feedback["cor"] = (0, 165, 255)
                elif angulo_braco >= 70:
                    feedback["mensagem"] = MENSAGENS["QUASE_LA"]
                    feedback["cor"] = (0, 165, 255)
                elif angulo_braco >= self._ANGULO_REPOUSO:
                    feedback["mensagem"] = MENSAGENS["CONTINUE_SUBINDO"]
                    feedback["cor"] = (0, 165, 255)
                else:
                    feedback["mensagem"] = MENSAGENS["LEVANTE_BRACO"]
                    feedback["cor"] = (0, 0, 255)

            elif angulo_braco >= 70:
                # Faltam ~10° para o alvo
                feedback["mensagem"] = MENSAGENS["QUASE_LA"]
                feedback["cor"] = (0, 165, 255)

            elif angulo_braco >= self._ANGULO_REPOUSO:
                # Acima da zona de repouso — braço claramente em subida
                feedback["mensagem"] = MENSAGENS["CONTINUE_SUBINDO"]
                feedback["cor"] = (0, 165, 255)

            else:
                # Zona de repouso (< 50°): braço baixo ou ainda descendo após rep
                feedback["mensagem"] = MENSAGENS["LEVANTE_BRACO"]
                feedback["cor"] = (0, 0, 255)

        elif controlador.fase == "CIMA":

            if angulo_braco > self._ANGULO_MAX:
                feedback["mensagem"] = MENSAGENS["ABAIXE_UM_POUCO"]
                feedback["cor"] = (0, 165, 255)

            elif angulo_braco <= self._ANGULO_BAIXO:
                # Braço retornou ao repouso — registra a repetição
                controlador.fase = "BAIXO"
                if controlador.movimento_valido:
                    controlador.contagem_reps += 1
                    feedback["mensagem"] = f"Repetição {controlador.contagem_reps} concluída!"
                    feedback["cor"] = (0, 220, 0)
                    log.debug("REP %d contada", controlador.contagem_reps)
                controlador.movimento_valido = False

            elif angulo_braco >= 70:
                # Braço ainda na zona de confirmação (≥ 70°) — mantém verde
                feedback["mensagem"] = MENSAGENS["BRACO_LEVANTADO"]
                feedback["cor"] = (0, 220, 0)

            else:
                # Braço descendo — instrução com laranja (movimento, não erro)
                feedback["mensagem"] = MENSAGENS["ABAIXE_BRACO"]
                feedback["cor"] = (0, 165, 255)

        log.debug("REPS fase=%s angulo=%.1f°", controlador.fase, angulo_braco)
        return feedback
