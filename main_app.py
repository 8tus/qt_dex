from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from app_controller import AppController
from cargador_pokedex import CargadorPokedex
from file_reader_thread import FileReaderThread
from menu import MenuPrincipal
from pantalla_carga import PantallaCarga
from aplicacion_pokedex import AplicacionPokedex
from aplicacion_creacion_equipo import AplicacionCreacionEquipo
from menu import MenuPrincipal
from aplicacion_pokedex import AplicacionPokedex
from aplicacion_ver_equipos import AplicacionVerEquipos
from pantalla_carga import PantallaCarga
from cargador_pokedex import CargadorPokedex
import os
from PyQt6.QtGui import QIcon


class MainAPP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokédex")

        # Crear el controlador de la aplicación
        self.app_controller = AppController()
    
        # Verificar si el archivo de icono existe
        icono_path = "pokeball.ico"
        if os.path.exists(icono_path):
            self.setWindowIcon(QIcon(icono_path))  # Cargar el ícono
        else:
            print(f"El archivo de icono no se encuentra: {icono_path}")  # Mensaje si no se encuentra

        # Crear el stacked_widget
        self.stacked_widget = QStackedWidget()

        # Crear y agregar las vistas (widgets)
        self.menu_principal = MenuPrincipal(self.stacked_widget)
        self.pokedex_app = AplicacionPokedex(self.app_controller, self.stacked_widget)
        self.creacion_equipo_app = AplicacionCreacionEquipo(self.stacked_widget, self.app_controller)  # Pasar app_controller y stacked_widget
        self.stacked_widget.addWidget(self.menu_principal)
        self.stacked_widget.addWidget(self.pokedex_app)
        self.stacked_widget.addWidget(self.creacion_equipo_app)
        self.stacked_widget.addWidget(AplicacionVerEquipos(self.stacked_widget))
        self.stacked_widget.addWidget(PantallaCarga())

        # Crear el hilo de carga de datos
        self.loader = FileReaderThread()
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
        # Asignar la Pokédex al controlador
        self.app_controller.datos_persistentes.pokedex = pokedex
        
        # Pasar la Pokédex a la vista de Crear Equipo
        self.creacion_equipo_app.cargar_lista_pokedex(pokedex)

        print("Pokédex cargada, cerrando pantalla de carga.")
        self.pantalla_carga.close()
        self.setCentralWidget(self.stacked_widget)
        self.pokedex_app.cargar_lista_pokedex(pokedex)
