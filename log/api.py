from rest_framework import serializers, viewsets
from .models import Entry, UserLogEntry, Island, Profile, User

class UserSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="log:id-detail")

    class Meta:
        model = User
        fields = ("__all__")

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# class PermissionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model: 

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Entry
        fields = ('__all__')
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

class UserEntrySerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserLogEntry
        fields = ('__all__')

class UserEntryViewset(viewsets.ModelViewSet):
    serializer_class = UserEntrySerializer
    queryset = UserLogEntry.objects.all()

class MyEntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.none()

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Entry.objects.none()
        else:
            return Entry.objects.filter(user=user)

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