from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from skillucketApp.models.user_skill import UserSkill
from skillucketApp.models.bucket_skill import BucketSkill
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill

""" test class that is testing matching user related endpoints """


client = Client()


class UserMatchesTest(TestCase):
    """ testing two different endpoints: first, automatic matches that the authenticated user gets according
    to his bucket list. second: matches according to a skill search term
    """
    def setUp(self):
        """ create db with few user and skills for test purposes """
        self.matches_url = reverse('api:matches')
        self.search_skill_url = reverse('api:search_skill')
        self.user1 = User.objects.create_user(username='test_user1', password='123')
        self.user2 = User.objects.create_user(username='test_user2', password='123')
        self.token = Token.objects.create(user=self.user1)
        # create new  category and skill in db (done by admin normally)
        self.category = Category.objects.create(name='baking')
        self.skill = Skill.objects.create(category=self.category, name='sourdough bread baking')
        # create skill for user2:
        self.user_skill = UserSkill.objects.create(user=self.user2,
                                                   skill=self.skill,
                                                   proficiency_level='beginner'
                                                   )
        # create bucket list skill for user1:
        self.bucket_skill = BucketSkill.objects.create(user=self.user1,
                                                       skill=self.skill
                                                       )
        # adding one more skill and one more user to check if we get the right match:
        self.user3 = User.objects.create(username='test_user3', password='123')
        self.category2 = Category.objects.create(name='programing')
        self.skill2 = Skill.objects.create(category=self.category, name='python')
        # the new user knows python:
        self.user_skill = UserSkill.objects.create(user=self.user3,
                                                   skill=self.skill2,
                                                   proficiency_level='beginner'
                                                   )

    def test_matches_with_authenticated_user(self):
        """ test the matches that auth user is getting """
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }
        response = client.get(self.matches_url, **headers)
        # test username2 name is on matches list:
        self.assertEquals(response.json()[0]["username"], "test_user2")
        self.assertEquals(response.status_code, 200)

    def test_matches_with_unauthenticated_user(self):
        """ test if unauthenticated user gets matches """
        response = client.get(self.matches_url)
        self.assertEquals(response.status_code, 401)

    def test_getting_the_right_match(self):
        """ testing if user1 getting user that doesn't match his bucket list skill (for example user3)"""
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }
        response = client.get(self.matches_url, **headers)
        for user in response.json():
            self.assertNotEquals(user["username"], "test_user3")

    def test_search_user_matches_authenticated_user(self):
        """ test matching users to the authenticated user by a skill search """
        """ test the matches that auth user is getting """
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }
        url_with_params = self.search_skill_url + '?name=python'
        response = client.get(url_with_params, **headers)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()[0]["username"], "test_user3")

    def test_search_user_matches_unauthenticated_user(self):
        """ test matching users with unauthenticated"""
        url_with_params = self.search_skill_url + '?name=python'
        response = client.get(url_with_params)
        self.assertEquals(response.status_code, 401)

    def test_search_non_existing_skill(self):
        """ test matching users to a skill search term that is not in the db """
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }
        url_with_params = self.search_skill_url + '?name=guitar playing'
        response = client.get(url_with_params, **headers)
        self.assertEquals(response.status_code, 404)
        self.assertIn("error", response.json())
