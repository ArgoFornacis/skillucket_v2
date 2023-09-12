from django.db import models

from skillucketApp.models.category import Category

from django.contrib.auth.models import User
from skillucketApp.constants import (
    CATEGORY_CHOICES,
)  # constants.py contains model constants for more modularity and flexibility



class Skill(models.Model):
    """Represents a skill that can be acquired or learned by a user.

    Skills are categorized into different categories such as 'Language', 'Music',
    'General Life Skills', etc. Each skill has a name, category and description.
    Example:
        skill = Skill(name="Python Programming", category="Programming",
                      description="Learn Python programming language")
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    # TODO choices for skill names from the json file
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available")

    def __str__(self):
        return self.name
