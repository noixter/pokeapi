from rest_framework.test import APITestCase
from rest_framework.exceptions import ParseError, NotFound
from ..serializers import PokemonSerializer
from ..models import Pokemon, BaseStats
from pokeapi.management.commands._baseclass import GetPokemonData
from django.urls import reverse
import random, string


class TestSetUp(APITestCase):

    def create_pokemon(self):
        base_url = 'https://pokeapi.co/api/v2/evolution-chain/'
        ids=1
        PokemonData = GetPokemonData(base_url, ids)
        PokemonData.get_initial_pokemon_data()
        PokemonData.get_complement_pokemon_data()
        PokemonData.save_pokemons()

    def setUp(self) -> None:
        self.create_pokemon()
        self.url_pokemons_list = reverse('pokemons:pokemon-list')
        self.pokemon_object = Pokemon.objects.get(id=1)
        super().setUp()

    def test_pokemon_name_does_not_exist(self):
        pokemon_name = 'test'
        res = self.client.get(reverse('pokemons:pokemon-detail', args=[pokemon_name]))
        self.assertEqual(res.status_code, 404)
        self.assertRaisesMessage(NotFound, 'Pokemon with name test not found')

    def test_url_name_cannot_be_with_numbers(self):
        pokemon_name = "".join(random.sample(string.ascii_lowercase+string.digits, 20))
        res = self.client.get(reverse('pokemons:pokemon-detail', args=[pokemon_name]))
        self.assertEqual(res.status_code, 400)
        self.assertRaisesMessage(ParseError, 'Pokemon name must no have numbers')

    def test_webservice_correspond_pokemon_object(self):
        pokemon = PokemonSerializer(self.pokemon_object)
        res = self.client.get(reverse('pokemons:pokemon-detail', args=[self.pokemon_object.name]))
        self.assertDictEqual(res.json(), pokemon.data)

    def test_only_6_basestats_per_pokemon(self):
        base_stats = BaseStats.objects.filter(pokemon=self.pokemon_object)
        self.assertEqual(len(base_stats), 6)

    def test_get_no_nulls_from_request(self):
        res = self.client.get(reverse('pokemons:pokemon-detail', args=[self.pokemon_object.name])).json()
        self.assertIn('pokemon', res)
        for value in res.get('pokemon').values():
            self.assertIsNotNone(value)
        self.assertIn('evolutions', res)
        for value in res.get('evolutions'):
            self.assertIsNotNone(value)