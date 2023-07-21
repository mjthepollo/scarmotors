import numpy as np
import pandas as pd
import pytest
from django.core.management import call_command
from django.test import TestCase

from demand.excel_load import (
    CHARGABLE_AMOUNT, CHARGE_AMOUNT, COMPONENT_TURNOVER, FACTORY_TURNOVER,
    INTEGRATED_TURNOVER, NOT_PAID_AMOUNT, NOT_PAID_TURNOVER, PAID_TURNOVER,
    PAYMENT_RATE, TURNOVER, WAGE_TURNOVER,
    check_line_numbers_for_registers_have_same_car_number,
    check_line_numbers_for_registers_have_unique_RO_number,
    check_values_of_column, compare_register_using_line_numbers_for_register,
    df_to_lines, get_client_name_and_insurance_agent_name,
    get_effective_data_frame, get_line_numbers,
    get_line_numbers_for_extra_sales, get_line_numbers_for_registers,
    get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers,
    load_data, make_extra_sales_from_line, make_models_from_effective_df)
from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import ExtraSales, Order, Register


class DataLoadTest(TestCase):
    """
    이 테스트 클래스는 data_loadxlsx 데이터를 불러와 모든 데이터가 제대로 불려지며, 어떤 위험 요소들이 있는지를 파악해주는 테스트입니다.
    """
    @classmethod
    def setUpClass(cls):
        super(DataLoadTest, cls).setUpClass()
        file_name = "src/data_load.xlsx"
        sheet_name = "22년 12월 미청구"
        # sheet_name = "23년 본사 상반기"
        # sheet_name = "23년 본사 하반기"
        cls.original_df = load_data(file_name, sheet_name)
        cls.df = get_effective_data_frame(
            file_name, sheet_name)
        cls.lines = df_to_lines(cls.df)
        cls.line_numbers_for_extra_sales = get_line_numbers_for_extra_sales(
            cls.df)
        cls.line_numbers_for_registers = get_line_numbers_for_registers(
            cls.df)

    def setUp(self):
        pass

    def test_load_data(self):
        assert type(pd.DataFrame()) == type(self.original_df)
        assert len(self.lines) == len(self.df)

    @pytest.mark.skip(reason="Line numbers are easily changed")
    def test_get_line_numbers(self):
        # 계산법은 excel기준 마지막줄의 index에서 6을 빼주면 된다.
        assert get_line_numbers(self.original_df) == 1181

    def test_get_effective_data_frame(self):
        num_rows, _ = self.df.shape
        assert get_line_numbers(self.original_df) == num_rows
        assert "부품매출" == list(self.df.columns)[-1]

    def test_get_effective_line_numbers(self):
        check_line_numbers_for_registers_have_same_car_number(self.df)
        check_line_numbers_for_registers_have_unique_RO_number(self.df)

    def test_get_line_numbers_for_extra_sales(self):
        # 폐차, 미수리출고, 세차의 경우의 line_numbers를 구한다. 이는 말그대로 line_numbers이므로, index 기준에서 6을 빼줘야 한다.
        # assert get_line_numbers_for_extra_sales(self.df) == [660, 673]
        pass

    def test_compare_register_using_line_numbers_for_register(self):
        """
        실제로 만들어진 Register의 Excel로 들어온 Register를 비교합니다.
        """
        make_models_from_effective_df(self.df)
        all_equal = True
        for line_numbers_for_register in self.line_numbers_for_registers:
            equal, check_list = compare_register_using_line_numbers_for_register(
                self.df, line_numbers_for_register)
            if not equal:
                print(check_list)
            all_equal = all_equal and equal
        assert all_equal

    def test_get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers(self):
        """
        실제로 만들어진 Register의 Excel로 들어온 Register를 비교합니다.
        """
        make_models_from_effective_df(self.df)
        list_of_check_list = get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers(
            self.df, self.line_numbers_for_registers)
        assert len(list_of_check_list) == 0

    def test_chargable_amount(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               CHARGABLE_AMOUNT, "get_chargable_amount")

    def test_charge_amount(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               CHARGE_AMOUNT, "get_charge_amount")

    def test_not_paid_amount(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               NOT_PAID_AMOUNT, "get_not_paid_amount")

    def test_payment_rate_for_input(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               PAYMENT_RATE, "get_payment_rate_for_input")

    def test_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               TURNOVER, "get_turnover")

    def test_factory_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               FACTORY_TURNOVER, "get_factory_turnover")

    def test_paid_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               PAID_TURNOVER, "get_paid_turnover")

    def test_not_paid_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               NOT_PAID_TURNOVER, "get_not_paid_turnover")

    def test_integrated_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               INTEGRATED_TURNOVER, "get_integrated_turnover")

    def test_component_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               COMPONENT_TURNOVER, "get_component_turnover")

    def test_wage_turnover(self):
        check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
                               self.line_numbers_for_extra_sales,
                               WAGE_TURNOVER, "get_wage_turnover")
