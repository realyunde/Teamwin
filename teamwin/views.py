from django.shortcuts import render, redirect
from . import auth
from .project.models import Project


def index(request):
    context = {}
    if auth.is_authenticated(request):
        return redirect('user')
    public_projects = Project.objects.filter(visibility=True)
    context['projects'] = public_projects
    return render(request, 'index.html', context)
