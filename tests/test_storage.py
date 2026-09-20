from pathlib import Path
from tempfile import TemporaryDirectory

from menu_planning.models import Dish
from menu_planning.storage import load_events


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
                "menu": ["Овощной салат"]
              }
            ]
            """,
            encoding="utf-8",
        )
        dishes = [Dish("Овощной салат", "дополнительное блюдо", [])]

        events = load_events(str(events_file), dishes)

        assert events[0].menu == [dishes[0]]
