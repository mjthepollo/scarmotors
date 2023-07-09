from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models

from core.models import TimeStampedModel
from core.utility import print_colored
from demand.sales_models import ExtraSales, Order, RecognizedSales
from demand.utility import print_fields


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

    paid_insurance_sales = models.IntegerField(
        default=0, verbose_name="[입금]보험")
    paid_general_expense = models.IntegerField(
        default=0, verbose_name="[입금]일반경정비")
    paid_general_pando = models.IntegerField(
        default=0, verbose_name="[입금]일반판도")
    paid_general_rent = models.IntegerField(
        default=0, verbose_name="[입금]렌트일반")
    paid_rent_pando = models.IntegerField(
        default=0, verbose_name="[입금]렌트판도")

    not_paid_insurance_sales = models.IntegerField(
        default=0, verbose_name="[미입금]보험")
    not_paid_general_expense = models.IntegerField(
        default=0, verbose_name="[미입금]일반경정비")
    not_paid_general_pando = models.IntegerField(
        default=0, verbose_name="[미입금]일반판도")
    not_paid_general_rent = models.IntegerField(
        default=0, verbose_name="[미입금]렌트일반")
    not_paid_rent_pando = models.IntegerField(
        default=0, verbose_name="[미입금]렌트판도")
    not_paid_recognized_sales = models.IntegerField(
        default=0, verbose_name="[미입금]인정매출")

    wage_turnover = models.IntegerField(default=0, verbose_name="공임매출")
    component_turnover = models.IntegerField(default=0, verbose_name="부품매출")
    charge_amount = models.IntegerField(default=0, verbose_name="청구금")
    deposit_amount = models.IntegerField(default=0, verbose_name="입금액")
    # Order의 get_net_payment에서 1.1을 나눠준 값이다.
    net_payment_amount = models.IntegerField(default=0, verbose_name="면책금")

    def get_kwargs(orders, all_extra_sales, all_recognized_sales):
        paid_insurance_sales = 0
        paid_general_expense = 0
        paid_general_pando = 0
        paid_general_rent = 0
        paid_rent_pando = 0
        not_paid_insurance_sales = 0
        not_paid_general_expense = 0
        not_paid_general_pando = 0
        not_paid_general_rent = 0
        not_paid_rent_pando = 0
        not_paid_recognized_sales = 0
        wage_turnover = 0
        component_turnover = 0
        charge_amount = 0
        deposit_amount = 0
        attemted_amount = 0
        net_payment_sales = 0

        for order in orders:
            if order.charge_type == "보험":
                paid_insurance_sales += order.get_paid_turnover()
                not_paid_insurance_sales += order.get_not_paid_turnover()
            elif order.charge_type == "일반경정비":
                paid_general_expense += order.get_paid_turnover()
                not_paid_general_expense += order.get_not_paid_turnover()
            elif order.charge_type == "일반판도":
                paid_general_pando += order.get_paid_turnover()
                not_paid_general_pando += order.get_not_paid_turnover()
            elif order.charge_type == "렌트일반":
                paid_general_rent += order.get_paid_turnover()
                not_paid_general_rent += order.get_not_paid_turnover()
            elif order.charge_type == "렌트판도":
                paid_rent_pando += order.get_paid_turnover()
                not_paid_rent_pando += order.get_not_paid_turnover()
            else:
                print_colored("잘못된 Charge Type입니다.", "magenta")
                print_fields(order)
            wage_turnover += order.get_wage_turnover()
            component_turnover += order.get_component_turnover()
            charge_amount += order.get_charge_amount()
            deposit_amount += order.get_deposit_amount()
            attemted_amount += order.get_attemted_amount()
            net_payment_sales += order.get_net_payment_sales()

        for extra_sales in all_extra_sales:
            paid_general_expense += extra_sales.get_paid_turnover()
            not_paid_general_expense += extra_sales.get_not_paid_turnover()
            wage_turnover += extra_sales.get_wage_turnover()
            component_turnover += extra_sales.get_component_turnover()
            charge_amount += extra_sales.get_charge_amount()
            deposit_amount += extra_sales.get_deposit_amount()
            attemted_amount += extra_sales.get_attemted_amount()
            net_payment_sales += extra_sales.get_net_payment_sales()

        for recognized_sales in all_recognized_sales:
            not_paid_recognized_sales += recognized_sales.get_not_paid_turnover()

        return {
            "paid_insurance_sales": paid_insurance_sales,
            "paid_general_expense": paid_general_expense,
            "paid_general_pando": paid_general_pando,
            "paid_general_rent": paid_general_rent,
            "paid_rent_pando": paid_rent_pando,
            "not_paid_insurance_sales": not_paid_insurance_sales,
            "not_paid_general_expense": not_paid_general_expense,
            "not_paid_general_pando": not_paid_general_pando,
            "not_paid_general_rent": not_paid_general_rent,
            "not_paid_rent_pando": not_paid_rent_pando,
            "not_paid_recognized_sales": not_paid_recognized_sales,
            "wage_turnover": wage_turnover,
            "component_turnover": component_turnover,
            "charge_amount": charge_amount,
            "deposit_amount": deposit_amount,
            "attempted_amount": attemted_amount,
            "net_payment_sales": net_payment_sales,
        }

    @property
    def whole_turnover(self):
        return self.paid_general_expense +\
            self.paid_general_pando +\
            self.paid_general_rent +\
            self.paid_insurance_sales +\
            self.paid_rent_pando +\
            self.not_paid_general_expense +\
            self.not_paid_general_pando +\
            self.not_paid_general_rent +\
            self.not_paid_insurance_sales +\
            self.not_paid_rent_pando

    @classmethod
    def create(cls, start_date, end_date):
        exist_sales = cls.objects.filter(
            start_date=start_date, end_date=end_date).first()
        if exist_sales:
            return exist_sales
        orders = Order.objects.filter(
            charge__charge_date__range=(start_date, end_date))
        all_extra_sales = ExtraSales.objects.filter(
            charge__charge_date__range=(start_date, end_date))
        all_recognized_sales = RecognizedSales.objects.filter(
            real_day_came_out__range=(start_date, end_date)
        )
        kwargs = cls.get_kwargs(orders, all_extra_sales, all_recognized_sales)
        kwargs["start_date"] = start_date
        kwargs["end_date"] = end_date
        return cls.objects.create(**kwargs)

    def update(self):
        orders = Order.objects.filter(
            charge__charge_date__range=(self.start_date, self.end_date))
        kwargs = self.get_kwargs(orders)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()


class MonthlySales(PeriodSales):
    """
    Monthly Sales는 한 달 동안의 매출 정보를 저장하는 Model이다.
    이는 Summary에서 보여지며, Sales의 updated 정보를 기반으로 업데이트 된다.
    """

    @property
    def month(self):
        return self.start_date.month

    @classmethod
    def create_monthly_sales(cls, year, month):
        start_date = date(year, month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        return cls.create(start_date, end_date)

    def __str__(self):
        return f"[{self.start_date.year}년{self.start_date.month}월] 매출"


class StatisticSales(PeriodSales):
    """
    Statistic Sales는 일정 기간 동안의 매출 정보를 저장하는 Model이다.
    이는 순간적으로 활용되며, 순간적인 활용 이후에는 바로 삭제된다.
    """

    def __str__(self):
        return f"[{self.start_date}~{self.end_date}] 매출"
