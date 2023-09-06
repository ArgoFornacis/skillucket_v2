
from django.shortcuts import render

def home_view(request):

    return render(request, 'home.html')

def profile_view(request):

    return render(request, 'profile.html')



