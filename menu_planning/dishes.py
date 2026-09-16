def find_dish(dishes: list[dict], dish_name: str) -> dict | None:
    """Найти блюдо по названию."""
    for dish in dishes:
        if dish["name"].lower() == dish_name.lower():
            return dish
    return None


def get_dishes_by_type(dishes: list[dict], dish_type: str) -> list[dict]:
    """Вернуть блюда выбранного типа."""
    result = []

    for dish in dishes:
        if dish["type"].lower() == dish_type.lower():
            result.append(dish)

    return result


def sort_dishes_by_name(dishes: list[dict]) -> list[dict]:
    """Отсортировать блюда по названию."""
    return sorted(dishes, key=lambda dish: dish["name"])


def count_dishes_by_type(dishes: list[dict], dish_type: str) -> int:
    """Посчитать блюда выбранного типа."""
    count = 0

    for dish in dishes:
        if dish["type"].lower() == dish_type.lower():
            count += 1

    return count
