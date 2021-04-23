from django.shortcuts import render, redirect
from .models import User
from .. import auth


def login(request):
    context = {
        'title': '登录',
    }
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if not all([username, password]):
            context['error'] = '账户不存在或密码错误！'
        else:
            if not User.auth_user(username, password):
                context['error'] = '账户不存在或密码错误！'
            else:
                user = User.get_by_name(username)
                auth.login(request, user.id)
                return redirect('user')
    return render(request, 'user/login.html', context)


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('index')


def signup(request):
    context = {
        'title': '注册',
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([username, email, password]):
            context['error'] = '注册失败'
        else:
            user = User.create_user(username, email, password)
            if user is None:
                context['error'] = '注册失败'
            else:
                auth.login(request, user.id)
                return redirect('user')
    return render(request, 'user/signup.html', context)


def index(request):
    if not auth.is_authenticated(request):
        return redirect('index')
    context = {
        'title': '首页',
    }
    account = auth.get_current_user(request)
    context['username'] = account.name
    return render(request, 'user/index.html', context)


def settings(request):
    if not auth.is_authenticated(request):
        return redirect('index')
    context = {
        'title': '设置',
    }
    account = auth.get_current_user(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'user/settings.html', context)


def projects(request):
    if not auth.is_authenticated(request):
        return redirect('index')
    context = {
        'title': '项目',
    }
    account = auth.get_current_user(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'user/projects.html', context)
