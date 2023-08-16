
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Case, When

from core.models import TimeStampedModel
from core.utility import key_from_dict, print_colored
from demand.excel_line_info import (dictionary_to_line,
                                    order_to_excel_dictionary)
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, RequestDepartment, Supporter)
from demand.utility import zero_if_none

STATUS_DICT = {"NO_CHARGE": "미청구", "NOT_PAID": "미입금", "NO_CAME_OUT": "미출고",
               "OVER_DEPOSIT": "과입금", "COMPLETE": "완료", "NEED_CHECK": "확인필요",
               "WASTED": "폐차", "UNREPAIRED": "미/출", "ERROR": "오류",
               "MANUALLY_COMPLETE": "완료(수동)"}
NOT_COMPLETE = 0
PROGRESS = 1
COMPLETE = 2
NEED_CHECK = 3
WARNING = 4
MANUALLY_COMPLETE = 5
STATUS_CLASS = ["not_complete", "progress",
                "complete", "need_check", "warning", "manually_complete"]

REGISTER_NEED_CHARGE = 0
REGISTER_PROGRESS = 1
REGISTER_COMPLETE = 2
REGISTER_NEED_CHECK = 3
REGISTER_MANUALLY_COMPLETE = 4
REGISTER_STATUS = ["청구 필요", "진행중", "완료", "확인 필요", "완료(수동)"]


def make_to_class_name(name):
    return name + "_class"


class Sales(TimeStampedModel):
    status = models.CharField(choices=[(value, value)for value in STATUS_DICT.values()],
                              max_length=20, default="미청구", verbose_name="상태")

    class Meta:
        ordering = ["-created",]
        verbose_name = "매출"
        verbose_name_plural = "매출(들)"
        abstract = True

# region Formatting Functions
    def formatted_day_came_in(self):
        if isinstance(self, Order):
            day_came_in = self.register.day_came_in if self.register else None
        else:
            day_came_in = self.day_came_in
        if day_came_in:
            return day_came_in.strftime("%m/%d")
        else:
            return "-"

    def formatted_real_day_came_out(self):
        if isinstance(self, Order):
            real_day_came_out = self.register.real_day_came_out if self.register else None
        else:
            real_day_came_out = self.real_day_came_out
        if real_day_came_out:
            return real_day_came_out.strftime("%m/%d")
        else:
            return "-"

    def formatted_charge_amount(self):
        charge_amount = self.get_charge_amount()
        if charge_amount:
            return format(int(charge_amount), ",")
        else:
            return "-"

    def formatted_chargable_amount(self):
        chargable_amount = self.get_chargable_amount()
        if chargable_amount:
            return format(int(chargable_amount), ",")
        else:
            return "-"

    def formatted_payment_rate(self):
        payment_rate = self.get_payment_rate()
        if payment_rate:
            return str(round(payment_rate*100))+"%"
        else:
            return "-"

    def formatted_net_payment(self):
        return format(int(self.get_net_payment()), ",")

    def formatted_deposit_amount(self):
        if self.deposit:
            if self.deposit.deposit_amount:
                return format(self.deposit.deposit_amount, ",")
        return "-"

    def formatted_turnover(self):
        turnover = self.get_turnover()
        if turnover:
            return format(int(turnover), ",")
        else:
            return "-"

    def formatted_wage_turnover(self):
        wage_turnover = self.get_wage_turnover()
        if wage_turnover:
            return format(int(wage_turnover), ",")
        else:
            return "-"

# endregion Formatted Functions

