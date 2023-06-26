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
from demand.sales_models import ExtraSales, Order, Register

temp_lines = [['0123', None, '1-1', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), datetime(2023, 1, 13, 0, 0), 11.0, '60저0130', '320D', '수입', None, 1.0, 1.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881890', 0.4, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 248740.80000000002, '무상7889', 392000.0, None, None, '카드', '우리', pd.Timestamp('2023-01-13 00:00:00'), 0.0, None, None, None, None, 0.0, None, 392000.0, 35636.36363636365, 356363.63636363635, None, "TEST", '완료', None, None, 1.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0, 356363.63636363635, 0.0],
              ['0123', None, None, pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-01-09 00:00:00'), None, 7.0, '60저0130', '320D', '수입', None, None, 0.0, '이성도(타)', '김석종/구본준', 1031370900, '보험', 'DB', '자차', '22-7881806', 0.6, 1.0, 230123.0, 565320.0, None, 565320.0, 56532.0, 373111.2, None,
               None, None, None, None, None, None, 373111.2, 1.0, 230119.0, 347821.0, 0.9322180626043924, 0.0, 0.06778193739560756, 347821.0, 31620.09090909094, 316200.90909090906, None, None, '완료', None, None, 1.0, 316200.90909090906, 0.0, 316200.90909090906, 0.0, 316200.90909090906, 0.0],
              ['0106', None, '1-21', pd.Timestamp('2023-01-03 00:00:00'), pd.Timestamp('2023-01-05 00:00:00'), datetime(2023, 1, 6, 0, 0), 3.0, '13버6789', '투싼', '국산', None, 2.0, 2.0, '이소정(직원)', '구본준담당', 1034361547, '보험', 'DB', '대물', '22-7868188', 1.0, 1.0, 230106.0, 539919.0, 28262.0, 568181.0, 56818.100000000006,
               624999.1000000001, '에스렌트', None, None, None, None, None, None, 624999.1000000001, 1.0, 230106.0, 620076.0, 0.9921230286571611, 0.0, 0.007876971342838934, 620076.0, 56370.54545454553, 563705.4545454545, None, None, '완료', None, None, 1.0, 563705.4545454545, 0.0, 563705.4545454545, 0.0, 535443.4545454545, 28262.0],
              [None, None, '1-79', pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 19, 0, 0), 7.0, '241마5742', 'QM6', '국산', 1.0, 2.0, 3.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', 'DB', '자차', '23-00330599', None, None, None, None, None, 0.0, 0.0,
               0.0, '반디', 500000.0, None, 300000.0, '은행', '하나', pd.Timestamp('2023-01-19 00:00:00'), 0.0, None, None, None, None, 0.0, None, 200000.0, 18181.818181818206, 181818.1818181818, None, None, '완료', None, None, 1.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0, 181818.1818181818, 0.0],
              [None, None, None, pd.Timestamp('2023-01-12 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), None, 8.0, '241마5742', 'QM6', '국산', None, None, 0.0, '이성도(타)', '김윤희/구본준', 1048104691, '보험', '삼성', '대물', '230112-1425',
               None, None, None, None, None, 0.0, 0.0, 0.0, None, None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, None, '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              ['0131', None, '1-100', pd.Timestamp('2023-01-17 00:00:00'), pd.Timestamp('2023-01-27 00:00:00'), datetime(2023, 1, 31, 0, 0), 14.0, '60구2264', '렉서스LS460', '수입', 3.0, None, 3.0, '장영수', '윤석영', '010-9403-4783', '보험', '하나손해', '대물', '1-5008', 1.0, 1.0, 230131.0, 2323181.818181818, None,
               2323181.818181818, 232318.1818181818, 2555500.0, '무상4760', None, None, None, None, None, None, 2555500.0, 2.0, 230202.0, 2420000.0, 0.9469771081980043, 0.0, 0.05302289180199571, 2420000.0, 220000.0, 2200000.0, None, None, '완료', None, None, 1.0, 2200000.0, 0.0, 2200000.0, 0.0, 2200000.0, 0.0],
              ['0131', None, None, pd.Timestamp('2023-01-17 00:00:00'), pd.Timestamp('2023-01-27 00:00:00'), datetime(2023, 1, 31, 0, 0), 14.0, '60구2264', '렉서스LS460', '수입', None, None, 0.0, '장영수', '윤석영', '010-9403-4783', '일반경정비', '일반경정비', None, None, 1.0, 1.0, 230131.0, 163636.36363636362, None, 163636.36363636362,
               16363.636363636362, 180000.0, None, 180000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-31 00:00:00'), 0.0, None, None, None, None, 0.0, None, 180000.0, 16363.636363636382, 163636.36363636362, None, None, '완료', '일반경정비', None, 1.0, 163636.36363636362, 0.0, 163636.36363636362, 0.0, 163636.36363636362, 0.0],
              ['0120', None, '1-101', pd.Timestamp('2023-01-20 00:00:00'), pd.Timestamp('2023-01-20 00:00:00'), datetime(2023, 1, 20, 0, 0), 0.0, '193허2950', 'K5', '국산', None, None, 0.0, '고객', None, None, '일반경정비', '일반경정비', None, '타이어펑크수리', 1.0, 1.0, 230120.0, 9090.90909090909, None, 9090.90909090909,
               909.090909090909, 10000.0, None, 10000.0, None, None, '카드', '삼성', pd.Timestamp('2023-01-20 00:00:00'), 0.0, None, None, None, None, 0.0, None, 10000.0, 909.0909090909099, 9090.90909090909, None, None, '완료', '일반경정비', None, 1.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0, 9090.90909090909, 0.0],
              [331.0, None, None, pd.Timestamp('2023-03-31 00:00:00'), None, datetime(2023, 3, 31, 0, 0), 0.0, 'xxxx', '세차', None, None, None, 0.0, None, '세차실장', None, '일반경정비', '일반경정비', None, '세차', 1.0, 3.0, 230331.0, None, 50000.0, 50000.0, 5000.0, 55000.00000000001,
               None, 55000.0, None, None, '카드', '신한', pd.Timestamp('2023-03-31 00:00:00'), 0.0, None, None, None, None, 0, None, 55000.0, 5000.000000000007, 49999.99999999999, None, None, '완료', '일반경정비', None, 1.0, 49999.99999999999, 0.0, 49999.99999999999, 0.0, 0.0, 50000.0],
              [412.0, None, None, pd.Timestamp('2023-04-12 00:00:00'), pd.Timestamp('2023-04-12 00:00:00'), datetime(2023, 4, 12, 0, 0), 0.0, '307누8223', 'IG', '국산', None, None, 0.0, None, '세차실장', '010-5407-9545', '일반경정비', '일반경정비', None, '부분 유리막코팅', 1.0, 4.0, 230412.0, None,
               90000.0, 90000.0, 9000.0, 99000.00000000001, None, 99000.0, None, None, '카드', '롯데', pd.Timestamp('2023-04-12 00:00:00'), 0.0, None, None, None, None, 0, None, 99000.0, 9000.0, 90000.0, None, None, '완료', '일반경정비', None, 1.0, 90000.0, 0.0, 90000.0, 0.0, 0.0, 90000.0],
              [None, None, '1-80', pd.Timestamp('2023-01-02 00:00:00'), pd.Timestamp('2023-02-03 00:00:00'), '폐차', None, '21하3555', 'SM7', '국산', 4.0, 4.0, 8.0, '이성도', '김용연/백준호', 1072230486, '보험', '현대', '대물', '12-109185', 1.0,
               None, None, None, None, 0.0, 0.0, 0.0, '스타렌트', None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, '폐차처리', '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [None, None, '1-103', pd.Timestamp('2023-01-21 00:00:00'), pd.Timestamp('2023-01-26 00:00:00'), '미수리출고', None, '48노5927', '클리오', '국산', 1.0, 1.0, 2.0, '김일한', '김장현담당', 1031717367, '보험', '현대', '대물', '23-01063895', None,
               None, None, None, None, 0.0, 0.0, 0.0, '롯데렌탈 용인영업소', None, None, None, None, None, None, 0.0, None, None, None, None, 0.0, None, 0.0, 0.0, 0.0, None, None, '미청구', None, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
              ]


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
    if request.method == "GET":
        order_formset = order_form_factory(
            queryset=register.orders.all())
        return render(request, "demand/edit_register.html", context={
            "register_form": register_form,
            "order_formset": order_formset,
        })
    else:
        register_form = EditRegisterForm(request.POST, instance=register)
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
def order_came_out(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.real_day_came_out = date.today()
    order.save()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


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
def extra_sales(request):
    return render(request, "demand/extra_sales.html", context={"extra_sales_queryset": ExtraSales.objects.all()})

# 차량번호 검색
# RO 번호 검색
#
