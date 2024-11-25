from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

class MenuPrincipal(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pokédex")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.pokedex_button = QPushButton('Pokédex', self)
        self.pokedex_button.clicked.connect(self.show_pokedex)
        layout.addWidget(self.pokedex_button)

        self.team_button = QPushButton('Crear Equipo', self)
        self.team_button.clicked.connect(self.show_team_creation)
        layout.addWidget(self.team_button)

        self.view_teams_button = QPushButton('Ver Equipos Guardados', self)
        self.view_teams_button.clicked.connect(self.show_team_viewer)
        layout.addWidget(self.view_teams_button)

        self.exit_button = QPushButton('Salir', self)
        self.exit_button.clicked.connect(self.close_application)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def show_pokedex(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_team_creation(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_team_viewer(self):
        self.stacked_widget.setCurrentIndex(3)

    def close_application(self):
        QApplication.instance().quit()
