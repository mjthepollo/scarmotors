from django.core.management.base import BaseCommand

from demand.models import (Charge, ChargedCompany, Deposit, Insurance,
                           InsuranceAgent, Order, Payment, Supporter)


class Command(BaseCommand):
    help = 'create initial models by 입출고대장'

    def handle(self, *args, **options):
        pass