# region Sales Utility Functions

    def get_chargable_amount(self) -> float:
        """
        청구 가능 금액을 반환한다. 청구객체가 없어서 반환이 불가능할시 None을 반환한다. 형태는 항상 float
        """
        if self.charge:
            if isinstance(self, Order):
                if self.fault_ratio:
                    return float(self.charge.get_repair_amount()*1.1*self.fault_ratio/100)
            return float(self.charge.get_repair_amount()*1.1)
        else:
            return None

    def get_indemnity_amount(self):
        if self.payment:
            return zero_if_none(self.payment.indemnity_amount)
        else:
            return 0

    def get_charge_amount(self) -> float:
        """
        청구금을 반환한다. 청구객체가 없어서 반환이 불가능할시 None을 반환한다. 형태는 항상 float
        """
        if self.charge:
            refund_amount = zero_if_none(
                self.payment.refund_amount if self.payment else 0)
            charge_amount = self.get_chargable_amount() - float(self.get_indemnity_amount()) + \
                float(refund_amount)
            if charge_amount > 0:
                return charge_amount
            else:
                return 0
        else:
            return None

    def get_deposit_amount(self):
        """
        입금액을 반환한다.
        """
        if self.deposit:
            return zero_if_none(self.deposit.deposit_amount)
        else:
            return 0

    def get_attempted_amount(self):
        """
        미수액을 반환한다. 미수액이란 청구는 됐으나 입금이 되지 않은 경우의 청구금액을 의미한다. 형태는 항상 float
        """
        if not self.deposit:
            return self.get_charge_amount()
        else:
            return float(0)

    def get_payment_rate_for_input(self):
        """
        EXCEL에서 사용하는 지급율
        """
        if self.charge:
            charge_amount = self.get_charge_amount()
            if charge_amount != 0:
                if self.deposit and self.deposit.deposit_amount:
                    return self.deposit.deposit_amount/charge_amount
                else:
                    return None
            else:
                return None
        else:
            return None

    def get_net_payment(self):
        if self.payment:
            refund_amount = zero_if_none(self.payment.refund_amount)
            discount_amount = zero_if_none(self.payment.discount_amount)
            indemnity_amount = zero_if_none(self.payment.indemnity_amount)
            return indemnity_amount-discount_amount-refund_amount
        else:
            return 0

    def get_net_payment_sales(self):
        """
        Preiod Sales. 형태는 float
        """
        return self.get_net_payment()/1.1

    def get_payment_rate(self):
        """
        지급율을 계산한다. 지급율이 계산이 불가능할시 None을 반환한다.
        """
        if not self.charge:
            return 0
        else:
            chargable_amount = self.get_chargable_amount()
            if chargable_amount == 0:
                return None
            # 일반
            if isinstance(self, ExtraSales) or self.charge_type[:2] == "일반":
                if self.payment:
                    return self.get_net_payment()/chargable_amount
            else:  # 보험
                charge_amount = self.get_charge_amount()
                if self.deposit and charge_amount:
                    if self.deposit.deposit_amount:
                        return self.deposit.deposit_amount/charge_amount
                return None

    def get_not_paid_amount(self):
        """
        미수액을 계산한다. 계산이 불가능할시에도 0을 반환한다.
        """
        charge_amount = self.get_charge_amount()
        if not self.deposit:
            return charge_amount if charge_amount else 0
        else:
            return 0

    def get_turnover(self) -> int:
        deposit_amount = self.deposit.deposit_amount if self.deposit else 0
        return deposit_amount+self.get_net_payment()

    def get_factory_turnover(self):
        return float(self.get_turnover()/1.1)

    def get_paid_turnover(self) -> float:
        return self.get_factory_turnover() if self.get_factory_turnover() > float(0) else float(0)

    def get_not_paid_turnover(self) -> float:
        if self.charge:
            if not self.deposit:
                return self.get_charge_amount()/1.1*0.95
            else:
                return 0.0
        else:
            return 0.0

    def get_integrated_turnover(self) -> float:
        return self.get_not_paid_turnover()+self.get_paid_turnover()

    def get_component_turnover(self) -> float:
        if self.charge:
            if self.charge.component_amount:
                if isinstance(self, Order):
                    if self.fault_ratio:
                        return float(self.fault_ratio*self.charge.component_amount/100)
                return self.charge.component_amount
        return 0

    def get_wage_turnover(self) -> float:
        return self.get_integrated_turnover() - self.get_component_turnover()

    def check_no_came_out(self):
        if isinstance(self, Order):
            if self.register:
                real_day_came_out = self.register.real_day_came_out
            else:
                return True
        else:  # ExtraSales Case
            real_day_came_out = self.real_day_came_out
        return False if real_day_came_out else True

    def get_status(self):
        """
        매출의 상태 순서는 다음과 같다.
        1. 출고가 안됐으면 미출고(NO_CAME_OUT)
        2. 출고가 됐지만 charge가 없으면 미청구
        3. 청구를 했지만 입금이 안됐으면 미입금
        4. 입금이 됐지만 입금액이 청구액보다 적으면 확인필요
        5. 입금이 됐지만 입금액이 청구액보다 많으면 과입금(1.01배)
        6. 입금이 됐고 0.85배보다 많으면 완료
        7. 입금이 됐고 위의 두 조건이 아니면 확인필요
        """
        try:
            if isinstance(self, Order):
                if not self.register:
                    return STATUS_DICT["ERROR"]
                if self.register.wasted:
                    return STATUS_DICT["WASTED"]
                if self.register.unrepaired:
                    return STATUS_DICT["UNREPAIRED"]

            if self.check_no_came_out():
                return STATUS_DICT["NO_CAME_OUT"]
            if not self.charge:
                return STATUS_DICT["NO_CHARGE"]
            else:
                # 부품비의 경우 charge_date가 없어도 존재할 수 있다. 따라서 청구 기준은 charge object가 아닌 청구일로 해야한다.
                if not self.charge.charge_date:
                    return STATUS_DICT["NO_CHARGE"]

            # 일반경정, 일반렌트, 기타매출의 경우 입금이 없음
            if isinstance(self, ExtraSales) or self.charge_type[:2] == "일반":
                if self.payment:
                    payment_rate = self.get_payment_rate()
                    if payment_rate > 1.01:
                        return STATUS_DICT["OVER_DEPOSIT"]
                    elif payment_rate < 0.99:
                        return STATUS_DICT["NEED_CHECK"]
                    else:
                        return STATUS_DICT["COMPLETE"]
                else:
                    return STATUS_DICT["NOT_PAID"]

            if isinstance(self, Order):  # 일반 주문의 경우
                if self.deposit:
                    payment_rate = self.get_payment_rate()
                    if payment_rate > 1.01:
                        return STATUS_DICT["OVER_DEPOSIT"]
                    elif payment_rate >= 0.85:
                        return STATUS_DICT["COMPLETE"]
                    else:
                        return STATUS_DICT["NEED_CHECK"]
                else:
                    return STATUS_DICT["NOT_PAID"]
            # 지금까지 해당 사항 없으면 ERROR임
            raise Exception("NO MATCHING CASE!")

        except Exception as e:

            if self == None:
                print_colored("self is None", "red")
            else:
                try:
                    print_colored(f"ERROR IN GET STATUS: {str(self)}", "red")
                except AttributeError:
                    print_colored(f"ERROR IN GET STATUS: {str(self)}", "red")
                    print_colored("[Below self is not printable]", "red")
                    print_colored(f"{type(self)}:{self.pk}", "red")
                print_colored(str(e), "magenta")
            return STATUS_DICT["ERROR"]

