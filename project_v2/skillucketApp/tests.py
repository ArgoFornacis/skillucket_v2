from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import custom_user_logout
from django.contrib.messages import get_messages
from .forms.register import RegisterForm
# SkillForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.messages.storage.fallback import FallbackStorage


class HomeViewTest(TestCase):
    def test_home_view(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class ProfileViewTest(TestCase):
    def test_profile_view(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")


class RegisterViewTest(TestCase):
    def test_register_view_GET(self):
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")


class UserLoginViewTest(TestCase):
    def test_user_login_view_GET(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class AddSkillsViewTest(TestCase):
    def test_add_skills_view_GET(self):
        url = reverse("add_skills")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_skills.html")


class EditProfileViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="mariana", password="bamboo123")

    def test_edit_profile_view_GET(self):
        url = reverse("edit_profile")
        self.client.login(username="mariana", password="bamboo123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_profile.html")


class CustomUserLogoutViewTest(TestCase):
    def test_custom_user_logout_view(self):
        url = reverse("custom_user_logout")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 302
        )  # Expecting a redirect to the home page
