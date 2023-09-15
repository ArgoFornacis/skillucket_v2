from django.urls import path
from .views.user_management import (
    RegisterApi,
    LoginApi,
    UserProfileView,
    LogoutView,
    ChangePasswordView,
)
from .views.skill_management import (
    get_categories,
    get_skills_by_category,
    manage_user_skills,
    manage_bucket_skills,
    get_user_skills,
    get_bucket_skills,
    user_skill_detail,
    bucket_skill_detail,
)
from .views.matching_users import MatchingUsersView, SearchUserBySkill

app_name = "api"

urlpatterns = [
    path("register/", RegisterApi.as_view(), name="register"),
    path("login/", LoginApi.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("categories/", get_categories, name="get_categories"),
    path(
        "categories/<int:category_id>/skills/",
        get_skills_by_category,
        name="get_skills_by_category",
    ),
    path("user_skills/", manage_user_skills, name="manage_user_skills"),
    path("bucket_skills/", manage_bucket_skills, name="manage_bucket_skills"),
    path("matches/", MatchingUsersView.as_view(), name="matches"),
    path("search_skill/", SearchUserBySkill.as_view(), name="search_skill"),
    path("user_skills_list/", get_user_skills, name="get_user_skills"),
    path("bucket_skills_list/", get_bucket_skills, name="get_bucket_skills"),
    path(
        "user_skills/<int:user_skill_id>/", user_skill_detail, name="user_skill_detail"
    ),
    path(
        "bucket_skills/<int:bucket_skill_id>/",
        bucket_skill_detail,
        name="bucket_skill_detail",
    ),
]
