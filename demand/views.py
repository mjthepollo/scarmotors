from datetime import date, datetime
from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import NumberInput, TextInput, modelformset_factory
from django.http import FileResponse  # Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.utility import go_to_previous_url_or_search_register, print_colored
from demand.excel_line_info import INDEXES
from demand.filter_forms import (IncentiveFilter, OrderFilter, RegisterFilter,
                                 RegisterFilterForOrderFilter)
from demand.key_model_forms import ChargeForm, DepositForm, PaymentForm
from demand.key_models import Charge, Deposit, Payment
from demand.sales_model_forms import (EditRegisterForm,
                                      EditSpecialRegisterForm, ExtraSalesForm,
                                      IncentiveForm, NewRegisterForm,
                                      OrderForm, RegisterNoteForm)
from demand.sales_models import ExtraSales, Order, Register
from demand.utility import print_fields


@login_required
def new_register(request):
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=1, can_delete=True)
    if request.method == "GET":
        register_form = NewRegisterForm(initial={'day_came_in': date.today()})
        register_note_form = RegisterNoteForm()
        order_formset = order_form_factory(
            queryset=Order.objects.none())
        return render(request, "demand/new_register.html", context={
            "register_form": register_form,
            "register_note_form": register_note_form,
            "order_formset": order_formset,
        })
    else:
        print(request.POST)
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
                register_note_form = RegisterNoteForm(
                    request.POST, instance=register)
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
    order_form_factory = modelformset_factory(
        Order, form=OrderForm, extra=0, can_delete=True)
    if request.method == "GET":
        register_form = EditRegisterForm(instance=register)
        edit_special_register_form = EditSpecialRegisterForm(instance=register)
        register_note_form = RegisterNoteForm(instance=register)
        order_formset = order_form_factory(
            queryset=Order.objects.none(), prefix="order_formset")
        order_forms = [OrderForm(instance=order, prefix=f"order-{i}")
                       for i, order in enumerate(register.all_orders)]
        payment_forms = [PaymentForm(
            instance=order.payment, prefix=f"payment-{i}")
            for i, order in enumerate(register.all_orders)]
        charge_forms = [ChargeForm(
            instance=order.charge, prefix=f"charge-{i}", order=order)
            for i, order in enumerate(register.all_orders)]
        deposit_forms = [DepositForm(
            instance=order.deposit, prefix=f"deposit-{i}", order=order)
            for i, order in enumerate(register.all_orders)]
        return render(request, "demand/edit_register.html", context={
            "register": register,
            "register_form": register_form,
            'edit_special_register_form': edit_special_register_form,
            "register_note_form": register_note_form,
            "order_formset": order_formset,
            "order_forms": order_forms,
            "payment_forms": payment_forms,
            "charge_forms": charge_forms,
            "deposit_forms": deposit_forms,
        })
    else:
        register_form = EditRegisterForm(request.POST, instance=register)
        edit_special_register_form = EditSpecialRegisterForm(
            request.POST, instance=register)
        register_note_form = RegisterNoteForm(request.POST, instance=register)
        order_formset = order_form_factory(
            request.POST, queryset=Order.objects.none(), prefix="order_formset")
        order_forms = [OrderForm(request.POST, instance=order, prefix=f"order-{i}")
                       for i, order in enumerate(register.all_orders)]
        payment_forms = [PaymentForm(
            request.POST, instance=order.payment, prefix=f"payment-{i}")
            for i, order in enumerate(register.all_orders)]
        charge_forms = [ChargeForm(
            request.POST, instance=order.charge, prefix=f"charge-{i}", order=order)
            for i, order in enumerate(register.all_orders)]
        deposit_forms = [DepositForm(
            request.POST, instance=order.deposit, prefix=f"deposit-{i}", order=order)
            for i, order in enumerate(register.all_orders)]
        order_forms_are_valid = not (
            False in [form.is_valid() for form in order_forms])
        payment_forms_are_valid = not (
            False in [form.is_valid() for form in payment_forms])
        charge_forms_are_valid = not (
            False in [form.is_valid() for form in charge_forms])
        deposit_forms_are_valid = not (
            False in [form.is_valid() for form in deposit_forms])
        if register_form.is_valid() and \
                edit_special_register_form.is_valid() and \
                register_note_form.is_valid() and \
                order_formset.is_valid() and \
                order_forms_are_valid and \
                payment_forms_are_valid and \
                charge_forms_are_valid and \
                deposit_forms_are_valid:
            register = register_form.save()
            edit_special_register_form.save()
            register_note_form.save()
            for i, order in enumerate(register.all_orders):
                order = order_forms[i].save()
                payment = payment_forms[i].save()
                deposit = deposit_forms[i].save()
                charge = charge_forms[i].save()
                if payment.is_default():
                    order.payment = None
                    payment.delete()
                else:
                    order.payment = payment
                if deposit.is_default():
                    order.deposit = None
                    deposit.delete()
                else:
                    order.deposit = deposit
                if charge.is_default():
                    order.charge = None
                    charge.delete()
                else:
                    order.charge = charge
                order.save()
            new_orders = order_formset.save()
            for new_order in new_orders:
                new_order.register = register
                new_order.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)
        return render(request, "demand/edit_register.html", context={
            "register": register,
            "register_form": register_form,
            'edit_special_register_form': edit_special_register_form,
            "register_note_form": register_note_form,
            "order_formset": order_formset,
            "order_forms": order_forms,
            "payment_forms": payment_forms,
            "charge_forms": charge_forms,
            "deposit_forms": deposit_forms,
        })


