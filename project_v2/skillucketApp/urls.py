from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home_view, name="home"),
    path("profile", views.profile_view, name="profile"),
    path('login/', views.user_login, name='login'),
]
