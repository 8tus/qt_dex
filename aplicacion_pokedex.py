import asyncio
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QTextEdit, QLabel, QMessageBox, QProgressBar, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
import requests
import aiohttp

from app_controller import AppController
from pokedex import Pokedex
from pokemon import Pokemon

class AplicacionPokedex(QWidget):
    def __init__(self, app_controller: AppController, stacked_widget):
        super().__init__()
        self.app_controller = app_controller
        self.stacked_widget = stacked_widget  # La instancia del stacked_widget para cambiar las vistas
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pokédex")
        self.setGeometry(100, 100, 400, 600)
        layout = QVBoxLayout()

        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self.mostrar_detalles_pokemon)
        layout.addWidget(self.list_widget)

        self.search_button = QPushButton('Buscar Pokémon', self)
        self.search_button.clicked.connect(self.buscar_pokemon)
        layout.addWidget(self.search_button)

        self.search_input = QLineEdit(self)
        layout.addWidget(self.search_input)

        self.details_layout = QVBoxLayout()
        self.details_image = QLabel(self)
        self.details_text = QTextEdit(self)
        self.details_text.setReadOnly(True)

        # Crear las barras de progreso para las estadísticas con etiquetas
        self.ps_label = QLabel('PS:', self)
        self.ps_bar = QProgressBar(self)
        self.ps_bar.setMaximum(255)  # Valor máximo ajustado
        self.ps_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        self.attack_label = QLabel('Ataque:', self)
        self.attack_bar = QProgressBar(self)
        self.attack_bar.setMaximum(250)  # Valor máximo ajustado
        self.attack_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        self.defense_label = QLabel('Defensa:', self)
        self.defense_bar = QProgressBar(self)
        self.defense_bar.setMaximum(250)  # Valor máximo ajustado
        self.defense_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        self.special_attack_label = QLabel('Ataque Especial:', self)
        self.special_attack_bar = QProgressBar(self)
        self.special_attack_bar.setMaximum(250)  # Valor máximo ajustado
        self.special_attack_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        self.special_defense_label = QLabel('Defensa Especial:', self)
        self.special_defense_bar = QProgressBar(self)
        self.special_defense_bar.setMaximum(250)  # Valor máximo ajustado
        self.special_defense_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        self.speed_label = QLabel('Velocidad:', self)
        self.speed_bar = QProgressBar(self)
        self.speed_bar.setMaximum(250)  # Valor máximo ajustado
        self.speed_bar.setTextVisible(False)  # Ocultar el texto de porcentaje

        # Agregar las etiquetas y las barras de progreso al layout
        self.details_layout.addWidget(self.details_image)
        self.details_layout.addWidget(self.details_text)

        self.details_layout.addWidget(self.ps_label)
        self.details_layout.addWidget(self.ps_bar)

        self.details_layout.addWidget(self.attack_label)
        self.details_layout.addWidget(self.attack_bar)

        self.details_layout.addWidget(self.defense_label)
        self.details_layout.addWidget(self.defense_bar)

        self.details_layout.addWidget(self.special_attack_label)
        self.details_layout.addWidget(self.special_attack_bar)

        self.details_layout.addWidget(self.special_defense_label)
        self.details_layout.addWidget(self.special_defense_bar)

        self.details_layout.addWidget(self.speed_label)
        self.details_layout.addWidget(self.speed_bar)

        layout.addLayout(self.details_layout)

        self.back_button = QPushButton('Volver al Menú Principal', self)
        self.back_button.clicked.connect(self.mostrar_menu_principal)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    async def fetch_image(self, session, url):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            return None

    def cargar_lista_pokedex(self, pokedex: Pokedex):
        """Carga la lista de Pokémon en el QListWidget y establece los datos."""
        self.pokedex = pokedex
        self.list_widget.clear()
        for pokemon in self.pokedex.pokemones:
            item = QListWidgetItem(pokemon.nombre.capitalize())
            self.list_widget.addItem(item)
        # Inicia la carga de íconos de manera asincrónica
        asyncio.run(self.cargar_iconos_pokemon())

    async def cargar_iconos_pokemon(self):
        async with aiohttp.ClientSession() as session:
            for i in range(self.list_widget.count()):
                pokemon:Pokemon = self.pokedex.pokemones[i]
                image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{pokemon.numero}.png"
                if image_url:
                    image_data = await self.fetch_image(session, image_url)
                    if image_data:
                        pixmap = QPixmap()
                        pixmap.loadFromData(image_data)
                        icon = QIcon(pixmap)
                        self.list_widget.item(i).setIcon(icon)

    def buscar_pokemon(self):
        pokemon_to_search = self.search_input.text().strip().lower()
        if pokemon_to_search:
            self.mostrar_detalles_pokemon(pokemon_to_search)
            self.search_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Introduce un nombre de Pokémon para buscar.")

    def mostrar_detalles_pokemon(self, item):
        if isinstance(item, str):
            pokemon_name = item
        else:
            pokemon_name = item.text().lower()

        found_pokemon = list(filter(lambda p: p.nombre.lower() == pokemon_name.lower(), self.pokedex.pokemones))

        if found_pokemon:
            pokemon: Pokemon = found_pokemon[0]
            tipos_str = ""
            if len(pokemon.tipos) > 1:
                tipos_str = f"Tipos: {pokemon.tipos[0].nombre} - {pokemon.tipos[1].nombre}"
            else:
                tipos_str = f"Tipo: {pokemon.tipos[0].nombre}"
            # movimientos_str = ''
            # for i in range(len(pokemon.info.movimientos)):
            #     movimientos_str = pokemon.info.movimientos[i].nombre
            #     if i != 0 and i != len(pokemon.info.habilidades)-1:
            #         movimientos_str += ' - '

            details = (
                f"Nombre: {pokemon.nombre.capitalize()}\n"
                f"Número: {pokemon.numero}\n"
                f"Altura: {pokemon.altura} m\n"
                f"Peso: {pokemon.peso} kg\n"
                f"{tipos_str}\n"
                # f"{movimientos_str}\n"
            )
            self.details_text.setText(details)
            print('pokemon ps', pokemon.estadisticas.ps)
            # Establecer valores en las barras de progreso (mostrar valores enteros)
            self.ps_bar.setValue(pokemon.estadisticas.ps)  # PS
            self.attack_bar.setValue(pokemon.estadisticas.ataque_especial)  # Ataque
            self.defense_bar.setValue(pokemon.estadisticas.defensa)  # Defensa
            self.special_attack_bar.setValue(pokemon.estadisticas.ataque_especial)  # Ataque Especial
            self.special_defense_bar.setValue(pokemon.estadisticas.defensa_especial)  # Defensa Especial
            self.speed_bar.setValue(pokemon.estadisticas.velocidad)  # Velocidad

            # Mostrar los valores enteros junto a las barras
            self.ps_label.setText(f"PS: {pokemon.estadisticas.ps}")
            self.attack_label.setText(f"Ataque: {pokemon.estadisticas.ataque}")
            self.defense_label.setText(f"Defensa: {pokemon.estadisticas.defensa}")
            self.special_attack_label.setText(f"Ataque Especial: {pokemon.estadisticas.ataque_especial}")
            self.special_defense_label.setText(f"Defensa Especial: {pokemon.estadisticas.defensa_especial}")
            self.speed_label.setText(f"Velocidad: {pokemon.estadisticas.velocidad}")

            # Cargar la imagen
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{pokemon.numero}.png"
            if image_url:
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(image_url).content)
                self.details_image.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        else:
            QMessageBox.warning(self, "Error", "Pokémon no encontrado.")

    def mostrar_menu_principal(self):
        self.stacked_widget.setCurrentIndex(0)  # Cambiar al primer widget en el stacked_widget
