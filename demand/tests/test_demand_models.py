from datetime import datetime
from random import randint

from django.test import TestCase

from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register
from demand.utility import string_to_date


def createRandomRegister():
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
    return ExtraSales.objects.create(
        day_came_in=string_to_date("2023-04-20"),
        expected_day_came_out=string_to_date("2023-04-25"),
        real_day_came_out=string_to_date("2023-04-26"),
        payment=payment, charge=charge, deposit=deposit
    )


def createRandomInsuranceOrder(register, fault_ratio, payment, charge, deposit):
    return Order.objects.create(
        register=register, charge_type="보험", receipt_number="TEST_RN",
        fault_ratio=fault_ratio, payment=payment, charge=charge, deposit=deposit,
    )


def createRandomOrdinaryOrder(register, fault_ratio, payment, charge, deposit):
    return Order.objects.create(
        register=register, charge_type="일반판도", receipt_number="TEST_RN",
        fault_ratio=fault_ratio, payment=payment, charge=charge, deposit=deposit,
    )


class DemandModelTest(TestCase):
    """
    Demand 모델 테스트, 직접 테스트케이스를 만들어서 테스트함
    """

    def setUp(self):
        self.supporter = Supporter.objects.create(name="test_supporter")
        self.charged_company = ChargedCompany.objects.create(
            name="test_charged_company")
        self.insurance_agent = InsuranceAgent.objects.create(
            name="test_insurance_agent")

        payment_date = string_to_date("2023-04-20")
        refund_date = string_to_date("2023-04-20")
        self.payment = Payment.objects.create(indemnity_amount=50000,
                                              discount_amount=10000, payment_type="카드",
                                              payment_info="신한카드", payment_date=payment_date,
                                              refund_amount=10000, refund_date=refund_date)

        charge_date = string_to_date("2023-04-20")
        self.charge = Charge.objects.create(charge_date=charge_date,
                                            wage_amount=100000, component_amount=20000)

        deposit_date = string_to_date("2023-04-20")
        self.deposit = Deposit.objects.create(deposit_date=deposit_date,
                                              deposit_amount=41000)
        day_came_in = string_to_date("2023-04-20")
        expected_day_came_out = datetime.strptime(
            "2023-04-25", '%Y-%m-%d').date()
        real_day_came_out = string_to_date("2023-04-27")
        self.register = Register.objects.create(
            RO_number="4-1234", car_number="12가1234", day_came_in=day_came_in,
            expected_day_came_out=expected_day_came_out, real_day_came_out=real_day_came_out,
            car_model="아반떼", abroad_type="국산", number_of_repair_works=1,
            number_of_exchange_works=2, supporter=self.supporter, client_name="김민준",
            insurance_agent=self.insurance_agent, phone_number="010-1234-5678"
        )

        self.order = Order.objects.create(
            register=self.register, charged_company=self.charged_company,
            order_type="자차", charge_type="보험",
            receipt_number="12-1234", fault_ratio=80,
            payment=self.payment, charge=self.charge, deposit=self.deposit,
            note="test 비고"
        )

    def setUpAbsentCase(self):
        payment_date = string_to_date("2023-04-19")
        refund_date = string_to_date("2023-04-19")
        self.no_order_payment = Payment.objects.create(indemnity_amount=100000,
                                                       discount_amount=10000, payment_type="카드",
                                                       payment_info="신한카드", payment_date=payment_date,
                                                       refund_amount=10000, refund_date=refund_date)
        self.no_register_payment = Payment.objects.create(indemnity_amount=100000,
                                                          discount_amount=10000, payment_type="카드",
                                                          payment_info="신한카드", payment_date=payment_date,
                                                          refund_amount=10000, refund_date=refund_date)

        charge_date = string_to_date("2023-04-19")
        self.no_order_charge = Charge.objects.create(charge_date=charge_date,
                                                     wage_amount=100000, component_amount=20000)
        self.no_register_charge = Charge.objects.create(charge_date=charge_date,
                                                        wage_amount=100000, component_amount=20000)

        deposit_date = string_to_date("2023-04-19")
        self.no_order_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                       deposit_amount=100000)
        self.no_register_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                          deposit_amount=100000)
        self.no_register_order = Order.objects.create(
            charged_company=self.charged_company,
            order_type="자차", charge_type="보험",
            receipt_number="23-2345", fault_ratio=80,
            payment=self.no_register_payment, charge=self.no_register_charge, deposit=self.no_register_deposit,
            note="test 비고"
        )

    def setUpExtraCase(self):
        payment_date = string_to_date("2023-03-19")
        refund_date = string_to_date("2023-03-19")
        charge_date = string_to_date("2023-03-19")
        deposit_date = string_to_date("2023-03-19")
        self.extra_sales_payment = Payment.objects.create(indemnity_amount=50000,
                                                          discount_amount=10000, payment_type="카드",
                                                          payment_info="삼성카드", payment_date=payment_date,
                                                          refund_amount=10000, refund_date=refund_date)
        self.extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                        wage_amount=100000, component_amount=20000)
        self.extra_sales_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                          deposit_amount=80000)

        self.extra_sales = ExtraSales.objects.create(
            day_came_in=string_to_date("2023-03-20"),
            payment=self.extra_sales_payment, charge=self.extra_sales_charge, deposit=self.extra_sales_deposit,
            note="기타매출"
        )

    def setUpOrderStatusTestCase(self):
        payment_date = string_to_date("2023-03-19")
        refund_date = string_to_date("2023-03-19")
        charge_date = string_to_date("2023-03-19")
        deposit_date = string_to_date("2023-03-19")
        register = createRandomRegister()
        register_without_day_came_out = createRandomRegister()
        register_without_day_came_out.real_day_came_out = None
        register_without_day_came_out.save()

        no_charge_order_payment = Payment.objects.create(indemnity_amount=50000,
                                                         discount_amount=10000, payment_type="카드",
                                                         payment_info="삼성카드", payment_date=payment_date,
                                                         refund_amount=10000, refund_date=refund_date)
        no_charge_order_deposit = Deposit.objects.create(
            deposit_date=deposit_date, deposit_amount=90000)
        self.no_charge_order1 = createRandomInsuranceOrder(
            register, 70, no_charge_order_payment, None, no_charge_order_deposit)
        self.no_charge_order2 = createRandomInsuranceOrder(
            register, 80, None, None, None)

        not_paid_order_charge1 = Charge.objects.create(charge_date=charge_date,
                                                       wage_amount=100000, component_amount=0)
        not_paid_order_charge2 = Charge.objects.create(charge_date=charge_date,
                                                       wage_amount=100000, component_amount=0)
        not_paid_order_payment = Payment.objects.create(indemnity_amount=50000,
                                                        discount_amount=10000, payment_type="카드",
                                                        payment_info="삼성카드", payment_date=payment_date,
                                                        refund_amount=10000, refund_date=refund_date)
        self.not_paid_order1 = createRandomInsuranceOrder(
            register, 100, not_paid_order_payment, not_paid_order_charge1, None)
        self.not_paid_order2 = createRandomInsuranceOrder(
            register, 100, None, not_paid_order_charge2, None)

        no_came_out_order_charge = Charge.objects.create(charge_date=charge_date,
                                                         wage_amount=100000, component_amount=0)
        no_came_out_order_deposit = Deposit.objects.create(
            deposit_date=deposit_date, deposit_amount=100000)
        self.no_came_out_order = createRandomInsuranceOrder(
            register_without_day_came_out, 100, None, no_came_out_order_charge, no_came_out_order_deposit)

        over_deposit_order_charge = Charge.objects.create(charge_date=charge_date,
                                                          wage_amount=100000, component_amount=0)
        over_deposit_order_deposit = Deposit.objects.create(
            deposit_date=deposit_date, deposit_amount=120000)
        self.over_deposit_order = createRandomInsuranceOrder(
            register, 100, None, over_deposit_order_charge, over_deposit_order_deposit)

        complete_order_charge1 = Charge.objects.create(charge_date=charge_date,
                                                       wage_amount=100000, component_amount=0)
        complete_order_charge2 = Charge.objects.create(charge_date=charge_date,
                                                       wage_amount=100000, component_amount=0)
        complete_order_payment = Payment.objects.create(indemnity_amount=120000,
                                                        discount_amount=10000, payment_type="카드",
                                                        payment_info="삼성카드", payment_date=payment_date,
                                                        refund_amount=0, refund_date=refund_date)
        complete_order_deposit = Deposit.objects.create(
            deposit_date=deposit_date, deposit_amount=100000)
        self.complete_order1 = createRandomOrdinaryOrder(
            register, 100, complete_order_payment, complete_order_charge1, None)
        self.complete_order2 = createRandomInsuranceOrder(
            register, 100, None, complete_order_charge2, complete_order_deposit)

        need_check_order_charge1 = Charge.objects.create(charge_date=charge_date,
                                                         wage_amount=100000, component_amount=0)
        need_check_order_charge2 = Charge.objects.create(charge_date=charge_date,
                                                         wage_amount=100000, component_amount=0)
        need_check_order_payment = Payment.objects.create(indemnity_amount=90000,
                                                          discount_amount=0, payment_type="카드",
                                                          payment_info="삼성카드", payment_date=payment_date,
                                                          refund_amount=0, refund_date=refund_date)
        need_check_order_deposit = Deposit.objects.create(
            deposit_date=deposit_date, deposit_amount=60000)
        self.need_check_order1 = createRandomOrdinaryOrder(
            register, 100, need_check_order_payment, need_check_order_charge1, None)
        self.need_check_order2 = createRandomInsuranceOrder(
            register, 100, None, need_check_order_charge2, need_check_order_deposit)

    def setUpExtraSalesStatusTestCase(self):
        payment_date = string_to_date("2023-03-19")
        refund_date = string_to_date("2023-03-19")
        charge_date = string_to_date("2023-03-19")

        no_charge_extra_sales_payment = Payment.objects.create(indemnity_amount=50000,
                                                               discount_amount=10000, payment_type="카드",
                                                               payment_info="삼성카드", payment_date=payment_date,
                                                               refund_amount=10000, refund_date=refund_date)
        self.no_charge_extra_sales1 = createRandomExtraSales(
            no_charge_extra_sales_payment, None, None)
        self.no_charge_extra_sales2 = createRandomExtraSales(None, None, None)

        not_paid_extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                            wage_amount=100000, component_amount=0)
        self.not_paid_extra_sales = createRandomExtraSales(
            None, not_paid_extra_sales_charge, None)

        no_came_out_extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                               wage_amount=100000, component_amount=0)
        no_came_out_extra_sales_payment = Payment.objects.create(indemnity_amount=110000,
                                                                 discount_amount=0, payment_type="카드",
                                                                 payment_info="삼성카드", payment_date=payment_date,
                                                                 refund_amount=0, refund_date=refund_date)
        self.no_came_out_extra_sales = createRandomExtraSales(
            no_came_out_extra_sales_payment, no_came_out_extra_sales_charge, None)
        self.no_came_out_extra_sales.real_day_came_out = None
        self.no_came_out_extra_sales.save()

        over_deposit_extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                                wage_amount=100000, component_amount=0)
        over_deposit_extra_sales_payment = Payment.objects.create(indemnity_amount=115000,
                                                                  discount_amount=0, payment_type="카드",
                                                                  payment_info="삼성카드", payment_date=payment_date,
                                                                  refund_amount=0, refund_date=refund_date)
        self.over_deposit_extra_sales = createRandomExtraSales(
            over_deposit_extra_sales_payment, over_deposit_extra_sales_charge, None)

        complete_extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                            wage_amount=100000, component_amount=0)
        complete_extra_sales_payment = Payment.objects.create(indemnity_amount=110000,
                                                              discount_amount=0, payment_type="카드",
                                                              payment_info="삼성카드", payment_date=payment_date,
                                                              refund_amount=0, refund_date=refund_date)
        self.complete_extra_sales = createRandomExtraSales(
            complete_extra_sales_payment, complete_extra_sales_charge, None)

        need_check_extra_sales_charge = Charge.objects.create(charge_date=charge_date,
                                                              wage_amount=100000, component_amount=0)
        need_check_extra_sales_payment = Payment.objects.create(indemnity_amount=90000,
                                                                discount_amount=0, payment_type="카드",
                                                                payment_info="삼성카드", payment_date=payment_date,
                                                                refund_amount=0, refund_date=refund_date)
        self.need_check_extra_sales = createRandomExtraSales(
            need_check_extra_sales_payment, need_check_extra_sales_charge, None)

    def test_get_work_days(self):
        self.assertEqual(self.register.get_work_days(), 7)

    def test_supporter_str(self):
        self.assertEqual(str(self.supporter), "test_supporter")

    def test_charged_company_str(self):
        self.assertEqual(str(self.charged_company), "test_charged_company")

    def test_insurance_agent_str(self):
        self.assertEqual(str(self.insurance_agent), "test_insurance_agent")

    def test_payment_str(self):
        self.setUpAbsentCase()
        self.setUpExtraCase()
        self.assertEqual(str(self.payment), "RO(4-1234) 주문[0] 결제")
        self.assertEqual(str(self.no_register_payment),
                         f"등록없음({self.no_register_payment.pk}_주문:{self.no_register_order.pk})")
        self.assertEqual(str(self.no_order_payment),
                         f"주문없음({self.no_order_payment.pk})")
        self.assertEqual(str(self.extra_sales_payment),
                         f"기타매출({self.extra_sales.pk}) 결제")

    def test_charge_str(self):
        self.setUpAbsentCase()
        self.setUpExtraCase()
        self.assertEqual(str(self.charge), "RO(4-1234) 주문[0] 청구")
        self.assertEqual(str(self.no_register_charge),
                         f"등록없음({self.no_register_charge.pk}_주문:{self.no_register_order.pk})")
        self.assertEqual(str(self.no_order_charge),
                         f"주문없음({self.no_order_charge.pk})")
        self.assertEqual(str(self.extra_sales_charge),
                         f"기타매출({self.extra_sales.pk}) 청구")

    def test_deposit_str(self):
        self.setUpAbsentCase()
        self.setUpExtraCase()
        self.assertEqual(str(self.deposit), "RO(4-1234) 주문[0] 입금")
        self.assertEqual(str(self.no_register_deposit),
                         f"등록없음({self.no_register_deposit.pk}_주문:{self.no_register_order.pk})")
        self.assertEqual(str(self.no_order_deposit),
                         f"주문없음({self.no_order_deposit.pk})")
        self.assertEqual(str(self.extra_sales_deposit),
                         f"기타매출({self.extra_sales.pk}) 입금")

    def test_register_str(self):
        self.assertEqual(str(self.register), "[4-1234]12가1234/010-1234-5678")

    def test_order_str(self):
        self.assertEqual(str(self.order), "4-1234 자차 보험")

    def test_extra_sales_str(self):
        self.setUpExtraCase()
        self.assertEqual(str(self.extra_sales), "(2023-03-20)입고: 기타매출")

    def test_get_charge_amount(self):
        self.setUpExtraCase()
        self.assertEqual(self.order.get_charge_amount(), 65600)
        self.assertEqual(self.extra_sales.get_charge_amount(), 92000)

    def test_get_payment_rate_for_input(self):
        self.setUpExtraCase()
        self.assertAlmostEqual(
            self.order.get_payment_rate_for_input(), 0.625, places=2)
        self.assertAlmostEqual(
            self.extra_sales.get_payment_rate_for_input(), 0.869, places=2)

    def test_get_number_of_works(self):
        self.assertEqual(self.register.get_number_of_works(), 3)

    def test_get_RO_number(self):
        self.assertEqual(Register.get_RO_number(), f"{datetime.now().month}-1")

    def test_get_order_status(self):
        self.setUpOrderStatusTestCase()
        self.assertEqual(self.no_charge_order1.get_status(),
                         STATUS_DICT["NO_CHARGE"])
        self.assertEqual(self.no_charge_order2.get_status(),
                         STATUS_DICT["NO_CHARGE"])
        self.assertEqual(self.not_paid_order1.get_status(),
                         STATUS_DICT["NOT_PAID"])
        self.assertEqual(self.not_paid_order2.get_status(),
                         STATUS_DICT["NOT_PAID"])
        self.assertEqual(self.no_came_out_order.get_status(),
                         STATUS_DICT["NO_CAME_OUT"])
        self.assertEqual(self.over_deposit_order.get_status(),
                         STATUS_DICT["OVER_DEPOSIT"])
        self.assertEqual(self.complete_order1.get_status(),
                         STATUS_DICT["COMPLETE"])
        self.assertEqual(self.complete_order2.get_status(),
                         STATUS_DICT["COMPLETE"])
        self.assertEqual(self.need_check_order1.get_status(),
                         STATUS_DICT["NEED_CHECK"])
        self.assertEqual(self.need_check_order2.get_status(),
                         STATUS_DICT["NEED_CHECK"])

    def test_get_extra_sales_status(self):
        self.setUpExtraSalesStatusTestCase()
        self.assertEqual(self.no_charge_extra_sales1.get_status(),
                         STATUS_DICT["NO_CHARGE"])
        self.assertEqual(self.no_charge_extra_sales2.get_status(),
                         STATUS_DICT["NO_CHARGE"])
        self.assertEqual(self.not_paid_extra_sales.get_status(),
                         STATUS_DICT["NOT_PAID"])
        self.assertEqual(self.no_came_out_extra_sales.get_status(),
                         STATUS_DICT["NO_CAME_OUT"])
        self.assertEqual(
            self.over_deposit_extra_sales.get_status(), STATUS_DICT["OVER_DEPOSIT"])
        self.assertEqual(self.complete_extra_sales.get_status(),
                         STATUS_DICT["COMPLETE"])
        self.assertEqual(self.need_check_extra_sales.get_status(),
                         STATUS_DICT["NEED_CHECK"])
