from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import asyncio
import aiohttp

from estadisticas import Estadisticas
from habilidad import Habilidad
from movimiento import Movimiento
from pokedex import Pokedex
from pokemon import Pokemon
from pokemon_info import PokemonInfo
from tipo import Tipo


class CargadorPokedex(QThread):
    pokedex_cargada = pyqtSignal(Pokedex)

    def run(self):
        asyncio.run(self.cargar_pokedex())

    async def cargar_pokedex(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=151"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pokedex = Pokedex()
                    pokedex.pokemones = [Pokemon(pokemon['name'], pokemon['url']) for pokemon in data['results']]
                    for pokemon in pokedex.pokemones:
                        async with session.get(pokemon.url) as poke_response:
                            if poke_response.status == 200:
                                pokemon_data = await poke_response.json()
                                # obtener lo necesario para crear PokemonInfo()
                                numero = pokemon_data['id']
                                altura = pokemon_data['height']
                                peso = pokemon_data['weight']
                                tipos = [Tipo(t['type']['name'] for t in pokemon_data['types'])]
                                habilidades = [Habilidad(a['ability']['name'] for a in pokemon_data['abilities'])]
                                movimientos = [Movimiento(m['move']['name'] for m in pokemon_data['moves'])]
                                sprite_url = pokemon_data['sprites']['front_default']
                                # Obtener lo necesario para crear Estadisticas()
                                ps = pokemon_data['stats'][0]['base_stat']
                                ataque = pokemon_data['stats'][1]['base_stat']
                                defensa = pokemon_data['stats'][2]['base_stat']
                                ataque_especial = pokemon_data['stats'][3]['base_stat']
                                defensa_especial = pokemon_data['stats'][4]['base_stat']
                                velocidad = pokemon_data['stats'][5]['base_stat']
                                estadisticas = Estadisticas(
                                    ps, ataque, defensa, ataque_especial,
                                    defensa_especial, velocidad
                                )
                                pokemon.info = PokemonInfo(
                                    numero, altura, peso, tipos,
                                    habilidades, movimientos,
                                    sprite_url, estadisticas
                                )
                    self.pokedex_cargada.emit(pokedex)
                else:
                    QMessageBox.warning(None, "Error", "No se pudo cargar la lista de Pokémon.")