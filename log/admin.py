from django.contrib import admin
from .models import Entry, Island, Profile

# Register your models here.
admin.site.register((Entry, Island, Profile))