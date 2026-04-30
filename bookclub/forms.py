from django import forms
from .models import Book, BookReview, Borrow
from datetime import timedelta


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "genre",
            "author",
            "contributor",
            "synopsis",
            "publication_year",
            "available_to_borrow",
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['contributor'].initial = user.profile
            self.fields['contributor'].widget = forms.HiddenInput()

class BookUpdateForm(forms.ModelForm):
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

class BookFormFactory:
    @classmethod
    def get_form(cls, context, user=None, **kwargs):
        if context == "review":
            return BookReviewForm(user=user, **kwargs)
        elif context == "contribute":
            return BookContributeForm(user=user, **kwargs)
        elif context == "update":
            return BookUpdateForm(**kwargs)
        else:
            raise ValueError(f"Unknown form context: {context}")



