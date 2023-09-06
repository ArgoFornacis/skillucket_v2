from django.db import models
from django.contrib.auth.models import User
from skillucketApp.constants import PROFICIENCY_CHOICES
from skillucketApp.models.skill import Skill


class UserSkill(models.Model):
    """ user skill model represents the skills that a specific user have """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(choices=PROFICIENCY_CHOICES)

    def __str__(self):
        return f"{self.user.username} knows: {self.skill.name}"
