from django.db import models
from django.urls import reverse


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
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.category)

    def get_absolute_url(self):
        return reverse("localevents:event-detail", args=[self.pk])

    class Meta:
        ordering = ["-created_on"]
