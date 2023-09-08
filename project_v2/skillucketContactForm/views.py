from django.shortcuts import render, redirect
from .models import ContactMessage
from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            # Redirect to a thank you page or homepage
            pass
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def contact_success(request):
    success = False  # Initialize the 'success' variable as False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]

            # Save the message to the database
            contact_message = ContactMessage(
                name=name, email=email, title=title, message=message
            )
            contact_message.save()

            success = True  # Set 'success' to True after a successful form submission

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "success": success})
