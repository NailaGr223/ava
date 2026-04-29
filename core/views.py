from django.shortcuts import render
from birds.models import Bird
from blog.models import BlogPost   

def home(request):
    featured_birds = Bird.objects.filter(is_available=True)[:6]
    recent_blogs = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    return render(request, 'index.html', {
        'featured_birds': featured_birds,
        'recent_blogs': recent_blogs,
    })
def contact(request):
    return render(request, 'contact.html')