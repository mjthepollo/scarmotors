from datetime import date

import django_filters
from dateutil.relativedelta import relativedelta
from django import forms
from django_filters.widgets import BooleanWidget

from demand.key_models import Supporter
from demand.sales_models import Order, Register


class NullBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", "-"), ("false", "O"),
                        ("true", "X"))


class RegisterFilter(django_filters.FilterSet):
    RO_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='RO_number', lookup_expr='icontains', label="RO번호")
    car_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='car_number', lookup_expr='icontains', label="차량번호")

    day_came_in__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gt', label="입고일(부터)")
    day_came_in__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lt', label="입고일(까지)")

    real_day_came_out__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='gt', label="출고일(부터)")
    real_day_came_out__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='lt', label="출고일(까지)")

    client_name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='client_name', lookup_expr='icontains', label="고객명")
    note = django_filters.BooleanFilter(
        field_name='note', label="비고여부", lookup_expr="isnull",
        widget=NullBooleanWidget())

    class Meta:
        model = Register
        fields = ["RO_number", "car_number",
                  "supporter", "client_name", "insurance_agent"]


class RegisterFilterForOrderFilter(django_filters.FilterSet):
    car_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='car_number', lookup_expr='icontains', label="차량번호")

    day_came_in__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gt', label="입고일(부터)")
    day_came_in__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lt', label="입고일(까지)")

    real_day_came_out__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='gt', label="출고일(부터)")
    real_day_came_out__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='lt', label="출고일(까지)")

    client_name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='client_name', lookup_expr='icontains', label="고객명")

    note = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='note', label="비고", lookup_expr="icontains")

    class Meta:
        model = Register
        fields = ["car_number", "supporter",
                  "client_name", "insurance_agent", "note"]


class OrderFilter(django_filters.FilterSet):
    receipt_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='receipt_number', lookup_expr='icontains', label="접수번호")

    status = django_filters.ChoiceFilter(
        choices=Order._meta.get_field('status').choices, label="상태")

    class Meta:
        model = Order
        fields = ["charged_company", "charge_type", "order_type"]


INCENTIVE_FILTER_CHOICES = (
    (date.today()+relativedelta(months=-1), "1개월"),
    (date.today()+relativedelta(months=-3), "3개월"),
    (date.today()+relativedelta(months=-6), "6개월"),
    (date.today()+relativedelta(months=-12), "1년"),
)


class OXBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", "-"), ("true", "O"),
                        ("false", "X"))


class IncentiveFilter(django_filters.FilterSet):
    register__supporter = django_filters.ModelChoiceFilter(
        queryset=Supporter.objects.all(), label="업체명")
    incentive_paid = django_filters.BooleanFilter(
        field_name='incentive_paid', label="지급여부",
        widget=OXBooleanWidget())
    day_came_in__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='register__day_came_in', lookup_expr='gt', label="입고일(부터)")
    day_came_in__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='register__day_came_in', lookup_expr='lt', label="입고일(까지)")

    class Meta:
        model = Order
        fields = ["register__supporter", 'incentive_paid']
