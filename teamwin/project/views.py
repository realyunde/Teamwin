import hashlib
from django.utils.http import urlquote
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render, redirect
from .models import Project, Member, SharedFile, Task, Sprint, Invitation, TaskComment
from ..user.models import User
from .. import auth


def is_member(user, project_id):
    members = Member.objects.filter(project_id=project_id)
    for item in members:
        if item.user == user:
            return True
    return False


def member_required(handler):
    def wrapper(request, project_id, *args, **kwargs):
        if not auth.is_authenticated(request):
            return redirect('index')
        else:
            user = auth.get_current_user(request)
            if not is_member(user, project_id):
                return redirect('user')
        return handler(request, project_id, *args, **kwargs)

    return wrapper


@member_required
def project_backlog(request, project_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'newTask':
            subject = request.POST.get('taskSubject')
            description = request.POST.get('taskDescription')
            assigned = request.POST.get('taskAssigned')
            task = Task(
                subject=subject,
                description=description,
                project_id=project_id,
            )
            if assigned == '':
                task.assigned = None
            else:
                task.assigned_id = assigned
            task.save()
        elif action == 'deleteTask':
            task_id = request.POST.get('taskId')
            task = Task.objects.get(id=task_id)
            task.delete()
    tasks = Task.objects.filter(project_id=project_id)
    members = Member.objects.filter(project_id=project_id).order_by('role')
    context['user'] = user
    context['tasks'] = tasks
    context['project'] = project
    context['members'] = members
    return render(request, 'project/backlog.html', context)


@member_required
def project_task(request, project_id, task_id):
    context = {}
    user = auth.get_current_user(request)
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deleteTask':
            task = Task.objects.get(id=task_id)
            task.delete()
            return redirect('project_backlog', project_id)
        elif action == 'updateTask':
            subject = request.POST.get('taskSubject')
            description = request.POST.get('taskDescription')
            assigned = request.POST.get('taskAssigned')
            task.subject = subject
            task.description = description
            if assigned == '':
                task.assigned_id = None
            else:
                try:
                    assigned = int(assigned)
                except Exception as e:
                    pass
                else:
                    task.assigned_id = assigned
            task.save()
        elif action == 'commentTask':
            comment = request.POST.get('comment')
            task_comment = TaskComment(
                comment=comment,
                author_id=user.id,
                task_id=task_id,
            )
            task_comment.save()
    members = Member.objects.filter(project_id=project_id).order_by('role')
    comments = TaskComment.objects.filter(task_id=task_id).order_by('created')
    context['user'] = user
    context['task'] = task
    context['project'] = project
    context['members'] = members
    context['comments'] = comments
    return render(request, 'project/task.html', context)


@member_required
def project_sprint(request, project_id, sprint_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    context['user'] = user
    context['project'] = project
    return render(request, 'project/sprint.html', context)


@member_required
def project_sprints(request, project_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'newSprint':
            name = request.POST.get('sprintName')
            goal = request.POST.get('sprintGoal')
            sprint = Sprint(
                name=name,
                goal=goal,
                project_id=project_id,
            )
            sprint.save()
    sprints = Sprint.objects.filter(project_id=project_id).order_by('-created')
    context['user'] = user
    context['project'] = project
    context['sprints'] = sprints
    return render(request, 'project/sprints.html', context)


@member_required
def project_share(request, project_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'uploadFile':
            f = request.FILES.get('uploadFile')
            path = hashlib.md5(f.name.encode('utf-8')).hexdigest()
            with open(settings.TEAMWIN_STORAGE_DIR + '/{}'.format(path), 'wb+') as fo:
                filesize = 0
                for chunk in f.chunks():
                    fo.write(chunk)
                    filesize += len(chunk)
            file = SharedFile(
                name=f.name,
                path=path,
                filesize=filesize,
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
            response = FileResponse(open(settings.TEAMWIN_STORAGE_DIR + '/{}'.format(file.path), 'rb'))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(urlquote(file.name))
            return response
    files = SharedFile.objects.filter(project_id=project_id)
    context['user'] = user
    context['project'] = project
    context['files'] = files
    return render(request, 'project/share.html', context)


@member_required
def project_settings(request, project_id):
    context = {}
    user = auth.get_current_user(request)
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
    context['user'] = user
    context['project'] = project
    return render(request, 'project/settings/index.html', context)


@member_required
def project_settings_team(request, project_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'inviteUser':
            user_name = request.POST.get('userName')
            invitee = User.get_by_name(user_name)
            if invitee is None:
                context['message'] = '该用户不存在！'
            else:
                if is_member(invitee, project_id):
                    context['message'] = '该用户已加入本项目！'
                else:
                    try:
                        invitation = Invitation(
                            inviter_id=user.id,
                            invitee_id=invitee.id,
                            project_id=project_id,
                        )
                        invitation.save()
                        context['message'] = '已邀请该用户！'
                    except Exception as e:
                        context['message'] = '已邀请该用户！' + e.__str__()
    members = Member.objects.filter(project_id=project_id).order_by('role')
    context['user'] = user
    context['project'] = project
    context['members'] = members
    return render(request, 'project/settings/team.html', context)


@member_required
def project_settings_role(request, project_id):
    context = {}
    user = auth.get_current_user(request)
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'updateRole':
            pass
    members = Member.objects.filter(project_id=project_id).order_by('role')
    context['user'] = user
    context['project'] = project
    context['members'] = members
    return render(request, 'project/settings/role.html', context)
