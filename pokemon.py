from pokemon_info import PokemonInfo


class Pokemon:
    def __init__(self, nombre, url):
        self.nombre = nombre
        self.url = url
        self.info = PokemonInfo.empty()
