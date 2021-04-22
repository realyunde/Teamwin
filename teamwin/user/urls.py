from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/login', views.login, name='login'),
    path('user/signup', views.register, name='register'),
    path('user', views.user_index, name='user'),
    path('user/logout', views.logout, name='logout'),
    path('user/settings', views.settings, name='user_settings'),
    path('user/projects', views.projects, name='user_projects'),
]
