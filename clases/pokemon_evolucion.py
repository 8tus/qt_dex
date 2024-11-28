from .estadisticas import Estadisticas
from .pokemon import Pokemon

class PokemonEvolucion(Pokemon):
    def __init__(self, nombre: str, numero: int, tipos: list,
                 altura: float, peso: float, movimientos_estado: list,
                 movimientos_fisicos: list, movimientos_especiales: list,
                 estadisticas: Estadisticas):
        super().__init__(nombre, numero, tipos, altura, peso, 
                         movimientos_estado, movimientos_fisicos, 
                         movimientos_especiales, estadisticas)

    def es_basico(self) -> bool:
        return False
