from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import list_route
# from rest_framework.decorators import action
from .models import Entry, UserLogEntry, Island, Profile, User
from django.shortcuts import get_object_or_404

import uuid

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
        queryset=Profile.objects.all() #TODO: This will not scale?
    )
    island = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Island.objects.all()
    )
    added_by = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='gamertag',
        queryset=Profile.objects.all() #TODO: This will not scale?
    )

    class Meta: 
        model = Entry
        fields = ('__all__')
       

class EntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all().order_by('-encounterTime')
    permission_classes = [IsAuthenticatedOrReadOnly]

# Viewset returning all entries that I am in as crew
class MyEntryViewset(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.none()

    def create(self, validated_data):
        breakpoint()
        pass

    # TODO: Investigate put/update vs. patch/partial_update
    def update(self, request, pk):
        entry = get_object_or_404(Entry.objects.all(), pk=uuid.UUID(pk))
        # Only update if it belongs to the user
        if request.user.profile == entry.added_by:
            if request.data.get('island')[0] != {}:
                newIsland = Island.objects.get(pk=request.data.get('island')[0].get('value')) #This is value to match react-select data
            else:
                newIsland = Island.objects.all()[0] # TODO: May be inefficent, but first island isn't id=0

            entry.myShip=request.data.get('myShip')
            entry.enemyShip=request.data.get('enemyShip')
            entry.treasure=request.data.get('treasure')
            entry.tears=request.data.get('tears')
            entry.island=newIsland
            # entry.encounterTime=request.data.get('dateTime')  For now do not update
            entry.loss=request.data.get('loss')

            entry.crew.set([])
            entry.crew.add(request.user.profile)

            # Only add crew for validated users.
            dbProfile = Profile.objects.get(pk=request.user.profile.id)
            reportedCrew = request.data.get('crew')
            if dbProfile.verified and reportedCrew != None:
                for crewMember in reportedCrew:
                    entry.crew.add(Profile.objects.get(pk=crewMember.get('value')))

            entry.save()

            return Response({"message": "Article with id '{}' has been updated.".format(pk)}, status=204)
        else:
            return Response({"message": "User not allowed to update this entry."}, status=401) # TODO: Verify status


    # TODO: This is not utilized
    def delete(self, request, pk):
        # Get object with this pk
        entry = get_object_or_404(Entry.objects.all(), pk=pk)
        breakpoint()
        # Only delete if it belongs to the user
        if request.user == entry.user:
            entry.delete()
            return Response({"message": "Article with id '{}' has been deleted.".format(pk)}, status=204)
        else:
            return Response({"message": "User not allowed to delete this entry."}, status=401) # TODO: Verify status
            
    def get_queryset(self):
        # Use token to find right user
        # breakpoint()
        profile = self.request.user.profile
        return Entry.objects.filter(crew__gamertag__contains=profile).order_by('-encounterTime')

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

# TODO:  This should filter for friends from the xboxAPI
class ProfileViewset(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.none()

    permission_classes = [IsAuthenticatedOrReadOnly]

    # Only return verified profiles
    def get_queryset(self):
        return Profile.objects.filter(verified=True)

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