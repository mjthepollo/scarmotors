from datetime import date

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


def get_time(time):
    if time.hour < 12:
        return "morning"
    else:
        return "night"


def print_colored(text, color):
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
    }
    if color not in colors:
        raise ValueError(f'Invalid color: {color}')
    print(f'\033[{colors[color]}m{text}\033[0m')


def list_to_queryset(model, data):
    from django.db.models.base import ModelBase

    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)


def insert_tag(original_div, field_name, inserting_tag):
    div_finish_tag = "</div>"
    discount_amount_index = original_div.find(field_name)
    discount_amount_finish_index = original_div.find(
        div_finish_tag, discount_amount_index) + len(div_finish_tag)
    return original_div[:discount_amount_finish_index] + \
        inserting_tag + original_div[discount_amount_finish_index:]


def key_from_dict(value, dict):
    key = next((k for k, v in dict.items() if v == value), None)
    return key


def go_to_previous_url_or_search_register(request, register):
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)


def get_current_half():
    """
    현재 상반기인지 하반기인지 내놓는다.
    """
    if date.today().month < 7:
        return "first"
    else:
        return "second"


def get_start_and_end_dates_of_half(year, half):
    """
    상반기/하반기의 시작일과 종료일을 내놓는다. 튜플형태로 리턴
    """
    if half == "first":
        start_date = date(year, 1, 1)
        end_date = date(year, 6, 30)
    elif half == "second":
        start_date = date(year, 7, 1)
        end_date = date(year, 12, 31)
    elif half == "all":
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
    else:
        raise ValueError(
            "half must be 'first' or 'second'"
        )
    return (start_date, end_date)
