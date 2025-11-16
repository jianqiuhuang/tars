from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re


def render_markdown_with_syntax_highlighting(markdown_text):
    """Convert markdown to HTML with syntax highlighting for code blocks"""
    
    # First, process code blocks with syntax highlighting
    def replace_code_block(match):
        lang = match.group(1) or 'text'
        code = match.group(2).strip()
        
        try:
            lexer = get_lexer_by_name(lang)
        except:
            lexer = get_lexer_by_name('text')
        
        formatter = HtmlFormatter(style='default', noclasses=False)
        highlighted = highlight(code, lexer, formatter)
        return highlighted
    
    # Replace ```language code ``` blocks with highlighted versions
    # This pattern handles: ```language\ncode\n```
    markdown_text = re.sub(
        r'```(\w+)\s*\n(.*?)\n```',
        replace_code_block,
        markdown_text,
        flags=re.DOTALL
    )
    
    # Also handle code blocks without language specifier
    def replace_code_block_no_lang(match):
        code = match.group(1).strip()
        lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter(style='default', noclasses=False)
        highlighted = highlight(code, lexer, formatter)
        return highlighted
    
    markdown_text = re.sub(
        r'```\n(.*?)\n```',
        replace_code_block_no_lang,
        markdown_text,
        flags=re.DOTALL
    )
    
    # Convert remaining markdown to HTML
    html = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables', 'extra'])
    return html


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('travel', 'Travel'),
        ('finance', 'Finance'),
        ('diy', 'DIY'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(help_text="Markdown content is supported. Use ```language for code blocks.")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def get_html_content(self):
        """Convert markdown content to HTML with syntax highlighting"""
        return render_markdown_with_syntax_highlighting(self.content)
    
    def get_excerpt(self, word_count=30):
        """Get plain text excerpt from markdown content"""
        text = self.content
        
        # Remove code blocks
        text = re.sub(r'```[\w\s]*\n(.*?)\n```', '', text, flags=re.DOTALL)
        # Remove bold/italic
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)
        # Remove links
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # Remove headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        
        # Truncate to word count
        words = text.split()[:word_count]
        excerpt = ' '.join(words)
        
        if len(text.split()) > word_count:
            excerpt += '...'
        
        return excerpt.strip()
