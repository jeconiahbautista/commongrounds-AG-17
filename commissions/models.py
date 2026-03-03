from django.db import models
from django.urls import reverse


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Commission(models.Model):
    type = models.ForeignKey(
        CommissionType, on_delete=models.CASCADE, related_name="commissions"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} from {}".format(self.title, self.type)

    def get_absolute_url(self):
        return reverse("commissions:request-detail", args=[str(self.pk)])

    class Meta:
        ordering = ["created_on"]
