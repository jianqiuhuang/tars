"""Main views: about page"""
from django.shortcuts import render


def about_view(request):
    """About page with personal description and social links"""
    context = {
        'linkedin_url': 'https://www.linkedin.com/in/leo-huang-34402a82 ',  # Update with your LinkedIn
        'github_url': 'https://github.com/jianqiuhuang',  # Update with your GitHub
        'profile_image': 'main/images/about_me.jpg',  # Profile image at main/static/main/images/about_me.jpg
    }
    return render(request, 'main/about.html', context)

