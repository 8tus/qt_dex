from .movimiento_ataque import MovimientoAtaque

class MovimientoFisico(MovimientoAtaque):
    def __init__(self, nombre: str):
        super().__init__(nombre)