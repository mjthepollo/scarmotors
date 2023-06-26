import numpy as np
import pandas as pd
from django.core.management import call_command

from demand.check_value_functions import (check_chargable_amount,
                                          check_charge_amount,
                                          check_component_turnover,
                                          check_factory_turnover,
                                          check_integrated_turnover,
                                          check_not_paid_amount,
                                          check_not_paid_turnover,
                                          check_paid_turnover,
                                          check_payment_rate, check_status,
                                          check_turnover, check_wage_turnover)
from demand.excel_line_info import *
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register
from demand.utility import (fault_ratio_to_int, input_to_date,
                            input_to_phone_number, int_or_none, print_fields,
                            str_or_none, zero_if_none)

SKIPPED_RO_NUMBERS = ["2-27", "2-128", "4-26", "4-30"]


def load_data(file_name, sheet_name):
    """
    엑셀 파일을 불러와 DataFrame으로 변환한다.
    """
    df = pd.read_excel(
        file_name, sheet_name=sheet_name, engine="openpyxl", header=HEADER
    )
    return df


def get_line_numbers(df):
    """
    DataFrame의 실질적인 lines 수를 파악한다.
    """
    days_came_in = df.iloc[:, DAY_CAME_IN]
    for i, day_came_in in enumerate(days_came_in):
        if pd.isnull(day_came_in):
            return i


def get_effective_data_frame(file_name, sheet_name):
    """
    엑셀 파일을 불러와서 실질적인 데이터를 가진 DataFrame으로 변환한다. 
    """
    original_df = load_data(file_name, sheet_name)
    line_numbers = get_line_numbers(original_df)
    return original_df.iloc[:line_numbers, :END].replace({pd.NaT: None, np.nan: None}, inplace=False)


def check_wash_line(df, line_number):
    """
    effective DataFrame의 line number에 해당하는 line이 세차를 가리키는 line인지 확인한다.
    """
    client_name_and_insurance_agent = df.iloc[line_number,
                                              CLIENT_NAME_AND_INSURANCE_AGENT]
    supporter_name = df.iloc[line_number, SUPPORTER]
    return "세차" in client_name_and_insurance_agent or "세차" in supporter_name


def check_wasted_line(df, line_number):
    """
    effective DataFrame의 line number에 해당하는 line이 폐차를 가리키는 line인지 확인한다.
    """
    pass


def check_unrepaired_line(df, line_number):
    """
    effective DataFrame의 line number에 해당하는 line이 미수리출고를 가리키는 line인지 확인한다.
    """
    pass


def get_line_numbers_for_extra_sales(effective_df):
    """
    ExtraSales로 평가될 line numbers를 반환한다. 이는 리스트로 반환된다.
    """
    line_numbers_for_extra_sales = []
    RO_numbers = effective_df.iloc[:, RO_NUMBER].values.tolist()
    for i, RO_number in enumerate(RO_numbers):
        if not RO_number:
            # 현재는 세차만 고려한다. 현재까지 유일하게 존재하는 extra sales는 세차다.
            if check_wash_line(effective_df, i):
                line_numbers_for_extra_sales.append(i)
    return line_numbers_for_extra_sales


def get_line_numbers_for_registers(effective_df):
    """
    Register로 평가될 line numbers를 반환한다. 이는 리스트로 반환된다.
    Excel에서 같은 RO_number가 들어오는 경우가 있으며, 또 ExtraSales도 고려해야 하기 때문에 강건성을 위해 만든 함수다.
    """
    RO_numbers = effective_df.iloc[:, RO_NUMBER].values.tolist()
    line_numbers_for_extra_sales = get_line_numbers_for_extra_sales(
        effective_df)
    line_numbers_for_registers = []
    for i, RO_number in enumerate(RO_numbers):
        if not RO_number:
            if i in line_numbers_for_extra_sales:
                # ExtraSales로 평가된 세차, 미수리 출고, 폐차의 경우는 Register에 저장하지 않는다.
                pass
            else:  # 일반적으로 RO_number가 없는 경우는 여러 개의 Order가 하나의 Register에 저장되는 경우다.
                line_numbers_for_registers[-1].append(i)
        else:  # RO_number가 있는 경우. 특수한 경우에 같은 RO_number가 두 라인에 있을 수 있어서 처리해줘야 한다.
            if RO_number == RO_numbers[i - 1]:
                line_numbers_for_registers[-1].append(i)
            else:
                line_numbers_for_registers.append([i])
    return line_numbers_for_registers


