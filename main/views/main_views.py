"""Main views: home and about pages"""
from django.shortcuts import render


def home_view(request):
    """Home page with navigation links"""
    return render(request, 'main/home.html')


def about_view(request):
    """About page with personal description and social links"""
    context = {
        'linkedin_url': 'https://www.linkedin.com/in/yourprofile',  # Update with your LinkedIn
        'github_url': 'https://github.com/yourusername',  # Update with your GitHub
    }
    return render(request, 'main/about.html', context)

