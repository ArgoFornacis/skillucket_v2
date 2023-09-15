import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
client = Client()


class RegisterApiTest(TestCase):
    """ test class to test register api """

    def test_successful_registration(self):
        """ test register new user with all required fields """
        new_user = {
            "username": "test",
            "password": 123,
            "email": "test@1.com"
        }
        response = client.post(reverse('api:register'),
                               data=json.dumps(new_user),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data["message"], "User registered successfully")

    def test_fail_to_register(self):
        """ test if it is possible to register new user without email required field """
        new_user = {
            "username": "test",
            "password": 123,
        }
        response = client.post(reverse('api:register'),
                               data=json.dumps(new_user),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, 400)


class LoginApiTest(TestCase):
    """  test class to test login api """
    def setUp(self):
        """ setup a fake database for test purposes """
        self.user = User.objects.create_user(username="test", password="123")

    def test_successful_log_in(self):
        """ test if user was able to log in with all required fields and a token was created """
        user = {"username": "test", "password": "123"}
        response = client.post(reverse('api:login'),
                               data=json.dumps(user),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertIn("user_id", response.json())

    def test_fail_to_login(self):
        """ test if user was able to log in without filling required fields, or not registered user """
        user = {"username": "test"}
        not_registered_user = {"username": "test_1", "password": "123"}
        response = client.post(reverse('api:login'),
                               data=json.dumps(user),
                               content_type='application/json'
                               )
        response_1 = client.post(reverse('api:login'),
                                 data=json.dumps(not_registered_user),
                                 content_type='application/json'
                                 )
        self.assertIn('password', response.json())
        self.assertEquals(response.json()['password'], ['This field is required.'])
        self.assertEquals(response_1.json()["message"], 'Wrong username or password')


class UserProfileApiTest(TestCase):
    """ test class to test profile api view """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='123')
        self.token = Token.objects.create(user=self.user)
        self.profile_url = reverse('api:profile')

    def test_get_user_profile_authenticated(self):
        """ test getting the profile of the authenticated user """
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}'
        }
        response = client.get(self.profile_url, **headers)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["username"], 'test_user')
        self.assertIn('first_name', response.json())

    def test_change_user_profile_authenticated(self):
        """ testing put request to profile api view with auth user """
        new_data = {"first_name": "new_user"}
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}',
            'content_type': 'application/json',
        }
        response = client.put(self.profile_url, data=json.dumps(new_data), **headers)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["first_name"], "new_user")

    def get_user_profile_unauthenticated(self):
        """ testing get request with unauthenticated user """
        response = client.get(self.profile_url)
        self.assertEquals(response.status_code, 401)

    def change_user_profile_unauthenticated(self):
        """ testing put request to profile api view with unauth user """
        new_data = {"last_name": "test_last"}
        response = client.put(self.profile_url,
                              data=json.dumps(new_data),
                              content_type='application/json'
                              )
        self.assertEquals(response.status_code, 401)


class ChangePasswordApiTest(TestCase):
    """ test class that testing the change user password api view """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='123')
        self.token = Token.objects.create(user=self.user)
        self.change_password_url = reverse('api:change_password')

    def test_change_password_authenticate_user(self):
        """ test put request to change password api view """
        password_data = {"old_password": "123", "new_password": "123456"}
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}',
            'content_type': 'application/json',
        }
        response = client.put(self.change_password_url, data=json.dumps(password_data), **headers)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["message"], 'Password updated successfully.')

    def test_change_password_unauthenticate_user(self):
        """ test put request to change password api view """
        password_data = {"old_password": "123", "new_password": "123456"}
        headers = {
            'content_type': 'application/json',
        }
        response = client.put(self.change_password_url, data=json.dumps(password_data), **headers)
        self.assertEquals(response.status_code, 401)
        self.assertEquals(response.json()["detail"], 'Authentication credentials were not provided.')

    def test_typing_wrong_old_password(self):
        """  test put request to change the password when the old password is incorrect and the user ia authenticated"""
        password_data = {"old_password": "1", "new_password": "123456"}
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}',
            'content_type': 'application/json',
        }
        response = client.put(self.change_password_url, data=json.dumps(password_data), **headers)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json(), {'old_password': ['Wrong password.']})


class LogoutApiTest(TestCase):
    """ test class that testing logout api view"""
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='123')
        self.token = Token.objects.create(user=self.user)
        self.logout_url = reverse('api:logout')

    def test_logout_authenticated_user(self):
        """ test logout with token authentication """
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.token.key}',
            'content_type': 'application/json',
        }
        response = client.post(self.logout_url, **headers)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["message"], "Logged out successfully")

    def test_logout_unauthenticated_user(self):
        """ test logout with unauthenticated """
        response = client.post(self.logout_url)
        self.assertEquals(response.status_code, 401)
        self.assertEquals(response.json()["detail"], "Authentication credentials were not provided.")