def check_line_numbers_for_registers_have_same_car_number(effective_df):
    """
    RO_number가 같은 경우, 차량번호는 같아야 한다.
    따라서 하나의 Register에 Line이 여러개인 경우 같은 차량번호를 가지는지를 확인한다.
    """
    line_numbers_for_registers = get_line_numbers_for_registers(effective_df)
    for line_numbers_for_register in line_numbers_for_registers:
        if len(line_numbers_for_register) > 1:
            all_car_number = [
                effective_df.iloc[:, CAR_NUMBER][line_number]
                for line_number in line_numbers_for_register
            ]
            try:
                assert all(car_number == all_car_number[0]
                           for car_number in all_car_number)
            except AssertionError as e:
                print(all_car_number[0])
                raise e


def check_line_numbers_for_registers_have_unique_RO_number(effective_df):
    """
    RO_number는 유일해야 한다. 같은 RO_number가 여러 라인에 있지 않은지 확인한다.
    """
    raw_RO_numbers = effective_df.iloc[:, RO_NUMBER].values.tolist()
    line_numbers_for_registers = get_line_numbers_for_registers(effective_df)
    RO_numbers = [raw_RO_numbers[line_numbers_for_register[0]]
                  for line_numbers_for_register in line_numbers_for_registers]
    RO_numbers_set = set(RO_numbers)
    try:
        assert len(RO_numbers) == len(RO_numbers_set)
    except AssertionError as e:
        for RO_number in RO_numbers:
            if RO_numbers.count(RO_number) > 1:
                print(RO_number)
        # print(len(RO_numbers), len(RO_numbers_set))
        raise e


def df_to_lines(df):
    lines = []
    for i in range(len(df)):
        lines.append(df.iloc[i, :].values.tolist())
    return lines


def register_to_tuple(register):
    return (register.RO_number,
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
            register.note,
            register.wasted,
            register.unrepaired,
            )


def get_client_name_and_insurance_agent_name(first_line):
    client_name_and_insurance_agent = first_line[CLIENT_NAME_AND_INSURANCE_AGENT]
    if isinstance(client_name_and_insurance_agent, str):
        if "/" in client_name_and_insurance_agent:
            return tuple(client_name_and_insurance_agent.split("/"))
        elif "담당" == client_name_and_insurance_agent[-2:]:
            return None, client_name_and_insurance_agent[:-2]
        else:
            if not client_name_and_insurance_agent:
                return None, None
            else:
                return None, client_name_and_insurance_agent
    else:
        return None, None


def get_refund_date(line):
    if line[REFUND_AMOUNT]:
        return input_to_date(line[PAYMENT_DATE])
    else:
        return None


def check_values_of_column(df, lines, line_numbers_for_registers,
                           line_numbers_for_extra_sales,
                           COLUMN_NUMBER, METHOD_NAME):
    CHECK_VALUE_FUNCTIONS = {
        CHARGE_AMOUNT: check_charge_amount,
        COMPONENT_TURNOVER: check_component_turnover,
        FACTORY_TURNOVER: check_factory_turnover,
        CHARGABLE_AMOUNT: check_chargable_amount,
        INTEGRATED_TURNOVER: check_integrated_turnover,
        NOT_PAID_AMOUNT: check_not_paid_amount,
        NOT_PAID_TURNOVER: check_not_paid_turnover,
        PAID_TURNOVER: check_paid_turnover,
        PAYMENT_RATE: check_payment_rate,
        STATUS: check_status,
        TURNOVER: check_turnover,
        WAGE_TURNOVER: check_wage_turnover,
    }
    call_command('clean_models')
    make_models_from_effective_df(df)
    for i, line_number in enumerate(line_numbers_for_extra_sales):
        try:
            extra_sales = ExtraSales.objects.get(
                car_number=lines[line_number][CAR_NUMBER])
            compared_value = getattr(extra_sales, METHOD_NAME)()
            expecting_value = lines[line_number][COLUMN_NUMBER]
            CHECK_VALUE_FUNCTIONS[COLUMN_NUMBER](
                extra_sales, compared_value, expecting_value)
        except Exception as e:
            print_fields(extra_sales)
            raise e

    for i, line_number in enumerate([line_number for line_numbers_for_register in line_numbers_for_registers for line_number in line_numbers_for_register]):
        try:
            order = Order.objects.all().order_by("created")[i]
            compared_value = getattr(order, METHOD_NAME)()
            expecting_value = lines[line_number][COLUMN_NUMBER]
            CHECK_VALUE_FUNCTIONS[COLUMN_NUMBER](
                order, compared_value, expecting_value)
        except Exception as e:
            print_fields(order)
            raise e


