"""Представления главной страницы и общий HTML-каркас."""
from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Сформировать общую HTML-страницу с Bootstrap и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-md bg-dark" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="/">Праздничное меню</a>
      <div class="navbar-nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/dishes/">Блюда</a>
        <a class="nav-link" href="/events/">События</a>
      </div>
    </div>
  </nav>
  <main class="container py-5">{content}</main>
</body>
</html>"""


def index(request):
    """Показать главную страницу проекта."""
    content = """
<section class="p-5 bg-white rounded-3 shadow-sm">
  <h1 class="display-5">Система планирования праздничного меню</h1>
  <p class="lead">
    Планируйте события, просматривайте блюда и рассчитывайте ингредиенты
    для нужного количества гостей.
  </p>
  <a href="/dishes/" class="btn btn-primary me-2">Блюда</a>
  <a href="/events/" class="btn btn-success">События</a>
</section>
"""
    return HttpResponse(page("Планирование праздничного меню", content))
