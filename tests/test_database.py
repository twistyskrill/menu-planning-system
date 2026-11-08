"""Проверки переноса, связей, SQL и сквозного отображения данных ПР7."""
import json
import shutil
import sqlite3

import pytest

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import Client

from db.database import BASE_DIR, connect
from db.import_json import import_json
from dishes.models import Dish, DishIngredient, Ingredient
from events.models import Event, EventDish, Organizer


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "menu.sqlite"
    import_json(database_path=path)
    return path


def test_import_counts_and_repeat(database):
    import_json(database_path=database)
    with connect(database) as conn:
        for table, expected in [("users", 2), ("ingredients", 17),
                                ("dishes", 6), ("events", 3),
                                ("dish_ingredients", 19), ("event_dishes", 9)]:
            # Имена таблиц фиксированы тестом, не получены от пользователя.
            assert conn.execute(
                "SELECT COUNT(*) FROM " + table).fetchone()[0] == expected
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_invalid_import_rolls_back(database, tmp_path):
    source = tmp_path / "source"
    shutil.copytree(BASE_DIR / "data", source, ignore=shutil.ignore_patterns(
        "*.sqlite", "*.sqlite-*"))
    events = json.loads((source / "events.json").read_text(encoding="utf-8"))
    events[0]["user_id"] = 999
    (source / "events.json").write_text(json.dumps(events), encoding="utf-8")
    with pytest.raises(sqlite3.IntegrityError):
        import_json(source, database)
    with connect(database) as conn:
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 3
        assert conn.execute("SELECT user_id FROM events WHERE id=1").fetchone()[0] == 1  # noqa: E501


def test_optional_organizer(seeded_orm):
    Organizer.objects.get(pk=1).delete()
    content = Client().get("/events/1/").content.decode()
    assert "не указан" in content
    assert "огурец — 800 г" in content


def test_filters_and_injection(seeded_orm):
    client = Client()
    content = client.get("/dishes/", {"type": "десерт"}).content.decode()
    assert "Фруктовый десерт" in content
    assert "Овощной салат" not in content
    content = client.get("/dishes/", {"q": "' OR 1=1 --"}).content.decode()
    assert "Блюда не найдены." in content
    content = client.get("/events/", {"date": "2026-12-31"}).content.decode()
    assert "Новый год" in content and "День рождения" not in content
    content = client.get("/events/", {"min_guests": "6"}).content.decode()
    assert "Новый год" in content and "Семейный ужин" not in content


def test_available_and_statistics(seeded_orm):
    client = Client()
    content = client.get("/dishes/available/", {"date": "2026-09-20"}).content.decode()  # noqa: E501
    assert "Овощной салат" not in content
    assert "Запеченная курица" not in content
    assert "Фруктовый десерт" in content
    Dish.objects.create(name="Новое", dish_type="десерт")
    assert "Новое" in client.get("/dishes/").content.decode()
    content = client.get("/events/statistics/").content.decode()
    assert "Всего гостей: 17" in content and "Новое" in content
    assert "Статистика" in content


@pytest.mark.parametrize("url", [
    "/events/?date=oops", "/events/?min_guests=-1",
    "/events/?min_guests=999999999999999999999999999999",
    "/dishes/available/?date=2026-99-99",
    "/dishes/available/?date=2026-09-20&page=oops",
])
def test_invalid_filters(seeded_orm, url):
    assert Client().get(url).status_code == 400


def test_all_queries_in_empty_database(empty_orm):
    client = Client()
    for url in ["/dishes/", "/events/", "/events/statistics/",
                "/dishes/available/?date=2026-09-20"]:
        assert client.get(url).status_code == 200
    assert client.get("/events/1/").status_code == 404
    content = client.get("/events/statistics/").content.decode()
    assert "Всего гостей: 0" in content


def test_available_pagination(seeded_orm):
    Dish.objects.bulk_create([
        Dish(name=f"Блюдо {i}", dish_type="десерт") for i in range(7, 22)
    ])
    client = Client()
    first = client.get("/dishes/available/?date=2026-01-01").content.decode()
    second = client.get(
        "/dishes/available/?date=2026-01-01&page=2"
    ).content.decode()
    assert "Овощной салат" in first and "Далее" in first
    assert "Овощной салат" not in second and "Назад" in second


def test_orm_import_counts_and_repeat(seeded_orm):
    call_command("import_pr7")
    for model, expected in [(Organizer, 2), (Ingredient, 17), (Dish, 6),
                            (Event, 3), (DishIngredient, 19), (EventDish, 9)]:
        assert model.objects.count() == expected
    event = Event.objects.get(pk=1)
    assert event.user.events.filter(pk=1).exists()
    assert event.menu.filter(pk=1).exists()


def test_orm_import_does_not_overwrite_conflicts(empty_orm):
    Dish.objects.create(pk=1, name="Свое блюдо", dish_type="десерт")
    with pytest.raises(CommandError, match="dishes, id=1"):
        call_command("import_pr7")
    assert Dish.objects.get(pk=1).name == "Свое блюдо"
    assert not Organizer.objects.exists()


def test_search_sort_and_pagination_together(seeded_orm):
    Event.objects.bulk_create([
        Event(name=f"Праздник {i}", event_date="2026-09-20", guests=i)
        for i in range(1, 13)
    ])
    params = {"date": "2026-09-20", "q": "Праздник", "sort": "guests"}
    first = Client().get("/events/", params)
    content = first.content.decode()
    assert "Праздник 12" in content and "Праздник 1<" not in content
    assert "sort=guests&amp;page=2" in content
    content = Client().get("/events/", {**params, "page": 2}).content.decode()
    assert "Праздник 1<" in content and "Праздник 12" not in content
