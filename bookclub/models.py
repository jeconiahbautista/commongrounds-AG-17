from django.db import models
from django.urls import reverse

from accounts.models import Profile

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
        Genre, on_delete=models.SET_NULL, related_name="books", null=True
    )
    contributor = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name = "books", null=True
    )
    author = models.CharField()
    synopsis = models.TextField(default="")
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("bookclub:book-detail", args=[str(self.pk)])


    class Meta:
        ordering = [
            "-publication_year",
        ]

class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        Profile, on_delete = models.CASCADE, related_name="reviews", null=True,
    )
    anon_reviewer = models.TextField(blank=True, null=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="bookreviews"
    )
    title = models.CharField()
    comment = models.TextField()


class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete = models.CASCADE
    )
    book = models.ForeignKey(
        Book, on_delete = models.CASCADE
    )
    date_bookmarked = models.DateField(auto_now_add=True)


class Borrow(models.Model):
    book = models.ForeignKey(
        Book, on_delete = models.CASCADE
    )
    borrower = models.ForeignKey(
        Profile, on_delete = models.CASCADE
    )
    name = models.CharField()
    date_borrowed = models.DateField()
    date_to_return = models.DateField()



