from datetime import datetime

from django.db import models

from core.models import TimeStampedModel
from core.utility import print_colored
from demand.excel_line_info import *

# Create your models here.
STATUS_DICT = {"NO_CHARGE": "미청구", "NOT_PAID": "미입금", "NO_CAME_OUT": "미출고",
               "OVER_DEPOSIT": "과입금", "COMPLETE": "완료", "NEED_CHECK": "확인필요",
               "ERROR": "오류", "MANUALLY_COMPLETE": "완료(수동)"}


NOT_COMPLETE = 0
PROGRESS = 1
COMPLETE = 2
NEED_CHECK = 3
MANUALLY_COMPLETE = 4
STATUS_CLASS = ["not_complete", "progress",
                "complete", "need_check", "manually_complete"]
REGISTER_STAUTS = ["청구 필요", "진행중", "완료", "확인 필요", "완료(수동)"]


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

    def get_indemnity_amount(self):
        if self.payment:
            return self.payment.indemnity_amount
        else:
            return 0

    def get_charge_amount(self):
        if self.charge:
            return self.charge.get_charge_amount()
        else:
            return None

    def formatted_day_came_in(self):
        if isinstance(self, Order):
            day_came_in = self.register.day_came_in if self.register else None
        else:
            day_came_in = self.day_came_in
        if day_came_in:
            return day_came_in.strftime("%m/%d")
        else:
            return "-"

    def formatted_charge_amount(self):
        charge_amount = self.get_charge_amount()
        if charge_amount:
            return format(charge_amount, ",")+" ₩"
        else:
            return "-"

    def formatted_payment_rate(self):
        payment_rate = self.get_payment_rate()
        if payment_rate:
            return str(round(payment_rate*100))+"%"
        else:
            return "-"

    def formatted_deposit_amount(self):
        if self.deposit:
            return format(self.deposit.deposit_amount, ",")+" ₩"
        return "-"

    def get_payment_rate_for_input(self):
        charge_amount = self.get_charge_amount()
        if not charge_amount:
            return None
        else:
            if charge_amount != 0:
                if self.deposit:
                    return self.deposit.deposit_amount/charge_amount
                else:
                    return None
            else:
                return None

    def get_net_payment(self):
        if self.payment:
            refund_amount = self.payment.refund_amount if self.payment.refund_amount else 0
            discount_amount = self.payment.discount_amount if self.payment.discount_amount else 0
            indemnity_amount = self.payment.indemnity_amount if self.payment.indemnity_amount else 0
        else:
            refund_amount = 0
            discount_amount = 0
            indemnity_amount = 0
        return indemnity_amount-discount_amount-refund_amount

    def get_payment_rate(self):
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
                else:
                    return 0
            else:  # 보험
                if self.deposit:
                    return self.deposit.deposit_amount/chargable_amount
                else:
                    return 0

    def get_chargable_amount(self):
        if self.charge:
            if isinstance(self, Order):
                if self.fault_ratio:
                    return round(self.charge.get_repair_amount()*1.1*self.fault_ratio/100)
            return round(self.charge.get_repair_amount()*1.1)
        else:
            None

    def get_not_paid_amount(self):
        charge_amount = self.get_charge_amount()
        if not self.deposit:
            return charge_amount if charge_amount else 0
        else:
            return 0

    def get_turnover(self):
        deposit_amount = self.deposit.deposit_amount if self.deposit else 0
        return deposit_amount+self.get_net_payment()

    def get_factory_turnover(self):
        return int(self.get_turnover()/1.1)

    def get_paid_turnover(self):
        return self.get_factory_turnover() if self.get_factory_turnover() > 0 else 0

    def get_not_paid_turnover(self):
        if self.charge:
            if not self.deposit:
                return round(self.get_charge_amount()/1.1*0.95)
            else:
                return 0.0
        else:
            return 0.0

    def get_integrated_turnover(self):
        return self.get_not_paid_turnover()+self.get_paid_turnover()

    def get_component_turnover(self):
        if self.charge:
            if self.charge.component_amount:
                if isinstance(self, Order):
                    if self.fault_ratio:
                        return int(self.fault_ratio*self.charge.component_amount/100)
                return self.charge.component_amount
        return 0

    def get_wage_turnover(self):
        return self.get_integrated_turnover() - self.get_component_turnover()

    def get_status(self):
        try:
            if isinstance(self, Order):
                real_day_came_out = self.register.real_day_came_out
            else:  # ExtraSales Case
                real_day_came_out = self.real_day_came_out

            if isinstance(self, ExtraSales) or self.charge_type[:2] == "일반":
                if not self.charge:
                    return STATUS_DICT["NO_CHARGE"]
                else:
                    if self.payment:
                        if real_day_came_out:
                            if self.get_payment_rate() > 1.01:
                                return STATUS_DICT["OVER_DEPOSIT"]
                            elif self.get_payment_rate() < 0.99:
                                return STATUS_DICT["NEED_CHECK"]
                            else:
                                return STATUS_DICT["COMPLETE"]
                        else:
                            return STATUS_DICT["NO_CAME_OUT"]
                    else:
                        return STATUS_DICT["NOT_PAID"]
            else:  # 보험의 경우
                if not self.charge:
                    return STATUS_DICT["NO_CHARGE"]
                else:
                    if self.deposit:
                        if real_day_came_out:
                            if self.get_payment_rate() > 1.01:
                                return STATUS_DICT["OVER_DEPOSIT"]
                            elif self.get_payment_rate() >= 0.85:
                                return STATUS_DICT["COMPLETE"]
                            else:
                                return STATUS_DICT["NEED_CHECK"]
                        else:
                            return STATUS_DICT["NO_CAME_OUT"]
                    else:
                        return STATUS_DICT["NOT_PAID"]
        except Exception as e:
            if self == None:
                print_colored("self is None", "red")
            else:
                try:
                    print_colored(self.__str__, "red")
                except AttributeError:
                    print_colored("[Below self is not printable]", "red")
                    print_colored(f"{type(self)}:{self.pk}", "red")

            return STATUS_DICT["ERROR"]

    def make_manually_complete(self):
        self.status = STATUS_DICT["MANUALLY_COMPLETE"]
        self.save()

    def finished(self):
        if self.status == STATUS_DICT["COMPLETE"] or self.status == STATUS_DICT["MANUALLY_COMPLETE"]:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if self.status != "완료(수동)":
            self.status = self.get_status()
        super().save(*args, **kwargs)

