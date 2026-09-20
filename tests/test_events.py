from menu_planning.events import (
    add_dish_to_event,
    is_dish_in_event,
    remove_dish_from_event,
)
from menu_planning.models import Dish, Event


def make_dish() -> Dish:
    return Dish("Овощной салат", "дополнительное блюдо", [])


def test_add_dish_to_event() -> None:
    events = [Event("День рождения", "2026-09-20", 4, [])]
    dishes = [make_dish()]

    result = add_dish_to_event(events, dishes, "День рождения", "Овощной салат")

    assert result is True
    assert events[0].menu == [dishes[0]]


def test_remove_dish_from_event() -> None:
    events = [Event("День рождения", "2026-09-20", 4, [make_dish()])]

    result = remove_dish_from_event(events, "День рождения", "Овощной салат")

    assert result is True
    assert events[0].menu == []


def test_is_dish_in_event() -> None:
    events = [Event("День рождения", "2026-09-20", 4, [make_dish()])]

    assert is_dish_in_event(events, "День рождения", "Овощной салат") is True


def test_event_str() -> None:
    event = Event("День рождения", "2026-09-20", 4, [])

    assert str(event) == "День рождения, дата: 2026-09-20, гостей: 4"
