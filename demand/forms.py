import django_filters
from django import forms

from demand.models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                           Order, Payment, Register, Supporter)


class SupporterForm(forms.ModelForm):
    class Meta:
        model = Supporter
        fields = ["name", "active"]


class ChargedCompanyForm(forms.ModelForm):
    class Meta:
        model = ChargedCompany
        fields = ["name", "active"]


class InsuranceAgentForm(forms.ModelForm):
    class Meta:
        model = InsuranceAgent
        fields = ["name", "active"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'refund_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = "__all__"


class NewRegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        exclude = ["RO_number", "real_day_came_out"]
        widgets = {
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
        }


class RegisterFilter(django_filters.FilterSet):
    car_number = django_filters.CharFilter(
        field_name='car_number', lookup_expr='icontains', label="차량번호")

    day_came_in__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gt', label="입고일(~부터)")
    day_came_in__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lt', label="입고일(~까지)")

    real_day_came_out__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='gt', label="출고일(~부터)")
    real_day_came_out__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='lt', label="출고일(~까지)")

    client_name = django_filters.CharFilter(
        field_name='client_name', lookup_expr='icontains', label="고객명")

    note = django_filters.CharFilter(
        field_name='note', lookup_expr='icontains', label="비고(차)")

    class Meta:
        model = Register
        fields = ["RO_number", "car_number",
                  "supporter", "client_name", "insurance_agent", "note"]


class RegisterFilterForOrderFilter(django_filters.FilterSet):
    car_number = django_filters.CharFilter(
        field_name='car_number', lookup_expr='icontains', label="차량번호")

    day_came_in__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='gt', label="입고일(~부터)")
    day_came_in__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='day_came_in', lookup_expr='lt', label="입고일(~까지)")

    real_day_came_out__gt = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='gt', label="출고일(~부터)")
    real_day_came_out__ls = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='real_day_came_out', lookup_expr='lt', label="출고일(~까지)")

    note = django_filters.CharFilter(
        field_name='note', lookup_expr='icontains', label="비고(차)")

    class Meta:
        model = Register
        fields = ["car_number", "supporter",
                  "client_name", "insurance_agent", "note"]


class OrderFilter(django_filters.FilterSet):
    receipt_number = django_filters.CharFilter(
        field_name='receipt_number', lookup_expr='icontains', label="접수번호")

    note = django_filters.CharFilter(
        field_name='note', lookup_expr='icontains', label="비고(주문)")

    class Meta:
        model = Order
        fields = ["charged_company", "charge_type", "order_type"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["register", "payment", "charge", "deposit",]


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = "__all__"
