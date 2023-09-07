from django.db import models
from skillucketApp.constants import CATEGORY_CHOICES


class Category(models.Model):
    name = models.CharField(max_length=100)  # choices=CATEGORY_CHOICES
    description = models.TextField(default="No description available")

    def __str__(self):
        return self.name
