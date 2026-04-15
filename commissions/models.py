from django.db import models
from django.urls import reverse

from accounts.models import Profile


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "commission type"
        verbose_name_plural = "commission types"


class Commission(models.Model):
    type = models.ForeignKey(
        CommissionType, on_delete=models.CASCADE, related_name="commissions"
    )
    maker = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="commissions"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return "{} from {}".format(self.title, self.type)

    def get_absolute_url(self):
        return reverse("commissions:request-detail", args=[str(self.pk)])

    class Meta:
        ordering = ["created_on"]
        verbose_name = "commission"
        verbose_name_plural = "commissions"


class Job(models.Model):
    STATUS_OPEN = "OPEN"
    STATUS_FULL = "FULL"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_FULL, "Full"),
    ]

    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="jobs"
    )
    role = models.CharField(max_length=255)
    manpower = models.IntegerField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN
    )

    class Meta:
        ordering = ["-status", "-manpower_required", "role"]
        verbose_name = "job"
        verbose_name_plural = "jobs"
