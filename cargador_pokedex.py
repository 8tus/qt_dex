from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import asyncio

from collect_pokemon_data import CollectPokemonData
from estadisticas import Estadisticas
from habilidad import Habilidad
from movimiento_especial import MovimientoEspecial
from movimiento_estado import MovimientoEstado
from movimiento_fisico import MovimientoFisico
from pokedex import Pokedex
from pokemon import Pokemon
from pokemon_basico import PokemonBasico
from pokemon_evolucion import PokemonEvolucion
from tipo import Tipo
import random


class CargadorPokedex(QThread):
    pokedex_cargada = pyqtSignal(Pokedex)

    def run(self):
        asyncio.run(self.cargar_pokedex())

    async def cargar_pokedex(self):
        try:    
            pokemon_list = await CollectPokemonData.leer_pokemon_desde_archivo('pokemon_151_official.txt')
            pokedex = Pokedex()
            for pokemon_data in pokemon_list:
                estaditicas_simuladas = self.generate_base_stats()
                estadisticas = Estadisticas(
                    estaditicas_simuladas['hp'],
                    estaditicas_simuladas['ataque'],
                    estaditicas_simuladas['defensa'],
                    estaditicas_simuladas['ataque_especial'],
                    estaditicas_simuladas['defensa_especial'],
                    estaditicas_simuladas['velocidad'],
                )
                tipos = [Tipo(tipo) for tipo in pokemon_data['tipos']]
                movimientos_estado = [MovimientoEstado(mov) for mov in pokemon_data['movimientos']['estado']]
                movimientos_fisicos = [MovimientoFisico(mov) for mov in pokemon_data['movimientos']['fisico']]
                movimientos_especiales = [MovimientoEspecial(mov) for mov in pokemon_data['movimientos']['especial']]
                if pokemon_data['es_basico'] == True:
                    pokemon = PokemonBasico(
                        pokemon_data['nombre'], pokemon_data['numero'],
                        tipos, pokemon_data['altura'],
                        pokemon_data['peso'], movimientos_estado,
                        movimientos_fisicos, movimientos_especiales, 
                        estadisticas
                    )
                    pokedex.pokemones.append(pokemon)
                else:
                    pokemon = PokemonEvolucion(
                        pokemon_data['nombre'], pokemon_data['numero'],
                        tipos, pokemon_data['altura'],
                        pokemon_data['peso'], movimientos_estado,
                        movimientos_fisicos, movimientos_especiales,
                        estadisticas
                    )
                    pokedex.pokemones.append(pokemon)
            self.pokedex_cargada.emit(pokedex)
        except:
            QMessageBox.warning(None, "Error", "No se pudo cargar la lista de Pokémon.")
    
    # Función para generar estadísticas base simuladas
    def generate_base_stats():
        return {
            "hp": random.randint(40, 120),
            "ataque": random.randint(30, 130),
            "defensa": random.randint(30, 130),
            "ataque_especial": random.randint(30, 130),
            "defensa_especial": random.randint(30, 130),
            "velocidad": random.randint(30, 130),
        }
