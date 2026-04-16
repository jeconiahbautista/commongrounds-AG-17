from django.shortcuts import redirect, render
from .models import (
    Genre,
    Book,
    BookReview,
    Bookmark,
    Borrow,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import BookForm, BookReviewForm, BorrowForm


@login_required
def book_list(request):
    profile = request.user.profile
    contributed_books = Book.objects.filter(contributor=profile)
    bookmarked_books = Book.objects.filter(bookmark__profile=profile).distinct()
    reviewed_books = Book.objects.filter(bookreviews__user_reviewer=profile).distinct()
   
    excluded_books = Book.objects.filter(
        Q(contributor=profile)
        | Q(bookmark__profile=profile)
        | Q(bookreviews__user_reviewer=profile)
    ).distinct()


    excluded_books = Book.objects.exclude(
        id__in=excluded_books.values_list("id", flat=True)
    )


    books = Book.objects.exclude(
        id__in=excluded_books.values_list("id", flat=True)
    )


    ctx = {
        "contributed_books": contributed_books,
        "bookmarked_books": bookmarked_books,
        "reviewed_books": reviewed_books,
        "books": books,
    }
   
    return render(request, "book_list.html", ctx)

@login_required
def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    reviews = BookReview.objects.filter(book=book)
    bookmark_count = Bookmark.objects.filter(book=book).count()


    if request.method == "POST":
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book


            if request.user.is_authenticated:
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = "Anonymous"


            review.save()
            return redirect('book_detail', pk=pk)
    else:
        form = BookReviewForm()


   
    ctx = {
        "book": book,
        "reviews": reviews,
        "bookmark_count": bookmark_count,
    }
    return render(request, "book_detail.html", ctx)