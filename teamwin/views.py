from django.shortcuts import render, redirect
from . import auth
from .user.models import User


def index(request):
    context = {}
    if auth.is_authenticated(request):
        return redirect('user')
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
    return render(request, 'index.html', context)
