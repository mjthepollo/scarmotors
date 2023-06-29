from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from demand.forms import ChargeForm, DepositForm, PaymentForm
from demand.sales_models import Order, Register


@login_required
def came_out_modal(request, pk):
    if request.method == "GET":
        register = Register.objects.get(pk=pk)
        return TemplateResponse(request, "demand/modals/came_out_modal.html", context={"register": register})
    else:
        register = get_object_or_404(Register, pk=pk)
        register.wasted = True if request.POST.get(
            "wasted", False) == "on" else False
        register.unrepaired = True if request.POST.get(
            "unrepaired", False) == 'on' else False
        register.real_day_came_out = request.POST.get(
            "real_day_came_out", None)
        register.save()
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+register.RO_number)


@login_required
def charge_modal(request, pk):
    order = Order.objects.get(pk=pk)
    charge_form = ChargeForm(instance=order.charge)
    if request.method == "GET":
        return TemplateResponse(request, "demand/modals/charge_modal.html",
                                context={"order": order, "charge_form": charge_form})
    else:
        pass
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)


@login_required
def deposit_modal(request, pk):
    order = Order.objects.get(pk=pk)
    deposit_form = DepositForm(instance=order.deposit)
    if request.method == "GET":
        return TemplateResponse(request, "demand/modals/deposit_modal.html",
                                context={"order": order, "deposit_form": deposit_form})
    else:
        pass
        previous_url = request.META.get('HTTP_REFERER', None)
        if previous_url:
            return redirect(previous_url)
        else:
            return redirect(reverse("demand:search_registers")+"?RO_number="+order.register.RO_number)
