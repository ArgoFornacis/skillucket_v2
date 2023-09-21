from django.shortcuts import render, redirect
from .models import ContactMessage
from .forms import ContactForm
from django.urls import reverse
from django.test import TestCase


"""
Django views for handling contact form, redirection, and contact success.

View Functions:
    - contact: View for displaying and processing the contact form.
    - redirect_view: View for redirecting to a specific URL.
    - contact_success: View for displaying a success message after form submission.

Dependencies:
    - This module depends on Django's render, redirect functions, and models from the application.
    - It also utilizes the ContactForm form class defined in the forms module.

Functions:
    - contact(request): Handles the contact form. Displays the form for GET requests
      and processes form submissions for POST requests.
    - redirect_view(request): Redirects the user to a specified URL.
    - contact_success(request): Displays a success message after a successful form submission.

"""


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

            return render(
                request, "contact_success.html", {"form": form, "success": True}
            )
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def redirect_view(request):

    destination_url = "http://localhost:8000/home/"
    return redirect(destination_url)


def contact_success(request):
    return render(request, "contact_success.html")
