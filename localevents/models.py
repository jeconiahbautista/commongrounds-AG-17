from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MinValueValidator


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        null=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    organizer = models.ManyToManyField(
        Profile,
        null=True,
        related_name="organizers",
    )
    event_image = models.ImageField(upload_to="localevents_images/", null=False)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10,
        choices=[
            ("Available", "Available"),
            ("Full", "Full"),
            ("Done", "Done"),
            ("Cancelled", "Cancelled"),
        ],
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.category)

    def get_absolute_url(self):
        return reverse("localevents:event-detail", args=[self.pk])

    class Meta:
        ordering = ["-created_on"]


class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        null=True,
        on_delete=models.CASCADE,
        related_name="events",
    )
    user_registrant = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name="users",
    )
    new_registrant = models.CharField(max_length=255)
