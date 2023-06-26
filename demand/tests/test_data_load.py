import numpy as np
import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register
from demand.utility import (
    CHARGABLE_AMOUNT, CHARGE_AMOUNT, COMPONENT_TURNOVER, FACTORY_TURNOVER,
    INTEGRATED_TURNOVER, NOT_PAID_AMOUNT, NOT_PAID_TURNOVER, PAID_TURNOVER,
    PAYMENT_RATE, STATUS, TURNOVER, WAGE_TURNOVER,
    check_line_numbers_for_registers_have_same_car_number,
    check_line_numbers_for_registers_have_unique_RO_number,
    check_values_of_column, check_wash_car, df_to_lines,
    get_effective_data_frame, get_effective_row_numbers,
    get_line_numbers_for_extra_sales, get_line_numbers_for_registers,
    get_sales_of_month_and_type, load_data, make_models_from_effective_df,
    zero_if_none)


class DataLoadTest(TestCase):
    """
    이 테스트 클래스는 data_loadxlsx 데이터를 불러와 모든 데이터가 제대로 불려지며, 어떤 위험 요소들이 있는지를 파악해주는 테스트입니다.
    """
    @classmethod
    def setUpClass(cls):
        super(DataLoadTest, cls).setUpClass()
        cls.original_df = load_data("src/data_load.xlsx", "23년 본사 상반기")
        cls.df = get_effective_data_frame(
            "src/data_load.xlsx", "23년 본사 상반기")
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

    def test_get_effective_row_numbers(self):
        pass
        # assert get_effective_row_numbers(self.original_df) == 843

    def test_get_effective_data_frame(self):
        num_rows, _ = self.df.shape
        assert get_effective_row_numbers(self.original_df) == num_rows
        assert "부품매출" == list(self.df.columns)[-1]

    def test_check_wash_car(self):
        # assert check_wash_car(self.df, 660)
        # assert check_wash_car(self.df, 673)
        pass

    def test_get_effective_line_numbers(self):
        check_line_numbers_for_registers_have_same_car_number(self.df)
        check_line_numbers_for_registers_have_unique_RO_number(self.df)
        # assert len(get_line_numbers_for_registers(
        # self.df)) == 156+145+184+174+47

    def test_get_line_numbers_for_extra_sales(self):
        pass
        # assert get_line_numbers_for_extra_sales(self.df) == [660, 673]

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

    def test_monthly_sales(self):
        from datetime import datetime
        current_month = datetime.now().month

        call_command('clean_models')
        make_models_from_effective_df(self.df)
        for month in range(1, current_month+1):
            print(f"Month : {month}")
            print("보험 : ", get_sales_of_month_and_type(month, "보험"))
            print("렌트일반 : ", get_sales_of_month_and_type(month, "렌트일반"))
            print("렌트판도 : ", get_sales_of_month_and_type(month, "렌트판도"))
            print("일반판도 : ", get_sales_of_month_and_type(month, "일반판도"))
            print("일반경정비 : ", get_sales_of_month_and_type(month, "일반경정비"))
            print("--------------")

        # call_command('clean_models')
        # not_charged_df = get_effective_data_frame(
        #     "src/basic.xlsx", "22년 12월 미청구")
        # make_models_from_effective_df(not_charged_df)
        # for month in range(1, current_month+1):
        #     print(f"Month : {month}")
        #     print("보험 : ", get_sales_of_month_and_type(month, "보험"))
        #     print("렌트일반 : ", get_sales_of_month_and_type(month, "렌트일반"))
        #     print("렌트판도 : ", get_sales_of_month_and_type(month, "렌트판도"))
        #     print("일반판도 : ", get_sales_of_month_and_type(month, "일반판도"))
        #     print("일반경정비 : ", get_sales_of_month_and_type(month, "일반경정비"))
        #     print("--------------")

    # def test_status(self):
    #     check_values_of_column(self.df, self.lines, self.line_numbers_for_registers,
    #                            self.line_numbers_for_extra_sales,
    #                            STATUS, "get_status")
