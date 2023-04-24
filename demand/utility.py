from datetime import date, datetime

import numpy as np
import pandas as pd

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)

END = 56
DAY_CAME_IN = 2
EXPECTED_DAY_CAME_OUT = 3
REAL_DAY_CAME_OUT = 4
CAR_NUMBER = 6
CAR_MODEL = 7
ABROAD_TYPE = 8
NUMBER_OF_REPAIRS_WORKS = 9
NUMBER_OF_EXCHANGE_WORKS = 10
SUPPORTER = 12
CLIENT_NAME_AND_INSURANCE_AGENT = 13
PHONE_NUMBER = 14
RENT_CAR_COMPANY_NAME = 27


def string_to_date(string):
    if "-" in string:
        return datetime.strptime(string, "%Y-%m-%d").date()
    elif "." in string:
        return datetime.strptime(string, "%Y.%m.%d").date()


def input_to_date(input_date):
    print(input_date, type(input_date))
    # timestamp is subcalss of date!
    if isinstance(input_date, pd.Timestamp):
        return input_date.date()
    elif isinstance(input_date, date):
        return input_date
    elif isinstance(input_date, str):
        return string_to_date(input_date)
    else:
        raise Exception("ERROR : WRONG INPUT TYPE")


def load_data(file_name, sheet_name):
    df = pd.read_excel(
        file_name, sheet_name=sheet_name, engine="openpyxl", header=5, index_col=2
    )
    return df


def get_effective_row_numbers(df):
    days_came_in = df.iloc[:, DAY_CAME_IN]
    for i, day_came_in in enumerate(days_came_in):
        if pd.isnull(day_came_in):
            return i


def get_effective_data_frame(file_name, sheet_name):
    original_df = load_data(file_name, sheet_name)
    effective_row_numbers = get_effective_row_numbers(original_df)
    return original_df.iloc[:effective_row_numbers, :END].replace(np.nan, None)


# -------------pandas utility finish---------------#


def check_effective_line_numbers_have_same_car_number(effective_df):
    effective_line_numbers = get_effective_line_numbers(effective_df)
    for effective_line_number in effective_line_numbers:
        if len(effective_line_number) > 1:
            all_car_number = [
                effective_df.iloc[:, CAR_NUMBER][line_number]
                for line_number in effective_line_number
            ]
            try:
                assert all(car_number == all_car_number[0]
                           for car_number in all_car_number)
            except AssertionError:
                print(all_car_number[0])
                raise AssertionError


def check_effective_line_numbers_have_unique_RO_number(effective_df):
    effective_line_numbers = get_effective_line_numbers(effective_df)
    RO_numbers = [
        effective_df.index.values[line_numbers[0]]
        for line_numbers in effective_line_numbers
    ]
    RO_numbers_set = set(RO_numbers)
    assert len(RO_numbers) == len(RO_numbers_set)


def get_effective_line_numbers(effective_df):
    effective_line_numbers = []
    for i, value in enumerate(effective_df.index.values):
        if pd.isnull(value):
            effective_line_numbers[-1].append(i)
        else:
            if value == effective_df.index.values[i - 1]:
                effective_line_numbers[-1].append(i)
            else:
                effective_line_numbers.append([i])
    return effective_line_numbers


def get_clinet_name_and_insurance_agent_name(first_line):
    if "/" in first_line[CLIENT_NAME_AND_INSURANCE_AGENT]:
        return first_line[CLIENT_NAME_AND_INSURANCE_AGENT].split("/")
    elif "담당" == first_line[CLIENT_NAME_AND_INSURANCE_AGENT][-2:]:
        return "", first_line[CLIENT_NAME_AND_INSURANCE_AGENT][:-2]


def make_order_from_first_line_number(first_line):
    supporter = Supporter.objects.get_or_create(name=first_line[SUPPORTER])
    client_name, insurance_agent_name = get_clinet_name_and_insurance_agent_name(
        first_line)
    insurance_agent = InsuranceAgent.objects.get_or_create(
        name=insurance_agent_name)
    return Order.objects.create(
        car_number=first_line[CAR_NUMBER],
        day_came_in=string_to_date(
            input_to_date(first_line[DAY_CAME_IN])),
        expected_day_came_out=string_to_date(
            input_to_date(first_line[EXPECTED_DAY_CAME_OUT])),
        real_day_came_out=string_to_date(
            input_to_date(first_line[REAL_DAY_CAME_OUT])),
        car_model=first_line[CAR_MODEL],
        abroad_type=first_line[ABROAD_TYPE],
        number_of_repairs_works=first_line[NUMBER_OF_REPAIRS_WORKS],
        number_of_exchange_works=first_line[NUMBER_OF_EXCHANGE_WORKS],
        supporter=supporter,
        client_name=client_name,
        insurance_agent=insurance_agent,
        phone_number=first_line[PHONE_NUMBER],
        rent_car_company_name=first_line[RENT_CAR_COMPANY_NAME],
    )


def make_order_from_effective_df(df):
    effective_line_numbers = get_effective_line_numbers(df)
    for effective_line_number in effective_line_numbers:
        first_line = df.iloc[effective_line_number[0], :].values.tolist()
        if len(effective_line_number) == 1:
            pass
