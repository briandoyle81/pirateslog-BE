from django.shortcuts import render


# From https://github.com/coriolinus/oauth2-article/blob/master/views.py
from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from requests.exceptions import HTTPError
from social_django.utils import psa
from django.utils.crypto import get_random_string
from django.core import serializers as core_serializers
import json

import requests
xboxAPIToken = "f620e857d2edf0a17550eb47b0e029534e43f857"

from .models import Profile, Entry, Island
from .api import ProfileSerializer

# TODO: Do this and the method below belong here or in api.py?
# TODO: Is this secure?  Where does request.user.FOO come from?
@api_view(http_method_names=['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_me(request):
    dbEntry = Entry.objects.get(pk=request.data.get('id'))
    # doublecheck user is found and remove
    # TODO: Doublecheck user isn't creator of entry
    filter = dbEntry.crew.filter(gamertag = request.user.profile.gamertag)
    if filter != None:
        dbEntry.crew.remove(request.user.profile)
        dbEntry.save()
        return(Response("Removed from entry"))
    else:
        return(Response("User not in entry"))


# TODO: Do this and the method below belong here or in api.py? EDIT: Now sure it should be in api.py
# TODO: Is this secure?  Where does request.user.FOO come from?
@api_view(http_method_names=['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_log(request):
    # Handle missing island by using first entry as default
    if request.data.get('island') != {}:
        newIsland = Island.objects.get(pk=request.data.get('island').get('value')) #This is value to match react-select data
    else:
        newIsland = Island.objects.all()[0] # TODO: May be inefficent, but first island isn't id=0

    newEntry = Entry.objects.create(
        title='None',
        myShip=request.data.get('myShip'),
        enemyShip=request.data.get('enemyShip'),
        treasure=request.data.get('treasure'),
        tears=request.data.get('tears'),
        enemyCrewSize='0',
        island=newIsland,
        content='none',
        notes='none',
        encounterTime=request.data.get('dateTime'),
        videoURL='http://www.youtube.com',
        added_by=request.user.profile,
        map_location=newIsland.location,
        loss=request.data.get('loss')
    )

    # Add the reporter as crew
    newEntry.crew.add(request.user.profile)

    # Only add crew for validated users.
    dbProfile = Profile.objects.get(pk=request.user.profile.id)
    reportedCrew = request.data.get('crew')
    if dbProfile.verified and reportedCrew != None:
        for crewMember in reportedCrew:
            newEntry.crew.add(Profile.objects.get(pk=crewMember.get('value')))

    newEntry.save()
    
    #TODO: Serialize with EntrySerializer and send whole profile object
    return(Response("Entry Added"))

# TODO: Do this and the method below belong here or in api.py?
# TODO: Is this secure?
@api_view(http_method_names=['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def verify_gamertag(request):
    print("trying to verify gamertag")
    profileValue = request.user.profile
    dbProfile = Profile.objects.get(pk=profileValue.id)
    if dbProfile.verificationCode == request.data.get('code'):
        print("code matches")
        dbProfile.verified = True
        dbProfile.save()
        return(Response("true"))
    return(Response("false"))

# TODO: Do this and the method below belong here or in api.py?
# TODO: Is this secure?
# TODO: Gamertag validation
@api_view(http_method_names=['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_gamertag(request):
    print("updating gamertag to: ", request.data.get('name'))
    newName = request.data.get('name')
    profileValue = request.user.profile
    dbProfile = Profile.objects.get(pk=profileValue.id)
    dbProfile.gamertag = newName
    
    if newName != "":
        # TODO: Codes should expire
        if(dbProfile.verificationCode == ""):
            print("creating verification code for new user")
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            dbProfile.verificationCode = get_random_string(6, chars)

        #: Get the related xbox xuid
        # Temporarily disabling - token keeps expiring
        # HEADERS = {'X-AUTH': xboxAPIToken}
        # r = requests.get(url='https://xboxapi.com/v2/xuid/' + newName, headers=HEADERS)
        # xuid = r.json()
        # dbProfile.xuid = xuid
        
        # #: And send the validation code
        # HEADERS = {'X-AUTH': xboxAPIToken, 'Content-Type': 'application/json'}
        # DATA = {
        # "to": [
        #     xuid
        # ],
        # "message": "Your verification code is " + dbProfile.verificationCode
        # }

        # r = requests.post(url='https://xboxapi.com/v2/messages', data=None, json=DATA, headers=HEADERS)
        # print(r)
        # print("code is " + dbProfile.verificationCode)
    
    dbProfile.save()
    #TODO: Serialize with ProfileSerializer and send whole profile object
    return(Response(newName))


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    # Determine if this is an 


    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                profile = Profile.objects.get_or_create(user=user)
                print("got user " + user.profile.gamertag)
               
                # TODO: Should this use the rest_framework serializer?
                profile[0].verificationCode = "" # Hide verification code from client
                data = core_serializers.serialize('json', [profile[0],])
                struct = json.loads(data) # remove array wrapper before return
                finalProfile = json.dumps(struct[0].get('fields'))
                return Response({'token': token.key, 'profile': finalProfile})
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )