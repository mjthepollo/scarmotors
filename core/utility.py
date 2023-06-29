

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
