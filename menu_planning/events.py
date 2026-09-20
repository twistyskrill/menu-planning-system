from menu_planning.dishes import find_dish
from menu_planning.models import Dish, Event


def find_event(events: list[Event], event_name: str) -> Event | None:
    """Найти событие по названию."""
    for event in events:
        if event.name.lower() == event_name.lower():
            return event
    return None


def add_dish_to_event(
    events: list[Event],
    dishes: list[Dish],
    event_name: str,
    dish_name: str,
) -> bool:
    """Добавить блюдо в меню события."""
    event = find_event(events, event_name)

    if event is None:
        return False

    dish = find_dish(dishes, dish_name)

    if dish is None:
        return False

    event.add_dish(dish)
    return True


def remove_dish_from_event(
    events: list[Event],
    event_name: str,
    dish_name: str,
) -> bool:
    """Удалить блюдо из меню события."""
    event = find_event(events, event_name)

    if event is None:
        return False

    return event.remove_dish(dish_name)


def is_dish_in_event(
    events: list[Event],
    event_name: str,
    dish_name: str,
) -> bool:
    """Проверить, есть ли блюдо в меню события."""
    event = find_event(events, event_name)

    if event is None:
        return False

    return event.has_dish(dish_name)
