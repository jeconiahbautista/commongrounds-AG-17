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
        verbose_name = "genre"
        verbose_name_plural = "genres"


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name="books", null=True
    )
    contributor = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name = "contributed_books", null=True
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField()
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
        verbose_name = "book"
        verbose_name_plural = "books"


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        Profile, on_delete = models.CASCADE, related_name="reviews", null=True, blank = True
    )
    anon_reviewer = models.TextField(blank=True, null=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="bookreviews"
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        reviewer = self.user_reviewer or self.anon_reviewer
        return f"{reviewer} - {self.title}"

    class Meta:
        verbose_name = "book review"
        verbose_name_plural = "book reviews"


class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete = models.CASCADE
    )
    book = models.ForeignKey(
        Book, on_delete = models.CASCADE
    )
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book}"

    class Meta:
        verbose_name = "bookmark"
        verbose_name_plural = "bookmarks"


class Borrow(models.Model):
    book = models.ForeignKey(
        Book, on_delete = models.CASCADE
    )
    borrower = models.ForeignKey(
        Profile, on_delete = models.CASCADE, null = True, blank = True
    )
    name = models.CharField(max_length=255, blank = True, null = True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        borrower_name = self.name if self.name else str(self.borrower)
        return f"{borrower_name} borrowed {self.book}"

    class Meta:
        verbose_name = "borrow"
        verbose_name_plural = "borrows"



