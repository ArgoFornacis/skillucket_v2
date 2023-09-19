from django import forms


class AddSkillsForm(forms.Form):
    skill = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={"placeholder": "Enter Skill"})
    )
