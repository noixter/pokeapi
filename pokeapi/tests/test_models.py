from django.test import TestCase
from ..models import Pokemon, BaseStats


class ModelTest(TestCase):

    def setUp(self) -> None:
        self.pokemon_data = {
            'id': 1,
            'name': 'bulbasaur',
            'height': 7,
            'weight': 69,
            'evolution_order': 1,
            'evolution_remaining': 2,
            'id_group': 1
        }
        super().setUp()
        self.evolution_constants = {
            1: 'PreEvolution',
            2: 'Evolution',
            3: 'Evolution'
        }

    def test_create_a_pokemon(self):
        Pokemon.objects.create(**self.pokemon_data)
        self.assertEqual(Pokemon.objects.count(), 1)
        self.assertEqual(Pokemon.objects.first().name, self.pokemon_data.get('name'))

    def test_get_evolution_order_from_constants(self):
        pokemon = Pokemon.objects.create(**self.pokemon_data)
        self.assertEqual(pokemon.get_evolution_order, self.evolution_constants.get(pokemon.evolution_order))
