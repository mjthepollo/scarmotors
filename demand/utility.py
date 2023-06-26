import re
from datetime import date, datetime

import pandas as pd

from demand.excel_line_info import *


def print_fields(obj):
    except_fields = ["updated", "created", "id"]
    foreign_fields = []
    for key in obj.__dict__:
        if "_id" in key:
            foreign_fields.append(key[:-3])
    model = obj._meta.model
    fields = model._meta.fields
    field_names = [field.name for field in fields]
    obj_dict = {}
    for field_name in field_names:
        if not field_name in except_fields:
            if field_name in foreign_fields:
                foreign_id = obj.__dict__[field_name+"_id"]
                related_model = obj._meta.get_field(field_name).related_model
                if foreign_id:
                    foreign_key = related_model.objects.get(id=foreign_id)
                    obj_dict[field_name] = str(foreign_key)
                else:
                    obj_dict[field_name] = None
            else:
                obj_dict[field_name] = str_or_none(obj.__dict__[field_name])
    print(obj_dict)


def int_or_none(input_data):
    if not input_data:
        return None
    else:
        return int(input_data)


def str_or_none(input_data):
    if not input_data:
        return None
    else:
        return str(input_data)


def string_to_date(string):
    if isinstance(string, str):
        pattern = r"^\d{2}\d{2}\d{2}$"
        if string.count("-") == 2:
            return datetime.strptime(string, "%Y-%m-%d").date()
        elif string.count(".") == 2:
            return datetime.strptime(string, "%Y.%m.%d").date()
        elif re.match(pattern, string):
            return datetime.strptime(string, "%y%m%d").date()
        else:
            raise Exception("ERROR : WRONG INPUT TYPE - FORMAT")
    else:
        raise Exception("ERROR : WRONG INPUT TYPE, NOT STRING!")


def input_to_phone_number(input_phone_number):
    if not input_phone_number:
        return None
    elif isinstance(input_phone_number, str):
        return input_phone_number.replace("-", "")
    elif isinstance(input_phone_number, int):
        return "0"+str(input_phone_number)
    else:
        raise Exception("ERROR : WRONG INPUT TYPE")


def fault_ratio_to_int(input_data):
    if not input_data:
        return None
    elif isinstance(input_data, str):
        if "%" in input_data:
            return int(input_data[:-1])
        else:
            return int(input_data)
    elif isinstance(input_data, int):
        return input_data
    elif isinstance(input_data, float):
        return int(input_data*100)
    else:
        raise Exception("FAULT RATIO ERROR")


def input_to_date(input_date):
    # timestamp is subcalss of date!
    if isinstance(input_date, pd.Timestamp):
        return input_date.date()
    elif isinstance(input_date, date):
        return input_date
    elif isinstance(input_date, str):
        if input_date == "폐차":
            return None
        elif input_date == "미수리출고":
            return None
        elif "1센" in input_date:
            return None
        else:
            return string_to_date(input_date)
    elif isinstance(input_date, float):
        return string_to_date(str(int(input_date)))
    elif isinstance(input_date, int):
        return string_to_date(str(input_date))
    elif input_date is None:
        return None
    else:
        print("Date string is not in the correct format.")
        raise Exception("ERROR : WRONG INPUT TYPE")


def zero_if_none(num):
    if num is None:
        return 0
    else:
        return num


def check_car_number(car_number):
    pattern = r"^\d{1,3}[가-힣]{1}\d{3,4}$"
    if re.match(pattern, car_number):
        return True
    else:
        return False
