"""Представления событий и расчёты для контекста шаблонов."""
from datetime import date

from django.shortcuts import render

from db.repository import fetch, load_events
from menu_planning.calculations import get_total_ingredients
from menu_planning.events import find_event_by_id


def _load_events():
    return load_events()


def events(request):
    """Передать события и даты для форматирования в шаблон."""
    value = request.GET.get("date", "")
    minimum = request.GET.get("min_guests", "0")
    error = ""
    try:
        minimum = int(minimum or "0")
        if not 0 <= minimum <= 1000000:
            raise ValueError
        if value:
            value = date.fromisoformat(value).isoformat()
        params = (value, value, minimum)
        events_list = (load_events(fetch("event_search", params))
                       if value or minimum else _load_events())
    except ValueError:
        events_list = []
        error = "Укажите корректную дату и число гостей от 0 до 1000000."
    rows = [
        {"event": event, "date": date.fromisoformat(event.event_date)}
        for event in events_list
    ]
    return render(request, "events/event_list.html", {
        "events": rows, "selected_date": value, "min_guests": minimum,
        "error": error,
    }, status=400 if error else 200)


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


def statistics(request):
    """Показать итоги, категории и востребованность блюд из SQL."""
    return render(request, "events/statistics.html", {
        "dish_totals": fetch("dish_totals")[0],
        "event_totals": fetch("event_totals")[0],
        "categories": fetch("categories"),
        "popularity": fetch("popularity"),
        "frequent": fetch("frequent", (2,)),
    })
