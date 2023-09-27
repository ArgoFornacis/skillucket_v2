from skillucketApp.forms.register import RegisterForm
from django.conf import settings
import requests
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from skillucketApp.forms.skills_profile import ProfileForm
from skillucketApp.forms.skills_profile import SkillForm
from .models.profile import Profile


def home_view(request):
    """
        Render the user's  home page, .

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered  home page as an HttpResponse.
    """
    return render(request, "home.html")


def profile_view(request):
    """
        Render the user's profile page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered profile page as an HttpResponse.
    """
    if request.user.is_authenticated:
        user_id = request.user.id
        profile = Profile.objects.get(user=user_id)
        # Now, user_id contains the ID of the authenticated user
    else:
        # The user is not authenticated
        user_id = None  # You can handle this case as needed

    return render(request, "profile_v2.html", {"profile": profile})


def register(request):
    """Register view handles get and post requests.
    Register new user to db and create automatically a profile for the user.
    If a profile pic was sent in the registration form, it is added to the profile.
    After successful registration, redirect to login.
    """

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                user = User.objects.create_user(username=form_data["username"], password=form_data["password"], email=form_data["email"])
                if user:
                    if "image" in request.FILES:
                        image = request.FILES["image"]
                        profile = Profile.objects.get(user=user)
                        profile.image = image
                        profile.save()
                    return redirect("login")
                else:
                    return HttpResponse("Failed to create user")
            except IntegrityError:
                form.add_error(None, "Username or email already exists")
    else:
        form = RegisterForm()

    return render(request, "register_v4.html", {"form": form})


def user_login(request):
    """
    Login view uses Django built in AuthenticationForm, authenticate function and login function
    """

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("profile")
    else:
        form = AuthenticationForm()

    return render(request, "login_v4.html", {"form": form})


def add_skills(request):
    """
    Handle adding skills to a user's profile.
    Returns:
            HttpResponse: If the request is a GET, the skill addition form is rendered as an HttpResponse.
                          If the request is a POST and skill addition is successful, a success message is returned.
                          If the request is a POST and skill addition fails, the skill addition form with error messages is returned.
    """
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user  # Associate the skill with the current user
            skill.save()
            messages.success(request, "Skill added successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SkillForm()

    return render(request, "add_skills.html", {"form": form})


@login_required
def edit_profile(request):
    """
        Handle editing a user's profile.
    Returns:
            HttpResponse: If the request is a GET, the profile editing form is rendered as an HttpResponse.
                          If the request is a POST and profile update is successful, the user is redirected to the profile page.
                          If the request is a POST and profile update fails, the profile editing form with error messages is returned.

    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect(
                "profile"
            )  # Redirect to the profile page after successful update
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, "edit_profile.html", {"form": form})


def custom_user_logout(request):
    """
        Handle user logout.
        This view logs the user out and redirects them to the home page.


    """
    logout(request)
    return redirect("home")
