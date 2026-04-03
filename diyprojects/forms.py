from django import forms
from .models import ProjectRating, ProjectReview


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
