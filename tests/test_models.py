from menu_planning.models import Dish, Event, Ingredient, User


def test_ingredient_amount_for_guests() -> None:
    ingredient = Ingredient("огурец", 200)

    assert ingredient.amount_for_guests(4) == 800


def test_event_add_dish_without_duplicate() -> None:
    dish = Dish("Овощной салат", "дополнительное блюдо", [])
    event = Event("День рождения", "2026-09-20", 4, [dish])

    event.add_dish(dish)

    assert event.menu == [dish]


def test_event_stores_user_object() -> None:
    user = User(1, "Егор", "egor@example.com")
    event = Event("День рождения", "2026-09-20", 4, [], user)

    assert event.user == user
    assert event.to_data()["user_id"] == 1
