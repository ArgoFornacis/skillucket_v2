from django.db import models
from django.contrib.auth.models import User
from skillucketApp.models.skill import Skill


class BucketSkill(models.Model):
    """bucket skill model represents the skills that a specific user wants to acquire"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    target_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s bucket list: {self.skill.name}"