# endregion Sales Utility Functions

# region Manually Complete
    def make_manually_complete(self):
        self.status = STATUS_DICT["MANUALLY_COMPLETE"]
        self.save()

    def cancel_manually_complete(self):
        self.status = self.get_status()
        self.save()

    def manually_completed(self):
        if self.status == STATUS_DICT["MANUALLY_COMPLETE"]:
            return True
        else:
            return False

    def completed(self):
        if self.status == STATUS_DICT["COMPLETE"] or self.status == STATUS_DICT["MANUALLY_COMPLETE"]\
                or self.status == STATUS_DICT["UNREPAIRED"] or self.status == STATUS_DICT["WASTED"]:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.manually_completed():
            self.status = self.get_status()
        super().save(*args, **kwargs)
# endregion Manually Complete

# region HTML FUNCTIONS
    def get_status_class(self):
        status_key = key_from_dict(self.status, STATUS_DICT)
        if status_key == None:
            raise ValueError(f"status_key is None. status:{self.status}")
        else:
            return make_to_class_name(status_key.lower())

    def get_came_out_class(self):
        if isinstance(self, Order):
            real_day_came_out = self.register.real_day_came_out if self.register else None
        else:
            real_day_came_out = self.real_day_came_out
        if real_day_came_out:
            status_class = STATUS_CLASS[COMPLETE]
        elif self.payment:
            status_class = STATUS_CLASS[WARNING]
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_charge_class(self):
        if self.charge:
            if self.charge.is_stable():
                status_class = STATUS_CLASS[COMPLETE]
            else:
                status_class = STATUS_CLASS[WARNING]
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_deposit_class(self):
        if self.deposit:
            if self.deposit.is_stable():
                status_class = STATUS_CLASS[COMPLETE]
            else:
                status_class = STATUS_CLASS[WARNING]
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_description(self):
        raise NotImplementedError
# endregion HTML FUNCTIONS
# --------------- EXCEL FUNCTION -----------------#

    def to_excel_line(self):
        raise NotImplementedError

# --------------- PRINT FUNCTION -----------------#

    def __str__(self):
        raise NotImplementedError


