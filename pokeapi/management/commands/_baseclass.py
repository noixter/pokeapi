from pokeapi.models import Pokemon, BaseStats
import requests

# Create your views here.


class GetPokemonData:
    """Service Class
    Provides an API to fetch and store pokemon data based on evolution chains
    docs: https://pokeapi.co/docs/v2#evolution-section
    params: Base_url  PokeAPI url evolution chain
    params: ids  Search Argument for base_url
    """

    def __init__(self, base_url, ids):
        self.base_url = base_url
        self.data = []
        self._chain = {}
        self.evolution_remaining = 0
        self.ids = ids

        _response = requests.get(self.base_url+str(self.ids))
        self._chain = _response.json().get('chain')
        self.id_group = _response.json().get('id')

    def _handle_evolution_chain(self, chain, evolution_remaining, data):
        """Recursive process to calculate chain depth"""

        self.evolution_remaining += 1
        self.data.append({
            'name': chain.get('species').get('name'),
            'evolution_order': self.evolution_remaining,
            'id_group': self.id_group
        })
        if len(chain.get('evolves_to')) == 0:   # Base Case
            return True
        return self._handle_evolution_chain(chain.get('evolves_to')[0], evolution_remaining, data)

    def get_initial_pokemon_data(self):
        """Get first info about pokemons contained in evolution chain"""

        self._handle_evolution_chain(self._chain, self.evolution_remaining, self.data)
        print(f'Number of evolutions: {self.evolution_remaining}')
        print(f'Resulting data = {self.data}')

    def get_complement_pokemon_data(self):
        """Get complement info about pokemons
        Webservice: 'https://pokeapi.co/api/v2/pokemon/'
        Search_Params: Pokemon Name
        """
        base_url = 'https://pokeapi.co/api/v2/pokemon/'
        for pokemon in self.data:
            response = requests.get(base_url+pokemon.get('name'))
            if response.status_code == 200:
                pokemon.update({
                    'id': response.json().get('id'),
                    'evolution_remaining': self.evolution_remaining - pokemon.get('evolution_order'),
                    'weight': response.json().get('weight'),
                    'height': response.json().get('height'),
                    'stats': response.json().get('stats')
                })

    def _save_stats(self, stats, pokemon_id):
        """Helper function"""

        stats_to_create = []
        pokemon = Pokemon.objects.get(id=pokemon_id)
        for stat in stats:
            stats_to_create.append(
                BaseStats(pokemon=Pokemon.objects.get(id=pokemon.id),
                          name=stat.get('stat').get('name'),
                          base_stat=stat.get('base_stat'),
                          effort=stat.get('effort'),
                          url=stat.get('stat').get('url'))
            )
        BaseStats.objects.bulk_create(stats_to_create)
        print(f'{len(stats_to_create)} BaseStats saved for Pokemon {pokemon.name}')

    def save_pokemons(self):
        """Store info contained on param data"""

        for pokemon in self.data:
            stats = pokemon.pop('stats')
            Pokemon.objects.create(**pokemon)
            self._save_stats(stats, pokemon.get('id'))
        print(f'Number of Pokemon saved: {len(self.data)}')