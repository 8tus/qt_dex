import sys
import os
import pygame
from PyQt6.QtWidgets import QApplication
from main_app import MainAPP

def main():
    app = QApplication(sys.argv)
    
    # Inicializar Pygame
    pygame.mixer.init()

    # Reproducir música en loop con volumen ajustable
    pygame.mixer.music.load("cancion.mp3")  # Ruta de tu archivo de música
    pygame.mixer.music.set_volume(0.0)  # Establecer el volumen (0.0 a 1.0)
    pygame.mixer.music.play(-1)  # Reproducir en loop (-1 significa loop infinito)
    
    # Cargar el estilo personalizado desde un archivo .qss
    load_style(app, "styles.qss")

    window = MainAPP()
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec())

def load_style(app, style_path):
    try:
        with open(style_path, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print(f"Error: archivo de estilo {style_path} no encontrado.")

if __name__ == "__main__":
    main()
