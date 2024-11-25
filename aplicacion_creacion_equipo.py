from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QMessageBox

# Clase para crear equipos
class AplicacionCreacionEquipo(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.team = []
        self.pokedex = []  # Agregar un atributo para almacenar la lista de Pokémon

    def initUI(self):
        self.setWindowTitle("Crear Equipo")
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        self.team_name_input = QLineEdit(self)
        self.team_name_input.setPlaceholderText("Nombre del equipo")
        layout.addWidget(self.team_name_input)

        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.agregar_pokemon_al_equipo)
        layout.addWidget(self.list_widget)

        self.save_team_button = QPushButton('Guardar Equipo', self)
        self.save_team_button.clicked.connect(self.guardar_equipo)
        layout.addWidget(self.save_team_button)

        self.view_teams_button = QPushButton('Ver Equipos Guardados', self)
        self.view_teams_button.clicked.connect(self.mostrar_ver_equipos)
        layout.addWidget(self.view_teams_button)

        self.back_button = QPushButton('Volver al Menú Principal', self)
        self.back_button.clicked.connect(self.mostrar_menu_principal)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def cargar_pokemon_a_equipo(self, pokedex):
        # Cargar la lista de Pokémon en el QListWidget
        self.pokedex = pokedex
        self.list_widget.clear()  # Limpiar la lista antes de agregar los nuevos Pokémon
        for pokemon in self.pokedex:
            self.list_widget.addItem(pokemon['name'].capitalize())  # Agregar solo el nombre del Pokémon

    def agregar_pokemon_al_equipo(self, item):
        pokemon_name = item.text()
        if len(self.team) < 6:
            if pokemon_name not in self.team:
                self.team.append(pokemon_name)
                self.list_widget.addItem(f"¡{pokemon_name} agregado al equipo!")
            else:
                QMessageBox.warning(self, "Error", f"{pokemon_name} ya está en el equipo.")
        else:
            QMessageBox.warning(self, "Límite alcanzado", "El equipo ya tiene el máximo de 6 Pokémon.")

    def guardar_equipo(self):
        team_name = self.team_name_input.text().strip()
        if team_name and self.team:
            file_name = f"equipo_{team_name}.txt"
            with open(file_name, "w") as f:
                for pokemon in self.team:
                    f.write(pokemon + "\n")
            QMessageBox.information(self, "Éxito", f"El equipo {team_name} ha sido guardado.")
        
            # Actualizar la lista de equipos después de guardar
            self.actualizar_lista_equipos()
        else:
            QMessageBox.warning(self, "Error", "Introduce un nombre y agrega al menos un Pokémon al equipo.")

    def actualizar_lista_equipos(self):
        # Llamar a la vista de equipos guardados (index 3) y actualizar la lista
        self.stacked_widget.widget(3).cargar_equipos_guardados()

    def mostrar_ver_equipos(self):
        self.stacked_widget.setCurrentIndex(3)  # Cambia al índice de la vista de equipos guardados

    def mostrar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)
