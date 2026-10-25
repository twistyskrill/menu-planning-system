"""Представления списка блюд и отдельного блюда."""
from django.shortcuts import render

from db.repository import fetch, load_dishes
from menu_planning.dishes import find_dish_by_id


def _load_dishes():
    return load_dishes()


def dishes(request):
    """Вывести каталог или результаты параметризованного поиска."""
    term = request.GET.get("q", "").strip()
    dish_type = request.GET.get("type", "").strip()
    params = (term, term, dish_type, dish_type)
    items = (load_dishes(fetch("dish_search", params))
             if term or dish_type else _load_dishes())
    return render(request, "dishes/dish_list.html", {
        "dishes": items, "q": term, "selected_type": dish_type,
        "categories": fetch("categories"),
    })


def dish_detail(request, dish_id: int):
    """Передать блюдо в шаблон, сохраняя HTTP 404 при отсутствии."""
    dish = find_dish_by_id(_load_dishes(), dish_id)
    return render(
        request, "dishes/dish_detail.html", {"dish": dish},
        status=404 if dish is None else 200,
    )


def available(request):
    """Подобрать блюда, не использованные в меню на выбранную дату."""
    from datetime import date

    value = request.GET.get("date", "")
    error = ""
    items = []
    try:
        page = max(1, int(request.GET.get("page", "1")))
        if page > 1000000:
            raise ValueError
        if value:
            value = date.fromisoformat(value).isoformat()
            rows = fetch("available", (value, 11, (page - 1) * 10))
            items = load_dishes(rows[:10])
        else:
            rows = []
    except ValueError:
        page, rows = 1, []
        error = "Укажите корректную дату и номер страницы."
    return render(request, "dishes/available.html", {
        "dishes": items, "selected_date": value, "error": error,
        "searched": bool(value) and not error, "page": page,
        "previous": page - 1, "next": page + 1, "has_next": len(rows) > 10,
    }, status=400 if error else 200)
