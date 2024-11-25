from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox
import os

class AplicacionVerEquipos(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ver Equipos Guardados")
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.mostrar_detalles_equipo)
        layout.addWidget(self.list_widget)

        # Botón para eliminar equipo
        self.delete_button = QPushButton('Eliminar Equipo', self)
        self.delete_button.clicked.connect(self.eliminar_equipo)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton('Volver al Menú Principal', self)
        self.back_button.clicked.connect(self.mostrar_menu_principal)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.cargar_equipos_guardados()

    def cargar_equipos_guardados(self):
        self.list_widget.clear()
        for filename in os.listdir():
            if filename.startswith("equipo_") and filename.endswith(".txt"):
                self.list_widget.addItem(filename)

    def mostrar_detalles_equipo(self, item):
        self.equipo_nombre = item.text()  # Guardar el nombre del equipo seleccionado
        with open(self.equipo_nombre, "r") as f:
            equipo_pokemon = f.readlines()
        detalles = "\n".join([pokemon.strip() for pokemon in equipo_pokemon])
        QMessageBox.information(self, "Detalles del Equipo", f"Pokémon en el equipo {self.equipo_nombre}:\n{detalles}")

    def eliminar_equipo(self):
        if hasattr(self, 'equipo_nombre'):
            confirmacion = QMessageBox.question(self, "Confirmar Eliminación", 
                                                f"¿Estás seguro de que deseas eliminar el equipo {self.equipo_nombre}?", 
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirmacion == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(self.equipo_nombre)  # Eliminar el archivo del equipo
                    QMessageBox.information(self, "Éxito", f"El equipo {self.equipo_nombre} ha sido eliminado.")
                    self.cargar_equipos_guardados()  # Actualizar la lista de equipos
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo eliminar el equipo. Error: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No se ha seleccionado un equipo para eliminar.")

    def mostrar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)