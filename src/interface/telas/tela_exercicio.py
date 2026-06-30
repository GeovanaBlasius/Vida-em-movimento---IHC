# src/interface/telas/tela_exercicio.py

import logging
import time
import cv2

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QMessageBox
)

from src.config import MODEL_PATH, CAMERA_WIDTH, CAMERA_HEIGHT, MENSAGENS
from src.interface.tema import Tema
from src.interface.feedback_visual import FeedbackVisual
from src.interface.widgets.painel_camera import PainelCamera
from src.interface.widgets.painel_video import PainelVideo
from src.interface.widgets.painel_feedback import PainelFeedback
from src.core.analisador import Analisador
from src.core.camera.gerenciador_camera import GerenciadorCamera
from src.core.video.gerenciador_video import GerenciadorVideo
from src.core.controle.estado_exercicio import EstadoExercicio
from src.core.controle.controlador_exercicio import ControladorExercicio
from src.core.processamento.processador_exercicio import ProcessadorExercicio
from src.core.exercicios.fabrica_exercicios import criar_exercicio

log = logging.getLogger(__name__)


class TelaExercicio(QWidget):

    def __init__(self, callback_inicio, callback_concluir, callback_voltar):
        super().__init__()

        self.callback_inicio = callback_inicio
        self.callback_concluir = callback_concluir
        self.callback_voltar = callback_voltar

        self.estado = EstadoExercicio()
        self.controlador = ControladorExercicio()
        self.processador = ProcessadorExercicio()
        self.exercicio = None

        self.analisador = Analisador(str(MODEL_PATH))
        self.camera = GerenciadorCamera(CAMERA_WIDTH, CAMERA_HEIGHT)
        self.video = GerenciadorVideo()

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_frame)

        self._ultimo_timestamp = 0

        self.montar_ui()

    # =====================================================
    # UI
    # =====================================================

    def montar_ui(self):
        self.setStyleSheet(Tema.obter_estilo("fundo_app"))

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # =====================================================
        # ESQUERDA (CÂMERA + FEEDBACK)
        # =====================================================

        esquerda = QVBoxLayout()
        esquerda.setSpacing(8)

        titulo = QLabel("REALIZE O MOVIMENTO")
        titulo.setStyleSheet(Tema.obter_estilo("titulo"))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFixedHeight(50)
        esquerda.addWidget(titulo)

        self.painel_camera = PainelCamera()
        esquerda.addWidget(self.painel_camera, 1)

        container_feedback = QWidget()
        container_feedback.setFixedHeight(120)
        container_feedback.setStyleSheet("background: transparent;")
        container_layout = QVBoxLayout(container_feedback)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.painel_feedback = PainelFeedback()
        container_layout.addWidget(self.painel_feedback)

        esquerda.addWidget(container_feedback)
        layout.addLayout(esquerda, 5)

        # =====================================================
        # DIREITA (VÍDEO + BOTÃO)
        # =====================================================

        direita = QVBoxLayout()
        direita.setSpacing(8)

        titulo_video = QLabel("DEMONSTRAÇÃO")
        titulo_video.setStyleSheet(Tema.obter_estilo("titulo"))
        titulo_video.setAlignment(Qt.AlignCenter)
        titulo_video.setFixedHeight(50)
        direita.addWidget(titulo_video)

        self.painel_video = PainelVideo()
        direita.addWidget(self.painel_video, 1)

        container_botao = QWidget()
        container_botao.setFixedHeight(120)
        container_botao.setStyleSheet("background: transparent;")
        container_layout_botao = QVBoxLayout(container_botao)
        container_layout_botao.setContentsMargins(0, 0, 0, 0)
        container_layout_botao.setSpacing(0)

        linha_botoes = QHBoxLayout()
        linha_botoes.setContentsMargins(0, 0, 0, 0)

        self.botao_voltar = QPushButton("← SAIR DO EXERCÍCIO")
        self.botao_voltar.setFixedSize(240, 46)
        self.botao_voltar.setStyleSheet(
            Tema.obter_estilo("botao_voltar") +
            "QPushButton{font-size:16px; padding:8px 14px;}"
        )
        self.botao_voltar.clicked.connect(self.voltar)

        linha_botoes.addStretch(1)
        linha_botoes.addWidget(self.botao_voltar)
        linha_botoes.addStretch(1)

        container_layout_botao.addLayout(linha_botoes)
        direita.addWidget(container_botao)

        layout.addLayout(direita, 2)
        self.setLayout(layout)

    # =====================================================
    # FORMATAÇÃO DE MENSAGEM
    # =====================================================

    def _obter_mensagem_braco(self, lado):
        if lado == "ESQUERDO":
            return "Braço ESQUERDO"
        elif lado == "DIREITO":
            return "Braço DIREITO"
        elif lado == "BILATERAL":
            return "AMBOS os braços"
        return ""

    def _formatar_mensagem_feedback(self, feedback_mensagem, lado, exercicio_nome=None):
        braco_texto = self._obter_mensagem_braco(lado)

        if not braco_texto:
            return feedback_mensagem

        # Instruções que identificam o braço explicitamente
        if MENSAGENS["LEVANTE_BRACO"] in feedback_mensagem:
            return f"Levante o {braco_texto}"

        if MENSAGENS["ABAIXE_BRACO"] in feedback_mensagem:
            return f"Abaixe o {braco_texto}"

        # Mensagens de progresso, forma e bilateral — passam sem modificação
        # (já contêm informação de lado ou são independentes de lado)
        passthrough = (
            MENSAGENS["CONTINUE_SUBINDO"],
            MENSAGENS["QUASE_LA"],
            MENSAGENS["BRACO_LEVANTADO"],
            MENSAGENS["MANTENHA_POSICAO"],
            MENSAGENS["INCLINE_MAIS"],
            MENSAGENS["MUITO_BEM"],
            MENSAGENS["REALIZE_MOVIMENTO"],
            MENSAGENS["ESTIQUE_COTOVELO"],
            MENSAGENS["LEVANTE_MAIS_ESQ"],
            MENSAGENS["LEVANTE_MAIS_DIR"],
            MENSAGENS["LEVANTE_COTOVELO"],
            MENSAGENS["LEVANTE_MAO_CABECA"],
            MENSAGENS["ABAIXE_UM_POUCO"],
        )
        for msg in passthrough:
            if msg in feedback_mensagem:
                return feedback_mensagem

        # "Repetição X concluída!" e outros dinâmicos
        if "Repetição" in feedback_mensagem or "concluída" in feedback_mensagem:
            return feedback_mensagem

        return feedback_mensagem

    # =====================================================
    # INICIAR
    # =====================================================

    def iniciar(self, dificuldade) -> bool:
        self.estado.resetar()
        self.controlador.resetar()
        self.controlador.definir_dificuldade(dificuldade)

        try:
            self.camera.abrir()
        except RuntimeError:
            QMessageBox.critical(
                self,
                "Câmera não encontrada",
                "Não foi possível acessar a câmera.\n\n"
                "Verifique se ela está conectada e tente novamente."
            )
            return False

        nome_exercicio, lado = self.estado.etapa_atual_info()
        self.exercicio = criar_exercicio(nome_exercicio, lado, dificuldade)
        self.video.carregar(self.exercicio.video_path)

        if self.exercicio.tipo == "reps":
            self.painel_feedback.resetar_progresso(f"0/{self.exercicio.meta_reps}")
        else:
            total_seg = self._frames_to_seconds(self.exercicio.meta_frames)
            self.painel_feedback.resetar_progresso(f"0.0s/{total_seg}")

        self.timer.start(33)
        return True

    def _frames_to_seconds(self, frames):
        intervalo_ms = self.timer.interval() if self.timer.interval() > 0 else 33
        return f"{frames * (intervalo_ms / 1000.0):.1f}s"

    # =====================================================
    # FRAME
    # =====================================================

    def atualizar_frame(self):
        frame = self.camera.ler_frame()
        if frame is None:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        timestamp = int(time.time() * 1000)
        if timestamp <= self._ultimo_timestamp:
            timestamp = self._ultimo_timestamp + 1
        self._ultimo_timestamp = timestamp

        resultado = self.analisador.detectar(frame_rgb, timestamp)

        if not resultado.pose_landmarks:
            self.painel_feedback.atualizar(
                "Posicione-se na câmera", (0, 165, 255)
            )
            self.painel_camera.atualizar_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            return

        if resultado.pose_landmarks:
            landmarks = resultado.pose_landmarks[0]

            (nariz, pescoco, cintura, pulso, pontos_braco) = self.analisador.extrair_pontos(
                landmarks, self.estado.lado_atual
            )

            # Variáveis extras para form e bilateral — valores default
            angulo_cotovelo    = 180
            angulo_esq_ind     = None
            angulo_dir_ind     = None
            ombro              = None
            cotovelo_ok_inc    = True   # só relevante para Inclinação Lateral

            if self.estado.lado_atual == "ESQUERDO":
                ombro       = [landmarks[12].x, landmarks[12].y]
                cotovelo    = [landmarks[14].x, landmarks[14].y]
                pulso_braco = [landmarks[16].x, landmarks[16].y]
                quadril = self.analisador.extrair_quadril(landmarks, "ESQUERDO")
                angulo_braco    = self.analisador.calcular_elevacao_braco(ombro, quadril, pulso_braco)
                angulo_cotovelo = self.analisador.calcular_angulo_3_pontos(ombro, cotovelo, pulso_braco)
                mao_ok = self.analisador.validar_braco(pulso, ombro)

            elif self.estado.lado_atual == "DIREITO":
                ombro       = [landmarks[11].x, landmarks[11].y]
                cotovelo    = [landmarks[13].x, landmarks[13].y]
                pulso_braco = [landmarks[15].x, landmarks[15].y]
                quadril = self.analisador.extrair_quadril(landmarks, "DIREITO")
                angulo_braco    = self.analisador.calcular_elevacao_braco(ombro, quadril, pulso_braco)
                angulo_cotovelo = self.analisador.calcular_angulo_3_pontos(ombro, cotovelo, pulso_braco)
                mao_ok = self.analisador.validar_braco(pulso, ombro)

            elif self.estado.lado_atual == "BILATERAL":
                (
                    ombro_esq, cotovelo_esq, pulso_esq,
                    ombro_dir, cotovelo_dir, pulso_dir
                ) = self.analisador.extrair_bracos_bilateral(landmarks)

                quadril_esq = [landmarks[24].x, landmarks[24].y]
                quadril_dir = [landmarks[23].x, landmarks[23].y]

                angulo_esq_ind = self.analisador.calcular_elevacao_braco(ombro_esq, quadril_esq, pulso_esq)
                angulo_dir_ind = self.analisador.calcular_elevacao_braco(ombro_dir, quadril_dir, pulso_dir)

                cot_esq = self.analisador.calcular_angulo_3_pontos(ombro_esq, cotovelo_esq, pulso_esq)
                cot_dir = self.analisador.calcular_angulo_3_pontos(ombro_dir, cotovelo_dir, pulso_dir)

                angulo_braco    = min(angulo_esq_ind, angulo_dir_ind)
                angulo_cotovelo = min(cot_esq, cot_dir)

                mao_esq_ok = self.analisador.validar_braco(pulso_esq, ombro_esq)
                mao_dir_ok = self.analisador.validar_braco(pulso_dir, ombro_dir)
                mao_ok = mao_esq_ok and mao_dir_ok

            if self.exercicio.nome == "Inclinação Lateral":
                angulo_tronco = self.analisador.calcular_inclinacao_lateral(
                    pescoco, cintura, self.estado.lado_atual
                )
                # cotovelo deve estar acima do ombro (Y menor = mais alto na tela)
                cotovelo_ok_inc = cotovelo[1] < ombro[1]
                # mão/pulso deve estar acima da cabeça (acima do nariz)
                mao_ok = pulso[1] < nariz[1]
            else:
                angulo_tronco = 0

            log.debug(
                "LADO=%s angulo_braco=%.1f° cotovelo=%.1f°",
                self.estado.lado_atual, angulo_braco, angulo_cotovelo
            )

            feedback = self.processador.processar(
                self.exercicio, self.controlador,
                angulo_tronco, angulo_braco, mao_ok,
                angulo_cotovelo=angulo_cotovelo,
                angulo_esq=angulo_esq_ind,
                angulo_dir=angulo_dir_ind,
                cotovelo_ok=cotovelo_ok_inc,
            )

            mensagem_formatada = self._formatar_mensagem_feedback(
                feedback["mensagem"], self.estado.lado_atual, self.exercicio.nome
            )
            self.painel_feedback.atualizar(mensagem_formatada, feedback["cor"])

            h, w, _ = frame.shape
            desenhar_tronco = self.exercicio.nome != "Elevação Lateral"

            if self.estado.lado_atual == "BILATERAL":
                FeedbackVisual.desenhar_esqueleto(frame, landmarks, [11, 13, 15], w, h, feedback["cor"], None, None)
                FeedbackVisual.desenhar_esqueleto(frame, landmarks, [12, 14, 16], w, h, feedback["cor"], None, None)
            else:
                FeedbackVisual.desenhar_esqueleto(
                    frame, landmarks, pontos_braco, w, h, feedback["cor"],
                    pescoco if desenhar_tronco else None,
                    cintura if desenhar_tronco else None
                )

            if desenhar_tronco:
                pescoco_px = (int(pescoco[0] * w), int(pescoco[1] * h))
                cintura_px = (int(cintura[0] * w), int(cintura[1] * h))
                cv2.line(frame, pescoco_px, cintura_px, (255, 255, 0), 4)

            if self.exercicio.tipo == "reps":
                progresso = int((self.controlador.contagem_reps / self.exercicio.meta_reps) * 100)
            else:
                progresso = int((self.controlador.contagem_pose / self.exercicio.meta_frames) * 100)

            pct = min(progresso, 100)

            if self.exercicio.tipo == "reps":
                self.painel_feedback.atualizar_progresso(
                    pct, f"{self.controlador.contagem_reps}/{self.exercicio.meta_reps}"
                )
            else:
                atual_seg = self._frames_to_seconds(self.controlador.contagem_pose)
                total_seg = self._frames_to_seconds(self.exercicio.meta_frames)
                self.painel_feedback.atualizar_progresso(pct, f"{atual_seg}/{total_seg}")

            # =====================================================
            # TROCA DE ETAPA
            # =====================================================

            meta_atingida = (
                self.controlador.contagem_reps >= self.exercicio.meta_reps
                if self.exercicio.tipo == "reps"
                else self.controlador.contagem_pose >= self.exercicio.meta_frames
            )

            if meta_atingida:
                self.estado.proxima_etapa()

                if self.estado.concluido:
                    # Exibe o frame final antes de finalizar
                    self.painel_camera.atualizar_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    self.finalizar_automatico()
                    return

                self.controlador.resetar()

                nome_exercicio, lado = self.estado.etapa_atual_info()
                self.exercicio = criar_exercicio(nome_exercicio, lado, self.controlador.dificuldade)

                if self.exercicio.tipo == "reps":
                    self.painel_feedback.resetar_progresso(f"0/{self.exercicio.meta_reps}")
                else:
                    total_seg = self._frames_to_seconds(self.exercicio.meta_frames)
                    self.painel_feedback.resetar_progresso(f"0.0s/{total_seg}")

                self.video.liberar()
                self.video.carregar(self.exercicio.video_path)
                self.video.reiniciar()

        # Sempre atualiza o painel da câmera (com ou sem esqueleto desenhado)
        self.painel_camera.atualizar_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        frame_video = self.video.ler_frame()
        if frame_video is not None:
            self.painel_video.atualizar_frame(cv2.cvtColor(frame_video, cv2.COLOR_BGR2RGB))

    # =====================================================
    # AÇÕES
    # =====================================================

    def _parar(self):
        self.timer.stop()
        self.camera.liberar()
        self.video.liberar()

    def voltar(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Sair do exercício?")
        msg.setText("Deseja sair do exercício?")
        msg.setInformativeText("Seu progresso será perdido.")
        msg.setIcon(QMessageBox.Question)

        btn_sair = msg.addButton("Sair", QMessageBox.AcceptRole)
        btn_continuar = msg.addButton("Continuar exercitando", QMessageBox.RejectRole)
        msg.setDefaultButton(btn_continuar)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0F172A;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 26px;
                font-weight: bold;
                min-width: 480px;
                padding: 10px 20px;
            }
            QPushButton {
                font-size: 22px;
                font-weight: bold;
                min-width: 220px;
                min-height: 64px;
                padding: 12px 24px;
                border-radius: 12px;
                margin: 6px;
            }
        """)

        btn_sair.setStyleSheet("""
            QPushButton {
                background-color: #EF5350;
                color: white;
                border-radius: 12px;
            }
            QPushButton:hover { background-color: #FF6F6C; }
        """)
        btn_continuar.setStyleSheet("""
            QPushButton {
                background-color: #00D4FF;
                color: black;
                border-radius: 12px;
            }
            QPushButton:hover { background-color: #3FE3FF; }
        """)

        msg.exec()

        if msg.clickedButton() == btn_sair:
            self._parar()
            self.callback_voltar()

    def finalizar_manual(self):
        self._parar()
        self.callback_voltar()

    def finalizar_automatico(self):
        self._parar()
        self.callback_concluir()

    def closeEvent(self, event):
        self._parar()
        self.analisador.fechar()
        event.accept()
