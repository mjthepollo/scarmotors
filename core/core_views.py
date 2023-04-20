from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms import NumberInput, TextInput, modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from demand.forms import (ChargedCompanyForm, ChargeForm, InsuranceAgentForm,
                          InsuranceForm, NewOrderForm, PaymentForm,
                          SupporterForm)
from demand.models import (Charge, ChargedCompany, Insurance, InsuranceAgent,
                           Order, Payment, Supporter)
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
def new_order(request):
    order_form = NewOrderForm(initial={
        'car_number': "TEST",
        'day_came_in': date.today()})
    insurance_form_factory = modelformset_factory(
        Insurance, form=InsuranceForm, extra=1)
    if request.method == "GET":
        insurance_formset = insurance_form_factory(
            queryset=Insurance.objects.none())
        return render(request, "new_order.html", context={
            "order_form": order_form,
            "insurance_formset": insurance_formset,
        })
    else:
        order_form = NewOrderForm(request.POST)
        insurance_formset = insurance_form_factory(
            request.POST, queryset=Insurance.objects.none())
        if order_form.is_valid():
            order = order_form.save()
            if insurance_formset.is_valid():
                insurnaces = insurance_formset.save()
                for insurance in insurnaces:
                    insurance.order = order
                    insurance.save()
                order.RO_number = Order.get_RO_number()
                order.save()
                return redirect(reverse("edit_order")+"?RO_number="+order.RO_number)
            else:
                order.delete()
                return render(request, "new_order.html", context={
                    "order_form": order_form,
                    "insurance_formset": insurance_formset,
                })
        else:
            return render(request, "new_order.html", context={
                "order_form": order_form,
                "insurance_formset": insurance_formset,
            })


@login_required
def edit_order(request):
    RO_number = request.GET.get("RO_number")
    order = Order.objects.get(RO_number=RO_number)
    order_form = NewOrderForm(instance=order)
    insurance_form_factory = modelformset_factory(
        Insurance, form=InsuranceForm, extra=0)
    if request.method == "GET":
        insurance_formset = insurance_form_factory(
            queryset=order.insurances.all())
        return render(request, "edit_order.html", context={
            "order_form": order_form,
            "insurance_formset": insurance_formset,
        })
    else:
        order_form = NewOrderForm(request.POST, instance=order)
        insurance_formset = insurance_form_factory(
            request.POST, queryset=order.insurances.all())
        if order_form.is_valid():
            order = order_form.save()
            if insurance_formset.is_valid():
                insurnaces = insurance_formset.save()
                for insurance in insurnaces:
                    insurance.order = order
                    insurance.save()
                order.save()
                return redirect(reverse("home"))
            else:
                return render(request, "edit_order.html", context={
                    "order_form": order_form,
                    "insurance_formset": insurance_formset,
                })
        else:
            return render(request, "edit_order.html", context={
                "order_form": order_form,
                "insurance_formset": insurance_formset,
            })


@ login_required
def finish_order(request):
    pass


@ login_required
def search_orders(request):
    pass
