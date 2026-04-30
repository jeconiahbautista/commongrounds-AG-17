from django import forms
from .models import ProjectRating, ProjectReview, Project


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = [
            "score",
        ]


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
                    "placeholder": "Share your experience with this project...",
                    "rows": 3,
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
        exclude = ["Project Creator"]
