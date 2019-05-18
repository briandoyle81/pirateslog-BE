from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class Entry(models.Model):
    SHIPS = (
            ('S', 'Sloop'),
            ('B', 'Brig'),
            ('G', 'Galleon'),
        )
    TREASURE = (
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    TEARS = (
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    ship = models.CharField(max_length=10, choices=SHIPS)
    treasure = models.CharField(max_length=10, choices=TREASURE)
    tears = models.CharField(max_length=10, choices=TEARS)
    enemyCrewSize = models.IntegerField()
    crew = models.ManyToManyField(User)
    island = models.ForeignKey('Island', on_delete=models.SET_DEFAULT, default=0)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
class Crewmate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)

class Island(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # friends = models.ManyToManyField(User, related_name='+')
