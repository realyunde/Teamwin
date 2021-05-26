from django.shortcuts import render, redirect
from .models import Project, Developer
from .. import auth


def index(request, project_id):
    context = {
        'project_id': project_id,
    }
    user = auth.get_current_user(request)
    context['user'] = user
    project = Project.objects.get(id=project_id)
    developer_list = Developer.objects.filter(project_id=project_id)
    context['project'] = project
    context['developer_list'] = developer_list
    return render(request, 'project/index.html', context)


def project_settings(request, project_id):
    context = {
        'project_id': project_id,
    }
    user = auth.get_current_user(request)
    context['user'] = user
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'updateProject':
            name = request.POST.get('projectName')
            description = request.POST.get('projectDescription')
            project.name = name
            project.description = description
            project.save()
            context['message'] = '已修改！'
        elif action == 'deleteProject':
            project.delete()
            return redirect('user')
    context['project'] = project
    return render(request, 'project/settings.html', context)
