from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    title = forms.CharField(max_length=100, label="Title")
    message = forms.CharField(widget=forms.Textarea, label="Message")
