class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pokemon_list = []

    def agregar_pokemon(self, pokemon):
        """Agrega un Pokémon al equipo."""
        if len(self.pokemon_list) < 6:  # Un equipo no puede tener más de 6 Pokémon
            self.pokemon_list.append(pokemon)
        else:
            print("El equipo ya tiene el máximo de 6 Pokémon.")
    
    def eliminar_pokemon(self, pokemon):
        """Elimina un Pokémon del equipo."""
        if pokemon in self.pokemon_list:
            self.pokemon_list.remove(pokemon)
        else:
            print("Este Pokémon no está en el equipo.")
    
    def obtener_pokemon(self):
        """Obtiene la lista de Pokémon del equipo."""
        return self.pokemon_list
    
    def guardar_equipo(self):
        """Guarda el equipo en un archivo."""
        with open(f"equipo_{self.nombre}.txt", "w") as f:
            for pokemon in self.pokemon_list:
                f.write(f"{pokemon.nombre}\n")
    
    def cargar_equipo(self):
        """Carga un equipo desde un archivo."""
        try:
            with open(f"{self.nombre}_equipo.txt", "r") as f:
                self.pokemon_list = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"No se encontró un archivo para el equipo {self.nombre}.")
