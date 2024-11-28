from abc import ABC

class Movimiento(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre