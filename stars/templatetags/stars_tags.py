from django import template
import stars.views as views
from stars.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('stars/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected_id}


@register.inclusion_tag('stars/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.all()}
