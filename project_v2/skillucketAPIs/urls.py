from django.urls import path
from .views.user_managment import RegisterApi, LoginApi, UserProfileView, LogoutView, ChangePasswordView
app_name = 'api'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
