from django.shortcuts import render, redirect


def index(request, project_id):
    return render(request, 'project/index.html')
