
import pytest
from django.test import TestCase

from demand.excel_load import (
    CHARGABLE_AMOUNT, CHARGE_AMOUNT, CLIENT_NAME_AND_INSURANCE_AGENT,
    COMPONENT_TURNOVER, FACTORY_TURNOVER, INTEGRATED_TURNOVER, NOT_PAID_AMOUNT,
    NOT_PAID_TURNOVER, PAID_TURNOVER, PAYMENT_RATE, TURNOVER, WAGE_TURNOVER,
    check_values_of_column, compare_register_using_line_numbers_for_register,
    df_to_lines, get_client_name_and_insurance_agent_name,
    get_effective_data_frame, get_line_numbers_for_extra_sales,
    get_line_numbers_for_registers,
    get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers,
    load_data, make_extra_sales_from_line, make_models_from_effective_df,
    register_to_tuple)
from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import ExtraSales, Order, Register


@pytest.mark.data_test
class ExcelLoadTest(TestCase):
    """
    이 테스트 클래스는 test.xlsx 데이터를 불러와 utility.py의 함수들과 model들이 전반적으로 잘 작동하는지에 대한 테스트입니다.
    """
    @classmethod
    def setUpClass(cls):
        super(ExcelLoadTest, cls).setUpClass()
        cls.original_df = load_data("src/test.xlsx", "UTILITY_TEST")
        cls.df = get_effective_data_frame(
            "src/test.xlsx", "UTILITY_TEST")
        cls.lines = df_to_lines(cls.df)
        cls.line_numbers_for_extra_sales = get_line_numbers_for_extra_sales(
            cls.df)
        cls.line_numbers_for_registers = get_line_numbers_for_registers(
            cls.df)
        cls.first_lines = [cls.lines[line_numbers_for_register[0]]
                           for line_numbers_for_register in cls.line_numbers_for_registers]
        make_models_from_effective_df(cls.df)
        cls.registers = Register.objects.all()
        cls.orders = Order.objects.all()

    def setUp(self):
        pass

    def test_get_client_name_and_insuranc_agent_name(self):
        """
        보험사와 고객명을 구분이 잘 되는지 확인
        """
        import copy
        empty_list = [None] * 20
        line1 = copy.deepcopy(empty_list)
        line1[CLIENT_NAME_AND_INSURANCE_AGENT] = "김석종/구본준"
        line2 = copy.deepcopy(empty_list)
        line2[CLIENT_NAME_AND_INSURANCE_AGENT] = "구본준담당"
        line3 = copy.deepcopy(empty_list)
        line3[CLIENT_NAME_AND_INSURANCE_AGENT] = "윤석영"
        line4 = copy.deepcopy(empty_list)
        line4[CLIENT_NAME_AND_INSURANCE_AGENT] = ""

        assert ("김석종", "구본준") == get_client_name_and_insurance_agent_name(line1)
        assert (None, "구본준") == get_client_name_and_insurance_agent_name(line2)
        assert (None, "윤석영") == get_client_name_and_insurance_agent_name(line3)
        assert (None, None) == get_client_name_and_insurance_agent_name(line4)

    def test_make_register_from_first_line_number(self):
        """
        Register가 잘 만들어졌는지만 확인합니다.
        """
        test_answers = [("1-1", "60저0130", "2023-01-02", "2023-01-09", "2023-01-13", "320D", "수입",
                         0, 1, "이성도", "김석종", "구본준", "01031370900", "무상7889", None, False, False),
                        ("1-21", "13버6789", "2023-01-03", "2023-01-05", "2023-01-06", "투싼", "국산",
                         0, 2, "이소정(직원)", None, "구본준", "01034361547", "에스렌트", None, False, False),
                        ("1-79", "241마5742", "2023-01-12", "2023-01-20", "2023-01-19", "QM6", "국산",
                         1, 2, "이성도", "김윤희", "구본준", "01048104691", "반디", None, False, False),
                        ("1-100", "60구2264", "2023-01-17", "2023-01-27", "2023-01-31", "렉서스LS460", "수입",
                         3, 0, "장영수", None, "윤석영", "01094034783", "무상4760", None, False, False),
                        ("1-101", "193허2950", "2023-01-20", "2023-01-20", "2023-01-20", "K5", "국산",
                         0, 0, "고객방문", None, None, None, None, None, False, False),
                        ("1-80", "21하3555", "2023-01-02", "2023-02-03", "None", "SM7", "국산",
                         4, 4, "이성도", "김용연", "백준호", "01072230486", "스타렌트", "폐차처리", True, False),
                        ("1-103", "48노5927", "2023-01-21", "2023-01-26", "None", "클리오", "국산",
                         1, 1, "김일한", None, "김장현", "01031717367", "롯데렌탈용인영업소", "미수리출고", False, True)]
        for i, register in enumerate(Register.objects.all().order_by("pk")):
            object_to_tuple = register_to_tuple(register)
            assert object_to_tuple == test_answers[i]
        assert Register.objects.count() == 7

    def test_make_extra_sales_from_effective_df(self):
        assert ExtraSales.objects.count() == 2

    def test_make_models_from_effective_df(self):
        assert Register.objects.count() == 7
        assert ExtraSales.objects.count() == 2
        assert Order.objects.count() == 10
        assert Deposit.objects.count() == 5
        assert Charge.objects.count() == 10
        assert Payment.objects.count() == 6

    def test_compare_register_using_line_numbers_for_register(self):
        """
        실제로 만들어진 Register의 Excel로 들어온 Register를 비교합니다.
        """
        all_equal = True
        for line_numbers_for_register in self.line_numbers_for_registers:
            equal, check_list, RO_number = compare_register_using_line_numbers_for_register(
                self.df, line_numbers_for_register)
            if not equal:
                print(RO_number, check_list)
            all_equal = all_equal and equal
        assert all_equal

    def test_get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers(self):
        """
        실제로 만들어진 Register의 Excel로 들어온 Register를 비교합니다.
        """
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
