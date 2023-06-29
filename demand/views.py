from datetime import date, datetime
from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import NumberInput, TextInput, modelformset_factory
from django.http import FileResponse  # Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from demand.excel_line_info import INDEXES
from demand.forms import (ChargeForm, DepositForm, EditRegisterForm,
                          NewRegisterForm, OrderFilter, OrderForm, PaymentForm,
                          RegisterFilter, RegisterFilterForOrderFilter)
from demand.key_models import Charge, Deposit, Payment
from demand.sales_models import ExtraSales, Order, Register


@login_required
def new_register(request):
    register_form = NewRegisterForm(initial={'day_came_in': date.today()})
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
    register_form = EditRegisterForm(instance=register)
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=0)
    payment_form_factory = modelformset_factory(
        Payment, form=PaymentForm, extra=0)
    charge_form_factory = modelformset_factory(
        Charge, form=ChargeForm, extra=0)
    deposit_form_factory = modelformset_factory(
        Deposit, form=DepositForm, extra=0)
    if request.method == "GET":
        order_formset = order_form_factory(
            queryset=register.orders.all(), prefix="order")
        payment_formset = payment_form_factory(
            queryset=register.get_mockups(Payment, "payment"), prefix="payment")
        charge_formset = charge_form_factory(
            queryset=register.get_mockups(Charge, "charge"), prefix="charge")
        deposit_formset = deposit_form_factory(
            queryset=register.get_mockups(Deposit, "deposit"), prefix="deposit")
        return render(request, "demand/edit_register.html", context={
            "register": register,
            "register_form": register_form,
            "order_formset": order_formset,
            "charge_formset": charge_formset,
            "payment_formset": payment_formset,
            "deposit_formset": deposit_formset,
        })
    else:
        register_form = EditRegisterForm(request.POST, instance=register)
        order_formset = order_form_factory(
            request.POST, queryset=register.orders.all(), prefix="order")
        payment_formset = payment_form_factory(
            request.POST, queryset=register.get_mockups(Payment, "payment"),
            prefix="payment")
        charge_formset = charge_form_factory(
            request.POST, queryset=register.get_mockups(Charge, "charge"),
            prefix="charge")
        deposit_formset = deposit_form_factory(
            request.POST, queryset=register.get_mockups(Deposit, "deposit"),
            prefix="deposit")
        if register_form.is_valid() and \
                order_formset.is_valid() and \
                payment_formset.is_valid() and \
                charge_formset.is_valid() and \
                deposit_formset.is_valid():
            register = register_form.save()
            payment_formset.save()
            charge_formset.save()
            deposit_formset.save()
            order_formset.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)
        return render(request, "demand/edit_register.html", context={
            "register": register,
            "register_form": register_form,
            "order_formset": order_formset,
            "charge_formset": charge_formset,
            "payment_formset": payment_formset,
            "deposit_formset": deposit_formset,
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


@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register, pk=pk)


@ login_required
def search_registers(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    page_num = int(request.GET.get('page_num', 20))
    paginator = Paginator(register_filter.qs, page_num)
    page = request.GET.get('page')
    registers = paginator.get_page(page)
    return render(request, "demand/search_registers.html",
                  context={"register_filter": register_filter,
                           "page_num": page_num,
                           "download_url": reverse("demand:registers_to_excel")+"?"+request.GET.urlencode(),
                           "table_view_url": reverse("demand:search_registers_table_view")+"?"+request.GET.urlencode(),
                           "registers": registers})
# 차량번호 검색


def search_registers_table_view(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    registers = register_filter.qs
    lines = [order.to_excel_line()
             for register in registers for order in register.orders.all()]
    df = pd.DataFrame(lines, columns=INDEXES.values())
    return render(request, "demand/table_view.html", context={
        "table": df.to_html(classes="table table-striped table-bordered table-hover")
    })


def registers_to_excel(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    registers = register_filter.qs
    lines = [order.to_excel_line()
             for register in registers for order in register.orders.all()]
    df = pd.DataFrame(lines, columns=INDEXES.values())
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.book.save(output)
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}.xlsx'
    return response


@ login_required
def search_orders(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs))
    page_num = int(request.GET.get('page_num', 20))
    paginator = Paginator(order_filter.qs, page_num)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, "demand/search_orders.html",
                  context={"register_filter": register_filter,
                           "order_filter": order_filter,
                           "page_num": page_num,
                           "table_view_url": reverse("demand:search_orders_table_view")+"?"+request.GET.urlencode(),
                           "download_url": reverse("demand:orders_to_excel")+"?"+request.GET.urlencode(),
                           "orders": orders})


def search_orders_table_view(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs))
    orders = order_filter.qs
    lines = [order.to_excel_line() for order in orders]
    df = pd.DataFrame(lines, columns=INDEXES.values())
    return render(request, "demand/table_view.html", context={
        "table": df.to_html(classes="table table-striped table-bordered table-hover")
    })


def orders_to_excel(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs))
    orders = order_filter.qs
    lines = [order.to_excel_line() for order in orders]
    df = pd.DataFrame(lines, columns=INDEXES.values())
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.book.save(output)
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}.xlsx'
    return response


@login_required
def order_charge(request, pk):
    order = get_object_or_404(Order, pk=pk)
    charge_form = ChargeForm(instance=order.charge)
    payment_form = PaymentForm(instance=order.payment)
    if request.method == "GET":
        return render(request, "demand/order_charge.html", context={
            "charge_form": charge_form,
            "payment_form": payment_form,
        })
    else:
        charge_form = ChargeForm(request.POST, instance=order.charge)
        payment_form = PaymentForm(request.POST, instance=order.payment)
        if charge_form.is_valid() and payment_form.is_valid():
            charge_form.save()
            payment_form.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
        else:
            return render(request, "demand/order_charge.html", context={
                "charge_form": charge_form,
                "payment_form": payment_form,
            })


@login_required
def order_deposit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    deposit_form = DepositForm(instance=order.deposit)
    if request.method == "GET":
        return render(request, "demand/order_deposit.html", context={
            "deposit_form": deposit_form,
        })
    else:
        deposit_form = DepositForm(request.POST, instance=order.deposit)
        if deposit_form.is_valid():
            deposit_form.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
        else:
            return render(request, "demand/order_deposit.html", context={
                "deposit_form": deposit_form,
            })


@login_required
def make_manually_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.make_manually_complete()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def cancel_manually_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.cancel_manually_complete()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def extra_sales(request):
    return render(request, "demand/extra_sales.html", context={"extra_sales_queryset": ExtraSales.objects.all()})

# 차량번호 검색
# RO 번호 검색
#
