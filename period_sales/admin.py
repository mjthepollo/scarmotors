from django.contrib import admin

from period_sales.models import MonthlySales

PAID_SALES_LIST_DISPLAY = [
    "__str__",
    "paid_insurance_sales",
    "paid_general_expense",
    "paid_general_pando",
    "paid_general_rent",
    "paid_rent_pando",
    "not_paid_insurance_sales",
    "not_paid_general_expense",
    "not_paid_general_pando",
    "not_paid_general_rent",
    "not_paid_rent_pando",
    "wage_turnover",
    "component_turnover",
    "charge_amount",
    "deposit_amount",
    "net_payment_sales"
]


# @admin.register(MonthlySales)
class MonthlySalesAdmin(admin.ModelAdmin):
    list_display = PAID_SALES_LIST_DISPLAY
