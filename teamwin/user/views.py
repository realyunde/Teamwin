from django.shortcuts import render, redirect
from .models import User
from ..project.models import Project
from .. import auth


def user_required(handler):
    def wrapper(request):
        if not auth.is_authenticated(request):
            return redirect('index')
        return handler(request)

    return wrapper


def logout(request):
    auth.logout(request)
    return redirect('index')


def signup(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([username, email, password]):
            context['error'] = '请正确填写信息'
        else:
            if User.name_exists(username):
                context['error'] = '该用户已存在'
            elif User.email_exists(email):
                context['error'] = '该邮箱已存在'
            else:
                try:
                    user = User.create_user(username, email, password)
                except Exception as e:
                    context['error'] = '注册失败' + e.__str__()
                else:
                    auth.login(request, user.id)
                    return redirect('user')
    return render(request, 'user/signup.html', context)


@user_required
def settings(request):
    context = {}
    user = auth.get_current_user(request)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'updateName':
            new_username = request.POST.get('newUsername')
            if User.name_exists(new_username):
                context['message'] = '该用户名已存在！'
            else:
                user.name = new_username
                user.save()
                context['message'] = '已修改！'
        elif action == 'updateEmail':
            new_email = request.POST.get('newEmail')
            if User.email_exists(new_email):
                context['message'] = '该邮箱已存在！'
            else:
                user.email = new_email
                user.save()
                context['message'] = '已修改！'
        elif action == 'updatePassword':
            password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            if User.auth_user(user.name, password):
                user.set_password(new_password)
                context['message'] = '已修改！'
            else:
                context['message'] = '原密码错误！'
    context['user'] = user
    return render(request, 'user/settings.html', context)


@user_required
def index(request):
    context = {}
    user = auth.get_current_user(request)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'new':
            name = request.POST.get('name')
            description = request.POST.get('description')
            try:
                Project.objects.create(
                    name=name,
                    owner=user,
                    description=description,
                )
            except Exception as e:
                context['message'] = '新建项目失败！' + e.__str__()
            else:
                context['message'] = '新建项目成功！'
    projects = Project.objects.filter(
        owner=user,
    )
    context['user'] = user
    context['projects'] = projects
    return render(request, 'user/index.html', context)
