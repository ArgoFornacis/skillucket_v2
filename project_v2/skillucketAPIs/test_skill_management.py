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

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create some skills within the category
        self.skill1 = Skill.objects.create(name='Skill 1', category=self.category)
        self.skill2 = Skill.objects.create(name='Skill 2', category=self.category)
        self.skill3 = Skill.objects.create(name='Skill 3', category=self.category)

        # Create test user skill
        self.userskill1 = UserSkill.objects.create(user=self.user, skill=self.skill1, proficiency_level="Expert")

    def test_add_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to add (use one of the created skills)
        skill_id = self.skill2.id

        # Make a POST request to add the skill
        response = self.client.post(reverse('api:manage-user-skills'), {'skill_id': skill_id}, format='json')

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
        response = self.client.delete(reverse('api:manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check the response data
        response_data = response.data  # Get the response data as a dictionary

        # Check if the "message" field in the response contains the expected message
        self.assertEqual(response_data.get('message', ''), "Skill removed from User Skills")

    def test_add_skill_unauthenticated(self):
        # Make a POST request without authentication
        response = self.client.post(reverse('api:manage-user-skills'), {'skill_id': self.skill2.id}, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_skill_unauthenticated(self):
        # Make a DELETE request without authentication
        response = self.client.delete(reverse('api:manage-user-skills'), {'skill_id': self.skill1.id}, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_skill_not_found(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Attempt to add a skill that doesn't exist (use an invalid skill_id)
        invalid_skill_id = 9999999999999

        # Make a POST request to add the skill
        response = self.client.post(reverse('api:manage-user-skills'), {'skill_id': invalid_skill_id}, format='json')

        # Check the response status code (should be 404 Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response data (verify the error message)
        response_data = response.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill not found")

    def test_remove_skill_not_found(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Attempt to remove a skill that doesn't exist (use a skill_id that doesn't exist)
        skill_id = 9999999999999

        # Make a DELETE request to remove the skill
        response = self.client.delete(reverse('api:manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 404 Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response data (verify the error message)
        response_data = response.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill not found in User Skills")

    def test_add_existing_skill(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to add (use one of the created skills)
        skill_id = self.skill3.id

        # Make a POST request to add the skill
        response1 = self.client.post(reverse('api:manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 201 Created)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Attempt to add the same skill again
        response2 = self.client.post(reverse('api:manage-user-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 400 Bad Request)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response data (verify the error message)
        response_data = response2.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill already exists in User Skills")


class ManageBucketSkillsTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create some skills within the category
        self.skill1 = Skill.objects.create(name='Skill 1', category=self.category)
        self.skill2 = Skill.objects.create(name='Skill 2', category=self.category)
        self.skill3 = Skill.objects.create(name='Skill 3', category=self.category)

        # Create test user skill
        self.bucketskill1 = BucketSkill.objects.create(user=self.user, skill=self.skill1)

    def test_add_bucket_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to add (use one of the created skills)
        skill_id = self.skill2.id

        # Make a POST request to add the skill to the bucket list
        response = self.client.post(reverse('api:manage-bucket-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response data
        self.assertIn('id', response.data)  # Assuming the response includes an 'id' field
        bucket_skill_id = response.data['id']

        # Check if the bucket skill exists in the database
        bucket_skill_exists = BucketSkill.objects.filter(id=bucket_skill_id).exists()
        self.assertTrue(bucket_skill_exists)

    def test_remove_bucket_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to remove (use one of the created skills)
        skill_id = self.skill1.id

        # Make a DELETE request to remove the skill from the bucket list
        response = self.client.delete(reverse('api:manage-bucket-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check the response data
        response_data = response.data  # Get the response data as a dictionary

        # Check if the "message" field in the response contains the expected message
        self.assertEqual(response_data.get('message', ''), "Skill removed from Bucket List")

    def test_add_bucket_skill_unauthenticated(self):
        # Make a POST request without authentication
        response = self.client.post(reverse('api:manage-bucket-skills'), {'skill_id': self.skill2.id}, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_bucket_skill_unauthenticated(self):
        # Make a DELETE request without authentication
        response = self.client.delete(reverse('api:manage-bucket-skills'), {'skill_id': self.skill1.id}, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_bucket_skill_not_found(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Attempt to add a skill that doesn't exist (use an invalid skill_id)
        invalid_skill_id = 9999999999999

        # Make a POST request to add the skill to the bucket list
        response = self.client.post(reverse('api:manage-bucket-skills'), {'skill_id': invalid_skill_id}, format='json')

        # Check the response status code (should be 404 Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response data (verify the error message)
        response_data = response.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill not found")

    def test_remove_bucket_skill_not_found(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Attempt to remove a skill that doesn't exist (use a skill_id that doesn't exist)
        skill_id = 9999999999999

        # Make a DELETE request to remove the skill from the bucket list
        response = self.client.delete(reverse('api:manage-bucket-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 404 Not Found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response data (verify the error message)
        response_data = response.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill not found")

    def test_add_existing_bucket_skill(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Skill ID to add (use one of the created skills)
        skill_id = self.skill3.id

        # Make a POST request to add the skill to the bucket list
        response1 = self.client.post(reverse('api:manage-bucket-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 201 Created)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Attempt to add the same skill again
        response2 = self.client.post(reverse('api:manage-bucket-skills'), {'skill_id': skill_id}, format='json')

        # Check the response status code (should be 400 Bad Request)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response data (verify the error message)
        response_data = response2.data  # Get the response data as a dictionary
        self.assertEqual(response_data.get('message', ''), "Skill already exists in Bucket List")


class GetUserSkillsTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create some skills within the category
        self.skill1 = Skill.objects.create(name='Skill 1', category=self.category)
        self.skill2 = Skill.objects.create(name='Skill 2', category=self.category)
        self.skill3 = Skill.objects.create(name='Skill 3', category=self.category)

        # Create user skills for the user
        self.userskill1 = UserSkill.objects.create(user=self.user, skill=self.skill1, proficiency_level="Expert")
        self.userskill2 = UserSkill.objects.create(user=self.user, skill=self.skill2, proficiency_level="Intermediate")

    def test_get_user_skills_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to get the user's skills
        response = self.client.get(reverse('api:get-user-skills'))

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = UserSkillSerializer([self.userskill1, self.userskill2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_user_skills_unauthenticated(self):
        # Make a GET request to get the user's skills without authentication
        response = self.client.get(reverse('api:get-user-skills'))

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetBucketSkillsTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create some skills within the category
        self.skill1 = Skill.objects.create(name='Skill 1', category=self.category)
        self.skill2 = Skill.objects.create(name='Skill 2', category=self.category)
        self.skill3 = Skill.objects.create(name='Skill 3', category=self.category)

        # Create bucket skills for the user
        self.bucketskill1 = BucketSkill.objects.create(user=self.user, skill=self.skill1)
        self.bucketskill2 = BucketSkill.objects.create(user=self.user, skill=self.skill2)

    def test_get_bucket_skills_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to get the user's bucket list skills
        response = self.client.get(reverse('api:get-bucket-skills'))

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = BucketSkillSerializer([self.bucketskill1, self.bucketskill2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_bucket_skills_unauthenticated(self):
        # Make a GET request to get the user's bucket list skills without authentication
        response = self.client.get(reverse('api:get-bucket-skills'))

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserSkillDetailTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create a skill within the category
        self.skill = Skill.objects.create(name='Test Skill', category=self.category)

        # Create a user skill for the user
        self.user_skill = UserSkill.objects.create(user=self.user, skill=self.skill, proficiency_level="Intermediate")

    def test_get_user_skill_detail_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Make a GET request to get the user skill detail
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.get(url)

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        expected_data = UserSkillSerializer(self.user_skill).data
        self.assertEqual(response.data, expected_data)

    def test_get_user_skill_detail_unauthenticated(self):
        # Make a GET request to get the user skill detail without authentication
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.get(url)

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Update the user skill data
        new_data = {
            'proficiency_level': 'Advanced'
        }
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.put(url, new_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        updated_user_skill = UserSkill.objects.get(id=self.user_skill.id)
        self.assertEqual(updated_user_skill.proficiency_level, 'Advanced')

    def test_update_user_skill_unauthenticated(self):
        # Update the user skill data without authentication
        new_data = {
            'proficiency_level': 'Advanced'
        }
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.put(url, new_data, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_user_skill_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Partially update the user skill data
        new_data = {
            'proficiency_level': 'Advanced'
        }
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.patch(url, new_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response data
        updated_user_skill = UserSkill.objects.get(id=self.user_skill.id)
        self.assertEqual(updated_user_skill.proficiency_level, 'Advanced')

    def test_partial_update_user_skill_unauthenticated(self):
        # Partially update the user skill data without authentication
        new_data = {
            'proficiency_level': 'Advanced'
        }
        url = reverse('api:user-skill-detail', args=[self.user_skill.id])
        response = self.client.patch(url, new_data, format='json')

        # Check the response status code (should be 401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
