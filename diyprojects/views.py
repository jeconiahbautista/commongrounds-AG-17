from django.shortcuts import redirect, render
from .models import (
    ProjectRating,
    Favorite,
    ProjectReview,
    ProjectCategory,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import ProjectRatingForm, ProjectReviewForm, ProjectForm
from accounts.decorators import role_required
from .repositories import ProjectRepository


def diyprojects_list(request):
    repo = ProjectRepository()
    all_projects = repo.get_all()

    if request.user.is_authenticated:
        profile = request.user.profile

        created_projects = all_projects.filter(creator=profile).distinct()
        favorited_projects = all_projects.filter(favorites__profile=profile).distinct()
        reviewed_projects = all_projects.filter(reviews__reviewer=profile).distinct()

        excluded_projects = all_projects.filter(
            Q(creator=profile)
            | Q(favorites__profile=profile)
            | Q(reviews__reviewer=profile)
        ).distinct()

        projects = all_projects.exclude(
            id__in=excluded_projects.values_list("id", flat=True)
        )
    else:
        created_projects = []
        favorited_projects = []
        reviewed_projects = []
        projects = all_projects

    ctx = {
        "created_projects": created_projects,
        "favorited_projects": favorited_projects,
        "reviewed_projects": reviewed_projects,
        "projects": projects,
    }

    return render(request, "diy-projects_list.html", ctx)


def diyprojects_detail(request, pk):
    repo = ProjectRepository()

    project = repo.get_by_id(pk)
    ratings = ProjectRating.objects.filter(project=project)
    reviews = ProjectReview.objects.filter(project=project)

    favorite_count = Favorite.objects.filter(project=project).count()
    existing_rating = None
    is_favorited = False
    is_owner = False

    rate_form = ProjectRatingForm()
    review_form = ProjectReviewForm()

    if ratings.exists():
        total = sum([r.score for r in ratings])
        average_rating = total / ratings.count()
    else:
        average_rating = None

    if request.user.is_authenticated:
        is_owner = project.creator == request.user.profile
        existing_rating = ProjectRating.objects.filter(
            project=project, profile=request.user.profile
        ).first()
        is_favorited = Favorite.objects.filter(
            project=project, profile=request.user.profile
        ).exists()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "rate":
            rate_form = ProjectRatingForm(request.POST)
            if rate_form.is_valid():
                ProjectRating.objects.update_or_create(
                    project=project,
                    profile=request.user.profile,
                    defaults={"score": rate_form.cleaned_data["score"]},
                )
                messages.success(request, project.title, extra_tags="project_rated")
                return redirect("diyprojects:diyprojects_detail", pk=project.pk)
        elif action == "favorite":
            favorite = Favorite.objects.filter(
                project=project, profile=request.user.profile
            ).first()
            if favorite:
                favorite.delete()
                messages.success(
                    request, project.title, extra_tags="project_unfavorited"
                )
            else:
                Favorite.objects.create(project=project, profile=request.user.profile)
                messages.success(request, project.title, extra_tags="project_favorited")
            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
        elif action == "review":
            review_form = ProjectReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                ProjectReview.objects.create(
                    project=project,
                    reviewer=request.user.profile,
                    comment=review_form.cleaned_data["comment"],
                    image=review_form.cleaned_data["image"],
                )
                messages.success(request, project.title, extra_tags="project_reviewed")
                return redirect("diyprojects:diyprojects_detail", pk=project.pk)

    ctx = {
        "project": project,
        "average_rating": average_rating,
        "existing_rating": existing_rating,
        "rate_form": rate_form,
        "is_favorited": is_favorited,
        "favorite_count": favorite_count,
        "reviews": reviews,
        "review_form": review_form,
        "is_owner": is_owner,
    }

    return render(request, "diy-projects_detail.html", ctx)


@login_required
@role_required("Project Creator")
def diyprojects_create(request):
    if request.user.profile.role != "Project Creator":
        return redirect("diyprojects:diyprojects_list")

    categories = ProjectCategory.objects.all()

    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user.profile
            project.save()

            messages.success(request, project.title, extra_tags="project_created")

            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
    else:
        project_form = ProjectForm()

    ctx = {
        "project_form": project_form,
        "categories": categories,
    }
    return render(request, "diy-projects_create_edit.html", ctx)


@login_required
@role_required("Project Creator")
def diyprojects_edit(request, pk):
    repo = ProjectRepository()

    if request.user.profile.role != "Project Creator":
        return redirect("diyprojects:diyprojects_list")

    project = repo.get_by_id(pk)

    if project.creator != request.user.profile:
        return redirect("diyprojects:diyprojects_detail", pk=project.pk)

    categories = ProjectCategory.objects.all()
    if request.method == "POST":
        project_form = ProjectForm(
            request.POST,
            instance=project,
        )
        if project_form.is_valid():
            project_form.save()
            messages.success(request, project.title, extra_tags="project_edited")
            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
    else:
        project_form = ProjectForm(instance=project)

    ctx = {
        "project_form": project_form,
        "categories": categories,
        "project": project,
    }
    return render(request, "diy-projects_create_edit.html", ctx)
