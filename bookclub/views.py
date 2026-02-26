from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Book

def index(request):
    return HttpResponse('Hello! This is the Book Club App.')

def book_list(request):
    books = Book.objects.all()
    ctx = { 'books': books }
    return render(request, "bookclub/book_list.html", ctx)

def book_detail(request, id):
    book = Book.objects.all()
    ctx = { 'books', Book.objects.get(id =id)}
    return render(request, 'bookclub/book_detail.html', ctx)

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'