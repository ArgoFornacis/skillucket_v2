from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect

"""
These test cases ensure that the contact form view behaves correctly in different scenarios
and that the redirection view redirects to the expected URL.

Test Case Classes:
    - ContactFormViewTest: Test cases for the contact form view.
    - RedirectTestCase: Test case for URL redirection.

Methods in ContactFormViewTest:
    - test_contact_view_GET: Test the HTTP GET request to the contact form page.
    - test_contact_view_POST_valid_data: Test the HTTP POST request with valid form data.
    - test_contact_view_POST_invalid_data: Test the HTTP POST request with invalid form data.

Methods in RedirectTestCase:
    - test_redirect: Test the URL redirection to the home page.

These test cases use Django's TestCase class to set up and run tests for the views.
"""


class ContactFormViewTest(TestCase):
    def test_contact_view_GET(self):

        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")

    def test_contact_view_POST_valid_data(self):
        form_data = {
            "name": "Your Name",
            "email": "your_email@example.com",
            "title": "Test Title",
            "message": "Thank you for the visit",
        }

        response = self.client.post(reverse("contact"), data=form_data)

        self.assertEqual(response.status_code, 200)

    def test_contact_view_POST_invalid_data(self):

        form_data = {
            "name": "",
            "email": "invalid_email",
            "title": "Test Title",
            "message": "",
        }

        response = self.client.post(reverse("contact"), data=form_data)


class RedirectTestCase(TestCase):
    def test_redirect(self):

        url_to_test = reverse("redirect")
        response = self.client.get(url_to_test)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertRedirects(
            response, "http://localhost:8000/home/", fetch_redirect_response=False
        )
