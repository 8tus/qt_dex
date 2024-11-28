from .movimiento import Movimiento

class MovimientoAtaque(Movimiento):
    def __init__(self, nombre: str):
        super().__init__(nombre)
