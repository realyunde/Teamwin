from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user'),
    path('signup', views.signup, name='user_signup'),
    path('logout', views.logout, name='user_logout'),
    path('settings', views.settings, name='user_settings'),
]
