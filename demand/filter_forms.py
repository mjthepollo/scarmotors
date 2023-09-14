from datetime import date

import django_filters
from dateutil.relativedelta import relativedelta
from django import forms
from django_filters.widgets import BooleanWidget

from demand.key_models import ChargedCompany, InsuranceAgent, Supporter
from demand.sales_models import Order, Register


class NullBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", "-"), ("false", "O"),
                        ("true", "X"))


class OXBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", "-"), ("true", "O"),
                        ("false", "X"))


class RegisterFilter(django_filters.FilterSet):
    RO_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '일치 검색'}),
        field_name='RO_number', lookup_expr='exact', label="RO번호")
    car_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='car_number', lookup_expr='icontains', label="차량번호")
    abroad_type = django_filters.ChoiceFilter(
        choices=Register._meta.get_field('abroad_type').choices,
        label="해외차여부")
    insurance_agent = django_filters.ModelChoiceFilter(
        field_name='insurance_agent', queryset=InsuranceAgent.objects.all(),
        label="보험 담당자")
    supporter = django_filters.ModelChoiceFilter(
        field_name='supporter', queryset=Supporter.objects.all(),
        label="입고지원")
    day_came_in__gte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gte', label="입고일(부터)")
    day_came_in__lte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lte', label="입고일(까지)")

    client_name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='client_name', lookup_expr='icontains', label="고객명")
    first_center_repaired = django_filters.BooleanFilter(
        field_name='first_center_repaired', label="1센터수리",
        widget=OXBooleanWidget())

    note = django_filters.BooleanFilter(
        field_name='note', label="비고여부", lookup_expr="isnull",
        widget=NullBooleanWidget())

    class Meta:
        model = Register
        fields = ["RO_number", "car_number", "client_name", ]


class RegisterFilterForOrderFilter(django_filters.FilterSet):
    car_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='car_number', lookup_expr='icontains', label="차량번호")
    abroad_type = django_filters.ChoiceFilter(
        choices=Register._meta.get_field('abroad_type').choices,
        label="해외차여부")
    insurance_agent = django_filters.ModelChoiceFilter(
        field_name='insurance_agent', queryset=InsuranceAgent.objects.all(),
        label="보험 담당자")
    supporter = django_filters.ModelChoiceFilter(
        field_name='supporter', queryset=Supporter.objects.all(),
        label="입고지원")
    day_came_in__gte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gte', label="입고일(부터)")
    day_came_in__lte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lte', label="입고일(까지)")

    client_name = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='client_name', lookup_expr='icontains', label="고객명")

    note = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='note', label="비고", lookup_expr="icontains")

    class Meta:
        model = Register
        fields = []


class OrderFilter(django_filters.FilterSet):
    charged_company = django_filters.ModelChoiceFilter(
        field_name='charged_company', queryset=ChargedCompany.objects.all(),
        label="보험사")
    receipt_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='receipt_number', lookup_expr='icontains', label="접수번호")
    phone_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='register__final_four_phone_number', lookup_expr='exact', label="핸드폰 뒷자리")

    charge__charge_date__gte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='charge__charge_date', lookup_expr='gte', label="청구일(부터)")
    charge__charge_date__lte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='charge__charge_date', lookup_expr='lte', label="청구일(까지)")
    deposit__deposit_date = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='deposit__deposit_date', lookup_expr='exact', label="입금일")

    status = django_filters.ChoiceFilter(
        choices=Order._meta.get_field('status').choices, label="상태")

    class Meta:
        model = Order
        fields = ["charge_type", "order_type"]


INCENTIVE_FILTER_CHOICES = (
    (date.today()+relativedelta(months=-1), "1개월"),
    (date.today()+relativedelta(months=-3), "3개월"),
    (date.today()+relativedelta(months=-6), "6개월"),
    (date.today()+relativedelta(months=-12), "1년"),
)


class IncentiveFilter(django_filters.FilterSet):
    register__car_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='register__car_number', lookup_expr='icontains', label="차량 번호"
    )
    register__supporter = django_filters.ModelChoiceFilter(
        queryset=Supporter.objects.all(), label="업체명")
    incentive_paid = django_filters.BooleanFilter(
        field_name='incentive_paid', label="지급여부",
        widget=OXBooleanWidget())
    day_came_in__gte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='register__day_came_in', lookup_expr='gte', label="입고일(부터)")
    day_came_in__lte = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='register__day_came_in', lookup_expr='lte', label="입고일(까지)")

    class Meta:
        model = Order
        fields = ["register__car_number",
                  "register__supporter", 'incentive_paid']
