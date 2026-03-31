from django import forms
from .models import ProjectRating


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = [
            "score",
        ]
