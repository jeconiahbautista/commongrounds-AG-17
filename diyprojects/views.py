from django.shortcuts import render
from .models import Project
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def diyprojects_list(request):
    profile = request.user.profile

    created_projects = Project.objects.filter(creator=profile)

    favorited_projects = Project.objects.filter(favorites__profile=profile)

    reviewed_projects = Project.objects.filter(reviews__reviewer=profile)

    excluded_projects = Project.objects.filter(
        Q(creator=profile)
        | Q(favorites__profile=profile)
        | Q(reviews__reviewer=profile)
    ).distinct()

    projects = Project.objects.exclude(
        id__in=excluded_projects.values_list("id", flat=True)
    )
    ctx = {
        "created_projects": created_projects,
        "favorited_projects": favorited_projects,
        "reviewed_projects": reviewed_projects,
        "projects": projects,
    }
    return render(request, "diy-projects_list.html", ctx)


def diyprojects_detail(request, pk):
    project = Project.objects.get(pk=pk)
    ctx = {"project": project}
    return render(request, "diy-projects_detail.html", ctx)
