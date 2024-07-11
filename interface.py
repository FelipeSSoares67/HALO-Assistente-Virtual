import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QPalette
from PyQt5.QtCore import Qt
from PIL import Image

class haloGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initAudio()

    def initUI(self):
        self.setWindowTitle("Halo")
        self.setGeometry(440, 200, 500, 300)

        self.setWindowFlags(Qt.FramelessWindowHint)

        layout = QVBoxLayout()

        # Load avatar image and resize
        avatar_path = "img/avatar.png" 
        avatar = Image.open(avatar_path)
        avatar = avatar.resize((500, 300), Image.LANCZOS)
        avatar = avatar.convert("RGBA")  # Ensure transparency handling
        data = avatar.tobytes("raw", "RGBA")
        qimage = QImage(data, avatar.size[0], avatar.size[1], QImage.Format_RGBA8888)
        self.avatar_pixmap = QPixmap.fromImage(qimage)

        # imagem de fundo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(self.avatar_pixmap))
        self.setPalette(palette)

        # grafico de audio
        self.figure, self.ax = plt.subplots(facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(500, 300)  # Fixed size for the canvas
        self.canvas.setStyleSheet("background:transparent;")
        self.canvas.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def initAudio(self):
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        
        # Aplique suavização aos dados de áudio
        smoothed_data = np.convolve(indata[:, 0], np.ones(10)/10, mode='same')
        
        # Defina um limite para detectar fala
        threshold = 0.02  # Ajuste este valor conforme suas necessidades
        if np.max(np.abs(smoothed_data)) < threshold:
            smoothed_data = np.zeros_like(smoothed_data)  # Defina como zero se estiver abaixo do limite

        # Atualize o gráfico com os dados de áudio suavizados
        self.ax.clear()
        self.ax.plot(smoothed_data, color='red')
        self.ax.set_ylim([-0.5, 0.5])  # Fixe os limites do eixo y para uma exibição mais estável
        self.ax.axis('off')  # Oculte os eixos para uma melhor visualização
        self.canvas.draw()

    def closeEvent(self, event):
        self.stream.stop()
        self.stream.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    gui = haloGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
