from django import forms
from .models import Book, BookReview, Borrow, BookRating
from datetime import timedelta


class BookContributeForm(forms.ModelForm):
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

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter book title',
                'class': 'form-input'
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Enter author name',
                'class': 'form-input'
            }),
            'synopsis': forms.Textarea(attrs={
                'placeholder': 'Enter book synopsis',
                'class': 'form-input',
                'rows': 8
            }),
            'publication_year': forms.NumberInput(attrs={
                'placeholder': 'Enter publication year',
                'class': 'form-input'
            }),
            'available_to_borrow': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.contributor = self.user.profile
        if commit:
            instance.save()
        return instance


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

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter review title',
                'class': 'form-input'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review here...',
                'class': 'form-input',
                'rows': 4
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user_reviewer = self.user.profile
        else:
            instance.anon_reviewer = "Anonymous"

        if commit:
            instance.save()
        return instance


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = [
            "name",
            "date_borrowed",
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name',
                'class': 'form-input'
            }),
            'date_borrowed': forms.DateInput(attrs={
                'placeholder': 'Enter date borrowed',
                'class': 'form-input'
            }),
        }

    def save(self, commit=True):
        borrow = super().save(commit=False)
        if borrow.date_borrowed:
            borrow.date_to_return = borrow.date_borrowed + timedelta(days=14)
        if commit:
            borrow.save()
        return borrow


class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ["score"]


class BookFormFactory:
    @classmethod
    def get_form(cls, context):
        if context == "review":
            return BookReviewForm
        elif context == "contribute":
            return BookContributeForm
        elif context == "update":
            return BookUpdateForm
        else:
            raise ValueError(f"Unknown form context: {context}")
