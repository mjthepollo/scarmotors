from django.contrib import admin

from demand.key_models import (Charge, ChargedCompany, Deposit, InsuranceAgent,
                               Payment, RequestDepartment, Supporter)
from demand.sales_models import ExtraSales, Order, RecognizedSales, Register


@admin.register(ExtraSales)
class ExtraSalesAdmin(admin.ModelAdmin):
    list_display = ["car_number", "sort", "day_came_in", "real_day_came_out", "car_model",
                    "phone_number"]
    search_fields = ["sort", "car_number", "note"]


@admin.register(RecognizedSales)
class RecongnizedSalesAdmin(admin.ModelAdmin):
    list_display = ["day_came_in", "real_day_came_out", "car_number",
                    "wage_amount", "component_amount", "request_department"]


@admin.register(RequestDepartment)
class RequestDepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]

    actions = ["make_active", "make_inactive",]

    @admin.action(description=f"선택한 {RequestDepartment._meta.verbose_name_plural}을 비활성화합니다.")
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)

    @admin.action(description=f"선택한 {RequestDepartment._meta.verbose_name_plural}을 활성화합니다.")
    def make_active(modeladmin, request, queryset):
        queryset.update(active=True)


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):

    admin
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]
    actions = ["make_active", "make_inactive",]

    @admin.action(description=f"선택한 {Supporter._meta.verbose_name_plural}을 비활성화합니다.")
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)

    @admin.action(description=f"선택한 {Supporter._meta.verbose_name_plural}을 활성화합니다.")
    def make_active(modeladmin, request, queryset):
        queryset.update(active=True)


@admin.register(ChargedCompany)
class ChargedCompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]

    actions = ["make_active", "make_inactive",]

    @admin.action(description=f"선택한 {ChargedCompany._meta.verbose_name_plural}을 비활성화합니다.")
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)

    @admin.action(description=f"선택한 {ChargedCompany._meta.verbose_name_plural}을 활성화합니다.")
    def make_active(modeladmin, request, queryset):
        queryset.update(active=True)


@admin.register(InsuranceAgent)
class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]

    actions = ["make_active", "make_inactive",]

    @admin.action(description=f"선택한 {InsuranceAgent._meta.verbose_name_plural}을 비활성화합니다.")
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)

    @admin.action(description=f"선택한 {InsuranceAgent._meta.verbose_name_plural}을 활성화합니다.")
    def make_active(modeladmin, request, queryset):
        queryset.update(active=True)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ["RO_number", "car_number", "insurance_agent"]
    list_filter = ["day_came_in", "expected_day_came_out",
                   "real_day_came_out", "phone_number"]
    search_fields = ["RO_number", "insurance_agent"]


# @admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["__str__", "indemnity_amount",
                    "discount_amount", "payment_type", "payment_info"]
    list_filter = ["payment_type"]


# @admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "charge_date",
                    "wage_amount", "component_amount"]
    search_fields = ["charge_date",]


# @admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ["__str__", "deposit_date", "deposit_amount"]
    search_fields = ["deposit_date"]


@admin.register(Order)
class IncentiveAdmin(admin.ModelAdmin):
    fieldsets = (
        ("수정가능한 정보", {
            "fields": ("incentive_paid", "incentive_paid_date",)
        }
        ),
    )

    list_display = ["register_RO_number", "register_car_number",
                    "incentive_paid", "incentive_paid_date"]
    search_fields = ["register__RO_number", "register__car_number"]

    def register_RO_number(self, obj):
        return obj.register.RO_number if obj.register else None

    def register_car_number(self, obj):
        return obj.register.car_number if obj.register else None
