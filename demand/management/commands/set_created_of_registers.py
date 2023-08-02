
import logging
# Create a logger with a custom log level
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from core.utility import print_colored
from demand.sales_models import Register


class Command(BaseCommand):
    help = 'clean models by 입출고대장'

    def handle(self, *args, **options):

        count = 0
        for register in Register.objects.all().order_by("pk"):
            created = datetime.combine(
                register.day_came_in, datetime.now().time())
            register.created = make_aware(created)
            register.save()
            count += 1

        print_colored(
            f"Register Set Craeted To Day Came IN FINISHED: {count} Registers", "green")
