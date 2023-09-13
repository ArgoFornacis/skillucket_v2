from django.shortcuts import render



def home_view(request):
    return render(request, "home.html")


def profile_view(request):
    return render(request, "profile.html")



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to a success page or perform other actions
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
