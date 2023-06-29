# custom_filters.py
import datetime

from django import template

register = template.Library()


@register.filter
def remove_page_param(query_dict):
    query_dict = query_dict.copy()
    query_dict.pop('page', None)
    return query_dict.urlencode()


@register.filter
def none_to_dash(value):
    if value is None:
        return '-'
    else:
        return value


@register.filter
def index_form(sequence, position):
    return sequence[position].as_div()