class Register(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "등록"
        verbose_name_plural = "등록(들)"
    RO_number = models.CharField(verbose_name="RO번호", max_length=10)
    car_number = models.CharField(verbose_name="차량번호", max_length=20)
    day_came_in = models.DateField(verbose_name="입고일")
    expected_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="출고예정일")
    # 나중에 출고시에 추가함
    real_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="실제출고일")
    car_model = models.CharField(max_length=90, verbose_name="차종")
    abroad_type = models.CharField(
        choices=(("국산", "국산"), ("수입", "수입")), max_length=10, verbose_name="국산/수입")
    number_of_repair_works = models.IntegerField(
        null=True, blank=True,
        default=0, verbose_name="보수 작업판수")
    number_of_exchange_works = models.IntegerField(
        null=True, blank=True,
        default=0, verbose_name="교환 작업판수")
    supporter = models.ForeignKey(
        Supporter, verbose_name="입고지원", blank=True, null=True, on_delete=models.SET_NULL, related_name="registers")
    client_name = models.CharField(
        blank=True, null=True, verbose_name="고객명", max_length=30)
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="orders", null=True, on_delete=models.SET_NULL, verbose_name="보험 담당자")
    phone_number = models.CharField(
        null=True, blank=True, verbose_name="전화번호", max_length=15)

    # 미수리출고와 폐차 여부는 출고시에 확정시킨다.
    unrepaired = models.BooleanField(default=False, verbose_name="미수리출고")
    wasted = models.BooleanField(default=False, verbose_name="폐차")

    rentcar_company_name = models.CharField(
        blank=True, null=True, max_length=100, verbose_name="렌트 업체명")
    note = models.TextField(
        blank=True, null=True, verbose_name="비고")

    first_center_repaired = models.BooleanField(
        default=False, verbose_name="1센터 수리건")

# region Register Utility Function
    @property
    def all_orders(self):
        return self.orders.all().order_by("created")

    def get_work_days(self):
        if self.real_day_came_out and self.day_came_in:
            return (self.real_day_came_out - self.day_came_in).days
        else:
            return None

    def get_number_of_works(self):
        return self.number_of_exchange_works + self.number_of_repair_works

    @classmethod
    def get_RO_number(cls, month=None, year=None):
        current_year = year or datetime.now().year
        current_month = month or datetime.now().month
        current_number = cls.objects.filter(
            RO_number__icontains=f"{current_month}-", created__year=current_year).count()+1
        return f"{current_month}-{current_number}"

    def set_RO_number(self, month=None, year=None):
        self.RO_number = Register.get_RO_number(month, year)
        self.save()
# endregion Register Utility Function


# region FOR HTML FUNCTIONS


    def get_status(self):
        orders = self.all_orders
        all_completed = True
        for order in orders:
            if not order.completed():
                all_completed = False
        if all_completed:
            return REGISTER_STATUS[REGISTER_COMPLETE]
        for order in orders:
            if order.status in [STATUS_DICT["ERROR"], STATUS_DICT["NEED_CHECK"]]:
                return REGISTER_STATUS[REGISTER_NEED_CHECK]
        for order in orders:
            if order.status == STATUS_DICT["NO_CHARGE"]:
                return REGISTER_STATUS[REGISTER_NEED_CHARGE]
        for order in orders:
            if order.status != STATUS_DICT["COMPLETE"]:
                return REGISTER_STATUS[REGISTER_PROGRESS]
        return REGISTER_STATUS[COMPLETE]

    def get_status_class(self):
        status = self.get_status()
        status_class = ""
        if status == REGISTER_STATUS[REGISTER_NEED_CHECK]:
            status_class = STATUS_CLASS[NEED_CHECK]
        elif status == REGISTER_STATUS[REGISTER_NEED_CHARGE]:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        elif status == REGISTER_STATUS[REGISTER_PROGRESS]:
            status_class = STATUS_CLASS[PROGRESS]
        elif status == REGISTER_STATUS[REGISTER_COMPLETE]:
            status_class = STATUS_CLASS[COMPLETE]
        else:
            raise ValueError(f"status:{status} is not valid")
        return make_to_class_name(status_class)

    def get_description(self):
        try:
            day_came_in = self.day_came_in.strftime(
                "%m-%d") if self.day_came_in else "없음"
            if not self.real_day_came_out and self.expected_day_came_out:
                day_came_out = self.expected_day_came_out.strftime(
                    "%m-%d") + " 예정"
            elif self.expected_day_came_out:
                day_came_out = self.expected_day_came_out.strftime(
                    "%m-%d") + " 출고"
            else:
                day_came_out = "없음"
            client_name = self.client_name if self.client_name else "없음"
            rentcar = self.rentcar_company_name if self.rentcar_company_name else "없음"
            supporter = self.supporter.name if self.supporter else "없음"
            insurance_agent = self.insurance_agent.name if self.insurance_agent else "없음"
            return f"입고:{day_came_in}/출고:{day_came_out}/차종:{self.car_model}/판수:{self.get_number_of_works()}/입고지원:{supporter}/고객명:{client_name}/담당자:{insurance_agent}/전화번호:{self.phone_number}/렌트:{rentcar}"
        except Exception as e:
            return str(e)
