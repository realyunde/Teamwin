from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.index, name='project_index'),
    path('<int:project_id>/settings', views.project_settings, name='project_settings'),
    path('<int:project_id>/share', views.project_share, name='project_share'),
    path('<int:project_id>/backlog', views.project_backlog, name='project_backlog'),
    path('<int:project_id>/sprint', views.project_sprint, name='project_sprint'),
]
