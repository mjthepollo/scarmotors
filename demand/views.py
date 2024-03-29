from datetime import date, datetime
from io import BytesIO

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import NumberInput, TextInput, modelformset_factory
from django.http import FileResponse  # Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.utility import (get_main_charged_company_pks,
                          go_to_previous_url_or_search_register)
from demand.excel_line_info import INDEXES
from demand.filter_forms import (IncentiveFilter, OrderFilter, RegisterFilter,
                                 RegisterFilterForOrderFilter)
from demand.key_model_forms import ChargeForm, DepositForm, PaymentForm
from demand.sales_model_forms import (EditRegisterForm,
                                      EditSpecialRegisterForm, ExtraSalesForm,
                                      IncentiveForm, NewRegisterForm,
                                      OrderForm, RecognizedSalesForm,
                                      RegisterNoteForm)
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register
from demand.utility import print_fields
from period_sales.forms import DeadlineFilter
from period_sales.models import DeadlineInfoOfPeriod


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


def get_registers_from_filter_and_page(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    page_num = int(request.GET.get('page_num', 50))
    paginator = Paginator(register_filter.qs, page_num)
    page = request.GET.get('page')
    registers = paginator.get_page(page)
    return registers


@ login_required
def search_registers(request):
    register_filter = RegisterFilter(
        request.GET, queryset=Register.objects.all())
    page_num = int(request.GET.get('page_num', 50))
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
    registers = get_registers_from_filter_and_page(request)
    lines = [order.to_excel_line()
             for register in registers for order in register.orders.all()]
    lines.reverse()
    df = pd.DataFrame(lines, columns=INDEXES.values())
    return render(request, "demand/table_view.html", context={
        "table": df.to_html(classes="table table-striped table-bordered table-hover")
    })


def registers_to_excel(request):
    registers = get_registers_from_filter_and_page(request)
    lines = [order.to_excel_line()
             for register in registers for order in register.orders.all()]
    lines.reverse()
    df = pd.DataFrame(lines, columns=INDEXES.values())
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}.xlsx'
    return response


def get_orders_from_filter_and_page(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs))
    page_num = int(request.GET.get('page_num', 50))
    paginator = Paginator(order_filter.qs, page_num)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return orders


@ login_required
def search_orders(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs))
    page_num = int(request.GET.get('page_num', 50))
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


@login_required
def search_etc_insurances_orders(request):
    register_filter = RegisterFilterForOrderFilter(
        request.GET, queryset=Register.objects.all())
    main_charged_company_pks = get_main_charged_company_pks().values()
    order_filter = OrderFilter(
        request.GET, queryset=Order.objects.filter(register__in=register_filter.qs).exclude(
            charged_company__in=main_charged_company_pks))
    page_num = int(request.GET.get('page_num', 50))
    paginator = Paginator(order_filter.qs, page_num)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, "demand/search_etc_insurances_orders.html",
                  context={"register_filter": register_filter,
                           "order_filter": order_filter,
                           "page_num": page_num,
                           "orders": orders})


def search_orders_table_view(request):
    orders = get_orders_from_filter_and_page(request)
    lines = [order.to_excel_line() for order in orders]
    lines.reverse()
    df = pd.DataFrame(lines, columns=INDEXES.values())
    return render(request, "demand/table_view.html", context={
        "table": df.to_html(classes="table table-striped table-bordered table-hover")
    })


