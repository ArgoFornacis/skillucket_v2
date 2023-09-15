from django.shortcuts import render, redirect
from .models import ContactMessage
from .forms import ContactForm
from django.urls import reverse
from django.test import TestCase


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]

            contact_message = ContactMessage(
                name=name, email=email, title=title, message=message
            )
            contact_message.save()

            return render(request, "home.html", {"form": form, "success": True})
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def redirect_view(request):

    destination_url = "http://localhost:8000/home/"
    return redirect(destination_url)


def contact_success(request):
    return render(request, "contact_success.html")
