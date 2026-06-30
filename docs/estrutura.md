# 📁 ESTRUTURA DO PROJETO - Vida em Movimento

## Organização de Pastas

```
vida-em-movimento/
│
├── main.py                              # Ponto de entrada da aplicação
├── requirements.txt                     # Dependências Python
├── pose_landmarker_full.task            # Modelo MediaPipe (baixar)
│
├── src/                                 # Código-fonte principal
│   ├── __init__.py
│   ├── config.py                        # Configurações globais
│   │
│   ├── vision/                          # Módulo de visão computacional
│   │   ├── __init__.py
│   │   └── analisador.py               # Detecção e análise de pose
│   │
│   ├── core/                            # Lógica de negócio
│   │   ├── __init__.py
│   │   └── exercicio.py                # Controlador e estado
│   │
│   └── interface/                       # Interface gráfica
│       ├── __init__.py
│       ├── app.py                      # Aplicação principal
│       ├── tema.py                     # Estilos e temas
│       └── telas.py                    # Todas as telas
│
├── assets/                              # Recursos (imagens, vídeos)
│   ├── Aviso.png                       # Logo/imagem de boas-vindas
│   └── exercicios/
│       ├── exercicio01.mp4             # Vídeo lado DIREITO
│       └── exercicio1.1.mp4            # Vídeo lado ESQUERDO
│
├── docs/                                # Documentação
│   ├── ESTRUTURA.md                    # Este arquivo
│   ├── API.md                          # Documentação das classes
│   └── ALTERACOES.md                   # Guia de alterações
│
└── README.md                            # Guia de instalação e uso

```

## Descrição dos Módulos

### `src/config.py`
Centraliza todas as configurações do projeto:
- Caminhos de arquivos
- Ângulos e tolerâncias por dificuldade
- Configurações de câmera e vídeo
- Mensagens da aplicação

### `src/vision/analisador.py`
Módulo responsável por:
- Detectar pose corporal usando MediaPipe
- Extrair pontos-chave do corpo
- Calcular ângulos de inclinação
- Validar posição do braço

**Classe Principal:** `AnalisadorFisio`

### `src/core/exercicio.py`
Lógica do exercício:
- Validar se o movimento está correto
- Gerenciar dificuldade (fácil/médio/difícil)
- Controlar contagem de poses válidas
- Gerenciar estado do exercício

**Classes Principais:** 
- `ControladorExercicio`
- `EstadoExercicio`

### `src/interface/tema.py`
Define estilo visual:
- Cores da aplicação
- Estilos CSS para botões
- Estilos para labels e barras de progresso
- Fonte e tamanhos de texto

**Classe Principal:** `Tema` (estática)

### `src/interface/telas.py`
Implementa todas as telas:
- `TelaInicial`: Boas-vindas
- `TelaDificuldade`: Seleção de nível
- `TelaExercicio`: Exercício com câmera
- `TelaFinal`: Conclusão e opções

### `src/interface/app.py`
Gerenciador principal:
- Controla navegação entre telas
- Gerencia stack de widgets
- Passa callbacks entre telas

**Classe Principal:** `App`

---

## Fluxo de Dados

```
main.py
    ↓
App (interface/app.py)
    ├── TelaInicial
    │   ├── Clique → abrir_dificuldade()
    │   └── Callback: callback
    │
    ├── TelaDificuldade
    │   ├── Seleciona nível
    │   ├── Callback: iniciar_exercicio(dificuldade)
    │   └── Passa para TelaExercicio
    │
    ├── TelaExercicio
    │   ├── Inicia AnalisadorFisio (vision/analisador.py)
    │   ├── Inicia ControladorExercicio (core/exercicio.py)
    │   ├── Loop: captura frame → análise → validação → feedback
    │   ├── Incrementa contagem com base em validação
    │   └── Callback: abrir_final()
    │
    └── TelaFinal
        ├── Mostra resultado
        ├── Opção: repetir (volta para dificuldade)
        └── Opção: sair (volta para inicial)
```

---

## Responsabilidades das Classes

