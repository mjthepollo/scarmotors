from datetime import datetime

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.excel_load import (get_effective_data_frame,
                               make_models_from_effective_df)
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register


class Command(BaseCommand):
    """
    Usage Example!
    python manage.py create_initial_model --file_name="src/data_load.xlsx" --sheet_name="23년 본사 상반기"
    """
    help = 'Create initial models'

    def add_arguments(self, parser):
        parser.add_argument('--file_name', type=str,
                            help="file_name(xlsx)", default=None)
        parser.add_argument('--sheet_name', type=str,
                            help="sheet_name", default=None)

    def handle(self, *args, **options):
        file_name = options.get("file_name")
        sheet_name = options.get("sheet_name")
        print(file_name, sheet_name)
        if not file_name:
            file_name = "src/test.xlsx"
        if not sheet_name:
            sheet_name = "23년 본사 상반기"
        df = get_effective_data_frame(file_name, sheet_name)
        make_models_from_effective_df(df)
        charge_count = Charge.objects.all().count()
        charget_company_count = ChargedCompany.objects.all().count()
        deposit_count = Deposit.objects.all().count()
        extra_sales_count = ExtraSales.objects.all().count()
        insurance_agent_count = InsuranceAgent.objects.all().count()
        order_count = Order.objects.all().count()
        payment_count = Payment.objects.all().count()
        register_count = Register.objects.all().count()
        supporter_count = Supporter.objects.all().count()
        print_colored(f"Charge Created Count: {charge_count}", "green")
        print_colored(
            f"ChargedCompany Created Count: {charget_company_count}", "green")
        print_colored(f"Deposit Created Count: {deposit_count}", "green")
        print_colored(
            f"ExtraSales Created Count: {extra_sales_count}", "green")
        print_colored(
            f"InsuranceAgent Created Count: {insurance_agent_count}", "green")
        print_colored(f"Order Created Count: {order_count}", "green")
        print_colored(f"Payment Created Count: {payment_count}", "green")
        print_colored(f"Register Created Count: {register_count}", "green")
        print_colored(f"Supporter Created Count: {supporter_count}", "green")
        print_colored("All models created", "magenta")