def create_order_from_line(line, register):
    if line[NOTE]:
        if register.note:
            register.note += "\n"+line[NOTE]
        else:
            register.note = line[NOTE]
    register.save()
    if line[CHARGED_COMPANY]:
        charged_company, _ = ChargedCompany.objects.get_or_create(
            name=line[CHARGED_COMPANY])
    else:
        charged_company = None
    fault_ratio = fault_ratio_to_int(line[FAULT_RATIO])
    return Order.objects.create(
        register=register,
        charged_company=charged_company,
        charge_type=line[CHARGE_TYPE],
        order_type=line[ORDER_TYPE],
        receipt_number=str_or_none(line[RECEIPT_NUMBER]),
        fault_ratio=fault_ratio,
    )


def create_deposit_from_line(line, sales):
    if line[DEPOSIT_DATE]:
        deposit = Deposit.objects.create(
            deposit_amount=int_or_none(line[DEPOSIT_AMOUNT]),
            deposit_date=input_to_date(line[DEPOSIT_DATE]),
        )
        sales.deposit = deposit
        sales.save()
    else:
        deposit = None
    return deposit


def create_charge_from_line(line, sales):
    if line[CHARGE_DATE]:
        charge = Charge.objects.create(
            charge_date=input_to_date(line[CHARGE_DATE]),
            wage_amount=zero_if_none(int_or_none(line[WAGE_AMOUNT])),
            component_amount=zero_if_none(int_or_none(line[COMPONENT_AMOUNT])),
        )
        sales.charge = charge
        sales.save()
    else:
        charge = None
    return charge


def create_payment_from_line(line, sales):
    if line[INDEMNITY_AMOUNT]:
        payment = Payment.objects.create(
            indemnity_amount=int_or_none(line[INDEMNITY_AMOUNT]),
            discount_amount=int_or_none(line[DISCOUNT_AMOUNT]),
            refund_amount=int_or_none(line[REFUND_AMOUNT]),
            payment_type=line[PAYMENT_TYPE],
            payment_info=line[PAYMENT_INFO],
            payment_date=input_to_date(input_to_date(line[PAYMENT_DATE])),
            refund_date=get_refund_date(line)
        )
        sales.payment = payment
        sales.save()
    else:
        payment = None
    return payment


def make_extra_sales_from_line(line):
    if line[SUPPORTER]:
        supporter, _ = Supporter.objects.get_or_create(name=line[SUPPORTER])
    else:
        supporter = None
    client_name, insurance_agent_name = get_client_name_and_insurance_agent_name(
        line)
    if insurance_agent_name:
        insurance_agent, _ = InsuranceAgent.objects.get_or_create(
            name=insurance_agent_name)
    else:
        insurance_agent = None

    extra_sales = ExtraSales.objects.create(
        car_number=line[CAR_NUMBER],
        day_came_in=input_to_date(line[DAY_CAME_IN]),
        expected_day_came_out=input_to_date(line[EXPECTED_DAY_CAME_OUT]),
        real_day_came_out=input_to_date(line[REAL_DAY_CAME_OUT]),
        car_model=str(line[CAR_MODEL]),
        abroad_type=line[ABROAD_TYPE],
        supporter=supporter,
        insurance_agent=insurance_agent,
        client_name=client_name,
        phone_number=input_to_phone_number(line[PHONE_NUMBER]),
        note=line[NOTE],
    )
    create_charge_from_line(line, extra_sales)
    create_deposit_from_line(line, extra_sales)
    create_payment_from_line(line, extra_sales)
    return extra_sales


