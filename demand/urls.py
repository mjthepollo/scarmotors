from django.urls import path

from demand import views

app_name = "demand"

urlpatterns = [
    path("cooperator/", views.cooperator, name="cooperator"),
    path("manage_insurance_agent/", views.manage_insurance_agent,
         name="manage_insurance_agent"),
]
