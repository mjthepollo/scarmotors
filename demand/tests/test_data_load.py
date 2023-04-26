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
    check_line_numbers_for_registers_have_unique_RO_number,
    check_values_of_column, check_wash_car, df_to_lines,
    get_effective_data_frame, get_effective_row_numbers,
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
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               CHARGABLE_AMOUNT, "get_chargable_amount")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               CHARGABLE_AMOUNT, "get_chargable_amount")

    def test_charge_amount(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               CHARGE_AMOUNT, "get_charge_amount")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               CHARGE_AMOUNT, "get_charge_amount")

    def test_not_paid_amount(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               NOT_PAID_AMOUNT, "get_not_paid_amount")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               NOT_PAID_AMOUNT, "get_not_paid_amount")

    def test_payment_rate(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               PAYMENT_RATE, "get_payment_rate")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               PAYMENT_RATE, "get_payment_rate")

    def test_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               TURNOVER, "get_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               TURNOVER, "get_turnover")

    def test_factory_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               FACTORY_TURNOVER, "get_factory_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               FACTORY_TURNOVER, "get_factory_turnover")

    def test_paid_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               PAID_TURNOVER, "get_paid_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               PAID_TURNOVER, "get_paid_turnover")

    def test_not_paid_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               NOT_PAID_TURNOVER, "get_not_paid_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               NOT_PAID_TURNOVER, "get_not_paid_turnover")

    def test_integrated_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               INTEGRATED_TURNOVER, "get_integrated_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               INTEGRATED_TURNOVER, "get_integrated_turnover")

    def test_component_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               COMPONENT_TURNOVER, "get_component_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               COMPONENT_TURNOVER, "get_component_turnover")

    def test_wage_turnover(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               WAGE_TURNOVER, "get_wage_turnover")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               WAGE_TURNOVER, "get_wage_turnover")

    def test_status(self):
        check_values_of_column(self.df1, self.lines1, self.line_numbers_for_registers1,
                               self.line_numbers_for_extra_sales1,
                               STATUS, "get_status")
        check_values_of_column(self.df2, self.lines2, self.line_numbers_for_registers2,
                               self.line_numbers_for_extra_sales2,
                               STATUS, "get_status")
