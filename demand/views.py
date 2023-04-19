# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def cooperator(request):
    pass


@login_required
def manage_insurance_agent(request):
    pass