# endregion FOR HTML FUNCTIONS

    def __str__(self):
        return f"[{self.RO_number}]{self.car_number}({self.day_came_in.year}/{self.day_came_in.month}/{self.day_came_in.day})"

    def save(self, *args, **kwargs):
        if self.number_of_exchange_works == None:
            self.number_of_exchange_works = 0
        if self.number_of_repair_works == None:
            self.number_of_repair_works = 0
        super(Register, self).save(*args, **kwargs)


class Order(Sales):
    """
    charge_type 수정시에 SalesInfo Model도 바꾸어야 한다.
    """
    class Meta:
        ordering = ["-created",]
        verbose_name = "주문 매출"
        verbose_name_plural = "주문 매출(들)"
    register = models.ForeignKey(
        Register, null=True, on_delete=models.CASCADE, verbose_name="등록", related_name="orders")
    charged_company = models.ForeignKey(
        ChargedCompany, null=True, related_name="orders", verbose_name="보험(렌트)", on_delete=models.SET_NULL)
    charge_type = models.CharField(choices=(("보험", "보험"), ("일반경정비", "일반경정비"), (
        "일반판도", "일반판도"), ("렌트판도", "렌트판도"), ("렌트일반", "렌트일반"),
        ("기타", "기타")), max_length=20, verbose_name="구분")
    order_type = models.CharField(null=True, blank=True, choices=(
        ("자차", "자차"), ("대물", "대물"), ("일반", "일반")), max_length=10, verbose_name="차/대/일")
    receipt_number = models.CharField(
        max_length=20, verbose_name="접수번호", null=True, blank=True)
    fault_ratio = models.IntegerField(
        null=True, blank=True, verbose_name="과실분")

    payment = models.OneToOneField(
        Payment, null=True, blank=True, related_name="order", verbose_name="결제", on_delete=models.SET_NULL)
    charge = models.OneToOneField(
        Charge, null=True, blank=True, related_name="order", verbose_name="청구", on_delete=models.SET_NULL)
    deposit = models.OneToOneField(
        Deposit, null=True, blank=True, related_name="order", verbose_name="입금", on_delete=models.SET_NULL)

    incentive_paid = models.BooleanField(
        default=False, verbose_name="인센티브 지급여부")
    incentive_paid_date = models.DateField(
        blank=True, null=True, verbose_name="인센티브 지급일")

    @property
    def order_index(self):
        try:
            return list(self.register.orders.all().order_by("created")).index(self)+1
        except Exception as e:
            print(f"ORDER INDEX PROBLEM {self.pk}")
            return None

    def get_description(self):
        try:
            charge = format(self.get_charge_amount(),
                            ",") if self.charge else "청구필요"
            deposit = format(self.deposit.deposit_amount,
                             ",") if self.deposit else "입금필요"
            return f"{self.charged_company.name} {self.charge_type} {self.order_type} 청구액:{charge} 입금액:{deposit} "
        except Exception as e:
            print(e)

    def get_incentive(self):
        if self.register:
            if self.register.supporter:
                return int(self.get_wage_turnover() * self.register.supporter.incentive_rate_percent/100)
        return 0

    def to_excel_line(self):
        return dictionary_to_line(order_to_excel_dictionary(self))

    def get_incentive_paid_month_display(self):
        if self.incentive_paid_date:
            paid_date = self.incentive_paid_date - relativedelta(months=1)
            return paid_date.strftime("%y/%m")
        else:
            return "미지급"

    def __str__(self):
        try:
            return f"{self.register.RO_number}[{self.order_index}] {self.order_type} {self.charge_type}"
        except Exception as e:
            try:
                print(
                    f"Exception in __str__ of order : REGISTER_{str(self.register.pk)}[{self.order_index}]")
            except Exception as e:
                print(
                    f"Double Exception in __str__ of order which has pk of {self.pk}")
                print(self.order_index)
                return f"Order [pk:{self.pk}], {e}"
            return f"{str(self.register)}[{self.order_index}]"


