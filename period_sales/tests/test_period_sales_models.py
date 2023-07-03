from django.test import TestCase

from demand.test_utility import (createRandomCharge, createRandomDeposit,
                                 createRandomOrdinaryOrder,
                                 createRandomPayment, createRandomRegister)


class PeriodSalesModelTest(TestCase):
    """
    PeriodSales 모델 테스트, 직접 테스트케이스를 만들어서 테스트함
    """

    def setUp(self):
        self.register = createRandomRegister()
        self.payment = createRandomPayment()
        self.charge = createRandomCharge()
        self.deposit = createRandomDeposit()
        self.order = createRandomOrdinaryOrder(
            self.register, 100, self.payment, self.charge, self.deposit)

    def test_order_update(self):
        """
        KeyModel들을 업데이트 할때도 Order의 updated가 업데이트 되는지 확인
        """
        print("")
        print(f"ORDER UPDATED:{self.order.updated}  PAYMENT_UPDATED:{self.payment.updated}\
              CHARGE_UPDATED:{self.charge.updated}  DEPOSIT_UPDATED:{self.deposit.updated}")
        order_updated_before_payment_save = self.order.updated
        self.payment.indemnity_amount = 100
        self.payment.save()
        order_updated_after_payment_save = self.order.updated
        self.assertTrue(order_updated_before_payment_save <
                        order_updated_after_payment_save)
        print(f"ORDER UPDATED:{self.order.updated}  PAYMENT_UPDATED:{self.payment.updated}\
              CHARGE_UPDATED:{self.charge.updated}  DEPOSIT_UPDATED:{self.deposit.updated}")
        order_updated_before_charge_save = self.order.updated
        self.charge.charge_amount = 100
        self.charge.save()
        order_updated_after_charge_save = self.order.updated
        self.assertTrue(order_updated_before_charge_save <
                        order_updated_after_charge_save)
        print(f"ORDER UPDATED:{self.order.updated}  PAYMENT_UPDATED:{self.payment.updated}\
              CHARGE_UPDATED:{self.charge.updated}  DEPOSIT_UPDATED:{self.deposit.updated}")
        order_updated_before_deposit_save = self.order.updated
        self.deposit.deposit_amount = 100
        self.deposit.save()
        order_updated_after_deposit_save = self.order.updated
        self.assertTrue(order_updated_before_deposit_save <
                        order_updated_after_deposit_save)

        print(f"ORDER UPDATED:{self.order.updated}  PAYMENT_UPDATED:{self.payment.updated}\
              CHARGE_UPDATED:{self.charge.updated}  DEPOSIT_UPDATED:{self.deposit.updated}")
