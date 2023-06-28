from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from demand.sales_models import Register


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
