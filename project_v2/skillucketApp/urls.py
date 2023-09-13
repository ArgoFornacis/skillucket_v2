from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home_view, name="home"),
    path("profile", views.profile_view, name="profile"),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]
