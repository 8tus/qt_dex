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
        """Cargar los equipos guardados en el QListWidget."""
        self.list_widget.clear()  # Limpiar la lista antes de cargar nuevos equipos
        for filename in os.listdir("equipos"):
            if filename.startswith("equipo_") and filename.endswith(".txt"):
                self.list_widget.addItem(filename)  # Agregar cada equipo a la lista

    def mostrar_detalles_equipo(self, item):
        equipo_nombre = item.text()
        try:
            with open(f"equipos/{equipo_nombre}", "r") as file:
                pokemon_names = file.readlines()
                pokemon_list = [name.strip() for name in pokemon_names]
                # Mostrar detalles de los Pokémon en el equipo
                detalle = "\n".join(pokemon_list)
                QMessageBox.information(self, f"Detalles de {equipo_nombre}", detalle)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"No se encontró el equipo '{equipo_nombre}'.")

    def eliminar_equipo(self):
        equipo_nombre = self.list_widget.currentItem().text()
        if equipo_nombre:
            try:
                os.remove(f"equipos/{equipo_nombre}")
                self.cargar_equipos_guardados()  # Recargar la lista de equipos
                QMessageBox.information(self, "Equipo Eliminado", f"El equipo '{equipo_nombre}' ha sido eliminado.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar el equipo '{equipo_nombre}'. Error: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No has seleccionado un equipo para eliminar.")
            
    def mostrar_menu_principal(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))  # Cambiar a la vista principal
