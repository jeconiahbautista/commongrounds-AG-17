from django import forms
from django.forms import inlineformset_factory

from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["type", "title", "description", "people_required", "status"]
        widgets = {
            
            "title": forms.TextInput(attrs={
                "placeholder": "Enter commission title..."
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe the commission..."
            }),
            "people_required": forms.TextInput(attrs={
                "placeholder": "Enter people required..."
            }),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["role", "manpower_required", "status"]
        widgets = {
            
            "role": forms.TextInput(attrs={
                "placeholder": "Enter role..."
            }),
            "manpower_required": forms.TextInput(attrs={
                "placeholder": "Enter manpower required..."
            }),
        }




JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1,
    can_delete=True,
)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []