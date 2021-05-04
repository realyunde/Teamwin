from django.shortcuts import render, redirect
from .models import User
from .. import auth


def user_required(handler):
    def wrapper(request):
        if not auth.is_authenticated(request):
            return redirect('index')
        return handler(request)

    return wrapper


def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if not all([username, password]):
            context['error'] = '账户不存在或密码错误'
        else:
            if not User.auth_user(username, password):
                context['error'] = '账户不存在或密码错误'
            else:
                user = User.get_by_name(username)
                auth.login(request, user.id)
                return redirect('user')
    return render(request, 'user/login.html', context)


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
def index(request):
    context = {}
    account = auth.get_current_user(request)
    context['username'] = account.name
    return render(request, 'user/index.html', context)


@user_required
def settings(request):
    context = {}
    account = auth.get_current_user(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'user/settings.html', context)


@user_required
def projects(request):
    context = {}
    account = auth.get_current_user(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'user/projects.html', context)
