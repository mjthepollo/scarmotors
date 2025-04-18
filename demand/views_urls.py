
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
    path("search_etc_insurances_orders/", views.search_etc_insurances_orders,
         name="search_etc_insurances_orders"),
    path("search_orders_table_view/", views.search_orders_table_view,
         name="search_orders_table_view"),
    path("order/make_manually_complete/<int:pk>/",
         views.make_manually_complete, name="make_manually_complete"),
    path("order/cancel_manually_complete/<int:pk>/",
         views.cancel_manually_complete, name="cancel_manually_complete"),
    path("orders_to_excel/", views.orders_to_excel, name="orders_to_excel"),
    path("incentive/", views.incentive, name="incentive"),
    path("undo_incentive/<int:pk>/", views.undo_incentive, name="undo_incentive"),
    path("search_extra_sales/", views.search_extra_sales,
         name="search_extra_sales"),
    path("new_extra_sales/",
         views.new_extra_sales, name="new_extra_sales"),
    path("edit_extra_sales/<int:pk>/",
         views.edit_extra_sales, name="edit_extra_sales"),
    path("search_recognized_sales/", views.search_recognized_sales,
         name="search_recognized_sales"),
    path("recognized_sales_to_excel/", views.recognized_sales_to_excel,
         name="recognized_sales_to_excel"),
    path("new_recognized_sales/",
         views.new_recognized_sales, name="new_recognized_sales"),
    path("edit_recognized_sales/<int:pk>/",
         views.edit_recognized_sales, name="edit_recognized_sales"),
    path("deadline", views.deadline, name="deadline"),
    path("deadline_to_excel", views.deadline_to_excel, name="deadline_to_excel"),
]
