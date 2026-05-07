from django import forms
from .models import ProjectRating, ProjectReview, Project


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = [
            "score",
        ]
        widgets = {
            "score": forms.NumberInput(
                attrs={
                    "class": "rating-field",
                    "min": 1,
                    "max": 5,
                }
            )
        }


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = [
            "comment",
            "image",
        ]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "review-field",
                    "placeholder": "Share your experience with this project...",
                    "rows": 4,
                }
            ),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "materials",
            "steps",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-title-field",
                    "placeholder": "Enter project title",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-category-select",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-text-area",
                    "rows": 7,
                    "placeholder": "Describe your project",
                }
            ),
            "materials": forms.Textarea(
                attrs={
                    "class": "form-text-area",
                    "rows": 7,
                    "placeholder": "List down the materials needed",
                }
            ),
            "steps": forms.Textarea(
                attrs={
                    "class": "form-text-area",
                    "rows": 7,
                    "placeholder": "List the steps",
                }
            ),
        }
        exclude = ["Project Creator"]
