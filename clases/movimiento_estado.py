from .movimiento import Movimiento

class MovimientoEstado(Movimiento):
    def __init__(self, nombre: str):
        super().__init__(nombre)