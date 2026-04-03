from django.shortcuts import redirect, render
from .models import Project, ProjectRating, Favorite
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProjectRatingForm


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

    ratings = ProjectRating.objects.filter(project=project)

    if ratings.exists():
        total = sum([r.score for r in ratings])
        average_rating = total / ratings.count()
    else:
        average_rating = None

    favorite_count = Favorite.objects.filter(project=project).count()

    existing_rating = None
    is_favorited = False

    if request.user.is_authenticated:
        existing_rating = ProjectRating.objects.filter(
            project=project, profile=request.user.profile
        ).first()
        is_favorited = Favorite.objects.filter(
            project=project, profile=request.user.profile
        ).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        action = request.POST.get("action")

        if action == "rate":
            form = ProjectRatingForm(request.POST)
            if form.is_valid():
                ProjectRating.objects.create(
                    project=project,
                    profile=request.user.profile,
                    score=form.cleaned_data["score"],
                )
                return redirect("diyprojects:diyprojects_detail", pk=project.pk)
        elif action == "favorite":
            favorite = Favorite.objects.filter(
                project=project, profile=request.user.profile
            ).first()
            if favorite:
                favorite.delete()
            else:
                Favorite.objects.create(project=project, profile=request.user.profile)
            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
    else:
        form = ProjectRatingForm()

    ctx = {
        "project": project,
        "average_rating": average_rating,
        "existing_rating": existing_rating,
        "form": form,
        "is_favorited": is_favorited,
        "favorite_count": favorite_count,
    }

    return render(request, "diy-projects_detail.html", ctx)
