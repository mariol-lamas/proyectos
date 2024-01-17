from pytube import YouTube
import PyQt5.QtWidgets as pq
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
class App(pq.QMainWindow):
    def __init__(self):
        super().__init__()
        self.principal_config()
        self.botones_centrales()
        pass

    def principal_config(self):
        # Configuramos la ventana principal
        self.setWindowTitle('Youtube Downloader')
        self.setGeometry(100, 100, 400, 200)
        # Establecemos el tamaño fijo de la ventana
        self.setFixedSize(400, 200)
    
    def botones_centrales(self):
        # Creamos un widget central para la ventana
        central_widget = pq.QWidget(self)
        self.setCentralWidget(central_widget)

        # Creamos un layout vertical para el widget central
        layout = pq.QVBoxLayout(central_widget)
        # Añadimos una imagen al QLabel
        imagen = pq.QLabel(self)
        pixmap = QPixmap('src/img/yt_logo')  # Reemplaza con la ruta de tu imagen
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)  # Ajustamos el tamaño manteniendo la proporción
        imagen.setPixmap(pixmap)
        imagen.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen)

        # Creamos un QLabel y lo añadimos al layout
        self.label = pq.QLabel('¡Bienvenido a Youtube Downloader!', self)
        layout.addWidget(self.label,alignment=Qt.AlignCenter)
        layout.addSpacing(10)

        #Creamos la entrada de texto
        self.texto=pq.QLineEdit(self)
        layout.addWidget(self.texto,alignment=Qt.AlignCenter)

        #Creamos el boton
        self.boton=pq.QPushButton('Descargar',self)
        self.boton.clicked.connect(self.descargar)
        layout.addWidget(self.boton, alignment=Qt.AlignCenter)
    
    def descargar(self):
        texto=self.texto.text()
        print(f'Este es el enlace : {texto}')
        try:
            yt=YouTube(texto)
            yt=yt.streams.get_highest_resolution()
            yt.download()
            print('\nDescarga completada con exito!!')
        except:
            print('\nHa ocurrido un error!\n\n¿Has introducido adecuadamente la url?')
        
    

    def run(self):
        self.show()


if __name__=='__main__':
    app=pq.QApplication(sys.argv)
    ventana_principal=App()
    ventana_principal.run()
    app.exec_()