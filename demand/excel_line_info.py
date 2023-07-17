# HEADER는 load_data에서 처음으로 유효한 행의 인덱스를 알려준다. +2를 했을 때 excel의 line_number가된다.
from demand.utility import zero_if_none, zero_if_not_number

HEADER = 5


RO_NUMBER = 2
DAY_CAME_IN = 3
EXPECTED_DAY_CAME_OUT = 4
REAL_DAY_CAME_OUT = 5
CAR_NUMBER = 7
CAR_MODEL = 8
ABROAD_TYPE = 9
NUMBER_OF_REPAIRS_WORKS = 10
NUMBER_OF_EXCHANGE_WORKS = 11
SUPPORTER = 13
CLIENT_NAME_AND_INSURANCE_AGENT = 14
PHONE_NUMBER = 15
CHARGE_TYPE = 16
CHARGED_COMPANY = 17
ORDER_TYPE = 18
RECEIPT_NUMBER = 19
FAULT_RATIO = 20
CHARGE_DATE = 22
WAGE_AMOUNT = 23
COMPONENT_AMOUNT = 24
REPAIR_AMOUNT = 25
VAT_AMOUNT = 26
CHARGABLE_AMOUNT = 27
ESTIMATE_AMOUNT = 28
RENT_CAR_COMPANY_NAME = 29
INDEMNITY_AMOUNT = 30
DISCOUNT_AMOUNT = 31
REFUND_AMOUNT = 32
PAYMENT_TYPE = 33
PAYMENT_INFO = 34
PAYMENT_DATE = 35
CHARGE_AMOUNT = 36
# REFUND_DATE = pass
DEPOSIT_DATE = 38
DEPOSIT_AMOUNT = 39
PAYMENT_RATE = 40
NOT_PAID_AMOUNT = 41
TURNOVER = 43
FACTORY_TURNOVER = 45
NOTE = 47
STATUS = 48
PAID_TURNOVER = 52
NOT_PAID_TURNOVER = 53
INTEGRATED_TURNOVER = 54
WAGE_TURNOVER = 56
COMPONENT_TURNOVER = 57
END = 58

INDEXES = {
    "RO_number": "접수번호",
    "day_came_in": "입고일",
    "expected_day_came_out": "출고예정일",
    "real_day_came_out": "실제출고일",
    "days_needed_to_fix": "작업일",
    "car_number": "차량번호",
    "car_model": "차종",
    "abroad_type": "국산/수입",
    "number_of_repair_works": "보수판수",
    "number_of_exchange_works": "교환판수",
    "number_of_works": "판수총계",
    "supporter": "입고지원",
    "client_name": "의뢰자",
    "insurance_agent": "보험담당자",
    "phone_number": "전화번호",
    "rentcar_company_name": "유상렌트",
    "charge_type": "등록타입",
    "charged_company": "보험사",
    "order_type": "주문타입",
    "receipt_number": "접수번호",
    "fault_ratio": "과실분",
    "charge_month": "청구월",
    "charge_date": "청구일",
    "wage_amount": "공임비(부가세별도)",
    "component_amount": "부품비",
    "repair_amount": "수리비",
    "vat_amouunt": "부가세",
    "chargable_amount": "청구가능금액",
    "estimate_amount": "선견적",
    "indemnity_amount": "면책금",
    "discount_amount": "할인금",
    "refund_amount": "환불금",
    "payment_type": "현금/카드",
    "payment_info": "카드사",
    "payment_date": "입금일",
    "charge_amount": "청구금액",
    "deposit_month": "입금월",
    "deposit_date": "입금일",
    "deposit_amount": "입금액",
    "payment_rate": "지급율",
    "not_paid_amount": "미수액",
    "not_paid_rate": "삭감율",
    "turnover": "입금매출",
    "turnover_vat": "부가세",
    "factory_turnover": "공장매출",
    "note": "비고",
    "paid_turnover": "입금매출",
    "not_paid_turnover": "미입금매출",
    "integrated_turnover": "종합매출",
    "wage_turnover": "공임매출",
    "component_turnover": "부품매출",
    "status": "주문상태",
}


