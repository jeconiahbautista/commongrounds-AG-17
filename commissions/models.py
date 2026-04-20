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
    STATUS_OPEN = "0"
    STATUS_FULL = "1"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_FULL, "Full"),
    ]

    type = models.ForeignKey(
        CommissionType, on_delete=models.SET_NULL, null=True, related_name="commissions"
    )
    maker = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="commissions"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} from {}".format(self.title, self.type)

    def get_absolute_url(self):
        return reverse("commissions:request-detail", args=[str(self.pk)])

    class Meta:
        ordering = ["created_on"]
        verbose_name = "commission"
        verbose_name_plural = "commissions"


class Job(models.Model):
    STATUS_OPEN = "0"
    STATUS_FULL = "1"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_FULL, "Full"),
    ]

    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name="jobs"
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_OPEN
    )

    def __str__(self):
        return "{} for {}".format(self.role, self.commission)

    class Meta:
        ordering = ["status", "-manpower_required", "role"]
        verbose_name = "job"
        verbose_name_plural = "jobs"


class JobApplication(models.Model):
    STATUS_PENDING = "0"
    STATUS_ACCEPTED = "1"
    STATUS_REJECTED = "2"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    ]


    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    applied_on =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.applicant, self.job)

    class Meta:
        ordering = ["status", "-applied_on"]
        verbose_name = "application"
        verbose_name_plural = "applications"
        


