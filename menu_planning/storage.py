import json
from pathlib import Path
from typing import Any

from menu_planning.dishes import find_dish
from menu_planning.models import Dish, Event, Ingredient, User
from menu_planning.users import find_user_by_id


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


def load_ingredients(path: str) -> list[Ingredient]:
    """Загрузить ингредиенты из JSON-файла."""
    data = load_json(path)
    ingredients = []

    for item in data:
        ingredients.append(Ingredient(item["name"], item["grams_for_guest"]))

    return ingredients


def find_ingredient(
    ingredients: list[Ingredient],
    ingredient_name: str,
) -> Ingredient | None:
    """Найти ингредиент по названию."""
    for ingredient in ingredients:
        if ingredient.name == ingredient_name:
            return ingredient

    return None


def load_users(path: str) -> list[User]:
    """Загрузить пользователей из JSON-файла."""
    data = load_json(path)
    users = []

    for item in data:
        users.append(User(item["id"], item["name"], item["email"]))

    return users


def load_dishes(
    path: str,
    ingredients_data: list[Ingredient] | None = None,
) -> list[Dish]:
    """Загрузить блюда из JSON-файла."""
    data = load_json(path)
    dishes = []

    for item in data:
        ingredients = []

        if isinstance(item["ingredients"], dict):
            for name, grams in item["ingredients"].items():
                ingredients.append(Ingredient(name, grams))
        else:
            for name in item["ingredients"]:
                ingredient = find_ingredient(ingredients_data or [], name)

                if ingredient is not None:
                    ingredients.append(ingredient)

        dishes.append(Dish(item["name"], item["type"], ingredients))

    return dishes


def load_events(
    path: str,
    dishes: list[Dish],
    users: list[User] | None = None,
) -> list[Event]:
    """Загрузить события из JSON-файла."""
    data = load_json(path)
    events = []

    for item in data:
        menu = []
        user = None

        if item.get("user_id") is not None:
            user = find_user_by_id(users or [], item["user_id"])

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
                user,
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


def save_users(path: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON-файл."""
    data = []

    for user in users:
        data.append(user.to_data())

    save_json(path, data)


def save_ingredients(path: str, ingredients: list[Ingredient]) -> None:
    """Сохранить ингредиенты в JSON-файл."""
    data = []

    for ingredient in ingredients:
        data.append(
            {
                "name": ingredient.name,
                "grams_for_guest": ingredient.grams_for_guest,
            }
        )

    save_json(path, data)
