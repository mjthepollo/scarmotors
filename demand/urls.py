from django.urls import path

from demand import views

app_name = "demand"

urlpatterns = [
    path("new_register/", views.new_register, name="new_register"),
    path("edit_register/<int:pk>/", views.edit_register, name="edit_register"),
    path("edit_order/<int:pk>/", views.edit_order, name="edit_order"),
    path("search_registers/", views.search_registers, name="search_registers"),
    path("registers_to_excel/", views.registers_to_excel,
         name="registers_to_excel"),
    path("search_orders/", views.search_orders, name="search_orders"),
    path("orders_to_excel/", views.orders_to_excel, name="orders_to_excel"),
    path("extra_sales/", views.extra_sales, name="extra_sales"),
]