### AnalisadorFisio
```python
# Uso típico
analisador = AnalisadorFisio("caminho/modelo.task")

# Detectar pose
resultado = analisador.detectar(frame_rgb, frame_id)

# Extrair pontos
nariz, pescoco, cintura, pulso, pts = analisador.extrair_pontos(
    resultado.pose_landmarks[0], 
    "ESQUERDO"
)

# Calcular ângulo
angulo = analisador.calcular_angulo(pescoco, cintura)

# Validar braço
braço_ok = analisador.validar_braco(pulso, nariz)
```

### ControladorExercicio
```python
# Uso típico
controlador = ControladorExercicio()
controlador.definir_dificuldade("medio")

# Validar movimento
resultado = controlador.validar(
    inclinacao=110,
    lado="ESQUERDO",
    mao_ok=True
)

# Incrementar/decrementar
if resultado["valido"]:
    controlador.incrementar(resultado["incremento"])
else:
    controlador.decrementar()

# Verificar conclusão
if controlador.contagem_pose >= meta_frames:
    # Exercício concluído
    pass
```

### EstadoExercicio
```python
# Uso típico
estado = EstadoExercicio()

# Avançar de etapa
estado.proxima_etapa()

# Acessar informações
lado_atual = ETAPAS[estado.indice_etapa]

# Resetar
estado.resetar()
```

### Tema
```python
# Uso típico
# Aplicar estilo
widget.setStyleSheet(Tema.obter_estilo("botao_principal"))

# Obter cor
cor = Tema.obter_cor("primaria")
```

---

## Configurações em `config.py`

### Ângulos Alvo
```python
META_ANGULAR = {
    "ESQUERDO": 110,  # Inclinação para esquerda
    "DIREITO": 70     # Inclinação para direita
}
```

### Tolerâncias por Dificuldade
```python
TOLERANCIAS = {
    "facil": 25,      # ±25° de erro aceitável
    "medio": 15,      # ±15° de erro aceitável
    "dificil": 8      # ±8° de erro aceitável
}
```

### Metas de Frames
```python
META_FRAMES = {
    "facil": 80,      # 80 frames corretos
    "medio": 100,     # 100 frames corretos
    "dificil": 120    # 120 frames corretos
}
```

---

## Integração de Componentes

```
TelaExercicio
    │
    ├── usa AnalisadorFisio
    │   └── detecta pose do frame
    │
    ├── usa ControladorExercicio
    │   └── valida movimento
    │
    ├── usa EstadoExercicio
    │   └── rastreia etapas
    │
    └── usa Tema
        └── aplica estilos
```

---

## Ciclo de Vida

1. **Inicialização** (main.py)
   - Cria QApplication
   - Cria App
   - Exibe em fullscreen

2. **TelaInicial**
   - Usuário clica "Começar"
   - Navega para TelaDificuldade

3. **TelaDificuldade**
   - Usuário seleciona nível
   - Inicia TelaExercicio

4. **TelaExercicio**
   - Inicializa câmera e modelo
   - Loop: 30 FPS
     - Captura frame
     - Detecta pose
     - Valida movimento
     - Atualiza UI
   - Verifica conclusão

5. **TelaFinal**
   - Mostra resultado
   - Usuário escolhe:
     - Repetir → volta para TelaDificuldade
     - Sair → volta para TelaInicial

---

## Recursos Necessários

### Arquivos Obrigatórios
- `pose_landmarker_full.task` - Modelo MediaPipe
- `assets/Aviso.png` - Imagem de boas-vindas
- `assets/exercicios/exercicio01.mp4` - Vídeo lado direito
- `assets/exercicios/exercicio1.1.mp4` - Vídeo lado esquerdo

### Hardware
- Câmera USB (mínimo 640x480)
- Processador com suporte a 30 FPS
- Mínimo 2GB RAM

---

## Notas Técnicas

1. **MediaPipe**: Usa PoseLandmarkerOptions (versão nova)
2. **OpenCV**: Apenas para captura de câmera e renderização
3. **PySide6**: Interface gráfica com QStackedWidget
4. **NumPy**: Cálculos matemáticos (ângulos)

---

**Última atualização:** Maio 2026
**Versão:** 2.0 (Consolidada)