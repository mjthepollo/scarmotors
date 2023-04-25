
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
                            input_to_date, input_to_phone_number, int_or_none,
                            load_data, make_complete_register_for_line_numbers,
                            make_order_payment_charge_and_deposit_with_line,
                            make_register_from_first_line_number, str_or_none,
                            string_to_date)


class UtilityTest(TestCase):
    def setUp(self):
        # mock up DF 만들어두기
        self.lines = [['0123', None, '1-1', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), datetime(2023, 1, 13, 0, 0), 11.0, '60저0130', '320D', '수입', None, 1.0, 1.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881890', 0.4, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 248740.80000000002, '무상7889', 392000.0, None, None, '카드', '우리', pd.Timestamp('2023-01-13 00:00:00'), 0.0, None, None, None, None, 0.0, None, 392000.0, 35636.36363636365, 356363.63636363635, None, "TEST", '완료', None, None, 1.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0],
                      ['0123', None, None, pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), None, 7.0, '60저0130', '320D', '수입', None, None, 0.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881806', 0.6, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 373111.2, None,
                       None, None, None, None, None, None, 373111.2, 1.0, 230119.0, 347821.0, 0.9322180626043924, 0.0, 0.06778193739560756, 347821.0, 31620.09090909094, 316200.90909090906, None, None, '완료', None, None, 1.0, 316200.90909090906, 0.0, 316200.90909090906, 0.0, 316200.90909090906, 0.0],
                      ['0106', None, '1-21', pd.Timestamp('2023-01-03 00:00:00'), pd.Timestamp('2023-01-05 00:00:00'), datetime(2023, 1, 6, 0, 0), 3.0, '13버6789', '투싼', '국산', None, 2.0, 2.0, '이소정(직원)', '구본준담당', 1034361547, '보험', 'DB', '대물', '22-7868188', 1.0, 1.0, 230106.0, 539919.0, 28262.0, 568181.0, 56818.100000000006,
                       624999.1000000001, '에스렌트', None, None, None, None, None, None, 624999.1000000001, 1.0, 230106.0, 620076.0, 0.9921230286571611, 0.0, 0.007876971342838934, 620076.0, 56370.54545454553, 563705.4545454545, None, None, '완료', None, None, 1.0, 563705.4545454545, 0.0, 563705.4545454545, 0.0, 535443.4545454545, 28262.0],
                      [None, None, '1-79', pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 19, 0, 0), 7.0, '241마5742', 'QM6', '국산', 1.0, 2.0, 3.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', 'DB', '자차', '23-00330599', None, None, None, None, None, 0.0, 0.0,
                       0.0, '반디', 500000.0, None, 300000.0, '은행', '하나', pd.Timestamp('2023-01-19 00:00:00'), 0.0, None, None, None, None, 0.0, None, 200000.0, 18181.818181818206, 181818.1818181818, None, None, '완료', None, None, 1.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0],
                      [None, None, None, pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), None, 8.0, '241마5742', 'QM6', '국산', None, None, 0.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', '삼성', '대물', '230112-1425',
                       None, None, None, None, None, 0.0, 0.0, 0.0, None, None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, None, '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      ['0131', None, '1-100', pd.Timestamp('2023-01-17 00:00:00'), pd.Timestamp('2023-01-27 00:00:00'), datetime(2023, 1, 31, 0, 0), 14.0, '60구2264', '렉서스LS460', '수입', 3.0, None, 3.0, '장영수', '윤석영', '010-9403-4783', '보험', '하나손해', '대물', '1-5008', 1.0, 1.0, 230131.0, 2323181.818181818, None,
                       2323181.818181818, 232318.1818181818, 2555500.0, '무상4760', None, None, None, None, None, None, 2555500.0, 2.0, 230202.0, 2420000.0, 0.9469771081980043, 0.0, 0.05302289180199571, 2420000.0, 220000.0, 2200000.0, None, None, '완료', None, None, 1.0, 2200000.0, 0.0, 2200000.0, 0.0, 2200000.0, 0.0],
                      ['0131', None, None, pd.Timestamp('2023-01-17 00:00:00'), pd.Timestamp('2023-01-27 00:00:00'), datetime(2023, 1, 31, 0, 0), 14.0, '60구2264', '렉서스LS460', '수입', None, None, 0.0, '장영수', '윤석영', '010-9403-4783', '일반경정비', '일반경정비', None, None, 1.0, 1.0, 230131.0, 163636.36363636362, None, 163636.36363636362,
                       16363.636363636362, 180000.0, None, 180000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-31 00:00:00'), 0.0, None, None, None, None, 0.0, None, 180000.0, 16363.636363636382, 163636.36363636362, None, None, '완료', '일반경정비', None, 1.0, 163636.36363636362, 0.0, 163636.36363636362, 0.0, 163636.36363636362, 0.0],
                      ['0120', None, '1-101', pd.Timestamp('2023-01-20 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 20, 0, 0), 0.0, '193허2950', 'K5', '국산', None, None, 0.0, '고객', None, None, '일반경정비', '일반경정비', None, '타이어펑크수리', 1.0, 1.0, 230120.0, 9090.90909090909, None, 9090.90909090909, 909.090909090909, 10000.0, None, 10000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-20 00:00:00'), 0.0, None, None, None, None, 0.0, None, 10000.0, 909.0909090909099, 9090.90909090909, None, None, '완료', '일반경정비', None, 1.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0]]
        self.line_numbers_for_registers = [[0, 1], [2], [3, 4], [5, 6], [7]]
        self.first_lines = [self.lines[line_numbers_for_register[0]]
                            for line_numbers_for_register in self.line_numbers_for_registers]
        self.registers = []
        for first_line in self.first_lines:
            register = make_register_from_first_line_number(first_line)
            self.registers.append(register)

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

    def test_get_refund_date(self):
        assert get_refund_date(self.lines[0]) == None
        assert get_refund_date(self.lines[3]) == string_to_date("2023-1-19")

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
        assert (None, "구본준") == get_client_name_and_insurance_agent_name(
            self.lines[2])
        assert (None, "윤석영") == get_client_name_and_insurance_agent_name(
            self.lines[5])
        assert (None, None) == get_client_name_and_insurance_agent_name(
            self.lines[7])

    def test_make_register_from_effective_df(self):
        pass

    def test_make_register_from_first_line_number(self):
        test_answers = [("1-1", "60저0130", "2023-01-02", "2023-01-09", "2023-01-13", "320D", "수입", 0, 1, "이성도(타)", "김석종", "구본준", "01031370900", "무상7889", "TEST"),
                        ("1-21", "13버6789", "2023-01-03", "2023-01-05", "2023-01-06", "투싼",
                         "국산", 0, 2, "이소정(직원)", None, "구본준", "01034361547", "에스렌트", None),
                        ("1-79", "241마5742", "2023-01-12", "2023-01-20", "2023-01-19", "QM6",
                         "국산", 1, 2, "이성도(타)", "김윤희", "구본준", "01048104691", "반디", None),
                        ("1-100", "60구2264", "2023-01-17", "2023-01-27", "2023-01-31", "렉서스LS460",
                         "수입", 3, 0, "장영수", None, "윤석영", "01094034783", "무상4760", None),
                        ("1-101", "193허2950", "2023-01-20", "2023-01-20", "2023-01-20", "K5", "국산", 0, 0, "고객", None, None, None, None, None),]
        for i, register in enumerate(Register.objects.all()):
            object_to_tuple = (register.RO_number,
                               register.car_number,
                               str(register.day_came_in),
                               str(register.expected_day_came_out),
                               str(register.real_day_came_out),
                               register.car_model,
                               register.abroad_type,
                               register.number_of_repair_works,
                               register.number_of_exchange_works,
                               str(register.supporter) if register.supporter else None,
                               register.client_name,
                               str(register.insurance_agent) if register.insurance_agent else None,
                               register.phone_number,
                               register.rentcar_company_name,
                               register.note)
            assert object_to_tuple == test_answers[i]
        assert Register.objects.count() == 5

    def test_make_order_payment_charge_and_deposit_wtih_line(self):
        for i in range(len(self.first_lines)):
            make_order_payment_charge_and_deposit_with_line(
                self.first_lines[i], self.registers[i])
        for register in self.registers:
            print(register)
            print(register.orders.all()[0])
            print(register.orders.all()[0].pk)
            print(register.orders.all()[0].deposit)
            print(register.orders.all()[0].payment)
            print(register.orders.all()[0].charge)
