import hashlib
from django.shortcuts import render, redirect
from .models import Account

TW_USERID_KEY = '_tw_userid'


def make_password(password):
    if not isinstance(password, (bytes, str)):
        raise TypeError('Password must be a string or bytes.')
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest()


def _login(request, userid):
    request.session[TW_USERID_KEY] = userid


def auth_account(request):
    userid = request.session.get(TW_USERID_KEY)
    if userid is None:
        return False
    return Account.user_exists(userid)


def get_current_account(request):
    userid = request.session.get(TW_USERID_KEY)
    return Account.get_by_id(userid)


def index(request):
    context = {
        'title': '首页',
    }
    if auth_account(request):
        return redirect('user')
    return render(request, 'account/index.html', context)


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
            token = make_password(password)
            try:
                user = Account.objects.get(name=username)
            except:
                context['error'] = '账户不存在或密码错误！'
            else:
                if user.token != token:
                    context['error'] = '账户不存在或密码错误！'
                else:
                    _login(request, user.id)
                    return redirect('user')
    return render(request, 'account/login.html', context)


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('index')


def register(request):
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
            token = make_password(password)
            try:
                user = Account(
                    name=username,
                    email=email,
                    token=token
                )
                user.save()
            except:
                context['error'] = '注册失败'
            else:
                _login(request, user.id)
                return redirect('user')
    return render(request, 'account/signup.html', context)


def user_index(request):
    if not auth_account(request):
        return redirect('index')
    context = {
        'title': '首页',
    }
    account = get_current_account(request)
    context['username'] = account.name
    return render(request, 'account/user.html', context)


def settings(request):
    if not auth_account(request):
        return redirect('index')
    context = {
        'title': '设置',
    }
    account = get_current_account(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'account/settings.html', context)


def projects(request):
    if not auth_account(request):
        return redirect('index')
    context = {
        'title': '项目',
    }
    account = get_current_account(request)
    context['username'] = account.name
    context['user_email'] = account.email
    return render(request, 'account/projects.html', context)
