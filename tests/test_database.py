"""Проверки переноса, связей, SQL и сквозного отображения данных ПР7."""
import json
import os
import shutil
import sqlite3

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menu_project.settings")
django.setup()

from django.test import Client, override_settings  # noqa: E402
from db.database import BASE_DIR, connect, initialize, query  # noqa: E402
from db.import_json import import_json  # noqa: E402


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "menu.sqlite"
    import_json(database_path=path)
    with override_settings(MENU_DATABASE=path):
        yield path


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


def test_constraints_and_optional_user(database):
    with connect(database) as conn:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO event_dishes VALUES (?, ?)", (1, 999))
        conn.execute("DELETE FROM users WHERE id = ?", (1,))
        conn.commit()
    content = Client().get("/events/1/").content.decode()
    assert "не указан" in content
    assert "огурец — 800 г" in content


def test_filters_and_injection(database):
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


def test_available_and_statistics(database):
    client = Client()
    content = client.get("/dishes/available/", {"date": "2026-09-20"}).content.decode()  # noqa: E501
    assert "Овощной салат" not in content
    assert "Запеченная курица" not in content
    assert "Фруктовый десерт" in content
    with connect(database) as conn:
        assert conn.execute(query("event_totals")).fetchone()["guests"] == 17
        assert len(conn.execute(query("frequent"), (2,)).fetchall()) == 3
        conn.execute("INSERT INTO dishes VALUES (?, ?, ?)", (7, "Новое", "десерт"))  # noqa: E501
        conn.commit()
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
def test_invalid_filters(database, url):
    assert Client().get(url).status_code == 400


def test_all_queries_in_empty_database(tmp_path):
    path = tmp_path / "empty.sqlite"
    initialize(path)
    with override_settings(MENU_DATABASE=path):
        client = Client()
        for url in ["/dishes/", "/events/", "/events/statistics/",
                    "/dishes/available/?date=2026-09-20"]:
            assert client.get(url).status_code == 200
        assert client.get("/events/1/").status_code == 404
        content = client.get("/events/statistics/").content.decode()
        assert "Всего гостей: 0" in content


def test_available_pagination(database):
    with connect(database) as conn:
        conn.executemany("INSERT INTO dishes VALUES (?, ?, ?)", [
            (i, "Блюдо " + str(i), "десерт") for i in range(7, 22)])
        conn.commit()
    client = Client()
    first = client.get("/dishes/available/?date=2026-01-01").content.decode()
    second = client.get("/dishes/available/?date=2026-01-01&page=2").content.decode()  # noqa: E501
    assert "Овощной салат" in first and "Далее" in first
    assert "Овощной салат" not in second and "Назад" in second
