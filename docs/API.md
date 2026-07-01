# 📚 DOCUMENTAÇÃO DA API - Vida em Movimento

## vision/analisador.py

### Classe: `AnalisadorFisio`

Responsável pela detecção e análise de pose corporal usando MediaPipe.

#### Método: `__init__(model_path)`
```python
def __init__(self, model_path):
    """
    Inicializa o analisador de pose.
    
    Args:
        model_path (str): Caminho absoluto para arquivo .task
        
    Raises:
        FileNotFoundError: Se arquivo não existir
        
    Exemplo:
        analisador = AnalisadorFisio("pose_landmarker_full.task")
    """
```

#### Método: `detectar(frame_rgb, frame_id)`
```python
def detectar(self, frame_rgb, frame_id):
    """
    Detecta pose no frame RGB.
    
    Args:
        frame_rgb (numpy.ndarray): Frame em formato RGB (H x W x 3)
        frame_id (int): ID do frame para sincronização MediaPipe
        
    Returns:
        mediapipe.tasks.vision.PoseLandmarkerResult
            .pose_landmarks: Lista com 33 landmarks
            
    Exemplo:
        resultado = analisador.detectar(frame_rgb, 0)
        if resultado.pose_landmarks:
            landmarks = resultado.pose_landmarks[0]
    """
```

#### Método: `extrair_pontos(landmarks, lado)`
```python
def extrair_pontos(self, landmarks, lado):
    """
    Extrai pontos-chave para análise.
    
    Args:
        landmarks: Lista de 33 pontos do corpo (MediaPipe)
        lado (str): "ESQUERDO" ou "DIREITO"
        
    Returns:
        tuple: (nariz, pescoco, cintura, pulso, pontos_braco)
            - nariz [x, y]: Coordenadas normalizadas
            - pescoco [x, y]: Média entre ombros
            - cintura [x, y]: Média entre quadris
            - pulso [x, y]: Pulso do lado selecionado
            - pontos_braco [indices]: Índices para desenho
            
    Nota:
        Coordenadas estão normalizadas (0-1), multiplicar por 
        (width, height) do frame para pixel coordinates
        
    Exemplo:
        nariz, pescoco, cintura, pulso, pts = analisador.extrair_pontos(
            landmarks, "ESQUERDO"
        )
    """
```

#### Método: `calcular_angulo(pescoco, cintura)`
```python
def calcular_angulo(self, pescoco, cintura):
    """
    Calcula ângulo de inclinação do tronco.
    
    Args:
        pescoco (list): [x, y] do pescoço (normalizado)
        cintura (list): [x, y] da cintura (normalizado)
        
    Returns:
        float: Ângulo em graus (0-180)
        
    Cálculo:
        1. Calcula dx = cintura[x] - pescoco[x]
        2. Calcula dy = cintura[y] - pescoco[y]
        3. Usa arctan2(dy, abs(dx))
        4. Converte para graus
        5. Retorna valor absoluto
        
    Exemplo:
        angulo = analisador.calcular_angulo([0.5, 0.3], [0.5, 0.7])
        # Retorna ~90 (movimento vertical)
    """
```

#### Método: `validar_braco(pulso, nariz)`
```python
def validar_braco(self, pulso, nariz):
    """
    Valida se braço está acima da cabeça.
    
    Args:
        pulso (list): [x, y] do pulso
        nariz (list): [x, y] do nariz
        
    Returns:
        bool: True se pulso[y] < nariz[y]
        
    Nota:
        Em OpenCV, y=0 é no topo, y aumenta para baixo
        Logo, pulso acima do nariz = pulso[y] < nariz[y]
        
    Exemplo:
        if analisador.validar_braco(pulso, nariz):
            print("Braço está levantado")
    """
```

#### Método: `fechar()`
```python
def fechar(self):
    """
    Fecha o detector e libera recursos.
    
    Importante: Chamar ao sair para liberar memória GPU/CPU
    
    Exemplo:
        analisador.fechar()
    """
```

---

## core/exercicio.py

### Classe: `ControladorExercicio`

Valida exercícios e fornece feedback visual.

#### Método: `__init__()`
```python
def __init__(self):
    """Inicializa o controlador com contagem zerada."""
    self.contagem_pose = 0
    self.dificuldade = "medio"
```

