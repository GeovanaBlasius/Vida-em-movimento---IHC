class Tema:

    CORES = {
        "primaria": "#0399F6",
        "secundaria": "#EF5350",
        "sucesso": "#00DD00",
        "aviso": "#FFD700",
        "fundo": "#0F172A",
        "painel": "#0F172A",
        "texto": "#FFFFFF",
        "texto_secundario": "#76AED4",
    }

    # =====================================================
    # DIMENSÕES
    # =====================================================

    BOTAO_DIFICULDADE_ALTURA = 140

    ESPACAMENTO_BOTOES_DIFICULDADE = 15

    MARGEM_LATERAL_DIFICULDADE = 80
    MARGEM_SUPERIOR_DIFICULDADE = 20
    MARGEM_INFERIOR_DIFICULDADE = 20

    BOTAO_VOLTAR_ALTURA = 70

    ESTILOS = {

        # =====================================================
        # APP
        # =====================================================

        "fundo_app": """
            QWidget {
                background-color: #0F172A;
                color: #FFFFFF;
                font-family: Arial;
            }
        """,

        # =====================================================
        # TITULOS
        # =====================================================

        "titulo": """
            QLabel {
                font-size: 48px;
                font-weight: bold;
                font-family: Arial;
                color: #00D4FF;
                background: transparent;
                border: none;
            }
        """,

        "subtitulo": """
            QLabel {
                font-size: 30px;
                font-weight: bold;
                font-family: Arial;
                color: #E6E6E6;
                background: transparent;
                border: none;
            }
        """,

        # =====================================================
        # FEEDBACK
        # =====================================================

        "feedback": """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #000000;
                background-color: #FFFFFF;
                padding: 8px 10px;
                border-radius: 0;
                border: none;
            }
        """,

        # =====================================================
        # BOTOES
        # =====================================================

        "botao_principal": """
            QPushButton {
                background-color: #00D4FF;
                color: black;
                font-size: 20px;
                font-weight: bold;
                border-radius: 16px;
                padding: 20px;
            }

            QPushButton:hover {
                background-color: #3FE3FF;
            }

            QPushButton:pressed {
                background-color: #00B5D9;
            }
        """,

        "botao_secundario": """
            QPushButton {
                background-color: #EF5350;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 12px;
                min-height: 55px;
            }

            QPushButton:hover {
                background-color: #FF6F6C;
            }

            QPushButton:pressed {
                background-color: #D63B38;
            }
        """,

        "botao_voltar": """
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 16px;
                font-weight: bold;
                min-height: 55px;
            }

            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                border-radius: 8px;
            }
        """,

        "botao_dificuldade_base": """
            QPushButton {
                color: white;
                border-radius: 18px;
                padding-left: 35px;
                text-align: left;
                font-size: 22px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """,

        # =====================================================
        # BARRA PROGRESSO
        # =====================================================

        "barra_progresso": """
            QProgressBar {
                background-color: #333333;
                border-radius: 10px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                color: white;
                min-height: 38px;
                border: 2px solid #444444;
            }

            QProgressBar::chunk {
                background-color: #00D084;
                border-radius: 8px;
            }
        """,

        "barra_progresso_feedback": """
            QProgressBar {
                background-color: #1E293B;
                border-radius: 0;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
                color: white;
                min-height: 48px;
                border: none;
                border-top: 2px solid #0F172A;
            }

            QProgressBar::chunk {
                background-color: #00D084;
                border-radius: 0;
            }
        """,

        # =====================================================
        # DIFICULDADE
        # =====================================================

        "botao_dificuldade_facil": """
            QPushButton {
                background-color: #00D084;
            }

            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """,

        "botao_dificuldade_medio": """
            QPushButton {
                background-color: #FFB74D;
            }

            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """,

        "botao_dificuldade_dificil": """
            QPushButton {
                background-color: #EF5350;
            }

            QPushButton:hover {
                background-color: white;
                color: black;
            }
        """,

        # =====================================================
        # PAINÉIS DE MÍDIA (câmera e vídeo)
        # =====================================================

        "midia": """
            QLabel {
                background-color: black;
                border: 4px solid #00D4FF;
                border-radius: 16px;
            }
        """,

        # =====================================================
        # PAINEL
        # =====================================================

        "painel": """
            QWidget {
                background-color: #22263A;
                border-radius: 18px;
            }
        """,

        "card": """
            QWidget {
                background-color: white;
                border-radius: 14px;
                border: 1px solid #E6EAF0;
            }
        """,
    }

    # =========================================================
    # OBTER ESTILO
    # =========================================================

    @staticmethod
    def obter_estilo(nome):

        return Tema.ESTILOS.get(
            nome,
            ""
        )

    # =========================================================
    # OBTER COR
    # =========================================================

    @staticmethod
    def obter_cor(nome):

        return Tema.CORES.get(
            nome,
            "#FFFFFF"
        )

    @staticmethod
    def obter_estilo_dificuldade(tipo):

        estilo_base = Tema.obter_estilo(
            "botao_dificuldade_base"
        )

        estilo_cor = Tema.obter_estilo(
            f"botao_dificuldade_{tipo}"
        )

        return estilo_base + estilo_cor

    @staticmethod
    def estilo_feedback_com_cor(cor_hex):

        return f"""
            QLabel {{
                background-color: {cor_hex};
                color: #000000;
                font-size: 24px;
                font-weight: bold;
                border-radius: 0;
                padding: 8px 10px;
                border: none;
            }}
        """

    @staticmethod
    def estilo_barra_feedback_com_cor(cor_hex):

        return f"""
            QProgressBar {{
                background-color: #1E293B;
                border-radius: 0;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
                color: white;
                min-height: 48px;
                border: none;
                border-top: 2px solid #0F172A;
            }}

            QProgressBar::chunk {{
                background-color: {cor_hex};
                border-radius: 0;
            }}
        """