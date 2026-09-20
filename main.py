from menu_planning.calculations import get_total_ingredients
from menu_planning.dishes import (
    count_dishes_by_type,
    find_dish,
    sort_dishes_by_name,
)
from menu_planning.events import (
    add_dish_to_event,
    find_event,
    is_dish_in_event,
    remove_dish_from_event,
)
from menu_planning.models import Dish, Event
from menu_planning.storage import load_dishes, load_events, save_events
from menu_planning.utils import input_int


EVENTS_PATH = "data/events.json"
DISHES_PATH = "data/dishes.json"


def show_actions() -> None:
    """Вывести список действий."""
    print("\n=== Система планирования праздничного меню ===")
    print("1. Показать события")
    print("2. Показать блюда")
    print("3. Найти блюдо по названию")
    print("4. Проверить блюдо в меню события")
    print("5. Добавить блюдо в меню события")
    print("6. Удалить блюдо из меню события")
    print("7. Показать меню события")
    print("8. Выход")


def show_events(events: list[Event]) -> None:
    """Вывести список событий."""
    print("\nСобытия:")

    for event in events:
        print(f"- {event}")


def show_event_menu(event: Event) -> None:
    """Вывести меню события с расчетом ингредиентов."""
    print()
    print(f"Событие: {event.name}")
    print(f"Дата: {event.event_date}")
    print(f"Количество гостей: {event.guests}")
    print("Меню:")

    for dish in event.menu:
        print(f"- {dish}")
        ingredients = get_total_ingredients(dish, event.guests)

        for name, grams in ingredients.items():
            print(f"  {name}: {grams} г")


def show_sorted_dishes(dishes: list[Dish]) -> None:
    """Вывести блюда, отсортированные по названию."""
    print("\nБлюда по алфавиту:")

    for dish in sort_dishes_by_name(dishes):
        print(f"- {dish.name}")


def show_found_dish(dishes: list[Dish]) -> None:
    """Найти и вывести блюдо."""
    dish_name = input("Название блюда: ")
    dish = find_dish(dishes, dish_name)

    if dish is None:
        print("Блюдо не найдено.")
        return

    print(f"Блюдо: {dish.name}")
    print(f"Тип: {dish.dish_type}")
    print("Ингредиенты:")

    for ingredient in dish.ingredients:
        print(f"- {ingredient}")


def check_dish_in_menu(events: list[Event]) -> None:
    """Проверить наличие блюда в меню события."""
    event_name = input("Название события: ")
    dish_name = input("Название блюда: ")

    if is_dish_in_event(events, event_name, dish_name):
        print("Блюдо уже есть в меню события.")
    else:
        print("Блюда нет в меню события.")


def add_dish(events: list[Event], dishes: list[Dish]) -> None:
    """Добавить блюдо в меню события."""
    event_name = input("Название события: ")
    dish_name = input("Название блюда: ")

    if find_dish(dishes, dish_name) is None:
        print("Такого блюда нет в списке блюд.")
        return

    if add_dish_to_event(events, dishes, event_name, dish_name):
        save_events(EVENTS_PATH, events)
        print("Блюдо добавлено в меню события.")
    else:
        print("Событие не найдено.")


def remove_dish(events: list[Event]) -> None:
    """Удалить блюдо из меню события."""
    event_name = input("Название события: ")
    dish_name = input("Название блюда: ")

    if remove_dish_from_event(events, event_name, dish_name):
        save_events(EVENTS_PATH, events)
        print("Блюдо удалено из меню события.")
    else:
        print("Событие или блюдо не найдено.")


def show_event_menu_by_name(events: list[Event]) -> None:
    """Вывести меню события по названию."""
    event_name = input("Название события: ")
    event = find_event(events, event_name)

    if event is None:
        print("Событие не найдено.")
        return

    show_event_menu(event)


def show_statistics(dishes: list[Dish]) -> None:
    """Вывести простую статистику по блюдам."""
    main_count = count_dishes_by_type(dishes, "основное блюдо")
    extra_count = count_dishes_by_type(dishes, "дополнительное блюдо")
    dessert_count = count_dishes_by_type(dishes, "десерт")

    print("\nСтатистика:")
    print(f"Всего блюд: {len(dishes)}")
    print(f"Основных блюд: {main_count}")
    print(f"Дополнительных блюд: {extra_count}")
    print(f"Десертов: {dessert_count}")


def main() -> None:
    """Запустить сценарий планирования меню."""
    dishes = load_dishes(DISHES_PATH)
    events = load_events(EVENTS_PATH, dishes)

    while True:
        show_actions()
        action = input_int("Выберите действие: ")

        if action == 1:
            show_events(events)
        elif action == 2:
            show_sorted_dishes(dishes)
            show_statistics(dishes)
        elif action == 3:
            show_found_dish(dishes)
        elif action == 4:
            check_dish_in_menu(events)
        elif action == 5:
            add_dish(events, dishes)
        elif action == 6:
            remove_dish(events)
        elif action == 7:
            show_event_menu_by_name(events)
        elif action == 8:
            print("Работа программы завершена.")
            break
        else:
            print("Такого пункта меню нет.")


if __name__ == "__main__":
    main()
