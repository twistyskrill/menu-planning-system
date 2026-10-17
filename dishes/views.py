"""Представления списка блюд и отдельного блюда."""
from django.conf import settings
from django.shortcuts import render

from menu_planning.dishes import find_dish_by_id
from menu_planning.storage import load_dishes, load_ingredients


def _load_dishes():
    ingredients_path = settings.BASE_DIR / "data/ingredients.json"
    ingredients = load_ingredients(str(ingredients_path))
    return load_dishes(
        str(settings.BASE_DIR / "data/dishes.json"),
        ingredients,
    )


def dishes(request):
    """Передать блюда из JSON в шаблон списка."""
    return render(request, "dishes/dish_list.html", {"dishes": _load_dishes()})


def dish_detail(request, dish_id: int):
    """Передать блюдо в шаблон, сохраняя HTTP 404 при отсутствии."""
    dish = find_dish_by_id(_load_dishes(), dish_id)
    return render(
        request, "dishes/dish_detail.html", {"dish": dish},
        status=404 if dish is None else 200,
    )
