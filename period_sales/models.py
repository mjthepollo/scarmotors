from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models

from core.models import TimeStampedModel
from core.utility import print_colored
from demand.key_models import ChargedCompany
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register
from demand.utility import print_fields


class PeriodSales(TimeStampedModel):
    """
    Period Sales는 일정기간동안 매출 정보를 저장하는 Abstract Model이다.
    Sales 모델들의 updated 정보를 기반으로 업데이트 하며, 자식 클래스로는 MonthlySales와 StatisticSales가 있다.
    """
    class Meta:
        ordering = ["created"]
        abstract = True
    start_date = models.DateField(verbose_name="시작 날짜")
    end_date = models.DateField(verbose_name="마지막 날짜")

    paid_insurance_sales = models.IntegerField(
        default=0, verbose_name="[입금]보험")
    paid_general_rent = models.IntegerField(
        default=0, verbose_name="[입금]렌트일반")
    paid_rent_pando = models.IntegerField(
        default=0, verbose_name="[입금]렌트판도")
    paid_general_pando = models.IntegerField(
        default=0, verbose_name="[입금]일반판도")
    paid_general_expense = models.IntegerField(
        default=0, verbose_name="[입금]일반경정비")

    not_paid_insurance_sales = models.IntegerField(
        default=0, verbose_name="[미입금]보험")
    not_paid_general_rent = models.IntegerField(
        default=0, verbose_name="[미입금]렌트일반")
    not_paid_rent_pando = models.IntegerField(
        default=0, verbose_name="[미입금]렌트판도")
    not_paid_general_pando = models.IntegerField(
        default=0, verbose_name="[미입금]일반판도")
    not_paid_general_expense = models.IntegerField(
        default=0, verbose_name="[미입금]일반경정비")
    not_paid_recognized_sales = models.IntegerField(
        default=0, verbose_name="[미입금]인정매출")

    wage_turnover = models.IntegerField(default=0, verbose_name="공임매출")
    component_turnover = models.IntegerField(default=0, verbose_name="부품매출")

    number_of_domestic_samsung_insurances = models.IntegerField(
        default=0, verbose_name="삼성보험(국산)")
    number_of_domestic_dongbu_insurances = models.IntegerField(
        default=0, verbose_name="동부보험(국산)")
    number_of_domestic_meritz_insurances = models.IntegerField(
        default=0, verbose_name="메리츠보험(국산)")
    number_of_domestic_etc_insurances = models.IntegerField(
        default=0, verbose_name="기타보험(국산)")
    number_of_domestic_rent = models.IntegerField(
        default=0, verbose_name="렌트(국산)")

    number_of_abroad_samsung_insurances = models.IntegerField(
        default=0, verbose_name="삼성보험(수입)")
    number_of_abroad_dongbu_insurances = models.IntegerField(
        default=0, verbose_name="동부보험(수입)")
    number_of_abroad_meritz_insurances = models.IntegerField(
        default=0, verbose_name="메리츠보험(수입)")
    number_of_abroad_etc_insurances = models.IntegerField(
        default=0, verbose_name="기타보험(수입)")
    number_of_abroad_rent = models.IntegerField(
        default=0, verbose_name="렌트(수입)")

    charge_amount = models.IntegerField(default=0, verbose_name="청구금")
    deposit_amount = models.IntegerField(default=0, verbose_name="입금액")
    attempted_amount = models.IntegerField(default=0, verbose_name="미수금")
    # Order의 get_net_payment에서 1.1을 나눠준 값이다.
    net_payment_sales = models.IntegerField(default=0, verbose_name="면책금")

    @classmethod
    def get_kwargs(cls, orders, all_extra_sales, all_recognized_sales):
        SAMSUNG, _ = ChargedCompany.objects.get_or_create(name="삼성")
        DONGBU, _ = ChargedCompany.objects.get_or_create(name="DB")
        MERITZ, _ = ChargedCompany.objects.get_or_create(name="메리츠")

        paid_insurance_sales = 0
        paid_general_rent = 0
        paid_rent_pando = 0
        paid_general_pando = 0
        paid_general_expense = 0

        not_paid_insurance_sales = 0
        not_paid_general_rent = 0
        not_paid_rent_pando = 0
        not_paid_general_pando = 0
        not_paid_general_expense = 0
        not_paid_recognized_sales = 0

        wage_turnover = 0
        component_turnover = 0

        number_of_domestic_samsung_insurances = 0
        number_of_domestic_dongbu_insurances = 0
        number_of_domestic_meritz_insurances = 0
        number_of_domestic_etc_insurances = 0
        number_of_domestic_rent = 0

        number_of_abroad_samsung_insurances = 0
        number_of_abroad_dongbu_insurances = 0
        number_of_abroad_meritz_insurances = 0
        number_of_abroad_etc_insurances = 0
        number_of_abroad_rent = 0

        charge_amount = 0
        deposit_amount = 0
        attempted_amount = 0  # 미수금
        net_payment_sales = 0  # 면책금 매출

        for order in orders:
            if order.charge_type == "보험":
                paid_insurance_sales += order.get_paid_turnover()
                not_paid_insurance_sales += order.get_not_paid_turnover()
                if order.register.abroad_type == "국산":
                    if order.charged_company == SAMSUNG:
                        number_of_domestic_samsung_insurances += 1
                    elif order.charged_company == DONGBU:
                        number_of_domestic_dongbu_insurances += 1
                    elif order.charged_company == MERITZ:
                        number_of_domestic_meritz_insurances += 1
                    else:
                        number_of_domestic_etc_insurances += 1
                elif order.register.abroad_type == "수입":
                    if order.charged_company == SAMSUNG:
                        number_of_abroad_samsung_insurances += 1
                    elif order.charged_company == DONGBU:
                        number_of_abroad_dongbu_insurances += 1
                    elif order.charged_company == MERITZ:
                        number_of_abroad_meritz_insurances += 1
                    else:
                        number_of_abroad_etc_insurances += 1
                else:
                    raise ValueError("잘못된 Abroad Type입니다. (보험)")
            elif order.charge_type == "렌트일반":
                paid_general_rent += order.get_paid_turnover()
                not_paid_general_rent += order.get_not_paid_turnover()
            elif order.charge_type == "렌트판도":
                paid_rent_pando += order.get_paid_turnover()
                not_paid_rent_pando += order.get_not_paid_turnover()
                if order.register.abroad_type == "국산":
                    number_of_domestic_rent += 1
                elif order.register.abroad_type == "수입":
                    number_of_abroad_rent += 1
                else:
                    raise ValueError("잘못된 Abroad Type입니다. (렌트)")
            elif order.charge_type == "일반판도":
                paid_general_pando += order.get_paid_turnover()
                not_paid_general_pando += order.get_not_paid_turnover()
            elif order.charge_type == "일반경정비":
                paid_general_expense += order.get_paid_turnover()
                not_paid_general_expense += order.get_not_paid_turnover()
            else:
                print_colored("잘못된 Charge Type입니다.", "magenta")
                print_fields(order)
            wage_turnover += order.get_wage_turnover()
            component_turnover += order.get_component_turnover()
            charge_amount += order.get_charge_amount()
            deposit_amount += order.get_deposit_amount()
            attempted_amount += order.get_attempted_amount()
            net_payment_sales += order.get_net_payment_sales()

        for extra_sales in all_extra_sales:
            paid_general_expense += extra_sales.get_paid_turnover()
            not_paid_general_expense += extra_sales.get_not_paid_turnover()
            wage_turnover += extra_sales.get_wage_turnover()
            component_turnover += extra_sales.get_component_turnover()
            charge_amount += extra_sales.get_charge_amount()
            deposit_amount += extra_sales.get_deposit_amount()
            attempted_amount += extra_sales.get_attempted_amount()
            net_payment_sales += extra_sales.get_net_payment_sales()

        for recognized_sales in all_recognized_sales:
            not_paid_recognized_sales += recognized_sales.get_not_paid_turnover()
            wage_turnover += recognized_sales.get_wage_turnover()
            component_turnover += recognized_sales.get_component_turnover()

        return {
            "paid_insurance_sales": paid_insurance_sales,
            "paid_general_rent": paid_general_rent,
            "paid_rent_pando": paid_rent_pando,
            "paid_general_pando": paid_general_pando,
            "paid_general_expense": paid_general_expense,
            "not_paid_insurance_sales": not_paid_insurance_sales,
            "not_paid_general_rent": not_paid_general_rent,
            "not_paid_rent_pando": not_paid_rent_pando,
            "not_paid_general_pando": not_paid_general_pando,
            "not_paid_general_expense": not_paid_general_expense,
            "not_paid_recognized_sales": not_paid_recognized_sales,
            "wage_turnover": wage_turnover,
            "component_turnover": component_turnover,

            "number_of_domestic_samsung_insurances": number_of_domestic_samsung_insurances,
            "number_of_domestic_dongbu_insurances": number_of_domestic_dongbu_insurances,
            "number_of_domestic_meritz_insurances": number_of_domestic_meritz_insurances,
            "number_of_domestic_etc_insurances": number_of_domestic_etc_insurances,
            "number_of_domestic_rent": number_of_domestic_rent,

            "number_of_abroad_samsung_insurances": number_of_abroad_samsung_insurances,
            "number_of_abroad_dongbu_insurances": number_of_abroad_dongbu_insurances,
            "number_of_abroad_meritz_insurances": number_of_abroad_meritz_insurances,
            "number_of_abroad_etc_insurances": number_of_abroad_etc_insurances,
            "number_of_abroad_rent": number_of_abroad_rent,

            "charge_amount": charge_amount,
            "deposit_amount": deposit_amount,
            "attempted_amount": attempted_amount,
            "net_payment_sales": net_payment_sales,
        }

    @property
    def rate_of_attempt(self):
        return self.attempted_amount / self.whole_turnover * 100

    @property
    def whole_not_paid_turnover(self):
        return self.not_paid_general_expense +\
            self.not_paid_general_pando +\
            self.not_paid_general_rent +\
            self.not_paid_insurance_sales +\
            self.not_paid_rent_pando +\
            self.not_paid_recognized_sales

    @property
    def whole_paid_turnover(self):
        return self.paid_general_expense +\
            self.paid_general_pando +\
            self.paid_general_rent +\
            self.paid_insurance_sales +\
            self.paid_rent_pando

    @property
    def whole_turnover(self):
        return self.whole_not_paid_turnover + self.whole_paid_turnover

    @property
    def number_of_domestic_insurances(self):
        return self.number_of_domestic_samsung_insurances +\
            self.number_of_domestic_dongbu_insurances +\
            self.number_of_domestic_meritz_insurances +\
            self.number_of_domestic_etc_insurances

    @property
    def number_of_abroad_insurances(self):
        return self.number_of_abroad_samsung_insurances +\
            self.number_of_abroad_dongbu_insurances +\
            self.number_of_abroad_meritz_insurances +\
            self.number_of_abroad_etc_insurances

    @property
    def number_of_all_insurances(self):
        return self.number_of_domestic_insurances +\
            self.number_of_abroad_insurances

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
        all_extra_sales = ExtraSales.objects.filter(
            charge__charge_date__range=(self.start_date, self.end_date))
        all_recognized_sales = RecognizedSales.objects.filter(
            real_day_came_out__range=(self.start_date, self.end_date)
        )
        kwargs = PeriodSales.get_kwargs(
            orders, all_extra_sales, all_recognized_sales)
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
    def create_or_get_all_monthly_sales(cls, year, start_month, finish_month):
        """
        start_month와 finish_month 까지의 MonthlySales를 가져오거나 없는 경우 생성하여,
        start_month부터 finish_month 까지의 MonthlySales를 QuerySet으로 반환해준다.
        """
        for month in range(start_month, finish_month+1):
            start_date = date(year, month, 1)
            end_date = start_date + \
                relativedelta(months=1) - relativedelta(days=1)
            monthly_sales = cls.objects.filter(
                start_date=start_date, end_date=end_date).first()
            if not monthly_sales:
                cls.create(start_date, end_date)
        returned_start_date = date(year, start_month, 1)
        returned_end_date = date(year, finish_month, 1) + \
            relativedelta(months=1) - relativedelta(days=1)
        return cls.objects.filter(
            start_date__gte=returned_start_date, end_date__lte=returned_end_date)

    @classmethod
    def create_monthly_sales(cls, year, month):
        start_date = date(year, month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        return cls.create(start_date, end_date)

    def __str__(self):
        return f"[{self.start_date.year}년{self.start_date.month}월] 매출"


def get_net_information(all_monthly_sales):
    return_dict = {}
    except_fields = ["id", "created", "updated", "start_date", "end_date"]
    property_list = ["whole_not_paid_turnover", "whole_paid_turnover",
                     "whole_turnover", "number_of_domestic_insurances",
                     "number_of_abroad_insurances", "number_of_all_insurances"]
    for field in MonthlySales._meta.fields:
        if field.name not in except_fields:
            net_field_name = f"net_{field.name}"
            return_dict[net_field_name] = 0
            for monthly_sales in all_monthly_sales:
                return_dict[net_field_name] += getattr(
                    monthly_sales, field.name)
    for property_name in property_list:
        net_property_name = f"net_{property_name}"
        return_dict[net_property_name] = 0
        for monthly_sales in all_monthly_sales:
            return_dict[net_property_name] += getattr(
                monthly_sales, property_name)
    return return_dict


class DeadlineInfoOfPeriod():
    def __init__(self, charge__charge_date__gte, charge__charge_date__lte):
        self.charge__charge_date__gte = charge__charge_date__gte
        self.charge__charge_date__lte = charge__charge_date__lte
        self.all_recognized_sales = RecognizedSales.objects.filter(
            real_day_came_out__range=(
                charge__charge_date__gte, charge__charge_date__lte)
        )
        all_orders = Order.objects.filter(
            charge__charge_date__range=(
                charge__charge_date__gte, charge__charge_date__lte)
        )
        self.numbers_of_car_for_general = 0
        self.numbers_of_car_for_recognized_sales = 0
        self.numbers_of_car_for_rent = 0
        self.numbers_of_car_for_domestic_insurance = 0
        self.numbers_of_car_for_abroad_insurance = 0

        self.component_turnover_of_general = 0
        self.component_turnover_of_recognized_sales = 0
        self.component_turnover_of_rent = 0
        self.component_turnover_of_domestic_insurance = 0
        self.component_turnover_of_abroad_insurance = 0

        self.wage_turnover_of_general = 0
        self.wage_turnover_of_recognized_sales = 0
        self.wage_turnover_of_rent = 0
        self.wage_turnover_of_domestic_insurance = 0
        self.wage_turnover_of_abroad_insurance = 0

        pk_of_registers = all_orders.values_list(
            "register__pk", flat=True).distinct()
        all_registers = Register.objects.filter(pk__in=pk_of_registers)

        self.registers_for_general = []
        self.registers_for_rent = []
        self.registers_for_domestic_insurance = []
        self.registers_for_abroad_insurance = []

        for register in all_registers:
            first_order = register.orders.order_by("created").first()
            if first_order.charge_type == "일반경정비" or first_order.charge_type == "렌트일반":
                self.numbers_of_car_for_general += 1
                self.registers_for_general.append(register)
            elif first_order.charge_type == "렌트판도":
                self.numbers_of_car_for_rent += 1
                self.registers_for_rent.append(register)
            elif first_order.charge_type == "보험" or first_order.charge_type == "일반판도":
                if register.abroad_type == "국산":
                    self.numbers_of_car_for_domestic_insurance += 1
                    self.registers_for_domestic_insurance.append(register)
                elif register.abroad_type == "수입":
                    self.numbers_of_car_for_abroad_insurance += 1
                    self.registers_for_abroad_insurance.append(register)
                else:
                    raise Exception("차량수 카운트에서 abroad_type이 잘못되었습니다.")
            else:
                raise Exception("차량수 카운트에서 charge_type이 잘못되었습니다.")

        for order in all_orders:
            if order.charge_type == "일반경정비" or order.charge_type == "렌트일반":
                self.component_turnover_of_general += order.get_component_turnover()
                self.wage_turnover_of_general += order.get_wage_turnover()
            elif order.charge_type == "렌트판도":
                self.component_turnover_of_rent += order.get_component_turnover()
                self.wage_turnover_of_rent += order.get_wage_turnover()
            elif order.charge_type == "보험" or order.charge_type == "일반판도":
                if order.register.abroad_type == "국산":
                    self.component_turnover_of_domestic_insurance += order.get_component_turnover()
                    self.wage_turnover_of_domestic_insurance += order.get_wage_turnover()
                elif order.register.abroad_type == "수입":
                    self.component_turnover_of_abroad_insurance += order.get_component_turnover()
                    self.wage_turnover_of_abroad_insurance += order.get_wage_turnover()
                else:
                    raise Exception("매출 계산에서 abroad_type이 잘못되었습니다.")
            else:
                raise Exception("매출 계산에서 abroad_type이 잘못되었습니다.")

        for recognized_sales in self.all_recognized_sales:
            self.numbers_of_car_for_recognized_sales += 1
            self.component_turnover_of_recognized_sales += recognized_sales.get_component_turnover()
            self.wage_turnover_of_recognized_sales += recognized_sales.get_wage_turnover()

        self.component_turnover_of_abroad_insurance = int(
            self.component_turnover_of_abroad_insurance)
        self.component_turnover_of_domestic_insurance = int(
            self.component_turnover_of_domestic_insurance)
        self.component_turnover_of_general = int(
            self.component_turnover_of_general)
        self.component_turnover_of_recognized_sales = int(
            self.component_turnover_of_recognized_sales)
        self.component_turnover_of_rent = int(self.component_turnover_of_rent)

        self.wage_turnover_of_abroad_insurance = int(
            self.wage_turnover_of_abroad_insurance)
        self.wage_turnover_of_domestic_insurance = int(
            self.wage_turnover_of_domestic_insurance)
        self.wage_turnover_of_general = int(self.wage_turnover_of_general)
        self.wage_turnover_of_recognized_sales = int(
            self.wage_turnover_of_recognized_sales)
        self.wage_turnover_of_rent = int(self.wage_turnover_of_rent)

        self.total_number_of_cars = self.numbers_of_car_for_abroad_insurance+self.numbers_of_car_for_domestic_insurance + \
            self.numbers_of_car_for_general + \
            self.numbers_of_car_for_recognized_sales+self.numbers_of_car_for_rent
        self.total_component_turnover = self.component_turnover_of_abroad_insurance+self.component_turnover_of_domestic_insurance + \
            self.component_turnover_of_general + \
            self.component_turnover_of_recognized_sales+self.component_turnover_of_rent
        self.total_wage_turnover = self.wage_turnover_of_abroad_insurance+self.wage_turnover_of_domestic_insurance + \
            self.wage_turnover_of_general + \
            self.wage_turnover_of_recognized_sales+self.wage_turnover_of_rent
