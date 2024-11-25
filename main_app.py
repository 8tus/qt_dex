import os
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from app_controller import AppController
from cargador_pokedex import CargadorPokedex
from menu import MenuPrincipal
from pantalla_carga import PantallaCarga
from aplicacion_pokedex import AplicacionPokedex
from aplicacion_creacion_equipo import AplicacionCreacionEquipo
from aplicacion_ver_equipos import AplicacionVerEquipos


class MainAPP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex")

        # creamos app controller
        self.app_controller = AppController()
    
        # Verificar que el archivo icono.ico exista en la misma carpeta
        icono_path = "pokeball.ico"  # Ruta relativa si el archivo está en la misma carpeta
        if os.path.exists(icono_path):
            self.setWindowIcon(QIcon(icono_path))  # Si el archivo existe, se carga
        else:
            print(f"El archivo de icono no se encuentra: {icono_path}")  # Mensaje si no se encuentra

        # Crear los widgets de la aplicación
        self.stacked_widget = QStackedWidget()
        self.menu_principal = MenuPrincipal(self.stacked_widget)
        self.pokedex_app = AplicacionPokedex(self.app_controller)
        self.stacked_widget.addWidget(self.menu_principal)
        self.stacked_widget.addWidget(self.pokedex_app)
        self.stacked_widget.addWidget(AplicacionCreacionEquipo(self.stacked_widget))
        self.stacked_widget.addWidget(AplicacionVerEquipos(self.stacked_widget))
        self.stacked_widget.addWidget(PantallaCarga())

        # Crear el hilo de carga de datos
        self.loader = CargadorPokedex()
        self.loader.pokedex_cargada.connect(self.on_pokedex_loaded)
        

        # Crear la pantalla de carga
        self.pantalla_carga = PantallaCarga()
        self.inicio_carga_datos_async()
        

    def inicio_carga_datos_async(self):
        # Mostrar la pantalla de carga
        self.pantalla_carga.show()
        self.loader.start()

        # Mostrar la ventana principal
        self.setCentralWidget(self.pantalla_carga)  # Se pone la pantalla de carga a

    def on_pokedex_loaded(self, pokedex):
        self.app_controller.datos_persistentes.pokedex = pokedex
        print("pokedex cargada cerrar loading")
        self.pantalla_carga.close
        self.setCentralWidget(self.stacked_widget)
        self.pokedex_app.cargar_lista_pokedex(pokedex)
        
    
