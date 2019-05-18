from rest_framework import serializers, viewsets
from .models import Entry, Island, Profile

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta: model = Entry
    fields = (
                'title',
                'ship',
                'enemyShip',
                'loss',
                'treature',
                'tears',
                'enemyCrewSize',
                'crew',
                'island',
                'content',
                'encounterTime',
                'created_at',
                'last_modified',
            )

class EntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()



    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # title = models.CharField(max_length=200)
    # ship = models.CharField(max_length=10, default='U', choices=SHIPS)
    # enemyShip = models.CharField(max_length=10, default='U', choices=SHIPS)
    # loss = models.BooleanField()
    # treasure = models.CharField(max_length=10, default='U', choices=TREASURE)
    # tears = models.CharField(max_length=10, default='U', choices=TEARS)
    # enemyCrewSize = models.IntegerField()
    # crew = models.ManyToManyField(User)
    # island = models.ForeignKey('Island', on_delete=models.SET_DEFAULT, default=0)
    # content = models.TextField(blank=True)
    # encounterTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # last_modified = models.DateTimeField(auto_now=True)

