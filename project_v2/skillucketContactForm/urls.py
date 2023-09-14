from django.urls import path
from . import views

urlpatterns = [
    path("", views.contact, name="contact"),
    # path("success/", views.contact_success, name="success"),
    path("redirect/", views.redirect_view, name="redirect"),
]
