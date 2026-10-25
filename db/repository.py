"""Преобразование строк SQLite в сохранённую предметную модель ПР1–ПР6."""
from django.conf import settings

from db.database import connect, query
from menu_planning.models import Dish, Event, Ingredient, User


def fetch(name, parameters=()):
    with connect(getattr(settings, "MENU_DATABASE", None)) as conn:
        return conn.execute(query(name), parameters).fetchall()


def load_dishes(rows=None):
    if rows is None:
        rows = fetch("dishes")
    ingredients = {}
    for row in fetch("composition"):
        ingredients.setdefault(row["dish_id"], []).append(
            Ingredient(row["name"], row["grams_for_guest"]))
    return [Dish(r["name"], r["dish_type"], ingredients.get(r["id"], []),
                 r["id"]) for r in rows]


def load_events(rows=None):
    if rows is None:
        rows = fetch("events")
    dishes = {d.dish_id: d for d in load_dishes()}
    menus = {}
    for row in fetch("menus"):
        menus.setdefault(row["event_id"], []).append(dishes[row["dish_id"]])
    return [Event(
        r["name"], r["event_date"], r["guests"], menus.get(r["id"], []),
        User(r["user_id"], r["user_name"], r["email"])
        if r["user_id"] is not None else None, r["id"],
    ) for r in rows]
