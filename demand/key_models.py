from datetime import date

from django.db import models

from core.models import TimeStampedModel
from demand.excel_line_info import *


class Supporter(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "입고 지원 업체"
        verbose_name_plural = "입고 지원 업체(들)"
    name = models.CharField(max_length=100, verbose_name="지원 업체명")
    active = models.BooleanField(default=True, verbose_name="활성화")
    incentive_rate_percent = models.IntegerField(
        default=15, verbose_name="지급율(%)")

    def __str__(self):
        return self.name


class ChargedCompany(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "보험회사"
        verbose_name_plural = "보험회사(들)"
    name = models.CharField(max_length=100, verbose_name="보험(렌트)")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class InsuranceAgent(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "보험 담당자"
        verbose_name_plural = "보험 담당자(들)"
    name = models.CharField(max_length=100, verbose_name="보험 담당자명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class Payment(TimeStampedModel):
    """
    Payment 객체. 보통 출고시 기록한다.
    만약 수정한다면 EditOrderForm은 직접 수정해줘야 한다.
    """
    class Meta:
        ordering = ["-created",]
        verbose_name = "면책금 정보"
        verbose_name_plural = "면책금 정보(들)"
    indemnity_amount = models.IntegerField(
        blank=True, null=True, verbose_name="면책금")
    discount_amount = models.IntegerField(
        blank=True, null=True, verbose_name="할인금")
    refund_amount = models.IntegerField(
        blank=True, null=True, verbose_name="환불액")
    payment_type = models.CharField(blank=True, null=True, max_length=30, choices=(
        ("카드", "카드"), ("현금", "현금"), ("은행", "은행")), verbose_name="결제형태")
    payment_info = models.CharField(
        blank=True, null=True, max_length=60, verbose_name="은행사/카드사")
    payment_date = models.DateField(blank=True, null=True, verbose_name="결제일")
    refund_date = models.DateField(blank=True, null=True, verbose_name="환불일")

    @classmethod
    def create_mockup(cls):
        return cls.objects.create()

    def is_mockup(self):
        result = True
        result = result and self.indemnity_amount == None
        result = result and self.discount_amount == None
        result = result and self.refund_amount == None
        result = result and self.payment_type == None
        result = result and self.payment_info == None
        result = result and self.payment_date == None
        result = result and self.refund_date == None
        return result

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                order_index = list(order.register.orders.all()).index(order)
                return f"RO({order.register.RO_number}) 주문[{order_index}] 결제"
            else:
                return f"등록없음({self.pk}_주문:{order.pk})"
        else:
            if hasattr(self, "extra_sales"):
                return f"기타매출({self.extra_sales.pk}) 결제"
            else:
                return f"주문없음({self.pk})"


class Charge(TimeStampedModel):
    """
    Charge 객체. 청구시 사용한다.
    만약 수정한다면 EditOrderForm은 직접 수정해줘야 한다.
    """
    class Meta:
        ordering = ["-created",]
        verbose_name = "청구 정보"
        verbose_name_plural = "청구 정보(들)"
    charge_date = models.DateField(verbose_name="청구일", blank=True, null=True)
    wage_amount = models.IntegerField(default=0, verbose_name="공임비")
    component_amount = models.IntegerField(default=0, verbose_name="부품비")

    def get_indemnity_amount(self):
        if hasattr(self, "order"):
            return self.order.get_indemnity_amount()
        elif hasattr(self, "extra_sales"):
            return self.extra_sales.get_indemnity_amount()
        else:
            raise Exception("Charge에 order나 extra_sales가 없습니다.")

    def get_repair_amount(self):
        return self.wage_amount+self.component_amount

    def get_charge_amount(self):
        if hasattr(self, "order"):
            sales = self.order
            refund_amount = self.order.payment.refund_amount if self.order.payment else 0
            refund_amount = refund_amount if refund_amount else 0
        elif hasattr(self, "extra_sales"):
            sales = self.extra_sales
            refund_amount = self.extra_sales.payment.refund_amount if self.extra_sales.payment else 0
        if not sales:
            raise Exception("Charge에 order나 extra_sales가 없습니다.")
        refund_amount = refund_amount if refund_amount else 0
        charge_amount = sales.get_chargable_amount() - self.get_indemnity_amount() + \
            refund_amount
        if charge_amount > 0:
            return charge_amount
        else:
            return 0

    @classmethod
    def create_mockup(cls):
        return cls.objects.create()

    def is_mockup(self):
        result = True
        result = result and self.charge_date == None
        result = result and self.wage_amount == 0
        result = result and self.component_amount == 0
        return result

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                order_index = list(order.register.orders.all()).index(order)
                return f"RO({order.register.RO_number}) 주문[{order_index}] 청구"
            else:
                return f"등록없음({self.pk}_주문:{order.pk})"
        else:
            if hasattr(self, "extra_sales"):
                return f"기타매출({self.extra_sales.pk}) 청구"
            else:
                return f"주문없음({self.pk})"


class Deposit(TimeStampedModel):
    """
    입금 정보. 수정 시 EditOrderForm은 직접 수정해줘야 한다.
    """
    class Meta:
        ordering = ["-created",]
        verbose_name = "입금 정보"
        verbose_name_plural = "입금 정보(들)"
    deposit_amount = models.IntegerField(verbose_name="입금액")
    deposit_date = models.DateField(verbose_name="입금일")
    mockup = models.BooleanField(default=False, verbose_name="모형")

    @classmethod
    def create_mockup(cls):
        return cls.objects.create(deposit_amount=0, deposit_date=date.today(), mockup=True)

    def is_mockup(self):
        return self.mockup

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                order_index = list(order.register.orders.all()).index(order)
                return f"RO({order.register.RO_number}) 주문[{order_index}] 입금"
            else:
                return f"등록없음({self.pk}_주문:{order.pk})"
        else:
            if hasattr(self, "extra_sales"):
                return f"기타매출({self.extra_sales.pk}) 입금"
            else:
                return f"주문없음({self.pk})"


class RequestDepartment(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "요청부서"
        verbose_name_plural = "요청부서(들)"
    name = models.CharField(max_length=30, verbose_name="요청부서명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name
