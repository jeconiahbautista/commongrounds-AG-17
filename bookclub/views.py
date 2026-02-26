from django.shortcuts import render
from django.http import HttpResponse
# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView

from .models import Book

def book_list(request):
    books = Book.objects.all()
    ctx = { 'books': books }
    return render(request, "book_list.html", ctx)

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    ctx = { 'book': book }
    return render(request, 'book_detail.html', ctx)

# class BookListView(ListView):
#     model = Book
#     template_name = 'book_list.html'

# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'