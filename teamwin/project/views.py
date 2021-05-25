from django.shortcuts import render, redirect
from .models import Project, Developer


def index(request, project_id):
    context = {
        'project_id': project_id,
    }
    project = Project.objects.get(id=project_id)
    developer_list = Developer.objects.filter(project_id=project_id)
    context['project'] = project
    context['developer_list'] = developer_list
    return render(request, 'project/index.html', context)


def project_settings(request, project_id):
    context = {
        'project_id': project_id,
    }
    return render(request, 'project/settings.html', context)
