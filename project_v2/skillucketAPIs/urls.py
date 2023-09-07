from django.urls import path
from .views import RegisterApi, LoginApi
app_name = 'api'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),

]
