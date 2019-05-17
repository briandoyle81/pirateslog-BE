from django.contrib import admin
from .models import Entry, Crewmate, Island

# Register your models here.
admin.site.register((Entry, Crewmate, Island))