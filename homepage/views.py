"""Представления главной страницы и общей ошибки 404."""
from django.shortcuts import render


def index(request):
    """Показать главную страницу проекта."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Показать страницу для неизвестного адреса."""
    return render(request, "404.html", status=404)