# --------------- HTML FUNCTION -----------------#
    def get_status_class(self):
        status_key = next(
            (k for k, v in STATUS_DICT.items() if v == self.status), None)
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
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_charge_class(self):
        if self.charge:
            status_class = STATUS_CLASS[COMPLETE]
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_deposit_class(self):
        if self.deposit:
            status_class = STATUS_CLASS[COMPLETE]
        else:
            status_class = STATUS_CLASS[NOT_COMPLETE]
        return make_to_class_name(status_class)

    def get_description(self):
        raise NotImplementedError

# --------------- EXCEL FUNCTION -----------------#

    def to_excel_line(self):
        raise NotImplementedError

# --------------- PRINT FUNCTION -----------------#

    def __str__(self):
        raise NotImplementedError


class Supporter(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "입고 지원 업체"
        verbose_name_plural = "입고 지원 업체(들)"
    name = models.CharField(max_length=100, verbose_name="지원 업체명")
    active = models.BooleanField(default=True, verbose_name="활성화")

    def __str__(self):
        return self.name


class ChargedCompany(TimeStampedModel):
    class Meta:
        ordering = ["-created",]
        verbose_name = "보험회사"
        verbose_name_plural = "보험회사(들)"
    name = models.CharField(max_length=100, verbose_name="담당 업체명")
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
    class Meta:
        ordering = ["-created",]
        verbose_name = "청구 정보"
        verbose_name_plural = "청구 정보(들)"
    charge_date = models.DateField(verbose_name="청구일")
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
    class Meta:
        ordering = ["-created",]
        verbose_name = "입금 정보"
        verbose_name_plural = "입금 정보(들)"
    deposit_amount = models.IntegerField(verbose_name="입금액")
    deposit_date = models.DateField(verbose_name="입금일")

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
        choices=(("domestic", "국산"), ("imported", "수입")), max_length=10, verbose_name="국산/수입")
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
    unrepaired = models.BooleanField(default=False, verbose_name="미수리출고")
    wash_car = models.BooleanField(default=False, verbose_name="세차")
    wasted = models.BooleanField(default=False, verbose_name="폐차")
    rentcar_company_name = models.CharField(
        blank=True, null=True, max_length=100, verbose_name="렌트 업체명")
    note = models.TextField(
        blank=True, null=True, verbose_name="비고")

    def get_work_days(self):
        if self.real_day_came_out and self.day_came_in:
            return (self.real_day_came_out - self.day_came_in).days
        else:
            return None

    def get_number_of_works(self):
        return self.number_of_exchange_works + self.number_of_repair_works

    @classmethod
    def get_RO_number(cls):
        current_month = datetime.now().month
        current_number = cls.objects.filter(
            created__month=current_month).count()
        return f"{current_month}-{current_number}"

    def set_RO_number(self):
        self.RO_number = Register.get_RO_number()
        self.save()

