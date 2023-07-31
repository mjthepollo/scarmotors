from django.core.management import call_command
from django.core.management.base import BaseCommand

from core.utility import print_colored


class Command(BaseCommand):
    help = 'REMOVE ALL MODELS AND CREATE INITAL MODELS USING "data load.xlsx" EXCEL SHEET'

    def handle(self, *args, **options):
        file_name = "src/data_load.xlsx"
        not_charged_sheet_name = "22년 12월 미청구"
        first_half_sheet_name = "23년 본사 상반기"
        second_half_sheet_name = "23년 본사 하반기"
        recognized_sales_sheet_name = "인정매출(회사차량)"

        print_colored("\n-----CLEANING ALL MODELDS!------", "magenta")
        call_command('clean_models')
        print_colored("-----CLEANING ALL MODELDS FINISHED!-----", "magenta")
        print_colored("\n-----CLEANING ALL MONTHLY SALES!------", "magenta")
        call_command('clean_monthly_sales')
        print_colored(
            "-----CLEANING ALL MONTHLY SALES FINISHED!-----", "magenta")

        print_colored("\n-----CREATING NOT CHARGED SALES!-----", "magenta")
        call_command(
            'create_initial_model', f'--file_name={file_name}', f'--sheet_name={not_charged_sheet_name}')
        print_colored("----- NOT CHARGED SALES!-----", "magenta")
        print_colored("\n-----CREATING FIRST HALF SALES!-----", "magenta")
        call_command(
            'create_initial_model', f'--file_name={file_name}', f'--sheet_name={first_half_sheet_name}')
        print_colored("----- FIRST HALF SALES!-----", "magenta")
        print_colored("\n-----CREATING SECONF HALF SALES!-----", "magenta")
        call_command(
            'create_initial_model', f'--file_name={file_name}', f'--sheet_name={second_half_sheet_name}')
        print_colored("----- SECONF HALF SALES!-----", "magenta")
        print_colored("\n-----CREATING RECOGNIZED SALES!-----", "magenta")
        call_command(
            'create_recognized_sales', f'--file_name={file_name}', f'--sheet_name={recognized_sales_sheet_name}')
        print_colored("----- RECOGNIZED SALES!-----", "magenta")
        print_colored("\n-----CREATE MONTHLY SALES!------", "magenta")
        call_command('create_initial_monthly_sales')
        print_colored("-----CREATE MONTHLY SALES FINISHED!-----", "magenta")
        call_command('set_incentive_date')
        print_colored("-----SET INCENTIVE DATE FINISHED!-----", "magenta")

        print_colored("\n!!!!!!!!!!!!!!INITALIZATION FINISH!!!!!!!!!", "cyan")
