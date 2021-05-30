from django.core.management.base import BaseCommand, CommandError
from pokeapi.models import Pokemon
from ._baseclass import GetPokemonData


class Command(BaseCommand):

    help = 'Fetch pokemon data based on evolution chains'

    def add_arguments(self, parser):
        parser.add_argument('ids',
                            nargs='+',
                            type=int,
                            help='Id evolution chain, to fetch many write with a intermediate space eg. [1 2 3]')

    def handle(self, *args, **options):
        for ids in options['ids']:
            if ids < 0 or ids > 467:   # make ids be in allowed PokeApi range
                raise CommandError('ids must be a positive integer field between 1 and 467')
            if Pokemon.objects.filter(id_group=ids):
                raise CommandError(f'Evolution chain {ids} had already beed stored')
            base_url = 'https://pokeapi.co/api/v2/evolution-chain/'
            PokemonData = GetPokemonData(base_url, ids)
            PokemonData.get_initial_pokemon_data()
            PokemonData.get_complement_pokemon_data()
            PokemonData.save_pokemons()
            self.stdout.write(self.style.SUCCESS(f'Evolution chain [{ids}] --> Successfully fetch'))