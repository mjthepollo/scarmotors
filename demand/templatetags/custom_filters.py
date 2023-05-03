# custom_filters.py
from django import template

register = template.Library()


@register.filter
def remove_page_param(query_dict):
    query_dict = query_dict.copy()
    query_dict.pop('page', None)
    return query_dict.urlencode()
