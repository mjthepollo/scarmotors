# Create your views here.
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import NumberInput, TextInput, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from demand.forms import (ChargeForm, DepositForm, NewRegisterForm, OrderForm,
                          PaymentForm, RegisterFilter)
from demand.models import Charge, Deposit, Order, Payment, Register


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
        return render(request, "demand/new_register.html", context={
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
                return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)
            else:
                register.delete()
                return render(request, "demand/new_register.html", context={
                    "register_form": register_form,
                    "order_formset": order_formset,
                })
        else:
            return render(request, "demand/new_register.html", context={
                "register_form": register_form,
                "order_formset": order_formset,
            })


@login_required
def edit_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    register_form = NewRegisterForm(instance=register)
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=0)
    if request.method == "GET":
        order_formset = order_form_factory(
            queryset=register.orders.all())
        return render(request, "demand/edit_register.html", context={
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
                return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)
            else:
                return render(request, "demand/edit_register.html", context={
                    "register_form": register_form,
                    "order_formset": order_formset,
                })
        else:
            return render(request, "demand/edit_register.html", context={
                "register_form": register_form,
                "order_formset": order_formset,
            })


@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_form = OrderForm(instance=order)
    deposit_form = DepositForm(instance=order.deposit)
    charge_form = ChargeForm(instance=order.charge)
    payment_form = PaymentForm(instance=order.payment)
    if request.method == "GET":
        return render(request, "demand/edit_order.html", context={
            "order_form": order_form,
            "deposit_form": deposit_form,
            "charge_form": charge_form,
            "payment_form": payment_form,
        })
    else:
        order_form = OrderForm(request.POST, instance=order)
        deposit_form = DepositForm(request.POST, instance=order.deposit)
        charge_form = ChargeForm(request.POST, instance=order.charge)
        payment_form = PaymentForm(request.POST, instance=order.payment)
        if order_form.is_valid() and deposit_form.is_valid() and charge_form.is_valid() and payment_form.is_valid():
            order_form.save()
            deposit_form.save()
            charge_form.save()
            payment_form.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
        else:
            return render(request, "demand/edit_order.html", context={
                "order_form": order_form,
                "deposit_form": deposit_form,
                "charge_form": charge_form,
                "payment_form": payment_form,
            })


@ login_required
def search_registers(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    paginator = Paginator(register_filter.qs, 20)
    page = request.GET.get('page')
    registers = paginator.get_page(page)
    return render(request, "demand/search_registers.html",
                  context={"register_filter": register_filter,
                           "registers": registers})
# 차량번호 검색


@ login_required
def search_sales(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    paginator = Paginator(register_filter.qs, 20)
    page = request.GET.get('page')
    registers = paginator.get_page(page)
    return render(request, "demand/search_registers.html",
                  context={"register_filter": register_filter,
                           "registers": registers})
# 차량번호 검색
# RO 번호 검색
#
