from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='profile_pics/')  # add default.jpg pic

    def __str__(self):
        return f"{self.user.username}'s profile"
