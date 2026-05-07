from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "category",
            "organizer",
            "event_image",
            "description",
            "location",
            "start_time",
            "end_time",
            "event_capacity",
            "status",
        ]

        widgets = {
            
            "title": forms.TextInput(attrs={
                "placeholder": "Enter event title..."
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe the event..."
            }),
            "start_time": forms.TextInput(attrs={
                "placeholder": "Add start time..."
            }),
            "end_time": forms.TextInput(attrs={
                "placeholder": "Add end time..."
            }),
            "location": forms.TextInput(attrs={
                "placeholder": "Enter location..."
            }),
            "event_capacity": forms.TextInput(attrs={
                "placeholder": "Add event time..."
            }),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["organizer"].initial = [user.profile]
            self.fields["organizer"].disabled = True
