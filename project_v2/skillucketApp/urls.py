from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.custom_user_logout, name="custom_user_logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(success_url=reverse_lazy("password_change_done")),
        name="password_change",
    ),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("add_skills/", views.add_skills, name="add_skills"),
]
