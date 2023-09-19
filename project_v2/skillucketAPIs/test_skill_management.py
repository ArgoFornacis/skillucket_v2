from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill
from skillucketApp.models.user_skill import UserSkill
from skillucketApp.models.bucket_skill import BucketSkill
from skillucketAPIs.serializers.skill_management_serializers import (
    CategorySerializer,
    SkillSerializer,
    UserSkillSerializer,
    BucketSkillSerializer,
)


class CategoryViewTests(APITestCase):
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
        response = self.client.get(reverse('api:get-categories'))

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = CategorySerializer([self.category1, self.category2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_categories_unauthenticated(self):
        # Make a GET request to the endpoint without authentication
        response = self.client.get(reverse('api:get-categories'))

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_categories_empty(self):
        # Delete existing categories to test when there are none
        Category.objects.all().delete()

        # Log in the user (if needed)
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the endpoint
        response = self.client.get(reverse('api:get-categories'))

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data is an empty list
        self.assertEqual(response.data, [])


class SkillByCategoryViewTests(APITestCase):
    def setUp(self):
        # Set up a test client
        self.client = APIClient()

        # Create a user (optional)
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create some skills within the category
        self.skill1 = Skill.objects.create(name='Skill 1', category=self.category)
        self.skill2 = Skill.objects.create(name='Skill 2', category=self.category)

    def test_get_skills_by_category_authenticated(self):
        # Log in the user (if needed)
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the endpoint
        url = reverse('api:get-skills-by-category', args=[self.category.id])
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = SkillSerializer([self.skill1, self.skill2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_skills_by_category_unauthenticated(self):
        # Make a GET request to the endpoint without authentication
        url = reverse('api:get-skills-by-category', args=[self.category.id])
        response = self.client.get(url)

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_skills_by_category_empty(self):
        # Delete existing skills to test when there are none
        Skill.objects.all().delete()

        # Log in the user (if needed)
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to the endpoint
        url = reverse('api:get-skills-by-category', args=[self.category.id])
        response = self.client.get(url)

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data is an empty list
        self.assertEqual(response.data, [])


class ManageUserSkillsTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some skills for testing
        self.skill1 = Skill.objects.create(name='Skill 1')
        self.skill2 = Skill.objects.create(name='Skill 2')

    def test_add_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to add (use one of the created skills)
        skill_id = self.skill1.id

        # Make a POST request to add the skill
        response = self.client.post(reverse('manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response data
        self.assertIn('id', response.data)  # Assuming the response includes an 'id' field
        user_skill_id = response.data['id']

        # Check if the user skill exists in the database
        user_skill_exists = UserSkill.objects.filter(id=user_skill_id).exists()
        self.assertTrue(user_skill_exists)

    def test_remove_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to remove (use one of the created skills)
        skill_id = self.skill1.id

        # Make a DELETE request to remove the skill
        response = self.client.delete(reverse('manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check the response data (you can assert that the skill was removed from the user's skills)

    def test_add_skill_unauthenticated(self):
        pass
        # Make a POST request without authentication
        # ...
        # Check the response status code (should be 401 Unauthorized)
        # Check the response data (verify the error message)

    def test_remove_skill_unauthenticated(self):
        pass
        # Make a DELETE request without authentication
        # ...
        # Check the response status code (should be 401 Unauthorized)
        # Check the response data (verify the error message)

    def test_add_skill_not_found(self):
        pass
        # Attempt to add a skill that doesn't exist
        # ...
        # Check the response status code (should be 404 Not Found)
        # Check the response data (verify the error message)

    def test_remove_skill_not_found(self):
        pass
        # Attempt to remove a skill that doesn't exist
        # ...
        # Check the response status code (should be 404 Not Found)
        # Check the response data (verify the error message)

    def test_add_existing_skill(self):
        pass
        # Add a skill to the user's skills
        # ...
        # Attempt to add the same skill again
        # ...
        # Check the response status code (should be 400 Bad Request)
        # Check the response data (verify the error message)
