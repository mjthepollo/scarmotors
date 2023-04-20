from datetime import datetime

from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, Insurance,
                           InsuranceAgent, Order, Payment, Supporter)


class STRTest(TestCase):

    def setUp(self):
        self.supporter = Supporter.objects.create(name="test_supporter")
        self.charged_company = ChargedCompany.objects.create(
            name="test_charged_company")
        self.insurance_agent = InsuranceAgent.objects.create(
            name="test_insurance_agent")

        payment_date = datetime.strptime("2023-04-20", '%Y-%m-%d').date()
        refund_date = datetime.strptime("2023-04-20", '%Y-%m-%d').date()
        self.payment = Payment.objects.create(indemnity_amount=100000,
                                              discount_amount=10000, payment_type="카드",
                                              payment_info="신한카드", payment_date=payment_date,
                                              refund_amount=10000, refund_date=refund_date)

        charge_date = datetime.strptime("2023-04-20", '%Y-%m-%d').date()
        self.charge = Charge.objects.create(charge_date=charge_date,
                                            repair_amount=100000, component_amount=20000,
                                            indemnity_amount=10000)

        deposit_date = datetime.strptime("2023-04-20", '%Y-%m-%d').date()
        self.deposit = Deposit.objects.create(deposit_date=deposit_date,
                                              deposit_amount=100000)
        day_came_in = datetime.strptime("2023-04-20", '%Y-%m-%d').date()
        expected_day_came_out = datetime.strptime(
            "2023-04-25", '%Y-%m-%d').date()
        real_day_came_out = datetime.strptime("2023-04-27", '%Y-%m-%d').date()
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

    def test_supporter_str(self):
        self.assertEqual(str(self.supporter), "test_supporter")

    def test_charged_company_str(self):
        self.assertEqual(str(self.charged_company), "test_charged_company")

    def test_insurance_agent_str(self):
        self.assertEqual(str(self.insurance_agent), "test_insurance_agent")

    def test_payment_str(self):
        self.assertEqual(str(self.payment), "4-1234 결제")

    def test_charge_str(self):
        self.assertEqual(str(self.charge), "4-1234 청구")

    def test_deposit_str(self):
        self.assertEqual(str(self.deposit), "4-1234 입금")

    def test_order_str(self):
        self.assertEqual(str(self.order), "12가1234/010-1234-5678")

    def test_insurance_str(self):
        self.assertEqual(str(self.insurance), "4-1234 자차 보험")
