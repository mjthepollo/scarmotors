import logging
from datetime import date

from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register
from period_sales.models import MonthlySales

# Create a logger with a custom log level


class Command(BaseCommand):
    help = 'create all iniitial monthly sales until now'

    def handle(self, *args, **options):
        current_year = date.today().year
        current_month = date.today().month
        before_count = MonthlySales.objects.count()
        for i in range(1, current_month + 1):
            MonthlySales.create_monthly_sales(current_year, i)
        after_count = MonthlySales.objects.count()
        print_colored(
            f'{after_count - before_count}개의 MonthlySales가 생성되었습니다.', 'green')
