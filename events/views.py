"""Представления событий и расчёты для контекста шаблонов."""
from datetime import date

from django.conf import settings
from django.shortcuts import render

from menu_planning.calculations import get_total_ingredients
from menu_planning.events import find_event_by_id
from menu_planning.storage import (
    load_dishes, load_events, load_ingredients, load_users,
)


def _load_events():
    data_dir = settings.BASE_DIR / "data"
    ingredients = load_ingredients(str(data_dir / "ingredients.json"))
    dishes = load_dishes(str(data_dir / "dishes.json"), ingredients)
    users = load_users(str(data_dir / "users.json"))
    return load_events(str(data_dir / "events.json"), dishes, users)


def events(request):
    """Передать события и даты для форматирования в шаблон."""
    events_list = _load_events()
    rows = [
        {"event": event, "date": date.fromisoformat(event.event_date)}
        for event in events_list
    ]
    return render(request, "events/event_list.html", {"events": rows})


def event_detail(request, event_id: int):
    """Подготовить объект и расчёты без формирования HTML."""
    event = find_event_by_id(_load_events(), event_id)
    context = {"event": event}
    if event is not None:
        context["event_date"] = date.fromisoformat(event.event_date)
        context["menu"] = [
            {"dish": dish,
             "ingredients": get_total_ingredients(dish, event.guests)}
            for dish in event.menu
        ]
    return render(
        request, "events/event_detail.html", context,
        status=404 if event is None else 200,
    )
