from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name="genres", null=True
    )
    author = models.CharField()
    publication_year = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bookclub:book-detail", args=[str(self.pk)])

    class Meta:
        ordering = [
            "-created_on",
        ]