"""Blog views: list and detail pages"""
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from ..models import BlogPost


def blog_list_view(request):
    """List all blog posts, optionally filterable by category"""
    posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date', '-created_at')
    
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    context = {
        'posts': posts,
        'categories': BlogPost.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'main/blog_list.html', context)


def blog_detail_view(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'main/blog_detail.html', context)