# --------------- HTML FUNCTION -----------------#
    def get_status(self):
        orders = self.orders.all()
        all_finished = True
        for order in orders:
            if not order.finished():
                all_finished = False
        if all_finished:
            return REGISTER_STAUTS[COMPLETE]
        for order in orders:
            if order.get_status() in [STATUS_DICT["ERROR"], STATUS_DICT["NEED_CHECK"]]:
                return REGISTER_STAUTS[NEED_CHECK]
        for order in orders:
            if order.get_status() == STATUS_DICT["NO_CHARGE"]:
                return REGISTER_STAUTS[NOT_COMPLETE]
        for order in orders:
            if order.get_status() != STATUS_DICT["COMPLETE"]:
                return REGISTER_STAUTS[PROGRESS]
        return REGISTER_STAUTS[COMPLETE]

    def get_status_class(self):
        status = self.get_status()
        status_class = ""
        if status == REGISTER_STAUTS[NEED_CHECK]:
            status_class = "need_check"
        elif status == REGISTER_STAUTS[NOT_COMPLETE]:
            status_class = "not_complete"
        elif status == REGISTER_STAUTS[PROGRESS]:
            status_class = "progress"
        elif status == REGISTER_STAUTS[COMPLETE]:
            status_class = "complete"
        else:
            raise ValueError(f"status:{status} is not valid")
        return make_to_class_name(status_class)

    def get_came_out_class(self):
        if self.real_day_came_out:
            return STATUS_CLASS[COMPLETE]
        else:
            return STATUS_CLASS[NOT_COMPLETE]

    def get_charge_class(self):
        if self.charge:
            return STATUS_CLASS[COMPLETE]
        else:
            return STATUS_CLASS[NOT_COMPLETE]

    def get_deposit_class(self):
        if self.deposit:
            return STATUS_CLASS[COMPLETE]
        else:
            return STATUS_CLASS[NOT_COMPLETE]

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

# --------------- PRINT FUNCTION -----------------#

    def __str__(self):
        return f"[{self.RO_number}]{self.car_number}/{self.phone_number}"


