"""Маршруты верхнего уровня."""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("dishes/", include("dishes.urls")),
    path("events/", include("events.urls")),
]
