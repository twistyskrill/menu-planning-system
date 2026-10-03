"""Представления списка блюд и отдельного блюда."""
from html import escape

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
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
    """Показать блюда из JSON-хранилища."""
    items = ""
    for dish in _load_dishes():
        name = escape(dish.name)
        dish_type = escape(dish.dish_type)
        items += f"""
<a href="/dishes/{dish.dish_id}/"
   class="list-group-item list-group-item-action">
  <strong>{name}</strong>
  <span class="badge text-bg-secondary float-end">{dish_type}</span>
</a>
"""
    content = f"""
<h1>Блюда</h1>
<p class="text-body-secondary">Данные загружены из data/dishes.json.</p>
<div class="list-group">{items}</div>
"""
    return HttpResponse(page("Блюда", content))


def dish_detail(request, dish_id: int):
    """Показать блюдо или вернуть страницу 404."""
    dish = find_dish_by_id(_load_dishes(), dish_id)
    if dish is None:
        content = """
<h1 class="text-danger">Блюдо не найдено</h1>
<a href="/dishes/" class="btn btn-outline-secondary">
  Вернуться к списку блюд
</a>
"""
        return HttpResponse(page("Блюдо не найдено", content), status=404)

    ingredient_items = "".join(
        (
            '<li class="list-group-item d-flex justify-content-between">'
            f"<span>{escape(ingredient.name)}</span>"
            f"<span>{ingredient.grams_for_guest} г на гостя</span>"
            "</li>"
        )
        for ingredient in dish.ingredients
    )
    content = f"""
<div class="card shadow-sm">
  <div class="card-body">
    <h1 class="card-title h3">{escape(dish.name)}</h1>
    <p><strong>ID:</strong> {dish.dish_id}</p>
    <p><strong>Тип:</strong> {escape(dish.dish_type)}</p>
    <h2 class="h5">Ингредиенты</h2>
    <ul class="list-group mb-4">{ingredient_items}</ul>
    <a href="/dishes/" class="btn btn-outline-secondary">
      Вернуться к списку блюд
    </a>
  </div>
</div>
"""
    return HttpResponse(page(escape(dish.name), content))
