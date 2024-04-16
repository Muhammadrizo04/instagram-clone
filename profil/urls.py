from django.urls import path
from .views import *

urlpatterns = [
    path('profile/edit', EditProfile, name="editprofile"),
    path('settings/', setting, name="setting"),
]
