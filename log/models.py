from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Entry(models.Model):
    SHIPS = (
            ('U', 'Unknown'),
            ('S', 'Sloop'),
            ('B', 'Brig'),
            ('G', 'Galleon'),
        )
    TREASURE = (
            ('U', 'Unknown'),
            ('N', 'None'),
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    TEARS = (
            ('U', 'Unknown'),
            ('N', 'None'),
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    myShip = models.CharField(max_length=10, default='U', choices=SHIPS)
    enemyShip = models.CharField(max_length=10, default='U', choices=SHIPS)
    loss = models.BooleanField(default=False)
    treasure = models.CharField(max_length=10, default='U', choices=TREASURE)
    tears = models.CharField(max_length=10, default='U', choices=TEARS)
    enemyCrewSize = models.IntegerField()
    crew = models.ManyToManyField('Profile', related_name='crewNames')
    island = models.ForeignKey('Island', on_delete=models.SET_DEFAULT, default=1, related_name='islandName')
    content = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    encounterTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    videoURL = models.URLField('URL', default='http://www.youtube.com')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL) # TODO: This shouldn't be nullable

    # #automatically save the current user in added_by
    # def save_model(self, request, obj, form, change):
    #     obj.added_by = request.user
    #     super().save_model(request, obj, form, change)

    # #automatically save the current user in added_by (possibly just from admin)
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         # Only set added_by during the first save.
    #         obj.added_by = request.user
    #     super().save_model(request, obj, form, change)

    def __str__(self):
        return self.title

class UserLogEntry(Entry):
    userCreatedBy = models.ForeignKey(User, on_delete=models.CASCADE), #TODO: Deleting user should preserve log

class Island(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='At Sea')
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%s' % (self.name)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gamertag = models.CharField(max_length=15)
    xuid = models.IntegerField(null=True)
    verified = models.BooleanField(default=False)
    verificationCode = models.CharField(max_length=6)
    friends = models.ManyToManyField('Profile', blank=True, related_name='myFriends')

    def __str__(self):
            return self.gamertag
