"""Перенос снимка JSON в SQLite: python -m db.import_json.

Повторный импорт полностью заменяет SQL-данные исходным снимком JSON.
Ошибки приводят к откату всей транзакции, исходные файлы не изменяются.
"""
import argparse
import json
from pathlib import Path

from db.database import BASE_DIR, DATABASE_PATH, connect, initialize


def import_json(data_dir=None, database_path=None):
    """Перенести сущности и связи с сохранением идентификаторов."""
    data_dir = Path(data_dir or BASE_DIR / "data")
    data = {}
    for name in ("users", "ingredients", "dishes", "events"):
        data[name] = json.loads(
            (data_dir / (name + ".json")).read_text(encoding="utf-8")
        )
    ingredients = {v["name"]: i for i, v in
                   enumerate(data["ingredients"], 1)}
    dishes = {v["name"]: v["id"] for v in data["dishes"]}
    norms = {v["name"]: v["grams_for_guest"] for v in data["ingredients"]}
    composition = []
    for dish in data["dishes"]:
        for name in dish["ingredients"]:
            grams = (dish["ingredients"][name]
                     if isinstance(dish["ingredients"], dict) else norms[name])
            composition.append((dish["id"], ingredients[name], grams))
    menus = [(event["id"], dishes[name]) for event in data["events"]
             for name in event["menu"]]
    initialize(database_path)
    with connect(database_path) as conn:
        try:
            conn.execute("BEGIN")
            for sql in (
                "DELETE FROM event_dishes", "DELETE FROM dish_ingredients",
                "DELETE FROM events", "DELETE FROM dishes",
                "DELETE FROM ingredients", "DELETE FROM users",
            ):
                conn.execute(sql)
            conn.executemany("INSERT INTO users VALUES (?, ?, ?)", [
                (v["id"], v["name"], v["email"]) for v in data["users"]])
            conn.executemany("INSERT INTO ingredients VALUES (?, ?, ?)", [
                (ingredients[v["name"]], v["name"], v["grams_for_guest"])
                for v in data["ingredients"]])
            conn.executemany("INSERT INTO dishes VALUES (?, ?, ?)", [
                (v["id"], v["name"], v["type"]) for v in data["dishes"]])
            conn.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?)", [
                (v["id"], v["name"], v["date"], v["guests"], v.get("user_id"))
                for v in data["events"]])
            conn.executemany(
                "INSERT INTO dish_ingredients VALUES (?, ?, ?)", composition)
            conn.executemany("INSERT INTO event_dishes VALUES (?, ?)", menus)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    return {name: len(rows) for name, rows in data.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=BASE_DIR / "data")
    parser.add_argument("--database", type=Path, default=DATABASE_PATH)
    args = parser.parse_args()
    print(import_json(args.data_dir, args.database))
