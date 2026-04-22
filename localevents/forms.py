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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["organizer"].initial = [user.profile]
            self.fields["organizer"].disabled = True
