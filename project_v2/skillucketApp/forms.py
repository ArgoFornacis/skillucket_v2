from django import forms
from .models.skill import Skill
from .models.profile import Profile


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "image"]
