import os
import hashlib
from django.utils.http import urlquote
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect
from .models import Project, Developer, SharedFile
from .. import auth


def user_required(handler):
    def wrapper(request, project_id):
        if not auth.is_authenticated(request):
            return redirect('index')
        return handler(request, project_id)

    return wrapper


@user_required
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


@user_required
def project_share(request, project_id):
    context = {
        'project_id': project_id,
    }
    user = auth.get_current_user(request)
    context['user'] = user
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'uploadFile':
            f = request.FILES.get('uploadFile')
            h = hashlib.md5(f.name.encode('utf-8')).hexdigest()
            with open(settings.TEAMWIN_STORAGE_DIR + '/{}'.format(h), 'wb+') as fo:
                for chunk in f.chunks():
                    fo.write(chunk)
            file = SharedFile(
                name=f.name,
                project_id=project_id,
            )
            file.save()
        elif action == 'deleteFile':
            file_id = request.POST.get('fileId')
            file = SharedFile.objects.get(id=file_id)
            file.delete()
        elif action == 'downloadFile':
            file_id = request.POST.get('fileId')
            file = SharedFile.objects.get(id=file_id)
            h = hashlib.md5(file.name.encode('utf-8')).hexdigest()
            response = FileResponse(open(settings.TEAMWIN_STORAGE_DIR + '/{}'.format(h), 'rb'))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(urlquote(file.name))
            return response
    files = SharedFile.objects.filter(project_id=project_id)
    for item in files:
        h = hashlib.md5(item.name.encode('utf-8')).hexdigest()
        item.filesize = os.stat(settings.TEAMWIN_STORAGE_DIR + '/{}'.format(h)).st_size
    context['files'] = files
    return render(request, 'project/share.html', context)


@user_required
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