@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_form = OrderForm(instance=order, prefix="order-0")
    payment_form = PaymentForm(instance=order.payment, prefix="payment-0")
    charge_form = ChargeForm(instance=order.charge,
                             order=order, prefix="charge-0")
    deposit_form = DepositForm(
        instance=order.deposit, prefix="deposit-0", order=order)
    if request.method == "GET":
        return render(request, "demand/edit_order.html", context={
            "order_form": order_form,
            "payment_form": payment_form,
            "charge_form": charge_form,
            "deposit_form": deposit_form,
        })
    else:
        order_form = OrderForm(request.POST, instance=order, prefix="order-0")
        payment_form = PaymentForm(
            request.POST, instance=order.payment, prefix="payment-0")
        charge_form = ChargeForm(
            request.POST, instance=order.charge, order=order, prefix="charge-0")
        deposit_form = DepositForm(
            request.POST, instance=order.deposit, prefix="deposit-0", order=order)
        if order_form.is_valid() and payment_form.is_valid() and charge_form.is_valid() and deposit_form.is_valid():
            order_form.save()
            payment_form.save()
            charge_form.save()
            deposit_form.save()
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
        else:
            return render(request, "demand/edit_order.html", context={
                "order_form": order_form,
                "payment_form": payment_form,
                "charge_form": charge_form,
                "deposit_form": deposit_form,
            })


@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    pass


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
    deposit_form = DepositForm(instance=order.deposit, order=order)
    if request.method == "GET":
        return render(request, "demand/order_deposit.html", context={
            "deposit_form": deposit_form,
        })
    else:
        deposit_form = DepositForm(
            request.POST, instance=order.deposit, order=order)
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
    return go_to_previous_url_or_search_register(request, order.register)


@login_required
def cancel_manually_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.cancel_manually_complete()
    return go_to_previous_url_or_search_register(request, order.register)


@login_required
def incentive(request):
    if request.path == request.get_full_path():
        return redirect(reverse("demand:incentive")+f"?day_came_in__gt={date.today().replace(day=1)}&day_came_in__ls={date.today()}")
    incentive_filter = IncentiveFilter(
        request.GET, queryset=Order.objects.all())
    if request.GET.get("register__supporter", None):
        orders = incentive_filter.qs
    else:
        orders = Order.objects.none()
    incentive_form_factory = modelformset_factory(
        Order, form=IncentiveForm, extra=0)
    supporter = orders.first().register.supporter if orders.exists() else None
    if request.method == "GET":
        incentive_formset = incentive_form_factory(
            queryset=orders, prefix="incentive")
    else:
        incentive_formset = incentive_form_factory(
            request.POST, queryset=orders, prefix="incentive")
        saved_orders = incentive_formset.save()
        for saved_order in saved_orders:
            saved_order.incentive_paid_date = date.today()
            saved_order.save()
    return render(request, "demand/incentive.html", context={
        "incentive_filter": incentive_filter,
        "supporter": supporter,
        "incentive_formset": incentive_formset,
    })


@login_required
def search_extra_sales(request):
    all_extra_sales = ExtraSales.objects.all()
    for extra_sales in all_extra_sales:
        print_fields(extra_sales)
        print_fields(extra_sales.payment)
        print_fields(extra_sales.charge)
        print(extra_sales.get_charge_amount())
    return render(request, "demand/search_extra_sales.html", context={"all_extra_sales": all_extra_sales})


@login_required
def new_extra_sales(request):
    if request.method == "GET":
        extra_sales_form = ExtraSalesForm()
        return render(request, "demand/new_extra_sales.html", context={
            "extra_sales_form": extra_sales_form,
        })
    else:
        extra_sales_form = ExtraSalesForm(request.POST)
        if extra_sales_form.is_valid():
            extra_sales = extra_sales_form.save()
            return redirect(reverse("demand:search_extra_sales"))
        else:
            return render(request, "demand/new_extra_sales.html", context={
                "extra_sales_form": extra_sales_form,
            })


@login_required
def edit_extra_sales(request, pk):
    extra_sales = ExtraSales.objects.get(pk=pk)
    if request.method == "GET":
        extra_sales_form = ExtraSalesForm(instance=extra_sales)
        return render(request, "demand/edit_extra_sales.html", context={
            "extra_sales_form": extra_sales_form,
        })
    else:
        extra_sales_form = ExtraSalesForm(request.POST, instance=extra_sales)
        if extra_sales_form.is_valid():
            extra_sales = extra_sales_form.save()
            return redirect(reverse("demand:search_extra_sales"))
        else:
            return render(request, "demand/edit_extra_sales.html", context={
                "extra_sales_form": extra_sales_form,
            })


# 차량번호 검색
# RO 번호 검색
#
