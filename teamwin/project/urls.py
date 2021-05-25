from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.index, name='project_index'),
]
