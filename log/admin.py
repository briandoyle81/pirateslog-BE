from django.contrib import admin
from .models import Entry, UserLogEntry, Island, Profile

# Register your models here.
admin.site.register((Entry, UserLogEntry, Island, Profile))