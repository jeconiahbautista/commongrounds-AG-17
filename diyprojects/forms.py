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
