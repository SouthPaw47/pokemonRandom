#!/usr/bin/env python3
import cgi
import cgitb
import json
import random


print("Content-Type: text/html\n")
class PokemonCollector:
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data()

    def load_pokemon_data(self):
        try:
            with open('pokemon_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_pokemon_data(self):
        with open('pokemon_data.json', 'w') as file:
            json.dump(self.pokemon_data, file, indent=4)

    def get_random_pokemon(self):
        response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1000')
        if response.status_code == 200:
            pokemon_list = response.json()['results']
            random_pokemon = random.choice(pokemon_list)
            return random_pokemon['name']
        else:
            print("Failed to retrieve Pokémon list.")
            return None

    def get_pokemon_details(self, pokemon_name):
        if pokemon_name in self.pokemon_data:
            print("Pokemon already in collection:")
            self.display_pokemon_details(self.pokemon_data[pokemon_name])
        else:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
            if response.status_code == 200:
                pokemon_data = response.json()
                self.pokemon_data[pokemon_name] = {
                    'name': pokemon_name,
                    'types': [t['type']['name'] for t in pokemon_data['types']],
                    'abilities': [a['ability']['name'] for a in pokemon_data['abilities']],
                    'base_stats': {s['stat']['name']: s['base_stat'] for s in pokemon_data['stats']}
                }
                self.save_pokemon_data()
                self.display_pokemon_details(self.pokemon_data[pokemon_name])
            else:
                print(f"Failed to retrieve details for {pokemon_name}.")

    def display_pokemon_details(self, pokemon_details):
        print(f"Name: {pokemon_details['name']}")
        print(f"Types: {', '.join(pokemon_details['types'])}")
        print(f"Abilities: {', '.join(pokemon_details['abilities'])}")
        print("Base Stats:")
        for stat, value in pokemon_details['base_stats'].items():
            print(f"  {stat}: {value}")

if __name__ == "__main__":
    collector = PokemonCollector()
    while True:
        draw_pokemon = input("Would you like to draw a Pokémon? (yes/no): ").lower()
        if draw_pokemon == 'yes':
            random_pokemon = collector.get_random_pokemon()
            if random_pokemon:
                collector.get_pokemon_details(random_pokemon)
        elif draw_pokemon == 'no':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
