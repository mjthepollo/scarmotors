
import numpy as np
import pandas as pd

from demand.key_models import RequestDepartment
from demand.sales_models import RecognizedSales
from demand.utility import input_to_date, zero_if_none

RECOGNIZED_SALES_HEADER = 2

DAY_CAME_IN = 3
REAL_DAY_CAME_OUT = 4
CAR_NUMBER = 5
REQUEST_DEPARTMENT = 6
WAGE_AMOUNT = 7
COMPONENT_AMOUNT = 8
REPAIR_AMOUNT = 9
NOTE = 10
END = 11


def load_recognized_sales_data(file_name, sheet_name):
    """
    엑셀 파일을 불러와 DataFrame으로 변환한다. 
    """
    df = pd.read_excel(
        file_name, sheet_name=sheet_name,
        engine="openpyxl", header=RECOGNIZED_SALES_HEADER
    )
    return df


def get_line_numbers(df):
    """
    DataFrame의 실질적인 lines 수를 파악한다.
    """
    days_came_in = df.iloc[:, DAY_CAME_IN]
    for i, day_came_in in enumerate(days_came_in):
        if pd.isnull(day_came_in):
            return i


def get_effective_data_frame(file_name, sheet_name):
    """
    엑셀 파일을 불러와서 실질적인 데이터를 가진 DataFrame으로 변환한다. 
    """
    original_df = load_recognized_sales_data(file_name, sheet_name)
    line_numbers = get_line_numbers(original_df)
    return original_df.iloc[:line_numbers, :END].replace({pd.NaT: None, np.nan: None}, inplace=False)


def df_to_lines(df):
    lines = []
    for i in range(len(df)):
        lines.append(df.iloc[i, :].values.tolist())
    return lines


def create_recognized_sales(file_name, sheet_name):
    """
    엑셀 파일을 불러와서 실질적인 데이터로 바꾼다.
    """
    df = get_effective_data_frame(file_name, sheet_name)
    lines = df_to_lines(df)
    for line in lines:
        request_department, _ = RequestDepartment.objects.get_or_create(
            name=line[REQUEST_DEPARTMENT])
        RecognizedSales.objects.create(
            day_came_in=input_to_date(line[DAY_CAME_IN]),
            real_day_came_out=input_to_date(line[REAL_DAY_CAME_OUT]),
            car_number=line[CAR_NUMBER],
            request_department=request_department,
            wage_amount=zero_if_none(line[WAGE_AMOUNT]),
            component_amount=zero_if_none(line[COMPONENT_AMOUNT]),
            note=line[NOTE]
        )
