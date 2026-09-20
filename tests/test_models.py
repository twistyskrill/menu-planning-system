from menu_planning.models import Dish, Event, Ingredient


def test_ingredient_amount_for_guests() -> None:
    ingredient = Ingredient("огурец", 200)

    assert ingredient.amount_for_guests(4) == 800


def test_event_add_dish_without_duplicate() -> None:
    dish = Dish("Овощной салат", "дополнительное блюдо", [])
    event = Event("День рождения", "2026-09-20", 4, [dish])

    event.add_dish(dish)

    assert event.menu == [dish]
