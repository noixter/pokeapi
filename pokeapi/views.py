import string, re
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Pokemon
from .serializers import PokemonSerializer, PokemonObjectSerializer


class PokemonViewSet(ReadOnlyModelViewSet):
    """Pokemon viewset
    methods_available: GET
    Can only perform list all pokemon available and retrieve a pokemon info with respective evolutions
    """

    lookup_field = 'pk'
    serializer_class = PokemonSerializer

    def get_queryset(self):
        """Query set based on action"""
        if self.action == 'list':
            return Pokemon.objects.all().values('name')
        elif self.action == 'retrieve':
            return Pokemon.objects.filter(name=self.kwargs['pk']).first()

    def get_serializer_class(self):
        """Serializer based on action"""

        if self.action == 'list':
            return PokemonObjectSerializer

    def get_serializer_context(self):
        """Extra context to serializers"""

        context = super(PokemonViewSet, self).get_serializer_context()
        context.update({
            'method': self.action
        })
        return context

    def get_object(self):
        return self.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve info of specific pokemon with its evolutions"""

        if re.search(r'[\d]', self.kwargs.get('pk')):
            raise ParseError(detail='Pokemon name must no have numbers', code=400)
        pokemon = self.get_object()
        if not pokemon:
            raise NotFound(detail=f'Pokemon with name {self.kwargs["pk"]} not found')
        response = self.serializer_class(pokemon)
        return Response(response.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)





