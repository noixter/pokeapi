from rest_framework import serializers
from .models import Pokemon, BaseStats


class BaseStatsSerializer(serializers.ModelSerializer):
    """Base Stats Model Serializer"""

    class Meta:
        model = BaseStats
        exclude = ['id', 'pokemon']  # exclude unnecessary fields


class PokemonObjectSerializer(serializers.ModelSerializer):
    """Pokemon information serializer,
     changes based on actions passed through serializer context"""

    base_stats = BaseStatsSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = ['id', 'name', 'weight', 'height', 'base_stats']

    def __init__(self, *args, **kwargs):
        super(PokemonObjectSerializer, self).__init__(*args, **kwargs)
        try:
            if self.context['method'] == 'list':  # Change fields dynamically based on action
                self.fields.pop('id')
                self.fields.pop('name')
                self.fields.pop('weight')
                self.fields.pop('height')
                self.fields.pop('base_stats')
                self.fields['available_pokemons'] = serializers.SerializerMethodField()
        except KeyError:
            pass

    def get_available_pokemons(self, obj):
        return obj


class EvolutionSerializer(serializers.Serializer):
    """Helper serializer to Evolution types"""

    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_evolution_order


class PokemonSerializer(serializers.Serializer):
    """Principal Serializer,
    Retrieve all the associated info about a pokemon"""

    pokemon = serializers.SerializerMethodField()
    evolutions = serializers.SerializerMethodField()

    def get_pokemon(self, obj):
        return PokemonObjectSerializer(obj).data

    def get_evolutions(self, obj):
        evolutions = Pokemon.objects.filter(id_group=obj.id_group).exclude(evolution_order=obj.evolution_order)
        return EvolutionSerializer(evolutions, many=True).data