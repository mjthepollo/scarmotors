
from django.urls import path

from demand import modal_views

modal_urlpatterns = [
    path("car_number_modal",
         modal_views.car_number_modal, name="car_number_modal"),
    path("came_out_modal/<int:pk>/",
         modal_views.came_out_modal, name="came_out_modal"),
    path("charge_modal/<int:pk>/",
         modal_views.charge_modal, name="charge_modal"),
    path("deposit_modal/<int:pk>/",
         modal_views.deposit_modal, name="deposit_modal"),
    path("delete_payment/<int:pk>/",
         modal_views.delete_payment, name="delete_payment"),
    path("delete_charge/<int:pk>/",
         modal_views.delete_charge, name="delete_charge"),
    path("delete_deposit/<int:pk>/",
         modal_views.delete_deposit, name="delete_deposit"),
    path("extra_sales_came_out_modal/<int:pk>/",
         modal_views.extra_sales_came_out_modal, name="extra_sales_came_out_modal"),
    path("extra_sales_charge_modal/<int:pk>/",
         modal_views.extra_sales_charge_modal, name="extra_sales_charge_modal"),
    path("extra_sales_delete_payment/<int:pk>/",
         modal_views.extra_sales_delete_payment, name="extra_sales_delete_payment"),
    path("extra_sales_delete_charge/<int:pk>/",
         modal_views.extra_sales_delete_charge, name="extra_sales_delete_charge"),
]
