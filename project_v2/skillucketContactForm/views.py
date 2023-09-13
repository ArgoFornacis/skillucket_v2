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

            # Save the message to the database
            contact_message = ContactMessage(
                name=name, email=email, title=title, message=message
            )
            contact_message.save()

            # Redirect to the same contact page with a success flag
            return render(request, "contact.html", {"form": form, "success": True})
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


class ContactFormViewTest(TestCase):
    def test_contact_view_GET(self):

        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Contact Form", status_code=200
        )
