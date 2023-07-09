from datetime import date

from django.conf import settings
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from core.utility import get_current_half, get_start_and_end_dates_of_half
from period_sales.models import MonthlySales, StatisticSales
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
    year = request.GET.get("year", date.today().year)
    half = request.GET.get("half", get_current_half())
    start_date, end_date = get_start_and_end_dates_of_half(year, half)
    monthly_sales = MonthlySales.objects.all(
        start_date__gte=start_date, end_date__lte=end_date)
    return render(request, "home.html", {"monthly_sales": monthly_sales})


@login_required
def update_period_sales(request):
    year = request.GET.get("year", date.today().year)
    half = request.GET.get("half", get_current_half())
    start_date, end_date = get_start_and_end_dates_of_half(year, half)
    monthly_sales = MonthlySales.objects.all(
        start_date__gte=start_date, end_date__lte=end_date)
    for monthly_sale in monthly_sales:
        monthly_sale.update()
    return redirect(reverse("home")+"?year="+year+"&half="+half)


@login_required
def download_db(request):
    db_path = settings.DATABASES['default']['NAME']
    response = FileResponse(open(db_path, 'rb'))
    return response
