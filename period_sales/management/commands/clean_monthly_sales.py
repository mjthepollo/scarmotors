import logging
from datetime import date

from django.core.management.base import BaseCommand

from core.utility import print_colored
from period_sales.models import MonthlySales

# Create a logger with a custom log level


class Command(BaseCommand):
    help = 'clean all monthly_sales'

    def handle(self, *args, **options):
        monthl_sales_count = MonthlySales.objects.count()
        MonthlySales.objects.all().delete()
        print_colored(
            f'{monthl_sales_count}개의 MonthlySales가 삭제되었습니다.', 'green')
