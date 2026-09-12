from datetime import date


event = "День рождения"
event_date = date(2026, 9, 20)
dish = "Овощной салат"
ingredient = "Огурец"
guests = 4
grams_for_guest = 200
is_main_dish = False


def get_portions(guests):
    return guests


def get_ingredient_amount(portions, grams_for_guest):
    return portions * grams_for_guest


def get_dish_type(is_main_dish):
    if is_main_dish:
        return "основное блюдо"
    return "дополнительное блюдо"


portions = get_portions(guests)
total_grams = get_ingredient_amount(portions, grams_for_guest)
dish_type = get_dish_type(is_main_dish)
amount = str(total_grams) + " г"

print("Система планирования праздничного меню")
print(f"Событие: {event}")
print(f"Дата: {event_date}")
print(f"Блюдо: {dish}")
print(f"Тип блюда: {dish_type}")
print(f"Ингредиент: {ingredient}")
print(f"Количество гостей: {guests}")
print(f"Количество порций: {portions}")
print(f"Нужно ингредиента: {amount}")
