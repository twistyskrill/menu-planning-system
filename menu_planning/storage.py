import json
from pathlib import Path
from typing import Any

from menu_planning.dishes import find_dish
from menu_planning.models import Dish, Event, Ingredient


def load_json(path: str) -> list[dict[str, Any]]:
    """Загрузить данные из JSON-файла."""
    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return data
    return []


def save_json(path: str, data: list[dict[str, Any]]) -> None:
    """Сохранить данные в JSON-файл."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_dishes(path: str) -> list[Dish]:
    """Загрузить блюда из JSON-файла."""
    data = load_json(path)
    dishes = []

    for item in data:
        ingredients = []

        for name, grams in item["ingredients"].items():
            ingredients.append(Ingredient(name, grams))

        dishes.append(Dish(item["name"], item["type"], ingredients))

    return dishes


def load_events(path: str, dishes: list[Dish]) -> list[Event]:
    """Загрузить события из JSON-файла."""
    data = load_json(path)
    events = []

    for item in data:
        menu = []

        for dish_name in item["menu"]:
            dish = find_dish(dishes, dish_name)

            if dish is not None:
                menu.append(dish)

        events.append(
            Event(
                item["name"],
                item["date"],
                item["guests"],
                menu,
            )
        )

    return events


def save_events(path: str, events: list[Event]) -> None:
    """Сохранить события в JSON-файл."""
    data = []

    for event in events:
        data.append(event.to_data())

    save_json(path, data)


def save_dishes(path: str, dishes: list[Dish]) -> None:
    """Сохранить блюда в JSON-файл."""
    data = []

    for dish in dishes:
        data.append(dish.to_data())

    save_json(path, data)
