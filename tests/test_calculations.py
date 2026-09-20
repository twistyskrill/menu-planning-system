from menu_planning.calculations import (
    get_dish_type,
    get_ingredient_amount,
    get_portions,
    get_total_ingredients,
)
from menu_planning.models import Dish, Ingredient


def test_get_portions() -> None:
    assert get_portions(4) == 4


def test_get_ingredient_amount() -> None:
    assert get_ingredient_amount(4, 200) == 800


def test_get_dish_type() -> None:
    assert get_dish_type(False) == "дополнительное блюдо"


def test_get_total_ingredients() -> None:
    dish = Dish(
        "Овощной салат",
        "дополнительное блюдо",
        [
            Ingredient("огурец", 200),
            Ingredient("помидор", 150),
        ],
    )

    assert get_total_ingredients(dish, 4) == {"огурец": 800, "помидор": 600}


def test_dish_str() -> None:
    dish = Dish("Овощной салат", "дополнительное блюдо", [])

    assert str(dish) == "Овощной салат (дополнительное блюдо)"
