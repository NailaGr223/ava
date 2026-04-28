from django.shortcuts import render
from birds.models import Bird

def home(request):
    featured_birds = Bird.objects.filter(is_available=True)[:6]
    return render(request, 'index.html', {'featured_birds': featured_birds})
def contact(request):
    return render(request, 'contact.html')