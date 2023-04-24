
from datetime import datetime

import numpy as np
import pandas as pd
from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)
from demand.utility import (END,
                            check_effective_line_numbers_have_same_car_number,
                            check_effective_line_numbers_have_unique_RO_number,
                            get_effective_data_frame,
                            get_effective_line_numbers,
                            get_effective_row_numbers, input_to_date,
                            load_data, string_to_date)


class UtilityTest(TestCase):
    def setUp(self):
        # mock up DF 만들어두기
        pass

    def test_string_to_date(self):
        assert string_to_date(
            "2019-01-01") == datetime.date(datetime(2019, 1, 1))
        assert string_to_date(
            "2019.01.01") == datetime.date(datetime(2019, 1, 1))

    def test_make_order_from_effective_df(self):
        pass

    def test_make_order_from_first_line_number(self):
        pass