#### Método: `validar(inclinacao, lado, mao_ok)`
```python
def validar(self, inclinacao, lado, mao_ok):
    """
    Valida se a pose está correta.
    
    Args:
        inclinacao (float): Ângulo atual do corpo
        lado (str): "ESQUERDO" ou "DIREITO"
        mao_ok (bool): Se braço está levantado
        
    Returns:
        dict: {
            "mensagem": str,        # Feedback para usuário
            "cor": (B, G, R),       # Cor BGR
            "valido": bool,         # Se pose é válida
            "incremento": int       # Quanto incrementar contagem
        }
        
    Lógica:
        1. Se braço não levantado → Vermelho, incremento 0
        2. Calcula erro = |inclinacao - meta|
        3. Se erro ≤ 30% tolerância → Verde, incremento 3
        4. Se erro ≤ 60% tolerância → Verde claro, incremento 2
        5. Se erro ≤ 100% tolerância → Amarelo, incremento 1
        6. Senão → Vermelho, incremento 0
        
    Exemplo:
        resultado = controlador.validar(110, "ESQUERDO", True)
        # Retorna: {"mensagem": "✓ MUITO BEM!", "cor": (0, 220, 0), ...}
    """
```

#### Método: `incrementar(valor=1)`
```python
def incrementar(self, valor=1):
    """
    Incrementa contagem de poses válidas.
    
    Args:
        valor (int): Quanto incrementar (padrão 1)
        
    Exemplo:
        if resultado["valido"]:
            controlador.incrementar(resultado["incremento"])
    """
```

#### Método: `decrementar()`
```python
def decrementar(self):
    """
    Decrementa contagem (nunca vai abaixo de 0).
    
    Exemplo:
        if not resultado["valido"]:
            controlador.decrementar()
    """
```

#### Método: `resetar()`
```python
def resetar(self):
    """
    Reseta contagem para começar novo lado/exercício.
    
    Exemplo:
        if controlador.contagem_pose >= meta_frames:
            controlador.resetar()
    """
```

#### Método: `definir_dificuldade(dificuldade)`
```python
def definir_dificuldade(self, dificuldade):
    """
    Define dificuldade do exercício.
    
    Args:
        dificuldade (str): "facil", "medio" ou "dificil"
        
    Efeito:
        Altera tolerância: fácil (25°), médio (15°), difícil (8°)
        
    Exemplo:
        controlador.definir_dificuldade("dificil")
    """
```

---

### Classe: `EstadoExercicio`

Rastreia o estado do exercício.

#### Método: `__init__()`
```python
def __init__(self):
    """Inicializa estado zerado."""
    self.indice_etapa = 0      # Qual lado (0=ESQUERDO, 1=DIREITO)
    self.lado_atual = None      # Nome do lado
    self.tempo = 0             # Tempo decorrido
    self.concluido = False     # Se exercício concluído
```

#### Método: `proxima_etapa()`
```python
def proxima_etapa(self):
    """
    Avança para próxima etapa (próximo lado).
    
    Exemplo:
        if controlador.contagem_pose >= meta_frames:
            estado.proxima_etapa()
            # Agora estado.indice_etapa = 1 (DIREITO)
    """
```

#### Método: `resetar()`
```python
def resetar(self):
    """
    Reseta estado para novo exercício.
    
    Exemplo:
        estado.resetar()
        # Volta para ESQUERDO
    """
```

---

## interface/telas.py

### Classe: `TelaInicial`

Tela de boas-vindas.

#### Método: `__init__(callback)`
```python
def __init__(self, callback):
    """
    Args:
        callback: Função chamada ao clicar em "Começar"
        
    Exemplo:
        tela = TelaInicial(lambda: print("Iniciando..."))
    """
```

---

### Classe: `TelaDificuldade`

Seleção de dificuldade.

#### Método: `__init__(callback)`
```python
def __init__(self, callback):
    """
    Args:
        callback: Função(dificuldade) chamada ao selecionar
        
    Exemplo:
        tela = TelaDificuldade(lambda d: print(f"Nível: {d}"))
        # Será chamado com "facil", "medio" ou "dificil"
    """
```

---

### Classe: `TelaExercicio`

Tela principal do exercício.

#### Método: `iniciar(dificuldade)`
```python
def iniciar(self, dificuldade):
    """
    Inicia exercício com dificuldade.
    
    Args:
        dificuldade (str): "facil", "medio" ou "dificil"
        
    Ações:
        1. Inicializa AnalisadorFisio
        2. Abre câmera (1280x720 @ 30 FPS)
        3. Carrega vídeo de demonstração
        4. Inicia timer (30 FPS)
        
    Exemplo:
        tela.iniciar("medio")
    """
```

#### Método: `atualizar_frame()`
```python
def atualizar_frame(self):
    """
    Processa um novo frame (chamado a cada 33ms).
    
    Fluxo:
        1. Lê frame da câmera
        2. Detecta pose
        3. Extrai pontos
        4. Calcula ângulo
        5. Valida movimento
        6. Desenha esqueleto
        7. Atualiza UI
        8. Verifica conclusão
    """
```

#### Método: `carregarVideo()`
```python
def carregarVideo(self):
    """
    Carrega primeiro frame do vídeo de demonstração.
    
    Busca em:
        - ESQUERDO: assets/exercicios/exercicio1.1.mp4
        - DIREITO: assets/exercicios/exercicio01.mp4
    """
```

