from datetime import date

from django.db import models

from core.models import TimeStampedModel
from demand.excel_line_info import *


class Supporter(TimeStampedModel):
    class Meta:
        ordering = ["name",]
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
        ordering = ["name",]
        verbose_name = "보험회사"
        verbose_name_plural = "보험회사(들)"
    name = models.CharField(max_length=100, verbose_name="보험(렌트)")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class InsuranceAgent(TimeStampedModel):
    class Meta:
        ordering = ["name",]
        verbose_name = "보험 담당자"
        verbose_name_plural = "보험 담당자(들)"
    name = models.CharField(max_length=100, verbose_name="보험 담당자명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class KeyModel(TimeStampedModel):
    """
    KeyModel은 Sales의 OneToOne Field가 되는 모델들이다.
    Payment, Charge, Deposit이 존재한다.
    """
    class Meta:
        ordering = ["-created"]
        abstract = True

    def is_stable(self):
        raise NotImplementedError

    def is_default(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        """
        for the status consistency save method of order must be called
        """
        if hasattr(self, "order"):
            self.order.save()
        super().save(*args, **kwargs)


class Payment(KeyModel):
    """
    Payment 객체. 보통 출고시 기록한다.
    """
    class Meta:
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

    def is_default(self):
        return self.indemnity_amount == None and self.discount_amount == None and\
            self.refund_amount == None and\
            self.payment_type == None and self.payment_info == None and\
            self.payment_date == None and self.refund_date == None

    def is_stable(self):
        return bool(self.payment_date)

    def get_settlement_amount(self):
        indemnity_amount = self.indemnity_amount if self.indemnity_amount else 0
        discount_amount = self.discount_amount if self.discount_amount else 0
        return indemnity_amount - discount_amount

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                return f"RO({order.register.RO_number}) 주문[{order.order_index}] 결제"
            else:
                return f"등록없음({self.pk}_주문:{order.pk})"
        else:
            if hasattr(self, "extra_sales"):
                return f"기타매출({self.extra_sales.pk}) 결제"
            else:
                return f"주문없음({self.pk})"


class Charge(KeyModel):
    """
    Charge 객체. 청구시 사용한다.
    """
    class Meta:
        verbose_name = "청구 정보"
        verbose_name_plural = "청구 정보(들)"
    charge_date = models.DateField(verbose_name="청구일", blank=True, null=True)
    wage_amount = models.IntegerField(
        default=0, verbose_name="공임비", blank=True, null=True)
    component_amount = models.IntegerField(
        default=0, verbose_name="부품비", blank=True, null=True)

    def get_repair_amount(self):
        return self.wage_amount+self.component_amount

    def is_default(self):
        return self.charge_date == None and\
            (self.wage_amount == 0 or self.wage_amount == None) and\
            (self.component_amount == 0 or self.component_amount == None)

    def is_stable(self):
        return bool(self.charge_date)

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                return f"RO({order.register.RO_number}) 주문[{order.order_index}] 청구"
            else:
                return f"등록없음({self.pk}_주문:{order.pk})"
        else:
            if hasattr(self, "extra_sales"):
                return f"기타매출({self.extra_sales.pk}) 청구"
            else:
                return f"주문없음({self.pk})"


class Deposit(KeyModel):
    """
    입금 정보
    """
    class Meta:
        verbose_name = "입금 정보"
        verbose_name_plural = "입금 정보(들)"
    deposit_amount = models.IntegerField(
        verbose_name="입금액", blank=True, null=True)
    deposit_date = models.DateField(verbose_name="입금일", blank=True, null=True)
    deposit_note = models.TextField(
        verbose_name="입금 정보", blank=True, null=True)

    def is_default(self):
        return self.deposit_amount == None and self.deposit_date == None and\
            (self.deposit_note == None or self.deposit_note == "")

    def is_stable(self):
        return self.deposit_amount and self.deposit_date

    def __str__(self):
        if hasattr(self, "order"):
            order = self.order
            if order.register != None:
                return f"RO({order.register.RO_number}) 주문[{order.order_index}] 입금"
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
