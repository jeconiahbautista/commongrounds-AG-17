from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ("Market Seller", "Market Seller"),
        ("Event Organizer", "Event Organizer"),
        ("Customer", "Customer"),
        ("Book Contributor", "Book Contributor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Customer")

    def __str__(self):
        return self.display_name
