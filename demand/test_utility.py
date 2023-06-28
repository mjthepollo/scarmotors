from datetime import date
from random import choice, randint

from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import ExtraSales, Order, Register
from demand.utility import string_to_date


def createRandomRegister():
    """
    테스트를 위해 Random한 Register를 만듭니다.
    """
    randint(1, 9)
    car_number = "RANDOM"
    RO_number = f"TEST_RO"
    return Register.objects.create(
        RO_number=RO_number, car_number=car_number,
        day_came_in=string_to_date("2023-04-20"),
        expected_day_came_out=string_to_date("2023-04-25"), real_day_came_out=string_to_date("2023-04-26"),
        car_model="아반떼", abroad_type="국산",
        number_of_repair_works=randint(0, 4), number_of_exchange_works=randint(0, 4), client_name="김민준",
        phone_number="010-1234-5678")


def createRandomExtraSales(payment, charge, deposit):
    """
    테스트를 위해 Random한 ExtraSales를 만듭니다.
    """
    return ExtraSales.objects.create(
        day_came_in=string_to_date("2023-04-20"),
        expected_day_came_out=string_to_date("2023-04-25"),
        real_day_came_out=string_to_date("2023-04-26"),
        payment=payment, charge=charge, deposit=deposit
    )


def createRandomInsuranceOrder(register, fault_ratio, payment, charge, deposit):
    """
    테스트를 위해 Random한 보험 타입 Order를 만듭니다.
    """
    return Order.objects.create(
        register=register, charge_type="보험", receipt_number="TEST_RN",
        fault_ratio=fault_ratio, payment=payment, charge=charge, deposit=deposit,
    )


def createRandomOrdinaryOrder(register, fault_ratio, payment, charge, deposit):
    """
    테스트를 위해 Random한 일반판도 or 일반경정비 타입 Order를 만듭니다.
    """
    return Order.objects.create(
        register=register, charge_type=choice(["일반경정비", "일반판도"]), receipt_number="TEST_RN",
        fault_ratio=fault_ratio, payment=payment, charge=charge, deposit=deposit,
    )


def createRandomPayment():
    return Payment.objects.create(indemnity_amount=randint(1, 9)*100000,
                                  discount_amount=randint(1, 9)*100000,
                                  payment_type="카드", payment_info="신한카드",
                                  payment_date=date.today())


def createRandomCharge():
    return Charge.objects.create(charge_date=date.today(),
                                 wage_amount=randint(1, 9)*100000,
                                 component_amount=randint(1, 9)*100000)


def createRandomDeposit():
    return Deposit.objects.create(deposit_date=date.today(),
                                  deposit_amount=randint(1, 9)*100000)
