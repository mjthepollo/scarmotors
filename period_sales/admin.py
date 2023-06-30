from django.contrib import admin

from period_sales.models import (MonthlySales, NotPaidTurnoverSalesInfo,
                                 PaidTurnoverSalesInfo, StatisticSales)


@admin.register(PaidTurnoverSalesInfo)
class PaidTurnoverSalesInfoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "insurance_sales",
                    "general_expense", "general_pando", "general_rent", "rent_pando"]


@admin.register(NotPaidTurnoverSalesInfo)
class NotPaidTurnoverSalesInfoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "insurance_sales",
                    "general_expense", "general_pando", "general_rent", "rent_pando"]


@admin.register(MonthlySales)
class MonthlySalesAdmin(admin.ModelAdmin):
    list_display = ["__str__", "paid_turnover_info", "not_paid_turnover_info",
                    "wage_turnover", "component_turnover", "charge_amount",
                    "deposit_amount", "net_payment_amount"]


@admin.register(StatisticSales)
class StatisticSalesAdmin(admin.ModelAdmin):
    list_display = ["__str__", "paid_turnover_info", "not_paid_turnover_info",
                    "wage_turnover", "component_turnover", "charge_amount",
                    "deposit_amount", "net_payment_amount"]
