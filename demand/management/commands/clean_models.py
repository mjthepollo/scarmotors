import logging

from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, RequestDepartment, Supporter)
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register

# Create a logger with a custom log level


class Command(BaseCommand):
    help = 'clean models by 입출고대장'

    def handle(self, *args, **options):
        supporter_count = Supporter.objects.all().count()
        Supporter.objects.all().delete()
        print_colored(f"Supporter Delete Count: {supporter_count}", "green")
        charget_company_count = ChargedCompany.objects.all().count()
        ChargedCompany.objects.all().delete()
        print_colored(
            f"ChargedCompany Delete Count: {charget_company_count}", "green")
        insurance_agent_count = InsuranceAgent.objects.all().count()
        InsuranceAgent.objects.all().delete()
        print_colored(
            f"InsuranceAgent Delete Count: {insurance_agent_count}", "green")

        payment_count = Payment.objects.all().count()
        Payment.objects.all().delete()
        print_colored(f"Payment Delete Count: {payment_count}", "green")
        charge_count = Charge.objects.all().count()
        Charge.objects.all().delete()
        print_colored(f"Charge Delete Count: {charge_count}", "green")
        deposit_count = Deposit.objects.all().count()
        Deposit.objects.all().delete()
        print_colored(f"Deposit Delete Count: {deposit_count}", "green")

        request_department_count = RequestDepartment.objects.all().count()
        RequestDepartment.objects.all().delete()
        print_colored(
            f"RequestDepartment Delete Count: {request_department_count}", "green")

        order_count = Order.objects.all().count()
        Order.objects.all().delete()
        print_colored(f"Order Delete Count: {order_count}", "green")

        register_count = Register.objects.all().count()
        Register.objects.all().delete()
        print_colored(f"Register Delete Count: {register_count}", "green")

        extra_sales_count = ExtraSales.objects.all().count()
        ExtraSales.objects.all().delete()
        print_colored(f"ExtraSales Delete Count: {extra_sales_count}", "green")

        RecognizedSales.objects.all().delete()
        recognized_sales_count = RecognizedSales.objects.all().count()
        print_colored(
            f"RecognizedSales Delete Count: {recognized_sales_count}", "green")

        print_colored("All models deleted", "blue")
