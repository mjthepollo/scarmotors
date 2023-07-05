from django import forms
from django.utils.safestring import mark_safe

from core.utility import insert_tag
from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, Supporter)
from demand.utility import zero_if_none


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
        fields = ["indemnity_amount", "discount_amount", "refund_amount",
                  "payment_type", 'payment_info', "payment_date", "refund_date"]
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'refund_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            "payment_info": "은행/카드"
        }

    def as_div(self, *args, **kwags):
        original_div = super(PaymentForm, self).as_div()
        inserting_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            결제금액:</label><span class='modal_additional_info settlement_amount_info'></span></div>"
        return_div = insert_tag(original_div, "discount_amount", inserting_tag)
        return mark_safe(return_div)


class ChargeForm(forms.ModelForm):
    """
    init할 때 Order가 필요하다!
    """
    class Meta:
        model = Charge
        fields = ["charge_date", 'wage_amount', "component_amount"]
        widgets = {
            'charge_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def as_div(self, *args, **kwargs):
        original_div = super(ChargeForm, self).as_div()
        inserting_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            수리금액:</label><span class='modal_additional_info repair_amount_info'></span></div>"
        return_div = insert_tag(
            original_div, "component_amount", inserting_tag)
        VAT_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            부가세:</label><span class='modal_additional_info VAT_info'></span></div>"
        chargable_amount_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>청구가능액:</label>\
                <span class='modal_additional_info chargable_amount_info'></span></div>"
        charge_amount_tag = f"<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            청구금액:</label><span class='modal_additional_info charge_amount_info'></span></div>"
        indemnity_amount = self.order.get_indemnity_amount() or ""
        fault_ratio = self.order.fault_ratio or ""
        refund_amount = zero_if_none(
            self.order.payment.refund_amount if self.order.payment else 0)
        indemnity_amount_data = f"data-indemnity_amount='{indemnity_amount}'"
        fault_ratio_data = f"data-fault_ratio='{fault_ratio}'"
        refund_amount_data = f"data-refund_amount='{refund_amount}'"
        data_tag = f"<div class='hidden charge_data' {indemnity_amount_data} {fault_ratio_data} {refund_amount_data}></div>"
        return_div = return_div + VAT_tag + \
            chargable_amount_tag + charge_amount_tag + data_tag
        return mark_safe(return_div)

    def __init__(self, *args, **kwargs):
        if kwargs.get('order', None):
            self.order = kwargs["order"]
        kwargs.pop('order', None)
        super(ChargeForm, self).__init__(*args, **kwargs)


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["deposit_date", 'deposit_amount', "deposit_note"]
        widgets = {
            'deposit_date': forms.DateInput(attrs={'type': 'date'}),
            'deposit_note': forms.Textarea(attrs={'class': 'deposit_note'}),
        }

    def as_div(self, *args, **kwags):
        original_div = super(DepositForm, self).as_div()
        inserting_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            지급율:</label><span class='modal_additional_info payment_rate_info'></span></div>"
        inserted_div = insert_tag(
            original_div, "deposit_date", inserting_tag)
        inserting_tag = "<div class='modal_additional_info_box'><label class='modal_additional_info_label'>\
            삭감율:</label><span class='modal_additional_info cut_rate_info'></span></div>"
        return_div = insert_tag(
            inserted_div, "deposit_amount", inserting_tag)
        return mark_safe(return_div)