class ExtraSales(Sales):
    """
    세차, 폐차, 미수리 출고 등 기타 매출은 여기에 잡힙니다.
    """
    class Meta:
        ordering = ["-created",]
        verbose_name = "기타 매출"
        verbose_name_plural = "기타 매출(들)"

    sort = models.CharField(choices=(
        ("세차", "세차"), ("기타", "기타")),
        max_length=20, verbose_name="구분")

    day_came_in = models.DateField(verbose_name="입고일", blank=True, null=True)
    expected_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="출고예정일")
    # 나중에 출고시에 추가함
    real_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="실제출고일")
    car_number = models.CharField(
        verbose_name="차량번호", blank=True, null=True, max_length=20)
    car_model = models.CharField(
        blank=True, null=True, max_length=90, verbose_name="차종")
    abroad_type = models.CharField(
        blank=True, null=True,
        choices=(("국산", "국산"), ("수입", "수입")), max_length=10, verbose_name="국산/수입")
    supporter = models.ForeignKey(
        Supporter, verbose_name="입고지원", blank=True, null=True, on_delete=models.SET_NULL, related_name="all_extra_sales")
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="all_extra_sales", null=True, on_delete=models.SET_NULL, verbose_name="보험 담당자")
    client_name = models.CharField(
        blank=True, null=True, verbose_name="고객명", max_length=30)
    phone_number = models.CharField(
        null=True, blank=True, max_length=15, verbose_name="전화번호")
    payment = models.OneToOneField(
        Payment, null=True, blank=True, related_name="extra_sales", verbose_name="결제", on_delete=models.SET_NULL)
    charge = models.OneToOneField(
        Charge, null=True, blank=True, related_name="extra_sales", verbose_name="청구", on_delete=models.SET_NULL)
    deposit = models.OneToOneField(
        Deposit, null=True, blank=True, related_name="extra_sales", verbose_name="입금", on_delete=models.SET_NULL)
    note = models.TextField(blank=True, null=True, verbose_name="비고")

    def get_description(self):
        return f"기타매출({self.pk})"

    def to_excel_line(self):
        pass

    def __str__(self):
        return f"[{self.sort}]{self.car_number}"


class RecognizedSales(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "인정매출"
        verbose_name_plural = "인정 매출(들)"
    day_came_in = models.DateField(verbose_name="입고일", blank=True, null=True)
    real_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="출고일")
    car_number = models.CharField(
        verbose_name="차량번호", blank=True, null=True, max_length=20)
    request_department = models.ForeignKey(
        RequestDepartment, on_delete=models.SET_NULL, null=True, verbose_name="요청부서")
    wage_amount = models.IntegerField(default=0, verbose_name="공임비")
    component_amount = models.IntegerField(default=0, verbose_name="부품비")
    note = models.TextField(default="부가세 별도", blank=True,
                            null=True, verbose_name="비고")

    def to_excel_line(self):
        return [
            self.day_came_in.month,
            self.day_came_in.strftime("%Y-%m-%d"),
            self.real_day_came_out.strftime("%Y-%m-%d"),
            self.car_number or "-",
            self.request_department.name or "-",
            self.wage_amount or 0,
            self.component_amount or 0,
            self.get_repair_amount() or 0,
            self.note or "-",
            int(self.get_not_paid_turnover()) or "-",
        ]

    def get_repair_amount(self):
        if self.wage_amount != None and self.component_amount != None:
            return self.wage_amount + self.component_amount
        else:
            None

    def formatted_day_came_in(self):
        if self.day_came_in:
            return self.day_came_in.strftime("%m/%d")
        else:
            return "-"

    def formatted_real_day_came_out(self):
        if self.real_day_came_out:
            return self.real_day_came_out.strftime("%m/%d")
        else:
            return "-"

    def get_not_paid_turnover(self):
        return self.get_repair_amount() if self.get_repair_amount() else 0

    def get_wage_turnover(self):
        return self.wage_amount if self.wage_amount else 0

    def get_component_turnover(self):
        return self.component_amount if self.component_amount else 0

    def __str__(self):
        if self.real_day_came_out:
            return f"[{self.car_number}] {self.real_day_came_out.strftime('%Y/%m/%d')} 출고"
        else:
            return f"[{self.car_number}]"
