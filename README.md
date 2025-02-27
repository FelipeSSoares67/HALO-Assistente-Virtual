                                 Halo - Assistente Virtual com Interface Gráfica
Halo é um assistente virtual baseado em reconhecimento de voz e interface gráfica que permite executar comandos no computador por meio de interações de voz. Ele utiliza bibliotecas como **PyQt5**, **speech_recognition**, **pyttsx3** e **pyautogui** para oferecer uma experiência interativa.

Funcionalidades
- Reconhecimento de comandos de voz
- Interface gráfica com um avatar animado
- Execução de comandos no sistema operacional
- Controle de mídia e volume
- Abertura de sites, aplicativos e buscas online
- Suporte a comandos personalizados

Tecnologias Utilizadas
- **Python** (Linguagem principal)
- **PyQt5** (Interface gráfica)
- **speech_recognition** (Reconhecimento de voz)
- **pyttsx3** (Síntese de fala)
- **pyautogui** (Automatização de comandos no sistema)
- **sounddevice** e **numpy** (Análise de áudio)
- **matplotlib** (Visualização do espectro de áudio)

Requisitos de Instalação
Antes de executar o Halo, instale as dependências necessárias:
```sh
pip install PyQt5 speechrecognition pyttsx3 pyautogui sounddevice numpy matplotlib pillow pywhatkit
```

Como Executar
1. Clone o repositório ou baixe os arquivos do projeto.
2. Execute o script principal:
   ```sh
   python halo.py
   ```

Comandos Disponíveis
| Comando | Ação |
|---------|------|
| **"Tocar [música]"** | Abre o Spotify e toca a música especificada |
| **"Abrir navegador"** | Abre o Opera GX |
| **"Abrir app [nome]"** | Abre o aplicativo especificado |
| **"Abrir site [nome]"** | Abre um site no navegador |
| **"Pesquisar [termo]"** | Faz uma busca na web |
| **"Reproduzir [vídeo]"** | Abre um vídeo no YouTube |
| **"Fechar"** | Fecha a janela ativa |
| **"Tarefa [descrição]"** | Adiciona uma tarefa no app To-Do |
| **"Aumentar volume"** | Aumenta o volume do sistema |
| **"Diminuir volume"** | Diminui o volume do sistema |
| **"Mudo"** | Silencia o volume |
| **"Volume baixo"** | Reduz o volume significativamente |
| **"Volume máximo"** | Aumenta o volume ao máximo |
| **"Pausar"** | Pausa ou retoma mídia |
| **"Encerrar"** | Fecha o assistente |

## Estrutura do Projeto
```
Halo/
├── img/
│   ├── avatar.png
├── halo.py
├── interface.py
├── README.md
```

## Personalização
- Para modificar a imagem do avatar, substitua **img/avatar.png**.
- Novos comandos podem ser adicionados na função `executar_comandos()`.

## Contribuição
Sinta-se à vontade para contribuir com melhorias!
