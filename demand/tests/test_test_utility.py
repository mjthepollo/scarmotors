from django.test import TestCase

from demand.key_models import Charge, Deposit, Payment
from demand.test_utility import (createRandomCharge, createRandomDeposit,
                                 createRandomPayment)


class TestUtilityTest(TestCase):

    def setUp(self):
        pass
