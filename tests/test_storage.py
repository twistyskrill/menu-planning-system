from pathlib import Path
from tempfile import TemporaryDirectory

from menu_planning.models import Dish, Ingredient, User
from menu_planning.storage import load_dishes, load_events, load_users


def test_load_events_creates_menu_with_dish_objects() -> None:
    with TemporaryDirectory() as directory:
        events_file = Path(directory) / "events.json"
        events_file.write_text(
            """
            [
              {
                "name": "День рождения",
                "date": "2026-09-20",
                "guests": 4,
                "user_id": 1,
                "menu": ["Овощной салат"]
              }
            ]
            """,
            encoding="utf-8",
        )
        dishes = [Dish("Овощной салат", "дополнительное блюдо", [])]
        users = [User(1, "Егор", "egor@example.com")]

        events = load_events(str(events_file), dishes, users)

        assert events[0].menu == [dishes[0]]
        assert events[0].user == users[0]


def test_load_dishes_uses_ingredients_from_json() -> None:
    with TemporaryDirectory() as directory:
        dishes_file = Path(directory) / "dishes.json"
        dishes_file.write_text(
            """
            [
              {
                "name": "Овощной салат",
                "type": "дополнительное блюдо",
                "ingredients": ["огурец"]
              }
            ]
            """,
            encoding="utf-8",
        )
        ingredients = [Ingredient("огурец", 200)]

        dishes = load_dishes(str(dishes_file), ingredients)

        assert dishes[0].ingredients == ingredients


def test_load_users() -> None:
    with TemporaryDirectory() as directory:
        users_file = Path(directory) / "users.json"
        users_file.write_text(
            """
            [
              {
                "id": 1,
                "name": "Егор",
                "email": "egor@example.com"
              }
            ]
            """,
            encoding="utf-8",
        )

        users = load_users(str(users_file))

        assert users[0].name == "Егор"
