def find_event(events: list[dict], event_name: str) -> dict | None:
    """Найти событие по названию."""
    for event in events:
        if event["name"].lower() == event_name.lower():
            return event
    return None


def add_dish_to_event(
    events: list[dict],
    event_name: str,
    dish_name: str,
) -> bool:
    """Добавить блюдо в меню события."""
    event = find_event(events, event_name)

    if event is None:
        return False

    if dish_name not in event["menu"]:
        event["menu"].append(dish_name)

    return True


def remove_dish_from_event(
    events: list[dict],
    event_name: str,
    dish_name: str,
) -> bool:
    """Удалить блюдо из меню события."""
    event = find_event(events, event_name)

    if event is None or dish_name not in event["menu"]:
        return False

    event["menu"].remove(dish_name)
    return True


def is_dish_in_event(
    events: list[dict],
    event_name: str,
    dish_name: str,
) -> bool:
    """Проверить, есть ли блюдо в меню события."""
    event = find_event(events, event_name)

    if event is None:
        return False

    return dish_name in event["menu"]
