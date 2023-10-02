from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """profile model uses like an extension to user model, contains users information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        upload_to="profile_pics/", default="profile_pics/jellyfisz.jpg"
    )
    about = models.TextField(default="Tell the world about yourself!")

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        # Add functionality to save method which resizes the image before saving
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
