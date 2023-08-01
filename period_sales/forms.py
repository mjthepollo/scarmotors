from datetime import date

from django import forms


class PeriodFilter(forms.Form):
    year = forms.ChoiceField(
        choices=[(x, x)for x in range(2023, date.today().year+1)], label="년도",
        widget=forms.Select(attrs={'class': 'form-select'}))
    half = forms.ChoiceField(
        choices=[("first", "상반기"), ("second", "하반기"), ("all", "전체")], label="분기",
        widget=forms.Select(attrs={'class': 'form-select'}))


class DeadlineFilter(forms.Form):
    charge__charge_date__gte = forms.DateField(
        label="청구일(부터)", widget=forms.DateInput(attrs={'type': 'date', 'required': 'required'}), required=False)
    charge__charge_date__lte = forms.DateField(
        label="청구일(까지)", widget=forms.DateInput(attrs={'type': 'date', "required": "required"}), required=False)
