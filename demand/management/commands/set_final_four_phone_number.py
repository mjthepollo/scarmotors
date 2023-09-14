
import logging
# Create a logger with a custom log level
from datetime import datetime

from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.sales_models import Register


class Command(BaseCommand):
    help = 'Set final four phone number for existed registers'

    def handle(self, *args, **options):
        count = 0
        for register in Register.objects.all().order_by("pk"):
            before_final_four_phone_number = register.final_four_phone_number
            register.save()
            after_final_four_phone_number = register.final_four_phone_number
            if before_final_four_phone_number != after_final_four_phone_number:
                count += 1

        print_colored(
            f"Now {count} Register have final four phone number!", "green")