def make_register_from_first_line_number(first_line):
    if first_line[SUPPORTER]:
        supporter, _ = Supporter.objects.get_or_create(
            name=first_line[SUPPORTER])
    else:
        supporter = None
    client_name, insurance_agent_name = get_client_name_and_insurance_agent_name(
        first_line)
    if insurance_agent_name:
        insurance_agent, _ = InsuranceAgent.objects.get_or_create(
            name=insurance_agent_name)
    else:
        insurance_agent = None

    wasted = first_line[REAL_DAY_CAME_OUT] == "폐차"
    unrepaired = first_line[REAL_DAY_CAME_OUT] == "미수리출고"

    if first_line[RO_NUMBER] in SKIPPED_RO_NUMBERS:
        return None
    try:
        return Register.objects.create(
            RO_number=first_line[RO_NUMBER],
            car_number=first_line[CAR_NUMBER],
            day_came_in=input_to_date(first_line[DAY_CAME_IN]),
            expected_day_came_out=input_to_date(
                first_line[EXPECTED_DAY_CAME_OUT]),
            real_day_came_out=input_to_date(first_line[REAL_DAY_CAME_OUT]),
            car_model=str(first_line[CAR_MODEL]),
            abroad_type=first_line[ABROAD_TYPE],
            number_of_repair_works=zero_if_none(
                first_line[NUMBER_OF_REPAIRS_WORKS]),
            number_of_exchange_works=zero_if_none(
                first_line[NUMBER_OF_EXCHANGE_WORKS]),
            supporter=supporter,
            client_name=client_name,
            insurance_agent=insurance_agent,
            phone_number=input_to_phone_number(first_line[PHONE_NUMBER]),
            rentcar_company_name=first_line[RENT_CAR_COMPANY_NAME],
            note=None,  # Note is handled in create_order_from_line
            wasted=wasted,
            unrepaired=unrepaired,
        )
    except Exception as e:
        print(first_line)
        raise e


def make_order_payment_charge_and_deposit_with_line(line, register):
    order = create_order_from_line(line, register)
    create_charge_from_line(line, order)
    create_deposit_from_line(line, order)
    create_payment_from_line(line, order)
    order.save()
    return order


def make_complete_register_for_line_numbers(df, line_numbers):
    first_line = df.iloc[line_numbers[0], :].values.tolist()
    register = make_register_from_first_line_number(first_line)
    try:
        for line_number in line_numbers:
            line = df.iloc[line_number, :].values.tolist()
            make_order_payment_charge_and_deposit_with_line(line, register)
    except Exception as e:
        print_fields(register)
        raise e


def make_models_from_effective_df(df):
    line_numbers_for_registers = get_line_numbers_for_registers(df)
    line_numbers_for_extra_sales = get_line_numbers_for_extra_sales(df)
    for line_numbers_for_register in line_numbers_for_registers:
        make_complete_register_for_line_numbers(df, line_numbers_for_register)
    for line_number in line_numbers_for_extra_sales:
        line = df.iloc[line_number, :].values.tolist()
        make_extra_sales_from_line(line)


def get_sales_of_month_and_type(month, charge_type):
    integrated_sales = 0
    paid_sales = 0
    not_paid_sales = 0
    if charge_type == "일반경정비":
        extra_sales_query = ExtraSales.objects.filter(
            charge__charge_date__month=month)
        for extra_sales in extra_sales_query:
            integrated_sales += extra_sales.get_integrated_turnover()
            paid_sales += extra_sales.get_paid_turnover()
            not_paid_sales += extra_sales.get_not_paid_turnover()
    orders = Order.objects.filter(
        charge__charge_date__month=month, charge_type=charge_type)
    for order in orders:
        integrated_sales += order.get_integrated_turnover()
        paid_sales += order.get_paid_turnover()
        not_paid_sales += order.get_not_paid_turnover()
    return {
        "paid_sales": paid_sales,
        "not_paid_sales": not_paid_sales,
        "integrated_sales": integrated_sales,
    }
