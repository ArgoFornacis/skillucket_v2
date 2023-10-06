from skillucketApp.forms.register import RegisterForm
from django.conf import settings
import requests
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
    return render(request, "profile.html")


def register(request):
    """
        Handle user registration.

        This view handles  POST requests. For GET requests, it renders the registration form.

        Returns:
            HttpResponse: If the request is a GET, the registration form is rendered as an HttpResponse.
                          If the request is a POST and registration is successful, a success message is returned.
                          If the request is a POST and registration fails, the registration form with error messages is returned.
    """

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_url = f"{settings.BASE_URL}/api/register/"
            response = requests.post(api_url, data=form.cleaned_data)
            print(response)
            if response.status_code == 201:
                return HttpResponse("Congratz!")
            # TODO ok, it actually could be enough
            # user = form.save()
            # Redirect to a success page or perform other actions
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    """
        Handle user login.

        Returns:
            HttpResponse: If the request is a GET, the login form is rendered as an HttpResponse.
                          If the request is a POST and login is successful, the user is redirected to the home page.
                          If the request is a POST and login fails, the login form with error messages is returned.
    """

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


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
