from django.urls import path
from .views.user_management import RegisterApi, LoginApi
from .views.skill_management import (
    get_categories,
    get_skills_by_category,
    manage_user_skills,
    manage_bucket_skills,
)

app_name = 'api'

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
    path('categories/', get_categories, name='get_categories'),
    path('categories/<int:category_id>/skills/', get_skills_by_category, name='get_skills_by_category'),
    path('user_skills/', manage_user_skills, name='manage_user_skills'),
    path('bucket_skills/', manage_bucket_skills, name='manage_bucket_skills'),
]
