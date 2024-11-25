from estadisticas import Estadisticas


class PokemonInfo:
    def __init__(self, numero, altura, peso, tipos, habilidades, movimientos, sprite_url, estadisticas):
        self.numero = numero
        self.altura = altura
        self.peso = peso
        self.tipos = tipos
        self.habilidades = habilidades
        self.movimientos = movimientos
        self.sprite_url = sprite_url
        self.estadisticas = estadisticas

    @staticmethod
    def empty():
        return PokemonInfo(
            -1,
            0,
            0,
            [],
            [],
            [],
            '',
            Estadisticas.empty(),
        )