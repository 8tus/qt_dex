from .movimiento_ataque import MovimientoAtaque


class MovimientoEspecial(MovimientoAtaque):
    def __init__(self, nombre: str):
        super().__init__(nombre)

