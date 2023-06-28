from django.test import TestCase

from demand.key_models import Charge, Deposit, Payment
from demand.test_utility import (createRandomCharge, createRandomDeposit,
                                 createRandomPayment)


class TestUtilityTest(TestCase):

    def setUp(self):
        self.payment = createRandomPayment()
        self.mockup_payment = Payment.create_mockup()

        self.charge = createRandomCharge()
        self.mockup_charge = Charge.create_mockup()

        self.depoist = createRandomDeposit()
        self.mockup_deposit = Deposit.create_mockup()
