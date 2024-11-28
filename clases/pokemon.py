from abc import ABC, abstractmethod

from .estadisticas import Estadisticas

class Pokemon(ABC):
    def __init__(self, nombre: str, numero: int, tipos: list,
                 altura: float, peso: float, movimientos_estado: list,
                 movimientos_fisicos: list, movimientos_especiales: list,
                 estadisticas: Estadisticas):
        self.nombre = nombre
        self.numero = numero
        self.tipos = tipos
        self.altura = altura,
        self.peso = peso
        self.movimientos_estado = movimientos_estado
        self.movimientos_fisicos = movimientos_fisicos
        self.movimientos_especiales = movimientos_especiales
        self.estadisticas = estadisticas

    @abstractmethod
    def es_basico(self) -> bool:
        pass
