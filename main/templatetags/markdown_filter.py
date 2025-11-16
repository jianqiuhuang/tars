from django import template
from main.models import render_markdown_with_syntax_highlighting
import re

register = template.Library()


@register.filter
def markdown(text):
    """Convert markdown to HTML with syntax highlighting"""
    if not text:
        return ""
    return render_markdown_with_syntax_highlighting(text)


@register.filter(name='markdown_excerpt')
def markdown_excerpt(text, word_count=30):
    """Convert markdown to text excerpt (stripped of tags and markdown)"""
    if not text:
        return ""
    
    # Remove markdown syntax first (simple approach)
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
