
from django.shortcuts import render
from django.http import HttpResponse

# def home_view(request):
#
#     return render(request, 'skillucketApp/home.html')
#
# def profile_view(request):
#
#     return render(request, 'skillucketApp/profile.html')


from django.http import HttpResponse

def home_view(request):

    html_content = "/home"
    return HttpResponse(html_content)

def profile_view(request):

    html_content = "/profile"
    return HttpResponse(html_content)
