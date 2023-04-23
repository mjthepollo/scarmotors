from datetime import datetime

from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, Insurance,
                           InsuranceAgent, Order, Payment, Supporter, WashCar,
                           Wasted)
from demand.utility import string_to_date


class ModelTest(TestCase):

    def setUp(self):
        self.supporter = Supporter.objects.create(name="test_supporter")
        self.charged_company = ChargedCompany.objects.create(
            name="test_charged_company")
        self.insurance_agent = InsuranceAgent.objects.create(
            name="test_insurance_agent")

        payment_date = string_to_date("2023-04-20")
        refund_date = string_to_date("2023-04-20")
        self.payment = Payment.objects.create(indemnity_amount=100000,
                                              discount_amount=10000, payment_type="카드",
                                              payment_info="신한카드", payment_date=payment_date,
                                              refund_amount=10000, refund_date=refund_date)

        charge_date = string_to_date("2023-04-20")
        self.charge = Charge.objects.create(charge_date=charge_date,
                                            repair_amount=100000, component_amount=20000,
                                            indemnity_amount=10000)

        deposit_date = string_to_date("2023-04-20")
        self.deposit = Deposit.objects.create(deposit_date=deposit_date,
                                              deposit_amount=100000)
        day_came_in = string_to_date("2023-04-20")
        expected_day_came_out = datetime.strptime(
            "2023-04-25", '%Y-%m-%d').date()
        real_day_came_out = string_to_date("2023-04-27")
        self.order = Order.objects.create(
            RO_number="4-1234", car_number="12가1234", day_came_in=day_came_in,
            expected_day_came_out=expected_day_came_out, real_day_came_out=real_day_came_out,
            car_model="아반떼", abroad_type="국산", number_of_repair_works=1,
            number_of_exchange_works=2, supporter=self.supporter, client_name="김민준",
            insurance_agent=self.insurance_agent, phone_number="010-1234-5678"
        )

        self.insurance = Insurance.objects.create(
            order=self.order, charged_company=self.charged_company,
            insurance_type="자차", charge_type="보험",
            receipt_number="12-1234", fault_ratio=80,
            payment=self.payment, charge=self.charge, deposit=self.deposit,
            note="test 비고"
        )

        self.wash_car_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                       deposit_amount=100000)
        self.wasted_car_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                         deposit_amount=100000)
        self.wash_car_charge = Charge.objects.create(charge_date=charge_date,
                                                     repair_amount=100000, component_amount=20000,
                                                     indemnity_amount=10000)
        self.wash_car_charge = Charge.objects.create(charge_date=charge_date,
                                                     repair_amount=100000, component_amount=20000,
                                                     indemnity_amount=10000)

        self.wash_car_payment = Payment.objects.create(indemnity_amount=100000,
                                                       discount_amount=10000, payment_type="카드",
                                                       payment_info="삼성카드", payment_date=payment_date,
                                                       refund_amount=10000, refund_date=refund_date)
        self.wasted_car_payment = Payment.objects.create(indemnity_amount=100000,
                                                         discount_amount=10000, payment_type="카드",
                                                         payment_info="현대카드", payment_date=payment_date,
                                                         refund_amount=10000, refund_date=refund_date)

        self.wash_car = WashCar.objects.create(
            payment=self.wash_car_payment, deposit=self.wash_car_deposit,
            charge=self.wash_car_charge, note="test 비고"
        )
        self.wasted = Wasted.objects.create(
            payment=self.wasted_car_payment, deposit=self.wasted_car_deposit,
            charge=self.wash_car_charge, note="test 비고"
        )

    def setUpAbsentCase(self):
        payment_date = string_to_date("2023-04-19")
        refund_date = string_to_date("2023-04-19")
        self.no_insurance_payment = Payment.objects.create(indemnity_amount=100000,
                                                           discount_amount=10000, payment_type="카드",
                                                           payment_info="신한카드", payment_date=payment_date,
                                                           refund_amount=10000, refund_date=refund_date)
        self.no_order_payment = Payment.objects.create(indemnity_amount=100000,
                                                       discount_amount=10000, payment_type="카드",
                                                       payment_info="신한카드", payment_date=payment_date,
                                                       refund_amount=10000, refund_date=refund_date)

        charge_date = string_to_date("2023-04-19")
        self.no_insurance_charge = Charge.objects.create(charge_date=charge_date,
                                                         repair_amount=100000, component_amount=20000,
                                                         indemnity_amount=10000)
        self.no_order_charge = Charge.objects.create(charge_date=charge_date,
                                                     repair_amount=100000, component_amount=20000,
                                                     indemnity_amount=10000)

        deposit_date = string_to_date("2023-04-19")
        self.no_insurance_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                           deposit_amount=100000)
        self.no_order_deposit = Deposit.objects.create(deposit_date=deposit_date,
                                                       deposit_amount=100000)
        self.no_order_insurance = Insurance.objects.create(
            charged_company=self.charged_company,
            insurance_type="자차", charge_type="보험",
            receipt_number="23-2345", fault_ratio=80,
            payment=self.no_order_payment, charge=self.no_order_charge, deposit=self.no_order_deposit,
            note="test 비고"
        )

    def test_supporter_str(self):
        self.assertEqual(str(self.supporter), "test_supporter")

    def test_charged_company_str(self):
        self.assertEqual(str(self.charged_company), "test_charged_company")

    def test_insurance_agent_str(self):
        self.assertEqual(str(self.insurance_agent), "test_insurance_agent")

    def test_payment_str(self):
        self.setUpAbsentCase()
        self.assertEqual(str(self.payment), "4-1234 결제")
        self.assertEqual(str(self.no_order_payment),
                         f"주문없음({self.no_order_payment.pk}_보험:{self.no_order_insurance.pk})")
        self.assertEqual(str(self.no_insurance_payment),
                         f"보험없음({self.no_insurance_payment.pk})")

    def test_charge_str(self):
        self.setUpAbsentCase()
        self.assertEqual(str(self.charge), "4-1234 청구")
        self.assertEqual(str(self.no_order_charge),
                         f"주문없음({self.no_order_charge.pk}_보험:{self.no_order_insurance.pk})")
        self.assertEqual(str(self.no_insurance_charge),
                         f"보험없음({self.no_insurance_charge.pk})")

    def test_deposit_str(self):
        self.setUpAbsentCase()
        self.assertEqual(str(self.deposit), "4-1234 입금")
        self.assertEqual(str(self.no_order_deposit),
                         f"주문없음({self.no_order_deposit.pk}_보험:{self.no_order_insurance.pk})")
        self.assertEqual(str(self.no_insurance_deposit),
                         f"보험없음({self.no_insurance_deposit.pk})")

    def test_order_str(self):
        self.assertEqual(str(self.order), "12가1234/010-1234-5678")

    def test_insurance_str(self):
        self.assertEqual(str(self.insurance), "4-1234 자차 보험")

    def test_get_charge_amount(self):
        self.assertEqual(self.charge.get_charge_amount(), 122000)

    def test_get_payment_rate(self):
        self.assertEqual(self.deposit.get_payment_rate(), 82)

    def test_get_number_of_works(self):
        self.assertEqual(self.order.get_number_of_works(), 3)

    def test_get_RO_number(self):
        self.assertEqual(Order.get_RO_number(), "4-1")
