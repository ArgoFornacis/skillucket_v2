from django.test import TestCase
from django.urls import reverse
from .forms import ContactForm


class ContactFormViewTest(TestCase):
    def test_contact_view_POST_valid_data(self):
        form_data = {
            "name": "Your Name",
            "email": "your_email@example.com",
            "title": "Test Title",
            "message": "Thank you for your visit",
        }

        response = self.client.post(reverse("contact"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you for your visit", status_code=200)
