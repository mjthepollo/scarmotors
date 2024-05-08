from datetime import datetime

import numpy as np
import pandas as pd
import pytest
from django.test import TestCase

from demand.utility import (check_car_number, fault_ratio_to_int,
                            input_to_date, input_to_phone_number, int_or_none,
                            str_or_none, string_to_date)


@pytest.mark.unit_test
class UtilityTest(TestCase):
    """
    이 테스트 클래스는 가장 기본적인 utility functions들을 테스트합니다.
    """

    def test_int_or_none(self):
        assert int_or_none(10) == 10
        assert int_or_none("10") == 10
        assert int_or_none("") == None
        assert int_or_none(None) == None

    def test_str_or_none(self):
        assert str_or_none(10) == "10"
        assert str_or_none("10") == "10"
        assert str_or_none("") == None
        assert str_or_none(None) == None

    def test_string_to_date(self):
        date = datetime.date(datetime(2019, 1, 1))
        assert string_to_date("2019-01-01") == date
        assert string_to_date("2019.01.01") == date
        assert string_to_date("190101") == date

    def test_input_to_phone_number(self):
        assert input_to_phone_number(None) == None
        assert input_to_phone_number("010-9403-4783") == "01094034783"
        assert input_to_phone_number(1094034783) == "01094034783"

    def test_fault_ratio_percent_to_int(self):
        assert None == fault_ratio_to_int("")
        assert 15 == fault_ratio_to_int("15%")
        assert 15 == fault_ratio_to_int("15")
        assert 15 == fault_ratio_to_int(15)
        assert 15 == fault_ratio_to_int(0.15)

    def test_input_to_date(self):
        string_date = "2019-01-01"
        date = datetime.date(datetime(2019, 1, 1))
        time_stamp = pd.Timestamp(string_date)
        assert date == input_to_date(string_date)
        assert date == input_to_date(date)
        assert date == input_to_date(time_stamp)
        assert date == input_to_date("190101")
        assert date == input_to_date(190101)
        assert date == input_to_date(190101.0)

    def test_check_car_number(self):
        car_numbers = ["165허981", "41허0417", "443버315", "365누173", "391누416",
                       "145하684", "145하684", "309라936", "145하667", "323보689",
                       "160하306", "155허744", "17허0140",]
        not_car_numbers = ["xxxxxx", "123456", "1234", "12345", "1234567"]
        assert all([check_car_number(car_number)
                   for car_number in car_numbers])
        assert all([not check_car_number(not_car_number)
                   for not_car_number in not_car_numbers])
