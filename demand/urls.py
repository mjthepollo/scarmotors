from demand.modal_urls import modal_urlpatterns
from demand.views_urls import views_urlpatterns

app_name = "demand"


urlpatterns = modal_urlpatterns + views_urlpatterns
