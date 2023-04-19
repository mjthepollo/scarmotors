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


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"


class NewOrderForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ["RO_number", "insurance_agent",]


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        exclude = ["order", "payment", "charge"]
