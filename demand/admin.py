from django.contrib import admin

from demand.models import (Charge, ChargedCompany, Deposit, Insurance,
                           InsuranceAgent, Order, Payment, Supporter)


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]


@admin.register(ChargedCompany)
class ChargedCompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]


@admin.register(InsuranceAgent)
class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["indemnity_amount",
                    "discount_amount", "payment_type", "payment_info"]
    list_filter = ["payment_type"]


@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ["charge_date", "repair_amount",
                    "component_amount", "indemnity_amount"]
    search_fields = ["charge_date",]


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["deposit_date", "deposit_amount"]
    search_fields = ["deposit_date"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["RO_number", "car_number", "insurance_agent"]
    list_filter = ["day_came_in", "expected_day_came_out",
                   "real_day_came_out", "phone_number"]
    search_fields = ["RO_number", "insurance_agent"]


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ["charged_company", "receipt_number", "order",
                    "charge_type", "receipt_number"]
    search_fields = ["order", "payment", "charge"]
