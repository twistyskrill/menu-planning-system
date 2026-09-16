def get_portions(guests: int) -> int:
    """Рассчитать количество порций по числу гостей."""
    return guests


def get_ingredient_amount(portions: int, grams_for_guest: int) -> int:
    """Рассчитать количество ингредиента в граммах."""
    return portions * grams_for_guest


def get_dish_type(is_main_dish: bool) -> str:
    """Вернуть тип блюда по логическому признаку."""
    if is_main_dish:
        return "основное блюдо"
    return "дополнительное блюдо"


def get_total_ingredients(dish: dict, guests: int) -> dict[str, int]:
    """Рассчитать все ингредиенты для блюда."""
    ingredients = {}

    for name, grams in dish["ingredients"].items():
        ingredients[name] = get_ingredient_amount(guests, grams)

    return ingredients
