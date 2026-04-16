from django import forms
from .models import Book, BookReview, Borrow
from datetime import timedelta


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "genre",
            "author",
            "synopsis",
            "publication_year",
            "available_to_borrow",
        ]


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = [
            "title",
            "comment",
        ]


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = [
            "name",
            "date_borrowed",
        ]


        def save(self, commit=True):
            borrow = super().save(commit=False)
            if borrow.date_borrowed:
                borrow.date_to_return = borrow.date_borrowed + timedelta(days=14)
            if commit:
                borrow.save()
            return borrow





