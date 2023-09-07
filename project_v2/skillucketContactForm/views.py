from django.shortcuts import render
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            # Redirect to a thank you page or homepage
            pass
    else:
        form = ContactForm()

    return render(request, 'skillucketContactForm/contact.html', {'form': form})
