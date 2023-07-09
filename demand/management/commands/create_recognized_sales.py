from django.core.management.base import BaseCommand

from demand.sales_models import RecognizedSales


def load_data_for_recognized_sales(file_name, sheet_name):
    """
    엑셀 파일을 불러와 DataFrame으로 변환한다.
    """
    df = pd.read_excel(
        file_name, sheet_name=sheet_name, engine="openpyxl", header=HEADER
    )
    return df


class Command(BaseCommand):
    help = 'Create Recognized Sales using excel sheet'

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
        for deposit in Deposit.objects.all():
            insurance.delete()
        for order in Order.objects.all():
            order.delete()
        print("All models deleted")
