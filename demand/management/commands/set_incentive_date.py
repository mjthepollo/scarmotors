from datetime import date

from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.excel_line_info import *
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, RequestDepartment, Supporter)
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register

# Create a logger with a custom log level


def get_incentive_commnet(row):
    return row[SUPPORTER].comment.text.replace("Windows 사용자:", "").replace("\n", "")


def get_incentive_date_from_row(row):
    comment = get_incentive_commnet(row)
    if "1월" in comment:
        return date(2023, 1, 1)
    elif "2월" in comment:
        if "입고" in "2월":
            print(row)
        return date(2023, 2, 1)
    elif "3월" in comment:
        return date(2023, 3, 1)
    elif "4월" in comment:
        return date(2023, 4, 1)
    elif "5월" in comment:
        return date(2023, 5, 1)
    elif "5얼" in comment:
        return date(2023, 5, 1)
    elif "6월" in comment:
        return date(2023, 6, 1)
    elif "6얼" in comment:
        return date(2023, 6, 1)
    elif "7월" in comment:
        return date(2023, 7, 1)
    elif "8월" in comment:
        return date(2022, 8, 1)
    elif "9월" in comment:
        return date(2022, 9, 1)
    elif "10월" in comment:
        return date(2022, 10, 1)
    elif "11월" in comment:
        return date(2022, 11, 1)
    elif "12월" in comment:
        return date(2022, 12, 1)
    else:
        print(f"WTF!! {comment}")


workbook = load_workbook('data_load.xlsx')
sheet_name1 = "22년 12월 미청구"
sheet_name2 = "23년 본사 상반기"
sheet_name3 = "23년 본사 하반기"
worksheet1 = workbook.get_sheet_by_name(sheet_name1)
worksheet2 = workbook.get_sheet_by_name(sheet_name2)
worksheet3 = workbook.get_sheet_by_name(sheet_name3)


RO_SET = set()
NONE_RO_SET = set()
for row in worksheet1.iter_rows():
    if row[SUPPORTER].comment:
        get_incentive_date_from_row(row)
        RO_SET.add(row[RO_NUMBER].value)
        if row[RO_NUMBER].value == None and row[RECEIPT_NUMBER].value == None:
            NONE_RO_SET.add(
                f"{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}")

for row in worksheet2.iter_rows():
    if row[SUPPORTER].comment:
        get_incentive_date_from_row(row)
        RO_SET.add(row[RO_NUMBER].value)
        if row[RO_NUMBER].value == None and row[RECEIPT_NUMBER].value == None:
            NONE_RO_SET.add(
                f"{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}")

for row in worksheet3.iter_rows():
    if row[SUPPORTER].comment:
        get_incentive_date_from_row(row)
        RO_SET.add(row[RO_NUMBER].value)
        if row[RO_NUMBER].value == None and row[RECEIPT_NUMBER].value == None:
            NONE_RO_SET.add(
                f"{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}")


class Command(BaseCommand):
    help = 'clean models by 입출고대장'

    def handle(self, *args, **options):
        pass
