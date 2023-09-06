from django.db import models
from django.contrib.auth.models import User


class UserSkill(models.Model):
    """ user skill model represents the skills that a specific user have """

    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # import Skill
    proficiency_level = models.CharField(choices=PROFICIENCY_CHOICES)

