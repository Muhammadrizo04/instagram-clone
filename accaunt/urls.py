from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import user_create_view, login_view
urlpatterns = [
    path('sigup/', user_create_view,name = 'sigup'),
    path('login/', login_view,name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),

]