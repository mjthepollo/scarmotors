from django import forms


class PeriodFilter(forms.Form):
    year = forms.ChoiceField(
        choices=[(x, x)for x in range(2023, 2024)], label="년도",
        widget=forms.Select(attrs={'class': 'form-select'}))
    half = forms.ChoiceField(
        choices=[("first", "상반기"), ("second", "하반기")], label="분기",
        widget=forms.Select(attrs={'class': 'form-select'}))
