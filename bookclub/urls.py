from django.urls import path
from .views import *

app_name = "bookclub"

urlpatterns = [
    path('', index, name='index'),
    path('books/', book_list, name = 'book-list'),
    path('book/<int:pk>', book_detail, name='book-detail'),
    ]