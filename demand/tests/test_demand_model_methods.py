from datetime import date
from random import choice, randint

from django.test import TestCase

from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import MockupCreated, Order
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

    def setUpMockup(self):
        self.payment = createRandomPayment()
        self.mockup_payment = Payment.create_mockup()

        self.charge = createRandomCharge()
        self.mockup_charge = Charge.create_mockup()

        self.depoist = createRandomDeposit()
        self.mockup_deposit = Deposit.create_mockup()

    def test_is_mockup(self):
        self.setUpMockup()
        self.assertTrue(self.mockup_payment.is_mockup())
        self.assertFalse(self.payment.is_mockup())
        self.assertTrue(self.mockup_charge.is_mockup())
        self.assertFalse(self.charge.is_mockup())
        self.assertTrue(self.mockup_deposit.is_mockup())
        self.assertFalse(self.depoist.is_mockup())

    def test_get_mockup(self):
        self.assertEqual(self.full_payments,
                         list(self.full_register.get_mockups(Payment, "payment")))
        self.assertTrue(self.not_full_register.get_mockups(
            Payment, "payment")[0].is_mockup())
        self.assertEqual(self.full_charges,
                         list(self.full_register.get_mockups(Charge, "charge")))
        self.assertTrue(self.not_full_register.get_mockups(
            Charge, "charge")[1].is_mockup())
        self.assertEqual(self.full_deposits,
                         list(self.full_register.get_mockups(Deposit, "deposit")))
        self.assertTrue(self.not_full_register.get_mockups(
            Deposit, "deposit")[2].is_mockup())
        self.assertTrue(len(MockupCreated.objects.all()) == 6)

    def test_ordering_of_get_mockup(self):
        full_orders_by_query = Order.objects.filter(
            register=self.full_register)
        full_payment_mockups = self.full_register.get_mockups(
            Payment, "payment")
        full_charge_mockups = self.full_register.get_mockups(
            Charge, "charge")
        full_deposit_mockups = self.full_register.get_mockups(
            Deposit, "deposit")
        for i, payment in enumerate(full_payment_mockups):
            self.assertEqual(payment.order, full_orders_by_query[i])
        for i, charge in enumerate(full_charge_mockups):
            self.assertEqual(charge.order, full_orders_by_query[i])
        for i, full_deposit_mockups in enumerate(full_deposit_mockups):
            self.assertEqual(full_deposit_mockups.order,
                             full_orders_by_query[i])

        not_full_orders_by_query = Order.objects.filter(
            register=self.not_full_register)
        not_full_payment_mockups = self.not_full_register.get_mockups(
            Payment, "payment")
        not_full_charge_mockups = self.not_full_register.get_mockups(
            Charge, "charge")
        not_full_deposit_mockups = self.not_full_register.get_mockups(
            Deposit, "deposit")
        for i, payment in enumerate(not_full_payment_mockups):
            self.assertEqual(payment.order, not_full_orders_by_query[i])
        for i, charge in enumerate(not_full_charge_mockups):
            self.assertEqual(charge.order, not_full_orders_by_query[i])
        for i, not_full_deposit_mockups in enumerate(not_full_deposit_mockups):
            self.assertEqual(not_full_deposit_mockups.order,
                             not_full_orders_by_query[i])

    def test_remove_mockups(self):
        self.not_full_register.get_mockups(
            Payment, "payment")
        self.full_register.remove_mockups(Payment, "payment")
        self.assertEqual(len(Payment.objects.all()), 6)
        self.not_full_register.remove_mockups(Payment, "payment")
        self.assertEqual(len(Payment.objects.all()), 5)
        self.not_full_register.get_mockups(
            Charge, "charge")
        self.full_register.remove_mockups(Charge, "charge")
        self.assertEqual(len(Charge.objects.all()), 6)
        self.not_full_register.remove_mockups(Charge, "charge")
        self.assertEqual(len(Charge.objects.all()), 5)
        self.not_full_register.get_mockups(
            Deposit, "deposit")
        self.full_register.remove_mockups(Deposit, "deposit")
        self.assertEqual(len(Deposit.objects.all()), 6)
        self.not_full_register.remove_mockups(Deposit, "deposit")
        self.assertEqual(len(Deposit.objects.all()), 5)

    def test_mockup_created_remove_all_mockups(self):
        self.not_full_register.get_mockups(
            Payment, "payment")
        self.not_full_register.get_mockups(
            Charge, "charge")
        self.not_full_register.get_mockups(
            Deposit, "deposit")
        self.assertTrue(len(MockupCreated.objects.all()) == 3)
        for mockup in MockupCreated.objects.all():
            mockup.remove_mockups()
        self.assertTrue(len(MockupCreated.objects.all()) == 0)
