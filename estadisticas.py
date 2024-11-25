class Estadisticas():
    def __init__(self, ps, ataque, defensa, ataque_especial, defensa_especial, velocidad):
        self.ps = ps
        self.ataque = ataque
        self.defensa = defensa
        self.ataque_especial = ataque_especial
        self.defensa_especial = defensa_especial
        self.velocidad = velocidad
    
    @staticmethod
    def empty():
        return Estadisticas(0, 0, 0, 0, 0, 0)