def dictionary_to_line(dictionary):
    return [
        dictionary["RO_number"],
        dictionary["day_came_in"],
        dictionary["expected_day_came_out"],
        dictionary["real_day_came_out"],
        dictionary["days_needed_to_fix"],
        dictionary["car_number"],
        dictionary["car_model"],
        dictionary["abroad_type"],
        dictionary["number_of_repair_works"],
        dictionary["number_of_exchange_works"],
        dictionary["number_of_works"],
        dictionary["supporter"],
        dictionary["client_name"],
        dictionary["insurance_agent"],
        dictionary["phone_number"],
        dictionary["renctcar_company_name"],
        dictionary["charge_type"],
        dictionary["charged_company"],
        dictionary["order_type"],
        dictionary["receipt_number"],
        dictionary["fault_ratio"],
        dictionary["charge_month"],
        dictionary["charge_date"],
        dictionary["wage_amount"],
        dictionary["component_amount"],
        dictionary["repair_amount"],
        dictionary["vat_amouunt"],
        dictionary["chargable_amount"],
        dictionary["estimate_amount"],
        dictionary["indemnity_amount"],
        dictionary["discount_amount"],
        dictionary["refund_amount"],
        dictionary["payment_type"],
        dictionary["payment_info"],
        dictionary["payment_date"],
        dictionary["charge_amount"],
        dictionary["deposit_month"],
        dictionary["deposit_date"],
        dictionary["deposit_amount"],
        dictionary["payment_rate"],
        dictionary["not_paid_amount"],
        dictionary["not_paid_rate"],
        dictionary["turnover"],
        dictionary["turnover_vat"],
        dictionary["factory_turnover"],
        dictionary["note"],
        dictionary["paid_turnover"],
        dictionary["not_paid_turnover"],
        dictionary["integrated_turnover"],
        dictionary["wage_turnover"],
        dictionary["component_turnover"],
        dictionary["status"],
    ]


def order_to_excel_dictionary(order):
    if order.register:
        register = order.register
        RO_number = register.RO_number or "NO-RO"
        day_came_in = register.day_came_in.strftime(
            "%Y-%m-%d") if register.day_came_in else "-"
        expected_day_came_out = register.expected_day_came_out.strftime(
            "%Y-%m-%d") if register.expected_day_came_out else "-"
        real_day_came_out = register.real_day_came_out.strftime(
            "%Y-%m-%d") if register.real_day_came_out else "-"
        days_needed_to_fix = zero_if_none(register.get_work_days())
        car_number = register.car_number or "-"
        car_model = register.car_model or "-"
        abroad_type = register.abroad_type or "-"
        number_of_repair_works = register.number_of_repair_works or 0
        number_of_exchange_works = register.number_of_exchange_works or 0
        number_of_works = number_of_repair_works + number_of_exchange_works
        supporter = register.supporter.name if register.supporter else "-"
        client_name = register.client_name or "-"
        insurance_agent = register.insurance_agent.name if register.insurance_agent else "-"
        rentcar_company_name = register.rentcar_company_name or "-"
        phone_number = register.phone_number or "-"
        register_note = register.note or "-"
    else:
        (RO_number, day_came_in, expected_day_came_out,
            real_day_came_out, days_needed_to_fix, car_number, car_model, abroad_type,
            number_of_repair_works, number_of_exchange_works,
            number_of_works, supporter, client_name, insurance_agent, rentcar_company_name, phone_number, register_note) = [""] * 16
    charge_type = order.charge_type or "-"
    charged_company = order.charged_company.name if order.charged_company else "-"
    order_type = order.order_type or "-"
    receipt_number = order.receipt_number or "-"
    fault_ratio = order.fault_ratio or "-"
    charge_date = order.charge.charge_date if order.charge else None
    charge_month = charge_date.month if charge_date else "-"
    charge_date = charge_date.strftime(
        "%Y-%m-%d") if charge_date else "-"
    wage_amount = order.charge.wage_amount if order.charge else 0
    wage_amount = zero_if_none(wage_amount)
    component_amount = order.charge.component_amount if order.charge else 0
    component_amount = zero_if_none(component_amount)
    repair_amount = wage_amount + component_amount
    vat_amouunt = int(repair_amount/10)
    chargable_amount = int(order.get_chargable_amount()
                           ) if order.get_chargable_amount() else 0
    indemnity_amount = zero_if_none(order.get_indemnity_amount())
    payment = order.payment
    discount_amount = payment.discount_amount if payment else 0
    discount_amount = zero_if_none(discount_amount)
    refund_amount = order.payment.refund_amount if payment else 0
    refund_amount = zero_if_none(refund_amount)
    payment_type = payment.payment_type if payment else "-"
    payment_type = payment_type or "-"
    payment_info = payment.payment_info if payment else "-"
    payment_info = payment_info or "-"
    payment_date = payment.payment_date if payment else None
    payment_date = payment_date.strftime("%Y-%m-%d") if payment_date else "-"
    charge_amount = int(zero_if_none(order.get_charge_amount()))
    deposit_date = order.deposit.deposit_date if order.deposit else None
    deposit_month = deposit_date.month if deposit_date else "-"
    deposit_date = deposit_date.strftime(
        "%Y-%m-%d") if deposit_date else "-"
    deposit_amount = order.deposit.deposit_amount if order.deposit else 0
    deposit_amount = zero_if_none(deposit_amount)
    payment_rate = int(order.get_payment_rate() *
                       100) if order.get_payment_rate() else "-"
    not_paid_amount = int(order.get_not_paid_amount())
    not_paid_rate = int(100 - order.get_payment_rate() *
                        100) if order.get_payment_rate() else "-"
    turnover = int(zero_if_none(order.get_turnover()))
    turnover_vat = int(turnover*10/11)
    factory_turnover = int(zero_if_none(order.get_factory_turnover()))
    paid_turnover = int(zero_if_none(order.get_paid_turnover()))
    not_paid_turnover = int(zero_if_none(order.get_not_paid_turnover()))
    integrated_turnover = int(zero_if_none(order.get_integrated_turnover()))
    wage_turnover = int(zero_if_none(order.get_wage_turnover()))
    component_turnover = int(zero_if_none(order.get_component_turnover()))
    status = order.status
    return {
        "RO_number": RO_number,
        "day_came_in": day_came_in,
        "expected_day_came_out": expected_day_came_out,
        "real_day_came_out": real_day_came_out,
        "days_needed_to_fix": days_needed_to_fix,
        "car_number": car_number,
        "car_model": car_model,
        "abroad_type": abroad_type,
        "number_of_repair_works": number_of_repair_works,
        "number_of_exchange_works": number_of_exchange_works,
        "number_of_works": number_of_works,
        "supporter": supporter,
        "client_name": client_name,
        "insurance_agent": insurance_agent,
        "phone_number": phone_number,
        "renctcar_company_name": rentcar_company_name,
        "charge_type": charge_type,
        "charged_company": charged_company,
        "order_type": order_type,
        "receipt_number": receipt_number,
        "fault_ratio": fault_ratio,
        "charge_month": charge_month,
        "charge_date": charge_date,
        "wage_amount": wage_amount,
        "component_amount": component_amount,
        "repair_amount": repair_amount,
        "vat_amouunt": vat_amouunt,
        "chargable_amount": chargable_amount,
        "estimate_amount": "-",
        "indemnity_amount": indemnity_amount,
        "discount_amount": discount_amount,
        "refund_amount": refund_amount,
        "payment_type": payment_type,
        "payment_info": payment_info,
        "payment_date": payment_date,
        "charge_amount": charge_amount,
        "deposit_month": deposit_month,
        "deposit_date": deposit_date,
        "deposit_amount": deposit_amount,
        "payment_rate": payment_rate,
        "not_paid_amount": not_paid_amount,
        "not_paid_rate": not_paid_rate,
        "turnover": turnover,
        "turnover_vat": turnover_vat,
        "factory_turnover": factory_turnover,
        "note": register_note,
        "paid_turnover": paid_turnover,
        "not_paid_turnover": not_paid_turnover,
        "integrated_turnover": integrated_turnover,
        "wage_turnover": wage_turnover,
        "component_turnover": component_turnover,
        "status": status,
    }


