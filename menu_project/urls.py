"""Маршруты верхнего уровня."""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path


handler404 = "homepage.views.page_not_found"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("dishes/", include("dishes.urls")),
    path("events/", include("events.urls")),
]

if settings.ENABLE_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
