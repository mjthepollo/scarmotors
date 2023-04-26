import numpy as np
import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, ExtraSales,
                           InsuranceAgent, Order, Payment, Register, Supporter)
from demand.utility import (
    CHARGABLE_AMOUNT, CHARGE_AMOUNT, COMPONENT_TURNOVER, FACTORY_TURNOVER,
    INTEGRATED_TURNOVER, NOT_PAID_AMOUNT, NOT_PAID_TURNOVER, PAID_TURNOVER,
    PAYMENT_RATE, STATUS, TURNOVER, WAGE_TURNOVER,
    check_line_numbers_for_registers_have_same_car_number,
    check_line_numbers_for_registers_have_unique_RO_number, check_wash_car,
    df_to_lines, get_effective_data_frame, get_effective_row_numbers,
    get_line_numbers_for_extra_sales, get_line_numbers_for_registers,
    load_data, make_models_from_effective_df, zero_if_none)


class DataLoadTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DataLoadTest, cls).setUpClass()
        cls.original_df1 = load_data("src/basic.xlsx", "23년 본사 상반기")
        cls.df1 = get_effective_data_frame(
            "src/basic.xlsx", "23년 본사 상반기")
        cls.original_df2 = load_data("src/230417.xlsx", "23년 본사 상반기")
        cls.df2 = get_effective_data_frame(
            "src/230417.xlsx", "23년 본사 상반기")
        cls.lines1 = df_to_lines(cls.df1)
        cls.lines2 = df_to_lines(cls.df2)
        cls.line_numbers_for_extra_sales1 = get_line_numbers_for_extra_sales(
            cls.df1)
        cls.line_numbers_for_extra_sales2 = get_line_numbers_for_extra_sales(
            cls.df2)
        cls.line_numbers_for_registers1 = get_line_numbers_for_registers(
            cls.df1)
        cls.line_numbers_for_registers2 = get_line_numbers_for_registers(
            cls.df2)

    def setUp(self):
        pass

    def test_load_data(self):
        assert type(pd.DataFrame()) == type(self.original_df1)
        assert type(pd.DataFrame()) == type(self.original_df2)
        assert len(self.lines1) == len(self.df1)
        assert len(self.lines2) == len(self.df2)

    def test_get_effective_row_numbers(self):
        assert get_effective_row_numbers(self.original_df1) == 242
        assert get_effective_row_numbers(self.original_df2) == 699

    def test_get_effective_data_frame(self):
        num_rows1, _ = self.df1.shape
        num_rows2, _ = self.df2.shape
        assert get_effective_row_numbers(self.original_df1) == num_rows1
        assert get_effective_row_numbers(self.original_df2) == num_rows2
        assert "부품매출" == list(self.df1.columns)[-1]
        assert "부품매출" == list(self.df2.columns)[-1]

    def test_check_wash_car(self):
        assert not check_wash_car(self.df1, 1)
        assert not check_wash_car(self.df1, 10)
        assert check_wash_car(self.df2, 659)
        assert check_wash_car(self.df2, 671)

    def test_get_effective_line_numbers(self):
        check_line_numbers_for_registers_have_same_car_number(
            self.df1)
        check_line_numbers_for_registers_have_same_car_number(
            self.df2)
        check_line_numbers_for_registers_have_unique_RO_number(
            self.df1)
        check_line_numbers_for_registers_have_unique_RO_number(
            self.df2)
        assert len(get_line_numbers_for_registers(
            self.df1)) == 157+24
        assert len(get_line_numbers_for_registers(
            self.df2)) == 156+145+184+99

    def test_get_line_numbers_for_extra_sales(self):
        assert get_line_numbers_for_extra_sales(self.df1) == []
        assert get_line_numbers_for_extra_sales(
            self.df2) == [659, 671]

    def test_chargable_amount(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df1)
        for i, line_number in enumerate(self.line_numbers_for_extra_sales1):
            extra_sales = ExtraSales.objects.all()[i]
            chargable_amount = extra_sales.get_chargable_amount()
            chargable_amount_value = self.lines[line_number][CHARGABLE_AMOUNT]
            if extra_sales.charge:
                assert abs(chargable_amount_value - chargable_amount) < 10
            else:
                if isinstance(chargable_amount_value, (float, int)):
                    assert chargable_amount_value == 0.0
                    assert chargable_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers2 for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            chargable_amount = order.get_chargable_amount()
            chargable_amount_value = self.lines[line_number][CHARGABLE_AMOUNT]
            if order.charge:
                assert abs(chargable_amount_value - chargable_amount) < 10
            else:
                if isinstance(chargable_amount_value, (float, int)):
                    assert chargable_amount_value == 0.0
                    assert chargable_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError

        call_command("clean_models")
        make_models_from_effective_df(self.df2)
        for i, line_number in enumerate(self.line_numbers_for_extra_sales2):
            extra_sales = ExtraSales.objects.all()[i]
            chargable_amount = extra_sales.get_chargable_amount()
            chargable_amount_value = self.lines[line_number][CHARGABLE_AMOUNT]
            if extra_sales.charge:
                assert abs(chargable_amount_value - chargable_amount) < 10
            else:
                if isinstance(chargable_amount_value, (float, int)):
                    assert chargable_amount_value == 0.0
                    assert chargable_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError

        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers2 for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            chargable_amount = order.get_chargable_amount()
            chargable_amount_value = self.lines[line_number][CHARGABLE_AMOUNT]
            if order.charge:
                assert abs(chargable_amount_value - chargable_amount) < 10
            else:
                if isinstance(chargable_amount_value, (float, int)):
                    assert chargable_amount_value == 0.0
                    assert chargable_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError

    def test_charge_amount(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df1)
        for i, line_number in enumerate(self.line_numbers_for_extra_sales1):
            extra_sales = ExtraSales.objects.all()[i]
            charge_amount = extra_sales.get_charge_amount()
            charge_amount_value = self.lines[line_number][CHARGE_AMOUNT]
            if extra_sales.charge:
                assert abs(charge_amount_value - charge_amount) < 10
            else:
                if isinstance(charge_amount_value, (float, int)):
                    assert charge_amount_value == 0.0
                    assert charge_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers2 for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            charge_amount = order.get_charge_amount()
            charge_amount_value = self.lines[line_number][CHARGE_AMOUNT]
            if order.charge:
                assert abs(charge_amount_value - charge_amount) < 10
            else:
                if isinstance(charge_amount_value, (float, int)):
                    assert charge_amount_value == 0.0
                    assert charge_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError
        call_command("clean_models")
        make_models_from_effective_df(self.df)
        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            extra_sales = ExtraSales.objects.all()[i]
            charge_amount = extra_sales.get_charge_amount()
            charge_amount_value = self.lines[line_number][CHARGE_AMOUNT]
            if extra_sales.charge:
                assert abs(charge_amount_value - charge_amount) < 10
            else:
                if isinstance(charge_amount_value, (float, int)):
                    assert charge_amount_value == 0.0
                    assert charge_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            charge_amount = order.get_charge_amount()
            charge_amount_value = self.lines[line_number][CHARGE_AMOUNT]
            if order.charge:
                assert abs(charge_amount_value - charge_amount) < 10
            else:
                if isinstance(charge_amount_value, (float, int)):
                    assert charge_amount_value == 0.0
                    assert charge_amount == None
                else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
                    raise AssertionError

    def test_not_paid_amount(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            extra_sales = ExtraSales.objects.all()[i]
            not_paid_amount = extra_sales.get_not_paid_amount()
            not_paid_amount_value = self.lines[line_number][NOT_PAID_AMOUNT]
            assert abs(not_paid_amount_value - not_paid_amount) < 10

        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            not_paid_amount = order.get_not_paid_amount()
            not_paid_amount_value = self.lines[line_number][NOT_PAID_AMOUNT]
            assert abs(not_paid_amount_value - not_paid_amount) < 10

    def test_payment_rate(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)
        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            extra_sales = ExtraSales.objects.all()[i]
            payment_rate = extra_sales.get_payment_rate()
            payment_rate_value = self.lines[line_number][PAYMENT_RATE]
            if payment_rate:
                assert abs(payment_rate_value - payment_rate) <= 0.01
            else:
                assert payment_rate_value == None
                assert payment_rate == None

        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            order = Order.objects.all()[i]
            payment_rate = order.get_payment_rate()
            payment_rate_value = self.lines[line_number][PAYMENT_RATE]
            if payment_rate:
                assert abs(payment_rate_value - payment_rate) <= 0.01
            else:
                assert payment_rate_value == None
                assert payment_rate == None

    def test_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][TURNOVER]) - ExtraSales.objects.all()[
                i].get_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][TURNOVER]) - Order.objects.all()[
                i].get_turnover()) < 10

    def test_factory_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][FACTORY_TURNOVER]) - ExtraSales.objects.all()[
                i].get_factory_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][FACTORY_TURNOVER]) - Order.objects.all()[
                i].get_factory_turnover()) < 10

    def test_paid_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][PAID_TURNOVER]) - ExtraSales.objects.all()[
                i].get_paid_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][PAID_TURNOVER]) - Order.objects.all()[
                i].get_paid_turnover()) < 10

    def test_not_paid_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][NOT_PAID_TURNOVER]) - ExtraSales.objects.all()[
                i].get_not_paid_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][NOT_PAID_TURNOVER]) - Order.objects.all()[
                i].get_not_paid_turnover()) < 10

    def test_integrated_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][INTEGRATED_TURNOVER]) - ExtraSales.objects.all()[
                i].get_integrated_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][INTEGRATED_TURNOVER]) - Order.objects.all()[
                i].get_integrated_turnover()) < 10

    def test_component_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][COMPONENT_TURNOVER]) - ExtraSales.objects.all()[
                i].get_component_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][COMPONENT_TURNOVER]) - Order.objects.all()[
                i].get_component_turnover()) < 10

    def test_wage_turnover(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert abs(zero_if_none(self.lines[line_number][WAGE_TURNOVER]) - ExtraSales.objects.all()[
                i].get_wage_turnover()) < 10
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert abs(zero_if_none(self.lines[line_number][WAGE_TURNOVER]) - Order.objects.all()[
                i].get_wage_turnover()) < 10

    def test_status(self):
        call_command("clean_models")
        make_models_from_effective_df(self.df)

        for i, line_number in enumerate(self.line_numbers_for_extra_sales):
            assert self.lines[line_number][STATUS] == ExtraSales.objects.all()[
                i].get_status()
        for i, line_number in enumerate([line_number for line_numbers_for_register in self.line_numbers_for_registers for line_number in line_numbers_for_register]):
            assert self.lines[line_number][STATUS] == Order.objects.all()[
                i].get_status()
