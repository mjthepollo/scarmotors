from django.core.management.base import BaseCommand

from demand.models import (Charge, ChargedCompany, Insurance, InsuranceAgent,
                           Order, Payment, Supporter)


class Command(BaseCommand):
    help = 'Load exsiting datas from excel file with sheet name and file name'

    def handle(self, *args, **options):
        for supporter in Supporter.objects.all():
            supporter.delete()
        for charged_company in ChargedCompany.objects.all():
            charged_company.delete()
        for insurance_agent in InsuranceAgent.objects.all():
            insurance_agent.delete()
        for payment in Payment.objects.all():
            payment.delete()
        for charge in Charge.objects.all():
            charge.delete()
        for insurance in Insurance.objects.all():
            insurance.delete()
        for order in Order.objects.all():
            order.delete()
        print("All models deleted")
