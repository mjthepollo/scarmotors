from datetime import datetime

from django.db import models

from core.models import TimeStampedModel

# Create your models here.


class Supporter(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="지원 업체명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class ChargedCompany(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="담당 업체명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class InsuranceAgent(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="보험 담당자명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class Payment(TimeStampedModel):
    indemnity_amount = models.IntegerField(
        blank=True, null=True, verbose_name="면책금")
    discount_amount = models.IntegerField(
        blank=True, null=True, verbose_name="할인금")
    payment_type = models.CharField(blank=True, null=True, max_length=30, choices=(
        ("카드", "카드"), ("현금", "현금"), ("은행", "은행")), verbose_name="결제형태")
    payment_info = models.CharField(
        blank=True, null=True, max_length=60, verbose_name="카드/은행")
    payment_date = models.DateField(blank=True, null=True, verbose_name="결제일")
    refund_amount = models.IntegerField(
        blank=True, null=True, verbose_name="환불액")
    refund_date = models.DateField(blank=True, null=True, verbose_name="환불일")

    def __str__(self):
        if hasattr(self, "insurance"):
            insurance = self.insurance
            if insurance.order != None:
                return f"{insurance.order.RO_number} 결제"
            else:
                return f"주문없음({self.pk}_보험:{insurance.pk})"
        return f"보험없음({self.pk})"


class Charge(TimeStampedModel):
    charge_date = models.DateField(verbose_name="청구일")
    repair_amount = models.IntegerField(default=0, verbose_name="공임비")
    component_amount = models.IntegerField(default=0, verbose_name="부품비")
    indemnity_amount = models.IntegerField(default=0, verbose_name="면책금")

    def get_charge_amount(self):
        return int((self.repair_amount + self.component_amount)*1.1) - self.indemnity_amount

    def __str__(self):
        if hasattr(self, "insurance"):
            insurance = self.insurance
            if insurance.order != None:
                return f"{insurance.order.RO_number} 청구"
            else:
                return f"주문없음({self.pk}_보험:{insurance.pk})"
        else:
            return f"보험없음({self.pk})"


class Deposit(TimeStampedModel):
    deposit_amount = models.IntegerField(verbose_name="입금액")
    deposit_date = models.DateField(verbose_name="입금일")

    def get_payment_rate(self):
        return round(self.deposit_amount/self.insurance.charge.get_charge_amount()*100)

    def __str__(self):
        if hasattr(self, "insurance"):
            insurance = self.insurance
            if insurance.order != None:
                return f"{insurance.order.RO_number} 입금"
            else:
                return f"주문없음({self.pk}_보험:{insurance.pk})"
        else:
            return f"보험없음({self.pk})"


class Order(TimeStampedModel):
    RO_number = models.CharField(verbose_name="RO번호", max_length=10)
    car_number = models.CharField(verbose_name="차량번호", max_length=20)
    day_came_in = models.DateField(verbose_name="입고일")
    expected_day_came_out = models.DateField(verbose_name="출고예정일")
    # 나중에 출고시에 추가함
    real_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="실제출고일")
    car_model = models.CharField(max_length=90, verbose_name="차종")
    abroad_type = models.CharField(
        choices=(("domestic", "국산"), ("imported", "수입")), max_length=10, verbose_name="국산/수입")
    number_of_repair_works = models.IntegerField(
        default=0, verbose_name="보수 작업판수")
    number_of_exchange_works = models.IntegerField(
        default=0, verbose_name="교환 작업판수")
    supporter = models.ForeignKey(
        Supporter, verbose_name="입고지원", blank=True, null=True, on_delete=models.SET_NULL, related_name="orders")
    client_name = models.CharField(verbose_name="고객명", max_length=30)
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="orders", null=True, on_delete=models.SET_NULL, verbose_name="보험 담당자")
    rentcar_company_name = models.CharField(
        blank=True, null=True, max_length=100, verbose_name="렌트 업체명")
    rentcar_company_note = models.CharField(
        blank=True, null=True, max_length=300, verbose_name="메모")
    phone_number = models.CharField(verbose_name="전화번호", max_length=15)

    def get_number_of_works(self):
        return self.number_of_exchange_works + self.number_of_repair_works

    @classmethod
    def get_RO_number(cls):
        current_month = datetime.now().month
        current_number = cls.objects.filter(
            created__month=current_month).count()
        return f"{current_month}-{current_number}"

    def set_RO_number(self):
        self.RO_number = Order.get_RO_number()
        self.save()

    def __str__(self):
        return f"{self.car_number}/{self.phone_number}"


class Insurance(TimeStampedModel):
    order = models.ForeignKey(
        Order, null=True, on_delete=models.CASCADE, verbose_name="주문", related_name="insurances")
    charged_company = models.ForeignKey(
        ChargedCompany, related_name="orders", verbose_name="담당 업체명", on_delete=models.CASCADE)
    insurance_type = models.CharField(choices=(
        ("자차", "자차"), ("대물", "대물"), ("일반", "일반")), max_length=10, verbose_name="차/대/일")
    charge_type = models.CharField(choices=(("보험", "보험"), ("일반경정", "일반경정"), (
        "일반판도", "일반판도"), ("렌트판도", "렌트판도"), ("렌트일반", "렌트일반"),
        ("인정매출", "인정매출")), max_length=20, verbose_name="구분")
    receipt_number = models.CharField(
        max_length=20, verbose_name="접수번호", unique=True)
    fault_ratio = models.IntegerField(verbose_name="과실분")

    payment = models.OneToOneField(
        Payment, null=True, blank=True, related_name="insurance", verbose_name="결제", on_delete=models.CASCADE)
    charge = models.OneToOneField(
        Charge, null=True, blank=True, related_name="insurance", verbose_name="청구", on_delete=models.CASCADE)
    deposit = models.OneToOneField(
        Deposit, null=True, blank=True, related_name="insurance", verbose_name="입금", on_delete=models.CASCADE)

    note = models.TextField(blank=True, null=True, verbose_name="비고")

    def __str__(self):
        return f"{self.order.RO_number} {self.insurance_type} {self.charge_type}"
