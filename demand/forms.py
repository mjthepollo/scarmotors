from django import forms

from demand.models import (Charge, ChargedCompany, Insurance, InsuranceAgent,
                           Order, Payment, Supporter)


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
        model = Payment
        fields = "__all__"


class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["RO_number", "real_day_came_out"]
        widgets = {
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
        }


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        exclude = ["order", "payment", "charge"]
