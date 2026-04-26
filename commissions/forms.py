from django import forms
from django.forms import inlineformset_factory

from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ["type", "title", "description", "people_required", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["role", "manpower_required", "status"]


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