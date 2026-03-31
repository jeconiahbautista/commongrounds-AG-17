from django.db import models
from django.urls import reverse

from accounts.models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, related_name="projects", null=True
    )
    description = models.TextField(null=False, blank=False)
    materials = models.TextField(null=False, blank=False)
    steps = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("diyprojects:diyprojects_detail", args=[str(self.id)])

    class Meta:
        ordering = [
            "created_on",
        ]


class Favorite(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="favorites"
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="favorites"
    )
    date_favorited = models.DateField(auto_now_add=True)
    status = models.CharField(
        choices=[("backlog", "Backlog"), ("todo", "To-Do"), ("done", "Done")],
        default="backlog",
    )

    def __str__(self):
        return "{} ({})".format(self.project, self.status)


class ProjectReview(models.Model):
    reviewer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="project_reviews"
    )
    comment = models.TextField()
    image = models.ImageField(upload_to="review_images/", blank=True, null=True)

    def __str__(self):
        return "Review by {}".format(self.reviewer)


class ProjectRating(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="project_ratings"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
