from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import list_route
# from rest_framework.decorators import action
from .models import Entry, UserLogEntry, Island, Profile, User

class UserSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="log:id-detail")

    class Meta:
        model = User
        fields = ("__all__")

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class EntrySerializer(serializers.ModelSerializer):
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='gamertag',
        queryset=Profile.objects.all() #TODO: This will not scale
    )
    island = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Island.objects.all()
    )

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
    permission_classes = [IsAuthenticatedOrReadOnly]

# Viewset returning all entries that I am in as crew
class MyEntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.none()

    def create(self, validated_data):
        breakpoint()
        pass

    def get_queryset(self):
        # Use token to find right user
        # breakpoint()
        profile = self.request.user.profile
        return Entry.objects.filter(crew__gamertag__contains=profile)

class IslandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Island
        fields = ('__all__')

class IslandViewset(viewsets.ModelViewSet):
    serializer_class = IslandSerializer
    queryset = Island.objects.none()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        return Response("Islands may only be added in admin")

    def get_queryset(self):
        return Island.objects.all()

class ProfileSerializer(serializers.ModelSerializer):
    # myFriends = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='gamertag'
    # )
    class Meta:
        model = Profile
        fields = ('id', 'gamertag', 'verified')

    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # gamertag = models.CharField(max_length=15)
    # friends = models.ManyToManyField('Profile', blank=True)

class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class MyProfileViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.none()

    # @list_route(methods=['post'])
    # def updateUserName(self, request):
    #     print(request)
    #     breakpoint()

    # def partial_update(self, request, pk=None):
    #     breakpoint()
    #     serializer = ProfileSerializer(request.user, data=request.data, partial=True)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)