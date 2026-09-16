from menu_planning.events import (
    add_dish_to_event,
    is_dish_in_event,
    remove_dish_from_event,
)


def test_add_dish_to_event() -> None:
    events = [{"name": "День рождения", "menu": []}]

    result = add_dish_to_event(events, "День рождения", "Овощной салат")

    assert result is True
    assert events[0]["menu"] == ["Овощной салат"]


def test_remove_dish_from_event() -> None:
    events = [{"name": "День рождения", "menu": ["Овощной салат"]}]

    result = remove_dish_from_event(events, "День рождения", "Овощной салат")

    assert result is True
    assert events[0]["menu"] == []


def test_is_dish_in_event() -> None:
    events = [{"name": "День рождения", "menu": ["Овощной салат"]}]

    assert is_dish_in_event(events, "День рождения", "Овощной салат") is True
