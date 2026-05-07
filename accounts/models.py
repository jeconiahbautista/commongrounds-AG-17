from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ("Market Seller", "Market Seller"),
        ("Event Organizer", "Event Organizer"),
        ("Customer", "Customer"),
        ("Commission Maker", "Commission Maker"),
        ("Project Creator", "Project Creator"),
        ("Book Contributor", "Book Contributor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Customer")

    def __str__(self):
        return self.display_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
