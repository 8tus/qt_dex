from asyncio import sleep
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from collect_pokemon_data import CollectPokemonData
from clases import Estadisticas, MovimientoEspecial, MovimientoEstado, MovimientoFisico, Pokedex, PokemonBasico, PokemonEvolucion, Tipo
import random
import time

class FileReaderThread(QThread):
    # Señales para comunicar el progreso o el resultado
    progress = pyqtSignal(str)
    pokedex_cargada = pyqtSignal(Pokedex)

    def run(self):
        time.sleep(8) #del 8tus
        try:    
            pokemon_list = CollectPokemonData.leer_pokemon_desde_archivo('pokemon_151_official.txt')
            print('archivo leido')
            pokedex = Pokedex()
            for pokemon_data in pokemon_list:
                print('crear estadisticas simuladas')
                estaditicas_simuladas = self.generate_base_stats()
                estadisticas = Estadisticas(
                    estaditicas_simuladas['hp'],
                    estaditicas_simuladas['ataque'],
                    estaditicas_simuladas['defensa'],
                    estaditicas_simuladas['ataque_especial'],
                    estaditicas_simuladas['defensa_especial'],
                    estaditicas_simuladas['velocidad'],
                )
                print('Identificar Tipos')
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
    def generate_base_stats(self):
        return {
            "hp": random.randint(40, 120),
            "ataque": random.randint(30, 130),
            "defensa": random.randint(30, 130),
            "ataque_especial": random.randint(30, 130),
            "defensa_especial": random.randint(30, 130),
            "velocidad": random.randint(30, 130),
        }