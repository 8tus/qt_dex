class CollectPokemonData:
    @staticmethod
    def leer_pokemon_desde_archivo(ruta_archivo):
        pokemon_list = []
        with open(ruta_archivo, "r", encoding='utf-8') as archivo:
            print('Archivo abierto')
            pokemon_actual = {}
            for linea in archivo:
                print('Leyendo ...')
                linea = linea.strip()
                if linea.startswith("Nombre:"):
                    if pokemon_actual:  # Si ya hay un Pokémon, agregarlo a la lista
                        pokemon_list.append(pokemon_actual)
                        pokemon_actual = {}
                    pokemon_actual["nombre"] = linea.split(": ")[1]
                elif linea.startswith("Número:"):
                    pokemon_actual["numero"] = int(linea.split(": ")[1])
                elif linea.startswith("Tipos:"):
                    pokemon_actual["tipos"] = linea.split(": ")[1].split(", ")
                elif linea.startswith("Básico:"):
                    pokemon_actual["es_basico"] = linea.split(": ")[1] == "Sí"
                elif linea.startswith("Altura:"):
                    pokemon_actual["altura"] = float(linea.split(": ")[1].replace(" m", ""))
                elif linea.startswith("Peso:"):
                    pokemon_actual["peso"] = float(linea.split(": ")[1].replace(" kg", ""))
                elif linea.startswith("- Estado:"):
                    pokemon_actual.setdefault("movimientos", {})["estado"] = linea.split(": ")[1].split(", ")
                elif linea.startswith("- Físico:"):
                    pokemon_actual["movimientos"]["fisico"] = linea.split(": ")[1].split(", ")
                elif linea.startswith("- Especial:"):
                    pokemon_actual["movimientos"]["especial"] = linea.split(": ")[1].split(", ")
                elif linea.startswith("-" * 40):  # Separador entre Pokémon
                    if pokemon_actual:
                        pokemon_list.append(pokemon_actual)
                        pokemon_actual = {}
            if pokemon_actual:  # Agregar el último Pokémon si existe
                pokemon_list.append(pokemon_actual)
        print('Retornar info leida desde archivo')
        return pokemon_list


# Ruta del archivo generado
# ruta_archivo = "pokemon_151_simulated.txt"

# # Leer el archivo y obtener la lista de Pokémon
# pokemones = leer_pokemon_desde_archivo(ruta_archivo)

# # Mostrar información de los primeros 5 Pokémon
# for pokemon in pokemones[:5]:
#     print(f"Nombre: {pokemon['nombre']}")
#     print(f"Número: {pokemon['numero']}")
#     print(f"Tipos: {', '.join(pokemon['tipos'])}")
#     print(f"Básico: {'Sí' if pokemon['es_basico'] else 'No'}")
#     print(f"Altura: {pokemon['altura']} m")
#     print(f"Peso: {pokemon['peso']} kg")
#     print(f"Movimientos:")
#     print(f"  - Estado: {', '.join(pokemon['movimientos']['estado'])}")
#     print(f"  - Físico: {', '.join(pokemon['movimientos']['fisico'])}")
#     print(f"  - Especial: {', '.join(pokemon['movimientos']['especial'])}")
#     print("-" * 40)
