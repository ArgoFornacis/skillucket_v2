from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserSkillsListView, UserSkillsCreateView, UserSkillUpdateView, UserSkillDeleteView,
    BucketSkillsListView, BucketSkillsCreateView, BucketSkillUpdateView, BucketSkillDeleteView
)


urlpatterns = [
    path("", views.home_view, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("matches/", views.list_matches_view, name="matching_users"),
    path('user_skills/', UserSkillsListView.as_view(), name='user_skills'),
    path("user_skills/create/", UserSkillsCreateView.as_view(), name='user_skills_create'),
    path("user_skills/<int:pk>", UserSkillUpdateView.as_view(), name='user_skill_update'),
    path("user_skills/<int:pk>/delete", UserSkillDeleteView.as_view(), name='user_skill_delete'),
    path('bucket_skills/', BucketSkillsListView.as_view(), name='bucket_skills'),
    path("bucket_skills/create/", BucketSkillsCreateView.as_view(), name='bucket_skills_create'),
    path("bucket_skills/<int:pk>", BucketSkillUpdateView.as_view(), name='bucket_skill_update'),
    path("bucket_skills/<int:pk>/delete", BucketSkillDeleteView.as_view(), name='bucket_skill_delete'),
    path('search/', views.search_skill_view, name='search'),

    path(
        "password_change/",
        PasswordChangeView.as_view(success_url=reverse_lazy("password_change_done")),
        name="password_change",
    ),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("add_skills/", views.add_skills, name="add_skills"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
