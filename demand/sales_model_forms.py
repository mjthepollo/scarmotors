from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.forms import DetailableModelForm
from core.utility import insert_tag
from demand.key_models import (ChargedCompany, InsuranceAgent,
                               RequestDepartment, Supporter)
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register


class RealDayCameOutForm(DetailableModelForm):
    class Meta:
        model = Register
        fields = ["real_day_came_out"]
        widgets = {
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
        }


class SpecialRegisterForm(DetailableModelForm):
    class Meta:
        model = Register
        fields = ['wasted', 'unrepaired']


class FirstCenterRegisterForm(DetailableModelForm):
    class Meta:
        model = Register
        fields = ['first_center_repaired']


class EditSpecialRegisterForm(DetailableModelForm):
    class Meta:
        model = Register
        fields = ['wasted', 'unrepaired', 'first_center_repaired']


class NewRegisterForm(DetailableModelForm):
    supporter = forms.ModelChoiceField(
        queryset=Supporter.objects.filter(active=True), label="입고지원")
    insurance_agent = forms.ModelChoiceField(
        queryset=InsuranceAgent.objects.filter(active=True), label="보험 담당자")

    class Meta:
        model = Register
        fields = ["car_number", "day_came_in", "expected_day_came_out",
                  "car_model", "abroad_type", "number_of_repair_works",
                  "number_of_exchange_works", "supporter", "client_name",
                  "insurance_agent", "phone_number", "rentcar_company_name",]
        widgets = {
            'car_number': forms.TextInput(attrs={'placeholder': '12가1234'}),
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'car_model': forms.TextInput(attrs={'placeholder': '아반떼'}),
            'client_name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '01012345678'}),
            'rentcar_company_name': forms.TextInput(attrs={'placeholder': '에스카렌트'}),
        }

    def as_div(self, *args, **kwags):
        original_div = super(NewRegisterForm, self).as_div()
        inserting_tag = f"<div id='car_number_button_box'>\
            <button type='button' id='car_number_button'\
            class='btn btn-info'\
            data-modal_default_url='{reverse('demand:car_number_modal')}?car_number='>차량 번호 확인</button></div>"
        return_div = insert_tag(
            original_div, "car_number", inserting_tag)
        return mark_safe(return_div)


class RegisterNoteForm(DetailableModelForm):
    class Meta:
        model = Register
        fields = ["note"]
        widgets = {
            "note": forms.Textarea(attrs={'placeholder': '메모, 특이사항 등'}),
        }


class EditRegisterForm(DetailableModelForm):
    supporter = forms.ModelChoiceField(
        queryset=Supporter.objects.filter(active=True), label="입고지원")
    insurance_agent = forms.ModelChoiceField(
        queryset=InsuranceAgent.objects.filter(active=True), label="보험 담당자")

    class Meta:
        model = Register
        fields = ["car_number", "day_came_in", "expected_day_came_out", "real_day_came_out",
                  "car_model", "abroad_type", "number_of_repair_works",
                  "number_of_exchange_works", "supporter", "client_name",
                  "insurance_agent", "phone_number", "rentcar_company_name"]
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


class OrderForm(DetailableModelForm):
    template_name = "demand/forms/deletable_order_form.html"

    charged_company = forms.ModelChoiceField(
        queryset=ChargedCompany.objects.filter(active=True), label="보험(렌트)")

    class Meta:
        model = Order
        fields = ["charge_type", "charged_company",
                  "order_type", "receipt_number", "fault_ratio"]
        widgets = {
            "charge_type": forms.Select(attrs={'required': 'required'}),
            "charged_company": forms.Select(attrs={'required': 'required'}),
            'receipt_number': forms.TextInput(attrs={"placeholder": "12-3456"}),
            'fault_ratio': forms.NumberInput(attrs={"placeholder": "100"}),
        }

        labels = {
            "fault_ratio": "과실분(%)"
        }


class IncentiveForm(DetailableModelForm):
    class Meta:
        model = Order
        fields = ["incentive_paid"]


class ExtraSalesForm(DetailableModelForm):
    supporter = forms.ModelChoiceField(
        queryset=Supporter.objects.filter(active=True), label="입고지원")
    insurance_agent = forms.ModelChoiceField(
        queryset=InsuranceAgent.objects.filter(active=True), label="보험 담당자")

    class Meta:
        model = ExtraSales
        fields = ["day_came_in", "expected_day_came_out", "real_day_came_out",
                  "car_number", "car_model", "sort", "abroad_type", "supporter",
                  "insurance_agent", "client_name", "phone_number", "note"]
        widgets = {
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'expected_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'car_number': forms.TextInput(attrs={'placeholder': '12가1234'}),
            'car_model': forms.TextInput(attrs={'placeholder': '아반떼'}),
            'client_name': forms.TextInput(attrs={'placeholder': '홍길동'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '01012345678'}),
            'note': forms.Textarea(attrs={'placeholder': '메모, 특이사항 등'}),
        }


class ExtraSalesRealDayCameOutForm(DetailableModelForm):
    class Meta:
        model = ExtraSales
        fields = ["real_day_came_out"]
        widgets = {
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
        }


class RecognizedSalesForm(DetailableModelForm):
    request_department = forms.ModelChoiceField(
        queryset=RequestDepartment.objects.filter(active=True), label="요청부서")

    class Meta:
        model = RecognizedSales
        fields = ["day_came_in", "real_day_came_out",
                  "car_number", "request_department", "wage_amount",
                  "component_amount", "note"]
        widgets = {
            'day_came_in': forms.DateInput(attrs={'type': 'date'}),
            'real_day_came_out': forms.DateInput(attrs={'type': 'date'}),
            'car_number': forms.TextInput(attrs={'placeholder': '12가1234'}),
            'wage_amount': forms.TextInput(attrs={'placeholder': '기입 필요'}),
            'component_amount': forms.TextInput(attrs={'placeholder': '기입 필요'}),
            'note': forms.Textarea(attrs={'placeholder': '메모, 특이사항 등'}),
        }
