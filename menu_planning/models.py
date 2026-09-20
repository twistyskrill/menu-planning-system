class Ingredient:
    """Ингредиент блюда."""

    def __init__(self, name: str, grams_for_guest: int) -> None:
        self.name = name
        self.grams_for_guest = grams_for_guest

    def amount_for_guests(self, guests: int) -> int:
        """Рассчитать количество ингредиента для гостей."""
        return self.grams_for_guest * guests

    def __str__(self) -> str:
        return f"{self.name}: {self.grams_for_guest} г на гостя"


class Dish:
    """Блюдо праздничного меню."""

    def __init__(
        self,
        name: str,
        dish_type: str,
        ingredients: list[Ingredient],
    ) -> None:
        self.name = name
        self.dish_type = dish_type
        self.ingredients = ingredients

    def get_total_ingredients(self, guests: int) -> dict[str, int]:
        """Рассчитать ингредиенты блюда для указанного числа гостей."""
        result = {}

        for ingredient in self.ingredients:
            result[ingredient.name] = ingredient.amount_for_guests(guests)

        return result

    def to_data(self) -> dict:
        """Преобразовать блюдо в словарь для JSON."""
        ingredients = {}

        for ingredient in self.ingredients:
            ingredients[ingredient.name] = ingredient.grams_for_guest

        return {
            "name": self.name,
            "type": self.dish_type,
            "ingredients": ingredients,
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.dish_type})"


class Event:
    """Событие, для которого составляется меню."""

    def __init__(
        self,
        name: str,
        event_date: str,
        guests: int,
        menu: list[Dish],
    ) -> None:
        self.name = name
        self.event_date = event_date
        self.guests = guests
        self.menu = menu

    def has_dish(self, dish_name: str) -> bool:
        """Проверить, есть ли блюдо в меню."""
        for dish in self.menu:
            if dish.name == dish_name:
                return True
        return False

    def add_dish(self, dish: Dish) -> None:
        """Добавить блюдо в меню."""
        if not self.has_dish(dish.name):
            self.menu.append(dish)

    def remove_dish(self, dish_name: str) -> bool:
        """Удалить блюдо из меню."""
        for dish in self.menu:
            if dish.name == dish_name:
                self.menu.remove(dish)
                return True

        return False

    def to_data(self) -> dict:
        """Преобразовать событие в словарь для JSON."""
        return {
            "name": self.name,
            "date": self.event_date,
            "guests": self.guests,
            "menu": [dish.name for dish in self.menu],
        }

    def __str__(self) -> str:
        return f"{self.name}, дата: {self.event_date}, гостей: {self.guests}"
