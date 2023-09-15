from django import forms
from skillucketApp.models.profile import Profile
from skillucketApp.models.skill import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "image"]
