from django import template
from school.models import *

register = template.Library()

@register.simple_tag(name='getyears')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag("school/list_categories.html")
def show_categories(sort=None, year_selected=0):
    if not sort:
        years = Category.objects.all()
    else:
        years = Category.objects.order_by(sort)

    return {"years": years, "year_selected": year_selected}
