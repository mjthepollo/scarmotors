from django.core.management.base import BaseCommand

from demand.load_recognized_sales import create_recognized_sales
from demand.sales_models import RecognizedSales


class Command(BaseCommand):
    help = 'Create Recognized Sales using excel sheet'

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
            sheet_name = "인정매출(회사차량)"
        create_recognized_sales(file_name, sheet_name)
        recognized_sales_count = RecognizedSales.objects.all().count()
        print(f"{recognized_sales_count} Recognized Sales Created")
