import re
from datetime import date, datetime

import numpy as np
import pandas as pd

from demand.models import (Charge, ChargedCompany, Deposit, ExtraSales,
                           InsuranceAgent, Order, Payment, Register, Supporter)

HEADER = 5
END = 57
DAY_CAME_IN = 3
EXPECTED_DAY_CAME_OUT = 4
REAL_DAY_CAME_OUT = 5
CAR_NUMBER = 7
CAR_MODEL = 8
ABROAD_TYPE = 9
NUMBER_OF_REPAIRS_WORKS = 10
NUMBER_OF_EXCHANGE_WORKS = 11
SUPPORTER = 13
CLIENT_NAME_AND_INSURANCE_AGENT = 14
PHONE_NUMBER = 15
CHARGE_TYPE = 16
CHARGED_COMPANY = 17
ORDER_TYPE = 18
RECEIPT_NUMBER = 19
FAULT_RATIO = 20
CHARGE_DATE = 22
REPAIR_AMOUNT = 23
EXCHANGE_AMOUNT = 24
COMPONENT_AMOUNT = 25
INDEMNITY_AMOUNT = 29
DISCOUNT_AMOUNT = 30
REFUND_AMOUNT = 31
PAYMENT_TYPE = 32
PAYMENT_INFO = 33
PAYMENT_DATE = 34
# REFUND_DATE = pass
DEPOSIT_DATE = 37
DEPOSIT_AMOUNT = 38
RENT_CAR_COMPANY_NAME = 28


def string_to_date(string):
    if "-" in string:
        return datetime.strptime(string, "%Y-%m-%d").date()
    elif "." in string:
        return datetime.strptime(string, "%Y.%m.%d").date()


def fault_ratio_to_int(string):
    if not string:
        return 0
    elif isinstance(string, str):
        if "%" in string:
            return int(string[:-1])
        else:
            return int(string)
    elif isinstance(string, int):
        return string
    else:
        raise Exception("FAULT RATIO ERROR")


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


def get_refund_date(line):
    if line[REFUND_AMOUNT]:
        return input_to_date(line[PAYMENT_DATE])
    else:
        return None


def check_car_number(car_number):
    pattern = r"^\d{1,3}[가-힣]{1}\d{3,4}$"
    if re.match(pattern, car_number):
        return True
    else:
        return False


# -------------- tested by data_load_test --------------#
def check_wash_car(df, line_number):
    client_name_and_insurance_agent = df.iloc[line_number,
                                              CLIENT_NAME_AND_INSURANCE_AGENT]
    return "세차" in client_name_and_insurance_agent


