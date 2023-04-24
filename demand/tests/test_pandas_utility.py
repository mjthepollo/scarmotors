
from datetime import datetime

import numpy as np
import pandas as pd
from django.test import TestCase

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)
from demand.utility import (check_car_number, check_wash_car,
                            fault_ratio_to_int,
                            get_client_name_and_insurance_agent_name,
                            get_effective_data_frame,
                            get_effective_row_numbers,
                            get_line_numbers_for_registers, get_refund_date,
                            input_to_date, load_data, string_to_date)


class UtilityTest(TestCase):
    def setUp(self):
        # mock up DF 만들어두기
        self.lines = [['0123', None, '1-1', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), datetime(2023, 1, 13, 0, 0), 11.0, '60저0130', '320D', '수입', None, 1.0, 1.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881890', 0.4, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 248740.80000000002, '무상7889', 392000.0, None, None, '카드', '우리', pd.Timestamp('2023-01-13 00:00:00'), 0.0, None, None, None, None, 0.0, None, 392000.0, 35636.36363636365, 356363.63636363635, None, None, '완료', None, None, 1.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0],
                      ['0106', None, '1-21', pd.Timestamp('2023-01-03 00:00:00'), pd.Timestamp('2023-01-05 00:00:00'), datetime(2023, 1, 6, 0, 0), 3.0, '13버6789', '투싼', '국산', None, 2.0, 2.0, '이소정(직원)', '구본준담당', 1034361547, '보험', 'DB', '대물', '22-7868188', 1.0, 1.0, 230106.0, 539919.0, 28262.0, 568181.0, 56818.100000000006,
                       624999.1000000001, '에스렌트', None, None, None, None, None, None, 624999.1000000001, 1.0, 230106.0, 620076.0, 0.9921230286571611, 0.0, 0.007876971342838934, 620076.0, 56370.54545454553, 563705.4545454545, None, None, '완료', None, None, 1.0, 563705.4545454545, 0.0, 563705.4545454545, 0.0, 535443.4545454545, 28262.0],
                      [None, None, '1-79', pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 19, 0, 0), 7.0, '241마5742', 'QM6', '국산', 1.0, 2.0, 3.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', 'DB', '자차', '23-00330599', None, None, None, None, None, 0.0, 0.0,
                       0.0, '반디', 500000.0, None, 300000.0, '은행', '하나', pd.Timestamp('2023-01-19 00:00:00'), 0.0, None, None, None, None, 0.0, None, 200000.0, 18181.818181818206, 181818.1818181818, None, None, '완료', None, None, 1.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0],
                      [None, None, None, pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), None, 8.0, '241마5742', 'QM6', '국산', None, None, 0.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', '삼성', '대물', '230112-1425',
                       None, None, None, None, None, 0.0, 0.0, 0.0, None, None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, None, '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      ['0131', None, '1-100', pd.Timestamp('2023-01-17 00:00:00'), pd.Timestamp('2023-01-27 00:00:00'), datetime(2023, 1, 31, 0, 0), 14.0, '60구2264', '렉서스LS460', '수입', 3.0, None, 3.0, '장영수', '윤석영', '010-9403-4783', '보험', '하나손해', '대물', '1-5008', 1.0, 1.0, 230131.0, 2323181.818181818, None,
                       2323181.818181818, 232318.1818181818, 2555500.0, '무상4760', None, None, None, None, None, None, 2555500.0, 2.0, 230202.0, 2420000.0, 0.9469771081980043, 0.0, 0.05302289180199571, 2420000.0, 220000.0, 2200000.0, None, None, '완료', None, None, 1.0, 2200000.0, 0.0, 2200000.0, 0.0, 2200000.0, 0.0],
                      ['0120', None, '1-101', pd.Timestamp('2023-01-20 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 20, 0, 0), 0.0, '193허2950', 'K5', '국산', None, None, 0.0, '고객', None, None, '일반경정비', '일반경정비', None, '타이어펑크수리', 1.0, 1.0, 230120.0, 9090.90909090909, None, 9090.90909090909, 909.090909090909, 10000.0, None, 10000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-20 00:00:00'), 0.0, None, None, None, None, 0.0, None, 10000.0, 909.0909090909099, 9090.90909090909, None, None, '완료', '일반경정비', None, 1.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0]]

    def test_string_to_date(self):
        assert string_to_date(
            "2019-01-01") == datetime.date(datetime(2019, 1, 1))
        assert string_to_date(
            "2019.01.01") == datetime.date(datetime(2019, 1, 1))

    def test_fault_ratio_percent_to_int(self):
        assert 0 == fault_ratio_to_int("")
        assert 15 == fault_ratio_to_int("15%")
        assert 15 == fault_ratio_to_int("15")
        assert 15 == fault_ratio_to_int(15)

    def test_input_to_date(self):
        string_date = "2019-01-01"
        date = datetime.date(datetime(2019, 1, 1))
        time_stamp = pd.Timestamp(string_date)
        assert datetime.date(datetime(2019, 1, 1)
                             ) == input_to_date(string_date)
        assert datetime.date(datetime(2019, 1, 1)) == input_to_date(date)
        assert datetime.date(datetime(2019, 1, 1)) == input_to_date(time_stamp)

    def test_get_refund_date(self):
        assert get_refund_date(self.lines[0]) == None
        assert get_refund_date(self.lines[2]) == string_to_date("2023-1-19")

    def test_check_car_number(self):
        car_numbers = ["165허981", "41허0417", "443버315", "365누173", "391누416",
                       "145하684", "145하684", "309라936", "145하667", "323보689",
                       "160하306", "155허744", "17허0140",]
        not_car_numbers = ["xxxxxx", "123456", "1234", "12345", "1234567"]
        assert all([check_car_number(car_number)
                   for car_number in car_numbers])
        assert all([not check_car_number(not_car_number)
                   for not_car_number in not_car_numbers])

    def test_get_client_name_and_insuranc_agent_name(self):
        assert ("김석종", "구본준") == get_client_name_and_insurance_agent_name(
            self.lines[0])
        assert ("", "구본준") == get_client_name_and_insurance_agent_name(
            self.lines[1])
        assert ("", "윤석영") == get_client_name_and_insurance_agent_name(
            self.lines[4])
        assert ("", "") == get_client_name_and_insurance_agent_name(
            self.lines[5])

    def test_make_order_from_effective_df(self):
        pass

    def test_make_order_from_first_line_number(self):
        pass
