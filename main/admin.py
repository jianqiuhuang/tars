from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'created_at')
    list_filter = ('category', 'published_date', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('category', 'published_date')
        }),
    )
