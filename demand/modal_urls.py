
from django.urls import path

from demand import modal_views

modal_urlpatterns = [
    path("came_out_modal/<int:pk>/",
         modal_views.came_out_modal, name="came_out_modal"),
]
