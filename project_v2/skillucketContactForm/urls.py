from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact, name="contact_success"),
    path('redirect/', views.redirect_view, name='redirect'),

]
