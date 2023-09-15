from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from skillucketApp.models.category import Category
from serializers.skill_management_serializers import CategorySerializer


class CategoryViewTests(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = APIClient()

        # Create a user (optional)
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some categories for testing
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_get_categories_authenticated(self):
        # Log in the user (if needed)
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the endpoint
        response = self.client.get(reverse('get-categories'))
        print(response)
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = CategorySerializer([self.category1, self.category2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_categories_unauthenticated(self):
        # Make a GET request to the endpoint without authentication
        response = self.client.get(reverse('get-categories'))

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories_empty(self):
        # Delete existing categories to test when there are none
        Category.objects.all().delete()

        # Log in the user (if needed)
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the endpoint
        response = self.client.get(reverse('get-categories'))

        # Check that the response data is an empty list
        self.assertEqual(response.data, ["hello"])

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
