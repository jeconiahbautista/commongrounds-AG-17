from django.db import models
from django.urls import reverse
from django.db.models import Sum

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
    creator = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name="projects", null=True
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
            "-created_on",
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
        max_length=255,
        choices=[("Backlog", "Backlog"), ("To-Do", "To-Do"), ("Done", "Done")],
        default="Backlog",
    )

    def __str__(self):
        return "{} ({})".format(self.project, self.status)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"


class ProjectReview(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    reviewer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="project_reviews"
    )
    comment = models.TextField()
    image = models.ImageField(upload_to="diyprojects_images/", blank=True, null=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    def __str__(self):
        return "Review by {}".format(self.reviewer)

    def score(self):
        return self.votes.aggregate(total=Sum("value"))["total"] or 0

    class Meta:
        verbose_name = "Project Review"
        verbose_name_plural = "Project Reviews"


class ProjectRating(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="ratings", null=True
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="project_ratings"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        stars = ""
        for i in range(self.score):
            stars += "★"
        return stars

    class Meta:
        verbose_name = "Project Rating"
        verbose_name_plural = "Project Ratings"
        unique_together = ["project", "profile"]


class ReviewVote(models.Model):
    review = models.ForeignKey(
        ProjectReview,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    value = models.IntegerField(choices=[(1, "Upvote"), (-1, "Downvote")])

    class Meta:
        unique_together = ["review", "user"]
