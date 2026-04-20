from django.shortcuts import redirect, render
from .models import (
    Project,
    ProjectRating,
    Favorite,
    ProjectReview,
    ProjectCategory,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProjectRatingForm, ProjectReviewForm, ProjectForm


@login_required
def diyprojects_list(request):
    profile = request.user.profile
    created_projects = Project.objects.filter(creator=profile)
    favorited_projects = Project.objects.filter(favorites__profile=profile).distinct()
    reviewed_projects = Project.objects.filter(reviews__reviewer=profile).distinct()

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


@login_required
def diyprojects_detail(request, pk):
    project = Project.objects.get(pk=pk)
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
        if not request.user.is_authenticated:
            return redirect("login")

        action = request.POST.get("action")

        if action == "rate":
            rate_form = ProjectRatingForm(request.POST)
            if rate_form.is_valid():
                ProjectRating.objects.create(
                    project=project,
                    profile=request.user.profile,
                    score=rate_form.cleaned_data["score"],
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
        elif action == "review":
            review_form = ProjectReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                ProjectReview.objects.create(
                    project=project,
                    reviewer=request.user.profile,
                    comment=review_form.cleaned_data["comment"],
                    image=review_form.cleaned_data["image"],
                )
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
def diyprojects_create(request):
    categories = ProjectCategory.objects.all()
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user.profile
            project.save()
            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
    else:
        project_form = ProjectForm()

    ctx = {
        "project_form": project_form,
        "categories": categories,
    }
    return render(request, "diy-projects_create_edit.html", ctx)


@login_required
def diyprojects_edit(request, pk):
    project = Project.objects.get(pk=pk)
    categories = ProjectCategory.objects.all()
    if request.method == "POST":
        project_form = ProjectForm(
            request.POST,
            instance=project,
        )
        if project_form.is_valid():
            project_form.save()
            return redirect("diyprojects:diyprojects_detail", pk=project.pk)
    else:
        project_form = ProjectForm(instance=project)

    ctx = {
        "project_form": project_form,
        "categories": categories,
        "project": project,
    }
    return render(request, "diy-projects_create_edit.html", ctx)
