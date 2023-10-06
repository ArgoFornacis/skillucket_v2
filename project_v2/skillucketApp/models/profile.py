from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """profile model uses like an extension to user model, contains users information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        upload_to="profile_pics/", default="profile_pics/jellyfisz.jpg"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
