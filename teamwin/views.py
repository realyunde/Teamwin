from django.shortcuts import render, redirect
from . import auth


def index(request):
    context = {}
    if auth.is_authenticated(request):
        return redirect('user')
    return render(request, 'index.html', context)
