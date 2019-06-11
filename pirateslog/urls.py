"""pirateslog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views
from log.api import UserViewset, EntryViewset, MyEntryViewset, IslandViewset, ProfileViewset, MyProfileViewset
from log.views import exchange_token, update_gamertag, create_log, verify_gamertag

router = routers.DefaultRouter()
router.register(r'users', UserViewset, 'user')
router.register(r'entries', EntryViewset, 'entry')
# router.register(r'user_entries', UserEntryViewset, 'user_entry')
router.register(r'my_entries', MyEntryViewset, 'my_entry')
router.register(r'islands', IslandViewset, 'island')
router.register(r'profiles', ProfileViewset, 'profile')
router.register(r'my_profile', MyProfileViewset, 'my_profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include(router.urls)),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
    path('social_serializer/', exchange_token),
    url('' + r'social/(?P<backend>[^/]+)/$', exchange_token),
    url('' + r'update_gamertag/', update_gamertag),
    url('' + r'create_log/', create_log),
    url('' + r'verify_gamertag/', verify_gamertag),
    url('', include('social_django.urls', namespace='social')),
]
