from django.urls import path
from . import views

urlpatterns = [

    path("contact/", views.contact, name="contact"),
    path("", views.contact, name="contact"),
    path("redirect/", views.redirect_view, name="redirect"),
    path('contact_success/', views.contact_success, name='contact_success'),
]
