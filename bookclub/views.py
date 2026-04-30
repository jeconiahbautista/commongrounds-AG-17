from django.shortcuts import redirect, render
from .models import (
    Book,
    BookReview,
    Bookmark,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import BookContributeForm, BookUpdateForm, BookReviewForm, BorrowForm, BookFormFactory


@login_required
def book_list(request):
    profile = request.user.profile
    contributed_books = Book.objects.filter(contributor=profile)
    bookmarked_books = Book.objects.filter(bookmark__profile=profile).distinct()
    reviewed_books = Book.objects.filter(bookreviews__user_reviewer=profile).distinct()
   
    excluded_ids = Book.objects.filter(
        Q(contributor=profile)
        | Q(bookmark__profile=profile)
        | Q(bookreviews__user_reviewer=profile)
    ).distinct()

    books = Book.objects.exclude(
        id__in=excluded_ids.values_list("id", flat=True)
    )


    ctx = {
        "contributed_books": contributed_books,
        "bookmarked_books": bookmarked_books,
        "reviewed_books": reviewed_books,
        "books": books,
    }
   
    return render(request, "book_list.html", ctx)


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    bookmark_count = Bookmark.objects.filter(book=book).count()
    reviews = BookReview.objects.filter(book=book)
    form = BookReviewForm()

    is_contributor = (
        request.user.is_authenticated and
        book.contributor == request.user.profile
    )

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            book=book,
            profile=request.user.profile
        ).exists()

    if request.method == "POST":

        if "bookmark" in request.POST and request.user.is_authenticated:
            bookmark, created = Bookmark.objects.get_or_create(
                profile=request.user.profile,
                book=book
            )
            if not created:
                bookmark.delete()
            return redirect("bookclub:book-detail", pk=pk)
        
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
        "reviews": reviews,
        "form": form,
        "is_contributor": is_contributor,
        "is_bookmarked": is_bookmarked,
    }
    return render(request, "book_detail.html", ctx)

@login_required
def book_create(request):
    # if request.user.profile.role != "Book Contributor":
    #     return redirect ("bookclub:book-list")
    
    form = BookFormFactory.get_form("contribute", user=request.user, data=request.POST)

    if request.method =="POST":
        form = BookContributeForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect('bookclub:book-list')
   
    ctx = {
       "form": form,
    }

    return render(request, "book_form.html", ctx)

@login_required
def book_update(request, pk):
    book = Book.objects.get(pk=pk)

    # if request.user.profile.role != "Book Contributor":
    #     return redirect ("bookclub:book-list")
    
    form = BookFormFactory.get_form("update", instance=book)


    if request.method =="POST":
        form = BookUpdateForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('bookclub:book-detail', pk=pk)
   
    ctx = {
        "form": form,
        "book": book,
    }

    return render(request, "book_form.html", ctx)


def book_borrow(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method =="POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            if request.user.is_authenticated:
                borrow.borrower = request.user.profile   
                borrow.name = request.user.profile.display_name
            borrow.save()
            return redirect('bookclub:book-list')
    else:
        form = BorrowForm()

    ctx = {
        "form": form,
        "book": book,
    }

    return render(request, "book_borrow.html", ctx)