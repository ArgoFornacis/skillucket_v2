from django.shortcuts import render
from skillucketApp.forms.register import RegisterForm
from django.conf import settings
import requests
from django.http import HttpResponse

def home_view(request):
    return render(request, "home.html")


def profile_view(request):
    return render(request, "profile.html")


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_url = f"{settings.BASE_URL}/api/register/"
            response = requests.post(api_url, data=form.cleaned_data)
            print(response)
            if response.status_code == 201:
                return HttpResponse("Congratz!")
            # TODO ok, it actually could be enough
            # user = form.save()
            # Redirect to a success page or perform other actions
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