def load_data(file_name, sheet_name):
    df = pd.read_excel(
        file_name, sheet_name=sheet_name, engine="openpyxl", header=HEADER
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
    return original_df.iloc[:effective_row_numbers, :END].replace({pd.NaT: None, np.nan: None}, inplace=False)


def check_line_numbers_for_registers_have_same_car_number(effective_df):
    line_numbers_for_registers = get_line_numbers_for_registers(effective_df)
    for line_numbers_for_register in line_numbers_for_registers:
        if len(line_numbers_for_register) > 1:
            all_car_number = [
                effective_df.iloc[:, CAR_NUMBER][line_number]
                for line_number in line_numbers_for_register
            ]
            try:
                assert all(car_number == all_car_number[0]
                           for car_number in all_car_number)
            except AssertionError:
                print(all_car_number[0])
                raise AssertionError


def check_line_numbers_for_registers_have_unique_RO_number(effective_df):
    line_numbers_for_registers = get_line_numbers_for_registers(effective_df)
    RO_numbers = [
        effective_df.index.values[line_numbers[0]]
        for line_numbers in line_numbers_for_registers
    ]
    RO_numbers_set = set(RO_numbers)
    try:
        assert len(RO_numbers) == len(RO_numbers_set)
    except AssertionError:
        print(line_numbers_for_registers)
        print(RO_numbers)
        for RO_number in RO_numbers:
            if RO_numbers.count(RO_number) > 1:
                print(RO_number)
        print(len(RO_numbers), len(RO_numbers_set))


def get_line_numbers_for_registers(effective_df):
    line_numbers_for_registers = []
    for i, RO_number in enumerate(effective_df.index.values):
        if pd.isnull(RO_number):
            if not check_wash_car(effective_df, i):
                line_numbers_for_registers[-1].append(i)
            else:  # 세차의 경우 RO_number가 없어야 한다.
                pass
        else:
            if RO_number == effective_df.index.values[i - 1]:
                line_numbers_for_registers[-1].append(i)
            else:
                line_numbers_for_registers.append([i])
    return line_numbers_for_registers

# -------------- tested by data_load_test finish--------------#


def get_client_name_and_insurance_agent_name(first_line):
    client_name_and_insurance_agent = first_line[CLIENT_NAME_AND_INSURANCE_AGENT]
    if isinstance(client_name_and_insurance_agent, str):
        if "/" in client_name_and_insurance_agent:
            return tuple(client_name_and_insurance_agent.split("/"))
        elif "담당" == client_name_and_insurance_agent[-2:]:
            return "", client_name_and_insurance_agent[:-2]
        else:
            return "", client_name_and_insurance_agent
    else:
        return "", ""


def make_extra_sales_from_line(line):
    pass


def make_extra_sales_from_effective_df(df):
    for i in range(len(df)):
        if check_wash_car(df, i):
            line = df.iloc[i, :].values.tolist()
            make_extra_sales_from_line(line)


def make_register_from_first_line_number(first_line):
    supporter, _ = Supporter.objects.get_or_create(name=first_line[SUPPORTER])
    client_name, insurance_agent_name = get_client_name_and_insurance_agent_name(
        first_line)
    if insurance_agent_name:
        insurance_agent, _ = InsuranceAgent.objects.get_or_create(
            name=insurance_agent_name)
    else:
        insurance_agent = None
    return Register.objects.create(
        car_number=first_line[CAR_NUMBER],
        day_came_in=input_to_date(first_line[DAY_CAME_IN]),
        expected_day_came_out=input_to_date(first_line[EXPECTED_DAY_CAME_OUT]),
        real_day_came_out=input_to_date(first_line[REAL_DAY_CAME_OUT]),
        car_model=str(first_line[CAR_MODEL]),
        abroad_type=first_line[ABROAD_TYPE],
        number_of_repair_works=first_line[NUMBER_OF_REPAIRS_WORKS],
        number_of_exchange_works=first_line[NUMBER_OF_EXCHANGE_WORKS],
        supporter=supporter,
        client_name=client_name,
        insurance_agent=insurance_agent,
        phone_number=str(first_line[PHONE_NUMBER]),
        rentcar_company_name=first_line[RENT_CAR_COMPANY_NAME],
    )


def make_order_payment_charge_and_deposit_with_line(line, register):
    charged_company = ChargedCompany.objects.get_or_create(
        name=line[CHARGED_COMPANY])
    fault_ratio = fault_ratio_to_int(line[FAULT_RATIO])
    Order.objects.create(
        register=register,
        charged_company=charged_company,
        charge_type=line[CHARGE_TYPE],
        order_type=line[ORDER_TYPE],
        receipt_number=str(line[RECEIPT_NUMBER]),
        fault_ratio=fault_ratio,
    )
    if line[INDEMNITY_AMOUNT]:
        Payment.objects.create(
            indemnity_amount=int(line[INDEMNITY_AMOUNT]),
            discount_amount=int(line[DISCOUNT_AMOUNT]),
            refund_amount=int(line[REFUND_AMOUNT]),
            payment_type=line[PAYMENT_TYPE],
            payment_info=line[PAYMENT_INFO],
            payment_date=input_to_date(input_to_date(line[PAYMENT_DATE])),
            refund_date=get_refund_date(line)
        )
    if line[CHARGE_DATE]:
        Charge.objects.create(
            charge_date=input_to_date(line[CHARGE_DATE]),
            repair_amount=int(line[REPAIR_AMOUNT]),
            component_amount=int(line[COMPONENT_AMOUNT]),
        )
    if line[DEPOSIT_DATE]:
        Deposit.objects.create(
            deposit_amount=int(line[DEPOSIT_AMOUNT]),
            deposit_day=input_to_date(line[DEPOSIT_DATE]),
        )


def make_complete_register_for_line_numbers(df, line_numbers):
    first_line = df.iloc[line_numbers[0], :].values.tolist()
    register = make_register_from_first_line_number(first_line)
    for line_number in line_numbers:
        line = df.iloc[line_number, :].values.tolist()
        make_extra_sales_from_line(line, register)


def make_order_from_effective_df(df):
    line_numbers_for_registers = get_line_numbers_for_registers(df)
    for line_numbers_for_register in line_numbers_for_registers:
        make_complete_register_from_df(df, line_numbers_for_register)
