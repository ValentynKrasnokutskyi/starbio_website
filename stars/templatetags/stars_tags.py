from django import template
from django.db.models import Count

from stars.models import Category, TagPost
from stars.utils import menu

register = template.Library()


@register.simple_tag
def get_menu():
    """
        Template tag to retrieve the navigation menu.
    """
    return menu


@register.inclusion_tag("stars/list_categories.html")
def show_categories(cat_selected_id=0):
    """
        Inclusion tag to display categories.
    """
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag("stars/list_tags.html")
def show_all_tags():
    """
        Inclusion tag to display all tags.
    """
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
