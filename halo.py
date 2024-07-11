import sys
import os
import threading
import speech_recognition as sr
import pyttsx3
import pyautogui as exe
import time
from subprocess import run
import pywhatkit as yt
from PyQt5.QtWidgets import QApplication
from interface import haloGUI 

audio = sr.Recognizer() #Instancia um reconhecedor de áudio para capturar e processar comandos de voz
halo = pyttsx3.init() #Inicializa o motor de síntese de voz para falar os comandos reconhecidos

class VoiceRecognitionThread(threading.Thread):  # executar a captura de comandos de voz em uma thread separada,permitindo a interface gráfica continue responsiva
    def __init__(self, callback, stop_callback): #Função que será chamada quando um comando for reconhecido
        super().__init__() #captura e processamento de voz
        self.audio = sr.Recognizer()
        self.callback = callback
        self.stop_callback = stop_callback

    def run(self): # escuta e processa comandos de voz, chamando o callback quando um comando é reconhecido
        while True:
            comando = self.voze_comandos()
            if comando is not None:
                self.callback(comando)

    def voze_comandos(self): #processamento do microfone
        comando = None
        try:
            with sr.Microphone(sample_rate=16000, chunk_size=1024) as source:
                print('Ajustando para o ruído ambiente...')
                self.audio.adjust_for_ambient_noise(source, duration=2)  # Aumente a duração para um ajuste mais preciso
                print('Ouvindo...')
                voz = self.audio.listen(source, timeout=10, phrase_time_limit=10)  # Ajuste os tempos conforme necessário
                print('Processando...')
                comando = self.processar_comando(voz)
                #áudio capturado é processado para reconhecer comandos, e se o comando incluir "halo", ele é retornado sem a palavra "halo"
                if comando and 'halo' in comando: 
                    comando_sem_halo = comando.replace('halo', '').strip()
                    print(f"Comando recebido: {comando_sem_halo}")
                    halo.say(comando_sem_halo) 
                    halo.runAndWait()
                    if 'encerrar' in comando_sem_halo:
                        self.stop_callback(0)
                    return comando_sem_halo  # Retorne o comando sem 'halo'
        except sr.RequestError as e:
            print(f"Erro de solicitação: {e}")
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido.")
        except sr.UnknownValueError:
            print("Não entendi o comando.")
        except Exception as e:
            print(f"Erro desconhecido: {e}")

        return None

    def processar_comando(self, voz): #Tenta reconhecer o comando usando a API do Google
        try:
            comando = self.audio.recognize_google(voz, language="pt-br")
            comando = comando.lower()
            return comando
        except sr.UnknownValueError:
            print("Tentando novamente...")
            return None
        except sr.RequestError as e:
            print(f"Erro de solicitação: {e}")
            return None

def executar_comandos(comando): #Executa ações com base no comando reconhecido
    if comando is not None: 
        if 'tocar' in comando: #tocar musica no spotfy
            musica = comando.replace('tocar', '').strip()
            os.system("spotify")
            time.sleep(5)
            exe.hotkey('ctrl', 'l')
            exe.write(musica, interval=0.5)
            for key in ['enter', 'pagedown', 'tab', 'tab', 'tab', 'enter']:
                time.sleep(0.5)
                exe.press(key)

        elif "abrir navegador" in comando: #abri o ópera
            exe.press('win')
            exe.write('Navegador Opera GX', interval=0.3)
            time.sleep(3)
            exe.press('enter')

        elif "abrir app" in comando: #abre um app selecionado
            item = comando.replace('abrir app', '').strip()
            exe.press('win')
            exe.write(item, interval=0.3)
            time.sleep(3)
            exe.press('enter')

        elif 'abrir site' in  comando: #abre um site selecionado
            item = comando.replace('abrir site', '').strip()
            exe.press('win')
            exe.write('Navegador Opera GX', interval=0.3)
            time.sleep(3)
            exe.press('enter')
            time.sleep(1)
            exe.hotkey('ctrl', 'l')
            exe.write(f'https://www.{item}.com', interval=0.1)
            exe.press('enter')

        elif 'pesquisar' in  comando: #realiza uma pesquisa
            pesquisar = comando.replace('pesquisar', '').strip()
            exe.press('win')
            exe.write('Navegador Opera GX', interval=0.3)
            time.sleep(3)
            exe.press('enter')
            time.sleep(1)
            exe.hotkey('ctrl', 'l')
            exe.write(pesquisar, interval=0.1)
            exe.press('enter')

        elif 'reproduzir' in  comando:# abre um video no youtube
            musica = comando.replace('reproduzir', '').strip()
            yt.playonyt(musica)

        elif 'fechar' in  comando: #fecha uma aba de um app
            exe.hotkey('alt', 'f4')

        elif 'tarefa' in  comando: #agenda uma tarefa no app to do list
            taref = comando.replace('tarefa', '').strip()
            exe.press('win')
            exe.write("to do", interval=0.5)
            exe.press('enter')
            time.sleep(3)
            exe.hotkey('ctrl', 'n')
            exe.write(taref, interval=0.5)
            time.sleep(3)
            exe.press('enter')
            exe.hotkey('alt', 'f4')

        elif 'aumentar volume' in  comando: #aumenta o volume do pc
            for _ in  range(5):
                exe.press('volumeup')

        elif 'diminuir volume' in  comando: #diminui o volume do pc
            for _ in  range(10):
                exe.press('volumedown')

        elif 'mudo' in  comando: #tira o volume do pc
            exe.press('volumemute')

        elif 'volume baixo' in  comando: #reduz muito o volume do pc
            for _ in  range(20):
                exe.press('volumedown')

        elif 'volume máximo' in  comando: #aumenta muito o volume do pc
            for _ in  range(100):
                exe.press('volumeup')

        elif 'pausar' in  comando: #utiliza o espaço pra pausar a aba principal
            exe.press('space')

        elif 'encerrar' in comando:# Força o encerramento do programa
            os._exit(0)  

def main(): #responsável por inicializar a aplicação gráfica e a thread de reconhecimento de voz.
    app = QApplication(sys.argv)
    gui = haloGUI()
    gui.show()
    # Iniciar a thread para reconhecimento de voz
    voice_thread = VoiceRecognitionThread(executar_comandos, os._exit)
    voice_thread.start()

    sys.exit(app.exec_()) #garante que a aplicação seja encerrada corretamente

if __name__ == "__main__": #verifica se o script está sendo executado diretamente
    main()
