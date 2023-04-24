
from datetime import datetime

import numpy as np
import pandas as pd
from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)
from demand.utility import (END,
                            check_effective_line_numbers_have_same_car_number,
                            check_effective_line_numbers_have_unique_RO_number,
                            check_wash_car, get_effective_data_frame,
                            get_effective_line_numbers,
                            get_effective_row_numbers, input_to_date,
                            load_data, string_to_date)


class DataLoadTest(TestCase):

    def setUp(self):
        self.original_df1 = load_data("src/basic.xlsx", "23년 본사 상반기")
        self.effective_df1 = get_effective_data_frame(
            "src/basic.xlsx", "23년 본사 상반기")
        self.original_df2 = load_data("src/230417.xlsx", "23년 본사 상반기")
        self.effective_df2 = get_effective_data_frame(
            "src/230417.xlsx", "23년 본사 상반기")

    def test_load_data(self):
        assert type(pd.DataFrame()) == type(self.original_df1)
        assert type(pd.DataFrame()) == type(self.original_df2)

    def test_get_effective_row_numbers(self):
        assert get_effective_row_numbers(self.original_df1) == 242
        assert get_effective_row_numbers(self.original_df2) == 699

    def test_get_effective_data_frame(self):
        num_rows1, _ = self.effective_df1.shape
        num_rows2, _ = self.effective_df2.shape
        assert get_effective_row_numbers(self.original_df1) == num_rows1
        assert get_effective_row_numbers(self.original_df2) == num_rows2
        assert "부품매출" == list(self.effective_df1.columns)[-1]
        assert "부품매출" == list(self.effective_df2.columns)[-1]

    def test_check_wash_car(self):
        assert not check_wash_car(self.effective_df1, 1)
        assert not check_wash_car(self.effective_df1, 10)
        assert check_wash_car(self.effective_df2, 659)
        assert check_wash_car(self.effective_df2, 671)

    def test_get_effective_line_numbers(self):
        check_effective_line_numbers_have_unique_RO_number(self.effective_df1)
        check_effective_line_numbers_have_unique_RO_number(self.effective_df2)
        check_effective_line_numbers_have_same_car_number(self.effective_df1)
        check_effective_line_numbers_have_same_car_number(self.effective_df2)
        assert len(get_effective_line_numbers(self.effective_df1)) == 157+24
        assert len(get_effective_line_numbers(
            self.effective_df2)) == 156+145+184+99
