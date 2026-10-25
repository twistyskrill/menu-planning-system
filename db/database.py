"""Подключение SQLite без Django ORM."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data/menu.sqlite"


@contextmanager
def connect(path=None):
    """Открыть соединение и гарантированно закрыть его после работы."""
    conn = sqlite3.connect(path or DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def initialize(path=None):
    """Создать таблицы; повторное выполнение не удаляет данные."""
    with connect(path) as conn:
        conn.executescript(
            (BASE_DIR / "sql/schema.sql").read_text(encoding="utf-8")
        )
        conn.commit()


def query(name):
    """Получить именованный запрос из единого SQL-каталога."""
    source = (BASE_DIR / "sql/queries.sql").read_text(encoding="utf-8")
    for block in source.split("-- name: ")[1:]:
        title, sql = block.split("\n", 1)
        if title.strip() == name:
            return sql.strip()
    raise KeyError(name)