def extra_sales_to_excel_dictionary(extra_sales):
    RO_number = f"기타매출{extra_sales.pk}"
    day_came_in = extra_sales.day_came_in.strftime(
        "%Y-%m-%d") if extra_sales.day_came_in else "-"
    expected_day_came_out = extra_sales.expected_day_came_out.strftime(
        "%Y-%m-%d") if extra_sales.expected_day_came_out else "-"
    real_day_came_out = extra_sales.real_day_came_out.strftime(
        "%Y-%m-%d") if extra_sales.real_day_came_out else "-"
    days_needed_to_fix = (
        real_day_came_out-day_came_in).days if real_day_came_out and day_came_in else "-"
    car_number = extra_sales.car_number or "-"
    car_model = extra_sales.car_model or "-"
    abroad_type = extra_sales.abroad_type or "-"
    number_of_repair_works = extra_sales.number_of_repair_works or 0
    number_of_exchange_works = extra_sales.number_of_exchange_works or 0
    number_of_works = number_of_repair_works + number_of_exchange_works
    supporter = extra_sales.supporter.name if extra_sales.supporter else "-"
    client_name = extra_sales.client_name or "-"
    insurance_agent = extra_sales.insurance_agent.name if extra_sales.insurance_agent else "-"
    rentcar_company_name = extra_sales.rentcar_company_name or "-"
    phone_number = extra_sales.phone_number or "-"

    charge_type = extra_sales.charge_type or "-"
    charged_company = extra_sales.charged_company.name if extra_sales.charged_company else "-"
    order_type = extra_sales.order_type or "-"
    receipt_number = extra_sales.receipt_number or "-"
    fault_ratio = extra_sales.fault_ratio or "-"
    charge_date = extra_sales.charge_date if extra_sales.charge_date else None
    charge_month = extra_sales.charge.charge_date.month if charge_date else "-"
    charge_date = charge_date.strftime(
        "%Y-%m-%d") if charge_date else "-"
    wage_amount = extra_sales.charge.wage_amount if extra_sales.charge else 0
    wage_amount = zero_if_none(wage_amount)
    component_amount = extra_sales.charge.component_amount if extra_sales.charge else 0
    component_amount = zero_if_none(component_amount)
    repair_amount = wage_amount + component_amount
    vat_amouunt = int(repair_amount/10)
    chargable_amount = int(extra_sales.get_chargable_amount())
    indemnity_amount = int(zero_if_none(extra_sales.get_indemnity_amount()))
    payment = extra_sales.payment
    discount_amount = payment.discount_amount if payment else 0
    discount_amount = int(zero_if_none(discount_amount))
    refund_amount = payment.refund_amount if payment else 0
    refund_amount = int(zero_if_none(refund_amount))
    payment_type = extra_sales.payment.payment_type if payment else "-"
    payment_type = payment_type or "-"
    payment_info = extra_sales.payment.payment_info if payment else "-"
    payment_info = payment_info or "-"
    payment_date = payment.payment_date if payment else None
    payment_date = payment_date.strftime(
        "%Y-%m-%d") if payment_date else "-"
    charge_amount = int(zero_if_none(extra_sales.get_charge_amount()))
    deposit_date = extra_sales.deposit.deosit_date if extra_sales.deposit else None
    deposit_month = deposit_date.month if deposit_date else "-"
    deposit_date = deposit_date.strftime(
        "%Y-%m-%d") if deposit_date else "-"
    deposit_amount = extra_sales.deposit.deposit_amount if extra_sales.deposit else 0
    deposit_amount = int(zero_if_none(deposit_amount))
    payment_rate = int(extra_sales.get_payment_rate() *
                       100) if extra_sales.get_payment_rate() else "-"
    not_paid_amount = extra_sales.get_not_paid_amount()
    not_paid_rate = int(100 - 100*extra_sales.get_payment_rate()
                        ) if extra_sales.get_payment_rate() else "-"
    turnover = int(zero_if_none(extra_sales.get_turnover()))
    turnover_vat = int(turnover*10/11)
    factory_turnover = int(zero_if_none(extra_sales.get_factory_turnover()))
    note = extra_sales.note or ""
    paid_turnover = int(zero_if_none(extra_sales.get_paid_turnover()))
    not_paid_turnover = int(zero_if_none(extra_sales.get_not_paid_turnover()))
    integrated_turnover = int(zero_if_none(
        extra_sales.get_integrated_turnover()))
    wage_turnover = int(zero_if_none(extra_sales.get_wage_turnover()))
    component_turnover = int(zero_if_none(
        extra_sales.get_component_turnover()))
    status = extra_sales.status
    return {
        "RO_number": RO_number,
        "day_came_in": day_came_in,
        "expected_day_came_out": expected_day_came_out,
        "real_day_came_out": real_day_came_out,
        "days_needed_to_fix": days_needed_to_fix,
        "car_number": car_number,
        "car_model": car_model,
        "abroad_type": abroad_type,
        "number_of_repair_works": number_of_repair_works,
        "number_of_exchange_works": number_of_exchange_works,
        "number_of_works": number_of_works,
        "supporter": supporter,
        "client_name": client_name,
        "insurance_agent": insurance_agent,
        "phone_number": phone_number,
        "renctcar_company_name": rentcar_company_name,
        "charge_type": charge_type,
        "charged_company": charged_company,
        "order_type": order_type,
        "receipt_number": receipt_number,
        "fault_ratio": fault_ratio,
        "charge_month": charge_month,
        "charge_date": charge_date,
        "wage_amount": wage_amount,
        "component_amount": component_amount,
        "repair_amount": repair_amount,
        "vat_amouunt": vat_amouunt,
        "chargable_amount": chargable_amount,
        "estimate_amount": None,
        "indemnity_amount": indemnity_amount,
        "discount_amount": discount_amount,
        "refund_amount": refund_amount,
        "payment_type": payment_type,
        "payment_info": payment_info,
        "payment_date": payment_date,
        "charge_amount": charge_amount,
        "deposit_month": deposit_month,
        "deposit_date": deposit_date,
        "deposit_amount": deposit_amount,
        "payment_rate": payment_rate,
        "not_paid_amount": not_paid_amount,
        "not_paid_rate": not_paid_rate,
        "turnover": turnover,
        "turnover_vat": turnover_vat,
        "factory_turnover": factory_turnover,
        "note": note,
        "paid_turnover": paid_turnover,
        "not_paid_turnover": not_paid_turnover,
        "integrated_turnover": integrated_turnover,
        "wage_turnover": wage_turnover,
        "component_turnover": component_turnover,
        "status": status,
    }
