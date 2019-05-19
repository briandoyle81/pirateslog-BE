from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class Entry(models.Model):
    SHIPS = (
            ('U', 'Unknown'),
            ('S', 'Sloop'),
            ('B', 'Brig'),
            ('G', 'Galleon'),
        )
    TREASURE = (
            ('U', 'Unknown'),
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    TEARS = (
            ('U', 'Unknown'),
            ('L', 'Low'),
            ('M', 'Medium'),
            ('H', 'High'),
            ('E', 'Extraordinary'),
        )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author"), #TODO: Deleting user should preserve log
    title = models.CharField(max_length=200)
    ship = models.CharField(max_length=10, default='U', choices=SHIPS)
    enemyShip = models.CharField(max_length=10, default='U', choices=SHIPS)
    loss = models.BooleanField(default=False)
    treasure = models.CharField(max_length=10, default='U', choices=TREASURE)
    tears = models.CharField(max_length=10, default='U', choices=TEARS)
    enemyCrewSize = models.IntegerField()
    crew = models.ManyToManyField(User)
    island = models.ForeignKey('Island', on_delete=models.SET_DEFAULT, default=1)
    content = models.TextField(blank=True)
    encounterTime = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Island(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='At Sea')
    def __str__(self):
        return self.name

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
