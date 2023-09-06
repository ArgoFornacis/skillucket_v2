from django.db import models
from django.contrib.auth.models import User


class UserSkill(models.Model):
    """ bucket skill model represents the skills that a specific user wants to acquire """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)  # import Skill
    date_added = models.DateField(auto_now_add=True)
    target_date = models.DateField(null=True, blank=True)  # do we want this field?

    def __str__(self):
        return f"{self.user.username}'s bucket list: {self.skill.name}"
