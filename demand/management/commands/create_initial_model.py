from datetime import datetime

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from core.utility import print_colored
from demand.models import (Charge, ChargedCompany, Deposit, ExtraSales,
                           InsuranceAgent, Order, Payment, Register, Supporter)
from demand.utility import (get_effective_data_frame,
                            make_models_from_effective_df)

test_lines = [['0123', None, '1-1', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), datetime(2023, 1, 13, 0, 0), 11.0, '60저0130', '320D', '수입', None, 1.0, 1.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881890', 0.4, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 248740.80000000002, '무상7889', 392000.0, None, None, '카드', '우리', pd.Timestamp('2023-01-13 00:00:00'), 0.0, None, None, None, None, 0.0, None, 392000.0, 35636.36363636365, 356363.63636363635, None, "TEST", '완료', None, None, 1.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0],
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
              ['0120', None, '1-101', pd.Timestamp('2023-01-20 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 20, 0, 0), 0.0, '193허2950', 'K5', '국산', None, None, 0.0, '고객', None, None, '일반경정비', '일반경정비', None, '타이어펑크수리', 1.0, 1.0, 230120.0, 9090.90909090909, None, 9090.90909090909,
               909.090909090909, 10000.0, None, 10000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-20 00:00:00'), 0.0, None, None, None, None, 0.0, None, 10000.0, 909.0909090909099, 9090.90909090909, None, None, '완료', '일반경정비', None, 1.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0],
              [331.0, None, None, pd.Timestamp('2023-03-31 00:00:00'), None, datetime(2023, 3, 31, 0, 0), 0.0, 'xxxx', '세차', None, None, None, 0.0, None, '세차실장', None, '일반경정비', '일반경정비', None, '세차', 1.0, 3.0, 230331.0, None, 50000.0, 50000.0, 5000.0, 55000.00000000001,
               None, 55000.0, None, None, '카드', '신한', pd.Timestamp('2023-03-31 00:00:00'), 0.0, None, None, None, None, 0, None, 55000.0, 5000.000000000007, 49999.99999999999, None, None, '완료', '일반경정비', None, 1.0, 49999.99999999999, 0.0, 49999.99999999999, 0.0, 0.0, 50000.0],
              [412.0, None, None, pd.Timestamp('2023-04-12 00:00:00'), pd.Timestamp('2023-04-12 00:00:00'), datetime(2023, 4, 12, 0, 0), 0.0, '307누8223', 'IG', '국산', None, None, 0.0, None, '세차실장', '010-5407-9545', '일반경정비', '일반경정비', None, '부분 유리막코팅', 1.0, 4.0, 230412.0, None,
               90000.0, 90000.0, 9000.0, 99000.00000000001, None, 99000.0, None, None, '카드', '롯데', pd.Timestamp('2023-04-12 00:00:00'), 0.0, None, None, None, None, 0, None, 99000.0, 9000.0, 90000.0, None, None, '완료', '일반경정비', None, 1.0, 90000.0, 0.0, 90000.0, 0.0, 0.0, 90000.0],
              [None, None, '1-80', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-02-03 00:00:00'), '폐차', None, '21하3555', 'SM7', '국산', 4.0, 4.0, 8.0, '이성도', '김용연/백준호', 1072230486, '보험', '현대', '대물', '12-109185', 1.0,
               None, None, None, None, 0.0, 0.0, 0.0, '스타렌트', None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, '폐차처리', '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [None, None, '1-103', pd.Timestamp('2023-01-21 00:00:00'), pd.Timestamp('2023-01-26 00:00:00'), '미수리출고', None, '48노5927', '클리오', '국산', 1.0, 1.0, 2.0, '김일한', '김장현담당', 1031717367, '보험', '현대', '대물', '23-01063895', None,
               None, None, None, None, 0.0, 0.0, 0.0, '롯데렌탈 용인영업소', None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, None, '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              ]


class Command(BaseCommand):
    help = 'Delete all models'

    def add_arguments(self, parser):
        parser.add_argument('--file_name', type=str,
                            help="file_name(xlsx)", default=None)
        parser.add_argument('--sheet_name', type=str,
                            help="sheet_name", default=None)

    def handle(self, *args, **options):
        file_name = options.get("file_name")
        sheet_name = options.get("sheet_name")
        if not file_name:
            df = pd.DataFrame(test_lines).replace(
                {pd.NaT: None, np.nan: None}, inplace=False)
        else:
            if not sheet_name:
                print_colored("sheet_name is required", "red")
                return
            else:
                df = get_effective_data_frame(file_name, sheet_name)
        make_models_from_effective_df(df)
        charge_count = Charge.objects.all().count()
        charget_company_count = ChargedCompany.objects.all().count()
        deposit_count = Deposit.objects.all().count()
        extra_sales_count = ExtraSales.objects.all().count()
        insurance_agent_count = InsuranceAgent.objects.all().count()
        order_count = Order.objects.all().count()
        payment_count = Payment.objects.all().count()
        register_count = Register.objects.all().count()
        supporter_count = Supporter.objects.all().count()
        print_colored(f"Charge Created Count: {charge_count}", "green")
        print_colored(
            f"ChargedCompany Created Count: {charget_company_count}", "green")
        print_colored(f"Deposit Created Count: {deposit_count}", "green")
        print_colored(
            f"ExtraSales Created Count: {extra_sales_count}", "green")
        print_colored(
            f"InsuranceAgent Created Count: {insurance_agent_count}", "green")
        print_colored(f"Order Created Count: {order_count}", "green")
        print_colored(f"Payment Created Count: {payment_count}", "green")
        print_colored(f"Register Created Count: {register_count}", "green")
        print_colored(f"Supporter Created Count: {supporter_count}", "green")
        print_colored("All models deleted", "blue")
