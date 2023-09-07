from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models.profile import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create user profile when User instance is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender, instance, **kwargs):
    """Automatically save user profile as an attribute of User"""
    instance.profile.save()
