from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from skillucketApp.forms import ProfileForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import SkillForm


def home_view(request):

    return render(request, "home.html")


def profile_view(request):

    return render(request, "profile.html")


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


from django.contrib.auth.forms import UserChangeForm


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(
        request,
        "edit_profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def add_skills(request):
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
