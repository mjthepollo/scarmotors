import django_filters
from django import forms

from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.sales_models import ExtraSales, Order, Register


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
        fields = ["car_number", "day_came_in", "expected_day_came_out",
                  "car_model", "abroad_type", "number_of_repair_works",
                  "number_of_exchange_works", "supporter", "client_name",
                  "insurance_agent", "phone_number", "rentcar_company_name",
                  "note"]
        widgets = {
            'car_number': forms.TextInput(attrs={'placeholder': '12가1234'}),
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'car_model': forms.TextInput(attrs={'placeholder': '아반떼'}),
            'client_name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '01012345678'}),
            'rentcar_company_name': forms.TextInput(attrs={'placeholder': '에스카렌트'}),
            'note': forms.Textarea(attrs={'placeholder': '메모, 특이사항 등'}),
        }


class EditRegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ["car_number", "day_came_in", "expected_day_came_out", "real_day_came_out",
                  "car_model", "abroad_type", "number_of_repair_works",
                  "number_of_exchange_works", "supporter", "client_name",
                  "insurance_agent", "phone_number", "rentcar_company_name",
                  "note", "unrepaired", "wasted"]
        widgets = {
            'car_number': forms.TextInput(attrs={'placeholder': '12가1234'}),
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'car_model': forms.TextInput(attrs={'placeholder': '아반떼'}),
            'client_name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '01012345678'}),
            'rentcar_company_name': forms.TextInput(attrs={'placeholder': '에스카렌트'}),
            'note': forms.Textarea(attrs={'placeholder': '메모, 특이사항 등'}),
        }


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

    note = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='note', lookup_expr='icontains', label="비고(차)")

    class Meta:
        model = Register
        fields = ["RO_number", "car_number",
                  "supporter", "client_name", "insurance_agent", "note"]


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
        field_name='note', lookup_expr='icontains', label="비고(차)")

    class Meta:
        model = Register
        fields = ["car_number", "supporter",
                  "client_name", "insurance_agent", "note"]


class OrderFilter(django_filters.FilterSet):
    receipt_number = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='receipt_number', lookup_expr='icontains', label="접수번호")

    note = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'placeholder': '포함 검색'}),
        field_name='note', lookup_expr='icontains', label="비고(주문)")

    status = django_filters.MultipleChoiceFilter(
        choices=Order._meta.get_field('status').choices, label="상태")

    class Meta:
        model = Order
        fields = ["status", "charged_company", "charge_type", "order_type"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["charge_type", "charged_company",
                  "order_type", "receipt_number", "fault_ratio"]
        widgets = {
            'receipt_number': forms.TextInput(),
            'fault_ratio': forms.NumberInput(),
        }

        labels = {
            "fault_ratio": "과실분(%)"
        }


class EditOrderForm(forms.ModelForm):
    # Payment
    indemnity_amount = forms.IntegerField()
    discount_amount = forms.IntegerField()
    refund_amount = forms.IntegerField()

    # Charge

    # Deposit

    class Meta:
        model = Order
        fields = ["charge_type", "charged_company",
                  "order_type", "receipt_number", "fault_ratio"]
        widgets = {
            'receipt_number': forms.TextInput(),
            'fault_ratio': forms.NumberInput(),
        }

        labels = {
            "fault_ratio": "과실분(%)"
        }

    def save(self, commit=True):
        instance = super(EditOrderForm, self).save(commit=False)
        instance.flag1 = 'flag1' in self.cleaned_data['multi_choice']  # etc
        if commit:
            instance.save()
        return instance


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = "__all__"
