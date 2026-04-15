from django.shortcuts import render

from .models import Book


def book_list(request):
    books = Book.objects.all()
    ctx = {"books": books}
    return render(request, "book_list.html", ctx)


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    ctx = {"book": book}
    return render(request, "book_detail.html", ctx)
