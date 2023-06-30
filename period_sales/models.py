from django.db import models

from core.models import TimeStampedModel
from demand.sales_models import ExtraSales, Order, Register


class SalesInfo(TimeStampedModel):
    """
    SalesInfo는 Sales의 OneToOne Field가 되는 모델이다.
    PaidTurnoverSalesInfo와 NotPaidTurnoverSalesInfo가 존재한다.
    모두 charge_type에 따른 프로퍼티들을 가진다. 따라서 charge_type의 수정은 이 모델의 수정을 필요로 한다.
    """
    class Meta:
        ordering = ["-created"]
        abstract = True

    insurance_sales = models.IntegerField(default=0, verbose_name="보험")
    general_expense = models.IntegerField(default=0, verbose_name="일반경정비")
    general_pando = models.IntegerField(default=0, verbose_name="일반판도")
    general_rent = models.IntegerField(default=0, verbose_name="렌트일반")
    rent_pando = models.IntegerField(default=0, verbose_name="렌트판도")

    def get_total(self):
        return self.insurance_sales + self.general_expense + self.general_pando + self.general_rent + self.rent_pando

    def set_info(self, start_date, end_date):
        raise NotImplementedError


class PaidTurnoverSalesInfo(SalesInfo):
    """
    PaidTurnoverSalesInfo는 입금매출로 SalesInfo를 지정한다.
    """

    def set_info(self, start_date, end_date):
        orders = Order.objects.filter(
            charge__charge_date__range=(start_date, end_date))
        insurance_sales = 0
        general_expense = 0
        general_pando = 0
        general_rent = 0
        rent_pando = 0
        for order in orders:
            if order.charge_type == "보함":
                insurance_sales += order.get_paid_turnover()
            elif order.charge_type == "일반경정비":
                general_expense += order.get_paid_turnover()
            elif order.charge_type == "일반판도":
                general_pando += order.get_paid_turnover()
            elif order.charge_type == "렌트일반":
                general_rent += order.get_paid_turnover()
            elif order.charge_type == "렌트판도":
                rent_pando += order.get_paid_turnover()
            else:
                raise ValueError("잘못된 Charge Type입니다.")
        self.insurance_sales = insurance_sales
        self.general_expense = general_expense
        self.general_pando = general_pando
        self.general_rent = general_rent
        self.rent_pando = rent_pando
        self.save()


class NotPaidTurnoverSalesInfo(SalesInfo):
    """
    NotPaidTurnoverSalesInfo는 미입금매출로 SalesInfo를 지정한다.
    """

    def set_info(self, start_date, end_date):
        orders = Order.objects.filter(
            charge__charge_date__range=(start_date, end_date))
        insurance_sales = 0
        general_expense = 0
        general_pando = 0
        general_rent = 0
        rent_pando = 0
        for order in orders:
            if order.charge_type == "보함":
                insurance_sales += order.get_not_paid_turnover()
            elif order.charge_type == "일반경정비":
                general_expense += order.get_not_paid_turnover()
            elif order.charge_type == "일반판도":
                general_pando += order.get_not_paid_turnover()
            elif order.charge_type == "렌트일반":
                general_rent += order.get_not_paid_turnover()
            elif order.charge_type == "렌트판도":
                rent_pando += order.get_not_paid_turnover()
            else:
                raise ValueError("잘못된 Charge Type입니다.")
        self.insurance_sales = insurance_sales
        self.general_expense = general_expense
        self.general_pando = general_pando
        self.general_rent = general_rent
        self.rent_pando = rent_pando
        self.save()


class PeriodSales(TimeStampedModel):
    """
    Period Sales는 일정기간동안 매출 정보를 저장하는 Abstract Model이다.
    Sales 모델들의 updated 정보를 기반으로 업데이트 하며, 자식 클래스로는 MonthlySales와 StatisticSales가 있다.
    """
    class Meta:
        ordering = ["-created"]
        abstract = True
    start_date = models.DateField(verbose_name="시작 날짜")
    end_date = models.DateField(verbose_name="마지막 날짜")

    paid_turnover_info = models.OneToOneField(
        PaidTurnoverSalesInfo, null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name="입금매출")
    not_paid_turnover_info = models.OneToOneField(
        NotPaidTurnoverSalesInfo, null=True, blank=True,
        on_delete=models.SET_NULL, verbose_name="미입금매출")

    wage_turnover = models.IntegerField(default=0, verbose_name="공임매출")
    component_turnover = models.IntegerField(default=0, verbose_name="부품매출")
    charge_amount = models.IntegerField(default=0, verbose_name="청구금")
    deposit_amount = models.IntegerField(default=0, verbose_name="입금액")
    # Order의 get_net_payment에서 1.1을 나눠준 값이다.
    net_payment_amount = models.IntegerField(default=0, verbose_name="면책금")

    def set_info(self, start_date, end_date):
        raise NotImplementedError


class MonthlySales(PeriodSales):
    """
    Monthly Sales는 한 달 동안의 매출 정보를 저장하는 Model이다.
    이는 Summary에서 보여지며, Sales의 updated 정보를 기반으로 업데이트 된다.
    """

    def set_info(self, start_date, end_date):
        pass


class StatisticSales(PeriodSales):
    """
    Statistic Sales는 일정 기간 동안의 매출 정보를 저장하는 Model이다.
    이는 순간적으로 활용되며, 순간적인 활용 이후에는 바로 삭제된다.
    """

    def set_info(self, start_date, end_date):
        pass
