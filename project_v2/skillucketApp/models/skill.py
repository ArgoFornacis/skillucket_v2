from django.db import models
from django.contrib.auth.models import User
from skillucketApp.constants import CATEGORY_CHOICES  # constants.py contains model constants for more modularity and flexibility


class Skill(models.Model):
    """Represents a skill that can be acquired or learned by a user.

    Skills are categorized into different categories such as 'Language', 'Music',
    'General Life Skills', etc. Each skill has a name, category, description, and
    can optionally be associated with a user.
    Example:
        skill = Skill(name="Python Programming", category="Programming",
                      description="Learn Python programming language")
    """
    # TODO choices for skill names from the json file
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description available")
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
