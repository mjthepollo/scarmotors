from datetime import date

from django import forms


class PeriodFilter(forms.Form):
    year = forms.ChoiceField(
        choices=[(x, x)for x in range(2023, date.today().year+1)], label="년도",
        widget=forms.Select(attrs={'class': 'form-select'}))
    half = forms.ChoiceField(
        choices=[("first", "상반기"), ("second", "하반기"), ("all", "전체")], label="분기",
        widget=forms.Select(attrs={'class': 'form-select'}))
