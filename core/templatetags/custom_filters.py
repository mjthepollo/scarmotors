# custom_filters.py
import datetime

from django import template
from django.utils.safestring import mark_safe

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
    if len(sequence) > position:
        return sequence[position]
    else:
        return mark_safe("")


@register.filter
def per_thousand(value):
    return int(value/1000)


@register.filter
def thousand_format(value):
    return format(int(value/1000), ',')


@register.filter
def get_percent(value, dividor):
    try:
        return f"{format(value/dividor, '10.2%')}"
    except ZeroDivisionError:
        return "-%"


@register.filter
def get_div(value, user):
    return value.get_div(user)
