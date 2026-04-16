from django.urls import path
from .views import book_list, book_detail
#book_create, book_update, book_borrow


app_name = "bookclub"


urlpatterns = [
    path("books/", book_list, name="book-list"),
    path("book/<int:pk>/", book_detail, name="book-detail"),
    # path("book/add/", book_create, name="book-create"),
    # path("book/<int:pk>/edit/", book_update, name="book-update"),
    # path("book/<int:pk>/borrow/", book_borrow, name="book-borrow"),
]
