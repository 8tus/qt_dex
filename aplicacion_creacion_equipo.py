from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
import aiohttp
import asyncio
from PyQt6.QtWidgets import QListWidgetItem
import os
from aplicacion_ver_equipos import AplicacionVerEquipos
from clases import Pokemon, Pokedex, Equipo

class AplicacionCreacionEquipo(QWidget):
    def __init__(self, stacked_widget, app_controller):
        super().__init__()
        self.stacked_widget = stacked_widget  # Guardamos la referencia a stacked_widget
        self.app_controller = app_controller
        self.pokemon_equipo = Equipo("Equipo de Prueba")  # Inicializamos el equipo vacío
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Crear Equipo")
        self.setGeometry(100, 100, 400, 600)
        layout = QVBoxLayout()

        # Crear un botón para volver al menú principal
        self.volver_button = QPushButton("Volver al Menú Principal", self)
        self.volver_button.clicked.connect(self.volver_al_menu_principal)
        layout.addWidget(self.volver_button)

        # Crear un QListWidget para mostrar los Pokémon
        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        # Crear un botón para agregar el Pokémon seleccionado al equipo
        self.add_button = QPushButton("Agregar al Equipo", self)
        self.add_button.clicked.connect(self.agregar_al_equipo)
        layout.addWidget(self.add_button)

        # Crear un campo de texto para el nombre del equipo
        self.nombre_equipo_input = QLineEdit(self)
        self.nombre_equipo_input.setPlaceholderText("Ingresa el nombre del equipo")
        layout.addWidget(self.nombre_equipo_input)

        # Crear un botón para guardar el equipo
        self.guardar_button = QPushButton("Guardar Equipo", self)
        self.guardar_button.clicked.connect(self.guardar_equipo)
        layout.addWidget(self.guardar_button)

        # Crear una etiqueta para mostrar el nombre del Pokémon seleccionado
        self.selected_pokemon_label = QLabel("Selecciona un Pokémon para agregar al equipo.", self)
        layout.addWidget(self.selected_pokemon_label)

        # Establecer el layout
        self.setLayout(layout)

    async def fetch_image(self, session, url):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            return None

    async def cargar_iconos_pokemon(self):
        async with aiohttp.ClientSession() as session:
            for i in range(self.list_widget.count()):
                pokemon: Pokemon = self.pokedex.pokemones[i]
                image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{pokemon.numero}.png"
                if image_url:
                    image_data = await self.fetch_image(session, image_url)
                    if image_data:
                        pixmap = QPixmap()
                        pixmap.loadFromData(image_data)
                        icon = QIcon(pixmap)
                        self.list_widget.item(i).setIcon(icon)

    def cargar_lista_pokedex(self, pokedex: Pokedex):
        """Carga la lista de Pokémon en el QListWidget y establece los datos."""
        self.pokedex = pokedex
        self.list_widget.clear()
        for pokemon in self.pokedex.pokemones:
            item = QListWidgetItem(pokemon.nombre.capitalize())
            self.list_widget.addItem(item)
        asyncio.run(self.cargar_iconos_pokemon())  # Cargar íconos de los Pokémon

    def agregar_al_equipo(self):
        # Verificar si el equipo ya tiene 6 Pokémon
        if len(self.pokemon_equipo.pokemon_list) >= 6:
            self.selected_pokemon_label.setText("El equipo ya está completo.")
            self.add_button.setEnabled(False)  # Deshabilitar el botón
            return
        
        # Obtener el Pokémon seleccionado
        selected_item = self.list_widget.currentItem()
        if selected_item:
            pokemon_name = selected_item.text().lower()
            # Buscar el Pokémon en la lista
            found_pokemon = list(filter(lambda p: p.nombre.lower() == pokemon_name, self.pokedex.pokemones))
            if found_pokemon:
                selected_pokemon = found_pokemon[0]
                # Agregarlo al equipo
                self.pokemon_equipo.agregar_pokemon(selected_pokemon)
                print(f"Pokémon {selected_pokemon.nombre} agregado al equipo.")
                self.selected_pokemon_label.setText(f"{selected_pokemon.nombre} ha sido agregado al equipo.")
                if len(self.pokemon_equipo.pokemon_list) == 6:
                    self.selected_pokemon_label.setText("El equipo está completo.")
                    self.add_button.setEnabled(False)  # Deshabilitar el botón cuando el equipo esté completo
            else:
                self.selected_pokemon_label.setText("Pokémon no encontrado.")
        else:
            self.selected_pokemon_label.setText("Selecciona un Pokémon para agregar al equipo.")
            
    def guardar_equipo(self):
        """Guarda el equipo con los Pokémon seleccionados."""
        equipo_nombre = self.nombre_equipo_input.text()
        if equipo_nombre:
            self.pokemon_equipo.nombre = equipo_nombre  # Cambiar el nombre del equipo
            # Solo guardar los Pokémon que están en el equipo
            if len(self.pokemon_equipo.pokemon_list) == 0:
                self.selected_pokemon_label.setText("No has agregado Pokémon al equipo.")
                return
            # Verificar y eliminar caracteres inválidos en el nombre del archivo
            equipo_nombre = "".join([c for c in equipo_nombre if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()
            # Guardar el equipo en un archivo
            if not os.path.exists("equipos"):
                try:
                    os.makedirs("equipos")  # Crear el directorio si no existe
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo crear el directorio 'equipos'. Error: {str(e)}")
                    return
                    
            with open(f"equipos/equipo_{equipo_nombre}.txt", "w") as f:  # Guardar en el directorio equipos/
                for pokemon in self.pokemon_equipo.pokemon_list:
                    f.write(f"{pokemon.nombre}\n")
            self.selected_pokemon_label.setText(f"Equipo '{equipo_nombre}' guardado correctamente.")
            self.limpiar_equipo()  # Limpiar el equipo para crear uno nuevo

            # **Recargar los equipos guardados directamente después de guardar el equipo**
            ver_equipos_widget = self.stacked_widget.widget(3)  # Obtener la vista de equipos
            if isinstance(ver_equipos_widget, AplicacionVerEquipos):
                ver_equipos_widget.cargar_equipos_guardados()  # Recargar la lista de equipos

    def limpiar_equipo(self):
        """Limpiar el equipo y la interfaz para permitir la creación de un nuevo equipo."""
        self.pokemon_equipo = Equipo("Equipo de Prueba")  # Reiniciar el equipo
        self.nombre_equipo_input.clear()  # Limpiar el nombre del equipo
        self.selected_pokemon_label.setText("Selecciona un Pokémon para agregar al nuevo equipo.")
        self.add_button.setEnabled(True)  # Reactivar el botón de agregar
        self.pokemon_equipo.pokemon_list.clear()  # Limpiar la lista de Pokémon del equipo
        self.list_widget.clearSelection()  # Limpiar la selección en el QListWidget

    def volver_al_menu_principal(self):
        """Método para volver al menú principal."""
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))  # Cambiar a la primera página (Menú Principal)
