from django.db import models


ORDER_EVOLUTIONS = {
    1: 'PreEvolution',
    2: 'Evolution',
    3: 'Evolution'
}


class Pokemon(models.Model):

    id = models.IntegerField(primary_key=True, null=False)
    id_group = models.IntegerField(blank=False)
    name = models.CharField(max_length=100, blank=False)
    weight = models.PositiveSmallIntegerField(blank=False)
    height = models.PositiveSmallIntegerField(blank=False)
    evolution_order = models.PositiveSmallIntegerField(blank=False)  # Auxiliar field for tree structures on DB
    evolution_remaining = models.PositiveSmallIntegerField(blank=False) # Auxiliar field for tree structures on DB

    def __str__(self):
        return f'[{self.id}], {self.name}'

    @property
    def get_evolution_order(self):
        return ORDER_EVOLUTIONS.get(self.evolution_order, '')

    @property
    def evolutions_quantity(self):
        return len(Pokemon.objects.filter(id_group=self.id_group))

    class Meta:
        ordering = ['evolution_order']


class BaseStats(models.Model):

    id = models.IntegerField(primary_key=True, null=False)
    base_stat = models.PositiveSmallIntegerField(blank=False)
    effort = models.IntegerField(blank=True)
    name = models.CharField(max_length=20, blank=False)
    url = models.URLField()
    pokemon = models.ForeignKey(Pokemon, related_name='base_stats', on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.id}]: {self.name} -> {self.base_stat}'
