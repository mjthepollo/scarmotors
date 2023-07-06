from datetime import date
from random import choice, randint

from dateutil.relativedelta import relativedelta
from django.test import TestCase

from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import Register
from demand.test_utility import (createRandomCharge, createRandomDeposit,
                                 createRandomOrdinaryOrder,
                                 createRandomPayment, createRandomRegister)


class DemandModelMethodTest(TestCase):
    """
    Demand 모델 테스트, 직접 테스트케이스를 만들어서 테스트함
    """

    def setUp(self):
        self.full_register = createRandomRegister()
        self.full_payments = [createRandomPayment() for _ in range(3)]
        self.full_charges = [createRandomCharge() for _ in range(3)]
        self.full_deposits = [createRandomDeposit() for _ in range(3)]
        self.full_orders = [createRandomOrdinaryOrder(self.full_register, 100,
                                                      self.full_payments[i],
                                                      self.full_charges[i],
                                                      self.full_deposits[i]
                                                      ) for i in range(3)]

        self.not_full_register = createRandomRegister()
        self.not_full_payments = [None,
                                  createRandomPayment(), createRandomPayment()]
        self.not_full_charges = [createRandomCharge(),
                                 None, createRandomCharge()]
        self.not_full_deposits = [createRandomDeposit(),
                                  createRandomDeposit(), None]
        self.not_full_orders = [createRandomOrdinaryOrder(self.not_full_register, 100,
                                                          self.not_full_payments[i],
                                                          self.not_full_charges[i],
                                                          self.not_full_deposits[i]
                                                          ) for i in range(3)]

    def test_RO_number(self):
        Register.objects.all().delete()
        last_month = (date.today() - relativedelta(months=1)).month
        current_month = date.today().month
        next_month = (date.today() + relativedelta(months=1)).month

        last_month_registers = [createRandomRegister(f"{last_month}-1")]
        new_last_month_register = createRandomRegister()
        new_last_month_register.set_RO_number(month=last_month)
        self.assertEqual(new_last_month_register.RO_number, f"{last_month}-2")

        current_month_register = createRandomRegister()
        current_month_register.set_RO_number()
        self.assertEqual(current_month_register.RO_number,
                         f"{current_month}-1")

        next_month_registers = [createRandomRegister(
            f"{next_month}-1"), createRandomRegister(f"{next_month}-5")]
        next_month_register = createRandomRegister()
        next_month_register.set_RO_number(month=next_month)
        self.assertEqual(next_month_register.RO_number,
                         f"{next_month}-3")
