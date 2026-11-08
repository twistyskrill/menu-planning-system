from datetime import date

from django.core.paginator import Paginator
from django.db.models import Count, Value
from django.db.models.functions import StrIndex
from django.shortcuts import render

from dishes.models import Dish


DISH_SORTS = {"id": ("id",), "name": ("name", "id")}


def dishes(request):
    term = request.GET.get("q", "").strip()
    dish_type = request.GET.get("type", "").strip()
    ingredient = request.GET.get("ingredient", "").strip()
    sort = request.GET.get("sort", "id")
    items = Dish.objects.all()
    if dish_type:
        items = items.filter(dish_type=dish_type)
    if term:
        items = items.alias(match=StrIndex("name", Value(term))).filter(
            match__gt=0
        )
    items = items.annotate(
        ingredient_count=Count("ingredients", distinct=True)
    )
    if ingredient:
        items = items.filter(
            ingredients__name__icontains=ingredient
        ).distinct()
    categories = Dish.objects.values("dish_type").distinct().order_by(
        "dish_type"
    )
    return render(request, "dishes/dish_list.html", {
        "dishes": items.order_by(*DISH_SORTS.get(sort, DISH_SORTS["id"])),
        "q": term, "selected_type": dish_type, "ingredient": ingredient,
        "categories": categories, "sort": sort,
    })


def dish_detail(request, dish_id: int):
    dish = Dish.objects.filter(pk=dish_id).first()
    servings = (
        dish.servings.select_related("ingredient").order_by("ingredient_id")
        if dish else ()
    )
    return render(request, "dishes/dish_detail.html", {
        "dish": dish, "servings": servings,
    }, status=200 if dish else 404)


def available(request):
    value = request.GET.get("date", "")
    page_obj = None
    error = ""
    try:
        page = int(request.GET.get("page", "1"))
        if not 1 <= page <= 1000000:
            raise ValueError
        if value:
            value = date.fromisoformat(value).isoformat()
            items = Dish.objects.exclude(events__event_date=value).annotate(
                ingredient_count=Count("ingredients")
            ).order_by("id")
            page_obj = Paginator(items, 10).get_page(page)
    except ValueError:
        error = "Укажите корректную дату и номер страницы."
    return render(request, "dishes/available.html", {
        "dishes": page_obj, "selected_date": value,
        "error": error, "searched": page_obj is not None,
        "page_obj": page_obj,
    }, status=400 if error else 200)
