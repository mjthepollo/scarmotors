
from django.urls import path

from demand import views

app_name = "demand"

views_urlpatterns = [
    path("new_register/", views.new_register, name="new_register"),
    path("edit_register/<int:pk>/", views.edit_register, name="edit_register"),
    path("edit_order/<int:pk>/", views.edit_order, name="edit_order"),
    path("search_registers/", views.search_registers, name="search_registers"),
    path("search_registers_table_view/", views.search_registers_table_view,
         name="search_registers_table_view"),
    path("registers_to_excel/", views.registers_to_excel,
         name="registers_to_excel"),
    path("search_orders/", views.search_orders, name="search_orders"),
    path("search_orders_table_view/", views.search_orders_table_view,
         name="search_orders_table_view"),
    path("order/charge/<int:pk>/", views.order_charge, name="order_charge"),
    path("order/deposit/<int:pk>/", views.order_deposit, name="order_deposit"),
    path("order/make_manually_complete/<int:pk>/",
         views.make_manually_complete, name="make_manually_complete"),
    path("order/cancel_manually_complete/<int:pk>/",
         views.cancel_manually_complete, name="cancel_manually_complete"),
    path("orders_to_excel/", views.orders_to_excel, name="orders_to_excel"),
    path("extra_sales/", views.extra_sales, name="extra_sales"),
]
