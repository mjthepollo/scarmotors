from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from core.utility import print_colored
from demand.excel_line_info import *
from demand.sales_models import Order

# Create a logger with a custom log level


class NoDateException(Exception):
    pass


def get_incentive_commnet(row):
    return row[SUPPORTER].comment.text.replace("Windows 사용자:", "").replace("\n", "")


def get_incentive_date_from_row(row):
    comment = get_incentive_commnet(row)
    if "1월" in comment:
        raw_date = date(2023, 1, 1)
    elif "2월" in comment:
        raw_date = date(2023, 2, 1)
    elif "3월" in comment:
        raw_date = date(2023, 3, 1)
    elif "4월" in comment:
        raw_date = date(2023, 4, 1)
    elif "5월" in comment:
        raw_date = date(2023, 5, 1)
    elif "5얼" in comment:
        raw_date = date(2023, 5, 1)
    elif "6월" in comment:
        raw_date = date(2023, 6, 1)
    elif "6얼" in comment:
        raw_date = date(2023, 6, 1)
    elif "7월" in comment:
        raw_date = date(2023, 7, 1)
    elif "8월" in comment:
        raw_date = date(2022, 8, 1)
    elif "9월" in comment:
        raw_date = date(2022, 9, 1)
    elif "10월" in comment:
        raw_date = date(2022, 10, 1)
    elif "11월" in comment:
        raw_date = date(2022, 11, 1)
    elif "12월" in comment:
        raw_date = date(2022, 12, 1)
    else:
        print(f"WTF!! {comment}")
        raise NoDateException()
    return raw_date + relativedelta(months=1)


workbook = load_workbook('src/data_load.xlsx')
sheet_names = ["22년 12월 미청구", "23년 본사 상반기", "23년 본사 하반기"]
worksheets = (workbook.get_sheet_by_name(
    sheet_name) for sheet_name in sheet_names)
print(worksheets)
INCENTIVED_SET = set()
NOT_INCENTIVED_SET = set()


class Command(BaseCommand):
    help = 'clean models by 입출고대장'

    def handle(self, *args, **options):
        for worksheet in worksheets:
            for row in worksheet.iter_rows():
                if row[SUPPORTER].comment:
                    try:
                        date = get_incentive_date_from_row(row)
                    except NoDateException:
                        print_colored(
                            f"NO DATE: {row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}", "red")
                        continue
                    receipt_number = row[RECEIPT_NUMBER].value
                    RO_number = row[RO_NUMBER].value
                    if receipt_number == None:
                        print_colored(
                            f"{row[RO_NUMBER].value}/{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}/{row[SUPPORTER].value}:{date.strftime('%y/%m')}", "magenta")
                        NOT_INCENTIVED_SET.add(
                            f"{row[RO_NUMBER].value}/{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}/{row[SUPPORTER].value}:{date.strftime('%y/%m')}")
                        continue
                    if receipt_number:
                        orders = Order.objects.filter(
                            receipt_number=receipt_number)
                        if orders.count() != 1:
                            RO_number = row[RO_NUMBER].value
                            orders = orders.filter(
                                register__RO_number=RO_number)
                            if orders.count() != 1:
                                print_colored(
                                    f"receipt_number: {receipt_number} is not unique", "red")
                                NOT_INCENTIVED_SET.add(
                                    f"{row[RO_NUMBER].value}/{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}/{row[SUPPORTER].value}:{date.strftime('%y/%m')}")
                                continue
                    else:
                        orders = Order.objects.filter(
                            register__RO_number=RO_number)
                        if orders.count() != 1:
                            print_colored(
                                f"receipt_number: {receipt_number} is not unique", "red")
                            NOT_INCENTIVED_SET.add(
                                f"{row[RO_NUMBER].value}/{row[RECEIPT_NUMBER].value}/{row[CAR_NUMBER].value}/{row[SUPPORTER].value}:{date.strftime('%y/%m')}")
                            continue
                    order = orders.first()
                    order.incentive_paid_date = date
                    order.incentive_paid = True
                    order.save()
                    INCENTIVED_SET.add(order)
        print_colored("---INCENTIVED_SET---", "blue")
        print_colored(str(INCENTIVED_SET), "blue")
        print_colored("---NOT_INCENTIVED_SET---", "red")
        for item in NOT_INCENTIVED_SET:
            print_colored(item, "red")