def orders_to_excel(request):
    orders = get_orders_from_filter_and_page(request)
    lines = [order.to_excel_line() for order in orders]
    lines.reverse()
    df = pd.DataFrame(lines, columns=INDEXES.values())
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}.xlsx'
    return response


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
        return redirect(reverse("demand:incentive")+f"?day_came_in__gte={date.today().replace(day=1)}&day_came_in__lte={date.today()}")
    incentive_filter = IncentiveFilter(
        request.GET, queryset=Order.objects.all())
    incentive_filter.form.label_suffix = ""
    if not request.GET.get("register__supporter", None) and not request.GET.get("register__car_number", None):
        orders = Order.objects.none()
    else:
        orders = incentive_filter.qs
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
def undo_incentive(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.incentive_paid_date = None
    order.incentive_paid = False
    order.save()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:incentive"))


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
            extra_sales_form.save()
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


@login_required
def search_recognized_sales(request):
    all_recognized_sales = RecognizedSales.objects.all()
    return render(request, "demand/search_recognized_sales.html", context={"all_recognized_sales": all_recognized_sales})


@login_required
def recognized_sales_to_excel(request):
    all_recognized_sales = RecognizedSales.objects.all()
    lines = [recognized_sales.to_excel_line()
             for recognized_sales in all_recognized_sales]
    lines.reverse()
    df = pd.DataFrame(lines, columns=[
                      "월", "입고", "출고", "차량번호", "요청부서", "공임", "부품", "수리금액", "비고", "공장매출"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='인정매출')
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="인정매출{datetime.now()}.xlsx'
    return response


@login_required
def new_recognized_sales(request):
    if request.method == "GET":
        recognized_sales_form = RecognizedSalesForm()
        return render(request, "demand/new_recognized_sales.html", context={
            "recognized_sales_form": recognized_sales_form,
        })
    else:
        recognized_sales_form = RecognizedSalesForm(request.POST)
        if recognized_sales_form.is_valid():
            recognized_sales_form.save()
            return redirect(reverse("demand:search_recognized_sales"))
        else:
            return render(request, "demand/new_recognized_sales.html", context={
                "recognized_sales_form": recognized_sales_form,
            })


@login_required
def edit_recognized_sales(request, pk):
    recognized_sales = RecognizedSales.objects.get(pk=pk)
    if request.method == "GET":
        recognized_sales_form = RecognizedSalesForm(instance=recognized_sales)
        return render(request, "demand/edit_recognized_sales.html", context={
            "recognized_sales_form": recognized_sales_form,
        })
    else:
        recognized_sales_form = RecognizedSalesForm(
            request.POST, instance=recognized_sales)
        if recognized_sales_form.is_valid():
            recognized_sales = recognized_sales_form.save()
            return redirect(reverse("demand:search_recognized_sales"))
        else:
            return render(request, "demand/edit_recognized_sales.html", context={
                "recognized_sales_form": recognized_sales_form,
            })


@login_required
def deadline(request):
    if request.path == request.get_full_path():
        return redirect(reverse("demand:deadline")+f"?charge__charge_date__gte={date.today().replace(day=1)}&charge__charge_date__lte={date.today()}")
    deadline_filter = DeadlineFilter(request.GET)
    deadline_filter.label_suffix = ""
    if deadline_filter.is_valid():
        charge__charge_date__gte = deadline_filter.cleaned_data["charge__charge_date__gte"]
        charge__charge_date__lte = deadline_filter.cleaned_data["charge__charge_date__lte"]
    else:
        raise ("DeadlineFilter is not valid!")
    if charge__charge_date__gte and charge__charge_date__lte:
        deadline_info_of_period = DeadlineInfoOfPeriod(
            charge__charge_date__gte, charge__charge_date__lte)
    else:
        deadline_info_of_period = None
    return render(request, "deadline.html", context={
        "deadline_filter": deadline_filter,
        "deadline_info_of_period": deadline_info_of_period,
        "download_url": reverse("demand:deadline_to_excel")+"?"+request.GET.urlencode(),
    })


@login_required
def deadline_to_excel(request):
    deadline_filter = DeadlineFilter(request.GET)
    deadline_filter.label_suffix = ""
    if deadline_filter.is_valid():
        charge__charge_date__gte = deadline_filter.cleaned_data["charge__charge_date__gte"]
        charge__charge_date__lte = deadline_filter.cleaned_data["charge__charge_date__lte"]
    else:
        raise ("DeadlineFilter is not valid!")
    deadline_info_of_period = DeadlineInfoOfPeriod(
        charge__charge_date__gte, charge__charge_date__lte)
    lines_for_general = [order.to_excel_line()
                         for register in deadline_info_of_period.registers_for_general for order in register.orders.all()]
    lines_for_rent = [order.to_excel_line()
                      for register in deadline_info_of_period.registers_for_rent for order in register.orders.all()]
    lines_for_domestic_insurance = [order.to_excel_line()
                                    for register in deadline_info_of_period.registers_for_domestic_insurance for order in register.orders.all()]
    lines_for_abroad_insurance = [order.to_excel_line()
                                  for register in deadline_info_of_period.registers_for_abroad_insurance for order in register.orders.all()]
    lines_for_general.reverse()
    lines_for_rent.reverse()
    lines_for_domestic_insurance.reverse()
    lines_for_abroad_insurance.reverse()
    df_for_general = pd.DataFrame(lines_for_general, columns=INDEXES.values())
    df_for_rent = pd.DataFrame(lines_for_rent, columns=INDEXES.values())
    df_for_domestic_insurance = pd.DataFrame(
        lines_for_domestic_insurance, columns=INDEXES.values())
    df_for_abroad_insurance = pd.DataFrame(
        lines_for_abroad_insurance, columns=INDEXES.values())
    lines_for_recognized_sales = [recognized_sales.to_excel_line()
                                  for recognized_sales in deadline_info_of_period.all_recognized_sales]
    lines_for_recognized_sales.reverse()
    df_for_recognized_sales = pd.DataFrame(lines_for_recognized_sales, columns=[
        "월", "입고", "출고", "차량번호", "요청부서", "공임", "부품", "수리금액", "비고", "공장매출"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_for_general.to_excel(writer, index=False, sheet_name='일반')
        df_for_rent.to_excel(writer, index=False, sheet_name='렌트')
        df_for_domestic_insurance.to_excel(
            writer, index=False, sheet_name='국내보험')
        df_for_abroad_insurance.to_excel(
            writer, index=False, sheet_name='수입보험')
        df_for_recognized_sales.to_excel(
            writer, index=False, sheet_name='인정매출')
    output.seek(0)
    response = FileResponse(
        output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{datetime.now()}.xlsx'
    return response
