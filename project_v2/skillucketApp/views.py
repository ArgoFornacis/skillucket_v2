from django.shortcuts import render
from skillucketApp.forms.register import RegisterForm
from django.conf import settings
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
# from .forms import UserProfileForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from .forms import SkillForm

def home_view(request):
    return render(request, "home.html")


def profile_view(request):
    return render(request, "profile.html")


def register(request):
    if request.method == 'POST':
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

    return render(request, 'register.html', {'form': form})


def user_login(request):
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


# @login_required
# def edit_profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(
#             request.POST, instance=request.user.profile
#         )  # Assuming you have a UserProfile model
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your profile has been updated.")
#             return redirect(
#                 "profile"
#             )  # Redirect to the profile page after successful update
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = UserProfileForm(
#             instance=request.user.profile
#         )  # Assuming you have a UserProfile model
#
#     return render(request, "edit_profile.html", {"form": form})


# def add_skills(request):
#     if request.method == 'POST':
#         form = SkillForm(request.POST)
#         if form.is_valid():
#             skill = form.save(commit=False)
#             skill.user = request.user  # Associate the skill with the current user
#             skill.save()
#             messages.success(request, 'Skill added successfully.')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = SkillForm()
#
#     return render(request, 'add_skills.html', {'form': form})


def custom_user_logout(request):
    logout(request)
    return redirect("home")


def custom_password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in again (optional)
            login(request, user)
            messages.success(request, "Your password was successfully changed.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "password_change.html", {"form": form})