#### Método: `finalizar()`
```python
def finalizar(self):
    """
    Finaliza exercício e libera recursos.
    
    - Para timer
    - Libera câmera
    - Fecha analisador
    - Chama callback_concluir()
    """
```

---

### Classe: `TelaFinal`

Tela de conclusão.

#### Método: `__init__(callback_voltar, callback_repetir)`
```python
def __init__(self, callback_voltar, callback_repetir):
    """
    Args:
        callback_voltar: Chamado ao clicar "Voltar"
        callback_repetir: Chamado ao clicar "Repetir"
    """
```

---

## interface/app.py

### Classe: `App`

Aplicação principal com navegação.

#### Método: `__init__()`
```python
def __init__(self):
    """Cria aplicação e todas as telas."""
```

#### Método: `abrir_dificuldade()`
```python
def abrir_dificuldade(self):
    """Mostra tela de seleção de dificuldade."""
```

#### Método: `iniciar_exercicio(dificuldade)`
```python
def iniciar_exercicio(self, dificuldade):
    """
    Args:
        dificuldade (str): "facil", "medio" ou "dificil"
        
    Ação:
        Inicia TelaExercicio com dificuldade
    """
```

#### Método: `abrir_final()`
```python
def abrir_final(self):
    """Mostra tela de conclusão."""
```

#### Método: `voltar_inicio()`
```python
def voltar_inicio(self):
    """Volta para tela inicial."""
```

---

## interface/tema.py

### Classe: `Tema` (estática)

Define cores e estilos.

#### Método: `obter_estilo(nome)`
```python
@staticmethod
def obter_estilo(nome):
    """
    Args:
        nome (str): "botao_principal", "botao_secundario", "titulo", etc.
        
    Returns:
        str: CSS styling para PySide6
        
    Exemplo:
        widget.setStyleSheet(Tema.obter_estilo("botao_principal"))
    """
```

#### Método: `obter_cor(nome)`
```python
@staticmethod
def obter_cor(nome):
    """
    Args:
        nome (str): "primaria", "secundaria", "texto", etc.
        
    Returns:
        str: Cor em formato HEX
        
    Exemplo:
        cor = Tema.obter_cor("primaria")  # "#00D4FF"
    """
```

---

## config.py

Arquivo de configuração com constantes:

```python
# Caminhos
BASE_DIR              # Diretório raiz
SRC_DIR               # Diretório src
ASSETS_DIR            # Diretório assets
MODEL_PATH            # Caminho do modelo
IMG_AVISO             # Imagem inicial
VIDEOS                # Dict com caminhos dos vídeos

# Ângulos
META_ANGULAR          # {"ESQUERDO": 110, "DIREITO": 70}

# Tolerâncias
TOLERANCIAS          # {"facil": 25, "medio": 15, "dificil": 8}

# Metas
META_FRAMES          # {"facil": 80, "medio": 100, "dificil": 120}

# Etapas
ETAPAS               # ["ESQUERDO", "DIREITO"]

# Vídeo
CAMERA_WIDTH         # 1280
CAMERA_HEIGHT        # 720
CAMERA_FPS           # 30

# Cores (BGR)
CORES                # {"VERDE": (0, 220, 0), ...}

# MediaPipe
MIN_DETECTION_CONFIDENCE  # 0.6
MIN_TRACKING_CONFIDENCE   # 0.6
```

---

## Fluxo Típico de Uso

```python
# 1. Iniciar aplicação
app = App()

# 2. Usuário seleciona dificuldade → TelaExercicio.iniciar("medio")

# 3. Na tela de exercício:
analisador = AnalisadorFisio("pose_landmarker_full.task")
controlador = ControladorExercicio()
estado = EstadoExercicio()

# 4. Loop a 30 FPS:
while True:
    # Capturar frame
    frame = camera.read()
    
    # Detectar pose
    resultado = analisador.detectar(frame_rgb, frame_mao_ok = analisador.validar_bracoid)
    
    # Extrair pontos
    nariz, pescoco, cintura, pulso, pts = analisador.extrair_pontos(
        resultado.pose_landmarks[0], 
        ETAPAS[estado.indice_etapa]
    )
    
    # Calcular
    angulo = analisador.calcular_angulo(pescoco, cintura)
    (pulso, nariz)
    
    # Validar
    validacao = controlador.validar(angulo, lado, mao_ok)
    
    # Incrementar
    if validacao["valido"]:
        controlador.incrementar(validacao["incremento"])
    else:
        controlador.decrementar()
    
    # Verificar conclusão
    if controlador.contagem_pose >= META_FRAMES[dificuldade]:
        estado.proxima_etapa()
        controlador.resetar()
        
        if estado.indice_etapa >= len(ETAPAS):
            # Exercício concluído!
            break

# 5. Fechar
analisador.fechar()
```

---

**Versão:** 2.0  
**Última atualização:** Maio 2026