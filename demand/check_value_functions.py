def check_chargable_amount(obj, compared_value, expecting_value):
    if obj.charge:
        assert abs(expecting_value - compared_value) < 10
    else:
        if isinstance(expecting_value, (float, int)):
            assert expecting_value == 0.0
            assert compared_value == None
        else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
            raise AssertionError


def check_charge_amount(obj, compared_value, expecting_value):
    if obj.charge:
        assert abs(expecting_value - compared_value) < 10
    else:
        if isinstance(expecting_value, (float, int)):
            assert expecting_value == 0.0
            assert compared_value == None
        else:  # 모두가 숫자일 것으로 예상되므로 이런 경우는 없어야 한다.
            raise AssertionError


def check_not_paid_amount(obj, compared_value, expecting_value):
    assert abs(compared_value - expecting_value) < 10


def check_payment_rate(obj, compared_value, expecting_value):
    if compared_value:
        assert abs(expecting_value - compared_value) <= 0.01
    else:
        assert expecting_value == None
        assert compared_value == None


def check_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_factory_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_paid_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_not_paid_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_integrated_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_component_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_wage_turnover(obj, compared_value, expecting_value):
    from demand.utility import zero_if_none
    assert abs(zero_if_none(expecting_value) - compared_value) < 10


def check_status(obj, compared_value, expecting_value):
    assert expecting_value == compared_value
