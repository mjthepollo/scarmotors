from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from demand.key_model_forms import ChargeForm, DepositForm, PaymentForm
from demand.key_models import Charge, Deposit, Payment
from demand.sales_model_forms import (FirstCenterRegisterForm,
                                      RealDayCameOutForm, SpecialRegisterForm)
from demand.sales_models import Order, Register


@login_required
def car_number_modal(request):
    car_number = request.GET.get("car_number", None)
    registers = Register.objects.filter(car_number=car_number)
    return TemplateResponse(
        request, "demand/modals/car_number_modal.html",
        context={'registers': registers})


@login_required
def came_out_modal(request, pk):
    order = Order.objects.get(pk=pk)
    register = order.register
    # prefix is need because of JS
    payment_prefix = "payment-0"
    if request.method == "GET":
        real_day_came_out_form = RealDayCameOutForm(instance=register)
        special_register_form = SpecialRegisterForm(instance=register)
        payment_form = PaymentForm(
            instance=order.payment, prefix=payment_prefix)
        return TemplateResponse(
            request, "demand/modals/came_out_modal.html",
            context={"order": order,
                     "real_day_came_out_form": real_day_came_out_form,
                     "special_register_form": special_register_form,
                     "payment_form": payment_form})
    else:
        real_day_came_out_form = RealDayCameOutForm(
            request.POST, instance=register)
        special_register_form = SpecialRegisterForm(
            request.POST, instance=register)
        real_day_came_out_form.save()
        special_register_form.save()
        payment_form = PaymentForm(
            request.POST, instance=order.payment, prefix=payment_prefix)
        if payment_form.is_valid():
            payment = payment_form.save()
            if payment.is_default():
                order.payment = None
                payment.delete()
            else:
                order.payment = payment
            order.save()
        else:
            return JsonResponse({"error_message": "Payment Formset is not valid"})
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)


@login_required
def charge_modal(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "GET":
        first_center_register_form = FirstCenterRegisterForm(
            instance=order.register)
        charge_form = ChargeForm(instance=order.charge, order=order)
        return TemplateResponse(request, "demand/modals/charge_modal.html",
                                context={"order": order,
                                         "first_center_register_form": first_center_register_form,
                                         "charge_form": charge_form})
    else:
        first_center_register_form = FirstCenterRegisterForm(
            request.POST, instance=order.register)
        first_center_register_form.save()
        charge_form = ChargeForm(
            request.POST, instance=order.charge, order=order)
        if charge_form.is_valid():
            charge = charge_form.save()
            order.charge = charge
            order.save()
        else:
            return JsonResponse({"error_message": "Charge Form is not valid"})
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def deposit_modal(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "GET":
        deposit_form = DepositForm(instance=order.deposit)
        return TemplateResponse(request, "demand/modals/deposit_modal.html",
                                context={"order": order, "deposit_form": deposit_form})
    else:
        deposit_form = DepositForm(request.POST, instance=order.deposit)
        if deposit_form.is_valid():
            deposit = deposit_form.save()
            order.deposit = deposit
            order.save()
        else:
            return JsonResponse({"error_message": "Deposit Form is not valid"})
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def delete_payment(request, pk):
    payment = Payment.objects.get(pk=pk)
    order = payment.order
    payment.delete()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def delete_charge(request, pk):
    charge = Charge.objects.get(pk=pk)
    order = charge.order
    charge.delete()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def delete_deposit(request, pk):
    deposit = Deposit.objects.get(pk=pk)
    order = deposit.order
    deposit.delete()
    previous_url = request.META.get('HTTP_REFERER', None)
    if previous_url:
        return redirect(previous_url)
    else:
        return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
