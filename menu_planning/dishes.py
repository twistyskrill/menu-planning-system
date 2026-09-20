from menu_planning.models import Dish


def find_dish(dishes: list[Dish], dish_name: str) -> Dish | None:
    """Найти блюдо по названию."""
    for dish in dishes:
        if dish.name.lower() == dish_name.lower():
            return dish
    return None


def get_dishes_by_type(dishes: list[Dish], dish_type: str) -> list[Dish]:
    """Вернуть блюда выбранного типа."""
    result = []

    for dish in dishes:
        if dish.dish_type.lower() == dish_type.lower():
            result.append(dish)

    return result


def sort_dishes_by_name(dishes: list[Dish]) -> list[Dish]:
    """Отсортировать блюда по названию."""
    return sorted(dishes, key=lambda dish: dish.name)


def count_dishes_by_type(dishes: list[Dish], dish_type: str) -> int:
    """Посчитать блюда выбранного типа."""
    count = 0

    for dish in dishes:
        if dish.dish_type.lower() == dish_type.lower():
            count += 1

    return count
