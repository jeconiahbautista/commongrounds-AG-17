from django.urls import path
from .views import book_list, book_detail

app_name = "bookclub"

urlpatterns = [
    path("bookclub/books/", book_list, name="book-list"),
    path("bookclub/book/<int:pk>", book_detail, name="book-detail"),
]
