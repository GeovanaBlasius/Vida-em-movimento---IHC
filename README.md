# Vida em Movimento

> Exercícios de alongamento assistidos por Inteligência Artificial para promover a consciência corporal em idosos e pessoas em processo de reabilitação.

---

## Sobre o Projeto

**Vida em Movimento** é uma aplicação desktop que utiliza visão computacional para guiar e corrigir exercícios físicos em tempo real. Através da câmera do computador, o sistema detecta a pose do usuário, analisa o movimento e fornece feedback instantâneo na tela — sem necessidade de sensores externos.

O projeto foi desenvolvido como trabalho acadêmico na disciplina de **Interação Humano-Computador (IHC)**, com foco em acessibilidade e facilidade de uso para o público idoso.

---

## ✨ Funcionalidades

- **Detecção de pose em tempo real** via câmera, usando MediaPipe
- **3 exercícios guiados** com vídeo demonstrativo lado a lado
- **3 níveis de dificuldade**: Fácil, Médio e Difícil
- **Feedback visual e textual** em tempo real durante o exercício
- **Fluxo completo**: tela inicial → seleção de dificuldade → exercício → resultado

### Exercícios disponíveis

| Exercício | Descrição |
|---|---|
| Elevação Frontal Unilateral | Elevação do braço para frente, alternando os lados |
| Elevação Lateral Bilateral | Elevação dos dois braços lateralmente |
| Inclinação Lateral | Inclinação do tronco para os lados com braço elevado |

---

## Como Instalar (Usuário Final)

> Não é necessário instalar Python ou nenhuma dependência.

### ⬇️ [Baixar instalador — Windows](https://github.com/GeovanaBlasius/Vida-em-movimento---IHC/releases/latest)

1. Clique no link acima e baixe o arquivo **`VidaEmMovimento-Setup-Windows.exe`**
2. Execute o instalador e siga os passos
3. Abra o app pelo atalho criado na área de trabalho ou no menu Iniciar

> ⚠️ O Windows pode exibir um aviso de segurança. Clique em **"Mais informações" → "Executar assim mesmo"** para prosseguir.

---

## 🛠️ Como Rodar o Código Fonte

### Pré-requisitos
- Python 3.11+
- Câmera conectada ao computador

### Instalação

```bash
# Clone o repositório
git clone https://github.com/GeovanaBlasius/Vida-em-movimento---IHC.git
cd Vida-em-movimento---IHC

# Instale as dependências
pip install -r requirements.txt

# Execute
python main.py
```

### Gerar o executável (Windows)

```bash
# Execute o script de build (requer Inno Setup 6 instalado)
build\build.bat
```

O instalador será gerado em `instaladores\VidaEmMovimento-Setup-Windows.exe`.

---

## 🗂️ Estrutura do Projeto

```
Vida em Movimento/
│
├── main.py                        # Ponto de entrada
├── requirements.txt               # Dependências
├── pose_landmarker_full.task      # Modelo de pose MediaPipe
│
├── src/
│   ├── config.py                  # Configurações globais
│   ├── core/
│   │   ├── analisador.py          # Detecção e análise de pose
│   │   ├── exercicios/            # Lógica de cada exercício
│   │   └── controle/              # Estado e validação
│   └── interface/
│       ├── app.py                 # Gerenciador de telas
│       ├── tema.py                # Estilos visuais
│       ├── telas/                 # Telas da aplicação
│       └── widgets/               # Componentes reutilizáveis
│
├── assets/
│   ├── Aviso.png                  # Imagem de boas-vindas
│   └── exercicios/                # Vídeos demonstrativos
│
└── build/
    ├── build.bat                  # Script de build (Windows)
    └── build_mac.sh               # Script de build (Mac)
```

---

## 🚀 Tecnologias

| Tecnologia | Uso |
|---|---|
| [Python 3.11](https://python.org) | Linguagem principal |
| [PySide6](https://doc.qt.io/qtforpython/) | Interface gráfica (Qt) |
| [MediaPipe](https://mediapipe.dev/) | Detecção de pose corporal |
| [OpenCV](https://opencv.org/) | Captura de câmera e processamento de vídeo |
| [NumPy](https://numpy.org/) | Cálculos de ângulos e geometria |

---

## 📐 Fluxo da Aplicação

```
Tela Inicial
    ↓ (clica INICIAR)
Seleção de Dificuldade  →  Fácil / Médio / Difícil
    ↓
Tela do Exercício
    ├── Câmera ao vivo com esqueleto detectado
    ├── Vídeo demonstrativo do exercício
    └── Feedback em tempo real
    ↓ (exercício concluído)
Tela Final  →  Repetir ou Voltar ao início
```

---

## Organizadores do projeto

**Geovana Blasius**
- GitHub: [@GeovanaBlasius](https://github.com/GeovanaBlasius)
- Email: blasiusgeovana61@gmail.com

**Davi Bianchi Ayres**
- GitHub: [@Davibianchi01](https://github.com/Davibianchi01)
- Email: dbianchiayres@gmail.com

**Miguel Antonio Campos de Oliveira**
- GitHub: [@MiqueasGames](https://github.com/MiqueasGames)
- Email: Omiguelantonio190@gmail.com

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

As bibliotecas utilizadas possuem suas próprias licenças. Consulte o arquivo [NOTICES.md](NOTICES.md) para detalhes completos de atribuição de terceiros.
