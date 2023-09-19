from django.db import models
from django.contrib.auth.models import User
from skillucketApp.models.skill import Skill


class UserSkill(models.Model):
    """user skill model represents the skills that a specific user have"""

    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=255, choices=PROFICIENCY_CHOICES)

    def __str__(self):
        return f"{self.user.username} knows: {self.skill.name}"
