"""Views package - imports all views for backward compatibility"""
from .main_views import home_view, about_view
from .blog_views import blog_list_view, blog_detail_view
from .secret_view import secret_view

__all__ = [
    'home_view',
    'about_view',
    'blog_list_view',
    'blog_detail_view',
    'secret_view',
]

