import os
from datetime import date
from math import ceil

from django.conf import settings
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from core.utility import get_current_half, get_start_and_end_dates_of_half
from demand.excel_load import (
    get_effective_data_frame, get_line_numbers_for_registers,
    get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers)
from period_sales.forms import PeriodFilter
from period_sales.models import (MonthlySales, StatisticSales,
                                 get_net_information)
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
    period_filter_form = PeriodFilter(request.GET)
    if period_filter_form.is_valid():
        year = int(period_filter_form.cleaned_data.get("year"))
        half = period_filter_form.cleaned_data.get("half")
    else:
        year = date.today().year
        half = get_current_half()
        period_filter_form = PeriodFilter({"year": year, "half": half})
    start_date, end_date = get_start_and_end_dates_of_half(year, half)
    monthly_sales = MonthlySales.create_or_get_all_monthly_sales(
        year, start_date.month, end_date.month)
    chunks = []
    for i in range(ceil(monthly_sales.count()/3)):
        chunks.append(monthly_sales[i*3:i*3+3])
    context = {"period_filter_form": period_filter_form,
               "monthly_sales": monthly_sales,
               "chunks": chunks}
    context.update(get_net_information(monthly_sales))
    return render(request, "home.html", context=context)


@login_required
def update_period_sales(request):
    year = int(request.GET.get("year", date.today().year))
    half = request.GET.get("half", get_current_half())
    start_date, end_date = get_start_and_end_dates_of_half(year, half)
    monthly_sales = MonthlySales.objects.filter(
        start_date__gte=start_date, end_date__lte=end_date)
    for monthly_sale in monthly_sales:
        monthly_sale.update()
    return redirect(reverse("home")+"?year="+str(year)+"&half="+half)


@login_required
def download_db(request):
    db_path = settings.DATABASES['default']['NAME']
    response = FileResponse(open(db_path, 'rb'))
    return response


@login_required
def set_db(request):
    if request.method == "GET":
        return render(request, "set_db.html")
    else:
        DB = request.FILES.get("DB")
        db_file = DB.read()
        db_path = settings.DATABASES['default']['NAME']
        with open(db_path, "wb") as f:
            f.write(db_file)

        return redirect(reverse("home"))


@login_required
def differences(request):
    if request.method == "GET":
        return render(request, "differences_get.html")
    else:
        EXCEL = request.FILES.get("EXCEL")
        excel_file = EXCEL.read()
        sheet_name = request.POST.get("sheet_name")
        sheet_name = sheet_name if sheet_name else "23년 본사 하반기"
        excel_save_path = os.path.join(
            settings.ROOT_DIR, "src/difference.xlsx")
        with open(excel_save_path, "wb") as f:
            f.write(excel_file)
        df = get_effective_data_frame(excel_save_path, sheet_name)
        line_numbers_for_registers = get_line_numbers_for_registers(df)
        list_of_check_list = get_list_of_check_list_by_comparing_registers_using_line_numbers_for_registers(
            df, line_numbers_for_registers)
        return render(request, "differences_post.html",
                      context={"list_of_check_list": list_of_check_list, "sheet_name": sheet_name})
