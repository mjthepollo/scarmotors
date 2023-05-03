from django.urls import path

from demand import views

app_name = "demand"

urlpatterns = [
    path("new_register/", views.new_register, name="new_register"),
    path("edit_register/", views.edit_register, name="edit_register"),
    path("edit_order/<int:pk>/", views.edit_order, name="edit_order"),
    path("search_registers/", views.search_registers, name="search_registers"),
]