class Order(Sales):
    class Meta:
        ordering = ["-created",]
        verbose_name = "주문 매출"
        verbose_name_plural = "주문 매출(들)"
    register = models.ForeignKey(
        Register, null=True, on_delete=models.CASCADE, verbose_name="등록", related_name="orders")
    charged_company = models.ForeignKey(
        ChargedCompany, null=True, related_name="orders", verbose_name="담당 업체명", on_delete=models.CASCADE)
    charge_type = models.CharField(choices=(("보험", "보험"), ("일반경정비", "일반경정비"), (
        "일반판도", "일반판도"), ("렌트판도", "렌트판도"), ("렌트일반", "렌트일반"),
        ("인정매출", "인정매출")), max_length=20, verbose_name="구분")
    order_type = models.CharField(null=True, blank=True, choices=(
        ("자차", "자차"), ("대물", "대물"), ("일반", "일반")), max_length=10, verbose_name="차/대/일")
    receipt_number = models.CharField(
        max_length=20, verbose_name="접수번호", null=True, blank=True)
    fault_ratio = models.IntegerField(
        null=True, blank=True, verbose_name="과실분")

    payment = models.OneToOneField(
        Payment, null=True, blank=True, related_name="order", verbose_name="결제", on_delete=models.CASCADE)
    charge = models.OneToOneField(
        Charge, null=True, blank=True, related_name="order", verbose_name="청구", on_delete=models.CASCADE)
    deposit = models.OneToOneField(
        Deposit, null=True, blank=True, related_name="order", verbose_name="입금", on_delete=models.CASCADE)

    note = models.TextField(blank=True, null=True, verbose_name="비고")

    def get_description(self):
        try:
            charge = format(self.get_charge_amount(),
                            ",")+"₩" if self.charge else "청구필요"
            deposit = format(self.deposit.deposit_amount,
                             ",")+"₩" if self.deposit else "입금필요"
            return f"{self.charged_company.name} {self.charge_type} {self.order_type} 청구액:{charge} 입금액:{deposit} "
        except Exception as e:
            print(e)

    def to_excel_line(self):
        return dictionary_to_line(order_to_excel_dictionary(self))

    def __str__(self):
        return f"{self.register.RO_number} {self.order_type} {self.charge_type}"


class ExtraSales(Sales):
    class Meta:
        ordering = ["-created",]
        verbose_name = "기타 매출"
        verbose_name_plural = "기타 매출(들)"
    car_number = models.CharField(
        verbose_name="차량번호", blank=True, null=True, max_length=20)
    day_came_in = models.DateField(verbose_name="입고일", blank=True, null=True)
    expected_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="출고예정일")
    # 나중에 출고시에 추가함
    real_day_came_out = models.DateField(
        blank=True, null=True, verbose_name="실제출고일")
    car_model = models.CharField(
        blank=True, null=True, max_length=90, verbose_name="차종")
    abroad_type = models.CharField(
        blank=True, null=True,
        choices=(("domestic", "국산"), ("imported", "수입")), max_length=10, verbose_name="국산/수입")
    supporter = models.ForeignKey(
        Supporter, verbose_name="입고지원", blank=True, null=True, on_delete=models.SET_NULL, related_name="all_extra_sales")
    insurance_agent = models.ForeignKey(
        InsuranceAgent, related_name="all_extra_sales", null=True, on_delete=models.SET_NULL, verbose_name="보험 담당자")
    client_name = models.CharField(
        blank=True, null=True, verbose_name="고객명", max_length=30)
    phone_number = models.CharField(
        null=True, blank=True, max_length=15, verbose_name="전화번호")
    payment = models.OneToOneField(
        Payment, null=True, blank=True, related_name="extra_sales", verbose_name="결제", on_delete=models.CASCADE)
    charge = models.OneToOneField(
        Charge, null=True, blank=True, related_name="extra_sales", verbose_name="청구", on_delete=models.CASCADE)
    deposit = models.OneToOneField(
        Deposit, null=True, blank=True, related_name="extra_sales", verbose_name="입금", on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True, verbose_name="비고")

    wasted = models.BooleanField(default=False, verbose_name="폐차")
    unrepaired = models.BooleanField(default=False, verbose_name="미수리출고")

    def get_description(self):
        return f"기타매출({self.pk})"

    def to_excel_line(self):
        pass

    def __str__(self):
        return f"({self.day_came_in})입고: {self.note}"
