from django import template
from core.models import Post, Comment, Category

register = template.Library()
@register.inclusion_tag('blog/latest_posts.html')
def latest_posts():
    context = {
        'l_posts': Post.objects.all()[0:5],
    }
    return context


@register.inclusion_tag('blog/latest_comments.html')
def latest_comments():
    context = {
        'l_comments': Comment.objects.all()[:5], # if you want to make comment filter change .all() to = .filter(active=True)
    }
    return context


@register.inclusion_tag('blog/l_categories.html')
def l_categories():
    context = {
        'l_categories': Category.objects.all()[:5], # if you want to make comment filter change .all() to = .filter(active=True)
    }
    return context