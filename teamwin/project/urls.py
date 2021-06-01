from django.urls import path
from . import views

urlpatterns = [
    # settings
    path('<int:project_id>/settings', views.project_settings, name='project_settings'),
    path('<int:project_id>/settings/team', views.project_settings_team, name='project_settings_team'),
    path('<int:project_id>/settings/role', views.project_settings_role, name='project_settings_role'),
    # share
    path('<int:project_id>/share', views.project_share, name='project_share'),
    # backlog
    path('<int:project_id>/backlog', views.project_backlog, name='project_backlog'),
    path('<int:project_id>/task/<int:task_id>', views.project_task, name='project_task'),
    # sprint
    path('<int:project_id>/sprints', views.project_sprints, name='project_sprints'),
    path('<int:project_id>/sprint/<int:sprint_id>', views.project_sprint, name='project_sprint'),
]
