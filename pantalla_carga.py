from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

class PantallaCarga(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cargando Datos")
        self.setGeometry(100, 100, 400, 300)  # Tamaño y posición de la ventana
        layout = QVBoxLayout()

        # Crear una etiqueta para mostrar el GIF
        self.label = QLabel(self)
        layout.addWidget(self.label)
        
        # Cargar el GIF de carga desde la misma carpeta del código
        movie = QMovie("cargando.gif")  # Ruta local si el GIF está en la misma carpeta
        self.label.setMovie(movie)
        
        # Iniciar la animación del GIF
        movie.start()
        
        self.setLayout(layout)