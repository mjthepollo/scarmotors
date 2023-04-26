from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.static import serve

from core import core_views

urlpatterns = [
    path("", core_views.home, name="home"),
    path("new_register/", core_views.new_register, name="new_register"),
    path("edit_register/", core_views.edit_register, name="edit_register"),
    path("finish_register/", core_views.finish_register, name="finish_register"),
    path("search_registers/", core_views.search_registers, name="search_registers"),
    path("demand/", include("demand.urls", namespace="demand")),
    # Django Admin, use {% url 'admin:index' %}
    path("login/", core_views.login, name="login"),
    path("logout/", core_views.logout, name="logout"),
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + [
    re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
            }),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
