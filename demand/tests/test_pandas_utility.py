
from datetime import datetime

import numpy as np
import pandas as pd
from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)
from demand.utility import (check_car_number,
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

    def test_input_to_date(self):
        string_date = "2019-01-01"
        date = datetime.date(datetime(2019, 1, 1))
        time_stamp = pd.Timestamp(string_date)
        assert datetime.date(datetime(2019, 1, 1)
                             ) == input_to_date(string_date)
        assert datetime.date(datetime(2019, 1, 1)) == input_to_date(date)
        assert datetime.date(datetime(2019, 1, 1)) == input_to_date(time_stamp)

    def test_check_car_number(self):
        car_numbers = ["165허981", "41허0417", "443버315", "365누173", "391누416",
                       "145하684", "145하684", "309라936", "145하667", "323보689",
                       "160하306", "155허744", "17허0140",]
        not_car_numbers = ["xxxxxx", "123456", "1234", "12345", "1234567"]
        assert all([check_car_number(car_number)
                   for car_number in car_numbers])
        assert all([not check_car_number(not_car_number)
                   for not_car_number in not_car_numbers])

    def test_make_order_from_effective_df(self):
        pass

    def test_make_order_from_first_line_number(self):
        pass
