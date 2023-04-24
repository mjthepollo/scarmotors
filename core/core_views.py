from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
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
from users.models import User


def login(request):
    if request.method == 'GET':
        login_form = AuthenticationForm(request)
        return render(request, "login.html", context={
            "login_form": login_form
        })
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login_user(request, user)
            return redirect(reverse("home"))
        else:
            return render(request, "login.html", context={"login_form": login_form})


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def new_register(request):
    register_form = NewRegisterForm(initial={
        'car_number': "TEST",
        'day_came_in': date.today()})
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=1)
    if request.method == "GET":
        order_formset = order_form_factory(
            queryset=Order.objects.none())
        return render(request, "new_register.html", context={
            "register_form": register_form,
            "order_formset": order_formset,
        })
    else:
        register_form = NewRegisterForm(request.POST)
        order_formset = order_form_factory(
            request.POST, queryset=Order.objects.none())
        if register_form.is_valid():
            register = register_form.save()
            if order_formset.is_valid():
                orders = order_formset.save()
                for order in orders:
                    order.register = register
                    order.save()
                register.RO_number = Register.get_RO_number()
                register.save()
                return redirect(reverse("edit_register")+"?RO_number="+Register.RO_number)
            else:
                register.delete()
                return render(request, "new_register.html", context={
                    "register_form": register_form,
                    "order_formset": order_formset,
                })
        else:
            return render(request, "new_register.html", context={
                "register_form": register_form,
                "order_formset": order_formset,
            })


@login_required
def edit_register(request):
    RO_number = request.GET.get("RO_number")
    register = Register.objects.get(RO_number=RO_number)
    register_form = NewRegisterForm(instance=register)
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=0)
    if request.method == "GET":
        order_formset = order_form_factory(
            queryset=register.orders.all())
        return render(request, "edit_register.html", context={
            "register_form": register_form,
            "order_formset": order_formset,
        })
    else:
        register_form = NewRegisterForm(request.POST, instance=register)
        order_formset = order_form_factory(
            request.POST, queryset=register.orders.all())
        if register_form.is_valid():
            register = register_form.save()
            if order_formset.is_valid():
                orders = order_formset.save()
                for order in orders:
                    order.register = register
                    order.save()
                register.save()
                return redirect(reverse("home"))
            else:
                return render(request, "edit_register.html", context={
                    "register_form": register_form,
                    "order_formset": order_formset,
                })
        else:
            return render(request, "edit_register.html", context={
                "register_form": register_form,
                "order_formset": order_formset,
            })


@ login_required
def finish_register(request):
    pass


@ login_required
def search_registers(request):
    return render(request, "search_registers.html")
# 차량번호 검색
# RO 번호 검색
#
