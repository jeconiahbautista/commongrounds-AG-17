from django.shortcuts import render
from .models import Project

def diyprojects_list(request):
    projects = Project.objects.all()
    ctx = {'projects': projects}
    return render(request, 'diy-projects_list.html', ctx)

def diyprojects_detail(request, pk):
    project = Project.objects.get(pk=pk)
    ctx = {
        'title': project.title,
        'category': project.category,
        'description': project.description,
        'materials': project.materials,
        'steps': project.steps,
        'created_on': project.created_on,
        'updated_on': project.updated_on,
    }
    return render(request, 'diy-projects_detail.html', ctx)