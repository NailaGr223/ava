from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/list.html', {'posts': posts})