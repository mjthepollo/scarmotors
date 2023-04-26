from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import NumberInput, TextInput, modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from demand.forms import (ChargedCompanyForm, ChargeForm, InsuranceAgentForm,
                          NewRegisterForm, OrderForm, PaymentForm,
                          SupporterForm)
from demand.models import (Charge, ChargedCompany, InsuranceAgent, Order,
                           Payment, Register, Supporter)
from users.forms import CustomAuthForm


def login(request):
    if request.method == 'GET':
        login_form = CustomAuthForm(request)
        return render(request, "login.html", context={
            "login_form": login_form
        })
    else:
        login_form = CustomAuthForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login_user(request, user)
            return redirect(reverse("home"))
        else:
            return render(request, "login.html", context={"login_form": login_form})


def logout(request):
    logout_user(request)
    return redirect(reverse("login"))


@login_required
def home(request):
    return render(request, "home.html")
