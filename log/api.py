from rest_framework import serializers, viewsets
from .models import Entry, Island, Profile, User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Entry
        fields = "__all__"
        # fields = (
        #             'title',
        #             'user',
        #             'ship',
        #             'enemyShip',
        #             'loss',
        #             'treasure',
        #             'tears',
        #             'enemyCrewSize',
        #             # 'crew',
        #             #'island',
        #             'content',
        #             'encounterTime',
        #             'created_at',
        #             'last_modified',
        #         )

class EntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()

class IslandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Island
        fields = "__all__"

class IslandViewset(viewsets.ModelViewSet):
    serializer_class = IslandSerializer
    queryset = Island.objects.all()

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()