"""Представления списка событий и отдельного события."""
from html import escape

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from menu_planning.calculations import get_total_ingredients
from menu_planning.events import find_event_by_id
from menu_planning.storage import (
    load_dishes,
    load_events,
    load_ingredients,
    load_users,
)


def _load_events():
    data_dir = settings.BASE_DIR / "data"
    ingredients = load_ingredients(str(data_dir / "ingredients.json"))
    dishes = load_dishes(str(data_dir / "dishes.json"), ingredients)
    users = load_users(str(data_dir / "users.json"))
    return load_events(str(data_dir / "events.json"), dishes, users)


def events(request):
    """Показать события из JSON-хранилища."""
    items = ""
    for event in _load_events():
        items += f"""
<a href="/events/{event.event_id}/"
   class="list-group-item list-group-item-action">
  <strong>{escape(event.name)}</strong>
  <span class="float-end">{escape(event.event_date)}</span>
  <div class="small text-body-secondary">Гостей: {event.guests}</div>
</a>
"""
    content = f"""
<h1>События</h1>
<p class="text-body-secondary">Данные загружены из data/events.json.</p>
<div class="list-group">{items}</div>
"""
    return HttpResponse(page("События", content))


def event_detail(request, event_id: int):
    """Показать событие с меню или вернуть страницу 404."""
    event = find_event_by_id(_load_events(), event_id)
    if event is None:
        content = """
<h1 class="text-danger">Событие не найдено</h1>
<a href="/events/" class="btn btn-outline-secondary">
  Вернуться к списку событий
</a>
"""
        return HttpResponse(page("Событие не найдено", content), status=404)

    menu_items = ""
    for dish in event.menu:
        totals = get_total_ingredients(dish, event.guests)
        ingredients = ", ".join(
            f"{escape(name)} — {grams} г" for name, grams in totals.items()
        )
        menu_items += f"""
<li class="list-group-item">
  <a href="/dishes/{dish.dish_id}/">{escape(dish.name)}</a>
  <div class="small text-body-secondary">{ingredients}</div>
</li>
"""
    user_name = (
        escape(event.user.name) if event.user is not None else "не указан"
    )
    content = f"""
<div class="card shadow-sm">
  <div class="card-body">
    <h1 class="card-title h3">{escape(event.name)}</h1>
    <p><strong>ID:</strong> {event.event_id}</p>
    <p><strong>Дата:</strong> {escape(event.event_date)}</p>
    <p><strong>Количество гостей:</strong> {event.guests}</p>
    <p><strong>Пользователь:</strong> {user_name}</p>
    <h2 class="h5">Меню и количество ингредиентов</h2>
    <ul class="list-group mb-4">{menu_items}</ul>
    <a href="/events/" class="btn btn-outline-secondary">
      Вернуться к списку событий
    </a>
  </div>
</div>
"""
    return HttpResponse(page(escape(event.name), content))
